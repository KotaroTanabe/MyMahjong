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
    riichi: bool = False
    seat_wind: str = "east"
    must_tsumogiri: bool = False

    def draw(self, tile: Tile) -> None:
        """Add a tile to the player's hand."""
        self.hand.tiles.append(tile)

    def discard(self, tile: Tile) -> None:
        """Remove a tile from the player's hand and add it to the river."""
        try:
            # prefer to remove by object identity to avoid accidentally
            # discarding a different tile with the same suit/value
            idx = next(i for i, t in enumerate(self.hand.tiles) if t is tile)
            self.hand.tiles.pop(idx)
        except StopIteration:
            # fall back to equality-based removal for backward compatibility
            self.hand.tiles.remove(tile)
        self.river.append(tile)

    def has_open_melds(self) -> bool:
        """Return ``True`` if the player has chi, pon or open kan melds."""
        return any(
            meld.type in {"chi", "pon", "kan", "added_kan"}
            for meld in self.hand.melds
        )

    def declare_riichi(self) -> None:
        """Declare riichi and pay the 1000 point stick."""
        if self.riichi:
            return
        self.score -= 1000
        self.riichi = True
        self.must_tsumogiri = True
