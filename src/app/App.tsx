import { useEffect, useMemo, useState } from 'react';
import { ErrorBoundary } from '@/components/ErrorBoundary';
import { AppLayout } from '@/layouts/AppLayout';
import { HomePage } from '@/pages/HomePage';
import { ConnectionPage } from '@/pages/ConnectionPage';
import { SettingsPage } from '@/pages/SettingsPage';
import { applyTheme } from '@/lib/theme';
import type { NavItem } from '@/components/NavMenu';
import { createServices } from '@/services';
import type { Services } from '@/services/contracts';
import type { AppEnv } from './env';
import { ServicesProvider } from '@/hooks/ServicesContext';

const NAV: readonly NavItem[] = [
  { id: 'inicio', label: 'Inicio' },
  { id: 'conexion', label: 'Estado de conexión' },
  { id: 'ajustes', label: 'Perfil y preferencias' },
];

interface AppProps {
  readonly env: AppEnv;
  /** Inyección de servicios (pruebas y arneses de navegador). Si se omite, se crean según el entorno. */
  readonly services?: Services;
}

export function App({ env, services: injected }: AppProps) {
  const [active, setActive] = useState('inicio');
  const services = useMemo(() => injected ?? createServices(env), [env, injected]);
  // Aplica el tema guardado al arrancar. Un fallo al leer no es grave: rige el tema del sistema.
  useEffect(() => {
    void services.preferences.get().then((r) => {
      if (r.ok) applyTheme(r.value.theme);
    });
  }, [services]);
  return (
    <ServicesProvider services={services}>
      <AppLayout
        isDemo={env.dataMode === 'demo'}
        items={NAV}
        activeId={active}
        onNavigate={setActive}
      >
        <ErrorBoundary key={active}>
          {active === 'conexion' ? (
            <ConnectionPage />
          ) : active === 'ajustes' ? (
            <SettingsPage />
          ) : (
            <HomePage />
          )}
        </ErrorBoundary>
      </AppLayout>
    </ServicesProvider>
  );
}

export function ConfigurationError({ message }: { message: string }) {
  return <p role="alert">Configuración inválida: {message}</p>;
}
