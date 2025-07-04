from __future__ import annotations

"""Helpers for '何切る問題' practice mode."""

from dataclasses import dataclass
import random

from mahjong.shanten import Shanten

from .rules import _tile_to_index

from .mahjong_engine import MahjongEngine
from .models import Tile
from .ai_adapter import send_state_to_ai, receive_action
from .ai_runner import ExternalAI


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


def suggest_discard(hand: list[Tile], use_ai: bool = False) -> Tile:
    """Return the AI suggested discard.

    If ``use_ai`` is ``True`` this function starts an external AI process
    and sends the practice hand via the MJAI adapter.  The discard returned by
    the AI is used.  Otherwise a simple shanten based heuristic picks the tile.
    """

    if use_ai:
        engine = MahjongEngine()
        engine.pop_events()
        engine.state.players[0].hand.tiles = hand.copy()
        ai = ExternalAI()
        ai.start()
        try:
            send_state_to_ai(engine.state, ai)
            action = receive_action(ai)
            if action.tile is not None:
                return action.tile
        finally:
            ai.stop()

    counts = _hand_counts(hand)
    shanten = Shanten()
    best_tiles: list[Tile] = []
    best_value = 8  # higher than any real shanten number

    for tile in hand:
        idx = _tile_to_index(tile)
        counts[idx] -= 1
        value = shanten.calculate_shanten(counts)
        counts[idx] += 1
        if value < best_value:
            best_value = value
            best_tiles = [tile]
        elif value == best_value:
            best_tiles.append(tile)

    return random.choice(best_tiles) if best_tiles else random.choice(hand)
