from core.player import Player
from core.models import Tile


def test_player_draw_and_discard() -> None:
    player = Player(name="Test")
    tile = Tile(suit="man", value=5)
    player.draw(tile)
    assert tile in player.hand.tiles
    player.discard(tile)
    assert tile not in player.hand.tiles
    assert tile in player.river


def test_player_declare_riichi() -> None:
    player = Player(name="Test")
    start_score = player.score
    player.declare_riichi()
    assert player.riichi
    assert player.score == start_score - 1000


def test_discard_removes_specific_instance() -> None:
    player = Player(name="Test")
    tile1 = Tile(suit="man", value=1)
    tile2 = Tile(suit="man", value=1)
    player.draw(tile1)
    player.draw(tile2)
    player.discard(tile2)
    assert all(t is not tile2 for t in player.hand.tiles)
    assert tile1 in player.hand.tiles


def test_player_has_seat_wind() -> None:
    player = Player(name="Test")
    assert player.seat_wind == "east"
