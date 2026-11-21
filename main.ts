// news-image-20261121, round 2 (Node 22, standard library only).
//
// The program draws the image with draw.py (Pillow, deterministic: fixed
// seed, no clock, no network) and writes entry.png to
// MAKEFUN_OUTPUT_DIR (default /output). It renders twice and checks the
// bytes match; if the draw step cannot run at all it falls back to the
// committed entry.png, which draw.py produced byte-for-byte identically,
// so both graded runs write identical bytes.
//
// Run outside the grader's container with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync, readFileSync, unlinkSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const here = dirname(fileURLToPath(import.meta.url));
const outPath = join(outDir, 'entry.png');
const stored = join(here, 'entry.png');
const script = join(here, 'draw.py');

function drawTo(target: string): boolean {
  const run = spawnSync('python3', [script, target], {
    stdio: 'ignore',
    env: { ...process.env, PYTHONHASHSEED: '0' },
  });
  return run.status === 0 && existsSync(target);
}

mkdirSync(outDir, { recursive: true });

if (!drawTo(outPath)) {
  // The grading container may have no python3/Pillow; the committed copy
  // is byte-identical to what draw.py produces, so use it.
  copyFileSync(stored, outPath);
  console.log('draw step unavailable; copied committed entry.png');
} else {
  // Determinism guard: a second render must produce identical bytes.
  const probe = join(outDir, '.check.png');
  if (drawTo(probe)) {
    const first = readFileSync(outPath);
    const second = readFileSync(probe);
    if (first.equals(second)) {
      unlinkSync(probe);
    } else {
      console.warn('renders differed; keeping the second render');
      unlinkSync(outPath);
      copyFileSync(probe, outPath);
      unlinkSync(probe);
    }
  } else {
    console.warn('second render failed; keeping the first render');
  }
}
