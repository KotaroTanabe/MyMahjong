"""Convert engine events to tenhou.net/6 style JSON logs."""
from __future__ import annotations
import json
from typing import Any, Iterable, List

from .models import GameEvent, Tile, GameState, Meld


_TILE_BASE = {
    "man": 10,
    "pin": 20,
    "sou": 30,
    "wind": 40,
    "dragon": 44,
}

# Map engine ryukyoku reasons to Tenhou strings
_REASON_MAP = {
    "wall_empty": "全員不聴",
    "four_winds": "四風連打",
    "four_riichi": "四家立直",
    "four_kans": "四槓散了",
    "nine_terminals": "九種九牌",
}


def tile_to_code(tile: Tile) -> int:
    """Return the numeric tile code used by tenhou.net/6."""
    base = _TILE_BASE.get(tile.suit)
    if base is None:
        raise ValueError(f"Unknown suit: {tile.suit}")
    return base + tile.value


def meld_to_string(meld: Meld) -> str:
    """Return the Tenhou meld notation for ``meld``."""
    codes = [str(tile_to_code(t)) for t in meld.tiles]
    if meld.type == "chi":
        idx = meld.called_from - 1 if meld.called_from is not None else 0
        codes.insert(idx, "c")
    elif meld.type == "pon":
        idx = meld.called_from - 1 if meld.called_from is not None else 0
        codes.insert(idx, "p")
    elif meld.type == "kan":
        idx = meld.called_from - 1 if meld.called_from is not None else 0
        codes.insert(idx, "m")
    elif meld.type == "added_kan":
        idx = meld.called_from - 1 if meld.called_from is not None else 0
        codes.insert(idx, "k")
    elif meld.type == "closed_kan":
        codes.insert(3, "a")
    return "".join(codes)


def events_to_tenhou_json(events: List[GameEvent]) -> str:
    """Serialize ``events`` into a tenhou.net/6 JSON log."""
    names: List[str] = []
    log: List[Any] = []
    kyoku: list[Any] | None = None
    player_data: list[list[list[Any]]] = []  # [ [hand, takes, dahai], ... ]
    riichi_pending: list[bool] = []
    start_scores: list[int] = []
    last_discard_player: int | None = None
    dead_wall: list[Tile] = []
    dora_indicators: list[int] = []
    ura_indicators: list[int] = []

    for ev in events:
        if ev.name == "start_kyoku":
            state: GameState = ev.payload["state"]
            names = [p.name for p in state.players]
            dealer = ev.payload.get("dealer", state.dealer)
            round_number = ev.payload.get("round", state.round_number)
            kyoku_num = (round_number - 1) * 4 + dealer
            dora_indicators = [tile_to_code(t) for t in state.dora_indicators]
            ura_indicators = [tile_to_code(t) for t in state.ura_dora_indicators]
            kyoku = [
                [kyoku_num, state.honba, state.riichi_sticks],
                [p.score for p in state.players],
                dora_indicators[:],
                [],
            ]
            player_data = []
            for idx, player in enumerate(state.players):
                hand = [tile_to_code(t) for t in player.hand.tiles]
                takes: list[Any] = []
                # Dealer is dealt 14 tiles. The extra tile should be recorded as
                # the first draw rather than in the starting hand array.
                if idx == dealer and len(hand) == 14:
                    takes.append(hand.pop())
                player_data.append([
                    hand,
                    takes,
                    [],
                ])
            riichi_pending = [False for _ in state.players]
            start_scores = [p.score for p in state.players]
            last_discard_player = None
            dead_wall = state.dead_wall.copy()
        elif ev.name == "draw_tile":
            p = ev.payload["player_index"]
            player_data[p][1].append(tile_to_code(ev.payload["tile"]))
            if ev.payload.get("from_dead_wall"):
                if dead_wall:
                    dead_wall.pop(0)
                if len(dead_wall) >= 5 + len(dora_indicators):
                    new_dora_tile = dead_wall[-(5 + len(dora_indicators))]
                    code = tile_to_code(new_dora_tile)
                    if kyoku is not None:
                        kyoku[2].append(code)
                    dora_indicators.append(code)
                if len(dead_wall) >= len(ura_indicators) + 1:
                    ura_tile = dead_wall[-(len(ura_indicators) + 1)]
                    ura_indicators.append(tile_to_code(ura_tile))
            last_discard_player = None
        elif ev.name == "discard":
            p = ev.payload["player_index"]
            code = tile_to_code(ev.payload["tile"])
            player_data[p][2].append(code)
            if riichi_pending and riichi_pending[p]:
                player_data[p][1].append(f"r{code}")
                riichi_pending[p] = False
            last_discard_player = p
        elif ev.name == "riichi":
            p = ev.payload["player_index"]
            if riichi_pending:
                riichi_pending[p] = True
        elif ev.name == "meld":
            p = ev.payload["player_index"]
            meld: Meld = ev.payload["meld"]
            player_data[p][1].append(meld_to_string(meld))
            if meld.type == "kan" and meld.called_from is not None:
                player_data[p][2].append(0)
        elif ev.name in {"tsumo", "ron"} and kyoku is not None:
            scores = ev.payload.get("scores", start_scores)
            delta = [scores[i] - start_scores[i] for i in range(len(scores))]
            win_player = ev.payload.get("player_index", 0)
            if ev.name == "ron":
                deal_in = last_discard_player if last_discard_player is not None else win_player
            else:
                deal_in = win_player
            result = ev.payload.get("result")
            point_str = ""
            yaku_list: list[str] = []
            if result:
                han = result.get("han")
                fu = result.get("fu")
                yaku_list = result.get("yaku") or []
                if han is not None and fu is not None:
                    point_str = f"{han}han{fu}fu"
            result_info = [win_player, deal_in, win_player, point_str, *yaku_list]
            for i in range(4):
                kyoku.extend(player_data[i])
            kyoku[3] = ura_indicators[:]
            kyoku.append(["和了", delta, result_info])
            log.append(kyoku)
            kyoku = None
            player_data = []
        elif ev.name == "ryukyoku" and kyoku is not None:
            scores = ev.payload.get("scores", start_scores)
            delta = [scores[i] - start_scores[i] for i in range(len(scores))]
            reason_key = ev.payload.get("reason")
            reason = _REASON_MAP.get(str(reason_key), str(reason_key or "不明"))
            for i in range(4):
                kyoku.extend(player_data[i])
            if any(delta):
                kyoku.append(["流局", delta])
            else:
                kyoku.append([reason])
            log.append(kyoku)
            kyoku = None
            player_data = []

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
