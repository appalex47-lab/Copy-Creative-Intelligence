/** Estado del almacenamiento del navegador. `null` = el navegador no lo expone (se muestra «No disponible»). */
export interface StorageInfo {
  readonly usageBytes: number | null;
  readonly quotaBytes: number | null;
  readonly persisted: boolean | null;
}

export const UNKNOWN_STORAGE: StorageInfo = { usageBytes: null, quotaBytes: null, persisted: null };

const validBytes = (v: unknown): number | null =>
  typeof v === 'number' && Number.isFinite(v) && v >= 0 ? v : null;

/** Normaliza lo que devuelve el navegador (dato no confiable): cualquier valor raro pasa a `null`. */
export function parseStorageInfo(usage: unknown, quota: unknown, persisted: unknown): StorageInfo {
  return {
    usageBytes: validBytes(usage),
    quotaBytes: validBytes(quota),
    persisted: typeof persisted === 'boolean' ? persisted : null,
  };
}

/** Formatea bytes con unidades binarias legibles; `null` → «No disponible». */
export function formatBytes(bytes: number | null): string {
  if (bytes === null) return 'No disponible';
  const units = ['B', 'KB', 'MB', 'GB', 'TB'];
  let value = bytes;
  let i = 0;
  while (value >= 1024 && i < units.length - 1) {
    value /= 1024;
    i++;
  }
  const text = i === 0 ? String(Math.round(value)) : value.toFixed(value >= 10 ? 0 : 1);
  return `${text} ${units[i]}`;
}
