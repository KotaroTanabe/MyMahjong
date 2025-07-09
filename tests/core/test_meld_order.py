import pytest
from core import api, models


def test_call_chi_tile_order_from_left() -> None:
    state = api.start_game(["A", "B", "C", "D"])
    tile = models.Tile("man", 3)
    discarder = state.players[1]
    caller = state.players[2]
    discarder.hand.tiles.append(tile)
    state.current_player = 1
    api.discard_tile(1, tile)
    caller.hand.tiles.extend([models.Tile("man", 1), models.Tile("man", 2)])
    api.call_chi(2, [models.Tile("man", 1), models.Tile("man", 2)])
    meld = caller.hand.melds[0]
    assert [t.value for t in meld.tiles] == [3, 1, 2]
    assert meld.called_index == 0
