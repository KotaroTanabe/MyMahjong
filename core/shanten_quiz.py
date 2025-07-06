from __future__ import annotations

"""Helpers for a simple shanten count quiz."""

from mahjong.shanten import Shanten

from .mahjong_engine import MahjongEngine
from .models import Tile
from .rules import _tile_to_index


def generate_hand() -> list[Tile]:
    """Return a random 13-tile hand for the quiz."""
    engine = MahjongEngine()
    engine.pop_events()  # discard start event
    hand = engine.state.players[0].hand.tiles.copy()
    if len(hand) > 13:
        hand = hand[:-1]
    return hand


def _hand_counts(hand: list[Tile]) -> list[int]:
    counts = [0] * 34
    for tile in hand:
        counts[_tile_to_index(tile)] += 1
    return counts


def calculate_shanten(hand: list[Tile]) -> int:
    """Return the shanten number for ``hand``."""
    counts = _hand_counts(hand)
    return Shanten().calculate_shanten(counts)
