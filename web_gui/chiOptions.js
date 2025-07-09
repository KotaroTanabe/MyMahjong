export async function getChiOptions(server, gameId, playerIndex, log = () => {}) {
  try {
    const url = `${server.replace(/\/$/, '')}/games/${gameId}/chi-options/${playerIndex}`;
    log('debug', `GET ${url} - fetch chi options`);
    const resp = await fetch(url);
    if (!resp.ok) return [];
    const data = await resp.json();
    return data.options || [];
  } catch {
    return [];
  }
}

