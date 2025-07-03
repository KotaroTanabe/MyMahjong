"""Mahjong game engine wrapper."""
from __future__ import annotations

from .models import GameState, Tile
from .player import Player
from .wall import Wall


class MahjongEngine:
    """Simplified engine that wraps the `mahjong` library."""

    def __init__(self) -> None:
        self.state = GameState(wall=Wall())
        self.state.players = [Player(name=f"Player {i}") for i in range(4)]

    def draw_tile(self, player_index: int) -> Tile:
        """Draw a tile for the specified player."""
        assert self.state.wall is not None
        tile = self.state.wall.draw_tile()
        self.state.players[player_index].draw(tile)
        return tile

    def discard_tile(self, player_index: int, tile: Tile) -> None:
        """Discard a tile from the specified player's hand."""
        self.state.players[player_index].discard(tile)
