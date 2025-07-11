from core.actions import CHI
import pytest
from core.mahjong_engine import MahjongEngine
from core.models import Tile
from core.exceptions import InvalidActionError


def test_call_chi_consumes_discard() -> None:
    engine = MahjongEngine()
    discarder = engine.state.players[0]
    caller = engine.state.players[1]
    tile = Tile("man", 3)
    discarder.hand.tiles = [tile]
    caller.hand.tiles = []
    engine.discard_tile(0, tile)
    caller.hand.tiles.extend([Tile("man", 1), Tile("man", 2)])
    engine.call_chi(1, [Tile("man", 1), Tile("man", 2), tile])
    assert len(caller.hand.melds) == 1
    assert caller.hand.melds[0].type == CHI
    assert tile not in discarder.river


def test_call_chi_invalid_missing_tile() -> None:
    engine = MahjongEngine()
    discarder = engine.state.players[0]
    caller = engine.state.players[1]
    tile = Tile("man", 3)
    discarder.hand.tiles = [tile]
    caller.hand.tiles = []
    engine.discard_tile(0, tile)
    caller.hand.tiles.append(Tile("man", 1))
    with pytest.raises(InvalidActionError):
        engine.call_chi(1, [Tile("man", 1), Tile("man", 2), tile])


def test_call_pon_invalid_structure() -> None:
    engine = MahjongEngine()
    discarder = engine.state.players[0]
    caller = engine.state.players[2]
    tile = Tile("sou", 7)
    discarder.hand.tiles = [tile]
    caller.hand.tiles = []
    engine.discard_tile(0, tile)
    caller.hand.tiles.extend([Tile("sou", 7), Tile("sou", 8)])
    with pytest.raises(InvalidActionError):
        engine.call_pon(2, [Tile("sou", 7), Tile("sou", 7), Tile("sou", 8)])


def test_call_kan_insufficient_tiles() -> None:
    engine = MahjongEngine()
    discarder = engine.state.players[0]
    caller = engine.state.players[1]
    tile = Tile("pin", 5)
    discarder.hand.tiles = [tile]
    caller.hand.tiles = []
    engine.discard_tile(0, tile)
    caller.hand.tiles.extend([Tile("pin", 5), Tile("pin", 5)])
    with pytest.raises(InvalidActionError):
        engine.call_kan(1, [Tile("pin", 5), Tile("pin", 5), Tile("pin", 5), tile])
