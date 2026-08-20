# FAQ

Anticipated hard questions, answered directly.

**Why sizing, when so many sizing tools already exist?**
Because none of the credible ones work without data an independent builder can't get — brand partnerships, garment measurements, body scans. FitMatch tests a narrower question: is a user's own fit history, alone, signal enough for a first pass. See `01-problem-research/competitor-audit.md`.

**Isn't a hand-tuned heuristic just a guess dressed up as AI?**
It's an inference method, not a lookup table — it backs out a body estimate from subjective feedback across brands with different cuts, which a static rule can't generalize to do. But it's honestly a v1 heuristic, not a learned model, and the repo says so directly rather than overselling it. That distinction is documented in `03-solution-design/solution-design.md`.

**Why does the confidence score matter so much?**
Because v1 is a heuristic, overclaiming certainty is the single biggest risk in this product. A prediction with a visible confidence level and score breakdown lets a user calibrate trust themselves — a bare "your size is M" doesn't.

**What happens with a brand that has an unusual cut?**
The confidence score should drop for that case, since the ease assumptions won't match well — see `03-solution-design/failure-modes.md`. This hasn't been tested against real unusual-cut brands yet.

**Why isn't there a business model built out yet?**
Because building one out before the core prediction mechanism is validated with real users would be planning ahead of evidence — the exact mistake the wardrobe-app direction risked. See `05-final-documentation/go-to-market.md` for what's deliberately left light and why.

**Why does the placeholder data matter enough to call out explicitly?**
Because early research for real size charts returned conflicting numbers from aggregator sites. Silently hardcoding unverified numbers would have made every downstream prediction meaningless without anyone knowing. Labeling it honestly costs nothing and prevents a much worse failure later.
