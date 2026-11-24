import { CHANNELS, type Channel } from './brief';
import { COPY_ID, validateCopyContent, type CopyContent } from './copy';
import { invalid, valid, type Validation } from './validation';

/**
 * Adaptación por canal (S2.8, función 7). Entidad independiente DERIVADA de un Copy de origen, con identidad y
 * trazabilidad propias: guarda el copy y la versión de la que partió. El canal de destino es el criterio de
 * adaptación. NO se audita directamente (no aprobado) ni implica aprobación o publicación. SUPUESTOS de Claude
 * (reversibles): varias adaptaciones por copy y canal son posibles; se edita en su lugar (sin versiones propias);
 * borrar el copy de origen se rechaza mientras tenga adaptaciones. Las llamadas no son canal aprobado.
 */
export interface AdaptationRecord {
  readonly id: string; // ada_…
  readonly copyId: string;
  /** Número de versión del copy de la que se derivó (trazabilidad). */
  readonly sourceVersion: number;
  readonly channel: Channel;
  readonly content: CopyContent;
  readonly createdAt: string;
  readonly updatedAt: string;
}

export const ADAPTATION_ID = /^ada_[A-Za-z0-9_-]{8,64}$/;
export const MAX_ADAPTATIONS = 5_000;
const ISO = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,3})?Z$/;
const isObject = (v: unknown): v is Record<string, unknown> =>
  typeof v === 'object' && v !== null && !Array.isArray(v);
const isIso = (v: unknown): v is string =>
  typeof v === 'string' && ISO.test(v) && !Number.isNaN(Date.parse(v));

export function validateAdaptationRecord(raw: unknown): Validation<AdaptationRecord> {
  if (
    !isObject(raw) ||
    !Object.keys(raw).every((k) =>
      ['id', 'copyId', 'sourceVersion', 'channel', 'content', 'createdAt', 'updatedAt'].includes(k),
    )
  )
    return invalid('La adaptación guardada no es válida.');
  if (typeof raw['id'] !== 'string' || !ADAPTATION_ID.test(raw['id']))
    return invalid('El identificador de la adaptación no es válido.');
  if (typeof raw['copyId'] !== 'string' || !COPY_ID.test(raw['copyId']))
    return invalid('El copy de origen no es válido.');
  const sv = raw['sourceVersion'];
  if (typeof sv !== 'number' || !Number.isInteger(sv) || sv < 1)
    return invalid('La versión de origen no es válida.');
  if (!CHANNELS.includes(raw['channel'] as Channel))
    return invalid('El canal de destino no es válido.');
  const content = validateCopyContent(raw['content']);
  if (!content.ok) return content;
  if (!isIso(raw['createdAt']) || !isIso(raw['updatedAt']) || raw['updatedAt'] < raw['createdAt'])
    return invalid('Las fechas de la adaptación no son válidas.');
  return valid({
    id: raw['id'],
    copyId: raw['copyId'],
    sourceVersion: sv,
    channel: raw['channel'] as Channel,
    content: content.value,
    createdAt: raw['createdAt'],
    updatedAt: raw['updatedAt'],
  });
}

export function compareAdaptationsNewestFirst(a: AdaptationRecord, b: AdaptationRecord): number {
  if (a.updatedAt !== b.updatedAt) return a.updatedAt < b.updatedAt ? 1 : -1;
  return a.id < b.id ? 1 : a.id > b.id ? -1 : 0;
}
