# EXPEDIENTE INDIVIDUAL DE LOS ESCENARIOS T-409 A T-422

**Alcance:** 14 escenarios de «conservación H-02 v8» (tipo Diseño, veredicto V26 «DEMUESTRA (lectura V20)»). Cada expediente separa la **revisión estática** (lectura de la especificación y de las reglas) de la **ejecución** (mutaciones del modelo en memoria `modelo_estructural.py`, ejecutadas localmente sin modificarlo con `scripts_validacion/ct_k47_por_escenario.py`).

**Qué significa «Rechazo (K47)».** En la especificación, el resultado esperado de los 14 escenarios es el rechazo por K47: el auditor estructural de conservación (invariantes I1…I12 sobre un motor en memoria) debe detectar la alteración. Es una verificación sobre un **modelo en memoria**, no sobre el esquema físico ni sobre funciones SQL.

**Limitación de la correspondencia.** La especificación no declara qué mutación K47 ejecuta cada escenario. La correspondencia T→mutación de este expediente es **inferencia del revisor** por coincidencia semántica entre el texto del escenario y la descripción de la mutación; está en `scripts_validacion/ct_k47_por_escenario.py` (diccionario MAP) y puede ser contradicha por el propietario técnico.

**Resultado global:** 25 mutaciones mapeadas, 25 detectadas, todas con estado inicial válido y un único cambio efectivo (`resultados/k47_por_escenario.txt`). Los 14 quedan en **PASS a nivel MODELO_EN_MEMORIA**; ninguno se ejecutó contra el esquema físico porque **las funciones físicas no existen** (Fase 1 no iniciada).

## T-409 — H-02 v8 conservación: sustitución sin segmentos idénticos elimina automáticamente la atribución

| Campo | Contenido |
|---|---|
| Línea en la especificación | 4130 |
| Texto del escenario | `¦ T-409 ¦ H-02 v8 conservación: sustitución sin segmentos idénticos elimina automáticamente la atribución ¦ Tabla de efectos válida ¦ Cambiar a sustituido el efecto a retirada automática ¦ Rechazo (K47) ¦ Retirar por segmentos ¦ Resultado esperado cumplido y ninguno prohibido ¦ Diseño ¦ IG5-97, IE-12 ¦` |
| Reglas | IG5-97, IE-12 |
| Veredicto V26 (sin alterar) | DEMUESTRA (lectura V20) |
| Revisión estática | Precondición «tabla de efectos válida»; la alteración y el resultado prohibido son coherentes con la regla IG5-97 (efectos estructurales por clasificación y fuente). |
| Regla IG5-97 (clase D) | Efectos estructurales por clasificación y fuente: brief, promoción y copy siguen exactamente la misma tabla. sin_cambio conserva todas las atribuciones activas y no crea contribuyentes; introducido incorpora al actor; modificado conserva todas las activas e incorpora al editor; sustituido conserva provisionalmente todas las activas e incorpora al sustituidor… |
| Regla IE-12 (clase D) | El verificador publicado ejecuta pruebas estructurales en memoria, no búsquedas de texto: K45 evalúa 15 controles (C01 a C15) sobre un modelo relacional con identidad propia y contrasta la matriz de correspondencias de 4.4.10 con los nombres físicos; K46 reconstruye la cadena y comprueba la independencia del resolutor (R1 a R9); K32, K44, K45 y K55 comprueba… |
| Ejecución K47-M01 | sustituir_campo retira automáticamente la atribución anterior → invariante esperado I1 → DETECTADA (detectada por I1, I15 · «una atribución activa anterior no sigue activa en la versión nueva: [('A', 'copy', 'headline', 'e1')]») |
| Resultado de esta revisión | **PASS (MODELO_EN_MEMORIA)** |
| Brecha | Sin ejecución en el esquema físico: la «tabla de efectos» (4.4.10) y las reglas IG5-97 no tienen aún función/trigger SQL que probar. |
| Procedimiento CCI-DEV (NO EJECUTADO) | Cuando existan las funciones de atribución, repetir la alteración equivalente sobre el esquema físico (`PLAN_VALIDACION_CCI_DEV.md`, bloque ATR) y confirmar que se rechaza; mientras no existan es BLOQUEADO_POR_IMPLEMENTACIÓN. |

## T-410 — H-02 v8 conservación: eliminación de campo elimina automáticamente la atribución

| Campo | Contenido |
|---|---|
| Línea en la especificación | 4131 |
| Texto del escenario | `¦ T-410 ¦ H-02 v8 conservación: eliminación de campo elimina automáticamente la atribución ¦ Tabla de efectos válida ¦ Cambiar a eliminado el efecto a retirada automática ¦ Rechazo (K47) ¦ Retirar por eliminar ¦ Resultado esperado cumplido y ninguno prohibido ¦ Diseño ¦ IG5-97, IE-12 ¦` |
| Reglas | IG5-97, IE-12 |
| Veredicto V26 (sin alterar) | DEMUESTRA (lectura V20) |
| Revisión estática | Precondición «tabla de efectos válida»; la alteración y el resultado prohibido son coherentes con la regla IG5-97 (efectos estructurales por clasificación y fuente). |
| Regla IG5-97 (clase D) | Efectos estructurales por clasificación y fuente: brief, promoción y copy siguen exactamente la misma tabla. sin_cambio conserva todas las atribuciones activas y no crea contribuyentes; introducido incorpora al actor; modificado conserva todas las activas e incorpora al editor; sustituido conserva provisionalmente todas las activas e incorpora al sustituidor… |
| Regla IE-12 (clase D) | El verificador publicado ejecuta pruebas estructurales en memoria, no búsquedas de texto: K45 evalúa 15 controles (C01 a C15) sobre un modelo relacional con identidad propia y contrasta la matriz de correspondencias de 4.4.10 con los nombres físicos; K46 reconstruye la cadena y comprueba la independencia del resolutor (R1 a R9); K32, K44, K45 y K55 comprueba… |
| Ejecución K47-M02 | eliminar_campo retira automáticamente la atribución anterior → invariante esperado I1 → DETECTADA (detectada por I1, I15 · «una atribución activa anterior no sigue activa en la versión nueva: [('A', 'copy', 'headline', 'e1')]») |
| Resultado de esta revisión | **PASS (MODELO_EN_MEMORIA)** |
| Brecha | Sin ejecución en el esquema físico: la «tabla de efectos» (4.4.10) y las reglas IG5-97 no tienen aún función/trigger SQL que probar. |
| Procedimiento CCI-DEV (NO EJECUTADO) | Cuando existan las funciones de atribución, repetir la alteración equivalente sobre el esquema físico (`PLAN_VALIDACION_CCI_DEV.md`, bloque ATR) y confirmar que se rechaza; mientras no existan es BLOQUEADO_POR_IMPLEMENTACIÓN. |

## T-411 — H-02 v8 conservación: modificación material pierde una atribución previa

| Campo | Contenido |
|---|---|
| Línea en la especificación | 4132 |
| Texto del escenario | `¦ T-411 ¦ H-02 v8 conservación: modificación material pierde una atribución previa ¦ Tabla de efectos válida ¦ Cambiar modificado a no conservar las anteriores ¦ Rechazo (K47) ¦ Perder atribuciones ¦ Resultado esperado cumplido y ninguno prohibido ¦ Diseño ¦ IG5-97, IE-12 ¦` |
| Reglas | IG5-97, IE-12 |
| Veredicto V26 (sin alterar) | DEMUESTRA (lectura V20) |
| Revisión estática | Precondición «tabla de efectos válida»; la alteración y el resultado prohibido son coherentes con la regla IG5-97 (efectos estructurales por clasificación y fuente). |
| Regla IG5-97 (clase D) | Efectos estructurales por clasificación y fuente: brief, promoción y copy siguen exactamente la misma tabla. sin_cambio conserva todas las atribuciones activas y no crea contribuyentes; introducido incorpora al actor; modificado conserva todas las activas e incorpora al editor; sustituido conserva provisionalmente todas las activas e incorpora al sustituidor… |
| Regla IE-12 (clase D) | El verificador publicado ejecuta pruebas estructurales en memoria, no búsquedas de texto: K45 evalúa 15 controles (C01 a C15) sobre un modelo relacional con identidad propia y contrasta la matriz de correspondencias de 4.4.10 con los nombres físicos; K46 reconstruye la cadena y comprueba la independencia del resolutor (R1 a R9); K32, K44, K45 y K55 comprueba… |
| Ejecución K47-M03 | modificar_campo pierde una atribución previa → invariante esperado I1 → DETECTADA (detectada por I1, I15 · «una atribución activa anterior no sigue activa en la versión nueva: [('A', 'copy', 'headline', 'e1')]») |
| Resultado de esta revisión | **PASS (MODELO_EN_MEMORIA)** |
| Brecha | Sin ejecución en el esquema físico: la «tabla de efectos» (4.4.10) y las reglas IG5-97 no tienen aún función/trigger SQL que probar. |
| Procedimiento CCI-DEV (NO EJECUTADO) | Cuando existan las funciones de atribución, repetir la alteración equivalente sobre el esquema físico (`PLAN_VALIDACION_CCI_DEV.md`, bloque ATR) y confirmar que se rechaza; mientras no existan es BLOQUEADO_POR_IMPLEMENTACIÓN. |

## T-412 — H-02 v8 conservación: introducción no incorpora al actor

| Campo | Contenido |
|---|---|
| Línea en la especificación | 4133 |
| Texto del escenario | `¦ T-412 ¦ H-02 v8 conservación: introducción no incorpora al actor ¦ Tabla de efectos válida ¦ Cambiar introducido a no incorporar ¦ Rechazo (K47) ¦ Omitir al actor ¦ Resultado esperado cumplido y ninguno prohibido ¦ Diseño ¦ IG5-97, IE-12 ¦` |
| Reglas | IG5-97, IE-12 |
| Veredicto V26 (sin alterar) | DEMUESTRA (lectura V20) |
| Revisión estática | Precondición «tabla de efectos válida»; la alteración y el resultado prohibido son coherentes con la regla IG5-97 (efectos estructurales por clasificación y fuente). |
| Regla IG5-97 (clase D) | Efectos estructurales por clasificación y fuente: brief, promoción y copy siguen exactamente la misma tabla. sin_cambio conserva todas las atribuciones activas y no crea contribuyentes; introducido incorpora al actor; modificado conserva todas las activas e incorpora al editor; sustituido conserva provisionalmente todas las activas e incorpora al sustituidor… |
| Regla IE-12 (clase D) | El verificador publicado ejecuta pruebas estructurales en memoria, no búsquedas de texto: K45 evalúa 15 controles (C01 a C15) sobre un modelo relacional con identidad propia y contrasta la matriz de correspondencias de 4.4.10 con los nombres físicos; K46 reconstruye la cadena y comprueba la independencia del resolutor (R1 a R9); K32, K44, K45 y K55 comprueba… |
| Ejecución K47-M04 | introducir_campo no incorpora al actor → invariante esperado I2 → DETECTADA (detectada por I2 · «el actor no se incorporó») |
| Resultado de esta revisión | **PASS (MODELO_EN_MEMORIA)** |
| Brecha | Sin ejecución en el esquema físico: la «tabla de efectos» (4.4.10) y las reglas IG5-97 no tienen aún función/trigger SQL que probar. |
| Procedimiento CCI-DEV (NO EJECUTADO) | Cuando existan las funciones de atribución, repetir la alteración equivalente sobre el esquema físico (`PLAN_VALIDACION_CCI_DEV.md`, bloque ATR) y confirmar que se rechaza; mientras no existan es BLOQUEADO_POR_IMPLEMENTACIÓN. |

## T-413 — H-02 v8 conservación: resolución rechazada modifica E

| Campo | Contenido |
|---|---|
| Línea en la especificación | 4134 |
| Texto del escenario | `¦ T-413 ¦ H-02 v8 conservación: resolución rechazada modifica E ¦ Tabla de efectos válida ¦ Hacer que la resolución rechazada saque a la persona de E ¦ Rechazo (K47) ¦ Cambiar E sin resolución válida ¦ Resultado esperado cumplido y ninguno prohibido ¦ Diseño ¦ IG5-97, IG5-93, IE-12 ¦` |
| Reglas | IG5-97, IG5-93, IE-12 |
| Veredicto V26 (sin alterar) | DEMUESTRA (lectura V20) |
| Revisión estática | Precondición «tabla de efectos válida»; la alteración y el resultado prohibido son coherentes con la regla IG5-97 (efectos estructurales por clasificación y fuente). |
| Regla IG5-97 (clase D) | Efectos estructurales por clasificación y fuente: brief, promoción y copy siguen exactamente la misma tabla. sin_cambio conserva todas las atribuciones activas y no crea contribuyentes; introducido incorpora al actor; modificado conserva todas las activas e incorpora al editor; sustituido conserva provisionalmente todas las activas e incorpora al sustituidor… |
| Regla IG5-93 (clase C) | Efecto y límites de la resolución: es un registro nuevo e inmutable que no reescribe registros históricos y deja la atribución original como evidencia; sin evidencia suficiente, con actor no elegible, duplicada (una sola resolución aceptada por atribución), sobre una versión distinta de la de la atribución referenciada o incompleta, la resolución se rechaza … |
| Regla IE-12 (clase D) | El verificador publicado ejecuta pruebas estructurales en memoria, no búsquedas de texto: K45 evalúa 15 controles (C01 a C15) sobre un modelo relacional con identidad propia y contrasta la matriz de correspondencias de 4.4.10 con los nombres físicos; K46 reconstruye la cadena y comprueba la independencia del resolutor (R1 a R9); K32, K44, K45 y K55 comprueba… |
| Ejecución K47-M05 | el cálculo de E excluye a la persona afectada por una resolución rechazada → invariante esperado I5 → DETECTADA (detectada por I5, I7 · «una resolución rechazada o inválida modificó atribuciones o E») |
| Ejecución K47-M18 | una resolución rechazada cambia el estado de una atribución → invariante esperado I5 → DETECTADA (detectada por I15, I5 · «una resolución rechazada o inválida modificó atribuciones o E») |
| Ejecución K47-M19 | una resolución con evidencia de otra versión modifica E → invariante esperado I5 → DETECTADA (detectada por I4, I5 · «una resolución rechazada o inválida modificó atribuciones o E») |
| Resultado de esta revisión | **PASS (MODELO_EN_MEMORIA)** |
| Brecha | Sin ejecución en el esquema físico: la «tabla de efectos» (4.4.10) y las reglas IG5-97 no tienen aún función/trigger SQL que probar. |
| Procedimiento CCI-DEV (NO EJECUTADO) | Cuando existan las funciones de atribución, repetir la alteración equivalente sobre el esquema físico (`PLAN_VALIDACION_CCI_DEV.md`, bloque ATR) y confirmar que se rechaza; mientras no existan es BLOQUEADO_POR_IMPLEMENTACIÓN. |

## T-414 — H-02 v8 conservación: resolución aceptada elimina otra atribución distinta

| Campo | Contenido |
|---|---|
| Línea en la especificación | 4135 |
| Texto del escenario | `¦ T-414 ¦ H-02 v8 conservación: resolución aceptada elimina otra atribución distinta ¦ Tabla de efectos válida ¦ Hacer que la resolución afecte todas las atribuciones del campo ¦ Rechazo (K47) ¦ Alcance mayor que la atribución referenciada ¦ Resultado esperado cumplido y ninguno prohibido ¦ Diseño ¦ IG5-97, IG5-93, IE-12 ¦` |
| Reglas | IG5-97, IG5-93, IE-12 |
| Veredicto V26 (sin alterar) | DEMUESTRA (lectura V20) |
| Revisión estática | Precondición «tabla de efectos válida»; la alteración y el resultado prohibido son coherentes con la regla IG5-97 (efectos estructurales por clasificación y fuente). |
| Regla IG5-97 (clase D) | Efectos estructurales por clasificación y fuente: brief, promoción y copy siguen exactamente la misma tabla. sin_cambio conserva todas las atribuciones activas y no crea contribuyentes; introducido incorpora al actor; modificado conserva todas las activas e incorpora al editor; sustituido conserva provisionalmente todas las activas e incorpora al sustituidor… |
| Regla IG5-93 (clase C) | Efecto y límites de la resolución: es un registro nuevo e inmutable que no reescribe registros históricos y deja la atribución original como evidencia; sin evidencia suficiente, con actor no elegible, duplicada (una sola resolución aceptada por atribución), sobre una versión distinta de la de la atribución referenciada o incompleta, la resolución se rechaza … |
| Regla IE-12 (clase D) | El verificador publicado ejecuta pruebas estructurales en memoria, no búsquedas de texto: K45 evalúa 15 controles (C01 a C15) sobre un modelo relacional con identidad propia y contrasta la matriz de correspondencias de 4.4.10 con los nombres físicos; K46 reconstruye la cadena y comprueba la independencia del resolutor (R1 a R9); K32, K44, K45 y K55 comprueba… |
| Ejecución K47-M06 | la resolución aceptada retira otra atribución distinta → invariante esperado I3 → DETECTADA (detectada por I15, I3, I7 · «la resolución retiró ['t3', 't5'] en lugar de solo la referenciada») |
| Ejecución K47-M17 | resolver una atribución retira todas las atribuciones de la persona → invariante esperado I3 → DETECTADA (detectada por I15, I3, I7 · «la resolución retiró ['t2', 't3', 't5'] en lugar de solo la referenciada») |
| Ejecución K47-M24 | la resolución retira un campo distinto del que declara → invariante esperado I3 → DETECTADA (detectada por I15, I3, I6 · «la resolución retiró ['t7'] en lugar de solo la referenciada») |
| Resultado de esta revisión | **PASS (MODELO_EN_MEMORIA)** |
| Brecha | Sin ejecución en el esquema físico: la «tabla de efectos» (4.4.10) y las reglas IG5-97 no tienen aún función/trigger SQL que probar. |
| Procedimiento CCI-DEV (NO EJECUTADO) | Cuando existan las funciones de atribución, repetir la alteración equivalente sobre el esquema físico (`PLAN_VALIDACION_CCI_DEV.md`, bloque ATR) y confirmar que se rechaza; mientras no existan es BLOQUEADO_POR_IMPLEMENTACIÓN. |

## T-415 — H-02 v8 conservación: resolución altera una versión histórica

| Campo | Contenido |
|---|---|
| Línea en la especificación | 4136 |
| Texto del escenario | `¦ T-415 ¦ H-02 v8 conservación: resolución altera una versión histórica ¦ Tabla de efectos válida ¦ Hacer que la resolución reescriba versiones anteriores ¦ Rechazo (K47) ¦ Reescribir historia ¦ Resultado esperado cumplido y ninguno prohibido ¦ Diseño ¦ IG5-97, IG5-87, IE-12 ¦` |
| Reglas | IG5-97, IG5-87, IE-12 |
| Veredicto V26 (sin alterar) | DEMUESTRA (lectura V20) |
| Revisión estática | Precondición «tabla de efectos válida»; la alteración y el resultado prohibido son coherentes con la regla IG5-97 (efectos estructurales por clasificación y fuente). |
| Regla IG5-97 (clase D) | Efectos estructurales por clasificación y fuente: brief, promoción y copy siguen exactamente la misma tabla. sin_cambio conserva todas las atribuciones activas y no crea contribuyentes; introducido incorpora al actor; modificado conserva todas las activas e incorpora al editor; sustituido conserva provisionalmente todas las activas e incorpora al sustituidor… |
| Regla IG5-87 (clase D) | Las correcciones de contribuciones y de procedencia producen registros nuevos: un evento se corrige con otro evento con previous_event_id, una exclusión es una resolución nueva en attribution_discard_resolutions que no modifica la atribución original, una atribución histórica no se reactiva; el actor de un evento no puede cambiarse ni los eventos eliminarse;… |
| Regla IE-12 (clase D) | El verificador publicado ejecuta pruebas estructurales en memoria, no búsquedas de texto: K45 evalúa 15 controles (C01 a C15) sobre un modelo relacional con identidad propia y contrasta la matriz de correspondencias de 4.4.10 con los nombres físicos; K46 reconstruye la cadena y comprueba la independencia del resolutor (R1 a R9); K32, K44, K45 y K55 comprueba… |
| Ejecución K47-M07 | la resolución aceptada altera una versión histórica → invariante esperado I10 → DETECTADA (detectada por I10 · «una versión, atribución, evento o estado anterior fue modificado o eliminado») |
| Ejecución K47-M26 | la resolución válida reescribe un registro anterior en lugar de agregar uno nuevo → invariante esperado I10 → DETECTADA (detectada por I10 · «una versión, atribución, evento o estado anterior fue modificado o eliminado») |
| Resultado de esta revisión | **PASS (MODELO_EN_MEMORIA)** |
| Brecha | Sin ejecución en el esquema físico: la «tabla de efectos» (4.4.10) y las reglas IG5-97 no tienen aún función/trigger SQL que probar. |
| Procedimiento CCI-DEV (NO EJECUTADO) | Cuando existan las funciones de atribución, repetir la alteración equivalente sobre el esquema físico (`PLAN_VALIDACION_CCI_DEV.md`, bloque ATR) y confirmar que se rechaza; mientras no existan es BLOQUEADO_POR_IMPLEMENTACIÓN. |

## T-416 — H-02 v8 conservación: atribución heredada desaparece al crear una versión

| Campo | Contenido |
|---|---|
| Línea en la especificación | 4137 |
| Texto del escenario | `¦ T-416 ¦ H-02 v8 conservación: atribución heredada desaparece al crear una versión ¦ Tabla de efectos válida ¦ Hacer que la versión nueva no herede ¦ Rechazo (K47) ¦ Perder herencia ¦ Resultado esperado cumplido y ninguno prohibido ¦ Diseño ¦ IG5-97, IG5-72, IE-12 ¦` |
| Reglas | IG5-97, IG5-72, IE-12 |
| Veredicto V26 (sin alterar) | DEMUESTRA (lectura V20) |
| Revisión estática | Precondición «tabla de efectos válida»; la alteración y el resultado prohibido son coherentes con la regla IG5-97 (efectos estructurales por clasificación y fuente). |
| Regla IG5-97 (clase D) | Efectos estructurales por clasificación y fuente: brief, promoción y copy siguen exactamente la misma tabla. sin_cambio conserva todas las atribuciones activas y no crea contribuyentes; introducido incorpora al actor; modificado conserva todas las activas e incorpora al editor; sustituido conserva provisionalmente todas las activas e incorpora al sustituidor… |
| Regla IG5-72 (clase B) | Propagación de atribuciones por campo de V_n-1 a V_n: (A) sin_cambio: se conservan y propagan todas las atribuciones con su condición activa o histórica y no se crea ningún contribuyente nuevo; (B) introducido: una atribución directa activa para quien introdujo el campo y ningún contribuyente anterior inventado; (C) modificado: se conservan todas las atribuc… |
| Regla IE-12 (clase D) | El verificador publicado ejecuta pruebas estructurales en memoria, no búsquedas de texto: K45 evalúa 15 controles (C01 a C15) sobre un modelo relacional con identidad propia y contrasta la matriz de correspondencias de 4.4.10 con los nombres físicos; K46 reconstruye la cadena y comprueba la independencia del resolutor (R1 a R9); K32, K44, K45 y K55 comprueba… |
| Ejecución K47-M08 | crear_version omite una atribución heredada → invariante esperado I10 → DETECTADA (detectada por I1, I10 · «la versión nueva no hereda todas las atribuciones activas») |
| Ejecución K47-M20 | crear_version omite una atribución heredada de segunda generación → invariante esperado I10 → DETECTADA (detectada por I1, I10 · «la versión nueva no hereda todas las atribuciones activas») |
| Resultado de esta revisión | **PASS (MODELO_EN_MEMORIA)** |
| Brecha | Sin ejecución en el esquema físico: la «tabla de efectos» (4.4.10) y las reglas IG5-97 no tienen aún función/trigger SQL que probar. |
| Procedimiento CCI-DEV (NO EJECUTADO) | Cuando existan las funciones de atribución, repetir la alteración equivalente sobre el esquema físico (`PLAN_VALIDACION_CCI_DEV.md`, bloque ATR) y confirmar que se rechaza; mientras no existan es BLOQUEADO_POR_IMPLEMENTACIÓN. |

## T-417 — H-02 v8 conservación: procedencia incompleta presentada como completa

| Campo | Contenido |
|---|---|
| Línea en la especificación | 4138 |
| Texto del escenario | `¦ T-417 ¦ H-02 v8 conservación: procedencia incompleta presentada como completa ¦ Tabla de efectos válida ¦ Hacer que una cadena incompleta produzca un E parcial ¦ Rechazo (K47) ¦ E parcial como completo ¦ Resultado esperado cumplido y ninguno prohibido ¦ Diseño ¦ IG5-97, IG5-94, IE-12 ¦` |
| Reglas | IG5-97, IG5-94, IE-12 |
| Veredicto V26 (sin alterar) | DEMUESTRA (lectura V20) |
| Revisión estática | Precondición «tabla de efectos válida»; la alteración y el resultado prohibido son coherentes con la regla IG5-97 (efectos estructurales por clasificación y fuente). |
| Regla IG5-97 (clase D) | Efectos estructurales por clasificación y fuente: brief, promoción y copy siguen exactamente la misma tabla. sin_cambio conserva todas las atribuciones activas y no crea contribuyentes; introducido incorpora al actor; modificado conserva todas las activas e incorpora al editor; sustituido conserva provisionalmente todas las activas e incorpora al sustituidor… |
| Regla IG5-94 (clase C) | El conjunto E incorpora los contribuyentes directos de la versión exacta de adaptación, los heredados activos, los de la versión exacta de la maestra y de las versiones intermedias del intervalo definido, los de briefs y promociones exactos incluidos los heredados activos por campo, los de los assets exactos usados y el proponente de la clasificación de inde… |
| Regla IE-12 (clase D) | El verificador publicado ejecuta pruebas estructurales en memoria, no búsquedas de texto: K45 evalúa 15 controles (C01 a C15) sobre un modelo relacional con identidad propia y contrasta la matriz de correspondencias de 4.4.10 con los nombres físicos; K46 reconstruye la cadena y comprueba la independencia del resolutor (R1 a R9); K32, K44, K45 y K55 comprueba… |
| Ejecución K47-M09 | una cadena de copy incompleta se presenta como completa → invariante esperado I8 → DETECTADA (detectada por I20, I8 · «procedencia incompleta presentada como completa o con E parcial») |
| Ejecución K47-M22 | la cadena de brief está incompleta pero E aparece como completo → invariante esperado I8 → DETECTADA (detectada por I8 · «procedencia incompleta presentada como completa o con E parcial») |
| Ejecución K47-M23 | la cadena de promoción está incompleta pero E aparece como completo → invariante esperado I8 → DETECTADA (detectada por I8 · «procedencia incompleta presentada como completa o con E parcial») |
| Resultado de esta revisión | **PASS (MODELO_EN_MEMORIA)** |
| Brecha | Sin ejecución en el esquema físico: la «tabla de efectos» (4.4.10) y las reglas IG5-97 no tienen aún función/trigger SQL que probar. |
| Procedimiento CCI-DEV (NO EJECUTADO) | Cuando existan las funciones de atribución, repetir la alteración equivalente sobre el esquema físico (`PLAN_VALIDACION_CCI_DEV.md`, bloque ATR) y confirmar que se rechaza; mientras no existan es BLOQUEADO_POR_IMPLEMENTACIÓN. |

## T-418 — H-02 v8 conservación: resolución válida elimina de E a quien conserva otra contribución activa

| Campo | Contenido |
|---|---|
| Línea en la especificación | 4139 |
| Texto del escenario | `¦ T-418 ¦ H-02 v8 conservación: resolución válida elimina de E a quien conserva otra contribución activa ¦ Tabla de efectos válida ¦ Hacer que la resolución saque siempre a la persona de E ¦ Rechazo (K47) ¦ Perder a un contribuyente real ¦ Resultado esperado cumplido y ninguno prohibido ¦ Diseño ¦ IG5-97, IG5-94, IE-12 ¦` |
| Reglas | IG5-97, IG5-94, IE-12 |
| Veredicto V26 (sin alterar) | DEMUESTRA (lectura V20) |
| Revisión estática | Precondición «tabla de efectos válida»; la alteración y el resultado prohibido son coherentes con la regla IG5-97 (efectos estructurales por clasificación y fuente). |
| Regla IG5-97 (clase D) | Efectos estructurales por clasificación y fuente: brief, promoción y copy siguen exactamente la misma tabla. sin_cambio conserva todas las atribuciones activas y no crea contribuyentes; introducido incorpora al actor; modificado conserva todas las activas e incorpora al editor; sustituido conserva provisionalmente todas las activas e incorpora al sustituidor… |
| Regla IG5-94 (clase C) | El conjunto E incorpora los contribuyentes directos de la versión exacta de adaptación, los heredados activos, los de la versión exacta de la maestra y de las versiones intermedias del intervalo definido, los de briefs y promociones exactos incluidos los heredados activos por campo, los de los assets exactos usados y el proponente de la clasificación de inde… |
| Regla IE-12 (clase D) | El verificador publicado ejecuta pruebas estructurales en memoria, no búsquedas de texto: K45 evalúa 15 controles (C01 a C15) sobre un modelo relacional con identidad propia y contrasta la matriz de correspondencias de 4.4.10 con los nombres físicos; K46 reconstruye la cadena y comprueba la independencia del resolutor (R1 a R9); K32, K44, K45 y K55 comprueba… |
| Ejecución K47-M10 | una resolución válida elimina de E a quien conserva otra atribución activa → invariante esperado I7 → DETECTADA (detectada por I7 · «E del motor distinto del E recalculado sobre las atribuciones reales») |
| Ejecución K47-M15 | resolución válida retira a quien conserva otra atribución activa en otro campo → invariante esperado I7 → DETECTADA (detectada por I15, I3, I7 · «salió de E una persona que conserva otra atribución activa») |
| Ejecución K47-M16 | resolución válida retira a quien conserva una contribución activa en otra fuente → invariante esperado I7 → DETECTADA (detectada por I15, I3, I7 · «salió de E una persona que conserva otra atribución activa») |
| Ejecución K47-M25 | quien contribuye a dos fuentes sale de E al resolver solo una → invariante esperado I7 → DETECTADA (detectada por I7 · «E del motor distinto del E recalculado sobre las atribuciones reales») |
| Resultado de esta revisión | **PASS (MODELO_EN_MEMORIA)** |
| Brecha | Sin ejecución en el esquema físico: la «tabla de efectos» (4.4.10) y las reglas IG5-97 no tienen aún función/trigger SQL que probar. |
| Procedimiento CCI-DEV (NO EJECUTADO) | Cuando existan las funciones de atribución, repetir la alteración equivalente sobre el esquema físico (`PLAN_VALIDACION_CCI_DEV.md`, bloque ATR) y confirmar que se rechaza; mientras no existan es BLOQUEADO_POR_IMPLEMENTACIÓN. |

## T-419 — H-02 v8 conservación: lógica de sustitución distinta entre copy y brief

| Campo | Contenido |
|---|---|
| Línea en la especificación | 4140 |
| Texto del escenario | `¦ T-419 ¦ H-02 v8 conservación: lógica de sustitución distinta entre copy y brief ¦ Tabla de efectos válida ¦ Cambiar solo la fila sustituido de copy ¦ Rechazo (K47) ¦ Reglas por fuente ¦ Resultado esperado cumplido y ninguno prohibido ¦ Diseño ¦ IG5-97, IE-12 ¦` |
| Reglas | IG5-97, IE-12 |
| Veredicto V26 (sin alterar) | DEMUESTRA (lectura V20) |
| Revisión estática | Precondición «tabla de efectos válida»; la alteración y el resultado prohibido son coherentes con la regla IG5-97 (efectos estructurales por clasificación y fuente). |
| Regla IG5-97 (clase D) | Efectos estructurales por clasificación y fuente: brief, promoción y copy siguen exactamente la misma tabla. sin_cambio conserva todas las atribuciones activas y no crea contribuyentes; introducido incorpora al actor; modificado conserva todas las activas e incorpora al editor; sustituido conserva provisionalmente todas las activas e incorpora al sustituidor… |
| Regla IE-12 (clase D) | El verificador publicado ejecuta pruebas estructurales en memoria, no búsquedas de texto: K45 evalúa 15 controles (C01 a C15) sobre un modelo relacional con identidad propia y contrasta la matriz de correspondencias de 4.4.10 con los nombres físicos; K46 reconstruye la cadena y comprueba la independencia del resolutor (R1 a R9); K32, K44, K45 y K55 comprueba… |
| Ejecución K47-M11 | la sustitución difiere entre copy y brief → invariante esperado I9 → DETECTADA (detectada por I9 · «las fuentes no aplican la misma regla») |
| Resultado de esta revisión | **PASS (MODELO_EN_MEMORIA)** |
| Brecha | Sin ejecución en el esquema físico: la «tabla de efectos» (4.4.10) y las reglas IG5-97 no tienen aún función/trigger SQL que probar. |
| Procedimiento CCI-DEV (NO EJECUTADO) | Cuando existan las funciones de atribución, repetir la alteración equivalente sobre el esquema físico (`PLAN_VALIDACION_CCI_DEV.md`, bloque ATR) y confirmar que se rechaza; mientras no existan es BLOQUEADO_POR_IMPLEMENTACIÓN. |

## T-420 — H-02 v8 conservación: lógica de eliminación distinta entre brief y promoción

| Campo | Contenido |
|---|---|
| Línea en la especificación | 4141 |
| Texto del escenario | `¦ T-420 ¦ H-02 v8 conservación: lógica de eliminación distinta entre brief y promoción ¦ Tabla de efectos válida ¦ Cambiar solo la fila eliminado de promoción ¦ Rechazo (K47) ¦ Reglas por fuente ¦ Resultado esperado cumplido y ninguno prohibido ¦ Diseño ¦ IG5-97, IE-12 ¦` |
| Reglas | IG5-97, IE-12 |
| Veredicto V26 (sin alterar) | DEMUESTRA (lectura V20) |
| Revisión estática | Precondición «tabla de efectos válida»; la alteración y el resultado prohibido son coherentes con la regla IG5-97 (efectos estructurales por clasificación y fuente). |
| Regla IG5-97 (clase D) | Efectos estructurales por clasificación y fuente: brief, promoción y copy siguen exactamente la misma tabla. sin_cambio conserva todas las atribuciones activas y no crea contribuyentes; introducido incorpora al actor; modificado conserva todas las activas e incorpora al editor; sustituido conserva provisionalmente todas las activas e incorpora al sustituidor… |
| Regla IE-12 (clase D) | El verificador publicado ejecuta pruebas estructurales en memoria, no búsquedas de texto: K45 evalúa 15 controles (C01 a C15) sobre un modelo relacional con identidad propia y contrasta la matriz de correspondencias de 4.4.10 con los nombres físicos; K46 reconstruye la cadena y comprueba la independencia del resolutor (R1 a R9); K32, K44, K45 y K55 comprueba… |
| Ejecución K47-M12 | la eliminación difiere entre brief y promoción → invariante esperado I9 → DETECTADA (detectada por I9 · «las fuentes no aplican la misma regla») |
| Resultado de esta revisión | **PASS (MODELO_EN_MEMORIA)** |
| Brecha | Sin ejecución en el esquema físico: la «tabla de efectos» (4.4.10) y las reglas IG5-97 no tienen aún función/trigger SQL que probar. |
| Procedimiento CCI-DEV (NO EJECUTADO) | Cuando existan las funciones de atribución, repetir la alteración equivalente sobre el esquema físico (`PLAN_VALIDACION_CCI_DEV.md`, bloque ATR) y confirmar que se rechaza; mientras no existan es BLOQUEADO_POR_IMPLEMENTACIÓN. |

## T-421 — H-02 v8 conservación: la similitud textual decide por sí sola el descarte

| Campo | Contenido |
|---|---|
| Línea en la especificación | 4142 |
| Texto del escenario | `¦ T-421 ¦ H-02 v8 conservación: la similitud textual decide por sí sola el descarte ¦ Tabla de efectos válida ¦ Activar la decisión por similitud en una fila ¦ Rechazo (K47) ¦ Descartar por similitud ¦ Resultado esperado cumplido y ninguno prohibido ¦ Diseño ¦ IG5-97, IG5-43, IE-12 ¦` |
| Reglas | IG5-97, IG5-43, IE-12 |
| Veredicto V26 (sin alterar) | DEMUESTRA (lectura V20) |
| Revisión estática | Precondición «tabla de efectos válida»; la alteración y el resultado prohibido son coherentes con la regla IG5-97 (efectos estructurales por clasificación y fuente). |
| Regla IG5-97 (clase D) | Efectos estructurales por clasificación y fuente: brief, promoción y copy siguen exactamente la misma tabla. sin_cambio conserva todas las atribuciones activas y no crea contribuyentes; introducido incorpora al actor; modificado conserva todas las activas e incorpora al editor; sustituido conserva provisionalmente todas las activas e incorpora al sustituidor… |
| Regla IG5-43 (clase C) | En duda sobre si una aportación anterior continúa presente en una versión posterior se conserva la atribución (PO-16): la procedencia se decide por contenido y por referencias exactas, nunca por porcentajes de similitud, embeddings ni puntuaciones semánticas, y la IA no la decide |
| Regla IE-12 (clase D) | El verificador publicado ejecuta pruebas estructurales en memoria, no búsquedas de texto: K45 evalúa 15 controles (C01 a C15) sobre un modelo relacional con identidad propia y contrasta la matriz de correspondencias de 4.4.10 con los nombres físicos; K46 reconstruye la cadena y comprueba la independencia del resolutor (R1 a R9); K32, K44, K45 y K55 comprueba… |
| Ejecución K47-M13 | la similitud textual determina el descarte → invariante esperado I11 → DETECTADA (detectada por I11 · «el resultado sobre las atribuciones depende de la similitud del texto») |
| Resultado de esta revisión | **PASS (MODELO_EN_MEMORIA)** |
| Brecha | Sin ejecución en el esquema físico: la «tabla de efectos» (4.4.10) y las reglas IG5-97 no tienen aún función/trigger SQL que probar. |
| Procedimiento CCI-DEV (NO EJECUTADO) | Cuando existan las funciones de atribución, repetir la alteración equivalente sobre el esquema físico (`PLAN_VALIDACION_CCI_DEV.md`, bloque ATR) y confirmar que se rechaza; mientras no existan es BLOQUEADO_POR_IMPLEMENTACIÓN. |

## T-422 — H-02 v8 conservación: un cambio de clasificación elimina atribuciones sin resolución

| Campo | Contenido |
|---|---|
| Línea en la especificación | 4143 |
| Texto del escenario | `¦ T-422 ¦ H-02 v8 conservación: un cambio de clasificación elimina atribuciones sin resolución ¦ Tabla de efectos válida ¦ Hacer que reclasificar retire atribuciones ¦ Rechazo (K47) ¦ Retirar por reclasificar ¦ Resultado esperado cumplido y ninguno prohibido ¦ Diseño ¦ IG5-97, IG5-91, IE-12 ¦` |
| Reglas | IG5-97, IG5-91, IE-12 |
| Veredicto V26 (sin alterar) | DEMUESTRA (lectura V20) |
| Revisión estática | Precondición «tabla de efectos válida»; la alteración y el resultado prohibido son coherentes con la regla IG5-97 (efectos estructurales por clasificación y fuente). |
| Regla IG5-97 (clase D) | Efectos estructurales por clasificación y fuente: brief, promoción y copy siguen exactamente la misma tabla. sin_cambio conserva todas las atribuciones activas y no crea contribuyentes; introducido incorpora al actor; modificado conserva todas las activas e incorpora al editor; sustituido conserva provisionalmente todas las activas e incorpora al sustituidor… |
| Regla IG5-91 (clase D) | La clasificación técnica del cambio (sin_cambio, introducido, modificado, sustituido, eliminado) y el estado de la atribución de los contribuyentes anteriores son conceptos separados: la clasificación sustituido no permite excluir automáticamente a los contribuyentes anteriores y la clasificación eliminado no autoriza a borrar la historia de atribución; ning… |
| Regla IE-12 (clase D) | El verificador publicado ejecuta pruebas estructurales en memoria, no búsquedas de texto: K45 evalúa 15 controles (C01 a C15) sobre un modelo relacional con identidad propia y contrasta la matriz de correspondencias de 4.4.10 con los nombres físicos; K46 reconstruye la cadena y comprueba la independencia del resolutor (R1 a R9); K32, K44, K45 y K55 comprueba… |
| Ejecución K47-M14 | cambiar la clasificación retira atribuciones sin resolución → invariante esperado I12 → DETECTADA (detectada por I12, I15 · «el cambio de clasificación alteró atribuciones o estados») |
| Resultado de esta revisión | **PASS (MODELO_EN_MEMORIA)** |
| Brecha | Sin ejecución en el esquema físico: la «tabla de efectos» (4.4.10) y las reglas IG5-97 no tienen aún función/trigger SQL que probar. |
| Procedimiento CCI-DEV (NO EJECUTADO) | Cuando existan las funciones de atribución, repetir la alteración equivalente sobre el esquema físico (`PLAN_VALIDACION_CCI_DEV.md`, bloque ATR) y confirmar que se rechaza; mientras no existan es BLOQUEADO_POR_IMPLEMENTACIÓN. |

## Limitaciones comunes
- Un único cambio por mutación y estado inicial válido (garantizado por `_correr_lista`): evita falsos positivos de detección por estado roto.
- La detección exige el invariante específico **y** su mensaje (`kw in v[1]`): sensible a cambios de redacción en los mensajes del modelo.
- Equivalencia modelo/físico no demostrada (ver `REVISION_22_FUNCIONES.md` y `MATRIZ_MODELO_LOGICO_FISICO.md`).
