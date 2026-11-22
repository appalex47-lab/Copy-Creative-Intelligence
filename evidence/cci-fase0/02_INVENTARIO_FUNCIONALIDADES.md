# Inventario de funcionalidades (CCI, commit auditado `ffb47bc319db0806250bcecf91d390fa59fa0d70`)
Niveles: **E** = código existente · **X** = ejecutable (compila y corre) · **C** = comprobada (prueba ejecutada y aprobada, con evidencia). «C» se basa en las ejecuciones propias de esta fase sobre una copia temporal del commit (ver `13_VERIFICACION_EJECUTADA.md`): typecheck, lint, formato, secretos, `vitest` 13 archivos / 162 pruebas aprobadas, build preview, `build:production` falla como se espera, Playwright 29/29 en 3 corridas consecutivas. Que una prueba exista no la hace comprobada; que una declaración documental exista no demuestra implementación.

## A. Funcionalidades reales (existen y están comprobadas)
| # | Funcionalidad | E | X | C | Evidencia |
|---|---|---|---|---|---|
| A1 | Aplicación React 19 + TS estricto + Vite que arranca y se compila (modo preview) | sí | sí | sí | `package.json`; build exit 0; E2E «arranca…» |
| A2 | Política de entorno única (build y ejecución); rechaza configuraciones contradictorias | sí | sí | sí | `src/app/envPolicy.ts`; `env.test.ts` (8); `buildGuard.test.ts` (6) |
| A3 | `build:production` falla a propósito mientras no haya persistencia/backend | sí | sí | sí | `build_production_esperado_FALLO.log` |
| A4 | Capas con inyección `useServices()` y reglas de arquitectura por AST | sí | sí | sí | `tests/architecture.test.ts`, `moduleReferences.test.ts` |
| A5 | `Result<T>`, 5 `AppErrorCode`, mensajes por código | sí | sí | sí | `errorMessages.test.ts`, `pages.errors.test.tsx` |
| A6 | `useAsyncResource` (carga/éxito/error, descarte de respuestas tardías, reintento) | sí | sí | sí | `useAsyncResource.test.tsx`; E2E de resiliencia |
| A7 | `ErrorBoundary` raíz y por página | sí | sí | sí | `ErrorBoundary.test.tsx`; E2E «Error Boundary» |
| A8 | Accesibilidad: salto, foco visible ≥3 px, teclado, axe sin violaciones | sí | sí | sí | `App.a11y.test.tsx`; E2E axe (2) |
| A9 | Responsive en 6 anchos × 2 pantallas + estado de error sin desbordes | sí | sí | sí | `e2e/responsive.spec.ts` (13 casos) |
| A10 | Escáner de secretos heurístico | sí | sí | sí | `scripts/check-secrets.mjs`; `tests/secrets.test.ts` (13) |
| A11 | CI (workflow) | sí | **no determinado** | **no** | `ci.yml` jamás ejecutado en un runner real |

## B. Funcionalidades parciales
| # | Funcionalidad | Qué existe | Qué falta |
|---|---|---|---|
| B1 | Navegación | 2 vistas (Inicio, Estado de conexión) por estado, sin rutas | rutas/URL, 9 módulos |
| B2 | Modelo de dominio | `UserIdentity`, `Organization`, `Membership`, `AppState` (provisionales, multiusuario) | dominio de producto (§06) |
| B3 | Contratos de servicio | 4 servicios de **lectura** | casos de uso, escritura, repositorios |
| B4 | Manejo de errores | `Result` + mensajes | ampliación para persistencia (cuota, aborto, versión) |
| B5 | Pruebas | unitarias, arquitectura, E2E de la fundación | dominio, persistencia, migraciones, export/import |

## C. Prototipos (existen pero no son producto)
| # | Elemento | Observación |
|---|---|---|
| C1 | Adaptador DEMO (1 identidad, 1 organización, 1 membresía ficticias, en memoria, solo lectura) | Sirve para probar capas; **no debe mostrarse como información operativa** (principio del propietario) |
| C2 | Pantalla «Resumen» (HomePage) y «Estado de conexión» | Muestran datos DEMO y avisos; no son Command Center |
| C3 | Aviso DEMO | Válido solo mientras existan datos ficticios |

## D. Funcionalidades inexistentes (sin código)
Persistencia (IndexedDB, Local Storage, migraciones, repositorios, preferencias) · Command Center con datos reales · Copy Studio (brief, generación, editor, reglas) · Creative Auditor · Promotion Validator · Channel Adaptation · Creative Library · Workflow & Approvals · Performance Intelligence · Brand Intelligence/Settings · exportación/importación/respaldo/restauración · cualquier integración de IA · casos de uso (capa de aplicación) · rutas · estado real del almacenamiento · manual de usuario y manual técnico.
Evidencia: 0 usos de `indexedDB`, `localStorage`, `fetch`, `XMLHttpRequest`, `WebSocket` en `src/`; `src/features/` y `src/types/` solo contienen `.gitkeep`; `docs/product/README.md` declara «sin funcionalidades de producto».

## E. Qué trabajo aceptado puede conservarse
Conservable sin cambio de intención: A1–A10 (infraestructura, calidad, accesibilidad, política de entorno **tras redefinir «producción»**, arquitectura por AST **ampliada**). Conservable con adaptación: contratos/`Result`/`useServices`; `entities.ts` (reemplazo del dominio, ver §06); `createServices` (nuevo modo local). Conservable como antecedente: expedientes `evidence/` y `docs/fase0/`.
