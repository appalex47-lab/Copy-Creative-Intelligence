// ============================ DATOS DE DEMOSTRACIÓN ============================
// Todo en este archivo es FICTICIO. No representa usuarios, organizaciones ni proyectos reales.
// Los identificadores llevan el prefijo "demo-" y cada entidad lleva origin: 'demo'.
import type { Membership, Organization, Project, UserIdentity } from '@/domain/entities';

export interface DemoDataset {
  readonly identity: UserIdentity;
  readonly organizations: readonly Organization[];
  readonly memberships: readonly Membership[];
  readonly projects: readonly Project[];
}

export const DEMO_IDENTITY: UserIdentity = {
  id: 'demo-user-1',
  displayName: 'Persona DEMO',
  origin: 'demo',
};

export const DEMO_ORGANIZATIONS: readonly Organization[] = [
  { id: 'demo-org-1', name: 'Organización DEMO', origin: 'demo' },
];

export const DEMO_MEMBERSHIPS: readonly Membership[] = [
  {
    userId: 'demo-user-1',
    organizationId: 'demo-org-1',
    roles: ['admin'],
    active: true,
    origin: 'demo',
  },
];

export const DEMO_PROJECTS: readonly Project[] = [
  { id: 'demo-project-1', organizationId: 'demo-org-1', name: 'Proyecto DEMO', origin: 'demo' },
];

export const DEMO_DATASET: DemoDataset = {
  identity: DEMO_IDENTITY,
  organizations: DEMO_ORGANIZATIONS,
  memberships: DEMO_MEMBERSHIPS,
  projects: DEMO_PROJECTS,
};

/** Comprueba la integridad referencial del conjunto de datos. Devuelve la lista de problemas (vacía si es válido). */
export function validateDemoDataset(d: DemoDataset): string[] {
  const problems: string[] = [];
  const orgIds = new Set(d.organizations.map((o) => o.id));
  const dup = (ids: readonly string[], what: string) => {
    if (new Set(ids).size !== ids.length) problems.push(`${what}: identificadores duplicados`);
  };
  dup(
    d.organizations.map((o) => o.id),
    'organizaciones',
  );
  dup(
    d.projects.map((p) => p.id),
    'proyectos',
  );
  const entities = [d.identity, ...d.organizations, ...d.projects, ...d.memberships];
  for (const e of entities) {
    if (e.origin !== 'demo') problems.push('toda entidad DEMO debe tener origin "demo"');
  }
  for (const id of [
    d.identity.id,
    ...d.organizations.map((o) => o.id),
    ...d.projects.map((p) => p.id),
  ]) {
    if (!id.startsWith('demo-')) problems.push(`identificador sin prefijo demo-: ${id}`);
  }
  for (const m of d.memberships) {
    if (!orgIds.has(m.organizationId))
      problems.push(`membresía hacia organización inexistente: ${m.organizationId}`);
    if (m.userId !== d.identity.id) problems.push(`membresía de usuario inexistente: ${m.userId}`);
  }
  for (const p of d.projects) {
    if (!orgIds.has(p.organizationId))
      problems.push(`proyecto hacia organización inexistente: ${p.organizationId}`);
  }
  return problems;
}
