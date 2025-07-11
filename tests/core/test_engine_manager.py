from core.engine_manager import EngineManager


def test_create_game_returns_id_and_state() -> None:
    mgr = EngineManager()
    game_id, state = mgr.create_game(["A", "B", "C", "D"])
    assert game_id == 1
    assert len(state.players) == 4
    next_id, _ = mgr.create_game(["E", "F", "G", "H"])
    assert next_id == 2


def test_record_next_actions_deduplicates() -> None:
    mgr = EngineManager()
    gid, _ = mgr.create_game(["A", "B", "C", "D"])
    mgr.record_next_actions(gid, 0, ["draw"])
    engine = mgr.get_engine(gid)
    assert any(e.name == "next_actions" for e in engine.events)
    mgr.record_next_actions(gid, 0, ["draw"])
    assert sum(1 for e in engine.event_history if e.name == "next_actions") == 1
