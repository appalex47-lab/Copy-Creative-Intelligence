import { classifyStorageError } from '@/adapters/persistenceErrors';
import { parseStorageInfo, UNKNOWN_STORAGE, type StorageInfo } from '@/domain/storageInfo';
import { fail, ok, type Result, type StorageService } from '@/services/contracts';

const MESSAGE = 'No se pudo consultar el almacenamiento.';

/** Subconjunto de `navigator.storage` que usamos (cada método puede no existir según el navegador). */
export interface StorageManagerLike {
  estimate?: () => Promise<{ usage?: unknown; quota?: unknown }>;
  persisted?: () => Promise<unknown>;
  persist?: () => Promise<unknown>;
}

/** Consulta uso, cuota y persistencia. Lo que el navegador no expone queda en `null` (nunca se inventa). */
export function createStorageInfoService(manager: StorageManagerLike | undefined): StorageService {
  const read = async (): Promise<Result<StorageInfo>> => {
    if (!manager) return ok(UNKNOWN_STORAGE);
    try {
      const est = manager.estimate ? await manager.estimate() : undefined;
      const persisted = manager.persisted ? await manager.persisted() : undefined;
      return ok(parseStorageInfo(est?.usage, est?.quota, persisted));
    } catch (e) {
      return fail(classifyStorageError(e), MESSAGE);
    }
  };
  return {
    get: read,
    requestPersistence: async () => {
      if (!manager?.persist) return read();
      try {
        await manager.persist();
      } catch (e) {
        return fail(classifyStorageError(e), MESSAGE);
      }
      return read();
    },
  };
}

export function createBrowserStorageInfoService(): StorageService {
  return createStorageInfoService(typeof navigator === 'undefined' ? undefined : navigator.storage);
}
