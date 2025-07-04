"""Mahjong game engine wrapper."""
from __future__ import annotations

from .models import GameState, Tile
from .player import Player
from .wall import Wall
from mahjong.hand_calculating.hand_response import HandResponse


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

    def calculate_score(
        self, player_index: int, win_tile: Tile
    ) -> HandResponse:
        """Return scoring information for the winning hand."""
        from mahjong.tile import TilesConverter
        from mahjong.hand_calculating.hand import HandCalculator
        from mahjong.hand_calculating.hand_config import HandConfig

        def tile_to_index(tile: Tile) -> int:
            if tile.suit == "man":
                return tile.value - 1
            if tile.suit == "pin":
                return 9 + tile.value - 1
            if tile.suit == "sou":
                return 18 + tile.value - 1
            if tile.suit == "wind":
                return 27 + tile.value - 1
            if tile.suit == "dragon":
                return 31 + tile.value - 1
            raise ValueError(f"Unknown suit: {tile.suit}")

        hand_tiles = self.state.players[player_index].hand.tiles
        counts = [0] * 34
        for t in hand_tiles:
            counts[tile_to_index(t)] += 1

        tiles_136 = TilesConverter.to_136_array(counts)
        win_tile_136 = TilesConverter.find_34_tile_in_136_array(
            tile_to_index(win_tile), tiles_136
        )
        assert win_tile_136 is not None, "Winning tile not found in hand"

        calculator = HandCalculator()
        return calculator.estimate_hand_value(
            tiles_136, win_tile_136, config=HandConfig(is_tsumo=True)
        )
