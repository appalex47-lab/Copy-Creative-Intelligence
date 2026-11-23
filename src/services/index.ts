import type { AppEnv } from '@/app/env';
import type { Services } from '@/services/contracts';
import { createLocalServices } from '@/adapters/local/localServices';
import { createDemoServices } from './adapters/demo/demoServices';

/** Fábrica de servicios por modo. Modos: demo (memoria, ficticio) y local (IndexedDB y Local Storage reales). */
export function createServices(env: AppEnv): Services {
  switch (env.dataMode) {
    case 'demo':
      return createDemoServices(env.appEnv);
    case 'local':
      return createLocalServices(env.appEnv);
    default: {
      // Estado imposible según los tipos; si ocurre en ejecución se falla de forma explícita (lo captura ErrorBoundary).
      const unreachable: never = env.dataMode;
      throw new Error(`Modo de datos no soportado: ${String(unreachable)}`);
    }
  }
}
