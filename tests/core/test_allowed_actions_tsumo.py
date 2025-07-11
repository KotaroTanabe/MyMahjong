from core.actions import TSUMO
from core.mahjong_engine import MahjongEngine
from core.rules import RuleSet
from mahjong.hand_calculating.hand_response import HandResponse


class AlwaysWinRules(RuleSet):
    def calculate_score(self, hand_tiles, melds, win_tile, *, is_tsumo=True):
        return HandResponse(han=1, cost={"total": 8000})


class NeverWinRules(RuleSet):
    def calculate_score(self, hand_tiles, melds, win_tile, *, is_tsumo=True):
        return HandResponse(han=0)


def test_allowed_actions_include_tsumo_when_winning() -> None:
    engine = MahjongEngine(ruleset=AlwaysWinRules())
    actions = engine.get_allowed_actions(0)
    assert "tsumo" in actions


def test_allowed_actions_exclude_tsumo_when_not_winning() -> None:
    engine = MahjongEngine(ruleset=NeverWinRules())
    actions = engine.get_allowed_actions(0)
    assert "tsumo" not in actions
