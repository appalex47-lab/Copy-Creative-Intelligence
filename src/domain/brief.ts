import { invalid, valid, type Validation } from './validation';

/**
 * Brief de Copy Studio (R-020, AC2-01/02). Los 13 campos salen de la matriz de requisitos.
 * SUPUESTOS de Claude aprobados por el propietario (S2.1, reversibles):
 *  - Obligatorios para estar «completo»: campaña, objetivo, producto, audiencia, mensaje, canal y CTA.
 *  - Opcionales: oferta, beneficio, vigencia, condiciones, tono y formato.
 *  - Longitud máxima: 120 caracteres en campos de una línea y 500 en campos de texto largo.
 * Un brief incompleto es un estado explícito con el motivo por campo; nunca se rellena ni se infiere un valor.
 */
export const CHANNELS = [
  'Ecommerce',
  'App',
  'WhatsApp',
  'Email',
  'Redes sociales',
  'Banners',
  'Landing pages',
] as const;
export type Channel = (typeof CHANNELS)[number];

export const BRIEF_SHORT_MAX = 120;
export const BRIEF_LONG_MAX = 500;

export interface BriefValidity {
  readonly from?: string; // AAAA-MM-DD
  readonly to?: string; // AAAA-MM-DD
}

export interface BriefFields {
  readonly campaign: string;
  readonly objective: string;
  readonly product: string;
  readonly audience: string;
  readonly offer?: string;
  readonly benefit?: string;
  readonly validity?: BriefValidity;
  readonly conditions?: string;
  readonly tone?: string;
  readonly message: string;
  readonly channel: Channel;
  readonly format?: string;
  readonly cta: string;
}

export type BriefField = keyof BriefFields;

export const BRIEF_FIELD_LABELS: Readonly<Record<BriefField, string>> = {
  campaign: 'Campaña',
  objective: 'Objetivo',
  product: 'Producto',
  audience: 'Audiencia',
  offer: 'Oferta',
  benefit: 'Beneficio',
  validity: 'Vigencia',
  conditions: 'Condiciones',
  tone: 'Tono',
  message: 'Mensaje central',
  channel: 'Canal',
  format: 'Formato',
  cta: 'CTA',
};

export const REQUIRED_FIELDS: readonly BriefField[] = [
  'campaign',
  'objective',
  'product',
  'audience',
  'message',
  'channel',
  'cta',
];

const LONG_FIELDS: ReadonlySet<BriefField> = new Set([
  'objective',
  'audience',
  'offer',
  'benefit',
  'conditions',
  'message',
]);

export interface FieldIssue {
  readonly field: BriefField;
  readonly reason: string;
}

export interface BriefEvaluation {
  /** «completo» solo si todos los obligatorios existen y ningún campo es inválido. */
  readonly status: 'completo' | 'incompleto';
  readonly brief: Partial<Record<BriefField, unknown>>;
  /** Campos obligatorios sin valor. */
  readonly missing: readonly FieldIssue[];
  /** Campos con valor pero inválido. */
  readonly invalid: readonly FieldIssue[];
}

// eslint-disable-next-line no-control-regex
const CONTROL = /[\u0000-\u0008\u000b-\u001f\u007f]/;
const DATE = /^\d{4}-\d{2}-\d{2}$/;

function isRealDate(s: string): boolean {
  if (!DATE.test(s)) return false;
  const [y, m, d] = s.split('-').map(Number) as [number, number, number];
  const dt = new Date(Date.UTC(y, m - 1, d));
  return dt.getUTCFullYear() === y && dt.getUTCMonth() === m - 1 && dt.getUTCDate() === d;
}

/** Valida un campo de texto; vacío o solo espacios = sin valor (undefined). */
export function validateBriefText(
  field: BriefField,
  input: unknown,
): Validation<string | undefined> {
  if (input === undefined || input === null) return valid(undefined);
  const label = BRIEF_FIELD_LABELS[field];
  if (typeof input !== 'string') return invalid(`${label} debe ser texto.`);
  const long = LONG_FIELDS.has(field);
  if (!long && /[\n\r]/.test(input.trim())) return invalid(`${label} debe ir en una sola línea.`);
  const text = (
    long ? input.replace(/[ \t]+/g, ' ').replace(/\n{3,}/g, '\n\n') : input.replace(/\s+/g, ' ')
  ).trim();
  if (text === '') return valid(undefined);
  if (CONTROL.test(text)) return invalid(`${label} contiene caracteres no permitidos.`);
  const max = long ? BRIEF_LONG_MAX : BRIEF_SHORT_MAX;
  if ([...text].length > max) return invalid(`${label} admite como máximo ${max} caracteres.`);
  return valid(text);
}

export function validateChannel(input: unknown): Validation<Channel | undefined> {
  if (input === undefined || input === null || input === '') return valid(undefined);
  if (typeof input !== 'string' || !(CHANNELS as readonly string[]).includes(input))
    return invalid(`Canal no aprobado. Canales válidos: ${CHANNELS.join(', ')}.`);
  return valid(input as Channel);
}

export function validateValidity(input: unknown): Validation<BriefValidity | undefined> {
  if (input === undefined || input === null) return valid(undefined);
  if (typeof input !== 'object') return invalid('La vigencia debe indicar fechas.');
  const r = input as Record<string, unknown>;
  const parts: { from?: string; to?: string } = {};
  for (const k of ['from', 'to'] as const) {
    const v = r[k];
    if (v === undefined || v === null || v === '') continue;
    if (typeof v !== 'string' || !isRealDate(v))
      return invalid(
        `La vigencia «${k === 'from' ? 'desde' : 'hasta'}» debe ser una fecha real AAAA-MM-DD.`,
      );
    parts[k] = v;
  }
  if (parts.from !== undefined && parts.to !== undefined && parts.from > parts.to)
    return invalid('La vigencia «desde» no puede ser posterior a «hasta».');
  return Object.keys(parts).length === 0 ? valid(undefined) : valid(parts);
}

/** Evalúa un brief (posiblemente parcial) y explica qué falta y qué es inválido. Determinista y sin efectos. */
export function evaluateBrief(input: unknown): BriefEvaluation {
  const raw = typeof input === 'object' && input !== null ? (input as Record<string, unknown>) : {};
  const brief: Partial<Record<BriefField, unknown>> = {};
  const missing: FieldIssue[] = [];
  const bad: FieldIssue[] = [];

  const textFields: BriefField[] = [
    'campaign',
    'objective',
    'product',
    'audience',
    'offer',
    'benefit',
    'conditions',
    'tone',
    'message',
    'format',
    'cta',
  ];
  const results: [BriefField, Validation<unknown>][] = [
    ...textFields.map((f): [BriefField, Validation<unknown>] => [f, validateBriefText(f, raw[f])]),
    ['channel', validateChannel(raw['channel'])],
    ['validity', validateValidity(raw['validity'])],
  ];
  for (const [field, v] of results) {
    if (!v.ok) bad.push({ field, reason: v.reason });
    else if (v.value !== undefined) brief[field] = v.value;
  }
  for (const field of REQUIRED_FIELDS) {
    if (bad.some((b) => b.field === field)) continue;
    if (brief[field] === undefined)
      missing.push({ field, reason: `Falta ${BRIEF_FIELD_LABELS[field]} (obligatorio).` });
  }
  const order = Object.keys(BRIEF_FIELD_LABELS);
  const byOrder = (a: FieldIssue, b: FieldIssue): number =>
    order.indexOf(a.field) - order.indexOf(b.field);
  missing.sort(byOrder);
  bad.sort(byOrder);
  return {
    status: missing.length === 0 && bad.length === 0 ? 'completo' : 'incompleto',
    brief,
    missing,
    invalid: bad,
  };
}
