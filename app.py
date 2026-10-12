from flask import Flask, render_template, request
from matching import (
    CUT_OPTIONS,
    REGULAR_CUT,
    SIZE_ORDER,
    load_size_charts,
    charts_for_gender,
    split_usable_items,
    estimate_body_measurements,
    predict_size,
)

app = Flask(__name__)

ALL_CHARTS = load_size_charts()
GENDERS = list(ALL_CHARTS["genders"].keys())  # e.g. ["women", "men"]
DEFAULT_GENDER = "women"
GENDER_LABELS = {"women": "women's tops", "men": "men's tops"}
FIT_OPTIONS = ["tight", "true", "loose"]


@app.route("/", methods=["GET", "POST"])
def index():
    # Gender is chosen once, up front, and applies to everything on the page:
    # the brands offered, the sizes offered, the owned items, and the target.
    # Women's and men's fit history are never mixed. It arrives either as
    # ?gender=men (the toggle links) or as a hidden field in the form POST.
    gender = request.values.get("gender", DEFAULT_GENDER)
    if gender not in GENDERS:
        gender = DEFAULT_GENDER

    charts = charts_for_gender(gender, ALL_CHARTS)
    brand_names = list(charts["brands"].keys())
    size_options = [
        s for s in SIZE_ORDER
        if any(s in brand["sizes"] for brand in charts["brands"].values())
    ]

    result = None

    if request.method == "POST":
        brands = request.form.getlist("owned_brand")
        sizes = request.form.getlist("owned_size")
        fits = request.form.getlist("owned_fit")
        cuts = request.form.getlist("owned_cut")
        target_brand = request.form.get("target_brand")

        # Rows come in as parallel lists. A missing or unknown cut counts as a
        # regular cut — it must never make a whole row disappear.
        all_items = []
        for i, (b, s, f) in enumerate(zip(brands, sizes, fits)):
            if not (b and s):
                continue
            cut = cuts[i] if i < len(cuts) else REGULAR_CUT
            if cut not in CUT_OPTIONS:
                cut = REGULAR_CUT
            all_items.append({"brand": b, "size": s, "fit": f, "cut": cut})

        # Only regular-cut items in a size the brand really makes may feed the
        # estimate. Everything else is set aside and SHOWN, with the reason.
        owned_items, set_aside = split_usable_items(all_items, charts)
        ignored_items = [item for item, why in set_aside if why == "no_such_size"]
        special_items = [item for item, why in set_aside if why == "special_cut"]

        if target_brand and all_items:
            if owned_items:
                body, ease, counts = estimate_body_measurements(owned_items, charts)
                size, confidence, scored = predict_size(
                    target_brand, body, ease, charts, count_by_type=counts
                )
            else:
                size, scored = None, []
                if special_items and not ignored_items:
                    confidence = ("Every item you logged is oversized or slim-cut, and this version "
                                  "can't adjust for cut yet — add at least one regular-cut item.")
                elif ignored_items and not special_items:
                    confidence = "None of the items you logged has that size in that brand's chart — check the sizes you picked."
                else:
                    confidence = ("None of the items you logged can be used: some have a size that brand "
                                  "doesn't make, the rest are oversized or slim-cut. Add at least one "
                                  "regular-cut item in a size the brand makes.")

            # Show only the owned items that actually informed THIS prediction:
            # items in the other measurement type were correctly left out of
            # the math, so they must be left out of this summary too.
            target_type = charts["brands"].get(target_brand, {}).get("measurement_type", "garment_flat")
            relevant_owned_items = [
                item for item in owned_items
                if charts["brands"][item["brand"]].get("measurement_type", "garment_flat") == target_type
            ]

            # Which brands in this result rest on invented (placeholder) numbers?
            # The target counts, and so does any owned item that fed the estimate.
            involved = [target_brand] + [item["brand"] for item in relevant_owned_items]
            placeholder_brands = sorted({b for b in involved if charts["brands"].get(b, {}).get("placeholder")})

            # Turn raw match-error scores into display bar widths (0-100) AND a
            # friendlier match percentage. Presentation-only: matching.py stays
            # free of anything about how results are shown. The percentage is a
            # rescaled view of the same error score, not a separate statistical
            # measure — 10 percentage points lost per unit of weighted error,
            # floored at 0%.
            scored_display = []
            if scored:
                max_score = max(s for _, s in scored) or 1
                for sz, sc in scored:
                    width = max(8, round(100 - (sc / max_score) * 85))
                    percent = max(0, round(100 - sc * 10))
                    scored_display.append({"size": sz, "score": sc, "width": width, "percent": percent})

            result = {
                "target_brand": target_brand,
                "predicted_size": size,          # None when there is no prediction
                "confidence": confidence,        # holds the explanation when size is None
                "scored": scored_display,
                "owned_items": relevant_owned_items,
                "ignored_items": ignored_items,
                "special_items": special_items,
                "placeholder_brands": placeholder_brands,
            }

    return render_template(
        "index.html",
        brands=brand_names,
        sizes=size_options,
        fits=FIT_OPTIONS,
        cuts=CUT_OPTIONS,
        genders=GENDERS,
        gender=gender,
        gender_labels=GENDER_LABELS,
        result=result,
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
