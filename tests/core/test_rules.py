from core.rules import RuleSet, StandardRuleSet
from core.mahjong_engine import MahjongEngine
from core.models import Tile, Meld
from mahjong.hand_calculating.hand_response import HandResponse


class DummyRuleSet(RuleSet):
    def __init__(self) -> None:
        self.called_with: tuple | None = None

    def calculate_score(
        self,
        hand_tiles: list[Tile],
        melds: list[Meld],
        win_tile: Tile,
        *,
        is_tsumo: bool = True,
        **_: object,
    ) -> HandResponse:
        self.called_with = (hand_tiles[:], melds[:], win_tile, is_tsumo)
        return HandResponse(han=0)


def test_engine_delegates_to_ruleset() -> None:
    ruleset = DummyRuleSet()
    engine = MahjongEngine(ruleset=ruleset)
    player = engine.state.players[0]
    tile = Tile("man", 1)
    player.hand.tiles.append(tile)
    engine.calculate_score(0, tile)
    assert ruleset.called_with is not None
    hand_tiles, melds, win_tile, is_tsumo = ruleset.called_with
    assert win_tile == tile
    assert hand_tiles[-1] == tile
    assert is_tsumo


def test_standard_ruleset_scoring() -> None:
    ruleset = StandardRuleSet()
    engine = MahjongEngine(ruleset=ruleset)
    player = engine.state.players[0]
    tiles = [Tile("man", v) for v in range(1, 10)] + [Tile("pin", 1)]
    player.hand.tiles = tiles
    result = engine.calculate_score(0, tiles[-1])
    assert isinstance(result, HandResponse)


def test_engine_passes_flags_to_ruleset() -> None:
    class CaptureRuleSet(RuleSet):
        def __init__(self) -> None:
            self.kwargs: dict[str, object] | None = None

        def calculate_score(
            self,
            hand_tiles: list[Tile],
            melds: list[Meld],
            win_tile: Tile,
            *,
            is_tsumo: bool = True,
            **kwargs: object,
        ) -> HandResponse:
            self.kwargs = kwargs
            return HandResponse(han=1)

    ruleset = CaptureRuleSet()
    engine = MahjongEngine(ruleset=ruleset)
    engine.state.round_number = 5  # south round
    player = engine.state.players[0]
    player.seat_wind = "south"
    player.riichi = True
    player.ippatsu_available = True
    tile = Tile("man", 3)
    player.hand.tiles.append(tile)
    engine.calculate_score(0, tile, is_tsumo=False)
    assert ruleset.kwargs == {
        "is_riichi": True,
        "is_ippatsu": True,
        "seat_wind": "south",
        "round_wind": "south",
    }


def test_riichi_and_ippatsu_scoring() -> None:
    ruleset = StandardRuleSet()
    engine = MahjongEngine(ruleset=ruleset)
    engine.state.round_number = 1
    player = engine.state.players[0]
    player.seat_wind = "east"
    tiles = (
        [Tile("man", v) for v in range(1, 10)]
        + [Tile("pin", 1), Tile("pin", 2), Tile("pin", 3)]
        + [Tile("wind", 1), Tile("wind", 1)]
    )
    player.hand.tiles = tiles
    player.riichi = True
    player.ippatsu_available = True
    win_tile = tiles[11]
    result = engine.calculate_score(0, win_tile)
    yaku_names = [y.name for y in result.yaku]
    assert "Riichi" in yaku_names
    assert "Ippatsu" in yaku_names
