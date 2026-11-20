# REGISTRO DE CAMBIOS V20 → V21

**Versión:** V21 · **Fecha:** 2026-11-20 · **Fuente:** `git diff ac84133b776cc73c0cb3416e51e2767039bb5132` sobre el árbol de trabajo y las pruebas de `scripts/v21_bateria_cierre.py` · **Estado de verificación:** cada defecto tiene una prueba de la batería que lo detecta y un control negativo (`salidas/salida_controles_negativos_V21.txt`) que demuestra que esa prueba falla si el defecto reaparece.

Alcance: solo `docs/fase0/`. No se modificaron el motor (22 funciones), el verificador, `historico/`, la v3.3, la especificación (salvo el bloque de estado final, que es uniforme en los cinco documentos activos), las salidas de ejecución originales ni ninguna decisión del propietario.

## A. Defectos encontrados y corregidos
| ID | Defecto comprobado | Dónde | Corrección | Prueba que lo vigila |
|---|---|---|---|---|
| D-01 | `INVENTARIO_DECISIONES_ABIERTAS_FASE0.md` conservaba la distribución previa a PE-01..PE-05 («1 A, 3 B, 69 C, 5 E») mientras el informe V20 y la matriz decían A 1, B 8, C 69, D 153, E 0 | inventario | Distribución corregida y explicada (las 5 reglas IG1-05, IG1-06, IG1-10, IG1-21 e IG5-36 pasaron de E a B; B 3 + 5 = 8; B no implica implementación en el producto) | V21-A02, V21-E01, V21-E02 |
| D-02 | La fila DG-20 del inventario la describía como «reservada en límites (sec. P)»; la especificación la define como la ampliación `approvals.decision` sujeta a aceptación | inventario | Descripción y fuente (líneas 4786 y 2778) ajustadas a la especificación; no se resolvió la decisión | V21-F04, V21-E06 |
| D-03 | `Linea_definicion` de **198 de las 231 reglas** apuntaba a una fila que ya no era su definición (numeración anterior a las últimas ediciones de V20) | `MATRIZ_FINAL_231_REGLAS_V16_V19.csv` | Recalculada desde el texto de la especificación vigente (`scripts/v21_corregir_lineas.py`) | V21-F01 |
| D-04 | `Linea_ESPEC` de **los 780 escenarios** desfasada (+11) | `MATRIZ_FINAL_780_ESCENARIOS_V16_V19.csv` | Recalculada desde texto | V21-F02 |
| D-05 | Las citas «narrativa: l.N» (90 citas en 66 reglas) se habían calculado contra la especificación del commit c6ef74b: 62 de las 66 filas apuntaban a líneas ya desplazadas | columna `Dependencias_y_relaciones` | Trasladadas por correspondencia de texto a la especificación vigente; cada cita contiene la regla | V21-F03 |
| D-06 | Citas de línea de la especificación desfasadas en documentos V20: «fila 1270», «línea 3620», «spec línea 1114», «Spec l.2556» | `MATRIZ_MODELO_DATOS_FINAL.md`, `AUDITORIA_FINAL_FASE0_V16_V19.md`, `PE_POSTGRESQL_V20/README.md`, `REVISION_FUENTES_…V20.md`, inventario | Actualizadas (1301, 3656, 1118) con la numeración anterior indicada donde corresponde; `ANCLAS_LINEAS_V21.csv` fija cada cita a un texto verificable | V21-F04 |
| D-07 | El bloque de estado de los cinco documentos activos afirmaba que el trabajo V20 estaba «solo en el árbol local, sin commit», aunque V20 ya estaba publicado (`ac84133`) | cinco documentos activos | Bloque V21 uniforme: última publicación verificada, `main` intacta, la publicación de V21 requiere autorización; no puede contener el SHA de su propio commit | V21-E03, V21-E04 |
| D-08 | Documentos V20 que ya no son vigentes carecían de aviso de sustitución (`INFORME_FINAL_V20.md`, `MATRIZ_ACEPTACION_V20_C01_C32.md`, manifiesto V20) y los tres avisos previos apuntaban a V20 | `expediente_final_v16_v19/` | Avisos «Superseded (V21)» y cadena de sustitución V19→V20→V21 | V21-G02 |
| D-09 | Nueve documentos de `evidencia_v16/` conservaban estados de publicación, cifras (363) y esquemas de clasificación antiguos sin aviso de que son históricos | `evidencia_v16/*.md` | Aviso «Documento HISTÓRICO (V21)» tras el título; contenido y salidas sin alterar | V21-G02, V21-G11 |
| D-10 | El README de PE nombraba la segunda corrida sin el prefijo real del archivo | `PE_POSTGRESQL_V20/README.md` | Nombre real | V21-F05 |
| D-11 | `REGISTRO_HISTORICO_VERSIONES.md` no tenía entrada para V21 | registro | Entrada V21 añadida al final (la historia anterior, incluida la línea 126 de PO-05, no se tocó) | V21-E07 |

## B. Verificado sin defecto (se repitió, no se corrigió nada)
- Cifras 231 / 780 / 41 / 22 / 366 / 63 / 14 / 59 / 300: coinciden con la evidencia primaria (`MATRIZ_CONCILIACION_V21.md`).
- Reconciliación 363/366: confirmada (363 + 3 positivos de K45).
- Trazabilidad reglas↔escenarios: 1592 pares bidireccionales, sin huérfanos.
- 22 funciones: tercera corrida real idéntica a las dos de V20. PostgreSQL: 63/63 y 14/14, tercera y segunda corrida reales idénticas a las de V20.
- Motor, verificador, `historico/`, v3.3, salidas originales: sin cambio (SHA-256 y diff).
- Observación sobre el verificador protegido (no modificable en esta intervención): sus 59 comprobaciones se identifican como 58 con número K (K01..K59 sin K43, que no se usa) más `K55-V12`, el control que en v12 compartía el identificador K55 (documentado en la especificación, sección N). No afecta a ningún resultado; se registra para que nadie busque un «K43».
- **Defectos del motor de CCI: ninguno detectado** (el motor no se modificó en cualquier caso).

## C. Sin cambios (protección)
`main` (6a1af24); las 22 funciones; el comportamiento del producto; PO-05 y el resto de decisiones; los 17 permisos, 5 roles, 13 transiciones T-02, 76 subfases y 27 tablas base; Supabase (sin conexión alguna); Fase 1 (no iniciada, no autorizada).

## D. Archivos
El inventario exacto de archivos creados, modificados y eliminados respecto de V20 se presenta en el informe final de la intervención (`git diff --name-status ac84133` y archivos sin seguimiento) y está cubierto por `MANIFIESTO_EVIDENCIAS_SHA256_V21.txt`. **Eliminados: ninguno.**
