"""Mahjong game engine wrapper."""
from __future__ import annotations

from .models import GameState, Tile, Meld
from .player import Player
from .wall import Wall
from mahjong.hand_calculating.hand_response import HandResponse


class MahjongEngine:
    """Simplified engine that wraps the `mahjong` library."""

    def __init__(self) -> None:
        self.state = GameState(wall=Wall())
        self.state.players = [Player(name=f"Player {i}") for i in range(4)]
        self.deal_initial_hands()

    def deal_initial_hands(self) -> None:
        """Deal 13 tiles to each player at the start of the game."""
        assert self.state.wall is not None
        for _ in range(13):
            for player in self.state.players:
                player.draw(self.state.wall.draw_tile())

    @property
    def remaining_tiles(self) -> int:
        """Number of tiles left in the wall."""
        assert self.state.wall is not None
        return self.state.wall.remaining_tiles

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

    def call_chi(self, player_index: int, tiles: list[Tile]) -> None:
        """Form a chi meld using the given tiles."""
        assert len(tiles) == 3, "Chi requires three tiles"
        player = self.state.players[player_index]
        for t in tiles:
            if t in player.hand.tiles:
                player.hand.tiles.remove(t)
        player.hand.melds.append(Meld(tiles=tiles, type="chi"))

    def call_pon(self, player_index: int, tiles: list[Tile]) -> None:
        """Form a pon meld using the given tiles."""
        assert len(tiles) == 3, "Pon requires three tiles"
        player = self.state.players[player_index]
        for t in tiles:
            if t in player.hand.tiles:
                player.hand.tiles.remove(t)
        player.hand.melds.append(Meld(tiles=tiles, type="pon"))

    def call_kan(self, player_index: int, tiles: list[Tile]) -> None:
        """Form a kan meld using the given tiles."""
        assert len(tiles) == 4, "Kan requires four tiles"
        player = self.state.players[player_index]
        for t in tiles:
            if t in player.hand.tiles:
                player.hand.tiles.remove(t)
        player.hand.melds.append(Meld(tiles=tiles, type="kan"))

    def declare_tsumo(self, player_index: int, win_tile: Tile) -> HandResponse:
        """Declare a self-drawn win and return scoring info."""
        return self.calculate_score(player_index, win_tile)

    def declare_ron(self, player_index: int, win_tile: Tile) -> HandResponse:
        """Declare a win on another player's discard."""
        return self.calculate_score(player_index, win_tile)

    def skip(self, player_index: int) -> None:
        """Skip action for the specified player."""
        _ = player_index  # currently no-op

    def end_game(self) -> GameState:
        """Reset the engine and return the final state."""
        final_state = self.state
        self.state = GameState(wall=Wall())
        self.state.players = [Player(name=f"Player {i}") for i in range(4)]
        return final_state
