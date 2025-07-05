import pytest
from core.mahjong_engine import MahjongEngine
from core.models import Tile


def test_call_closed_kan_draws_replacement_and_dora() -> None:
    engine = MahjongEngine()
    engine.pop_events()
    tiles = [Tile("man", 5) for _ in range(4)]
    engine.state.players[0].hand.tiles = tiles.copy()
    before_dead = len(engine.state.dead_wall)
    before_dora = len(engine.state.dora_indicators)
    engine.call_kan(0, tiles)
    player = engine.state.players[0]
    assert any(m.type == "closed_kan" for m in player.hand.melds)
    assert len(player.hand.tiles) == 1
    assert len(engine.state.dead_wall) == before_dead - 1
    assert len(engine.state.dora_indicators) == before_dora + 1


def test_call_added_kan_upgrades_pon() -> None:
    engine = MahjongEngine()
    discarder = engine.state.players[0]
    caller = engine.state.players[1]
    tile = Tile("sou", 3)
    discarder.hand.tiles = [tile]
    engine.discard_tile(0, tile)
    caller.hand.tiles = [Tile("sou", 3), Tile("sou", 3)]
    engine.call_pon(1, [Tile("sou", 3), Tile("sou", 3), tile])
    extra = Tile("sou", 3)
    caller.hand.tiles.append(extra)
    before_dead = len(engine.state.dead_wall)
    before_dora = len(engine.state.dora_indicators)
    engine.call_kan(1, [Tile("sou", 3)] * 4)
    meld = caller.hand.melds[0]
    assert meld.type == "added_kan"
    assert len(meld.tiles) == 4
    assert len(engine.state.dead_wall) == before_dead - 1
    assert len(engine.state.dora_indicators) == before_dora + 1
