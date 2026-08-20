# Solution Design

The core prediction mechanism — a fit-history-based inference engine.

## How it works

1. User logs items they already own: brand, size, fit rating per region (tight / true / loose)
2. The engine backs out an estimated body measurement per item — garment measurement minus an "ease" allowance implied by the fit rating — and averages across owned items
3. For a target brand, the engine scores every available size against the user's estimated body measurement *plus* their personal preferred ease, and returns the closest match with a confidence level

## Design principle

The system doesn't ask the user what their measurements are. It infers them from what they already know — how things have actually fit. The user never has to translate their own body into numbers; the fit history does that translation for them.

## v1 vs. v2

v1 uses a hand-tuned heuristic — fixed ease-in-cm assumptions per fit rating, chosen by hand, not learned. This is a deliberate, stated simplification: there's no aggregate user data yet to learn from. The documented upgrade path replaces these fixed assumptions with values learned from real fit outcomes across many users once that data exists.
