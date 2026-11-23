import { describe, expect, it } from 'vitest';
import { validateActivityEvent } from './activity';
import { DISPLAY_NAME_MAX, parseLocalProfile, validateDisplayName } from './profile';
import { DEFAULT_SETTINGS, parseSettings } from './settings';

describe('perfil local', () => {
  it('el nombre es opcional: undefined, null y vacío equivalen a sin nombre', () => {
    for (const v of [undefined, null, '', '   '])
      expect(validateDisplayName(v)).toEqual({ ok: true, value: undefined });
  });
  it('recorta y normaliza espacios', () => {
    expect(validateDisplayName('  Ana   María ')).toEqual({ ok: true, value: 'Ana María' });
  });
  it('rechaza no texto, exceso de longitud y caracteres de control', () => {
    expect(validateDisplayName(5).ok).toBe(false);
    expect(validateDisplayName('x'.repeat(DISPLAY_NAME_MAX + 1)).ok).toBe(false);
    expect(validateDisplayName('x'.repeat(DISPLAY_NAME_MAX)).ok).toBe(true);
    expect(validateDisplayName('a\u0007b').ok).toBe(false);
  });
  it('conserva texto con forma de HTML sin interpretarlo (se escapa al mostrar)', () => {
    expect(validateDisplayName('<img src=x onerror=alert(1)>')).toEqual({
      ok: true,
      value: '<img src=x onerror=alert(1)>',
    });
  });
  it('parseLocalProfile ignora claves desconocidas (sin identidad, organización ni roles)', () => {
    expect(parseLocalProfile({ displayName: 'Ana', role: 'admin', organizationId: '1' })).toEqual({
      displayName: 'Ana',
    });
    expect(parseLocalProfile({ displayName: 7 })).toEqual({});
    expect(parseLocalProfile('x')).toEqual({});
  });
});

describe('configuración', () => {
  it('sin datos devuelve los valores por defecto', () => {
    expect(parseSettings(undefined)).toEqual(DEFAULT_SETTINGS);
    expect(parseSettings({})).toEqual(DEFAULT_SETTINGS);
  });
  it('acepta valores válidos y descarta claves fuera de la lista permitida', () => {
    const s = parseSettings({
      theme: 'dark',
      lastView: 'conexion',
      token: 'secreto',
      seenNotices: ['a1', 'a1', 'b-2'],
      lastBackupAt: '2026-11-22T10:00:00Z',
    });
    expect(s).toEqual({
      theme: 'dark',
      language: 'es',
      lastView: 'conexion',
      seenNotices: ['a1', 'b-2'],
      lastBackupAt: '2026-11-22T10:00:00Z',
    });
    expect(Object.keys(s)).not.toContain('token');
  });
  it('reemplaza por el default los valores inválidos', () => {
    const s = parseSettings({
      theme: 'neon',
      language: 'xx',
      lastView: 'otra',
      seenNotices: [1, '<x>', 'ok'],
      lastBackupAt: 'ayer',
    });
    expect(s).toEqual({ ...DEFAULT_SETTINGS, seenNotices: ['ok'] });
  });
  it('limita la cantidad de avisos vistos', () => {
    const many = Array.from({ length: 80 }, (_, i) => `n${i}`);
    expect(parseSettings({ seenNotices: many }).seenNotices).toHaveLength(50);
  });
});

describe('evento de actividad', () => {
  const ok = { id: 'evt_00000001', at: '2026-11-22T10:00:00.000Z', kind: 'app_opened' };
  it('acepta un evento válido', () => {
    expect(validateActivityEvent(ok)).toEqual({ ok: true, value: ok });
  });
  it('rechaza tipo no permitido, fecha inválida, id inválido y campos extra (sin contenido del usuario)', () => {
    expect(validateActivityEvent({ ...ok, kind: 'otro' }).ok).toBe(false);
    expect(validateActivityEvent({ ...ok, at: 'hoy' }).ok).toBe(false);
    expect(validateActivityEvent({ ...ok, id: 'x' }).ok).toBe(false);
    expect(validateActivityEvent({ ...ok, displayName: 'Ana' }).ok).toBe(false);
    expect(validateActivityEvent(null).ok).toBe(false);
  });
});
