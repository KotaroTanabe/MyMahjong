from core.actions import SKIP
from core.actions import SKIP
from core import api, models


def test_skip_not_offered_when_no_claims() -> None:
    state = api.start_game(["A", "B", "C", "D"])
    assert state.waiting_for_claims == []
    for i in range(4):
        actions = api.get_allowed_actions(i)
        assert SKIP not in actions


def test_skip_offered_to_all_waiting_players() -> None:
    state = api.start_game(["A", "B", "C", "D"])
    tile = state.players[0].hand.tiles[0]
    api.discard_tile(0, tile)
    for i in range(1, 4):
        assert i in state.waiting_for_claims
        actions = api.get_allowed_actions(i)
        assert SKIP in actions
    assert 0 not in state.waiting_for_claims
    assert SKIP not in api.get_allowed_actions(0)
