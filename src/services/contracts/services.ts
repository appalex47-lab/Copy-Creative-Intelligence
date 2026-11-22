import type { AppState, Membership, Organization, Project, UserIdentity } from '@/domain/entities';
import type { Result } from './result';

// Contratos de servicios PROVISIONALES. Ninguna implementación concreta (ni Supabase) se importa aquí.
// Fase 1.0 no define inicio de sesión: la identidad se "consulta", no se "autentica".
//
// SEMÁNTICA UNIFORME de consultas por recurso padre (aplica a todo adaptador, DEMO o futuro):
//  - parámetro ausente o inválido (no es texto o está vacío)  -> error `validation_error`
//  - el recurso padre NO existe                                -> error `not_found`
//  - el recurso padre existe pero no tiene elementos           -> lista vacía (éxito)
// Un fallo nunca se representa como lista vacía. No define reglas de negocio ni permisos definitivos.

export interface IdentityService {
  getCurrentIdentity(): Promise<Result<UserIdentity>>;
}

export interface OrganizationService {
  listForCurrentUser(): Promise<Result<readonly Organization[]>>;
}

export interface MembershipService {
  listForOrganization(organizationId: string): Promise<Result<readonly Membership[]>>;
}

export interface ProjectService {
  listForOrganization(organizationId: string): Promise<Result<readonly Project[]>>;
}

export interface AppStateService {
  getState(): Promise<Result<AppState>>;
}

/** Conjunto de servicios que consume la interfaz. Se intercambia por modo (demo | backend futuro). */
export interface Services {
  readonly identity: IdentityService;
  readonly organizations: OrganizationService;
  readonly memberships: MembershipService;
  readonly projects: ProjectService;
  readonly appState: AppStateService;
}
