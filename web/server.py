from __future__ import annotations

from dataclasses import asdict

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Request
import asyncio
import logging
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from core import api, models, shanten_quiz
from core.engine_manager import EngineManager
from core.exceptions import InvalidActionError, NotYourTurnError
from core.models import GameEvent

app = FastAPI()
manager = EngineManager()
_ws_connections: set[WebSocket] = set()
logger = logging.getLogger(__name__)


@app.exception_handler(InvalidActionError)
@app.exception_handler(NotYourTurnError)
async def _invalid_action_handler(
    request: Request, exc: InvalidActionError
) -> JSONResponse:
    return JSONResponse(status_code=409, content={"detail": str(exc)})


def handle_conflict(func):
    """Log conflicts and re-raise action errors."""

    def wrapper(req: "ActionRequest"):
        try:
            return func(req)
        except (InvalidActionError, NotYourTurnError) as err:
            logger.info(
                "409 conflict: player %s attempted %s -> %s",
                req.player_index,
                req.action,
                err,
            )
            raise

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
    rounds = req.max_rounds if req.max_rounds is not None else 8
    game_id, state = manager.create_game(req.players, max_rounds=rounds)
    return {"id": game_id, **asdict(state)}


@app.get("/games/{game_id}")
def get_game(game_id: int) -> dict:
    """Return basic game state for the given game id."""
    try:
        with manager.use_engine(game_id):
            return asdict(api.get_state())
    except KeyError:
        raise HTTPException(status_code=404, detail="Game not started")


@app.get("/games/{game_id}/log")
def get_log(game_id: int) -> dict:
    """Return the Tenhou-format log for the current game."""
    try:
        with manager.use_engine(game_id):
            data = api.get_tenhou_log()
    except KeyError:
        raise HTTPException(status_code=404, detail="Game not started")
    return {"log": data}


@app.get("/games/{game_id}/mjai-log")
def get_mjai_log(game_id: int) -> dict:
    """Return the MJAI-format event log for the current game."""

    try:
        with manager.use_engine(game_id):
            data = api.get_mjai_log()
    except KeyError:
        raise HTTPException(status_code=404, detail="Game not started")
    return {"log": data}


@app.get("/games/{game_id}/events")
def get_events(game_id: int) -> dict:
    """Return raw event history."""

    try:
        with manager.use_engine(game_id):
            events = [asdict(e) for e in api.get_event_history()]
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
        with manager.use_engine(game_id):
            state = api.get_state()
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
        with manager.use_engine(game_id):
            actions = api.get_allowed_actions(player_index)
    except KeyError:
        raise HTTPException(status_code=404, detail="Game not started")
    except IndexError:
        raise HTTPException(status_code=404, detail="Player not found")
    return {"actions": actions}


@app.get("/games/{game_id}/chi-options/{player_index}")
def chi_options(game_id: int, player_index: int) -> dict:
    """Return chi tile pairs for ``player_index``."""

    try:
        with manager.use_engine(game_id):
            options = api.get_chi_options(player_index)
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
        with manager.use_engine(game_id):
            actions = api.get_all_allowed_actions()
    except KeyError:
        raise HTTPException(status_code=404, detail="Game not started")
    return {"actions": actions}


@app.get("/games/{game_id}/next-actions")
def next_actions(game_id: int) -> dict:
    """Return the next actor index and their allowed actions."""

    try:
        with manager.use_engine(game_id):
            idx, actions = api.get_next_actions()
    except KeyError:
        raise HTTPException(status_code=404, detail="Game not started")
    manager.record_next_actions(game_id, idx, actions)
    return {"player_index": idx, "actions": actions}


@app.post("/games/{game_id}/start-kyoku")
async def start_kyoku_route(game_id: int, req: StartKyokuRequest) -> dict:
    """Start a new hand and notify connected clients."""
    try:
        with manager.use_engine(game_id):
            state = api.start_kyoku(req.dealer, req.round)
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
def _draw(req: ActionRequest) -> dict:
    try:
        tile = api.draw_tile(req.player_index)
    except IndexError:
        raise InvalidActionError("Wall is empty")
    except (InvalidActionError, NotYourTurnError):
        raise
    return asdict(tile)


@handle_conflict
def _discard(req: ActionRequest) -> dict:
    if not req.tile:
        raise InvalidActionError("Tile required")
    tile = models.Tile(**req.tile)
    try:
        api.discard_tile(req.player_index, tile)
    except (InvalidActionError, NotYourTurnError):
        raise
    return {"status": "ok"}


@handle_conflict
def _chi(req: ActionRequest) -> dict:
    if not req.tiles:
        raise InvalidActionError("Tiles required")
    tiles = [models.Tile(**t) for t in req.tiles]
    try:
        api.call_chi(req.player_index, tiles)
    except (InvalidActionError, NotYourTurnError):
        raise
    return {"status": "ok"}


@handle_conflict
def _pon(req: ActionRequest) -> dict:
    if not req.tiles:
        raise InvalidActionError("Tiles required")
    tiles = [models.Tile(**t) for t in req.tiles]
    try:
        api.call_pon(req.player_index, tiles)
    except (InvalidActionError, NotYourTurnError):
        raise
    return {"status": "ok"}


@handle_conflict
def _kan(req: ActionRequest) -> dict:
    if not req.tiles:
        raise InvalidActionError("Tiles required")
    tiles = [models.Tile(**t) for t in req.tiles]
    try:
        api.call_kan(req.player_index, tiles)
    except (InvalidActionError, NotYourTurnError):
        raise
    return {"status": "ok"}


@handle_conflict
def _riichi(req: ActionRequest) -> dict:
    if not req.tile:
        raise InvalidActionError("Tile required")
    tile = models.Tile(**req.tile)
    try:
        api.discard_tile(req.player_index, tile)
    except (InvalidActionError, NotYourTurnError):
        raise
    try:
        api.declare_riichi(req.player_index)
    except (InvalidActionError, NotYourTurnError):
        raise
    return {"status": "ok"}


@handle_conflict
def _tsumo(req: ActionRequest) -> dict:
    if not req.tile:
        raise InvalidActionError("Tile required")
    tile = models.Tile(**req.tile)
    try:
        result = api.declare_tsumo(req.player_index, tile)
    except (InvalidActionError, NotYourTurnError):
        raise
    return result.__dict__


@handle_conflict
def _ron(req: ActionRequest) -> dict:
    if not req.tile:
        raise InvalidActionError("Tile required")
    tile = models.Tile(**req.tile)
    try:
        result = api.declare_ron(req.player_index, tile)
    except (InvalidActionError, NotYourTurnError):
        raise
    return result.__dict__


@handle_conflict
def _skip(req: ActionRequest) -> dict:
    try:
        api.skip(req.player_index)
    except (InvalidActionError, NotYourTurnError):
        raise
    return {"status": "ok"}


@handle_conflict
def _auto(req: ActionRequest) -> dict:
    ai_type = req.ai_type or "simple"
    state = api.get_state()
    allowed_players = (
        state.waiting_for_claims if state.waiting_for_claims else [state.current_player]
    )
    if req.player_index not in allowed_players:
        raise InvalidActionError(
            f"Action not allowed: player {req.player_index} attempted auto. allowed players={allowed_players}"
        )
    try:
        tile = api.auto_play_turn(
            req.player_index,
            ai_type=ai_type,
            claim_players=[req.player_index],
        )
    except (InvalidActionError, NotYourTurnError):
        raise
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
        with manager.use_engine(game_id):
            allowed = api.get_allowed_actions(req.player_index)
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
            return handler(req)
    except KeyError:
        raise HTTPException(status_code=404, detail="Game not started")
    except IndexError:
        raise HTTPException(status_code=404, detail="Player not found")


@app.websocket("/ws/{game_id}")
async def game_events(websocket: WebSocket, game_id: int) -> None:
    """Stream game events to the client."""
    await websocket.accept()
    _ws_connections.add(websocket)
    prev_actions: list[list[str]] | None = None
    try:
        # send initial allowed actions if a game is running
        try:
            with manager.use_engine(game_id):
                prev_actions = api.get_all_allowed_actions()
            await websocket.send_json(
                {"name": "allowed_actions", "payload": {"actions": prev_actions}}
            )
        except KeyError:
            prev_actions = None
        while True:
            try:
                with manager.use_engine(game_id):
                    events = api.pop_events()
            except KeyError:
                events = []
            for event in events:
                await websocket.send_json(asdict(event))
                if event.name == "round_end":
                    prev_actions = None
                if event.name == "discard":
                    try:
                        with manager.use_engine(game_id):
                            updated = api.get_all_allowed_actions()
                    except KeyError:
                        updated = None
                    if updated is not None:
                        prev_actions = updated
                        await websocket.send_json(
                            {"name": "allowed_actions", "payload": {"actions": updated}}
                        )
            try:
                with manager.use_engine(game_id):
                    actions = api.get_all_allowed_actions()
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
