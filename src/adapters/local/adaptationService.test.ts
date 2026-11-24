import { describe, expect, it } from 'vitest';
import { createMemoryRepositories } from '@/adapters/memory/memoryRepositories';
import { ok, type Result } from '@/services/contracts';
import { createAdaptationService } from './adaptationService';
import { createCopyService } from './copyService';

async function setup() {
  const repos = createMemoryRepositories();
  let tick = 0;
  let n = 0;
  const writable = <T>(run: () => Promise<Result<T>>) => run();
  const now = () => new Date(Date.UTC(2026, 10, 23, 10, 0, tick++));
  const at = '2026-11-23T09:00:00.000Z';
  await repos.briefs.put({ id: 'brf_test0001', createdAt: at, updatedAt: at, fields: {} });
  const copies = createCopyService({
    copies: () => Promise.resolve(ok(repos.copies)),
    briefs: () => Promise.resolve(ok(repos.briefs)),
    adaptations: () => Promise.resolve(ok(repos.adaptations)),
    writable,
    now,
    newId: () => 'cpy_test0001',
  });
  const adaptations = createAdaptationService({
    repo: () => Promise.resolve(ok(repos.adaptations)),
    copies: () => Promise.resolve(ok(repos.copies)),
    writable,
    now,
    newId: () => `ada_test000${++n}`,
  });
  const copy = must(
    await copies.create({
      briefId: 'brf_test0001',
      label: 'Principal',
      content: { headline: 'Hola' },
    }),
  );
  return { repos, copies, adaptations, copy };
}
const must = <T>(r: Result<T>): T => {
  if (!r.ok) throw new Error(`falló: ${r.error.code} ${r.error.message}`);
  return r.value;
};

describe('servicio de adaptaciones (S2.8)', () => {
  it('crea desde un copy con la versión actual, lista por copy, edita y borra', async () => {
    const { copies, adaptations, copy } = await setup();
    const v2 = must(await copies.saveVersion({ id: copy.id, content: { headline: 'Hola 2' } }));
    const a = must(
      await adaptations.create({
        copyId: v2.id,
        channel: 'WhatsApp',
        content: { headline: 'Hola 2' },
      }),
    );
    expect(a.sourceVersion).toBe(2);
    expect(a.channel).toBe('WhatsApp');
    expect(must(await adaptations.list(v2.id))).toHaveLength(1);
    const u = must(await adaptations.update({ id: a.id, content: { headline: 'Ajustado' } }));
    expect(u.content).toEqual({ headline: 'Ajustado' });
    expect(u.channel).toBe('WhatsApp');
    expect(u.sourceVersion).toBe(2);
    must(await adaptations.remove(a.id));
    expect(must(await adaptations.list())).toHaveLength(0);
  });

  it('admite una versión de origen anterior y rechaza una inexistente', async () => {
    const { copies, adaptations, copy } = await setup();
    must(await copies.saveVersion({ id: copy.id, content: { headline: 'Hola 2' } }));
    const a = must(
      await adaptations.create({
        copyId: copy.id,
        channel: 'Email',
        content: { headline: 'x' },
        sourceVersion: 1,
      }),
    );
    expect(a.sourceVersion).toBe(1);
    const bad = await adaptations.create({
      copyId: copy.id,
      channel: 'Email',
      content: { headline: 'x' },
      sourceVersion: 9,
    });
    expect(bad.ok).toBe(false);
  });

  it('rechaza canal no aprobado (Llamadas), contenido vacío y copy inexistente', async () => {
    const { adaptations, copy } = await setup();
    expect(
      (
        await adaptations.create({
          copyId: copy.id,
          channel: 'Llamadas',
          content: { headline: 'x' },
        })
      ).ok,
    ).toBe(false);
    expect((await adaptations.create({ copyId: copy.id, channel: 'Email', content: {} })).ok).toBe(
      false,
    );
    const nf = await adaptations.create({
      copyId: 'cpy_noexiste1',
      channel: 'Email',
      content: { headline: 'x' },
    });
    expect(!nf.ok && nf.error.code).toBe('not_found');
  });

  it('un copy con adaptaciones no se borra; sin ellas sí', async () => {
    const { copies, adaptations, copy } = await setup();
    const a = must(
      await adaptations.create({ copyId: copy.id, channel: 'App', content: { headline: 'x' } }),
    );
    const del = await copies.remove(copy.id);
    expect(!del.ok && del.error.code).toBe('conflict');
    must(await adaptations.remove(a.id));
    must(await copies.remove(copy.id));
  });
});
