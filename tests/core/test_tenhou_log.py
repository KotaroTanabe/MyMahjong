from core.mahjong_engine import MahjongEngine
from core.tenhou_log import events_to_tenhou_json, mjai_log_to_tenhou_json
import json
from dataclasses import asdict, is_dataclass


def test_events_to_tenhou_json_basic() -> None:
    engine = MahjongEngine()
    tile = engine.state.players[0].hand.tiles[0]
    engine.declare_tsumo(0, tile)
    engine.end_game()
    data = json.loads(events_to_tenhou_json(engine.pop_events()))
    assert data["name"][0] == "Player 0"
    assert data["rule"]["disp"] == "MyMahjong"
    assert len(data["log"]) == 1
    kyoku = data["log"][0]
    assert kyoku[0] == [0, 0, 0]
    assert kyoku[-1][0] == "和了"


def test_tenhou_log_includes_all_starting_hands() -> None:
    engine = MahjongEngine()
    tile = engine.state.players[0].hand.tiles[0]
    engine.declare_tsumo(0, tile)
    engine.end_game()
    data = json.loads(events_to_tenhou_json(engine.pop_events()))
    kyoku = data["log"][0]
    # After the meta arrays we expect four starting hand arrays
    hands = kyoku[4:8]
    assert len(hands[0]) in {13, 14}
    assert all(len(hand) == 13 for hand in hands[1:])


def test_mjai_log_conversion() -> None:
    engine = MahjongEngine()
    tile = engine.state.players[0].hand.tiles[0]
    engine.declare_tsumo(0, tile)
    engine.end_game()
    events = engine.pop_events()

    tenhou_direct = events_to_tenhou_json(events)

    def encode(obj):
        if is_dataclass(obj) and not isinstance(obj, type):
            return {k: encode(v) for k, v in asdict(obj).items()}
        if isinstance(obj, dict):
            return {k: encode(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [encode(v) for v in obj]
        return obj

    lines = []
    for e in events:
        payload = {"type": e.name, **encode(e.payload)}
        lines.append(json.dumps(payload, ensure_ascii=False))

    tenhou_from_mjai = mjai_log_to_tenhou_json(lines)

    assert json.loads(tenhou_direct) == json.loads(tenhou_from_mjai)
