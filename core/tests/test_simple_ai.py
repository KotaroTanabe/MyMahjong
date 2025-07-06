from core.mahjong_engine import MahjongEngine
from core.simple_ai import smart_turn
from core.shanten_quiz import calculate_shanten
from core.models import Tile


HAND_14 = [
    Tile("man", 1), Tile("man", 2), Tile("man", 3),
    Tile("pin", 1), Tile("pin", 2), Tile("pin", 3),
    Tile("sou", 1), Tile("sou", 2), Tile("sou", 3),
    Tile("man", 7), Tile("man", 8), Tile("man", 9),
    Tile("pin", 9), Tile("sou", 9),
]

HAND_13 = HAND_14[:-1]


def test_smart_turn_discards_without_increasing_shanten() -> None:
    engine = MahjongEngine()
    dealer = engine.state.dealer
    player = engine.state.players[dealer]
    player.hand.tiles = HAND_14.copy()
    before = calculate_shanten(player.hand.tiles)

    discarded = smart_turn(engine, dealer)

    after = calculate_shanten(player.hand.tiles)
    assert after <= before
    assert discarded == player.river[-1]
    assert len(player.hand.tiles) == 13


def test_smart_turn_draws_when_needed() -> None:
    engine = MahjongEngine()
    idx = (engine.state.dealer + 1) % 4
    player = engine.state.players[idx]
    player.hand.tiles = HAND_13.copy()
    before = calculate_shanten(player.hand.tiles)

    discarded = smart_turn(engine, idx)

    after = calculate_shanten(player.hand.tiles)
    assert after <= before
    assert discarded == player.river[-1]
    assert len(player.hand.tiles) == 13
