from click.testing import CliRunner

from cli.main import cli
from core import models, api
from core import player as player_module


def test_shanten_command_remote(monkeypatch) -> None:
    def fake_get(server: str, game_id: int) -> dict:
        return {
            "players": [
                {"hand": {"tiles": [{"suit": "man", "value": 1} for _ in range(13)], "melds": []}}
            ]
        }

    monkeypatch.setattr("cli.remote_game.get_game", fake_get)
    monkeypatch.setattr(api, "calculate_shanten", lambda h: 2)
    runner = CliRunner()
    result = runner.invoke(cli, ["shanten", "1", "0", "-s", "http://host"])
    assert result.exit_code == 0
    assert "Shanten: 2" in result.output


def test_shanten_command_local(monkeypatch) -> None:
    player = player_module.Player(name="A")
    player.hand.tiles = [models.Tile("man", 1) for _ in range(13)]
    state = models.GameState(players=[player])
    monkeypatch.setattr(api, "get_state", lambda: state)
    monkeypatch.setattr(api, "calculate_shanten", lambda h: 3)
    runner = CliRunner()
    result = runner.invoke(cli, ["shanten", "1", "0"])
    assert result.exit_code == 0
    assert "Shanten: 3" in result.output
