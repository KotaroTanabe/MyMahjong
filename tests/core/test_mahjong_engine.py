from core.mahjong_engine import MahjongEngine
from core.models import Tile


def test_engine_initialization() -> None:
    engine = MahjongEngine()
    assert len(engine.state.players) == 4
    assert engine.state.wall is not None


def test_draw_tile_updates_state() -> None:
    engine = MahjongEngine()
    assert engine.state.wall is not None
    tile = Tile(suit="pin", value=3)
    engine.state.wall.tiles.append(tile)
    engine.draw_tile(0)
    assert tile in engine.state.players[0].hand.tiles


def test_discard_tile_updates_state() -> None:
    engine = MahjongEngine()
    tile = Tile(suit="pin", value=4)
    # Add tile to player's hand directly for simplicity
    engine.state.players[1].draw(tile)
    engine.discard_tile(1, tile)
    assert tile not in engine.state.players[1].hand.tiles
    assert tile in engine.state.players[1].river


def test_calculate_score_returns_value() -> None:
    engine = MahjongEngine()
    player = engine.state.players[0]
    tiles = [
        Tile("man", 1),
        Tile("man", 2),
        Tile("man", 3),
        Tile("man", 4),
        Tile("man", 5),
        Tile("man", 6),
        Tile("man", 7),
        Tile("man", 8),
        Tile("man", 9),
        Tile("pin", 2),
        Tile("pin", 3),
        Tile("pin", 4),
        Tile("sou", 5),
        Tile("sou", 5),
    ]
    player.hand.tiles = tiles.copy()
    result = engine.calculate_score(0, tiles[-1])
    assert result.han is not None and result.han > 0


def test_call_pon_adds_meld() -> None:
    engine = MahjongEngine()
    tiles = [Tile("man", 1) for _ in range(3)]
    player = engine.state.players[0]
    player.hand.tiles.extend(tiles[:2])
    engine.call_pon(0, tiles)
    assert len(player.hand.melds) == 1
    assert player.hand.melds[0].type == "pon"


def test_end_game_resets_state() -> None:
    engine = MahjongEngine()
    old_state = engine.state
    finished = engine.end_game()
    assert finished is old_state
    assert engine.state is not old_state
