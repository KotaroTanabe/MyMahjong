# Kyoku (Hand) Flow

This document summarizes the sequence of steps during a single hand. The engine implements these steps in `core.mahjong_engine.MahjongEngine`.

```mermaid
flowchart TD
    A[draw_tile()] --> B{declare_tsumo() / call_kan()?}
    B -- tsumo --> C[declare_tsumo()]
    B -- kan --> D[call_kan() and draw replacement]
    D --> E1[emit draw_tile(source: dead_wall)]
    B -- none --> E{declare_riichi()?}
    E -- yes --> F[declare_riichi()]
    E -- no --> G[discard_tile()]
    F --> G
    G --> H[waiting for claims]
    H -->|ron| I[declare_ron()]
    H -->|kan| J[call_kan()]
    H -->|pon| K[call_pon()]
    H -->|chi| L[call_chi()]
    H -->|skip all| M[draw_tile() for next player]
```

Each node corresponds to a method in `MahjongEngine`:

- `draw_tile()` – draw a tile from the wall and advance `current_player`.
- `call_kan()` – form a kan meld and draw a replacement tile.
  The engine emits a `draw_tile` event immediately with `source: "dead_wall"`.
- `declare_tsumo()` – self-drawn win; updates scores and ends the hand.
- `declare_riichi()` – declare riichi and set `must_tsumogiri`.
- `discard_tile()` – place a tile in the river and set `waiting_for_claims`.
- `declare_ron()` – win on another player's discard.
- `call_pon()` / `call_chi()` – claim the discard to form a meld.
- `skip()` – pass on the discard; once all players skip, the next player draws.

This sequence matches the engine logic around lines 164–528 of `mahjong_engine.py`.
