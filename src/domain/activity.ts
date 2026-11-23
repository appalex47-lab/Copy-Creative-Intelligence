import { invalid, valid, type Validation } from './validation';

/**
 * Evento de actividad (entidad aprobada; estructura y eventos SIN especificar en los documentos).
 * SUPUESTO de Claude (S1-D08, reversible): el evento guarda solo un tipo cerrado y una marca de tiempo, nunca
 * contenido del usuario (ni siquiera el nombre visible).
 */
export const ACTIVITY_KINDS = [
  'app_opened',
  'profile_changed',
  'setting_changed',
  'backup_exported',
  'backup_imported',
  'storage_error',
] as const;
export type ActivityKind = (typeof ACTIVITY_KINDS)[number];

export interface ActivityEvent {
  readonly id: string;
  /** ISO 8601 UTC. */
  readonly at: string;
  readonly kind: ActivityKind;
}

const ID = /^[A-Za-z0-9_-]{8,64}$/;

export function validateActivityEvent(raw: unknown): Validation<ActivityEvent> {
  if (typeof raw !== 'object' || raw === null) return invalid('El evento debe ser un objeto.');
  const r = raw as Record<string, unknown>;
  const { id, at, kind } = r;
  if (typeof id !== 'string' || !ID.test(id)) return invalid('Identificador de evento inválido.');
  if (
    typeof at !== 'string' ||
    !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,3})?Z$/.test(at) ||
    Number.isNaN(Date.parse(at))
  )
    return invalid('Marca de tiempo inválida.');
  const k = ACTIVITY_KINDS.find((x) => x === kind);
  if (k === undefined) return invalid('Tipo de evento no permitido.');
  const extra = Object.keys(r).filter((x) => x !== 'id' && x !== 'at' && x !== 'kind');
  if (extra.length > 0) return invalid('El evento no admite campos adicionales.');
  return valid({ id, at, kind: k });
}
