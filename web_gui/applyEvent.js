export function applyEvent(state, event) {
  if (!state) return state;
  const newState = JSON.parse(JSON.stringify(state));
  if (!Array.isArray(newState.waiting_for_claims)) newState.waiting_for_claims = [];
  switch (event.name) {
    case 'start_game':
      return event.payload.state;
    case 'start_kyoku':
      return event.payload.state;
    case 'draw_tile': {
      const p = newState.players[event.payload.player_index];
      if (p) p.hand.tiles.push(event.payload.tile);
      const replacement =
        event.payload.replacement_for_kan ||
        newState._pendingKanReplacement === true;
      if (replacement) {
        if (Array.isArray(newState.dead_wall) && newState.dead_wall.length) {
          newState.dead_wall.pop();
        }
      } else if (!event.payload.from_dead_wall && newState.wall?.tiles?.length) {
        newState.wall.tiles.pop();
      }
      newState._pendingKanReplacement = false;
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
      newState.waiting_for_claims = newState.players
        .map((_, i) => i)
        .filter((i) => i !== event.payload.player_index);
      break;
    }
    case 'claims': {
      newState.claim_options = event.payload.claims || [];
      break;
    }
    case 'meld': {
      const p = newState.players[event.payload.player_index];
      if (p) {
        const called = event.payload.meld.called_index;
        event.payload.meld.tiles.forEach((m, i) => {
          if (called !== null && i === called) return;
          const idx = p.hand.tiles.findIndex(
            (t) => t.suit === m.suit && t.value === m.value,
          );
          if (idx !== -1) p.hand.tiles.splice(idx, 1);
        });
        p.hand.melds.push(event.payload.meld);
      }
      if (typeof newState.last_discard_player === 'number') {
        const d = newState.players[newState.last_discard_player];
        if (d?.river?.length) d.river.pop();
      }
      newState.last_discard = null;
      newState.last_discard_player = null;
      newState.current_player = event.payload.player_index;
      newState.waiting_for_claims = [];
      if (event.payload.meld?.type?.includes('kan')) {
        newState._pendingKanReplacement = true;
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
      if (Array.isArray(event.payload.scores)) {
        newState.players.forEach((p, i) => {
          if (p) p.score = event.payload.scores[i];
        });
      }
      newState.result = { type: event.name, ...event.payload };
      newState.waiting_for_claims = [];
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
    case 'end_game': {
      if (Array.isArray(event.payload.scores)) {
        newState.players.forEach((p, i) => {
          if (p) p.score = event.payload.scores[i];
        });
      }
      newState.result = { type: 'end_game', ...event.payload };
      newState.waiting_for_claims = [];
      break;
    }
    case 'round_end':
      break;
    case 'claims_closed':
      newState.waiting_for_claims = [];
      break;
    case 'next_actions':
      if (typeof event.payload.player_index === 'number') {
        newState.current_player = event.payload.player_index;
      }
      break;
    case 'skip': {
      if (!Array.isArray(state.waiting_for_claims) || state.waiting_for_claims.length === 0) {
        break;
      }
      newState.waiting_for_claims = newState.waiting_for_claims.filter(
        (i) => i !== event.payload.player_index,
      );
      if (newState.waiting_for_claims.length === 0) {
        const base =
          typeof newState.last_discard_player === 'number'
            ? newState.last_discard_player
            : event.payload.player_index;
        newState.current_player = (base + 1) % newState.players.length;
      }
      break;
    }
    default:
      break;
  }
  return newState;
}
