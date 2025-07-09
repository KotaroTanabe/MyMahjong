import pytest
from core.mahjong_engine import MahjongEngine
from core.models import Tile


def test_call_kan_emits_meld_and_draw_tile() -> None:
    engine = MahjongEngine()
    engine.pop_events()
    tiles = [Tile("man", 5) for _ in range(4)]
    engine.state.players[0].hand.tiles = tiles.copy()
    engine.call_kan(0, tiles)
    events = engine.pop_events()
    names = [e.name for e in events]
    assert set(names) == {"meld", "draw_tile"}
    assert names[0] == "draw_tile"
    assert names[1] == "meld"


