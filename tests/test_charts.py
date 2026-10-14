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


FLAG_LABELS = {"placeholder": "PLACEHOLDER", "unverified": "NOT VERIFIED", "approximate": "APPROXIMATE"}


def test_every_flag_and_its_label_always_agree():
    """
    The app's visible notes are driven by the flags; the human-readable label
    is the start of _source. They must not drift apart, in either direction.
    """
    for gender, name, chart in all_brands():
        for flag, label in FLAG_LABELS.items():
            flagged = chart.get(flag) is True
            labelled = chart.get("_source", "").startswith(label)
            assert flagged == labelled, f"{gender}/{name}: {flag} flag={flagged} but _source label={labelled}"


def test_flagged_brands_are_exactly_the_ones_decided():
    """Locks in the v8 decisions, so a data edit can't quietly add or drop a flag."""
    flagged = {(g, n, f) for g, n, c in all_brands() for f in FLAG_LABELS if c.get(f)}
    assert flagged == {
        ("men", "Zudio", "placeholder"),
        ("women", "Zudio", "unverified"),
        ("women", "Zara", "approximate"),
        ("men", "Zara", "approximate"),
    }


def test_removed_brands_stay_removed():
    for gender, slice_ in ALL["genders"].items():
        assert "Roadster" not in slice_["brands"] and "HRX" not in slice_["brands"], gender


def test_every_brand_is_body_measurements_now():
    """Every brand-wide chart found was a body chart; Zara is converted. garment_flat stays supported by the engine."""
    for gender, name, chart in all_brands():
        assert chart["measurement_type"] == "body_circumference", f"{gender}/{name}"


def test_zara_numbers_are_exactly_the_stated_conversion():
    """body = flat chest x 2 - ease, from the raw garment numbers kept in the chart. No hand-typed results."""
    for gender in ("women", "men"):
        zara = matching.charts_for_gender(gender)["brands"]["Zara"]
        field = zara["measurement_fields"][0]
        ease = zara["_ease_subtracted_cm"]
        assert ease == 2 * matching.EASE_CM["garment_flat"]["true"]["chest"]   # the engine's own true-fit ease
        assert set(zara["_garment_flat_chest"]) == set(zara["sizes"])
        for size, flat in zara["_garment_flat_chest"].items():
            assert zara["sizes"][size][field] == round(flat * 2 - ease, 1), f"{gender}/Zara/{size}"


def test_mens_placeholder_is_exactly_the_average_of_the_real_mens_charts():
    """
    Documents the one assumption behind the men's placeholder: per measurement,
    the average of every real men's chart that publishes it at every size the
    placeholder covers, so each size averages over the same charts.
    """
    men = matching.charts_for_gender("men")["brands"]
    real = {b: c for b, c in men.items() if not any(c.get(f) for f in FLAG_LABELS)}
    fakes = [b for b, c in men.items() if c.get("placeholder")]
    assert len(real) >= 3 and fakes == ["Zudio"]
    for fake in fakes:
        sizes = list(men[fake]["sizes"])
        for field in men[fake]["measurement_fields"]:
            contributors = [b for b, c in real.items()
                            if field in c["measurement_fields"] and all(s in c["sizes"] for s in sizes)]
            assert len(contributors) >= 3, f"{field}: too few charts to average"
            for size in sizes:
                avg = round(sum(real[b]["sizes"][size][field] for b in contributors) / len(contributors), 1)
                assert men[fake]["sizes"][size][field] == avg, f"{fake}/{size}/{field}"


def test_plus_sizes_exist_only_where_a_real_chart_gave_them():
    women = matching.charts_for_gender("women")["brands"]
    with_plus = {name for name, c in women.items() if "3XL" in c["sizes"] or "4XL" in c["sizes"]}
    assert with_plus == {"Adidas", "Levi's", "H&M", "Uniqlo", "Max"}
    for name in with_plus:
        assert not any(women[name].get(f) for f in FLAG_LABELS)
