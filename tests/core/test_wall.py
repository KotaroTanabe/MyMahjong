from core.wall import Wall
from core.models import Tile


def test_wall_draw_tile() -> None:
    tile1 = Tile(suit="sou", value=2)
    tile2 = Tile(suit="sou", value=3)
    wall = Wall(tiles=[tile1, tile2])
    drawn = wall.draw_tile()
    assert drawn == tile2
    assert wall.tiles == [tile1]
