import { describe, expect, it } from 'vitest';
import { parseEnv } from './env';
import { DEMO_ALLOWED_ENVS, evaluateEnvPolicy } from './envPolicy';

const code = (raw: Record<string, string | undefined>) => {
  const r = parseEnv(raw);
  return r.ok ? 'ok' : r.error.code;
};

describe('política de entorno y modo de datos', () => {
  it.each(['development', 'test', 'preview'] as const)('%s: DEMO permitido', (mode) => {
    expect(parseEnv({ MODE: mode })).toEqual({
      ok: true,
      value: { appEnv: mode, dataMode: 'demo' },
    });
    expect(parseEnv({ MODE: mode, VITE_APP_ENV: mode, VITE_DATA_MODE: 'demo' }).ok).toBe(true);
  });

  it('producción rechaza DEMO (explícito e implícito) con mensaje claro', () => {
    for (const raw of [{ MODE: 'production' }, { MODE: 'production', VITE_DATA_MODE: 'demo' }]) {
      const r = parseEnv(raw);
      expect(r.ok).toBe(false);
      expect(!r.ok && r.error.code).toBe('invalid_configuration');
      expect(!r.ok && r.error.message).toContain('producción no puede usar datos DEMO');
    }
  });

  it('producción con supabase: aún no implementado (no se acepta)', () => {
    expect(code({ MODE: 'production', VITE_DATA_MODE: 'supabase' })).toBe('not_implemented');
  });

  it('supabase en cualquier entorno: no implementado', () => {
    for (const m of ['development', 'test', 'preview']) {
      expect(code({ MODE: m, VITE_DATA_MODE: 'supabase' })).toBe('not_implemented');
    }
  });

  it('configuración contradictoria: VITE_APP_ENV distinto del modo', () => {
    for (const [mode, declared] of [
      ['production', 'development'],
      ['development', 'production'],
      ['preview', 'production'],
      ['test', 'preview'],
    ] as const) {
      const r = parseEnv({ MODE: mode, VITE_APP_ENV: declared });
      expect(r.ok).toBe(false);
      expect(!r.ok && r.error.message).toContain('contradictoria');
    }
  });

  it('variables ausentes o inválidas se rechazan', () => {
    expect(code({})).toBe('invalid_configuration'); // MODE ausente
    expect(code({ MODE: '' })).toBe('invalid_configuration');
    expect(code({ MODE: 'staging' })).toBe('invalid_configuration');
    expect(code({ MODE: 'development', VITE_APP_ENV: 'staging' })).toBe('invalid_configuration');
    expect(code({ MODE: 'development', VITE_DATA_MODE: 'otro' })).toBe('invalid_configuration');
  });

  it('VITE_APP_ENV y VITE_DATA_MODE vacíos equivalen a no definidos', () => {
    expect(parseEnv({ MODE: 'development', VITE_APP_ENV: '', VITE_DATA_MODE: '' }).ok).toBe(true);
  });

  it('preview no tiene conexión a backend: el único modo de datos posible es demo', () => {
    const p = evaluateEnvPolicy({ MODE: 'preview' });
    expect(p).toEqual({ ok: true, appEnv: 'preview', dataMode: 'demo' });
    expect(DEMO_ALLOWED_ENVS).not.toContain('production');
  });
});
