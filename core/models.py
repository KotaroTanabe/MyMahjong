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
    current_player: int = 0


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
