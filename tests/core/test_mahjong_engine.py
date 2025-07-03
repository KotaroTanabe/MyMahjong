from core.mahjong_engine import MahjongEngine
from core.models import Tile


def test_engine_initialization() -> None:
    engine = MahjongEngine()
    assert len(engine.state.players) == 4
    assert engine.state.wall is not None


def test_draw_tile_updates_state() -> None:
    engine = MahjongEngine()
    assert engine.state.wall is not None
    tile = Tile(suit="pin", value=3)
    engine.state.wall.tiles.append(tile)
    engine.draw_tile(0)
    assert tile in engine.state.players[0].hand.tiles
