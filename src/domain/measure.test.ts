import { describe, expect, it } from 'vitest';
import {
  analyzeExperiment,
  ctr,
  parseResultsCsv,
  validateFigures,
  validateMeasureRecord,
  type ExperimentRecord,
} from './measure';

const exp = (
  a: [number, number, number],
  b: [number, number, number],
  primary: 'ctr' | 'conversion' = 'ctr',
): ExperimentRecord => ({
  kind: 'experimento',
  id: 'mea_abcdefgh1234',
  name: 'Titular',
  hypothesis: 'Beneficio gana',
  variable: 'titular',
  primary,
  variants: [
    { label: 'A', impressions: a[0], clicks: a[1], conversions: a[2] },
    { label: 'B', impressions: b[0], clicks: b[1], conversions: b[2] },
  ],
  createdAt: '2026-11-24T10:00:00.000Z',
  updatedAt: '2026-11-24T10:00:00.000Z',
});

describe('figuras', () => {
  it('exige coherencia', () => {
    expect(validateFigures({ impressions: 10, clicks: 11, conversions: 0 }).ok).toBe(false);
    expect(validateFigures({ impressions: 10, clicks: 5, conversions: 6 }).ok).toBe(false);
    expect(validateFigures({ impressions: 10, clicks: 5, conversions: 1.5 }).ok).toBe(false);
    expect(ctr({ impressions: 200, clicks: 10, conversions: 1 })).toBeCloseTo(0.05);
    expect(ctr({ impressions: 0, clicks: 0, conversions: 0 })).toBeNull();
  });
});

describe('experimento A/B', () => {
  it('muestra pequeña: no concluye', () => {
    const r = analyzeExperiment(exp([50, 5, 1], [50, 10, 2]));
    expect(r.smallSample).toBe(true);
    expect(r.winner).toBeNull();
  });
  it('diferencia grande con muestra suficiente: declara ganador', () => {
    const r = analyzeExperiment(exp([10000, 200, 10], [10000, 320, 20]));
    expect(r.winner).toBe('B');
    expect(r.p).toBeLessThan(0.05);
    expect(r.lift).toBeCloseTo(0.6);
  });
  it('diferencia pequeña: sin ganador', () => {
    const r = analyzeExperiment(exp([10000, 200, 10], [10000, 205, 10]));
    expect(r.winner).toBeNull();
    expect(r.message).toContain('Sin diferencia significativa');
  });
  it('conversión se mide sobre clics', () => {
    const r = analyzeExperiment(exp([1000, 500, 10], [1000, 500, 60], 'conversion'));
    expect(r.rateA).toBeCloseTo(0.02);
    expect(r.winner).toBe('B');
  });
  it('sin datos', () => {
    expect(analyzeExperiment(exp([0, 0, 0], [0, 0, 0])).winner).toBeNull();
  });
});

describe('registros', () => {
  it('valida resultado y experimento', () => {
    expect(
      validateMeasureRecord({
        kind: 'resultado',
        id: 'mea_abcdefgh1234',
        label: 'Pieza',
        impressions: 100,
        clicks: 5,
        conversions: 1,
        createdAt: '2026-11-24T10:00:00.000Z',
      }).ok,
    ).toBe(true);
    expect(validateMeasureRecord(exp([10, 1, 0], [10, 1, 0])).ok).toBe(true);
    expect(validateMeasureRecord({ ...exp([10, 1, 0], [10, 1, 0]), secondary: 'ctr' }).ok).toBe(
      false,
    );
    expect(validateMeasureRecord({ kind: 'otro' }).ok).toBe(false);
  });
});

describe('importación CSV', () => {
  it('lee filas, comillas, BOM y punto y coma', () => {
    const r = parseResultsCsv(
      '﻿objetivo;impresiones;clics;conversiones;ventas\n"Promo, email";1000;50;5;1200.5\n',
    );
    expect(r.ok && r.value[0]).toMatchObject({
      label: 'Promo, email',
      impressions: 1000,
      sales: 1200.5,
    });
  });
  it('todo o nada con el número de fila', () => {
    const r = parseResultsCsv('objetivo,impresiones,clics,conversiones\nA,100,5,1\nB,100,500,1\n');
    expect(r.ok).toBe(false);
    expect(!r.ok && r.reason).toContain('Fila 3');
  });
  it('rechaza columnas faltantes y vacío', () => {
    expect(parseResultsCsv('objetivo,impresiones\nA,1').ok).toBe(false);
    expect(parseResultsCsv('objetivo,impresiones,clics,conversiones\n').ok).toBe(false);
  });
});
