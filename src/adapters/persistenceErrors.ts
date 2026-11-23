import type { StorageErrorCode } from '@/services/contracts';

/** Nombre de la excepción del navegador, sin conservar su texto (puede contener detalles internos). */
const nameOf = (e: unknown): string =>
  typeof e === 'object' && e !== null && 'name' in e && typeof e.name === 'string' ? e.name : '';

/**
 * Clasifica un fallo de IndexedDB o Local Storage en un código del catálogo (AC1-08).
 * Solo se usa el NOMBRE de la excepción; el texto interno nunca llega a la interfaz.
 */
export function classifyStorageError(error: unknown): StorageErrorCode {
  switch (nameOf(error)) {
    case 'QuotaExceededError':
      return 'storage_quota_exceeded';
    case 'VersionError':
      return 'storage_newer_schema';
    case 'SecurityError':
    case 'InvalidStateError':
    case 'NotSupportedError':
      return 'storage_unavailable';
    default:
      return 'storage_failed';
  }
}
