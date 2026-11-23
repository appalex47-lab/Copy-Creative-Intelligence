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
import { validateDisplayName, parseLocalProfile, type LocalProfile } from '@/domain/profile';
import { compareNewestFirst, normalizeLimit, type Repositories } from '@/repositories/contracts';
import { fail, ok, type Result } from '@/services/contracts';

export const DEFAULT_DB_NAME = 'cci';
const STORE_ACTIVITY = 'activity';
const STORE_PROFILE = 'profile';
const STORE_META = 'meta';
const STORE_BRIEFS = 'briefs';
const STORE_COPIES = 'copies';
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
            [STORE_ACTIVITY, STORE_PROFILE, STORE_BRIEFS, STORE_COPIES],
            'readonly',
          ); // una sola lectura consistente
          const [rawEvents, rawProfile, rawBriefs, rawCopies] = await Promise.all([
            promisify<unknown[]>(tx.objectStore(STORE_ACTIVITY).getAll()),
            promisify<unknown>(tx.objectStore(STORE_PROFILE).get(PROFILE_KEY)),
            promisify<unknown[]>(tx.objectStore(STORE_BRIEFS).getAll()),
            promisify<unknown[]>(tx.objectStore(STORE_COPIES).getAll()),
          ]);
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
          return ok({ profile: parseLocalProfile(rawProfile), activity, briefs, copies });
        }),
      replaceAll: (raw) =>
        guard(async () => {
          const v = validateSnapshot(raw); // se valida TODO antes de tocar la base
          if (!v.ok) return fail('validation_error', v.reason);
          const tx = db.transaction(
            [STORE_ACTIVITY, STORE_PROFILE, STORE_BRIEFS, STORE_COPIES],
            'readwrite',
          );
          const done = txDone(tx);
          try {
            const events = tx.objectStore(STORE_ACTIVITY);
            const profile = tx.objectStore(STORE_PROFILE);
            events.clear();
            tx.objectStore(STORE_BRIEFS).clear();
            tx.objectStore(STORE_COPIES).clear();
            for (const e of v.value.activity) events.put(e);
            for (const b of v.value.briefs) tx.objectStore(STORE_BRIEFS).put(b);
            for (const c of v.value.copies) tx.objectStore(STORE_COPIES).put(c);
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
