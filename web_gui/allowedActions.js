export async function getAllowedActions(server, gameId, playerIndex, log = () => {}) {
  try {
    const url = `${server.replace(/\/$/, '')}/games/${gameId}/allowed-actions/${playerIndex}`;
    log('debug', `GET ${url} - update allowed actions`);
    const resp = await fetch(url);
    if (!resp.ok) return [];
    const data = await resp.json();
    return data.actions || [];
  } catch {
    return [];
  }
}

export async function getAllAllowedActions(server, gameId, log = () => {}) {
  try {
    const url = `${server.replace(/\/$/, '')}/games/${gameId}/allowed-actions`;
    log('debug', `GET ${url} - fetch allowed actions`);
    const resp = await fetch(url);
    if (!resp.ok) return [];
    const data = await resp.json();
    return data.actions || [];
  } catch {
    return [];
  }
}

export function applyAllowedActionsEvent(current, event) {
  if (event?.name === 'allowed_actions' && Array.isArray(event.payload?.actions)) {
    return event.payload.actions;
  }
  return current;
}
