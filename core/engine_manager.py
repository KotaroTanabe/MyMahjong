from __future__ import annotations

from contextlib import contextmanager
from typing import Dict, Iterator, Tuple

from .mahjong_engine import MahjongEngine
from .models import GameEvent, GameState
from . import api


class EngineManager:
    """Manage multiple MahjongEngine instances keyed by game id."""

    def __init__(self) -> None:
        self._engines: Dict[int, MahjongEngine] = {}
        self._next_id: int = 1

    def create_game(self, players: list[str], *, max_rounds: int = 8) -> Tuple[int, GameState]:
        """Create a new game and return its id and initial state."""
        engine = MahjongEngine(max_rounds=max_rounds)
        for i, name in enumerate(players):
            if i < len(engine.state.players):
                engine.state.players[i].name = name
        game_id = self._next_id
        self._next_id += 1
        self._engines[game_id] = engine
        api._engine = engine
        return game_id, engine.state

    def get_engine(self, game_id: int) -> MahjongEngine:
        return self._engines[game_id]

    def get_state(self, game_id: int) -> GameState:
        return self.get_engine(game_id).state

    def pop_events(self, game_id: int) -> list[GameEvent]:
        engine = self.get_engine(game_id)
        return engine.pop_events()

    @contextmanager
    def use_engine(self, game_id: int) -> Iterator[None]:
        engine = self.get_engine(game_id)
        prev = api._engine
        api._engine = engine
        try:
            yield
        finally:
            api._engine = prev

    def record_next_actions(self, game_id: int, player_index: int, actions: list[str]) -> None:
        engine = self.get_engine(game_id)
        payload = {"player_index": player_index, "actions": actions}
        last = engine.event_history[-1] if engine.event_history else None
        if (
            last is None
            or last.name != "next_actions"
            or last.payload.get("player_index") != player_index
            or last.payload.get("actions") != actions
        ):
            evt = GameEvent(name="next_actions", payload=payload)
            engine.queue_event(evt)
