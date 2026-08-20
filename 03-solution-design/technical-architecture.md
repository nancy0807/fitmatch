# Technical Architecture

Three components, cleanly separated.

```mermaid
flowchart LR
    subgraph Client
        UI[Browser: index.html form]
    end
    subgraph Server [Flask app.py]
        Route[POST / route]
    end
    subgraph Engine [matching.py]
        Estimate[estimate_body_measurements]
        Predict[predict_size]
    end
    subgraph Data
        Charts[(size_charts.json)]
    end

    UI -- form submit --> Route
    Route -- owned items --> Estimate
    Estimate -- reads --> Charts
    Estimate -- body estimate + preferred ease --> Predict
    Predict -- reads --> Charts
    Predict -- predicted size, confidence, scores --> Route
    Route -- rendered result --> UI
```

- **Matching engine** — pure functions, no knowledge of Flask or HTTP. Takes fit data in, returns a prediction out. Swappable into a different interface (API, CLI) without touching the logic itself.
- **Flask layer** — only handles the web boundary: reads form fields, calls the engine, renders the result. Does not contain prediction logic.
- **Data layer** — flat JSON for v1. The dataset is small, read-heavy, and doesn't change mid-session — a database buys nothing at this scale. Documented upgrade path to SQLite once brand/category count grows.

**Deliberately absent in v1:** no persistence, no accounts, no session storage. Every prediction is stateless. Infrastructure gets built once there's a validated reason for returning users, not before.
