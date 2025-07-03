"""Player representation for MyMahjong."""
from __future__ import annotations

from dataclasses import dataclass, field

from .models import Hand, Tile


@dataclass
class Player:
    """Represents a seat at the table."""

    name: str
    hand: Hand = field(default_factory=Hand)
    score: int = 25000
    river: list[Tile] = field(default_factory=list)

    def draw(self, tile: Tile) -> None:
        """Add a tile to the player's hand."""
        self.hand.tiles.append(tile)

    def discard(self, tile: Tile) -> None:
        """Remove a tile from the player's hand and add it to the river."""
        self.hand.tiles.remove(tile)
        self.river.append(tile)
