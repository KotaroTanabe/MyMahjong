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
    # 14 tiles are reserved for the dead wall
    assert wall.remaining_tiles == 122
    counts: dict[tuple[str, int], int] = {}
    for t in wall.tiles + wall.dead_wall:
        key = (t.suit, t.value)
        counts[key] = counts.get(key, 0) + 1
    assert all(c == 4 for c in counts.values())


def test_wall_remaining_decreases() -> None:
    wall = Wall()
    before = wall.remaining_tiles
    wall.draw_tile()
    assert wall.remaining_tiles == before - 1


def test_wall_sets_dead_wall_and_dora() -> None:
    wall = Wall()
    assert len(wall.dead_wall) == 14
    assert len(wall.dora_indicators) == 1
    assert wall.dora_indicators[0] in wall.dead_wall
