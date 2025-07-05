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
