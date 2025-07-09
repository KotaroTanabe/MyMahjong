from core.mahjong_engine import MahjongEngine


def test_bankruptcy_triggers_end_game() -> None:
    engine = MahjongEngine()
    engine.pop_events()
    engine.state.players[1].score = 0
    tile = engine.state.players[0].hand.tiles[0]
    engine.declare_tsumo(0, tile)
    events = engine.pop_events()
    names = [e.name for e in events]
    assert names == ["tsumo", "end_game"]
    end_event = events[-1]
    assert end_event.payload.get("reason") == "bankruptcy"


def test_advance_hand_bankruptcy() -> None:
    engine = MahjongEngine()
    engine.pop_events()
    engine.state.players[0].score = -100
    engine.advance_hand(None)
    events = engine.pop_events()
    assert [e.name for e in events] == ["end_game"]
