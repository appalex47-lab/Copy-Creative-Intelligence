import {
  OCR_LANGS,
  RESOURCE_LIMITS,
  validateDimensions,
  validateResourceFile,
  type ResourceRecord,
} from '@/domain/resource';
import type { ResourceRepository } from '@/repositories/contracts';
import { fail, type OcrEngine, type ResourceService, type Result } from '@/services/contracts';

export interface ResourceServiceDeps {
  readonly repo: () => Promise<Result<ResourceRepository>>;
  readonly engine: () => OcrEngine;
  readonly readSize: (
    blob: Blob,
  ) => Promise<{ readonly width: number; readonly height: number } | null>;
  readonly engineName: string;
  readonly writable: <T>(run: () => Promise<Result<T>>) => Promise<Result<T>>;
  readonly now?: () => Date;
  readonly newId?: () => string;
}

const defaultId = (): string => `res_${crypto.randomUUID().replaceAll('-', '')}`;

/**
 * Casos de uso de recursos visuales (S3.3). Reglas: el original se guarda tal cual y nunca se reescribe; lo
 * detectado por el OCR (`ocr`) y lo validado por una persona (`reviewedText`) son campos distintos; las palabras
 * dudosas se marcan, no se corrigen. Un recurso no es una Pieza creativa ni una aprobación.
 */
export function createResourceService(deps: ResourceServiceDeps): ResourceService {
  const now = deps.now ?? (() => new Date());
  const newId = deps.newId ?? defaultId;
  const withRepo = async <T>(
    run: (r: ResourceRepository) => Promise<Result<T>>,
  ): Promise<Result<T>> => {
    const r = await deps.repo();
    return r.ok ? run(r.value) : fail(r.error.code, r.error.message);
  };
  const update = (id: string, change: (r: ResourceRecord) => ResourceRecord) =>
    withRepo(async (repo) => {
      const cur = await repo.get(id);
      if (!cur.ok) return cur;
      return repo.put(change(cur.value));
    });
  return {
    list: () => withRepo((r) => r.list()),
    add: (file) =>
      deps.writable(() =>
        withRepo(async (repo) => {
          const v = validateResourceFile(file);
          if (!v.ok) return fail<ResourceRecord>('validation_error', v.reason);
          const count = await repo.count();
          if (!count.ok) return fail<ResourceRecord>(count.error.code, count.error.message);
          if (count.value >= RESOURCE_LIMITS.maxResources)
            return fail<ResourceRecord>(
              'validation_error',
              `Ya hay ${String(RESOURCE_LIMITS.maxResources)} recursos guardados; elimina alguno.`,
            );
          const size = await deps.readSize(file);
          if (!size || !validateDimensions(size.width, size.height).ok)
            return fail<ResourceRecord>(
              'validation_error',
              'La imagen no se pudo leer o tiene demasiados píxeles.',
            );
          return repo.put({
            id: newId(),
            name: v.value.name,
            mime: file.type,
            size: file.size,
            width: size.width,
            height: size.height,
            createdAt: now().toISOString(),
            blob: file,
          });
        }),
      ),
    runOcr: async (id, onProgress) => {
      const cur = await withRepo((r) => r.get(id));
      if (!cur.ok) return cur;
      // El OCR es lento: se ejecuta fuera del candado y solo el guardado final es una escritura.
      const out = await deps.engine().recognize(cur.value.blob, onProgress);
      if (!out.ok) return fail<ResourceRecord>(out.error.code, out.error.message);
      return deps.writable(() =>
        update(id, (r) => ({
          ...r,
          ocr: {
            engine: deps.engineName,
            langs: OCR_LANGS,
            threshold: RESOURCE_LIMITS.lowConfidence,
            ranAt: now().toISOString(),
            text: out.value.text.slice(0, 100_000),
            words: out.value.words,
          },
        })),
      );
    },
    saveReview: (id, text) =>
      deps.writable(() => {
        if (typeof text !== 'string')
          return Promise.resolve(
            fail<ResourceRecord>('validation_error', 'El texto no es válido.'),
          );
        if (text.length > RESOURCE_LIMITS.maxReviewedLength)
          return Promise.resolve(
            fail<ResourceRecord>(
              'validation_error',
              `El texto validado admite hasta ${String(RESOURCE_LIMITS.maxReviewedLength)} caracteres.`,
            ),
          );
        return update(id, (r) => {
          const rest: Record<string, unknown> = { ...r };
          delete rest['reviewedText'];
          delete rest['reviewedAt'];
          return (text.trim().length === 0
            ? rest
            : {
                ...rest,
                reviewedText: text,
                reviewedAt: now().toISOString(),
              }) as unknown as ResourceRecord;
        });
      }),
    remove: (id) => deps.writable(() => withRepo((r) => r.remove(id))),
  };
}
