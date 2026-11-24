import { describe, expect, it } from 'vitest';
import {
  COPY_LIMITS,
  COPY_MAX_VERSIONS,
  addVariant,
  appendVersion,
  compareCopiesNewestFirst,
  currentVersion,
  diffContent,
  removeVariant,
  updateVariant,
  variantsOf,
  validateCopyContent,
  validateCopyRecord,
  validateLabel,
  validateTags,
  type CopyRecord,
} from './copy';

const T0 = '2026-11-23T10:00:00.000Z';
const base: CopyRecord = {
  id: 'cpy_abcdefgh1',
  briefId: 'brf_abcdefgh1',
  label: 'Principal',
  tags: [],
  createdAt: T0,
  updatedAt: T0,
  versions: [{ n: 1, createdAt: T0, content: { headline: 'Hola' } }],
};

describe('copy (S2.4)', () => {
  it('contenido: descarta vacíos, exige al menos un campo y respeta límites exactos', () => {
    const v = validateCopyContent({ headline: ' Hola  mundo ', body: '   ' });
    expect(v.ok && v.value).toEqual({ headline: 'Hola mundo' });
    expect(validateCopyContent({}).ok).toBe(false);
    expect(validateCopyContent({ headline: '  ' }).ok).toBe(false);
    expect(validateCopyContent({ headline: 'a'.repeat(COPY_LIMITS.headline) }).ok).toBe(true);
    expect(validateCopyContent({ headline: 'a'.repeat(COPY_LIMITS.headline + 1) }).ok).toBe(false);
    expect(validateCopyContent({ body: 'a'.repeat(COPY_LIMITS.body + 1) }).ok).toBe(false);
    expect(validateCopyContent({ headline: 5 }).ok).toBe(false);
    expect(validateCopyContent({ headline: 'a\u0000' }).ok).toBe(false);
    expect(validateCopyContent({ headline: 'a', extra: 'b' }).ok).toBe(false);
    for (const x of [null, 'x', [], 5]) expect(validateCopyContent(x).ok).toBe(false);
  });

  it('etiquetas y nombre de variante', () => {
    expect(validateLabel('  B ').ok).toBe(true);
    expect(validateLabel('  ').ok).toBe(false);
    expect(validateLabel('a'.repeat(61)).ok).toBe(false);
    const t = validateTags(['Promo', 'promo', ' ', 'Buen Fin']);
    expect(t.ok && t.value).toEqual(['Promo', 'Buen Fin']);
    expect(validateTags(Array.from({ length: 9 }, (_, i) => `t${i}`)).ok).toBe(false);
    expect(validateTags(['a'.repeat(31)]).ok).toBe(false);
    expect(validateTags('x').ok).toBe(false);
    expect(validateTags(undefined).ok).toBe(true);
  });

  it('registro: válido, y rechaza ids, brief, versiones salteadas, desordenadas o vacías', () => {
    expect(validateCopyRecord(base).ok).toBe(true);
    expect(validateCopyRecord({ ...base, id: 'x' }).ok).toBe(false);
    expect(validateCopyRecord({ ...base, briefId: 'x' }).ok).toBe(false);
    expect(validateCopyRecord({ ...base, versions: [] }).ok).toBe(false);
    expect(validateCopyRecord({ ...base, versions: [{ ...base.versions[0], n: 2 }] }).ok).toBe(
      false,
    );
    expect(validateCopyRecord({ ...base, extra: 1 }).ok).toBe(false);
    const two = [
      base.versions[0],
      { n: 2, createdAt: '2026-11-22T10:00:00.000Z', content: { headline: 'x' } },
    ];
    expect(validateCopyRecord({ ...base, versions: two }).ok).toBe(false);
    expect(
      validateCopyRecord({
        ...base,
        versions: [
          base.versions[0],
          { n: 2, createdAt: T0, content: { headline: 'x' }, restoredFrom: 2 },
        ],
      }).ok,
    ).toBe(false);
  });

  it('guardar AÑADE una versión y nunca modifica las anteriores (inmutabilidad)', () => {
    const frozen = structuredClone(base);
    const r = appendVersion(base, { headline: 'Nuevo' }, '2026-11-23T11:00:00.000Z');
    expect(r.ok).toBe(true);
    if (!r.ok) return;
    expect(r.value.versions).toHaveLength(2);
    expect(r.value.versions[0]).toEqual(base.versions[0]);
    expect(currentVersion(r.value).content).toEqual({ headline: 'Nuevo' });
    expect(r.value.updatedAt).toBe('2026-11-23T11:00:00.000Z');
    expect(base).toEqual(frozen); // el original no se tocó
    expect(validateCopyRecord(r.value).ok).toBe(true);
  });

  it('sin cambios no crea versión; contenido inválido se rechaza; reloj atrasado no rompe el orden', () => {
    expect(appendVersion(base, { headline: 'Hola' }, T0).ok).toBe(false);
    expect(appendVersion(base, { headline: '' }, T0).ok).toBe(false);
    const r = appendVersion(base, { headline: 'Otro' }, '2020-01-01T00:00:00.000Z');
    expect(r.ok && r.value.versions[1]?.createdAt).toBe(T0);
  });

  it('recuperar una versión antigua crea una versión nueva con restoredFrom (historial intacto)', () => {
    const v2 = appendVersion(base, { headline: 'B' }, '2026-11-23T11:00:00.000Z');
    if (!v2.ok) throw new Error('v2');
    const v3 = appendVersion(v2.value, { headline: 'Hola' }, '2026-11-23T12:00:00.000Z', 1);
    expect(v3.ok).toBe(true);
    if (!v3.ok) return;
    expect(v3.value.versions.map((v) => v.n)).toEqual([1, 2, 3]);
    expect(v3.value.versions[2]?.restoredFrom).toBe(1);
    expect(validateCopyRecord(v3.value).ok).toBe(true);
  });

  it('máximo de versiones', () => {
    let c = base;
    for (let i = 2; i <= COPY_MAX_VERSIONS; i++) {
      const r = appendVersion(c, { headline: `v${i}` }, T0);
      if (!r.ok) throw new Error(r.reason);
      c = r.value;
    }
    expect(c.versions).toHaveLength(COPY_MAX_VERSIONS);
    expect(appendVersion(c, { headline: 'una más' }, T0).ok).toBe(false);
  });

  it('diff por campo y orden por actualización', () => {
    expect(
      diffContent({ headline: 'a', cta: 'x' }, { headline: 'b', cta: 'x', body: 'z' }),
    ).toEqual([
      { field: 'headline', before: 'a', after: 'b' },
      { field: 'body', before: undefined, after: 'z' },
    ]);
    const older = { ...base, id: 'cpy_aaaaaaaa1' };
    const newer = { ...base, id: 'cpy_bbbbbbbb1', updatedAt: '2026-11-24T10:00:00.000Z' };
    expect([older, newer].sort(compareCopiesNewestFirst).map((c) => c.id)).toEqual([
      'cpy_bbbbbbbb1',
      'cpy_aaaaaaaa1',
    ]);
  });
});

describe('variantes dentro del copy (S2.7): sin versiones propias', () => {
  const at = '2026-11-23T10:00:00.000Z';
  const later = '2026-11-23T11:00:00.000Z';
  const base: CopyRecord = {
    id: 'cpy_abcdefgh1',
    briefId: 'brf_abcdefgh1',
    label: 'Principal',
    tags: [],
    createdAt: '2026-11-23T09:00:00.000Z',
    updatedAt: '2026-11-23T09:00:00.000Z',
    versions: [{ n: 1, createdAt: '2026-11-23T09:00:00.000Z', content: { headline: 'Hola' } }],
  };
  const added = (): CopyRecord => {
    const r = addVariant(
      base,
      { id: 'var_abcdefgh1', label: 'B', content: { headline: 'Otro' } },
      at,
    );
    if (!r.ok) throw new Error(r.reason);
    return r.value;
  };

  it('agregar no toca el historial de versiones del copy', () => {
    const c = added();
    expect(c.versions).toEqual(base.versions);
    expect(variantsOf(c)).toHaveLength(1);
    expect(c.updatedAt).toBe(at);
    expect(validateCopyRecord(c).ok).toBe(true);
  });
  it('un copy sin variantes no lleva la clave `variants` (compatibilidad)', () => {
    const v = validateCopyRecord(base);
    expect(v.ok && 'variants' in v.value).toBe(false);
  });
  it('editar una variante cambia su contenido en su lugar, sin crear versiones', () => {
    const r = updateVariant(
      added(),
      { variantId: 'var_abcdefgh1', label: 'B', content: { headline: 'Nuevo' } },
      later,
    );
    expect(r.ok && variantsOf(r.value)[0]?.content).toEqual({ headline: 'Nuevo' });
    expect(r.ok && r.value.versions).toHaveLength(1);
    expect(r.ok && variantsOf(r.value)[0]?.createdAt).toBe(at);
  });
  it('rechaza sin cambios, nombre repetido, variante inexistente y exceso', () => {
    const c = added();
    expect(
      updateVariant(
        c,
        { variantId: 'var_abcdefgh1', label: 'B', content: { headline: 'Otro' } },
        later,
      ).ok,
    ).toBe(false);
    expect(
      addVariant(c, { id: 'var_abcdefgh2', label: ' b ', content: { cta: 'x' } }, later).ok,
    ).toBe(false);
    expect(
      updateVariant(c, { variantId: 'var_zzzzzzzz1', label: 'C', content: { cta: 'x' } }, later).ok,
    ).toBe(false);
    let cur: CopyRecord = base;
    for (let i = 0; i < 10; i++) {
      const r = addVariant(
        cur,
        { id: `var_abcdefg${i}x`, label: `V${i}`, content: { cta: 'x' } },
        at,
      );
      if (!r.ok) throw new Error(r.reason);
      cur = r.value;
    }
    expect(
      addVariant(cur, { id: 'var_abcdefgz11', label: 'V11', content: { cta: 'x' } }, at).ok,
    ).toBe(false);
  });
  it('eliminar quita la variante y, si era la última, la clave', () => {
    const r = removeVariant(added(), 'var_abcdefgh1', later);
    expect(r.ok && 'variants' in r.value).toBe(false);
    expect(removeVariant(base, 'var_abcdefgh1', later).ok).toBe(false);
  });
  it('un registro guardado con variantes repetidas o inválidas se rechaza', () => {
    const c = added();
    const v = variantsOf(c)[0];
    expect(validateCopyRecord({ ...c, variants: [v, v] }).ok).toBe(false);
    expect(validateCopyRecord({ ...c, variants: [{ ...v, id: 'x' }] }).ok).toBe(false);
    expect(validateCopyRecord({ ...c, variants: 'x' }).ok).toBe(false);
  });
});
