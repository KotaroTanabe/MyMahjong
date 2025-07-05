from __future__ import annotations

"""Helpers for '何切る問題' practice mode."""

from dataclasses import dataclass
import random

from mahjong.shanten import Shanten

from .rules import _tile_to_index

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
    # The dealer begins with 14 tiles so no initial draw is needed
    hand = engine.state.players[0].hand.tiles.copy()
    if engine.state.wall:
        dora = random.choice(engine.state.wall.tiles)
    else:
        dora = Tile("man", 1)
    seat_wind = random.choice(["east", "south", "west", "north"])
    return PracticeProblem(hand=hand, dora_indicator=dora, seat_wind=seat_wind)


def _hand_counts(hand: list[Tile]) -> list[int]:
    """Return 34-tile count representation of ``hand``."""

    counts = [0] * 34
    for tile in hand:
        counts[_tile_to_index(tile)] += 1
    return counts


def evaluate_discards(hand: list[Tile]) -> list[tuple[Tile, int]]:
    """Return the shanten number for discarding each tile in ``hand``."""

    counts = _hand_counts(hand)
    shanten = Shanten()
    results: list[tuple[Tile, int]] = []

    for tile in hand:
        idx = _tile_to_index(tile)
        counts[idx] -= 1
        value = shanten.calculate_shanten(counts)
        counts[idx] += 1
        results.append((tile, value))

    return results


def suggest_discard(hand: list[Tile]) -> Tile:
    """Return the AI suggested discard using a basic shanten heuristic."""

    evaluations = evaluate_discards(hand)
    best_value = min(val for _, val in evaluations)
    best_tiles = [t for t, v in evaluations if v == best_value]
    return random.choice(best_tiles) if best_tiles else random.choice(hand)
