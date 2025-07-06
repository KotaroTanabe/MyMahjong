from core.mahjong_engine import MahjongEngine
from core.simple_ai import tsumogiri_turn


def test_tsumogiri_turn_discards_when_already_drawn() -> None:
    engine = MahjongEngine()
    dealer = engine.state.dealer
    player = engine.state.players[dealer]
    assert len(player.hand.tiles) == 14
    last_tile = player.hand.tiles[-1]
    tsumogiri_turn(engine, dealer)
    assert engine.state.current_player == (dealer + 1) % 4
    assert player.river[-1] == last_tile
    assert len(player.hand.tiles) == 13


def test_tsumogiri_turn_draws_when_needed() -> None:
    engine = MahjongEngine()
    player_index = (engine.state.dealer + 1) % 4
    player = engine.state.players[player_index]
    assert len(player.hand.tiles) == 13
    tsumogiri_turn(engine, player_index)
    assert len(player.hand.tiles) == 13
    assert len(player.river) == 1
