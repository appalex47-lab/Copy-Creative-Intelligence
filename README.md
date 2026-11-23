# Copy Creative Intelligence (CCI)

Aplicación web para copy y auditoría de piezas creativas. **Arquitectura: solo navegador (browser-only), un usuario por navegador.** Sin cuentas, login, backend, servidor ni sincronización. Los datos viven en IndexedDB del navegador (preferencias ligeras en Local Storage) y se respaldan con exportar/importar local.

**Estado:** Fase 1 aceptada con reservas ([acta](evidence/CCI_FASE1_S1_12_ACEPTACION_Y_CIERRES_20261123T063410Z/00_ACTA_VERIFICACION_Y_ACEPTACION_FASE1.md)); Fase 2 (Copy Studio) en curso. Hospedaje: GitHub Pages ([flujo](.github/workflows/pages.yml), manual).

## Stack

React 19 · TypeScript estricto · Vite · Vitest + Testing Library · Playwright (Chrome real) + axe · ESLint · Prettier.

## Inicio rápido

```bash
npm ci          # instalar dependencias (versiones exactas en package-lock.json)
npm run dev     # servidor local (modo DEMO)
npm run verify  # typecheck + lint + formato + pruebas + secretos + build
```

Scripts: `build` (vista previa con DEMO), `build:production` (requiere `VITE_DATA_MODE=local`; falla a propósito con DEMO), `preview`, `test:e2e` (Chrome real + axe).
Entornos y protección DEMO: [ENTORNOS_Y_MODO_DEMO](docs/architecture/ENTORNOS_Y_MODO_DEMO.md). Licencia: **todos los derechos reservados** ([LICENSE](LICENSE), [decisión](docs/decisions/LICENCIA_PENDIENTE.md)).
Guías: [instalación](docs/architecture/GUIA_INSTALACION_LOCAL.md) · [ejecución](docs/architecture/GUIA_EJECUCION.md) · [pruebas](docs/architecture/GUIA_PRUEBAS.md).

## Mapa del repositorio

| Ruta | Contenido |
| --- | --- |
| `src/` | Aplicación ([arquitectura](docs/architecture/ARQUITECTURA.md)) |
| `tests/`, `e2e/` | Pruebas unitarias, de arquitectura y de navegador real |
| `docs/decisions/` | Decisiones vigentes ([DECISIONES](docs/decisions/DECISIONES.md)) |
| `docs/fase0/` | **Histórico** de la etapa con servidor/Supabase; se conserva intacto |
| `evidence/` | Expedientes por fase (Fase 0 y Fase 1/2) con huellas SHA-256 |
| `database/`, `supabase/` | **Históricos**: diseño de servidor descartado; no se usan |
| `.github/workflows/` | `ci.yml` (verificación) y `pages.yml` (despliegue manual) |

Las menciones a Supabase, PostgreSQL, Auth o multiusuario en documentos antiguos son **históricas** y no describen la aplicación vigente.
