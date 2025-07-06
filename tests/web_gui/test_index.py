from pathlib import Path


def test_index_html_exists() -> None:
    index = Path('web_gui/index.html')
    assert index.is_file(), 'index.html missing'
    text = index.read_text()
    assert 'MyMahjong GUI' in text
    assert '<div id="app"></div>' in text
    assert 'main.jsx' in text
    assert 'style.css' in text
    assert 'bulma.min.css' in text


def test_main_js_exists() -> None:
    script = Path('web_gui/main.jsx')
    assert script.is_file(), 'main.jsx missing'


def test_app_jsx_exists() -> None:
    app = Path('web_gui/App.jsx')
    assert app.is_file(), 'App.jsx missing'


def test_game_board_exists() -> None:
    board = Path('web_gui/GameBoard.jsx')
    assert board.is_file(), 'GameBoard.jsx missing'


def test_hand_component_exists() -> None:
    hand = Path('web_gui/Hand.jsx')
    assert hand.is_file(), 'Hand.jsx missing'


def test_river_component_exists() -> None:
    river = Path('web_gui/River.jsx')
    assert river.is_file(), 'River.jsx missing'


def test_meld_area_component_exists() -> None:
    meld = Path('web_gui/MeldArea.jsx')
    assert meld.is_file(), 'MeldArea.jsx missing'


def test_center_display_component_exists() -> None:
    center = Path('web_gui/CenterDisplay.jsx')
    assert center.is_file(), 'CenterDisplay.jsx missing'


def test_controls_component_exists() -> None:
    controls = Path('web_gui/Controls.jsx')
    assert controls.is_file(), 'Controls.jsx missing'


def test_game_board_references_center_display() -> None:
    board = Path('web_gui/GameBoard.jsx').read_text()
    assert 'CenterDisplay' in board


def test_game_board_uses_player_panel() -> None:
    board = Path('web_gui/GameBoard.jsx').read_text()
    assert 'PlayerPanel' in board


def test_player_panel_component_exists() -> None:
    panel = Path('web_gui/PlayerPanel.jsx')
    assert panel.is_file(), 'PlayerPanel.jsx missing'


def test_style_css_exists() -> None:
    css = Path('web_gui/style.css')
    assert css.is_file(), 'style.css missing'


def test_app_has_server_selection() -> None:
    text = Path('web_gui/App.jsx').read_text()
    assert '<input' in text
    assert 'aria-label="Retry"' in text


def test_app_can_start_game() -> None:
    text = Path('web_gui/App.jsx').read_text()
    assert 'Start Game' in text
    assert '/games' in text


def test_app_has_game_id_input() -> None:
    text = Path('web_gui/App.jsx').read_text()
    assert 'Game ID:' in text
    assert 'Join Game' in text
    assert 'localStorage' in text


def test_app_opens_websocket() -> None:
    text = Path('web_gui/App.jsx').read_text()
    assert '/ws/${' in text


def test_controls_use_server_prop() -> None:
    text = Path('web_gui/Controls.jsx').read_text()
    assert 'server' in text
    assert '/games/${' in text


def test_hand_supports_discard() -> None:
    text = Path('web_gui/Hand.jsx').read_text()
    assert 'onDiscard' in text


def test_hand_uses_tile_to_emoji() -> None:
    text = Path('web_gui/Hand.jsx').read_text()
    assert 'tileToEmoji' in text


def test_app_handles_websocket_events() -> None:
    text = Path('web_gui/App.jsx').read_text()
    assert 'handleMessage' in text
    assert 'event-log' in text


def test_game_board_displays_melds_and_remaining() -> None:
    text = Path('web_gui/GameBoard.jsx').read_text()
    assert 'northMelds' in text
    assert 'remaining={remaining}' in text


def test_game_board_passes_remaining_prop() -> None:
    board = Path('web_gui/GameBoard.jsx').read_text()
    assert 'remaining={' in board


def test_south_hand_displays_images() -> None:
    board = Path('web_gui/GameBoard.jsx').read_text()
    assert 'south?.hand?.tiles.map(tileLabel)' in board


def test_app_updates_wall_on_draw() -> None:
    app = Path('web_gui/App.jsx').read_text()
    assert 'applyEvent' in app
    logic = Path('web_gui/applyEvent.js').read_text()
    assert 'wall.tiles.pop()' in logic


def test_controls_include_extra_actions() -> None:
    text = Path('web_gui/Controls.jsx').read_text()
    for action in ['chi', 'pon', 'kan', 'riichi', 'tsumo', 'ron', 'skip']:
        assert action in text


def test_app_handles_new_events() -> None:
    text = Path('web_gui/applyEvent.js').read_text()
    for evt in ['meld', 'riichi', 'tsumo', 'ron', 'skip']:
        assert evt in text


def test_controls_include_riichi() -> None:
    text = Path('web_gui/Controls.jsx').read_text()
    assert 'Riichi' in text


def test_style_defines_tile_font_size() -> None:
    css = Path('web_gui/style.css').read_text()
    assert '--tile-font-size' in css


def test_practice_component_exists() -> None:
    practice = Path('web_gui/Practice.jsx')
    assert practice.is_file(), 'Practice.jsx missing'


def test_app_has_mode_select() -> None:
    text = Path('web_gui/App.jsx').read_text()
    assert 'Mode:' in text
    assert 'Practice' in text


def test_app_uses_local_storage_for_server() -> None:
    text = Path('web_gui/App.jsx').read_text()
    assert "localStorage.getItem('serverUrl')" in text
    assert "localStorage.setItem('serverUrl'" in text
    assert "localStorage.setItem('gameId'" in text
