from core.mahjong_engine import MahjongEngine
from core.models import Tile


def test_draw_advances_turn() -> None:
    engine = MahjongEngine()
    current = engine.state.current_player
    engine.draw_tile(current)
    assert engine.state.current_player == (current + 1) % len(engine.state.players)


def test_discard_advances_turn() -> None:
    engine = MahjongEngine()
    current = engine.state.current_player
    tile = engine.state.players[current].hand.tiles[0]
    for i, p in enumerate(engine.state.players):
        if i != current:
            p.hand.tiles.clear()
    engine.discard_tile(current, tile)
    assert engine.state.current_player == (current + 1) % len(engine.state.players)


def test_discard_waits_for_skip_when_call_possible() -> None:
    engine = MahjongEngine()
    engine.pop_events()
    tile = Tile("man", 1)
    engine.state.players[0].hand.tiles = [tile]
    engine.state.players[1].hand.tiles = [Tile("man", 1), Tile("man", 1)]
    for p in engine.state.players[2:]:
        p.hand.tiles.clear()
    engine.discard_tile(0, tile)
    assert engine.state.current_player == 0
    engine.skip(1)
    assert engine.state.current_player == 1

