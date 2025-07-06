from core import api, models


def test_get_next_actions_autodraw() -> None:
    state = api.start_game(["A", "B", "C", "D"])
    api._engine.state.current_player = 1  # type: ignore[assignment]
    p = state.players[1]
    p.hand.tiles = [models.Tile("man", i + 1) for i in range(9)] + [
        models.Tile("pin", i + 1) for i in range(4)
    ]
    p.riichi = True
    tile = models.Tile("sou", 9)
    state.wall.tiles = [tile]
    idx, actions = api.get_next_actions()
    assert isinstance(idx, int)
    assert isinstance(actions, list)
