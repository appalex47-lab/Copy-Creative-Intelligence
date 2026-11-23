import type { AppState } from '@/domain/entities';
import { ok } from '@/services/contracts';
import type { Services } from '@/services/contracts';

/**
 * Adaptador DEMO: en memoria y de solo lectura. No simula autenticación ni persistencia y NO inventa actividad:
 * la actividad reciente está vacía hasta que exista persistencia real (estado vacío honesto, AC1-11).
 */
export function createDemoServices(environment: AppState['environment']): Services {
  return {
    appState: {
      getState: () => Promise.resolve(ok({ dataMode: 'demo', environment, isDemo: true })),
    },
    activity: { listRecent: () => Promise.resolve(ok([])) },
  };
}
