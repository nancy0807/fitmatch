"""
Fit prediction engine — v1

CONCEPT: A user owns items from brands they've already worn. For each, they
rate how it fits (tight / true / loose) per body region. From that, we back
out an ESTIMATE of their actual body measurement (garment measurement minus
an "ease" allowance implied by the fit rating). Averaging across their owned
items gives a body-measurement estimate that's brand-independent.

To predict a size in a NEW brand, we don't just find the size closest to
their raw body estimate — we also account for how much ease they personally
prefer (some people like tees snug, some baggy). We find the size in the
new brand whose (garment measurement - preferred ease) is closest to their
estimated body measurement.

MEASUREMENT TYPES: not every brand measures the same way. Some publish flat
GARMENT measurements (chest/shoulder/length of the actual piece of fabric).
Others publish BODY CIRCUMFERENCE measurements (bust or chest, waist, hip — a
measurement of the body the size targets, not the garment itself). These are
different physical quantities, not just different units, so fit history from
one type can never be used to predict a size in the other. Estimates are kept
separate per measurement_type; if a user has no fit history in the target
brand's measurement system yet, we say so honestly instead of guessing.

GENDER: size charts are split into gender slices (see data/size_charts.json).
The engine itself never sees more than one slice at a time: the caller picks
a slice with charts_for_gender() and passes it in, so women's and men's fit
history are never mixed. The engine code is the same for both; the only
difference is region naming (women's body charts use "bust", men's use "chest").

WHY THIS COUNTS AS THE 'AI' PART (not just a database lookup):
A static size-chart lookup only works if the user already knows their exact
body measurements — most people don't. This engine instead learns a body
estimate FROM SUBJECTIVE FIT FEEDBACK across brands with different cuts,
which is a pattern-inference problem, not a direct lookup.

v2 UPGRADE PATH (documented for the case study, not built yet):
Once there's fit data from many users, this heuristic (fixed ease-per-rating)
should be replaced with a learned model — e.g. an embedding per brand/size
learned from aggregate fit outcomes, so ease assumptions aren't hand-picked
but inferred from real data. That's the difference between a v1 heuristic
and a real ML system, and it's worth being explicit about which one this is.
"""

import json
from pathlib import Path

DATA_PATH = Path(__file__).parent / "data" / "size_charts.json"

# Canonical size order, smallest to largest. Used to build the size dropdown
# and checked against the data so a typo'd size label can't silently vanish.
SIZE_ORDER = ["XXS", "XS", "S", "M", "L", "XL", "XXL", "3XL", "4XL"]

# Hand-picked ease assumptions (cm) per fit rating, per measurement type.
# This is the part a v2 model would learn from real data instead.
# body_circumference ease is deliberately smaller than garment_flat ease:
# these numbers already describe the body a size targets, not a flat piece
# of fabric, so there's less gap to account for than a garment's total width.
# "bust" (women's charts) and "chest" (men's charts) are the same idea under
# the name each chart actually uses — every region a chart lists MUST have an
# entry in both tables below, or it would be silently ignored (tests check this).
EASE_CM = {
    "garment_flat": {
        "tight": {"chest": 2, "shoulder": 0.5, "length": -1},
        "true":  {"chest": 6, "shoulder": 1.5, "length": 1},
        "loose": {"chest": 10, "shoulder": 2.5, "length": 3},
    },
    "body_circumference": {
        "tight": {"bust": 1, "chest": 1, "waist": 1, "hip": 1},
        "true":  {"bust": 3, "chest": 3, "waist": 3, "hip": 3},
        "loose": {"bust": 6, "chest": 6, "waist": 6, "hip": 6},
    },
}

REGION_WEIGHTS = {
    "garment_flat": {"chest": 0.5, "shoulder": 0.35, "length": 0.15},
    "body_circumference": {"bust": 0.5, "chest": 0.5, "waist": 0.3, "hip": 0.2},
}


def load_size_charts():
    """Returns the whole file: {"genders": {"women": {...}, "men": {...}}}."""
    with open(DATA_PATH) as f:
        return json.load(f)


def charts_for_gender(gender, all_charts=None):
    """
    Returns one gender's slice as {"category": ..., "brands": {...}} — the
    shape estimate_body_measurements() and predict_size() expect.
    Raises KeyError for a gender that isn't in the data, rather than guessing.
    """
    if all_charts is None:
        all_charts = load_size_charts()
    genders = all_charts["genders"]
    if gender not in genders:
        raise KeyError(f"No size charts for gender {gender!r}. Available: {list(genders)}")
    return genders[gender]


# How an item is cut. Every size chart describes a REGULAR cut. An oversized tee in
# size XS can hang looser than a regular M, and a stretchy slim tee can measure
# smaller than the body that wears it, so such items would corrupt the body
# estimate (a user logging an oversized XS as "loose" would be read as a much
# smaller person). Until the engine can adjust for cut, those items are set
# aside and shown to the user — never silently dropped, never used.
# See failure-modes.md: "Cut varies per product, not per brand".
REGULAR_CUT = "regular"
CUT_OPTIONS = {"regular": "regular cut", "oversized": "oversized", "slim": "slim / stretchy"}


def split_usable_items(owned_items, charts):
    """
    Sort owned items into those the estimate can safely use and those it must
    set aside, with the reason. Never drops an item silently.

    Returns (usable, set_aside), where set_aside is a list of (item, reason)
    and reason is "no_such_size" (that brand doesn't make that size) or
    "special_cut" (oversized / slim — see above). An item with no "cut" key
    counts as a regular cut, so older callers keep working.
    """
    usable, set_aside = [], []
    for item in owned_items:
        sizes = charts["brands"].get(item["brand"], {}).get("sizes", {})
        if item["size"] not in sizes:
            set_aside.append((item, "no_such_size"))
        elif item.get("cut", REGULAR_CUT) != REGULAR_CUT:
            set_aside.append((item, "special_cut"))
        else:
            usable.append(item)
    return usable, set_aside


def estimate_body_measurements(owned_items, charts):
    """
    owned_items: list of dicts like
        {"brand": "H&M", "size": "M", "fit": "true"}
    charts: ONE gender slice, from charts_for_gender().

    A user's owned items may span BOTH measurement types (e.g. an H&M top
    and a Westside top). We keep a fully separate body estimate per type —
    never averaged together, since chest-width and bust-circumference are
    different physical quantities.

    Returns three dicts, each keyed by measurement_type
    ("garment_flat" / "body_circumference"):
      body_by_type   — {"garment_flat": {"chest": 85.3, ...}, ...}
      ease_by_type   — same shape, the user's average preferred ease
      count_by_type  — {"garment_flat": 3, "body_circumference": 1}
    """
    buckets = {}  # measurement_type -> {"region_estimates": {}, "ease_used": {}, "count": 0}

    for item in owned_items:
        brand_chart = charts["brands"].get(item["brand"])
        if not brand_chart:
            continue
        size_data = brand_chart["sizes"].get(item["size"])
        if not size_data:
            continue

        m_type = brand_chart.get("measurement_type", "garment_flat")
        fields = brand_chart.get("measurement_fields", [])
        fit_rating = item.get("fit", "true")
        ease_table = EASE_CM.get(m_type, EASE_CM["garment_flat"])
        ease = ease_table.get(fit_rating, ease_table["true"])

        bucket = buckets.setdefault(m_type, {"region_estimates": {}, "ease_used": {}, "count": 0})
        bucket["count"] += 1

        for region in fields:
            if region not in size_data:
                continue
            garment_measure = size_data[region]
            body_estimate = garment_measure - ease.get(region, 0)
            bucket["region_estimates"].setdefault(region, []).append(body_estimate)
            bucket["ease_used"].setdefault(region, []).append(ease.get(region, 0))

    def avg(lst):
        return sum(lst) / len(lst) if lst else None

    body_by_type = {}
    ease_by_type = {}
    count_by_type = {}
    for m_type, bucket in buckets.items():
        body_by_type[m_type] = {r: avg(v) for r, v in bucket["region_estimates"].items()}
        ease_by_type[m_type] = {r: avg(v) for r, v in bucket["ease_used"].items()}
        count_by_type[m_type] = bucket["count"]

    return body_by_type, ease_by_type, count_by_type


# Below this many owned items (of the SAME measurement type as the
# prediction target), the body estimate is too thin to trust, regardless
# of how tight the score gap looks. Matches the "add 3-5 owned items
# first" prompt in user-flows.md, so the code and the UX copy agree on
# what "enough" means.
MIN_ITEMS_FOR_FULL_CONFIDENCE = 3

# Confidence downgrades by one level when data is thin (see below).
CONFIDENCE_LEVELS = ["high", "medium", "low"]


def predict_size(target_brand, body_by_type, ease_by_type, charts, count_by_type):
    """
    body_by_type / ease_by_type / count_by_type: from estimate_body_measurements,
    keyed by measurement_type. We only ever use the slice matching the
    target brand's own measurement_type — a user's Westside fit history
    can never be used to predict an H&M size, and vice versa.
    charts: ONE gender slice, from charts_for_gender().

    Returns (predicted_size, confidence_note, scored_sizes)
    """
    brand_chart = charts["brands"].get(target_brand)
    if not brand_chart:
        return None, f"No size chart on file for {target_brand}.", []

    m_type = brand_chart.get("measurement_type", "garment_flat")
    item_count = count_by_type.get(m_type, 0)

    if item_count == 0:
        kind = "body-measurement (bust-or-chest/waist/hip)" if m_type == "body_circumference" else "garment-measurement (chest/shoulder/length)"
        return None, (
            f"No fit history yet in {kind} brands — {target_brand} uses this "
            f"measurement system. Log an item from a brand that uses it first."
        ), []

    body_estimate = body_by_type.get(m_type, {})
    preferred_ease = ease_by_type.get(m_type, {})
    weights = REGION_WEIGHTS.get(m_type, REGION_WEIGHTS["garment_flat"])
    fields = brand_chart.get("measurement_fields", list(weights.keys()))

    scored = []
    for size, measures in brand_chart["sizes"].items():
        error = 0
        regions_used = 0
        for region in fields:
            weight = weights.get(region, 0)
            if body_estimate.get(region) is None:
                continue
            target = body_estimate[region] + preferred_ease.get(region, 0)
            diff = abs(measures[region] - target)
            error += weight * diff
            regions_used += 1
        if regions_used > 0:
            scored.append((size, error))

    scored.sort(key=lambda x: x[1])
    if not scored:
        return None, "Not enough data to predict.", []

    best_size, best_error = scored[0]

    # Step 1: confidence from score gap alone, same as before.
    if best_error < 1.5:
        level = "high"
    elif best_error < 3.5:
        level = "medium"
    else:
        level = "low"

    # Step 2: downgrade one level if the underlying data is thin. A great
    # score match built on one owned item is still a guess dressed up as
    # a good score — this keeps that from reading as "high confidence".
    thin_data = item_count < MIN_ITEMS_FOR_FULL_CONFIDENCE
    if thin_data and level != "low":
        level = CONFIDENCE_LEVELS[CONFIDENCE_LEVELS.index(level) + 1]

    # Build the message last, once we know the final level and *why* we
    # landed there — thin data and a genuinely bad score match are different
    # problems and deserve different explanations.
    if level == "low" and thin_data:
        confidence = f"low — only {item_count} owned item(s) logged in this measurement system, not enough to be confident yet"
    elif level == "low":
        confidence = "low — fit history is thin or this brand's cut is unusual for you"
    else:
        confidence = level

    return best_size, confidence, scored
