import { describe, expect, it } from 'vitest';
import { createMemoryRepositories } from '@/adapters/memory/memoryRepositories';
import { ok, type Result } from '@/services/contracts';
import { createAuditService } from './auditService';
import { createCopyService } from './copyService';

async function setup(channel: string | null = 'Email') {
  const repos = createMemoryRepositories();
  let tick = 0;
  let n = 0;
  const writable = <T>(run: () => Promise<Result<T>>) => run();
  const now = () => new Date(Date.UTC(2026, 10, 23, 10, 0, tick++));
  const at = '2026-11-23T09:00:00.000Z';
  await repos.briefs.put({
    id: 'brf_test0001',
    createdAt: at,
    updatedAt: at,
    fields: { campaign: 'Buen Fin', ...(channel ? { channel } : {}), offer: '20% de descuento' },
  });
  const copies = createCopyService({
    copies: () => Promise.resolve(ok(repos.copies)),
    briefs: () => Promise.resolve(ok(repos.briefs)),
    audits: () => Promise.resolve(ok(repos.audits)),
    writable,
    now,
    newId: () => 'cpy_test0001',
  });
  const audits = createAuditService({
    repo: () => Promise.resolve(ok(repos.audits)),
    copies: () => Promise.resolve(ok(repos.copies)),
    briefs: () => Promise.resolve(ok(repos.briefs)),
    rules: () => Promise.resolve(ok(repos.rules)),
    writable,
    now,
    newId: () => `aud_test000${++n}`,
  });
  return { repos, copies, audits };
}
const must = <T>(r: Result<T>): T => {
  if (!r.ok) throw new Error(`falló: ${r.error.code} ${r.error.message}`);
  return r.value;
};

describe('servicio de auditorías (S3.1)', () => {
  it('audita el copy vigente con las reglas actuales y guarda la foto', async () => {
    const { copies, audits } = await setup();
    const c = must(
      await copies.create({
        briefId: 'brf_test0001',
        label: 'Principal',
        content: { headline: 'Una cura para todo con 20% de descuento', cta: 'Compra ahora' },
      }),
    );
    const a = must(await audits.create({ copyId: c.id }));
    expect(a.sourceVersion).toBe(1);
    expect(a.channel).toBe('Email');
    expect(a.targetLabel).toBe('Principal');
    expect(a.rules).toEqual({ isTemplate: true, legends: 0, brandTerms: 7 });
    expect(a.findings.some((f) => f.ruleId.startsWith('marca'))).toBe(true);
    expect(must(await audits.list(c.id))).toHaveLength(1);
  });

  it('la auditoría es una foto: no cambia si el copy cambia después', async () => {
    const { copies, audits } = await setup();
    const c = must(
      await copies.create({
        briefId: 'brf_test0001',
        label: 'Principal',
        content: { headline: 'Hola', cta: 'Compra' },
      }),
    );
    const a1 = must(await audits.create({ copyId: c.id }));
    must(
      await copies.saveVersion({
        id: c.id,
        content: { headline: 'Una cura única', cta: 'Compra' },
      }),
    );
    const a2 = must(await audits.create({ copyId: c.id }));
    expect(a2.sourceVersion).toBe(2);
    const stored = must(await audits.list(c.id));
    expect(stored.find((x) => x.id === a1.id)).toEqual(a1);
    expect(stored).toHaveLength(2);
    expect(a2.score).toBeLessThanOrEqual(a1.score);
  });

  it('exige canal en el brief y copy existente', async () => {
    const s = await setup(null);
    const c = must(
      await s.copies.create({ briefId: 'brf_test0001', label: 'P', content: { headline: 'Hola' } }),
    );
    const r = await s.audits.create({ copyId: c.id });
    expect(!r.ok && r.error.message).toContain('canal');
    const nf = await s.audits.create({ copyId: 'cpy_noexiste1' });
    expect(!nf.ok && nf.error.code).toBe('not_found');
  });

  it('un copy con auditorías no se borra; al eliminarlas sí', async () => {
    const { copies, audits } = await setup();
    const c = must(
      await copies.create({
        briefId: 'brf_test0001',
        label: 'P',
        content: { headline: 'Hola', cta: 'x' },
      }),
    );
    const a = must(await audits.create({ copyId: c.id }));
    const del = await copies.remove(c.id);
    expect(!del.ok && del.error.code).toBe('conflict');
    must(await audits.remove(a.id));
    must(await copies.remove(c.id));
  });
});
