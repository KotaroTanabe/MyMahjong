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


def test_evaluate_discards(monkeypatch):
    hand = [Tile("man", i) for i in range(1, 10)] + [Tile("pin", i) for i in range(1, 5)]

    def fake_calc(self, counts):
        return counts[0]

    monkeypatch.setattr(practice.Shanten, "calculate_shanten", fake_calc)
    results = practice.evaluate_discards(hand)
    assert len(results) == len(hand)
    assert results[0][1] == 0
    assert all(v == 1 for _, v in results[1:])
