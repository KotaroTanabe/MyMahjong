"""High-level core API functions."""
from __future__ import annotations

from .mahjong_engine import MahjongEngine
from .actions import (CHI, PON, KAN, RIICHI, TSUMO, RON, SKIP, DRAW, DISCARD, START_KYOKU, ADVANCE_HAND, END_GAME, AUTO)
from . import exceptions
from .models import GameState, Tile, GameEvent, GameAction
from .ai import AI_REGISTRY
from . import practice, shanten_quiz
from mahjong.hand_calculating.hand_response import HandResponse

# Singleton engine instance used by interfaces
_engine: MahjongEngine | None = None


def start_game(player_names: list[str], *, max_rounds: int = 8) -> GameState:
    """Initialize a new game and return its state."""
    global _engine
    _engine = MahjongEngine(max_rounds=max_rounds)
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
    """Public wrapper for MahjongEngine.call_chi.

    ``tiles`` may contain either the full meld including the discarded tile or
    just the two tiles from the caller's hand. When only two tiles are
    provided the current discard is automatically inserted to form the meld.
    """
    assert _engine is not None, "Game not started"

    last_tile = _engine.state.last_discard
    last_player = _engine.state.last_discard_player
    if last_tile is None or last_player is None:
        raise exceptions.InvalidActionError("No discard available for chi")

    # Remove any discard representation so the engine instance is used.
    hand_tiles = [
        t
        for t in tiles
        if not (t.suit == last_tile.suit and t.value == last_tile.value)
    ]
    if len(hand_tiles) != 2:
        raise exceptions.InvalidActionError("Chi requires exactly two tiles from hand")

    hand_tiles = sorted(hand_tiles, key=lambda t: t.value)
    called_from = (player_index - last_player) % len(_engine.state.players)

    if called_from == 1:
        meld_tiles = [last_tile, *hand_tiles]
    elif called_from == 3:
        meld_tiles = [*hand_tiles, last_tile]
    else:
        meld_tiles = sorted([*hand_tiles, last_tile], key=lambda t: t.value)

    _engine.call_chi(player_index, meld_tiles)


def call_pon(player_index: int, tiles: list[Tile]) -> None:
    """Public wrapper for MahjongEngine.call_pon."""
    assert _engine is not None, "Game not started"
    _engine.call_pon(player_index, tiles)


def call_kan(player_index: int, tiles: list[Tile]) -> None:
    """Public wrapper for MahjongEngine.call_kan.

    ``tiles`` may contain either the full meld including the discarded tile or
    just the three tiles from the caller's hand. When only three tiles are
    provided the current discard is automatically inserted and any matching
    tile in ``tiles`` is replaced with the engine instance so object identity
    checks succeed.
    """

    assert _engine is not None, "Game not started"

    meld_tiles = tiles
    last_tile = _engine.state.last_discard
    last_player = _engine.state.last_discard_player

    if len(tiles) == 3:
        if last_tile is None or last_player is None:
            raise exceptions.InvalidActionError("No discard available for kan")
        meld_tiles = [last_tile, *tiles]

    if last_tile is not None:
        meld_tiles = [
            last_tile if t.suit == last_tile.suit and t.value == last_tile.value else t
            for t in meld_tiles
        ]

    _engine.call_kan(player_index, meld_tiles)


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


def auto_play_turn(
    player_index: int | None = None,
    ai_type: str = "simple",
    *,
    claim_players: list[int] | None = None,
) -> Tile:
    """Have the specified AI draw and discard for ``player_index``.

    ``claim_players`` limits which players will automatically claim or skip a
    discard when waiting for calls.  By default all players are processed to
    preserve the original behaviour used by the CLI game loop.
    """

    assert _engine is not None, "Game not started"
    idx = player_index if player_index is not None else _engine.state.current_player
    ai = AI_REGISTRY.get(ai_type)
    if ai is None:
        raise ValueError(f"Unknown ai_type: {ai_type}")

    claim_list = list(_engine.state.waiting_for_claims)
    if claim_players is not None:
        claim_list = [p for p in claim_list if p in claim_players]

    for p in claim_list:
        if ai_type == "simple":
            from .simple_ai import claim_meld

            if claim_meld(_engine, p):
                continue
        _engine.skip(p)
    if _engine.state.waiting_for_claims:
        assert _engine.state.last_discard is not None
        return _engine.state.last_discard

    current = _engine.state.current_player
    if player_index is not None and current != player_index:
        # Claims advanced the turn to another player; do not play for the
        # original index. Return the drawn tile for the next player instead.
        player = _engine.state.players[current]
        return player.hand.tiles[-1]

    idx = current
    return ai(_engine, idx)


def advance_hand(winner_index: int | None = None) -> GameState:
    """Advance to the next hand and return the updated state."""
    assert _engine is not None, "Game not started"
    _engine.advance_hand(winner_index)
    return _engine.state


def end_game() -> GameState:
    """End the current game and reset the engine."""
    assert _engine is not None, "Game not started"
    return _engine.end_game()


def is_game_over() -> bool:
    """Return True if the current game has ended."""
    assert _engine is not None, "Game not started"
    return _engine.is_game_over


def pop_events() -> list[GameEvent]:
    """Retrieve and clear pending engine events."""
    assert _engine is not None, "Game not started"
    return _engine.pop_events()


def get_tenhou_log() -> str:
    """Return the accumulated event log in Tenhou JSON format."""
    assert _engine is not None, "Game not started"
    from .tenhou_log import events_to_tenhou_json

    history = _engine.get_event_history()
    return events_to_tenhou_json(history)


def get_mjai_log() -> str:
    """Return the accumulated event log in MJAI JSON format."""
    assert _engine is not None, "Game not started"
    import json
    from dataclasses import asdict, is_dataclass
    from typing import Any, Mapping, cast

    def encode(obj: Any) -> Any:
        if is_dataclass(obj) and not isinstance(obj, type):
            return {k: encode(v) for k, v in asdict(obj).items()}
        if isinstance(obj, dict):
            return {k: encode(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [encode(v) for v in obj]
        return obj

    history = _engine.get_event_history()
    lines = []
    for e in history:
        payload = {
            "type": e.name,
            **cast(Mapping[str, Any], encode(e.payload)),
        }
        lines.append(json.dumps(payload, ensure_ascii=False))
    return "\n".join(lines)


def get_event_history() -> list[GameEvent]:
    """Return the full event history."""

    assert _engine is not None, "Game not started"
    return _engine.get_event_history()


def generate_practice_problem() -> practice.PracticeProblem:
    """Return a new practice problem."""

    return practice.generate_problem()


def suggest_practice_discard(hand: list[Tile], use_ai: bool = False) -> Tile:
    """Return AI suggested discard for ``hand``.

    ``use_ai`` controls whether an external AI should be invoked.
    """

    return practice.suggest_discard(hand, use_ai=use_ai)


def calculate_shanten(hand: list[Tile]) -> int:
    """Return the shanten number for ``hand``."""

    return shanten_quiz.calculate_shanten(hand)


def get_allowed_actions(player_index: int) -> list[str]:
    """Return allowed actions for ``player_index`` in the current game."""

    assert _engine is not None, "Game not started"
    return _player_actions(player_index)


def get_chi_options(player_index: int) -> list[list[Tile]]:
    """Return chi tile pairs available to ``player_index``."""

    assert _engine is not None, "Game not started"
    return _engine.get_chi_options(player_index)


def get_all_allowed_actions() -> list[list[str]]:
    """Return allowed actions for all players."""

    assert _engine is not None, "Game not started"
    return [
        _player_actions(i) for i in range(len(_engine.state.players))
    ]


def get_claim_options() -> list[list[str]]:
    """Return claim options for every player.

    Each list contains actions like ``chi`` or ``ron`` if the player can
    claim the most recent discard. Players not able to act have an empty list.
    """

    assert _engine is not None, "Game not started"
    state = _engine.state
    opts: list[list[str]] = []
    for i in range(len(state.players)):
        if i in state.waiting_for_claims:
            actions = [
                a
                for a in _engine.get_allowed_actions(i)
                if a in {CHI, PON, KAN, RON, SKIP}
            ]
            opts.append(actions)
        else:
            opts.append([])
    return opts


def _player_actions(player_index: int) -> list[str]:
    """Return full action list for ``player_index`` including draw/discard."""

    assert _engine is not None, "Game not started"
    actions = set(_engine.get_allowed_actions(player_index))
    state = _engine.state
    if not state.waiting_for_claims and player_index == state.current_player:
        player = state.players[player_index]
        if len(player.hand.tiles) % 3 == 1:
            actions.add(DRAW)
        else:
            actions.add(DISCARD)
    return sorted(actions)


def get_next_actions() -> tuple[int, list[str]]:
    """Return the next actor and their allowed actions.

    If the only available action is ``draw`` it is performed automatically and
    the next actor is returned instead.
    """

    assert _engine is not None, "Game not started"

    while True:
        state = _engine.state
        if state.waiting_for_claims:
            return state.current_player, []
        idx = state.current_player
        actions = _player_actions(idx)
        if actions == [DRAW]:
            _engine.draw_tile(idx)
            continue
        return idx, actions


def apply_action(action: GameAction) -> object | None:
    """Apply ``action`` to the running engine and return any result."""

    assert _engine is not None, "Game not started"

    if action.type == DRAW:
        assert action.player_index is not None
        return _engine.draw_tile(action.player_index)
    if action.type == DISCARD and action.tile is not None:
        assert action.player_index is not None
        _engine.discard_tile(action.player_index, action.tile)
        return None
    if action.type == CHI and action.tiles is not None:
        assert action.player_index is not None
        _engine.call_chi(action.player_index, action.tiles)
        return None
    if action.type == PON and action.tiles is not None:
        assert action.player_index is not None
        _engine.call_pon(action.player_index, action.tiles)
        return None
    if action.type == KAN and action.tiles is not None:
        assert action.player_index is not None
        _engine.call_kan(action.player_index, action.tiles)
        return None
    if action.type == RIICHI:
        assert action.player_index is not None
        _engine.declare_riichi(action.player_index)
        return None
    if action.type == TSUMO and action.tile is not None:
        assert action.player_index is not None
        return _engine.declare_tsumo(action.player_index, action.tile)
    if action.type == RON and action.tile is not None:
        assert action.player_index is not None
        return _engine.declare_ron(action.player_index, action.tile)
    if action.type == SKIP:
        assert action.player_index is not None
        _engine.skip(action.player_index)
        return None
    if action.type == START_KYOKU:
        assert action.dealer is not None and action.round_number is not None
        _engine.start_kyoku(action.dealer, action.round_number)
        return None
    if action.type == ADVANCE_HAND:
        _engine.advance_hand(action.player_index)
        return None
    if action.type == END_GAME:
        return _engine.end_game()

    raise ValueError(f"Unknown action: {action.type}")
