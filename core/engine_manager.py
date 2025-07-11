from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Mapping, Any
import json

from .mahjong_engine import MahjongEngine
from .models import GameState, Tile, GameEvent
from .ai import AI_REGISTRY
from .simple_ai import claim_meld
from mahjong.hand_calculating.hand_response import HandResponse
from .tenhou_log import events_to_tenhou_json


class EngineManager:
    """Manage multiple ``MahjongEngine`` instances indexed by game id."""

    def __init__(self) -> None:
        self._games: dict[int, MahjongEngine] = {}
        self._next_id = 1

    def reset(self) -> None:
        """Clear all games and id counter (for tests)."""
        self._games.clear()
        self._next_id = 1

    def create_game(self, players: list[str], *, max_rounds: int = 8) -> tuple[int, GameState]:
        """Create a new game and return its id and state."""
        engine = MahjongEngine(max_rounds=max_rounds)
        for i, name in enumerate(players):
            if i < len(engine.state.players):
                engine.state.players[i].name = name
        game_id = self._next_id
        self._next_id += 1
        self._games[game_id] = engine
        # keep default engine reference for compatibility
        try:
            from . import api  # local import to avoid cycle

            if api._engine is None:
                api._engine = engine
        except Exception:
            pass
        return game_id, engine.state

    def get_engine(self, game_id: int) -> MahjongEngine:
        if game_id not in self._games:
            raise KeyError("Game not found")
        return self._games[game_id]

    # basic helpers
    def get_state(self, game_id: int) -> GameState:
        return self.get_engine(game_id).state

    def start_kyoku(self, game_id: int, dealer: int, round_number: int) -> GameState:
        engine = self.get_engine(game_id)
        engine.start_kyoku(dealer, round_number)
        return engine.state

    def draw_tile(self, game_id: int, player_index: int) -> Tile:
        engine = self.get_engine(game_id)
        return engine.draw_tile(player_index)

    def discard_tile(self, game_id: int, player_index: int, tile: Tile) -> None:
        engine = self.get_engine(game_id)
        engine.discard_tile(player_index, tile)

    def call_chi(self, game_id: int, player_index: int, tiles: list[Tile]) -> None:
        engine = self.get_engine(game_id)
        last_tile = engine.state.last_discard
        last_player = engine.state.last_discard_player
        if last_tile is None or last_player is None:
            raise ValueError("No discard available for chi")
        hand_tiles = [
            t
            for t in tiles
            if not (t.suit == last_tile.suit and t.value == last_tile.value)
        ]
        if len(hand_tiles) != 2:
            raise ValueError("Chi requires exactly two tiles from hand")
        hand_tiles = sorted(hand_tiles, key=lambda t: t.value)
        called_from = (player_index - last_player) % len(engine.state.players)
        if called_from == 1:
            meld_tiles = [last_tile, *hand_tiles]
        elif called_from == 3:
            meld_tiles = [*hand_tiles, last_tile]
        else:
            meld_tiles = sorted([*hand_tiles, last_tile], key=lambda t: t.value)
        engine.call_chi(player_index, meld_tiles)

    def call_pon(self, game_id: int, player_index: int, tiles: list[Tile]) -> None:
        engine = self.get_engine(game_id)
        engine.call_pon(player_index, tiles)

    def call_kan(self, game_id: int, player_index: int, tiles: list[Tile]) -> None:
        engine = self.get_engine(game_id)
        meld_tiles = tiles
        last_tile = engine.state.last_discard
        last_player = engine.state.last_discard_player
        if len(tiles) == 3:
            if last_tile is None or last_player is None:
                raise ValueError("No discard available for kan")
            meld_tiles = [last_tile, *tiles]
        if last_tile is not None:
            meld_tiles = [
                last_tile if t.suit == last_tile.suit and t.value == last_tile.value else t
                for t in meld_tiles
            ]
        engine.call_kan(player_index, meld_tiles)

    def declare_riichi(self, game_id: int, player_index: int) -> None:
        engine = self.get_engine(game_id)
        engine.declare_riichi(player_index)

    def declare_tsumo(self, game_id: int, player_index: int, tile: Tile) -> HandResponse:
        engine = self.get_engine(game_id)
        return engine.declare_tsumo(player_index, tile)

    def declare_ron(self, game_id: int, player_index: int, tile: Tile) -> HandResponse:
        engine = self.get_engine(game_id)
        return engine.declare_ron(player_index, tile)

    def skip(self, game_id: int, player_index: int) -> None:
        engine = self.get_engine(game_id)
        engine.skip(player_index)

    def auto_play_turn(
        self,
        game_id: int,
        player_index: int | None = None,
        *,
        ai_type: str = "simple",
        claim_players: list[int] | None = None,
    ) -> Tile:
        engine = self.get_engine(game_id)
        idx = player_index if player_index is not None else engine.state.current_player
        ai = AI_REGISTRY.get(ai_type)
        if ai is None:
            raise ValueError(f"Unknown ai_type: {ai_type}")
        claim_list = list(engine.state.waiting_for_claims)
        if claim_players is not None:
            claim_list = [p for p in claim_list if p in claim_players]
        for p in claim_list:
            if ai_type == "simple" and claim_meld(engine, p):
                continue
            engine.skip(p)
        if engine.state.waiting_for_claims:
            assert engine.state.last_discard is not None
            return engine.state.last_discard
        if player_index is None:
            idx = engine.state.current_player
        return ai(engine, idx)

    def pop_events(self, game_id: int) -> list[GameEvent]:
        engine = self.get_engine(game_id)
        return engine.pop_events()

    def get_event_history(self, game_id: int) -> list[GameEvent]:
        return self.get_engine(game_id).get_event_history()

    def get_allowed_actions(self, game_id: int, player_index: int) -> list[str]:
        engine = self.get_engine(game_id)
        return engine.get_allowed_actions(player_index)

    def get_all_allowed_actions(self, game_id: int) -> list[list[str]]:
        engine = self.get_engine(game_id)
        return [engine.get_allowed_actions(i) for i in range(len(engine.state.players))]

    def get_chi_options(self, game_id: int, player_index: int) -> list[list[Tile]]:
        engine = self.get_engine(game_id)
        return engine.get_chi_options(player_index)

    def _player_actions(self, engine: MahjongEngine, player_index: int) -> list[str]:
        actions = set(engine.get_allowed_actions(player_index))
        state = engine.state
        if not state.waiting_for_claims and player_index == state.current_player:
            player = state.players[player_index]
            if len(player.hand.tiles) % 3 == 1:
                actions.add("draw")
            else:
                actions.add("discard")
        return sorted(actions)

    def get_next_actions(self, game_id: int) -> tuple[int, list[str]]:
        engine = self.get_engine(game_id)
        while True:
            state = engine.state
            idx = state.waiting_for_claims[0] if state.waiting_for_claims else state.current_player
            actions = self._player_actions(engine, idx)
            if actions == ["draw"]:
                engine.draw_tile(idx)
                continue
            return idx, actions

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
            engine.events.append(evt)
            engine.event_history.append(evt)

    def get_tenhou_log(self, game_id: int) -> str:
        history = self.get_event_history(game_id)
        return events_to_tenhou_json(history)

    def get_mjai_log(self, game_id: int) -> str:
        history = self.get_event_history(game_id)

        def encode(obj: Any) -> Any:
            if is_dataclass(obj) and not isinstance(obj, type):
                return {k: encode(v) for k, v in asdict(obj).items()}
            if isinstance(obj, Mapping):
                return {k: encode(v) for k, v in obj.items()}
            if isinstance(obj, list):
                return [encode(v) for v in obj]
            return obj

        lines = []
        for e in history:
            payload = {"type": e.name, **encode(e.payload)}
            lines.append(json.dumps(payload, ensure_ascii=False))
        return "\n".join(lines)

