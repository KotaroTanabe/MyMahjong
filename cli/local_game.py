"""Simple automated local game loop."""
from __future__ import annotations

import click

from core import api


def run_game(players: list[str]) -> None:
    """Run an automated local game."""
    state = api.start_game(players)
    players_display = ', '.join(p.name for p in state.players)
    click.echo(f"Game started with players: {players_display}")
    turn = 0
    while state.wall and state.wall.remaining_tiles > 0:
        tile = api.draw_tile(turn)
        name = state.players[turn].name
        click.echo(f"{name} drew {tile.suit}{tile.value}")
        api.discard_tile(turn, tile)
        click.echo(f"{name} discarded {tile.suit}{tile.value}")
        turn = (turn + 1) % len(state.players)
    api.end_game()
    click.echo("Game ended")
