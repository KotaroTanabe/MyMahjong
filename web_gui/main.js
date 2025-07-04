export async function init() {
  const statusEl = document.getElementById('status');
  if (!statusEl) return;
  try {
    const resp = await fetch('http://localhost:8000/health');
    if (resp.ok) {
      const data = await resp.json();
      statusEl.textContent = `Server status: ${data.status}`;
    } else {
      statusEl.textContent = `Server error: ${resp.status}`;
    }
  } catch (err) {
    statusEl.textContent = 'Failed to contact server';
  }
}

init();
