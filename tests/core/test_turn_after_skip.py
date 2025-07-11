from core.mahjong_engine import MahjongEngine


def test_turn_advances_after_all_players_skip() -> None:
    engine = MahjongEngine()
    engine.pop_events()  # clear start_game/start_kyoku

    discarder = engine.state.dealer
    tile = engine.state.players[discarder].hand.tiles[-1]
    engine.discard_tile(discarder, tile)

    engine.skip((discarder + 1) % 4)
    engine.skip((discarder + 2) % 4)
    engine.skip((discarder + 3) % 4)

    next_player = (discarder + 1) % 4
    drawn = engine.state.players[next_player].hand.tiles[-1]
    engine.discard_tile(next_player, drawn)

    names = [e.name for e in engine.event_history[-7:]]
    assert names == [
        "discard",
        "skip",
        "skip",
        "skip",
        "claims_closed",
        "draw_tile",
        "discard",
    ]
    assert engine.state.current_player == (next_player + 1) % 4
