from core import api, models


def test_auto_play_turn_respects_claim_players() -> None:
    state = api.start_game(["A", "B", "C", "D"])
    discarder = 0
    tile = state.players[discarder].hand.tiles[-1]
    api.discard_tile(discarder, tile)
    assert state.waiting_for_claims == [1, 2, 3]

    api.auto_play_turn(1, claim_players=[1])
    assert state.waiting_for_claims == [2, 3]
