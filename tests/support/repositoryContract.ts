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

const br = (
  id: string,
  updatedAt: string,
  fields: Record<string, unknown> = { campaign: 'Buen Fin' },
) => ({
  id,
  createdAt: '2026-11-22T09:00:00.000Z',
  updatedAt,
  fields,
});

const cp = (id: string, briefId: string, updatedAt: string, headline = 'Hola') => ({
  id,
  briefId,
  label: 'Principal',
  tags: [],
  createdAt: '2026-11-22T09:00:00.000Z',
  updatedAt,
  versions: [{ n: 1, createdAt: '2026-11-22T09:00:00.000Z', content: { headline } }],
});

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
  {
    name: 'briefs vacíos: lista [] (éxito), cuenta 0 y get de uno inexistente es error de validación',
    run: async (r) => {
      same(await r.briefs.list(), { ok: true, value: [] }, 'lista');
      same(await r.briefs.count(), { ok: true, value: 0 }, 'cuenta');
      const g = await r.briefs.get('brf_noexiste1');
      assert(!g.ok && g.error.code === 'validation_error', 'get inexistente');
    },
  },
  {
    name: 'briefs: guardar un borrador incompleto, leerlo, reemplazarlo por id y listar más reciente primero',
    run: async (r) => {
      const a = br('brf_aaaaaaaa1', '2026-11-22T10:00:00.000Z');
      const b = br('brf_bbbbbbbb1', '2026-11-22T12:00:00.000Z', {
        campaign: 'B',
        channel: 'Email',
      });
      same(await r.briefs.put(a), { ok: true, value: a }, 'put a');
      same(await r.briefs.put(b), { ok: true, value: b }, 'put b');
      same(await r.briefs.get('brf_aaaaaaaa1'), { ok: true, value: a }, 'get');
      const a2 = br('brf_aaaaaaaa1', '2026-11-22T13:00:00.000Z', { campaign: 'A2' });
      await r.briefs.put(a2);
      const res = await r.briefs.list();
      assert(res.ok, 'list ok');
      same(
        res.value.map((x) => x.id),
        ['brf_aaaaaaaa1', 'brf_bbbbbbbb1'],
        'orden',
      );
      same(res.value[0]?.fields, { campaign: 'A2' }, 'reemplazo por id');
      same(await r.briefs.count(), { ok: true, value: 2 }, 'cuenta');
    },
  },
  {
    name: 'briefs: datos inválidos se rechazan sin guardar nada; borrar es idempotente',
    run: async (r) => {
      const buen = br('brf_aaaaaaaa1', '2026-11-22T10:00:00.000Z');
      await r.briefs.put(buen);
      for (const malo of [
        br('x', '2026-11-22T10:00:00.000Z'),
        br('brf_cccccccc1', '2026-11-22T10:00:00.000Z', { channel: 'Llamadas' }),
        br('brf_cccccccc1', '2026-11-22T10:00:00.000Z', { campaign: 'a'.repeat(121) }),
        { ...buen, extra: 1 },
        null,
      ]) {
        const res = await r.briefs.put(malo);
        assert(!res.ok && res.error.code === 'validation_error', 'debe rechazar');
      }
      same(await r.briefs.count(), { ok: true, value: 1 }, 'solo el bueno');
      same(await r.briefs.remove('brf_aaaaaaaa1'), { ok: true, value: undefined }, 'remove');
      same(
        await r.briefs.remove('brf_aaaaaaaa1'),
        { ok: true, value: undefined },
        'remove otra vez',
      );
      const bad = await r.briefs.remove('x');
      assert(!bad.ok && bad.error.code === 'validation_error', 'id inválido');
      same(await r.briefs.count(), { ok: true, value: 0 }, 'vacío');
    },
  },
  {
    name: 'respaldo: exportAll incluye briefs y replaceAll los reemplaza (sin briefs = se borran) todo o nada',
    run: async (r) => {
      const a = br('brf_aaaaaaaa1', '2026-11-22T10:00:00.000Z');
      await r.briefs.put(a);
      const res = await r.backup.exportAll();
      assert(res.ok, 'export ok');
      same(res.value.briefs, [a], 'briefs exportados');
      const b = br('brf_bbbbbbbb1', '2026-11-23T10:00:00.000Z', { campaign: 'B' });
      same(
        await r.backup.replaceAll({ profile: {}, activity: [], briefs: [b] }),
        { ok: true, value: undefined },
        'replace',
      );
      same(await r.briefs.list(), { ok: true, value: [b] }, 'solo el nuevo');
      const malo = await r.backup.replaceAll({
        profile: {},
        activity: [],
        briefs: [a, { id: 'x' }],
      });
      assert(!malo.ok && malo.error.code === 'validation_error', 'rechaza briefs inválidos');
      same(await r.briefs.list(), { ok: true, value: [b] }, 'intacto');
      same(
        await r.backup.replaceAll({ profile: {}, activity: [] }),
        { ok: true, value: undefined },
        'sin briefs',
      );
      same(await r.briefs.count(), { ok: true, value: 0 }, 'se borraron');
    },
  },
  {
    name: 'copys: guardar con historial, leer, filtrar por brief, reemplazar por id y borrar (idempotente)',
    run: async (r) => {
      const a = cp('cpy_aaaaaaaa1', 'brf_aaaaaaaa1', '2026-11-22T10:00:00.000Z');
      const b = cp('cpy_bbbbbbbb1', 'brf_bbbbbbbb1', '2026-11-22T12:00:00.000Z', 'B');
      same(await r.copies.put(a), { ok: true, value: a }, 'put a');
      await r.copies.put(b);
      same(await r.copies.get('cpy_aaaaaaaa1'), { ok: true, value: a }, 'get');
      const todos = await r.copies.list();
      assert(todos.ok, 'list ok');
      same(
        todos.value.map((x) => x.id),
        ['cpy_bbbbbbbb1', 'cpy_aaaaaaaa1'],
        'orden',
      );
      const delA = await r.copies.list('brf_aaaaaaaa1');
      assert(delA.ok, 'filtro ok');
      same(
        delA.value.map((x) => x.id),
        ['cpy_aaaaaaaa1'],
        'filtrado por brief',
      );
      const v2 = {
        ...a,
        updatedAt: '2026-11-22T13:00:00.000Z',
        versions: [
          ...a.versions,
          { n: 2, createdAt: '2026-11-22T13:00:00.000Z', content: { headline: 'Nuevo' } },
        ],
      };
      await r.copies.put(v2);
      const g = await r.copies.get('cpy_aaaaaaaa1');
      assert(g.ok && g.value.versions.length === 2, 'historial completo');
      same(await r.copies.count(), { ok: true, value: 2 }, 'cuenta');
      same(await r.copies.remove('cpy_aaaaaaaa1'), { ok: true, value: undefined }, 'remove');
      same(
        await r.copies.remove('cpy_aaaaaaaa1'),
        { ok: true, value: undefined },
        'remove otra vez',
      );
      const bad = await r.copies.remove('x');
      assert(!bad.ok && bad.error.code === 'validation_error', 'id inválido');
      const nf = await r.copies.get('cpy_noexiste1');
      assert(!nf.ok && nf.error.code === 'validation_error', 'inexistente');
    },
  },
  {
    name: 'copys: datos inválidos se rechazan sin guardar nada',
    run: async (r) => {
      const buen = cp('cpy_aaaaaaaa1', 'brf_aaaaaaaa1', '2026-11-22T10:00:00.000Z');
      await r.copies.put(buen);
      for (const malo of [
        cp('x', 'brf_aaaaaaaa1', '2026-11-22T10:00:00.000Z'),
        cp('cpy_cccccccc1', 'x', '2026-11-22T10:00:00.000Z'),
        { ...buen, id: 'cpy_cccccccc1', versions: [] },
        { ...buen, id: 'cpy_cccccccc1', versions: [{ ...buen.versions[0], n: 2 }] },
        { ...buen, id: 'cpy_cccccccc1', extra: 1 },
        null,
      ]) {
        const res = await r.copies.put(malo);
        assert(!res.ok && res.error.code === 'validation_error', 'debe rechazar');
      }
      same(await r.copies.count(), { ok: true, value: 1 }, 'solo el bueno');
    },
  },
  {
    name: 'respaldo: incluye copys; replaceAll los reemplaza y exige que su brief exista (todo o nada)',
    run: async (r) => {
      const b = br('brf_bbbbbbbb1', '2026-11-23T10:00:00.000Z', { campaign: 'B' });
      const c = cp('cpy_aaaaaaaa1', 'brf_bbbbbbbb1', '2026-11-23T11:00:00.000Z');
      same(
        await r.backup.replaceAll({ profile: {}, activity: [], briefs: [b], copies: [c] }),
        { ok: true, value: undefined },
        'replace',
      );
      const ex = await r.backup.exportAll();
      assert(ex.ok, 'export ok');
      same(ex.value.copies, [c], 'copys exportados');
      const huerfano = await r.backup.replaceAll({
        profile: {},
        activity: [],
        briefs: [],
        copies: [c],
      });
      assert(!huerfano.ok && huerfano.error.code === 'validation_error', 'copy sin brief');
      same(await r.copies.list(), { ok: true, value: [c] }, 'intacto');
      same(
        await r.backup.replaceAll({ profile: {}, activity: [] }),
        { ok: true, value: undefined },
        'sin copys',
      );
      same(await r.copies.count(), { ok: true, value: 0 }, 'se borraron');
    },
  },
  {
    name: 'reglas: sin guardar es null; guardar, reemplazar, rechazar inválido y limpiar',
    run: async (r) => {
      same(await r.rules.get(), { ok: true, value: null }, 'sin configuración');
      const doc = {
        legends: [
          { text: 'Consulta a tu médico', channels: ['Email'], required: true, active: true },
        ],
        brandTerms: [{ text: 'cura', kind: 'prohibido', severity: 'mayor' }],
      };
      same(await r.rules.save(doc), { ok: true, value: doc }, 'guardar');
      same(await r.rules.get(), { ok: true, value: doc }, 'leer');
      const malo = await r.rules.save({ legends: [{ text: '' }], brandTerms: [] });
      assert(!malo.ok && malo.error.code === 'validation_error', 'inválido');
      same(await r.rules.get(), { ok: true, value: doc }, 'intacto tras rechazo');
      same(await r.rules.clear(), { ok: true, value: undefined }, 'limpiar');
      same(await r.rules.clear(), { ok: true, value: undefined }, 'limpiar es idempotente');
      same(await r.rules.get(), { ok: true, value: null }, 'otra vez null');
    },
  },
  {
    name: 'respaldo: las reglas se exportan y replaceAll las reemplaza (sin reglas = null)',
    run: async (r) => {
      const doc = {
        legends: [],
        brandTerms: [{ text: 'milagro', kind: 'prohibido', severity: 'mayor' }],
      };
      same(
        await r.backup.replaceAll({ profile: {}, activity: [], rules: doc }),
        { ok: true, value: undefined },
        'replace',
      );
      const ex = await r.backup.exportAll();
      assert(ex.ok, 'export ok');
      same(ex.value.rules, doc, 'reglas exportadas');
      same(
        await r.backup.replaceAll({ profile: {}, activity: [] }),
        { ok: true, value: undefined },
        'sin reglas',
      );
      same(await r.rules.get(), { ok: true, value: null }, 'se limpiaron');
    },
  },
  {
    name: 'catálogo y adaptaciones: put/get/list/remove, rechazo de inválidos y respaldo con referencias',
    run: async (r) => {
      const t = '2026-11-23T09:00:00.000Z';
      const camp = {
        id: 'cmp_aaaaaaaa1',
        kind: 'campaign',
        name: 'Buen Fin',
        createdAt: t,
        updatedAt: t,
      };
      const prod = {
        id: 'prd_aaaaaaaa1',
        kind: 'product',
        name: 'Paracetamol',
        note: 'x',
        createdAt: t,
        updatedAt: t,
      };
      assert((await r.entities.put(camp)).ok, 'put campaña');
      assert((await r.entities.put(prod)).ok, 'put producto');
      const malo = await r.entities.put({ ...camp, id: 'prd_aaaaaaaa1' });
      assert(!malo.ok && malo.error.code === 'validation_error', 'id/tipo incoherentes');
      const all = await r.entities.list();
      assert(all.ok && all.value.length === 2, 'lista total');
      const onlyP = await r.entities.list('product');
      assert(
        onlyP.ok && onlyP.value.length === 1 && onlyP.value[0]?.name === 'Paracetamol',
        'por tipo',
      );
      assert(!(await r.entities.get('cmp_noexiste1')).ok, 'get inexistente falla');
      same(await r.entities.remove('prd_aaaaaaaa1'), { ok: true, value: undefined }, 'remove');
      same(await r.entities.remove('prd_aaaaaaaa1'), { ok: true, value: undefined }, 'idempotente');

      const ad = {
        id: 'ada_aaaaaaaa1',
        copyId: 'cpy_aaaaaaaa1',
        sourceVersion: 1,
        channel: 'Email',
        content: { headline: 'Hola' },
        createdAt: t,
        updatedAt: t,
      };
      assert((await r.adaptations.put(ad)).ok, 'put adaptación');
      const none = await r.adaptations.put({ ...ad, id: 'ada_aaaaaaaa2', channel: 'Llamadas' });
      assert(!none.ok, 'canal no válido');
      const byCopy = await r.adaptations.list('cpy_aaaaaaaa1');
      assert(byCopy.ok && byCopy.value.length === 1, 'por copy');
      const other = await r.adaptations.list('cpy_bbbbbbbb1');
      assert(other.ok && other.value.length === 0, 'otro copy vacío');
      same(await r.adaptations.count(), { ok: true, value: 1 }, 'count');

      const ex = await r.backup.exportAll();
      assert(
        ex.ok && ex.value.entities.length === 1 && ex.value.adaptations.length === 1,
        'export',
      );
      same(
        await r.backup.replaceAll({ profile: {}, activity: [] }),
        { ok: true, value: undefined },
        'replace vacío',
      );
      same(await r.adaptations.count(), { ok: true, value: 0 }, 'adaptaciones limpias');
      const l = await r.entities.list();
      assert(l.ok && l.value.length === 0, 'catálogo limpio');
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
