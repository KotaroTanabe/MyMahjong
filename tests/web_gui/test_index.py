from pathlib import Path


def test_index_html_exists() -> None:
    index = Path('web_gui/index.html')
    assert index.is_file(), 'index.html missing'
    text = index.read_text()
    assert 'MyMahjong GUI' in text
    assert '<div id="app"></div>' in text
    assert 'main.jsx' in text
    assert 'style.css' in text


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


def test_game_board_references_controls() -> None:
    board = Path('web_gui/GameBoard.jsx').read_text()
    assert 'Controls' in board


def test_style_css_exists() -> None:
    css = Path('web_gui/style.css')
    assert css.is_file(), 'style.css missing'


def test_app_has_server_selection() -> None:
    text = Path('web_gui/App.jsx').read_text()
    assert '<input' in text
    assert 'Retry' in text


def test_app_can_start_game() -> None:
    text = Path('web_gui/App.jsx').read_text()
    assert 'Start Game' in text
    assert '/games' in text


def test_app_opens_websocket() -> None:
    text = Path('web_gui/App.jsx').read_text()
    assert '/ws/1' in text


def test_controls_use_server_prop() -> None:
    text = Path('web_gui/Controls.jsx').read_text()
    assert 'server' in text
    assert '/games/1/action' in text


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


def test_south_hand_displays_emojis() -> None:
    board = Path('web_gui/GameBoard.jsx').read_text()
    assert 'south?.hand?.tiles.map(tileLabel)' in board


def test_app_updates_wall_on_draw() -> None:
    text = Path('web_gui/eventHandlers.js').read_text()
    assert 'wall.tiles.pop()' in text


def test_style_defines_tile_font_size() -> None:
    css = Path('web_gui/style.css').read_text()
    assert '--tile-font-size' in css
