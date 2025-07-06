from __future__ import annotations

"""Registry for available AI strategies."""

from typing import Callable, Dict

from .mahjong_engine import MahjongEngine
from .models import Tile
from .simple_ai import smart_turn

AI_REGISTRY: Dict[str, Callable[[MahjongEngine, int], Tile]] = {
    "simple": smart_turn,
}


def register_ai(name: str, func: Callable[[MahjongEngine, int], Tile]) -> None:
    """Register a new AI strategy under ``name``."""
    AI_REGISTRY[name] = func
