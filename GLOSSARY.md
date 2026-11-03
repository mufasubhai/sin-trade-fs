# SinTrade

A personal tool that watches crypto prices for the assets a user cares about and emails them when there is a worthwhile moment to buy or sell.

## Language

### Assets

**Tracked Asset**:
A crypto ticker the system collects prices for, shared by every user who watches it.
_Avoid_: Active asset

**Watched Asset**:
A Tracked Asset that one user has chosen to follow. It may or may not be something they own.
_Avoid_: Active asset, user asset, holding

**Last Purchased**:
The optional moment a user says they last bought a Watched Asset. It belongs to that user and asset only.
_Avoid_: Purchase, buy date

**Position**:
Reserved for a future concept: a Watched Asset with a quantity and cost basis. Not modelled today.

**Target**:
A price a user sets on a Watched Asset; crossing it produces an Alert. Its direction comes from which side of the price it was set on.
_Avoid_: Price alert, trigger

**Hit**:
The state of a Target that has been crossed and alerted once; it stays quiet until the user re-arms it.
_Avoid_: Triggered, fired

### Signals

**Signal**:
A rule-based recommendation for one Tracked Asset at one moment, the same for every user watching it: buy, sell or hold, with a Confidence, valid for a fixed four-hour horizon and then graded against the price at the end of it. It is derived from recent price action, not forecast by a trained model.
_Avoid_: Prediction, forecast, target

**Hold**:
A Signal recommending no action.
_Avoid_: Neutral, hold_to_avoid_losses

**Outcome**:
How a buy or sell Signal turned out at the end of its horizon: Correct, Wrong, or Flat when the price barely moved. Holds have no Outcome.
_Avoid_: Result, was_correct

**Confidence**:
How strongly the voting indicators agree on a Signal, adjusted by that ticker's past accuracy.
_Avoid_: Probability, score

**Accuracy**:
The share of a ticker's buy or sell Signals with a Correct Outcome, ignoring Flat ones.
_Avoid_: Success rate, win rate

**Baseline**:
How often any four-hour window for a ticker moved the same way anyway; the bar Accuracy must beat to mean anything.
_Avoid_: Benchmark, control

**Alert**:
An email telling a user about one of their Watched Assets: either a buy or sell Signal that differs from the last Signal Alert they received (or has stood for a day), or a Target being crossed. A Hold never produces an Alert.
_Avoid_: Notification, email (as the domain term)
