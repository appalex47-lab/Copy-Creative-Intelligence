import { validateSnapshot } from '@/domain/backup';
import { validateActivityEvent, type ActivityEvent } from '@/domain/activity';
import {
  compareBriefsNewestFirst,
  BRIEF_ID,
  validateBriefRecord,
  type BriefRecord,
} from '@/domain/briefRecord';
import { validateDisplayName, type LocalProfile } from '@/domain/profile';
import { compareNewestFirst, normalizeLimit, type Repositories } from '@/repositories/contracts';
import { fail, ok } from '@/services/contracts';

/** Repositorios en memoria: sirven para pruebas y como referencia de comportamiento del adaptador IndexedDB. */
export function createMemoryRepositories(): Repositories {
  const events = new Map<string, ActivityEvent>();
  const briefs = new Map<string, BriefRecord>();
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
    briefs: {
      put: (raw) => {
        const v = validateBriefRecord(raw);
        if (!v.ok) return Promise.resolve(fail('validation_error', v.reason));
        briefs.set(v.value.id, v.value);
        return Promise.resolve(ok(v.value));
      },
      get: (id) => {
        const b = BRIEF_ID.test(id) ? briefs.get(id) : undefined;
        return Promise.resolve(b ? ok(b) : fail('validation_error', 'El brief no existe.'));
      },
      list: () => Promise.resolve(ok([...briefs.values()].sort(compareBriefsNewestFirst))),
      remove: (id) => {
        if (!BRIEF_ID.test(id))
          return Promise.resolve(fail('validation_error', 'Identificador de brief no válido.'));
        briefs.delete(id);
        return Promise.resolve(ok(undefined));
      },
      count: () => Promise.resolve(ok(briefs.size)),
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
    backup: {
      exportAll: () =>
        Promise.resolve(
          ok({
            profile: profile(),
            activity: [...events.values()].sort(compareNewestFirst),
            briefs: [...briefs.values()].sort(compareBriefsNewestFirst),
          }),
        ),
      replaceAll: (raw) => {
        const v = validateSnapshot(raw);
        if (!v.ok) return Promise.resolve(fail('validation_error', v.reason));
        events.clear();
        briefs.clear();
        for (const e of v.value.activity) events.set(e.id, e);
        for (const b of v.value.briefs) briefs.set(b.id, b);
        name = v.value.profile.displayName;
        return Promise.resolve(ok(undefined));
      },
    },
  };
}
