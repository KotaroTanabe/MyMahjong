from click.testing import CliRunner

from cli.main import cli
from core import shanten_quiz, models


def test_shanten_quiz_command(monkeypatch):
    hand = [models.Tile("man", 1) for _ in range(13)]
    monkeypatch.setattr(shanten_quiz, "generate_hand", lambda: hand)
    monkeypatch.setattr(shanten_quiz, "calculate_shanten", lambda h: 1)
    runner = CliRunner()
    result = runner.invoke(cli, ["shanten-quiz"], input="1\n")
    assert result.exit_code == 0
    assert "Hand:" in result.output
    assert "Correct!" in result.output
