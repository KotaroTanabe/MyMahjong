import pytest
from core import api, models


def test_auto_play_turn_last_skip_does_not_play_wrong_player() -> None:
    state = api.start_game(["A", "B", "C", "D"])
    engine = api._engine
    assert engine is not None
    engine.pop_events()

    discarder = state.dealer
    tile = models.Tile("man", 1)
    for p in state.players:
        p.hand.tiles = [models.Tile("sou", 9)] * 13
    state.players[discarder].hand.tiles.append(tile)
    api.discard_tile(discarder, tile)
    engine.pop_events()

    api.skip(1)
    api.skip(2)
    api.auto_play_turn(3, claim_players=[3])

    events = engine.pop_events()
    names = [e.name for e in events]
    assert names[0] == "skip"
    assert names[-1] == "draw_tile"
    assert state.current_player == (discarder + 1) % 4
