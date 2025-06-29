import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const cssPath = path.join(__dirname, '../../src/style.css');

const css = fs.readFileSync(cssPath, 'utf8');

test('style.css includes responsive media query', () => {
  assert.match(css, /@media\s*\(max-width:\s*600px\)/);
  assert.match(css, /grid-template-areas:[^}]*'top'[\s\S]*'left'[\s\S]*'right'[\s\S]*'center'[\s\S]*'bottom'/);
});
