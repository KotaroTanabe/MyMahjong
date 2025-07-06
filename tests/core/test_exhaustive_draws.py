import pytest
from core.mahjong_engine import MahjongEngine
from core.models import Tile


def test_four_kans_triggers_ryukyoku() -> None:
    engine = MahjongEngine()
    engine.pop_events()
    player = engine.state.players[0]
    player.hand.tiles = (
        [Tile("man", 1)] * 4
        + [Tile("pin", 1)] * 4
        + [Tile("sou", 1)] * 4
        + [Tile("man", 9)] * 4
    )
    engine.call_kan(0, [Tile("man", 1)] * 4)
    engine.call_kan(0, [Tile("pin", 1)] * 4)
    engine.call_kan(0, [Tile("sou", 1)] * 4)
    engine.call_kan(0, [Tile("man", 9)] * 4)
    events = engine.pop_events()
    assert any(
        e.name == "ryukyoku" and e.payload.get("reason") == "four_kans"
        for e in events
    )


def test_four_riichi_triggers_ryukyoku() -> None:
    engine = MahjongEngine()
    engine.pop_events()
    for i in range(4):
        engine.declare_riichi(i)
    events = engine.pop_events()
    assert any(
        e.name == "ryukyoku" and e.payload.get("reason") == "four_riichi"
        for e in events
    )


def test_nine_terminals_triggers_ryukyoku() -> None:
    engine = MahjongEngine()
    engine.pop_events()
    tiles = [
        Tile("man", 1),
        Tile("man", 9),
        Tile("pin", 1),
        Tile("pin", 9),
        Tile("sou", 1),
        Tile("sou", 9),
        Tile("wind", 1),
        Tile("wind", 2),
        Tile("dragon", 1),
    ] + [Tile("man", 2)] * 5
    engine.state.players[0].hand.tiles = tiles
    engine.abort_nine_terminals(0)
    events = engine.pop_events()
    assert any(
        e.name == "ryukyoku" and e.payload.get("reason") == "nine_terminals"
        for e in events
    )
