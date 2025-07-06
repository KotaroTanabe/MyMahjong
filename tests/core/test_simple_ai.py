from core import api, models
import random


def test_auto_play_turn_discards_best_tile(monkeypatch) -> None:
    state = api.start_game(["A", "B", "C", "D"])
    player = state.current_player
    actor = state.players[player]
    actor.hand.tiles = [
        models.Tile("man", 1), models.Tile("man", 2), models.Tile("man", 3),
        models.Tile("man", 4), models.Tile("man", 5), models.Tile("man", 6),
        models.Tile("man", 7), models.Tile("man", 8), models.Tile("man", 9),
        models.Tile("pin", 1), models.Tile("pin", 2), models.Tile("pin", 3),
        models.Tile("sou", 7), models.Tile("sou", 9),
    ]
    monkeypatch.setattr(random, "choice", lambda seq: seq[0])

    discarded = api.auto_play_turn()

    assert discarded.suit == "sou" and discarded.value == 7
    assert discarded == actor.river[-1]
    assert len(actor.hand.tiles) == 13
    assert state.current_player == (player + 1) % 4

