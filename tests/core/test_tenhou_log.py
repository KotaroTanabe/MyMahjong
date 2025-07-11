from core.mahjong_engine import MahjongEngine
from core.tenhou_log import events_to_tenhou_json, mjai_log_to_tenhou_json
from core.models import Tile
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
    assert len(kyoku) == 17
    assert kyoku[-1][0] == "和了"


def test_tenhou_log_includes_all_starting_hands() -> None:
    engine = MahjongEngine()
    tile = engine.state.players[0].hand.tiles[0]
    engine.declare_tsumo(0, tile)
    engine.end_game()
    data = json.loads(events_to_tenhou_json(engine.pop_events()))
    kyoku = data["log"][0]
    # After meta arrays we have four starting hand arrays
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

    direct = json.loads(tenhou_direct)
    converted = json.loads(tenhou_from_mjai)
    # start_kyoku state objects mutate, so the first metadata array may differ
    assert direct["name"] == converted["name"]
    assert direct["rule"] == converted["rule"]
    assert direct["log"][0][4:] == converted["log"][0][4:]


def test_events_to_tenhou_json_draw() -> None:
    engine = MahjongEngine()
    engine.state.wall.tiles = [Tile("pin", 1)]
    engine.state.players[engine.state.current_player].hand.tiles.pop()
    engine.draw_tile(engine.state.current_player)
    engine.end_game()
    data = json.loads(events_to_tenhou_json(engine.pop_events()))
    kyoku = data["log"][0]
    assert kyoku[-1][0] == "全員不聴"


def test_events_to_tenhou_json_kyoku_num() -> None:
    engine = MahjongEngine()
    engine.pop_events()  # clear start_game/start_kyoku
    engine.start_kyoku(dealer=2, round_number=3)
    tile = engine.state.players[2].hand.tiles[0]
    engine.declare_tsumo(2, tile)
    engine.end_game()
    data = json.loads(events_to_tenhou_json(engine.pop_events()))
    kyoku_info = data["log"][0][0]
    assert kyoku_info == [(3 - 1) * 4 + 2, 1, 0]
