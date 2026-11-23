// ARNÉS DE PRUEBAS DE NAVEGADOR. No forma parte de la aplicación ni del build.
// Monta la MISMA <App> real con servicios que fallan o se retrasan de forma controlada, para probar en un
// navegador real los estados de carga, error, reintento, ErrorBoundary, StrictMode y respuestas tardías.
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { App } from '@/app/App';
import '@/styles/global.css';
import { ErrorBoundary } from '@/components/ErrorBoundary';
import { fail, ok, type Services } from '@/services/contracts';
import { createDemoServices } from '@/services/adapters/demo/demoServices';

interface Control {
  calls: { activity: number; appState: number };
  /** Libera todas las llamadas retenidas (escenario "gated"). */
  release: () => void;
  /** Deja de fallar (escenarios "unavailable" y "throw"): simula que el servicio se recuperó. */
  heal: () => void;
}
declare global {
  interface Window {
    __cci: Control;
  }
}

const scenario = new URLSearchParams(location.search).get('s') ?? 'ok';
const base = createDemoServices('development');
const waiting: (() => void)[] = [];
// StrictMode ejecuta los efectos dos veces en desarrollo: el fallo no depende del número de llamada sino de `failing`.
let failing = true;
const control: Control = {
  calls: { activity: 0, appState: 0 },
  release: () => waiting.splice(0).forEach((r) => r()),
  heal: () => {
    failing = false;
  },
};
window.__cci = control;

const gate = () => new Promise<void>((resolve) => waiting.push(resolve));

const services: Services = {
  ...base,
  activity: {
    record: () => Promise.resolve(ok(undefined)),
    listRecent: async () => {
      control.calls.activity += 1;
      if (scenario === 'gated') await gate();
      if (scenario === 'unavailable' && failing) return fail('unavailable', 'DETALLE_INTERNO_SQL');
      if (scenario === 'notfound') return fail('not_found', 'DETALLE_INTERNO_SQL');
      if (scenario === 'throw' && failing) throw new Error('DETALLE_INTERNO_STACK');
      if (scenario === 'render-bomb') {
        // Valor inválido como hijo de React: provoca un error REAL de renderizado.
        return {
          ok: true,
          value: [
            {
              id: 'evt_00000001',
              at: { oops: 1 } as unknown as string,
              kind: 'app_opened' as const,
            },
          ],
        };
      }
      return base.activity.listRecent();
    },
  },
  appState: {
    getState: async () => {
      control.calls.appState += 1;
      if (scenario === 'gated') await gate();
      if (scenario === 'state-unavailable') return fail('unavailable', 'DETALLE_INTERNO_SQL');
      return base.appState.getState();
    },
  },
};

const root = document.getElementById('root');
if (!root) throw new Error('No existe #root');
createRoot(root).render(
  <StrictMode>
    <ErrorBoundary>
      <App env={{ appEnv: 'development', dataMode: 'demo' }} services={services} />
    </ErrorBoundary>
  </StrictMode>,
);
