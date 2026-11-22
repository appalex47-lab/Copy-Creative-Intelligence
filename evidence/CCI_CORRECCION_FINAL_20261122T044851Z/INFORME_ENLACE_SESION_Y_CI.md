# Corrección documental final: enlace de sesión y estado del CI

Rama: `review/cci-publication-cleanup-final`, creada desde `review/cci-publication-cleanup` (commit `60a027931910fb155a8badb61fa61013786e0cdd`, padre `afa2b72b819af4c885e0c8a565c869ab07bfbfd6`). Un único commit adicional; sin reescritura de historia.

## 1. Cambios de esta rama
| Archivo | Cambio |
|---|---|
| `.github/workflows/ci.yml` | **Solo las 3 líneas de comentario del encabezado**, reemplazadas por 7 líneas de comentario que dicen: versionado y publicado en ramas de revisión; habilitación no demostrada; sin evidencia de ejecución real; sin validar en runner real; acciones `@v4` pendientes de validación y anclaje por SHA; no despliega ni publica. Desde `name: CI` el archivo es byte a byte idéntico y su estructura YAML interpretada es idéntica (disparadores, jobs, pasos, permisos, versiones, comandos) |
| `docs/architecture/CI.md` | Reescrito: tabla Versionado / Publicado / Habilitado / Ejecutado / Validado, disparadores, los 7 puntos de aclaración y pendientes de la primera ejecución real |
| `README.md` | 2 frases sobre CI alineadas con `CI.md` |
| Este informe | Nuevo |

No se tocaron `src/`, `tests/`, `e2e/`, `scripts/`, configuraciones funcionales, expedientes originales, `evidence/public/`, `INFORME_LIMPIEZA.md`, `AUDITORIA_SEGURIDAD_PREVIA.md` ni los inventarios. `INVENTARIO_CAMBIOS.txt` (de la limpieza anterior) describe el commit `60a0279…`: sus entradas de `README.md` y `docs/architecture/CI.md` quedan desactualizadas a propósito; la lista vigente de cambios está en `INVENTARIO_CAMBIOS.txt` de esta carpeta.

## 2. Enlace de sesión en `afa2b72…` (revisión solo de lectura)
- **Ubicación exacta:** mensaje del commit `afa2b72b819af4c885e0c8a565c869ab07bfbfd6`, línea 17, tráiler `Claude-Session:` con una URL de sesión (ID enmascarado en este informe). Visible en GitHub: el mensaje del commit aparece en la API pública del repositorio (el repositorio es público).
- **Alcance real (hallazgo nuevo):** enlaces de ese mismo tipo aparecen en el mensaje de **74 de los 76 commits** de todas las referencias del repositorio, incluidos **16 de los 17 commits alcanzables desde `main`**. No es una particularidad de `afa2b72…`: ya estaba en el historial publicado antes de las ramas de revisión.
- **En archivos del árbol:** 0 enlaces. Las 24 coincidencias del patrón `session_…` en el árbol son el parámetro de PostgreSQL `session_replication_role`, no enlaces.
- **Identidad del autor/committer del commit:** `Claude <noreply@anthropic.com>` (dirección genérica).
- **Accesibilidad:** una petición HTTP sin iniciar sesión a esa URL devolvió **403** con una página de desafío de verificación («Just a moment…»), sin redirección. Esto **no permite concluir** si el contenido es público o privado: es una respuesta de verificación anti-bots de la plataforma desde el entorno de trabajo. No se intentó eludir el desafío ni acceder a contenido, no se inició sesión y no se tocaron permisos de la sesión. **No se afirma que el enlace sea seguro ni inseguro.**
- **Riesgos que sí pueden demostrarse:** (a) el identificador de la sesión es legible por cualquiera en el historial público; (b) está en 74 commits, 16 de ellos en `main`, de modo que corregir solo `afa2b72…` no lo retiraría del repositorio; (c) reescribir historia cambiaría los hashes de commits de `main` y de las ramas de auditoría, y los commits antiguos seguirían accesibles por SHA mientras GitHub los conserve. **No demostrado:** que alguien pueda abrir la sesión, ni qué contendría.
- **Recomendación (sin ejecutar acciones):** no reescribir historia por este motivo salvo que el propietario lo decida después de un análisis de impacto (afecta a `main`). Como paso de bajo impacto, el propietario puede comprobar desde su cuenta si esas sesiones están compartidas públicamente y, si lo desea, ajustar o retirar el uso compartido desde su lado (no lo hice yo). Para commits futuros, omitir el tráiler. La decisión de conservar o rehacer historia corresponde al propietario.

## 3. Pendientes y límites
No se resolvieron D1–D9, T11, T12, T13 ni la definición de `Project`; no se añadió LICENSE; no se abrió PR; no se ejecutó CI; no se avanzó a Fase 1.1-B. Sin verificar: configuración de Actions del repositorio (403), accesibilidad real del enlace, comportamiento del CI en un runner.
