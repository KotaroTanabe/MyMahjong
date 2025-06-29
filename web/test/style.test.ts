import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'fs/promises';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));

async function readCss(): Promise<string> {
  const cssPath = join(__dirname, '../../src/style.css');
  return readFile(cssPath, 'utf8');
}

test('style.css includes height and overflow rules', async () => {
  const css = await readCss();
  assert.match(css, /\.player-area\.top[^}]*min-height:\s*6rem/);
  assert.match(css, /\.player-area\.bottom[^}]*min-height:\s*6rem/);
  assert.match(css, /\.player-area\.left[^}]*min-height:\s*6rem/);
  assert.match(css, /\.player-area\.right[^}]*min-height:\s*6rem/);
  assert.match(css, /\.discards[^}]*overflow-y:\s*auto/);
  assert.match(css, /\.melds[^}]*overflow-y:\s*auto/);
});

test('hand layout is horizontal', async () => {
  const css = await readCss();
  assert.match(css, /\.hand[^}]*display:\s*flex/);
});

test('font sizes are reduced for small screens', async () => {
  const css = await readCss();
  assert.match(css, /body[^}]*font-size:\s*0\.875rem/);
  assert.match(css, /\.app h1[^}]*font-size:\s*1\.25rem/);
});
