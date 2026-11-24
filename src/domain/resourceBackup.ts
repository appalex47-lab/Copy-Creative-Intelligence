import { RESOURCE_LIMITS, validateResourceRecord } from './resource';
import { invalid, valid, type Validation } from './validation';

/**
 * Respaldo de imágenes (S3.3b): archivo APARTE del respaldo JSON de datos (que tiene tope de 5 MB). Contiene cada
 * recurso con su imagen en base64 y su huella SHA-256 para detectar archivos dañados. Al restaurar solo se AGREGAN
 * los recursos que no existen (mismo id): nunca se reemplaza ni se borra nada. SUPUESTO: tope de 150 MB por archivo.
 */
export const RESOURCES_BACKUP_FORMAT = 'cci-recursos';
export const RESOURCES_BACKUP_VERSION = 1;
export const RESOURCES_BACKUP_MAX_BYTES = 150 * 1024 * 1024;

const isObject = (v: unknown): v is Record<string, unknown> =>
  typeof v === 'object' && v !== null && !Array.isArray(v);

export function backupFileName(now: Date): string {
  return `cci-recursos-${now.toISOString().slice(0, 10)}.json`;
}

/** Valida la estructura (sin decodificar imágenes). Devuelve las entradas crudas ya comprobadas en su metadato. */
export function parseResourcesBackup(
  text: string,
): Validation<readonly { raw: Record<string, unknown>; sha256: string; data: string }[]> {
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
    doc['version'] !== RESOURCES_BACKUP_VERSION ||
    !Array.isArray(doc['resources']) ||
    doc['resources'].length > RESOURCE_LIMITS.maxResources
  )
    return bad;
  const out: { raw: Record<string, unknown>; sha256: string; data: string }[] = [];
  for (const item of doc['resources'] as unknown[]) {
    if (!isObject(item)) return bad;
    const { data, sha256, ...meta } = item;
    if (typeof data !== 'string' || typeof sha256 !== 'string' || !/^[0-9a-f]{64}$/.test(sha256))
      return bad;
    // El metadato se valida con un blob provisional: el real se arma al decodificar.
    if (!validateResourceRecord({ ...meta, blob: new Blob([]) }).ok) return bad;
    out.push({ raw: meta, sha256, data });
  }
  return valid(out);
}
