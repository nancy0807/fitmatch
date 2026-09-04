# Final Documentation

The complete case study in one place — written so anyone can understand it, technical enough that no detail is lost.

## The problem

Sizing isn't standardized across clothing brands. A "Medium" in one brand and a "Medium" in another can fit completely differently. This isn't a minor annoyance — size and fit is the single most cited reason for online apparel returns (53% of surveyed retailers, Coresight Research 2023), driving a 24.4% average return rate and an estimated $38B in returned merchandise annually. The industry has invested heavily in fixing this — virtual try-on, size recommenders, body scanning — and return rates still haven't meaningfully moved.

## Why not a wardrobe app

The project started in a different place: an AI-powered wardrobe/styling tool. Competitive research killed it fast. That category is already crowded — Whering, Acloset, Stylebook, and others already compete there, and the complaints in that space are about execution quality, not a missing capability. Building another one would have proven nothing. Full reasoning in `01-problem-research/competitor-audit.md`.

## Why this problem is different

Cross-brand sizing has also been attempted — but by companies relying on data an independent builder doesn't have: brand partnerships, garment measurement databases, body scans. What hasn't been built at scale is a **user-owned fit profile** — sizing intelligence that travels with the shopper, not the brand. That's the wedge.

## How FitMatch works

A user logs a few items they already own — brand, size, and how it fits (tight / true / loose). The engine infers an estimated body measurement from that feedback, then scores every size in a new brand against that estimate plus the user's typical preferred ease. It returns a predicted size with a confidence level and the full score breakdown, so the reasoning is visible, not a black box.

v1 runs on a hand-tuned heuristic, not a learned model — a deliberate, stated simplification given there's no aggregate fit data yet to learn from. The upgrade path is documented, not hidden.

## Why a heuristic, not a model

It would have been easy to bolt an ML layer onto this and call it "AI-powered." That would have been the wrong call, and it's worth being explicit about why.

A learned model needs something to learn from: real fit outcomes across many users, so ease assumptions (how much room a "true" fit actually implies, per body region) can be inferred from data instead of hand-picked. That data doesn't exist yet — there are no users, so there's no aggregate fit history to train on. Training a model on synthetic or self-generated data at this stage wouldn't be learning anything real; it would just be a heuristic wearing an ML costume, and it would actively work against the confidence-scoring system, which is designed to be honest about how much it doesn't know.

So v1 uses a transparent, auditable heuristic instead: ease-per-fit-rating constants (documented in `matching.py`) that convert a garment measurement into an estimated body measurement, weighted by region, with confidence that explicitly downgrades when the underlying data is thin. Every prediction is explainable — you can see exactly which owned items and which assumptions produced it.

The "AI" in this v1 isn't the arithmetic — it's the reframing underneath it: inferring a body estimate from *subjective, cross-brand fit feedback* is a pattern-inference problem, not a lookup, and that's the part a static size chart can't do on its own. The genuinely learned version — an embedding per brand/size, ease assumptions inferred from real aggregate outcomes instead of hand-picked — is the documented v2 path, and it becomes the right call the moment real usage data exists to train it on. Shipping a model before that data exists would optimize for looking sophisticated over being honest, and this product's whole thesis is the opposite of that.

## What was built across all phases

- **Problem research** — market sizing, competitor audit, the kill decision
- **User research** — persona, journey map, the intervention point (the size selector on an unfamiliar brand, the last moment before a costly guess)
- **Solution design** — the matching mechanism, user flows, technical architecture, failure modes
- **Ethics & metrics** — honest risk accounting (overconfidence from thin data, an untested heuristic, body-adjacent personal data), a north-star metric tied to actual prediction accuracy, not vanity engagement numbers
- **A working v1 prototype** — Flask app, matching engine, tested end-to-end against simulated users — further than research-only case studies typically go

## Honest limitations

- Size-chart data is currently structurally realistic placeholder data for most brands, not yet verified against official brand pages — Westside is the one exception, sourced from Westside's real official size guide
- **Sourcing obstacle found while trying to fix the above:** most brands, including large global ones (confirmed on Uniqlo's own size-chart help pages), don't publish one canonical brand-wide size chart at all — measurements are given per product/style, not per brand, because cut varies style to style. Several Indian D2C brands (Pantaloons, Zudio, The Souled Store) additionally render their size guide inside non-crawlable JS tabs. This means "verify the brand chart" wasn't a data-entry task — it surfaced a real structural mismatch between how FitMatch's data model assumes sizing works (one chart per brand) and how brands actually publish it (one chart per product). Documented in `open-questions.md`; the real fix is likely sourcing measurements per representative product per brand rather than per brand, which is a data-model change, not just a data-fill task.
- The confidence-scoring logic doesn't yet account for how little data (how few owned items) backs a given prediction — a known, tracked gap, not a hidden one
- The ease-per-fit-rating heuristic was hand-picked, not learned — it may not generalize well across body types or unusually-cut brands
- Not yet tested with real users — that's the next phase, not a completed claim
