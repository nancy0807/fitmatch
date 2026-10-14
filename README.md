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
| — | Working v1 prototype | ✅ Live — women's tops (14 brands) and men's tops (13 brands), cut guardrail, illustrated UI |
| — | Real size-chart data | ✅ 23 of 27 charts from published size guides; the 4 exceptions are flagged on every result that uses them |
| — | Real user testing | 🔄 In Progress — 1 tester so far, target 8–10 |

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
Not every chart measures the same thing. Some publish flat garment measurements (chest/shoulder/length); others — confirmed first with Westside's official size guide — publish body-circumference measurements instead (bust/waist/hip), a genuinely different physical quantity, not just different units. The original matching engine assumed one schema for every brand; testing against a real cross-brand prediction surfaced a crash (`KeyError`) the moment a body-circumference brand's fit history was used to predict a garment-measurement brand. Fixed by keeping body estimates fully separate per measurement type — a user's fit history in one system is never averaged with, or used to predict, the other. A prediction across mismatched systems now returns an honest "no fit history in this measurement system yet" message instead of a silent wrong answer. (In v8 every real chart turned out to be body type, so this guard is now mainly a safety net; it stays tested.)

### Women's and men's tops
Charts are split into two gender slices, chosen once per session with a toggle. Fit history never crosses between them, and the same engine serves both (women's charts say "bust", men's say "chest").

### Cut guardrail
User feedback from a fashion designer showed an oversized H&M XS still hanging loose on a regular-M wearer. Each owned item now records its cut. Oversized and slim items are set aside, shown with the reason, and never used. The cut of the product being *bought* adjusts the result by assumed amounts (oversized +10 cm, slim −4 cm), which caps confidence at medium and says so on the page.

### Real size charts (v8)
The early charts were mostly invented placeholders, because search couldn't reach brands' JavaScript size-guide popups. v8 replaces them with numbers transcribed from screenshots of each brand's own popup: 23 of the 27 charts now come from a published size guide (Levi's from retailer copies of its US chart; the rest from the brand's own site). Two findings shaped the data:

- **Every brand-wide chart found is a body chart** (bust or chest, waist, hip). Garment measurements are only published per product, so a brand's garment numbers describe one item, not its sizing.
- **The four exceptions are labelled, not hidden.** Zara (both genders) is *approximate*, women's Zudio is from an *unverified* third-party site, and men's Zudio is a *placeholder* averaged from the real men's charts. Each shows its own note on any result it touches.

Roadster and HRX were removed rather than kept as invented numbers.

### Zara: converting a garment chart
Zara publishes only per-product garment measurements, so it couldn't connect to any other brand: the engine never compares garment and body charts. Rather than leave it isolated, its flat chest is converted to an approximate body size (flat chest × 2 − 12 cm, the engine's own true-fit ease). Slim products give impossible results this way (an M chest of 81 cm), so a non-slim product represents each gender. Confidence is capped at medium and the page names the product used.

### Fairer scoring
Some charts publish only chest; others publish chest, waist and hip. Scores are now a weighted *average* over the measurements actually compared, so a one-measurement chart no longer looks twice as good as it is.

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
