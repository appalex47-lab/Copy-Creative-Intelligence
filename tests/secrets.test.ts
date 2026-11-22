import { spawnSync } from 'node:child_process';
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';
import { listUninspectedArchives, scanText, scanTree } from '../scripts/check-secrets.mjs';

const REPO = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const SCRIPT = join(REPO, 'scripts', 'check-secrets.mjs');

// Valores FICTICIOS construidos por partes: este archivo no contiene literales con forma de secreto.
const fake = {
  jwt: [
    'eyJ',
    'hbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9',
    '.eyJzdWIiOiIxMjM0NTY3ODkwIn0',
    '.abcdefghijklmnop',
  ].join(''),
  conn: ['postgresql', '://user:pass', '@host/db'].join(''),
  pem: ['-----BEGIN ', 'PRIVATE KEY-----'].join(''),
  supaUrl: ['https://', 'abcdefghijklmnopqrst', '.supabase.co'].join(''),
  cohere: ['COHERE_API', '_KEY=', 'a1B2c3D4e5F6g7H8i9J0k1L2m3N4o5P6q7R8s9T0'].join(''),
  coShort: ['CO_API', '_KEY=', 'Zz9Yy8Xx7Ww6Vv5Uu4Tt3Ss2Rr1Qq0Pp9Oo8Nn7Mm6'].join(''),
  aws: ['AKIA', 'ABCDEFGHIJKLMNOP'].join(''),
  gh: ['ghp', '_', 'abcdefghijklmnopqrstuvwxyz0123456789'].join(''),
  sk: ['sk', '-', 'abcdefghijklmnopqrstuvwxyz0123456789'].join(''),
  sbp: ['sb', 'p_', '0123456789abcdef0123456789abcdef01234567'].join(''),
  stripe: ['sk', '_live_', 'abcdefghijklmnopqrstuvwx'].join(''),
  npm: ['npm', '_', 'abcdefghijklmnopqrstuvwxyz0123456789'].join(''),
  hf: ['hf', '_', 'abcdefghijklmnopqrstuvwxyzABCDEFGH'].join(''),
  npmrc: ['//registry.npmjs.org/', ':_auth', 'Token=', 'abcdefghij0123456789'].join(''),
  bearer: ['Authorization: Bearer ', 'abcdefghijklmnopqrstuvwxyz0123456789'].join(''),
  generic: ['MY_SERVICE_TOKEN', '=', 'abcdefghij0123456789klmnop'].join(''),
};

describe('scanText (positivas)', () => {
  it.each([
    ['JWT', fake.jwt],
    ['cadena de conexión', fake.conn],
    ['clave privada', fake.pem],
    ['URL de proyecto Supabase', fake.supaUrl],
    ['clave Cohere', fake.cohere],
    ['clave Cohere', fake.coShort],
    ['clave AWS', fake.aws],
    ['token GitHub', fake.gh],
    ['clave tipo sk- (OpenAI/Anthropic)', fake.sk],
    ['token personal Supabase (sbp_)', fake.sbp],
    ['clave Stripe', fake.stripe],
    ['token npm', fake.npm],
    ['token Hugging Face', fake.hf],
    ['token de .npmrc', fake.npmrc],
    ['cabecera Authorization con token', fake.bearer],
    ['asignación genérica de secreto', fake.generic],
  ])('detecta %s', (nombre, texto) => {
    expect(scanText(texto)).toContain(nombre);
  });
});

describe('scanText (negativas)', () => {
  it.each([
    'VITE_APP_ENV=development',
    'VITE_DATA_MODE=demo',
    '# VITE_SUPABASE_ANON_KEY=',
    'COHERE_API_KEY=',
    'COHERE_API_KEY=your-cohere-key-goes-here-example',
    'const token = useToken();',
    'password: string;',
    'Authorization: `Bearer ${token}`',
    '//registry.npmjs.org/:_authToken=${NPM_TOKEN}',
  ])('no marca %s', (texto) => {
    expect(scanText(texto)).toEqual([]);
  });
});

describe('scanTree con archivos temporales', () => {
  let dir: string;
  beforeEach(() => {
    dir = mkdtempSync(join(tmpdir(), 'cci-secrets-'));
    mkdirSync(join(dir, 'src'));
  });
  afterEach(() => rmSync(dir, { recursive: true, force: true }));

  it.each(['.env', '.env.local', '.env.production', '.env.development.local'])(
    'detecta %s en la raíz sin leer su valor',
    (name) => {
      writeFileSync(join(dir, name), 'FOO=bar\n');
      const f = scanTree(dir);
      expect(f.map((x) => x.file)).toContain(name);
      expect(JSON.stringify(f)).not.toContain('bar');
    },
  );

  it('detecta un .env dentro de un directorio de la app', () => {
    writeFileSync(join(dir, 'src', '.env.local'), 'A=1\n');
    expect(scanTree(dir).map((x) => x.file)).toContain(join('src', '.env.local'));
  });

  it('acepta un .env.example con solo valores de ejemplo', () => {
    writeFileSync(
      join(dir, '.env.example'),
      [
        'VITE_APP_ENV=development',
        'VITE_DATA_MODE=demo',
        '# VITE_SUPABASE_ANON_KEY=',
        'COHERE_API_KEY=',
        '',
      ].join('\n'),
    );
    expect(scanTree(dir)).toEqual([]);
  });

  it('rechaza un .env.example que contenga un valor real-looking', () => {
    writeFileSync(join(dir, '.env.example'), `${fake.cohere}\n`);
    expect(scanTree(dir).map((x) => x.problem)).toContain('clave Cohere');
  });

  it('detecta secretos en archivos de la raíz y en src, con línea y sin revelar el valor', () => {
    writeFileSync(join(dir, 'config.txt'), `ok\n${fake.generic}\n`);
    writeFileSync(join(dir, 'src', 'a.ts'), `const x = '${fake.jwt}';\n`);
    const f = scanTree(dir);
    expect(f).toEqual(
      expect.arrayContaining([
        { file: 'config.txt', line: 2, problem: 'asignación genérica de secreto' },
        { file: join('src', 'a.ts'), line: 1, problem: 'JWT' },
      ]),
    );
    const out = JSON.stringify(f);
    for (const v of [fake.jwt, 'abcdefghij0123456789klmnop']) expect(out).not.toContain(v);
  });

  it.each(['id_rsa', 'server.pem', 'clave.key', 'credentials.json', '.netrc'])(
    'detecta archivo con nombre típico de material secreto: %s',
    (name) => {
      writeFileSync(join(dir, name), 'x\n');
      expect(scanTree(dir).map((x) => x.file)).toContain(name);
    },
  );

  it('detecta .envrc', () => {
    writeFileSync(join(dir, '.envrc'), 'export A=1\n');
    expect(scanTree(dir).map((x) => x.file)).toContain('.envrc');
  });

  it('los comprimidos no se abren y se listan como NO inspeccionados (límite documentado)', () => {
    writeFileSync(join(dir, 'evidencia.zip'), `${fake.jwt}`);
    mkdirSync(join(dir, 'src', 'x'));
    writeFileSync(join(dir, 'src', 'x', 'a.tar.gz'), `${fake.jwt}`);
    expect(scanTree(dir)).toEqual([]); // ni se abren ni se marcan
    expect(listUninspectedArchives(dir).sort()).toEqual([
      'evidencia.zip',
      join('src', 'x', 'a.tar.gz'),
    ]);
  });

  it('ignora node_modules, dist y directorios fuera del alcance (docs)', () => {
    for (const d of ['node_modules', 'dist', 'docs']) {
      mkdirSync(join(dir, d));
      writeFileSync(join(dir, d, 'x.txt'), `${fake.jwt}\n`);
    }
    expect(scanTree(dir)).toEqual([]);
  });
});

describe('CLI', () => {
  it('funciona desde cualquier directorio de trabajo y no filtra valores', () => {
    const cwd = mkdtempSync(join(tmpdir(), 'cci-cwd-'));
    try {
      const ok = spawnSync('node', [SCRIPT], { cwd, encoding: 'utf8' });
      expect(ok.status).toBe(0);

      const bad = mkdtempSync(join(tmpdir(), 'cci-bad-'));
      writeFileSync(join(bad, '.env'), `${fake.cohere}\n`);
      const r = spawnSync('node', [SCRIPT, bad], { cwd, encoding: 'utf8' });
      expect(r.status).toBe(1);
      expect(r.stderr).toContain('.env');
      expect(r.stdout + r.stderr).not.toContain(fake.cohere.split('=')[1] ?? 'x');
      rmSync(bad, { recursive: true, force: true });
    } finally {
      rmSync(cwd, { recursive: true, force: true });
    }
  });

  it('el repositorio real no contiene secretos ni .env (independiente del cwd)', () => {
    expect(scanTree()).toEqual([]);
  });
});
