from core.mahjong_engine import MahjongEngine


def test_auto_draw_after_all_players_skip() -> None:
    engine = MahjongEngine()
    discarder = engine.state.dealer
    next_player = (discarder + 1) % 4
    player = engine.state.players[discarder]
    tile = player.hand.tiles[-1]
    engine.discard_tile(discarder, tile)
    # First player (next player) skips claim
    engine.skip(next_player)
    # Remaining players skip
    engine.skip((discarder + 2) % 4)
    engine.skip((discarder + 3) % 4)
    assert len(engine.state.players[next_player].hand.tiles) == 14
    assert engine.state.current_player == next_player
