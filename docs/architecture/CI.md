# Integración continua — estado documental

Archivo: `.github/workflows/ci.yml`. Sin credenciales, sin secretos, sin Supabase, sin despliegue ni publicación de la aplicación; permisos `contents: read`.

**Resumen:** el workflow está versionado y publicado en ramas de revisión. **No hay evidencia de que se haya ejecutado nunca ni de que funcione en GitHub.** Tampoco puede afirmarse que Actions esté habilitado o deshabilitado en el repositorio. La primera ejecución real sigue pendiente.

## Definiciones usadas en este documento
| Estado | Significado |
|---|---|
| Versionado | El archivo existe en Git |
| Publicado | Está presente en una rama remota |
| Habilitado | GitHub permite su ejecución en el contexto correspondiente |
| Ejecutado | Existe una ejecución registrada |
| Validado | Una ejecución real completó satisfactoriamente los controles |

## Estado actual (a la fecha de esta documentación)
| Estado | Resultado | Base |
|---|---|---|
| Versionado | **Sí** | Está en los commits de las ramas de revisión |
| Publicado | **Sí**, en ramas de revisión (`review/cci-fase1-1-audit`, `review/cci-publication-cleanup` y la rama de corrección final). **No** está en `main` | Contenido de las ramas remotas |
| Habilitado | **No determinado.** No se afirma ni que esté habilitado ni que esté deshabilitado | La API de configuración de Actions devolvió 403 desde el entorno de trabajo; la lista de workflows solo mostró `pages-build-deployment`, lo cual no demuestra por sí solo que Actions esté deshabilitado |
| Ejecutado | **Sin ejecución registrada.** 0 ejecuciones asociadas a las ramas de revisión; las 17 ejecuciones visibles son de GitHub Pages sobre `main`, anteriores a la publicación | API de ejecuciones (lectura) |
| Validado | **No** | Los mismos comandos se ejecutaron localmente en copias limpias (`npm ci`, `npm run verify`, `npm run test:e2e`). Eso **no** valida el workflow ni el runner de GitHub |

## Disparadores actuales
```
on:
  pull_request:
  push:
    branches: ['development/**']
  workflow_dispatch:
```
1. **Un push a una rama `review/*` no coincide** con el disparador `push`, que solo admite `development/**`. Por eso la publicación de las ramas de revisión no activó el workflow.
2. **`workflow_dispatch`** (ejecución manual): según la documentación de GitHub, el workflow debe estar presente en la rama predeterminada para que GitHub habilite la ejecución manual desde la interfaz. Hoy no está en `main`; no se comprobó este comportamiento en este repositorio.
3. **`pull_request`** es un disparador configurado, **no** equivale a una ejecución realizada. No se abrió ningún PR para probarlo. Que una ejecución ocurra al abrir un PR depende además de que Actions esté habilitado, algo no determinado.
4. No hay evidencia de ejecución real de este workflow.
5. No hay validación en un runner real.
6. La API de GitHub Actions devolvió 403 en la revisión anterior; por tanto **no se afirma** que Actions esté habilitado ni deshabilitado.
7. La primera ejecución real sigue pendiente.

No se afirma que el workflow funcione en GitHub hasta que exista evidencia de una ejecución real. Los disparadores no se modificaron para resolver esta situación.

## Qué haría (jobs `verify` y `e2e`)
`npm ci` (lockfile), TypeScript, ESLint, Prettier, Vitest (unitarias, componentes, arquitectura por AST, secretos, guarda de build), check de secretos, build preview, comprobación de que el build de producción **falla** y, en otro job, Playwright + axe + responsive en Chrome.

## Pendientes para una primera ejecución real
- Decidir quién y cómo habilita o ejecuta el workflow (esta documentación no lo hace).
- Comprobar la configuración de Actions del repositorio (hoy no consultable desde el entorno de trabajo).
- Validar el YAML con `actionlint` o en GitHub (hasta ahora solo se validó la sintaxis).
- Comprobar la vigencia de las acciones `@v4` y valorar anclarlas por SHA.
- Confirmar que el runner `ubuntu-latest` tiene Chrome preinstalado (se asume).
- Registrar el resultado como evidencia; solo entonces podrá hablarse de «validado».

## Notas de documentación
- El encabezado de `ci.yml` se corrigió en esta rama (solo comentarios; sin cambios en disparadores, jobs, pasos, permisos, versiones ni comandos). Antes decía «PREPARADO LOCALMENTE, NO PUBLICADO NI HABILITADO», lo que ya no era exacto.
- El expediente 1.0.2 (`05_CI_PREPARADO.md`) y otros expedientes describen el CI como no publicado: era cierto en su fecha y no se reescribieron.
- `package.json` (`format`, `format:check`) referencia `.github`; sin ese directorio `format:check` y `verify` fallan. Es el motivo de que `ci.yml` se incluya en las ramas de revisión.
