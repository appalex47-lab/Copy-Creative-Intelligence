import { describe, expect, it } from 'vitest';
import {
  compareAuditsNewestFirst,
  diffAudits,
  previousOf,
  validateAuditRecord,
  type AuditRecord,
} from './audit';

const base: AuditRecord = {
  id: 'aud_aaaaaaaa1',
  copyId: 'cpy_aaaaaaaa1',
  sourceVersion: 1,
  targetLabel: 'Principal',
  channel: 'Email',
  score: 75,
  verdict: 'revisar',
  blocked: false,
  findings: [
    { ruleId: 'marca.cura', category: 'marca', severity: 'mayor', message: 'Término «cura»' },
    { ruleId: 'claridad.cta', category: 'claridad', severity: 'mayor', message: 'Falta CTA' },
  ],
  rules: { isTemplate: true, legends: 0, brandTerms: 7 },
  createdAt: '2026-11-23T10:00:00.000Z',
};
const mk = (over: Partial<AuditRecord>): AuditRecord => ({ ...base, ...over });

describe('auditoría guardada (dominio)', () => {
  it('acepta un registro válido y lo devuelve igual', () => {
    const r = validateAuditRecord(base);
    expect(r.ok && r.value).toEqual(base);
  });
  it('acepta evidencia y campo opcionales en los hallazgos', () => {
    const r = validateAuditRecord({
      ...base,
      findings: [{ ...base.findings[0], evidence: 'cura', field: 'headline' }],
    });
    expect(r.ok).toBe(true);
  });
  it('rechaza claves desconocidas, puntajes fuera de rango y datos mal formados', () => {
    expect(validateAuditRecord({ ...base, extra: 1 }).ok).toBe(false);
    expect(validateAuditRecord({ ...base, score: 101 }).ok).toBe(false);
    expect(validateAuditRecord({ ...base, score: 50.5 }).ok).toBe(false);
    expect(validateAuditRecord({ ...base, verdict: 'ok' }).ok).toBe(false);
    expect(validateAuditRecord({ ...base, channel: 'Llamadas' }).ok).toBe(false);
    expect(validateAuditRecord({ ...base, sourceVersion: 0 }).ok).toBe(false);
    expect(validateAuditRecord({ ...base, createdAt: 'ayer' }).ok).toBe(false);
    expect(validateAuditRecord({ ...base, findings: [{ ruleId: 'x' }] }).ok).toBe(false);
    expect(validateAuditRecord({ ...base, findings: Array(101).fill(base.findings[0]) }).ok).toBe(
      false,
    );
    expect(
      validateAuditRecord({ ...base, rules: { isTemplate: 'si', legends: 0, brandTerms: 0 } }).ok,
    ).toBe(false);
    expect(validateAuditRecord(null).ok).toBe(false);
  });
  it('compara con la anterior: puntaje, hallazgos nuevos y resueltos', () => {
    const next = mk({
      id: 'aud_aaaaaaaa2',
      score: 90,
      createdAt: '2026-11-23T11:00:00.000Z',
      findings: [
        ...base.findings.slice(0, 1),
        {
          ruleId: 'canal.longitud.headline',
          category: 'canal',
          severity: 'mayor',
          message: 'Largo',
        },
      ],
    });
    const d = diffAudits(base, next);
    expect(d.scoreDelta).toBe(15);
    expect(d.added.map((f) => f.ruleId)).toEqual(['canal.longitud.headline']);
    expect(d.resolved.map((f) => f.ruleId)).toEqual(['claridad.cta']);
  });
  it('previousOf busca la anterior del mismo copy, no de otro', () => {
    const other = mk({
      id: 'aud_aaaaaaaa2',
      copyId: 'cpy_bbbbbbbb1',
      createdAt: '2026-11-23T10:30:00.000Z',
    });
    const c2 = mk({ id: 'aud_aaaaaaaa4', createdAt: '2026-11-23T13:00:00.000Z' });
    const list = [c2, other, base].sort(compareAuditsNewestFirst);
    expect(list[0]?.id).toBe('aud_aaaaaaaa4');
    expect(previousOf(list, c2)?.id).toBe(base.id);
    expect(previousOf(list, base)).toBeUndefined();
    expect(previousOf(list, other)).toBeUndefined();
  });
});
