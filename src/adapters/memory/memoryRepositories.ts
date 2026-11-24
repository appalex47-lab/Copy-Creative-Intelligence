import { validateSnapshot } from '@/domain/backup';
import { validateActivityEvent, type ActivityEvent } from '@/domain/activity';
import {
  compareBriefsNewestFirst,
  BRIEF_ID,
  validateBriefRecord,
  type BriefRecord,
} from '@/domain/briefRecord';
import {
  compareCopiesNewestFirst,
  COPY_ID,
  validateCopyRecord,
  type CopyRecord,
} from '@/domain/copy';
import {
  AUDIT_ID,
  compareAuditsNewestFirst,
  validateAuditRecord,
  type AuditRecord,
} from '@/domain/audit';
import {
  ADAPTATION_ID,
  compareAdaptationsNewestFirst,
  validateAdaptationRecord,
  type AdaptationRecord,
} from '@/domain/adaptation';
import {
  compareEntities,
  ENTITY_ID,
  validateEntityRecord,
  type EntityRecord,
} from '@/domain/entity';
import { validateRulesDoc, type RulesDoc } from '@/domain/rulesConfig';
import { validateDisplayName, type LocalProfile } from '@/domain/profile';
import { compareNewestFirst, normalizeLimit, type Repositories } from '@/repositories/contracts';
import { fail, ok } from '@/services/contracts';

/** Repositorios en memoria: sirven para pruebas y como referencia de comportamiento del adaptador IndexedDB. */
export function createMemoryRepositories(): Repositories {
  const events = new Map<string, ActivityEvent>();
  const briefs = new Map<string, BriefRecord>();
  const copies = new Map<string, CopyRecord>();
  const entities = new Map<string, EntityRecord>();
  const adaptations = new Map<string, AdaptationRecord>();
  const audits = new Map<string, AuditRecord>();
  let rules: RulesDoc | null = null;
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
    copies: {
      put: (raw) => {
        const v = validateCopyRecord(raw);
        if (!v.ok) return Promise.resolve(fail('validation_error', v.reason));
        copies.set(v.value.id, v.value);
        return Promise.resolve(ok(v.value));
      },
      get: (id) => {
        const c = COPY_ID.test(id) ? copies.get(id) : undefined;
        return Promise.resolve(c ? ok(c) : fail('validation_error', 'El copy no existe.'));
      },
      list: (briefId) =>
        Promise.resolve(
          ok(
            [...copies.values()]
              .filter((c) => briefId === undefined || c.briefId === briefId)
              .sort(compareCopiesNewestFirst),
          ),
        ),
      remove: (id) => {
        if (!COPY_ID.test(id))
          return Promise.resolve(fail('validation_error', 'Identificador de copy no válido.'));
        copies.delete(id);
        return Promise.resolve(ok(undefined));
      },
      count: () => Promise.resolve(ok(copies.size)),
    },
    entities: {
      put: (raw) => {
        const v = validateEntityRecord(raw);
        if (!v.ok) return Promise.resolve(fail('validation_error', v.reason));
        entities.set(v.value.id, v.value);
        return Promise.resolve(ok(v.value));
      },
      get: (id) => {
        const e = ENTITY_ID.test(id) ? entities.get(id) : undefined;
        return Promise.resolve(e ? ok(e) : fail('validation_error', 'El registro no existe.'));
      },
      list: (kind) =>
        Promise.resolve(
          ok(
            [...entities.values()]
              .filter((e) => kind === undefined || e.kind === kind)
              .sort(compareEntities),
          ),
        ),
      remove: (id) => {
        if (!ENTITY_ID.test(id))
          return Promise.resolve(fail('validation_error', 'Identificador no válido.'));
        entities.delete(id);
        return Promise.resolve(ok(undefined));
      },
    },
    adaptations: {
      put: (raw) => {
        const v = validateAdaptationRecord(raw);
        if (!v.ok) return Promise.resolve(fail('validation_error', v.reason));
        adaptations.set(v.value.id, v.value);
        return Promise.resolve(ok(v.value));
      },
      get: (id) => {
        const a = ADAPTATION_ID.test(id) ? adaptations.get(id) : undefined;
        return Promise.resolve(a ? ok(a) : fail('validation_error', 'La adaptación no existe.'));
      },
      list: (copyId) =>
        Promise.resolve(
          ok(
            [...adaptations.values()]
              .filter((a) => copyId === undefined || a.copyId === copyId)
              .sort(compareAdaptationsNewestFirst),
          ),
        ),
      remove: (id) => {
        if (!ADAPTATION_ID.test(id))
          return Promise.resolve(fail('validation_error', 'Identificador no válido.'));
        adaptations.delete(id);
        return Promise.resolve(ok(undefined));
      },
      count: () => Promise.resolve(ok(adaptations.size)),
    },
    audits: {
      put: (raw) => {
        const v = validateAuditRecord(raw);
        if (!v.ok) return Promise.resolve(fail('validation_error', v.reason));
        audits.set(v.value.id, v.value);
        return Promise.resolve(ok(v.value));
      },
      get: (id) => {
        const a = AUDIT_ID.test(id) ? audits.get(id) : undefined;
        return Promise.resolve(a ? ok(a) : fail('validation_error', 'La auditoría no existe.'));
      },
      list: (copyId) =>
        Promise.resolve(
          ok(
            [...audits.values()]
              .filter((a) => copyId === undefined || a.copyId === copyId)
              .sort(compareAuditsNewestFirst),
          ),
        ),
      remove: (id) => {
        if (!AUDIT_ID.test(id))
          return Promise.resolve(fail('validation_error', 'Identificador no válido.'));
        audits.delete(id);
        return Promise.resolve(ok(undefined));
      },
      count: () => Promise.resolve(ok(audits.size)),
    },
    rules: {
      get: () => Promise.resolve(ok(rules)),
      save: (raw) => {
        const v = validateRulesDoc(raw);
        if (!v.ok) return Promise.resolve(fail('validation_error', v.reason));
        rules = v.value;
        return Promise.resolve(ok(v.value));
      },
      clear: () => {
        rules = null;
        return Promise.resolve(ok(undefined));
      },
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
            copies: [...copies.values()].sort(compareCopiesNewestFirst),
            rules,
            entities: [...entities.values()].sort(compareEntities),
            adaptations: [...adaptations.values()].sort(compareAdaptationsNewestFirst),
            audits: [...audits.values()].sort(compareAuditsNewestFirst),
          }),
        ),
      replaceAll: (raw) => {
        const v = validateSnapshot(raw);
        if (!v.ok) return Promise.resolve(fail('validation_error', v.reason));
        events.clear();
        briefs.clear();
        copies.clear();
        entities.clear();
        adaptations.clear();
        audits.clear();
        for (const e of v.value.activity) events.set(e.id, e);
        for (const b of v.value.briefs) briefs.set(b.id, b);
        for (const c of v.value.copies) copies.set(c.id, c);
        for (const e of v.value.entities) entities.set(e.id, e);
        for (const a of v.value.adaptations) adaptations.set(a.id, a);
        for (const a of v.value.audits) audits.set(a.id, a);
        rules = v.value.rules;
        name = v.value.profile.displayName;
        return Promise.resolve(ok(undefined));
      },
    },
  };
}
