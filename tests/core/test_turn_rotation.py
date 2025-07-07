import pytest
from core.mahjong_engine import MahjongEngine


def test_draw_advances_turn() -> None:
    engine = MahjongEngine()
    current = engine.state.current_player
    engine.draw_tile(current)
    assert engine.state.current_player == current


def test_discard_advances_turn() -> None:
    engine = MahjongEngine()
    current = engine.state.current_player
    tile = engine.state.players[current].hand.tiles[0]
    engine.discard_tile(current, tile)
    assert engine.state.current_player == (current + 1) % len(engine.state.players)


def test_draw_out_of_turn_raises_error() -> None:
    engine = MahjongEngine()
    wrong_player = (engine.state.current_player + 1) % len(engine.state.players)
    with pytest.raises(ValueError):
        engine.draw_tile(wrong_player)


def test_discard_out_of_turn_raises_error() -> None:
    engine = MahjongEngine()
    wrong_player = (engine.state.current_player + 1) % len(engine.state.players)
    tile = engine.state.players[wrong_player].hand.tiles[0]
    with pytest.raises(ValueError):
        engine.discard_tile(wrong_player, tile)
