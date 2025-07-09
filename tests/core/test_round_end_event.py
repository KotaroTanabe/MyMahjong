from core.mahjong_engine import MahjongEngine
from core.models import Tile


def test_round_end_after_win() -> None:
    engine = MahjongEngine()
    engine.pop_events()
    tile = engine.state.players[0].hand.tiles[0]
    engine.declare_tsumo(0, tile)
    names = [e.name for e in engine.pop_events()]
    assert names == ["tsumo", "round_end", "start_kyoku"]


def test_round_end_after_draw() -> None:
    engine = MahjongEngine()
    engine.pop_events()
    engine.state.wall.tiles = [Tile("pin", 1)]
    engine.draw_tile(engine.state.current_player)
    names = [e.name for e in engine.pop_events()]
    assert names == ["draw_tile", "ryukyoku", "round_end", "start_kyoku"]
