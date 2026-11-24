import { RESOURCE_LIMITS, validateResourceRecord } from './resource';
import { validateReviewRecord, type ReviewRecord } from './review';
import { validatePieceRecord, type PieceRecord } from './piece';
import { validateMeasureRecord, type MeasureRecord } from './measure';
import { validatePromoRecord, type PromoRecord } from './promo';
import { invalid, valid, type Validation } from './validation';

/**
 * Respaldo de imágenes (S3.3b): archivo APARTE del respaldo JSON de datos (que tiene tope de 5 MB). Contiene cada
 * recurso con su imagen en base64 y su huella SHA-256 para detectar archivos dañados. Al restaurar solo se AGREGAN
 * los recursos que no existen (mismo id): nunca se reemplaza ni se borra nada. SUPUESTO: tope de 150 MB por archivo.
 */
export const RESOURCES_BACKUP_FORMAT = 'cci-recursos';
export const RESOURCES_BACKUP_VERSION = 4;
export const RESOURCES_BACKUP_MAX_BYTES = 150 * 1024 * 1024;

const isObject = (v: unknown): v is Record<string, unknown> =>
  typeof v === 'object' && v !== null && !Array.isArray(v);

export function backupFileName(now: Date): string {
  return `cci-recursos-${now.toISOString().slice(0, 10)}.json`;
}

export interface ParsedResourcesBackup {
  readonly resources: readonly { raw: Record<string, unknown>; sha256: string; data: string }[];
  readonly pieces: readonly PieceRecord[];
  readonly reviews: readonly ReviewRecord[];
  readonly measures: readonly MeasureRecord[];
  readonly promos: readonly PromoRecord[];
}

/** Valida la estructura (sin decodificar imágenes). Las versiones 1 a 3 (sin piezas, revisiones, mediciones o promociones) también se aceptan. */
export function parseResourcesBackup(text: string): Validation<ParsedResourcesBackup> {
  const bad = invalid<never>('El archivo no es un respaldo de imágenes válido.');
  if (text.length > RESOURCES_BACKUP_MAX_BYTES)
    return invalid('El archivo supera el máximo permitido.');
  let doc: unknown;
  try {
    doc = JSON.parse(text);
  } catch {
    return bad;
  }
  if (
    !isObject(doc) ||
    doc['format'] !== RESOURCES_BACKUP_FORMAT ||
    (doc['version'] !== 1 &&
      doc['version'] !== 2 &&
      doc['version'] !== 3 &&
      doc['version'] !== 4) ||
    !Array.isArray(doc['resources']) ||
    doc['resources'].length > RESOURCE_LIMITS.maxResources
  )
    return bad;
  const resources: { raw: Record<string, unknown>; sha256: string; data: string }[] = [];
  for (const item of doc['resources'] as unknown[]) {
    if (!isObject(item)) return bad;
    const { data, sha256, ...meta } = item;
    if (typeof data !== 'string' || typeof sha256 !== 'string' || !/^[0-9a-f]{64}$/.test(sha256))
      return bad;
    // El metadato se valida con un blob provisional: el real se arma al decodificar.
    if (!validateResourceRecord({ ...meta, blob: new Blob([]) }).ok) return bad;
    resources.push({ raw: meta, sha256, data });
  }
  const rawPieces = doc['pieces'] ?? [];
  if (!Array.isArray(rawPieces) || rawPieces.length > 500) return bad;
  const pieces: PieceRecord[] = [];
  for (const p of rawPieces as unknown[]) {
    const v = validatePieceRecord(p);
    if (!v.ok) return bad;
    pieces.push(v.value);
  }
  const rawReviews = doc['reviews'] ?? [];
  if (!Array.isArray(rawReviews) || rawReviews.length > 2000) return bad;
  const reviews: ReviewRecord[] = [];
  for (const r of rawReviews as unknown[]) {
    const v = validateReviewRecord(r);
    if (!v.ok) return bad;
    reviews.push(v.value);
  }
  const rawMeasures = doc['measures'] ?? [];
  if (!Array.isArray(rawMeasures) || rawMeasures.length > 3000) return bad;
  const measures: MeasureRecord[] = [];
  for (const m of rawMeasures as unknown[]) {
    const v = validateMeasureRecord(m);
    if (!v.ok) return bad;
    measures.push(v.value);
  }
  const rawPromos = doc['promos'] ?? [];
  if (!Array.isArray(rawPromos) || rawPromos.length > 1000) return bad;
  const promos: PromoRecord[] = [];
  for (const m of rawPromos as unknown[]) {
    const v = validatePromoRecord(m);
    if (!v.ok) return bad;
    promos.push(v.value);
  }
  return valid({ resources, pieces, reviews, measures, promos });
}
