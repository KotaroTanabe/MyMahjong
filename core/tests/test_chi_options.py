from core.mahjong_engine import MahjongEngine
from core.models import Tile


def test_get_chi_options_multiple() -> None:
    engine = MahjongEngine()
    engine.state.last_discard = Tile("man", 5)
    engine.state.last_discard_player = 0
    engine.state.waiting_for_claims = [1, 2, 3]
    player = engine.state.players[1]
    player.hand.tiles = [
        Tile("man", 3),
        Tile("man", 4),
        Tile("man", 6),
        Tile("pin", 1),
    ]
    opts = engine.get_chi_options(1)
    values = [[t.value for t in pair] for pair in opts]
    assert sorted(values) == [[3, 4], [4, 6]]
