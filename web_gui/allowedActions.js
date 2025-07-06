export function getAllowedActions(state, playerIndex) {
  const actions = new Set();
  if (!state || !state.players || !state.players[playerIndex]) return [];
  const player = state.players[playerIndex];
  const tiles = player.hand?.tiles || [];
  const last = state.last_discard;
  const lastPlayer = state.last_discard_player;
  const numPlayers = state.players.length;

  if (playerIndex === state.current_player || state.waiting_for_claims?.includes(playerIndex)) {
    actions.add('skip');
  }

  if (last && lastPlayer !== null && lastPlayer !== playerIndex) {
    const match = (t) => t.suit === last.suit && t.value === last.value;
    const count = tiles.filter(match).length;
    if (count >= 2) actions.add('pon');
    if (count >= 3) actions.add('kan');
    if (
      (lastPlayer + 1) % numPlayers === playerIndex &&
      ['man', 'pin', 'sou'].includes(last.suit)
    ) {
      const has = (v) =>
        tiles.some((t) => t.suit === last.suit && t.value === v);
      if (has(last.value - 2) && has(last.value - 1)) actions.add('chi');
      if (has(last.value - 1) && has(last.value + 1)) actions.add('chi');
      if (has(last.value + 1) && has(last.value + 2)) actions.add('chi');
    }
    // Ron detection not implemented
  }

  const counts = {};
  for (const t of tiles) {
    if (!t) continue;
    const key = `${t.suit}-${t.value}`;
    counts[key] = (counts[key] || 0) + 1;
    if (counts[key] >= 4) actions.add('kan');
  }

  if (!player.riichi) actions.add('riichi');

  return Array.from(actions);
}
