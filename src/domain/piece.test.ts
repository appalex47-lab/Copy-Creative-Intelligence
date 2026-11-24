import { describe, expect, it } from 'vitest';
import { DEFAULT_CONFIG } from './copyRules';
import {
  diffPieceAudits,
  evaluatePiece,
  validatePieceInput,
  validatePieceRecord,
  withFindingStatus,
  type PieceRecord,
} from './piece';
import { flagWords, type ResourceRecord } from './resource';

const res = (over: Partial<ResourceRecord> = {}): ResourceRecord => ({
  id: 'res_abcdefgh1234',
  name: 'b.png',
  mime: 'image/png',
  size: 10,
  width: 1200,
  height: 400,
  createdAt: '2026-11-23T10:00:00.000Z',
  blob: new Blob(['x']),
  ...over,
});
const ocr = (text: string, conf = 95) => ({
  engine: 't',
  langs: 'spa+eng',
  threshold: 60,
  ranAt: '2026-11-23T10:05:00.000Z',
  text,
  words: flagWords(text.split(' ').map((t) => ({ text: t, confidence: conf }))),
});

describe('validatePieceInput', () => {
  it('exige nombre y canal', () => {
    expect(validatePieceInput({ name: ' ', channel: 'Email' }).ok).toBe(false);
    expect(validatePieceInput({ name: 'A', channel: 'Radio' }).ok).toBe(false);
    expect(validatePieceInput({ name: ' A ', channel: 'Email' })).toEqual({
      ok: true,
      value: { name: 'A', channel: 'Email' },
    });
  });
});

describe('evaluatePiece', () => {
  it('sin texto no se puede auditar', () => {
    expect(evaluatePiece('Email', res(), DEFAULT_CONFIG).ok).toBe(false);
  });
  it('con texto solo detectado avisa y marca dudosas; no exige CTA', () => {
    const r = evaluatePiece('Email', res({ ocr: ocr('Ofer1a hoy', 40) }), DEFAULT_CONFIG);
    if (!r.ok) throw new Error('x');
    expect(r.value.textSource).toBe('detectado');
    const ids = r.value.findings.map((f) => f.ruleId);
    expect(ids).toContain('ocr.sin_validar');
    expect(ids).toContain('ocr.palabras_dudosas');
    expect(ids).not.toContain('claridad.cta');
    expect(r.value.findings.find((f) => f.ruleId === 'ocr.palabras_dudosas')?.severity).toBe(
      'mayor',
    );
  });
  it('con texto validado no marca OCR y baja baja resolución', () => {
    const r = evaluatePiece(
      'Email',
      res({
        width: 300,
        reviewedText: 'Cuida tu salud',
        reviewedAt: '2026-11-23T11:00:00.000Z',
        ocr: ocr('x', 10),
      }),
      DEFAULT_CONFIG,
    );
    if (!r.ok) throw new Error('x');
    expect(r.value.textSource).toBe('validado');
    const ids = r.value.findings.map((f) => f.ruleId);
    expect(ids).toContain('visual.resolucion');
    expect(ids.some((i) => i.startsWith('ocr.'))).toBe(false);
  });
  it('un término de marca prohibido bloquea el puntaje', () => {
    const r = evaluatePiece(
      'Email',
      res({ reviewedText: 'Una cura milagrosa', reviewedAt: '2026-11-23T11:00:00.000Z' }),
      { ...DEFAULT_CONFIG, brandTerms: [{ text: 'cura', kind: 'prohibido', severity: 'critica' }] },
    );
    if (!r.ok) throw new Error('x');
    expect(r.value.score).toBeLessThanOrEqual(59);
  });
});

describe('estado de hallazgos y comparación', () => {
  const piece = (): PieceRecord => {
    const r = evaluatePiece('Email', res({ ocr: ocr('Hola mundo') }), DEFAULT_CONFIG);
    if (!r.ok) throw new Error('x');
    return {
      id: 'pie_abcdefgh1234',
      name: 'P',
      channel: 'Email',
      resourceId: 'res_abcdefgh1234',
      createdAt: '2026-11-23T10:00:00.000Z',
      updatedAt: '2026-11-23T10:00:00.000Z',
      audits: [{ ...r.value, id: 'pau_abcdefgh1234', createdAt: '2026-11-23T10:10:00.000Z' }],
    };
  };
  it('cambia el estado con nota y fecha; valida índices y longitud', () => {
    const p = piece();
    const r = withFindingStatus(
      p,
      'pau_abcdefgh1234',
      0,
      'resuelto',
      ' ya ',
      '2026-11-23T12:00:00.000Z',
    );
    if (!r.ok) throw new Error('x');
    expect(r.value.audits[0]?.findings[0]).toMatchObject({
      status: 'resuelto',
      note: 'ya',
      resolvedAt: '2026-11-23T12:00:00.000Z',
    });
    expect(validatePieceRecord(r.value).ok).toBe(true);
    expect(withFindingStatus(p, 'pau_abcdefgh1234', 99, 'resuelto', '', 'x').ok).toBe(false);
    expect(withFindingStatus(p, 'pau_abcdefgh1234', 0, 'resuelto', 'n'.repeat(301), 'x').ok).toBe(
      false,
    );
    const back = withFindingStatus(
      r.value,
      'pau_abcdefgh1234',
      0,
      'abierto',
      '',
      '2026-11-23T13:00:00.000Z',
    );
    expect(back.ok && back.value.audits[0]?.findings[0]?.resolvedAt).toBeUndefined();
  });
  it('compara dos auditorías', () => {
    const p = piece();
    const a = p.audits[0];
    if (!a) throw new Error('x');
    const d = diffPieceAudits(a, { ...a, score: a.score + 5, findings: [] });
    expect(d.scoreDelta).toBe(5);
    expect(d.resolved.length).toBe(a.findings.length);
    expect(d.added).toEqual([]);
  });
  it('rechaza registros mal formados', () => {
    expect(validatePieceRecord({ id: 'x' }).ok).toBe(false);
  });
});
