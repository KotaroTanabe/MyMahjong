from core.models import Tile, Hand


def test_models_basic() -> None:
    tile = Tile(suit="man", value=1)
    hand = Hand()
    hand.tiles.append(tile)
    assert hand.tiles[0] == tile
