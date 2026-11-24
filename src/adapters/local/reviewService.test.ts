import { describe, expect, it } from 'vitest';
import { createMemoryRepositories } from '@/adapters/memory/memoryRepositories';
import { emptyReviewBody } from '@/domain/review';
import { ok } from '@/services/contracts';
import { createReviewService } from './reviewService';

function setup() {
  const repos = createMemoryRepositories();
  let n = 0;
  const service = createReviewService({
    repo: () => Promise.resolve(ok(repos.reviews)),
    copies: () => Promise.resolve(ok(repos.copies)),
    pieces: () => Promise.resolve(ok(repos.pieces)),
    writable: (run) => run(),
    now: () => new Date(`2026-11-23T10:00:0${String(n)}.000Z`),
    newId: () => `rev_test${String((n += 1)).padStart(6, '0')}`,
  });
  return { service, repos };
}

describe('reviewService', () => {
  it('rechaza un objetivo que no existe', async () => {
    const { service } = setup();
    const r = await service.save({
      targetType: 'copy',
      targetId: 'cpy_noexiste',
      body: emptyReviewBody(),
    });
    expect(r.ok).toBe(false);
  });

  it('crea y luego actualiza la misma revisión de una pieza', async () => {
    const { service, repos } = setup();
    await repos.pieces.put({
      id: 'pie_abcdefgh1234',
      name: 'Promo',
      channel: 'Email',
      resourceId: 'res_abcdefgh1234',
      createdAt: '2026-11-23T10:00:00.000Z',
      updatedAt: '2026-11-23T10:00:00.000Z',
      audits: [],
    });
    const a = await service.save({
      targetType: 'pieza',
      targetId: 'pie_abcdefgh1234',
      body: emptyReviewBody(),
    });
    const b = await service.save({
      targetType: 'pieza',
      targetId: 'pie_abcdefgh1234',
      body: { ...emptyReviewBody(), scores: { cta: 7 } },
    });
    expect(a.ok && b.ok && a.value.id === b.value.id).toBe(true);
    expect(b.ok && b.value.scores.cta).toBe(7);
    const l = await service.list();
    expect(l.ok && l.value).toHaveLength(1);
  });

  it('no guarda un contenido inválido', async () => {
    const { service, repos } = setup();
    await repos.pieces.put({
      id: 'pie_abcdefgh1234',
      name: 'Promo',
      channel: 'Email',
      resourceId: 'res_abcdefgh1234',
      createdAt: '2026-11-23T10:00:00.000Z',
      updatedAt: '2026-11-23T10:00:00.000Z',
      audits: [],
    });
    const r = await service.save({
      targetType: 'pieza',
      targetId: 'pie_abcdefgh1234',
      body: { ...emptyReviewBody(), scores: { cta: 99 } },
    });
    expect(r.ok).toBe(false);
  });
});
