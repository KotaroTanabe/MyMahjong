from core.mahjong_engine import MahjongEngine
from core.simple_ai import shanten_turn, claim_meld
from core.models import Tile
import random


def test_shanten_turn_discards_best_tile(monkeypatch) -> None:
    engine = MahjongEngine()
    dealer = engine.state.dealer
    player = engine.state.players[dealer]
    player.hand.tiles = [
        Tile("man", 1), Tile("man", 2), Tile("man", 3),
        Tile("man", 4), Tile("man", 5), Tile("man", 6),
        Tile("man", 7), Tile("man", 8), Tile("man", 9),
        Tile("pin", 1), Tile("pin", 2), Tile("pin", 3),
        Tile("sou", 7), Tile("sou", 9),
    ]
    monkeypatch.setattr(random, "choice", lambda seq: seq[0])
    discarded = shanten_turn(engine, dealer)
    assert discarded.suit == "sou" and discarded.value == 7
    assert len(player.hand.tiles) == 13
    assert player.river[-1] == discarded


def test_shanten_turn_handles_tsumogiri(monkeypatch) -> None:
    engine = MahjongEngine()
    dealer = engine.state.dealer
    player = engine.state.players[dealer]
    player.hand.tiles = [Tile("man", 1)] * 14
    player.must_tsumogiri = True
    discarded = shanten_turn(engine, dealer)
    assert discarded == player.river[-1]
    assert not player.must_tsumogiri


def test_claim_meld_improves_shanten() -> None:
    engine = MahjongEngine()
    discarder = engine.state.players[0]
    caller = engine.state.players[1]
    tile = Tile("man", 1)
    discarder.hand.tiles = [tile]
    caller.hand.tiles = [
        Tile("man", 1), Tile("man", 1), Tile("man", 2), Tile("man", 3),
        Tile("man", 3), Tile("man", 4), Tile("man", 5), Tile("man", 5),
        Tile("man", 6), Tile("man", 7), Tile("man", 7), Tile("pin", 9), Tile("pin", 9),
    ]
    engine.discard_tile(0, tile)
    called = claim_meld(engine, 1)
    assert called
    assert len(caller.hand.melds) == 1
    assert caller.hand.melds[0].type == "pon"
    assert engine.state.current_player == 1
