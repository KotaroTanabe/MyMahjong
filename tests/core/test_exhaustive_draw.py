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

