import pytest
from core.mahjong_engine import MahjongEngine
from core.models import Tile


def test_open_kan_events_order() -> None:
    engine = MahjongEngine()
    engine.pop_events()
    discarder = engine.state.players[1]
    caller = engine.state.players[0]
    tile = Tile('man', 1)
    discarder.hand.tiles.append(tile)
    engine.state.current_player = 1
    engine.discard_tile(1, tile)
    engine.pop_events()
    caller.hand.tiles.extend([Tile('man', 1) for _ in range(3)])
    engine.call_kan(0, [Tile('man', 1)] * 4)
    events = engine.pop_events()
    names = [e.name for e in events]
    assert names == ['claims_closed', 'draw_tile', 'meld']
    meld = events[-1].payload['meld']
    assert meld.type == 'kan'
    assert len(meld.tiles) == 4
    assert events[-1].payload['player_index'] == 0


def test_closed_kan_event() -> None:
    engine = MahjongEngine()
    engine.pop_events()
    engine.state.players[0].hand.tiles = [Tile('sou', 5)] * 4
    engine.call_kan(0, [Tile('sou', 5)] * 4)
    events = engine.pop_events()
    assert [e.name for e in events] == ['draw_tile', 'meld']
    meld = events[1].payload['meld']
    assert meld.type == 'closed_kan'
    assert len(meld.tiles) == 4


def test_added_kan_event() -> None:
    engine = MahjongEngine()
    engine.pop_events()
    discarder = engine.state.players[1]
    caller = engine.state.players[0]
    tile = Tile('pin', 2)
    discarder.hand.tiles.append(tile)
    engine.state.current_player = 1
    engine.discard_tile(1, tile)
    caller.hand.tiles.extend([Tile('pin', 2), Tile('pin', 2)])
    engine.call_pon(0, [Tile('pin', 2), Tile('pin', 2), tile])
    engine.pop_events()
    caller.hand.tiles.append(Tile('pin', 2))
    engine.call_kan(0, [Tile('pin', 2)] * 4)
    events = engine.pop_events()
    assert [e.name for e in events] == ['draw_tile', 'meld']
    meld = events[1].payload['meld']
    assert meld.type == 'added_kan'
    assert len(meld.tiles) == 4
