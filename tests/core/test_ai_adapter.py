from core.ai_adapter import game_state_to_json, send_state_to_ai
from core.models import GameState, Tile
from core.mortal_runner import MortalAI
from core.player import Player
from core.wall import Wall
import json


class DummyAI(MortalAI):
    def __init__(self) -> None:
        self.sent_messages: list[str] = []

    def send(self, message: str) -> None:  # type: ignore[override]
        self.sent_messages.append(message)


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
