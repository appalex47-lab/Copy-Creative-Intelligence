import { describe, expect, it } from 'vitest';
import { createMemoryRepositories } from '@/adapters/memory/memoryRepositories';
import { fail, ok, type Result } from '@/services/contracts';
import { createBriefService } from './briefService';
import { createCopyService } from './copyService';

async function setup(opts: { writable?: boolean } = {}) {
  const repos = createMemoryRepositories();
  let tick = 0;
  let n = 0;
  const writable = <T>(run: () => Promise<Result<T>>) =>
    opts.writable === false ? Promise.resolve(fail<T>('storage_read_only', 'ro')) : run();
  const now = () => new Date(Date.UTC(2026, 10, 23, 10, 0, tick++));
  const copies = createCopyService({
    copies: () => Promise.resolve(ok(repos.copies)),
    briefs: () => Promise.resolve(ok(repos.briefs)),
    writable,
    now,
    newId: () => `cpy_test000${++n}`,
  });
  const briefs = createBriefService({
    repo: () => Promise.resolve(ok(repos.briefs)),
    copies: () => Promise.resolve(ok(repos.copies)),
    writable,
    now,
    newId: () => 'brf_test0001',
  });
  const at = '2026-11-23T09:00:00.000Z';
  const b = await repos.briefs.put({
    id: 'brf_test0001',
    createdAt: at,
    updatedAt: at,
    fields: { campaign: 'Buen Fin' },
  });
  if (!b.ok) throw new Error('brief');
  return { repos, copies, briefs, briefId: b.value.id };
}
const must = <T>(r: Result<T>): T => {
  if (!r.ok) throw new Error(`falló: ${r.error.code}`);
  return r.value;
};

describe('servicio de copys (S2.4)', () => {
  it('crea un copy con versión 1; el brief debe existir', async () => {
    const { copies, briefId } = await setup();
    const c = must(
      await copies.create({ briefId, label: 'Principal', content: { headline: 'Hola' } }),
    );
    expect(c.versions).toHaveLength(1);
    expect(c.versions[0]?.content).toEqual({ headline: 'Hola' });
    const orphan = await copies.create({
      briefId: 'brf_noexiste1',
      label: 'X',
      content: { headline: 'x' },
    });
    expect(!orphan.ok && orphan.error.code).toBe('not_found');
    const bad = await copies.create({ briefId, label: 'X', content: {} });
    expect(!bad.ok && bad.error.code).toBe('validation_error');
    expect(must(await copies.list(briefId))).toHaveLength(1);
  });

  it('guardar AÑADE versiones; las anteriores no cambian; sin cambios no guarda', async () => {
    const { copies, briefId } = await setup();
    const c = must(await copies.create({ briefId, label: 'P', content: { headline: 'Uno' } }));
    const v2 = must(await copies.saveVersion({ id: c.id, content: { headline: 'Dos' } }));
    expect(v2.versions.map((v) => v.n)).toEqual([1, 2]);
    expect(v2.versions[0]).toEqual(c.versions[0]);
    const same = await copies.saveVersion({ id: c.id, content: { headline: 'Dos' } });
    expect(!same.ok && same.error.code).toBe('validation_error');
    expect(must(await copies.get(c.id)).versions).toHaveLength(2);
  });

  it('recuperar una versión crea una nueva con restoredFrom; versión inexistente se rechaza', async () => {
    const { copies, briefId } = await setup();
    const c = must(await copies.create({ briefId, label: 'P', content: { headline: 'Uno' } }));
    must(await copies.saveVersion({ id: c.id, content: { headline: 'Dos' } }));
    const r = must(await copies.restoreVersion({ id: c.id, version: 1 }));
    expect(r.versions.map((v) => v.n)).toEqual([1, 2, 3]);
    expect(r.versions[2]).toMatchObject({ content: { headline: 'Uno' }, restoredFrom: 1 });
    const none = await copies.restoreVersion({ id: c.id, version: 9 });
    expect(!none.ok && none.error.code).toBe('validation_error');
    const current = await copies.restoreVersion({ id: c.id, version: 3 });
    expect(current.ok).toBe(false); // recuperar la versión vigente no cambia nada: se rechaza
  });

  it('metadatos y variantes dentro del copy, sin versiones propias', async () => {
    const { copies, briefId } = await setup();
    const c = must(
      await copies.create({ briefId, label: 'P', content: { headline: 'Uno', cta: 'Ya' } }),
    );
    const m = must(
      await copies.updateMeta({ id: c.id, label: 'Principal', tags: ['Promo', 'promo'] }),
    );
    expect(m).toMatchObject({ label: 'Principal', tags: ['Promo'] });
    expect(m.versions).toHaveLength(1);
    const a = must(
      await copies.addVariant({ id: c.id, label: 'B', content: { headline: 'Otro' } }),
    );
    expect(a.versions).toHaveLength(1); // agregar variante no crea versión
    expect(a.variants).toHaveLength(1);
    const variantId = a.variants?.[0]?.id ?? '';
    const u = must(
      await copies.updateVariant({ id: c.id, variantId, label: 'B', content: { headline: 'Más' } }),
    );
    expect(u.variants?.[0]?.content).toEqual({ headline: 'Más' });
    expect(u.versions).toHaveLength(1); // editar una variante tampoco
    const same = await copies.updateVariant({
      id: c.id,
      variantId,
      label: 'B',
      content: { headline: 'Más' },
    });
    expect(same.ok).toBe(false);
    const dup = await copies.addVariant({ id: c.id, label: 'b', content: { cta: 'x' } });
    expect(dup.ok).toBe(false);
    must(await copies.saveVersion({ id: c.id, content: { headline: 'Solo versión' } }));
    expect(must(await copies.get(c.id)).variants).toHaveLength(1); // las variantes sobreviven a las versiones
    const r = must(await copies.removeVariant({ id: c.id, variantId }));
    expect(r.variants).toBeUndefined();
  });

  it('borrar un brief con copys se rechaza (conflict); sin copys se borra', async () => {
    const { copies, briefs, briefId } = await setup();
    const c = must(await copies.create({ briefId, label: 'P', content: { headline: 'Uno' } }));
    const r = await briefs.remove(briefId);
    expect(!r.ok && r.error.code).toBe('conflict');
    expect(must(await briefs.list())).toHaveLength(1);
    must(await copies.remove(c.id));
    must(await briefs.remove(briefId));
    expect(must(await briefs.list())).toEqual([]);
  });

  it('en solo lectura no escribe nada', async () => {
    const ro = await setup({ writable: false });
    const w = await ro.copies.create({
      briefId: ro.briefId,
      label: 'P',
      content: { headline: 'x' },
    });
    expect(!w.ok && w.error.code).toBe('storage_read_only');
  });
});
