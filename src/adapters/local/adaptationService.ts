import { validateAdaptationRecord, type AdaptationRecord } from '@/domain/adaptation';
import { currentVersion, validateCopyContent } from '@/domain/copy';
import type { AdaptationRepository, CopyRepository } from '@/repositories/contracts';
import { fail, type AdaptationService, type Result } from '@/services/contracts';

export interface AdaptationServiceDeps {
  readonly repo: () => Promise<Result<AdaptationRepository>>;
  readonly copies: () => Promise<Result<CopyRepository>>;
  readonly writable: <T>(run: () => Promise<Result<T>>) => Promise<Result<T>>;
  readonly now?: () => Date;
  readonly newId?: () => string;
}

const defaultId = (): string => `ada_${crypto.randomUUID().replaceAll('-', '')}`;

/** Casos de uso de adaptaciones por canal. Sin red. No auditan, puntúan ni aprueban. */
export function createAdaptationService(deps: AdaptationServiceDeps): AdaptationService {
  const now = deps.now ?? (() => new Date());
  const newId = deps.newId ?? defaultId;
  const withRepo = async <T>(
    run: (r: AdaptationRepository) => Promise<Result<T>>,
  ): Promise<Result<T>> => {
    const r = await deps.repo();
    return r.ok ? run(r.value) : fail(r.error.code, r.error.message);
  };
  return {
    list: (copyId) => withRepo((r) => r.list(copyId)),
    create: (i) =>
      deps.writable(() =>
        withRepo(async (r) => {
          const cr = await deps.copies();
          if (!cr.ok) return fail<AdaptationRecord>(cr.error.code, cr.error.message);
          const copy = await cr.value.get(i.copyId);
          if (!copy.ok) return fail<AdaptationRecord>('not_found', 'El copy de origen no existe.');
          const cur = currentVersion(copy.value);
          const sv = i.sourceVersion ?? cur.n;
          if (!copy.value.versions.some((v) => v.n === sv))
            return fail<AdaptationRecord>('validation_error', 'La versión de origen no existe.');
          const at = now().toISOString();
          const v = validateAdaptationRecord({
            id: newId(),
            copyId: i.copyId,
            sourceVersion: sv,
            channel: i.channel,
            content: i.content,
            createdAt: at,
            updatedAt: at,
          });
          if (!v.ok) return fail<AdaptationRecord>('validation_error', v.reason);
          return r.put(v.value);
        }),
      ),
    update: (i) =>
      deps.writable(() =>
        withRepo(async (r) => {
          const cur = await r.get(i.id);
          if (!cur.ok) return cur;
          const content = validateCopyContent(i.content);
          if (!content.ok) return fail<AdaptationRecord>('validation_error', content.reason);
          const at = now().toISOString();
          const v = validateAdaptationRecord({
            ...cur.value,
            content: content.value,
            updatedAt: at < cur.value.createdAt ? cur.value.createdAt : at,
          });
          if (!v.ok) return fail<AdaptationRecord>('validation_error', v.reason);
          return r.put(v.value);
        }),
      ),
    remove: (id) => deps.writable(() => withRepo((r) => r.remove(id))),
  };
}
