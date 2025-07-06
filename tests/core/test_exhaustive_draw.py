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

