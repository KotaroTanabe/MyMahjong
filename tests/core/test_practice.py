from core import practice
from core.models import Tile


def test_generate_problem(monkeypatch):
    # make random.choice deterministic
    monkeypatch.setattr(practice.random, "choice", lambda seq: seq[0])
    prob = practice.generate_problem()
    assert len(prob.hand) == 14
    assert isinstance(prob.dora_indicator, Tile)
    assert prob.seat_wind == "east"


def test_suggest_discard(monkeypatch):
    # all tiles equal so algorithm relies on random.choice
    tiles = [Tile("man", 1) for _ in range(14)]
    monkeypatch.setattr(practice.random, "choice", lambda seq: seq[-1])
    tile = practice.suggest_discard(tiles)
    assert tile == tiles[-1]


def test_suggest_discard_external(monkeypatch):
    class DummyAI(practice.ExternalAI):
        def __init__(self) -> None:
            self.messages: list[str] = []

        def start(self) -> None:  # type: ignore[override]
            pass

        def stop(self) -> None:  # type: ignore[override]
            pass

        def send(self, msg: str) -> None:  # type: ignore[override]
            self.messages.append(msg)

        def receive(self) -> str:  # type: ignore[override]
            # always discard first tile
            return '{"type": "discard", "tile": {"suit": "man", "value": 1}}'

    monkeypatch.setattr(practice, "ExternalAI", DummyAI)
    tiles = [Tile("man", 1) for _ in range(14)]
    tile = practice.suggest_discard(tiles, use_ai=True)
    assert isinstance(tile, Tile)
    assert tile.suit == "man" and tile.value == 1
