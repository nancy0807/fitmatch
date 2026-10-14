# Metrics

A measurement framework built around one north star question: does the predicted size match what the user would actually buy?

**North star metric:** prediction agreement rate — predicted size matches the size the user confirms they'd purchase, tested against 8-10 real users using their own brands.

### First real result

Tester 1: owned H&M (L), Zara (L), Max (M). Predicted Roadster L, 94% match, high confidence. Tester said yes, they'd actually buy that size.

1 of 1 testers so far said yes — too early to call this a rate. It also needs an honest caveat: at the time, all four charts involved (H&M, Zara, Max and Roadster) were invented placeholders, so this showed the flow made sense to a real person, not that the numbers were right. Roadster has since been removed, and H&M, Zara and Max now use real (or, for Zara, approximate) charts, so this exact prediction can't be re-run. It stays here as the historical first result. Every tester from v8 on predicts against real charts. Needs 7-9 more testers.

**Primary metrics:**

- Prediction agreement rate, overall and split by confidence level (high-confidence predictions should agree more often than low-confidence ones — if they don't, the confidence logic itself is broken)
- Minimum owned-items count where predictions start being reliable (informs onboarding guidance — how many items should the product ask a new user to log before predicting)

**What is deliberately not measured (yet):** conversion, retention, session length, signups. Optimizing for those before the core mechanism is validated would be planning ahead of evidence — the same mistake the wardrobe-app direction risked making. Business-model metrics belong after the prediction mechanism proves itself, not before.
