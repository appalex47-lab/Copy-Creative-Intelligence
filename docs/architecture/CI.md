# Integración continua — estado documental

Archivo: `.github/workflows/ci.yml`. **Está publicado en ramas de revisión, pero no se ha ejecutado nunca en GitHub y no está validado en un runner real.** Sin credenciales, sin secretos, sin Supabase, sin despliegue ni publicación de paquetes; permisos `contents: read`.

## Estado por categoría (a la fecha de esta documentación)
| # | Pregunta | Estado | Base |
|---|---|---|---|
| 1 | ¿Publicado en una rama? | **Sí**: existe en `review/cci-fase1-1-audit` (commit `afa2b72b…`) y en `review/cci-publication-cleanup`. **No** está en `main` | Contenido de las ramas remotas |
| 2 | ¿Habilitado en GitHub? | **No verificado.** La consulta de la API de workflows solo lista `pages-build-deployment`; el workflow de CI no figura (normalmente se registra al existir en la rama predeterminada o al ejecutarse). La configuración de Actions del repositorio no pudo consultarse desde el entorno de trabajo | API de workflows; el permiso de Actions devolvió 403 |
| 3 | ¿Ejecutado? | **No.** 0 ejecuciones asociadas a la rama de revisión; las 17 ejecuciones existentes son de GitHub Pages sobre `main`, anteriores a la publicación | API de ejecuciones |
| 4 | ¿Validado en un runner real? | **No.** Los mismos comandos se ejecutaron localmente en copias limpias (`npm ci`, `npm run verify`, `npm run test:e2e`), lo que **no** valida el workflow ni el runner de GitHub | Expedientes 1.0.2 y publicación de revisión |
| 5 | ¿Qué sigue pendiente? | Primera ejecución real; validar el YAML con `actionlint` o en GitHub; comprobar la vigencia de las acciones (`@v4`) y anclarlas por SHA; confirmar Chrome preinstalado en `ubuntu-latest`; decidir si se habilita | — |

## Disparadores reales del workflow
```
on:
  pull_request:
  push:
    branches: ['development/**']
  workflow_dispatch:
```
- `pull_request`: cualquier PR (no se abrió ninguno).
- `push` a ramas `development/**` (la rama local `development/cci-app-foundation` no está publicada).
- `workflow_dispatch`: ejecución manual (no se ejecutó).

**El push a `review/cci-fase1-1-audit` no activó el workflow porque ese nombre no coincide con `development/**` y el push no es un PR ni una ejecución manual.** Lo mismo aplica a `review/cci-publication-cleanup`. Abrir un PR desde cualquier rama sí ejecutaría el workflow.

## Qué hace (jobs `verify` y `e2e`)
`npm ci` (lockfile), TypeScript, ESLint, Prettier, Vitest (unitarias, componentes, arquitectura por AST, secretos, guarda de build), check de secretos, build preview, comprobación de que el build de producción **falla** y, en otro job, Playwright + axe + responsive en Chrome.

## Hallazgos de documentación (sin ampliar el alcance)
- El comentario de cabecera de `ci.yml` aún dice «PREPARADO LOCALMENTE, NO PUBLICADO NI HABILITADO». Ya no es exacto (está publicado en ramas); no se editó el archivo para no tocar el workflow.
- El expediente 1.0.2 (`05_CI_PREPARADO.md`) y expedientes posteriores describen el CI como no publicado: era cierto en su fecha y no se reescribió.
- `package.json` (`format`, `format:check`) referencia `.github`; sin ese directorio `format:check` y `verify` fallan. Es el motivo de que `ci.yml` se incluya en las ramas de revisión.
- Sin verificar: el YAML solo se validó sintácticamente; las acciones usan etiquetas mayores (`@v4`) y no se comprobó su vigencia.
