from core.mahjong_engine import MahjongEngine
from core.models import Tile
from core.rules import RuleSet
from mahjong.hand_calculating.hand_response import HandResponse


def test_engine_initialization() -> None:
    engine = MahjongEngine()
    assert len(engine.state.players) == 4
    assert engine.state.wall is not None
    assert engine.state.seat_winds == ["east", "south", "west", "north"]


def test_initial_hands_dealt() -> None:
    engine = MahjongEngine()
    dealer = engine.state.dealer
    counts = [len(p.hand.tiles) for p in engine.state.players]
    assert counts[dealer] == 14
    assert all(counts[i] == 13 for i in range(4) if i != dealer)
    assert engine.remaining_tiles == 136 - (14 + 13 * 3)


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
    assert all(t is not tile for t in engine.state.players[1].hand.tiles)
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


def test_remaining_tiles_property() -> None:
    engine = MahjongEngine()
    remaining = engine.remaining_tiles
    engine.draw_tile(0)
    assert engine.remaining_tiles == remaining - 1


def test_remaining_yama_tiles_property() -> None:
    engine = MahjongEngine()
    yama_remaining = engine.remaining_yama_tiles
    engine.draw_tile(0)
    assert engine.remaining_yama_tiles == yama_remaining - 1


def test_declare_riichi() -> None:
    engine = MahjongEngine()
    player = engine.state.players[0]
    start_score = player.score
    engine.declare_riichi(0)
    assert player.riichi
    assert player.score == start_score - 1000


class DummyRuleSet(RuleSet):
    def calculate_score(self, hand_tiles, melds, win_tile, *, is_tsumo=True):
        return HandResponse(han=1)


def test_event_log() -> None:
    engine = MahjongEngine(ruleset=DummyRuleSet())
    engine.pop_events()  # clear start_game
    tile = Tile("man", 1)
    engine.state.wall.tiles.append(tile)
    drawn = engine.draw_tile(0)
    engine.discard_tile(0, drawn)
    engine.declare_riichi(0)
    engine.declare_tsumo(0, drawn)
    engine.end_game()
    names = [e.name for e in engine.pop_events()]
    assert names == [
        "draw_tile",
        "discard",
        "riichi",
        "tsumo",
        "end_game",
    ]


def test_skip_advances_turn_and_emits_event() -> None:
    engine = MahjongEngine()
    assert engine.state.current_player == 0
    engine.pop_events()  # clear start_game
    engine.skip(0)
    assert engine.state.current_player == 1
    events = engine.pop_events()
    assert events and events[0].name == "skip"


def test_skip_ignored_if_not_players_turn() -> None:
    engine = MahjongEngine()
    engine.pop_events()
    engine.skip(1)
    assert engine.state.current_player == 0
    assert not engine.pop_events()


def test_start_kyoku_resets_state_and_emits_event() -> None:
    engine = MahjongEngine()
    engine.pop_events()  # clear start_game and start_kyoku
    engine.start_kyoku(dealer=1, round_number=2)
    assert engine.state.dealer == 1
    assert engine.state.round_number == 2
    events = engine.pop_events()
    assert events and events[0].name == "start_kyoku"


def test_start_kyoku_assigns_seat_winds() -> None:
    engine = MahjongEngine()
    engine.pop_events()
    engine.start_kyoku(dealer=1, round_number=1)
    winds = [p.seat_wind for p in engine.state.players]
    assert winds == ["north", "east", "south", "west"]


def test_ryukyoku_event_on_wall_empty() -> None:
    engine = MahjongEngine()
    engine.pop_events()  # clear initial events
    assert engine.state.wall is not None
    engine.state.wall.tiles = [Tile("man", 1)]
    engine.draw_tile(0)
    events = engine.pop_events()
    names = [e.name for e in events]
    assert "ryukyoku" in names
