from __future__ import annotations

"""Helpers for '何切る問題' practice mode."""

from dataclasses import dataclass
import random

from .mahjong_engine import MahjongEngine
from .models import Tile


@dataclass
class PracticeProblem:
    """Scenario presented to the player."""

    hand: list[Tile]
    dora_indicator: Tile
    seat_wind: str


def generate_problem() -> PracticeProblem:
    """Return a practice scenario with a random hand, seat wind and dora."""

    engine = MahjongEngine()
    engine.pop_events()  # discard start event
    engine.draw_tile(0)
    hand = engine.state.players[0].hand.tiles.copy()
    if engine.state.wall:
        dora = random.choice(engine.state.wall.tiles)
    else:
        dora = Tile("man", 1)
    seat_wind = random.choice(["east", "south", "west", "north"])
    return PracticeProblem(hand=hand, dora_indicator=dora, seat_wind=seat_wind)


def suggest_discard(hand: list[Tile]) -> Tile:
    """Return the AI suggested discard. Placeholder implementation."""

    return random.choice(hand)
