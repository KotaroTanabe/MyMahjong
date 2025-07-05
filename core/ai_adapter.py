"""Simple MJAI protocol adapter.

This module converts :class:`GameState` objects into JSON messages and sends
them to an AI process. Only the minimal pieces required for local play are
implemented. Full protocol support will be added incrementally.
"""

from __future__ import annotations

import json
from dataclasses import asdict

from .models import GameEvent, GameState, Tile
from .mortal_runner import MortalAI
from .mahjong_engine import MahjongEngine


def game_state_to_json(state: GameState) -> str:
    """Return a JSON string representation of the game state."""

    return json.dumps(asdict(state))


def send_state_to_ai(state: GameState, ai: MortalAI) -> None:
    """Serialize ``state`` and send it to ``ai``."""

    message = game_state_to_json(state)
    ai.send(message)


def event_to_json(event: GameEvent) -> str:
    """Return a JSON message describing ``event``."""

    payload = {"type": event.name}
    payload.update(event.payload)
    return json.dumps(payload)


def send_event_to_ai(event: GameEvent, ai: MortalAI) -> None:
    """Serialize ``event`` and send it to ``ai``."""

    ai.send(event_to_json(event))


def json_to_action(message: str) -> dict:
    """Parse a JSON-encoded AI action message."""

    return json.loads(message)


def receive_action(ai: MortalAI) -> dict:
    """Receive a JSON action from ``ai`` and return it as a dict."""

    return json_to_action(ai.receive())


def apply_action(action: dict, engine: "MahjongEngine") -> None:
    """Apply an AI action dict to the given engine."""
    action_type = action.get("type")
    player_index = action.get("player_index", 0)
    if action_type == "draw":
        engine.draw_tile(player_index)
    elif action_type == "discard":
        tile_data = action.get("tile")
        assert tile_data is not None, "discard action requires tile"
        tile = Tile(**tile_data)
        engine.discard_tile(player_index, tile)
    elif action_type == "riichi":
        engine.declare_riichi(player_index)
    elif action_type == "chi":
        tiles = [Tile(**t) for t in action.get("tiles", [])]
        engine.call_chi(player_index, tiles)
    elif action_type == "pon":
        tiles = [Tile(**t) for t in action.get("tiles", [])]
        engine.call_pon(player_index, tiles)
    elif action_type == "kan":
        tiles = [Tile(**t) for t in action.get("tiles", [])]
        engine.call_kan(player_index, tiles)
    elif action_type == "tsumo":
        tile_data = action.get("tile")
        assert tile_data is not None, "tsumo action requires tile"
        tile = Tile(**tile_data)
        engine.declare_tsumo(player_index, tile)
    elif action_type == "ron":
        tile_data = action.get("tile")
        assert tile_data is not None, "ron action requires tile"
        tile = Tile(**tile_data)
        engine.declare_ron(player_index, tile)
    elif action_type == "skip":
        engine.skip(player_index)
    else:
        raise ValueError(f"Unknown action type: {action_type}")
