import { columnIndex, parseCsv } from './csvParse';
import { invalid, valid, type Validation } from './validation';

/**
 * Medición y aprendizaje (S4.2; etapa 7 de la metodología CCI). Dos tipos de registro, capturados por una persona o
 * importados por CSV (la app no se conecta a ninguna plataforma de medición):
 *  - resultado: impresiones, clics, conversiones y ventas de una pieza o copy en un periodo;
 *  - experimento A/B: hipótesis, variable, indicador principal y secundario, y las dos variantes con sus cifras.
 * CTR = clics / impresiones; conversión = conversiones / clics (SUPUESTO: conversión sobre clics). La comparación A/B es
 * ORIENTATIVA: prueba z de dos proporciones, con aviso de muestra pequeña (menos de 100 en la base de cualquier variante).
 * No se declara ganador sin diferencia significativa (p < 0.05).
 */
export const MEASURE_ID = /^mea_[A-Za-z0-9_-]{8,64}$/;
export const MAX_MEASURES = 3_000;
export const MAX_IMPORT_ROWS = 500;
export const MIN_SAMPLE = 100;
export const METRICS = ['ctr', 'conversion'] as const;
export type Metric = (typeof METRICS)[number];
export const METRIC_LABELS: Readonly<Record<Metric, string>> = {
  ctr: 'CTR',
  conversion: 'Conversión',
};

export interface Figures {
  readonly impressions: number;
  readonly clicks: number;
  readonly conversions: number;
}
export interface ResultRecord extends Figures {
  readonly kind: 'resultado';
  readonly id: string;
  readonly label: string;
  readonly targetType?: 'copy' | 'pieza';
  readonly targetId?: string;
  readonly sales?: number;
  readonly from?: string;
  readonly to?: string;
  readonly note?: string;
  readonly createdAt: string;
}
export interface Variant extends Figures {
  readonly label: string;
}
export interface ExperimentRecord {
  readonly kind: 'experimento';
  readonly id: string;
  readonly name: string;
  readonly hypothesis: string;
  readonly variable: string;
  readonly primary: Metric;
  readonly secondary?: Metric;
  readonly variants: readonly [Variant, Variant];
  readonly conclusion?: string;
  readonly createdAt: string;
  readonly updatedAt: string;
}
export type MeasureRecord = ResultRecord | ExperimentRecord;

const ISO = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,3})?Z$/;
const DAY = /^\d{4}-\d{2}-\d{2}$/;
const isObject = (v: unknown): v is Record<string, unknown> =>
  typeof v === 'object' && v !== null && !Array.isArray(v);
const isIso = (v: unknown): v is string =>
  typeof v === 'string' && ISO.test(v) && !Number.isNaN(Date.parse(v));
const isDay = (v: unknown): v is string =>
  typeof v === 'string' && DAY.test(v) && !Number.isNaN(Date.parse(v));
const str = (v: unknown, max: number): v is string =>
  typeof v === 'string' && v.trim().length > 0 && [...v].length <= max;
const int = (v: unknown): v is number =>
  typeof v === 'number' && Number.isInteger(v) && v >= 0 && v <= 1_000_000_000;

export function validateFigures(f: unknown): Validation<Figures> {
  if (!isObject(f) || !int(f['impressions']) || !int(f['clicks']) || !int(f['conversions']))
    return invalid('Impresiones, clics y conversiones deben ser números enteros de 0 o más.');
  if (f['clicks'] > f['impressions'])
    return invalid('Los clics no pueden superar las impresiones.');
  if (f['conversions'] > f['clicks'])
    return invalid('Las conversiones no pueden superar los clics.');
  return valid({
    impressions: f['impressions'],
    clicks: f['clicks'],
    conversions: f['conversions'],
  });
}

export const ctr = (f: Figures): number | null =>
  f.impressions > 0 ? f.clicks / f.impressions : null;
export const conversionRate = (f: Figures): number | null =>
  f.clicks > 0 ? f.conversions / f.clicks : null;
const rate = (f: Figures, m: Metric) => (m === 'ctr' ? ctr(f) : conversionRate(f));
const base = (f: Figures, m: Metric) => (m === 'ctr' ? f.impressions : f.clicks);
const hits = (f: Figures, m: Metric) => (m === 'ctr' ? f.clicks : f.conversions);
export const pct = (x: number | null): string =>
  x === null ? 'sin datos' : `${(x * 100).toFixed(2)} %`;

function erf(x: number): number {
  const t = 1 / (1 + 0.3275911 * Math.abs(x));
  const y =
    1 -
    ((((1.061405429 * t - 1.453152027) * t + 1.421413741) * t - 0.284496736) * t + 0.254829592) *
      t *
      Math.exp(-x * x);
  return x >= 0 ? y : -y;
}

export interface ExperimentAnalysis {
  readonly rateA: number | null;
  readonly rateB: number | null;
  /** Diferencia relativa de B frente a A. */
  readonly lift: number | null;
  readonly p: number | null;
  readonly smallSample: boolean;
  readonly winner: 'A' | 'B' | null;
  readonly message: string;
}

export function analyzeExperiment(
  e: ExperimentRecord,
  metric: Metric = e.primary,
): ExperimentAnalysis {
  const [a, b] = e.variants;
  const ra = rate(a, metric);
  const rb = rate(b, metric);
  const na = base(a, metric);
  const nb = base(b, metric);
  const smallSample = na < MIN_SAMPLE || nb < MIN_SAMPLE;
  if (ra === null || rb === null || na === 0 || nb === 0)
    return {
      rateA: ra,
      rateB: rb,
      lift: null,
      p: null,
      smallSample: true,
      winner: null,
      message: 'Faltan datos para comparar.',
    };
  const lift = ra > 0 ? (rb - ra) / ra : null;
  const pooled = (hits(a, metric) + hits(b, metric)) / (na + nb);
  const se = Math.sqrt(pooled * (1 - pooled) * (1 / na + 1 / nb));
  const z = se === 0 ? 0 : (rb - ra) / se;
  const p = se === 0 ? 1 : 1 - erf(Math.abs(z) / Math.SQRT2);
  const significant = p < 0.05;
  const winner = significant && !smallSample ? (rb > ra ? 'B' : 'A') : null;
  const message = smallSample
    ? `Muestra pequeña (menos de ${String(MIN_SAMPLE)} en la base de alguna variante): no se puede concluir.`
    : winner
      ? `Diferencia significativa a favor de la variante ${winner} (p = ${p.toFixed(3)}). Orientativo.`
      : `Sin diferencia significativa (p = ${p.toFixed(3)}): no declares ganador.`;
  return { rateA: ra, rateB: rb, lift, p, smallSample, winner, message };
}

function validateVariant(v: unknown): Validation<Variant> {
  if (!isObject(v) || !str(v['label'], 60))
    return invalid('Cada variante necesita un nombre (hasta 60 caracteres).');
  const f = validateFigures(v);
  if (!f.ok) return invalid(f.reason);
  return valid({ label: v['label'].trim(), ...f.value });
}

export function validateMeasureRecord(raw: unknown): Validation<MeasureRecord> {
  const bad = invalid<MeasureRecord>('El registro de medición no es válido.');
  if (
    !isObject(raw) ||
    typeof raw['id'] !== 'string' ||
    !MEASURE_ID.test(raw['id']) ||
    !isIso(raw['createdAt'])
  )
    return bad;
  if (raw['kind'] === 'resultado') {
    if (!str(raw['label'], 120)) return bad;
    const f = validateFigures(raw);
    if (!f.ok) return invalid(f.reason);
    if (
      raw['sales'] !== undefined &&
      (typeof raw['sales'] !== 'number' || !(raw['sales'] >= 0) || raw['sales'] > 1e12)
    )
      return bad;
    if (raw['from'] !== undefined && !isDay(raw['from'])) return bad;
    if (raw['to'] !== undefined && !isDay(raw['to'])) return bad;
    if (typeof raw['from'] === 'string' && typeof raw['to'] === 'string' && raw['from'] > raw['to'])
      return invalid('La fecha inicial no puede ser posterior a la final.');
    if (raw['note'] !== undefined && !str(raw['note'], 300)) return bad;
    if (
      raw['targetType'] !== undefined &&
      raw['targetType'] !== 'copy' &&
      raw['targetType'] !== 'pieza'
    )
      return bad;
    return valid({
      kind: 'resultado',
      id: raw['id'],
      label: raw['label'].trim(),
      ...f.value,
      ...(raw['targetType'] !== undefined
        ? { targetType: raw['targetType'] as 'copy' | 'pieza' }
        : {}),
      ...(typeof raw['targetId'] === 'string' ? { targetId: raw['targetId'] } : {}),
      ...(typeof raw['sales'] === 'number' ? { sales: raw['sales'] } : {}),
      ...(typeof raw['from'] === 'string' ? { from: raw['from'] } : {}),
      ...(typeof raw['to'] === 'string' ? { to: raw['to'] } : {}),
      ...(typeof raw['note'] === 'string' ? { note: raw['note'].trim() } : {}),
      createdAt: raw['createdAt'],
    });
  }
  if (raw['kind'] === 'experimento') {
    if (!str(raw['name'], 120) || !str(raw['hypothesis'], 300) || !str(raw['variable'], 120))
      return invalid('El experimento necesita nombre, hipótesis y variable.');
    if (!METRICS.includes(raw['primary'] as Metric))
      return invalid('Elige el indicador principal.');
    if (
      raw['secondary'] !== undefined &&
      raw['secondary'] !== '' &&
      !METRICS.includes(raw['secondary'] as Metric)
    )
      return bad;
    if (raw['secondary'] === raw['primary'])
      return invalid('El indicador secundario debe ser distinto del principal.');
    if (!Array.isArray(raw['variants']) || raw['variants'].length !== 2)
      return invalid('Un experimento A/B tiene dos variantes.');
    const a = validateVariant(raw['variants'][0]);
    if (!a.ok) return invalid(a.reason);
    const b = validateVariant(raw['variants'][1]);
    if (!b.ok) return invalid(b.reason);
    if (raw['conclusion'] !== undefined && raw['conclusion'] !== '' && !str(raw['conclusion'], 500))
      return bad;
    if (!isIso(raw['updatedAt'])) return bad;
    return valid({
      kind: 'experimento',
      id: raw['id'],
      name: raw['name'].trim(),
      hypothesis: raw['hypothesis'].trim(),
      variable: raw['variable'].trim(),
      primary: raw['primary'] as Metric,
      ...(raw['secondary'] ? { secondary: raw['secondary'] as Metric } : {}),
      variants: [a.value, b.value],
      ...(typeof raw['conclusion'] === 'string' && raw['conclusion'] !== ''
        ? { conclusion: raw['conclusion'].trim() }
        : {}),
      createdAt: raw['createdAt'],
      updatedAt: raw['updatedAt'],
    });
  }
  return bad;
}

export const compareMeasuresNewestFirst = (a: MeasureRecord, b: MeasureRecord): number => {
  const ka = a.kind === 'experimento' ? a.updatedAt : a.createdAt;
  const kb = b.kind === 'experimento' ? b.updatedAt : b.createdAt;
  return ka < kb ? 1 : ka > kb ? -1 : a.id < b.id ? 1 : -1;
};

export interface ResultRow {
  readonly label: string;
  readonly impressions: number;
  readonly clicks: number;
  readonly conversions: number;
  readonly sales?: number;
  readonly from?: string;
  readonly to?: string;
  readonly note?: string;
}

/** Importa resultados desde CSV. Columnas: objetivo, impresiones, clics, conversiones, [ventas, desde, hasta, nota]. Todo o nada. */
export function parseResultsCsv(text: string): Validation<readonly ResultRow[]> {
  const t = parseCsv(text);
  if (!t) return invalid('El archivo no es un CSV válido.');
  const c = (...n: string[]) => columnIndex(t.header, ...n);
  const iLabel = c('objetivo', 'pieza', 'nombre', 'copy');
  const iImp = c('impresiones');
  const iClk = c('clics', 'clicks');
  const iCnv = c('conversiones');
  if ([iLabel, iImp, iClk, iCnv].some((i) => i < 0))
    return invalid('Faltan columnas: objetivo, impresiones, clics y conversiones.');
  const iSales = c('ventas');
  const iFrom = c('desde');
  const iTo = c('hasta');
  const iNote = c('nota');
  if (t.rows.length === 0) return invalid('El archivo no tiene filas.');
  if (t.rows.length > MAX_IMPORT_ROWS)
    return invalid(`Se admiten hasta ${String(MAX_IMPORT_ROWS)} filas.`);
  const num = (s: string | undefined) =>
    Number((s ?? '').trim().replaceAll(',', '').replace(/\s/g, ''));
  const out: ResultRow[] = [];
  for (const [n, r] of t.rows.entries()) {
    const at = `Fila ${String(n + 2)}`;
    const label = (r[iLabel] ?? '').trim();
    const row = { impressions: num(r[iImp]), clicks: num(r[iClk]), conversions: num(r[iCnv]) };
    if (label === '' || [...label].length > 120)
      return invalid(`${at}: el objetivo es obligatorio (hasta 120 caracteres).`);
    const f = validateFigures(row);
    if (!f.ok) return invalid(`${at}: ${f.reason}`);
    const salesRaw = iSales >= 0 ? (r[iSales] ?? '').trim() : '';
    const sales = salesRaw === '' ? undefined : num(salesRaw);
    if (sales !== undefined && !(sales >= 0)) return invalid(`${at}: las ventas no son válidas.`);
    const from = iFrom >= 0 ? (r[iFrom] ?? '').trim() : '';
    const to = iTo >= 0 ? (r[iTo] ?? '').trim() : '';
    if ((from !== '' && !isDay(from)) || (to !== '' && !isDay(to)))
      return invalid(`${at}: las fechas deben ser AAAA-MM-DD.`);
    const note = iNote >= 0 ? (r[iNote] ?? '').trim() : '';
    if ([...note].length > 300) return invalid(`${at}: la nota admite hasta 300 caracteres.`);
    out.push({
      label,
      ...f.value,
      ...(sales !== undefined ? { sales } : {}),
      ...(from !== '' ? { from } : {}),
      ...(to !== '' ? { to } : {}),
      ...(note !== '' ? { note } : {}),
    });
  }
  return valid(out);
}
