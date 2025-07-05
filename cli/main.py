import click

from . import remote_game
from .local_game import run_game


@click.group()
def cli() -> None:
    """MyMahjong command line interface."""


@cli.command()
@click.argument("players", nargs=-1)
@click.option("--server", "server", "-s", help="Base URL of remote server")
def start(players: tuple[str, ...], server: str | None) -> None:
    """Start a game with the given PLAYERS."""
    if not players:
        players = ("You", "AI1", "AI2", "AI3")
    if server:
        data = remote_game.create_game(server, list(players))
        names = ", ".join(p["name"] for p in data.get("players", []))
        click.echo(f"Remote game created with players: {names}")
        return
    run_game(list(players))


@cli.command()
@click.argument("game_id", type=int)
@click.option(
    "--server",
    "server",
    "-s",
    required=True,
    help="Base URL of remote server",
)
def join(game_id: int, server: str) -> None:
    """Join an existing remote game."""
    data = remote_game.get_game(server, game_id)
    names = ", ".join(p["name"] for p in data.get("players", []))
    click.echo(f"Joined game {game_id} with players: {names}")


@cli.command()
@click.argument("game_id", type=int)
@click.argument("player_index", type=int)
@click.option(
    "--server",
    "server",
    "-s",
    required=True,
    help="Base URL of remote server",
)
def draw(game_id: int, player_index: int, server: str) -> None:
    """Draw a tile for PLAYER_INDEX in a remote game."""
    tile = remote_game.draw_tile(server, game_id, player_index)
    click.echo(f"Player {player_index} drew {tile['suit']}{tile['value']}")


@cli.command()
@click.option(
    "--server",
    "server",
    "-s",
    required=True,
    help="Base URL of remote server",
)
def health(server: str) -> None:
    """Check remote server health."""
    data = remote_game.check_health(server)
    status = data.get("status", "unknown")
    click.echo(f"Server status: {status}")


if __name__ == "__main__":
    cli()
