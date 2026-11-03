# Signals belong to Tracked Assets, not to users

A Signal is computed once per Tracked Asset, not once per user, because the indicator vote depends only on price action and is identical for everyone watching the same ticker. The only user-specific input, whether the user bought within the last day, is applied when deciding whether to send that user an Alert, not when generating the Signal. This removes duplicate computation and rows, and gives Accuracy a single graded series per ticker.

## Considered Options

- **Per-user Signals (the original design):** lets the recently-purchased rule change the stored Signal, but duplicates every Signal per watcher and makes per-ticker Accuracy ambiguous when the copies disagree.
