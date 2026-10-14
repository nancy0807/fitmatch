"""
Tests for matching.py — the core fit-prediction engine.

These aren't invented coverage. Every test here reflects a scenario that
was actually run and verified by hand during development, most of them
after finding a real bug (see the measurement-type crash test below).
Written as plain pytest functions with plain asserts so they read without
pytest experience.

Since v8 every real brand publishes (or is converted to) body measurements,
so no real chart is garment_flat any more. The engine still supports both
types and must still keep them apart; those tests use one clearly labelled
SYNTHETIC garment chart (see mixed_charts) rather than a real brand.
"""

import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import matching


def load_charts():
    """The women's slice."""
    return matching.charts_for_gender("women")


def load_mens_charts():
    return matching.charts_for_gender("men")


def mixed_charts():
    """
    The women's slice plus ONE synthetic garment_flat brand, used only to test
    that the two measurement types are kept apart. Not real data and never
    shown in the app.
    """
    charts = copy.deepcopy(load_charts())
    charts["brands"]["Synthetic Garment Co"] = {
        "measurement_type": "garment_flat",
        "measurement_fields": ["chest", "shoulder", "length"],
        "_source": "SYNTHETIC test data, not a real brand.",
        "sizes": {
            "S": {"chest": 46, "shoulder": 37, "length": 64},
            "M": {"chest": 49, "shoulder": 38.5, "length": 66},
            "L": {"chest": 52, "shoulder": 40, "length": 68},
        },
    }
    return charts


def run(owned, target, charts, **kwargs):
    body, ease, counts = matching.estimate_body_measurements(owned, charts)
    return matching.predict_size(target, body, ease, charts, count_by_type=counts, **kwargs)


def test_estimate_body_measurements_single_body_item():
    """Westside women's M, fit 'true' -> chart minus 3 cm ease, verified by hand."""
    charts = load_charts()
    owned = [{"brand": "Westside", "size": "M", "fit": "true"}]
    body, ease, counts = matching.estimate_body_measurements(owned, charts)

    assert counts == {"body_circumference": 1}
    assert body["body_circumference"] == {"bust": 89, "waist": 71, "hip": 96}


def test_same_type_prediction_does_not_crash():
    size, confidence, scored = run([{"brand": "Westside", "size": "M", "fit": "true"}], "H&M", load_charts())
    assert size is not None
    assert len(scored) > 0


def test_thin_data_confidence_is_downgraded():
    """With only 1 owned item, confidence should never read 'high'."""
    size, confidence, scored = run([{"brand": "Westside", "size": "M", "fit": "true"}], "H&M", load_charts())
    assert "high" not in confidence
    assert "only 1 owned item" in confidence


def test_cross_measurement_type_does_not_crash():
    """
    The real bug this project hit: predicting a garment_flat brand from
    body_circumference fit history used to raise a KeyError. It must fail
    gracefully instead of crashing.
    """
    size, confidence, scored = run([{"brand": "Westside", "size": "M", "fit": "true"}],
                                   "Synthetic Garment Co", mixed_charts())
    assert size is None
    assert "No fit history yet" in confidence
    assert scored == []


def test_cross_measurement_type_reversed_does_not_crash():
    """Same bug, opposite direction: garment_flat history -> body_circumference target."""
    size, confidence, scored = run([{"brand": "Synthetic Garment Co", "size": "M", "fit": "true"}],
                                   "Westside", mixed_charts())
    assert size is None
    assert "No fit history yet" in confidence


def test_mixed_owned_items_only_uses_matching_type():
    """A user with items of BOTH types: each prediction uses only its own type."""
    charts = mixed_charts()
    owned = [
        {"brand": "Synthetic Garment Co", "size": "M", "fit": "true"},
        {"brand": "Westside", "size": "M", "fit": "true"},
    ]
    body, ease, counts = matching.estimate_body_measurements(owned, charts)
    assert counts == {"garment_flat": 1, "body_circumference": 1}
    assert matching.predict_size("Synthetic Garment Co", body, ease, charts, count_by_type=counts)[0] is not None
    assert matching.predict_size("Westside", body, ease, charts, count_by_type=counts)[0] is not None


def test_single_item_fit_rating_has_no_effect_documented_quirk():
    """
    KNOWN, DOCUMENTED LIMITATION (see failure-modes.md): with exactly one
    owned item, the tight/true/loose rating cancels out mathematically and
    has zero effect on the prediction. This test locks in that this is the
    CURRENT actual behavior, so a future fix will make this test fail on
    purpose, as a reminder to update failure-modes.md when it's addressed.
    """
    charts = load_charts()
    _, _, scored_tight = run([{"brand": "Westside", "size": "M", "fit": "tight"}], "Nike", charts)
    _, _, scored_loose = run([{"brand": "Westside", "size": "M", "fit": "loose"}], "Nike", charts)
    assert scored_tight == scored_loose


def test_unknown_target_brand():
    size, confidence, scored = run([{"brand": "Westside", "size": "M", "fit": "true"}], "NotARealBrand", load_charts())
    assert size is None
    assert "No size chart on file" in confidence


# ---- scoring: weighted average over the measurements actually compared ----

def test_a_chest_only_chart_scores_the_plain_chest_distance():
    """
    The Souled Store men's chart lists chest only. Its score must be the plain
    chest distance in cm, not half of it (chest's weight is 0.5): before the
    normalisation, one-measurement charts looked twice as good as they were.
    """
    charts = load_mens_charts()
    owned = [{"brand": "Adidas", "size": "M", "fit": "true"}]
    body, ease, counts = matching.estimate_body_measurements(owned, charts)
    _, _, scored = matching.predict_size("The Souled Store", body, ease, charts, count_by_type=counts)

    target_chest = body["body_circumference"]["chest"] + ease["body_circumference"]["chest"]
    chart = charts["brands"]["The Souled Store"]["sizes"]
    for size, score in scored:
        assert abs(score - abs(chart[size]["chest"] - target_chest)) < 1e-9


def test_scores_for_full_charts_are_unchanged_by_the_normalisation():
    """Body weights sum to 1.0, so a chart with chest, waist and hip divides by 1: same scores as before."""
    charts = load_mens_charts()
    owned = [{"brand": "Adidas", "size": "M", "fit": "true"}]
    body, ease, counts = matching.estimate_body_measurements(owned, charts)
    _, _, scored = matching.predict_size("Nike", body, ease, charts, count_by_type=counts)
    w = matching.REGION_WEIGHTS["body_circumference"]
    nike = charts["brands"]["Nike"]["sizes"]
    for size, score in scored:
        raw = sum(w[r] * abs(nike[size][r] - (body["body_circumference"][r] + ease["body_circumference"][r]))
                  for r in ("chest", "waist", "hip"))
        assert abs(score - raw) < 1e-9


# ---- men's slice ----

def test_mens_prediction_works_across_brands():
    """Men's charts use 'chest' instead of 'bust'; the same engine must handle them."""
    charts = load_mens_charts()
    owned = [{"brand": "Adidas", "size": "M", "fit": "true"}, {"brand": "Nike", "size": "M", "fit": "true"}]
    body, ease, counts = matching.estimate_body_measurements(owned, charts)
    size, confidence, scored = matching.predict_size("Levi's", body, ease, charts, count_by_type=counts)

    assert counts == {"body_circumference": 2}
    assert "chest" in body["body_circumference"]
    assert size == "M"


def test_mens_chest_actually_drives_the_prediction():
    """A much bigger chest in the owned item must give a bigger predicted size."""
    charts = load_mens_charts()

    def predict_from(owned_size):
        return run([{"brand": "Nike", "size": owned_size, "fit": "true"}], "Adidas", charts)[0]

    small, large = predict_from("S"), predict_from("XL")
    assert matching.SIZE_ORDER.index(large) > matching.SIZE_ORDER.index(small)


# ---- cut guardrail ----

def test_oversized_and_slim_items_are_set_aside_with_a_reason():
    charts = load_charts()
    items = [
        {"brand": "H&M", "size": "M", "fit": "true", "cut": "regular"},
        {"brand": "H&M", "size": "XS", "fit": "loose", "cut": "oversized"},
        {"brand": "Nike", "size": "S", "fit": "true", "cut": "slim"},
    ]
    usable, set_aside = matching.split_usable_items(items, charts)

    assert [i["size"] for i in usable] == ["M"]
    assert [(i["brand"], why) for i, why in set_aside] == [("H&M", "special_cut"), ("Nike", "special_cut")]


def test_an_item_without_a_cut_counts_as_regular():
    """Older callers never send 'cut'. They must keep working, not lose their items."""
    usable, set_aside = matching.split_usable_items([{"brand": "H&M", "size": "M", "fit": "true"}], load_charts())
    assert len(usable) == 1 and set_aside == []


def test_a_size_the_brand_does_not_make_is_set_aside_not_dropped():
    usable, set_aside = matching.split_usable_items([{"brand": "Lulu & Sky", "size": "XXL", "fit": "true"}], load_charts())
    assert usable == [] and set_aside[0][1] == "no_such_size"


def test_excluding_an_oversized_item_gives_the_same_answer_as_never_logging_it():
    """The point of the guardrail: the oversized XS can no longer drag the estimate down."""
    charts = load_charts()
    regular = [{"brand": "H&M", "size": "M", "fit": "true"}, {"brand": "Nike", "size": "M", "fit": "true"}]
    with_oversized = regular + [{"brand": "H&M", "size": "XS", "fit": "loose", "cut": "oversized"}]

    def go(items):
        usable, _ = matching.split_usable_items(items, charts)
        return run(usable, "Uniqlo", charts)

    assert go(with_oversized) == go(regular)


def test_without_the_guardrail_an_oversized_loose_xs_would_wreck_the_estimate():
    """Documents WHY the guardrail exists: the same item, used naively, shifts the prediction down."""
    charts = load_charts()
    regular = [{"brand": "H&M", "size": "M", "fit": "true"}]
    naive = regular + [{"brand": "H&M", "size": "XS", "fit": "loose"}]   # no cut recorded -> used as-is

    order = matching.SIZE_ORDER
    assert order.index(run(naive, "Westside", charts)[0]) < order.index(run(regular, "Westside", charts)[0])


# ---- target cut (the cut of the product being bought) ----

def _target_run(cut=None, charts=None, target="Nike"):
    charts = charts or load_mens_charts()
    owned = [{"brand": b, "size": "M", "fit": "true"} for b in ("Adidas", "Nike", "Levi's")]
    body, ease, counts = matching.estimate_body_measurements(owned, charts)
    kwargs = {} if cut is None else {"target_cut": cut}
    return matching.predict_size(target, body, ease, charts, count_by_type=counts,
                                 history_brands=["Adidas", "Nike", "Levi's"], **kwargs)


def test_target_cut_defaults_to_regular():
    """Existing callers never pass target_cut and must get exactly the old answer."""
    assert _target_run() == _target_run("regular")


def test_an_oversized_product_gets_a_smaller_size_and_slim_never_a_smaller_one():
    order = matching.SIZE_ORDER
    regular, oversized, slim = _target_run("regular")[0], _target_run("oversized")[0], _target_run("slim")[0]
    assert order.index(oversized) < order.index(regular)
    assert order.index(slim) >= order.index(regular)


def test_a_non_regular_target_cut_never_claims_high_confidence():
    """The adjustment is an assumption, so it must not produce 'high'."""
    assert _target_run("regular")[1] == "high"           # the baseline really is high ...
    assert _target_run("oversized")[1] == "medium"       # ... and the assumption caps it


def test_cut_room_table_covers_every_cut_and_regular_adds_nothing():
    assert set(matching.CUT_ROOM_CM) == set(matching.CUT_OPTIONS)
    assert matching.CUT_ROOM_CM["regular"] == 0


# ---- approximate charts (converted from garment measurements, e.g. Zara) ----

def _mark_approximate(brand):
    charts = copy.deepcopy(load_mens_charts())
    charts["brands"][brand]["approximate"] = True
    return charts


def test_an_approximate_target_chart_never_claims_high_confidence():
    """Same baseline as above (high), but with the target's chart marked approximate."""
    assert _target_run("regular")[1] == "high"
    assert _target_run("regular", charts=_mark_approximate("Nike"))[1] == "medium"


def test_an_approximate_chart_in_the_history_also_caps_confidence():
    """The body estimate itself rests on assumed numbers when a history brand is approximate."""
    assert _target_run("regular", charts=_mark_approximate("Levi's"))[1] == "medium"


def test_approximate_flag_does_not_change_the_predicted_size():
    """Only the confidence is capped; the maths is the same."""
    size, _, scored = _target_run("regular")
    size_a, _, scored_a = _target_run("regular", charts=_mark_approximate("Nike"))
    assert size == size_a and scored == scored_a


def test_zara_now_connects_to_real_brands():
    """Converted to body sizes, Zara can be predicted from real brands, with a capped confidence."""
    size, confidence, _ = _target_run("regular", target="Zara")
    assert size is not None
    assert "high" not in confidence
