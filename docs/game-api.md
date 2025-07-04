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
| `GameState`| Aggregated state of an ongoing game.  |

## Commands (GUI/CLI -> Core)

| Command            | Arguments                               | Purpose |
| ------------------ | --------------------------------------- | ------- |
| `start_game`       | list of player names                    | Begin a new hanchan. Returns `GameState`. |
| `draw_tile`        | `player_index`                          | Draw the next tile for a player. |
| `discard_tile`     | `player_index`, `Tile`                  | Discard a tile from the player's hand. |
| `call_chi`         | `player_index`, `tiles`                 | Call `chi` using the given tiles. |
| `call_pon`         | `player_index`, `tiles`                 | Call `pon` using the given tiles. |
| `call_kan`         | `player_index`, `tiles`                 | Declare an open or closed `kan`. |
| `declare_ron`      | `player_index`, `Tile`                  | Win on another player's discard. |
| `declare_tsumo`    | `player_index`, `Tile`                  | Win on self-drawn tile. |
| `skip`             | `player_index`                          | Pass on an action. |
| `end_game`         | none                                    | Terminate the current game. |
| `get_state`        | none                                    | Retrieve the current `GameState`. |

## Events (Core -> GUI/CLI)

When actions are processed the engine emits events that front ends and AIs can
consume. Events closely resemble the MJAI protocol so that adapters can
translate them directly.

| Event              | Data                                    | Notes |
| ------------------ | --------------------------------------- | ----- |
| `start_game`       | `GameState`                             | Sent once at the beginning. |
| `start_kyoku`      | dealer seat and round number            | Signals the start of a hand. |
| `draw_tile`        | `player_index`, `Tile`                  | Tile drawn from the wall. |
| `discard`          | `player_index`, `Tile`                  | Tile placed into the river. |
| `meld`             | `player_index`, `Meld`                  | Meld call (chi/pon/kan). |
| `riichi`           | `player_index`                          | Player declares riichi. |
| `tsumo`            | `player_index`, `HandResponse`, scores  | Self-drawn win. |
| `ron`              | `player_index`, `HandResponse`, scores  | Win on discard. |
| `ryukyoku`         | reason                                  | Hand ends in draw. |
| `end_game`         | final scores                            | Sent after the last hand. |

Front ends are expected to update their displays or AI processes whenever an
event is received.  The low level transport (function call, WebSocket, etc.) is
left to each interface implementation.

