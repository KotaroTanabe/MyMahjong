import click

from .local_game import run_game


@click.group()
def cli() -> None:
    """MyMahjong command line interface."""


@cli.command()
@click.argument("players", nargs=-1)
def start(players: tuple[str, ...]) -> None:
    """Start a local game with the given PLAYERS."""
    if not players:
        players = ("You", "AI1", "AI2", "AI3")
    run_game(list(players))


@cli.command()
def join() -> None:
    """Join an existing game (not implemented)."""
    click.echo("Join command is not implemented yet.")


if __name__ == "__main__":
    cli()
