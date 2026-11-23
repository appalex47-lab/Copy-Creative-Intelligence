import type { StorageInfo } from '@/domain/storageInfo';
import type { ActivityEvent, ActivityKind } from '@/domain/activity';
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
  readonly coordination: CoordinationService;
}
