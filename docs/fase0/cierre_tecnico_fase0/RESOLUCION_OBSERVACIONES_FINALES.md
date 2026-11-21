# RESOLUCIÓN DE LAS OBSERVACIONES DE LA REVISIÓN INDEPENDIENTE (reconciliación 51/51 y cuatro referencias)

Generado por `scripts_validacion/ct_gen_resolucion_observaciones.py` a partir del commit revisado `5b008485706bde3e9cf8407e71c0652cfd0497a5` (leído con git) y del árbol actual. Las columnas «existe» se calculan; no se copian de mensajes anteriores.

## 1. Contradicción en la reconciliación
| Documento en el commit revisado (resultado HISTÓRICO, no vigente) | Totales |
|---|---|
| `INFORME_RECONCILIACION_INTEGRAL.md` (commit revisado) | TOTAL=56 PASS=56 FAIL=0 |
| `scripts_validacion/resultados/reconciliacion_integral.txt` (commit revisado) | TOTAL=56 PASS=56 FAIL=0 |

**Comprobación fallida (recuperada del informe revisado):** `nombres de archivo citados existen en el dossier…`. Referencias que la hicieron fallar: 0.

**Causa exacta (defecto de orden de generación y de autorreferencia, no del contenido del expediente):** el Markdown se generó a partir de la salida de una ejecución previa de la reconciliación (con FAIL=1) y *después* se volvió a ejecutar la reconciliación, que reescribió solo el TXT (FAIL=0). Eran dos ejecuciones distintas con dos fuentes distintas. Además la comprobación de referencias leía el propio informe generado (que cita sus fallos y su propio TXT) y aceptaba un nombre por coincidencia de nombre base en cualquier carpeta (verificador débil).

**Corrección:** `ct_reconciliacion_integral.py` produce en una sola ejecución `reconciliacion_integral.json` (fuente), `.txt` e `INFORME_RECONCILIACION_INTEGRAL.md`, con evidencia (archivo y SHA-256) por comprobación; `ct_verificar_consistencia_informe.py` comprueba que los tres coinciden (totales y estado por comprobación) y tiene controles negativos (incluye la contradicción original FAIL=0→FAIL=1). El verificador de referencias exige ruta exacta cuando la referencia incluye carpeta, nombre exacto (sensible a mayúsculas) cuando no, comprueba enlaces relativos, excluye el informe generado y solo admite citas de archivos retirados si la línea está etiquetada como histórica.

## 2. Las cuatro referencias
| # | Documento que la cita | Referencia | Existe en el commit revisado | Existe ahora | Mayúsculas/ruta exactas | Cita vigente en el documento (commit revisado) | Resolución |
|---|---|---|---|---|---|---|---|

Lectura: dos referencias eran citas históricas de herramientas retiradas (no son enlaces rotos) y dos eran referencias válidas pero evaluadas antes de existir o de forma autorreferente. Ninguna exigía restaurar archivos ni borrar trazabilidad histórica. El resultado del verificador de referencias corregido (ejecución completa desde cero) consta en `INFORME_RECONCILIACION_INTEGRAL.md` (comprobación «referencias a archivos…») y en `reconciliacion_integral.json`.

