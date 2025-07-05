from core import api, models


def test_start_game() -> None:
    state = api.start_game(["A", "B", "C", "D"])
    assert len(state.players) == 4
    assert state.players[0].name == "A"


def test_start_game_deals_hands() -> None:
    state = api.start_game(["A", "B", "C", "D"])
    counts = [len(p.hand.tiles) for p in state.players]
    assert all(c == 13 for c in counts)


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


def test_call_pon() -> None:
    state = api.start_game(["A", "B", "C", "D"])
    tiles = [models.Tile("pin", 1) for _ in range(3)]
    player = state.players[0]
    player.hand.tiles.extend(tiles[:2])
    api.call_pon(0, tiles)
    assert len(player.hand.melds) == 1
    assert player.hand.melds[0].type == "pon"


def test_end_game_creates_new_state() -> None:
    state = api.start_game(["A", "B", "C", "D"])
    finished = api.end_game()
    assert finished is state
    new_state = api.start_game(["E", "F", "G", "H"])
    assert new_state is not state


def test_declare_riichi_api() -> None:
    state = api.start_game(["A", "B", "C", "D"])
    player = state.players[0]
    score = player.score
    api.declare_riichi(0)
    assert player.riichi
    assert player.score == score - 1000


def test_start_kyoku_api() -> None:
    api.start_game(["A", "B", "C", "D"])
    state = api.start_kyoku(2, 3)
    assert state.dealer == 2
    assert state.round_number == 3
