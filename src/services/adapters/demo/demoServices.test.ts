import { describe, expect, it } from 'vitest';
import type { Membership, Organization, Project } from '@/domain/entities';
import { createDemoServices } from './demoServices';
import { DEMO_DATASET, validateDemoDataset, type DemoDataset } from './fixtures';

const org = (id: string): Organization => ({ id, name: id, origin: 'demo' });
const withData = (over: Partial<DemoDataset>): DemoDataset => ({ ...DEMO_DATASET, ...over });

describe('adaptador DEMO — identidad y estado', () => {
  const s = createDemoServices('test');

  it('identifica todo como demo y no ofrece autenticación', async () => {
    const id = await s.identity.getCurrentIdentity();
    expect(id.ok && id.value.origin).toBe('demo');
    expect(id.ok && id.value.id.startsWith('demo-')).toBe(true);
    expect(Object.keys(s.identity)).toEqual(['getCurrentIdentity']); // sin login/logout/token
  });

  it('solo ofrece operaciones de lectura (sin escritura ni persistencia remota)', () => {
    const ops = [s.identity, s.organizations, s.memberships, s.projects, s.appState].flatMap((x) =>
      Object.keys(x),
    );
    expect(ops.sort()).toEqual([
      'getCurrentIdentity',
      'getState',
      'listForCurrentUser',
      'listForOrganization',
      'listForOrganization',
    ]);
  });

  it.each(['development', 'test', 'preview'] as const)(
    'el estado declara demo en %s',
    async (env) => {
      const st = await createDemoServices(env).appState.getState();
      expect(st).toEqual({ ok: true, value: { dataMode: 'demo', environment: env, isDemo: true } });
    },
  );

  it('todas las entidades demo llevan origin demo', async () => {
    const orgs = await s.organizations.listForCurrentUser();
    expect(orgs.ok && orgs.value.every((o) => o.origin === 'demo')).toBe(true);
  });
});

describe('semántica uniforme: padre existente / inexistente / parámetro inválido', () => {
  const noChildren = withData({
    organizations: [org('demo-org-1'), org('demo-org-vacia')],
  });
  const s = createDemoServices('test', noChildren);

  it('organización válida con membresías y proyectos → listas con elementos', async () => {
    const m = await s.memberships.listForOrganization('demo-org-1');
    const p = await s.projects.listForOrganization('demo-org-1');
    expect(m.ok && m.value).toHaveLength(1);
    expect(p.ok && p.value).toHaveLength(1);
  });

  it('organización existente sin membresías ni proyectos → lista vacía (éxito), nunca error', async () => {
    expect(await s.memberships.listForOrganization('demo-org-vacia')).toEqual({
      ok: true,
      value: [],
    });
    expect(await s.projects.listForOrganization('demo-org-vacia')).toEqual({ ok: true, value: [] });
  });

  it.each(['no-existe', 'demo-org-99'])(
    'organización inexistente (%s) → not_found en membresías y proyectos',
    async (id) => {
      for (const r of [
        await s.memberships.listForOrganization(id),
        await s.projects.listForOrganization(id),
      ]) {
        expect(r).toEqual({
          ok: false,
          error: { code: 'not_found', message: 'Organización DEMO inexistente' },
        });
      }
    },
  );

  it.each(['', '   ', undefined, null, 42, {}] as unknown[])(
    'parámetro inválido (%j) → validation_error',
    async (bad) => {
      for (const r of [
        await s.memberships.listForOrganization(bad as string),
        await s.projects.listForOrganization(bad as string),
      ]) {
        expect(r.ok).toBe(false);
        expect(!r.ok && r.error.code).toBe('validation_error');
      }
    },
  );
});

describe('integridad referencial del conjunto de datos', () => {
  it('el conjunto DEMO por defecto es consistente', () => {
    expect(validateDemoDataset(DEMO_DATASET)).toEqual([]);
  });

  it('detecta membresía hacia organización inexistente', () => {
    const m: Membership = {
      ...(DEMO_DATASET.memberships[0] as Membership),
      organizationId: 'demo-org-x',
    };
    expect(validateDemoDataset(withData({ memberships: [m] }))).toEqual([
      'membresía hacia organización inexistente: demo-org-x',
    ]);
  });

  it('detecta membresía de usuario inexistente', () => {
    const m: Membership = { ...(DEMO_DATASET.memberships[0] as Membership), userId: 'demo-user-9' };
    expect(validateDemoDataset(withData({ memberships: [m] }))).toEqual([
      'membresía de usuario inexistente: demo-user-9',
    ]);
  });

  it('detecta proyecto hacia organización inexistente, duplicados, origin y prefijo', () => {
    const p: Project = { id: 'p1', organizationId: 'demo-org-x', name: 'x', origin: 'backend' };
    const problems = validateDemoDataset(withData({ projects: [p, p] }));
    expect(problems).toEqual(
      expect.arrayContaining([
        'proyectos: identificadores duplicados',
        'toda entidad DEMO debe tener origin "demo"',
        'identificador sin prefijo demo-: p1',
        'proyecto hacia organización inexistente: demo-org-x',
      ]),
    );
  });

  it('el adaptador se niega a crearse con datos inconsistentes (no los sirve en silencio)', () => {
    const m: Membership = {
      ...(DEMO_DATASET.memberships[0] as Membership),
      organizationId: 'demo-org-x',
    };
    expect(() => createDemoServices('test', withData({ memberships: [m] }))).toThrow(
      'Conjunto de datos DEMO inconsistente',
    );
  });
});
