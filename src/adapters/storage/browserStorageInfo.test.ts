import { describe, expect, it } from 'vitest';
import { createStorageInfoService } from './browserStorageInfo';

describe('createStorageInfoService', () => {
  it('sin navegador compatible: todo null (no se inventa nada)', async () => {
    expect(await createStorageInfoService(undefined).get()).toEqual({
      ok: true,
      value: { usageBytes: null, quotaBytes: null, persisted: null },
    });
    expect(await createStorageInfoService({}).get()).toEqual({
      ok: true,
      value: { usageBytes: null, quotaBytes: null, persisted: null },
    });
  });
  it('lee uso, cuota y persistencia', async () => {
    const s = createStorageInfoService({
      estimate: () => Promise.resolve({ usage: 2048, quota: 1_000_000 }),
      persisted: () => Promise.resolve(false),
    });
    expect(await s.get()).toEqual({
      ok: true,
      value: { usageBytes: 2048, quotaBytes: 1_000_000, persisted: false },
    });
  });
  it('solicitar persistencia vuelve a leer el estado', async () => {
    let p = false;
    const s = createStorageInfoService({
      persisted: () => Promise.resolve(p),
      persist: () => {
        p = true;
        return Promise.resolve(true);
      },
    });
    const r = await s.requestPersistence();
    expect(r.ok && r.value.persisted).toBe(true);
  });
  it('un fallo del navegador devuelve un código del catálogo sin detalle', async () => {
    const s = createStorageInfoService({
      estimate: () => Promise.reject(new DOMException('interno', 'SecurityError')),
    });
    const r = await s.get();
    expect(!r.ok && r.error.code).toBe('storage_unavailable');
    expect(JSON.stringify(r)).not.toContain('interno');
  });
});
