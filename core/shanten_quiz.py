from __future__ import annotations

"""Helpers for a simple shanten count quiz."""

from mahjong.shanten import Shanten

from typing import TYPE_CHECKING, Any

from .models import Tile, Meld
from .rules import _tile_to_index

if TYPE_CHECKING:  # pragma: no cover - for type checking
    from .mahjong_engine import MahjongEngine
else:  # placeholder for runtime monkeypatching in tests
    MahjongEngine: Any | None = None


def generate_hand() -> list[Tile]:
    """Return a random 13-tile hand for the quiz."""
    from .mahjong_engine import MahjongEngine

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


def is_tenpai(hand_tiles: list[Tile], melds: list[Meld]) -> bool:
    """Return ``True`` if the hand is in tenpai."""

    counts = _hand_counts(hand_tiles)
    shanten = Shanten().calculate_shanten(counts)
    return shanten == 0
