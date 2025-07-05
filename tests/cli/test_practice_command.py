from click.testing import CliRunner

from cli.main import cli
from core import practice, models


def test_practice_command(monkeypatch):
    hand = [models.Tile("man", 1) for _ in range(14)]
    problem = practice.PracticeProblem(
        hand=hand,
        dora_indicator=models.Tile("pin", 9),
        seat_wind="east",
    )
    monkeypatch.setattr(practice, "generate_problem", lambda: problem)

    def fake_suggest(hand: list[models.Tile], use_ai: bool = False) -> models.Tile:
        return hand[0]

    monkeypatch.setattr(practice, "suggest_discard", fake_suggest)

    runner = CliRunner()
    result = runner.invoke(cli, ["practice"], input="1\n")

    assert result.exit_code == 0
    assert "Seat wind: east" in result.output
    assert "AI suggests discarding m1" in result.output


def test_practice_command_external(monkeypatch):
    hand = [models.Tile("man", 1) for _ in range(14)]
    problem = practice.PracticeProblem(
        hand=hand,
        dora_indicator=models.Tile("pin", 9),
        seat_wind="east",
    )
    monkeypatch.setattr(practice, "generate_problem", lambda: problem)

    called: dict[str, bool] = {"ai": False}

    def fake_suggest(hand: list[models.Tile], use_ai: bool = False) -> models.Tile:
        called["ai"] = use_ai
        return hand[0]

    monkeypatch.setattr(practice, "suggest_discard", fake_suggest)

    runner = CliRunner()
    result = runner.invoke(cli, ["practice", "--ai"], input="1\n")

    assert result.exit_code == 0
    assert called["ai"] is True
