// Entidades PROVISIONALES de Fase 1.0.
// NO son el modelo de datos definitivo: las 41 tablas de Fase 0 son un diseño documental sin validar.
// Estas formas existen solo para desacoplar la UI; se revisarán en Fase 1.x junto con el esquema físico.

/** Marca de procedencia: permite que la UI distinga datos de demostración de datos reales. */
export type DataOrigin = 'demo' | 'backend';

export interface UserIdentity {
  readonly id: string;
  readonly displayName: string;
  readonly origin: DataOrigin;
}

export interface Organization {
  readonly id: string;
  readonly name: string;
  readonly origin: DataOrigin;
}

/**
 * Roles de negocio decididos por el propietario (Fase 0). PROVISIONAL.
 * IMPORTANTE: un rol que llega al navegador es solo informativo para la interfaz; nunca es una autorización.
 * La autorización real será del backend (RLS / funciones).
 */
export type MembershipRole = 'admin' | 'ecommerce' | 'design' | 'marketing' | 'reviewer';

export interface Membership {
  readonly userId: string;
  readonly organizationId: string;
  readonly roles: readonly MembershipRole[];
  readonly active: boolean;
  readonly origin: DataOrigin;
}

export interface Project {
  readonly id: string;
  readonly organizationId: string;
  readonly name: string;
  readonly origin: DataOrigin;
}

/** Estado de aplicación de alto nivel (no es estado de UI transitorio). */
export interface AppState {
  readonly dataMode: 'demo' | 'backend';
  readonly environment: 'development' | 'test' | 'preview' | 'production';
  readonly isDemo: boolean;
}
