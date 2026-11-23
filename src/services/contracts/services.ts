import type { ActivityEvent } from '@/domain/activity';
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
export interface Services {
  readonly appState: AppStateService;
  readonly activity: ActivityService;
  readonly profile: ProfileService;
  readonly preferences: PreferencesService;
}
