const controllers = new Map();

function prepareSignal(id, signal) {
  if (signal) return signal;
  if (!id) return undefined;
  const prev = controllers.get(id);
  if (prev) prev.abort();
  const controller = new AbortController();
  controllers.set(id, controller);
  return controller.signal;
}

export async function getAllowedActions(
  server,
  gameId,
  playerIndex,
  log = () => {},
  { signal, requestId } = {},
) {
  const finalSignal = prepareSignal(requestId, signal);
  try {
    const url = `${server.replace(/\/$/, '')}/games/${gameId}/allowed-actions/${playerIndex}`;
    log('debug', `GET ${url} - update allowed actions`);
    const resp = await fetch(url, { signal: finalSignal });
    if (!resp.ok) return [];
    const data = await resp.json();
    return data.actions || [];
  } catch (err) {
    if (err.name !== 'AbortError') {
      /* ignore other errors */
    }
    return [];
  } finally {
    if (requestId) controllers.delete(requestId);
  }
}

export async function getAllAllowedActions(
  server,
  gameId,
  log = () => {},
  { signal, requestId } = {},
) {
  const finalSignal = prepareSignal(requestId, signal);
  try {
    const url = `${server.replace(/\/$/, '')}/games/${gameId}/allowed-actions`;
    log('debug', `GET ${url} - fetch allowed actions`);
    const resp = await fetch(url, { signal: finalSignal });
    if (!resp.ok) return [];
    const data = await resp.json();
    return data.actions || [];
  } catch (err) {
    if (err.name !== 'AbortError') {
      /* ignore other errors */
    }
    return [];
  } finally {
    if (requestId) controllers.delete(requestId);
  }
}
