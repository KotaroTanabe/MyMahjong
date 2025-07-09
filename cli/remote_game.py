"""Helpers for interacting with the web server."""
from __future__ import annotations

import requests


def create_game(server: str, players: list[str], *, max_rounds: int | None = None) -> dict:
    """Create a remote game and return the JSON response."""
    url = f"{server.rstrip('/')}/games"
    data: dict[str, object] = {"players": players}
    if max_rounds is not None:
        data["max_rounds"] = max_rounds
    resp = requests.post(url, json=data)
    resp.raise_for_status()
    return resp.json()


def get_game(server: str, game_id: int) -> dict:
    """Retrieve the game state for ``game_id`` from the server."""
    url = f"{server.rstrip('/')}/games/{game_id}"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()


def draw_tile(server: str, game_id: int, player_index: int) -> dict:
    """Draw a tile for ``player_index`` in ``game_id`` and return the tile."""
    url = f"{server.rstrip('/')}/games/{game_id}/action"
    resp = requests.post(
        url, json={"player_index": player_index, "action": "draw"}
    )
    resp.raise_for_status()
    return resp.json()


def check_health(server: str) -> dict:
    """Check the remote server health endpoint."""
    url = f"{server.rstrip('/')}/health"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()
