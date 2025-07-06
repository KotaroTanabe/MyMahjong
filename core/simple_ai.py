"""Very basic AI helpers.

This module currently provides a simple shanten based AI used by the
``auto_play_turn`` API helper.  The AI tries to keep the hand close to
tenpai by discarding tiles that do not increase the shanten number.  It
also calls ``chi`` or ``pon`` when doing so will move the hand closer to
tenpai.
"""
from __future__ import annotations

from .mahjong_engine import MahjongEngine
from .models import Tile
from .rules import _tile_to_index
from mahjong.shanten import Shanten
import random


def _hand_shanten(tiles: list[Tile]) -> int:
    """Return shanten number for ``tiles``."""

    counts = [0] * 34
    for t in tiles:
        counts[_tile_to_index(t)] += 1
    return Shanten().calculate_shanten(counts)


def _choose_discard(tiles: list[Tile]) -> Tile:
    """Return a tile to discard that keeps shanten minimal."""

    counts = [0] * 34
    for t in tiles:
        counts[_tile_to_index(t)] += 1
    base = Shanten().calculate_shanten(counts)
    keep_shanten: list[Tile] = []
    best_tiles: list[Tile] = []
    best_value = 8

    for tile in tiles:
        idx = _tile_to_index(tile)
        counts[idx] -= 1
        value = Shanten().calculate_shanten(counts)
        counts[idx] += 1
        if value == base:
            keep_shanten.append(tile)
        if value < best_value:
            best_value = value
            best_tiles = [tile]
        elif value == best_value:
            best_tiles.append(tile)

    if keep_shanten:
        return random.choice(keep_shanten)
    if best_tiles:
        return random.choice(best_tiles)
    return random.choice(tiles)


def _maybe_call_meld(engine: MahjongEngine, player_index: int) -> bool:
    """Attempt to chi/pon the last discard if it improves shanten."""

    state = engine.state
    if player_index not in state.waiting_for_claims:
        return False

    last_tile = state.last_discard
    last_player = state.last_discard_player
    if last_tile is None or last_player is None or player_index == last_player:
        return False

    player = state.players[player_index]
    base = _hand_shanten(player.hand.tiles)
    best_action: tuple[str, list[Tile]] | None = None
    best_value = base

    # Pon check
    count = sum(
        1 for t in player.hand.tiles if t.suit == last_tile.suit and t.value == last_tile.value
    )
    if count >= 2:
        new_hand = player.hand.tiles.copy()
        removed = 0
        for i in range(len(new_hand) - 1, -1, -1):
            t = new_hand[i]
            if t.suit == last_tile.suit and t.value == last_tile.value:
                new_hand.pop(i)
                removed += 1
                if removed == 2:
                    break
        shanten = _hand_shanten(new_hand)
        if shanten < best_value:
            best_value = shanten
            tiles = [Tile(last_tile.suit, last_tile.value) for _ in range(3)]
            best_action = ("pon", tiles)

    # Chi check
    if (
        last_tile.suit in {"man", "pin", "sou"}
        and (last_player + 1) % len(state.players) == player_index
    ):
        for offset in (-2, -1, 0):
            start = last_tile.value + offset
            seq = [start, start + 1, start + 2]
            if min(seq) < 1 or max(seq) > 9:
                continue
            needed = [v for v in seq if v != last_tile.value]
            if all(
                any(t.suit == last_tile.suit and t.value == v for t in player.hand.tiles)
                for v in needed
            ):
                new_hand = player.hand.tiles.copy()
                for v in needed:
                    for i, t in enumerate(new_hand):
                        if t.suit == last_tile.suit and t.value == v:
                            new_hand.pop(i)
                            break
                shanten = _hand_shanten(new_hand)
                if shanten < best_value:
                    best_value = shanten
                    tiles = [Tile(last_tile.suit, x) for x in seq]
                    best_action = ("chi", tiles)

    if best_action is None:
        return False

    if best_action[0] == "pon":
        engine.call_pon(player_index, best_action[1])
    else:
        engine.call_chi(player_index, best_action[1])
    return True


def smart_turn(engine: MahjongEngine, player_index: int) -> Tile:
    """Play a full turn using a shanten based heuristic."""

    state = engine.state

    if player_index in state.waiting_for_claims:
        if _maybe_call_meld(engine, player_index):
            # After calling, the player must discard
            player = state.players[player_index]
            discard = _choose_discard(player.hand.tiles)
            engine.discard_tile(player_index, discard)
            return discard
        engine.skip(player_index)
        assert state.last_discard is not None
        return state.last_discard

    player = state.players[player_index]

    if len(player.hand.tiles) < 14:
        engine.draw_tile(player_index)

    discard = _choose_discard(player.hand.tiles)
    engine.discard_tile(player_index, discard)
    return discard
