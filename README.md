# MyMahjong

MyMahjong is a simple TypeScript monorepo for experimenting with a Mahjong game engine and related tooling. It contains three packages:

- **core** – the game logic such as tiles, players and wall implementation
- **cli** – a command line interface for playing the game in the terminal
- **web** – a minimal web layer that demonstrates using the core package

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

## Contributing

1. Fork the repository and create a new branch.
2. Install dependencies and ensure `npm run lint`, `npm run typecheck`, `npm run build`, and `npm test` all succeed.
3. Commit your changes with clear messages and open a pull request.

Feel free to open issues or suggestions for improvements.

