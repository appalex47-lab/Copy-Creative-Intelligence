import { describe, expect, it } from 'vitest';
import {
  CATEGORY_WEIGHTS,
  DEFAULT_CONFIG,
  containsTerm,
  evaluateCopy,
  extractPercents,
  type Legend,
  type RulesConfig,
} from './copyRules';

const email = { channel: 'Email' as const, offer: '20% de descuento' };
const clean = {
  headline: 'Tu salud con descuento',
  description: 'Ofertas de vitaminas',
  cta: 'Compra ahora',
};

describe('pesos Q-5', () => {
  it('suman 100', () => {
    expect(Object.values(CATEGORY_WEIGHTS).reduce((a, b) => a + b, 0)).toBe(100);
  });
});

describe('containsTerm', () => {
  it('ignora mayúsculas y acentos y exige palabra completa', () => {
    expect(containsTerm('Es una CURA total', 'cura')).toBe(true);
    expect(containsTerm('Adelgaza RÁPIDO hoy', 'adelgaza rapido')).toBe(true);
    expect(containsTerm('Procura descansar', 'cura')).toBe(false);
    expect(containsTerm('Es 100% efectivo.', '100% efectivo')).toBe(true);
    expect(containsTerm('algo', '')).toBe(false);
  });
});

describe('extractPercents', () => {
  it('lee varios formatos', () => {
    expect(extractPercents('20% y 12,5 % y 7.25%')).toEqual([20, 12.5, 7.25]);
    expect(extractPercents('sin porcentaje')).toEqual([]);
  });
});

describe('evaluateCopy', () => {
  it('copy limpio: 100 y apto', () => {
    const r = evaluateCopy(email, clean);
    expect(r).toMatchObject({ score: 100, verdict: 'apto', blocked: false, findings: [] });
  });

  it('excede longitud del canal (Email asunto ≤ 60) y falta CTA obligatorio', () => {
    const r = evaluateCopy(email, { headline: 'x'.repeat(61) });
    expect(r.findings.map((f) => f.ruleId).sort()).toEqual([
      'canal.longitud.headline',
      'claridad.cta',
    ]);
    expect(r.score).toBe(100 - 10 - 15);
  });

  it('CTA recomendado en redes: solo aviso, no resta', () => {
    const r = evaluateCopy({ channel: 'Redes sociales' }, { body: 'Hola' });
    expect(r.findings).toHaveLength(1);
    expect(r.findings[0]?.severity).toBe('aviso');
    expect(r.score).toBe(100);
  });

  it('término prohibido crítico bloquea y limita a 59', () => {
    const r = evaluateCopy(email, { ...clean, description: 'Sin efectos secundarios' });
    expect(r.blocked).toBe(true);
    expect(r.score).toBe(59);
    expect(r.verdict).toBe('no_apto');
  });

  it('término mayor resta el peso de marca; menor, la mitad', () => {
    expect(evaluateCopy(email, { ...clean, description: 'Una cura' }).score).toBe(85);
    expect(evaluateCopy(email, { ...clean, description: 'El mejor precio' }).score).toBe(92.5);
  });

  it('leyenda obligatoria ausente es crítica; presente, no; inactiva o de otro canal, se ignora', () => {
    const legend: Legend = {
      text: 'Consulta a tu médico',
      channels: ['Email'] as Legend['channels'],
      required: true,
      active: true,
    };
    const cfg = (l: Partial<typeof legend>): RulesConfig => ({
      ...DEFAULT_CONFIG,
      legends: [{ ...legend, ...l }],
    });
    expect(evaluateCopy(email, clean, cfg({})).findings[0]?.ruleId).toBe('cumplimiento.leyenda');
    expect(
      evaluateCopy(email, { ...clean, description: 'consulta a tu MÉDICO' }, cfg({})).findings,
    ).toEqual([]);
    expect(evaluateCopy(email, clean, cfg({ active: false })).findings).toEqual([]);
    expect(evaluateCopy(email, clean, cfg({ channels: ['App'] })).findings).toEqual([]);
    expect(evaluateCopy(email, clean, cfg({ channels: [] })).findings).toHaveLength(1);
  });

  it('porcentajes: dentro de tolerancia pasa; fuera es crítica; sin respaldo es mayor', () => {
    expect(evaluateCopy(email, { ...clean, headline: '20% de descuento' }).findings).toEqual([]);
    expect(evaluateCopy(email, { ...clean, headline: '20.4% menos' }).findings).toEqual([]);
    const bad = evaluateCopy(email, { ...clean, headline: '25% menos' });
    expect(bad.findings[0]?.ruleId).toBe('precios.porcentaje_distinto');
    expect(bad.blocked).toBe(true);
    const none = evaluateCopy({ channel: 'Email' }, { ...clean, headline: '25% menos' });
    expect(none.findings[0]?.ruleId).toBe('precios.porcentaje_sin_respaldo');
    expect(none.score).toBe(75);
  });

  it('redacción: espacios dobles, signos repetidos y titular en mayúsculas', () => {
    const r = evaluateCopy(email, { ...clean, headline: 'OFERTA ESPECIAL!!', description: 'a  b' });
    expect(r.findings.map((f) => f.ruleId).sort()).toEqual([
      'redaccion.espacios',
      'redaccion.mayusculas',
      'redaccion.signos_repetidos',
    ]);
    expect(r.deductions.redaccion).toBe(10); // tope por categoría
  });

  it('es determinista', () => {
    const c = { ...clean, description: 'Una cura!!' };
    expect(evaluateCopy(email, c)).toEqual(evaluateCopy(email, c));
  });
});
