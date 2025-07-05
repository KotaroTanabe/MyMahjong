"""Mahjong game engine wrapper."""
from __future__ import annotations

from .models import GameState, Tile, Meld, GameEvent
from .player import Player
from .wall import Wall
from .rules import RuleSet, StandardRuleSet
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

    def _emit(self, name: str, payload: dict) -> None:
        self.events.append(GameEvent(name=name, payload=payload))

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
        if self.state.wall.remaining_tiles == 0:
            self._emit("ryukyoku", {"reason": "wall_empty"})
        else:
            self.state.current_player = (player_index + 1) % len(self.state.players)
        return tile

    def discard_tile(self, player_index: int, tile: Tile) -> None:
        """Discard a tile from the specified player's hand."""
        self.state.players[player_index].discard(tile)
        self._emit("discard", {"player_index": player_index, "tile": tile})
        self.state.current_player = (player_index + 1) % len(self.state.players)

    def declare_riichi(self, player_index: int) -> None:
        """Declare riichi for the given player."""
        player = self.state.players[player_index]
        player.declare_riichi()
        self._emit("riichi", {"player_index": player_index})

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
        assert len(tiles) == 3, "Chi requires three tiles"
        player = self.state.players[player_index]
        for t in tiles:
            if t in player.hand.tiles:
                player.hand.tiles.remove(t)
        meld = Meld(tiles=tiles, type="chi")
        player.hand.melds.append(meld)
        self._emit("meld", {"player_index": player_index, "meld": meld})

    def call_pon(self, player_index: int, tiles: list[Tile]) -> None:
        """Form a pon meld using the given tiles."""
        assert len(tiles) == 3, "Pon requires three tiles"
        player = self.state.players[player_index]
        for t in tiles:
            if t in player.hand.tiles:
                player.hand.tiles.remove(t)
        meld = Meld(tiles=tiles, type="pon")
        player.hand.melds.append(meld)
        self._emit("meld", {"player_index": player_index, "meld": meld})

    def call_kan(self, player_index: int, tiles: list[Tile]) -> None:
        """Form a kan meld using the given tiles."""
        assert len(tiles) == 4, "Kan requires four tiles"
        player = self.state.players[player_index]
        for t in tiles:
            if t in player.hand.tiles:
                player.hand.tiles.remove(t)
        meld = Meld(tiles=tiles, type="kan")
        player.hand.melds.append(meld)
        self._emit("meld", {"player_index": player_index, "meld": meld})

    def declare_tsumo(self, player_index: int, win_tile: Tile) -> HandResponse:
        """Declare a self-drawn win and return scoring info."""
        result = self.calculate_score(player_index, win_tile)
        player = self.state.players[player_index]
        if result.cost and "total" in result.cost:
            player.score += int(result.cost["total"])
        scores = [p.score for p in self.state.players]
        self._emit(
            "tsumo",
            {
                "player_index": player_index,
                "result": result,
                "scores": scores,
            },
        )
        return result

    def declare_ron(self, player_index: int, win_tile: Tile) -> HandResponse:
        """Declare a win on another player's discard."""
        result = self.calculate_score(player_index, win_tile)
        player = self.state.players[player_index]
        if result.cost and "total" in result.cost:
            player.score += int(result.cost["total"])
        scores = [p.score for p in self.state.players]
        self._emit(
            "ron",
            {"player_index": player_index, "result": result, "scores": scores},
        )
        return result

    def skip(self, player_index: int) -> None:
        """Skip action for the specified player."""
        if player_index != self.state.current_player:
            return
        self.state.current_player = (self.state.current_player + 1) % len(
            self.state.players
        )
        self._emit("skip", {"player_index": player_index})

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
        self.state.seat_winds = []
        return final_state
