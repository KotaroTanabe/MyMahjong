"""MJAI protocol adapter helpers.

This module converts :class:`GameState`, :class:`GameEvent` and
``GameAction`` instances to and from the JSON messages understood by
MJAI compatible engines. Earlier versions only provided basic
serialization. The functions below now support full round–trip
conversion so external AIs can be used for practice mode or as players
in the future.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from typing import Any

from .models import GameAction, GameEvent, GameState, Tile, Meld, Hand
from .player import Player
from .wall import Wall
from .ai_runner import ExternalAI


def _decode_tile(d: dict[str, Any]) -> Tile:
    return Tile(**d)


def _decode_meld(d: dict[str, Any]) -> Meld:
    return Meld(tiles=[_decode_tile(t) for t in d["tiles"]], type=d["type"])


def _decode_hand(d: dict[str, Any]) -> Hand:
    tiles = [_decode_tile(t) for t in d.get("tiles", [])]
    melds = [_decode_meld(m) for m in d.get("melds", [])]
    return Hand(tiles=tiles, melds=melds)


def _decode_player(d: dict[str, Any]) -> Player:
    return Player(
        name=d.get("name", ""),
        hand=_decode_hand(d.get("hand", {})),
        score=d.get("score", 25000),
        river=[_decode_tile(t) for t in d.get("river", [])],
        riichi=d.get("riichi", False),
        seat_wind=d.get("seat_wind", "east"),
    )


def _decode_wall(d: dict[str, Any]) -> Wall:
    return Wall(
        tiles=[_decode_tile(t) for t in d.get("tiles", [])],
        dead_wall=[_decode_tile(t) for t in d.get("dead_wall", [])],
        dora_indicators=[_decode_tile(t) for t in d.get("dora_indicators", [])],
        wanpai_size=d.get("wanpai_size", 14),
    )


def _decode_state(d: dict[str, Any]) -> GameState:
    wall_data = d.get("wall")
    wall = _decode_wall(wall_data) if wall_data else None
    return GameState(
        players=[_decode_player(p) for p in d.get("players", [])],
        wall=wall,
        dora_indicators=[_decode_tile(t) for t in d.get("dora_indicators", [])],
        dead_wall=[_decode_tile(t) for t in d.get("dead_wall", [])],
        current_player=d.get("current_player", 0),
        dealer=d.get("dealer", 0),
        round_number=d.get("round_number", 1),
        honba=d.get("honba", 0),
        riichi_sticks=d.get("riichi_sticks", 0),
        seat_winds=d.get("seat_winds", []),
        last_discard=_decode_tile(d["last_discard"]) if d.get("last_discard") else None,
        last_discard_player=d.get("last_discard_player"),
    )


def _encode(obj: Any) -> Any:
    """Recursively convert dataclasses for JSON serialization."""

    if hasattr(obj, "__dataclass_fields__"):
        return {k: _encode(v) for k, v in asdict(obj).items()}
    if isinstance(obj, list):
        return [_encode(v) for v in obj]
    return obj


def game_state_to_json(state: GameState) -> str:
    """Return a JSON string representation of the game state."""

    return json.dumps(_encode(state))


def send_state_to_ai(state: GameState, ai: ExternalAI) -> None:
    """Serialize ``state`` and send it to ``ai``."""

    message = game_state_to_json(state)
    ai.send(message)


def json_to_game_state(message: str) -> GameState:
    """Parse ``message`` into a :class:`GameState`."""

    data = json.loads(message)
    return _decode_state(data)


def event_to_json(event: GameEvent) -> str:
    """Return a JSON message describing ``event``."""

    payload = {"type": event.name}
    payload.update({k: _encode(v) for k, v in event.payload.items()})
    return json.dumps(payload)


def json_to_event(message: str) -> GameEvent:
    """Deserialize an MJAI event message."""

    def decode(value: Any) -> Any:
        if isinstance(value, dict):
            if "suit" in value and "value" in value:
                return _decode_tile(value)
            if "tiles" in value and "type" in value:
                return _decode_meld(value)
            if "players" in value:
                return _decode_state(value)
            return {k: decode(v) for k, v in value.items()}
        if isinstance(value, list):
            return [decode(v) for v in value]
        return value

    data = json.loads(message)
    if "type" not in data:
        raise ValueError("Missing event type")
    name = data.pop("type")
    payload = {k: decode(v) for k, v in data.items()}
    return GameEvent(name=name, payload=payload)


def send_event_to_ai(event: GameEvent, ai: ExternalAI) -> None:
    """Serialize ``event`` and send it to ``ai``."""

    ai.send(event_to_json(event))


def action_to_json(action: GameAction) -> str:
    """Serialize a :class:`GameAction` for sending to the AI."""

    return json.dumps(_encode(action))


def json_to_action(message: str) -> GameAction:
    """Parse a JSON-encoded AI action message."""

    data = json.loads(message)
    tile = data.get("tile")
    tiles = data.get("tiles")
    return GameAction(
        type=data["type"],
        player_index=data.get("player_index"),
        tile=_decode_tile(tile) if tile else None,
        tiles=[_decode_tile(t) for t in tiles] if tiles else None,
        dealer=data.get("dealer"),
        round_number=data.get("round_number"),
    )


def receive_action(ai: ExternalAI) -> GameAction:
    """Receive and deserialize a JSON action from ``ai``."""

    return json_to_action(ai.receive())


def validate_action(action: GameAction) -> None:
    """Ensure ``action`` has required fields for its type."""

    required: dict[str, list[str]] = {
        "draw": ["player_index"],
        "discard": ["player_index", "tile"],
        "chi": ["player_index", "tiles"],
        "pon": ["player_index", "tiles"],
        "kan": ["player_index", "tiles"],
        "riichi": ["player_index"],
        "tsumo": ["player_index", "tile"],
        "ron": ["player_index", "tile"],
        "skip": ["player_index"],
        "start_kyoku": ["dealer", "round_number"],
        "end_game": [],
    }
    if action.type not in required:
        raise ValueError(f"Unknown action type: {action.type}")
    for field in required[action.type]:
        if getattr(action, field) is None:
            raise ValueError(f"Missing required field {field} for {action.type}")
