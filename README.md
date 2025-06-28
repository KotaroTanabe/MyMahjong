# MyMahjong

MyMahjong is a simple TypeScript monorepo for experimenting with a Mahjong game engine and related tooling. It contains three packages:

- **core** – the game logic such as tiles, players and wall implementation
- **cli** – a command line interface for playing the game in the terminal
- **web** – a minimal web layer that demonstrates using the core package

## Deployed to

https://kotarotanabe.github.io/MyMahjong/

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

### Run Tests

Tests are written with Node's built‑in `node:test` runner. Build and run tests for every package with:

```bash
npm test
```

### Package Layout

```
core/  – reusable game engine
cli/   – terminal interface using the core package
web/   – example web package also using the core package
```

Each package has its own `package.json` and `tsconfig.json`. The root `package.json` defines npm workspaces so the packages can reference each other.

## Continuous Integration

GitHub Actions run linting, type checking, build and tests for every pull request.
Once these checks succeed, the workflow automatically approves and merges the PR.

## Contributing

This repository is provided as a demonstration of Codex. We are not accepting
external pull requests or commits. If you have questions or suggestions, feel
free to open an issue.

