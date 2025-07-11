const controllers = new Map();

export function cleanupClaimOptions() {
  for (const c of controllers.values()) c.abort();
  controllers.clear();
}

function prepareSignal(id, signal) {
  if (!id) {
    console.warn('getClaimOptions requires a requestId');
    return signal;
  }
  if (signal) return signal;
  const prev = controllers.get(id);
  if (prev) prev.abort();
  const controller = new AbortController();
  controllers.set(id, controller);
  return controller.signal;
}

export async function getClaimOptions(server, gameId, log = () => {}, { signal, requestId } = {}) {
  const finalSignal = prepareSignal(requestId, signal);
  try {
    const url = `${server.replace(/\/$/, '')}/games/${gameId}/claims`;
    log('debug', `GET ${url} - fetch claim options`);
    const resp = await fetch(url, { signal: finalSignal });
    if (!resp.ok) return null;
    const data = await resp.json();
    return data.claims || [];
  } catch (err) {
    if (err.name === 'AbortError') return { aborted: true };
    return null;
  } finally {
    if (requestId) controllers.delete(requestId);
  }
}
