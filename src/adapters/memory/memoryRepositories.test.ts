import { describe, expect, it } from 'vitest';
import { CONTRACT_CASES, runContract } from '../../../tests/support/repositoryContract';
import { createMemoryRepositories } from './memoryRepositories';

describe('repositorios en memoria cumplen el contrato', () => {
  it('ejecuta todos los casos del contrato sin fallos', async () => {
    const failures = await runContract(() =>
      Promise.resolve({ repos: createMemoryRepositories(), dispose: () => Promise.resolve() }),
    );
    expect(failures).toEqual([]);
    expect(CONTRACT_CASES.length).toBeGreaterThanOrEqual(9);
  });
  it('dos instancias no comparten datos', async () => {
    const a = createMemoryRepositories();
    const b = createMemoryRepositories();
    await a.profile.save('Ana');
    expect(await b.profile.get()).toEqual({ ok: true, value: {} });
  });
});
