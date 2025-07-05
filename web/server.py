from __future__ import annotations

from dataclasses import asdict

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
import asyncio
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from core import api, models

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CreateGameRequest(BaseModel):
    """Request body for creating a new game."""

    players: list[str]


class SuggestRequest(BaseModel):
    """Request body for AI discard suggestion."""

    hand: list[dict]


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


@app.get("/practice")
def practice_problem() -> dict:
    """Return a random practice problem."""

    problem = api.generate_practice_problem()
    return asdict(problem)


@app.post("/practice/suggest")
def practice_suggest(req: SuggestRequest) -> dict:
    """Return AI discard suggestion for the provided hand."""

    hand = [models.Tile(**t) for t in req.hand]
    tile = api.suggest_practice_discard(hand)
    return asdict(tile)


class ActionRequest(BaseModel):
    """Request body for game actions."""

    player_index: int
    action: str
    tile: dict | None = None
    tiles: list[dict] | None = None


@app.post("/games/{game_id}/action")
def game_action(game_id: int, req: ActionRequest) -> dict:
    """Perform a simple game action and return its result."""
    _ = game_id  # placeholder for future multi-game support
    if req.action == "draw":
        try:
            tile = api.draw_tile(req.player_index)
        except IndexError:
            raise HTTPException(status_code=409, detail="Wall is empty")
        return asdict(tile)
    if req.action == "discard" and req.tile:
        tile = models.Tile(**req.tile)
        api.discard_tile(req.player_index, tile)
        return {"status": "ok"}
    if req.action == "chi" and req.tiles:
        tiles = [models.Tile(**t) for t in req.tiles]
        api.call_chi(req.player_index, tiles)
        return {"status": "ok"}
    if req.action == "pon" and req.tiles:
        tiles = [models.Tile(**t) for t in req.tiles]
        api.call_pon(req.player_index, tiles)
        return {"status": "ok"}
    if req.action == "kan" and req.tiles:
        tiles = [models.Tile(**t) for t in req.tiles]
        api.call_kan(req.player_index, tiles)
        return {"status": "ok"}
    if req.action == "riichi":
        api.declare_riichi(req.player_index)
        return {"status": "ok"}
    if req.action == "tsumo" and req.tile:
        tile = models.Tile(**req.tile)
        result = api.declare_tsumo(req.player_index, tile)
        return result.__dict__
    if req.action == "ron" and req.tile:
        tile = models.Tile(**req.tile)
        result = api.declare_ron(req.player_index, tile)
        return result.__dict__
    if req.action == "skip":
        api.skip(req.player_index)
        return {"status": "ok"}
    raise HTTPException(status_code=400, detail="Unknown action")


@app.websocket("/ws/{game_id}")
async def game_events(websocket: WebSocket, game_id: int) -> None:
    """Stream game events to the client."""
    _ = game_id  # placeholder for future multi-game support
    await websocket.accept()
    try:
        while True:
            events = api.pop_events()
            for event in events:
                await websocket.send_json(asdict(event))
            await asyncio.sleep(0.1)
    except WebSocketDisconnect:
        pass
