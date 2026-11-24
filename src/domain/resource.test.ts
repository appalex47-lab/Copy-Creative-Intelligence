import { describe, expect, it } from 'vitest';
import {
  RESOURCE_LIMITS,
  countUncertain,
  flagWords,
  validateDimensions,
  validateResourceFile,
  validateResourceRecord,
} from './resource';

const base = () => ({
  id: 'res_abcdefgh1234',
  name: 'banner.png',
  mime: 'image/png',
  size: 1000,
  width: 100,
  height: 50,
  createdAt: '2026-11-23T10:00:00.000Z',
  blob: new Blob(['x'], { type: 'image/png' }),
});

describe('validateResourceFile', () => {
  it('admite PNG, JPEG y WebP dentro del límite', () => {
    for (const type of RESOURCE_LIMITS.mimes)
      expect(validateResourceFile({ name: 'a', type, size: 10 }).ok).toBe(true);
  });
  it('rechaza formato, vacío y exceso de tamaño', () => {
    expect(validateResourceFile({ name: 'a.gif', type: 'image/gif', size: 10 }).ok).toBe(false);
    expect(validateResourceFile({ name: 'a', type: 'image/png', size: 0 }).ok).toBe(false);
    const big = validateResourceFile({
      name: 'a',
      type: 'image/png',
      size: RESOURCE_LIMITS.maxBytes + 1,
    });
    expect(big.ok).toBe(false);
  });
  it('recorta el nombre y pone uno por defecto', () => {
    const r = validateResourceFile({ name: '  ', type: 'image/png', size: 5 });
    expect(r.ok && r.value.name).toBe('Imagen sin nombre');
  });
});

describe('validateDimensions', () => {
  it('limita los píxeles', () => {
    expect(validateDimensions(100, 100).ok).toBe(true);
    expect(validateDimensions(0, 10).ok).toBe(false);
    expect(validateDimensions(6000, 6000).ok).toBe(false);
  });
});

describe('flagWords', () => {
  it('marca dudosas sin cambiar el texto y descarta vacías', () => {
    const w = flagWords([
      { text: 'Oferta', confidence: 96.4 },
      { text: 'lO%', confidence: 31 },
      { text: '  ', confidence: 99 },
    ]);
    expect(w).toEqual([
      { text: 'Oferta', confidence: 96, uncertain: false },
      { text: 'lO%', confidence: 31, uncertain: true },
    ]);
    expect(countUncertain(w)).toBe(1);
  });
  it('acota la confianza a 0–100', () => {
    expect(flagWords([{ text: 'a', confidence: 150 }])[0]?.confidence).toBe(100);
    expect(flagWords([{ text: 'a', confidence: -3 }])[0]?.uncertain).toBe(true);
  });
});

describe('validateResourceRecord', () => {
  it('acepta un recurso sin OCR', () => {
    expect(validateResourceRecord(base()).ok).toBe(true);
  });
  it('exige blob y rechaza el texto revisado sin fecha', () => {
    expect(validateResourceRecord({ ...base(), blob: 'x' }).ok).toBe(false);
    expect(validateResourceRecord({ ...base(), reviewedText: 'hola' }).ok).toBe(false);
    expect(
      validateResourceRecord({
        ...base(),
        reviewedText: 'hola',
        reviewedAt: '2026-11-23T11:00:00.000Z',
      }).ok,
    ).toBe(true);
  });
  it('valida el OCR', () => {
    const ocr = {
      engine: 'tesseract.js 5.1.1',
      langs: 'spa+eng',
      threshold: 60,
      ranAt: '2026-11-23T10:05:00.000Z',
      text: 'Oferta',
      words: [{ text: 'Oferta', confidence: 90, uncertain: false }],
    };
    expect(validateResourceRecord({ ...base(), ocr }).ok).toBe(true);
    expect(validateResourceRecord({ ...base(), ocr: { ...ocr, words: [{ text: 1 }] } }).ok).toBe(
      false,
    );
  });
});
