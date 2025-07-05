"""Simple MJAI protocol adapter.

This module converts :class:`GameState` objects into JSON messages and sends
them to an AI process. Only the minimal pieces required for local play are
implemented. Full protocol support will be added incrementally.
"""

from __future__ import annotations

import json
from dataclasses import asdict

from .models import GameState
from .mortal_runner import MortalAI


def game_state_to_json(state: GameState) -> str:
    """Return a JSON string representation of the game state."""

    return json.dumps(asdict(state))


def send_state_to_ai(state: GameState, ai: MortalAI) -> None:
    """Serialize ``state`` and send it to ``ai``."""

    message = game_state_to_json(state)
    ai.send(message)
