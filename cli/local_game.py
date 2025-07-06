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
    start_round = state.round_number
    start_honba = state.honba
    while (
        state.wall
        and state.wall.remaining_tiles > 0
        and state.round_number == start_round
        and state.honba == start_honba
    ):
        tile = api.draw_tile(turn)
        name = state.players[turn].name
        click.echo(f"{name} drew {tile.suit}{tile.value}")
        try:
            api.discard_tile(turn, tile)
        except ValueError:
            # skip invalid discards if the tile vanished somehow
            pass
        click.echo(f"{name} discarded {tile.suit}{tile.value}")
        turn = (turn + 1) % len(state.players)
    api.end_game()
    click.echo("Game ended")
