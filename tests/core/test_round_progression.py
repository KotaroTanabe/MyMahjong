from core.mahjong_engine import MahjongEngine
from core.models import Tile


def test_dealer_rotates_and_round_increments() -> None:
    engine = MahjongEngine()
    engine.pop_events()
    tile = engine.state.players[1].hand.tiles[0]
    engine.declare_tsumo(1, tile)
    assert engine.state.dealer == 1
    assert engine.state.round_number == 2
    assert engine.state.honba == 0


def test_honba_increments_on_draw() -> None:
    engine = MahjongEngine()
    engine.pop_events()
    assert engine.state.wall is not None
    engine.state.wall.tiles = [Tile("pin", 1)]
    engine.draw_tile(engine.state.current_player)
    assert engine.state.honba == 1
    assert engine.state.round_number == 1
    assert engine.state.dealer == 0


def test_hanchan_ends_after_south4() -> None:
    engine = MahjongEngine(max_rounds=8)
    engine.pop_events()
    for _ in range(8):
        winner = (engine.state.dealer + 1) % 4
        tile = engine.state.players[winner].hand.tiles[0]
        engine.declare_tsumo(winner, tile)
    events = engine.pop_events()
    assert events[-1].name == "end_game"


def test_east_only_ends_after_east4() -> None:
    engine = MahjongEngine(max_rounds=4)
    engine.pop_events()
    for _ in range(4):
        winner = (engine.state.dealer + 1) % 4
        tile = engine.state.players[winner].hand.tiles[0]
        engine.declare_tsumo(winner, tile)
    events = engine.pop_events()
    assert events[-1].name == "end_game"
