# REPORTE DE FORMATO E INTEGRIDAD (V20)

**Versión:** V20 · **Fecha:** 2026-11-19 · **Fuente:** `git diff --check` con índice temporal (`GIT_INDEX_FILE`, sin tocar el índice real) · **Estado de verificación:** ejecutado; resultado real abajo.

## Clasificación de las 2.217 advertencias previas
| Causa | Cantidad | Tratamiento |
|---|---|---|
| Fin de línea CRLF en 4 CSV de `evidencia_v16/` | 2.177 | Normalizados a LF sin BOM; igualdad lógica de contenido verificada (mismas filas/columnas/valores). |
| Espacio final real en `EVIDENCIA_PRUEBAS_INDIVIDUALES_V16.md` y `REPORTE_REGRESION_V16.md` | 40 (incl. 1 + 1 en prosa; el resto en tablas/salidas) | Eliminado el espacio final de prosa; ver política de salidas crudas. |
| Salidas crudas `salida_*.txt` con espacios finales | (parte de las 40) | **No se editan** (evidencia byte a byte); `.gitattributes` en `evidencia_v16/`: `salida_*.txt whitespace=-trailing-space`. |

Política V20: UTF-8 sin BOM, LF; las salidas crudas de herramientas son evidencia original y están exentas del control de espacio final.

## Resultado real
- `git diff --cached --check 6a1af24` (índice temporal con todo `docs/`): **RC=0, 0 líneas de advertencia**.
- `git diff --cached --check c6ef74b`: **RC=0, 0 líneas**.
- Archivos `salida_*.txt` y motor, verificador e históricos: sin modificación (`git diff --quiet c6ef74b` sobre esas rutas = sin cambios).
- v3.3 SHA-256 `b5dccdc73a8103966ab1e1b1e84b2e7ead68cd736fba666ec71d0e790d51c1da` (sin cambio).
- motor `cc87236a19b924617e13346f80eb642d0dc5f0090664908d1e96d8780f4fc52a`; verificador `1acec85dc5e76c9e004d8f2b7ed942c94826377ff240c346bee9f2792e7a035a` (sin cambio).
- Hashes de todos los archivos del expediente: ver `MANIFIESTO_EVIDENCIAS_SHA256.txt`.

## No verificado
No se probó la renderización en visores externos ni la lectura de los CSV por Excel/otras herramientas (solo parseo con Python).

## Verificación V20 (2026-11-20, segunda pasada)
Sobre los 59+ archivos modificados o nuevos de `docs/`: 0 BOM, 0 CR, UTF-8; todos los CSV (9) se releyen con el lector `csv` con número de columnas constante por fila (filas: 231 reglas, 780 escenarios, 1.592 pares, 366 casos, 1.148 + 30 referencias, etc.). `git diff --cached --check` con índice temporal contra 6a1af24 y contra c6ef74b: ver resultado en `INFORME_FINAL_V20.md` (sección E). Las salidas crudas `salida_*.txt` y los `.sql`/`.sh` de `PE_POSTGRESQL_V20/` siguen la misma convención (UTF-8, LF); las salidas crudas están exentas del control de espacio final por `.gitattributes`.
