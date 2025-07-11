from __future__ import annotations

from dataclasses import asdict

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
import asyncio
import logging
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from core import api, models, shanten_quiz
from core.models import GameEvent

app = FastAPI()
_ws_connections: set[WebSocket] = set()
logger = logging.getLogger(__name__)


class GameActionError(Exception):
    """Raised when a game action cannot be performed."""


def handle_conflict(func):
    """Convert ``GameActionError`` to an HTTP 409 error with logging."""

    def wrapper(game_id: int, req: "ActionRequest"):
        try:
            return func(game_id, req)
        except GameActionError as err:
            _raise_conflict(req.player_index, req.action, str(err))

    return wrapper


def _raise_conflict(player_index: int, action: str, detail: str) -> None:
    """Log a conflict and raise an HTTP 409 error."""
    logger.info(
        "409 conflict: player %s attempted %s -> %s",
        player_index,
        action,
        detail,
    )
    raise HTTPException(status_code=409, detail=detail)
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


class StartKyokuRequest(BaseModel):
    """Request body for starting a new hand."""

    dealer: int
    round: int


@app.get("/health")
def health() -> dict[str, str]:
    """Simple health check endpoint."""
    return {"status": "ok"}


@app.post("/games")
def create_game(req: CreateGameRequest) -> dict:
    """Create a new game and return its id and state."""
    if req.max_rounds is not None:
        game_id, state = api.manager.create_game(
            req.players, max_rounds=req.max_rounds
        )
    else:
        game_id, state = api.manager.create_game(req.players)
    return {"id": game_id, **asdict(state)}


@app.get("/games/{game_id}")
def get_game(game_id: int) -> dict:
    """Return basic game state for the given game id."""
    try:
        state = api.manager.get_state(game_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Game not started")
    return asdict(state)


@app.get("/games/{game_id}/log")
def get_log(game_id: int) -> dict:
    """Return the Tenhou-format log for the current game."""
    try:
        data = api.manager.get_tenhou_log(game_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Game not started")
    return {"log": data}


@app.get("/games/{game_id}/mjai-log")
def get_mjai_log(game_id: int) -> dict:
    """Return the MJAI-format event log for the current game."""

    try:
        data = api.manager.get_mjai_log(game_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Game not started")
    return {"log": data}


@app.get("/games/{game_id}/events")
def get_events(game_id: int) -> dict:
    """Return raw event history."""

    try:
        events = [asdict(e) for e in api.manager.get_event_history(game_id)]
    except KeyError:
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
    try:
        state = api.manager.get_state(game_id)
    except KeyError:
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
    try:
        actions = api.manager.get_allowed_actions(game_id, player_index)
    except KeyError:
        raise HTTPException(status_code=404, detail="Game not started")
    except IndexError:
        raise HTTPException(status_code=404, detail="Player not found")
    return {"actions": actions}


@app.get("/games/{game_id}/chi-options/{player_index}")
def chi_options(game_id: int, player_index: int) -> dict:
    """Return chi tile pairs for ``player_index``."""

    try:
        options = api.manager.get_chi_options(game_id, player_index)
    except KeyError:
        raise HTTPException(status_code=404, detail="Game not started")
    except IndexError:
        raise HTTPException(status_code=404, detail="Player not found")

    def dump(pair: list[models.Tile]) -> list[dict]:
        return [asdict(t) for t in pair]

    return {"options": [dump(o) for o in options]}


@app.get("/games/{game_id}/allowed-actions")
def allowed_actions_all(game_id: int) -> dict:
    """Return allowed actions for all players."""
    try:
        actions = api.manager.get_all_allowed_actions(game_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Game not started")
    return {"actions": actions}


@app.get("/games/{game_id}/next-actions")
def next_actions(game_id: int) -> dict:
    """Return the next actor index and their allowed actions."""

    try:
        idx, actions = api.manager.get_next_actions(game_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Game not started")
    api.record_next_actions(game_id, idx, actions)
    return {"player_index": idx, "actions": actions}


@app.post("/games/{game_id}/start-kyoku")
async def start_kyoku_route(game_id: int, req: StartKyokuRequest) -> dict:
    """Start a new hand and notify connected clients."""
    try:
        state = api.manager.start_kyoku(game_id, req.dealer, req.round)
    except KeyError:
        raise HTTPException(status_code=404, detail="Game not started")

    event = {
        "name": "start_kyoku",
        "payload": {
            "dealer": req.dealer,
            "round": req.round,
            "state": asdict(state),
        },
    }
    for ws in list(_ws_connections):
        try:
            await ws.send_json(event)
        except Exception:
            pass
    return event


class ActionRequest(BaseModel):
    """Request body for game actions."""

    player_index: int
    action: str
    tile: dict | None = None
    tiles: list[dict] | None = None
    ai_type: str | None = None


@handle_conflict
def _draw(game_id: int, req: ActionRequest) -> dict:
    try:
        tile = api.manager.draw_tile(game_id, req.player_index)
    except IndexError:
        raise GameActionError("Wall is empty")
    except ValueError as err:
        raise GameActionError(str(err))
    return asdict(tile)


@handle_conflict
def _discard(game_id: int, req: ActionRequest) -> dict:
    if not req.tile:
        raise GameActionError("Tile required")
    tile = models.Tile(**req.tile)
    try:
        api.manager.discard_tile(game_id, req.player_index, tile)
    except ValueError as err:
        raise GameActionError(str(err))
    return {"status": "ok"}


@handle_conflict
def _chi(game_id: int, req: ActionRequest) -> dict:
    if not req.tiles:
        raise GameActionError("Tiles required")
    tiles = [models.Tile(**t) for t in req.tiles]
    try:
        api.manager.call_chi(game_id, req.player_index, tiles)
    except ValueError as err:
        raise GameActionError(str(err))
    return {"status": "ok"}


@handle_conflict
def _pon(game_id: int, req: ActionRequest) -> dict:
    if not req.tiles:
        raise GameActionError("Tiles required")
    tiles = [models.Tile(**t) for t in req.tiles]
    try:
        api.manager.call_pon(game_id, req.player_index, tiles)
    except ValueError as err:
        raise GameActionError(str(err))
    return {"status": "ok"}


@handle_conflict
def _kan(game_id: int, req: ActionRequest) -> dict:
    if not req.tiles:
        raise GameActionError("Tiles required")
    tiles = [models.Tile(**t) for t in req.tiles]
    try:
        api.manager.call_kan(game_id, req.player_index, tiles)
    except ValueError as err:
        raise GameActionError(str(err))
    return {"status": "ok"}


@handle_conflict
def _riichi(game_id: int, req: ActionRequest) -> dict:
    if not req.tile:
        raise GameActionError("Tile required")
    tile = models.Tile(**req.tile)
    try:
        api.manager.discard_tile(game_id, req.player_index, tile)
    except ValueError as err:
        raise GameActionError(str(err))
    try:
        api.manager.declare_riichi(game_id, req.player_index)
    except ValueError as err:
        raise GameActionError(str(err))
    return {"status": "ok"}


@handle_conflict
def _tsumo(game_id: int, req: ActionRequest) -> dict:
    if not req.tile:
        raise GameActionError("Tile required")
    tile = models.Tile(**req.tile)
    try:
        result = api.manager.declare_tsumo(game_id, req.player_index, tile)
    except ValueError as err:
        raise GameActionError(str(err))
    return result.__dict__


@handle_conflict
def _ron(game_id: int, req: ActionRequest) -> dict:
    if not req.tile:
        raise GameActionError("Tile required")
    tile = models.Tile(**req.tile)
    try:
        result = api.manager.declare_ron(game_id, req.player_index, tile)
    except ValueError as err:
        raise GameActionError(str(err))
    return result.__dict__


@handle_conflict
def _skip(game_id: int, req: ActionRequest) -> dict:
    try:
        api.manager.skip(game_id, req.player_index)
    except ValueError as err:
        raise GameActionError(str(err))
    return {"status": "ok"}


@handle_conflict
def _auto(game_id: int, req: ActionRequest) -> dict:
    ai_type = req.ai_type or "simple"
    state = api.manager.get_state(game_id)
    allowed_players = (
        state.waiting_for_claims if state.waiting_for_claims else [state.current_player]
    )
    if req.player_index not in allowed_players:
        raise GameActionError(
            f"Action not allowed: player {req.player_index} attempted auto. allowed players={allowed_players}"
        )
    try:
        tile = api.manager.auto_play_turn(
            game_id,
            req.player_index,
            ai_type=ai_type,
            claim_players=[req.player_index],
        )
    except ValueError as err:
        raise GameActionError(str(err))
    return asdict(tile)


ACTION_HANDLERS = {
    "draw": _draw,
    "discard": _discard,
    "chi": _chi,
    "pon": _pon,
    "kan": _kan,
    "riichi": _riichi,
    "tsumo": _tsumo,
    "ron": _ron,
    "skip": _skip,
    "auto": _auto,
}


@app.post("/games/{game_id}/action")
def game_action(game_id: int, req: ActionRequest) -> dict:
    """Perform a simple game action and return its result."""
    try:
        allowed = api.manager.get_allowed_actions(game_id, req.player_index)
    except KeyError:
        raise HTTPException(status_code=404, detail="Game not started")
    except IndexError:
        raise HTTPException(status_code=404, detail="Player not found")
    if req.action in {"chi", "pon", "kan", "riichi", "skip"} and req.action not in allowed:
        logger.info(
            "Player %s attempted disallowed action %s (allowed=%s)",
            req.player_index,
            req.action,
            allowed,
        )
        _raise_conflict(
            req.player_index,
            req.action,
            f"Action not allowed: player {req.player_index} attempted {req.action}. allowed={allowed}",
        )

    handler = ACTION_HANDLERS.get(req.action)
    if not handler:
        raise HTTPException(status_code=400, detail="Unknown action")
    return handler(game_id, req)


@app.websocket("/ws/{game_id}")
async def game_events(websocket: WebSocket, game_id: int) -> None:
    """Stream game events to the client."""
    await websocket.accept()
    _ws_connections.add(websocket)
    prev_actions: list[list[str]] | None = None
    try:
        # send initial allowed actions if a game is running
        try:
            prev_actions = api.manager.get_all_allowed_actions(game_id)
            await websocket.send_json(
                {"name": "allowed_actions", "payload": {"actions": prev_actions}}
            )
        except KeyError:
            prev_actions = None
        while True:
            try:
                events = api.manager.pop_events(game_id)
            except KeyError:
                events = []
            for event in events:
                await websocket.send_json(asdict(event))
                if event.name == "round_end":
                    prev_actions = None
                if event.name == "discard":
                    try:
                        updated = api.manager.get_all_allowed_actions(game_id)
                    except KeyError:
                        updated = None
                    if updated is not None:
                        prev_actions = updated
                        await websocket.send_json(
                            {"name": "allowed_actions", "payload": {"actions": updated}}
                        )
            try:
                actions = api.manager.get_all_allowed_actions(game_id)
            except KeyError:
                actions = None
            if actions is not None and actions != prev_actions:
                prev_actions = actions
                await websocket.send_json(
                    {"name": "allowed_actions", "payload": {"actions": actions}}
                )
            await asyncio.sleep(0.1)
    except WebSocketDisconnect:
        pass
    finally:
        _ws_connections.discard(websocket)
