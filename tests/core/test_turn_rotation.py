import pytest
from core.mahjong_engine import MahjongEngine
from core.exceptions import NotYourTurnError


def test_draw_advances_turn() -> None:
    engine = MahjongEngine()
    current = engine.state.current_player
    engine.state.players[current].hand.tiles.pop()
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
    current = engine.state.current_player
    wrong_player = (current + 1) % len(engine.state.players)
    with pytest.raises(NotYourTurnError) as exc:
        engine.draw_tile(wrong_player)
    assert (
        str(exc.value)
        == f"Player {wrong_player} attempted draw on player {current}'s turn"
    )


def test_discard_out_of_turn_raises_error() -> None:
    engine = MahjongEngine()
    current = engine.state.current_player
    wrong_player = (current + 1) % len(engine.state.players)
    tile = engine.state.players[wrong_player].hand.tiles[0]
    with pytest.raises(NotYourTurnError) as exc:
        engine.discard_tile(wrong_player, tile)
    assert (
        str(exc.value)
        == f"Player {wrong_player} attempted discard on player {current}'s turn"
    )
