import {
  createIndexedDbRepositories,
  openDatabase,
} from '@/adapters/indexeddb/indexedDbRepositories';
import { createBrowserStorageInfoService } from '@/adapters/storage/browserStorageInfo';
import { createBrowserPreferencesStore } from '@/adapters/localstorage/preferencesStore';
import type { AppState } from '@/domain/entities';
import type { Repositories } from '@/repositories/contracts';
import { fail, ok, type Result, type Services } from '@/services/contracts';

/**
 * Servicios de datos REALES del navegador: IndexedDB (actividad y perfil) y Local Storage (preferencias).
 * No hay backend, cuentas ni sincronización. La base se abre de forma perezosa en el primer uso; si falla, cada
 * operación devuelve el error (nunca datos vacíos) y se reintenta en la siguiente.
 */
export function createLocalServices(environment: AppState['environment']): Services {
  let opening: Promise<Result<Repositories>> | undefined;
  const repos = (): Promise<Result<Repositories>> => {
    opening ??= openDatabase().then((r) => {
      if (r.ok) return ok(createIndexedDbRepositories(r.value));
      opening = undefined; // permite reintentar
      return fail(r.error.code, r.error.message);
    });
    return opening;
  };
  const via =
    <A extends unknown[], T>(pick: (r: Repositories) => (...a: A) => Promise<Result<T>>) =>
    async (...args: A): Promise<Result<T>> => {
      const r = await repos();
      return r.ok ? pick(r.value)(...args) : fail(r.error.code, r.error.message);
    };
  return {
    appState: {
      getState: () => Promise.resolve(ok({ dataMode: 'local', environment, isDemo: false })),
    },
    activity: { listRecent: via((r) => (limit?: number) => r.activity.listRecent(limit)) },
    profile: {
      get: via((r) => () => r.profile.get()),
      save: via((r) => (name: unknown) => r.profile.save(name)),
      clear: via((r) => () => r.profile.clear()),
    },
    preferences: createBrowserPreferencesStore(),
    storage: createBrowserStorageInfoService(),
  };
}
