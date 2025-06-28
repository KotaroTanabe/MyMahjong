import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'fs/promises';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';

// Ensure built index.html contains the repo base path
// This verifies vite.config.ts is configured for GitHub Pages

test('build outputs assets under /MyMahjong/', async () => {
  const __dirname = dirname(fileURLToPath(import.meta.url));
  const indexPath = join(__dirname, '..', 'index.html');
  const html = await readFile(indexPath, 'utf8');
  assert.ok(
    html.includes('/MyMahjong/'),
    'index.html should reference assets relative to /MyMahjong/'
  );
});
