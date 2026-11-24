import { useEffect, useMemo, useRef, useState } from 'react';
import { ReadOnlyNotice } from '@/components/ReadOnlyNotice';
import { ErrorBoundary } from '@/components/ErrorBoundary';
import { AppLayout } from '@/layouts/AppLayout';
import { HomePage } from '@/pages/HomePage';
import { ConnectionPage } from '@/pages/ConnectionPage';
import { BriefsPage } from '@/pages/BriefsPage';
import { CatalogPage } from '@/pages/CatalogPage';
import { RulesPage } from '@/pages/RulesPage';
import { BackupPage } from '@/pages/BackupPage';
import { StoragePage } from '@/pages/StoragePage';
import { SettingsPage } from '@/pages/SettingsPage';
import { applyTheme } from '@/lib/theme';
import type { NavItem } from '@/components/NavMenu';
import { createServices } from '@/services';
import type { Services } from '@/services/contracts';
import type { AppEnv } from './env';
import { ServicesProvider } from '@/hooks/ServicesContext';

const NAV: readonly NavItem[] = [
  { id: 'inicio', label: 'Inicio' },
  { id: 'briefs', label: 'Briefs' },
  { id: 'catalogo', label: 'Catálogo' },
  { id: 'reglas', label: 'Reglas' },
  { id: 'conexion', label: 'Estado de conexión' },
  { id: 'ajustes', label: 'Perfil y preferencias' },
  { id: 'almacenamiento', label: 'Almacenamiento' },
  { id: 'respaldo', label: 'Respaldo' },
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
  // Anota «app abierta» una sola vez por carga (StrictMode ejecuta los efectos dos veces en desarrollo).
  const openedFor = useRef<Services | null>(null);
  useEffect(() => {
    if (openedFor.current === services) return;
    openedFor.current = services;
    void services.activity.record('app_opened');
  }, [services]);
  return (
    <ServicesProvider services={services}>
      <AppLayout
        isDemo={import.meta.env.MODE !== 'production' && env.dataMode === 'demo'}
        items={NAV}
        activeId={active}
        onNavigate={setActive}
      >
        <ReadOnlyNotice />
        <ErrorBoundary key={active}>
          {active === 'briefs' ? (
            <BriefsPage />
          ) : active === 'catalogo' ? (
            <CatalogPage />
          ) : active === 'reglas' ? (
            <RulesPage />
          ) : active === 'conexion' ? (
            <ConnectionPage />
          ) : active === 'ajustes' ? (
            <SettingsPage />
          ) : active === 'almacenamiento' ? (
            <StoragePage />
          ) : active === 'respaldo' ? (
            <BackupPage />
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
