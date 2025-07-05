from core.wall import Wall
from core.models import Tile


def test_wall_draw_tile() -> None:
    tile1 = Tile(suit="sou", value=2)
    tile2 = Tile(suit="sou", value=3)
    wall = Wall(tiles=[tile1, tile2])
    drawn = wall.draw_tile()
    assert drawn == tile2
    assert wall.tiles == [tile1]


def test_wall_initializes_standard_set() -> None:
    wall = Wall()
    assert wall.remaining_tiles == 136
    counts: dict[tuple[str, int], int] = {}
    for t in wall.tiles:
        key = (t.suit, t.value)
        counts[key] = counts.get(key, 0) + 1
    assert all(c == 4 for c in counts.values())


def test_wall_remaining_decreases() -> None:
    wall = Wall()
    before = wall.remaining_tiles
    wall.draw_tile()
    assert wall.remaining_tiles == before - 1


def test_remaining_yama_tiles_excludes_wanpai() -> None:
    wall = Wall()
    assert wall.remaining_yama_tiles == 136 - wall.wanpai_size
    wall.draw_tile()
    assert wall.remaining_yama_tiles == 136 - wall.wanpai_size - 1
    # Remove all drawable tiles
    wall.tiles = wall.tiles[-wall.wanpai_size:]
    assert wall.remaining_yama_tiles == 0
