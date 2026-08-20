# Competitor Audit

Why the first direction was killed, and why the second one wasn't.

## Direction 1 — Wardrobe Tracking / Styling (Killed)

Catalogue what a user owns and generate AI styling suggestions.

The category is not empty. Whering, Acloset, Stylebook, Indyx, Cladwell, Clueless, and Style DNA already compete here.

**Key findings:**

- AI outfit recommendations get mixed reviews even from users who otherwise like the apps — the styling layer is the weak point industry-wide, not a gap nobody has attempted
- Auto-tagging accuracy is inconsistent (colour worse than category), so users still correct entries manually — the exact friction these apps exist to remove
- The market has already specialised: Stylebook on analytics, Acloset on interface, Whering on sustainability, Cladwell on capsule wardrobes. No single app owns both cataloguing and styling quality
- The sharper diagnosis: these apps answer "what do I own?" The harder question — "which of these should I wear right now?" — is a judgment problem cataloguing doesn't solve

**Verdict:** real problem, mature category, no defensible gap. Building another wardrobe app would need to out-execute funded products solving the same job. Killed.

## Direction 2 — Cross-Brand Sizing (Selected)

Predict a user's size in a brand they haven't worn, from their fit history in brands they own.

**Key findings:**

- The problem is severe and well-documented (see `market-analysis.md`)
- It is not unattempted — True Fit, Fit Analytics, body-scanning vendors, and size-recommender tools already exist
- It is, however, still unsolved at scale: return rates haven't meaningfully moved despite that investment, and cross-brand fit comparison specifically remains rare (1 in 4 retailers)
- Every existing serious attempt depends on data this project doesn't have access to — brand partnerships, garment measurement data, or body scans

**Verdict:** the opportunity isn't inventing size prediction. It's a narrower, testable question — can a user's *own* fit history, without brand-side data, provide enough signal to translate across brands? Selected.
