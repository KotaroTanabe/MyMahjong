from core import mahjong_engine, player, wall, ai_adapter, models


def test_module_imports() -> None:
    assert mahjong_engine is not None
    assert player is not None
    assert wall is not None
    assert ai_adapter is not None
    assert models is not None


def test_basic_classes() -> None:
    engine = mahjong_engine.MahjongEngine()
    assert len(engine.state.players) == 4
    tile = models.Tile(suit="man", value=1)
    assert engine.state.wall is not None
    engine.state.wall.tiles.append(tile)
    drawn = engine.draw_tile(0)
    assert drawn == tile
