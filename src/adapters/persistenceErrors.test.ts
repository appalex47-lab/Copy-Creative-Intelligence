import { describe, expect, it } from 'vitest';
import { classifyStorageError } from './persistenceErrors';

describe('classifyStorageError (AC1-08)', () => {
  it.each([
    ['QuotaExceededError', 'storage_quota_exceeded'],
    ['VersionError', 'storage_newer_schema'],
    ['SecurityError', 'storage_unavailable'],
    ['InvalidStateError', 'storage_unavailable'],
    ['NotSupportedError', 'storage_unavailable'],
    ['AbortError', 'storage_failed'],
    ['UnknownError', 'storage_failed'],
  ])('%s → %s', (name, code) => {
    expect(classifyStorageError(new DOMException('texto interno', name))).toBe(code);
  });
  it('valores que no son excepciones caen en fallo general', () => {
    for (const v of [undefined, null, 'x', 42, {}])
      expect(classifyStorageError(v)).toBe('storage_failed');
  });
});
