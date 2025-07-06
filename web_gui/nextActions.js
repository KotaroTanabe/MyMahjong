export async function getNextActions(server, gameId) {
  try {
    const resp = await fetch(
      `${server.replace(/\/$/, '')}/games/${gameId}/next-actions`
    );
    if (!resp.ok) return null;
    return await resp.json();
  } catch {
    return null;
  }
}
