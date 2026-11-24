import {
  OCR_LANGS,
  RESOURCE_LIMITS,
  validateDimensions,
  validateResourceRecord,
  validateResourceFile,
  type ResourceRecord,
} from '@/domain/resource';
import {
  backupFileName,
  parseResourcesBackup,
  RESOURCES_BACKUP_FORMAT,
  RESOURCES_BACKUP_MAX_BYTES,
  RESOURCES_BACKUP_VERSION,
} from '@/domain/resourceBackup';
import type {
  MeasureRepository,
  PieceRepository,
  PromoRepository,
  ResourceRepository,
  ReviewRepository,
} from '@/repositories/contracts';
import { fail, ok, type OcrEngine, type ResourceService, type Result } from '@/services/contracts';

export interface ResourceServiceDeps {
  readonly repo: () => Promise<Result<ResourceRepository>>;
  /** Piezas que usan los recursos (para no borrar una imagen en uso y para el respaldo). */
  readonly pieces: () => Promise<Result<PieceRepository>>;
  readonly reviews: () => Promise<Result<ReviewRepository>>;
  readonly measures: () => Promise<Result<MeasureRepository>>;
  readonly promos: () => Promise<Result<PromoRepository>>;
  readonly engine: () => OcrEngine;
  readonly readSize: (
    blob: Blob,
  ) => Promise<{ readonly width: number; readonly height: number } | null>;
  readonly engineName: string;
  readonly writable: <T>(run: () => Promise<Result<T>>) => Promise<Result<T>>;
  readonly now?: () => Date;
  readonly newId?: () => string;
}

const toBase64 = (blob: Blob): Promise<string> =>
  new Promise((resolve, reject) => {
    const fr = new FileReader();
    fr.onload = () => resolve(String(fr.result).split(',')[1] ?? '');
    fr.onerror = () => reject(new Error('lectura'));
    fr.readAsDataURL(blob);
  });
const fromBase64 = (b64: string, type: string): Blob => {
  const bin = atob(b64);
  const bytes = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
  return new Blob([bytes], { type });
};
const sha256Hex = async (blob: Blob): Promise<string> =>
  [...new Uint8Array(await crypto.subtle.digest('SHA-256', await blob.arrayBuffer()))]
    .map((b) => b.toString(16).padStart(2, '0'))
    .join('');

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
    exportBackup: () =>
      withRepo(async (repo) => {
        type Out = { fileName: string; blob: Blob };
        const all = await repo.list();
        if (!all.ok) return fail<Out>(all.error.code, all.error.message);
        const pr = await deps.pieces();
        if (!pr.ok) return fail<Out>(pr.error.code, pr.error.message);
        const pieces = await pr.value.list();
        if (!pieces.ok) return fail<Out>(pieces.error.code, pieces.error.message);
        const rr = await deps.reviews();
        if (!rr.ok) return fail<Out>(rr.error.code, rr.error.message);
        const reviews = await rr.value.list();
        if (!reviews.ok) return fail<Out>(reviews.error.code, reviews.error.message);
        const mr = await deps.measures();
        if (!mr.ok) return fail<Out>(mr.error.code, mr.error.message);
        const measures = await mr.value.list();
        if (!measures.ok) return fail<Out>(measures.error.code, measures.error.message);
        const prr = await deps.promos();
        if (!prr.ok) return fail<Out>(prr.error.code, prr.error.message);
        const promos = await prr.value.list();
        if (!promos.ok) return fail<Out>(promos.error.code, promos.error.message);
        try {
          const parts: string[] = [
            `{"format":"${RESOURCES_BACKUP_FORMAT}","version":${String(RESOURCES_BACKUP_VERSION)},"exportedAt":"${now().toISOString()}","resources":[`,
          ];
          let first = true;
          for (const r of all.value) {
            const { blob, ...meta } = r;
            parts.push(
              (first ? '' : ',') +
                JSON.stringify({
                  ...meta,
                  sha256: await sha256Hex(blob),
                  data: await toBase64(blob),
                }),
            );
            first = false;
          }
          parts.push(
            `],"pieces":${JSON.stringify(pieces.value)},"reviews":${JSON.stringify(reviews.value)},"measures":${JSON.stringify(measures.value)},"promos":${JSON.stringify(promos.value)}}`,
          );
          return ok({
            fileName: backupFileName(now()),
            blob: new Blob(parts, { type: 'application/json' }),
          });
        } catch {
          return fail<Out>('storage_failed', 'No se pudo preparar el respaldo de imágenes.');
        }
      }),
    importBackup: (file) =>
      deps.writable(() =>
        withRepo(async (repo) => {
          type Out = {
            added: number;
            skipped: number;
            piecesAdded: number;
            reviewsAdded: number;
            measuresAdded: number;
            promosAdded: number;
          };
          const bad = (m: string) => fail<Out>('validation_error', m);
          if (file.size > RESOURCES_BACKUP_MAX_BYTES)
            return bad('El archivo supera el máximo permitido.');
          const parsed = parseResourcesBackup(await file.text());
          if (!parsed.ok) return bad(parsed.reason);
          const existing = await repo.list();
          if (!existing.ok) return fail<Out>(existing.error.code, existing.error.message);
          const pr = await deps.pieces();
          if (!pr.ok) return fail<Out>(pr.error.code, pr.error.message);
          const existingPieces = await pr.value.list();
          if (!existingPieces.ok)
            return fail<Out>(existingPieces.error.code, existingPieces.error.message);
          const rr = await deps.reviews();
          if (!rr.ok) return fail<Out>(rr.error.code, rr.error.message);
          const existingReviews = await rr.value.list();
          if (!existingReviews.ok)
            return fail<Out>(existingReviews.error.code, existingReviews.error.message);
          const haveReviews = new Set(existingReviews.value.map((r) => r.id));
          const newReviews = parsed.value.reviews.filter((r) => !haveReviews.has(r.id));
          const mr = await deps.measures();
          if (!mr.ok) return fail<Out>(mr.error.code, mr.error.message);
          const existingMeasures = await mr.value.list();
          if (!existingMeasures.ok)
            return fail<Out>(existingMeasures.error.code, existingMeasures.error.message);
          const haveMeasures = new Set(existingMeasures.value.map((r) => r.id));
          const newMeasures = parsed.value.measures.filter((r) => !haveMeasures.has(r.id));
          const prr = await deps.promos();
          if (!prr.ok) return fail<Out>(prr.error.code, prr.error.message);
          const existingPromos = await prr.value.list();
          if (!existingPromos.ok)
            return fail<Out>(existingPromos.error.code, existingPromos.error.message);
          const havePromos = new Set(existingPromos.value.map((r) => r.id));
          const newPromos = parsed.value.promos.filter((r) => !havePromos.has(r.id));
          const have = new Set(existing.value.map((r) => r.id));
          const records: ResourceRecord[] = [];
          for (const e of parsed.value.resources) {
            if (have.has(String(e.raw['id']))) continue;
            let blob: Blob;
            try {
              blob = fromBase64(e.data, String(e.raw['mime']));
            } catch {
              return bad('Una imagen del respaldo está dañada.');
            }
            if ((await sha256Hex(blob)) !== e.sha256)
              return bad('Una imagen del respaldo está dañada (la huella no coincide).');
            const v = validateResourceRecord({ ...e.raw, blob });
            if (!v.ok || v.value.size !== blob.size)
              return bad('Una imagen del respaldo no es válida.');
            records.push(v.value);
          }
          if (existing.value.length + records.length > RESOURCE_LIMITS.maxResources)
            return bad(
              `Se superaría el máximo de ${String(RESOURCE_LIMITS.maxResources)} recursos.`,
            );
          const known = new Set([...have, ...records.map((r) => r.id)]);
          const havePieces = new Set(existingPieces.value.map((p) => p.id));
          const newPieces = parsed.value.pieces.filter(
            (p) => !havePieces.has(p.id) && known.has(p.resourceId),
          );
          // Todo se validó antes de escribir: o se agrega lo que falta o no se toca nada.
          for (const r of records) {
            const p = await repo.put(r);
            if (!p.ok) return fail<Out>(p.error.code, p.error.message);
          }
          for (const p of newPieces) {
            const w = await pr.value.put(p);
            if (!w.ok) return fail<Out>(w.error.code, w.error.message);
          }
          for (const r of newReviews) {
            const w = await rr.value.put(r);
            if (!w.ok) return fail<Out>(w.error.code, w.error.message);
          }
          for (const r of newMeasures) {
            const w = await mr.value.put(r);
            if (!w.ok) return fail<Out>(w.error.code, w.error.message);
          }
          for (const r of newPromos) {
            const w = await prr.value.put(r);
            if (!w.ok) return fail<Out>(w.error.code, w.error.message);
          }
          return ok({
            measuresAdded: newMeasures.length,
            promosAdded: newPromos.length,
            reviewsAdded: newReviews.length,
            added: records.length,
            skipped: parsed.value.resources.length - records.length,
            piecesAdded: newPieces.length,
          });
        }),
      ),
    counts: async () => {
      const r = await withRepo((repo) => repo.count());
      if (!r.ok) return fail(r.error.code, r.error.message);
      const pr = await deps.pieces();
      if (!pr.ok) return fail(pr.error.code, pr.error.message);
      const p = await pr.value.count();
      if (!p.ok) return fail(p.error.code, p.error.message);
      const rr = await deps.reviews();
      if (!rr.ok) return fail(rr.error.code, rr.error.message);
      const rv = await rr.value.count();
      if (!rv.ok) return fail(rv.error.code, rv.error.message);
      const mr = await deps.measures();
      if (!mr.ok) return fail(mr.error.code, mr.error.message);
      const m = await mr.value.count();
      if (!m.ok) return fail(m.error.code, m.error.message);
      const prr = await deps.promos();
      if (!prr.ok) return fail(prr.error.code, prr.error.message);
      const pm = await prr.value.count();
      if (!pm.ok) return fail(pm.error.code, pm.error.message);
      return ok({
        resources: r.value,
        pieces: p.value,
        reviews: rv.value,
        measures: m.value,
        promos: pm.value,
      });
    },
    remove: (id) =>
      deps.writable(async () => {
        const pr = await deps.pieces();
        if (!pr.ok) return fail<never>(pr.error.code, pr.error.message);
        const used = await pr.value.list();
        if (!used.ok) return fail<never>(used.error.code, used.error.message);
        if (used.value.some((p) => p.resourceId === id))
          return fail<never>(
            'conflict',
            'Esta imagen la usa una pieza creativa. Elimina primero la pieza.',
          );
        return withRepo((r) => r.remove(id));
      }),
  };
}
