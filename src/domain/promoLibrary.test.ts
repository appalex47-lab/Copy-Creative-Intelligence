import { describe, expect, it } from 'vitest';
import { draftAll, draftFor, type FormulaInput } from './copyFormulas';
import { buildLibrary } from './library';
import {
  checkTextAgainstPromo,
  parsePromosCsv,
  validatePromoRecord,
  type PromoRecord,
} from './promo';

const promo = (over: Partial<PromoRecord> = {}): PromoRecord => ({
  id: 'prm_abcdefgh1234',
  name: 'Buen Fin',
  discountPct: 20,
  skus: ['A1'],
  from: '2026-11-01',
  to: '2026-11-30',
  createdAt: '2026-11-01T00:00:00.000Z',
  ...over,
});

describe('checkTextAgainstPromo', () => {
  it('porcentaje distinto y vencida son críticos', () => {
    const r = checkTextAgainstPromo('Aprovecha 30% de descuento', promo(), '2026-12-02');
    expect(r.map((x) => x.severity)).toEqual(['critica', 'critica']);
  });
  it('coincide dentro de la tolerancia y vigente', () => {
    expect(checkTextAgainstPromo('20% de descuento', promo(), '2026-11-15')).toEqual([]);
  });
  it('sin porcentaje en el texto y restricciones sin comunicar', () => {
    const r = checkTextAgainstPromo(
      'Compra hoy',
      promo({ restrictions: 'Solo en línea' }),
      '2026-11-15',
    );
    expect(r.map((x) => x.severity).sort()).toEqual(['mayor', 'menor']);
  });
  it('no define porcentaje pero el texto sí', () => {
    expect(
      checkTextAgainstPromo('15%', promo({ discountPct: undefined } as never), '2026-11-15'),
    ).toHaveLength(1);
  });
});

describe('promos CSV', () => {
  it('une filas del mismo nombre y junta SKUs', () => {
    const r = parsePromosCsv(
      'nombre,porcentaje,sku,desde,hasta\nBuen Fin,20%,A1,2026-11-01,2026-11-30\nBuen Fin,,B2,,\n',
    );
    expect(r.ok && r.value).toHaveLength(1);
    expect(r.ok && r.value[0]).toMatchObject({ discountPct: 20, skus: ['A1', 'B2'] });
  });
  it('rechaza fechas y porcentajes inválidos con fila', () => {
    const r = parsePromosCsv('nombre,porcentaje\nA,200\n');
    expect(!r.ok && r.reason).toContain('Fila 2');
    expect(validatePromoRecord({ ...promo(), from: '2026-12-01' }).ok).toBe(false);
  });
});

describe('plantillas', () => {
  const full: FormulaInput = {
    product: 'productos participantes',
    need: 'Buscas ahorrar en tu salud',
    benefit: 'Encuentra lo que necesitas a mejor precio',
    offer: '20% de descuento',
    differentiator: '',
    cta: 'Compra ahora',
    validity: '',
    conditions: '',
  };
  it('no inventa: sin vigencia no hay urgencia', () => {
    const f = draftAll(full).map((d) => d.formula);
    expect(f).not.toContain('Urgencia');
    expect(f).toContain('AIDA');
    expect(
      draftFor('Urgencia', { ...full, validity: 'hasta el 30 de noviembre' })?.headline,
    ).toContain('Últimos días');
  });
  it('solo usa lo escrito', () => {
    const d = draftFor('Oferta + beneficio + CTA', full);
    expect(d?.headline).toBe('20% de descuento en productos participantes');
    expect(d?.cta).toBe('Compra ahora');
    expect(draftFor('PAS', { ...full, need: '' })).toBeNull();
  });
});

describe('biblioteca', () => {
  it('vacía no falla', () => {
    const l = buildLibrary({ reviews: [], copyAudits: [], pieces: [], measures: [] });
    expect(l).toMatchObject({ approved: [], rejected: [], recurring: [], best: [] });
  });
});

import { isReviewDue } from './reminder';
describe('recordatorio', () => {
  const now = new Date('2026-11-24T12:00:00Z');
  it('sin registros o viejo: toca; reciente: no', () => {
    expect(isReviewDue([], now)).toBe(true);
    expect(isReviewDue(['2026-11-10T00:00:00Z'], now)).toBe(true);
    expect(isReviewDue(['2026-11-20T00:00:00Z', '2026-11-01T00:00:00Z'], now)).toBe(false);
  });
});
