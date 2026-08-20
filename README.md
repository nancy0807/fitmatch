# FitMatch

**Predicting your size in a clothing brand you've never bought from — using how items from other brands have actually fit you.**

*A product management case study: problem discovery → competitive validation → a killed direction → a validated pivot → MVP build.*

📄 [Full PRD](docs/PRD.md) · 📊 [Competitive Analysis](docs/competitive-analysis.md) · 🧭 [Decision Log](docs/decision-log.md)
🎨 [Design & User Flow](docs/design.md) · 🏗️ [Architecture](docs/architecture.md) · 📣 [Go-To-Market](docs/go-to-market.md) · ⚖️ [AI Ethics](docs/ai-ethics.md)

## The Problem

Clothing sizing isn't standardized across brands. A "Medium" from one brand can fit completely differently from a "Medium" in another. This isn't a minor annoyance — industry data puts fit as the #1 reason for online apparel returns (roughly 20-40% of orders), costing an estimated $94B in 2019 alone. Attempts to standardize sizing across the industry have failed repeatedly, and existing fit-prediction tools mostly require brand partnerships or detailed body scanning to work — both out of reach for an independent shopper.

## Why This, Not a Wardrobe App

This project started as a wardrobe-organization/styling app idea. Competitive research killed it: the AI wardrobe app space is already crowded (Whering, Acloset, Stylebook, Indyx, Cladwell, and others), and the complaints in that space are about *quality of execution*, not *unsolved problems*. Cross-brand sizing, by contrast, has been attempted for over a decade and still isn't solved — return rates haven't meaningfully dropped. That's a stronger signal of a genuinely open problem.

## Why AI (Not Just a Lookup Table)

A static size-chart lookup only works if the user already knows their exact body measurements — most people don't, and self-measuring is enough friction to kill adoption. The harder, AI-relevant problem is inferring a body estimate from **subjective fit feedback** ("snug in the shoulders, baggy at the waist") across brands with different cuts. That's pattern inference, not a database join.

## How It Works (v1)

1. User logs items they already own: brand, size, and a fit rating (tight / true / loose)
2. The engine backs out an estimated body measurement per item, using a per-fit-rating "ease" assumption, then averages across owned items
3. For a target brand, it scores every available size against the user's estimated body measurement *plus* their preferred ease, and returns the closest match with a confidence level

**This is a v1 heuristic, not a learned model** — the ease-per-fit-rating values are hand-picked, not learned from data. The documented upgrade path is to replace that heuristic with a model learned from aggregate fit outcomes once there's enough real usage data. That distinction is intentional and part of the case study, not an oversight.

## Current Scope (MVP)

- One category: women's tops
- 5 brands with size charts (currently placeholder data — see note below)
- Web form only, no auth, no persistence between sessions yet

**Explicitly out of scope for MVP:** jeans/dresses (harder fit geometry), computer vision, multi-region sizing, real brand data partnerships, mobile app.

## Data Status

The size chart in `data/size_charts.json` is **structurally realistic placeholder data**, not yet verified against official brand size guides. Early web research surfaced only inconsistent third-party aggregator numbers, which weren't reliable enough to build against. Pulling verified numbers directly from each brand's own official size-guide page is the next concrete task before user testing.

## Stack

Flask + Python, size-chart data in JSON (SQLite planned as the dataset grows), plain HTML/Jinja frontend — deliberately simple, since the interesting part of this project is the matching logic, not the framework.

## Status

- [x] Problem discovery and competitive validation
- [x] v1 matching engine, tested against simulated users
- [x] Working web form (Flask)
- [ ] Verified official size-chart data (5+ brands)
- [ ] Testing with 8-10 real users
- [ ] Case study writeup

## Roadmap

See the [Status](#status) checklist above. This README will be updated as each stage completes, in line with a problem-first, evidence-first build process — including the decisions that got *killed*, not just the ones that survived.
