"""Very basic AI helpers."""
from __future__ import annotations

from .mahjong_engine import MahjongEngine
from .models import Tile


def tsumogiri_turn(engine: MahjongEngine, player_index: int) -> Tile:
    """Play a full turn by discarding the drawn tile.

    If the player has already drawn (hand size >= 14), simply discard the last
    tile instead of drawing again. This allows enabling AI mid-turn.
    """

    player = engine.state.players[player_index]
    if len(player.hand.tiles) >= 14:
        tile = player.hand.tiles[-1]
        engine.discard_tile(player_index, tile)
        return tile

    tile = engine.draw_tile(player_index)
    if tile in player.hand.tiles:
        engine.discard_tile(player_index, tile)
    return tile
