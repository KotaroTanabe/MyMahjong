from __future__ import annotations

from dataclasses import asdict

from fastapi import FastAPI

from core.mahjong_engine import MahjongEngine

app = FastAPI()

_engine = MahjongEngine()


@app.get("/health")
def health() -> dict[str, str]:
    """Simple health check endpoint."""
    return {"status": "ok"}


@app.get("/games/{game_id}")
def get_game(game_id: int) -> dict:
    """Return basic game state for the given game id."""
    # For now we ignore game_id and return the singleton engine state
    return asdict(_engine.state)
