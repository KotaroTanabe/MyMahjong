from __future__ import annotations

from dataclasses import asdict

from fastapi import FastAPI
from pydantic import BaseModel

from core import api

app = FastAPI()


class CreateGameRequest(BaseModel):
    """Request body for creating a new game."""

    players: list[str]


@app.get("/health")
def health() -> dict[str, str]:
    """Simple health check endpoint."""
    return {"status": "ok"}


@app.post("/games")
def create_game(req: CreateGameRequest) -> dict:
    """Create a new game and return its state."""
    state = api.start_game(req.players)
    return asdict(state)


@app.get("/games/{game_id}")
def get_game(game_id: int) -> dict:
    """Return basic game state for the given game id."""
    # For now we ignore game_id and return the singleton engine state
    return asdict(api.get_state())
