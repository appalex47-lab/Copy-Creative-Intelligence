# INFORME DE CONCILIACIÓN DE CONTROLES V25

**Alcance:** exclusivamente documental y de trazabilidad. No se modificó código funcional, pruebas, resultados, clasificaciones, limitaciones ni decisiones. **V25 no constituye aceptación formal de Fase 0**, no autoriza Fase 1 ni validaciones en Supabase; la aceptación corresponde exclusivamente al propietario.

## 1. Dictamen de la reconstrucción
La diferencia 16 vs 18 **no es una contradicción de resultados**: es el mismo conjunto de controles ejecutado en dos pasadas de V24. Los reportes mostraban cada una por separado sin una cifra consolidada.

**Cifra consolidada V24 (única, usada en todos los documentos V25): 18 controles de validación documental distintos (C01–C18), todos PASS.** Pasada previa al manifiesto: 16 ejecutados (C01–C16), 16/16 PASS. Pasada final posterior al manifiesto: 18 ejecutados (C01–C18), 18/18 PASS (repite C01–C16 y añade C17–C18). Aparte, 8 verificaciones remotas de publicación (R01–R08).

## 2. Secuencia real reconstruida (con evidencia)
| Etapa | Qué ocurrió | Evidencia |
|---|---|---|
| A. Validación previa al manifiesto | Se ejecutó `val24.py`: 16 controles (C01–C16), 16/16 PASS. Existían el expediente corregido, `INFORME_CORRECCIONES_V24.md` y `MATRIZ_OBSERVACIONES_V23_V24.md`; **aún no** existían `REPORTE_VALIDACION_V24.md` ni `MANIFIESTO_SHA256_V24.txt` (por eso C05 listó 2 archivos nuevos) | `evidencia_reconstruccion_V25/salida_val24_pasada_A_previa_manifiesto.txt`; idéntica al bloque embebido en `REPORTE_VALIDACION_V24.md` |
| B. Generación del manifiesto | Se creó `MANIFIESTO_SHA256_V24.txt` con 256 entradas (todos los archivos de `expediente_final_v24/` salvo él mismo) | Manifiesto V24; `reejecucion_V25_descargas_remotas_V24.txt` (256 coinciden) |
| C. Validación posterior al manifiesto | Se ejecutó de nuevo el mismo script: ahora con el manifiesto presente, se activan C17 y C18 → 18 controles, 18/18 PASS. C05 listó 4 archivos nuevos | `salida_val24_pasada_C_posterior_manifiesto.txt`; idéntica al bloque embebido en `REPORTE_PUBLICACION_V24_GITHUB.md` |
| D. Publicación | Commit `a1dfedb8…` (expediente) y `b88bde03…` (reporte de publicación) en `audit/fase0-v24-review` | GitHub |
| E. Verificación remota | R01–R08 declaradas en el reporte de publicación V24 | Ver §5 |

Respuestas a las preguntas de la reconstrucción: (1) los 16 originales son C01–C16 de la tabla de §3; (2) los 2 adicionales son C17 (manifiesto cubre exactamente los archivos y los hashes coinciden, comparación en Python) y C18 (`sha256sum -c` del manifiesto, método independiente); (3) entrada, resultado y evidencia de cada uno están en `MATRIZ_CONTROLES_V25.csv`; (4) C01–C16 en A y de nuevo en C; C17–C18 solo en C; (5) **sí** se ejecutaron después de generar el manifiesto, porque el script solo los activa si el manifiesto existe y su salida muestra «archivos=256 coinciden=256»; (6) sí se verificó el manifiesto (C17, C18) y los archivos que contiene (256 de 256), y V25 lo re-ejecutó; (7) **no hay duplicados ni omitidos**: los C01–C16 se repiten por diseño entre pasadas; (8) los 18 son complementarios; C17 y C18 comprueban la misma propiedad con dos implementaciones independientes; (9) archivos por etapa: ver Etapa A y C arriba.

## 3. Matriz consolidada (resumen; detalle completo en `MATRIZ_CONTROLES_V25.csv`)
| ID | Etapa | Control | Estado |
|---|---|---|---|
| C01 | A | V23 en el árbol de trabajo idéntico al inventario previo (253 archivos) | PASS |
| C02 | A | V23 sin cambios respecto al commit 8674114 (git) | PASS |
| C03 | A | V24 conserva los 253 archivos de V23 | PASS |
| C04 | A | Solo difieren de V23 el LEEME y SHA256SUMS interno (los otros 251 conservan su SHA-256) | PASS |
| C05 | A | Archivos nuevos en V24 limitados a los 4 autorizados (los presentes) | PASS |
| C06 | A | Evidencias técnicas, scripts, resultados, matrices y diff sin alteración | PASS |
| C07 | A | OBS-01: versión del expediente V21 / corrección V23 / revisión V24 distinguidas; sin «(empaquetado V22)» como  | PASS |
| C08 | A | OBS-02 §3: declaración histórica conservada + aclaración | PASS |
| C09 | A | OBS-02 §15: declaración histórica conservada + aclaración | PASS |
| C10 | A | OBS-03: limitaciones explícitas en LEEME §13 | PASS |
| C11 | A | OBS-03: documentos de limitaciones V23 (sin modificar) ya contienen cada limitación | PASS |
| C12 | A | 12 escenarios PARCIAL listados | PASS |
| C13 | A | Decisiones pendientes del propietario conservadas | PASS |
| C14 | A | Resultados 46/46 (x2), 26/26, 59/59, 300/300, 63/63, 14/14 intactos | PASS |
| C15 | A | SHA256SUMS.txt interno regenerado y válido (no incluye su propio hash) | PASS |
| C16 | A | Sin cambios fuera de docs/fase0/ y ninguno en herramientas/ o historico/ reales | PASS |
| C17 | C | MANIFIESTO_SHA256_V24 cubre exactamente todos los archivos de V24 (salvo él mismo) y todos los hashes coincide | PASS |
| C18 | C | sha256sum -c MANIFIESTO_SHA256_V24.txt desde expediente_final_v24/ | PASS |
| R01 | E | La rama v24 existe y apunta al commit b88bde03… | PASS |
| R02 | E | El commit del expediente V24 tiene como padre el commit V23 y no toca nada fuera de expediente_final_v24 | PASS |
| R03 | E | El árbol remoto (REST) es idéntico al local | PASS |
| R04 | E | Los 256 archivos del manifiesto V24 existen en GitHub y sus hashes coinciden | PASS |
| R05 | E | V23 conserva su rama y su SHA de árbol | PASS |
| R06 | E | V20 y main conservan su SHA | PASS |
| R07 | E | No existe ningún PR | PASS |
| R08 | E | Los documentos corregidos de V24 son accesibles en GitHub | PASS |

Estados usados: PASS, FAIL, BLOCKED, NOT VERIFIED. Resultado: **26 PASS (18 documentales + 8 remotos), 0 FAIL, 0 BLOCKED, 0 NOT VERIFIED**, con las salvedades de §4.

## 4. Salvedades y hallazgos (registrados, sin ocultar)
1. **Ejecuciones intermedias no archivadas.** Durante la preparación de V24 el validador se ejecutó antes de las dos pasadas descritas: una vez con 15/16 PASS (un control de §15 tenía un defecto del propio validador, sensible a mayúsculas, ya corregido) y una vez con 16/16 PASS antes de existir `INFORME_CORRECCIONES_V24.md`. Su salida **no se guardó en archivo**; solo consta en la transcripción de la sesión. No se cuentan en la cifra consolidada.
2. **Script de validación V24 no publicado en V24.** `val24.py` residía fuera del repositorio; V25 lo archiva sin modificar junto con las dos salidas crudas (que coinciden byte a byte con los bloques embebidos en los reportes V24).
3. **Verificaciones remotas R01–R08 de V24:** la salida cruda histórica no se archivó; estaban declaradas en el reporte de publicación V24. **Históricamente NOT VERIFIED por falta de salida cruda; re-ejecutadas en V25 (ejecución nueva, no histórica), todas PASS** (`reejecucion_V25_remoto_V24.txt`). La matriz las marca PASS con esa evidencia y etapa explícita.
4. **Debilidad de diseño de C05:** comprueba que los archivos nuevos sean un subconjunto de los 4 autorizados, no que existan los 4; su existencia queda cubierta por C17/C18 (el manifiesto cubre exactamente los archivos). No es un defecto de resultado.
5. El manifiesto V24 y la nota de V25 se concilian como se explica en `MATRIZ_CAMBIOS_V24_V25.md` (el V24 verifica en V25 con 3 discrepancias esperadas, controladas por P07).

## 5. Ejecuciones nuevas de V25 (no históricas)
- `val24.py` sobre V24 publicado (commit `b88bde03…`, árbol limpio): 18/18 PASS, mismos estados que la pasada final histórica.
- Verificaciones remotas R01–R08 contra GitHub: todas PASS (256 de 256 archivos descargados coinciden con el manifiesto V24).

## 6. Correcciones documentales realizadas
Se añadió una «Nota de conciliación V25» con la cifra consolidada a `REPORTE_VALIDACION_V24.md`, `INFORME_CORRECCIONES_V24.md`, `MATRIZ_OBSERVACIONES_V23_V24.md` y `V24_publicacion/REPORTE_PUBLICACION_V24_GITHUB.md` (copias dentro de V25). Su contenido original no cambia. V24 sigue intacto en su rama.

## 7. Limitaciones que permanecen (sin cambio)
PostgreSQL temporal: 63/63 pruebas y 14/14 mutaciones según la evidencia existente, sobre un fixture que no es el esquema aprobado; 12 escenarios PARCIAL; T-409 a T-422 sin ejecución individual propia; 22 funciones validadas indirectamente por ejecución, no línea por línea; sin validación física en CCI-DEV; sin validación de RLS, privilegios, concurrencia real ni del esquema físico aprobado; trigger R1–R9 no ejecutado; HV-02 / PO-05 sin verificación. Decisiones pendientes del propietario abiertas: PO-05, G-1, G-5, G-10, DG-19, DG-20, DG-09, DG-12, DG-16, DG-18, DEP-RET-01, G-9, RP-01, P-01 a P-05, P-10, OD-13.
