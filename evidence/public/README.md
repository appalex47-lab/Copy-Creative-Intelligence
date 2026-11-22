# `evidence/public/` — copias de consulta pública (derivadas)

**Esta carpeta NO contiene evidencia original ni manifiestos originales verificados.** Son copias de consulta de algunos archivos de los expedientes originales, en las que solo se sustituyeron rutas del entorno temporal de ejecución por descripciones neutrales. Los expedientes originales permanecen intactos en `evidence/CCI_FASE1_*` con sus propios manifiestos `MANIFEST.sha256`; ante cualquier duda, **el original manda**.

## Qué se cambió y qué no
- Se sustituyeron 28 referencias a rutas del entorno de trabajo temporal (en 14 archivos) por `[entorno temporal de ejecución]`, `[archivo temporal de líneas base]` o `[directorio temporal de respaldos]`. El resto del contenido es idéntico: mismos resultados, conclusiones, versiones y recuentos.
- En 6 logs `.txt` se eliminaron además las líneas en blanco finales (solo para que `git diff --check` pase); no cambia ningún resultado. Está registrado en la columna `otros_cambios` de `TRANSFORMACIONES.csv`.
- Los `.md` y `.txt` llevan una línea/bloque inicial que los identifica como copia pública y cita el SHA-256 del original. Los `.json` no llevan banner para no alterar su estructura (siguen siendo JSON válido).
- Solo se derivaron los archivos que contenían esas rutas; el resto de cada expediente no se duplica: se consulta en el original.
- `TRANSFORMACIONES.csv` registra, por archivo: ruta y SHA-256 del original, ruta y SHA-256 de la copia, referencias sustituidas y si se añadió banner.
- `MANIFEST_PUBLICO.sha256` cubre únicamente los archivos de esta carpeta (derivados, este README y `TRANSFORMACIONES.csv`; no se lista a sí mismo). Verifica estas copias, **no** las evidencias originales.

## Limitaciones
- Una copia derivada no demuestra por sí sola la ejecución original: para trazabilidad completa usar el archivo original y su manifiesto. Las trazas y las rutas literales siguen existiendo en los originales (no se sacrificó trazabilidad).
- Un lector no distingue en la copia si la ruta original era la del clon de trabajo o la de la copia limpia; esa distinción se conserva en los nombres de archivo (`work_*` / `clean_*`) y en los originales.
- El historial Git de la rama anterior contiene los originales sin cambios; esta carpeta no reescribe historia.
- Los expedientes describen el estado **a la fecha en que se emitieron**. En particular, las menciones a «CI preparado, no publicado» (expediente 1.0.2) eran ciertas entonces; el estado actual del CI está en [`docs/architecture/CI.md`](../../docs/architecture/CI.md).

## Índice de expedientes originales
| Expediente original | Contenido | Manifiesto original | Copias públicas aquí |
|---|---|---|---|
| [`CCI_FASE1_0_20261122T024706Z`](../CCI_FASE1_0_20261122T024706Z/) | Fase 1.0: fundación técnica de la aplicación | `MANIFEST.sha256` en el expediente | 3 archivos |
| [`CCI_FASE1_0_1_20261122T030445Z`](../CCI_FASE1_0_1_20261122T030445Z/) | Fase 1.0.1: corrección de los hallazgos 1–4 | `MANIFEST.sha256` en el expediente | 3 archivos |
| [`CCI_FASE1_0_2_20261122T031336Z`](../CCI_FASE1_0_2_20261122T031336Z/) | Fase 1.0.2: hallazgos 5–8, accesibilidad, navegador real, responsive, CI preparado | `MANIFEST.sha256` en el expediente | 7 archivos |
| [`CCI_FASE1_1_20261122T032947Z`](../CCI_FASE1_1_20261122T032947Z/) | Fase 1.1-A: trazabilidad de contratos contra el diseño de Fase 0 (no aprobado) | `MANIFEST.sha256` en el expediente | ninguno (sin rutas internas) |
| [`CCI_FASE1_1_A1_20261122T033450Z`](../CCI_FASE1_1_A1_20261122T033450Z/) | Fase 1.1-A1: revisión complementaria (matriz normalizada, identificadores) | `MANIFEST.sha256` en el expediente | 1 archivo |

Los documentos de la publicación de revisión están en [`../CCI_REVISION_PUBLICACION_20261122T034938Z/`](../CCI_REVISION_PUBLICACION_20261122T034938Z/) y el informe de esta limpieza en `../CCI_LIMPIEZA_PUBLICACION_20261122T044210Z/`.
