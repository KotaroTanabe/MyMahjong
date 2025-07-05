from click.testing import CliRunner

from cli.main import cli


def test_start_command_runs() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["start", "A", "B", "C", "D"])
    assert result.exit_code == 0
    assert "Game started" in result.output
    assert "Game ended" in result.output


def test_join_command_placeholder() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["join"])
    assert result.exit_code == 0
    assert "not implemented" in result.output
