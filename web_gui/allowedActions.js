export async function getAllowedActions(server, gameId, playerIndex) {
  try {
    const resp = await fetch(
      `${server.replace(/\/$/, '')}/games/${gameId}/allowed-actions/${playerIndex}`
    );
    if (resp.ok) {
      const data = await resp.json();
      return Array.isArray(data.actions) ? data.actions : [];
    }
  } catch {
    /* ignore fetch errors */
  }
  return [];
}
