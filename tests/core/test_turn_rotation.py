from core.mahjong_engine import MahjongEngine


def test_draw_advances_turn() -> None:
    engine = MahjongEngine()
    current = engine.state.current_player
    engine.draw_tile(current)
    assert engine.state.current_player == (current + 1) % len(engine.state.players)


def test_discard_advances_turn() -> None:
    engine = MahjongEngine()
    current = engine.state.current_player
    tile = engine.state.players[current].hand.tiles[0]
    engine.discard_tile(current, tile)
    assert engine.state.current_player == (current + 1) % len(engine.state.players)
