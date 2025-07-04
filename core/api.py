"""High-level core API functions."""
from __future__ import annotations

from .mahjong_engine import MahjongEngine
from .models import GameState, Tile

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
