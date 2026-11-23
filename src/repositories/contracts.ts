import type { ActivityEvent } from '@/domain/activity';
import type { LocalProfile } from '@/domain/profile';
import type { Result } from '@/services/contracts';

// Contratos de repositorios de la Fase 1. La interfaz y los casos de uso solo ven estas interfaces; IndexedDB solo
// se toca desde `src/adapters/indexeddb/` (AC1-06, probado por AST). Un fallo nunca se representa como dato vacío.

export interface ActivityRepository {
  /** Guarda un evento validado; repetir el mismo `id` lo reemplaza (idempotente). */
  add(event: unknown): Promise<Result<ActivityEvent>>;
  /** Más nuevos primero (empate por `at`: `id` descendente). `limit` entre 1 y 500; por defecto 50. */
  listRecent(limit?: number): Promise<Result<readonly ActivityEvent[]>>;
  count(): Promise<Result<number>>;
}

export interface ProfileRepository {
  /** Perfil guardado o `{}` si no hay nombre. */
  get(): Promise<Result<LocalProfile>>;
  /** Un nombre vacío o ausente equivale a borrarlo. */
  save(displayName: unknown): Promise<Result<LocalProfile>>;
  clear(): Promise<Result<LocalProfile>>;
}

export interface Repositories {
  readonly activity: ActivityRepository;
  readonly profile: ProfileRepository;
}

export const DEFAULT_LIST_LIMIT = 50;
export const MAX_LIST_LIMIT = 500;

/** Normaliza `limit`: entero entre 1 y 500; cualquier otro valor es inválido. */
export function normalizeLimit(limit: unknown): number | null {
  if (limit === undefined) return DEFAULT_LIST_LIMIT;
  return typeof limit === 'number' &&
    Number.isInteger(limit) &&
    limit >= 1 &&
    limit <= MAX_LIST_LIMIT
    ? limit
    : null;
}

/** Orden canónico: `at` descendente y, en empate, `id` descendente (igual que el índice de IndexedDB recorrido hacia atrás). */
export function compareNewestFirst(a: ActivityEvent, b: ActivityEvent): number {
  if (a.at !== b.at) return a.at < b.at ? 1 : -1;
  return a.id < b.id ? 1 : a.id > b.id ? -1 : 0;
}
