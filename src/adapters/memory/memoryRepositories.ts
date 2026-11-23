import { validateActivityEvent, type ActivityEvent } from '@/domain/activity';
import { validateDisplayName, type LocalProfile } from '@/domain/profile';
import { compareNewestFirst, normalizeLimit, type Repositories } from '@/repositories/contracts';
import { fail, ok } from '@/services/contracts';

/** Repositorios en memoria: sirven para pruebas y como referencia de comportamiento del adaptador IndexedDB. */
export function createMemoryRepositories(): Repositories {
  const events = new Map<string, ActivityEvent>();
  let name: string | undefined;
  const profile = (): LocalProfile => (name === undefined ? {} : { displayName: name });
  return {
    activity: {
      add: (raw) => {
        const v = validateActivityEvent(raw);
        if (!v.ok) return Promise.resolve(fail('validation_error', v.reason));
        events.set(v.value.id, v.value);
        return Promise.resolve(ok(v.value));
      },
      listRecent: (limit) => {
        const n = normalizeLimit(limit);
        if (n === null) return Promise.resolve(fail('validation_error', 'Límite inválido.'));
        return Promise.resolve(ok([...events.values()].sort(compareNewestFirst).slice(0, n)));
      },
      count: () => Promise.resolve(ok(events.size)),
    },
    profile: {
      get: () => Promise.resolve(ok(profile())),
      save: (displayName) => {
        const v = validateDisplayName(displayName);
        if (!v.ok) return Promise.resolve(fail('validation_error', v.reason));
        name = v.value;
        return Promise.resolve(ok(profile()));
      },
      clear: () => {
        name = undefined;
        return Promise.resolve(ok(profile()));
      },
    },
  };
}
