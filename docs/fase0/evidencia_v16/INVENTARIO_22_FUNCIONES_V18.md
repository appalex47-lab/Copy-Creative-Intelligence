# INVENTARIO DE LAS 22 FUNCIONES DE EJECUCIÓN (V18)

Trabajo documental local posterior a V16 (commit 6a1af24); no publicado. Fuente: `docs/fase0/herramientas/modelo_estructural.py` (sin modificar) y `verificar_expediente.py` (sin modificar). Resultados individuales obtenidos con el script externo `instrumentar_22_funciones_v18.py` (solo lectura); salidas en `salida_22_funciones_corrida1.txt` y `..._corrida2.txt` (SHA-256 idéntico: 2b856198…f2f4). Alcance de la evidencia: **modelo en memoria**; no es PostgreSQL ni Supabase.

| # | Función | Casos | Qué verifica | Componente | Cómo la invoca el verificador (líneas) | Resultado individual | Cobertura suficiente (en el modelo) | Instrumentación adicional |
|---|---|---|---|---|---|---|---|---|
| 1 | pruebas_guarda | 9 | Guarda de publicación: asignaciones directas y nonce | Guarda/trigger de publicación (G-10) | verificar_k47_modelo 1318; criterios_v12 1617; informe 1681 | Sí, impresa por el verificador (tabla «sí/NO») | Sí, 9/9 | No |
| 2 | pruebas_atomicidad | 20 | Atomicidad de escrituras de procedencia (fallo a mitad) | Motor de procedencia | verificar_k55_modelo 1280; k47 1320; informe 1679 | Sí, impresa | Sí, 20/20 | No |
| 3 | correr_mutaciones_rechazo | 12 | Rechazo del motor ante alteraciones de la carga original | Motor, cadena de assets | verificar_rs14 836; k47 1311; mutaciones 1351 | Sí (flags por caso en el modelo; el verificador agrega) | Sí, 12/12 con 7 indicadores por caso | No |
| 4 | correr_adversariales | 16 | El motor forzado acepta y el auditor independiente detecta | Auditor, E, publicación | checks_v7 988; k47 1315; informe 1677 | Sí en el modelo; el verificador agrega | Sí, 16/16 | No |
| 5 | correr_escenarios | 17 | Escenarios de conservación y sustitución de atribuciones | Atribuciones por campo | checks_v7 983; k47 1300; informe 1652 | Sí en el modelo; el verificador agrega | Sí, 17/17 | No |
| 6 | correr_mutaciones_k47 | 36 | Mutaciones del auditor (invariantes I1…) | Auditor K47 | checks_v7 983; k47 1304; mutaciones 1334 | Sí (cada mutación DETECTADA en la salida) | Sí, 36/36 | No |
| 7 | correr_mutaciones_resoluciones | 12 | Inmutabilidad y reglas de resoluciones de descarte | Resoluciones (I13) | checks_v7 984; k47 1307; mutaciones 1336 | Sí (DETECTADA en la salida) | Sí, 12/12 | No |
| 8 | correr_mutaciones_assets | 53 | Procedencia de arte: uploader, evento, atribución | Assets (I16…) | rs14 836; k55 1282/1286; k47 1309; mutaciones 1338 | Sí (DETECTADA en la salida) | Sí, 53/53 | No |
| 9 | correr_positivos_arte | 26 | Casos válidos de arte que deben aceptarse | Assets | checks_v7 984; k47 1313; criterios_v12 1617; informe 1675 | Sí en el modelo; el verificador agrega | Sí, 26/26 | No |
| 10 | correr_mutaciones_k45 | 30 (27 mutaciones + 3 positivos) | Mutaciones sobre la matriz 4.4.10 (K45) | Contrato semántico de relaciones | k45 1101; mutaciones 1330; criterios_v12 1625 | Sí (DETECTADA) | Sí | No (requiere la matriz de la especificación) |
| 11 | correr_mutaciones_cadena | 24 | Cadena de procedencia: eslabón alterado | Cadena de assets (K56) | _ejecutadas14 765; estructura15 801; mutaciones 1342 | Sí (CHAIN-NN en la salida) | Sí, 24/24 | No |
| 12 | correr_adversariales_cadena | 24 | Motor forzado + auditor sobre la cadena | Auditor de cadena | _ejecutadas14 765; estructura15 801 | Sí en el modelo; agregado en el verificador | Sí, 24/24 | No |
| 13 | correr_mutaciones_atribucion | 12 | Mutaciones de atribución (I13, I15…) | Atribuciones | _ejecutadas14 765; mutaciones 1347 | Sí (ATTR-NN) | Sí, 12/12 | No |
| 14 | **pruebas_atomicidad14** | 11 | Atomicidad de operaciones de v14 (carga de asset, reutilización…): fallo a mitad, actor ajeno, versión inexistente; estado completo idéntico | Escrituras de procedencia | _ejecutadas14 766; estructura15 801; K56 línea 953 (cuenta) | Sí, cada caso AT14-01…AT14-11 con `ok`; el verificador solo imprime «AT14 11/11» | Sí, 11/11 | **Resuelta con el script V18 (sin modificar la lógica)** |
| 15 | **pruebas_E14** | 6 | Reconstrucción de E con contribuyentes verificables y fallo cerrado | Conjunto excluido E | _ejecutadas14 766; estructura15 801; K56 953 | Sí, E14-01…E14-06 con `ok`; el verificador imprime «E14 6/6» | Sí, 6/6 | Resuelta con el script V18 |
| 16 | correr_mutaciones_av | 8 | `asset_version` incorrecto en eslabones propios | Cadena (K58) | _ejecutadas14 767 | Sí en el modelo (14 indicadores por caso) | Sí, 8/8 | Resuelta con el script V18 |
| 17 | correr_mutaciones_cf | 8 | Campo incorrecto en eventos propios | Cadena (K58) | _ejecutadas14 767 | Ídem | Sí, 8/8 | Resuelta con el script V18 |
| 18 | correr_mutaciones_ac | 6 | Combinaciones `asset_version` + campo | Cadena (K58) | _ejecutadas14 767 | Ídem | Sí, 6/6 | Resuelta con el script V18 |
| 19 | correr_positivos15 | 8 | Cadenas válidas de v15 que deben aceptarse | Cadena | _ejecutadas14 767 | Sí en el modelo | Sí, 8/8 | Resuelta con el script V18 |
| 20 | correr_adversariales15 | 8 | Motor forzado + auditor con v15 | Auditor | _ejecutadas14 767 | Sí en el modelo | Sí, 8/8 | Resuelta con el script V18 |
| 21 | **pruebas_atomicidad15** | 8 | Atomicidad antes/después de validar la raíz; el reintento sin fallo repone el estado | Escrituras de procedencia | _ejecutadas14 767 | Sí, AT15-01…AT15-08 con `ok` | Sí, 8/8 | Resuelta con el script V18 |
| 22 | correr_mutaciones_modelo14 | 12 | Mutaciones del propio modelo (p. ej. validación por eslabón convertida en no-op) | Modelo / K56-M | _ejecutadas14 766; mutaciones 1349; criterios | Sí (K56-MNN) | Sí, 12/12 | No |

**Totales:** 22 funciones, 366 casos individuales (363 de mutación/negativos/adversariales/escenarios + 3 positivos de K45; corregido en V20: la cifra de V18 «363» no contaba los 3 positivos que sí se imprimían), 0 fallos, dos corridas idénticas.

**Aprobación agregada frente a individual.** Antes de V18 solo 2 de las 22 (guarda y atomicidad) tenían resultado individual a la vista; el verificador agregaba el resto. Con la instrumentación externa los 366 casos tienen veredicto individual PASS **en el modelo en memoria**. Esto no equivale a «las 22 funciones individualmente aprobadas contra una base real»: la aprobación individual es del modelo en memoria y se basa en los indicadores `ok`/`det` que el propio modelo devuelve. No se modificó la lógica de ninguna prueba.

**Límite.** «Cobertura suficiente» significa que el recuento de casos coincide con el esperado por el verificador (K45–K59) y que todos pasan; no demuestra que el conjunto de casos sea exhaustivo para Fase 1.

## Nota V20 (2026-11-19) sobre el estado de publicación

Las expresiones «local», «no publicado» y «sin commit» de las secciones anteriores describen el estado en la fecha de cada sección (histórico, no se borra). Desde entonces V16–V19 se publicó en la rama `audit/fase0-v19-review` (commit `c6ef74be4db185ac3e4fd36810f24619e6f51fcf`); `main` sigue en V16. El trabajo V20 está en el árbol local sin commit. Estado vigente y cierre: `../expediente_final_v16_v19/`.
