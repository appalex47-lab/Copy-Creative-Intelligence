import { describe, expect, it } from 'vitest';
import { compareBriefsNewestFirst, evaluateRecord, validateBriefRecord } from './briefRecord';

const base = {
  id: 'brf_abcdefgh1',
  createdAt: '2026-11-23T10:00:00.000Z',
  updatedAt: '2026-11-23T10:00:00.000Z',
  fields: { campaign: 'Buen Fin' },
};

describe('briefRecord (S2.2)', () => {
  it('acepta un borrador incompleto y lo reporta incompleto al leerlo', () => {
    const v = validateBriefRecord(base);
    expect(v.ok).toBe(true);
    if (v.ok) {
      expect(evaluateRecord(v.value).status).toBe('incompleto');
      expect(v.value.fields).toEqual({ campaign: 'Buen Fin' });
    }
  });

  it('rechaza id, fechas, orden de fechas y claves desconocidas', () => {
    expect(validateBriefRecord({ ...base, id: 'x' }).ok).toBe(false);
    expect(validateBriefRecord({ ...base, createdAt: '2026-11-23' }).ok).toBe(false);
    expect(validateBriefRecord({ ...base, updatedAt: '2026-11-22T10:00:00.000Z' }).ok).toBe(false);
    expect(validateBriefRecord({ ...base, extra: 1 }).ok).toBe(false);
    expect(validateBriefRecord({ ...base, fields: { campaign: 'x', foo: 'y' } }).ok).toBe(false);
    for (const x of [null, 5, 'x', [], undefined]) expect(validateBriefRecord(x).ok).toBe(false);
    expect(validateBriefRecord({ ...base, fields: 'x' }).ok).toBe(false);
  });

  it('un campo inválido no se guarda; uno vacío se descarta', () => {
    expect(validateBriefRecord({ ...base, fields: { channel: 'Llamadas' } }).ok).toBe(false);
    expect(validateBriefRecord({ ...base, fields: { campaign: 'a'.repeat(121) } }).ok).toBe(false);
    const v = validateBriefRecord({ ...base, fields: { campaign: 'A', tone: '   ' } });
    expect(v.ok && v.value.fields).toEqual({ campaign: 'A' });
  });

  it('acepta los valores vacíos que envía el formulario (texto vacío, vigencia vacía)', () => {
    const v = validateBriefRecord({
      ...base,
      fields: { campaign: 'A', objective: '', channel: '', validity: { from: '', to: '' } },
    });
    expect(v.ok && v.value.fields).toEqual({ campaign: 'A' });
  });

  it('ordena por actualización descendente y desempata por id', () => {
    const a = { ...base, id: 'brf_aaaaaaaa1', fields: {} };
    const b = { ...base, id: 'brf_bbbbbbbb1', fields: {}, updatedAt: '2026-11-24T10:00:00.000Z' };
    const c = { ...base, id: 'brf_cccccccc1', fields: {} };
    expect([a, b, c].sort(compareBriefsNewestFirst).map((r) => r.id)).toEqual([
      'brf_bbbbbbbb1',
      'brf_cccccccc1',
      'brf_aaaaaaaa1',
    ]);
  });
});
