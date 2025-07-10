import json
import pytest

from core.mahjong_engine import MahjongEngine
from core.tenhou_log import events_to_tenhou_json
from core.tenhou_validator import validate_tenhou, ValidationError


def test_validator_accepts_generated_log() -> None:
    engine = MahjongEngine()
    tile = engine.state.players[0].hand.tiles[0]
    engine.declare_tsumo(0, tile)
    engine.end_game()
    data = json.loads(events_to_tenhou_json(engine.pop_events()))
    validate_tenhou(data)


def test_validator_rejects_bad_tile_code() -> None:
    bad = {
        "title": ["", ""],
        "name": ["a", "b", "c", "d"],
        "rule": {"disp": "x", "aka": 0},
        "log": [
            [
                [0, 0, 0],
                [25000, 25000, 25000, 25000],
                [11],
                [],
                [11], 12, 99,
                ["流局"],
            ]
        ],
    }
    with pytest.raises(ValidationError):
        validate_tenhou(bad)


