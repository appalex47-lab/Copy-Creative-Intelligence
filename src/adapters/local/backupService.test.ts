import { describe, expect, it } from 'vitest';
import { createMemoryRepositories } from '@/adapters/memory/memoryRepositories';
import {
  createMemoryStorage,
  createPreferencesStore,
} from '@/adapters/localstorage/preferencesStore';
import { ok, type Result } from '@/services/contracts';
import type { Repositories } from '@/repositories/contracts';
import { createBackupService } from './backupService';

function setup(repos: Repositories = createMemoryRepositories()) {
  const preferences = createPreferencesStore(createMemoryStorage());
  const recorded: string[] = [];
  const service = createBackupService({
    repos: () => Promise.resolve(ok(repos)),
    preferences,
    record: (k) => {
      recorded.push(k);
      return Promise.resolve(ok(undefined));
    },
    now: () => new Date('2026-11-22T12:00:00.000Z'),
  });
  return { repos, preferences, recorded, service };
}
const must = <T>(r: Result<T>): T => {
  if (!r.ok) throw new Error(`falló: ${r.error.code}`);
  return r.value;
};

describe('servicio de respaldo', () => {
  it('exporta, y un archivo exportado se importa en otra instalación con los mismos datos', async () => {
    const a = setup();
    await a.repos.profile.save('Ana');
    await a.repos.activity.add({
      id: 'evt_00000001',
      at: '2026-11-22T10:00:00.000Z',
      kind: 'app_opened',
    });
    await a.repos.briefs.put({
      id: 'brf_abcdefgh1',
      createdAt: '2026-11-22T09:00:00.000Z',
      updatedAt: '2026-11-22T09:30:00.000Z',
      fields: { campaign: 'Buen Fin' },
    });
    await a.preferences.update({ theme: 'dark' });
    const exp = must(await a.service.export());
    expect(exp.fileName).toBe('cci-respaldo-20261122-120000.json');
    expect(exp.summary).toEqual({
      exportedAt: '2026-11-22T12:00:00.000Z',
      activityCount: 1,
      briefCount: 1,
      hasName: true,
    });
    expect(a.recorded).toEqual(['backup_exported']);
    expect(must(await a.preferences.get()).lastBackupAt).toBe('2026-11-22T12:00:00.000Z');

    const b = setup();
    await b.repos.briefs.put({
      id: 'brf_zzzzzzzz9',
      createdAt: '2026-01-01T00:00:00.000Z',
      updatedAt: '2026-01-01T00:00:00.000Z',
      fields: {},
    });
    await b.repos.activity.add({
      id: 'evt_99999999',
      at: '2026-01-01T00:00:00.000Z',
      kind: 'app_opened',
    });
    const restored = must(await b.service.restore(exp.text));
    expect(restored.settings.theme).toBe('dark');
    expect(must(await b.repos.profile.get())).toEqual({ displayName: 'Ana' });
    expect(must(await b.repos.activity.listRecent()).map((e) => e.id)).toEqual(['evt_00000001']);
    expect(must(await b.repos.briefs.list()).map((x) => x.id)).toEqual(['brf_abcdefgh1']);
    expect(must(await b.preferences.get()).theme).toBe('dark');
    expect(b.recorded).toEqual(['backup_imported']);
  });

  it('un archivo modificado (suma distinta) se rechaza y no cambia nada', async () => {
    const a = setup();
    await a.repos.profile.save('Ana');
    const exp = must(await a.service.export());
    const tampered = exp.text.replace('"displayName": "Ana"', '"displayName": "Eva"');
    expect(tampered).not.toBe(exp.text);
    const b = setup();
    await b.repos.profile.save('Original');
    const r = await b.service.restore(tampered);
    expect(!r.ok && r.error.code).toBe('validation_error');
    expect(!r.ok && r.error.message).toContain('dañado');
    expect(must(await b.repos.profile.get())).toEqual({ displayName: 'Original' });
    expect(b.recorded).toEqual([]);
  });

  it('inspect valida sin cambiar nada', async () => {
    const a = setup();
    const exp = must(await a.service.export());
    const b = setup();
    await b.repos.profile.save('Original');
    expect(must(await b.service.inspect(exp.text)).hasName).toBe(false);
    expect(must(await b.repos.profile.get())).toEqual({ displayName: 'Original' });
    const bad = await b.service.inspect('{}');
    expect(!bad.ok && bad.error.code).toBe('validation_error');
  });

  it('si la base falla al reemplazar, las preferencias vuelven a las anteriores', async () => {
    const a = setup();
    await a.preferences.update({ theme: 'dark' });
    const exp = must(await a.service.export());
    const base = createMemoryRepositories();
    const broken: Repositories = {
      ...base,
      backup: {
        ...base.backup,
        replaceAll: () =>
          Promise.resolve({ ok: false, error: { code: 'storage_failed', message: 'x' } }),
      },
    };
    const b = setup(broken);
    await b.preferences.update({ theme: 'light' });
    const r = await b.service.restore(exp.text);
    expect(!r.ok && r.error.code).toBe('storage_failed');
    expect(must(await b.preferences.get()).theme).toBe('light');
    expect(b.recorded).toEqual([]);
  });
});
