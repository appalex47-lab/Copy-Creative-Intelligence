import type { Repositories } from '@/repositories/contracts';

/** Fábrica: una instancia NUEVA y vacía por caso, y cómo liberarla. */
export type RepositoryFactory = () => Promise<{
  repos: Repositories;
  dispose: () => Promise<void>;
}>;

export interface ContractCase {
  readonly name: string;
  readonly run: (repos: Repositories) => Promise<void>;
}

const ev = (id: string, at: string, kind = 'app_opened') => ({ id, at, kind });

function assert(cond: unknown, msg: string): asserts cond {
  if (!cond) throw new Error(msg);
}
const same = (a: unknown, b: unknown, msg: string) =>
  assert(
    JSON.stringify(a) === JSON.stringify(b),
    `${msg}: obtenido ${JSON.stringify(a)}, esperado ${JSON.stringify(b)}`,
  );

/** Casos del contrato; sin dependencia de Vitest para poder ejecutarse también en un navegador real. */
export const CONTRACT_CASES: readonly ContractCase[] = [
  {
    name: 'actividad vacía: lista [] (éxito) y cuenta 0',
    run: async (r) => {
      same(await r.activity.listRecent(), { ok: true, value: [] }, 'lista');
      same(await r.activity.count(), { ok: true, value: 0 }, 'cuenta');
    },
  },
  {
    name: 'actividad: guardar y leer devuelve el evento',
    run: async (r) => {
      const e = ev('evt_00000001', '2026-11-22T10:00:00.000Z');
      same(await r.activity.add(e), { ok: true, value: e }, 'add');
      same(await r.activity.listRecent(), { ok: true, value: [e] }, 'lista');
    },
  },
  {
    name: 'actividad: más nuevos primero y, en empate, id descendente',
    run: async (r) => {
      await r.activity.add(ev('evt_00000001', '2026-11-22T10:00:00.000Z'));
      await r.activity.add(ev('evt_00000003', '2026-11-22T11:00:00.000Z'));
      await r.activity.add(ev('evt_00000002', '2026-11-22T11:00:00.000Z'));
      const res = await r.activity.listRecent();
      assert(res.ok, 'lista ok');
      same(
        res.value.map((x) => x.id),
        ['evt_00000003', 'evt_00000002', 'evt_00000001'],
        'orden',
      );
    },
  },
  {
    name: 'actividad: respeta el límite y rechaza límites inválidos',
    run: async (r) => {
      for (let i = 1; i <= 5; i++)
        await r.activity.add(ev(`evt_0000000${i}`, `2026-11-22T10:00:0${i}.000Z`));
      const res = await r.activity.listRecent(2);
      assert(res.ok && res.value.length === 2, 'límite 2');
      for (const bad of [0, -1, 501, 1.5, '3'] as unknown[]) {
        const x = await r.activity.listRecent(bad as number);
        assert(!x.ok && x.error.code === 'validation_error', `límite inválido ${String(bad)}`);
      }
    },
  },
  {
    name: 'actividad: un evento inválido se rechaza y no se guarda',
    run: async (r) => {
      for (const bad of [
        null,
        {},
        ev('x', 'hoy'),
        { ...ev('evt_00000001', '2026-11-22T10:00:00Z'), extra: 1 },
      ]) {
        const x = await r.activity.add(bad);
        assert(!x.ok && x.error.code === 'validation_error', 'rechazo');
      }
      same(await r.activity.count(), { ok: true, value: 0 }, 'sin cambios');
    },
  },
  {
    name: 'actividad: repetir el mismo id reemplaza (idempotente)',
    run: async (r) => {
      await r.activity.add(ev('evt_00000001', '2026-11-22T10:00:00.000Z', 'app_opened'));
      await r.activity.add(ev('evt_00000001', '2026-11-22T10:00:00.000Z', 'storage_error'));
      same(await r.activity.count(), { ok: true, value: 1 }, 'cuenta');
      const res = await r.activity.listRecent();
      assert(res.ok && res.value[0]?.kind === 'storage_error', 'reemplazado');
    },
  },
  {
    name: 'perfil: vacío por defecto; guardar, normalizar y leer',
    run: async (r) => {
      same(await r.profile.get(), { ok: true, value: {} }, 'vacío');
      same(
        await r.profile.save('  Ana   María '),
        { ok: true, value: { displayName: 'Ana María' } },
        'guardar',
      );
      same(await r.profile.get(), { ok: true, value: { displayName: 'Ana María' } }, 'leer');
    },
  },
  {
    name: 'perfil: un nombre inválido se rechaza y no cambia lo guardado',
    run: async (r) => {
      await r.profile.save('Ana');
      for (const bad of [5, 'x'.repeat(61), 'a\u0007b'] as unknown[]) {
        const x = await r.profile.save(bad);
        assert(!x.ok && x.error.code === 'validation_error', 'rechazo');
      }
      same(await r.profile.get(), { ok: true, value: { displayName: 'Ana' } }, 'intacto');
    },
  },
  {
    name: 'perfil: nombre vacío, undefined y clear() lo borran',
    run: async (r) => {
      await r.profile.save('Ana');
      same(await r.profile.save(''), { ok: true, value: {} }, 'vacío');
      await r.profile.save('Ana');
      same(await r.profile.save(undefined), { ok: true, value: {} }, 'undefined');
      await r.profile.save('Ana');
      same(await r.profile.clear(), { ok: true, value: {} }, 'clear');
      same(await r.profile.get(), { ok: true, value: {} }, 'leer');
    },
  },
  {
    name: 'respaldo: exportAll devuelve perfil y actividad (más nuevos primero)',
    run: async (r) => {
      await r.profile.save('Ana');
      await r.activity.add(ev('evt_00000001', '2026-11-22T10:00:00.000Z'));
      await r.activity.add(ev('evt_00000002', '2026-11-22T11:00:00.000Z'));
      const res = await r.backup.exportAll();
      assert(res.ok, 'export ok');
      same(res.value.profile, { displayName: 'Ana' }, 'perfil');
      same(
        res.value.activity.map((x) => x.id),
        ['evt_00000002', 'evt_00000001'],
        'orden',
      );
    },
  },
  {
    name: 'respaldo: replaceAll reemplaza TODO (lo anterior desaparece)',
    run: async (r) => {
      await r.profile.save('Ana');
      await r.activity.add(ev('evt_00000001', '2026-11-22T10:00:00.000Z'));
      const nuevo = ev('evt_00000009', '2026-11-23T10:00:00.000Z', 'profile_changed');
      same(
        await r.backup.replaceAll({ profile: {}, activity: [nuevo] }),
        { ok: true, value: undefined },
        'replace',
      );
      same(await r.profile.get(), { ok: true, value: {} }, 'perfil borrado');
      same(await r.activity.listRecent(), { ok: true, value: [nuevo] }, 'solo lo nuevo');
      same(await r.activity.count(), { ok: true, value: 1 }, 'cuenta');
    },
  },
  {
    name: 'respaldo: datos inválidos se rechazan y NO alteran nada (todo o nada)',
    run: async (r) => {
      await r.profile.save('Ana');
      const previo = ev('evt_00000001', '2026-11-22T10:00:00.000Z');
      await r.activity.add(previo);
      const buenos = ev('evt_00000002', '2026-11-22T11:00:00.000Z');
      for (const malo of [
        { profile: {}, activity: [buenos, { id: 'x', at: 'no', kind: 'app_opened' }] },
        { profile: {}, activity: [buenos, buenos] },
        { profile: { displayName: 'x'.repeat(61) }, activity: [] },
        { profile: {}, activity: [], extra: 1 },
        null,
      ]) {
        const res = await r.backup.replaceAll(malo);
        assert(!res.ok && res.error.code === 'validation_error', 'debe rechazar');
      }
      same(await r.profile.get(), { ok: true, value: { displayName: 'Ana' } }, 'perfil intacto');
      same(await r.activity.listRecent(), { ok: true, value: [previo] }, 'actividad intacta');
    },
  },
];

/** Ejecuta todos los casos y devuelve los fallos (lista vacía = todo correcto). */
export async function runContract(factory: RepositoryFactory): Promise<string[]> {
  const failures: string[] = [];
  for (const c of CONTRACT_CASES) {
    const { repos, dispose } = await factory();
    try {
      await c.run(repos);
    } catch (e) {
      failures.push(`${c.name}: ${e instanceof Error ? e.message : String(e)}`);
    } finally {
      await dispose();
    }
  }
  return failures;
}
