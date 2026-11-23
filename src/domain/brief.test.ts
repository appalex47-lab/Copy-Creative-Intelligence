import { describe, expect, it } from 'vitest';
import {
  BRIEF_LONG_MAX,
  BRIEF_SHORT_MAX,
  CHANNELS,
  REQUIRED_FIELDS,
  evaluateBrief,
  validateChannel,
  validateValidity,
} from './brief';

const COMPLETE = {
  campaign: 'Buen Fin',
  objective: 'Aumentar conversión',
  product: 'Vitamina C',
  audience: 'Clientes recurrentes',
  message: 'Cuida tu salud con descuento',
  channel: 'Email',
  cta: 'Compra ahora',
};

describe('brief (AC2-01, AC2-02)', () => {
  it('un brief con los obligatorios es completo', () => {
    const e = evaluateBrief(COMPLETE);
    expect(e.status).toBe('completo');
    expect(e.missing).toEqual([]);
    expect(e.invalid).toEqual([]);
  });

  it('cada obligatorio ausente se señala con su motivo y nada se rellena', () => {
    for (const f of REQUIRED_FIELDS) {
      const { [f]: _omit, ...rest } = COMPLETE as Record<string, string>;
      void _omit;
      const e = evaluateBrief(rest);
      expect(e.status).toBe('incompleto');
      expect(e.missing.map((m) => m.field)).toEqual([f]);
      expect(e.missing[0]?.reason).toMatch(/obligatorio/);
      expect(e.brief[f]).toBeUndefined();
    }
  });

  it('entrada vacía o no objeto: incompleto con todos los obligatorios faltantes', () => {
    for (const x of [undefined, null, 5, 'x', [], {}]) {
      const e = evaluateBrief(x);
      expect(e.status).toBe('incompleto');
      expect(e.missing.map((m) => m.field)).toEqual([...REQUIRED_FIELDS]);
    }
  });

  it('solo espacios cuenta como vacío', () => {
    const e = evaluateBrief({ ...COMPLETE, cta: '   ' });
    expect(e.missing.map((m) => m.field)).toEqual(['cta']);
  });

  it('los opcionales no bloquean y se conservan limpios', () => {
    const e = evaluateBrief({ ...COMPLETE, tone: '  cercano   y claro ', offer: 'x' });
    expect(e.status).toBe('completo');
    expect(e.brief['tone']).toBe('cercano y claro');
    expect(e.brief['offer']).toBe('x');
  });

  it('límites de longitud: frontera exacta y exceso', () => {
    expect(evaluateBrief({ ...COMPLETE, campaign: 'a'.repeat(BRIEF_SHORT_MAX) }).status).toBe(
      'completo',
    );
    const over = evaluateBrief({ ...COMPLETE, campaign: 'a'.repeat(BRIEF_SHORT_MAX + 1) });
    expect(over.status).toBe('incompleto');
    expect(over.invalid.map((i) => i.field)).toEqual(['campaign']);
    expect(evaluateBrief({ ...COMPLETE, message: 'a'.repeat(BRIEF_LONG_MAX) }).status).toBe(
      'completo',
    );
    expect(evaluateBrief({ ...COMPLETE, message: 'a'.repeat(BRIEF_LONG_MAX + 1) }).status).toBe(
      'incompleto',
    );
  });

  it('rechaza tipos incorrectos, saltos de línea en campos cortos y caracteres de control', () => {
    expect(evaluateBrief({ ...COMPLETE, product: 5 }).invalid[0]?.field).toBe('product');
    expect(evaluateBrief({ ...COMPLETE, product: 'a\nb' }).invalid[0]?.field).toBe('product');
    expect(evaluateBrief({ ...COMPLETE, cta: 'a\u0000b' }).invalid[0]?.field).toBe('cta');
    expect(evaluateBrief({ ...COMPLETE, message: 'línea 1\nlínea 2' }).status).toBe('completo');
  });

  it('un campo inválido no se reporta además como faltante', () => {
    const e = evaluateBrief({ ...COMPLETE, cta: 7 });
    expect(e.missing).toEqual([]);
    expect(e.invalid.map((i) => i.field)).toEqual(['cta']);
  });

  it('canal: solo los 7 aprobados; Llamadas no entra', () => {
    for (const c of CHANNELS) expect(validateChannel(c).ok).toBe(true);
    expect(validateChannel('Llamadas').ok).toBe(false);
    expect(validateChannel('email').ok).toBe(false);
    expect(evaluateBrief({ ...COMPLETE, channel: 'Llamadas' }).invalid[0]?.field).toBe('channel');
  });

  it('vigencia: fechas reales, orden y vacío', () => {
    expect(validateValidity(undefined)).toEqual({ ok: true, value: undefined });
    expect(validateValidity({})).toEqual({ ok: true, value: undefined });
    expect(validateValidity({ from: '2026-11-01', to: '2026-11-30' }).ok).toBe(true);
    expect(validateValidity({ from: '2026-11-01', to: '2026-11-01' }).ok).toBe(true);
    expect(validateValidity({ from: '2026-11-30', to: '2026-11-01' }).ok).toBe(false);
    expect(validateValidity({ from: '2026-02-30' }).ok).toBe(false);
    expect(validateValidity({ from: '2026-13-01' }).ok).toBe(false);
    expect(validateValidity({ from: '01/11/2026' }).ok).toBe(false);
    expect(validateValidity({ to: '2024-02-29' }).ok).toBe(true);
    expect(validateValidity({ to: '2026-02-29' }).ok).toBe(false);
    expect(validateValidity('x').ok).toBe(false);
  });

  it('es determinista y no muta la entrada', () => {
    const input = Object.freeze({ ...COMPLETE });
    expect(evaluateBrief(input)).toEqual(evaluateBrief(input));
  });
});
