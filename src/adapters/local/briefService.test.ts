import { describe, expect, it } from 'vitest';
import { createMemoryRepositories } from '@/adapters/memory/memoryRepositories';
import { fail, ok, type Result } from '@/services/contracts';
import { createBriefService } from './briefService';

function setup(opts: { writable?: boolean } = {}) {
  const repos = createMemoryRepositories();
  let tick = 0;
  let n = 0;
  const service = createBriefService({
    repo: () => Promise.resolve(ok(repos.briefs)),
    writable: (run) =>
      opts.writable === false ? Promise.resolve(fail('storage_read_only', 'solo lectura')) : run(),
    now: () => new Date(Date.UTC(2026, 10, 23, 10, 0, tick++)),
    newId: () => `brf_test000${++n}`,
  });
  return { repos, service };
}
const must = <T>(r: Result<T>): T => {
  if (!r.ok) throw new Error(`falló: ${r.error.code}`);
  return r.value;
};

describe('servicio de briefs (S2.3)', () => {
  it('crea con id y fechas del servicio, y un borrador incompleto es válido', async () => {
    const { service } = setup();
    const r = must(await service.save({ fields: { campaign: 'Buen Fin' } }));
    expect(r.id).toBe('brf_test0001');
    expect(r.createdAt).toBe(r.updatedAt);
    expect(r.fields).toEqual({ campaign: 'Buen Fin' });
    expect(must(await service.list())).toHaveLength(1);
  });

  it('actualizar conserva createdAt y avanza updatedAt; el más reciente va primero', async () => {
    const { service } = setup();
    const a = must(await service.save({ fields: { campaign: 'A' } }));
    const b = must(await service.save({ fields: { campaign: 'B' } }));
    const a2 = must(await service.save({ id: a.id, fields: { campaign: 'A2' } }));
    expect(a2.createdAt).toBe(a.createdAt);
    expect(a2.updatedAt > a.updatedAt).toBe(true);
    expect(must(await service.list()).map((x) => x.id)).toEqual([a.id, b.id]);
  });

  it('un id desconocido no crea nada; un campo inválido no se guarda', async () => {
    const { service } = setup();
    const unknown = await service.save({ id: 'brf_noexiste1', fields: { campaign: 'x' } });
    expect(!unknown.ok && unknown.error.code).toBe('validation_error');
    const bad = await service.save({ fields: { channel: 'Llamadas' } });
    expect(!bad.ok && bad.error.code).toBe('validation_error');
    expect(must(await service.list())).toEqual([]);
  });

  it('borrar quita el brief; en solo lectura no escribe nada', async () => {
    const { service } = setup();
    const a = must(await service.save({ fields: { campaign: 'A' } }));
    must(await service.remove(a.id));
    expect(must(await service.list())).toEqual([]);
    const ro = setup({ writable: false });
    const w = await ro.service.save({ fields: { campaign: 'A' } });
    expect(!w.ok && w.error.code).toBe('storage_read_only');
    const d = await ro.service.remove('brf_test0001');
    expect(!d.ok && d.error.code).toBe('storage_read_only');
    expect(must(await ro.service.list())).toEqual([]);
  });
});
