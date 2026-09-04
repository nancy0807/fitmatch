# FitMatch — Cross-Brand Fit Prediction

A research-backed product management case study applying evidence-first problem discovery, competitive validation, and honest AI-scoping to the cross-brand apparel sizing problem.

---

## Thesis

Existing sizing tools fail people who want to try a new brand because they solve the problem *within* a brand, not *across* brands — they need body scans or brand-side data the shopper (and an independent builder) doesn't have.

This case study argues the missing piece isn't better prediction technology. It's a **user-owned fit profile** — sizing signal that travels with the shopper instead of living inside one brand's system.

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
| — | Working v1 prototype | ✅ Built and tested |
| — | Verified size-chart data | ⏳ In progress |
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
The core mechanism: infer a body estimate from owned-item fit feedback, then match against a target brand's size chart adjusted for personal ease preference. v1 is a stated heuristic, not a learned model — the upgrade path is documented, not hidden.

### user-flows.md
Full interaction map. Design principle: an empty-state prediction is worse than no prediction, so the flow makes it structurally impossible to skip logging fit history first.

### technical-architecture.md
Clean separation between the matching engine (pure functions, no web-framework knowledge), the Flask layer, and the data layer. No persistence in v1 — deliberate, not an oversight.

### failure-modes.md
Four named failure modes with root cause and mitigation — thin-data overconfidence, heuristic generalization risk, unusual brand cuts, and placeholder-data risk.

---

## Phase 04 — Ethics & Metrics (Complete)

### ethics.md
Three concerns examined honestly: overconfidence from thin fit history, a heuristic that may not generalize across body types, and handling of body-adjacent personal data. Not a checklist — a real accounting of where v1 is fragile.

### metrics.md
North star: does the predicted size match what the user would actually buy? Deliberately excludes engagement vanity metrics (signups, session length) until the core mechanism is validated.

---

## Phase 05 — Final Documentation (Complete)

### final-documentation.md
The complete case study in one document, written for a reader who's never seen the repo.

### decision-log.md
Every real decision point, including the ones that got killed or corrected — not just the winning path.

### go-to-market.md
Positioning, launch approach for validation-stage testing, and what's deliberately left out until the core mechanism is proven.

### faq.md
Hard questions, answered directly — including why a hand-tuned heuristic isn't overclaimed as more sophisticated than it is.

---

## The Build

Beyond the research and design documents, FitMatch has a working v1 prototype: `app.py` (Flask), `matching.py` (the inference engine), `templates/index.html` (the interface), and `data/size_charts.json` (placeholder size data, clearly labeled, pending verified real-world numbers).

---

## Why This Project

Most product case studies show either the research or the build, rarely both connected end to end. This one traces every design choice back to a research finding or a killed alternative — including the parts that didn't survive.

The persona isn't invented. The intervention point wasn't assumed. The problem wasn't decided in advance — it emerged from discovery, and a stronger direction (this one) only got selected after a weaker one (the wardrobe app) was tested against evidence and killed.

---

## Author

Niharika Chauhan
B.Tech CS + AI/ML, VIT Bhopal
GitHub: github.com/nancy0807
