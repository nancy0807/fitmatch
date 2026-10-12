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
    html = predict("women", [("H&M", "L", "true"), ("Zara", "L", "true"), ("Max", "M", "true")], "Roadster")
    assert '<div class="size">' in html
    assert "based on 3 owned items" in html


def test_mens_prediction_renders_a_size():
    html = predict("men", [("Adidas", "M", "true"), ("Nike", "M", "true")], "Levi's")
    assert '<div class="size">' in html
    assert "predicted size in Levi" in html


def test_no_prediction_shows_the_reason_not_the_word_None():
    """Westside history can't predict Zara (different measurement systems)."""
    html = predict("women", [("Westside", "M", "true")], "Zara")
    assert "No fit history yet" in html
    assert '<div class="size">' not in html
    assert "None" not in html


def test_summary_line_only_lists_items_that_informed_the_prediction():
    """Westside is body_circumference, Roadster is garment_flat: Westside must not be listed."""
    html = predict("women", [("Uniqlo", "M", "loose"), ("Westside", "L", "loose"), ("H&M", "M", "true")], "Roadster")
    assert "based on 2 owned items" in html
    assert "Uniqlo (M, loose)" in html and "H&M (M, true)" in html
    assert "Westside (L, loose)" not in html


def test_item_with_a_size_the_brand_does_not_make_is_set_aside_visibly():
    html = predict("women", [("Zara", "XXL", "true"), ("H&M", "M", "true")], "Uniqlo")
    assert "set aside" in html
    assert "Zara (XXL, true)" in html


def test_womens_page_offers_plus_sizes_up_to_4xl():
    html = page("/")
    assert '<option value="3XL">' in html and '<option value="4XL">' in html


def test_plus_size_prediction_works_where_real_plus_charts_exist():
    html = predict("women", [("Adidas", "3XL", "true")], "Levi's")
    assert '<div class="size">3XL</div>' in html


def test_plus_size_in_a_brand_without_one_is_set_aside_not_guessed():
    html = predict("women", [("Zara", "4XL", "true"), ("Adidas", "3XL", "true")], "Levi's")
    assert "set aside" in html and "Zara (4XL, true)" in html


def test_placeholder_note_appears_when_a_placeholder_brand_is_involved():
    html = predict("men", [("H&M", "M", "true"), ("Nike", "M", "true")], "Adidas")
    assert "heads up" in html and "H&M" in html.split("heads up")[1].split("</p>")[0]


def test_no_placeholder_note_when_every_brand_is_sourced():
    html = predict("men", [("Adidas", "M", "true"), ("Nike", "M", "true")], "Levi's")
    assert "heads up" not in html


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
    base = [("H&M", "M", "true"), ("Zara", "M", "true")]
    clean = predict("women", base, "Uniqlo")
    with_oversized = predict("women", base + [("H&M", "XS", "loose", "oversized")], "Uniqlo")

    assert bars_section(with_oversized) == bars_section(clean)
    assert "set aside (oversized and slim items" in with_oversized
    assert "H&M (XS, loose, oversized)" in with_oversized


def test_if_every_item_is_oversized_or_slim_the_user_is_told_why_not_shown_a_guess():
    html = predict("women", [("H&M", "XS", "loose", "oversized")], "Zara")
    assert '<div class="size">' not in html
    assert "oversized or slim-cut" in html and "add at least one regular-cut item" in html


def test_form_without_a_cut_field_still_works():
    """An old page or hand-made request sends no owned_cut at all; rows must not vanish."""
    r = client.post("/", data={"gender": "women", "owned_brand": ["H&M"], "owned_size": ["M"],
                               "owned_fit": ["true"], "target_brand": "Zara"})
    html = html_lib.unescape(r.data.decode("utf-8"))
    assert r.status_code == 200 and '<div class="size">' in html


def test_an_unknown_cut_value_counts_as_regular():
    html = predict("women", [("H&M", "M", "true", "banana")], "Zara")
    assert '<div class="size">' in html


def test_predictions_always_state_the_regular_cut_assumption():
    html = predict("women", [("H&M", "M", "true"), ("Zara", "M", "true")], "Uniqlo")
    assert "assume a regular-cut item" in html
