from core import api, models


def test_start_game() -> None:
    state = api.start_game(["A", "B", "C", "D"])
    assert len(state.players) == 4
    assert state.players[0].name == "A"


def test_draw_and_discard() -> None:
    state = api.start_game(["A", "B", "C", "D"])
    assert state.wall is not None
    tile = models.Tile(suit="sou", value=9)
    state.wall.tiles.append(tile)
    drawn = api.draw_tile(0)
    assert drawn == tile
    api.discard_tile(0, tile)
    assert tile in state.players[0].river


def test_get_state() -> None:
    state = api.start_game(["A", "B", "C", "D"])
    assert api.get_state() is state
