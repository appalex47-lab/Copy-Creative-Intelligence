import { describe, expect, it } from 'vitest';
import { createMemoryRepositories } from '@/adapters/memory/memoryRepositories';
import { flagWords, RESOURCE_LIMITS } from '@/domain/resource';
import { fail, ok, type OcrEngine } from '@/services/contracts';
import { createResourceService } from './resourceService';

const png = (bytes = 10, type = 'image/png') =>
  new File([new Uint8Array(bytes).fill(1)], 'banner.png', { type });

function setup(
  engine?: OcrEngine,
  size: { width: number; height: number } | null = { width: 80, height: 40 },
) {
  const repos = createMemoryRepositories();
  let n = 0;
  const calls = { recognize: 0 };
  const eng: OcrEngine = engine ?? {
    recognize: () => {
      calls.recognize += 1;
      return Promise.resolve(
        ok({
          text: 'Oferta 20%',
          words: flagWords([
            { text: 'Oferta', confidence: 95 },
            { text: '20%', confidence: 40 },
          ]),
        }),
      );
    },
  };
  const service = createResourceService({
    repo: () => Promise.resolve(ok(repos.resources)),
    pieces: () => Promise.resolve(ok(repos.pieces)),
    engine: () => eng,
    readSize: () => Promise.resolve(size),
    engineName: 'test',
    writable: (run) => run(),
    now: () => new Date('2026-11-23T10:00:00.000Z'),
    newId: () => `res_test${String((n += 1)).padStart(6, '0')}`,
  });
  return { service, calls };
}

describe('resourceService', () => {
  it('agrega una imagen válida sin modificarla', async () => {
    const { service } = setup();
    const f = png();
    const r = await service.add(f);
    expect(r.ok && r.value.blob).toBe(f);
    expect(r.ok && r.value.width).toBe(80);
    const l = await service.list();
    expect(l.ok && l.value).toHaveLength(1);
  });

  it('rechaza formato, tamaño y lecturas imposibles', async () => {
    const { service } = setup();
    expect((await service.add(png(10, 'image/gif'))).ok).toBe(false);
    expect((await service.add(png(RESOURCE_LIMITS.maxBytes + 1))).ok).toBe(false);
    const bad = setup(undefined, null);
    expect((await bad.service.add(png())).ok).toBe(false);
  });

  it('el OCR guarda lo detectado y marca las palabras dudosas, sin tocar el texto validado', async () => {
    const { service, calls } = setup();
    const a = await service.add(png());
    if (!a.ok) throw new Error('add');
    const rev = await service.saveReview(a.value.id, 'Oferta 20 %');
    expect(rev.ok && rev.value.reviewedText).toBe('Oferta 20 %');
    const o = await service.runOcr(a.value.id);
    expect(calls.recognize).toBe(1);
    expect(o.ok && o.value.ocr?.words.map((w) => w.uncertain)).toEqual([false, true]);
    expect(o.ok && o.value.ocr?.text).toBe('Oferta 20%');
    expect(o.ok && o.value.reviewedText).toBe('Oferta 20 %');
  });

  it('un fallo del OCR no cambia el recurso', async () => {
    const { service } = setup({
      recognize: () => Promise.resolve(fail('unavailable', 'sin motor')),
    });
    const a = await service.add(png());
    if (!a.ok) throw new Error('add');
    const o = await service.runOcr(a.value.id);
    expect(o.ok).toBe(false);
    const l = await service.list();
    expect(l.ok && l.value[0]?.ocr).toBeUndefined();
  });

  it('un texto vacío quita la validación y uno demasiado largo se rechaza', async () => {
    const { service } = setup();
    const a = await service.add(png());
    if (!a.ok) throw new Error('add');
    await service.saveReview(a.value.id, 'algo');
    const q = await service.saveReview(a.value.id, '   ');
    expect(q.ok && q.value.reviewedText).toBeUndefined();
    expect(q.ok && q.value.reviewedAt).toBeUndefined();
    expect(
      (await service.saveReview(a.value.id, 'x'.repeat(RESOURCE_LIMITS.maxReviewedLength + 1))).ok,
    ).toBe(false);
    expect((await service.saveReview(a.value.id, 5)).ok).toBe(false);
  });

  it('elimina el recurso', async () => {
    const { service } = setup();
    const a = await service.add(png());
    if (!a.ok) throw new Error('add');
    expect((await service.remove(a.value.id)).ok).toBe(true);
    const l = await service.list();
    expect(l.ok && l.value).toHaveLength(0);
    expect((await service.runOcr(a.value.id)).ok).toBe(false);
  });
});
