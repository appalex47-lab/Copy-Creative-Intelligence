# Estado de la integración Supabase

**No integrada.** No hay conexión a CCI-DEV ni CCI-PROD, credenciales, SQL, tablas, roles ni RLS en este repositorio de aplicación; no se usa el Supabase de RevNavigator.
Puntos de integración futuros: Auth (sesión → `IdentityService`), PostgreSQL + RLS (adaptadores de servicios), Edge Functions (operaciones sensibles, p. ej. `transition_piece_status` según Fase 0), Storage, separación DEV/PROD.
Decisiones pendientes: ver `docs/decisions/DECISIONES.md`. La validación de seguridad y PostgreSQL 17 de Fase 0 sigue independiente y no queda aprobada por esta fase.
