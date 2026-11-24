import { columnIndex, parseCsv } from './csvParse';
import { extractPercents, type Severity } from './copyRules';
import { invalid, valid, type Validation } from './validation';

/**
 * Validador de promociones (S4.2; módulo 3 de la metodología CCI). Las promociones las captura o importa una persona
 * (la app no las inventa ni consulta el catálogo): nombre, porcentaje, SKUs, vigencia y restricciones. El validador
 * contrasta el TEXTO de un copy o de una pieza (el validado o el detectado por OCR) con la promoción elegida. No
 * verifica disponibilidad, precios en pesos ni SKUs dentro de imágenes. Tolerancia de porcentaje: 0.5 pp (Q-1).
 */
export const PROMO_ID = /^prm_[A-Za-z0-9_-]{8,64}$/;
export const MAX_PROMOS = 1_000;
export const MAX_SKUS = 500;
export const PROMO_TOLERANCE_PP = 0.5;

export interface PromoRecord {
  readonly id: string;
  readonly name: string;
  readonly discountPct?: number;
  readonly skus: readonly string[];
  readonly from?: string;
  readonly to?: string;
  readonly restrictions?: string;
  readonly createdAt: string;
}

const ISO = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,3})?Z$/;
const DAY = /^\d{4}-\d{2}-\d{2}$/;
const isObject = (v: unknown): v is Record<string, unknown> =>
  typeof v === 'object' && v !== null && !Array.isArray(v);
const isDay = (v: unknown): v is string =>
  typeof v === 'string' && DAY.test(v) && !Number.isNaN(Date.parse(v));

export function validatePromoRecord(raw: unknown): Validation<PromoRecord> {
  const bad = invalid<PromoRecord>('La promoción no es válida.');
  if (!isObject(raw) || typeof raw['id'] !== 'string' || !PROMO_ID.test(raw['id'])) return bad;
  const name = typeof raw['name'] === 'string' ? raw['name'].trim() : '';
  if (name.length === 0 || [...name].length > 120)
    return invalid('El nombre es obligatorio (hasta 120 caracteres).');
  const d = raw['discountPct'];
  if (d !== undefined && (typeof d !== 'number' || !(d > 0) || d > 100))
    return invalid('El porcentaje debe estar entre 0 y 100.');
  const skusRaw = raw['skus'] ?? [];
  if (
    !Array.isArray(skusRaw) ||
    skusRaw.length > MAX_SKUS ||
    skusRaw.some((s) => typeof s !== 'string' || s.trim() === '' || s.length > 40)
  )
    return invalid(`Hasta ${String(MAX_SKUS)} SKUs de máximo 40 caracteres.`);
  const from = raw['from'];
  const to = raw['to'];
  if ((from !== undefined && !isDay(from)) || (to !== undefined && !isDay(to)))
    return invalid('Las fechas deben ser AAAA-MM-DD.');
  if (typeof from === 'string' && typeof to === 'string' && from > to)
    return invalid('La fecha inicial no puede ser posterior a la final.');
  const r = raw['restrictions'];
  if (r !== undefined && (typeof r !== 'string' || [...r].length > 500))
    return invalid('Las restricciones admiten hasta 500 caracteres.');
  if (typeof raw['createdAt'] !== 'string' || !ISO.test(raw['createdAt'])) return bad;
  return valid({
    id: raw['id'],
    name,
    ...(typeof d === 'number' ? { discountPct: d } : {}),
    skus: [...new Set((skusRaw as string[]).map((s) => s.trim()))],
    ...(typeof from === 'string' ? { from } : {}),
    ...(typeof to === 'string' ? { to } : {}),
    ...(typeof r === 'string' && r.trim() !== '' ? { restrictions: r.trim() } : {}),
    createdAt: raw['createdAt'],
  });
}

export const comparePromosByName = (a: PromoRecord, b: PromoRecord): number =>
  a.name.localeCompare(b.name, 'es') || (a.id < b.id ? -1 : 1);

export interface PromoCheck {
  readonly severity: Severity;
  readonly message: string;
}

/** Contrasta un texto con una promoción. `today` es AAAA-MM-DD (se inyecta para poder probarlo). */
export function checkTextAgainstPromo(
  text: string,
  promo: PromoRecord,
  today: string,
): readonly PromoCheck[] {
  const out: PromoCheck[] = [];
  if (promo.to !== undefined && promo.to < today)
    out.push({ severity: 'critica', message: `La promoción venció el ${promo.to}.` });
  if (promo.from !== undefined && promo.from > today)
    out.push({ severity: 'aviso', message: `La promoción aún no inicia (desde ${promo.from}).` });
  const found = extractPercents(text);
  if (promo.discountPct !== undefined) {
    if (found.length === 0)
      out.push({
        severity: 'mayor',
        message: `El texto no menciona el descuento de la promoción (${String(promo.discountPct)} %).`,
      });
    for (const p of found)
      if (Math.abs(p - promo.discountPct) > PROMO_TOLERANCE_PP)
        out.push({
          severity: 'critica',
          message: `El texto dice ${String(p)} % pero la promoción es de ${String(promo.discountPct)} %.`,
        });
  } else if (found.length > 0)
    out.push({
      severity: 'mayor',
      message: `El texto menciona ${found.map(String).join(', ')} % pero la promoción no define porcentaje.`,
    });
  if (promo.restrictions && !/restricci|condicion|aplican|vigencia|t[eé]rminos|\*/i.test(text))
    out.push({
      severity: 'menor',
      message: 'La promoción tiene restricciones y el texto no parece comunicarlas.',
    });
  return out;
}

/** Importa promociones desde CSV: nombre, porcentaje, sku, desde, hasta, restricciones. Filas con el mismo nombre se unen. */
export function parsePromosCsv(
  text: string,
): Validation<readonly Omit<PromoRecord, 'id' | 'createdAt'>[]> {
  const t = parseCsv(text);
  if (!t) return invalid('El archivo no es un CSV válido.');
  const c = (...n: string[]) => columnIndex(t.header, ...n);
  const iName = c('nombre', 'promocion', 'promoción');
  if (iName < 0) return invalid('Falta la columna «nombre».');
  const iPct = c('porcentaje', 'descuento');
  const iSku = c('sku');
  const iFrom = c('desde');
  const iTo = c('hasta');
  const iRes = c('restricciones');
  if (t.rows.length === 0) return invalid('El archivo no tiene filas.');
  if (t.rows.length > 5_000) return invalid('Se admiten hasta 5 000 filas.');
  const map = new Map<
    string,
    {
      name: string;
      discountPct?: number;
      skus: string[];
      from?: string;
      to?: string;
      restrictions?: string;
    }
  >();
  for (const [n, r] of t.rows.entries()) {
    const at = `Fila ${String(n + 2)}`;
    const name = (r[iName] ?? '').trim();
    if (name === '') return invalid(`${at}: el nombre es obligatorio.`);
    const cur = map.get(name) ?? { name, skus: [] };
    const pctRaw = iPct >= 0 ? (r[iPct] ?? '').trim().replace('%', '').replace(',', '.') : '';
    if (pctRaw !== '') {
      const p = Number(pctRaw);
      if (!(p > 0) || p > 100) return invalid(`${at}: el porcentaje no es válido.`);
      cur.discountPct = p;
    }
    const sku = iSku >= 0 ? (r[iSku] ?? '').trim() : '';
    if (sku !== '') cur.skus.push(sku);
    const from = iFrom >= 0 ? (r[iFrom] ?? '').trim() : '';
    const to = iTo >= 0 ? (r[iTo] ?? '').trim() : '';
    if ((from !== '' && !isDay(from)) || (to !== '' && !isDay(to)))
      return invalid(`${at}: las fechas deben ser AAAA-MM-DD.`);
    if (from !== '') cur.from = from;
    if (to !== '') cur.to = to;
    const res = iRes >= 0 ? (r[iRes] ?? '').trim() : '';
    if (res !== '') cur.restrictions = res;
    map.set(name, cur);
  }
  const out: Omit<PromoRecord, 'id' | 'createdAt'>[] = [];
  for (const m of map.values()) {
    const v = validatePromoRecord({
      id: 'prm_validate0',
      createdAt: '2000-01-01T00:00:00.000Z',
      ...m,
    });
    if (!v.ok) return invalid(`«${m.name}»: ${v.reason}`);
    out.push({
      name: v.value.name,
      skus: v.value.skus,
      ...(v.value.discountPct !== undefined ? { discountPct: v.value.discountPct } : {}),
      ...(v.value.from !== undefined ? { from: v.value.from } : {}),
      ...(v.value.to !== undefined ? { to: v.value.to } : {}),
      ...(v.value.restrictions !== undefined ? { restrictions: v.value.restrictions } : {}),
    });
  }
  return valid(out);
}
