// news-image-20261127 entry (Node, standard library only). The image is entry.png beside this file, rendered
// offline by tools/build.py. This program validates the gate, then writes /output/entry.png atomically.
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { readFileSync, writeFileSync, renameSync, rmSync } from 'node:fs';
import { join } from 'node:path';

const MAX_BYTES = 1024 * 1024;
const MAX_DIM = 1024;

function fail(msg: string): never {
  console.error(`entry check failed: ${msg}`);
  process.exit(1);
}

const bytes = readFileSync(new URL('./entry.png', import.meta.url));
if (bytes.length > MAX_BYTES) fail(`${bytes.length} bytes exceeds ${MAX_BYTES}`);
const sig = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (bytes.length < 33 || !bytes.subarray(0, 8).equals(sig)) fail('not a PNG');
if (bytes.subarray(12, 16).toString('latin1') !== 'IHDR') fail('PNG missing IHDR');
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width < 1 || height < 1 || width > MAX_DIM || height > MAX_DIM) fail(`dimensions ${width}x${height} exceed ${MAX_DIM}x${MAX_DIM}`);
if (!bytes.subarray(bytes.length - 12).equals(Buffer.from('0000000049454e44ae426082', 'hex'))) fail('PNG truncated (no IEND)');

const dir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const tmp = join(dir, '.entry.png.tmp');
try {
  writeFileSync(tmp, bytes);
  renameSync(tmp, join(dir, 'entry.png'));
} catch (e) {
  rmSync(tmp, { force: true });
  fail(`could not write output: ${(e as Error).message}`);
}
