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

export async function getNextActions(
  server,
  gameId,
  log = () => {},
  { signal, requestId } = {},
) {
  const finalSignal = prepareSignal(requestId, signal);
  try {
    const url = `${server.replace(/\/$/, '')}/games/${gameId}/next-actions`;
    log('debug', `GET ${url} - fetch next actions`);
    const resp = await fetch(url, { signal: finalSignal });
    if (!resp.ok) return null;
    return await resp.json();
  } catch (err) {
    if (err.name === 'AbortError') return { aborted: true };
    return null;
  } finally {
    if (requestId) controllers.delete(requestId);
  }
}
