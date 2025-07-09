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


def test_auto_play_turn_after_chi_no_draw() -> None:
    state = api.start_game(["A", "B", "C", "D"])
    engine = api._engine
    assert engine is not None
    engine.pop_events()
    discarder = 0
    caller = 1
    chi_tile = models.Tile("man", 1)
    engine.state.players[discarder].hand.tiles = [chi_tile] * 14
    engine.state.current_player = discarder
    api.discard_tile(discarder, chi_tile)
    engine.pop_events()
    engine.state.players[caller].hand.tiles = [
        models.Tile("man", 2),
        models.Tile("man", 3),
        *([models.Tile("pin", 1)] * 11),
    ]
    api.call_chi(caller, [models.Tile("man", 2), models.Tile("man", 3)])
    engine.pop_events()
    api.auto_play_turn(caller)
    events = engine.pop_events()
    assert [e.name for e in events] == ["discard"]
    assert len(engine.state.players[caller].hand.tiles) == 10


def test_auto_play_turn_after_pon_no_draw() -> None:
    state = api.start_game(["A", "B", "C", "D"])
    engine = api._engine
    assert engine is not None
    engine.pop_events()
    discarder = 0
    caller = 2
    pon_tile = models.Tile("pin", 5)
    engine.state.players[discarder].hand.tiles = [pon_tile] * 14
    engine.state.current_player = discarder
    api.discard_tile(discarder, pon_tile)
    engine.pop_events()
    engine.state.players[caller].hand.tiles = [
        pon_tile,
        pon_tile,
        *([models.Tile("sou", 1)] * 11),
    ]
    api.call_pon(caller, [pon_tile, pon_tile, pon_tile])
    engine.pop_events()
    api.auto_play_turn(caller)
    events = engine.pop_events()
    assert [e.name for e in events] == ["discard"]
    assert len(engine.state.players[caller].hand.tiles) == 10


def test_auto_play_turn_after_kan_no_extra_draw() -> None:
    state = api.start_game(["A", "B", "C", "D"])
    engine = api._engine
    assert engine is not None
    engine.pop_events()
    caller = 0
    kan_tile = models.Tile("sou", 5)
    engine.state.players[caller].hand.tiles = [kan_tile] * 4 + [models.Tile("man", 1)] * 10
    api.call_kan(caller, [kan_tile] * 4)
    # events: draw_tile from dead wall then meld
    engine.pop_events()
    api.auto_play_turn(caller)
    events = engine.pop_events()
    assert [e.name for e in events] == ["discard"]
    assert len(engine.state.players[caller].hand.tiles) == 10

