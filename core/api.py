"""High-level core API functions."""
from __future__ import annotations

from .mahjong_engine import MahjongEngine
from .models import GameState, Tile, GameEvent, GameAction
from . import practice
from mahjong.hand_calculating.hand_response import HandResponse

# Singleton engine instance used by interfaces
_engine: MahjongEngine | None = None


def start_game(player_names: list[str]) -> GameState:
    """Initialize a new game and return its state."""
    global _engine
    _engine = MahjongEngine()
    for i, name in enumerate(player_names):
        if i < len(_engine.state.players):
            _engine.state.players[i].name = name
    return _engine.state


def start_kyoku(dealer: int, round_number: int) -> GameState:
    """Begin a new hand and return the updated state."""
    assert _engine is not None, "Game not started"
    _engine.start_kyoku(dealer, round_number)
    return _engine.state


def draw_tile(player_index: int) -> Tile:
    """Draw a tile for the given player."""
    assert _engine is not None, "Game not started"
    return _engine.draw_tile(player_index)


def discard_tile(player_index: int, tile: Tile) -> None:
    """Discard a tile from the player's hand."""
    assert _engine is not None, "Game not started"
    _engine.discard_tile(player_index, tile)


def declare_riichi(player_index: int) -> None:
    """Declare riichi for the specified player."""
    assert _engine is not None, "Game not started"
    _engine.declare_riichi(player_index)


def get_state() -> GameState:
    """Return the current game state."""
    assert _engine is not None, "Game not started"
    return _engine.state


def call_chi(player_index: int, tiles: list[Tile]) -> None:
    """Public wrapper for MahjongEngine.call_chi."""
    assert _engine is not None, "Game not started"
    _engine.call_chi(player_index, tiles)


def call_pon(player_index: int, tiles: list[Tile]) -> None:
    """Public wrapper for MahjongEngine.call_pon."""
    assert _engine is not None, "Game not started"
    _engine.call_pon(player_index, tiles)


def call_kan(player_index: int, tiles: list[Tile]) -> None:
    """Public wrapper for MahjongEngine.call_kan."""
    assert _engine is not None, "Game not started"
    _engine.call_kan(player_index, tiles)


def declare_tsumo(player_index: int, tile: Tile) -> HandResponse:
    """Declare a self-drawn win."""
    assert _engine is not None, "Game not started"
    return _engine.declare_tsumo(player_index, tile)


def declare_ron(player_index: int, tile: Tile) -> HandResponse:
    """Declare a ron win on another player's discard."""
    assert _engine is not None, "Game not started"
    return _engine.declare_ron(player_index, tile)


def skip(player_index: int) -> None:
    """Skip action for the player."""
    assert _engine is not None, "Game not started"
    _engine.skip(player_index)


def end_game() -> GameState:
    """End the current game and reset the engine."""
    assert _engine is not None, "Game not started"
    return _engine.end_game()


def pop_events() -> list[GameEvent]:
    """Retrieve and clear pending engine events."""
    assert _engine is not None, "Game not started"
    return _engine.pop_events()


def generate_practice_problem() -> practice.PracticeProblem:
    """Return a new practice problem."""

    return practice.generate_problem()


def suggest_practice_discard(hand: list[Tile]) -> Tile:
    """Return AI suggested discard for ``hand``."""

    return practice.suggest_discard(hand)


def apply_action(action: GameAction) -> object | None:
    """Apply ``action`` to the running engine and return any result."""

    assert _engine is not None, "Game not started"

    if action.type == "draw":
        assert action.player_index is not None
        return _engine.draw_tile(action.player_index)
    if action.type == "discard" and action.tile is not None:
        assert action.player_index is not None
        _engine.discard_tile(action.player_index, action.tile)
        return None
    if action.type == "chi" and action.tiles is not None:
        assert action.player_index is not None
        _engine.call_chi(action.player_index, action.tiles)
        return None
    if action.type == "pon" and action.tiles is not None:
        assert action.player_index is not None
        _engine.call_pon(action.player_index, action.tiles)
        return None
    if action.type == "kan" and action.tiles is not None:
        assert action.player_index is not None
        _engine.call_kan(action.player_index, action.tiles)
        return None
    if action.type == "riichi":
        assert action.player_index is not None
        _engine.declare_riichi(action.player_index)
        return None
    if action.type == "tsumo" and action.tile is not None:
        assert action.player_index is not None
        return _engine.declare_tsumo(action.player_index, action.tile)
    if action.type == "ron" and action.tile is not None:
        assert action.player_index is not None
        return _engine.declare_ron(action.player_index, action.tile)
    if action.type == "skip":
        assert action.player_index is not None
        _engine.skip(action.player_index)
        return None
    if action.type == "start_kyoku":
        assert action.dealer is not None and action.round_number is not None
        _engine.start_kyoku(action.dealer, action.round_number)
        return None
    if action.type == "end_game":
        return _engine.end_game()

    raise ValueError(f"Unknown action: {action.type}")
