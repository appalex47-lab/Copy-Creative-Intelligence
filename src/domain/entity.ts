import { normalize } from './copyRules';
import { invalid, valid, type Validation } from './validation';

/**
 * Campaña, Producto y Oferta (S2.8). Entidades independientes y SIMPLES: nombre y nota opcional. Por decisión del
 * propietario (documento de funciones de Fase 2) no se asumen atributos, relaciones obligatorias, estados ni ciclo de
 * vida: no hay precios, SKU, vigencias ni relación Producto–Oferta. Única relación implementada: un Brief puede
 * referenciar UNA campaña (opcional). SUPUESTOS de Claude (reversibles): nombre único por tipo (sin distinguir
 * mayúsculas ni acentos), máximo 500 por tipo, nota de hasta 500 caracteres.
 */
export const ENTITY_KINDS = ['campaign', 'product', 'offer'] as const;
export type EntityKind = (typeof ENTITY_KINDS)[number];
export const ENTITY_LABELS: Readonly<
  Record<EntityKind, { one: string; many: string; add: string; added: string }>
> = {
  campaign: {
    one: 'campaña',
    many: 'Campañas',
    add: 'Nueva campaña',
    added: 'Se agregó la campaña.',
  },
  product: {
    one: 'producto',
    many: 'Productos',
    add: 'Nuevo producto',
    added: 'Se agregó el producto.',
  },
  offer: { one: 'oferta', many: 'Ofertas', add: 'Nueva oferta', added: 'Se agregó la oferta.' },
};
export const ENTITY_PREFIX: Readonly<Record<EntityKind, string>> = {
  campaign: 'cmp',
  product: 'prd',
  offer: 'ofr',
};
export const ENTITY_NAME_MAX = 120;
export const ENTITY_NOTE_MAX = 500;
export const MAX_ENTITIES_PER_KIND = 500;

export interface EntityRecord {
  readonly id: string;
  readonly kind: EntityKind;
  readonly name: string;
  readonly note?: string;
  readonly createdAt: string;
  readonly updatedAt: string;
}

export const CAMPAIGN_ID = /^cmp_[A-Za-z0-9_-]{8,64}$/;
const ID_BY_KIND: Readonly<Record<EntityKind, RegExp>> = {
  campaign: CAMPAIGN_ID,
  product: /^prd_[A-Za-z0-9_-]{8,64}$/,
  offer: /^ofr_[A-Za-z0-9_-]{8,64}$/,
};
export const ENTITY_ID = /^(cmp|prd|ofr)_[A-Za-z0-9_-]{8,64}$/;
const ISO = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,3})?Z$/;
// eslint-disable-next-line no-control-regex
const CONTROL = /[\u0000-\u0008\u000b-\u001f\u007f]/;
const isObject = (v: unknown): v is Record<string, unknown> =>
  typeof v === 'object' && v !== null && !Array.isArray(v);
const isIso = (v: unknown): v is string =>
  typeof v === 'string' && ISO.test(v) && !Number.isNaN(Date.parse(v));

export function validateEntityName(input: unknown): Validation<string> {
  if (typeof input !== 'string') return invalid('El nombre debe ser texto.');
  const t = input.replace(/\s+/g, ' ').trim();
  if (t === '') return invalid('El nombre es obligatorio.');
  if (CONTROL.test(t)) return invalid('El nombre contiene caracteres no permitidos.');
  if ([...t].length > ENTITY_NAME_MAX)
    return invalid(`El nombre admite como máximo ${ENTITY_NAME_MAX} caracteres.`);
  return valid(t);
}

export function validateEntityNote(input: unknown): Validation<string | undefined> {
  if (input === undefined || input === null) return valid(undefined);
  if (typeof input !== 'string') return invalid('La nota debe ser texto.');
  const t = input
    .replace(/[ \t]+/g, ' ')
    .replace(/\n{3,}/g, '\n\n')
    .trim();
  if (t === '') return valid(undefined);
  if (CONTROL.test(t)) return invalid('La nota contiene caracteres no permitidos.');
  if ([...t].length > ENTITY_NOTE_MAX)
    return invalid(`La nota admite como máximo ${ENTITY_NOTE_MAX} caracteres.`);
  return valid(t);
}

export function validateEntityRecord(raw: unknown): Validation<EntityRecord> {
  if (
    !isObject(raw) ||
    !Object.keys(raw).every((k) =>
      ['id', 'kind', 'name', 'note', 'createdAt', 'updatedAt'].includes(k),
    )
  )
    return invalid('El registro no es válido.');
  const kind = raw['kind'];
  if (!ENTITY_KINDS.includes(kind as EntityKind))
    return invalid('El tipo de registro no es válido.');
  const k = kind as EntityKind;
  if (typeof raw['id'] !== 'string' || !ID_BY_KIND[k].test(raw['id']))
    return invalid('El identificador no es válido.');
  const name = validateEntityName(raw['name']);
  if (!name.ok) return name;
  const note = validateEntityNote(raw['note']);
  if (!note.ok) return note;
  if (!isIso(raw['createdAt']) || !isIso(raw['updatedAt']) || raw['updatedAt'] < raw['createdAt'])
    return invalid('Las fechas no son válidas.');
  return valid({
    id: raw['id'],
    kind: k,
    name: name.value,
    ...(note.value !== undefined ? { note: note.value } : {}),
    createdAt: raw['createdAt'],
    updatedAt: raw['updatedAt'],
  });
}

/** Clave de unicidad por tipo (sin distinguir mayúsculas ni acentos). */
export const entityKey = (e: Pick<EntityRecord, 'kind' | 'name'>): string =>
  `${e.kind}|${normalize(e.name)}`;

/** Orden alfabético por nombre (es), para listas estables. */
export const compareEntities = (a: EntityRecord, b: EntityRecord): number =>
  a.name.localeCompare(b.name, 'es') || (a.id < b.id ? -1 : 1);
