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
    """Represents the live wall plus dead wall, wanpai, and dora indicators."""

    tiles: List[Tile] = field(default_factory=list)
    dead_wall: List[Tile] = field(default_factory=list)
    dora_indicators: List[Tile] = field(default_factory=list)
    wanpai_size: int = 14

    def __post_init__(self) -> None:
        if not self.tiles:
            self.reset()

    def reset(self) -> None:
        """Fill the wall with a freshly shuffled standard tile set."""
        self.tiles = create_standard_wall()
        # Reserve the last 14 tiles as the dead wall
        self.dead_wall = [self.tiles.pop() for _ in range(14)]
        # Reveal the 5th tile from the end of the dead wall as the
        # dora indicator
        if len(self.dead_wall) >= 5:
            self.dora_indicators = [self.dead_wall[-5]]
        else:
            self.dora_indicators = []

    @property
    def remaining_yama_tiles(self) -> int:
        """Tiles left that can still be drawn this hand."""
        return max(len(self.tiles) - self.wanpai_size, 0)

    @property
    def remaining_tiles(self) -> int:
        """Return the number of tiles left in the wall."""
        return len(self.tiles)

    def draw_tile(self) -> Tile:
        """Draw and return the next tile from the wall."""
        return self.tiles.pop()
