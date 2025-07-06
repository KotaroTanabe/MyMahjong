export async function getAllowedActions(server, gameId, playerIndex) {
  try {
    const resp = await fetch(
      `${server.replace(/\/$/, '')}/games/${gameId}/allowed-actions/${playerIndex}`
    );
    if (!resp.ok) return [];
    const data = await resp.json();
    return data.actions || [];
  } catch {
    return [];
  }
}
