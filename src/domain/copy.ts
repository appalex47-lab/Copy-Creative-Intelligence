import { BRIEF_ID } from './briefRecord';
import { invalid, valid, type Validation } from './validation';

/**
 * Copy de Copy Studio (R-022…, AC2-04, AC2-07). Un copy pertenece a un brief y guarda un HISTORIAL DE VERSIONES
 * inmutables: guardar siempre AÑADE una versión (nunca modifica una anterior) y recuperar una versión antigua crea
 * una versión nueva con ese contenido (el historial se conserva). Una variante es otro copy del mismo brief con su
 * propia etiqueta. SUPUESTOS de Claude aprobados por el propietario (S2.4, reversibles): campos del contenido
 * (titular, texto, descripción, CTA), límites de longitud, máximo de 200 versiones por copy y etiquetas de hasta 8.
 * El estado del flujo (Q-3) llega en la Fase 5; en Fase 2 todo copy es un borrador.
 */
export const COPY_FIELDS = ['headline', 'body', 'description', 'cta'] as const;
export type CopyField = (typeof COPY_FIELDS)[number];

export const COPY_FIELD_LABELS: Readonly<Record<CopyField, string>> = {
  headline: 'Titular',
  body: 'Texto',
  description: 'Descripción',
  cta: 'CTA',
};
export const COPY_LIMITS: Readonly<Record<CopyField, number>> = {
  headline: 120,
  body: 1000,
  description: 500,
  cta: 120,
};
export const COPY_MAX_VERSIONS = 200;
export const COPY_MAX_TAGS = 8;
export const COPY_TAG_MAX = 30;
export const COPY_LABEL_MAX = 60;

export type CopyContent = Partial<Record<CopyField, string>>;

export interface CopyVersion {
  readonly n: number; // 1, 2, 3… sin huecos
  readonly createdAt: string;
  readonly content: CopyContent;
  /** Si esta versión recupera otra, el número de la versión origen. */
  readonly restoredFrom?: number;
}

/**
 * Variante (S2.7, decisión del propietario D-Fase2): alternativa de texto que COEXISTE con otras dentro de un copy.
 * NO tiene versiones propias (se edita en su lugar); el historial de versiones es solo del copy. No es una versión.
 * SUPUESTO de Claude (reversible): máximo 10 variantes por copy.
 */
export interface CopyVariant {
  readonly id: string; // var_…
  readonly label: string;
  readonly content: CopyContent;
  readonly createdAt: string;
  readonly updatedAt: string;
}
export const VARIANT_ID = /^var_[A-Za-z0-9_-]{8,64}$/;
export const COPY_MAX_VARIANTS = 10;

export interface CopyRecord {
  readonly id: string; // cpy_…
  readonly briefId: string;
  /** Nombre de la variante («Principal», «B»…). */
  readonly label: string;
  readonly tags: readonly string[];
  readonly createdAt: string;
  readonly updatedAt: string;
  readonly versions: readonly CopyVersion[]; // de la más antigua a la más reciente, inmutables
  /** Alternativas del copy sin versiones propias. Ausente = ninguna (así los copys anteriores siguen siendo válidos). */
  readonly variants?: readonly CopyVariant[];
}

export const COPY_ID = /^cpy_[A-Za-z0-9_-]{8,64}$/;
const ISO = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,3})?Z$/;
// eslint-disable-next-line no-control-regex
const CONTROL = /[\u0000-\u0008\u000b-\u001f\u007f]/;

const isObject = (v: unknown): v is Record<string, unknown> =>
  typeof v === 'object' && v !== null && !Array.isArray(v);
const isIso = (v: unknown): v is string =>
  typeof v === 'string' && ISO.test(v) && !Number.isNaN(Date.parse(v));
const onlyKeys = (o: Record<string, unknown>, allowed: readonly string[]) =>
  Object.keys(o).every((k) => allowed.includes(k));

/** Valida el contenido; los campos vacíos se descartan. Debe quedar al menos un campo con texto. */
export function validateCopyContent(input: unknown): Validation<CopyContent> {
  if (!isObject(input)) return invalid('El contenido del copy no es válido.');
  if (!onlyKeys(input, COPY_FIELDS)) return invalid('El copy contiene campos no permitidos.');
  const out: CopyContent = {};
  for (const f of COPY_FIELDS) {
    const v = input[f];
    if (v === undefined || v === null) continue;
    const label = COPY_FIELD_LABELS[f];
    if (typeof v !== 'string') return invalid(`${label} debe ser texto.`);
    const text = v
      .replace(/[ \t]+/g, ' ')
      .replace(/\n{3,}/g, '\n\n')
      .trim();
    if (text === '') continue;
    if (CONTROL.test(text)) return invalid(`${label} contiene caracteres no permitidos.`);
    if ([...text].length > COPY_LIMITS[f])
      return invalid(`${label} admite como máximo ${COPY_LIMITS[f]} caracteres.`);
    out[f] = text;
  }
  if (Object.keys(out).length === 0) return invalid('Escribe al menos un campo del copy.');
  return valid(out);
}

export function validateLabel(input: unknown): Validation<string> {
  if (typeof input !== 'string') return invalid('La etiqueta de la variante debe ser texto.');
  const t = input.replace(/\s+/g, ' ').trim();
  if (t === '') return invalid('La variante necesita un nombre.');
  if (CONTROL.test(t))
    return invalid('El nombre de la variante contiene caracteres no permitidos.');
  if ([...t].length > COPY_LABEL_MAX)
    return invalid(`El nombre de la variante admite como máximo ${COPY_LABEL_MAX} caracteres.`);
  return valid(t);
}

export function validateTags(input: unknown): Validation<string[]> {
  if (input === undefined) return valid([]);
  if (!Array.isArray(input)) return invalid('Las etiquetas no son válidas.');
  const out: string[] = [];
  for (const raw of input) {
    if (typeof raw !== 'string') return invalid('Las etiquetas deben ser texto.');
    const t = raw.replace(/\s+/g, ' ').trim();
    if (t === '') continue;
    if (CONTROL.test(t)) return invalid('Una etiqueta contiene caracteres no permitidos.');
    if ([...t].length > COPY_TAG_MAX)
      return invalid(`Cada etiqueta admite como máximo ${COPY_TAG_MAX} caracteres.`);
    if (!out.some((x) => x.toLocaleLowerCase('es') === t.toLocaleLowerCase('es'))) out.push(t);
  }
  if (out.length > COPY_MAX_TAGS) return invalid(`Máximo ${COPY_MAX_TAGS} etiquetas por copy.`);
  return valid(out);
}

function validateVersion(raw: unknown, expectedN: number): Validation<CopyVersion> {
  if (!isObject(raw) || !onlyKeys(raw, ['n', 'createdAt', 'content', 'restoredFrom']))
    return invalid('Una versión del copy no es válida.');
  if (raw['n'] !== expectedN) return invalid('Las versiones del copy no son consecutivas.');
  if (!isIso(raw['createdAt'])) return invalid('La fecha de una versión no es válida.');
  const content = validateCopyContent(raw['content']);
  if (!content.ok) return content;
  const rf = raw['restoredFrom'];
  if (
    rf !== undefined &&
    (!Number.isInteger(rf) || (rf as number) < 1 || (rf as number) >= expectedN)
  )
    return invalid('El origen de la versión recuperada no es válido.');
  return valid({
    n: expectedN,
    createdAt: raw['createdAt'],
    content: content.value,
    ...(rf !== undefined ? { restoredFrom: rf as number } : {}),
  });
}

export function validateVariant(raw: unknown): Validation<CopyVariant> {
  if (!isObject(raw) || !onlyKeys(raw, ['id', 'label', 'content', 'createdAt', 'updatedAt']))
    return invalid('Una variante no es válida.');
  if (typeof raw['id'] !== 'string' || !VARIANT_ID.test(raw['id']))
    return invalid('El identificador de una variante no es válido.');
  const label = validateLabel(raw['label']);
  if (!label.ok) return label;
  const content = validateCopyContent(raw['content']);
  if (!content.ok) return content;
  if (!isIso(raw['createdAt']) || !isIso(raw['updatedAt']) || raw['updatedAt'] < raw['createdAt'])
    return invalid('Las fechas de una variante no son válidas.');
  return valid({
    id: raw['id'],
    label: label.value,
    content: content.value,
    createdAt: raw['createdAt'],
    updatedAt: raw['updatedAt'],
  });
}

function validateVariants(raw: unknown): Validation<CopyVariant[]> {
  if (raw === undefined) return valid([]);
  if (!Array.isArray(raw) || raw.length > COPY_MAX_VARIANTS)
    return invalid(`Las variantes no son válidas (máximo ${COPY_MAX_VARIANTS}).`);
  const out: CopyVariant[] = [];
  const ids = new Set<string>();
  const names = new Set<string>();
  for (const item of raw) {
    const v = validateVariant(item);
    if (!v.ok) return v;
    const key = v.value.label.toLocaleLowerCase('es');
    if (ids.has(v.value.id) || names.has(key))
      return invalid('Hay variantes repetidas (mismo identificador o mismo nombre).');
    ids.add(v.value.id);
    names.add(key);
    out.push(v.value);
  }
  return valid(out);
}

export function validateCopyRecord(raw: unknown): Validation<CopyRecord> {
  if (
    !isObject(raw) ||
    !onlyKeys(raw, [
      'id',
      'briefId',
      'label',
      'tags',
      'createdAt',
      'updatedAt',
      'versions',
      'variants',
    ])
  )
    return invalid('El copy guardado no es válido.');
  const { id, briefId, createdAt, updatedAt } = raw;
  if (typeof id !== 'string' || !COPY_ID.test(id))
    return invalid('El identificador del copy no es válido.');
  if (typeof briefId !== 'string' || !BRIEF_ID.test(briefId))
    return invalid('El brief del copy no es válido.');
  if (!isIso(createdAt) || !isIso(updatedAt)) return invalid('Las fechas del copy no son válidas.');
  const label = validateLabel(raw['label']);
  if (!label.ok) return label;
  const tags = validateTags(raw['tags']);
  if (!tags.ok) return tags;
  const rv = raw['versions'];
  if (!Array.isArray(rv) || rv.length < 1 || rv.length > COPY_MAX_VERSIONS)
    return invalid('El historial de versiones del copy no es válido.');
  const versions: CopyVersion[] = [];
  for (const [i, item] of rv.entries()) {
    const v = validateVersion(item, i + 1);
    if (!v.ok) return v;
    if (i > 0 && v.value.createdAt < (versions[i - 1] as CopyVersion).createdAt)
      return invalid('Las versiones del copy no están en orden cronológico.');
    versions.push(v.value);
  }
  if (updatedAt < createdAt)
    return invalid('La fecha de actualización es anterior a la de creación.');
  const variants = validateVariants(raw['variants']);
  if (!variants.ok) return variants;
  return valid({
    id,
    briefId,
    label: label.value,
    tags: tags.value,
    createdAt,
    updatedAt,
    versions,
    ...(variants.value.length > 0 ? { variants: variants.value } : {}),
  });
}

/** Contenido vigente = el de la última versión. */
export const currentVersion = (c: CopyRecord): CopyVersion =>
  c.versions[c.versions.length - 1] as CopyVersion;

export function compareCopiesNewestFirst(a: CopyRecord, b: CopyRecord): number {
  if (a.updatedAt !== b.updatedAt) return a.updatedAt < b.updatedAt ? 1 : -1;
  return a.id < b.id ? 1 : a.id > b.id ? -1 : 0;
}

export interface ContentDiff {
  readonly field: CopyField;
  readonly before: string | undefined;
  readonly after: string | undefined;
}

/** Diferencias campo por campo entre dos contenidos (solo los campos que cambian). */
export function diffContent(before: CopyContent, after: CopyContent): readonly ContentDiff[] {
  return COPY_FIELDS.filter((f) => before[f] !== after[f]).map((field) => ({
    field,
    before: before[field],
    after: after[field],
  }));
}

/** Añade una versión nueva (si el contenido cambió) sin tocar las anteriores. Pura: devuelve un registro nuevo. */
export function appendVersion(
  copy: CopyRecord,
  content: unknown,
  at: string,
  restoredFrom?: number,
): Validation<CopyRecord> {
  const c = validateCopyContent(content);
  if (!c.ok) return c;
  if (copy.versions.length >= COPY_MAX_VERSIONS)
    return invalid(`Este copy llegó al máximo de ${COPY_MAX_VERSIONS} versiones.`);
  if (diffContent(currentVersion(copy).content, c.value).length === 0)
    return invalid('No hay cambios respecto de la versión actual.');
  const when = at < currentVersion(copy).createdAt ? currentVersion(copy).createdAt : at;
  const version: CopyVersion = {
    n: copy.versions.length + 1,
    createdAt: when,
    content: c.value,
    ...(restoredFrom !== undefined ? { restoredFrom } : {}),
  };
  return valid({ ...copy, updatedAt: when, versions: [...copy.versions, version] });
}

export const variantsOf = (c: CopyRecord): readonly CopyVariant[] => c.variants ?? [];

const withVariants = (
  copy: CopyRecord,
  variants: readonly CopyVariant[],
  at: string,
): CopyRecord => {
  const { variants: _old, ...rest } = copy;
  void _old;
  return {
    ...rest,
    updatedAt: at < copy.updatedAt ? copy.updatedAt : at,
    ...(variants.length > 0 ? { variants } : {}),
  };
};

/** Agrega una variante. No toca el historial de versiones del copy. */
export function addVariant(
  copy: CopyRecord,
  input: { readonly id: string; readonly label: unknown; readonly content: unknown },
  at: string,
): Validation<CopyRecord> {
  const v = validateVariant({
    id: input.id,
    label: input.label,
    content: input.content,
    createdAt: at,
    updatedAt: at,
  });
  if (!v.ok) return v;
  const cur = variantsOf(copy);
  if (cur.length >= COPY_MAX_VARIANTS)
    return invalid(`Este copy llegó al máximo de ${COPY_MAX_VARIANTS} variantes.`);
  if (cur.some((x) => x.label.toLocaleLowerCase('es') === v.value.label.toLocaleLowerCase('es')))
    return invalid('Ya hay una variante con ese nombre.');
  return valid(withVariants(copy, [...cur, v.value], at));
}

/** Edita una variante EN SU LUGAR (sin versiones). */
export function updateVariant(
  copy: CopyRecord,
  input: { readonly variantId: string; readonly label: unknown; readonly content: unknown },
  at: string,
): Validation<CopyRecord> {
  const cur = variantsOf(copy);
  const old = cur.find((x) => x.id === input.variantId);
  if (!old) return invalid('La variante no existe.');
  const v = validateVariant({
    id: old.id,
    label: input.label,
    content: input.content,
    createdAt: old.createdAt,
    updatedAt: at < old.createdAt ? old.createdAt : at,
  });
  if (!v.ok) return v;
  if (
    cur.some(
      (x) =>
        x.id !== old.id &&
        x.label.toLocaleLowerCase('es') === v.value.label.toLocaleLowerCase('es'),
    )
  )
    return invalid('Ya hay una variante con ese nombre.');
  if (v.value.label === old.label && diffContent(old.content, v.value.content).length === 0)
    return invalid('No hay cambios respecto de la variante actual.');
  return valid(
    withVariants(
      copy,
      cur.map((x) => (x.id === old.id ? v.value : x)),
      at,
    ),
  );
}

export function removeVariant(
  copy: CopyRecord,
  variantId: string,
  at: string,
): Validation<CopyRecord> {
  const cur = variantsOf(copy);
  if (!cur.some((x) => x.id === variantId)) return invalid('La variante no existe.');
  return valid(
    withVariants(
      copy,
      cur.filter((x) => x.id !== variantId),
      at,
    ),
  );
}
