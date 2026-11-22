# Limpieza documental posterior a la publicación de revisión

Rama: `review/cci-publication-cleanup`, creada desde el commit de referencia `afa2b72b819af4c885e0c8a565c869ab07bfbfd6` (rama `review/cci-fase1-1-audit`, sin cambios). Un único commit adicional; sin reescritura de historia ni force-push; sin PR, merge ni deploy.

## 1. Alcance de los cambios
- **Modificados (3):** `README.md`, `docs/architecture/CI.md`, `evidence/CCI_REVISION_PUBLICACION_20261122T034938Z/AUDITORIA_SEGURIDAD_PREVIA.md`.
- **Nuevos:** `evidence/public/` (14 copias derivadas, `README.md`, `TRANSFORMACIONES.csv`, `MANIFEST_PUBLICO.sha256`) y `evidence/CCI_LIMPIEZA_PUBLICACION_20261122T044210Z/` (este informe e `INVENTARIO_CAMBIOS.txt`). Lista exacta con SHA-256 en `INVENTARIO_CAMBIOS.txt`.
- **Intactos (comprobado):** 252 de los 255 archivos de la rama de referencia (los otros 3 son los modificados). Sin cambios en `src/`, `tests/`, `e2e/`, `scripts/`, `public/`, `package*.json`, `tsconfig*`, configuraciones, `.github/` ni `docs/fase0/`.

## 2. Rutas internas del entorno temporal
**Detectadas: 31 referencias en 15 archivos** (28 en 14 archivos de expedientes originales + 3 en un documento de la publicación de revisión). Raíces: 3 rutas distintas bajo `/tmp` más una bajo `/home`; ninguna contiene nombres de persona, hosts, credenciales ni URL privadas.

| Clase | Referencias | Dónde | Tratamiento |
|---|---|---|---|
| A. Muestran con qué raíz/herramienta se ejecutó una prueba (la versión y la estructura importan; la ruta literal, poco) | 23 | 10 líneas `RUN vX.Y.Z <raíz>` en logs de Vitest; 8 rutas de configuración/directorios en `e2e_results.json`; 5 líneas de la traza del fallo esperado del build de producción | Original conservado intacto; copia pública con descripción neutral |
| B. Rutas internas sin valor para el lector | 8 | 5 en narrativa de expedientes (estado inicial 1.0; estado Git de 1.1-A1: líneas base temporales y directorio de respaldos); 3 en `AUDITORIA_SEGURIDAD_PREVIA.md` | Copia pública para las 5 de expedientes; las 3 del documento de publicación se editaron en el propio documento (neutralizadas) |
| C. Permiten identificar información privada o interna sensible | 0 | — | No aplica. `/home/...` es el directorio de usuario genérico del entorno de herramientas, no de una persona |

- **Tratadas: 31 de 31.** 28 mediante copias derivadas en `evidence/public/` (sustituciones: `[entorno temporal de ejecución]`, `[archivo temporal de líneas base]`, `[directorio temporal de respaldos]`) y 3 editando el documento de publicación.
- **Conservadas por trazabilidad: 28**, en los expedientes originales, que no se tocaron ni se reemplazaron (sus manifiestos no se alteraron). Las 3 del documento de publicación no se conservan literalmente.
- **Limitación:** el historial Git de `afa2b72…` y los originales siguen conteniendo esas rutas; es una decisión explícita (no reescribir historia, no sacrificar trazabilidad). Las rutas son de un entorno de trabajo temporal y ya no existen como tales.
- Se sustituyeron 28 ocurrencias en la capa pública y, en 6 logs, se eliminaron líneas en blanco finales (para `git diff --check`); registrado en `evidence/public/TRANSFORMACIONES.csv`.

## 3. Mensaje del commit de referencia
El mensaje de `afa2b72…` contiene un enlace de sesión de una herramienta de trabajo. **No se reescribió** (no hay force-push ni rebase). El nuevo commit no incluye identificadores de sesión, enlaces privados ni metadatos internos de herramientas; tampoco las líneas de coautoría automáticas que se añadían a commits anteriores, por la restricción de «metadatos internos».

## 4. CI (resumen; detalle en `docs/architecture/CI.md`)
Publicado en ramas de revisión: sí. Habilitado en GitHub: no verificado (el permiso de Actions devolvió 403). Ejecutado: no (0 ejecuciones en la rama; solo hay ejecuciones de GitHub Pages sobre `main`). Validado en runner real: no. Pendiente: primera ejecución, validación del YAML, acciones `@v4`, Chrome en el runner. Disparadores: `pull_request`, `push` a `development/**`, `workflow_dispatch`; el push a `review/cci-fase1-1-audit` no coincidió con ninguno. `ci.yml` no se modificó (su comentario de cabecera quedó desactualizado: hallazgo documentado).

## 5. Revisión de los documentos de publicación
- `INVENTARIO_ARCHIVOS.txt` e `INVENTARIO.sha256` **no se modificaron**: describen el commit `afa2b72…` (193 archivos). En la nueva rama, `README.md` y `docs/architecture/CI.md` ya no coinciden con esas entradas y hay archivos nuevos; esto se declara en la nota añadida a `AUDITORIA_SEGURIDAD_PREVIA.md` y en este informe. La verificación del inventario antiguo contra el árbol actual falla en esos dos archivos **de forma esperada**.
- `AUDITORIA_SEGURIDAD_PREVIA.md`: se añadió una nota de actualización y se neutralizaron las rutas; se conservaron las limitaciones, las pruebas pendientes y las decisiones no resueltas. Reafirma que el escaneo heurístico **no garantiza** ausencia absoluta de secretos.
- No se incorporaron nuevos expedientes originales ni evidencia de Fase 0.

## 6. Controles antes del commit
| Control | Resultado |
|---|---|
| Cambios limitados a documentación y metadatos autorizados | Sí: 3 modificados + archivos nuevos solo bajo `evidence/` |
| Sin cambios en `src/`, `tests/`, `e2e/`, `scripts/`, configuraciones funcionales | 0 entradas en esas rutas |
| Escaneo de secretos (20 archivos modificados/nuevos al momento del escaneo; escáner del proyecto + regex independiente de 14 familias, incluidas rutas internas e identificadores de sesión) | 0 hallazgos |
| SHA-256 de los 255 archivos de la rama de referencia | 252 idénticos; los 3 distintos son exactamente los modificados esperados |
| Manifiestos originales de los 5 expedientes (`sha256sum -c`) | 0 fallos |
| `MANIFEST_PUBLICO.sha256` (16 entradas) | 0 fallos |
| Copias derivadas vs originales | Difieren solo en las líneas sustituidas (verificado por script); JSON válido |
| `git diff --check` | exit 0 |
| Archivos temporales/secretos añadidos | Ninguno |
| Pruebas funcionales | No ejecutadas (no necesarias; no se alteraron resultados históricos) |

## 7. No verificado / pendiente del propietario
Habilitación de Actions y validación en runner; resolución de T11, T12, T13 y D1–D9 (no tocadas); licencia; si se retira `ci.yml` de las ramas de revisión; si se conserva o rehace el commit con el enlace de sesión (requeriría reescritura, no autorizada).
