# MATRIZ DE PRUEBAS — 22 FUNCIONES / 366 CASOS (V20)

**Versión:** V20 · **Fecha:** 2026-11-20 · **Fuente:** `herramientas/modelo_estructural.py` (cc87236a…c52a, sin modificar), `herramientas/verificar_expediente.py` (1acec85d…035a, sin modificar), `evidencia_v16/instrumentar_22_funciones_v20.py` · **Estado:** reejecutado; registro normalizado en `REGISTRO_CASOS_22_FUNCIONES_V20.csv`.

## H-01 — Reconciliación 363 / 366 (causa raíz)
- El log histórico `salida_22_funciones_corrida1.txt` tiene **366 líneas de resultado individual, todas PASS** (368 líneas con las 2 de resumen).
- El script V18 imprimía los 3 casos positivos de `correr_mutaciones_k45` (POS-01..03) pero **no los sumaba** al contador (`tot[f]=n` solo contaba las 27 mutaciones) → «TOTAL casos=363». El inventario V18 sumaba 366 en sus renglones (27 de K45) y a la vez decía «363 incluye los 3 positivos»: contradicción interna.
- **Total real: 366 = 363 casos de mutación/adversariales/atomicidad/escenarios/etc. + 3 positivos de K45.** La cifra 363 queda solo como subtotal histórico. Ningún caso se eliminó ni se ignoró; el script V20 cuenta todas las filas.

## Totales verificables
- Casos individuales (resultados): **366**; PASS 366; FAIL 0; SKIP 0.
- Claves únicas `función:id`: **366** (0 duplicados reales).
- Invocaciones repetidas: las 22 funciones se invocan una vez en la instrumentación; el verificador las invoca desde varios puntos (ver inventario V20, columna de invocación); **no aportan casos adicionales** (misma función, mismo conjunto).
- IDs numéricos 01–09 compartidos entre `pruebas_guarda` y `pruebas_atomicidad`: son casos **distintos** (distinta función y descripción); la clave única incluye la función.
- 27 descripciones se repiten en 54 casos de funciones distintas (p. ej. atomicidad del motor y mutación del auditor sobre el mismo defecto): son ejecuciones **distintas** (id y propósito distintos), no duplicados; se conservan y se marcan en el registro.
- Agregaciones del verificador: el verificador agrega indicadores (p. ej. «E14 6/6»); no se cuentan como casos adicionales.

## Por función
| # | Función | Casos | Grupos |
|---|---|---|---|
| 1 | pruebas_guarda | 9 | guarda 9 |
| 2 | pruebas_atomicidad | 20 | atomicidad 20 |
| 3 | correr_mutaciones_rechazo | 12 | mutación 12 |
| 4 | correr_adversariales | 16 | adversarial 16 |
| 5 | correr_escenarios | 17 | escenario 17 |
| 6 | correr_mutaciones_k47 | 36 | mutación 36 |
| 7 | correr_mutaciones_resoluciones | 12 | mutación 12 |
| 8 | correr_mutaciones_assets | 53 | mutación 53 |
| 9 | correr_positivos_arte | 26 | positivo 26 |
| 10 | correr_mutaciones_k45 | 30 | mutación 30 |
| 11 | correr_mutaciones_cadena | 24 | mutación 24 |
| 12 | correr_adversariales_cadena | 24 | adversarial 24 |
| 13 | correr_mutaciones_atribucion | 12 | mutación 12 |
| 14 | pruebas_atomicidad14 | 11 | atomicidad 11 |
| 15 | pruebas_E14 | 6 | reconstrucción E 6 |
| 16 | correr_mutaciones_av | 8 | mutación 8 |
| 17 | correr_mutaciones_cf | 8 | mutación 8 |
| 18 | correr_mutaciones_ac | 6 | mutación 6 |
| 19 | correr_positivos15 | 8 | positivo 8 |
| 20 | correr_adversariales15 | 8 | adversarial 8 |
| 21 | pruebas_atomicidad15 | 8 | atomicidad 8 |
| 22 | correr_mutaciones_modelo14 | 12 | mutación 12 |

Por grupo: guarda 9, atomicidad 39, mutación 213, adversarial 48, escenario 17, positivo 34, reconstrucción E 6.

## Reejecución V20
Comando: `env -i PATH=/usr/bin:/bin LC_ALL=C.UTF-8 PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 python3 -I evidencia_v16/instrumentar_22_funciones_v20.py herramientas ESPECIFICACION_TECNICA_G1_G5_G10.md` → `TOTAL funciones=22 casos=366 fallos=0`, exit 0. Los resultados individuales (líneas de caso) son idénticos byte a byte a los de V18.

## Alcance y límites
Pruebas en memoria sobre un modelo Python; no prueban PostgreSQL (ver `PE_POSTGRESQL_V20/` para lo ejecutado en un clúster temporal) ni Supabase. 258 escenarios demostrados por ejecución en el modelo (criterios E1/E2/E3).
