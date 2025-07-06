from core import api, models
import pytest


def test_auto_play_turn_respects_ai_players() -> None:
    state = api.start_game(["A", "B", "C", "D"])
    tile = models.Tile("man", 1)
    # give player 0 a simple hand with the discard tile last
    state.players[0].hand.tiles = [models.Tile("sou", 1)] * 13 + [tile]
    for p in state.players[1:]:
        p.hand.tiles = [models.Tile("pin", (i % 9) + 1) for i in range(13)]
    api.discard_tile(0, tile)
    assert state.waiting_for_claims
    with pytest.raises(ValueError):
        api.auto_play_turn(1, ai_players=[1, 3])
    assert state.waiting_for_claims == [2]
