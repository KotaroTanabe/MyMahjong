from core import api, models


def test_auto_play_turn_discards_drawn_tile() -> None:
    state = api.start_game(["A", "B", "C", "D"])
    assert state.wall is not None
    tile = models.Tile(suit="man", value=9)
    state.wall.tiles.append(tile)
    player = state.current_player
    hand_len = len(state.players[player].hand.tiles)

    discarded = api.auto_play_turn()

    # With a full hand, the AI should discard without drawing
    assert discarded == state.players[player].river[-1]
    assert len(state.players[player].hand.tiles) == hand_len - 1
    assert state.current_player == (player + 1) % 4

