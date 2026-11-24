// Verificación estática de secretos de la APLICACIÓN.
// Alcance: TODOS los archivos de la raíz del repositorio (incluidos .env*) + directorios de la app.
// No recorre docs/, evidencia/, evidence/ ni AUDITORIA_*: la documentación de Fase 0 tiene su propio control.
// Nunca imprime valores: solo archivo, línea y tipo de hallazgo.
import { existsSync, readdirSync, readFileSync, statSync } from 'node:fs';
import { dirname, join, relative, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const SCRIPT_ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');

// Directorios de la app que se recorren recursivamente (además de los archivos de la raíz).
export const APP_DIRS = ['src', 'tests', 'scripts', 'public', 'database', 'supabase', '.github'];
const SKIP_DIRS = new Set(['node_modules', 'dist', 'coverage', '.git', 'ocr']);
const SKIP_FILES = new Set(['package-lock.json']);
const BINARY_EXT =
  /\.(png|jpe?g|gif|webp|ico|woff2?|ttf|otf|eot|zip|gz|tgz|tar|7z|rar|pdf|mp4|mp3)$/i;

const KEYWORDS =
  '(?:api[_-]?key|secret|token|passw(?:or)?d|private[_-]?key|service[_-]?role|access[_-]?key)';

export const PATTERNS = [
  ['JWT', /eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}/],
  ['clave Supabase sb_', /\bsb_(secret|publishable)_[A-Za-z0-9_-]{10,}/],
  ['cadena de conexión', /postgres(?:ql)?:\/\/[^\s'"]+:[^\s'"@]+@/],
  ['clave privada', /-----BEGIN [A-Z ]*PRIVATE KEY-----/],
  ['clave tipo sk- (OpenAI/Anthropic)', /\bsk-(?:ant-)?[A-Za-z0-9_-]{20,}/],
  ['URL de proyecto Supabase', /https:\/\/[a-z0-9]{20}\.supabase\.co/],
  ['asignación service_role', /service_role[_a-z]*\s*[=:]\s*['"][A-Za-z0-9._-]{20,}/i],
  // Cohere no usa prefijo: se detecta por el nombre de la variable y un valor de 30+ caracteres.
  [
    'clave Cohere',
    /\b(?:CO_API_KEY|COHERE[A-Z0-9_]*(?:KEY|TOKEN|SECRET))\s*[=:]\s*['"]?[A-Za-z0-9]{30,}/i,
  ],
  ['clave AWS', /\b(?:AKIA|ASIA)[0-9A-Z]{16}\b/],
  ['token GitHub', /\b(?:ghp|gho|ghs|ghu)_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}/],
  ['clave Google API', /\bAIza[0-9A-Za-z_-]{35}\b/],
  ['token Slack', /\bxox[baprs]-[A-Za-z0-9-]{10,}/],
  ['token personal Supabase (sbp_)', /\bsbp_[a-f0-9]{40}\b/],
  ['clave Stripe', /\b[spr]k_(?:live|test)_[A-Za-z0-9]{20,}/],
  ['token npm', /\bnpm_[A-Za-z0-9]{36}\b/],
  ['token Hugging Face', /\bhf_[A-Za-z0-9]{34,}\b/],
  ['clave Groq', /\bgsk_[A-Za-z0-9]{40,}\b/],
  ['clave SendGrid', /\bSG\.[A-Za-z0-9_-]{22}\.[A-Za-z0-9_-]{43}\b/],
  ['token de .npmrc', /:_authToken\s*=\s*(?!\$\{)[^\s]{10,}/],
  [
    'cabecera Authorization con token',
    /\bAuthorization['"]?\s*[:=]\s*['"]?(?:Bearer|Basic|Token)\s+[A-Za-z0-9._~+/=-]{30,}/i,
  ],
];

// Asignación genérica de algo que parece secreto (NOMBRE_CLAVE=valor largo). Se ignoran los marcadores.
const GENERIC_ASSIGNMENT = new RegExp(
  `\\b[A-Za-z0-9_]*${KEYWORDS}[A-Za-z0-9_]*\\s*[=:]\\s*['"]?([A-Za-z0-9._/+=-]{20,})['"]?`,
  'i',
);
const PLACEHOLDER =
  /^(?:your|example|sample|changeme|change-me|placeholder|dummy|fake|test|xxx|<|\.\.\.)/i;
const looksLikePlaceholder = (value) =>
  PLACEHOLDER.test(value) || /(?:example|placeholder|changeme|xxxx)/i.test(value);

const GENERIC = 'asignación genérica de secreto';

/** Devuelve los nombres de los tipos de secreto detectados en un texto (nunca el valor). */
export function scanText(text) {
  const found = PATTERNS.filter(([, re]) => re.test(text)).map(([name]) => name);
  for (const line of text.split('\n')) {
    const m = GENERIC_ASSIGNMENT.exec(line);
    if (m && !looksLikePlaceholder(m[1] ?? '') && !found.includes(GENERIC)) found.push(GENERIC);
  }
  return found;
}

/** Igual que scanText pero con número de línea; nunca incluye el contenido de la línea. */
export function scanTextWithLines(text) {
  const findings = [];
  text.split('\n').forEach((line, i) => {
    for (const problem of scanText(line)) findings.push({ line: i + 1, problem });
  });
  return findings;
}

const isEnvFile = (name) => /^\.env(\..+|rc)?$/.test(name);
// Archivos que por su nombre suelen contener material secreto: no deben existir en el árbol de la app.
const SENSITIVE_NAME =
  /^(?:id_(?:rsa|dsa|ecdsa|ed25519)|\.netrc|credentials\.json|service-account.*\.json)$|\.(?:pem|p12|pfx|key)$/i;
const ARCHIVE_EXT = /\.(zip|gz|tgz|tar|7z|rar)$/i;

function* walk(dir) {
  for (const e of readdirSync(dir)) {
    if (SKIP_DIRS.has(e)) continue;
    const p = join(dir, e);
    if (statSync(p).isDirectory()) yield* walk(p);
    else yield p;
  }
}

function* candidates(root) {
  // 1) Todos los archivos de la raíz (no recursivo), incluidos dotfiles y .env*.
  for (const e of readdirSync(root)) {
    const p = join(root, e);
    if (statSync(p).isFile()) yield p;
  }
  // 2) Directorios de la app (recursivo).
  for (const d of APP_DIRS) {
    const p = join(root, d);
    if (existsSync(p) && statSync(p).isDirectory()) yield* walk(p);
  }
}

/**
 * Escanea `root` (por defecto, la raíz del repositorio calculada desde la ubicación de este script,
 * por lo que no depende del directorio de trabajo). Devuelve [{file, line?, problem}] sin valores.
 */
export function scanTree(root = SCRIPT_ROOT) {
  const findings = [];
  for (const f of candidates(root)) {
    const name = f.split('/').pop() ?? '';
    const rel = relative(root, f);
    if (SENSITIVE_NAME.test(name)) {
      findings.push({ file: rel, problem: 'archivo con nombre típico de material secreto' });
      continue;
    }
    if (SKIP_FILES.has(name) || BINARY_EXT.test(name)) continue;
    // Un .env real (no .env.example) no debe existir dentro del árbol de la app.
    if (isEnvFile(name) && name !== '.env.example') {
      findings.push({
        file: rel,
        problem: 'archivo .env presente (debe estar ignorado y no versionarse)',
      });
      continue;
    }
    const buf = readFileSync(f);
    if (buf.includes(0)) continue; // binario
    for (const h of scanTextWithLines(buf.toString('utf8'))) findings.push({ file: rel, ...h });
  }
  return findings;
}

/** Archivos comprimidos dentro del alcance que el escáner NO inspecciona (no se abren). */
export function listUninspectedArchives(root = SCRIPT_ROOT) {
  return [...candidates(root)].filter((f) => ARCHIVE_EXT.test(f)).map((f) => relative(root, f));
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const root = process.argv[2] ? resolve(process.argv[2]) : SCRIPT_ROOT;
  const findings = scanTree(root);
  if (findings.length) {
    console.error('SECRETOS/ARCHIVOS SOSPECHOSOS (valores omitidos):');
    for (const f of findings)
      console.error(` - ${f.file}${f.line ? `:${f.line}` : ''} — ${f.problem}`);
    process.exit(1);
  }
  console.log(
    'check:secrets OK — sin secretos detectados (análisis heurístico; ver docs/architecture/CONTROL_DE_SECRETOS.md)',
  );
  const skipped = listUninspectedArchives(root);
  if (skipped.length)
    console.log(
      `NOTA: ${skipped.length} archivo(s) comprimido(s) en el alcance NO se inspeccionan: ${skipped.join(', ')}`,
    );
}
