# FitMatch — Cross-Brand Fit Prediction

A research-backed product management case study applying evidence-first problem discovery, competitive validation, and honest AI-scoping to the cross-brand apparel sizing problem.

---

## Thesis

Existing sizing tools fail people who want to try a new brand because they solve the problem *within* a brand, not *across* brands — they need body scans or brand-side data the shopper (and an independent builder) doesn't have.

This case study argues the missing piece isn't better prediction technology. It's a **user-owned fit profile** — a sizing signal that travels with the shopper instead of living inside one brand's system.

FitMatch does not ask "what are your measurements?" It asks "how has what you already own fit you?" — and infers the rest.

---

## Core Insight

Most sizing tools intervene *after* the wrong size has already shipped — at the return, when the cost is already sunk.

This case study identifies the size selector on an unfamiliar brand's page as the primary high-leverage intervention point: the last moment where a prediction can still change the outcome, before a guess turns into a return.

FitMatch intervenes at that moment. Everything before and after it is out of scope for v1.

---

## Case Study Structure

| Phase | Focus | Status |
|---|---|---|
| 01 | Problem Research | ✅ Complete |
| 02 | User Research | ✅ Complete |
| 03 | Solution Design | ✅ Complete |
| 04 | Ethics & Metrics | ✅ Complete |
| 05 | Final Documentation | ✅ Complete |
| — | Working v1 prototype | ✅ Live — 12 brands, dual measurement-type support (garment vs. body-circumference sizing), illustrated UI |
| — | Verified size-chart data | 🔄 In Progress — 1 of 12 brands verified (Westside); the rest are clearly-labelled placeholders |
| — | Real user testing | ⏳ Pending |

---

## Phase 01 — Problem Research (Complete)

### market-analysis.md
The scale of the problem and why it's still open. Key findings: 53% of retailers cite size/fit as the top return reason; $38B in annual returned apparel; despite heavy industry investment (85% adopting virtual try-on), only 1 in 4 retailers offer cross-brand fit guidance.

### competitor-audit.md
Why the original wardrobe/styling app direction was killed, and why cross-brand sizing was selected instead. Key finding: the wardrobe app category is crowded and the gaps there are execution gaps, not opportunity gaps. Sizing, by contrast, is well-attempted but still structurally unsolved across brands.

### phase1-synthesis.md
The one-page argument: the industry has built size intelligence within brands, not across them. That's the wedge.

---

## Phase 02 — User Research (Complete)

### personas.md
Primary persona: an online shopper whose hesitation isn't about price or style — it's specifically "will this fit," surfacing at the moment of selecting a size on an unfamiliar brand.

### journey-map.md
Five-moment map of a cross-brand purchase decision. Critical finding: the coping response (over-ordering, cart abandonment) is a diagnostic signal of the problem's cost — the fix belongs earlier, at the size-selection moment itself.

### opportunity-spaces.md
Identifies the size selector as the primary intervention point, and makes the case for why AI (inference from subjective fit feedback) is justified there over a static lookup or hand-coded rules.

---

## Phase 03 — Solution Design (Complete)

### solution-design.md
The core prediction mechanism: a fit-history-based inference engine. Backs out an estimated body measurement per owned item (garment measurement minus an ease allowance implied by fit rating), averages across items, then scores every size in a target brand against that estimate plus preferred ease. v1 runs on a hand-tuned heuristic, not a learned model — a stated simplification, with a documented upgrade path once aggregate fit data exists.

### user-flows.md
The complete interaction map: log → predict → interpret. Design principle: an empty-state prediction is worse than no prediction, so the flow requires fit history before it will predict at all. The score breakdown is shown, not hidden, so the user can judge confidence themselves rather than take a label on faith.

### technical-architecture.md
Three cleanly separated components: a pure-function matching engine with no knowledge of HTTP, a thin Flask layer that only handles the web boundary, and flat-JSON data storage sized to a small, read-heavy dataset. No persistence or accounts in v1 — a deliberate choice, not an oversight.

### failure-modes.md
Named failure modes and their mitigations, including overconfident predictions from thin data (**fixed** — confidence now downgrades when fewer than 3 items are logged), a heuristic that may not generalise across body types, and the risk of an unusually-cut brand breaking the ease assumptions.

---

## Phase 04 — Ethics & Metrics (Complete)

### ethics.md
Three risks examined honestly: overconfidence from thin data (**fixed**), a heuristic tuned by one person's intuition rather than learned from diverse data, and fit history as body-adjacent personal data — mitigated in v1 by having no accounts and no persistence.

### metrics.md
A measurement framework built around one north-star question: does the predicted size match what the user would actually buy. Deliberately excludes conversion, retention, and signup metrics until the core prediction mechanism itself is validated.

---

## Phase 05 — Final Documentation (Complete)

### final-documentation.md
The complete case study in one place: the problem, why the wardrobe-app direction was killed, why cross-brand sizing is the wedge, how FitMatch works, and an honest limitations section.

### decision-log.md
Every real decision point with the evidence behind it — including a caught-and-corrected pair of unverified statistics from an early draft, flagged deliberately rather than hidden.

### faq.md
Anticipated hard questions about the project, answered directly — including why a hand-tuned heuristic isn't just "a guess dressed up as AI," and why the confidence score is the single most important design element in v1.

### go-to-market.md
Positioning and launch scope for a portfolio-stage validation, not a funded commercial launch — deliberately light on business-model depth until the core prediction mechanism is proven with real users.

---

## v1 Build Log

Work on the actual prototype, past the original five research/design phases.

### Dual measurement-type architecture
Not every brand sizes the same way. Some brands (H&M, Zara, Uniqlo...) publish flat garment measurements (chest/shoulder/length). Others — confirmed first with Westside's official size guide — publish body-circumference measurements instead (bust/waist/hip), a genuinely different physical quantity, not just different units. The original matching engine assumed one schema for every brand; testing against a real cross-brand prediction surfaced a crash (`KeyError`) the moment a body-circumference brand's fit history was used to predict a garment-measurement brand. Fixed by keeping body estimates fully separate per measurement type — a user's fit history in one system is never averaged with, or used to predict, the other. A prediction across mismatched systems now returns an honest "no fit history in this measurement system yet" message instead of a silent wrong answer.

### Brand coverage: 12 brands
Expanded from the original 5 to 12, adding Westside, Pantaloons, Zudio, Roadster, The Souled Store, Max, and Lulu & Sky. Only Westside's data is verified against an official size guide. The other 6 new brands are clearly labeled placeholders — repeated attempts to source real charts for Pantaloons, Zudio, and The Souled Store found their official size guides are rendered in JS-based "Fit Guide" tabs that aren't crawlable by search, a real, documented data-sourcing constraint rather than an oversight.

### Frontend redesign
Moved from a bare, unstyled form to an illustrated interface: a custom hero illustration grounded in the actual product moment (checking a garment's fit against a mirror), hand-lettered headings, and a match-percentage display alongside the existing raw score and animated confidence bars.

---

## Why This Project

Most product case studies show either the research or the build, rarely both connected end to end. This one traces every design choice back to a research finding or a killed alternative — including the parts that didn't survive.

The persona isn't invented. The intervention point wasn't assumed. The problem wasn't decided in advance — it emerged from discovery, and a stronger direction (this one) only got selected after a weaker one (the wardrobe app) was tested against evidence and killed.

---

## Author

Niharika Chauhan
B.Tech CS + AI/ML, VIT Bhopal
