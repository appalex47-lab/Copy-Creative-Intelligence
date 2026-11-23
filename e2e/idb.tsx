// ARNÉS DE NAVEGADOR: ejecuta el MISMO contrato de repositorios contra IndexedDB real. No forma parte de la app.
import {
  MIGRATIONS,
  NEWER_SCHEMA_MESSAGE,
  createIndexedDbRepositories,
  deleteDatabase,
  openDatabase,
} from '@/adapters/indexeddb/indexedDbRepositories';
import { runContract } from '../tests/support/repositoryContract';

interface SchemaInfo {
  version: number;
  stores: string[];
  activityIndexes: string[];
  schemaVersion: unknown;
}
declare global {
  interface Window {
    __idb: { done: boolean; failures: string[] };
    __schema: () => Promise<SchemaInfo>;
    __mig: {
      v0ToLatest: () => Promise<unknown>;
      v1ToV2WithSeeds: () => Promise<unknown>;
      newerVersionRejected: () => Promise<unknown>;
      failingMigrationRollsBack: () => Promise<unknown>;
      blockedByOtherConnection: () => Promise<unknown>;
      failingMigrationCode: () => Promise<unknown>;
    };
  }
}
window.__schema = async () => {
  const name = `cci-esquema-${Date.now()}`;
  const opened = await openDatabase(name);
  if (!opened.ok) throw new Error('no se pudo abrir IndexedDB');
  const db = opened.value;
  const tx = db.transaction(['activity', 'meta'], 'readonly');
  const schemaVersion = await new Promise<unknown>((resolve, reject) => {
    const r = tx.objectStore('meta').get('schemaVersion');
    r.onsuccess = () => resolve(r.result);
    r.onerror = () => reject(r.error);
  });
  const info: SchemaInfo = {
    version: db.version,
    stores: [...db.objectStoreNames].sort(),
    activityIndexes: [...tx.objectStore('activity').indexNames],
    schemaVersion,
  };
  db.close();
  await deleteDatabase(name);
  return info;
};
window.__idb = { done: false, failures: [] };
let n = 0;
void runContract(async () => {
  const name = `cci-test-${Date.now()}-${n++}`;
  const opened = await openDatabase(name);
  if (!opened.ok) throw new Error('no se pudo abrir IndexedDB');
  const db = opened.value;
  return {
    repos: createIndexedDbRepositories(db),
    dispose: async () => {
      db.close();
      await deleteDatabase(name);
    },
  };
}).then((failures) => {
  window.__idb = { done: true, failures };
  (document.getElementById('out') as HTMLElement).textContent = failures.length
    ? failures.join('\n')
    : 'OK';
});

// ---- Escenarios de migración (bases construidas a mano, independientes del adaptador) ----
const rawOpen = (
  name: string,
  version: number | undefined,
  upgrade?: (db: IDBDatabase, tx: IDBTransaction) => void,
) =>
  new Promise<IDBDatabase>((resolve, reject) => {
    const r = version === undefined ? indexedDB.open(name) : indexedDB.open(name, version);
    r.onupgradeneeded = () => r.transaction && upgrade?.(r.result, r.transaction);
    r.onsuccess = () => resolve(r.result);
    r.onerror = () => reject(r.error);
  });
const req = <T,>(r: IDBRequest<T>) =>
  new Promise<T>((resolve, reject) => {
    r.onsuccess = () => resolve(r.result);
    r.onerror = () => reject(r.error);
  });
const done = (tx: IDBTransaction) =>
  new Promise<void>((resolve, reject) => {
    tx.oncomplete = () => resolve();
    tx.onabort = () => reject(tx.error);
  });
const uniq = (p: string) => `${p}-${Date.now()}-${Math.floor(Math.random() * 1e6)}`;
const SEED = [
  { id: 'evt_seed0001', at: '2026-01-01T00:00:00.000Z', kind: 'app_opened' },
  { id: 'evt_seed0002', at: '2026-01-02T00:00:00.000Z', kind: 'profile_changed' },
];
/** Construye a mano una base v1 con semillas (sin usar el adaptador). */
async function seedV1(name: string) {
  const db = await rawOpen(name, 1, (d) => {
    d.createObjectStore('meta');
    d.createObjectStore('profile');
    d.createObjectStore('activity', { keyPath: 'id' }).createIndex('at', 'at');
  });
  const tx = db.transaction(['meta', 'profile', 'activity'], 'readwrite');
  tx.objectStore('meta').put(1, 'schemaVersion');
  tx.objectStore('profile').put({ displayName: 'Ana' }, 'local');
  for (const e of SEED) tx.objectStore('activity').put(e);
  await done(tx);
  db.close();
}
const inspect = async (name: string) => {
  const db = await rawOpen(name, undefined);
  const tx = db.transaction(['meta', 'profile', 'activity'], 'readonly');
  const out = {
    version: db.version,
    stores: [...db.objectStoreNames].sort(),
    indexes: [...tx.objectStore('activity').indexNames].sort(),
    schemaVersion: await req(tx.objectStore('meta').get('schemaVersion')),
    profile: await req(tx.objectStore('profile').get('local')),
    ids: (await req(tx.objectStore('activity').getAllKeys())).sort(),
    byKind: await req(tx.objectStore('activity').index('kind').getAllKeys('profile_changed')).catch(
      () => 'sin-indice-kind',
    ),
  };
  db.close();
  return out;
};
window.__mig = {
  v0ToLatest: async () => {
    const name = uniq('mig-v0');
    const o = await openDatabase(name);
    if (!o.ok) throw new Error('apertura');
    o.value.close();
    const r = await inspect(name);
    await deleteDatabase(name);
    return r;
  },
  v1ToV2WithSeeds: async () => {
    const name = uniq('mig-v1');
    await seedV1(name);
    const o = await openDatabase(name);
    if (!o.ok) throw new Error('apertura');
    const repos = createIndexedDbRepositories(o.value);
    const viaRepo = await repos.activity.listRecent();
    o.value.close();
    const r = { ...(await inspect(name)), viaRepo };
    await deleteDatabase(name);
    return r;
  },
  newerVersionRejected: async () => {
    const name = uniq('mig-newer');
    const db = await rawOpen(name, MIGRATIONS.length + 1, (d) => {
      d.createObjectStore('sentinel');
    });
    const tx = db.transaction('sentinel', 'readwrite');
    tx.objectStore('sentinel').put('intacto', 'k');
    await done(tx);
    db.close();
    const o = await openDatabase(name);
    const after = await rawOpen(name, undefined);
    const val = await req(after.transaction('sentinel').objectStore('sentinel').get('k'));
    const info = {
      opened: o.ok,
      error: o.ok ? null : o.error,
      version: after.version,
      stores: [...after.objectStoreNames],
      val,
      expectedMessage: NEWER_SCHEMA_MESSAGE,
    };
    after.close();
    await deleteDatabase(name);
    return info;
  },
  // Otra conexión abierta a la versión anterior (sin cerrarse) bloquea la actualización: debe dar storage_blocked.
  blockedByOtherConnection: async () => {
    const name = uniq('mig-blocked');
    const held = await rawOpen(name, 1, (d) => {
      d.createObjectStore('meta');
    });
    const o = await openDatabase(name);
    held.close();
    await deleteDatabase(name);
    return { opened: o.ok, code: o.ok ? null : o.error.code };
  },
  failingMigrationCode: async () => {
    const name = uniq('mig-code');
    await seedV1(name);
    const o = await openDatabase(name, [
      MIGRATIONS[0] as never,
      () => {
        throw new Error('fallo simulado');
      },
    ]);
    await deleteDatabase(name);
    return { opened: o.ok, code: o.ok ? null : o.error.code };
  },
  failingMigrationRollsBack: async () => {
    const name = uniq('mig-abort');
    await seedV1(name);
    const o = await openDatabase(name, [
      MIGRATIONS[0] as never,
      (_db, tx) => {
        tx.objectStore('activity').createIndex('kind', 'kind');
        tx.objectStore('activity').put({
          id: 'evt_parcial1',
          at: '2026-02-01T00:00:00.000Z',
          kind: 'app_opened',
        });
        throw new Error('fallo simulado de migración');
      },
    ]);
    const db = await rawOpen(name, undefined);
    const tx = db.transaction(['activity', 'meta'], 'readonly');
    const info = {
      opened: o.ok,
      version: db.version,
      indexes: [...tx.objectStore('activity').indexNames].sort(),
      ids: (await req(tx.objectStore('activity').getAllKeys())).sort(),
      schemaVersion: await req(tx.objectStore('meta').get('schemaVersion')),
    };
    db.close();
    await deleteDatabase(name);
    return info;
  },
};
