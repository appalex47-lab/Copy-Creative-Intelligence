import type { BriefRecord } from '@/domain/briefRecord';
import type { BriefRepository, CopyRepository, EntityRepository } from '@/repositories/contracts';
import { fail, type BriefService, type Result } from '@/services/contracts';

export interface BriefServiceDeps {
  /** Repositorio de briefs (perezoso: puede fallar al abrir la base). */
  readonly repo: () => Promise<Result<BriefRepository>>;
  /** Envuelve toda escritura (P12: solo la pestaña escritora guarda). */
  readonly writable: <T>(run: () => Promise<Result<T>>) => Promise<Result<T>>;
  /** Si se indica, borrar un brief con copys se rechaza (sin pérdida de datos). */
  readonly copies?: () => Promise<Result<CopyRepository>>;
  /** Si se indica, la campaña referenciada debe existir. */
  readonly entities?: () => Promise<Result<EntityRepository>>;
  readonly now?: () => Date;
  readonly newId?: () => string;
}

const defaultId = (): string => `brf_${crypto.randomUUID().replaceAll('-', '')}`;

/** Casos de uso de briefs. Sin red. Las fechas e ids los pone el servicio, nunca la interfaz. */
export function createBriefService(deps: BriefServiceDeps): BriefService {
  const now = deps.now ?? (() => new Date());
  const newId = deps.newId ?? defaultId;
  const withRepo = async <T>(
    run: (r: BriefRepository) => Promise<Result<T>>,
  ): Promise<Result<T>> => {
    const r = await deps.repo();
    return r.ok ? run(r.value) : fail(r.error.code, r.error.message);
  };
  return {
    list: () => withRepo((r) => r.list()),
    get: (id) => withRepo((r) => r.get(id)),
    save: (input) =>
      deps.writable(() =>
        withRepo(async (r) => {
          const stamp = now().toISOString();
          let createdAt = stamp;
          let id = input.id;
          if (id === undefined) id = newId();
          else {
            const existing = await r.get(id);
            if (!existing.ok) return existing; // no se crea por accidente con un id desconocido
            createdAt = existing.value.createdAt;
          }
          const updatedAt = stamp < createdAt ? createdAt : stamp; // un reloj atrasado no rompe el orden de fechas
          const cid = input.campaignId ?? undefined;
          if (cid !== undefined) {
            if (!deps.entities)
              return fail<BriefRecord>('validation_error', 'Las campañas no están disponibles.');
            const e = await deps.entities();
            if (!e.ok) return fail<BriefRecord>(e.error.code, e.error.message);
            const camp = await e.value.get(cid);
            if (!camp.ok || camp.value.kind !== 'campaign')
              return fail<BriefRecord>('validation_error', 'La campaña elegida no existe.');
          }
          const record: unknown = {
            id,
            createdAt,
            updatedAt,
            fields: input.fields,
            ...(cid !== undefined ? { campaignId: cid } : {}),
          };
          return r.put(record);
        }),
      ),
    remove: (id) =>
      deps.writable(async () => {
        if (deps.copies) {
          const c = await deps.copies();
          if (!c.ok) return fail(c.error.code, c.error.message);
          const mine = await c.value.list(id);
          if (!mine.ok) return fail(mine.error.code, mine.error.message);
          if (mine.value.length > 0)
            return fail('conflict', 'El brief tiene copys; elimínalos primero.');
        }
        return withRepo((r) => r.remove(id));
      }),
  };
}

export type { BriefRecord };
