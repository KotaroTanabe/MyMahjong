"""Tile wall management."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from .models import Tile


@dataclass
class Wall:
    """Represents the tile wall and dora indicators."""

    tiles: List[Tile] = field(default_factory=list)

    def draw_tile(self) -> Tile:
        """Draw and return the next tile from the wall."""
        return self.tiles.pop()
