import { createMemoryRepositories } from '@/adapters/memory/memoryRepositories';
import {
  createMemoryStorage,
  createPreferencesStore,
} from '@/adapters/localstorage/preferencesStore';
import type { AppState } from '@/domain/entities';
import { ok } from '@/services/contracts';
import type { Services } from '@/services/contracts';

/**
 * Adaptador DEMO: en memoria y de solo lectura. No simula autenticación ni persistencia y NO inventa actividad:
 * la actividad reciente está vacía y el perfil y las preferencias viven solo en memoria
 * (se pierden al recargar). La persistencia real es el modo `local`.
 */
export function createDemoServices(environment: AppState['environment']): Services {
  const memory = createMemoryRepositories();
  return {
    appState: {
      getState: () => Promise.resolve(ok({ dataMode: 'demo', environment, isDemo: true })),
    },
    activity: { listRecent: () => Promise.resolve(ok([])) },
    profile: memory.profile,
    preferences: createPreferencesStore(createMemoryStorage()),
  };
}
