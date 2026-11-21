# REVISIÓN LÍNEA A LÍNEA DE LAS 22 FUNCIONES DE EJECUCIÓN

**Fuente inspeccionada (sin modificar):** `docs/fase0/herramientas/modelo_estructural.py` (SHA-256 `cc87236a…`). **Método:** (1) lectura de cada función y de sus ayudantes críticos (`_correr_lista`, `_correr15`, `pruebas_E14`, `pruebas_guarda`, `correr_mutaciones_rechazo`, `pruebas_atomicidad`, `correr_adversariales_cadena`); (2) análisis estático automatizado por AST (`scripts_validacion/ct_inspeccion_22_funciones.py`: líneas, argumentos, dependencias, bloques try, `except` amplios, escrituras globales, uso de deepcopy); (3) ejecución local de las mutaciones K47 por escenario (`ct_k47_por_escenario.py`).

**Etiquetas usadas:** `INSPECCION_ESTÁTICA_COMPLETA` (código leído/analizado por AST), `PRUEBA_LOCAL_EJECUTADA` (ejecutada en este cierre), `VALIDACIÓN_FÍSICA_PENDIENTE` (sin equivalente físico en CCI-DEV).

**Honestidad de alcance.** «Línea por línea» se cumplió con lectura directa en las funciones críticas y con análisis AST sobre las 22; las funciones de una línea (k47, resoluciones, assets, av, cf, ac) son delegaciones a `_correr_lista`/`_correr15` y su lógica es la de esos ayudantes. No se reescribió ni se ejecutó el modelo completo de nuevo (V26 ya lo hizo: 366 casos, 0 fallos).

## Rasgos comunes a las 22 funciones (verificados)

- **Sin E/S externa:** `modelo_estructural.py` no contiene `open(`, ni `random`, `time`, `uuid`, `datetime` ni acceso a entorno (búsqueda realizada); importa `copy, functools, difflib, hashlib, json` y `contextlib`. Determinista.
- **Sin escrituras globales:** el AST no encuentra `global` en ninguna de las 22; cada función construye su propio motor/fixture. Las listas de casos (K47_MUT, ART_MUT…) son de sólo lectura.
- **Lecturas/escrituras:** sólo estructuras en memoria del propio motor (`Motor`, `m.res`, `m.at`, `m.assets`, `m.ev`); ninguna toca base de datos.
- **Concurrencia/idempotencia:** el modelo es secuencial y de un solo hilo; no representa transacciones concurrentes. Dos ejecuciones consecutivas producen resultados idénticos (V20 corrida1/corrida2 y V26). La concurrencia es `VALIDACIÓN_FÍSICA_PENDIENTE`.
- **Datos nulos/duplicados/inválidos:** cubiertos sólo donde hay casos explícitos (p. ej. evento de carga nulo, ID de asset duplicado, resolutor inválido); no hay prueba generalizada (fuzzing) de nulos en todos los campos.

## Resumen por función

| # | Función | Líneas | Casos | Resultado V26 | Responsabilidad | Reglas / invariantes | Estado de la inspección |
|---|---|---|---|---|---|---|---|
| 1 | `pruebas_guarda` | 1810–1822 (13) | 9 | PASS 9 | Intentos directos de alterar el registro de resoluciones (9) deben lanzar ResolucionInmutable y dejar el registro idéntico | IG5-98; I13 | INSPECCION_ESTÁTICA_COMPLETA; PRUEBA_LOCAL_EJECUTADA (366/366 re-ejecutados, resultados/22_funciones_reejecucion_local.txt); VALIDACIÓN_FÍSICA_PENDIENTE |
| 2 | `pruebas_atomicidad` | 2104–2117 (14) | 20 | PASS 20 | Reutilización de asset con elemento ausente/inconsistente falla antes de escribir y no deja registros parciales (20 casos: 8 propios + 12 de correr_mutaciones_rechazo) | IG5-102; H-01 | INSPECCION_ESTÁTICA_COMPLETA; PRUEBA_LOCAL_EJECUTADA (366/366 re-ejecutados, resultados/22_funciones_reejecucion_local.txt); VALIDACIÓN_FÍSICA_PENDIENTE |
| 3 | `correr_mutaciones_rechazo` | 2259–2272 (14) | 12 | PASS 12 | A54..A65: altera UNA relación del origen y exige rechazo antes de escribir, error identificado, estado idéntico, E nulo y sin impacto ni publicación | IG5-102, IG5-103; relaciones RS-01 a RS-06 | INSPECCION_ESTÁTICA_COMPLETA; PRUEBA_LOCAL_EJECUTADA (366/366 re-ejecutados, resultados/22_funciones_reejecucion_local.txt); VALIDACIÓN_FÍSICA_PENDIENTE |
| 4 | `correr_adversariales` | 2325–2329 (5) | 16 | PASS 16 | Motor forzado acepta una alteración y el auditor independiente la detecta (16) | IE-12; I1..I28 | INSPECCION_ESTÁTICA_COMPLETA; PRUEBA_LOCAL_EJECUTADA (366/366 re-ejecutados, resultados/22_funciones_reejecucion_local.txt); VALIDACIÓN_FÍSICA_PENDIENTE |
| 5 | `correr_escenarios` | 2333–2341 (9) | 17 | PASS 17 | 12 escenarios A..L, resoluciones RS, uniformidad y metamorfismo con el motor correcto (17 casos) | IG5-97; IG5-72; IG5-91 | INSPECCION_ESTÁTICA_COMPLETA; PRUEBA_LOCAL_EJECUTADA (366/366 re-ejecutados, resultados/22_funciones_reejecucion_local.txt); VALIDACIÓN_FÍSICA_PENDIENTE |
| 6 | `correr_mutaciones_k47` | 2361–2361 (1) | 36 | PASS 36 | 36 mutaciones del auditor K47: cada una cambia UNA cosa y exige el invariante específico y su mensaje | IG5-97, IE-12; I1..I12 | INSPECCION_ESTÁTICA_COMPLETA; PRUEBA_LOCAL_EJECUTADA (366/366 re-ejecutados, resultados/22_funciones_reejecucion_local.txt); VALIDACIÓN_FÍSICA_PENDIENTE |
| 7 | `correr_mutaciones_resoluciones` | 2362–2362 (1) | 12 | PASS 12 | 12 mutaciones R01..R12 de inmutabilidad y reglas de resoluciones de descarte | IG5-98, IG5-93; I13 | INSPECCION_ESTÁTICA_COMPLETA; PRUEBA_LOCAL_EJECUTADA (366/366 re-ejecutados, resultados/22_funciones_reejecucion_local.txt); VALIDACIÓN_FÍSICA_PENDIENTE |
| 8 | `correr_mutaciones_assets` | 2363–2363 (1) | 53 | PASS 53 | 53 mutaciones de procedencia de arte (uploader, evento, atribución, reutilización) | IG5-100, IG5-101, IG5-102, IG5-103 | INSPECCION_ESTÁTICA_COMPLETA; PRUEBA_LOCAL_EJECUTADA (366/366 re-ejecutados, resultados/22_funciones_reejecucion_local.txt); VALIDACIÓN_FÍSICA_PENDIENTE |
| 9 | `correr_positivos_arte` | 2364–2369 (6) | 26 | PASS 26 | 26 casos válidos de arte que el motor debe aceptar sin violaciones | IG5-100, IG5-101, IG5-102 | INSPECCION_ESTÁTICA_COMPLETA; PRUEBA_LOCAL_EJECUTADA (366/366 re-ejecutados, resultados/22_funciones_reejecucion_local.txt); VALIDACIÓN_FÍSICA_PENDIENTE |
| 10 | `correr_mutaciones_k45` | 2371–2385 (15) | 30 | PASS 30 | 27 mutaciones sobre la matriz 4.4.10 (K45) + 3 positivos; deepcopy del fixture | IE-12; K45 C01..C15 | INSPECCION_ESTÁTICA_COMPLETA; PRUEBA_LOCAL_EJECUTADA (366/366 re-ejecutados, resultados/22_funciones_reejecucion_local.txt); VALIDACIÓN_FÍSICA_PENDIENTE |
| 11 | `correr_mutaciones_cadena` | 2520–2534 (15) | 24 | PASS 24 | CHAIN-01..20 sobre eslabones intermedios de una cadena válida de tres niveles | IG5-103; K56 | INSPECCION_ESTÁTICA_COMPLETA; PRUEBA_LOCAL_EJECUTADA (366/366 re-ejecutados, resultados/22_funciones_reejecucion_local.txt); VALIDACIÓN_FÍSICA_PENDIENTE |
| 12 | `correr_adversariales_cadena` | 2543–2557 (15) | 24 | PASS 24 | Motor forzado + auditor sobre la cadena (24); exige aceptación, detección, E bloqueado, impacto falla y no publica | IG5-103; K56 | INSPECCION_ESTÁTICA_COMPLETA; PRUEBA_LOCAL_EJECUTADA (366/366 re-ejecutados, resultados/22_funciones_reejecucion_local.txt); VALIDACIÓN_FÍSICA_PENDIENTE |
| 13 | `correr_mutaciones_atribucion` | 2585–2622 (38) | 12 | PASS 12 | 12 mutaciones de atribución (I13, I15…) con autorretiro y resoluciones forzadas | IG5-97; I13, I15 | INSPECCION_ESTÁTICA_COMPLETA; PRUEBA_LOCAL_EJECUTADA (366/366 re-ejecutados, resultados/22_funciones_reejecucion_local.txt); VALIDACIÓN_FÍSICA_PENDIENTE |
| 14 | `pruebas_atomicidad14` | 2687–2753 (67) | 11 | PASS 11 | Atomicidad de v14 (carga de asset, reutilización): fallo a mitad, actor ajeno, versión inexistente; estado completo idéntico (11) | IG5-102 | INSPECCION_ESTÁTICA_COMPLETA; PRUEBA_LOCAL_EJECUTADA (366/366 re-ejecutados, resultados/22_funciones_reejecucion_local.txt); VALIDACIÓN_FÍSICA_PENDIENTE |
| 15 | `pruebas_E14` | 2764–2793 (30) | 6 | PASS 6 | Reconstrucción de E y elegibilidad del evaluador E1..E7 con fallo cerrado (6) | IG5-108; IG5-42 | INSPECCION_ESTÁTICA_COMPLETA; PRUEBA_LOCAL_EJECUTADA (366/366 re-ejecutados, resultados/22_funciones_reejecucion_local.txt); VALIDACIÓN_FÍSICA_PENDIENTE |
| 16 | `correr_mutaciones_av` | 2879–2879 (1) | 8 | PASS 8 | 8 mutaciones: asset_version incorrecto en eslabones propios | IG5-103; K58 | INSPECCION_ESTÁTICA_COMPLETA; PRUEBA_LOCAL_EJECUTADA (366/366 re-ejecutados, resultados/22_funciones_reejecucion_local.txt); VALIDACIÓN_FÍSICA_PENDIENTE |
| 17 | `correr_mutaciones_cf` | 2880–2880 (1) | 8 | PASS 8 | 8 mutaciones: campo incorrecto en eventos propios | IG5-103; K58 | INSPECCION_ESTÁTICA_COMPLETA; PRUEBA_LOCAL_EJECUTADA (366/366 re-ejecutados, resultados/22_funciones_reejecucion_local.txt); VALIDACIÓN_FÍSICA_PENDIENTE |
| 18 | `correr_mutaciones_ac` | 2881–2881 (1) | 6 | PASS 6 | 6 mutaciones: combinaciones asset_version + campo | IG5-103; K58 | INSPECCION_ESTÁTICA_COMPLETA; PRUEBA_LOCAL_EJECUTADA (366/366 re-ejecutados, resultados/22_funciones_reejecucion_local.txt); VALIDACIÓN_FÍSICA_PENDIENTE |
| 19 | `correr_positivos15` | 2925–2931 (7) | 8 | PASS 8 | 8 cadenas válidas v15 que deben aceptarse | IG5-103 | INSPECCION_ESTÁTICA_COMPLETA; PRUEBA_LOCAL_EJECUTADA (366/366 re-ejecutados, resultados/22_funciones_reejecucion_local.txt); VALIDACIÓN_FÍSICA_PENDIENTE |
| 20 | `correr_adversariales15` | 2947–2964 (18) | 8 | PASS 8 | Motor forzado + auditor con v15 (8) | IG5-103 | INSPECCION_ESTÁTICA_COMPLETA; PRUEBA_LOCAL_EJECUTADA (366/366 re-ejecutados, resultados/22_funciones_reejecucion_local.txt); VALIDACIÓN_FÍSICA_PENDIENTE |
| 21 | `pruebas_atomicidad15` | 2984–2999 (16) | 8 | PASS 8 | Atomicidad antes/después de validar la raíz; el reintento sin fallo repone el estado (8) | IG5-102 | INSPECCION_ESTÁTICA_COMPLETA; PRUEBA_LOCAL_EJECUTADA (366/366 re-ejecutados, resultados/22_funciones_reejecucion_local.txt); VALIDACIÓN_FÍSICA_PENDIENTE |
| 22 | `correr_mutaciones_modelo14` | 3057–3067 (11) | 12 | PASS 12 | 12 mutaciones del propio modelo (validación por eslabón convertida en no-op) | K56-M | INSPECCION_ESTÁTICA_COMPLETA; PRUEBA_LOCAL_EJECUTADA (366/366 re-ejecutados, resultados/22_funciones_reejecucion_local.txt); VALIDACIÓN_FÍSICA_PENDIENTE |

## Ficha detallada por función

### 1. `pruebas_guarda`

- **Identificador y ubicación:** `modelo_estructural.py` líneas 1810–1822; SHA-256 del fuente de la función (16 primeros): `97e746949c85fea1`.
- **Responsabilidad:** Intentos directos de alterar el registro de resoluciones (9) deben lanzar ResolucionInmutable y dejar el registro idéntico.
- **Entradas/salidas:** entradas: ninguna (usa listas globales); salida: lista de resultados por caso (`9` casos individuales en el registro V20/V26).
- **Reglas / invariantes:** IG5-98; I13. **Escenarios que citan esas reglas (calculado de la matriz de 780):** IG5-98: 17 escenarios (p. ej. T-423, T-424, T-425, T-426).
- **Dependencias internas (nombres del módulo):** `Motor`, `ResolucionInmutable`, `_plano`, `esc_resol`.
- **Lecturas / escrituras:** sólo memoria del motor; sin E/S.
- **Manejo de errores:** 1 bloque(s) try, 1 `except` amplios (`Exception`).
- **Riesgos de seguridad/integridad y observaciones:** `except Exception: ok=False` convierte un error inesperado en «no rechazado» (conservador, no oculta fallos).
- **Idempotencia/concurrencia:** determinista y secuencial; concurrencia no modelada.
- **Pruebas existentes:** 9 casos en `REGISTRO_CASOS_22_FUNCIONES_V20.csv`, todos PASS en V26.
- **Brechas y recomendaciones:** Sólo guarda en memoria; el equivalente físico es trigger+privilegios (PRUEBAS_RLS_PRIVILEGIOS_CONCURRENCIA.md).

### 2. `pruebas_atomicidad`

- **Identificador y ubicación:** `modelo_estructural.py` líneas 2104–2117; SHA-256 del fuente de la función (16 primeros): `634eff5a980cfe59`.
- **Responsabilidad:** Reutilización de asset con elemento ausente/inconsistente falla antes de escribir y no deja registros parciales (20 casos: 8 propios + 12 de correr_mutaciones_rechazo).
- **Entradas/salidas:** entradas: ninguna (usa listas globales); salida: lista de resultados por caso (`20` casos individuales en el registro V20/V26).
- **Reglas / invariantes:** IG5-102; H-01. **Escenarios que citan esas reglas (calculado de la matriz de 780):** IG5-102: 36 escenarios (p. ej. T-541, T-542, T-543, T-544).
- **Dependencias internas (nombres del módulo):** `Motor`, `ReutilizacionInvalida`, `_base`, `_estado_completo`, `_intro_cv`, `correr_mutaciones_rechazo`.
- **Lecturas / escrituras:** sólo memoria del motor; sin E/S.
- **Manejo de errores:** 1 bloque(s) try, 1 `except` amplios (`Exception`).
- **Riesgos de seguridad/integridad y observaciones:** Acoplamiento: reusa correr_mutaciones_rechazo; un fallo allí se propaga a esta función.
- **Idempotencia/concurrencia:** determinista y secuencial; concurrencia no modelada.
- **Pruebas existentes:** 20 casos en `REGISTRO_CASOS_22_FUNCIONES_V20.csv`, todos PASS en V26.
- **Brechas y recomendaciones:** Atomicidad física (transacción/rollback) no validada.

### 3. `correr_mutaciones_rechazo`

- **Identificador y ubicación:** `modelo_estructural.py` líneas 2259–2272; SHA-256 del fuente de la función (16 primeros): `bac621363f3d38a3`.
- **Responsabilidad:** A54..A65: altera UNA relación del origen y exige rechazo antes de escribir, error identificado, estado idéntico, E nulo y sin impacto ni publicación.
- **Entradas/salidas:** entradas: ninguna (usa listas globales); salida: lista de resultados por caso (`12` casos individuales en el registro V20/V26).
- **Reglas / invariantes:** IG5-102, IG5-103; relaciones RS-01 a RS-06. **Escenarios que citan esas reglas (calculado de la matriz de 780):** IG5-102: 36 escenarios (p. ej. T-541, T-542, T-543, T-544); IG5-103: 50 escenarios (p. ej. T-577, T-578, T-579, T-580).
- **Dependencias internas (nombres del módulo):** `ART_RECH`, `Motor`, `_bloqueada`, `_estado_completo`, `_fx13`, `_hall_arte_exactas`, `_intento`, `auditar_E`, `calcular_E_verificado`, `snapshot`.
- **Lecturas / escrituras:** sólo memoria del motor; sin E/S.
- **Manejo de errores:** 1 bloque(s) try, 1 `except` amplios (`Exception`).
- **Riesgos de seguridad/integridad y observaciones:** Código muerto `x0.E("ca") if False else …` (línea 2264); inofensivo.
- **Idempotencia/concurrencia:** determinista y secuencial; concurrencia no modelada.
- **Pruebas existentes:** 12 casos en `REGISTRO_CASOS_22_FUNCIONES_V20.csv`, todos PASS en V26.
- **Brechas y recomendaciones:** FK compuestas RS-xx no ejecutadas en esquema físico.

### 4. `correr_adversariales`

- **Identificador y ubicación:** `modelo_estructural.py` líneas 2325–2329; SHA-256 del fuente de la función (16 primeros): `f8da3cf90506cb4a`.
- **Responsabilidad:** Motor forzado acepta una alteración y el auditor independiente la detecta (16).
- **Entradas/salidas:** entradas: ninguna (usa listas globales); salida: lista de resultados por caso (`16` casos individuales en el registro V20/V26).
- **Reglas / invariantes:** IE-12; I1..I28. **Escenarios que citan esas reglas (calculado de la matriz de 780):** IE-12: 308 escenarios (p. ej. T-377, T-378, T-379, T-380).
- **Dependencias internas (nombres del módulo):** `ADV`.
- **Lecturas / escrituras:** sólo memoria del motor; sin E/S.
- **Manejo de errores:** 0 bloque(s) try, 0 `except` amplios (`Exception`).
- **Riesgos de seguridad/integridad y observaciones:** Lee la lista global ADV; depende de que ADV sea completa.
- **Idempotencia/concurrencia:** determinista y secuencial; concurrencia no modelada.
- **Pruebas existentes:** 16 casos en `REGISTRO_CASOS_22_FUNCIONES_V20.csv`, todos PASS en V26.
- **Brechas y recomendaciones:** Equivalencia auditor/SQL no demostrada.

### 5. `correr_escenarios`

- **Identificador y ubicación:** `modelo_estructural.py` líneas 2333–2341; SHA-256 del fuente de la función (16 primeros): `c37e3ce933f91536`.
- **Responsabilidad:** 12 escenarios A..L, resoluciones RS, uniformidad y metamorfismo con el motor correcto (17 casos).
- **Entradas/salidas:** entradas: ninguna (usa listas globales); salida: lista de resultados por caso (`17` casos individuales en el registro V20/V26).
- **Reglas / invariantes:** IG5-97; IG5-72; IG5-91. **Escenarios que citan esas reglas (calculado de la matriz de 780):** IG5-72: 25 escenarios (p. ej. T-275, T-276, T-277, T-278); IG5-91: 5 escenarios (p. ej. T-279, T-299, T-336, T-354); IG5-97: 20 escenarios (p. ej. T-404, T-405, T-406, T-407).
- **Dependencias internas (nombres del módulo):** `ESCENARIOS`, `Motor`, `esc_Rtodas`, `esc_indep`, `esc_meta`, `esc_resol`, `esc_unif`.
- **Lecturas / escrituras:** sólo memoria del motor; sin E/S.
- **Manejo de errores:** 1 bloque(s) try, 1 `except` amplios (`Exception`).
- **Riesgos de seguridad/integridad y observaciones:** Casos con aserciones codificadas a mano (valores esperados fijos).
- **Idempotencia/concurrencia:** determinista y secuencial; concurrencia no modelada.
- **Pruebas existentes:** 17 casos en `REGISTRO_CASOS_22_FUNCIONES_V20.csv`, todos PASS en V26.
- **Brechas y recomendaciones:** Modelo en memoria, sin concurrencia.

### 6. `correr_mutaciones_k47`

- **Identificador y ubicación:** `modelo_estructural.py` líneas 2361–2361; SHA-256 del fuente de la función (16 primeros): `461166f2da779c78`.
- **Responsabilidad:** 36 mutaciones del auditor K47: cada una cambia UNA cosa y exige el invariante específico y su mensaje.
- **Entradas/salidas:** entradas: ninguna (usa listas globales); salida: lista de resultados por caso (`36` casos individuales en el registro V20/V26).
- **Reglas / invariantes:** IG5-97, IE-12; I1..I12. **Escenarios que citan esas reglas (calculado de la matriz de 780):** IE-12: 308 escenarios (p. ej. T-377, T-378, T-379, T-380); IG5-97: 20 escenarios (p. ej. T-404, T-405, T-406, T-407).
- **Dependencias internas (nombres del módulo):** `K47_MUT`, `_correr_lista`.
- **Lecturas / escrituras:** sólo memoria del motor; sin E/S.
- **Manejo de errores:** 0 bloque(s) try, 0 `except` amplios (`Exception`).
- **Riesgos de seguridad/integridad y observaciones:** Detección exige coincidencia de mensaje (`kw in v[1]`): frágil ante cambios de redacción.
- **Idempotencia/concurrencia:** determinista y secuencial; concurrencia no modelada.
- **Pruebas existentes:** 36 casos en `REGISTRO_CASOS_22_FUNCIONES_V20.csv`, todos PASS en V26.
- **Brechas y recomendaciones:** 11 mutaciones (M16, M21, M27..M36) sin escenario T asociado en el texto de la especificación.

### 7. `correr_mutaciones_resoluciones`

- **Identificador y ubicación:** `modelo_estructural.py` líneas 2362–2362; SHA-256 del fuente de la función (16 primeros): `b138e3707577e52b`.
- **Responsabilidad:** 12 mutaciones R01..R12 de inmutabilidad y reglas de resoluciones de descarte.
- **Entradas/salidas:** entradas: ninguna (usa listas globales); salida: lista de resultados por caso (`12` casos individuales en el registro V20/V26).
- **Reglas / invariantes:** IG5-98, IG5-93; I13. **Escenarios que citan esas reglas (calculado de la matriz de 780):** IG5-93: 14 escenarios (p. ej. T-340, T-343, T-344, T-345); IG5-98: 17 escenarios (p. ej. T-423, T-424, T-425, T-426).
- **Dependencias internas (nombres del módulo):** `RES_MUT`, `_correr_lista`.
- **Lecturas / escrituras:** sólo memoria del motor; sin E/S.
- **Manejo de errores:** 0 bloque(s) try, 0 `except` amplios (`Exception`).
- **Riesgos de seguridad/integridad y observaciones:** Igual que k47 (delegada en _correr_lista).
- **Idempotencia/concurrencia:** determinista y secuencial; concurrencia no modelada.
- **Pruebas existentes:** 12 casos en `REGISTRO_CASOS_22_FUNCIONES_V20.csv`, todos PASS en V26.
- **Brechas y recomendaciones:** Equivalente físico: trigger + índice único parcial (probado en PE_POSTGRESQL_V20 PG-AD).

### 8. `correr_mutaciones_assets`

- **Identificador y ubicación:** `modelo_estructural.py` líneas 2363–2363; SHA-256 del fuente de la función (16 primeros): `145b0471b1f18b75`.
- **Responsabilidad:** 53 mutaciones de procedencia de arte (uploader, evento, atribución, reutilización).
- **Entradas/salidas:** entradas: ninguna (usa listas globales); salida: lista de resultados por caso (`53` casos individuales en el registro V20/V26).
- **Reglas / invariantes:** IG5-100, IG5-101, IG5-102, IG5-103. **Escenarios que citan esas reglas (calculado de la matriz de 780):** IG5-100: 37 escenarios (p. ej. T-466, T-467, T-468, T-469); IG5-101: 38 escenarios (p. ej. T-503, T-504, T-505, T-506); IG5-102: 36 escenarios (p. ej. T-541, T-542, T-543, T-544); IG5-103: 50 escenarios (p. ej. T-577, T-578, T-579, T-580).
- **Dependencias internas (nombres del módulo):** `ART_MUT`, `_correr_lista`.
- **Lecturas / escrituras:** sólo memoria del motor; sin E/S.
- **Manejo de errores:** 0 bloque(s) try, 0 `except` amplios (`Exception`).
- **Riesgos de seguridad/integridad y observaciones:** Igual que k47; 53 casos (A01..A53) dependen de IDs fijos.
- **Idempotencia/concurrencia:** determinista y secuencial; concurrencia no modelada.
- **Pruebas existentes:** 53 casos en `REGISTRO_CASOS_22_FUNCIONES_V20.csv`, todos PASS en V26.
- **Brechas y recomendaciones:** FK RS-xx no ejecutadas físicamente.

### 9. `correr_positivos_arte`

- **Identificador y ubicación:** `modelo_estructural.py` líneas 2364–2369; SHA-256 del fuente de la función (16 primeros): `91dbedf595500ae4`.
- **Responsabilidad:** 26 casos válidos de arte que el motor debe aceptar sin violaciones.
- **Entradas/salidas:** entradas: ninguna (usa listas globales); salida: lista de resultados por caso (`26` casos individuales en el registro V20/V26).
- **Reglas / invariantes:** IG5-100, IG5-101, IG5-102. **Escenarios que citan esas reglas (calculado de la matriz de 780):** IG5-100: 37 escenarios (p. ej. T-466, T-467, T-468, T-469); IG5-101: 38 escenarios (p. ej. T-503, T-504, T-505, T-506); IG5-102: 36 escenarios (p. ej. T-541, T-542, T-543, T-544).
- **Dependencias internas (nombres del módulo):** `ESC_ARTE`, `Motor`.
- **Lecturas / escrituras:** sólo memoria del motor; sin E/S.
- **Manejo de errores:** 1 bloque(s) try, 1 `except` amplios (`Exception`).
- **Riesgos de seguridad/integridad y observaciones:** Contiene `if False` (línea 2276, en _pos13).
- **Idempotencia/concurrencia:** determinista y secuencial; concurrencia no modelada.
- **Pruebas existentes:** 26 casos en `REGISTRO_CASOS_22_FUNCIONES_V20.csv`, todos PASS en V26.
- **Brechas y recomendaciones:** Positivos sólo en el modelo.

### 10. `correr_mutaciones_k45`

- **Identificador y ubicación:** `modelo_estructural.py` líneas 2371–2385; SHA-256 del fuente de la función (16 primeros): `c6ec663f62d7209f`.
- **Responsabilidad:** 27 mutaciones sobre la matriz 4.4.10 (K45) + 3 positivos; deepcopy del fixture.
- **Entradas/salidas:** entradas: M; salida: lista de resultados por caso (`30` casos individuales en el registro V20/V26).
- **Reglas / invariantes:** IE-12; K45 C01..C15. **Escenarios que citan esas reglas (calculado de la matriz de 780):** IE-12: 308 escenarios (p. ej. T-377, T-378, T-379, T-380).
- **Dependencias internas (nombres del módulo):** `K45_MUT`, `evaluar_k45_estructural`, `fixture_k45`, `variantes_positivas_k45`.
- **Lecturas / escrituras:** sólo memoria del motor; sin E/S.
- **Manejo de errores:** 2 bloque(s) try, 2 `except` amplios (`Exception`).
- **Riesgos de seguridad/integridad y observaciones:** Único con `copy.deepcopy`; retorna tupla (res, positivos).
- **Idempotencia/concurrencia:** determinista y secuencial; concurrencia no modelada.
- **Pruebas existentes:** 30 casos en `REGISTRO_CASOS_22_FUNCIONES_V20.csv`, todos PASS en V26.
- **Brechas y recomendaciones:** Requiere la matriz de la especificación; no se ejecuta aislado.

### 11. `correr_mutaciones_cadena`

- **Identificador y ubicación:** `modelo_estructural.py` líneas 2520–2534; SHA-256 del fuente de la función (16 primeros): `ae541f9f3d104bd5`.
- **Responsabilidad:** CHAIN-01..20 sobre eslabones intermedios de una cadena válida de tres niveles.
- **Entradas/salidas:** entradas: ninguna (usa listas globales); salida: lista de resultados por caso (`24` casos individuales en el registro V20/V26).
- **Reglas / invariantes:** IG5-103; K56. **Escenarios que citan esas reglas (calculado de la matriz de 780):** IG5-103: 50 escenarios (p. ej. T-577, T-578, T-579, T-580).
- **Dependencias internas (nombres del módulo):** `CHAIN`, `Motor`, `_CHAIN_A1B`, `_bloqueada`, `_estado_completo`, `_fx14`, `_hall_arte_exactas`, `_intento14`, `auditar_E`, `calcular_E_verificado`, `snapshot`.
- **Lecturas / escrituras:** sólo memoria del motor; sin E/S.
- **Manejo de errores:** 1 bloque(s) try, 1 `except` amplios (`Exception`).
- **Riesgos de seguridad/integridad y observaciones:** Lista CHAIN global; casos por eslabón.
- **Idempotencia/concurrencia:** determinista y secuencial; concurrencia no modelada.
- **Pruebas existentes:** 24 casos en `REGISTRO_CASOS_22_FUNCIONES_V20.csv`, todos PASS en V26.
- **Brechas y recomendaciones:** FK de cadena físicas no ejecutadas.

### 12. `correr_adversariales_cadena`

- **Identificador y ubicación:** `modelo_estructural.py` líneas 2543–2557; SHA-256 del fuente de la función (16 primeros): `af7aff2757c8fbd1`.
- **Responsabilidad:** Motor forzado + auditor sobre la cadena (24); exige aceptación, detección, E bloqueado, impacto falla y no publica.
- **Entradas/salidas:** entradas: ninguna (usa listas globales); salida: lista de resultados por caso (`24` casos individuales en el registro V20/V26).
- **Reglas / invariantes:** IG5-103; K56. **Escenarios que citan esas reglas (calculado de la matriz de 780):** IG5-103: 50 escenarios (p. ej. T-577, T-578, T-579, T-580).
- **Dependencias internas (nombres del módulo):** `CHAIN`, `ProcedenciaIncompleta`, `_CHAIN_A1B`, `_Forzado14`, `_fx14`, `auditar_E`, `calcular_E_verificado`, `evaluar_impacto`, `puede_publicar`, `snapshot`.
- **Lecturas / escrituras:** sólo memoria del motor; sin E/S.
- **Manejo de errores:** 3 bloque(s) try, 2 `except` amplios (`Exception`).
- **Riesgos de seguridad/integridad y observaciones:** `except Exception: acepta=False` anidado: un error inesperado se registra como «el motor no acepta» (hace fallar el caso, conservador).
- **Idempotencia/concurrencia:** determinista y secuencial; concurrencia no modelada.
- **Pruebas existentes:** 24 casos en `REGISTRO_CASOS_22_FUNCIONES_V20.csv`, todos PASS en V26.
- **Brechas y recomendaciones:** —

### 13. `correr_mutaciones_atribucion`

- **Identificador y ubicación:** `modelo_estructural.py` líneas 2585–2622; SHA-256 del fuente de la función (16 primeros): `310bc22a622666b6`.
- **Responsabilidad:** 12 mutaciones de atribución (I13, I15…) con autorretiro y resoluciones forzadas.
- **Entradas/salidas:** entradas: ninguna (usa listas globales); salida: lista de resultados por caso (`12` casos individuales en el registro V20/V26).
- **Reglas / invariantes:** IG5-97; I13, I15. **Escenarios que citan esas reglas (calculado de la matriz de 780):** IG5-97: 20 escenarios (p. ej. T-404, T-405, T-406, T-407).
- **Dependencias internas (nombres del módulo):** `Motor`, `_AutoRetiro`, `_ForzRes`, `_aplicar_y_auditar`, `_aud_estado`, `_base`, `_res`, `_sc_res`, `_sc_res_aplicada`, `_sello_ind`, `_set_res`.
- **Lecturas / escrituras:** sólo memoria del motor; sin E/S.
- **Manejo de errores:** 0 bloque(s) try, 0 `except` amplios (`Exception`).
- **Riesgos de seguridad/integridad y observaciones:** 38 líneas sin try: una excepción aborta toda la función (no se aísla por caso).
- **Idempotencia/concurrencia:** determinista y secuencial; concurrencia no modelada.
- **Pruebas existentes:** 12 casos en `REGISTRO_CASOS_22_FUNCIONES_V20.csv`, todos PASS en V26.
- **Brechas y recomendaciones:** Sin concurrencia.

### 14. `pruebas_atomicidad14`

- **Identificador y ubicación:** `modelo_estructural.py` líneas 2687–2753; SHA-256 del fuente de la función (16 primeros): `1ca5e86439fedf15`.
- **Responsabilidad:** Atomicidad de v14 (carga de asset, reutilización): fallo a mitad, actor ajeno, versión inexistente; estado completo idéntico (11).
- **Entradas/salidas:** entradas: ninguna (usa listas globales); salida: lista de resultados por caso (`11` casos individuales en el registro V20/V26).
- **Reglas / invariantes:** IG5-102. **Escenarios que citan esas reglas (calculado de la matriz de 780):** IG5-102: 36 escenarios (p. ej. T-541, T-542, T-543, T-544).
- **Dependencias internas (nombres del módulo):** `Motor`, `OperacionInvalida`, `ProcedenciaIncompleta`, `ReutilizacionInvalida`, `_Falla`, `_Forzado14`, `_base`, `_estado_completo`, `_ev_pr`, `_fx14`, `_intro_cv`, `_res`.
- **Lecturas / escrituras:** sólo memoria del motor; sin E/S.
- **Manejo de errores:** 4 bloque(s) try, 1 `except` amplios (`Exception`).
- **Riesgos de seguridad/integridad y observaciones:** 4 bloques try; un `except Exception` amplio.
- **Idempotencia/concurrencia:** determinista y secuencial; concurrencia no modelada.
- **Pruebas existentes:** 11 casos en `REGISTRO_CASOS_22_FUNCIONES_V20.csv`, todos PASS en V26.
- **Brechas y recomendaciones:** Atomicidad física no validada.

### 15. `pruebas_E14`

- **Identificador y ubicación:** `modelo_estructural.py` líneas 2764–2793; SHA-256 del fuente de la función (16 primeros): `1acb81f654bc5b85`.
- **Responsabilidad:** Reconstrucción de E y elegibilidad del evaluador E1..E7 con fallo cerrado (6).
- **Entradas/salidas:** entradas: ninguna (usa listas globales); salida: lista de resultados por caso (`6` casos individuales en el registro V20/V26).
- **Reglas / invariantes:** IG5-108; IG5-42. **Escenarios que citan esas reglas (calculado de la matriz de 780):** IG5-108: 6 escenarios (p. ej. T-698, T-699, T-700, T-701); IG5-42: 9 escenarios (p. ej. T-166, T-167, T-225, T-226).
- **Dependencias internas (nombres del módulo):** `_E`, `_ev_pr`, `_fx_E`, `_sc_res_aplicada`, `calcular_E_verificado`, `elegibilidad_evaluador`, `snapshot`.
- **Lecturas / escrituras:** sólo memoria del motor; sin E/S.
- **Manejo de errores:** 1 bloque(s) try, 1 `except` amplios (`Exception`).
- **Riesgos de seguridad/integridad y observaciones:** Conjuntos esperados fijos (p. ej. {A,Pm,B,U,D,W}); usa comprensiones con efectos laterales (`[m.at.pop(...)]`).
- **Idempotencia/concurrencia:** determinista y secuencial; concurrencia no modelada.
- **Pruebas existentes:** 6 casos en `REGISTRO_CASOS_22_FUNCIONES_V20.csv`, todos PASS en V26.
- **Brechas y recomendaciones:** El trigger físico R1–R9 no existe.

### 16. `correr_mutaciones_av`

- **Identificador y ubicación:** `modelo_estructural.py` líneas 2879–2879; SHA-256 del fuente de la función (16 primeros): `cb63a5cfbb4089c2`.
- **Responsabilidad:** 8 mutaciones: asset_version incorrecto en eslabones propios.
- **Entradas/salidas:** entradas: ninguna (usa listas globales); salida: lista de resultados por caso (`8` casos individuales en el registro V20/V26).
- **Reglas / invariantes:** IG5-103; K58. **Escenarios que citan esas reglas (calculado de la matriz de 780):** IG5-103: 50 escenarios (p. ej. T-577, T-578, T-579, T-580).
- **Dependencias internas (nombres del módulo):** `AV`, `_correr15`.
- **Lecturas / escrituras:** sólo memoria del motor; sin E/S.
- **Manejo de errores:** 0 bloque(s) try, 0 `except` amplios (`Exception`).
- **Riesgos de seguridad/integridad y observaciones:** Una línea; delega en _correr15.
- **Idempotencia/concurrencia:** determinista y secuencial; concurrencia no modelada.
- **Pruebas existentes:** 8 casos en `REGISTRO_CASOS_22_FUNCIONES_V20.csv`, todos PASS en V26.
- **Brechas y recomendaciones:** —

### 17. `correr_mutaciones_cf`

- **Identificador y ubicación:** `modelo_estructural.py` líneas 2880–2880; SHA-256 del fuente de la función (16 primeros): `88d4adb6c10bebb8`.
- **Responsabilidad:** 8 mutaciones: campo incorrecto en eventos propios.
- **Entradas/salidas:** entradas: ninguna (usa listas globales); salida: lista de resultados por caso (`8` casos individuales en el registro V20/V26).
- **Reglas / invariantes:** IG5-103; K58. **Escenarios que citan esas reglas (calculado de la matriz de 780):** IG5-103: 50 escenarios (p. ej. T-577, T-578, T-579, T-580).
- **Dependencias internas (nombres del módulo):** `CF`, `_correr15`.
- **Lecturas / escrituras:** sólo memoria del motor; sin E/S.
- **Manejo de errores:** 0 bloque(s) try, 0 `except` amplios (`Exception`).
- **Riesgos de seguridad/integridad y observaciones:** Delega en _correr15.
- **Idempotencia/concurrencia:** determinista y secuencial; concurrencia no modelada.
- **Pruebas existentes:** 8 casos en `REGISTRO_CASOS_22_FUNCIONES_V20.csv`, todos PASS en V26.
- **Brechas y recomendaciones:** —

### 18. `correr_mutaciones_ac`

- **Identificador y ubicación:** `modelo_estructural.py` líneas 2881–2881; SHA-256 del fuente de la función (16 primeros): `f2ecd46024f47a4e`.
- **Responsabilidad:** 6 mutaciones: combinaciones asset_version + campo.
- **Entradas/salidas:** entradas: ninguna (usa listas globales); salida: lista de resultados por caso (`6` casos individuales en el registro V20/V26).
- **Reglas / invariantes:** IG5-103; K58. **Escenarios que citan esas reglas (calculado de la matriz de 780):** IG5-103: 50 escenarios (p. ej. T-577, T-578, T-579, T-580).
- **Dependencias internas (nombres del módulo):** `AC`, `_correr15`.
- **Lecturas / escrituras:** sólo memoria del motor; sin E/S.
- **Manejo de errores:** 0 bloque(s) try, 0 `except` amplios (`Exception`).
- **Riesgos de seguridad/integridad y observaciones:** Delega en _correr15.
- **Idempotencia/concurrencia:** determinista y secuencial; concurrencia no modelada.
- **Pruebas existentes:** 6 casos en `REGISTRO_CASOS_22_FUNCIONES_V20.csv`, todos PASS en V26.
- **Brechas y recomendaciones:** —

### 19. `correr_positivos15`

- **Identificador y ubicación:** `modelo_estructural.py` líneas 2925–2931; SHA-256 del fuente de la función (16 primeros): `8efe9148492c4b51`.
- **Responsabilidad:** 8 cadenas válidas v15 que deben aceptarse.
- **Entradas/salidas:** entradas: ninguna (usa listas globales); salida: lista de resultados por caso (`8` casos individuales en el registro V20/V26).
- **Reglas / invariantes:** IG5-103. **Escenarios que citan esas reglas (calculado de la matriz de 780):** IG5-103: 50 escenarios (p. ej. T-577, T-578, T-579, T-580).
- **Dependencias internas (nombres del módulo):** `AP`.
- **Lecturas / escrituras:** sólo memoria del motor; sin E/S.
- **Manejo de errores:** 1 bloque(s) try, 1 `except` amplios (`Exception`).
- **Riesgos de seguridad/integridad y observaciones:** Contiene aserciones por AP.
- **Idempotencia/concurrencia:** determinista y secuencial; concurrencia no modelada.
- **Pruebas existentes:** 8 casos en `REGISTRO_CASOS_22_FUNCIONES_V20.csv`, todos PASS en V26.
- **Brechas y recomendaciones:** —

### 20. `correr_adversariales15`

- **Identificador y ubicación:** `modelo_estructural.py` líneas 2947–2964; SHA-256 del fuente de la función (16 primeros): `f95d7fd1e03365e9`.
- **Responsabilidad:** Motor forzado + auditor con v15 (8).
- **Entradas/salidas:** entradas: ninguna (usa listas globales); salida: lista de resultados por caso (`8` casos individuales en el registro V20/V26).
- **Reglas / invariantes:** IG5-103. **Escenarios que citan esas reglas (calculado de la matriz de 780):** IG5-103: 50 escenarios (p. ej. T-577, T-578, T-579, T-580).
- **Dependencias internas (nombres del módulo):** `ADV15`, `ProcedenciaIncompleta`, `_Forzado15`, `_fx15`, `auditar_E`, `calcular_E_verificado`, `evaluar_impacto`, `puede_publicar`, `snapshot`.
- **Lecturas / escrituras:** sólo memoria del motor; sin E/S.
- **Manejo de errores:** 2 bloque(s) try, 1 `except` amplios (`Exception`).
- **Riesgos de seguridad/integridad y observaciones:** `… if True else False` (línea 2959): condición tautológica, inofensiva.
- **Idempotencia/concurrencia:** determinista y secuencial; concurrencia no modelada.
- **Pruebas existentes:** 8 casos en `REGISTRO_CASOS_22_FUNCIONES_V20.csv`, todos PASS en V26.
- **Brechas y recomendaciones:** —

### 21. `pruebas_atomicidad15`

- **Identificador y ubicación:** `modelo_estructural.py` líneas 2984–2999; SHA-256 del fuente de la función (16 primeros): `287fcc75e21ec0ca`.
- **Responsabilidad:** Atomicidad antes/después de validar la raíz; el reintento sin fallo repone el estado (8).
- **Entradas/salidas:** entradas: ninguna (usa listas globales); salida: lista de resultados por caso (`8` casos individuales en el registro V20/V26).
- **Reglas / invariantes:** IG5-102. **Escenarios que citan esas reglas (calculado de la matriz de 780):** IG5-102: 36 escenarios (p. ej. T-541, T-542, T-543, T-544).
- **Dependencias internas (nombres del módulo):** `_Falla15`, `_derivados`, `_estado_completo`, `_fx14`, `_sin_huerfanos`, `auditar_E`, `snapshot`.
- **Lecturas / escrituras:** sólo memoria del motor; sin E/S.
- **Manejo de errores:** 2 bloque(s) try, 1 `except` amplios (`Exception`).
- **Riesgos de seguridad/integridad y observaciones:** Verifica reintento (idempotencia lógica) sólo en memoria.
- **Idempotencia/concurrencia:** determinista y secuencial; concurrencia no modelada.
- **Pruebas existentes:** 8 casos en `REGISTRO_CASOS_22_FUNCIONES_V20.csv`, todos PASS en V26.
- **Brechas y recomendaciones:** Idempotencia física/concurrencia no validadas.

### 22. `correr_mutaciones_modelo14`

- **Identificador y ubicación:** `modelo_estructural.py` líneas 3057–3067; SHA-256 del fuente de la función (16 primeros): `2abfd56ed0a49d47`.
- **Responsabilidad:** 12 mutaciones del propio modelo (validación por eslabón convertida en no-op).
- **Entradas/salidas:** entradas: ninguna (usa listas globales); salida: lista de resultados por caso (`12` casos individuales en el registro V20/V26).
- **Reglas / invariantes:** K56-M. **Escenarios que citan esas reglas (calculado de la matriz de 780):** sin ID de regla individual.
- **Dependencias internas (nombres del módulo):** `K56_MUT`, `_baterias14`.
- **Lecturas / escrituras:** sólo memoria del motor; sin E/S.
- **Manejo de errores:** 1 bloque(s) try, 0 `except` amplios (`Exception`).
- **Riesgos de seguridad/integridad y observaciones:** Es una prueba de la prueba (meta-mutación).
- **Idempotencia/concurrencia:** determinista y secuencial; concurrencia no modelada.
- **Pruebas existentes:** 12 casos en `REGISTRO_CASOS_22_FUNCIONES_V20.csv`, todos PASS en V26.
- **Brechas y recomendaciones:** —

## Defectos hallados

Ninguno altera un resultado (no hay falsos PASS demostrados). Todos son de mantenibilidad o robustez del arnés; **no se modificó ninguna función original**.

| ID | Función | Línea | Descripción | Reproducción | Causa raíz | Impacto | Corrección propuesta | Prueba necesaria |
|---|---|---|---|---|---|---|---|---|
| DEF-F01 | correr_mutaciones_rechazo | 2264 | Rama muerta `x0.E("ca") if False else calcular_E_verificado(...)` | Ejecutar la función y leer la línea; la rama `x0.E` nunca se evalúa | Resto de refactorización | Ninguno funcional; confunde la lectura y oculta la intención | Eliminar la rama muerta (en una copia; no se modificó el original) | Re-ejecutar las 22 funciones y comparar los 366 casos |
| DEF-F02 | correr_positivos_arte (_pos13) | 2276 | `ev["source_root_asset_id"] if False else ...` | Lectura de la línea | Resto de refactorización | Ninguno funcional | Eliminar la rama muerta | Re-ejecución de los 26 positivos |
| DEF-F03 | correr_adversariales15 | 2959 | `... if True else False`: condición tautológica | Lectura de la línea | Condición temporal dejada en el código | Ninguno funcional | Quitar el condicional | Re-ejecución de los 8 adversariales |
| DEF-F04 | correr_mutaciones_atribucion | 2585 | Sin try/except por caso: una excepción inesperada aborta los 12 casos en lugar de marcar uno como error | Inspección AST (try=0 en 38 líneas) | Diseño del arnés | Un fallo del modelo se vería como caída de la función, no como FAIL localizado (no oculta fallos) | Envolver por caso como hace _correr_lista | Mutar el modelo para lanzar excepción y comprobar que sólo falla un caso |
| DEF-F05 | correr_mutaciones_k47/resoluciones/assets (_correr_lista) | 2344 | La detección exige `kw in mensaje`: acopla la prueba a la redacción de mensajes del auditor | Lectura de _correr_lista | Diseño del arnés | Un cambio de texto en un mensaje produciría falsos «no detectada» (falla visible, no un falso PASS) | Identificar por código de violación y no por subcadena | Cambiar la redacción de un mensaje y observar el resultado |

## Límites de las 22 funciones como evidencia

- Prueban un **modelo en memoria**; no demuestran FK, triggers, RLS, privilegios, transacciones ni concurrencia del esquema físico (ver `MATRIZ_MODELO_LOGICO_FISICO.md`).
- 366 casos PASS significan que el modelo detecta las mutaciones que sus autores previeron; no demuestra exhaustividad para Fase 1.
- La matriz función→regla→escenario→prueba está en `MATRIZ_FUNCION_REGLA_ESCENARIO_PRUEBA.csv`.
