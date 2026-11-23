import {
  createIndexedDbRepositories,
  openDatabase,
} from '@/adapters/indexeddb/indexedDbRepositories';
import { createBackupService } from './backupService';
import { createBrowserStorageInfoService } from '@/adapters/storage/browserStorageInfo';
import { createBrowserPreferencesStore } from '@/adapters/localstorage/preferencesStore';
import type { ActivityKind } from '@/domain/activity';
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
  const preferences = createBrowserPreferencesStore();
  const saveProfile = via((r) => (name: unknown) => r.profile.save(name));
  const clearProfile = via((r) => () => r.profile.clear());
  const add = via(
    (r) => (kind: ActivityKind) =>
      r.activity.add({
        id: `evt_${crypto.randomUUID().replaceAll('-', '')}`,
        at: new Date().toISOString(),
        kind,
      }),
  );
  const record = async (kind: ActivityKind): Promise<Result<void>> => {
    const r = await add(kind);
    return r.ok ? ok(undefined) : fail(r.error.code, r.error.message);
  };
  /** Tras un cambio correcto, anota el evento. Es secundario: si no se puede anotar, el cambio igual vale. */
  const noting = async <T>(result: Result<T>, kind: ActivityKind): Promise<Result<T>> => {
    if (result.ok) await record(kind);
    return result;
  };
  const backup = createBackupService({ repos, preferences, record });
  return {
    appState: {
      getState: () => Promise.resolve(ok({ dataMode: 'local', environment, isDemo: false })),
    },
    activity: {
      listRecent: via((r) => (limit?: number) => r.activity.listRecent(limit)),
      record,
    },
    profile: {
      get: via((r) => () => r.profile.get()),
      save: async (name: unknown) => noting(await saveProfile(name), 'profile_changed'),
      clear: async () => noting(await clearProfile(), 'profile_changed'),
    },
    preferences: {
      get: () => preferences.get(),
      update: async (patch: unknown) => noting(await preferences.update(patch), 'setting_changed'),
      reset: async () => noting(await preferences.reset(), 'setting_changed'),
    },
    storage: createBrowserStorageInfoService(),
    backup,
  };
}
