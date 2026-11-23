import { describe, expect, it } from 'vitest';
import { DEFAULT_SETTINGS } from '@/domain/settings';
import { PREFS_KEY, createMemoryStorage, createPreferencesStore } from './preferencesStore';

describe('preferencias en Local Storage', () => {
  it('sin datos devuelve los valores por defecto', async () => {
    expect(await createPreferencesStore(createMemoryStorage()).get()).toEqual({
      ok: true,
      value: DEFAULT_SETTINGS,
    });
  });
  it('guarda un cambio válido, lo conserva entre instancias y fusiona cambios parciales', async () => {
    const storage = createMemoryStorage();
    await createPreferencesStore(storage).update({ theme: 'dark' });
    const r = await createPreferencesStore(storage).update({ lastView: 'ajustes' });
    expect(r).toEqual({
      ok: true,
      value: { ...DEFAULT_SETTINGS, theme: 'dark', lastView: 'ajustes' },
    });
    expect(await createPreferencesStore(storage).get()).toEqual(r);
  });
  it('rechaza claves no permitidas y valores inválidos sin escribir', async () => {
    const storage = createMemoryStorage();
    const s = createPreferencesStore(storage);
    for (const bad of [{ token: 'x' }, { theme: 'neon' }, null]) {
      const r = await s.update(bad);
      expect(!r.ok && r.error.code).toBe('validation_error');
    }
    expect(storage.getItem(PREFS_KEY)).toBeNull();
  });
  it('lo guardado se lee de forma tolerante: JSON corrupto, claves extra y valores inválidos', async () => {
    const storage = createMemoryStorage();
    storage.setItem(PREFS_KEY, '{no es json');
    expect(await createPreferencesStore(storage).get()).toEqual({
      ok: true,
      value: DEFAULT_SETTINGS,
    });
    storage.setItem(
      PREFS_KEY,
      JSON.stringify({ theme: 'light', token: 'secreto', language: 'xx' }),
    );
    expect(await createPreferencesStore(storage).get()).toEqual({
      ok: true,
      value: { ...DEFAULT_SETTINGS, theme: 'light' },
    });
  });
  it('reset borra lo guardado', async () => {
    const storage = createMemoryStorage();
    const s = createPreferencesStore(storage);
    await s.update({ theme: 'dark' });
    expect(await s.reset()).toEqual({ ok: true, value: DEFAULT_SETTINGS });
    expect(storage.getItem(PREFS_KEY)).toBeNull();
  });
  it('un almacenamiento que falla devuelve un código del catálogo sin detalle', async () => {
    const boom = (name: string) => () => {
      throw new DOMException('detalle interno', name);
    };
    const broken = {
      getItem: boom('SecurityError'),
      setItem: boom('SecurityError'),
      removeItem: boom('SecurityError'),
    };
    const s = createPreferencesStore(broken);
    for (const r of [await s.get(), await s.update({ theme: 'dark' }), await s.reset()]) {
      expect(!r.ok && r.error.code).toBe('storage_unavailable');
      expect(JSON.stringify(r)).not.toContain('interno');
    }
  });
  it('un fallo al escribir (cuota) se informa y no cambia lo leído', async () => {
    const storage = createMemoryStorage();
    const s = createPreferencesStore({
      ...storage,
      setItem: () => {
        throw new DOMException('x', 'QuotaExceededError');
      },
    });
    const r = await s.update({ theme: 'dark' });
    expect(!r.ok && r.error.code).toBe('storage_quota_exceeded');
    expect(await s.get()).toEqual({ ok: true, value: DEFAULT_SETTINGS });
  });
});
