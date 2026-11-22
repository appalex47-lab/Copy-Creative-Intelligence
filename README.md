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
| `evidence/`                                                           | Expedientes de la fundación de la aplicación (Fase 1.x)                           |
| `evidencia/`, `AUDITORIA_*`, `ARTEFACTOS_REVISION_PUBLICACION/`       | Expedientes previos de Fase 0 (no se modifican)                                   |

`evidence/` (nuevo, app) y `evidencia/` (existente, Fase 0) coexisten; no se renombra ni se mueve nada histórico.

## Estado

Fase 0 (diseño de datos y seguridad) **no está aprobada ni cerrada** por esta fundación; su validación PostgreSQL 17 sigue independiente. Ver [roadmap](docs/roadmap/ROADMAP.md).
