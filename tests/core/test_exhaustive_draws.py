from core.mahjong_engine import MahjongEngine
from core.models import Tile


def test_four_kans_causes_ryukyoku() -> None:
    engine = MahjongEngine()
    engine.pop_events()
    player = engine.state.players[0]
    for v in range(1, 5):
        tiles = [Tile("man", v) for _ in range(4)]
        player.hand.tiles = tiles.copy()
        engine.call_kan(0, tiles)
    events = engine.pop_events()
    assert any(e.name == "ryukyoku" and e.payload.get("reason") == "four_kans" for e in events)


def test_four_riichi_causes_ryukyoku() -> None:
    engine = MahjongEngine()
    engine.pop_events()
    for i in range(4):
        engine.declare_riichi(i)
    events = engine.pop_events()
    assert any(e.name == "ryukyoku" and e.payload.get("reason") == "four_riichi" for e in events)


def test_nine_terminals_causes_ryukyoku(monkeypatch) -> None:
    engine = MahjongEngine()
    engine.pop_events()
    orig = engine.deal_initial_hands

    def rigged_deal() -> None:
        monkeypatch.setattr(engine, "deal_initial_hands", orig)
        nt_tiles = [
            Tile("man", 1), Tile("man", 9), Tile("pin", 1), Tile("pin", 9),
            Tile("sou", 1), Tile("sou", 9),
            Tile("wind", 1), Tile("wind", 2), Tile("wind", 3), Tile("wind", 4),
            Tile("dragon", 1), Tile("dragon", 2), Tile("dragon", 3), Tile("man", 1),
        ]
        engine.state.players[0].hand.tiles = nt_tiles[:14]
        for p in engine.state.players[1:]:
            p.hand.tiles = [Tile("man", 2) for _ in range(13)]

    monkeypatch.setattr(engine, "deal_initial_hands", rigged_deal)
    engine.start_kyoku(engine.state.dealer, engine.state.round_number)
    events = engine.pop_events()
    assert any(e.name == "ryukyoku" and e.payload.get("reason") == "nine_terminals" for e in events)
