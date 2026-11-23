import { UNKNOWN_STORAGE } from '@/domain/storageInfo';
import { createMemoryRepositories } from '@/adapters/memory/memoryRepositories';
import {
  createMemoryStorage,
  createPreferencesStore,
} from '@/adapters/localstorage/preferencesStore';
import type { AppState } from '@/domain/entities';
import { fail, ok } from '@/services/contracts';
import type { Services } from '@/services/contracts';

/**
 * Adaptador DEMO: en memoria y de solo lectura. No simula autenticación ni persistencia y NO inventa actividad:
 * la actividad reciente está vacía y el perfil y las preferencias viven solo en memoria
 * (se pierden al recargar). La persistencia real es el modo `local`.
 */
/** Marca no enumerable del adaptador DEMO: permite comprobar que NO está en el bundle de producción. */
export const DEMO_ADAPTER_MARKER = 'cci-adaptador-demo-v1';

export function createDemoServices(environment: AppState['environment']): Services {
  const memory = createMemoryRepositories();
  const services: Services = {
    appState: {
      getState: () => Promise.resolve(ok({ dataMode: 'demo', environment, isDemo: true })),
    },
    activity: {
      listRecent: () => Promise.resolve(ok([])),
      record: () => Promise.resolve(ok(undefined)), // DEMO no guarda actividad
    },
    profile: memory.profile,
    preferences: createPreferencesStore(createMemoryStorage()),
    // DEMO no usa almacenamiento real: no se inventan cifras.
    // DEMO es solo memoria de una pestaña: siempre puede escribir.
    coordination: {
      getState: () => 'writer',
      subscribe: () => () => undefined,
      whenWriter: () => Promise.resolve(true),
    },
    backup: {
      export: () =>
        Promise.resolve(fail('not_implemented', 'DEMO no tiene datos reales que respaldar.')),
      inspect: () => Promise.resolve(fail('not_implemented', 'DEMO no admite respaldos.')),
      restore: () => Promise.resolve(fail('not_implemented', 'DEMO no admite respaldos.')),
    },
    storage: {
      get: () => Promise.resolve(ok(UNKNOWN_STORAGE)),
      requestPersistence: () => Promise.resolve(ok(UNKNOWN_STORAGE)),
    },
  };
  return Object.defineProperty(services, '__adapter', { value: DEMO_ADAPTER_MARKER });
}
