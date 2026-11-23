# 02 — Mapa de reutilización (S1.0)
> **Clasificación PROPUESTA, no aprobada.** Categorías: **Reutilizable** (sirve como está para la Fase 1 del expediente), **Adaptar** (sirve con cambios), **Decisión** (depende de una decisión del propietario; no se toca sin ella). La marca «S1.1/S1.2» indica si el cambio caería dentro de lo que el propietario autorizaría al activar esas subfases (código fuente, pruebas y configuración; sin dominio, persistencia ni datos del Command Center).

| Elemento | Ubicación | Clasificación | Observación | Alcance S1.1/S1.2 |
|---|---|---|---|---|
| `Result<T>`, `ok`, `fail` | `src/services/contracts/result.ts` | Reutilizable | Resultado explícito sin excepciones como flujo normal | sí |
| `AppErrorCode` (5 códigos) | `result.ts` | Decisión | Ampliar con códigos de persistencia queda fuera de la autorización (AC1-08) | no |
| `ErrorBoundary` (+ prueba) | `src/components/ErrorBoundary.tsx` | Reutilizable | Captura errores de render | sí |
| `useAsyncResource` (+ prueba) | `src/hooks/useAsyncResource.ts` | Reutilizable | Estados de carga/éxito/error con reintento | sí |
| `ServicesProvider`/`useServices` | `src/hooks/ServicesContext.tsx` | Adaptar | El tipo `Services` cambiará cuando cambie el dominio | parcial |
| `StatusNotices` | `src/components/StatusNotices.tsx` | Reutilizable | Estados de carga y error accesibles | sí |
| `NavMenu` | `src/components/NavMenu.tsx` | Adaptar | Navegación por estado; el catálogo de vistas depende de S1-D07 | sí |
| `AppLayout` (enlace de salto, foco al cambiar de vista) | `src/layouts/AppLayout.tsx` | Adaptar | Título fijo «(DEMO)» (F-07); `isDemo` depende de S1-D03 | sí |
| `DemoBanner` | `src/components/DemoBanner.tsx` | Decisión | Depende de si DEMO se conserva (S1-D03) | parcial |
| Estilos y tokens | `src/styles/` | Reutilizable | «Identidad visual provisional» | sí |
| Prueba de arquitectura por AST | `tests/architecture.test.ts`, `tests/support/moduleReferences.ts` | Adaptar | Extender a `fetch`/XHR/WebSocket (AC1-01); hoy aísla Supabase | sí |
| `buildGuard`, `secrets` (pruebas y script) | `tests/`, `scripts/check-secrets.mjs` | Adaptar | Contienen referencias a Supabase (F-10) | sí |
| Arnés E2E, `axeViolations`, pruebas responsive y de resiliencia | `e2e/` | Reutilizable | Base para AC1-03, 04 y 13; anchos concretos por decidir (S1-D14) | sí |
| `entities.ts` (`UserIdentity`, `Organization`, `Membership`, `Project`, `AppState`) | `src/domain/entities.ts` | Decisión | Contradice P1; reemplazo = dominio (S1.3, no autorizada) | no |
| Contratos de servicios (identidad, organizaciones, membresías, proyectos, estado) | `src/services/contracts/services.ts` | Decisión | Mismo motivo | no |
| Adaptador DEMO y fixtures | `src/services/adapters/demo/` | Decisión | Depende de S1-D01/S1-D03 | no |
| `HomePage`, `ConnectionPage` | `src/pages/` | Decisión | Muestran datos del dominio provisional | no |
| Política de entorno y guardia de Vite | `src/app/envPolicy.ts`, `vite.config.ts` | Decisión | Sin modo local; rechaza `production` (F-03) | parcial |
| `supabase/`, `database/`, `docs/architecture/*` | raíz y `docs/` | Decisión | Alcance de la limpieza: S1-D04 | no |
| Estructura de capas | `src/` | Adaptar | Faltan aplicación y repositorios; crear la capa de aplicación es S1.1 | sí |
