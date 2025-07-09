# Tenhou.net/6 JSON Log Format

*ＡＩによる解説なので、誤りが含まれる場合があります。*

This document describes the structure of the JSON logs output by the
`events_to_tenhou_json` helper in the **core** package. The format is
modeled after the logs produced by `tenhou.net/6`.

Logs can be generated directly from engine events or converted from a
newline separated MJAI log using the `mjai_log_to_tenhou_json` helper.

## Overview

A log object has four top-level keys:

```json
{
  "title": ["", ""],
  "name": ["A", "B", "C", "D"],
  "rule": {"disp": "MyMahjong", "aka": 0},
  "log": []
}
```

- `title` – metadata embedded at the start of the long replay URL.
- `name` – player names in table order.
- `rule` – rule display string and red dora count.
- `log` – an array of per-hand records.

## Hand Array

Each hand is represented as an array. Elements are:

1. `[oya, honba, kyotaku]` – dealer index, honba count and riichi
   stick count.
2. `[score0, score1, score2, score3]` – starting scores.
3. `[dora_marker]` – numeric tile codes for dora indicators.
4. `[ura_marker]` – numeric tile codes for ura dora indicators.
5. `[hai0_1, …, hai0_13]` – starting hand for player 0.
6. `[hai1_1, …, hai1_13]` – starting hand for player 1.
7. `[hai2_1, …, hai2_13]` – starting hand for player 2.
8. `[hai3_1, …, hai3_13]` – starting hand for player 3.
9. `[event0_1, …]` – draw, discard and meld actions for player 0.
10. `[event1_1, …]` – events for player 1.
11. `[event2_1, …]` – events for player 2.
12. `[event3_1, …]` – events for player 3.
13. `["和了", [Δ0, Δ1, Δ2, Δ3], result_info]` – win result, or
    `["流局", [Δ0, Δ1, Δ2, Δ3]]` when drawn.

`result_info` is an array used by `tenhou.net/6` to describe the
winning hand.  It typically begins with the winning player index and
the losing player (or the winner again when tsumo) followed by the hand
value string and yaku list.

Tiles use the numeric codes from `tenhou.net/6`:

```
11–19: characters
21–29: circles
31–39: bamboo
41–47: honor tiles
```

Meld calls such as chi, pon and kan are encoded as strings beginning with
`c`, `p` or `m` followed by the tile codes, for example `c111213` for
a chi using 1-2-3 characters. The `result_info` array lists the winning
and losing players, a hand value string and the yaku.

Our implementation currently supports only a subset of this
specification:

- Ura dora markers are always empty.
- Meld calls are omitted – only draws and discards are recorded.
- The result array stores only score deltas without yaku or winner
  information.

Despite these limitations, the produced logs can be consumed by tools
expecting the basic `tenhou.net/6` structure.
