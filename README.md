# MyMahjong

MyMahjong is a simple TypeScript monorepo for experimenting with a Mahjong game engine and related tooling.  The repository is intentionally small so the entire system can be understood at a glance.  It contains three packages:

- **core** – the game logic such as tiles, players and wall implementation
- **cli** – a command line interface for playing the game in the terminal
- **web** – a minimal web layer that demonstrates using the core package

## Deployed to

https://kotarotanabe.github.io/MyMahjong/

### GitHub Pages

Running `npm run build` from the repository root compiles every package and
produces static files for the web demo under `web/dist`. The CI workflow deploys
those files to GitHub Pages using
[peaceiris/actions-gh-pages](https://github.com/peaceiris/actions-gh-pages).
You can preview the built site locally with:

```bash
npm run build
npm run preview -w web
```

The web build uses the repository name as its base path so assets resolve
correctly on GitHub Pages. If you fork this project, update `web/vite.config.ts`
to use your repository name.


## Overview

The **core** package models tiles, player hands and the wall.  The **cli**
package provides a simple terminal interface for a few demonstration turns, and
the **web** package shows how the same logic can drive a React app.  Feel free
to expand the rules or presentation layer to suit your needs.

## Getting Started

### Install Dependencies

Use [Node.js](https://nodejs.org/) and install dependencies for all workspaces from the repository root:

```bash
npm install
```

### Build

Compile all TypeScript packages using:

```bash
npm run build
```

You can also build a specific workspace by passing the `-w` option. For example
the following will compile only the core package:

```bash
npm run build -w core
```
### Running the CLI

Build and launch the command line interface:

```bash
npm run build -w cli
npm start -w cli
```

### Running the Web Demo

Start the Vite development server:

```bash
npm run dev -w web
```

Then open `http://localhost:5173` in your browser.

The board layout places each player's area around the center. Discards are displayed as a traditional 河 with tiles aligned per seat. At this stage only
the bottom player shows the actual hand and discard pile. Further layout details
are described in [docs/board-layout.md](docs/board-layout.md).

### Custom Game Setup

The `useGame` hook accepts an optional `Game` instance. This is handy for tests
or when you want to provide a pre-configured wall of tiles. If no game is
provided, `useGame` creates a new one and deals the first player.

### Scoring

After each discard the game now evaluates your hand for the simple `tanyao` yaku
and checks for `chiitoitsu` (seven pairs). The scorer also detects `yakuhai`
triplets of winds or dragons.
When applicable, the CLI and web UI display the possible yaku, the number of han
and total points.

### Rule Coverage

The core engine implements only a small slice of Mahjong. Below is the current
status and a suggested roadmap for extending the rules.

**Implemented**

- Generation of all 136 tiles and shuffled wall
- Dealing, drawing and discarding tiles
- Basic win detection for standard hands
- Win by ron (claiming another player's discard)
- Ability to call pon, chi and kan (melds)
- Scoring for:
  - `tanyao` (all simples)
  - `chiitoitsu` (seven pairs)
  - `yakuhai` triplets of winds or dragons
  - `iipeikou` (two identical sequences)
  - `dora` bonus tiles from indicators
- Seat wind assignment and dealer rotation
- Round progression with changing round winds

**Not Yet Implemented**

- Additional yaku and detailed fu/han scoring
- Riichi and other advanced rules

**Recommended Next Steps**

1. Expand the scoring system with more yaku and fu calculations
2. Add riichi declarations for advanced rules


### Run Tests

Tests are written with Node's built‑in `node:test` runner. Build and run tests for every package with:

```bash
npm test
```

Individual workspaces can be tested using `-w` as well. The command below runs only the CLI tests:

```bash
npm test -w cli
```

### Package Layout

```
core/  – reusable game engine
cli/   – terminal interface using the core package
web/   – example web package also using the core package
```

Each package has its own `package.json` and `tsconfig.json`. The root
`package.json` defines npm workspaces so the packages can reference each other
without publishing to a registry. Source lives in the `src` folders and compiled
JavaScript is emitted to `dist` when you run the build script.

## Continuous Integration

GitHub Actions run linting, type checking, build and tests for every pull request.
Once these checks succeed, the workflow automatically approves and merges the PR.

## Contributing

This repository is provided as a demonstration of Codex. We are not accepting
external pull requests or commits. If you have questions or suggestions, feel
free to open an issue.

