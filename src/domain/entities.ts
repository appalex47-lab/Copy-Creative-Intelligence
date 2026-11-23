// Estado de aplicación de alto nivel. S1.3 retiró las entidades provisionales de la era Supabase
// (UserIdentity, Organization, Membership con roles y Project): contradecían P1 (perfil local opcional, sin
// identidad, organización, membresía ni roles). El dominio vigente está en profile.ts, settings.ts y activity.ts.

/** Estado de aplicación de alto nivel (no es estado de UI transitorio). */
export interface AppState {
  readonly dataMode: 'demo' | 'local';
  readonly environment: 'development' | 'test' | 'preview' | 'production';
  readonly isDemo: boolean;
}
