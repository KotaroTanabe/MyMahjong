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
