"""Mahjong game engine wrapper."""
from __future__ import annotations

from .models import GameState, Tile, Meld, GameEvent
from .player import Player
from .wall import Wall
from .rules import RuleSet, StandardRuleSet, _tile_to_index
from mahjong.shanten import Shanten
from mahjong.hand_calculating.hand_response import HandResponse


class MahjongEngine:
    """Simplified engine that wraps the `mahjong` library."""

    def __init__(self, ruleset: RuleSet | None = None) -> None:
        self.ruleset: RuleSet = ruleset or StandardRuleSet()
        self.state = GameState(wall=Wall())
        self.state.players = [Player(name=f"Player {i}") for i in range(4)]
        self.state.current_player = 0
        self.events: list[GameEvent] = []
        self._emit("start_game", {"state": self.state})
        self.start_kyoku(dealer=0, round_number=1)

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
        self.events.append(GameEvent(name=name, payload=payload))

    def _is_tenpai(self, player: Player) -> bool:
        """Return True if ``player`` is in tenpai."""
        counts = [0] * 34
        for t in player.hand.tiles:
            counts[_tile_to_index(t)] += 1
        for meld in player.hand.melds:
            for t in meld.tiles:
                counts[_tile_to_index(t)] += 1
        if sum(counts) > 14 and player.hand.tiles:
            counts[_tile_to_index(player.hand.tiles[-1])] -= 1
        return Shanten().calculate_shanten(counts) == 0

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

    def start_kyoku(self, dealer: int, round_number: int) -> None:
        """Begin a new hand with fresh tiles."""
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
        assert self.state.wall is not None
        tile = self.state.wall.draw_tile()
        self.state.players[player_index].draw(tile)
        self._emit("draw_tile", {"player_index": player_index, "tile": tile})
        player = self.state.players[player_index]
        if len(player.river) == 0 and not player.hand.melds:
            self._check_nine_terminals(player)
        if self.state.wall.remaining_tiles == 0:
            self._resolve_ryukyoku("wall_empty")
        else:
            self.state.current_player = (player_index + 1) % len(self.state.players)
        return tile

    def discard_tile(self, player_index: int, tile: Tile) -> None:
        """Discard a tile from the specified player's hand."""
        player = self.state.players[player_index]
        if player.must_tsumogiri and player.hand.tiles and player.hand.tiles[-1] is not tile:
            raise ValueError("Must discard the drawn tile after declaring riichi")
        player.discard(tile)
        player.must_tsumogiri = False
        self._emit("discard", {"player_index": player_index, "tile": tile})
        self.state.current_player = (player_index + 1) % len(self.state.players)
        self.state.last_discard = tile
        self.state.last_discard_player = player_index

    def declare_riichi(self, player_index: int) -> None:
        """Declare riichi for the given player."""
        player = self.state.players[player_index]
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

        meld = Meld(tiles=tiles, type="chi")
        player.hand.melds.append(meld)
        self.state.last_discard = None
        self.state.last_discard_player = None
        self._emit("meld", {"player_index": player_index, "meld": meld})

    def call_pon(self, player_index: int, tiles: list[Tile]) -> None:
        """Form a pon meld using the given tiles."""
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

        meld = Meld(tiles=tiles, type="pon")
        player.hand.melds.append(meld)
        self.state.last_discard = None
        self.state.last_discard_player = None
        self._emit("meld", {"player_index": player_index, "meld": meld})

    def call_kan(self, player_index: int, tiles: list[Tile]) -> None:
        """Form a kan meld. Supports open, closed and added kan."""
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
            meld = Meld(tiles=meld_tiles, type="kan")
            player.hand.melds.append(meld)
            self.state.last_discard = None
            self.state.last_discard_player = None
            self._draw_replacement_tile(player)
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
                self._draw_replacement_tile(player)
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
        self._draw_replacement_tile(player)
        self._emit("meld", {"player_index": player_index, "meld": meld})
        self.state.kan_count += 1
        if self.state.kan_count >= 4:
            self._resolve_ryukyoku("four_kans")

    def declare_tsumo(self, player_index: int, win_tile: Tile) -> HandResponse:
        """Declare a self-drawn win and return scoring info."""
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
                "result": result,
                "scores": scores,
            },
        )
        self.advance_hand(player_index)
        return result

    def declare_ron(self, player_index: int, win_tile: Tile) -> HandResponse:
        """Declare a win on another player's discard."""
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
            {"player_index": player_index, "result": result, "scores": scores},
        )
        self.advance_hand(player_index)
        return result

    def skip(self, player_index: int) -> None:
        """Skip action for the specified player."""
        if player_index != self.state.current_player:
            return
        self.state.current_player = (self.state.current_player + 1) % len(
            self.state.players
        )
        self._emit("skip", {"player_index": player_index})

    def advance_hand(self, winner_index: int | None = None) -> None:
        """Move to the next hand and handle dealer rotation."""
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
        return final_state
