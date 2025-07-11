from fastapi.testclient import TestClient
import logging
import pytest

from web.server import app
from core.actions import DRAW, DISCARD, CHI, PON, KAN, RIICHI, TSUMO, RON, SKIP, AUTO
from core import api, models
from core import exceptions as core_exceptions

client = TestClient(app)


def test_get_game_returns_404_when_not_started() -> None:
    api._engine = None  # type: ignore[assignment]
    response = client.get("/games/1")
    assert response.status_code == 404


def test_websocket_connect_without_game() -> None:
    api._engine = None  # type: ignore[assignment]
    with client.websocket_connect("/ws/1"):
        pass


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_and_get_game() -> None:
    create = client.post("/games", json={"players": ["A", "B", "C", "D"]})
    assert create.status_code == 200
    data = create.json()
    assert len(data["players"]) == 4
    assert data["id"] == 1

    response = client.get("/games/1")
    assert response.status_code == 200
    data = response.json()
    assert "players" in data


def test_get_log_endpoint() -> None:
    client.post("/games", json={"players": ["A", "B", "C", "D"]})
    resp = client.get("/games/1/log")
    assert resp.status_code == 200
    data = resp.json()
    assert "log" in data and data["log"].startswith("{")


def test_get_mjai_log_endpoint() -> None:
    client.post("/games", json={"players": ["A", "B", "C", "D"]})
    resp = client.get("/games/1/mjai-log")
    assert resp.status_code == 200
    data = resp.json()
    assert "log" in data and data["log"].startswith("{")


def test_get_events_endpoint() -> None:
    client.post("/games", json={"players": ["A", "B", "C", "D"]})
    resp = client.get("/games/1/events")
    assert resp.status_code == 200
    data = resp.json()
    assert "events" in data and isinstance(data["events"], list)


def test_draw_action_endpoint() -> None:
    client.post("/games", json={"players": ["A", "B", "C", "D"]})
    from core import api
    assert api._engine is not None
    api._engine.state.players[0].hand.tiles.pop()
    resp = client.post(
        "/games/1/action",
        json={"player_index": 0, "action": DRAW},
    )
    assert resp.status_code == 200
    tile = resp.json()
    assert "suit" in tile and "value" in tile


def test_draw_without_discard_returns_409() -> None:
    client.post("/games", json={"players": ["A", "B", "C", "D"]})
    resp = client.post(
        "/games/1/action",
        json={"player_index": 0, "action": DRAW},
    )
    assert resp.status_code == 409
    assert resp.json() == {"detail": "Cannot draw before discarding"}


def test_draw_without_discard_logs_conflict(caplog: pytest.LogCaptureFixture) -> None:
    client.post("/games", json={"players": ["A", "B", "C", "D"]})
    with caplog.at_level(logging.INFO):
        resp = client.post(
            "/games/1/action",
            json={"player_index": 0, "action": DRAW},
        )
    assert resp.status_code == 409
    assert any("409 conflict" in rec.message for rec in caplog.records)


def test_invalid_action_handler(monkeypatch) -> None:
    client.post("/games", json={"players": ["A", "B", "C", "D"]})

    def fail(_idx: int) -> None:
        raise core_exceptions.InvalidActionError("bad")

    monkeypatch.setattr(api, "draw_tile", fail)

    resp = client.post("/games/1/action", json={"player_index": 0, "action": DRAW})
    assert resp.status_code == 409
    assert resp.json() == {"detail": "bad"}


def test_discard_action_endpoint() -> None:
    client.post("/games", json={"players": ["A", "B", "C", "D"]})
    state = api.get_state()
    assert api._engine is not None
    api._engine.state.players[state.current_player].hand.tiles = [
        models.Tile("man", 1)
    ] * 13
    draw = client.post(
        "/games/1/action",
        json={"player_index": state.current_player, "action": DRAW},
    )
    tile = draw.json()
    resp = client.post(
        "/games/1/action",
        json={"player_index": 0, "action": DISCARD, "tile": tile},
    )
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_discard_invalid_tile_returns_409() -> None:
    client.post("/games", json={"players": ["A", "B", "C", "D"]})
    state = api.get_state()
    player = state.players[state.current_player]
    tile = {"suit": "man", "value": 1}
    while models.Tile(**tile) in player.hand.tiles:
        if tile["value"] < 9:
            tile["value"] += 1
        else:
            tile["value"] = 1
            tile["suit"] = "pin" if tile["suit"] == "man" else "sou"
    resp = client.post(
        "/games/1/action",
        json={"player_index": state.current_player, "action": DISCARD, "tile": tile},
    )
    assert resp.status_code == 409


def test_chi_without_discard_returns_409() -> None:
    client.post("/games", json={"players": ["A", "B", "C", "D"]})
    state = api.get_state()
    chi_tile = {"suit": "man", "value": 3}
    state.players[0].hand.tiles = [models.Tile(**chi_tile)]
    state.players[1].hand.tiles = [models.Tile("man", 1), models.Tile("man", 2)]
    client.post(
        "/games/1/action",
        json={"player_index": 0, "action": DISCARD, "tile": chi_tile},
    )
    assert api._engine is not None
    api.get_allowed_actions(1)  # cache chi as allowed
    assert api._engine is not None
    api._engine.state.last_discard = None
    api._engine.state.last_discard_player = None
    resp = client.post(
        "/games/1/action",
        json={
            "player_index": 1,
            "action": CHI,
            "tiles": [
                {"suit": "man", "value": 1},
                {"suit": "man", "value": 2},
            ],
        },
    )
    assert resp.status_code == 409


def test_additional_action_endpoints() -> None:
    client.post("/games", json={"players": ["A", "B", "C", "D"]})
    state = api.get_state()

    # Prepare chi on player 0 discard
    chi_tile = {"suit": "man", "value": 3}
    state.players[0].hand.tiles = [models.Tile(**chi_tile)]
    state.players[1].hand.tiles = []
    client.post(
        "/games/1/action",
        json={"player_index": 0, "action": DISCARD, "tile": chi_tile},
    )
    state.players[1].hand.tiles = [models.Tile("man", 1), models.Tile("man", 2)]
    resp = client.post(
        "/games/1/action",
        json={
            "player_index": 1,
            "action": CHI,
            "tiles": [
                {"suit": "man", "value": 1},
                {"suit": "man", "value": 2},
                chi_tile,
            ],
        },
    )
    assert resp.status_code == 200

    # Prepare pon on new discard
    pon_tile = {"suit": "pin", "value": 1}
    state.players[1].hand.tiles = [models.Tile(**pon_tile)]
    state.players[0].hand.tiles = []
    client.post(
        "/games/1/action",
        json={"player_index": 1, "action": DISCARD, "tile": pon_tile},
    )
    state.players[0].hand.tiles = [models.Tile("pin", 1), models.Tile("pin", 1)]
    resp = client.post(
        "/games/1/action",
        json={
            "player_index": 0,
            "action": PON,
            "tiles": [
                pon_tile,
                {"suit": "pin", "value": 1},
                {"suit": "pin", "value": 1},
            ],
        },
    )
    assert resp.status_code == 200

    # Prepare kan on another discard
    kan_tile = {"suit": "sou", "value": 9}
    state.players[0].hand.tiles = [models.Tile(**kan_tile)]
    state.players[1].hand.tiles = []
    client.post(
        "/games/1/action",
        json={"player_index": 0, "action": DISCARD, "tile": kan_tile},
    )
    state.players[1].hand.tiles = [models.Tile("sou", 9) for _ in range(3)]
    resp = client.post(
        "/games/1/action",
        json={
            "player_index": 1,
            "action": KAN,
            "tiles": [
                kan_tile,
                {"suit": "sou", "value": 9},
                {"suit": "sou", "value": 9},
                {"suit": "sou", "value": 9},
            ],
        },
    )
    assert resp.status_code == 200

    resp = client.post(
        "/games/1/action",
        json={"player_index": 0, "action": RIICHI, "tile": {"suit": "man", "value": 1}},
    )
    assert resp.status_code == 409

    state = api.get_state()
    assert api._engine is not None
    api._engine.state.players[state.current_player].hand.tiles = [
        models.Tile("man", 1)
    ]
    draw = client.post(
        "/games/1/action",
        json={"player_index": state.current_player, "action": DRAW},
    )
    tile = draw.json()

    resp = client.post(
        "/games/1/action",
        json={"player_index": state.current_player, "action": TSUMO, "tile": tile},
    )
    assert resp.status_code == 200

    resp = client.post(
        "/games/1/action",
        json={"player_index": state.current_player, "action": SKIP},
    )
    assert resp.status_code == 409


def test_draw_from_empty_wall_returns_error() -> None:
    client.post("/games", json={"players": ["A", "B", "C", "D"]})
    from core import api
    assert api._engine is not None
    api._engine.state.wall.tiles = []  # type: ignore[list]
    api._engine.state.players[0].hand.tiles.pop()
    resp = client.post(
        "/games/1/action",
        json={"player_index": 0, "action": DRAW},
    )
    assert resp.status_code == 409
    assert resp.json() == {"detail": "Wall is empty"}


def test_websocket_streams_events() -> None:
    client.post("/games", json={"players": ["A", "B", "C", "D"]})
    with client.websocket_connect("/ws/1") as ws:
        data = ws.receive_json()
        assert data["name"] == "allowed_actions"
        data = ws.receive_json()
        assert data["name"] == "start_game"
        data = ws.receive_json()
        assert data["name"] == "start_kyoku"
        from core import api
        assert api._engine is not None
        api._engine.state.players[0].hand.tiles.pop()
        client.post(
            "/games/1/action",
            json={"player_index": 0, "action": DRAW},
        )
        data = ws.receive_json()
        assert data["name"] == "draw_tile"


def test_practice_endpoints() -> None:
    prob = client.get("/practice")
    assert prob.status_code == 200
    data = prob.json()
    assert "hand" in data and "dora_indicator" in data

    resp = client.post("/practice/suggest", json={"hand": data["hand"]})
    assert resp.status_code == 200
    tile = resp.json()
    assert "suit" in tile and "value" in tile


def test_practice_endpoints_external(monkeypatch) -> None:
    def fake_suggest(hand: list[models.Tile], use_ai: bool = False) -> models.Tile:
        assert use_ai
        return hand[0]

    monkeypatch.setattr(api, "suggest_practice_discard", fake_suggest)

    prob = client.get("/practice")
    data = prob.json()
    resp = client.post("/practice/suggest?ai=true", json={"hand": data["hand"]})
    assert resp.status_code == 200


def test_shanten_quiz_endpoints() -> None:
    hand_resp = client.get("/shanten-quiz")
    assert hand_resp.status_code == 200
    hand = hand_resp.json()
    assert isinstance(hand, list)

    check = client.post("/shanten-quiz/check", json={"hand": hand})
    assert check.status_code == 200
    data = check.json()
    assert "shanten" in data


def test_auto_action_endpoint() -> None:
    client.post("/games", json={"players": ["A", "B", "C", "D"]})
    resp = client.post(
        "/games/1/action",
        json={"player_index": 0, "action": AUTO, "ai_type": "simple"},
    )
    assert resp.status_code == 200
    tile = resp.json()
    assert "suit" in tile and "value" in tile


def test_auto_action_wrong_turn_returns_409() -> None:
    client.post("/games", json={"players": ["A", "B", "C", "D"]})
    state = api.get_state()
    wrong = (state.current_player + 1) % 4
    resp = client.post(
        "/games/1/action",
        json={"player_index": wrong, "action": AUTO, "ai_type": "simple"},
    )
    assert resp.status_code == 409


def test_auto_action_claim_phase_checks_player() -> None:
    client.post("/games", json={"players": ["A", "B", "C", "D"]})
    state = api.get_state()
    start = state.current_player
    tile = state.players[start].hand.tiles[0]
    client.post(
        "/games/1/action",
        json={"player_index": start, "action": DISCARD, "tile": tile.__dict__},
    )
    resp = client.post(
        "/games/1/action",
        json={"player_index": start, "action": AUTO},
    )
    assert resp.status_code == 409


def test_shanten_endpoint() -> None:
    client.post("/games", json={"players": ["A", "B", "C", "D"]})
    resp = client.get("/games/1/shanten/0")
    assert resp.status_code == 200
    data = resp.json()
    assert "shanten" in data and isinstance(data["shanten"], int)


def test_allowed_actions_endpoint() -> None:
    client.post("/games", json={"players": ["A", "B", "C", "D"]})
    state = api.get_state()
    for p in state.players:
        p.hand.tiles = []
    tile = {"suit": "man", "value": 2}
    state.players[0].hand.tiles = [models.Tile(**tile)]
    client.post(
        "/games/1/action",
        json={"player_index": 0, "action": DISCARD, "tile": tile},
    )
    state.players[1].hand.tiles = [models.Tile("man", 1), models.Tile("man", 3)]
    resp = client.get("/games/1/allowed-actions/1")
    assert resp.status_code == 200
    actions = resp.json().get("actions")
    assert CHI in actions and SKIP in actions


def test_all_allowed_actions_endpoint() -> None:
    client.post("/games", json={"players": ["A", "B", "C", "D"]})
    state = api.get_state()
    for p in state.players:
        p.hand.tiles = []
    tile = {"suit": "man", "value": 2}
    state.players[0].hand.tiles = [models.Tile(**tile)]
    client.post(
        "/games/1/action",
        json={"player_index": 0, "action": DISCARD, "tile": tile},
    )
    state.players[1].hand.tiles = [models.Tile("man", 1), models.Tile("man", 3)]
    resp = client.get("/games/1/allowed-actions")
    assert resp.status_code == 200
    actions = resp.json().get("actions")
    assert isinstance(actions, list) and CHI in actions[1]


def test_unknown_action_returns_400() -> None:
    client.post("/games", json={"players": ["A", "B", "C", "D"]})
    resp = client.post(
        "/games/1/action",
        json={"player_index": 0, "action": "unknown"},
    )
    assert resp.status_code == 400


def test_next_actions_endpoint_autodraw() -> None:
    client.post("/games", json={"players": ["A", "B", "C", "D"]})
    state = api.get_state()
    state.current_player = 1
    state.players[1].hand.tiles = [models.Tile("man", i + 1) for i in range(9)] + [
        models.Tile("pin", i + 1) for i in range(4)
    ]
    state.players[1].riichi = True
    state.wall.tiles = [models.Tile("sou", 9)]
    resp = client.get("/games/1/next-actions")
    assert resp.status_code == 200
    data = resp.json()
    assert "player_index" in data and "actions" in data

def test_next_actions_endpoint_logs_event() -> None:
    client.post("/games", json={"players": ["A", "B", "C", "D"]})
    api.pop_events()  # clear initial events
    resp = client.get("/games/1/next-actions")
    assert resp.status_code == 200
    events = api.pop_events()
    assert any(e.name == "next_actions" for e in events)


def test_next_actions_endpoint_deduplicates_events() -> None:
    client.post("/games", json={"players": ["A", "B", "C", "D"]})
    api.pop_events()
    resp1 = client.get("/games/1/next-actions")
    assert resp1.status_code == 200
    events = api.pop_events()
    assert sum(1 for e in events if e.name == "next_actions") == 1
    resp2 = client.get("/games/1/next-actions")
    assert resp2.status_code == 200
    events = api.pop_events()
    assert not any(e.name == "next_actions" for e in events)


def test_action_rejected_when_not_allowed(caplog: pytest.LogCaptureFixture) -> None:
    client.post("/games", json={"players": ["A", "B", "C", "D"]})
    with caplog.at_level(logging.INFO):
        resp = client.post(
            "/games/1/action",
            json={
                "player_index": 1,
                "action": CHI,
                "tiles": [
                    {"suit": "man", "value": 1},
                    {"suit": "man", "value": 2},
                    {"suit": "man", "value": 3},
                ],
            },
        )
    assert resp.status_code == 409
    detail = resp.json()["detail"]
    assert detail.startswith("Action not allowed:")
    assert "player 1" in detail and CHI in detail
    assert any("disallowed action" in rec.message for rec in caplog.records)


def test_action_succeeds_when_allowed() -> None:
    client.post("/games", json={"players": ["A", "B", "C", "D"]})
    state = api.get_state()
    for p in state.players:
        p.hand.tiles = []
    tile = {"suit": "man", "value": 2}
    state.players[0].hand.tiles = [models.Tile(**tile)]
    client.post(
        "/games/1/action",
        json={"player_index": 0, "action": DISCARD, "tile": tile},
    )
    state.players[1].hand.tiles = [models.Tile("man", 1), models.Tile("man", 3)]
    resp = client.post(
        "/games/1/action",
        json={
            "player_index": 1,
            "action": CHI,
            "tiles": [
                {"suit": "man", "value": 1},
                {"suit": "man", "value": 2},
                {"suit": "man", "value": 3},
            ],
        },
    )
    assert resp.status_code == 200


def test_discard_wrong_player_returns_409() -> None:
    client.post("/games", json={"players": ["A", "B", "C", "D"]})
    state = api.get_state()
    tile = state.players[1].hand.tiles[0]
    resp = client.post(
        "/games/1/action",
        json={"player_index": 1, "action": DISCARD, "tile": tile.__dict__},
    )
    assert resp.status_code == 409


def test_chi_wrong_player_returns_409() -> None:
    client.post("/games", json={"players": ["A", "B", "C", "D"]})
    state = api.get_state()
    disc_tile = state.players[0].hand.tiles[0]
    client.post(
        "/games/1/action",
        json={"player_index": 0, "action": DISCARD, "tile": disc_tile.__dict__},
    )
    resp = client.post(
        "/games/1/action",
        json={
            "player_index": 2,
            "action": CHI,
            "tiles": [
                disc_tile.__dict__,
                disc_tile.__dict__,
                disc_tile.__dict__,
            ],
        },
    )
    assert resp.status_code == 409


def test_pon_invalid_tiles_returns_409() -> None:
    client.post("/games", json={"players": ["A", "B", "C", "D"]})
    state = api.get_state()
    disc_tile = state.players[0].hand.tiles[0]
    client.post(
        "/games/1/action",
        json={"player_index": 0, "action": DISCARD, "tile": disc_tile.__dict__},
    )
    resp = client.post(
        "/games/1/action",
        json={
            "player_index": 1,
            "action": PON,
            "tiles": [
                disc_tile.__dict__,
                disc_tile.__dict__,
                {"suit": disc_tile.suit, "value": (disc_tile.value % 9) + 1},
            ],
        },
    )
    assert resp.status_code == 409


def test_kan_invalid_tiles_returns_409() -> None:
    client.post("/games", json={"players": ["A", "B", "C", "D"]})
    state = api.get_state()
    disc_tile = state.players[0].hand.tiles[0]
    client.post(
        "/games/1/action",
        json={"player_index": 0, "action": DISCARD, "tile": disc_tile.__dict__},
    )
    resp = client.post(
        "/games/1/action",
        json={
            "player_index": 1,
            "action": KAN,
            "tiles": [
                disc_tile.__dict__,
                disc_tile.__dict__,
                disc_tile.__dict__,
            ],
        },
    )
    assert resp.status_code == 409


def test_riichi_action_discards_and_flags_player() -> None:
    client.post("/games", json={"players": ["A", "B", "C", "D"]})
    state = api.get_state()
    tiles = [
        models.Tile("man", 1), models.Tile("man", 1),
        models.Tile("man", 2), models.Tile("man", 2),
        models.Tile("man", 3), models.Tile("man", 3),
        models.Tile("pin", 4), models.Tile("pin", 4),
        models.Tile("pin", 5), models.Tile("pin", 5),
        models.Tile("sou", 6), models.Tile("sou", 6),
        models.Tile("sou", 7), models.Tile("sou", 8),
    ]
    player = state.players[state.current_player]
    player.hand.tiles = tiles.copy()
    tile = player.hand.tiles[-1]
    resp = client.post(
        "/games/1/action",
        json={"player_index": state.current_player, "action": RIICHI, "tile": tile.__dict__},
    )
    assert resp.status_code == 200
    assert player.riichi
    assert tile in player.river
def test_start_kyoku_endpoint_and_ws() -> None:
    client.post("/games", json={"players": ["A", "B", "C", "D"]})
    with client.websocket_connect("/ws/1") as ws:
        ws.receive_json()  # allowed_actions
        ws.receive_json()  # start_game
        ws.receive_json()  # start_kyoku for first hand

        resp = client.post(
            "/games/1/start-kyoku",
            json={"dealer": 1, "round": 2},
        )
        assert resp.status_code == 200
        state = api.get_state()
        assert state.dealer == 1
        assert state.round_number == 2
        data = ws.receive_json()
        assert data["name"] == "start_kyoku"
        assert data["payload"]["dealer"] == 1
        assert data["payload"]["round"] == 2

