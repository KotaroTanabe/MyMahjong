from core.mahjong_engine import MahjongEngine
from core.rules import RuleSet
from core.models import Tile
from core.actions import RON
from mahjong.hand_calculating.hand_response import HandResponse


class AlwaysWinRules(RuleSet):
    def calculate_score(self, hand_tiles, melds, win_tile, *, is_tsumo=True):
        return HandResponse(han=1, cost={"total": 8000})


class NeverWinRules(RuleSet):
    def calculate_score(self, hand_tiles, melds, win_tile, *, is_tsumo=True):
        return HandResponse(han=0)


def test_allowed_actions_include_ron_when_winning() -> None:
    engine = MahjongEngine(ruleset=AlwaysWinRules())
    tile = engine.state.players[0].hand.tiles[-1]
    engine.discard_tile(0, tile)
    engine.state.players[1].hand.tiles = [Tile("pin", 1)] * 13
    actions = engine.get_allowed_actions(1)
    assert RON in actions


def test_allowed_actions_exclude_ron_when_not_winning() -> None:
    engine = MahjongEngine(ruleset=NeverWinRules())
    tile = engine.state.players[0].hand.tiles[-1]
    engine.discard_tile(0, tile)
    engine.state.players[1].hand.tiles = [Tile("pin", 1)] * 13
    actions = engine.get_allowed_actions(1)
    assert RON not in actions
