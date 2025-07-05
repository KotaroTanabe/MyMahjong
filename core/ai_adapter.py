"""Simple MJAI protocol adapter.

This module converts :class:`GameState` objects into JSON messages and sends
them to an AI process. Only the minimal pieces required for local play are
implemented. Full protocol support will be added incrementally.
"""

from __future__ import annotations

import json
from dataclasses import asdict

from .models import GameEvent, GameState
from .mortal_runner import MortalAI


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
