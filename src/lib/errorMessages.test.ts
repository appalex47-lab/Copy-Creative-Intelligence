import { describe, expect, it } from 'vitest';
import { describeError, isRetryable } from './errorMessages';

describe('errorMessages', () => {
  it('describe por código y no reproduce el texto interno', () => {
    const text = describeError({ code: 'unavailable', message: 'detalle interno SQL' });
    expect(text).toBe('El servicio no está disponible en este momento.');
    expect(text).not.toContain('SQL');
  });
  it('solo "unavailable" es reintentable', () => {
    expect(isRetryable('unavailable')).toBe(true);
    for (const c of [
      'not_found',
      'not_implemented',
      'invalid_configuration',
      'validation_error',
    ] as const)
      expect(isRetryable(c)).toBe(false);
  });
});
