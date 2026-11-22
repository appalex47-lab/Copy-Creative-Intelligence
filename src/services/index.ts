import type { AppEnv } from '@/app/env';
import type { Services } from '@/services/contracts';
import { createDemoServices } from './adapters/demo/demoServices';

/** Fábrica de servicios por modo. El modo "backend" (Supabase) se añadirá como otro adaptador, sin tocar la UI. */
export function createServices(env: AppEnv): Services {
  switch (env.dataMode) {
    case 'demo':
      return createDemoServices(env.appEnv);
    default: {
      // Estado imposible según los tipos; si ocurre en ejecución se falla de forma explícita (lo captura ErrorBoundary).
      const unreachable: never = env.dataMode;
      throw new Error(`Modo de datos no soportado: ${String(unreachable)}`);
    }
  }
}
