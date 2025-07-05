from click.testing import CliRunner

from cli.main import cli


def test_start_command_runs() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["start", "A", "B", "C", "D"])
    assert result.exit_code == 0
    assert "Game started" in result.output
    assert "Game ended" in result.output


def test_start_command_remote(monkeypatch) -> None:
    def fake_create(server: str, players: list[str]) -> dict:
        return {"players": [{"name": p} for p in players]}

    monkeypatch.setattr("cli.remote_game.create_game", fake_create)
    runner = CliRunner()
    result = runner.invoke(cli, ["start", "A", "B", "-s", "http://host"])
    assert result.exit_code == 0
    assert "Remote game created" in result.output


def test_join_command_remote(monkeypatch) -> None:
    def fake_get(server: str, game_id: int) -> dict:
        return {"players": [{"name": "A"}, {"name": "B"}]}

    monkeypatch.setattr("cli.remote_game.get_game", fake_get)
    runner = CliRunner()
    result = runner.invoke(cli, ["join", "1", "-s", "http://host"])
    assert result.exit_code == 0
    assert "Joined game 1" in result.output


def test_draw_command_remote(monkeypatch) -> None:
    def fake_draw(server: str, game_id: int, player_index: int) -> dict:
        return {"suit": "m", "value": 5}

    monkeypatch.setattr("cli.remote_game.draw_tile", fake_draw)
    runner = CliRunner()
    result = runner.invoke(cli, ["draw", "1", "0", "-s", "http://host"])
    assert result.exit_code == 0
    assert "drew m5" in result.output


def test_health_command_remote(monkeypatch) -> None:
    def fake_health(server: str) -> dict:
        return {"status": "ok"}

    monkeypatch.setattr("cli.remote_game.check_health", fake_health)
    runner = CliRunner()
    result = runner.invoke(cli, ["health", "-s", "http://host"])
    assert result.exit_code == 0
    assert "Server status: ok" in result.output
