import pytest
from core import api, models


def test_apply_action_draw_discard() -> None:
    state = api.start_game(["A", "B", "C", "D"])
    assert state.wall is not None
    tile = models.Tile(suit="sou", value=9)
    state.wall.tiles.append(tile)
    draw = models.GameAction(type="draw", player_index=0)
    result = api.apply_action(draw)
    assert result == tile
    discard = models.GameAction(type="discard", player_index=0, tile=tile)
    api.apply_action(discard)
    assert tile in state.players[0].river


def test_apply_action_unknown() -> None:
    api.start_game(["A", "B", "C", "D"])
    action = models.GameAction(type="foo", player_index=0)
    with pytest.raises(ValueError):
        api.apply_action(action)
