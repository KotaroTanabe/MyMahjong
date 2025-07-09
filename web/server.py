from __future__ import annotations

from dataclasses import asdict

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
import asyncio
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from core import api, models, shanten_quiz
from core.models import GameEvent

app = FastAPI()
# very small in-memory id tracker until multi-game support exists
_next_game_id = 1
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
    max_rounds: int | None = None


class SuggestRequest(BaseModel):
    """Request body for AI discard suggestion."""

    hand: list[dict]


@app.get("/health")
def health() -> dict[str, str]:
    """Simple health check endpoint."""
    return {"status": "ok"}


@app.post("/games")
def create_game(req: CreateGameRequest) -> dict:
    """Create a new game and return its id and state."""
    global _next_game_id
    if req.max_rounds is not None:
        state = api.start_game(req.players, max_rounds=req.max_rounds)
    else:
        state = api.start_game(req.players)
    game_id = _next_game_id
    _next_game_id += 1
    return {"id": game_id, **asdict(state)}


@app.get("/games/{game_id}")
def get_game(game_id: int) -> dict:
    """Return basic game state for the given game id."""
    # For now we ignore game_id and return the singleton engine state
    try:
        return asdict(api.get_state())
    except AssertionError:
        raise HTTPException(status_code=404, detail="Game not started")


@app.get("/games/{game_id}/log")
def get_log(game_id: int) -> dict:
    """Return the Tenhou-format log for the current game."""
    _ = game_id  # placeholder for future multi-game support
    try:
        data = api.get_tenhou_log()
    except AssertionError:
        raise HTTPException(status_code=404, detail="Game not started")
    return {"log": data}


@app.get("/games/{game_id}/mjai-log")
def get_mjai_log(game_id: int) -> dict:
    """Return the MJAI-format event log for the current game."""

    _ = game_id  # placeholder for future multi-game support
    try:
        data = api.get_mjai_log()
    except AssertionError:
        raise HTTPException(status_code=404, detail="Game not started")
    return {"log": data}


@app.get("/games/{game_id}/events")
def get_events(game_id: int) -> dict:
    """Return raw event history."""

    _ = game_id  # placeholder for future multi-game support
    try:
        events = [asdict(e) for e in api.get_event_history()]
    except AssertionError:
        raise HTTPException(status_code=404, detail="Game not started")
    return {"events": events}


@app.get("/practice")
def practice_problem() -> dict:
    """Return a random practice problem."""

    problem = api.generate_practice_problem()
    return asdict(problem)


@app.post("/practice/suggest")
def practice_suggest(req: SuggestRequest, ai: bool = False) -> dict:
    """Return AI discard suggestion for the provided hand."""

    hand = [models.Tile(**t) for t in req.hand]
    tile = api.suggest_practice_discard(hand, use_ai=ai)
    return asdict(tile)


class QuizRequest(BaseModel):
    """Request body for shanten quiz check."""

    hand: list[dict]


@app.get("/shanten-quiz")
def shanten_quiz_hand() -> list[dict]:
    """Return a random hand for the shanten quiz."""

    hand = shanten_quiz.generate_hand()
    return [asdict(t) for t in hand]


@app.post("/shanten-quiz/check")
def shanten_quiz_check(req: QuizRequest) -> dict:
    """Return the shanten number for the provided hand."""

    hand = [models.Tile(**t) for t in req.hand]
    value = shanten_quiz.calculate_shanten(hand)
    return {"shanten": value}


@app.get("/games/{game_id}/shanten/{player_index}")
def shanten_number(game_id: int, player_index: int) -> dict:
    """Return the shanten number for ``player_index`` in the current game."""

    _ = game_id  # placeholder for future multi-game support
    try:
        state = api.get_state()
    except AssertionError:
        raise HTTPException(status_code=404, detail="Game not started")
    try:
        tiles = state.players[player_index].hand.tiles
    except IndexError:
        raise HTTPException(status_code=404, detail="Player not found")
    value = api.calculate_shanten(tiles)
    return {"shanten": value}


@app.get("/games/{game_id}/allowed-actions/{player_index}")
def allowed_actions(game_id: int, player_index: int) -> dict:
    """Return allowed actions for ``player_index``."""

    _ = game_id  # placeholder for future multi-game support
    try:
        actions = api.get_allowed_actions(player_index)
    except AssertionError:
        raise HTTPException(status_code=404, detail="Game not started")
    except IndexError:
        raise HTTPException(status_code=404, detail="Player not found")
    return {"actions": actions}


@app.get("/games/{game_id}/allowed-actions")
def allowed_actions_all(game_id: int) -> dict:
    """Return allowed actions for all players."""

    _ = game_id  # placeholder for future multi-game support
    try:
        actions = api.get_all_allowed_actions()
    except AssertionError:
        raise HTTPException(status_code=404, detail="Game not started")
    return {"actions": actions}


@app.get("/games/{game_id}/next-actions")
def next_actions(game_id: int) -> dict:
    """Return the next actor index and their allowed actions."""

    _ = game_id  # placeholder for future multi-game support
    try:
        idx, actions = api.get_next_actions()
    except AssertionError:
        raise HTTPException(status_code=404, detail="Game not started")
    if api._engine is not None:
        evt = GameEvent(name="next_actions", payload={"player_index": idx, "actions": actions})
        api._engine.events.append(evt)
        api._engine.event_history.append(evt)
    return {"player_index": idx, "actions": actions}


class ActionRequest(BaseModel):
    """Request body for game actions."""

    player_index: int
    action: str
    tile: dict | None = None
    tiles: list[dict] | None = None
    ai_type: str | None = None


@app.post("/games/{game_id}/action")
def game_action(game_id: int, req: ActionRequest) -> dict:
    """Perform a simple game action and return its result."""
    _ = game_id  # placeholder for future multi-game support
    try:
        allowed = api.get_allowed_actions(req.player_index)
    except AssertionError:
        raise HTTPException(status_code=404, detail="Game not started")
    except IndexError:
        raise HTTPException(status_code=404, detail="Player not found")
    if req.action in {"chi", "pon", "kan", "riichi", "skip"} and req.action not in allowed:
        raise HTTPException(status_code=409, detail="Action not allowed")
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
        try:
            api.declare_riichi(req.player_index)
        except ValueError as e:
            raise HTTPException(status_code=409, detail=str(e))
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
    if req.action == "auto":
        ai_type = req.ai_type or "simple"
        tile = api.auto_play_turn(
            req.player_index,
            ai_type=ai_type,
            claim_players=[req.player_index],
        )
        return asdict(tile)
    raise HTTPException(status_code=400, detail="Unknown action")


@app.websocket("/ws/{game_id}")
async def game_events(websocket: WebSocket, game_id: int) -> None:
    """Stream game events to the client."""
    _ = game_id  # placeholder for future multi-game support
    await websocket.accept()
    prev_actions: list[list[str]] | None = None
    try:
        # send initial allowed actions if a game is running
        try:
            prev_actions = api.get_all_allowed_actions()
            await websocket.send_json(
                {"name": "allowed_actions", "payload": {"actions": prev_actions}}
            )
        except AssertionError:
            prev_actions = None
        while True:
            try:
                events = api.pop_events()
            except AssertionError:
                events = []
            for event in events:
                await websocket.send_json(asdict(event))
            try:
                actions = api.get_all_allowed_actions()
            except AssertionError:
                actions = None
            if actions is not None and actions != prev_actions:
                prev_actions = actions
                await websocket.send_json(
                    {"name": "allowed_actions", "payload": {"actions": actions}}
                )
            await asyncio.sleep(0.1)
    except WebSocketDisconnect:
        pass
