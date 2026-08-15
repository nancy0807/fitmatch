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

# Hand-picked ease assumptions (cm) per fit rating, per region.
# This is the part a v2 model would learn from real data instead.
EASE_CM = {
    "tight": {"chest": 2, "shoulder": 0.5, "length": -1},
    "true":  {"chest": 6, "shoulder": 1.5, "length": 1},
    "loose": {"chest": 10, "shoulder": 2.5, "length": 3},
}

REGION_WEIGHTS = {"chest": 0.5, "shoulder": 0.35, "length": 0.15}


def load_size_charts():
    with open(DATA_PATH) as f:
        return json.load(f)


def estimate_body_measurements(owned_items, charts):
    """
    owned_items: list of dicts like
        {"brand": "H&M", "size": "M", "fit": "true"}
    Returns estimated body measurements dict, e.g. {"chest": 85.3, ...}
    and the user's average preferred ease per region (for re-applying later).
    """
    region_estimates = {"chest": [], "shoulder": [], "length": []}
    ease_used = {"chest": [], "shoulder": [], "length": []}

    for item in owned_items:
        brand_chart = charts["brands"].get(item["brand"])
        if not brand_chart:
            continue
        size_data = brand_chart["sizes"].get(item["size"])
        if not size_data:
            continue
        fit_rating = item.get("fit", "true")
        ease = EASE_CM.get(fit_rating, EASE_CM["true"])

        for region in ("chest", "shoulder", "length"):
            garment_measure = size_data[region]
            body_estimate = garment_measure - ease[region]
            region_estimates[region].append(body_estimate)
            ease_used[region].append(ease[region])

    def avg(lst):
        return sum(lst) / len(lst) if lst else None

    body = {r: avg(v) for r, v in region_estimates.items()}
    preferred_ease = {r: avg(v) for r, v in ease_used.items()}
    return body, preferred_ease


def predict_size(target_brand, body_estimate, preferred_ease, charts):
    """
    Returns (predicted_size, confidence_note, scored_sizes)
    """
    brand_chart = charts["brands"].get(target_brand)
    if not brand_chart:
        return None, f"No size chart on file for {target_brand}.", []

    scored = []
    for size, measures in brand_chart["sizes"].items():
        error = 0
        regions_used = 0
        for region, weight in REGION_WEIGHTS.items():
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
    if best_error < 1.5:
        confidence = "high"
    elif best_error < 3.5:
        confidence = "medium"
    else:
        confidence = "low — fit history is thin or this brand's cut is unusual for you"

    return best_size, confidence, scored
