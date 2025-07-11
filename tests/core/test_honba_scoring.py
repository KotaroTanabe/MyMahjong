from core.mahjong_engine import MahjongEngine
from core.models import Tile
from core.rules import RuleSet
from mahjong.hand_calculating.hand_response import HandResponse


class ScoringRuleSet(RuleSet):
    def calculate_score(self, hand_tiles, melds, win_tile, *, is_tsumo=True, **_):
        return HandResponse(han=1, cost={"total": 8000})


def test_tsumo_honba_bonus() -> None:
    engine = MahjongEngine(ruleset=ScoringRuleSet())
    engine.pop_events()
    engine.state.honba = 2
    tile = Tile("man", 1)
    engine.state.players[0].hand.tiles.append(tile)
    start_scores = [p.score for p in engine.state.players]
    engine.declare_tsumo(0, tile)
    assert engine.state.players[0].score == start_scores[0] + 8000 + 600
    assert engine.state.players[1].score == start_scores[1] - 2866


def test_ron_honba_bonus() -> None:
    engine = MahjongEngine(ruleset=ScoringRuleSet())
    engine.pop_events()
    engine.state.honba = 1
    tile = Tile("man", 2)
    engine.state.players[1].hand.tiles.append(tile)
    engine.state.current_player = 1
    engine.discard_tile(1, tile)
    engine.state.players[0].hand.tiles.append(Tile("man", 2))
    start_scores = [p.score for p in engine.state.players]
    engine.declare_ron(0, Tile("man", 2))
    assert engine.state.players[0].score == start_scores[0] + 8000 + 300
    assert engine.state.players[1].score == start_scores[1] - (8000 + 300)
