import { describe, expect, it } from 'vitest';
import { formatLocalDateTime } from './formatDate';

describe('formatLocalDateTime', () => {
  it('formatea una fecha válida sin mostrar el formato ISO crudo', () => {
    const t = formatLocalDateTime('2026-11-23T17:01:40.995Z');
    expect(t).not.toContain('T17');
    expect(t).not.toContain('Z');
    expect(t).toMatch(/2026/);
  });
  it('devuelve el texto original si no es una fecha válida', () => {
    expect(formatLocalDateTime('no es fecha')).toBe('no es fecha');
  });
});
