import { CHANNELS, type Channel } from './brief';
import {
  DEFAULT_BRAND_TERMS,
  DEFAULT_TOLERANCE_PP,
  normalize,
  type BrandTerm,
  type Legend,
  type RulesConfig,
  type Severity,
} from './copyRules';
import { invalid, valid, type Validation } from './validation';

/**
 * Configuración editable de reglas (S2.5b): leyendas y términos de marca capturados por el propietario. Se guarda en
 * IndexedDB y entra en el respaldo (v4). Sin configuración guardada se usa la plantilla de ejemplo (leyendas vacías
 * y términos de ejemplo NO validados). El permiso/aviso de publicidad se omite por decisión del propietario.
 */
export interface RulesDoc {
  readonly legends: readonly Legend[];
  readonly brandTerms: readonly BrandTerm[];
}

export const LEGEND_TEXT_MAX = 300;
export const TERM_TEXT_MAX = 80;
export const TERM_SUGGESTION_MAX = 120;
export const MAX_LEGENDS = 100;
export const MAX_TERMS = 200;
export const SEVERITIES: readonly Severity[] = ['critica', 'mayor', 'menor', 'aviso'];
export const TERM_KINDS = ['prohibido', 'preferido'] as const;

export const TEMPLATE_DOC: RulesDoc = { legends: [], brandTerms: DEFAULT_BRAND_TERMS };

const isObject = (v: unknown): v is Record<string, unknown> =>
  typeof v === 'object' && v !== null && !Array.isArray(v);
// eslint-disable-next-line no-control-regex
const CONTROL = /[\u0000-\u001f\u007f]/;
const onlyKeys = (o: Record<string, unknown>, allowed: readonly string[]) =>
  Object.keys(o).every((k) => allowed.includes(k));

function cleanText(v: unknown, max: number, what: string): Validation<string> {
  if (typeof v !== 'string') return invalid(`${what} debe ser texto.`);
  const t = v.trim();
  if (t === '') return invalid(`${what} no puede estar vacío.`);
  if (CONTROL.test(t)) return invalid(`${what} contiene caracteres no permitidos.`);
  if (t.length > max) return invalid(`${what} no puede pasar de ${max} caracteres.`);
  return valid(t);
}

export function validateLegend(raw: unknown): Validation<Legend> {
  if (!isObject(raw) || !onlyKeys(raw, ['text', 'channels', 'required', 'active']))
    return invalid('La leyenda no es válida.');
  const text = cleanText(raw['text'], LEGEND_TEXT_MAX, 'El texto de la leyenda');
  if (!text.ok) return text;
  const ch = raw['channels'];
  if (!Array.isArray(ch) || !ch.every((c) => CHANNELS.includes(c as Channel)))
    return invalid('Los canales de la leyenda no son válidos.');
  const channels = [...new Set(ch as Channel[])];
  if (typeof raw['required'] !== 'boolean' || typeof raw['active'] !== 'boolean')
    return invalid('La leyenda debe indicar si es obligatoria y si está activa.');
  return valid({ text: text.value, channels, required: raw['required'], active: raw['active'] });
}

export function validateBrandTerm(raw: unknown): Validation<BrandTerm> {
  if (!isObject(raw) || !onlyKeys(raw, ['text', 'kind', 'severity', 'suggestion']))
    return invalid('El término de marca no es válido.');
  const text = cleanText(raw['text'], TERM_TEXT_MAX, 'El término');
  if (!text.ok) return text;
  if (!TERM_KINDS.includes(raw['kind'] as 'prohibido'))
    return invalid('El tipo del término debe ser prohibido o preferido.');
  if (!SEVERITIES.includes(raw['severity'] as Severity))
    return invalid('La severidad del término no es válida.');
  let suggestion: string | undefined;
  if (raw['suggestion'] !== undefined && raw['suggestion'] !== '') {
    const s = cleanText(raw['suggestion'], TERM_SUGGESTION_MAX, 'La sugerencia');
    if (!s.ok) return s;
    suggestion = s.value;
  }
  return valid({
    text: text.value,
    kind: raw['kind'] as BrandTerm['kind'],
    severity: raw['severity'] as Severity,
    ...(suggestion !== undefined ? { suggestion } : {}),
  });
}

export function validateRulesDoc(raw: unknown): Validation<RulesDoc> {
  if (!isObject(raw) || !onlyKeys(raw, ['legends', 'brandTerms']))
    return invalid('La configuración de reglas no es válida.');
  const l = raw['legends'];
  const t = raw['brandTerms'];
  if (!Array.isArray(l) || l.length > MAX_LEGENDS)
    return invalid(`Las leyendas no son válidas (máximo ${MAX_LEGENDS}).`);
  if (!Array.isArray(t) || t.length > MAX_TERMS)
    return invalid(`Los términos no son válidos (máximo ${MAX_TERMS}).`);
  const legends: Legend[] = [];
  const seenL = new Set<string>();
  for (const item of l) {
    const v = validateLegend(item);
    if (!v.ok) return v;
    const key = normalize(v.value.text);
    if (seenL.has(key)) return invalid('Hay leyendas repetidas.');
    seenL.add(key);
    legends.push(v.value);
  }
  const brandTerms: BrandTerm[] = [];
  const seenT = new Set<string>();
  for (const item of t) {
    const v = validateBrandTerm(item);
    if (!v.ok) return v;
    const key = `${v.value.kind}|${normalize(v.value.text)}`;
    if (seenT.has(key)) return invalid('Hay términos de marca repetidos.');
    seenT.add(key);
    brandTerms.push(v.value);
  }
  return valid({ legends, brandTerms });
}

/** Forma canónica (orden de claves fijo) para la suma de integridad del respaldo. */
export function canonicalRules(d: RulesDoc | null): unknown {
  if (d === null) return null;
  return {
    legends: d.legends.map((x) => ({
      text: x.text,
      channels: x.channels,
      required: x.required,
      active: x.active,
    })),
    brandTerms: d.brandTerms.map((x) => ({
      text: x.text,
      kind: x.kind,
      severity: x.severity,
      ...(x.suggestion !== undefined ? { suggestion: x.suggestion } : {}),
    })),
  };
}

/** Configuración que consume el motor de reglas. */
export const toRulesConfig = (d: RulesDoc): RulesConfig => ({
  legends: d.legends,
  brandTerms: d.brandTerms,
  tolerancePp: DEFAULT_TOLERANCE_PP,
});
