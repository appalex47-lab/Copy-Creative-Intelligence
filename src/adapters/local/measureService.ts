import {
  MAX_MEASURES,
  parseResultsCsv,
  validateMeasureRecord,
  type MeasureRecord,
} from '@/domain/measure';
import type { MeasureRepository } from '@/repositories/contracts';
import { fail, ok, type MeasureService, type Result } from '@/services/contracts';

export interface MeasureServiceDeps {
  readonly repo: () => Promise<Result<MeasureRepository>>;
  readonly writable: <T>(run: () => Promise<Result<T>>) => Promise<Result<T>>;
  readonly now?: () => Date;
  readonly newId?: () => string;
}

/** Casos de uso de medición (S4.2): resultados manuales o por CSV y experimentos A/B. Todo local, sin plataformas externas. */
export function createMeasureService(deps: MeasureServiceDeps): MeasureService {
  const now = deps.now ?? (() => new Date());
  const newId = deps.newId ?? (() => `mea_${crypto.randomUUID().replaceAll('-', '')}`);
  const withRepo = async <T>(
    run: (r: MeasureRepository) => Promise<Result<T>>,
  ): Promise<Result<T>> => {
    const r = await deps.repo();
    return r.ok ? run(r.value) : fail(r.error.code, r.error.message);
  };
  const capacity = async (r: MeasureRepository, extra: number): Promise<Result<never> | null> => {
    const n = await r.count();
    if (!n.ok) return fail(n.error.code, n.error.message);
    return n.value + extra > MAX_MEASURES
      ? fail('validation_error', 'Se alcanzó el máximo de mediciones.')
      : null;
  };
  return {
    list: () => withRepo((r) => r.list()),
    saveResult: (input) =>
      deps.writable(() =>
        withRepo(async (repo) => {
          const full = await capacity(repo, 1);
          if (full) return full;
          const v = validateMeasureRecord({
            ...input,
            kind: 'resultado',
            id: newId(),
            createdAt: now().toISOString(),
          });
          if (!v.ok) return fail<MeasureRecord>('validation_error', v.reason);
          return repo.put(v.value);
        }),
      ),
    importResults: (csv) =>
      deps.writable(() =>
        withRepo(async (repo) => {
          const rows = parseResultsCsv(csv);
          if (!rows.ok) return fail<number>('validation_error', rows.reason);
          const full = await capacity(repo, rows.value.length);
          if (full) return full;
          const at = now().toISOString();
          const records: MeasureRecord[] = [];
          for (const [i, row] of rows.value.entries()) {
            const v = validateMeasureRecord({
              ...row,
              kind: 'resultado',
              id: newId(),
              createdAt: at,
            });
            if (!v.ok)
              return fail<number>('validation_error', `Fila ${String(i + 2)}: ${v.reason}`);
            records.push(v.value);
          }
          for (const r of records) {
            const p = await repo.put(r);
            if (!p.ok) return fail<number>(p.error.code, p.error.message);
          }
          return ok(records.length);
        }),
      ),
    saveExperiment: (input) =>
      deps.writable(() =>
        withRepo(async (repo) => {
          let prevCreated: string | undefined;
          if (input.id !== undefined) {
            const prev = await repo.get(input.id);
            if (!prev.ok) return fail<MeasureRecord>('not_found', 'El experimento no existe.');
            prevCreated = prev.value.createdAt;
          } else {
            const full = await capacity(repo, 1);
            if (full) return full;
          }
          const at = now().toISOString();
          const rest = Object.fromEntries(Object.entries(input).filter(([k]) => k !== 'id'));
          const v = validateMeasureRecord({
            ...rest,
            kind: 'experimento',
            id: input.id ?? newId(),
            createdAt: prevCreated ?? at,
            updatedAt: at,
          });
          if (!v.ok) return fail<MeasureRecord>('validation_error', v.reason);
          return repo.put(v.value);
        }),
      ),
    remove: (id) => deps.writable(() => withRepo((r) => r.remove(id))),
  };
}
