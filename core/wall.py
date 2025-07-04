"""Tile wall management."""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import List

from .models import Tile


def create_standard_wall() -> list[Tile]:
    """Return a shuffled list containing the full set of 136 tiles."""
    tiles: list[Tile] = []
    for suit in ("man", "pin", "sou"):
        for value in range(1, 10):
            tiles.extend([Tile(suit=suit, value=value) for _ in range(4)])
    for value in range(1, 5):
        tiles.extend([Tile(suit="wind", value=value) for _ in range(4)])
    for value in range(1, 4):
        tiles.extend([Tile(suit="dragon", value=value) for _ in range(4)])
    random.shuffle(tiles)
    return tiles


@dataclass
class Wall:
    """Represents the tile wall and dora indicators."""

    tiles: List[Tile] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.tiles:
            self.reset()

    def reset(self) -> None:
        """Fill the wall with a freshly shuffled standard tile set."""
        self.tiles = create_standard_wall()

    @property
    def remaining_tiles(self) -> int:
        """Return the number of tiles left in the wall."""
        return len(self.tiles)

    def draw_tile(self) -> Tile:
        """Draw and return the next tile from the wall."""
        return self.tiles.pop()
