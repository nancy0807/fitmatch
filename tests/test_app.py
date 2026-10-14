"""
Tests for the web layer (app.py + templates/index.html), using Flask's test client.
Most of these exist because the page once did something the engine tests could
never see — e.g. showing 'None' as the predicted size.
"""

import html as html_lib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app import app

client = app.test_client()


def page(path="/"):
    r = client.get(path)
    assert r.status_code == 200
    # unescape so assertions can read naturally ("H&M", "women's") instead of "H&amp;M", "women&#39;s"
    return html_lib.unescape(r.data.decode("utf-8"))


def predict(gender, owned, target):
    """owned: list of (brand, size, fit) or (brand, size, fit, cut)"""
    data = {
        "gender": gender,
        "owned_brand": [o[0] for o in owned],
        "owned_size": [o[1] for o in owned],
        "owned_fit": [o[2] for o in owned],
        "owned_cut": [o[3] if len(o) > 3 else "regular" for o in owned],
        "target_brand": target,
    }
    r = client.post("/", data=data)
    assert r.status_code == 200
    return html_lib.unescape(r.data.decode("utf-8"))


def test_default_page_is_women_with_a_gender_toggle():
    html = page("/")
    assert 'value="Westside"' in html
    assert "women's tops" in html and "men's tops" in html


def test_men_page_shows_only_mens_brands():
    html = page("/?gender=men")
    assert 'value="Nike"' in html
    assert 'value="Lulu & Sky"' not in html      # a women-only brand
    assert 'name="gender" value="men"' in html


def test_unknown_gender_falls_back_to_women():
    html = page("/?gender=bogus")
    assert 'value="Westside"' in html


def test_womens_prediction_renders_a_size():
    html = predict("women", [("H&M", "L", "true"), ("Nike", "L", "true"), ("Max", "M", "true")], "Westside")
    assert '<div class="size">' in html
    assert "based on 3 owned items" in html


def test_mens_prediction_renders_a_size():
    html = predict("men", [("Adidas", "M", "true"), ("Nike", "M", "true")], "Levi's")
    assert '<div class="size">' in html
    assert "predicted size in Levi" in html


def test_no_prediction_shows_the_reason_not_the_word_None():
    """Lulu & Sky has no XXS, so nothing usable is left: the page must say why, not print 'None'."""
    html = predict("women", [("Lulu & Sky", "XXS", "true")], "Westside")
    assert "check the sizes you picked" in html
    assert '<div class="size">' not in html
    assert ">None<" not in html and "confidence — None" not in html   # the old bug: Python's None printed as text


def test_summary_line_only_lists_items_that_informed_the_prediction():
    """A set-aside oversized item must not appear in the 'based on' line."""
    html = predict("women", [("H&M", "M", "true"), ("Nike", "M", "true"), ("H&M", "XS", "loose", "oversized")], "Westside")
    assert "based on 2 owned items" in html
    assert "H&M (M, true)" in html and "Nike (M, true)" in html
    assert "H&M (XS, loose)," not in html.split("based on")[1].split("</p>")[0]


def test_item_with_a_size_the_brand_does_not_make_is_set_aside_visibly():
    html = predict("women", [("Lulu & Sky", "XXL", "true"), ("H&M", "M", "true")], "Uniqlo")
    assert "set aside" in html
    assert "Lulu & Sky (XXL, true)" in html


def test_womens_page_offers_plus_sizes_up_to_4xl():
    html = page("/")
    assert '<option value="3XL">' in html and '<option value="4XL">' in html


def test_plus_size_prediction_works_where_real_plus_charts_exist():
    html = predict("women", [("Adidas", "3XL", "true")], "Levi's")
    assert '<div class="size">3XL</div>' in html


def test_plus_size_in_a_brand_without_one_is_set_aside_not_guessed():
    html = predict("women", [("Nike", "4XL", "true"), ("Adidas", "3XL", "true")], "Levi's")
    assert "set aside" in html and "Nike (4XL, true)" in html


def test_placeholder_note_appears_when_a_placeholder_brand_is_involved():
    html = predict("men", [("Zudio", "M", "true"), ("Nike", "M", "true")], "Adidas")
    assert "heads up" in html and "Zudio" in html.split("heads up")[1].split("</p>")[0]


def test_no_flag_notes_when_every_brand_is_sourced():
    html = predict("men", [("Adidas", "M", "true"), ("Nike", "M", "true")], "Levi's")
    assert "heads up" not in html and "unverified source" not in html and "approximate:" not in html


def test_unverified_note_appears_for_womens_zudio():
    html = predict("women", [("Zudio", "M", "true"), ("Nike", "M", "true")], "Westside")
    assert "unverified source" in html and "Zudio" in html.split("unverified source")[1].split("</p>")[0]


def test_zara_is_predicted_with_an_approximate_note_and_never_high():
    html = predict("men", [("Adidas", "M", "true"), ("Nike", "M", "true"), ("Levi's", "M", "true")], "Zara")
    assert '<div class="size">' in html and "No fit history" not in html
    assert "approximate: Zara (from its men's relaxed fit interlock tee)" in html
    assert "confidence — high" not in html


def test_a_zara_item_in_the_history_also_shows_the_approximate_note():
    html = predict("women", [("Zara", "M", "true"), ("Nike", "M", "true")], "Westside")
    assert "approximate: Zara (from its women's regular-fit long-sleeve slogan tee)" in html


def bars_section(html):
    """The part of the result card that depends on the maths, without the set-aside notes."""
    card = html.split('<div class="tag">')[1].split("<script>")[0]
    card = card.split('<div class="bars">')[1]
    card = card.split('<p class="basis"')[0]          # stop before any "set aside" note
    text = " ".join(card.split())
    while text.endswith("</div>"):                    # the card's closing tag is only there when no note follows
        text = text[: -len("</div>")].rstrip()
    return text


def test_page_has_a_cut_dropdown_on_each_owned_item():
    html = page("/")
    assert 'name="owned_cut"' in html
    assert '<option value="oversized">' in html and '<option value="slim">' in html


def test_oversized_item_is_set_aside_and_does_not_change_the_prediction():
    """The designer's case: an oversized H&M XS logged as 'loose' must not distort the result."""
    base = [("H&M", "M", "true"), ("Nike", "M", "true")]
    clean = predict("women", base, "Uniqlo")
    with_oversized = predict("women", base + [("H&M", "XS", "loose", "oversized")], "Uniqlo")

    assert bars_section(with_oversized) == bars_section(clean)
    assert "set aside (oversized and slim items" in with_oversized
    assert "H&M (XS, loose, oversized)" in with_oversized


def test_if_every_item_is_oversized_or_slim_the_user_is_told_why_not_shown_a_guess():
    html = predict("women", [("H&M", "XS", "loose", "oversized")], "Nike")
    assert '<div class="size">' not in html
    assert "oversized or slim-cut" in html and "add at least one regular-cut item" in html


def test_form_without_a_cut_field_still_works():
    """An old page or hand-made request sends no owned_cut at all; rows must not vanish."""
    r = client.post("/", data={"gender": "women", "owned_brand": ["H&M"], "owned_size": ["M"],
                               "owned_fit": ["true"], "target_brand": "Nike"})
    html = html_lib.unescape(r.data.decode("utf-8"))
    assert r.status_code == 200 and '<div class="size">' in html


def test_an_unknown_cut_value_counts_as_regular():
    html = predict("women", [("H&M", "M", "true", "banana")], "Nike")
    assert '<div class="size">' in html


def test_predictions_always_state_the_regular_cut_assumption():
    html = predict("women", [("H&M", "M", "true"), ("Nike", "M", "true")], "Uniqlo")
    assert "assume a regular-cut item" in html


def predict_with_target_cut(target_cut):
    data = {"gender": "men", "owned_brand": ["Adidas", "Nike", "Levi's"], "owned_size": ["M", "M", "M"],
            "owned_fit": ["true", "true", "true"], "owned_cut": ["regular"] * 3,
            "target_brand": "Nike", "target_cut": target_cut}
    r = client.post("/", data=data)
    assert r.status_code == 200
    return html_lib.unescape(r.data.decode("utf-8"))


def test_page_lets_you_pick_the_cut_of_the_product_you_want():
    html = page("/")
    assert 'name="target_cut"' in html


def test_oversized_target_changes_the_result_and_says_it_is_an_assumption():
    regular = predict_with_target_cut("regular")
    oversized = predict_with_target_cut("oversized")
    assert '<div class="size">M</div>' in regular
    assert '<div class="size">S</div>' in oversized
    assert "adjusted for the oversized cut" in oversized
    assert "an assumption, not measured" in oversized


def test_regular_target_keeps_the_regular_cut_note_and_no_assumption_note():
    html = predict_with_target_cut("regular")
    assert "assume a regular-cut item" in html
    assert "an assumption, not measured" not in html


def test_unknown_target_cut_counts_as_regular():
    assert predict_with_target_cut("banana") == predict_with_target_cut("regular")


# ---- the form remembers what you entered ----

def post_rows(rows, target="Max", target_cut="regular", gender="women"):
    """rows: list of (brand, size, fit, cut), blanks allowed."""
    data = {"gender": gender, "owned_brand": [r[0] for r in rows], "owned_size": [r[1] for r in rows],
            "owned_fit": [r[2] for r in rows], "owned_cut": [r[3] for r in rows],
            "target_brand": target, "target_cut": target_cut}
    r = client.post("/", data=data)
    assert r.status_code == 200
    return html_lib.unescape(r.data.decode("utf-8"))


def test_first_visit_shows_one_blank_row_with_nothing_chosen():
    html = page("/")
    assert html.count('name="owned_brand"') == 1
    assert 'value="H&M" selected' not in html and 'value="Max" selected' not in html


def test_after_predicting_every_row_and_the_target_are_still_filled_in():
    html = post_rows([("H&M", "M", "true", "regular"), ("Zara", "L", "loose", "oversized"), ("Uniqlo", "S", "tight", "regular")],
                     target="Max", target_cut="oversized")
    assert html.count('name="owned_brand"') == 3                      # all three rows came back
    for brand in ("H&M", "Zara", "Uniqlo"):
        assert f'<option value="{brand}" selected>' in html
    assert '<option value="loose" selected>' in html                  # fit remembered
    assert '<option value="oversized" selected>' in html              # cut remembered
    assert '<option value="Max" selected>' in html                    # the target brand, not the first in the list


def test_a_half_filled_row_comes_back_so_it_can_be_fixed():
    html = post_rows([("Zara", "", "true", "regular")])
    assert '<option value="Zara" selected>' in html
    assert '<div class="tag">' not in html                           # nothing complete -> no result card


def test_completely_blank_rows_are_dropped_but_one_row_always_remains():
    html = post_rows([("", "", "tight", "regular"), ("H&M", "M", "true", "regular"), ("", "", "tight", "regular")])
    assert html.count('name="owned_brand"') == 1
    html = post_rows([("", "", "tight", "regular")])
    assert html.count('name="owned_brand"') == 1


def test_remembering_the_form_does_not_change_the_prediction():
    plain = predict("women", [("H&M", "M", "true"), ("Nike", "M", "true")], "Uniqlo")
    assert '<div class="size">' in plain and "predicted size in Uniqlo" in plain
