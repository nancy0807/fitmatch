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

## What was built across all phases

- **Problem research** — market sizing, competitor audit, the kill decision
- **User research** — persona, journey map, the intervention point (the size selector on an unfamiliar brand, the last moment before a costly guess)
- **Solution design** — the matching mechanism, user flows, technical architecture, failure modes
- **Ethics & metrics** — honest risk accounting (overconfidence from thin data, an untested heuristic, body-adjacent personal data), a north-star metric tied to actual prediction accuracy, not vanity engagement numbers
- **A working v1 prototype** — Flask app, matching engine, tested end-to-end against simulated users — further than research-only case studies typically go

## Honest limitations

- Size-chart data is currently structurally realistic placeholder data, not yet verified against official brand pages
- The confidence-scoring logic doesn't yet account for how little data (how few owned items) backs a given prediction — a known, tracked gap, not a hidden one
- The ease-per-fit-rating heuristic was hand-picked, not learned — it may not generalize well across body types or unusually-cut brands
- Not yet tested with real users — that's the next phase, not a completed claim
