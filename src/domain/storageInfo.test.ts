import { describe, expect, it } from 'vitest';
import { formatBytes, parseStorageInfo } from './storageInfo';

describe('storageInfo', () => {
  it('formatea bytes y usa «No disponible» para null', () => {
    expect(formatBytes(null)).toBe('No disponible');
    expect(formatBytes(0)).toBe('0 B');
    expect(formatBytes(1023)).toBe('1023 B');
    expect(formatBytes(1536)).toBe('1.5 KB');
    expect(formatBytes(5 * 1024 * 1024)).toBe('5.0 MB');
    expect(formatBytes(300 * 1024 ** 3)).toBe('300 GB');
  });
  it('valores no confiables o raros pasan a null', () => {
    expect(parseStorageInfo(10, 100, true)).toEqual({
      usageBytes: 10,
      quotaBytes: 100,
      persisted: true,
    });
    expect(parseStorageInfo(-1, NaN, 'sí')).toEqual({
      usageBytes: null,
      quotaBytes: null,
      persisted: null,
    });
    expect(parseStorageInfo(undefined, Infinity, undefined)).toEqual({
      usageBytes: null,
      quotaBytes: null,
      persisted: null,
    });
  });
});
