"""Simple automated local game loop."""
from __future__ import annotations

import click

from core import api


def run_game(players: list[str]) -> None:
    """Run an automated local game."""
    state = api.start_game(players)
    players_display = ', '.join(p.name for p in state.players)
    click.echo(f"Game started with players: {players_display}")
    start_round = state.round_number
    start_honba = state.honba
    while (
        state.wall
        and state.wall.remaining_tiles > 0
        and state.round_number == start_round
        and state.honba == start_honba
    ):
        player_index = state.current_player
        name = state.players[player_index].name
        tile = api.auto_play_turn()
        click.echo(f"{name} drew {tile.suit}{tile.value} and discarded it")
    api.end_game()
    click.echo("Game ended")
