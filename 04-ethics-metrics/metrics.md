# Metrics

A measurement framework built around one north star question: does the predicted size match what the user would actually buy?

**North star metric:** prediction agreement rate — predicted size matches the size the user confirms they'd purchase, tested against 8-10 real users using their own brands.

**Primary metrics:**

- Prediction agreement rate, overall and split by confidence level (high-confidence predictions should agree more often than low-confidence ones — if they don't, the confidence logic itself is broken)
- Minimum owned-items count where predictions start being reliable (informs onboarding guidance — how many items should the product ask a new user to log before predicting)

**What is deliberately not measured (yet):** conversion, retention, session length, signups. Optimizing for those before the core mechanism is validated would be planning ahead of evidence — the same mistake the wardrobe-app direction risked making. Business-model metrics belong after the prediction mechanism proves itself, not before.
