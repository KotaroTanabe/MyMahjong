from core.mahjong_engine import MahjongEngine
from core.models import Tile


def test_four_kans_triggers_ryukyoku() -> None:
    engine = MahjongEngine()
    engine.pop_events()
    engine.state.kan_count = 3
    tiles = [Tile("man", 1) for _ in range(4)]
    engine.state.players[0].hand.tiles = tiles.copy()
    engine.call_kan(0, tiles)
    names = [e.name for e in engine.pop_events()]
    assert "ryukyoku" in names
    assert engine.state.honba == 1
    assert engine.state.kan_count == 0


def test_nine_terminals_triggers_ryukyoku() -> None:
    engine = MahjongEngine()
    engine.pop_events()
    player = engine.state.players[1]
    player.hand.tiles = [
        Tile("man", 1),
        Tile("man", 9),
        Tile("pin", 1),
        Tile("pin", 9),
        Tile("sou", 1),
        Tile("sou", 9),
        Tile("wind", 1),
        Tile("wind", 2),
        Tile("man", 2),
        Tile("man", 3),
        Tile("man", 4),
        Tile("man", 5),
        Tile("man", 6),
    ]
    engine.state.wall.tiles.append(Tile("dragon", 1))
    engine.state.current_player = 1
    engine.draw_tile(1)
    events = engine.pop_events()
    assert any(
        e.name == "ryukyoku" and e.payload.get("reason") == "nine_terminals"
        for e in events
    )
    assert engine.state.honba == 1


def _set_tenpai_hand(player) -> None:
    player.hand.tiles = [
        Tile("man", 1), Tile("man", 1),
        Tile("man", 2), Tile("man", 2),
        Tile("man", 3), Tile("man", 3),
        Tile("pin", 4), Tile("pin", 4),
        Tile("pin", 5), Tile("pin", 5),
        Tile("sou", 6), Tile("sou", 6),
        Tile("sou", 7), Tile("sou", 8),
    ]


def test_four_riichi_triggers_ryukyoku() -> None:
    engine = MahjongEngine()
    engine.pop_events()
    for p in engine.state.players:
        _set_tenpai_hand(p)
    for i in range(4):
        engine.declare_riichi(i)
    events = engine.pop_events()
    assert any(
        e.name == "ryukyoku" and e.payload.get("reason") == "four_riichi"
        for e in events
    )
    assert engine.state.honba == 1


def test_four_winds_triggers_ryukyoku() -> None:
    engine = MahjongEngine()
    engine.pop_events()
    engine.state.players[0].hand.tiles[-1] = Tile("wind", 1)
    east0 = engine.state.players[0].hand.tiles[-1]
    engine.discard_tile(0, east0)
    engine.skip(1)
    engine.skip(2)
    engine.skip(3)
    engine.state.players[1].hand.tiles[-1] = Tile("wind", 1)
    east1 = engine.state.players[1].hand.tiles[-1]
    engine.discard_tile(1, east1)
    engine.skip(2)
    engine.skip(3)
    engine.skip(0)
    engine.state.players[2].hand.tiles[-1] = Tile("wind", 1)
    east2 = engine.state.players[2].hand.tiles[-1]
    engine.discard_tile(2, east2)
    engine.skip(3)
    engine.skip(0)
    engine.skip(1)
    engine.state.players[3].hand.tiles[-1] = Tile("wind", 1)
    east3 = engine.state.players[3].hand.tiles[-1]
    engine.discard_tile(3, east3)
    engine.skip(0)
    engine.skip(1)
    engine.skip(2)
    events = engine.pop_events()
    assert any(
        e.name == "ryukyoku" and e.payload.get("reason") == "four_winds"
        for e in events
    )
    assert engine.state.honba == 1

