from core.actions import PON
import pytest
from core.mahjong_engine import MahjongEngine
from core.exceptions import InvalidActionError
from core.models import Tile
from core.rules import RuleSet
from mahjong.hand_calculating.hand_response import HandResponse


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
    # Only 122 tiles are available for play after reserving the dead wall
    assert engine.remaining_tiles == 122 - (14 + 13 * 3)


def test_draw_tile_updates_state() -> None:
    engine = MahjongEngine()
    assert engine.state.wall is not None
    tile = Tile(suit="pin", value=3)
    engine.state.wall.tiles.append(tile)
    engine.state.players[0].hand.tiles.pop()
    engine.draw_tile(0)
    assert tile in engine.state.players[0].hand.tiles


def test_discard_tile_updates_state() -> None:
    engine = MahjongEngine()
    tile = Tile(suit="pin", value=4)
    # Add tile to player's hand directly for simplicity
    engine.state.players[1].draw(tile)
    engine.state.current_player = 1
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
    tile = Tile("man", 1)
    discarder = engine.state.players[0]
    caller = engine.state.players[1]
    discarder.hand.tiles.append(tile)
    engine.discard_tile(0, tile)
    caller.hand.tiles.extend([Tile("man", 1), Tile("man", 1)])
    engine.call_pon(1, [Tile("man", 1), Tile("man", 1), tile])
    assert len(caller.hand.melds) == 1
    assert caller.hand.melds[0].type == PON
    assert tile not in discarder.river


def test_end_game_resets_state() -> None:
    engine = MahjongEngine()
    old_state = engine.state
    finished = engine.end_game()
    assert finished is old_state
    assert engine.state is not old_state
    assert engine.state.honba == 0
    assert engine.state.riichi_sticks == 0


def test_end_game_ignored_on_subsequent_calls() -> None:
    engine = MahjongEngine()
    engine.pop_events()  # clear start_game/start_kyoku
    first = engine.end_game()
    events = engine.pop_events()
    assert events and events[-1].name == "end_game"
    second = engine.end_game()
    events = engine.pop_events()
    assert not any(e.name == "end_game" for e in events)
    assert first is second
    assert engine.is_game_over


def test_remaining_tiles_property() -> None:
    engine = MahjongEngine()
    remaining = engine.remaining_tiles
    engine.state.players[0].hand.tiles.pop()
    engine.draw_tile(0)
    assert engine.remaining_tiles == remaining - 1


def test_remaining_yama_tiles_property() -> None:
    engine = MahjongEngine()
    yama_remaining = engine.remaining_yama_tiles
    engine.state.players[0].hand.tiles.pop()
    engine.draw_tile(0)
    assert engine.remaining_yama_tiles == yama_remaining - 1


def test_declare_riichi() -> None:
    engine = MahjongEngine()
    player = engine.state.players[0]
    _set_tenpai_hand(player)
    start_score = player.score
    engine.declare_riichi(0)
    assert player.riichi
    assert player.score == start_score - 1000
    assert engine.state.riichi_sticks == 1


def test_riichi_event_includes_score_and_sticks() -> None:
    engine = MahjongEngine()
    engine.pop_events()  # clear start_game
    start_score = engine.state.players[0].score
    _set_tenpai_hand(engine.state.players[0])
    engine.declare_riichi(0)
    events = engine.pop_events()
    riichi_evt = next(e for e in events if e.name == "riichi")
    assert riichi_evt.payload["score"] == start_score - 1000
    assert riichi_evt.payload["riichi_sticks"] == 1


def test_discard_requires_tsumogiri_after_riichi() -> None:
    engine = MahjongEngine()
    player = engine.state.players[0]
    _set_tenpai_hand(player)
    tile_to_discard = player.hand.tiles[0]
    engine.declare_riichi(0)
    with pytest.raises(InvalidActionError):
        engine.discard_tile(0, tile_to_discard)


def test_tsumogiri_allowed_after_riichi() -> None:
    engine = MahjongEngine()
    player = engine.state.players[0]
    _set_tenpai_hand(player)
    drawn = player.hand.tiles[-1]
    engine.declare_riichi(0)
    engine.discard_tile(0, drawn)
    assert drawn in player.river
    assert not player.must_tsumogiri


def test_tsumo_updates_scores_and_emits_event() -> None:
    engine = MahjongEngine(ruleset=ScoringRuleSet())
    engine.pop_events()
    tile = Tile("man", 1)
    engine.state.players[0].hand.tiles.append(tile)
    _set_tenpai_hand(engine.state.players[1])
    engine.declare_riichi(1)
    start_score = engine.state.players[0].score
    loser_start = engine.state.players[1].score
    engine.declare_tsumo(0, tile)
    assert engine.state.players[0].score == start_score + 8000 + 1000
    assert engine.state.players[1].score == loser_start - 2666
    assert engine.state.riichi_sticks == 0
    events = engine.pop_events()
    tsumo_evt = next(e for e in events if e.name == "tsumo")
    assert tsumo_evt.payload["scores"][0] == start_score + 8000 + 1000


def test_ron_updates_scores_and_emits_event() -> None:
    engine = MahjongEngine(ruleset=ScoringRuleSet())
    engine.pop_events()
    tile = Tile("man", 2)
    engine.state.players[0].hand.tiles.append(tile)
    _set_tenpai_hand(engine.state.players[2])
    engine.declare_riichi(2)
    engine.state.players[1].hand.tiles.append(Tile("man", 2))
    engine.state.current_player = 1
    engine.discard_tile(1, engine.state.players[1].hand.tiles[-1])
    start_score = engine.state.players[0].score
    loser_start = engine.state.players[1].score
    engine.declare_ron(0, tile)
    assert engine.state.players[0].score == start_score + 8000 + 1000
    assert engine.state.players[1].score == loser_start - 8000
    assert engine.state.riichi_sticks == 0
    events = engine.pop_events()
    ron_evt = next(e for e in events if e.name == "ron")
    assert ron_evt.payload["scores"][0] == start_score + 8000 + 1000


class DummyRuleSet(RuleSet):
    def calculate_score(self, hand_tiles, melds, win_tile, *, is_tsumo=True, **_):
        return HandResponse(han=1)


class ScoringRuleSet(RuleSet):
    def calculate_score(self, hand_tiles, melds, win_tile, *, is_tsumo=True, **_):
        return HandResponse(han=1, cost={"total": 8000})


def test_event_log() -> None:
    engine = MahjongEngine(ruleset=DummyRuleSet())
    engine.pop_events()  # clear start_game
    tile = Tile("man", 1)
    engine.state.wall.tiles.append(tile)
    engine.state.players[0].hand.tiles.pop()
    drawn = engine.draw_tile(0)
    engine.discard_tile(0, drawn)
    _set_tenpai_hand(engine.state.players[0])
    engine.declare_riichi(0)
    engine.declare_tsumo(0, drawn)
    engine.end_game()
    names = [e.name for e in engine.pop_events()]
    assert names == [
        "draw_tile",
        "discard",
        "riichi",
        "tsumo",
        "round_end",
        "start_kyoku",
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
    tile = engine.state.players[0].hand.tiles[0]
    engine.discard_tile(0, tile)
    engine.skip(0)
    assert engine.state.current_player == 1
    events = engine.pop_events()
    assert not any(e.name == "skip" and e.payload["player_index"] == 0 for e in events)


def test_draw_blocked_until_all_skip() -> None:
    engine = MahjongEngine()
    tile = engine.state.players[0].hand.tiles[0]
    engine.discard_tile(0, tile)
    with pytest.raises(InvalidActionError):
        engine.draw_tile(1)
    engine.skip(1)
    engine.skip(2)
    engine.skip(3)
    assert len(engine.state.players[1].hand.tiles) == 14


def test_draw_disallowed_after_chi() -> None:
    engine = MahjongEngine()
    engine.pop_events()
    discarder = 0
    caller = 1
    tile = Tile("man", 3)
    engine.state.players[discarder].hand.tiles.append(tile)
    engine.state.current_player = discarder
    engine.discard_tile(discarder, tile)
    engine.pop_events()
    engine.state.players[caller].hand.tiles = [
        Tile("man", 1),
        Tile("man", 2),
        *([Tile("pin", 1)] * 11),
    ]
    engine.call_chi(caller, [Tile("man", 1), Tile("man", 2), tile])
    with pytest.raises(InvalidActionError):
        engine.draw_tile(caller)


def test_draw_disallowed_after_pon() -> None:
    engine = MahjongEngine()
    engine.pop_events()
    discarder = 0
    caller = 2
    tile = Tile("pin", 5)
    engine.state.players[discarder].hand.tiles.append(tile)
    engine.state.current_player = discarder
    engine.discard_tile(discarder, tile)
    engine.pop_events()
    engine.state.players[caller].hand.tiles = [
        Tile("pin", 5),
        Tile("pin", 5),
        *([Tile("sou", 1)] * 11),
    ]
    engine.call_pon(caller, [Tile("pin", 5), Tile("pin", 5), tile])
    with pytest.raises(InvalidActionError):
        engine.draw_tile(caller)


def test_draw_disallowed_after_kan() -> None:
    engine = MahjongEngine()
    engine.pop_events()
    caller = 0
    tile = Tile("sou", 7)
    engine.state.players[caller].hand.tiles = [tile] * 4 + [Tile("man", 1)] * 9
    engine.draw_tile(caller)
    engine.call_kan(caller, [tile] * 4)
    engine.pop_events()
    with pytest.raises(InvalidActionError):
        engine.draw_tile(caller)


def test_start_kyoku_resets_state_and_emits_event() -> None:
    engine = MahjongEngine()
    engine.pop_events()  # clear start_game and start_kyoku
    engine.start_kyoku(dealer=1, round_number=2)
    assert engine.state.dealer == 1
    assert engine.state.round_number == 2
    assert len(engine.state.dora_indicators) == 1
    assert engine.state.dora_indicators[0] in engine.state.dead_wall
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
    engine.state.players[0].hand.tiles.pop()
    engine.draw_tile(0)
    events = engine.pop_events()
    names = [e.name for e in events]
    assert "ryukyoku" in names


def test_start_kyoku_clears_previous_discard_state() -> None:
    engine = MahjongEngine()
    engine.pop_events()  # clear initial events
    discard = engine.state.players[0].hand.tiles[-1]
    engine.discard_tile(0, discard)
    assert engine.state.waiting_for_claims
    engine.start_kyoku(dealer=1, round_number=2)
    engine.pop_events()  # clear start_kyoku event
    assert engine.state.current_player == 1
    assert engine.state.last_discard is None
    assert engine.state.last_discard_player is None
    assert engine.state.waiting_for_claims == []
