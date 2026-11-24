import { describe, expect, it } from 'vitest';
import type { AuditRecord } from './audit';
import { filterAudits, localDay } from './auditFilter';

const mk = (id: string, over: Partial<AuditRecord>): AuditRecord => ({
  id: `aud_${id}0000000`,
  copyId: 'cpy_aaaaaaaa1',
  sourceVersion: 1,
  targetLabel: 'Principal',
  channel: 'Email',
  score: 90,
  verdict: 'apto',
  blocked: false,
  findings: [],
  rules: { isTemplate: true, legends: 0, brandTerms: 7 },
  createdAt: '2026-11-23T18:00:00.000Z',
  ...over,
});
const a = mk('a', {});
const b = mk('b', {
  verdict: 'no_apto',
  channel: 'WhatsApp',
  targetLabel: 'Promo Vitaminas',
  createdAt: '2026-11-10T18:00:00.000Z',
  findings: [
    { ruleId: 'marca.cura', category: 'marca', severity: 'mayor', message: 'Término «cura»' },
  ],
});
const all = [a, b];

describe('filtros de auditorías', () => {
  it('sin filtros devuelve todo', () => {
    expect(filterAudits(all, {})).toEqual(all);
  });
  it('por veredicto y canal', () => {
    expect(filterAudits(all, { verdict: 'no_apto' })).toEqual([b]);
    expect(filterAudits(all, { channel: 'Email' })).toEqual([a]);
    expect(filterAudits(all, { channel: 'Email', verdict: 'no_apto' })).toEqual([]);
  });
  it('por rango de fechas locales, ambos extremos inclusive', () => {
    const d = localDay(b.createdAt);
    expect(filterAudits(all, { from: d, to: d })).toEqual([b]);
    expect(filterAudits(all, { from: localDay(a.createdAt) })).toEqual([a]);
    expect(filterAudits(all, { to: '2026-11-01' })).toEqual([]);
  });
  it('por texto en nombre u hallazgos, sin acentos ni mayúsculas', () => {
    expect(filterAudits(all, { query: 'VITAMINAS' })).toEqual([b]);
    expect(filterAudits(all, { query: 'termino cura' })).toEqual([b]);
    expect(filterAudits(all, { query: 'nada' })).toEqual([]);
  });
});
