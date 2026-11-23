# 01 — Auditoría técnica del estado real del repositorio (S1.0)
> Resultados **propuestos**; ningún hallazgo ni clasificación está aprobado. Hechos = lo observado en el commit base; interpretación = marcada [INTERPRETACIÓN].

## 1. Base auditada
- Commit `7bcba74e05577761081d68ca14fdc19f2400248d`. Es descendiente de `afa2b72` (rama `review/cci-fase1-1-audit`, «estado reproducible de la aplicación Fase 1.0–1.1-A1»): cuatro commits solo documentales; `git diff --stat` de `src`, `tests`, `e2e` y `package.json` entre ambos: vacío. **El código es el de «Fase 1.0–1.1-A1»**, una numeración anterior e independiente de la Fase 1 del expediente actual (riesgo de confusión de nombres; ver S1-D16).
- `main` solo contiene `README.md` y `docs/`; el código vive en ramas `review/*`.

## 2. Inventario
- `src/`: 34 archivos (2 `.gitkeep`) en `app`, `components`, `domain`, `hooks`, `layouts`, `lib`, `pages`, `services/{contracts,adapters/demo}`, `styles`. Capas observadas: presentación (pages/components/layouts), hooks, dominio provisional, contratos de servicios, adaptador DEMO. **No existen** capa de aplicación (casos de uso) ni repositorios ni adaptadores IndexedDB/preferencias.
- Pruebas: 13 archivos de Vitest (130 pruebas) y 3 especificaciones Playwright (29 pruebas, Chrome real).
- Dependencias de ejecución: solo `react` y `react-dom` (19.3.1). Sin enrutador, sin librería de IndexedDB, sin validación de esquemas. Herramientas: TypeScript 6.0.3 (`strict`, `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`), ESLint con `--max-warnings 0`, Prettier, Vitest 5.1.1, Playwright 1.65.1 y `@axe-core/playwright`.
- `package.json` declara `engines.node >= 22.22.2`. `supabase/` y `database/` contienen solo un README («reservado»).

## 3. Resultados de las pruebas existentes (sin modificarlas)
| Comando | Resultado | Registro |
|---|---|---|
| `npm ci` | éxito, 232 paquetes | `logs/npm_ci.txt` |
| `npm run typecheck` | rc 0 | `logs/typecheck.txt` |
| `npm run lint` | rc 0 | `logs/lint.txt` |
| `npm run format:check` | rc 0 | `logs/format_check.txt` |
| `npm run test:run` | 13 archivos, **130 pruebas, todas pasan** | `logs/test_run.txt` |
| `npm run check:secrets` | rc 0 | `logs/check_secrets.txt` |
| `npm run build` (modo preview) | rc 0 | `logs/build.txt` |
| `npm run build:production` | **rc 1, rechazado por diseño:** «Un entorno de producción no puede usar datos DEMO y aún no existe un backend real» | `logs/build_production.txt` |
| `npm run test:e2e` (6 corridas) | 4 corridas 29/29; **2 corridas con 1 fallo** (runs 3 y 5) | `logs/e2e_run1.txt` … `e2e_run6.txt` |
- Playwright no pudo descargar su navegador (`cdn.playwright.dev`, HTTP 403 por la lista de permitidos del entorno: `logs/pw_install.txt`); se usó el Chrome del sistema (Chrome for Testing 153.0.8010.12) que la configuración selecciona por `channel: 'chrome'`.
- El repositorio quedó sin cambios rastreados tras todas las ejecuciones (`git status` limpio; los artefactos están en rutas ignoradas).

## 4. Hallazgos
| Id | Hallazgo (hecho) | Relación con el expediente | Referencia |
|---|---|---|---|
| F-01 | El dominio provisional es de la era Supabase: `UserIdentity`, `Organization`, `Membership` con `MembershipRole` (`admin`, `ecommerce`, `design`, `marketing`, `reviewer`) y `Project`; el contrato `Services` y `HomePage` los consumen | P1 resuelta: perfil local opcional **sin** identidad, organización, membresías ni roles; ninguna de esas entidades está entre las 18 aprobadas | `src/domain/entities.ts`, `src/services/contracts/services.ts`, `src/pages/HomePage.tsx` |
| F-02 | `AppErrorCode` tiene 5 códigos genéricos (`not_found`, `not_implemented`, `unavailable`, `invalid_configuration`, `validation_error`); no existen los códigos de persistencia | AC1-08 exige códigos de persistencia con mensaje, prueba y UI; la autorización de S1.1/S1.2 excluye ampliar el catálogo | `src/services/contracts/result.ts` |
| F-03 | Solo existe el modo de datos `demo`; la política rechaza `production` con DEMO y rechaza `supabase` («no implementado»). **No hay un modo operativo local** | P9: modo operativo local; AC1-11 exige un build de producción sin datos DEMO. Hoy no es posible generar un build de producción | `src/app/envPolicy.ts`, `vite.config.ts`, `logs/build_production.txt` |
| F-04 | No hay IndexedDB, Local Storage, repositorios, migraciones ni pantalla de almacenamiento (búsqueda sin coincidencias de `indexedDB`, `localStorage`, `sessionStorage`, `navigator.storage` en `src`, `tests`, `e2e`) | AC1-06, 07, 08, 09, 10, 12 sin iniciar (esperado) | `src/` |
| F-05 | Ninguna prueba impone la ausencia de `fetch`/XHR/WebSocket/EventSource: la prueba de arquitectura por AST solo comprueba el aislamiento de Supabase y reglas de importación (búsqueda sin coincidencias en `tests/`). `src` tampoco usa esas APIs hoy | AC1-01 exige esa prueba sobre `src/` | `tests/architecture.test.ts`, `tests/support/moduleReferences.ts` |
| F-06 | Navegación por estado (`useState`), 2 vistas: «Inicio» (resumen de identidad/organizaciones/proyectos) y «Estado de conexión»; sin enrutador | AC1-03 (navegación y foco): existe enlace de salto, foco al encabezado al cambiar de vista y pruebas E2E; las vistas del expediente (Command Center, almacenamiento, preferencias/perfil) no existen | `src/app/App.tsx`, `src/layouts/AppLayout.tsx` |
| F-07 | El título del documento añade siempre «(DEMO)» y el encabezado dice «Fundación técnica en construcción — identidad visual provisional» | Con un modo local operativo (P9), «DEMO» fijo contradice AC1-11 | `src/layouts/AppLayout.tsx` |
| F-08 | Componentes reutilizables: `NavMenu`, `StatusNotices` (`AsyncStatus`, `ErrorNotice`), `ErrorBoundary`, `DemoBanner`; no hay botones, campos, tarjetas, tablas ni indicadores como componentes propios | AC1-04 (componentes reutilizables con pruebas, sin violaciones axe): parcial | `src/components/` |
| F-09 | Prueba E2E **intermitente**: «foco visible: contorno de al menos 3px…» (`e2e/app.spec.ts:70`) falló en 2 de 6 corridas con `outlineStyle === 'none'` tras dos pulsaciones de Tab | Regla de cierre: 3 corridas E2E consecutivas | `logs/e2e_run3.txt`, `e2e_run5.txt` |
| F-10 | Documentación del repositorio base afirma que PostgreSQL/Supabase será la fuente de verdad y IndexedDB/localStorage solo caché futura; hay referencias a Supabase/Auth/RLS en `envPolicy.ts`, `.env.example`, `ci.yml`, `scripts/check-secrets.mjs`, pruebas y `docs/architecture/` | P2 y P3: arquitectura browser-only; los antecedentes Supabase son históricos | `docs/architecture/ARQUITECTURA.md`, archivos citados |
| F-11 | CI declarado como no demostrado: el propio `ci.yml` indica que no hay evidencia de ejecución real en GitHub ni de validación en un runner | La evidencia de la Fase 1 exigirá ejecuciones reproducibles | `.github/workflows/ci.yml` |
| F-12 | Solo se probó en Chrome for Testing 153; ninguna prueba corre en Edge, Firefox ni Safari/WebKit | P11 (por niveles) exige validar Edge y cubrir Firefox/Safari en mejor esfuerzo | `playwright.config.ts` |

## 5. Interpretaciones (no hechos)
- [INTERPRETACIÓN] F-09: la prueba pulsa Tab sin esperar a que React haya montado la interfaz; no se verificó esa causa. No se modificó la prueba.
- [INTERPRETACIÓN] F-01 y F-06 implican que el contenido actual de las dos vistas existentes (identidad/organizaciones/proyectos) no puede sobrevivir a la Fase 1 del expediente; cuándo reemplazarlo es decisión del propietario (S1-D01), porque la autorización de S1.1/S1.2 excluye dominio y datos del Command Center.

## 6. Lo que esta auditoría NO verificó
Web Locks (P12), cuotas de IndexedDB, compatibilidad en otros navegadores, ejecución de CI, `docs/fase0/` (histórico), los directorios `evidence/` anteriores, el comportamiento en producción real (no existe), ni la corrección del código más allá de las pruebas existentes.
