import { useCallback, useRef } from 'react';
import { AsyncStatus, ErrorNotice } from '@/components/StatusNotices';
import { useAsyncResource } from '@/hooks/useAsyncResource';
import { useServices } from '@/hooks/ServicesContext';

/** Estado de conexión: deja explícito que no hay backend ni autenticación reales. */
export function ConnectionPage() {
  const services = useServices();
  const heading = useRef<HTMLHeadingElement>(null);
  const load = useCallback(() => services.appState.getState(), [services]);
  const { state, retry } = useAsyncResource(load);

  const onRetry = () => {
    heading.current?.focus();
    retry();
  };

  return (
    <section aria-labelledby="titulo-conexion">
      <h2 id="titulo-conexion" tabIndex={-1} ref={heading}>
        Estado de conexión
      </h2>
      <p>
        Modo de datos:{' '}
        <strong>{state.status === 'success' ? state.data.dataMode.toUpperCase() : 'DEMO'}</strong>
        {state.status === 'success' && (
          <>
            {' '}
            · Entorno: <strong>{state.data.environment}</strong>
          </>
        )}
      </p>
      <p role="note">
        Esta aplicación <strong>no está conectada a ningún backend</strong>. No hay autenticación,
        sincronización ni persistencia remota. Es una fundación técnica en construcción; no es
        producción.
      </p>
      <AsyncStatus status={state.status} loadingLabel="Cargando estado…" />
      {state.status === 'error' && (
        <ErrorNotice message={state.message} onRetry={state.retryable ? onRetry : undefined} />
      )}
      {state.status === 'success' && (
        <div
          role="region"
          aria-label="Estado de la aplicación (JSON)"
          tabIndex={0}
          className="json-region"
        >
          <pre>{JSON.stringify(state.data, null, 2)}</pre>
        </div>
      )}
    </section>
  );
}
