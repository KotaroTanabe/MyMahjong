# MyMahjong

MyMahjong is a simple TypeScript monorepo for experimenting with a Mahjong game engine and related tooling.  The repository is intentionally small so the entire system can be understood at a glance.  It contains three packages:

- **core** – the game logic such as tiles, players and wall implementation
- **cli** – a command line interface for playing the game in the terminal
- **web** – a minimal web layer that demonstrates using the core package

## Implementation status

The repository currently includes initial engine modules in the **core**
package along with a minimal **cli**, **web** server and **web_gui**.
Future work will expand these components.

### Packages

 - [x] core
 - [x] cli
 - [x] web
 - [x] web_gui

### Features

- [ ] Mortal AI integration
- [x] Mortal backend integration design
- [ ] MJAI protocol support
- [x] Basic MJAI event serialization
- [x] GameState JSON serialization
- [x] RuleSet interface for scoring
- [x] Local single-player play via CLI
- [x] Basic remote game creation via CLI
- [x] Join remote games via CLI
- [x] Draw tile in remote games via CLI
- [x] View remote game state via CLI
- [x] Remote server health check via CLI
- [x] REST + WebSocket API
- [x] Basic REST endpoints (create game, fetch game, health)
- [x] Web GUI served through GitHub Pages
- [x] Basic GUI status display
- [x] GUI server selection and retry
- [x] React front-end skeleton
- [x] Basic board layout
- [x] Hand & River components
- [x] Meld area component
- [x] Center display (dora & wall count)
- [x] Tile emoji rendering in GUI
- [x] Basic draw control via REST API
- [x] Discard tiles via GUI
- [x] Start game via GUI
- [x] Continuous integration workflow
- [x] Core <-> interface API documented
- [x] GUI design documented
- [ ] 何切る問題 mode

### Core engine capabilities

 - [x] start_game
 - [x] deal_initial_hands
- [x] draw_tile
- [x] discard_tile
- [x] get_state
- [x] scoring
- [x] call_chi
- [x] call_pon
- [x] call_kan
- [x] declare_tsumo
- [x] declare_ron
- [x] declare_riichi
- [x] skip
- [x] end_game
- [x] standard wall initialization
- [x] configurable ruleset
- [x] event log
- [x] current player tracking
- [x] action dispatch helper

## Implementation plan progress

- [x] **1. Create the game engine** – wrap the Python `mahjong` library and expose
  methods for drawing, discarding and scoring.
- [ ] **2. Integrate Mortal AI** – add a module that uses the
  [MJAI high level API](https://mjai.app/docs/highlevel-api) to communicate with
  the AI process and execute its moves.
- [x] **3. Build CLI** – provide commands for starting a local game against the AI and
  for connecting to remote games.
- [x] **4. Implement FastAPI server** – expose REST endpoints and prepare a WebSocket
  channel for real-time play.
- [x] **5. Develop React front-end** – consume the API and present a board based on the
  `docs/board-layout.md` design.
- [ ] **6. Implement MJAI adapter** – translate game state to and from
  `docs/mjai-ai-integration.md` so AI engines can connect via the protocol.
- [x] **7. Set up GitHub Actions** – lint, type check, run tests and deploy the built
  web front-end to GitHub Pages.
- [ ] **8. Add action endpoints** – implement `POST /games/{id}/action` for draw,
  discard, meld calls and win declarations.
- [x] **9. Stream events via WebSocket** – create `/ws/{id}` to push engine events so
  the GUI updates instantly.
 - [x] **10. Connect GUI state** – update React components to fetch the initial game,
  handle WebSocket events and send player actions.
- [ ] **11. Provide a mock AI** – run a simple MJAI-compatible process through the
  adapter with an interface that later swaps in Mortal.
- [ ] **12. Write end-to-end tests** – cover REST routes, WebSocket updates and basic
  GUI interactions.
- [ ] **13. Add `何切る問題` mode** – offer a practice scenario with a random seat wind
  and dora where the user picks a discard and the AI suggests a move.

### Remaining tasks

The following plan steps are not yet implemented:

- Step 2 – Integrate Mortal AI.
- Step 6 – Implement MJAI adapter.
- Step 8 – Add full action endpoints.
- Step 11 – Provide a mock AI.
- Step 12 – Write end-to-end tests.
- Step 13 – Add `何切る問題` mode.

See `docs/detailed-design.md` for an overview of the planned architecture.
`docs/web-gui-architecture.md` provides more details about the planned React GUI.

## 何切る問題 mode (planned)

This practice mode will present a what-to-discard problem to the player.

### Planned workflow

1. Randomly choose the seat wind and dora indicator.
2. Assume it is the dealer's first turn with no prior actions.
3. Display the hand and let the user select a discard.
4. Ask the AI to compute its recommended discard.
5. Show the AI suggestion to the user for comparison.

## Running locally

### Start the FastAPI server

The API server depends on the **core** package. Install the [**uv**](https://github.com/astral-sh/uv) tool and use it to install the editable packages before running `uvicorn`:

```bash
curl -Ls https://astral.sh/uv/install.sh | sh
uv pip install -e ./core -e ./web
uvicorn web.server:app --reload
```

### Start the web GUI

The front-end is a small React app built with Vite. Start the development server
from the `web_gui` directory:

```bash
cd web_gui
npm install
npx vite --open
```

### Start both together

You can launch the FastAPI server and the React GUI at the same time using
`run_local.py`:

```bash
python run_local.py
```

The GUI will automatically connect to the local FastAPI server's REST endpoints.

## Deployed to

The static web GUI in the `web_gui` directory is built and deployed via GitHub Pages:

https://kotarotanabe.github.io/MyMahjong/

## Continuous Integration

GitHub Actions run linting, type checking, build and tests for every pull request.
Once these checks succeed, the workflow automatically approves and merges the PR.
