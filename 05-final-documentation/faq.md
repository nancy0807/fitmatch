# FAQ

Anticipated hard questions, answered directly.

**Why sizing, when so many sizing tools already exist?**
Because none of the credible ones work without data an independent builder can't get — brand partnerships, garment measurements, body scans. FitMatch tests a narrower question: is a user's own fit history, alone, signal enough for a first pass. See `01-problem-research/competitor-audit.md`.

**Isn't a hand-tuned heuristic just a guess dressed up as AI?**
It's an inference method, not a lookup table — it backs out a body estimate from subjective feedback across brands with different cuts, which a static rule can't generalize to do. But it's honestly a v1 heuristic, not a learned model, and the repo says so directly rather than overselling it. That distinction is documented in `03-solution-design/solution-design.md`.

**Why does the confidence score matter so much?**
Because v1 is a heuristic, overclaiming certainty is the single biggest risk in this product. A prediction with a visible confidence level and score breakdown lets a user calibrate trust themselves — a bare "your size is M" doesn't.

**What happens with an oversized or slim item?**
If you *own* one, it's set aside and shown to you, never used: a loose oversized XS would make you look like a much smaller person. If you're *buying* one, pick its cut and the result shifts by an assumed amount, with confidence capped at medium and a note saying the amount is an assumption. See `03-solution-design/failure-modes.md`.

**Why isn't there a business model built out yet?**
Because building one out before the core prediction mechanism is validated with real users would be planning ahead of evidence — the exact mistake the wardrobe-app direction risked. See `05-final-documentation/go-to-market.md` for what's deliberately left light and why.

**Where do the size charts come from?**
Screenshots of each brand's own size-guide popup, transcribed by hand and stored as range midpoints; 23 of 27 charts come from a published size guide. The other four are flagged on every result that uses them: Zara is *approximate*, women's Zudio is *unverified*, and men's Zudio is a *placeholder* averaged from the real men's charts. Early versions used invented placeholder numbers, clearly labelled, because aggregator sites disagreed and search couldn't reach the brands' popups. Silently hardcoding unverified numbers would have made every prediction meaningless without anyone knowing.

**Why is Zara "approximate"?**
Zara only publishes garment measurements for each product, never a body chart, and FitMatch never compares garment and body charts directly. Left like that, Zara couldn't connect to any other brand. So its flat chest is converted to an estimated body size (× 2, minus the engine's own 12 cm true-fit ease), from one regular or relaxed product per gender. Slim products were tried and gave impossible body sizes, which is itself a good argument for keeping the two kinds of chart apart. Confidence is capped at medium and the page names the product used.

**Why were Roadster and HRX removed?**
No real chart was available for either, and keeping invented numbers for brands nobody asked about added nothing. Removing them was more honest than keeping them as placeholders.
