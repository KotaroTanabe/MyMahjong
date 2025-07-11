from core.actions import DRAW, DISCARD, START_KYOKU
import pytest
from core import api, models


def test_apply_action_draw_discard() -> None:
    state = api.start_game(["A", "B", "C", "D"])
    assert state.wall is not None
    tile = models.Tile(suit="sou", value=9)
    state.wall.tiles.append(tile)
    state.players[0].hand.tiles.pop()
    draw = models.GameAction(type=DRAW, player_index=0)
    result = api.apply_action(draw)
    assert result == tile
    discard = models.GameAction(type=DISCARD, player_index=0, tile=tile)
    api.apply_action(discard)
    assert tile in state.players[0].river


def test_apply_action_unknown() -> None:
    api.start_game(["A", "B", "C", "D"])
    action = models.GameAction(type="foo", player_index=0)
    with pytest.raises(ValueError):
        api.apply_action(action)


def test_apply_action_start_kyoku() -> None:
    api.start_game(["A", "B", "C", "D"])
    action = models.GameAction(type=START_KYOKU, dealer=1, round_number=2)
    api.apply_action(action)
    state = api.get_state()
    assert state.dealer == 1
    assert state.round_number == 2
    assert state.seat_winds == ["north", "east", "south", "west"]
