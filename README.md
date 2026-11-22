# Copy Creative Intelligence (CCI)

Aplicación web para copy y auditoría de piezas creativas. **Estado: fundación técnica (Fase 1.0) en construcción.** No es producción, no está conectada a ningún backend y no tiene autenticación real.

## Stack

React 19 · TypeScript (estricto) · Vite · Vitest + React Testing Library · ESLint · Prettier. Backend futuro (NO conectado): Supabase / PostgreSQL / Auth / RLS / Edge Functions / Storage, con entornos independientes CCI-DEV y CCI-PROD.

## Inicio rápido

```bash
npm ci          # instalar dependencias (versiones exactas en package-lock.json)
npm run dev     # servidor local (modo DEMO)
npm run verify  # typecheck + lint + formato + pruebas + secretos + build
```

Scripts: `npm run build` (preview con DEMO), `build:production` (falla a propósito: no hay backend), `preview`, `test:e2e` (Chrome real + axe).
Entornos y protección DEMO: [ENTORNOS_Y_MODO_DEMO](docs/architecture/ENTORNOS_Y_MODO_DEMO.md). Licencia: **pendiente** ([nota](docs/decisions/LICENCIA_PENDIENTE.md)); sin LICENSE no hay permiso de reutilización.
Guías: [instalación](docs/architecture/GUIA_INSTALACION_LOCAL.md) · [ejecución](docs/architecture/GUIA_EJECUCION.md) · [pruebas](docs/architecture/GUIA_PRUEBAS.md).

## Mapa del repositorio

| Ruta                                                                  | Contenido                                                                         |
| --------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| `src/`                                                                | Aplicación (ver [arquitectura](docs/architecture/ARQUITECTURA.md))                |
| `tests/`                                                              | Preparación de pruebas y pruebas de arquitectura/secretos                         |
| `scripts/`                                                            | `check-secrets.mjs` (solo rutas de la app)                                        |
| `docs/architecture`, `docs/decisions`, `docs/roadmap`, `docs/product` | Documentación de la aplicación (Fase 1.0)                                         |
| `docs/fase0/`                                                         | **Documentación y expedientes de Fase 0 — se conservan intactos en su ubicación** |
| `database/`, `supabase/`                                              | Solo README: integración futura, sin SQL ni conexión                              |
| `evidence/`                                                           | Expedientes originales de la fundación de la aplicación (Fase 1.x) y documentos de publicación |
| `evidence/public/`                                                    | Copias de consulta pública derivadas (sin rutas del entorno temporal); **no son evidencia original** ([léelo](evidence/public/README.md)) |
| `.github/workflows/ci.yml`                                            | Workflow de CI versionado y publicado en ramas de revisión; **sin ejecución registrada, habilitación no determinada y no validado en un runner real** ([estado](docs/architecture/CI.md)) |

`evidence/` (aplicación) y `evidencia/` (Fase 0) coexisten en el árbol de trabajo original. **Esta rama de revisión no incluye `evidencia/`, `AUDITORIA_*` ni `ARTEFACTOS_REVISION_PUBLICACION/`**: solo `docs/fase0/` (heredado de `main`) y `evidence/`. No se renombra ni se mueve nada histórico.

**CI:** el workflow está versionado y publicado en ramas de revisión (no en `main`). No hay ejecución registrada ni validación en un runner real, y no se afirma que Actions esté habilitado o deshabilitado (la consulta de configuración devolvió 403). Un push a una rama `review/*` no coincide con su disparador `push` (solo `development/**`); `pull_request` es un disparador configurado, no una ejecución hecha, y la ejecución manual (`workflow_dispatch`) requiere, según GitHub, que el workflow esté en la rama predeterminada. La primera ejecución real sigue pendiente. Detalle en [CI](docs/architecture/CI.md).

## Estado

Fase 0 (diseño de datos y seguridad) **no está aprobada ni cerrada** por esta fundación; su validación PostgreSQL 17 sigue independiente. Ver [roadmap](docs/roadmap/ROADMAP.md).
