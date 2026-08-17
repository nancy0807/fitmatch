# Product Requirements Document — FitMatch

**Status:** MVP v1 built and tested internally. Verified data + user testing pending.
**Owner:** Nicole
**Last updated:** see repo commit history

---

## 1. Problem Statement

Online apparel shoppers cannot reliably predict their size across different clothing brands, because sizing is not standardized industry-wide. This drives high return rates — commonly cited in the 20.8-40% range for US online apparel, with fit/sizing issues responsible for an estimated 50-77% of those returns depending on the study — and suppresses purchases outright for shoppers who avoid unfamiliar brands rather than risk a bad fit. Attempts to standardize sizing across the industry have not happened; the problem is not new, and reporting on return rates shows no clear improving trend despite years of vendor attention. Full sourcing in `competitive-analysis.md`.

## 2. Target User

**Primary:** Online apparel shoppers who have been burned by inconsistent sizing enough times that they now actively hesitate before buying from an unfamiliar brand — checking multiple reviews, size charts, and forums before committing, or avoiding new brands altogether.

**Job to be done:** *"When I want to buy from a brand I haven't worn before, I want to know what size to order, so I can buy with confidence instead of guessing, over-ordering to return the wrong size, or avoiding the purchase."*

## 3. Value Proposition

Tell FitMatch how a few items you already own fit — it predicts your size in a brand you've never tried, using your own fit history instead of requiring you to know your exact body measurements.

## 4. Product Thesis

Fit prediction tools that require body measurements or brand partnerships create adoption friction or dependency on data most independent builders can't access. A tool built on **subjective fit feedback across brands the user already owns** sidesteps both problems — it uses data the user already has in their head, and it works incrementally as they add more items.

## 5. Core Experience

1. User logs 3-5 items they own (brand, size, how it fits by region)
2. User selects a brand they want to buy from but haven't worn
3. System returns a predicted size with a confidence level and reasoning (score breakdown across candidate sizes)

## 6. MVP Scope

| In scope (v1) | Out of scope (v1) |
|---|---|
| One category: women's tops | Jeans, dresses (harder fit geometry) |
| 5-8 brands with size charts | Real brand data partnerships |
| Manual fit-rating input (tight/true/loose) | Computer vision / photo input |
| Web form, single session | Accounts, saved profiles, persistence |
| Confidence score + reasoning shown | Multi-region sizing (UK/US/EU conversion) |

**Why this scope:** the goal of v1 is to prove the *matching logic* works on a narrow, well-defined slice before expanding surface area. Expanding categories or brands multiplies data-collection cost without testing whether the core prediction approach is sound.

## 7. Why AI (Build vs. Buy vs. Simple Logic)

| Approach | Verdict |
|---|---|
| Static size-chart lookup | Insufficient — requires the user to already know exact body measurements, which most don't have |
| Rule-based logic (if/else per brand) | Insufficient — doesn't generalize across brands with different cuts, and doesn't improve with more data |
| Inference from subjective fit feedback (chosen approach) | Justified — this is a pattern-matching problem across noisy, brand-specific signals, which static rules can't capture well |

v1 uses a hand-tuned heuristic (fixed ease-cm assumptions per fit rating) rather than a learned model — this is a deliberate, documented simplification, not a hidden limitation. See Decision Log.

## 8. Differentiation

Existing cross-brand fit tools (e.g. True Fit, Fit Analytics) largely require brand-side integration or detailed body scanning — both inaccessible to an independent product. FitMatch's differentiation is functioning entirely from user-supplied fit history, with no brand partnership dependency, trading some initial accuracy for zero-integration-cost adoption.

## 9. Success Metrics

**For MVP validation (this case study):**
- Prediction agrees with what the user says they'd actually buy, across 8-10 test users
- Confidence score correlates with actual prediction accuracy (high-confidence predictions should be right more often)

**For a hypothetical v2 (documented, not built):**
- Return rate reduction among users who used a FitMatch prediction vs. those who didn't
- Repeat usage (does a user come back when buying from a new brand again)

## 10. Business Model (Exploratory — Not Validated)

Not a focus of this MVP, but for completeness: a plausible model is a freemium web tool with premium features (saved profiles, more categories) or a B2B licensing angle (retailers embedding fit prediction at checkout) — the latter closer to how incumbents like True Fit actually monetize. This MVP does not attempt to validate willingness-to-pay; that's explicitly out of scope for a portfolio-stage case study.

## 11. Risks & Assumptions

- **Assumption:** users can accurately self-report fit (tight/true/loose) without body measurement training — untested.
- **Assumption:** ease-per-fit-rating heuristic generalizes across brands — likely to break for brands with unusual cuts (e.g., boxy/oversized labels).
- **Risk:** placeholder size-chart data must be replaced with verified numbers before any user testing, or results are meaningless.
- **Risk:** a 5-8 brand, 1-category MVP may be too narrow to produce a compelling demo if a tester's brands aren't covered.

## 12. Roadmap

1. ~~Problem discovery and competitive validation~~ (done)
2. ~~v1 matching engine + Flask MVP~~ (done)
3. Verified size-chart data (5+ brands, official sources)
4. User testing (8-10 people) and metric collection
5. Case study writeup and public documentation
6. (Stretch) v2 — learned ease model from aggregate fit data, category expansion
