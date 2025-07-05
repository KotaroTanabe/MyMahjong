from __future__ import annotations

from dataclasses import asdict

from fastapi import FastAPI, HTTPException
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


class ActionRequest(BaseModel):
    """Request body for game actions."""

    player_index: int
    action: str


@app.post("/games/{game_id}/action")
def game_action(game_id: int, req: ActionRequest) -> dict:
    """Perform a simple game action and return its result."""
    _ = game_id  # placeholder for future multi-game support
    if req.action == "draw":
        tile = api.draw_tile(req.player_index)
        return asdict(tile)
    raise HTTPException(status_code=400, detail="Unknown action")
