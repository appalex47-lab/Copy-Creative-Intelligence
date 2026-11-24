import {
  ENTITY_KINDS,
  ENTITY_PREFIX,
  MAX_ENTITIES_PER_KIND,
  entityKey,
  validateEntityName,
  validateEntityNote,
  validateEntityRecord,
  type EntityRecord,
} from '@/domain/entity';
import type { BriefRepository, EntityRepository } from '@/repositories/contracts';
import { fail, ok, type EntityService, type Result } from '@/services/contracts';

export interface EntityServiceDeps {
  readonly repo: () => Promise<Result<EntityRepository>>;
  /** Para impedir borrar una campaña referenciada por briefs. */
  readonly briefs: () => Promise<Result<BriefRepository>>;
  readonly writable: <T>(run: () => Promise<Result<T>>) => Promise<Result<T>>;
  readonly now?: () => Date;
  readonly newSuffix?: () => string;
}

const defaultSuffix = (): string => crypto.randomUUID().replaceAll('-', '');

/** Casos de uso del catálogo (campañas, productos, ofertas). Sin red. Ids y fechas los pone el servicio. */
export function createEntityService(deps: EntityServiceDeps): EntityService {
  const now = deps.now ?? (() => new Date());
  const suffix = deps.newSuffix ?? defaultSuffix;
  const withRepo = async <T>(
    run: (r: EntityRepository) => Promise<Result<T>>,
  ): Promise<Result<T>> => {
    const r = await deps.repo();
    return r.ok ? run(r.value) : fail(r.error.code, r.error.message);
  };
  const duplicate = (all: readonly EntityRecord[], cand: EntityRecord): boolean =>
    all.some((e) => e.id !== cand.id && entityKey(e) === entityKey(cand));
  return {
    list: (kind) => withRepo((r) => r.list(kind)),
    create: (i) =>
      deps.writable(() =>
        withRepo(async (r) => {
          if (!ENTITY_KINDS.includes(i.kind))
            return fail<EntityRecord>('validation_error', 'El tipo de registro no es válido.');
          const name = validateEntityName(i.name);
          if (!name.ok) return fail<EntityRecord>('validation_error', name.reason);
          const note = validateEntityNote(i.note);
          if (!note.ok) return fail<EntityRecord>('validation_error', note.reason);
          const at = now().toISOString();
          const cand = validateEntityRecord({
            id: `${ENTITY_PREFIX[i.kind]}_${suffix()}`,
            kind: i.kind,
            name: name.value,
            ...(note.value !== undefined ? { note: note.value } : {}),
            createdAt: at,
            updatedAt: at,
          });
          if (!cand.ok) return fail<EntityRecord>('validation_error', cand.reason);
          const all = await r.list(i.kind);
          if (!all.ok) return all;
          if (all.value.length >= MAX_ENTITIES_PER_KIND)
            return fail<EntityRecord>('validation_error', 'Se alcanzó el máximo de registros.');
          if (duplicate(all.value, cand.value))
            return fail<EntityRecord>('validation_error', 'Ya existe un registro con ese nombre.');
          return r.put(cand.value);
        }),
      ),
    update: (i) =>
      deps.writable(() =>
        withRepo(async (r) => {
          const cur = await r.get(i.id);
          if (!cur.ok) return cur;
          const name = validateEntityName(i.name);
          if (!name.ok) return fail<EntityRecord>('validation_error', name.reason);
          const note = validateEntityNote(i.note);
          if (!note.ok) return fail<EntityRecord>('validation_error', note.reason);
          const at = now().toISOString();
          const cand = validateEntityRecord({
            id: cur.value.id,
            kind: cur.value.kind,
            name: name.value,
            ...(note.value !== undefined ? { note: note.value } : {}),
            createdAt: cur.value.createdAt,
            updatedAt: at < cur.value.createdAt ? cur.value.createdAt : at,
          });
          if (!cand.ok) return fail<EntityRecord>('validation_error', cand.reason);
          const all = await r.list(cur.value.kind);
          if (!all.ok) return all;
          if (duplicate(all.value, cand.value))
            return fail<EntityRecord>('validation_error', 'Ya existe un registro con ese nombre.');
          return r.put(cand.value);
        }),
      ),
    remove: (id) =>
      deps.writable(() =>
        withRepo(async (r) => {
          if (id.startsWith('cmp_')) {
            const b = await deps.briefs();
            if (!b.ok) return fail<never>(b.error.code, b.error.message);
            const all = await b.value.list();
            if (!all.ok) return fail<never>(all.error.code, all.error.message);
            if (all.value.some((x) => x.campaignId === id))
              return fail<never>(
                'conflict',
                'La campaña está en uso por briefs; quita la referencia primero.',
              );
          }
          const res = await r.remove(id);
          return res.ok ? ok(undefined) : res;
        }),
      ),
  };
}
