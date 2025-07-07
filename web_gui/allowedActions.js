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
