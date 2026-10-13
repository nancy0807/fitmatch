"""
Tests for matching.py — the core fit-prediction engine.

These aren't invented coverage. Every test here reflects a scenario that
was actually run and verified by hand during development, most of them
after finding a real bug (see the measurement-type crash test below).
Written as plain pytest functions with plain asserts so they read without
pytest experience.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import matching


def load_charts():
    """The women's slice — what every test below was originally written against."""
    return matching.charts_for_gender("women")


def load_mens_charts():
    return matching.charts_for_gender("men")


def test_estimate_body_measurements_single_garment_flat_item():
    """H&M size M, fit 'true' -> known body estimate, verified by hand."""
    charts = load_charts()
    owned = [{"brand": "H&M", "size": "M", "fit": "true"}]
    body, ease, counts = matching.estimate_body_measurements(owned, charts)

    assert counts == {"garment_flat": 1}
    assert body["garment_flat"]["chest"] == 86.0
    assert body["garment_flat"]["length"] == 65.0
    assert body["garment_flat"]["shoulder"] == 37.0


def test_same_type_prediction_does_not_crash():
    """H&M (garment_flat) owned -> Zara (garment_flat) target: the basic case."""
    charts = load_charts()
    owned = [{"brand": "H&M", "size": "M", "fit": "true"}]
    body, ease, counts = matching.estimate_body_measurements(owned, charts)
    size, confidence, scored = matching.predict_size("Zara", body, ease, charts, count_by_type=counts)

    assert size is not None
    assert len(scored) > 0


def test_thin_data_confidence_is_downgraded():
    """With only 1 owned item, confidence should never read 'high'."""
    charts = load_charts()
    owned = [{"brand": "H&M", "size": "M", "fit": "true"}]
    body, ease, counts = matching.estimate_body_measurements(owned, charts)
    size, confidence, scored = matching.predict_size("Zara", body, ease, charts, count_by_type=counts)

    assert "high" not in confidence
    assert "only 1 owned item" in confidence


def test_cross_measurement_type_does_not_crash():
    """
    The real bug this project hit: predicting a garment_flat brand (Zara)
    using body_circumference fit history (Westside) used to raise a
    KeyError. It must now fail gracefully instead of crashing.
    """
    charts = load_charts()
    owned = [{"brand": "Westside", "size": "M", "fit": "true"}]
    body, ease, counts = matching.estimate_body_measurements(owned, charts)
    size, confidence, scored = matching.predict_size("Zara", body, ease, charts, count_by_type=counts)

    assert size is None
    assert "No fit history yet" in confidence
    assert scored == []


def test_cross_measurement_type_reversed_does_not_crash():
    """Same bug, opposite direction: garment_flat history -> body_circumference target."""
    charts = load_charts()
    owned = [{"brand": "H&M", "size": "M", "fit": "true"}]
    body, ease, counts = matching.estimate_body_measurements(owned, charts)
    size, confidence, scored = matching.predict_size("Westside", body, ease, charts, count_by_type=counts)

    assert size is None
    assert "No fit history yet" in confidence


def test_mixed_owned_items_only_uses_matching_type():
    """
    A user with BOTH garment_flat and body_circumference items owned should
    only have the matching-type items count toward a given prediction.
    """
    charts = load_charts()
    owned = [
        {"brand": "H&M", "size": "M", "fit": "true"},
        {"brand": "Westside", "size": "M", "fit": "true"},
    ]
    body, ease, counts = matching.estimate_body_measurements(owned, charts)

    assert counts == {"garment_flat": 1, "body_circumference": 1}

    size_zara, _, _ = matching.predict_size("Zara", body, ease, charts, count_by_type=counts)
    size_westside, _, _ = matching.predict_size("Westside", body, ease, charts, count_by_type=counts)

    assert size_zara is not None
    assert size_westside is not None


def test_single_item_fit_rating_has_no_effect_documented_quirk():
    """
    KNOWN, DOCUMENTED LIMITATION (see failure-modes.md): with exactly one
    owned item, the tight/true/loose rating cancels out mathematically and
    has zero effect on the prediction. This test locks in that this is the
    CURRENT actual behavior, so a future fix will make this test fail on
    purpose, as a reminder to update failure-modes.md when it's addressed.
    """
    charts = load_charts()
    owned_tight = [{"brand": "H&M", "size": "M", "fit": "tight"}]
    owned_loose = [{"brand": "H&M", "size": "M", "fit": "loose"}]

    body_t, ease_t, counts_t = matching.estimate_body_measurements(owned_tight, charts)
    body_l, ease_l, counts_l = matching.estimate_body_measurements(owned_loose, charts)

    _, _, scored_tight = matching.predict_size("Zara", body_t, ease_t, charts, count_by_type=counts_t)
    _, _, scored_loose = matching.predict_size("Zara", body_l, ease_l, charts, count_by_type=counts_l)

    assert scored_tight == scored_loose


def test_unknown_target_brand():
    charts = load_charts()
    owned = [{"brand": "H&M", "size": "M", "fit": "true"}]
    body, ease, counts = matching.estimate_body_measurements(owned, charts)
    size, confidence, scored = matching.predict_size("NotARealBrand", body, ease, charts, count_by_type=counts)

    assert size is None
    assert "No size chart on file" in confidence


# ---- men's slice ----

def test_mens_prediction_works_across_brands():
    """Men's charts use 'chest' instead of 'bust'; the same engine must handle them."""
    charts = load_mens_charts()
    owned = [
        {"brand": "Adidas", "size": "M", "fit": "true"},
        {"brand": "Nike", "size": "M", "fit": "true"},
    ]
    body, ease, counts = matching.estimate_body_measurements(owned, charts)
    size, confidence, scored = matching.predict_size("Levi's", body, ease, charts, count_by_type=counts)

    assert counts == {"body_circumference": 2}
    assert "chest" in body["body_circumference"]
    assert size == "M"


def test_mens_chest_actually_drives_the_prediction():
    """
    Guards the silent-failure risk: if 'chest' had no weight the engine would
    quietly ignore it. A much bigger chest in the owned item must give a
    bigger predicted size.
    """
    charts = load_mens_charts()

    def predict_from(owned_size):
        owned = [{"brand": "Nike", "size": owned_size, "fit": "true"}]
        body, ease, counts = matching.estimate_body_measurements(owned, charts)
        size, _, _ = matching.predict_size("Adidas", body, ease, charts, count_by_type=counts)
        return size

    small, large = predict_from("S"), predict_from("XL")
    assert matching.SIZE_ORDER.index(large) > matching.SIZE_ORDER.index(small)


# ---- cut guardrail ----

def test_oversized_and_slim_items_are_set_aside_with_a_reason():
    charts = load_charts()
    items = [
        {"brand": "H&M", "size": "M", "fit": "true", "cut": "regular"},
        {"brand": "H&M", "size": "XS", "fit": "loose", "cut": "oversized"},
        {"brand": "Zara", "size": "S", "fit": "true", "cut": "slim"},
    ]
    usable, set_aside = matching.split_usable_items(items, charts)

    assert [i["size"] for i in usable] == ["M"]
    assert [(i["brand"], why) for i, why in set_aside] == [("H&M", "special_cut"), ("Zara", "special_cut")]


def test_an_item_without_a_cut_counts_as_regular():
    """Older callers never send 'cut'. They must keep working, not lose their items."""
    charts = load_charts()
    usable, set_aside = matching.split_usable_items([{"brand": "H&M", "size": "M", "fit": "true"}], charts)
    assert len(usable) == 1 and set_aside == []


def test_a_size_the_brand_does_not_make_is_set_aside_not_dropped():
    charts = load_charts()
    usable, set_aside = matching.split_usable_items([{"brand": "Zara", "size": "XXL", "fit": "true"}], charts)
    assert usable == [] and set_aside[0][1] == "no_such_size"


def test_excluding_an_oversized_item_gives_the_same_answer_as_never_logging_it():
    """The point of the guardrail: the oversized XS can no longer drag the estimate down."""
    charts = load_charts()
    regular = [{"brand": "H&M", "size": "M", "fit": "true"}, {"brand": "Zara", "size": "M", "fit": "true"}]
    with_oversized = regular + [{"brand": "H&M", "size": "XS", "fit": "loose", "cut": "oversized"}]

    def run(items):
        usable, _ = matching.split_usable_items(items, charts)
        body, ease, counts = matching.estimate_body_measurements(usable, charts)
        return matching.predict_size("Uniqlo", body, ease, charts, count_by_type=counts)

    assert run(with_oversized) == run(regular)


def test_without_the_guardrail_an_oversized_loose_xs_would_wreck_the_estimate():
    """Documents WHY the guardrail exists: the same item, used naively, shifts the prediction down."""
    charts = load_charts()
    regular = [{"brand": "H&M", "size": "M", "fit": "true"}]
    naive = regular + [{"brand": "H&M", "size": "XS", "fit": "loose"}]   # no cut recorded -> used as-is

    def size_for(items):
        body, ease, counts = matching.estimate_body_measurements(items, charts)
        return matching.predict_size("Zara", body, ease, charts, count_by_type=counts)[0]

    order = matching.SIZE_ORDER
    assert order.index(size_for(naive)) < order.index(size_for(regular))


# ---- target cut (the cut of the product being bought) ----

def _target_run(cut=None):
    charts = load_mens_charts()
    owned = [{"brand": b, "size": "M", "fit": "true"} for b in ("Adidas", "Nike", "Levi's")]
    body, ease, counts = matching.estimate_body_measurements(owned, charts)
    kwargs = {} if cut is None else {"target_cut": cut}
    return matching.predict_size("Nike", body, ease, charts, count_by_type=counts, **kwargs)


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
