from core import api, models
from core.shanten_quiz import calculate_shanten


HAND_14 = [
    models.Tile("man", 1), models.Tile("man", 2), models.Tile("man", 3),
    models.Tile("pin", 1), models.Tile("pin", 2), models.Tile("pin", 3),
    models.Tile("sou", 1), models.Tile("sou", 2), models.Tile("sou", 3),
    models.Tile("man", 7), models.Tile("man", 8), models.Tile("man", 9),
    models.Tile("pin", 9), models.Tile("sou", 9),
]


def test_auto_play_turn_discards_without_increasing_shanten() -> None:
    state = api.start_game(["A", "B", "C", "D"])
    player = state.current_player
    state.players[player].hand.tiles = HAND_14.copy()
    before = calculate_shanten(state.players[player].hand.tiles)

    discarded = api.auto_play_turn(player)

    after = calculate_shanten(state.players[player].hand.tiles)
    assert after <= before
    assert discarded == state.players[player].river[-1]
    assert state.current_player == (player + 1) % 4

