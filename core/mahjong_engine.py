"""Mahjong game engine wrapper."""
from __future__ import annotations

from .models import GameState, Tile, Meld, GameEvent
from .player import Player
from .wall import Wall
from .rules import RuleSet, StandardRuleSet, _tile_to_index
from mahjong.shanten import Shanten
from mahjong.hand_calculating.hand_response import HandResponse
from dataclasses import asdict
from typing import Any


def _hand_response_dict(resp: HandResponse) -> dict[str, Any]:
    """Return a JSON serializable representation of ``resp``."""
    return {
        "han": resp.han,
        "fu": resp.fu,
        "cost": resp.cost,
        "yaku": [y.name for y in resp.yaku] if resp.yaku else None,
        "fu_details": resp.fu_details,
        "error": resp.error,
        "is_open_hand": resp.is_open_hand,
    }


class MahjongEngine:
    """Simplified engine that wraps the `mahjong` library."""

    def __init__(self, ruleset: RuleSet | None = None) -> None:
        self.ruleset: RuleSet = ruleset or StandardRuleSet()
        self.state = GameState(wall=Wall())
        self.state.players = [Player(name=f"Player {i}") for i in range(4)]
        self.state.current_player = 0
        self.events: list[GameEvent] = []
        self.event_history: list[GameEvent] = []
        self._cached_allowed_actions: list[list[str]] | None = None
        self._claims_open = False
        self._emit("start_game", {"state": self.state})
        self.start_kyoku(dealer=0, round_number=1)

    def _invalidate_cache(self) -> None:
        """Clear cached allowed actions."""
        self._cached_allowed_actions = None

    def _draw_replacement_tile(self, player: Player) -> None:
        """Draw a replacement tile from the dead wall and reveal new dora."""
        assert self.state.wall is not None
        if not self.state.wall.dead_wall:
            return
        tile = self.state.wall.dead_wall.pop(0)
        player.draw(tile)
        if self.state.dead_wall:
            self.state.dead_wall.pop(0)
        # Reveal next dora indicator if available
        if len(self.state.wall.dead_wall) >= 5 + len(self.state.dora_indicators):
            new_dora = self.state.wall.dead_wall[
                -(5 + len(self.state.dora_indicators))
            ]
            self.state.wall.dora_indicators.append(new_dora)
            self.state.dora_indicators.append(new_dora)

    def _check_nine_terminals(self, player: Player) -> None:
        """Detect nine terminals/honors and end the hand."""
        unique = set(
            (t.suit, t.value)
            for t in player.hand.tiles
            if t.is_terminal_or_honor()
        )
        if len(unique) >= 9:
            self._resolve_ryukyoku("nine_terminals")

    def _emit(self, name: str, payload: dict) -> None:
        evt = GameEvent(name=name, payload=payload)
        self.events.append(evt)
        self.event_history.append(evt)

    def _close_claims(self) -> None:
        """Emit ``claims_closed`` if a discard claim window was open."""
        if self._claims_open:
            self._claims_open = False
            self._emit("claims_closed", {})

    def _is_tenpai(self, player: Player) -> bool:
        """Return True if ``player`` is in tenpai."""
        from .shanten_quiz import is_tenpai

        return is_tenpai(player.hand.tiles, player.hand.melds)

    def _resolve_ryukyoku(self, reason: str) -> None:
        """Handle a draw, apply noten penalties and advance the hand."""
        tenpai = [self._is_tenpai(p) for p in self.state.players]
        tenpai_players = [i for i, t in enumerate(tenpai) if t]
        noten_players = [i for i, t in enumerate(tenpai) if not t]
        if tenpai_players and noten_players:
            pool = 3000
            per_tenpai = pool // len(tenpai_players)
            per_noten = pool // len(noten_players)
            for i in tenpai_players:
                self.state.players[i].score += per_tenpai
            for i in noten_players:
                self.state.players[i].score -= per_noten
        scores = [p.score for p in self.state.players]
        self._emit(
            "ryukyoku",
            {"reason": reason, "tenpai": tenpai, "scores": scores},
        )
        self.advance_hand(None)

    def pop_events(self) -> list[GameEvent]:
        events = self.events[:]
        self.events.clear()
        return events

    def get_event_history(self) -> list[GameEvent]:
        """Return all events emitted since the engine was created."""
        return self.event_history[:]

    def start_kyoku(self, dealer: int, round_number: int) -> None:
        """Begin a new hand with fresh tiles."""
        self._invalidate_cache()
        self.state.wall = Wall()
        wall = self.state.wall
        assert wall is not None
        self.state.dora_indicators = wall.dora_indicators.copy()
        self.state.dead_wall = wall.dead_wall.copy()
        for p in self.state.players:
            p.hand.tiles.clear()
            p.hand.melds.clear()
            p.river.clear()
            p.riichi = False
            p.must_tsumogiri = False
        self.state.last_discard = None
        self.state.last_discard_player = None
        self.state.waiting_for_claims = []
        self._claims_open = False
        self.state.kan_count = 0
        winds = ["east", "south", "west", "north"]
        self.state.seat_winds = []
        for i, p in enumerate(self.state.players):
            wind = winds[(i - dealer) % 4]
            p.seat_wind = wind
            self.state.seat_winds.append(wind)
        self.state.dealer = dealer
        self.state.round_number = round_number
        self.state.current_player = dealer
        self.deal_initial_hands()
        self._emit(
            "start_kyoku",
            {"dealer": dealer, "round": round_number, "state": self.state},
        )
        self._check_nine_terminals(self.state.players[dealer])

    def deal_initial_hands(self) -> None:
        """Deal initial tiles: 14 for the dealer and 13 for others."""
        assert self.state.wall is not None
        # everyone starts with 13 tiles
        for _ in range(13):
            for player in self.state.players:
                player.draw(self.state.wall.draw_tile())

        # dealer gets one extra tile to begin their first turn
        dealer_index = self.state.dealer
        self.state.players[dealer_index].draw(self.state.wall.draw_tile())

    @property
    def remaining_tiles(self) -> int:
        """Number of tiles left in the wall."""
        assert self.state.wall is not None
        return self.state.wall.remaining_tiles

    @property
    def remaining_yama_tiles(self) -> int:
        """Number of drawable tiles left this hand."""
        assert self.state.wall is not None
        return self.state.wall.remaining_yama_tiles

    def draw_tile(self, player_index: int) -> Tile:
        """Draw a tile for the specified player."""
        self._invalidate_cache()
        if self.state.waiting_for_claims:
            raise ValueError("Waiting for other players to claim discard")
        if player_index != self.state.current_player:
            raise ValueError("Not player's turn")
        assert self.state.wall is not None
        tile = self.state.wall.draw_tile()
        self.state.players[player_index].draw(tile)
        self._emit("draw_tile", {"player_index": player_index, "tile": tile})
        player = self.state.players[player_index]
        if len(player.river) == 0 and not player.hand.melds:
            self._check_nine_terminals(player)
        if self.state.wall.remaining_tiles == 0:
            self._resolve_ryukyoku("wall_empty")
        # current_player will advance after the player discards
        return tile

    def discard_tile(self, player_index: int, tile: Tile) -> None:
        """Discard a tile from the specified player's hand."""
        self._invalidate_cache()
        if self.state.waiting_for_claims:
            raise ValueError("Waiting for other players to claim discard")
        if player_index != self.state.current_player:
            raise ValueError("Not player's turn")
        player = self.state.players[player_index]
        if player.must_tsumogiri and player.hand.tiles and player.hand.tiles[-1] is not tile:
            raise ValueError("Must discard the drawn tile after declaring riichi")
        player.discard(tile)
        player.must_tsumogiri = False
        self._emit("discard", {"player_index": player_index, "tile": tile})
        self.state.current_player = (player_index + 1) % len(self.state.players)
        self.state.waiting_for_claims = [
            i for i in range(len(self.state.players)) if i != player_index
        ]
        self._claims_open = True
        self.state.last_discard = tile
        self.state.last_discard_player = player_index

    def declare_riichi(self, player_index: int) -> None:
        """Declare riichi for the given player."""
        self._invalidate_cache()
        from .shanten_quiz import is_tenpai

        player = self.state.players[player_index]
        if player.has_open_melds():
            raise ValueError("Cannot declare riichi with open melds")
        if not is_tenpai(player.hand.tiles, player.hand.melds):
            raise ValueError("Cannot declare riichi when not in tenpai")
        player.declare_riichi()
        self.state.riichi_sticks += 1
        self._emit(
            "riichi",
            {
                "player_index": player_index,
                "score": player.score,
                "riichi_sticks": self.state.riichi_sticks,
            },
        )

    def calculate_score(
        self, player_index: int, win_tile: Tile
    ) -> HandResponse:
        """Return scoring information for the winning hand."""
        player = self.state.players[player_index]
        return self.ruleset.calculate_score(
            player.hand.tiles, player.hand.melds, win_tile, is_tsumo=True
        )

    def call_chi(self, player_index: int, tiles: list[Tile]) -> None:
        """Form a chi meld using the given tiles."""
        self._invalidate_cache()
        if len(tiles) != 3:
            raise ValueError("Chi requires three tiles")

        last_tile = self.state.last_discard
        last_player = self.state.last_discard_player
        if last_tile is None or last_player is None:
            raise ValueError("No discard available for chi")
        if (last_player + 1) % len(self.state.players) != player_index:
            raise ValueError("Chi must use the previous player's discard")
        if last_tile not in tiles:
            raise ValueError("Discarded tile must be included in meld")

        suit = tiles[0].suit
        if not all(t.suit == suit for t in tiles):
            raise ValueError("Chi tiles must have the same suit")
        values = sorted(t.value for t in tiles)
        if not (values[1] == values[0] + 1 and values[2] == values[0] + 2):
            raise ValueError("Chi tiles must be sequential")

        player = self.state.players[player_index]
        needed = tiles[:]
        needed.remove(last_tile)
        for tile in needed:
            if tile not in player.hand.tiles:
                raise ValueError("Player missing required tiles for chi")
        for tile in needed:
            idx = next(i for i, t in enumerate(player.hand.tiles) if t == tile)
            player.hand.tiles.pop(idx)

        discarder = self.state.players[last_player]
        if not discarder.river or discarder.river[-1] != last_tile:
            raise ValueError("Discard mismatch")
        discarder.river.pop()

        called_index = None
        called_from = None
        if last_tile in tiles:
            called_index = tiles.index(last_tile)
            called_from = (player_index - last_player) % len(self.state.players)
        meld = Meld(
            tiles=tiles,
            type="chi",
            called_index=called_index,
            called_from=called_from,
        )
        player.hand.melds.append(meld)
        self.state.last_discard = None
        self.state.last_discard_player = None
        self.state.waiting_for_claims = []
        self._close_claims()
        self.state.current_player = player_index
        self._emit("meld", {"player_index": player_index, "meld": meld})

    def call_pon(self, player_index: int, tiles: list[Tile]) -> None:
        """Form a pon meld using the given tiles."""
        self._invalidate_cache()
        if len(tiles) != 3:
            raise ValueError("Pon requires three tiles")

        last_tile = self.state.last_discard
        last_player = self.state.last_discard_player
        if last_tile is None or last_player is None:
            raise ValueError("No discard available for pon")
        if player_index == last_player:
            raise ValueError("Cannot pon your own discard")
        if not all(
            t.suit == tiles[0].suit and t.value == tiles[0].value for t in tiles
        ):
            raise ValueError("Pon tiles must be identical")
        if last_tile.suit != tiles[0].suit or last_tile.value != tiles[0].value:
            raise ValueError("Discarded tile must match meld tiles")

        player = self.state.players[player_index]
        count = sum(
            1
            for t in player.hand.tiles
            if t.suit == tiles[0].suit and t.value == tiles[0].value
        )
        if count < 2:
            raise ValueError("Player missing tiles for pon")
        removed = 0
        for i in range(len(player.hand.tiles) - 1, -1, -1):
            if (
                player.hand.tiles[i].suit == tiles[0].suit
                and player.hand.tiles[i].value == tiles[0].value
            ):
                player.hand.tiles.pop(i)
                removed += 1
                if removed == 2:
                    break

        discarder = self.state.players[last_player]
        if not discarder.river or discarder.river[-1] != last_tile:
            raise ValueError("Discard mismatch")
        discarder.river.pop()

        called_index = None
        called_from = None
        if last_tile in tiles:
            called_index = tiles.index(last_tile)
            called_from = (player_index - last_player) % len(self.state.players)
        meld = Meld(
            tiles=tiles,
            type="pon",
            called_index=called_index,
            called_from=called_from,
        )
        player.hand.melds.append(meld)
        self.state.last_discard = None
        self.state.last_discard_player = None
        self.state.waiting_for_claims = []
        self._close_claims()
        self.state.current_player = player_index
        self._emit("meld", {"player_index": player_index, "meld": meld})

    def call_kan(self, player_index: int, tiles: list[Tile]) -> None:
        """Form a kan meld. Supports open, closed and added kan."""
        self._invalidate_cache()
        if len(tiles) != 4:
            raise ValueError("Kan requires four tiles")

        suit = tiles[0].suit
        value = tiles[0].value
        if not all(t.suit == suit and t.value == value for t in tiles):
            raise ValueError("Kan tiles must be identical")

        player = self.state.players[player_index]
        last_tile = self.state.last_discard
        last_player = self.state.last_discard_player

        # Open kan using another player's discard
        if last_tile is not None and last_player is not None:
            if player_index == last_player:
                raise ValueError("Cannot kan your own discard")
            if last_tile.suit != suit or last_tile.value != value:
                raise ValueError("Discarded tile must match meld tiles")
            count = sum(
                1
                for t in player.hand.tiles
                if t.suit == suit and t.value == value
            )
            if count < 3:
                raise ValueError("Player missing tiles for kan")
            meld_tiles: list[Tile] = [last_tile]
            removed = 0
            for i in range(len(player.hand.tiles) - 1, -1, -1):
                tile_obj = player.hand.tiles[i]
                if tile_obj.suit == suit and tile_obj.value == value:
                    meld_tiles.append(player.hand.tiles.pop(i))
                    removed += 1
                    if removed == 3:
                        break
            discarder = self.state.players[last_player]
            if not discarder.river or discarder.river[-1] != last_tile:
                raise ValueError("Discard mismatch")
            discarder.river.pop()
            called_index = 0
            called_from = (player_index - last_player) % len(self.state.players)
            meld = Meld(
                tiles=meld_tiles,
                type="kan",
                called_index=called_index,
                called_from=called_from,
            )
            player.hand.melds.append(meld)
            self.state.last_discard = None
            self.state.last_discard_player = None
            self.state.waiting_for_claims = []
            self._close_claims()
            self._draw_replacement_tile(player)
            self.state.current_player = player_index
            self._emit("meld", {"player_index": player_index, "meld": meld})
            self.state.kan_count += 1
            if self.state.kan_count >= 4:
                self._resolve_ryukyoku("four_kans")
            return

        # Added kan upgrade from an existing pon
        for meld in player.hand.melds:
            if meld.type == "pon" and all(
                t.suit == suit and t.value == value for t in meld.tiles
            ):
                idx = next(
                    (
                        i
                        for i, t in enumerate(player.hand.tiles)
                        if t.suit == suit and t.value == value
                    ),
                    None,
                )
                if idx is None:
                    raise ValueError("Player missing tile for added kan")
                meld.tiles.append(player.hand.tiles.pop(idx))
                meld.type = "added_kan"
                self.state.waiting_for_claims = []
                self._close_claims()
                self._draw_replacement_tile(player)
                self.state.current_player = player_index
                self._emit("meld", {"player_index": player_index, "meld": meld})
                self.state.kan_count += 1
                if self.state.kan_count >= 4:
                    self._resolve_ryukyoku("four_kans")
                return

        # Closed kan from hand
        count = sum(1 for t in player.hand.tiles if t.suit == suit and t.value == value)
        if count < 4:
            raise ValueError("Player missing tiles for kan")
        meld_tiles = []
        removed = 0
        for i in range(len(player.hand.tiles) - 1, -1, -1):
            tile_obj = player.hand.tiles[i]
            if tile_obj.suit == suit and tile_obj.value == value:
                meld_tiles.append(player.hand.tiles.pop(i))
                removed += 1
                if removed == 4:
                    break
        meld = Meld(tiles=meld_tiles, type="closed_kan")
        player.hand.melds.append(meld)
        self.state.waiting_for_claims = []
        self._close_claims()
        self._draw_replacement_tile(player)
        self.state.current_player = player_index
        self._emit("meld", {"player_index": player_index, "meld": meld})
        self.state.kan_count += 1
        if self.state.kan_count >= 4:
            self._resolve_ryukyoku("four_kans")

    def declare_tsumo(self, player_index: int, win_tile: Tile) -> HandResponse:
        """Declare a self-drawn win and return scoring info."""
        self._invalidate_cache()
        result = self.calculate_score(player_index, win_tile)
        player = self.state.players[player_index]
        if result.cost and "total" in result.cost:
            total = int(result.cost["total"])
            honba_bonus = self.state.honba * 100
            player.score += total + honba_bonus * (len(self.state.players) - 1)
            share = total // (len(self.state.players) - 1)
            for i, p in enumerate(self.state.players):
                if i != player_index:
                    p.score -= share + honba_bonus
            player.score += self.state.riichi_sticks * 1000
            self.state.riichi_sticks = 0
        scores = [p.score for p in self.state.players]
        self._emit(
            "tsumo",
            {
                "player_index": player_index,
                "win_tile": win_tile,
                "hand": asdict(player.hand),
                "result": _hand_response_dict(result),
                "scores": scores,
            },
        )
        self.state.waiting_for_claims = []
        self.advance_hand(player_index)
        return result

    def declare_ron(self, player_index: int, win_tile: Tile) -> HandResponse:
        """Declare a win on another player's discard."""
        self._invalidate_cache()
        result = self.calculate_score(player_index, win_tile)
        player = self.state.players[player_index]
        if result.cost and "total" in result.cost:
            total = int(result.cost["total"])
            honba_bonus = self.state.honba * 300
            player.score += total + honba_bonus
            discarder = self.state.last_discard_player
            if discarder is not None and discarder != player_index:
                self.state.players[discarder].score -= total + honba_bonus
            player.score += self.state.riichi_sticks * 1000
            self.state.riichi_sticks = 0
        scores = [p.score for p in self.state.players]
        self._emit(
            "ron",
            {
                "player_index": player_index,
                "win_tile": win_tile,
                "hand": asdict(player.hand),
                "result": _hand_response_dict(result),
                "scores": scores,
            },
        )
        self.state.waiting_for_claims = []
        self._close_claims()
        self.advance_hand(player_index)
        return result

    def skip(self, player_index: int) -> None:
        """Skip action for the specified player."""
        self._invalidate_cache()
        # Waiting for claims from other players
        if self.state.waiting_for_claims:
            if player_index in self.state.waiting_for_claims:
                self.state.waiting_for_claims.remove(player_index)
                self._emit("skip", {"player_index": player_index})
                if not self.state.waiting_for_claims:
                    self._close_claims()
                    # All players have passed on the discard; draw for next player
                    next_player = self.state.current_player
                    self.draw_tile(next_player)
                    # draw_tile advances current_player; reset to drawer
                    self.state.current_player = next_player
            return
        if player_index != self.state.current_player:
            return
        self.state.current_player = (self.state.current_player + 1) % len(
            self.state.players
        )
        self._emit("skip", {"player_index": player_index})
        new_player = self.state.current_player
        self.draw_tile(new_player)
        # draw_tile advances current_player; reset to drawer
        self.state.current_player = new_player

    def advance_hand(self, winner_index: int | None = None) -> None:
        """Move to the next hand and handle dealer rotation."""
        self._invalidate_cache()
        if winner_index is None or winner_index == self.state.dealer:
            self.state.honba += 1
        else:
            self.state.honba = 0
            self.state.dealer = (self.state.dealer + 1) % len(self.state.players)
            self.state.round_number += 1

        if self.state.round_number > 8:
            self.end_game()
        else:
            self.start_kyoku(self.state.dealer, self.state.round_number)

    def end_game(self) -> GameState:
        """Reset the engine and return the final state."""
        self._invalidate_cache()
        final_state = self.state
        scores = [p.score for p in final_state.players]
        self._emit("end_game", {"scores": scores})
        self.state = GameState(wall=Wall())
        wall = self.state.wall
        assert wall is not None
        self.state.dora_indicators = wall.dora_indicators.copy()
        self.state.dead_wall = wall.dead_wall.copy()
        self.state.players = [Player(name=f"Player {i}") for i in range(4)]
        self.state.current_player = 0
        self.state.honba = 0
        self.state.riichi_sticks = 0
        self.state.kan_count = 0
        self.state.seat_winds = []
        self.state.last_discard = None
        self.state.last_discard_player = None
        self._claims_open = False
        return final_state

    def _compute_allowed_actions(self, player_index: int) -> list[str]:
        """Compute allowed actions for ``player_index``."""

        state = self.state
        player = state.players[player_index]
        tiles = player.hand.tiles

        actions: set[str] = set()

        last = state.last_discard
        last_player = state.last_discard_player

        if player_index in state.waiting_for_claims:
            actions.add("skip")

        if last is not None and last_player is not None and last_player != player_index:
            same = [t for t in tiles if t.suit == last.suit and t.value == last.value]
            if len(same) >= 2:
                actions.add("pon")
            if len(same) >= 3:
                actions.add("kan")
            if (
                (last_player + 1) % len(state.players) == player_index
                and last.suit in {"man", "pin", "sou"}
            ):
                def has(v: int) -> bool:
                    return any(t.suit == last.suit and t.value == v for t in tiles)

                if has(last.value - 2) and has(last.value - 1):
                    actions.add("chi")
                if has(last.value - 1) and has(last.value + 1):
                    actions.add("chi")
                if has(last.value + 1) and has(last.value + 2):
                    actions.add("chi")

        counts: dict[tuple[str, int], int] = {}
        for t in tiles:
            key = (t.suit, t.value)
            counts[key] = counts.get(key, 0) + 1
            if counts[key] >= 4:
                actions.add("kan")

        if not player.riichi and self._is_tenpai(player):
            actions.add("riichi")

        return sorted(actions)

    def get_allowed_actions(self, player_index: int) -> list[str]:
        """Return cached allowed actions for ``player_index``."""

        if player_index < 0 or player_index >= len(self.state.players):
            raise IndexError("Invalid player index")

        if self._cached_allowed_actions is None or len(self._cached_allowed_actions) != len(self.state.players):
            self._cached_allowed_actions = [self._compute_allowed_actions(i) for i in range(len(self.state.players))]

        return self._cached_allowed_actions[player_index]
