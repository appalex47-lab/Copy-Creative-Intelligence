import { validateSnapshot } from '@/domain/backup';
import { classifyStorageError } from '@/adapters/persistenceErrors';
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
import {
  REVIEW_ID,
  compareReviewsNewestFirst,
  validateReviewRecord,
  type ReviewRecord,
} from '@/domain/review';
import {
  MEASURE_ID,
  compareMeasuresNewestFirst,
  validateMeasureRecord,
  type MeasureRecord,
} from '@/domain/measure';
import {
  PROMO_ID,
  comparePromosByName,
  validatePromoRecord,
  type PromoRecord,
} from '@/domain/promo';
import {
  PIECE_ID,
  comparePiecesNewestFirst,
  validatePieceRecord,
  type PieceRecord,
} from '@/domain/piece';
import {
  RESOURCE_ID,
  compareResourcesNewestFirst,
  validateResourceRecord,
  type ResourceRecord,
} from '@/domain/resource';
import { validateRulesDoc, type RulesDoc } from '@/domain/rulesConfig';
import { validateDisplayName, parseLocalProfile, type LocalProfile } from '@/domain/profile';
import { compareNewestFirst, normalizeLimit, type Repositories } from '@/repositories/contracts';
import { fail, ok, type Result } from '@/services/contracts';

export const DEFAULT_DB_NAME = 'cci';
const STORE_ACTIVITY = 'activity';
const STORE_PROFILE = 'profile';
const STORE_META = 'meta';
const STORE_BRIEFS = 'briefs';
const STORE_COPIES = 'copies';
const STORE_RULES = 'rules';
const STORE_ENTITIES = 'entities';
const STORE_ADAPTATIONS = 'adaptations';
const STORE_AUDITS = 'audits';
const STORE_RESOURCES = 'resources';
const STORE_PIECES = 'pieces';
const STORE_REVIEWS = 'reviews';
const STORE_MEASURES = 'measures';
const STORE_PROMOS = 'promos';
const RULES_KEY = 'config';
const PROFILE_KEY = 'local';

/** Un paso de migración: se ejecuta dentro de la transacción `versionchange`; si lanza, TODO se revierte. */
export type MigrationStep = (db: IDBDatabase, tx: IDBTransaction) => void;

/**
 * Migraciones en orden. El índice + 1 es la versión a la que llega cada paso.
 * v0 → v1: instalación nueva (v0 = no existe la base): crea los tres almacenes y el índice por fecha.
 * v1 → v2 (SUPUESTO técnico de Claude, S1-D13, reversible): añade el índice `kind` en `activity` para filtrar por tipo
 * sin recorrer todo; no agrega atributos de negocio y conserva todos los datos.
 * v2 → v3 (S2.2): crea el almacén `briefs` (clave `id`, índice `updatedAt`); no toca los datos existentes.
 * v3 → v4 (S2.4): crea el almacén `copies` (clave `id`, índices `briefId` y `updatedAt`); no toca datos existentes.
 * v4 → v5 (S2.5b): crea el almacén `rules` (un solo documento con clave `config`: leyendas y términos de marca).
 * v5 → v6 (S2.8): crea `entities` (campañas, productos y ofertas; índice `kind`) y `adaptations` (índice `copyId`).
 * v6 → v7 (S3.1): crea `audits` (auditorías guardadas; índice `copyId`).
 * v10 → v11 (S4.2): crea `measures` (resultados y experimentos) y `promos` (promociones). Tampoco van en el respaldo JSON.
 * v9 → v10 (S4.1): crea `reviews` (revisiones de calidad; índice `updatedAt`). Tampoco van en el respaldo JSON de datos.
 * v8 → v9 (S3.4): crea `pieces` (piezas creativas con sus auditorías; índice `updatedAt`). Tampoco van en el respaldo JSON.
 * v7 → v8 (S3.3): crea `resources` (imágenes con su OCR; índice `createdAt`). No van en el respaldo JSON.
 */
export const MIGRATIONS: readonly MigrationStep[] = [
  (db) => {
    db.createObjectStore(STORE_META);
    db.createObjectStore(STORE_PROFILE);
    db.createObjectStore(STORE_ACTIVITY, { keyPath: 'id' }).createIndex('at', 'at');
  },
  (_db, tx) => {
    tx.objectStore(STORE_ACTIVITY).createIndex('kind', 'kind');
  },
  (db) => {
    db.createObjectStore(STORE_BRIEFS, { keyPath: 'id' }).createIndex('updatedAt', 'updatedAt');
  },
  (db) => {
    const store = db.createObjectStore(STORE_COPIES, { keyPath: 'id' });
    store.createIndex('briefId', 'briefId');
    store.createIndex('updatedAt', 'updatedAt');
  },
  (db) => {
    db.createObjectStore(STORE_RULES);
  },
  (db) => {
    db.createObjectStore(STORE_ENTITIES, { keyPath: 'id' }).createIndex('kind', 'kind');
    const ad = db.createObjectStore(STORE_ADAPTATIONS, { keyPath: 'id' });
    ad.createIndex('copyId', 'copyId');
    ad.createIndex('updatedAt', 'updatedAt');
  },
  (db) => {
    db.createObjectStore(STORE_AUDITS, { keyPath: 'id' }).createIndex('copyId', 'copyId');
  },
  (db) => {
    db.createObjectStore(STORE_RESOURCES, { keyPath: 'id' }).createIndex('createdAt', 'createdAt');
  },
  (db) => {
    db.createObjectStore(STORE_PIECES, { keyPath: 'id' }).createIndex('updatedAt', 'updatedAt');
  },
  (db) => {
    db.createObjectStore(STORE_REVIEWS, { keyPath: 'id' }).createIndex('updatedAt', 'updatedAt');
  },
  (db) => {
    db.createObjectStore(STORE_MEASURES, { keyPath: 'id' });
    db.createObjectStore(STORE_PROMOS, { keyPath: 'id' });
  },
];

/** Versión de esquema vigente = número de migraciones. */
export const SCHEMA_VERSION = MIGRATIONS.length;

export const NEWER_SCHEMA_MESSAGE =
  'La base local fue creada por una versión más reciente de la aplicación; no se modificó.';

const UNAVAILABLE = 'El almacenamiento local no está disponible.';

const promisify = <T>(req: IDBRequest<T>): Promise<T> =>
  new Promise((resolve, reject) => {
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error ?? new Error('IDBRequest'));
  });

const txDone = (tx: IDBTransaction): Promise<void> =>
  new Promise((resolve, reject) => {
    tx.oncomplete = () => resolve();
    tx.onerror = () => reject(tx.error ?? new Error('IDBTransaction'));
    tx.onabort = () => reject(tx.error ?? new Error('IDBTransactionAbort'));
  });

/**
 * Abre la base y aplica las migraciones pendientes desde la versión guardada hasta la última.
 * - Si la base tiene una versión MAYOR que la de este código, se rechaza SIN escribir nada (VersionError).
 * - Si una migración falla, la transacción se aborta y la base queda en su versión anterior con sus datos intactos.
 */
export function openDatabase(
  name = DEFAULT_DB_NAME,
  migrations: readonly MigrationStep[] = MIGRATIONS,
): Promise<Result<IDBDatabase>> {
  return new Promise((resolve) => {
    if (typeof indexedDB === 'undefined') {
      resolve(fail('storage_unavailable', UNAVAILABLE));
      return;
    }
    let req: IDBOpenDBRequest;
    try {
      req = indexedDB.open(name, migrations.length);
    } catch (e) {
      resolve(
        fail(
          classifyStorageError(e) === 'storage_failed'
            ? 'storage_unavailable'
            : classifyStorageError(e),
          UNAVAILABLE,
        ),
      );
      return;
    }
    req.onupgradeneeded = (event) => {
      const tx = req.transaction;
      if (!tx) return;
      try {
        for (let v = event.oldVersion; v < migrations.length; v++) migrations[v]?.(req.result, tx);
        tx.objectStore(STORE_META).put(migrations.length, 'schemaVersion');
      } catch {
        tx.abort(); // sin estado parcial: la base conserva su versión y datos anteriores
      }
    };
    req.onsuccess = () => resolve(ok(req.result));
    req.onerror = () => {
      const code = classifyStorageError(req.error);
      resolve(fail(code, code === 'storage_newer_schema' ? NEWER_SCHEMA_MESSAGE : UNAVAILABLE));
    };
    req.onblocked = () => resolve(fail('storage_blocked', UNAVAILABLE));
  });
}

/** Borra una base (uso en pruebas y en un futuro «borrar datos»). */
export function deleteDatabase(name: string): Promise<void> {
  return new Promise((resolve) => {
    const req = indexedDB.deleteDatabase(name);
    req.onsuccess = () => resolve();
    req.onerror = () => resolve();
    req.onblocked = () => resolve();
  });
}

async function guard<T>(run: () => Promise<Result<T>>): Promise<Result<T>> {
  try {
    return await run();
  } catch (e) {
    return fail(classifyStorageError(e), UNAVAILABLE); // sin detalle interno hacia la interfaz
  }
}

/** Repositorios sobre una base ya abierta. */
export function createIndexedDbRepositories(db: IDBDatabase): Repositories {
  const profileFrom = async (): Promise<LocalProfile> => {
    const tx = db.transaction(STORE_PROFILE, 'readonly');
    const raw: unknown = await promisify(tx.objectStore(STORE_PROFILE).get(PROFILE_KEY));
    return parseLocalProfile(raw);
  };
  const rulesFrom = async (): Promise<RulesDoc | null> => {
    const tx = db.transaction(STORE_RULES, 'readonly');
    const raw = await promisify<unknown>(tx.objectStore(STORE_RULES).get(RULES_KEY));
    if (raw === undefined) return null;
    const v = validateRulesDoc(raw);
    return v.ok ? v.value : null; // un documento dañado se trata como «sin configuración»; no rompe la pantalla
  };
  return {
    activity: {
      add: (raw) =>
        guard(async () => {
          const v = validateActivityEvent(raw);
          if (!v.ok) return fail('validation_error', v.reason);
          const tx = db.transaction(STORE_ACTIVITY, 'readwrite');
          tx.objectStore(STORE_ACTIVITY).put(v.value);
          await txDone(tx);
          return ok(v.value);
        }),
      listRecent: (limit) =>
        guard(async () => {
          const n = normalizeLimit(limit);
          if (n === null) return fail('validation_error', 'Límite inválido.');
          const tx = db.transaction(STORE_ACTIVITY, 'readonly');
          const out: ActivityEvent[] = [];
          await new Promise<void>((resolve, reject) => {
            const req = tx.objectStore(STORE_ACTIVITY).index('at').openCursor(null, 'prev');
            req.onerror = () => reject(req.error ?? new Error('cursor'));
            req.onsuccess = () => {
              const cur = req.result;
              if (!cur || out.length >= n) return resolve();
              const v = validateActivityEvent(cur.value);
              if (v.ok) out.push(v.value); // un registro corrupto se omite; no rompe la lista
              cur.continue();
            };
          });
          return ok(out);
        }),
      count: () =>
        guard(async () => {
          const tx = db.transaction(STORE_ACTIVITY, 'readonly');
          return ok(await promisify(tx.objectStore(STORE_ACTIVITY).count()));
        }),
    },
    briefs: {
      put: (raw) =>
        guard(async () => {
          const v = validateBriefRecord(raw);
          if (!v.ok) return fail('validation_error', v.reason);
          const tx = db.transaction(STORE_BRIEFS, 'readwrite');
          tx.objectStore(STORE_BRIEFS).put(v.value);
          await txDone(tx);
          return ok(v.value);
        }),
      get: (id) =>
        guard(async () => {
          if (!BRIEF_ID.test(id))
            return fail('validation_error', 'Identificador de brief no válido.');
          const tx = db.transaction(STORE_BRIEFS, 'readonly');
          const v = validateBriefRecord(
            await promisify<unknown>(tx.objectStore(STORE_BRIEFS).get(id)),
          );
          return v.ok ? ok(v.value) : fail('validation_error', 'El brief no existe.');
        }),
      list: () =>
        guard(async () => {
          const tx = db.transaction(STORE_BRIEFS, 'readonly');
          const raw = await promisify<unknown[]>(tx.objectStore(STORE_BRIEFS).getAll());
          const out: BriefRecord[] = [];
          for (const item of raw) {
            const v = validateBriefRecord(item);
            if (v.ok) out.push(v.value); // un registro corrupto se omite; no rompe la lista
          }
          return ok(out.sort(compareBriefsNewestFirst));
        }),
      remove: (id) =>
        guard(async () => {
          if (!BRIEF_ID.test(id))
            return fail('validation_error', 'Identificador de brief no válido.');
          const tx = db.transaction(STORE_BRIEFS, 'readwrite');
          tx.objectStore(STORE_BRIEFS).delete(id);
          await txDone(tx);
          return ok(undefined);
        }),
      count: () =>
        guard(async () => {
          const tx = db.transaction(STORE_BRIEFS, 'readonly');
          return ok(await promisify(tx.objectStore(STORE_BRIEFS).count()));
        }),
    },
    copies: {
      put: (raw) =>
        guard(async () => {
          const v = validateCopyRecord(raw);
          if (!v.ok) return fail('validation_error', v.reason);
          const tx = db.transaction(STORE_COPIES, 'readwrite');
          tx.objectStore(STORE_COPIES).put(v.value);
          await txDone(tx);
          return ok(v.value);
        }),
      get: (id) =>
        guard(async () => {
          if (!COPY_ID.test(id))
            return fail('validation_error', 'Identificador de copy no válido.');
          const tx = db.transaction(STORE_COPIES, 'readonly');
          const v = validateCopyRecord(
            await promisify<unknown>(tx.objectStore(STORE_COPIES).get(id)),
          );
          return v.ok ? ok(v.value) : fail('validation_error', 'El copy no existe.');
        }),
      list: (briefId) =>
        guard(async () => {
          const tx = db.transaction(STORE_COPIES, 'readonly');
          const store = tx.objectStore(STORE_COPIES);
          const raw = await promisify<unknown[]>(
            briefId === undefined ? store.getAll() : store.index('briefId').getAll(briefId),
          );
          const out: CopyRecord[] = [];
          for (const item of raw) {
            const v = validateCopyRecord(item);
            if (v.ok) out.push(v.value); // un registro corrupto se omite; no rompe la lista
          }
          return ok(out.sort(compareCopiesNewestFirst));
        }),
      remove: (id) =>
        guard(async () => {
          if (!COPY_ID.test(id))
            return fail('validation_error', 'Identificador de copy no válido.');
          const tx = db.transaction(STORE_COPIES, 'readwrite');
          tx.objectStore(STORE_COPIES).delete(id);
          await txDone(tx);
          return ok(undefined);
        }),
      count: () =>
        guard(async () => {
          const tx = db.transaction(STORE_COPIES, 'readonly');
          return ok(await promisify(tx.objectStore(STORE_COPIES).count()));
        }),
    },
    entities: {
      put: (raw) =>
        guard(async () => {
          const v = validateEntityRecord(raw);
          if (!v.ok) return fail('validation_error', v.reason);
          const tx = db.transaction(STORE_ENTITIES, 'readwrite');
          tx.objectStore(STORE_ENTITIES).put(v.value);
          await txDone(tx);
          return ok(v.value);
        }),
      get: (id) =>
        guard(async () => {
          if (!ENTITY_ID.test(id)) return fail('validation_error', 'Identificador no válido.');
          const tx = db.transaction(STORE_ENTITIES, 'readonly');
          const v = validateEntityRecord(
            await promisify<unknown>(tx.objectStore(STORE_ENTITIES).get(id)),
          );
          return v.ok ? ok(v.value) : fail('validation_error', 'El registro no existe.');
        }),
      list: (kind) =>
        guard(async () => {
          const tx = db.transaction(STORE_ENTITIES, 'readonly');
          const store = tx.objectStore(STORE_ENTITIES);
          const raw = await promisify<unknown[]>(
            kind === undefined ? store.getAll() : store.index('kind').getAll(kind),
          );
          const out: EntityRecord[] = [];
          for (const item of raw) {
            const v = validateEntityRecord(item);
            if (v.ok) out.push(v.value);
          }
          return ok(out.sort(compareEntities));
        }),
      remove: (id) =>
        guard(async () => {
          if (!ENTITY_ID.test(id)) return fail('validation_error', 'Identificador no válido.');
          const tx = db.transaction(STORE_ENTITIES, 'readwrite');
          tx.objectStore(STORE_ENTITIES).delete(id);
          await txDone(tx);
          return ok(undefined);
        }),
    },
    adaptations: {
      put: (raw) =>
        guard(async () => {
          const v = validateAdaptationRecord(raw);
          if (!v.ok) return fail('validation_error', v.reason);
          const tx = db.transaction(STORE_ADAPTATIONS, 'readwrite');
          tx.objectStore(STORE_ADAPTATIONS).put(v.value);
          await txDone(tx);
          return ok(v.value);
        }),
      get: (id) =>
        guard(async () => {
          if (!ADAPTATION_ID.test(id)) return fail('validation_error', 'Identificador no válido.');
          const tx = db.transaction(STORE_ADAPTATIONS, 'readonly');
          const v = validateAdaptationRecord(
            await promisify<unknown>(tx.objectStore(STORE_ADAPTATIONS).get(id)),
          );
          return v.ok ? ok(v.value) : fail('validation_error', 'La adaptación no existe.');
        }),
      list: (copyId) =>
        guard(async () => {
          const tx = db.transaction(STORE_ADAPTATIONS, 'readonly');
          const store = tx.objectStore(STORE_ADAPTATIONS);
          const raw = await promisify<unknown[]>(
            copyId === undefined ? store.getAll() : store.index('copyId').getAll(copyId),
          );
          const out: AdaptationRecord[] = [];
          for (const item of raw) {
            const v = validateAdaptationRecord(item);
            if (v.ok) out.push(v.value);
          }
          return ok(out.sort(compareAdaptationsNewestFirst));
        }),
      remove: (id) =>
        guard(async () => {
          if (!ADAPTATION_ID.test(id)) return fail('validation_error', 'Identificador no válido.');
          const tx = db.transaction(STORE_ADAPTATIONS, 'readwrite');
          tx.objectStore(STORE_ADAPTATIONS).delete(id);
          await txDone(tx);
          return ok(undefined);
        }),
      count: () =>
        guard(async () => {
          const tx = db.transaction(STORE_ADAPTATIONS, 'readonly');
          return ok(await promisify(tx.objectStore(STORE_ADAPTATIONS).count()));
        }),
    },
    reviews: {
      put: (raw) =>
        guard(async () => {
          const v = validateReviewRecord(raw);
          if (!v.ok) return fail('validation_error', v.reason);
          const tx = db.transaction(STORE_REVIEWS, 'readwrite');
          tx.objectStore(STORE_REVIEWS).put(v.value);
          await txDone(tx);
          return ok(v.value);
        }),
      get: (id) =>
        guard(async () => {
          if (!REVIEW_ID.test(id)) return fail('validation_error', 'Identificador no válido.');
          const tx = db.transaction(STORE_REVIEWS, 'readonly');
          const v = validateReviewRecord(
            await promisify<unknown>(tx.objectStore(STORE_REVIEWS).get(id)),
          );
          return v.ok ? ok(v.value) : fail('not_found', 'La revisión no existe.');
        }),
      list: () =>
        guard(async () => {
          const tx = db.transaction(STORE_REVIEWS, 'readonly');
          const raw = await promisify<unknown[]>(tx.objectStore(STORE_REVIEWS).getAll());
          const out: ReviewRecord[] = [];
          for (const item of raw) {
            const v = validateReviewRecord(item);
            if (v.ok) out.push(v.value);
          }
          return ok(out.sort(compareReviewsNewestFirst));
        }),
      remove: (id) =>
        guard(async () => {
          if (!REVIEW_ID.test(id)) return fail('validation_error', 'Identificador no válido.');
          const tx = db.transaction(STORE_REVIEWS, 'readwrite');
          tx.objectStore(STORE_REVIEWS).delete(id);
          await txDone(tx);
          return ok(undefined);
        }),
      count: () =>
        guard(async () => {
          const tx = db.transaction(STORE_REVIEWS, 'readonly');
          return ok(await promisify(tx.objectStore(STORE_REVIEWS).count()));
        }),
    },
    measures: {
      put: (raw) =>
        guard(async () => {
          const v = validateMeasureRecord(raw);
          if (!v.ok) return fail('validation_error', v.reason);
          const tx = db.transaction(STORE_MEASURES, 'readwrite');
          tx.objectStore(STORE_MEASURES).put(v.value);
          await txDone(tx);
          return ok(v.value);
        }),
      get: (id) =>
        guard(async () => {
          if (!MEASURE_ID.test(id)) return fail('validation_error', 'Identificador no válido.');
          const tx = db.transaction(STORE_MEASURES, 'readonly');
          const v = validateMeasureRecord(
            await promisify<unknown>(tx.objectStore(STORE_MEASURES).get(id)),
          );
          return v.ok ? ok(v.value) : fail('not_found', 'La medición no existe.');
        }),
      list: () =>
        guard(async () => {
          const tx = db.transaction(STORE_MEASURES, 'readonly');
          const raw = await promisify<unknown[]>(tx.objectStore(STORE_MEASURES).getAll());
          const out: MeasureRecord[] = [];
          for (const item of raw) {
            const v = validateMeasureRecord(item);
            if (v.ok) out.push(v.value);
          }
          return ok(out.sort(compareMeasuresNewestFirst));
        }),
      remove: (id) =>
        guard(async () => {
          if (!MEASURE_ID.test(id)) return fail('validation_error', 'Identificador no válido.');
          const tx = db.transaction(STORE_MEASURES, 'readwrite');
          tx.objectStore(STORE_MEASURES).delete(id);
          await txDone(tx);
          return ok(undefined);
        }),
      count: () =>
        guard(async () => {
          const tx = db.transaction(STORE_MEASURES, 'readonly');
          return ok(await promisify(tx.objectStore(STORE_MEASURES).count()));
        }),
    },
    promos: {
      put: (raw) =>
        guard(async () => {
          const v = validatePromoRecord(raw);
          if (!v.ok) return fail('validation_error', v.reason);
          const tx = db.transaction(STORE_PROMOS, 'readwrite');
          tx.objectStore(STORE_PROMOS).put(v.value);
          await txDone(tx);
          return ok(v.value);
        }),
      get: (id) =>
        guard(async () => {
          if (!PROMO_ID.test(id)) return fail('validation_error', 'Identificador no válido.');
          const tx = db.transaction(STORE_PROMOS, 'readonly');
          const v = validatePromoRecord(
            await promisify<unknown>(tx.objectStore(STORE_PROMOS).get(id)),
          );
          return v.ok ? ok(v.value) : fail('not_found', 'La promoción no existe.');
        }),
      list: () =>
        guard(async () => {
          const tx = db.transaction(STORE_PROMOS, 'readonly');
          const raw = await promisify<unknown[]>(tx.objectStore(STORE_PROMOS).getAll());
          const out: PromoRecord[] = [];
          for (const item of raw) {
            const v = validatePromoRecord(item);
            if (v.ok) out.push(v.value);
          }
          return ok(out.sort(comparePromosByName));
        }),
      remove: (id) =>
        guard(async () => {
          if (!PROMO_ID.test(id)) return fail('validation_error', 'Identificador no válido.');
          const tx = db.transaction(STORE_PROMOS, 'readwrite');
          tx.objectStore(STORE_PROMOS).delete(id);
          await txDone(tx);
          return ok(undefined);
        }),
      count: () =>
        guard(async () => {
          const tx = db.transaction(STORE_PROMOS, 'readonly');
          return ok(await promisify(tx.objectStore(STORE_PROMOS).count()));
        }),
    },
    pieces: {
      put: (raw) =>
        guard(async () => {
          const v = validatePieceRecord(raw);
          if (!v.ok) return fail('validation_error', v.reason);
          const tx = db.transaction(STORE_PIECES, 'readwrite');
          tx.objectStore(STORE_PIECES).put(v.value);
          await txDone(tx);
          return ok(v.value);
        }),
      get: (id) =>
        guard(async () => {
          if (!PIECE_ID.test(id)) return fail('validation_error', 'Identificador no válido.');
          const tx = db.transaction(STORE_PIECES, 'readonly');
          const v = validatePieceRecord(
            await promisify<unknown>(tx.objectStore(STORE_PIECES).get(id)),
          );
          return v.ok ? ok(v.value) : fail('not_found', 'La pieza no existe.');
        }),
      list: () =>
        guard(async () => {
          const tx = db.transaction(STORE_PIECES, 'readonly');
          const raw = await promisify<unknown[]>(tx.objectStore(STORE_PIECES).getAll());
          const out: PieceRecord[] = [];
          for (const item of raw) {
            const v = validatePieceRecord(item);
            if (v.ok) out.push(v.value);
          }
          return ok(out.sort(comparePiecesNewestFirst));
        }),
      remove: (id) =>
        guard(async () => {
          if (!PIECE_ID.test(id)) return fail('validation_error', 'Identificador no válido.');
          const tx = db.transaction(STORE_PIECES, 'readwrite');
          tx.objectStore(STORE_PIECES).delete(id);
          await txDone(tx);
          return ok(undefined);
        }),
      count: () =>
        guard(async () => {
          const tx = db.transaction(STORE_PIECES, 'readonly');
          return ok(await promisify(tx.objectStore(STORE_PIECES).count()));
        }),
    },
    resources: {
      put: (raw) =>
        guard(async () => {
          const v = validateResourceRecord(raw);
          if (!v.ok) return fail('validation_error', v.reason);
          const tx = db.transaction(STORE_RESOURCES, 'readwrite');
          tx.objectStore(STORE_RESOURCES).put(v.value);
          await txDone(tx);
          return ok(v.value);
        }),
      get: (id) =>
        guard(async () => {
          if (!RESOURCE_ID.test(id)) return fail('validation_error', 'Identificador no válido.');
          const tx = db.transaction(STORE_RESOURCES, 'readonly');
          const v = validateResourceRecord(
            await promisify<unknown>(tx.objectStore(STORE_RESOURCES).get(id)),
          );
          return v.ok ? ok(v.value) : fail('not_found', 'El recurso no existe.');
        }),
      list: () =>
        guard(async () => {
          const tx = db.transaction(STORE_RESOURCES, 'readonly');
          const raw = await promisify<unknown[]>(tx.objectStore(STORE_RESOURCES).getAll());
          const out: ResourceRecord[] = [];
          for (const item of raw) {
            const v = validateResourceRecord(item);
            if (v.ok) out.push(v.value);
          }
          return ok(out.sort(compareResourcesNewestFirst));
        }),
      remove: (id) =>
        guard(async () => {
          if (!RESOURCE_ID.test(id)) return fail('validation_error', 'Identificador no válido.');
          const tx = db.transaction(STORE_RESOURCES, 'readwrite');
          tx.objectStore(STORE_RESOURCES).delete(id);
          await txDone(tx);
          return ok(undefined);
        }),
      count: () =>
        guard(async () => {
          const tx = db.transaction(STORE_RESOURCES, 'readonly');
          return ok(await promisify(tx.objectStore(STORE_RESOURCES).count()));
        }),
    },
    audits: {
      put: (raw) =>
        guard(async () => {
          const v = validateAuditRecord(raw);
          if (!v.ok) return fail('validation_error', v.reason);
          const tx = db.transaction(STORE_AUDITS, 'readwrite');
          tx.objectStore(STORE_AUDITS).put(v.value);
          await txDone(tx);
          return ok(v.value);
        }),
      get: (id) =>
        guard(async () => {
          if (!AUDIT_ID.test(id)) return fail('validation_error', 'Identificador no válido.');
          const tx = db.transaction(STORE_AUDITS, 'readonly');
          const v = validateAuditRecord(
            await promisify<unknown>(tx.objectStore(STORE_AUDITS).get(id)),
          );
          return v.ok ? ok(v.value) : fail('validation_error', 'La auditoría no existe.');
        }),
      list: (copyId) =>
        guard(async () => {
          const tx = db.transaction(STORE_AUDITS, 'readonly');
          const store = tx.objectStore(STORE_AUDITS);
          const raw = await promisify<unknown[]>(
            copyId === undefined ? store.getAll() : store.index('copyId').getAll(copyId),
          );
          const out: AuditRecord[] = [];
          for (const item of raw) {
            const v = validateAuditRecord(item);
            if (v.ok) out.push(v.value);
          }
          return ok(out.sort(compareAuditsNewestFirst));
        }),
      remove: (id) =>
        guard(async () => {
          if (!AUDIT_ID.test(id)) return fail('validation_error', 'Identificador no válido.');
          const tx = db.transaction(STORE_AUDITS, 'readwrite');
          tx.objectStore(STORE_AUDITS).delete(id);
          await txDone(tx);
          return ok(undefined);
        }),
      count: () =>
        guard(async () => {
          const tx = db.transaction(STORE_AUDITS, 'readonly');
          return ok(await promisify(tx.objectStore(STORE_AUDITS).count()));
        }),
    },
    rules: {
      get: () => guard(async () => ok(await rulesFrom())),
      save: (raw) =>
        guard(async () => {
          const v = validateRulesDoc(raw);
          if (!v.ok) return fail('validation_error', v.reason);
          const tx = db.transaction(STORE_RULES, 'readwrite');
          tx.objectStore(STORE_RULES).put(v.value, RULES_KEY);
          await txDone(tx);
          return ok(v.value);
        }),
      clear: () =>
        guard(async () => {
          const tx = db.transaction(STORE_RULES, 'readwrite');
          tx.objectStore(STORE_RULES).delete(RULES_KEY);
          await txDone(tx);
          return ok(undefined);
        }),
    },
    profile: {
      get: () => guard(async () => ok(await profileFrom())),
      save: (displayName) =>
        guard(async () => {
          const v = validateDisplayName(displayName);
          if (!v.ok) return fail('validation_error', v.reason);
          const tx = db.transaction(STORE_PROFILE, 'readwrite');
          const store = tx.objectStore(STORE_PROFILE);
          if (v.value === undefined) store.delete(PROFILE_KEY);
          else store.put({ displayName: v.value }, PROFILE_KEY);
          await txDone(tx);
          return ok(await profileFrom());
        }),
      clear: () =>
        guard(async () => {
          const tx = db.transaction(STORE_PROFILE, 'readwrite');
          tx.objectStore(STORE_PROFILE).delete(PROFILE_KEY);
          await txDone(tx);
          return ok<LocalProfile>({});
        }),
    },
    backup: {
      exportAll: () =>
        guard(async () => {
          const tx = db.transaction(
            [
              STORE_ACTIVITY,
              STORE_PROFILE,
              STORE_BRIEFS,
              STORE_COPIES,
              STORE_RULES,
              STORE_ENTITIES,
              STORE_ADAPTATIONS,
              STORE_AUDITS,
            ],
            'readonly',
          ); // una sola lectura consistente
          const [
            rawEvents,
            rawProfile,
            rawBriefs,
            rawCopies,
            rawRules,
            rawEntities,
            rawAdaptations,
            rawAudits,
          ] = await Promise.all([
            promisify<unknown[]>(tx.objectStore(STORE_ACTIVITY).getAll()),
            promisify<unknown>(tx.objectStore(STORE_PROFILE).get(PROFILE_KEY)),
            promisify<unknown[]>(tx.objectStore(STORE_BRIEFS).getAll()),
            promisify<unknown[]>(tx.objectStore(STORE_COPIES).getAll()),
            promisify<unknown>(tx.objectStore(STORE_RULES).get(RULES_KEY)),
            promisify<unknown[]>(tx.objectStore(STORE_ENTITIES).getAll()),
            promisify<unknown[]>(tx.objectStore(STORE_ADAPTATIONS).getAll()),
            promisify<unknown[]>(tx.objectStore(STORE_AUDITS).getAll()),
          ]);
          const rulesParsed = rawRules === undefined ? undefined : validateRulesDoc(rawRules);
          const rules = rulesParsed?.ok ? rulesParsed.value : null;
          const entities: EntityRecord[] = [];
          for (const item of rawEntities) {
            const e = validateEntityRecord(item);
            if (e.ok) entities.push(e.value);
          }
          entities.sort(compareEntities);
          const adaptations: AdaptationRecord[] = [];
          for (const item of rawAdaptations) {
            const a = validateAdaptationRecord(item);
            if (a.ok) adaptations.push(a.value);
          }
          adaptations.sort(compareAdaptationsNewestFirst);
          const audits: AuditRecord[] = [];
          for (const item of rawAudits) {
            const a = validateAuditRecord(item);
            if (a.ok) audits.push(a.value);
          }
          audits.sort(compareAuditsNewestFirst);
          const copies: CopyRecord[] = [];
          for (const item of rawCopies) {
            const c = validateCopyRecord(item);
            if (c.ok) copies.push(c.value);
          }
          copies.sort(compareCopiesNewestFirst);
          const briefs: BriefRecord[] = [];
          for (const item of rawBriefs) {
            const b = validateBriefRecord(item);
            if (b.ok) briefs.push(b.value);
          }
          briefs.sort(compareBriefsNewestFirst);
          const activity: ActivityEvent[] = [];
          for (const item of rawEvents) {
            const v = validateActivityEvent(item);
            if (v.ok) activity.push(v.value); // un registro corrupto no se exporta
          }
          activity.sort(compareNewestFirst);
          return ok({
            profile: parseLocalProfile(rawProfile),
            activity,
            briefs,
            copies,
            rules,
            entities,
            adaptations,
            audits,
          });
        }),
      replaceAll: (raw) =>
        guard(async () => {
          const v = validateSnapshot(raw); // se valida TODO antes de tocar la base
          if (!v.ok) return fail('validation_error', v.reason);
          const tx = db.transaction(
            [
              STORE_ACTIVITY,
              STORE_PROFILE,
              STORE_BRIEFS,
              STORE_COPIES,
              STORE_RULES,
              STORE_ENTITIES,
              STORE_ADAPTATIONS,
              STORE_AUDITS,
            ],
            'readwrite',
          );
          const done = txDone(tx);
          try {
            const events = tx.objectStore(STORE_ACTIVITY);
            const profile = tx.objectStore(STORE_PROFILE);
            events.clear();
            tx.objectStore(STORE_BRIEFS).clear();
            tx.objectStore(STORE_COPIES).clear();
            tx.objectStore(STORE_RULES).clear();
            tx.objectStore(STORE_ENTITIES).clear();
            tx.objectStore(STORE_ADAPTATIONS).clear();
            tx.objectStore(STORE_AUDITS).clear();
            for (const e of v.value.activity) events.put(e);
            for (const b of v.value.briefs) tx.objectStore(STORE_BRIEFS).put(b);
            for (const c of v.value.copies) tx.objectStore(STORE_COPIES).put(c);
            for (const e of v.value.entities) tx.objectStore(STORE_ENTITIES).put(e);
            for (const a of v.value.adaptations) tx.objectStore(STORE_ADAPTATIONS).put(a);
            for (const a of v.value.audits) tx.objectStore(STORE_AUDITS).put(a);
            if (v.value.rules !== null) tx.objectStore(STORE_RULES).put(v.value.rules, RULES_KEY);
            profile.delete(PROFILE_KEY);
            if (v.value.profile.displayName !== undefined)
              profile.put({ displayName: v.value.profile.displayName }, PROFILE_KEY);
          } catch (e) {
            tx.abort(); // sin estado parcial: la base queda como estaba
            await done.catch(() => undefined);
            throw e;
          }
          await done;
          return ok(undefined);
        }),
    },
  };
}
