from flask import Flask, render_template, request
from matching import load_size_charts, estimate_body_measurements, predict_size

app = Flask(__name__)
charts = load_size_charts()
BRAND_NAMES = list(charts["brands"].keys())
SIZE_OPTIONS = ["XS", "S", "M", "L", "XL"]
FIT_OPTIONS = ["tight", "true", "loose"]


@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        brands = request.form.getlist("owned_brand")
        sizes = request.form.getlist("owned_size")
        fits = request.form.getlist("owned_fit")
        target_brand = request.form.get("target_brand")

        owned_items = [
            {"brand": b, "size": s, "fit": f}
            for b, s, f in zip(brands, sizes, fits)
            if b and s
        ]

        if owned_items and target_brand:
            body, ease = estimate_body_measurements(owned_items, charts)
            size, confidence, scored = predict_size(
                target_brand, body, ease, charts, item_count=len(owned_items)
            )
            result = {
                "target_brand": target_brand,
                "predicted_size": size,
                "confidence": confidence,
                "scored": scored,
                "owned_items": owned_items,
            }

    return render_template(
        "index.html",
        brands=BRAND_NAMES,
        sizes=SIZE_OPTIONS,
        fits=FIT_OPTIONS,
        result=result,
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)