from core import api, models


def test_claim_options_removed_after_draw() -> None:
    state = api.start_game(["A", "B", "C", "D"])
    discard = models.Tile("man", 3)
    state.players[0].hand.tiles = [discard]
    api.discard_tile(0, discard)
    state.players[1].hand.tiles = [models.Tile("man", 1), models.Tile("man", 2)]
    actions = api.get_allowed_actions(1)
    assert "chi" in actions
    api.skip(1)
    api.skip(2)
    api.skip(3)
    actions_after = api.get_allowed_actions(1)
    assert "chi" not in actions_after
    assert "pon" not in actions_after
