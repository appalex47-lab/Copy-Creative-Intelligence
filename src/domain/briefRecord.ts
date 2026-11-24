import { BRIEF_FIELD_LABELS, evaluateBrief, type BriefEvaluation, type BriefFields } from './brief';
import { CAMPAIGN_ID } from './entity';
import { invalid, valid, type Validation } from './validation';

/**
 * Brief guardado (S2.2). Un borrador INCOMPLETO se puede guardar (AC2-02: se señala, no se bloquea), pero un campo
 * con valor inválido nunca se guarda. El estado «completo/incompleto» se DERIVA al leer; no se almacena, para que
 * no pueda quedar desactualizado respecto de las reglas.
 */
export interface BriefRecord {
  readonly id: string;
  readonly createdAt: string;
  readonly updatedAt: string;
  readonly fields: Partial<BriefFields>;
  /** Referencia OPCIONAL a una campaña registrada (S2.8). Ausente = sin referencia. */
  readonly campaignId?: string;
}

export const BRIEF_ID = /^brf_[A-Za-z0-9_-]{8,64}$/;
const ISO = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,3})?Z$/;
const KEYS = ['id', 'createdAt', 'updatedAt', 'fields', 'campaignId'] as const;

const isObject = (v: unknown): v is Record<string, unknown> =>
  typeof v === 'object' && v !== null && !Array.isArray(v);
const isIso = (v: unknown): v is string =>
  typeof v === 'string' && ISO.test(v) && !Number.isNaN(Date.parse(v));

export function validateBriefRecord(raw: unknown): Validation<BriefRecord> {
  if (!isObject(raw) || !Object.keys(raw).every((k) => (KEYS as readonly string[]).includes(k)))
    return invalid('El brief guardado no es válido.');
  const { id, createdAt, updatedAt } = raw;
  if (typeof id !== 'string' || !BRIEF_ID.test(id))
    return invalid('El identificador del brief no es válido.');
  if (!isIso(createdAt) || !isIso(updatedAt))
    return invalid('Las fechas del brief no son válidas.');
  if (updatedAt < createdAt)
    return invalid('La fecha de actualización no puede ser anterior a la de creación.');
  if (!isObject(raw['fields'])) return invalid('Los campos del brief no son válidos.');
  const e = evaluateBrief(raw['fields']);
  const first = e.invalid[0];
  if (first !== undefined) return invalid(first.reason);
  // Una clave que no es uno de los 13 campos se rechaza en lugar de ignorarse en silencio.
  if (Object.keys(raw['fields']).some((k) => !(k in BRIEF_FIELD_LABELS)))
    return invalid('El brief contiene campos no permitidos.');
  const cid = raw['campaignId'];
  if (cid !== undefined && (typeof cid !== 'string' || !CAMPAIGN_ID.test(cid)))
    return invalid('La campaña referenciada no es válida.');
  return valid({
    id,
    createdAt,
    updatedAt,
    fields: e.brief as Partial<BriefFields>,
    ...(cid !== undefined ? { campaignId: cid } : {}),
  });
}

/** Evalúa un brief guardado con las reglas VIGENTES (si cambian las reglas, cambia el estado). */
export function evaluateRecord(record: BriefRecord): BriefEvaluation {
  return evaluateBrief(record.fields);
}

/** Orden canónico: actualizado más reciente primero; empate por id descendente. */
export function compareBriefsNewestFirst(a: BriefRecord, b: BriefRecord): number {
  if (a.updatedAt !== b.updatedAt) return a.updatedAt < b.updatedAt ? 1 : -1;
  return a.id < b.id ? 1 : a.id > b.id ? -1 : 0;
}
