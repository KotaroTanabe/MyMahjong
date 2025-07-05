"""Helpers for interacting with the web server."""
from __future__ import annotations

import requests


def create_game(server: str, players: list[str]) -> dict:
    """Create a remote game and return the JSON response."""
    url = f"{server.rstrip('/')}/games"
    resp = requests.post(url, json={"players": players})
    resp.raise_for_status()
    return resp.json()


def get_game(server: str, game_id: int) -> dict:
    """Retrieve the game state for ``game_id`` from the server."""
    url = f"{server.rstrip('/')}/games/{game_id}"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()
