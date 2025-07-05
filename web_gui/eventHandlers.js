export function applyEvent(state, event) {
  if (!state) return state;
  const newState = JSON.parse(JSON.stringify(state));
  switch (event.name) {
    case 'start_game':
    case 'start_kyoku':
      return event.payload.state;
    case 'draw_tile': {
      const p = newState.players[event.payload.player_index];
      if (p) p.hand.tiles.push(event.payload.tile);
      if (newState.wall?.tiles?.length) newState.wall.tiles.pop();
      break;
    }
    case 'discard': {
      const p = newState.players[event.payload.player_index];
      if (p) {
        const { tile } = event.payload;
        const idx = p.hand.tiles.findIndex(
          (t) => t.suit === tile.suit && t.value === tile.value,
        );
        if (idx !== -1) p.hand.tiles.splice(idx, 1);
        p.river.push(tile);
      }
      break;
    }
    default:
      break;
  }
  return newState;
}
