from core.mahjong_engine import MahjongEngine
from core.tenhou_log import events_to_tenhou_json
import json


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
