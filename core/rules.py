from __future__ import annotations

"""Rule set abstractions for scoring and validation."""

from dataclasses import dataclass

from mahjong.hand_calculating.hand import HandCalculator
from mahjong.hand_calculating.hand_config import HandConfig
from mahjong.hand_calculating.hand_response import HandResponse
from mahjong.tile import TilesConverter
from mahjong.constants import EAST, SOUTH, WEST, NORTH

from .models import Tile, Meld


def _tile_to_index(tile: Tile) -> int:
    if tile.suit == "man":
        return tile.value - 1
    if tile.suit == "pin":
        return 9 + tile.value - 1
    if tile.suit == "sou":
        return 18 + tile.value - 1
    if tile.suit == "wind":
        return 27 + tile.value - 1
    if tile.suit == "dragon":
        return 31 + tile.value - 1
    raise ValueError(f"Unknown suit: {tile.suit}")


class RuleSet:
    """Base interface for Mahjong rule sets."""

    def calculate_score(
        self,
        hand_tiles: list[Tile],
        melds: list[Meld],
        win_tile: Tile,
        *,
        is_tsumo: bool = True,
        is_riichi: bool = False,
        is_ippatsu: bool = False,
        seat_wind: str | None = None,
        round_wind: str | None = None,
    ) -> HandResponse:
        """Return scoring for the given hand."""
        raise NotImplementedError


@dataclass
class StandardRuleSet(RuleSet):
    """Default rules using the `mahjong` library's hand calculator."""

    calculator: HandCalculator = HandCalculator()

    def calculate_score(
        self,
        hand_tiles: list[Tile],
        melds: list[Meld],
        win_tile: Tile,
        *,
        is_tsumo: bool = True,
        is_riichi: bool = False,
        is_ippatsu: bool = False,
        seat_wind: str | None = None,
        round_wind: str | None = None,
    ) -> HandResponse:
        counts = [0] * 34
        for t in hand_tiles:
            counts[_tile_to_index(t)] += 1
        for meld in melds:
            for t in meld.tiles:
                counts[_tile_to_index(t)] += 0  # meld tiles already removed
        tiles_136 = TilesConverter.to_136_array(counts)
        win_tile_136 = TilesConverter.find_34_tile_in_136_array(
            _tile_to_index(win_tile), tiles_136
        )
        assert win_tile_136 is not None, "Winning tile not found in hand"
        wind_map = {
            "east": EAST,
            "south": SOUTH,
            "west": WEST,
            "north": NORTH,
        }
        config = HandConfig(
            is_tsumo=is_tsumo,
            is_riichi=is_riichi,
            is_ippatsu=is_ippatsu,
            player_wind=wind_map.get(seat_wind) if seat_wind else None,
            round_wind=wind_map.get(round_wind) if round_wind else None,
        )
        return self.calculator.estimate_hand_value(
            tiles_136, win_tile_136, config=config
        )
