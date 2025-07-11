from core import api, models


def test_record_next_actions() -> None:
    game_id, state = api.manager.create_game(["A", "B", "C", "D"])
    api.manager.record_next_actions(game_id, 0, ["draw", "discard"])
    engine = api.manager.get_engine(game_id)
    assert engine.event_history[-1].name == "next_actions"
    payload = engine.event_history[-1].payload
    assert payload["player_index"] == 0
    assert payload["actions"] == ["draw", "discard"]

