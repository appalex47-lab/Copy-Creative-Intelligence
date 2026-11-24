import type { ActivityEvent } from '@/domain/activity';
import type { MeasureRecord } from '@/domain/measure';
import type { PromoRecord } from '@/domain/promo';
import type { ReviewRecord } from '@/domain/review';
import type { PieceRecord } from '@/domain/piece';
import type { ResourceRecord } from '@/domain/resource';
import type { AuditRecord } from '@/domain/audit';
import type { AdaptationRecord } from '@/domain/adaptation';
import type { EntityKind, EntityRecord } from '@/domain/entity';
import type { BriefRecord } from '@/domain/briefRecord';
import type { CopyRecord } from '@/domain/copy';
import type { LocalProfile } from '@/domain/profile';
import type { RulesDoc } from '@/domain/rulesConfig';
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

export interface BriefRepository {
  /** Guarda (crea o reemplaza por `id`) un brief validado; un borrador incompleto es válido. */
  put(record: unknown): Promise<Result<BriefRecord>>;
  /** El brief o `validation_error` si no existe o el id no es válido. */
  get(id: string): Promise<Result<BriefRecord>>;
  /** Más recientemente actualizados primero. */
  list(): Promise<Result<readonly BriefRecord[]>>;
  /** Borra un brief; borrar uno inexistente es válido (idempotente). */
  remove(id: string): Promise<Result<void>>;
  count(): Promise<Result<number>>;
}

export interface CopyRepository {
  /** Guarda (crea o reemplaza por `id`) un copy validado con su historial de versiones. */
  put(record: unknown): Promise<Result<CopyRecord>>;
  get(id: string): Promise<Result<CopyRecord>>;
  /** Más recientemente actualizados primero; con `briefId`, solo los de ese brief. */
  list(briefId?: string): Promise<Result<readonly CopyRecord[]>>;
  /** Idempotente. */
  remove(id: string): Promise<Result<void>>;
  count(): Promise<Result<number>>;
}

export interface RulesRepository {
  /** La configuración guardada o `null` si nunca se guardó (se usa entonces la plantilla de ejemplo). */
  get(): Promise<Result<RulesDoc | null>>;
  /** Reemplaza toda la configuración (validada). */
  save(doc: unknown): Promise<Result<RulesDoc>>;
  /** Vuelve al estado «sin configuración guardada». Idempotente. */
  clear(): Promise<Result<void>>;
}

export interface EntityRepository {
  /** Guarda (crea o reemplaza por `id`) un registro validado. */
  put(record: unknown): Promise<Result<EntityRecord>>;
  get(id: string): Promise<Result<EntityRecord>>;
  /** Por nombre; con `kind`, solo ese tipo. */
  list(kind?: EntityKind): Promise<Result<readonly EntityRecord[]>>;
  /** Idempotente. */
  remove(id: string): Promise<Result<void>>;
}

export interface AdaptationRepository {
  put(record: unknown): Promise<Result<AdaptationRecord>>;
  get(id: string): Promise<Result<AdaptationRecord>>;
  /** Más recientes primero; con `copyId`, solo las de ese copy. */
  list(copyId?: string): Promise<Result<readonly AdaptationRecord[]>>;
  remove(id: string): Promise<Result<void>>;
  count(): Promise<Result<number>>;
}

export interface AuditRepository {
  /** Guarda una auditoría validada (inmutable por convención: el servicio nunca reescribe una existente). */
  put(record: unknown): Promise<Result<AuditRecord>>;
  get(id: string): Promise<Result<AuditRecord>>;
  /** Más recientes primero; con `copyId`, solo las de ese copy. */
  list(copyId?: string): Promise<Result<readonly AuditRecord[]>>;
  remove(id: string): Promise<Result<void>>;
  count(): Promise<Result<number>>;
}

/** Recursos visuales (S3.3). Solo en este navegador; NO forman parte del respaldo (BackupSnapshot). */
export interface ResourceRepository {
  put(resource: unknown): Promise<Result<ResourceRecord>>;
  get(id: string): Promise<Result<ResourceRecord>>;
  /** Más recientes primero. */
  list(): Promise<Result<readonly ResourceRecord[]>>;
  remove(id: string): Promise<Result<void>>;
  count(): Promise<Result<number>>;
}

/** Piezas creativas con sus auditorías (S3.4). Como los recursos, NO forman parte del respaldo JSON de datos. */
export interface PieceRepository {
  put(piece: unknown): Promise<Result<PieceRecord>>;
  get(id: string): Promise<Result<PieceRecord>>;
  /** Más recientes primero. */
  list(): Promise<Result<readonly PieceRecord[]>>;
  remove(id: string): Promise<Result<void>>;
  count(): Promise<Result<number>>;
}

/** Revisiones de calidad (S4.1). Como piezas y recursos, NO forman parte del respaldo JSON de datos. */
export interface ReviewRepository {
  put(review: unknown): Promise<Result<ReviewRecord>>;
  get(id: string): Promise<Result<ReviewRecord>>;
  /** Más recientes primero. */
  list(): Promise<Result<readonly ReviewRecord[]>>;
  remove(id: string): Promise<Result<void>>;
  count(): Promise<Result<number>>;
}

/** Mediciones y experimentos (S4.2). No forman parte del respaldo JSON de datos (van en el archivo de recursos). */
export interface MeasureRepository {
  put(m: unknown): Promise<Result<MeasureRecord>>;
  get(id: string): Promise<Result<MeasureRecord>>;
  /** Más recientes primero. */
  list(): Promise<Result<readonly MeasureRecord[]>>;
  remove(id: string): Promise<Result<void>>;
  count(): Promise<Result<number>>;
}

/** Promociones capturadas o importadas por CSV (S4.2). Tampoco van en el respaldo JSON de datos. */
export interface PromoRepository {
  put(p: unknown): Promise<Result<PromoRecord>>;
  get(id: string): Promise<Result<PromoRecord>>;
  /** Por nombre. */
  list(): Promise<Result<readonly PromoRecord[]>>;
  remove(id: string): Promise<Result<void>>;
  count(): Promise<Result<number>>;
}

export interface BackupSnapshot {
  readonly profile: LocalProfile;
  /** Más nuevos primero. */
  readonly activity: readonly ActivityEvent[];
  /** Briefs guardados (S2.2), más recientes primero. */
  readonly briefs: readonly BriefRecord[];
  /** Copys con su historial (S2.4), más recientes primero. */
  readonly copies: readonly CopyRecord[];
  /** Leyendas y términos de marca (S2.5b); `null` si nunca se configuraron. */
  readonly rules: RulesDoc | null;
  /** Campañas, productos y ofertas (S2.8). */
  readonly entities: readonly EntityRecord[];
  /** Adaptaciones por canal (S2.8), más recientes primero. */
  readonly adaptations: readonly AdaptationRecord[];
  /** Auditorías guardadas (S3.1), más recientes primero. */
  readonly audits: readonly AuditRecord[];
}

export interface BackupRepository {
  /** Copia consistente de perfil y actividad (una sola lectura). */
  exportAll(): Promise<Result<BackupSnapshot>>;
  /**
   * Reemplaza TODO (perfil y actividad) de forma atómica: o queda todo lo nuevo o todo lo anterior (nunca un estado
   * parcial). Valida los datos antes de tocar nada.
   */
  replaceAll(snapshot: unknown): Promise<Result<void>>;
}

export interface Repositories {
  readonly activity: ActivityRepository;
  readonly profile: ProfileRepository;
  readonly briefs: BriefRepository;
  readonly copies: CopyRepository;
  readonly rules: RulesRepository;
  readonly entities: EntityRepository;
  readonly adaptations: AdaptationRepository;
  readonly audits: AuditRepository;
  readonly resources: ResourceRepository;
  readonly pieces: PieceRepository;
  readonly reviews: ReviewRepository;
  readonly measures: MeasureRepository;
  readonly promos: PromoRepository;
  readonly backup: BackupRepository;
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
