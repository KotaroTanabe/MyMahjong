from core import api, models


def test_allowed_actions_cache_invalidated_on_discard() -> None:
    state = api.start_game(["A", "B", "C", "D"])
    _ = api.get_allowed_actions(0)

    discard = models.Tile("man", 2)
    state.players[0].hand.tiles = [discard]
    api.discard_tile(0, discard)
    state.players[1].hand.tiles = [models.Tile("man", 1), models.Tile("man", 3)]

    actions = api.get_allowed_actions(1)
    assert "chi" in actions and "skip" in actions

