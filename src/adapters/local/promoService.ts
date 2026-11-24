import { MAX_PROMOS, parsePromosCsv, validatePromoRecord, type PromoRecord } from '@/domain/promo';
import type { PromoRepository } from '@/repositories/contracts';
import { fail, ok, type PromoService, type Result } from '@/services/contracts';

export interface PromoServiceDeps {
  readonly repo: () => Promise<Result<PromoRepository>>;
  readonly writable: <T>(run: () => Promise<Result<T>>) => Promise<Result<T>>;
  readonly now?: () => Date;
  readonly newId?: () => string;
}

/** Promociones capturadas o importadas por CSV (S4.2). La app no las inventa ni las consulta en ningún catálogo. */
export function createPromoService(deps: PromoServiceDeps): PromoService {
  const now = deps.now ?? (() => new Date());
  const newId = deps.newId ?? (() => `prm_${crypto.randomUUID().replaceAll('-', '')}`);
  const withRepo = async <T>(
    run: (r: PromoRepository) => Promise<Result<T>>,
  ): Promise<Result<T>> => {
    const r = await deps.repo();
    return r.ok ? run(r.value) : fail(r.error.code, r.error.message);
  };
  return {
    list: () => withRepo((r) => r.list()),
    save: (input) =>
      deps.writable(() =>
        withRepo(async (repo) => {
          let created = now().toISOString();
          if (input.id !== undefined) {
            const prev = await repo.get(input.id);
            if (!prev.ok) return fail<PromoRecord>('not_found', 'La promoción no existe.');
            created = prev.value.createdAt;
          } else {
            const n = await repo.count();
            if (n.ok && n.value >= MAX_PROMOS)
              return fail<PromoRecord>('validation_error', 'Se alcanzó el máximo de promociones.');
          }
          const v = validatePromoRecord({ ...input, id: input.id ?? newId(), createdAt: created });
          if (!v.ok) return fail<PromoRecord>('validation_error', v.reason);
          return repo.put(v.value);
        }),
      ),
    importCsv: (csv) =>
      deps.writable(() =>
        withRepo(async (repo) => {
          const rows = parsePromosCsv(csv);
          if (!rows.ok) return fail<number>('validation_error', rows.reason);
          const all = await repo.list();
          if (!all.ok) return fail<number>(all.error.code, all.error.message);
          if (all.value.length + rows.value.length > MAX_PROMOS)
            return fail<number>('validation_error', 'Se alcanzó el máximo de promociones.');
          const at = now().toISOString();
          const records: PromoRecord[] = [];
          for (const row of rows.value) {
            const v = validatePromoRecord({ ...row, id: newId(), createdAt: at });
            if (!v.ok) return fail<number>('validation_error', `«${row.name}»: ${v.reason}`);
            records.push(v.value);
          }
          for (const r of records) {
            const p = await repo.put(r);
            if (!p.ok) return fail<number>(p.error.code, p.error.message);
          }
          return ok(records.length);
        }),
      ),
    remove: (id) => deps.writable(() => withRepo((r) => r.remove(id))),
  };
}
