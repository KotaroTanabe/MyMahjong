"""High-level core API functions."""
from __future__ import annotations

from .mahjong_engine import MahjongEngine
from .models import GameState, Tile
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


def draw_tile(player_index: int) -> Tile:
    """Draw a tile for the given player."""
    assert _engine is not None, "Game not started"
    return _engine.draw_tile(player_index)


def discard_tile(player_index: int, tile: Tile) -> None:
    """Discard a tile from the player's hand."""
    assert _engine is not None, "Game not started"
    _engine.discard_tile(player_index, tile)


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
