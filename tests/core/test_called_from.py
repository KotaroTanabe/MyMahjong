import pytest
from core.mahjong_engine import MahjongEngine
from core.models import Tile


def _setup_discard(engine: MahjongEngine, discarder_idx: int, tile: Tile) -> None:
    discarder = engine.state.players[discarder_idx]
    discarder.hand.tiles.append(tile)
    engine.state.current_player = discarder_idx
    engine.discard_tile(discarder_idx, tile)


@pytest.mark.parametrize(
    "discarder_idx,expected",
    [(3, 1), (2, 2), (1, 3)],
)
def test_call_pon_called_from(discarder_idx: int, expected: int) -> None:
    engine = MahjongEngine()
    tile = Tile("man", 1)
    _setup_discard(engine, discarder_idx, tile)
    caller = engine.state.players[0]
    caller.hand.tiles.extend([Tile("man", 1), Tile("man", 1)])
    engine.call_pon(0, [Tile("man", 1), Tile("man", 1), tile])
    meld = caller.hand.melds[0]
    assert meld.called_from == expected


def test_call_chi_called_from_left() -> None:
    engine = MahjongEngine()
    tile = Tile("man", 3)
    _setup_discard(engine, 3, tile)
    caller = engine.state.players[0]
    caller.hand.tiles.extend([Tile("man", 1), Tile("man", 2)])
    engine.call_chi(0, [Tile("man", 1), Tile("man", 2), tile])
    meld = caller.hand.melds[0]
    assert meld.called_from == 1
