from core.mahjong_engine import MahjongEngine
from core.models import Tile


def _set_tenpai_hand(player) -> None:
    player.hand.tiles = [
        Tile("man", 1), Tile("man", 1),
        Tile("man", 2), Tile("man", 2),
        Tile("man", 3), Tile("man", 3),
        Tile("pin", 4), Tile("pin", 4),
        Tile("pin", 5), Tile("pin", 5),
        Tile("sou", 6), Tile("sou", 6),
        Tile("sou", 7), Tile("sou", 8),
    ]


def test_ippatsu_flag_set_and_cleared_on_draw() -> None:
    engine = MahjongEngine()
    player = engine.state.players[0]
    _set_tenpai_hand(player)
    drawn = player.hand.tiles[-1]
    engine.declare_riichi(0)
    engine.discard_tile(0, drawn)
    assert player.ippatsu_available
    # Simulate passing of claims and player's next draw
    engine.state.waiting_for_claims = []
    engine.state.current_player = 0
    engine.draw_tile(0)
    assert not player.ippatsu_available


def test_ippatsu_cleared_on_other_player_meld() -> None:
    engine = MahjongEngine()
    player0 = engine.state.players[0]
    player1 = engine.state.players[1]
    _set_tenpai_hand(player0)
    engine.declare_riichi(0)
    discard = player0.hand.tiles[-1]
    engine.discard_tile(0, discard)
    player1.hand.tiles = [
        Tile(discard.suit, discard.value),
        Tile(discard.suit, discard.value),
        *([Tile("pin", 1)] * 11),
    ]
    engine.state.current_player = 1
    engine.call_pon(1, [
        Tile(discard.suit, discard.value),
        Tile(discard.suit, discard.value),
        discard,
    ])
    assert not player0.ippatsu_available


def test_ippatsu_persists_until_draw() -> None:
    engine = MahjongEngine()
    player = engine.state.players[0]
    _set_tenpai_hand(player)
    win_tile = Tile("sou", 9)
    engine.declare_riichi(0)
    drawn = player.hand.tiles[-1]
    engine.discard_tile(0, drawn)
    player.hand.tiles.append(win_tile)
    assert player.ippatsu_available
    engine.declare_tsumo(0, win_tile)
    assert not player.ippatsu_available
