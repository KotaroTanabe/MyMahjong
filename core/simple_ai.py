"""Very basic AI helpers."""
from __future__ import annotations

import random
from typing import Iterable

from mahjong.shanten import Shanten

from .actions import CHI, PON
from .mahjong_engine import MahjongEngine
from .models import Tile
from .rules import _tile_to_index


def tsumogiri_turn(engine: MahjongEngine, player_index: int) -> Tile:
    """Play a full turn by discarding the drawn tile.

    The AI only draws when the player has just discarded (hand size modulo 3
    equals 1). After calling melds the hand size will not satisfy this
    condition so no extra draw occurs.
    """

    player = engine.state.players[player_index]
    if len(player.hand.tiles) % 3 == 1:
        tile = engine.draw_tile(player_index)
    else:
        tile = player.hand.tiles[-1]
    engine.discard_tile(player_index, tile)
    return tile


def _hand_counts(hand: Iterable[Tile]) -> list[int]:
    counts = [0] * 34
    for tile in hand:
        counts[_tile_to_index(tile)] += 1
    return counts


def suggest_discard(hand: list[Tile]) -> Tile:
    """Return a discard that keeps the hand close to tenpai."""

    counts = _hand_counts(hand)
    shanten = Shanten()
    best_tiles: list[Tile] = []
    best_value = 8  # higher than any real shanten number

    for tile in hand:
        idx = _tile_to_index(tile)
        counts[idx] -= 1
        value = shanten.calculate_shanten(counts)
        counts[idx] += 1
        if value < best_value:
            best_value = value
            best_tiles = [tile]
        elif value == best_value:
            best_tiles.append(tile)

    return random.choice(best_tiles) if best_tiles else random.choice(hand)


def shanten_turn(engine: MahjongEngine, player_index: int) -> Tile:
    """Play a turn by discarding a shanten-neutral tile."""

    player = engine.state.players[player_index]
    if len(player.hand.tiles) % 3 == 1:
        engine.draw_tile(player_index)
    tile = suggest_discard(player.hand.tiles)
    engine.discard_tile(player_index, tile)
    return tile


def _calculate_shanten(tiles: Iterable[Tile]) -> int:
    counts = _hand_counts(list(tiles))
    return Shanten().calculate_shanten(counts)


def claim_meld(engine: MahjongEngine, player_index: int) -> bool:
    """Claim pon/chi if it improves shanten. Return True if meld was called."""

    state = engine.state
    last_tile = state.last_discard
    last_player = state.last_discard_player
    if last_tile is None or last_player is None:
        return False

    player = state.players[player_index]
    current = _calculate_shanten(player.hand.tiles)
    best_action: tuple[str, list[Tile]] | None = None
    best_value = current

    # Pon candidate
    same = [t for t in player.hand.tiles if t.suit == last_tile.suit and t.value == last_tile.value]
    if len(same) >= 2:
        remaining = player.hand.tiles.copy()
        remaining.remove(same[0])
        remaining.remove(same[1])
        value = _calculate_shanten(remaining)
        if value < best_value:
            best_value = value
            best_action = (PON, [same[0], same[1], last_tile])

    # Chi candidate
    if (last_player + 1) % len(state.players) == player_index and last_tile.suit in {"man", "pin", "sou"}:
        for delta1, delta2 in [(-2, -1), (-1, 1), (1, 2)]:
            v1 = last_tile.value + delta1
            v2 = last_tile.value + delta2
            if not (1 <= v1 <= 9 and 1 <= v2 <= 9):
                continue
            needed: list[Tile] = []
            for v in (v1, v2):
                found = next((t for t in player.hand.tiles if t.suit == last_tile.suit and t.value == v and t not in needed), None)
                if found is None:
                    needed = []
                    break
                needed.append(found)
            if len(needed) == 2:
                remaining = player.hand.tiles.copy()
                remaining.remove(needed[0])
                remaining.remove(needed[1])
                value = _calculate_shanten(remaining)
                if value < best_value:
                    best_value = value
                    meld_tiles = [*needed, last_tile]
                    meld_tiles.sort(key=lambda t: t.value)
                    best_action = (CHI, meld_tiles)

    if best_action is None or best_value >= current:
        return False

    if best_action[0] == PON:
        engine.call_pon(player_index, best_action[1])
    else:
        engine.call_chi(player_index, best_action[1])
    return True
