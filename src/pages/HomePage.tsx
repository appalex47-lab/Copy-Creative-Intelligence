import { useCallback, useRef } from 'react';
import { AsyncStatus, ErrorNotice } from '@/components/StatusNotices';
import type { Organization, Project, UserIdentity } from '@/domain/entities';
import { useAsyncResource } from '@/hooks/useAsyncResource';
import { useServices } from '@/hooks/ServicesContext';
import type { Result } from '@/services/contracts';

interface Snapshot {
  readonly identity: UserIdentity;
  readonly organizations: readonly Organization[];
  readonly projects: readonly Project[];
}

/** Página de fundación: demuestra que la UI consume solo contratos, nunca un proveedor concreto. */
export function HomePage() {
  const services = useServices();
  const heading = useRef<HTMLHeadingElement>(null);
  const load = useCallback(async (): Promise<Result<Snapshot>> => {
    const [identity, orgs] = await Promise.all([
      services.identity.getCurrentIdentity(),
      services.organizations.listForCurrentUser(),
    ]);
    if (!identity.ok) return identity;
    if (!orgs.ok) return orgs;
    const first = orgs.value[0];
    const projects = first ? await services.projects.listForOrganization(first.id) : null;
    if (projects && !projects.ok) return projects;
    return {
      ok: true,
      value: {
        identity: identity.value,
        organizations: orgs.value,
        projects: projects?.value ?? [],
      },
    };
  }, [services]);
  const { state, retry } = useAsyncResource(load);

  // Tras reintentar, el botón desaparece: el foco se devuelve al encabezado para no perderlo.
  const onRetry = () => {
    heading.current?.focus();
    retry();
  };

  return (
    <section aria-labelledby="titulo-inicio">
      <h2 id="titulo-inicio" tabIndex={-1} ref={heading}>
        Resumen
      </h2>
      <AsyncStatus status={state.status} />
      {state.status === 'error' && (
        <ErrorNotice message={state.message} onRetry={state.retryable ? onRetry : undefined} />
      )}
      {state.status === 'success' && (
        <>
          <p>
            Identidad: <strong>{state.data.identity.displayName}</strong> (
            {state.data.identity.origin})
          </p>
          <p>
            Organizaciones:{' '}
            {state.data.organizations.length > 0
              ? state.data.organizations.map((o) => o.name).join(', ')
              : 'ninguna'}
          </p>
          <p>
            Proyectos:{' '}
            {state.data.projects.length > 0
              ? state.data.projects.map((p) => p.name).join(', ')
              : 'ninguno'}
          </p>
        </>
      )}
    </section>
  );
}
