from __future__ import annotations

"""Helpers for a simple shanten count quiz."""

from mahjong.shanten import Shanten

from typing import Any, Type

from .models import Meld, Tile
from .rules import _tile_to_index

# Optional override used by tests to substitute a dummy engine
ENGINE_CLASS: Type[Any] | None = None


def _get_engine() -> Type[Any]:
    """Return the MahjongEngine class or test override."""
    if ENGINE_CLASS is not None:
        return ENGINE_CLASS
    from .mahjong_engine import MahjongEngine
    return MahjongEngine


def generate_hand() -> list[Tile]:
    """Return a random 13-tile hand for the quiz."""
    engine_class = _get_engine()
    engine = engine_class()
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


def is_tenpai(hand_tiles: list[Tile], melds: list[Meld]) -> bool:
    """Return ``True`` if the combined tiles form a tenpai hand."""
    counts = [0] * 34
    for t in hand_tiles:
        counts[_tile_to_index(t)] += 1
    for meld in melds:
        for t in meld.tiles:
            counts[_tile_to_index(t)] += 1
    total = sum(counts)
    if total > 14 and hand_tiles:
        excess = total - 14
        for _ in range(excess):
            counts[_tile_to_index(hand_tiles[-1])] -= 1
    return Shanten().calculate_shanten(counts) == 0
