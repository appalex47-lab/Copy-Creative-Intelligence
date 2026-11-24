// Copia los archivos del OCR (tesseract.js) a public/ocr para que se sirvan DESDE LA PROPIA APP: sin CDN, sin red
// externa. Se ejecuta en `postinstall`; public/ocr está en .gitignore (se regenera con `npm ci`).
import { copyFileSync, mkdirSync, existsSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const NM = join(ROOT, 'node_modules');
const OUT = join(ROOT, 'public', 'ocr');

const FILES = [
  ['tesseract.js/dist/worker.min.js', 'worker.min.js'],
  ['tesseract.js-core/tesseract-core-simd-lstm.wasm.js', 'core/tesseract-core-simd-lstm.wasm.js'],
  ['tesseract.js-core/tesseract-core-lstm.wasm.js', 'core/tesseract-core-lstm.wasm.js'],
  ['@tesseract.js-data/spa/4.0.0_best_int/spa.traineddata.gz', 'lang/spa.traineddata.gz'],
  ['@tesseract.js-data/eng/4.0.0_best_int/eng.traineddata.gz', 'lang/eng.traineddata.gz'],
];

for (const [from, to] of FILES) {
  const src = join(NM, from);
  if (!existsSync(src)) {
    console.error(`[ocr] Falta ${from}. Ejecuta "npm ci".`);
    process.exit(1);
  }
  mkdirSync(dirname(join(OUT, to)), { recursive: true });
  copyFileSync(src, join(OUT, to));
}
console.log(`[ocr] ${String(FILES.length)} archivos copiados a public/ocr`);
