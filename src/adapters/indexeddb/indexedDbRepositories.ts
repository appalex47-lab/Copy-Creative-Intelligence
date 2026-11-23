import { validateActivityEvent, type ActivityEvent } from '@/domain/activity';
import { validateDisplayName, parseLocalProfile, type LocalProfile } from '@/domain/profile';
import { normalizeLimit, type Repositories } from '@/repositories/contracts';
import { fail, ok, type Result } from '@/services/contracts';

/** Versión de esquema vigente. Las migraciones v0→v1→v2 se definen en S1.5; hoy solo existe la creación de v1. */
export const SCHEMA_VERSION = 1;
export const DEFAULT_DB_NAME = 'cci';
const STORE_ACTIVITY = 'activity';
const STORE_PROFILE = 'profile';
const STORE_META = 'meta';
const PROFILE_KEY = 'local';

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

/** Abre (y crea si hace falta) la base. Devuelve `unavailable` si IndexedDB no existe o falla. */
export function openDatabase(name = DEFAULT_DB_NAME): Promise<Result<IDBDatabase>> {
  return new Promise((resolve) => {
    if (typeof indexedDB === 'undefined') {
      resolve(fail('unavailable', UNAVAILABLE));
      return;
    }
    let req: IDBOpenDBRequest;
    try {
      req = indexedDB.open(name, SCHEMA_VERSION);
    } catch {
      resolve(fail('unavailable', UNAVAILABLE));
      return;
    }
    req.onupgradeneeded = () => {
      const db = req.result;
      if (!db.objectStoreNames.contains(STORE_META)) db.createObjectStore(STORE_META);
      if (!db.objectStoreNames.contains(STORE_PROFILE)) db.createObjectStore(STORE_PROFILE);
      if (!db.objectStoreNames.contains(STORE_ACTIVITY)) {
        const s = db.createObjectStore(STORE_ACTIVITY, { keyPath: 'id' });
        s.createIndex('at', 'at');
      }
      req.transaction?.objectStore(STORE_META).put(SCHEMA_VERSION, 'schemaVersion');
    };
    req.onsuccess = () => resolve(ok(req.result));
    req.onerror = () => resolve(fail('unavailable', UNAVAILABLE));
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
