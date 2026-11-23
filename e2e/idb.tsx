// ARNÉS DE NAVEGADOR: ejecuta el MISMO contrato de repositorios contra IndexedDB real. No forma parte de la app.
import {
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
