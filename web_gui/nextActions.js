export async function getNextActions(server, gameId, log = () => {}) {
  try {
    const url = `${server.replace(/\/$/, '')}/games/${gameId}/next-actions`;
    log('debug', `GET ${url} - fetch next actions`);
    const resp = await fetch(url);
    if (!resp.ok) return null;
    return await resp.json();
  } catch {
    return null;
  }
}
