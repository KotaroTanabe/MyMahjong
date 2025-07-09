# Core <-> Interface API

This document defines the minimal set of commands and events exchanged between the
`core` package and its front ends (CLI and GUI).  The goal is to provide enough
structure for a full "hanchan" when an MJAI-compatible AI participates.

The API does not attempt to mirror every detail of the MJAI protocol. Instead it
abstracts the common actions that a player or AI must perform so the engine can
manage game state consistently.  Messages can be represented as Python dataclasses
or JSON objects when crossing process boundaries.

## Data Model

The following classes defined in `core.models` are used throughout the API:

| Class      | Description                           |
| ---------- | ------------------------------------- |
| `Tile`     | Single tile with `suit` and `value`.  |
| `Meld`     | Collection of tiles forming a meld.   |
| `Hand`     | Player hand consisting of tiles and melds. |
| `Player`   | Seat information including hand and score. |
| `GameState`| Aggregated state of an ongoing game including `max_rounds`.  |

## Commands (GUI/CLI -> Core)

| Command            | Arguments                               | Purpose |
| ------------------ | --------------------------------------- | ------- |
| `start_game`       | list of player names, `max_rounds`=8    | Begin a new game with the specified round limit. Returns `GameState`. |
| `draw_tile`        | `player_index`                          | Draw the next tile for a player. |
| `discard_tile`     | `player_index`, `Tile`                  | Discard a tile from the player's hand. |
| `riichi`           | `player_index`, `Tile`                  | Discard a tile and declare riichi in one step. |
| `call_chi`         | `player_index`, `tiles`                 | Call `chi` using the given tiles. Two hand tiles may be passed and the discard is automatically inserted, or a full meld may be provided. Any discard tile sent by the front end is replaced with the engine's instance. |
| `call_pon`         | `player_index`, `tiles`                 | Call `pon` using the given tiles. |
| `call_kan`         | `player_index`, `tiles`                 | Declare an open or closed `kan`. For an open kan, three hand tiles may be passed and the discard is inserted automatically. Any discard tile sent by the front end is replaced with the engine's instance. |
| `declare_ron`      | `player_index`, `Tile`                  | Win on another player's discard. |
| `declare_tsumo`    | `player_index`, `Tile`                  | Win on self-drawn tile. |
| `skip`             | `player_index`                          | Pass on an action. |
| `auto_play_turn`   | `player_index`, `ai_type`               | Draw and discard using the chosen AI. |
| `end_game`         | none                                    | Terminate the current game. |
| `get_state`        | none                                    | Retrieve the current `GameState`. |
| `get_chi_options`  | `player_index`                          | List possible chi tile pairs for the last discard. |

## Events (Core -> GUI/CLI)

When actions are processed the engine emits events that front ends and AIs can
consume. Events closely resemble the MJAI protocol so that adapters can
translate them directly.

| Event              | Data                                    | Notes |
| ------------------ | --------------------------------------- | ----- |
| `start_game`       | `GameState`                             | Sent once at the beginning. |
| `start_kyoku`      | dealer seat and round number            | Signals the start of a hand. |
| `draw_tile`        | `player_index`, `Tile`, `source`        | Tile drawn from the wall. When emitted after a kan, `source` will be `"dead_wall"`. |
| `discard`          | `player_index`, `Tile`                  | Tile placed into the river. |
| `meld`             | `player_index`, `Meld`                  | Meld call (chi/pon/kan). |
| `claims_closed`    | none                                    | No player called the discard. |
| `riichi`           | `player_index`                          | Player declares riichi after their discard. |
| `tsumo`            | `player_index`, `HandResponse`, scores  | Self-drawn win. |
| `ron`              | `player_index`, `HandResponse`, scores  | Win on discard. |
| `ryukyoku`         | reason                                  | Hand ends in draw. |
| `round_end`        | next dealer and round                   | Fired before the next hand begins. |
| `end_game`         | final scores, reason                    | Sent after the last hand or when a player goes bankrupt. |

The replacement tile drawn after any kan uses this `draw_tile` event so
front ends always receive the tile and know it came from the dead wall.

Front ends are expected to update their displays or AI processes whenever an
event is received.  The low level transport (function call, WebSocket, etc.) is
left to each interface implementation.

