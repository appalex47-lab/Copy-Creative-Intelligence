import type { AppState, Organization } from '@/domain/entities';
import { fail, ok } from '@/services/contracts';
import type { Result, Services } from '@/services/contracts';
import { DEMO_DATASET, validateDemoDataset, type DemoDataset } from './fixtures';

/** Valida el identificador del recurso padre y comprueba que exista (semántica uniforme, ver contratos). */
function resolveOrganization(data: DemoDataset, organizationId: unknown): Result<Organization> {
  if (typeof organizationId !== 'string' || organizationId.trim() === '') {
    return fail('validation_error', 'Identificador de organización requerido');
  }
  const org = data.organizations.find((o) => o.id === organizationId);
  return org ? ok(org) : fail('not_found', 'Organización DEMO inexistente');
}

/**
 * Adaptador DEMO: datos ficticios en memoria, de solo lectura.
 * NO simula autenticación, autorización ni persistencia remota: no hay sesión, no hay escritura.
 * Un conjunto de datos con referencias inconsistentes es un error de programación y falla al crearse.
 */
export function createDemoServices(
  environment: AppState['environment'],
  data: DemoDataset = DEMO_DATASET,
): Services {
  const problems = validateDemoDataset(data);
  if (problems.length > 0) {
    throw new Error(`Conjunto de datos DEMO inconsistente: ${problems.join('; ')}`);
  }
  return {
    identity: { getCurrentIdentity: () => Promise.resolve(ok(data.identity)) },
    organizations: { listForCurrentUser: () => Promise.resolve(ok(data.organizations)) },
    memberships: {
      listForOrganization: (organizationId) => {
        const org = resolveOrganization(data, organizationId);
        if (!org.ok) return Promise.resolve(org);
        return Promise.resolve(
          ok(data.memberships.filter((m) => m.organizationId === org.value.id)),
        );
      },
    },
    projects: {
      listForOrganization: (organizationId) => {
        const org = resolveOrganization(data, organizationId);
        if (!org.ok) return Promise.resolve(org);
        return Promise.resolve(ok(data.projects.filter((p) => p.organizationId === org.value.id)));
      },
    },
    appState: {
      getState: () => Promise.resolve(ok({ dataMode: 'demo', environment, isDemo: true })),
    },
  };
}
