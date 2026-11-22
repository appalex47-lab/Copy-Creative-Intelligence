# Arquitectura técnica (Fase 1.0 — fundación)

| Carpeta                                   | Responsabilidad                                                                                                 | Puede importar             |
| ----------------------------------------- | --------------------------------------------------------------------------------------------------------------- | -------------------------- |
| `src/domain/`                             | Entidades **provisionales** (User, Organization, Membership, Project, AppState); no son las 41 tablas de Fase 0 | nada                       |
| `src/services/contracts/`                 | Interfaces de servicios (`Services`) y `Result<T>`, independientes del proveedor                                | `domain`                   |
| `src/services/adapters/demo/`             | Adaptador DEMO: datos ficticios en memoria, solo lectura                                                        | contratos, `domain`        |
| `src/services/index.ts`                   | `createServices(env)`: elige adaptador por `VITE_DATA_MODE`                                                     | contratos, adaptadores     |
| `src/app/`                                | Raíz de composición: entorno, servicios, `App`                                                                  | todo                       |
| `src/hooks/`                              | `ServicesProvider` / `useServices()`                                                                            | contratos                  |
| `src/components/`, `layouts/`, `pages/`   | UI; solo consumen contratos vía `useServices()`                                                                 | contratos, `domain`, hooks |
| `src/features/`, `src/lib/`, `src/types/` | Reservadas (`.gitkeep`); se llenan cuando un módulo lo justifique                                               | —                          |

## Desacoplamiento

La UI nunca importa un proveedor. Un futuro adaptador `src/services/adapters/supabase/` cumplirá los mismos contratos y será la única ubicación permitida para `@supabase/*`. Controles: (1) ESLint `no-restricted-imports` y `no-restricted-syntax` (imports dinámicos) con excepción solo para `src/services/adapters/supabase/**`; (2) pruebas de arquitectura basadas en el **AST de TypeScript** (`tests/support/moduleReferences.ts`) que detectan `import … from`, imports de efecto lateral, `export … from`, `import()` (literal, concatenado o con plantilla), `require`, `import type` y literales `@supabase/*`; la interfaz tampoco puede importar adaptadores, la fábrica ni `src/app`, ni usar `import()` no resoluble estáticamente.

## Manejo de errores

Toda carga asíncrona de la UI pasa por `useAsyncResource`: estados `loading | success | error`, captura de `Result` fallidos y de excepciones, descarte de respuestas tardías y reintento (solo cuando el fallo puede ser transitorio). Los mensajes se derivan del código de error; el detalle interno nunca se muestra. `ErrorBoundary` (raíz en `main.tsx` y por página en `App`) cubre errores inesperados de renderizado. `createServices` falla de forma explícita ante un modo no soportado.

## Fuente de verdad

PostgreSQL/Supabase será la fuente central; IndexedDB/localStorage solo como caché futura. Hoy no hay persistencia.

## Seguridad por diseño

Sin claves en el cliente (`VITE_*` es público); `.env*` ignorados salvo `.env.example`; los roles del cliente son informativos, la autoridad será el backend (RLS, funciones, Edge Functions). No hay autenticación ni aislamiento por organización simulados.

## Contratos provisionales

Todos los de `src/domain` y `src/services/contracts` son **provisionales** y deben validarse contra el diseño de datos definitivo de Fase 0 (aún no aprobado) antes de usarse como base de un adaptador real. No contienen reglas de negocio definitivas.
