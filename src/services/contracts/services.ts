import type { StorageInfo } from '@/domain/storageInfo';
import type { ActivityEvent, ActivityKind } from '@/domain/activity';
import type { BriefRecord } from '@/domain/briefRecord';
import type { CopyRecord } from '@/domain/copy';
import type { RulesDoc } from '@/domain/rulesConfig';
import type { AppState } from '@/domain/entities';
import type { LocalProfile } from '@/domain/profile';
import type { AppSettings } from '@/domain/settings';
import type { Result } from './result';

// Contratos de servicios de la Fase 1. Ninguna implementación concreta se importa aquí.
// No hay inicio de sesión, identidad, organización ni roles (P1). Un fallo nunca se representa como lista vacía:
// una lista vacía legítima es un éxito con cero elementos.

export interface AppStateService {
  getState(): Promise<Result<AppState>>;
}

export interface ActivityService {
  /** Actividad local reciente, de la más nueva a la más antigua. Vacía si aún no hay actividad. */
  listRecent(): Promise<Result<readonly ActivityEvent[]>>;
  /** Registra un evento local (solo tipo y hora; nunca contenido). En DEMO no guarda nada. */
  record(kind: ActivityKind): Promise<Result<void>>;
}

export interface ProfileService {
  /** Perfil guardado o `{}` si no hay nombre. */
  get(): Promise<Result<LocalProfile>>;
  /** Un nombre vacío o ausente equivale a borrarlo. */
  save(displayName: unknown): Promise<Result<LocalProfile>>;
  clear(): Promise<Result<LocalProfile>>;
}

export interface PreferencesService {
  get(): Promise<Result<AppSettings>>;
  /** Cambio parcial validado contra la lista permitida (AC1-09). */
  update(patch: unknown): Promise<Result<AppSettings>>;
  reset(): Promise<Result<AppSettings>>;
}

/** Conjunto de servicios que consume la interfaz. */
/** Estado del almacenamiento del navegador y solicitud de almacenamiento persistente. */
export interface StorageService {
  get(): Promise<Result<StorageInfo>>;
  requestPersistence(): Promise<Result<StorageInfo>>;
}

export interface BackupSummary {
  readonly exportedAt: string;
  readonly activityCount: number;
  readonly briefCount: number;
  readonly copyCount: number;
  readonly hasRules: boolean;
  readonly hasName: boolean;
}

export interface BackupExport {
  readonly fileName: string;
  readonly text: string;
  readonly summary: BackupSummary;
}

/** Respaldo local: exportar a un archivo e importar REEMPLAZANDO todos los datos locales (con confirmación en la UI). */
export interface BackupService {
  export(): Promise<Result<BackupExport>>;
  /** Valida el archivo (formato, límites, integridad) sin cambiar nada. */
  inspect(text: string): Promise<Result<BackupSummary>>;
  /** Reemplaza todo. Si falla, los datos anteriores quedan intactos. */
  restore(text: string): Promise<Result<{ summary: BackupSummary; settings: AppSettings }>>;
}

/** Briefs de Copy Studio (S2.3). Guardar un borrador incompleto es válido; un campo inválido se rechaza. */
export interface BriefService {
  /** Más recientemente actualizados primero. Vacía si aún no hay briefs. */
  list(): Promise<Result<readonly BriefRecord[]>>;
  get(id: string): Promise<Result<BriefRecord>>;
  /** Sin `id` crea uno nuevo; con `id` actualiza conservando la fecha de creación. */
  save(input: { readonly id?: string; readonly fields: unknown }): Promise<Result<BriefRecord>>;
  remove(id: string): Promise<Result<void>>;
}

/** Copys con historial de versiones inmutables (S2.4). Guardar siempre AÑADE una versión; nunca edita una anterior. */
export interface CopyService {
  /** Más recientemente actualizados primero; con `briefId`, solo los de ese brief. */
  list(briefId?: string): Promise<Result<readonly CopyRecord[]>>;
  get(id: string): Promise<Result<CopyRecord>>;
  /** Crea un copy (o variante) del brief con su versión 1. El brief debe existir. */
  create(input: {
    readonly briefId: string;
    readonly label: unknown;
    readonly content: unknown;
    readonly tags?: unknown;
  }): Promise<Result<CopyRecord>>;
  /** Añade una versión con el contenido nuevo. Sin cambios o contenido inválido: error y no guarda. */
  saveVersion(input: {
    readonly id: string;
    readonly content: unknown;
  }): Promise<Result<CopyRecord>>;
  /** Recupera una versión antigua creando una versión NUEVA con ese contenido. */
  restoreVersion(input: {
    readonly id: string;
    readonly version: number;
  }): Promise<Result<CopyRecord>>;
  /** Cambia nombre y etiquetas (no son parte del historial de contenido). */
  updateMeta(input: {
    readonly id: string;
    readonly label: unknown;
    readonly tags: unknown;
  }): Promise<Result<CopyRecord>>;
  /** Agrega una variante (alternativa de texto sin versiones propias). No toca el historial del copy. */
  addVariant(input: {
    readonly id: string;
    readonly label: unknown;
    readonly content: unknown;
  }): Promise<Result<CopyRecord>>;
  /** Edita una variante en su lugar. Sin cambios o inválida: error y no guarda. */
  updateVariant(input: {
    readonly id: string;
    readonly variantId: string;
    readonly label: unknown;
    readonly content: unknown;
  }): Promise<Result<CopyRecord>>;
  removeVariant(input: {
    readonly id: string;
    readonly variantId: string;
  }): Promise<Result<CopyRecord>>;
  remove(id: string): Promise<Result<void>>;
}

/** Leyendas y términos de marca editables (S2.5b). Sin configuración guardada se ofrece la plantilla de ejemplo. */
export interface RulesService {
  get(): Promise<Result<{ readonly doc: RulesDoc; readonly isTemplate: boolean }>>;
  /** Reemplaza toda la configuración. Inválida: error y no guarda. */
  save(doc: unknown): Promise<Result<RulesDoc>>;
  /** Descarta lo guardado y vuelve a la plantilla de ejemplo. */
  resetToTemplate(): Promise<Result<void>>;
}

export type CoordinationState = 'checking' | 'writer' | 'reader';

/** Coordinación entre pestañas (P12): una pestaña escribe; las demás, solo lectura con aviso visible. */
export interface CoordinationService {
  getState(): CoordinationState;
  subscribe(listener: () => void): () => void;
  /** Resuelve true cuando esta pestaña puede escribir; false si no lo logra en `timeoutMs` (por defecto 1500). */
  whenWriter(timeoutMs?: number): Promise<boolean>;
}

export interface Services {
  readonly appState: AppStateService;
  readonly activity: ActivityService;
  readonly profile: ProfileService;
  readonly preferences: PreferencesService;
  readonly storage: StorageService;
  readonly backup: BackupService;
  readonly briefs: BriefService;
  readonly copies: CopyService;
  readonly rules: RulesService;
  readonly coordination: CoordinationService;
}
