"""
Tests for the size-chart DATA itself (data/size_charts.json).

Most failures in this project have been data/code mismatches, not logic bugs:
a brand with fields the engine didn't know about, a type the engine couldn't
handle. These tests catch that class of problem the moment the data changes,
instead of when a user hits a crash — or worse, a silently wrong answer.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import matching

ALL = matching.load_size_charts()


def all_brands():
    for gender, slice_ in ALL["genders"].items():
        for name, chart in slice_["brands"].items():
            yield gender, name, chart


def test_there_are_women_and_men_slices_with_brands():
    assert set(ALL["genders"]) == {"women", "men"}
    for gender, slice_ in ALL["genders"].items():
        assert len(slice_["brands"]) >= 3, f"{gender} needs at least 3 brands to predict across"


def test_every_measurement_type_is_known_to_the_engine():
    for gender, name, chart in all_brands():
        t = chart["measurement_type"]
        assert t in matching.EASE_CM, f"{gender}/{name}: unknown type {t}"
        assert t in matching.REGION_WEIGHTS, f"{gender}/{name}: unknown type {t}"


def test_every_region_has_a_weight_and_ease_so_none_is_silently_ignored():
    """The engine does weights.get(region, 0): a region with no weight would just vanish from the maths."""
    for gender, name, chart in all_brands():
        t = chart["measurement_type"]
        for field in chart["measurement_fields"]:
            assert matching.REGION_WEIGHTS[t].get(field, 0) > 0, f"{gender}/{name}: '{field}' has no weight"
            for rating in ("tight", "true", "loose"):
                assert field in matching.EASE_CM[t][rating], f"{gender}/{name}: '{field}' has no '{rating}' ease"


def test_every_size_lists_every_field():
    for gender, name, chart in all_brands():
        for size, row in chart["sizes"].items():
            for field in chart["measurement_fields"]:
                assert field in row, f"{gender}/{name}/{size}: missing '{field}'"


def test_measurements_never_shrink_as_sizes_grow():
    """Catches typos in hand-entered numbers (e.g. 98 typed as 89)."""
    for gender, name, chart in all_brands():
        previous = None
        for size, row in chart["sizes"].items():
            if previous is not None:
                for field in chart["measurement_fields"]:
                    assert row[field] >= previous[field], f"{gender}/{name}/{size}: '{field}' went down"
            previous = row


def test_size_labels_are_all_known_to_the_size_dropdown():
    """A label outside SIZE_ORDER (e.g. '2XL') would silently never appear in the dropdown."""
    for gender, name, chart in all_brands():
        for size in chart["sizes"]:
            assert size in matching.SIZE_ORDER, f"{gender}/{name}: size label '{size}' is not in SIZE_ORDER"


def test_charts_for_gender_returns_that_genders_brands_only():
    men = matching.charts_for_gender("men")
    women = matching.charts_for_gender("women")
    assert "Lulu & Sky" in women["brands"] and "Lulu & Sky" not in men["brands"]
    assert men["brands"]["Adidas"]["measurement_fields"][0] == "chest"
    assert women["brands"]["Adidas"]["measurement_fields"][0] == "bust"


def test_a_brand_in_both_slices_has_a_separate_chart_for_each():
    """Westside sells both; its men's and women's charts must be different data, not one shared chart."""
    men = matching.charts_for_gender("men")["brands"]["Westside"]
    women = matching.charts_for_gender("women")["brands"]["Westside"]
    assert men["measurement_fields"] != women["measurement_fields"]
    assert men["sizes"]["M"] != women["sizes"]["M"]


def test_unknown_gender_raises_instead_of_guessing():
    raised = False
    try:
        matching.charts_for_gender("kids")
    except KeyError:
        raised = True
    assert raised


def test_placeholder_flag_and_label_always_agree():
    """The app's visible 'placeholder' note is driven by the flag; the human-readable label lives in _source. They must not drift apart."""
    for gender, name, chart in all_brands():
        flagged = chart.get("placeholder") is True
        labelled = chart.get("_source", "").startswith("PLACEHOLDER")
        assert flagged == labelled, f"{gender}/{name}: placeholder flag={flagged} but _source label={labelled}"


def test_mens_placeholder_brands_are_exactly_the_average_of_the_real_mens_charts():
    """Documents the one assumption behind every men's placeholder: no per-brand guesses."""
    men = matching.charts_for_gender("men")["brands"]
    real = [b for b, c in men.items() if not c.get("placeholder")]
    fakes = [b for b, c in men.items() if c.get("placeholder")]
    assert len(real) >= 3 and len(fakes) >= 1
    for fake in fakes:
        for size, row in men[fake]["sizes"].items():
            for field in ("chest", "waist", "hip"):
                avg = round(sum(men[b]["sizes"][size][field] for b in real) / len(real), 1)
                assert row[field] == avg, f"{fake}/{size}/{field}: {row[field]} != average of real charts {avg}"


def test_plus_sizes_exist_only_where_a_real_chart_gave_them():
    women = matching.charts_for_gender("women")["brands"]
    with_plus = {name for name, c in women.items() if "3XL" in c["sizes"] or "4XL" in c["sizes"]}
    assert with_plus == {"Adidas", "Levi's"}
    assert "4XL" in women["Adidas"]["sizes"] and "4XL" not in women["Levi's"]["sizes"]
    for name in with_plus:
        assert not women[name].get("placeholder")
