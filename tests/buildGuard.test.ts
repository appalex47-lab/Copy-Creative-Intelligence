import { spawnSync } from 'node:child_process';
import { mkdtempSync, readdirSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { describe, expect, it } from 'vitest';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const VITE = join(ROOT, 'node_modules', '.bin', 'vite');

function build(mode: string, extraEnv: Record<string, string> = {}) {
  const out = mkdtempSync(join(tmpdir(), 'cci-build-'));
  const env = Object.fromEntries(
    Object.entries(process.env).filter(([k]) => !k.startsWith('VITE_') && k !== 'MODE'),
  );
  const r = spawnSync(VITE, ['build', '--mode', mode, '--outDir', out, '--emptyOutDir'], {
    cwd: ROOT,
    env: { ...env, ...extraEnv },
    encoding: 'utf8',
  });
  const files = (() => {
    try {
      return readdirSync(out);
    } catch {
      return [];
    }
  })();
  rmSync(out, { recursive: true, force: true });
  return { status: r.status, output: `${r.stdout}${r.stderr}`, files };
}

describe('guarda de entorno en el build (integración con Vite)', () => {
  it('build de preview (DEMO) funciona y genera salida', { timeout: 120_000 }, () => {
    const r = build('preview');
    expect(r.status).toBe(0);
    expect(r.files).toContain('index.html');
  });

  it(
    'build de producción con DEMO (implícito) FALLA con mensaje claro y sin salida',
    { timeout: 120_000 },
    () => {
      const r = build('production');
      expect(r.status).not.toBe(0);
      expect(r.output).toContain('Configuración de entorno rechazada (production)');
      expect(r.output).toContain('producción no puede usar datos DEMO');
      expect(r.files).toEqual([]);
    },
  );

  it('build de producción con DEMO explícito FALLA', { timeout: 120_000 }, () => {
    const r = build('production', { VITE_DATA_MODE: 'demo' });
    expect(r.status).not.toBe(0);
    expect(r.output).toContain('producción no puede usar datos DEMO');
  });

  it('configuración contradictoria FALLA', { timeout: 120_000 }, () => {
    const r = build('production', { VITE_APP_ENV: 'development' });
    expect(r.status).not.toBe(0);
    expect(r.output).toContain('contradictoria');
  });

  it('VITE_DATA_MODE=supabase FALLA (adaptador no implementado)', { timeout: 120_000 }, () => {
    const r = build('preview', { VITE_DATA_MODE: 'supabase' });
    expect(r.status).not.toBe(0);
    expect(r.output).toContain('no existe todavía');
  });

  it('modo desconocido FALLA', { timeout: 120_000 }, () => {
    const r = build('staging');
    expect(r.status).not.toBe(0);
    expect(r.output).toContain('Modo de ejecución inválido');
  });
});
