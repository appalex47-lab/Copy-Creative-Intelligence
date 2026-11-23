import { describe, expect, it } from 'vitest';
import { describeError, isRetryable } from './errorMessages';

describe('errorMessages', () => {
  it('describe por código y no reproduce el texto interno', () => {
    const text = describeError({ code: 'unavailable', message: 'detalle interno SQL' });
    expect(text).toBe('El servicio no está disponible en este momento.');
    expect(text).not.toContain('SQL');
  });
  it('cada código de almacenamiento tiene un mensaje propio y distinto, sin texto interno', () => {
    const codes = [
      'storage_unavailable',
      'storage_blocked',
      'storage_quota_exceeded',
      'storage_newer_schema',
      'storage_failed',
    ] as const;
    const texts = codes.map((code) => describeError({ code, message: 'SECRETO_INTERNO' }));
    expect(new Set(texts).size).toBe(codes.length);
    for (const t of texts) expect(t).not.toContain('SECRETO');
  });
  it('solo los fallos transitorios son reintentables', () => {
    for (const c of ['unavailable', 'storage_blocked', 'storage_failed'] as const)
      expect(isRetryable(c)).toBe(true);
    for (const c of [
      'storage_unavailable',
      'storage_quota_exceeded',
      'storage_newer_schema',
      'not_found',
      'not_implemented',
      'invalid_configuration',
      'validation_error',
    ] as const)
      expect(isRetryable(c)).toBe(false);
  });
});
