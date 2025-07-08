from core.mahjong_engine import MahjongEngine


def test_claims_closed_event_after_all_skip() -> None:
    engine = MahjongEngine()
    discarder = engine.state.dealer
    next_player = (discarder + 1) % 4
    tile = engine.state.players[discarder].hand.tiles[-1]

    engine.discard_tile(discarder, tile)
    engine.skip(next_player)
    engine.skip((discarder + 2) % 4)
    engine.skip((discarder + 3) % 4)

    names = [e.name for e in engine.event_history[-3:]]
    assert names[-2:] == ["claims_closed", "draw_tile"]
