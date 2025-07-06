import pytest
from core.mahjong_engine import MahjongEngine
from core.models import Tile, Meld


def _tenpai_tiles() -> list[Tile]:
    return [
        Tile("man", 1), Tile("man", 1),
        Tile("man", 2), Tile("man", 2),
        Tile("man", 3), Tile("man", 3),
        Tile("pin", 4), Tile("pin", 4),
        Tile("pin", 5), Tile("pin", 5),
        Tile("sou", 6), Tile("sou", 6),
        Tile("sou", 7), Tile("sou", 8),
    ]


def test_riichi_rejected_when_not_tenpai() -> None:
    engine = MahjongEngine()
    player = engine.state.players[0]
    base = [
        Tile("man", 1), Tile("man", 1), Tile("man", 1),
        Tile("man", 2), Tile("man", 3), Tile("man", 4),
        Tile("man", 5), Tile("man", 6), Tile("man", 7),
        Tile("pin", 1), Tile("pin", 2), Tile("sou", 3), Tile("sou", 4),
    ]
    player.hand.tiles = base + [Tile("sou", 6)]
    with pytest.raises(ValueError):
        engine.declare_riichi(0)


def test_riichi_rejected_with_open_meld() -> None:
    engine = MahjongEngine()
    player = engine.state.players[0]
    player.hand.tiles = _tenpai_tiles()
    player.hand.melds.append(
        Meld(tiles=[Tile("man", 1)] * 3, type="pon")
    )
    with pytest.raises(ValueError):
        engine.declare_riichi(0)
