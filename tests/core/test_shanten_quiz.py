from core import shanten_quiz, models


def test_generate_hand(monkeypatch):
    class DummyPlayer:
        def __init__(self) -> None:
            self.hand = models.Hand(tiles=[models.Tile("man", 1) for _ in range(14)])

    class DummyState:
        def __init__(self) -> None:
            self.players = [DummyPlayer()]

    class DummyEngine:
        def __init__(self) -> None:
            self.state = DummyState()

        def pop_events(self) -> None:
            pass

    monkeypatch.setattr(shanten_quiz, "ENGINE_CLASS", DummyEngine)
    hand = shanten_quiz.generate_hand()
    assert len(hand) == 13


def test_calculate_shanten(monkeypatch):
    called = {}

    class DummyShanten:
        def calculate_shanten(self, counts: list[int]) -> int:
            called["counts"] = counts
            return 2

    monkeypatch.setattr(shanten_quiz, "Shanten", DummyShanten)
    hand = [models.Tile("man", 1) for _ in range(13)]
    value = shanten_quiz.calculate_shanten(hand)
    assert value == 2
    assert called["counts"][0] == 13


def test_is_tenpai_helper(monkeypatch) -> None:
    class DummyShanten:
        def calculate_shanten(self, counts: list[int]) -> int:
            # Return 0 when a specific count is passed to simulate tenpai
            return 0 if counts[0] == 14 else 1

    monkeypatch.setattr(shanten_quiz, "Shanten", DummyShanten)
    tiles = [models.Tile("man", 1) for _ in range(14)]
    assert shanten_quiz.is_tenpai(tiles, [])
    assert not shanten_quiz.is_tenpai(tiles[:-1], [])
