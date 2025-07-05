import os
import subprocess
from pathlib import Path


def run_node(code: str) -> str:
    result = subprocess.run(
        ["node", "-e", code], capture_output=True, text=True, cwd="web_gui"
    )
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


def ensure_node_modules() -> None:
    if not Path('web_gui/node_modules').exists():
        subprocess.run(['npm', 'ci'], cwd='web_gui', check=True)


def test_score_board_renders() -> None:
    ensure_node_modules()
    output = run_node(
        "import React from 'react';\n"
        "import ReactDOMServer from 'react-dom/server';\n"
        "import ScoreBoard from './ScoreBoard.js';\n"
        "const players = [\n"
        "  {name: 'Alice', score: 32000, hand: {tiles: [], melds: []}, river: []},\n"
        "  {name: 'Bob', score: 28000, hand: {tiles: [], melds: []}, river: []},\n"
        "  {name: 'Carol', score: 26000, hand: {tiles: [], melds: []}, river: []},\n"
        "  {name: 'Dave', score: 24000, hand: {tiles: [], melds: []}, river: []}\n"
        "];\n"
        "const html = ReactDOMServer.renderToStaticMarkup(\n"
        "  React.createElement(ScoreBoard, { players })\n"
        ");\n"
        "console.log(html);"
    )
    assert 'Alice' in output
    assert 'South' in output
    assert '32000' in output
