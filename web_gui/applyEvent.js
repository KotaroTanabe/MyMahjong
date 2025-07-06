export function applyEvent(state, event) {
  if (!state) return state;
  const newState = JSON.parse(JSON.stringify(state));
  switch (event.name) {
    case 'start_game':
      return event.payload.state;
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
      newState.current_player =
        (event.payload.player_index + 1) % newState.players.length;
      newState.last_discard = event.payload.tile;
      newState.last_discard_player = event.payload.player_index;
      break;
    }
    case 'meld': {
      const p = newState.players[event.payload.player_index];
      if (p) {
        event.payload.meld.tiles.forEach((m) => {
          const idx = p.hand.tiles.findIndex(
            (t) => t.suit === m.suit && t.value === m.value,
          );
          if (idx !== -1) p.hand.tiles.splice(idx, 1);
        });
        p.hand.melds.push(event.payload.meld);
      }
      break;
    }
    case 'riichi': {
      const p = newState.players[event.payload.player_index];
      if (p) {
        p.riichi = true;
        if (typeof event.payload.score === 'number') {
          p.score = event.payload.score;
        }
      }
      if (typeof event.payload.riichi_sticks === 'number') {
        newState.riichi_sticks = event.payload.riichi_sticks;
      }
      break;
    }
    case 'tsumo':
    case 'ron': {
      newState.result = event.payload;
      break;
    }
    case 'ryukyoku': {
      if (Array.isArray(event.payload.scores)) {
        newState.players.forEach((p, i) => {
          if (p) p.score = event.payload.scores[i];
        });
      }
      newState.result = { type: 'ryukyoku', ...event.payload };
      break;
    }
    case 'skip': {
      const next = (event.payload.player_index + 1) % newState.players.length;
      newState.current_player = next;
      break;
    }
    default:
      break;
  }
  return newState;
}
