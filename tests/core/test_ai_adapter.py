from core.ai_adapter import (
    game_state_to_json,
    send_state_to_ai,
    event_to_json,
    send_event_to_ai,
    json_to_action,
    receive_action,
)
from core.models import GameState, Tile, GameEvent
from core.mortal_runner import MortalAI
from core.player import Player
from core.wall import Wall
import json


class DummyAI(MortalAI):
    def __init__(self) -> None:
        self.sent_messages: list[str] = []

    def send(self, message: str) -> None:  # type: ignore[override]
        self.sent_messages.append(message)

    def receive(self) -> str:  # type: ignore[override]
        return self.sent_messages.pop(0)


def test_game_state_to_json() -> None:
    state = GameState(
        players=[Player(name="A")],
        wall=Wall(tiles=[Tile("man", 1)]),
    )
    data = json.loads(game_state_to_json(state))
    assert data["players"][0]["name"] == "A"
    assert data["wall"]["tiles"][0]["value"] == 1


def test_send_state_to_ai() -> None:
    state = GameState(players=[Player(name="A")])
    ai = DummyAI()
    send_state_to_ai(state, ai)
    assert len(ai.sent_messages) == 1
    assert json.loads(ai.sent_messages[0])["players"][0]["name"] == "A"


def test_event_conversion_roundtrip() -> None:
    event = GameEvent(
        name="draw_tile",
        payload={"player_index": 0, "tile": {"suit": "man", "value": 1}},
    )
    data = json.loads(event_to_json(event))
    assert data["type"] == "draw_tile"
    assert data["tile"]["value"] == 1


def test_json_to_action() -> None:
    msg = '{"type": "discard", "tile": {"suit": "pin", "value": 3}}'
    action = json_to_action(msg)
    assert action["type"] == "discard"
    assert action["tile"]["value"] == 3


def test_send_and_receive_event() -> None:
    ai = DummyAI()
    event = GameEvent(
        name="end_game",
        payload={"scores": [25000, 24000, 23000, 26000]},
    )
    send_event_to_ai(event, ai)
    received = receive_action(ai)
    assert received["type"] == "end_game"
    assert received["scores"] == [25000, 24000, 23000, 26000]

from core.mahjong_engine import MahjongEngine
from core.ai_adapter import apply_action


def test_apply_action_draw_and_discard() -> None:
    engine = MahjongEngine()
    tile = Tile(suit="sou", value=9)
    assert engine.state.wall is not None
    engine.state.wall.tiles.append(tile)

    apply_action({"type": "draw", "player_index": 0}, engine)
    assert tile in engine.state.players[0].hand.tiles

    apply_action(
        {"type": "discard", "player_index": 0, "tile": {"suit": "sou", "value": 9}},
        engine,
    )
    assert tile in engine.state.players[0].river
