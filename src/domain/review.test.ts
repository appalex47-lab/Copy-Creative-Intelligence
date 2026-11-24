import { describe, expect, it } from 'vitest';
import {
  DIMENSIONS,
  emptyReviewBody,
  summarizeReview,
  validateReviewBody,
  validateReviewRecord,
  type ReviewInput,
  type ReviewRecord,
} from './review';

const full = (n: number): Record<string, number> =>
  Object.fromEntries(DIMENSIONS.map((d) => [d.id, Math.min(d.max, n)]));
const rec = (over: Partial<ReviewInput> = {}): ReviewRecord => {
  const b = validateReviewBody({ ...emptyReviewBody(), ...over });
  if (!b.ok) throw new Error(b.reason);
  return {
    id: 'rev_abcdefgh1234',
    targetType: 'copy',
    targetId: 'cpy_abcdefgh',
    targetLabel: 'Principal',
    ...b.value,
    createdAt: '2026-11-23T10:00:00.000Z',
    updatedAt: '2026-11-23T10:00:00.000Z',
  };
};

describe('matriz', () => {
  it('suma 100 puntos', () => {
    expect(DIMENSIONS.reduce((a, d) => a + d.max, 0)).toBe(100);
  });
});

describe('summarizeReview', () => {
  it('incompleta = pendiente, sin aprobación definitiva', () => {
    const s = summarizeReview(rec({ scores: { claridad: 15 } }));
    expect(s.verdict).toBe('pendiente');
    expect(s.score).toBeNull();
    expect(s.publishable).toBe(false);
  });
  it('bandas y veredictos', () => {
    expect(summarizeReview(rec({ scores: full(100) })).verdict).toBe('aprobado');
    const mid = { ...full(100), claridad: 5, titular: 5 }; // 100-10-10=80
    const s80 = summarizeReview(rec({ scores: mid }));
    expect(s80.score).toBe(80);
    expect(s80.verdict).toBe('aprobado_con_ajustes');
    const low = { ...full(100), claridad: 0, titular: 0, beneficio: 5 }; // 100-15-15-10=60
    const s60 = summarizeReview(rec({ scores: low }));
    expect(s60.verdict).toBe('rechazado');
    expect(s60.band).toBe('Requiere replanteamiento');
  });
  it('un hallazgo bloqueante rechaza aunque el puntaje sea 100', () => {
    const f = {
      hallazgo: 'Descuento incorrecto',
      impacto: 'Publicidad engañosa',
      recomendacion: 'Corregir a 20 %',
      bloqueante: true,
    };
    const s = summarizeReview(rec({ scores: full(100), findings: [f] }));
    expect(s.verdict).toBe('rechazado');
    expect(s.blocking).toBe(1);
    expect(s.publishable).toBe(false);
  });
  it('solo es publicable con APROBADO y los dos filtros aprobados', () => {
    const ok = rec({
      scores: full(100),
      commercial: [true, true, true, true, true, true],
      creativeFilter: 'aprobado',
      commercialFilter: 'aprobado',
    });
    expect(summarizeReview(ok).publishable).toBe(true);
    const half = rec({ scores: full(100), creativeFilter: 'aprobado' });
    const s = summarizeReview(half);
    expect(s.publishable).toBe(false);
    expect(s.reasons.join(' ')).toContain('comercial');
  });
});

describe('validateReviewBody', () => {
  it('rechaza puntajes fuera de rango', () => {
    expect(validateReviewBody({ ...emptyReviewBody(), scores: { cta: 11 } }).ok).toBe(false);
    expect(validateReviewBody({ ...emptyReviewBody(), scores: { cta: -1 } }).ok).toBe(false);
  });
  it('no deja aprobar filtros sin sustento', () => {
    expect(validateReviewBody({ ...emptyReviewBody(), creativeFilter: 'aprobado' }).ok).toBe(false);
    expect(validateReviewBody({ ...emptyReviewBody(), commercialFilter: 'aprobado' }).ok).toBe(
      false,
    );
    const f = { hallazgo: 'a', impacto: 'b', recomendacion: 'c', bloqueante: true };
    expect(
      validateReviewBody({
        ...emptyReviewBody(),
        scores: full(100),
        findings: [f],
        creativeFilter: 'aprobado',
      }).ok,
    ).toBe(false);
  });
  it('exige los 3 elementos de cada hallazgo', () => {
    expect(
      validateReviewBody({
        ...emptyReviewBody(),
        findings: [{ hallazgo: 'a', impacto: '', recomendacion: 'c', bloqueante: false }],
      }).ok,
    ).toBe(false);
  });
  it('round-trip de un registro', () => {
    expect(validateReviewRecord(rec({ scores: full(90) })).ok).toBe(true);
    expect(validateReviewRecord({ id: 'x' }).ok).toBe(false);
  });
});
