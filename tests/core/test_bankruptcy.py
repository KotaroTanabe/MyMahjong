from core.mahjong_engine import MahjongEngine
from core.models import Tile
from core.rules import RuleSet
from mahjong.hand_calculating.hand_response import HandResponse


class BigScoreRuleSet(RuleSet):
    def calculate_score(self, hand_tiles, melds, win_tile, *, is_tsumo=True):
        return HandResponse(han=1, cost={"total": 40000})


def test_end_game_on_bankruptcy() -> None:
    engine = MahjongEngine(ruleset=BigScoreRuleSet())
    engine.pop_events()
    engine.state.players[1].score = 1000
    tile = Tile("man", 1)
    engine.state.players[0].hand.tiles.append(tile)
    engine.declare_tsumo(0, tile)
    events = engine.pop_events()
    assert events[-1].name == "end_game"
    assert events[-1].payload.get("reason") == "bankruptcy"
