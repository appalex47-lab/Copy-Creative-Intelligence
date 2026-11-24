import { describe, expect, it } from 'vitest';
import { createMemoryRepositories } from '@/adapters/memory/memoryRepositories';
import { fail, ok, type Result } from '@/services/contracts';
import { createBriefService } from './briefService';
import { createEntityService } from './entityService';

function setup(opts: { writable?: boolean } = {}) {
  const repos = createMemoryRepositories();
  let tick = 0;
  let n = 0;
  const writable = <T>(run: () => Promise<Result<T>>) =>
    opts.writable === false ? Promise.resolve(fail<T>('storage_read_only', 'ro')) : run();
  const now = () => new Date(Date.UTC(2026, 10, 23, 10, 0, tick++));
  const entities = createEntityService({
    repo: () => Promise.resolve(ok(repos.entities)),
    briefs: () => Promise.resolve(ok(repos.briefs)),
    writable,
    now,
    newSuffix: () => `test${String(++n).padStart(6, '0')}`,
  });
  const briefs = createBriefService({
    repo: () => Promise.resolve(ok(repos.briefs)),
    copies: () => Promise.resolve(ok(repos.copies)),
    entities: () => Promise.resolve(ok(repos.entities)),
    writable,
    now,
    newId: () => 'brf_test0001',
  });
  return { repos, entities, briefs };
}
const must = <T>(r: Result<T>): T => {
  if (!r.ok) throw new Error(`falló: ${r.error.code} ${r.error.message}`);
  return r.value;
};

describe('servicio de catálogo (S2.8)', () => {
  it('crea, lista por tipo, edita y borra', async () => {
    const { entities } = setup();
    const c = must(
      await entities.create({ kind: 'campaign', name: '  Buen   Fin ', note: 'nota' }),
    );
    expect(c.id.startsWith('cmp_')).toBe(true);
    expect(c.name).toBe('Buen Fin');
    must(await entities.create({ kind: 'product', name: 'Paracetamol' }));
    expect(must(await entities.list('campaign'))).toHaveLength(1);
    expect(must(await entities.list())).toHaveLength(2);
    const u = must(await entities.update({ id: c.id, name: 'Buen Fin 2026' }));
    expect(u.name).toBe('Buen Fin 2026');
    expect(u.note).toBeUndefined();
    expect(u.createdAt).toBe(c.createdAt);
    must(await entities.remove(c.id));
    expect(must(await entities.list('campaign'))).toHaveLength(0);
  });

  it('el nombre es único por tipo (sin mayúsculas ni acentos) y puede repetirse entre tipos', async () => {
    const { entities } = setup();
    must(await entities.create({ kind: 'offer', name: 'Envío gratis' }));
    const dup = await entities.create({ kind: 'offer', name: 'ENVIO GRATIS' });
    expect(!dup.ok && dup.error.code).toBe('validation_error');
    must(await entities.create({ kind: 'product', name: 'Envío gratis' }));
    const b = must(await entities.create({ kind: 'offer', name: 'Otra' }));
    const clash = await entities.update({ id: b.id, name: 'envío gratis' });
    expect(clash.ok).toBe(false);
    must(await entities.update({ id: b.id, name: 'Otra', note: 'misma' })); // se puede guardar con su propio nombre
  });

  it('rechaza nombre vacío, largo, nota larga y tipo inválido', async () => {
    const { entities } = setup();
    expect((await entities.create({ kind: 'campaign', name: '   ' })).ok).toBe(false);
    expect((await entities.create({ kind: 'campaign', name: 'x'.repeat(121) })).ok).toBe(false);
    expect(
      (await entities.create({ kind: 'campaign', name: 'ok', note: 'x'.repeat(501) })).ok,
    ).toBe(false);
    expect((await entities.create({ kind: 'otro' as never, name: 'ok' })).ok).toBe(false);
  });

  it('en solo lectura no escribe', async () => {
    const { entities } = setup({ writable: false });
    const r = await entities.create({ kind: 'campaign', name: 'A' });
    expect(!r.ok && r.error.code).toBe('storage_read_only');
  });

  it('un brief puede referenciar una campaña; borrarla se rechaza hasta quitar la referencia', async () => {
    const { entities, briefs } = setup();
    const c = must(await entities.create({ kind: 'campaign', name: 'Buen Fin' }));
    const b = must(await briefs.save({ fields: { campaign: 'Buen Fin' }, campaignId: c.id }));
    expect(b.campaignId).toBe(c.id);
    const del = await entities.remove(c.id);
    expect(!del.ok && del.error.code).toBe('conflict');
    const b2 = must(
      await briefs.save({ id: b.id, fields: { campaign: 'Buen Fin' }, campaignId: null }),
    );
    expect(b2.campaignId).toBeUndefined();
    must(await entities.remove(c.id));
  });

  it('un brief no puede referenciar una campaña inexistente ni un producto', async () => {
    const { entities, briefs } = setup();
    const bad = await briefs.save({ fields: {}, campaignId: 'cmp_noexiste1' });
    expect(bad.ok).toBe(false);
    const p = must(await entities.create({ kind: 'product', name: 'P' }));
    expect((await briefs.save({ fields: {}, campaignId: p.id })).ok).toBe(false);
  });
});
