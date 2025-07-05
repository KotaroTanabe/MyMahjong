# Tenhou.net/6 JSON Log Format

*ＡＩによる解説なので、誤りが含まれる場合があります。*

This document describes the structure of the JSON logs output by the
`events_to_tenhou_json` helper in the **core** package. The format is
modeled after the logs produced by `tenhou.net/6`.

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
6. `[event0_1, …]` – draw/discard and call events for player 0.
7. `[event1_1, …]` – events for player 1, and so on.
8. `[...]` – repeat event arrays as needed.
9. `["和了", [Δ0, Δ1, Δ2, Δ3], [riichi, honba], [yakufus]]` – result
   information, or `["流局", [Δ0, Δ1, Δ2, Δ3]]` when drawn.

Tiles use the numeric codes from `tenhou.net/6`:

```
11–19: characters
21–29: circles
31–39: bamboo
41–47: honor tiles
```

Our current implementation supports only a subset of this specification:

- Ura dora markers are always empty.
- Meld calls are recorded only as tile codes without detailed notation.
- The result array omits yaku details and riichi/honba counts.

Despite these limitations, the produced logs can be consumed by tools
expecting the basic `tenhou.net/6` structure.
