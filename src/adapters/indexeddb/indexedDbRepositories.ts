import { validateActivityEvent, type ActivityEvent } from '@/domain/activity';
import { validateDisplayName, parseLocalProfile, type LocalProfile } from '@/domain/profile';
import { normalizeLimit, type Repositories } from '@/repositories/contracts';
import { fail, ok, type Result } from '@/services/contracts';

export const DEFAULT_DB_NAME = 'cci';
const STORE_ACTIVITY = 'activity';
const STORE_PROFILE = 'profile';
const STORE_META = 'meta';
const PROFILE_KEY = 'local';

/** Un paso de migración: se ejecuta dentro de la transacción `versionchange`; si lanza, TODO se revierte. */
export type MigrationStep = (db: IDBDatabase, tx: IDBTransaction) => void;

/**
 * Migraciones en orden. El índice + 1 es la versión a la que llega cada paso.
 * v0 → v1: instalación nueva (v0 = no existe la base): crea los tres almacenes y el índice por fecha.
 * v1 → v2 (SUPUESTO técnico de Claude, S1-D13, reversible): añade el índice `kind` en `activity` para filtrar por tipo
 * sin recorrer todo; no agrega atributos de negocio y conserva todos los datos.
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
      resolve(fail('unavailable', UNAVAILABLE));
      return;
    }
    let req: IDBOpenDBRequest;
    try {
      req = indexedDB.open(name, migrations.length);
    } catch {
      resolve(fail('unavailable', UNAVAILABLE));
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
    req.onerror = () =>
      resolve(
        fail(
          'unavailable',
          req.error?.name === 'VersionError' ? NEWER_SCHEMA_MESSAGE : UNAVAILABLE,
        ),
      );
    req.onblocked = () => resolve(fail('unavailable', UNAVAILABLE));
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
  } catch {
    return fail('unavailable', UNAVAILABLE); // sin detalle interno hacia la interfaz
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
  };
}
