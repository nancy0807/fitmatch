"""
Tests for matching.py — the core fit-prediction engine.

These aren't invented coverage. Every test here reflects a scenario that
was actually run and verified by hand during development, most of them
after finding a real bug (see the measurement-type crash test below).
Kept as pytest since it's the standard, but every test reads plainly
enough to follow without pytest experience.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import matching


def load_charts():
    return matching.load_size_charts()


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
