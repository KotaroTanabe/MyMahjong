from core.mahjong_engine import MahjongEngine
from core.models import Tile


def test_ryukyoku_noten_penalty() -> None:
    engine = MahjongEngine()
    engine.pop_events()

    def fake_is_tenpai(player):
        idx = engine.state.players.index(player)
        return idx % 2 == 0

    engine._is_tenpai = fake_is_tenpai  # type: ignore
    assert engine.state.wall is not None
    engine.state.wall.tiles = [Tile("man", 1)]
    engine.draw_tile(engine.state.current_player)
    events = engine.pop_events()
    ryukyoku = next(e for e in events if e.name == "ryukyoku")
    assert ryukyoku.payload["tenpai"] == [True, False, True, False]
    assert ryukyoku.payload["scores"][0] == 26500
    assert ryukyoku.payload["scores"][1] == 23500
