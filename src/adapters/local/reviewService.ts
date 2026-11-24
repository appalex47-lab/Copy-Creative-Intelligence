import { currentVersion } from '@/domain/copy';
import {
  MAX_REVIEWS,
  validateReviewBody,
  validateReviewRecord,
  type ReviewRecord,
} from '@/domain/review';
import type { CopyRepository, PieceRepository, ReviewRepository } from '@/repositories/contracts';
import { fail, type Result, type ReviewService } from '@/services/contracts';

export interface ReviewServiceDeps {
  readonly repo: () => Promise<Result<ReviewRepository>>;
  readonly copies: () => Promise<Result<CopyRepository>>;
  readonly pieces: () => Promise<Result<PieceRepository>>;
  readonly writable: <T>(run: () => Promise<Result<T>>) => Promise<Result<T>>;
  readonly now?: () => Date;
  readonly newId?: () => string;
}

/** Casos de uso de revisiones de calidad (S4.1): validan el contenido y reglas de los filtros; el objetivo debe existir. */
export function createReviewService(deps: ReviewServiceDeps): ReviewService {
  const now = deps.now ?? (() => new Date());
  const newId = deps.newId ?? (() => `rev_${crypto.randomUUID().replaceAll('-', '')}`);
  const withRepo = async <T>(
    run: (r: ReviewRepository) => Promise<Result<T>>,
  ): Promise<Result<T>> => {
    const r = await deps.repo();
    return r.ok ? run(r.value) : fail(r.error.code, r.error.message);
  };
  return {
    list: () => withRepo((r) => r.list()),
    save: (input) =>
      deps.writable(() =>
        withRepo(async (repo) => {
          const body = validateReviewBody(input.body);
          if (!body.ok) return fail<ReviewRecord>('validation_error', body.reason);
          let label: string;
          if (input.targetType === 'copy') {
            const cr = await deps.copies();
            if (!cr.ok) return fail<ReviewRecord>(cr.error.code, cr.error.message);
            const c = await cr.value.get(input.targetId);
            if (!c.ok) return fail<ReviewRecord>('validation_error', 'El copy no existe.');
            label = `${c.value.label} (v${String(currentVersion(c.value).n)})`;
          } else {
            const pr = await deps.pieces();
            if (!pr.ok) return fail<ReviewRecord>(pr.error.code, pr.error.message);
            const p = await pr.value.get(input.targetId);
            if (!p.ok) return fail<ReviewRecord>('validation_error', 'La pieza no existe.');
            label = p.value.name;
          }
          const all = await repo.list();
          if (!all.ok) return fail<ReviewRecord>(all.error.code, all.error.message);
          const prev = all.value.find(
            (r) => r.targetType === input.targetType && r.targetId === input.targetId,
          );
          if (!prev && all.value.length >= MAX_REVIEWS)
            return fail<ReviewRecord>('validation_error', 'Se alcanzó el máximo de revisiones.');
          const at = now().toISOString();
          const rec = validateReviewRecord({
            id: prev?.id ?? newId(),
            targetType: input.targetType,
            targetId: input.targetId,
            targetLabel: label,
            ...body.value,
            createdAt: prev?.createdAt ?? at,
            updatedAt: at,
          });
          if (!rec.ok) return fail<ReviewRecord>('validation_error', rec.reason);
          return repo.put(rec.value);
        }),
      ),
    remove: (id) => deps.writable(() => withRepo((r) => r.remove(id))),
  };
}
