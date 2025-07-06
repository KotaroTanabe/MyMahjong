import pytest

from core.ai_adapter import (
    game_state_to_json,
    json_to_game_state,
    send_state_to_ai,
    event_to_json,
    json_to_event,
    send_event_to_ai,
    action_to_json,
    json_to_action,
    receive_action,
    validate_action,
)
from core import models
from core.models import GameState, Tile, GameEvent
from core.ai_runner import ExternalAI
from core.player import Player
from core.wall import Wall
import json


class DummyAI(ExternalAI):
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

    restored = json_to_game_state(game_state_to_json(state))
    assert restored.players[0].name == "A"


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
    msg = event_to_json(event)
    data = json.loads(msg)
    assert data["type"] == "draw_tile"
    assert data["tile"]["value"] == 1
    restored = json_to_event(msg)
    assert restored.name == "draw_tile"


def test_json_to_action() -> None:
    msg = '{"type": "discard", "tile": {"suit": "pin", "value": 3}}'
    action = json_to_action(msg)
    assert isinstance(action, models.GameAction)
    assert action.type == "discard"
    assert action.tile and action.tile.value == 3


def test_action_to_json_roundtrip() -> None:
    action = models.GameAction(
        type="discard",
        player_index=0,
        tile=models.Tile("pin", 5),
    )
    msg = action_to_json(action)
    restored = json_to_action(msg)
    assert restored.type == "discard"
    assert restored.tile and restored.tile.value == 5


def test_send_and_receive_event() -> None:
    ai = DummyAI()
    event = GameEvent(
        name="end_game",
        payload={"scores": [25000, 24000, 23000, 26000]},
    )
    send_event_to_ai(event, ai)
    received = receive_action(ai)
    assert received.type == "end_game"
    assert received.tile is None
    assert received.tiles is None


def test_start_game_event_roundtrip() -> None:
    state = GameState(players=[Player(name="P")])
    event = GameEvent(name="start_game", payload={"state": state})
    msg = event_to_json(event)
    restored = json_to_event(msg)
    assert restored.name == "start_game"
    rst_state = restored.payload["state"]
    assert isinstance(rst_state, GameState)
    assert rst_state.players[0].name == "P"


def test_meld_event_roundtrip() -> None:
    meld = models.Meld(
        tiles=[Tile("man", 1), Tile("man", 2), Tile("man", 3)], type="chi"
    )
    event = GameEvent(name="meld", payload={"player_index": 0, "meld": meld})
    msg = event_to_json(event)
    restored = json_to_event(msg)
    assert restored.name == "meld"
    assert restored.payload["meld"].type == "chi"


def test_meld_action_roundtrip() -> None:
    action = models.GameAction(
        type="pon",
        player_index=1,
        tiles=[Tile("sou", 7), Tile("sou", 7), Tile("sou", 7)],
    )
    msg = action_to_json(action)
    restored = json_to_action(msg)
    assert restored.type == "pon"
    assert restored.tiles and len(restored.tiles) == 3


def test_validate_action_errors() -> None:
    with pytest.raises(ValueError):
        validate_action(models.GameAction(type="discard", player_index=0))
    with pytest.raises(ValueError):
        validate_action(models.GameAction(type="foo"))
