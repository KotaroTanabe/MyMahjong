"""Convert engine events to tenhou.net/6 style JSON logs."""
from __future__ import annotations
import json
from typing import Any, Iterable, List

from .models import GameEvent, Tile, GameState


_TILE_BASE = {
    "man": 10,
    "pin": 20,
    "sou": 30,
    "wind": 40,
    "dragon": 44,
}


def tile_to_code(tile: Tile) -> int:
    """Return the numeric tile code used by tenhou.net/6."""
    base = _TILE_BASE.get(tile.suit)
    if base is None:
        raise ValueError(f"Unknown suit: {tile.suit}")
    return base + tile.value


def events_to_tenhou_json(events: List[GameEvent]) -> str:
    """Serialize ``events`` into a tenhou.net/6 JSON log."""
    names: List[str] = []
    log: List[Any] = []
    kyoku: list[Any] | None = None
    per_player: list[list[Any]] = []
    start_scores: list[int] = []

    for ev in events:
        if ev.name == "start_kyoku":
            state: GameState = ev.payload["state"]
            names = [p.name for p in state.players]
            kyoku = [
                [ev.payload.get("dealer", 0), 0, 0],
                [p.score for p in state.players],
                [tile_to_code(t) for t in state.dora_indicators],
                [],
            ]
            for player in state.players:
                kyoku.append([tile_to_code(t) for t in player.hand.tiles])
            per_player = [[] for _ in state.players]
            start_scores = [p.score for p in state.players]
        elif ev.name == "draw_tile":
            per_player[ev.payload["player_index"]].append(
                tile_to_code(ev.payload["tile"])
            )
        elif ev.name == "discard":
            per_player[ev.payload["player_index"]].append(
                tile_to_code(ev.payload["tile"])
            )
        elif ev.name == "riichi":
            per_player[ev.payload["player_index"]].append("reach")
        elif ev.name in {"tsumo", "ron"} and kyoku is not None:
            scores = ev.payload.get("scores", start_scores)
            delta = [scores[i] - start_scores[i] for i in range(len(scores))]
            kyoku.extend(per_player)
            kyoku.append(["和了", delta, []])
            log.append(kyoku)
            kyoku = None
        elif ev.name == "ryukyoku" and kyoku is not None:
            kyoku.extend(per_player)
            kyoku.append(["流局"])
            log.append(kyoku)
            kyoku = None

    data = {
        "title": ["", ""],
        "name": names,
        "rule": {"disp": "MyMahjong", "aka": 0},
        "log": log,
    }
    return json.dumps(data, ensure_ascii=False)


def mjai_log_to_tenhou_json(lines: Iterable[str]) -> str:
    """Convert MJAI log ``lines`` to Tenhou-style JSON."""

    events: list[GameEvent] = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        data = json.loads(line)
        name = data.pop("type")
        payload: dict[str, Any] = {}
        for k, v in data.items():
            if name == "start_kyoku" and k == "state":
                from .ai_adapter import json_to_game_state

                payload[k] = json_to_game_state(json.dumps(v))
            elif isinstance(v, dict) and "suit" in v and "value" in v:
                payload[k] = Tile(**v)
            else:
                payload[k] = v
        events.append(GameEvent(name=name, payload=payload))

    return events_to_tenhou_json(events)
