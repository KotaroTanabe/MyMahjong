from core import api, models, practice


def test_start_game() -> None:
    state = api.start_game(["A", "B", "C", "D"])
    assert len(state.players) == 4
    assert state.players[0].name == "A"


def test_start_game_deals_hands() -> None:
    state = api.start_game(["A", "B", "C", "D"])
    dealer = state.dealer
    counts = [len(p.hand.tiles) for p in state.players]
    assert counts[dealer] == 14
    assert all(counts[i] == 13 for i in range(4) if i != dealer)


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
    tile = models.Tile("pin", 1)
    discarder = state.players[1]
    caller = state.players[0]
    discarder.hand.tiles.append(tile)
    api.discard_tile(1, tile)
    caller.hand.tiles.extend([models.Tile("pin", 1), models.Tile("pin", 1)])
    api.call_pon(0, [models.Tile("pin", 1), models.Tile("pin", 1), tile])
    assert len(caller.hand.melds) == 1
    assert caller.hand.melds[0].type == "pon"


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
    assert state.seat_winds == ["west", "north", "east", "south"]


def test_practice_api_functions(monkeypatch) -> None:
    monkeypatch.setattr(practice.random, "choice", lambda seq: seq[0])
    prob = api.generate_practice_problem()
    assert len(prob.hand) == 14
    tile = api.suggest_practice_discard(prob.hand)
    assert isinstance(tile, models.Tile)


def test_practice_api_external(monkeypatch) -> None:
    prob = practice.PracticeProblem(
        hand=[models.Tile("man", 1) for _ in range(14)],
        dora_indicator=models.Tile("pin", 9),
        seat_wind="east",
    )
    monkeypatch.setattr(practice, "generate_problem", lambda: prob)

    def fake_suggest(hand: list[models.Tile], use_ai: bool = False) -> models.Tile:
        assert use_ai
        return hand[0]

    monkeypatch.setattr(practice, "suggest_discard", fake_suggest)
    tile = api.suggest_practice_discard(prob.hand, use_ai=True)
    assert tile.suit == "man"
