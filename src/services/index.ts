import type { AppEnv } from '@/app/env';
import type { Services } from '@/services/contracts';
import { createLocalServices } from '@/adapters/local/localServices';
import { createDemoServices } from './adapters/demo/demoServices';

/** Fábrica de servicios por modo. Modos: demo (memoria, ficticio) y local (IndexedDB y Local Storage reales). */
export function createServices(env: AppEnv): Services {
  switch (env.dataMode) {
    case 'demo':
      // En producción el modo DEMO no existe (la política de entorno ya lo rechaza); esta guarda además permite que
      // el empaquetador elimine el adaptador DEMO del build de producción (AC1-11).
      if (import.meta.env.MODE === 'production')
        throw new Error('El modo DEMO no está disponible en producción.');
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
