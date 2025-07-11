"""Simple automated local game loop."""
from __future__ import annotations

import click

from core import api


def run_game(players: list[str], *, max_rounds: int = 8) -> None:
    """Run an automated local game."""
    state = api.start_game(players, max_rounds=max_rounds)
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
        for ev in api.pop_events():
            if ev.name == "ryukyoku":
                reason = ev.payload.get("reason")
                scores = ev.payload.get("scores")
                click.echo(f"\u6d41\u5c40({reason}) \u2192 scores: {scores}")
    if not api.is_game_over():
        api.end_game()
    click.echo("Game ended")
