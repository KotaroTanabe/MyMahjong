export async function getClaims(server, gameId, log = () => {}, { signal, requestId } = {}) {
  try {
    const url = `${server.replace(/\/$/, '')}/games/${gameId}/claims`;
    log('debug', `GET ${url} - fetch claim options`);
    const resp = await fetch(url, { signal });
    if (!resp.ok) return { error: `HTTP ${resp.status}` };
    return await resp.json();
  } catch (err) {
    if (err.name === 'AbortError') return { aborted: true };
    return { error: err.message };
  }
}
