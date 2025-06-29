# @mymahjong/web

A minimal React front end that consumes the core Mahjong logic. To develop locally run `npm run dev -w web` and open `http://localhost:5173`.

The web package is intentionally simple and serves as a reference for using the core logic in the browser. The game board lays out each player's area around a central stack. Currently only the bottom player's hand is interactive.

Tile images live under `public/tiles/`. Real graphics are omitted here because binary assets cannot be committed. Each file is a tiny SVG displaying an emoji placeholder.
