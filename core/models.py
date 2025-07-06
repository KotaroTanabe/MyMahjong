"""Data models used by the core engine."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - used for type checking
    from .player import Player
    from .wall import Wall


@dataclass
class Tile:
    """Represents a single Mahjong tile."""
    suit: str
    value: int

    def is_terminal_or_honor(self) -> bool:
        """Return True if the tile is a terminal or honor."""
        if self.suit in {"wind", "dragon"}:
            return True
        return self.value in {1, 9}


@dataclass
class Meld:
    """Collection of tiles forming a meld (chi, pon, kan)."""
    tiles: List[Tile]
    type: str


@dataclass
class Hand:
    """Player hand consisting of tiles and melds."""
    tiles: List[Tile] = field(default_factory=list)
    melds: List[Meld] = field(default_factory=list)


@dataclass
class GameState:
    """Overall game state placeholder."""

    players: List["Player"] = field(default_factory=list)
    wall: Optional["Wall"] = None
    dora_indicators: List[Tile] = field(default_factory=list)
    dead_wall: List[Tile] = field(default_factory=list)
    current_player: int = 0
    dealer: int = 0
    round_number: int = 1
    honba: int = 0
    riichi_sticks: int = 0
    kan_count: int = 0
    seat_winds: list[str] = field(default_factory=list)
    last_discard: Tile | None = None
    last_discard_player: int | None = None


@dataclass
class GameEvent:
    """Generic event emitted by the Mahjong engine."""

    name: str
    payload: dict[str, Any]


@dataclass
class GameAction:
    """Action issued by a player or AI."""

    type: str
    player_index: int | None = None
    tile: Tile | None = None
    tiles: list[Tile] | None = None
    dealer: int | None = None
    round_number: int | None = None
