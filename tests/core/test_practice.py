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
    tiles = [Tile("man", 1), Tile("pin", 2)]
    monkeypatch.setattr(practice.random, "choice", lambda seq: seq[-1])
    tile = practice.suggest_discard(tiles)
    assert tile == tiles[-1]
