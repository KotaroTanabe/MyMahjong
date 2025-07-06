"""Very basic AI helpers."""
from __future__ import annotations

from .mahjong_engine import MahjongEngine
from .models import Tile


def tsumogiri_turn(engine: MahjongEngine, player_index: int) -> Tile:
    """Draw and immediately discard a tile for ``player_index``."""
    tile = engine.draw_tile(player_index)
    hand = engine.state.players[player_index].hand.tiles
    if tile in hand:
        engine.discard_tile(player_index, tile)
    return tile
