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

    def decode_tile(d: dict[str, Any]) -> Tile:
        return Tile(**d)

    def decode_meld(d: dict[str, Any]) -> Meld:
        return Meld(
            tiles=[decode_tile(t) for t in d["tiles"]],
            type=d["type"],
            called_index=d.get("called_index"),
            called_from=d.get("called_from"),
        )

    def decode_hand(d: dict[str, Any]) -> Hand:
        tiles = [decode_tile(t) for t in d.get("tiles", [])]
        melds = [decode_meld(m) for m in d.get("melds", [])]
        return Hand(tiles=tiles, melds=melds)

    def decode_player(d: dict[str, Any]) -> Player:
        return Player(
            name=d.get("name", ""),
            hand=decode_hand(d.get("hand", {})),
            score=d.get("score", 25000),
            river=[decode_tile(t) for t in d.get("river", [])],
            riichi=d.get("riichi", False),
            seat_wind=d.get("seat_wind", "east"),
        )

    wall_data = data.get("wall")
    wall = None
    if wall_data:
        wall = Wall(
            tiles=[decode_tile(t) for t in wall_data.get("tiles", [])],
            dead_wall=[decode_tile(t) for t in wall_data.get("dead_wall", [])],
            dora_indicators=[
                decode_tile(t) for t in wall_data.get("dora_indicators", [])
            ],
            wanpai_size=wall_data.get("wanpai_size", 14),
        )

    state = GameState(
        players=[decode_player(p) for p in data.get("players", [])],
        wall=wall,
        dora_indicators=[decode_tile(t) for t in data.get("dora_indicators", [])],
        dead_wall=[decode_tile(t) for t in data.get("dead_wall", [])],
        current_player=data.get("current_player", 0),
        dealer=data.get("dealer", 0),
        round_number=data.get("round_number", 1),
        seat_winds=data.get("seat_winds", []),
    )
    return state


def event_to_json(event: GameEvent) -> str:
    """Return a JSON message describing ``event``."""

    payload = {"type": event.name}
    payload.update(event.payload)
    return json.dumps(payload)


def json_to_event(message: str) -> GameEvent:
    """Deserialize an MJAI event message."""

    data = json.loads(message)
    if "type" not in data:
        raise ValueError("Missing event type")
    name = data.pop("type")
    return GameEvent(name=name, payload=data)


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
        tile=Tile(**tile) if tile else None,
        tiles=[Tile(**t) for t in tiles] if tiles else None,
        dealer=data.get("dealer"),
        round_number=data.get("round_number"),
    )


def receive_action(ai: ExternalAI) -> GameAction:
    """Receive and deserialize a JSON action from ``ai``."""

    return json_to_action(ai.receive())
