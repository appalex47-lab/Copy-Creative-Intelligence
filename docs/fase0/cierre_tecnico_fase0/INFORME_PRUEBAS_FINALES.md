# INFORME DE PRUEBAS FINALES (locales) — generado desde `resultados/bateria_final/`

**Etiqueta:** todos los resultados son de PostgreSQL 16 temporal local, modelo en memoria o análisis estático. **Ninguno valida el esquema físico de CCI-DEV** ni toca Supabase/CCI-PROD. Las salidas anteriores se borraron antes de ejecutar (ninguna se reutiliza); cada fila tiene fecha, comando, resultado y SHA-256 de la salida.

## Entorno

```
inicio_bateria_utc=2026-11-21T02:36:35Z
anfitrion_so=Linux 6.18.44-fc-v726
python=Python 3.13.18
postgres=PostgreSQL 16.15 (Ubuntu 16.15-0ubuntu0.24.04.1) on x86_64-pc-linux-gnu, compiled by gcc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0, 64-bit
base_local=clúster temporal en socket Unix (no Supabase)
HEAD_local=51ebb72263b49fe0e84eee137ef68c74c27372e1
fin_bateria_utc=2026-11-21T02:38:49Z
```

## Resultados de la batería

| Paso | Naturaleza | Inicio UTC | Fin UTC | rc | Resultado | Salida | SHA-256 (16) |
|---|---|---|---|---|---|---|---|
| v20_pe | LOCAL fixture V20 | 2026-11-21T02:36:35Z | 2026-11-21T02:36:36Z | 0 | TOTAL pruebas=63 PASS=63 FAIL=0 | `/tmp/ct/docs/fase0/cierre_tecnico_fase0/scripts_validacion/resultados/base_V20_pe_utf8.txt` | cdf6aeb213bc8667 |
| v20_mutaciones | LOCAL fixture V20 | 2026-11-21T02:36:36Z | 2026-11-21T02:36:39Z | 0 | TOTAL mutaciones=14 DETECTADAS=14 | `/tmp/ct/docs/fase0/cierre_tecnico_fase0/scripts_validacion/resultados/base_V20_mutaciones_utf8.txt` | 5ff31240b365e382 |
| extension_local | LOCAL prototipos | 2026-11-21T02:36:39Z | 2026-11-21T02:36:39Z | 0 | TOTAL pruebas=80 PASS=80 FAIL=0 | `/tmp/ct/docs/fase0/cierre_tecnico_fase0/scripts_validacion/resultados/ext_utf8.txt` | 54f6941ea7d3da97 |
| concurrencia_local | LOCAL (2 sesiones) | 2026-11-21T02:36:39Z | 2026-11-21T02:36:46Z | 0 | CC-02 / IG1-14 numeración de versión única bajo concurrencia / esperado: B bloqueada >=1.5s y luego 23505; filas=1 / obtenido: espera=2.07s filas=1 err=ERROR | `/tmp/ct/docs/fase0/cierre_tecnico_fase0/scripts_validacion/resultados/concurrencia_local_utf8.txt` | 68e70e9dbaede5f9 |
| dg19 | LOCAL experimento | 2026-11-21T02:36:46Z | 2026-11-21T02:36:46Z | 0 | DG-19 PK natural: TOTAL pruebas=63 PASS=63 FAIL=0 | `/tmp/ct/docs/fase0/cierre_tecnico_fase0/scripts_validacion/resultados/dg19_pk_experimento.txt` | 02cd7664a3971b2d |
| hash_encadenado | LOCAL (pgcrypto) | 2026-11-21T02:36:46Z | 2026-11-21T02:36:46Z | 0 | TOTAL=16 PASS=16 FAIL=0 | `/tmp/ct/docs/fase0/cierre_tecnico_fase0/scripts_validacion/resultados/hash_cadena_referencia.txt` | ce96f96482d220ad |
| estatica_T47_T124 | ESTÁTICA (textos) | 2026-11-21T02:36:46Z | 2026-11-21T02:36:46Z | 0 | TOTAL=12 PASS=10 FAIL=0 SIN_DATOS=2 | `/tmp/ct/docs/fase0/cierre_tecnico_fase0/scripts_validacion/resultados/revision_estatica_T47_T124.txt` | 8bf91cd4b2ecd73c |
| k47_por_escenario | MODELO en memoria | 2026-11-21T02:36:46Z | 2026-11-21T02:36:47Z | 0 | TOTAL mutaciones mapeadas=25 DETECTADAS=25 todas_detectadas_con_estado_inicial_valido=True ; total K47_MUT=36 | `/tmp/ct/docs/fase0/cierre_tecnico_fase0/scripts_validacion/resultados/k47_por_escenario.txt` | f3a8022065d55224 |
| t409_individual | MODELO en memoria | 2026-11-21T02:36:47Z | 2026-11-21T02:36:47Z | 0 | TOTAL variantes=26 DETECTADAS=26 escenarios=14 (14 esperados) control_sin_alterar_ok=True todo_ok=True | `/tmp/ct/docs/fase0/cierre_tecnico_fase0/scripts_validacion/resultados/t409_t422_individual.txt` | 683734df7fcdfb18 |
| t409_repro_2a_corrida | MODELO en memoria (reproducibilidad) | 2026-11-21T02:36:47Z | 2026-11-21T02:36:47Z | 0 | TOTAL variantes=26 DETECTADAS=26 escenarios=14 (14 esperados) control_sin_alterar_ok=True todo_ok=True | `/tmp/ct/docs/fase0/cierre_tecnico_fase0/scripts_validacion/resultados/bateria_final/t409_repro.txt` | 683734df7fcdfb18 |
| t409_repro_comparacion | comparación byte a byte | 2026-11-21T02:36:47Z | 2026-11-21T02:36:47Z | 0 | IDENTICO_BYTE_A_BYTE | `/tmp/ct/docs/fase0/cierre_tecnico_fase0/scripts_validacion/resultados/bateria_final/t409_repro_cmp.txt` | 50a86dd8d80492b2 |
| t409_correspondencia | análisis de correspondencia (inferido) | 2026-11-21T02:36:47Z | 2026-11-21T02:36:47Z | 0 | 14 12 con coincidencia; 0 no establecidas | `/tmp/ct/docs/fase0/cierre_tecnico_fase0/scripts_validacion/resultados/bateria_final/t409_correspondencia.txt` | 3f0b1e881fff2375 |
| funciones_22 | MODELO en memoria | 2026-11-21T02:36:47Z | 2026-11-21T02:37:48Z | 0 | TOTAL funciones=22 casos_reportados=366 fallos=0 | `/tmp/ct/docs/fase0/cierre_tecnico_fase0/scripts_validacion/resultados/bateria_final/22_stdout.txt` | cac467d3949f2511 |
| exc_modelo14 | MODELO en memoria | 2026-11-21T02:37:48Z | 2026-11-21T02:38:40Z | 0 | TOTAL entradas EXC en las 12 mutaciones=0 | `/tmp/ct/docs/fase0/cierre_tecnico_fase0/scripts_validacion/resultados/exc_en_mutaciones_modelo14.txt` | b663615ec6bdc470 |
| catalogo_except | AST + ejecución en memoria | 2026-11-21T02:38:40Z | 2026-11-21T02:38:42Z | 0 | EQUIVALENCIA_RAMAS_MUERTAS=True | `/tmp/ct/docs/fase0/cierre_tecnico_fase0/scripts_validacion/resultados/catalogo_except_y_ramas_muertas.txt` | 25406127f826d5be |
| arnes_r1r9 | LOCAL: prueba el ARNÉS (stubs), no R1–R9 | 2026-11-21T02:38:42Z | 2026-11-21T02:38:43Z | 0 |  TOTAL pruebas_arnes=28 PASS=28 FAIL=0 | `/tmp/ct/docs/fase0/cierre_tecnico_fase0/scripts_validacion/resultados/arnes_r1r9_autoprueba_local.txt` | 200fa4e5808fcc54 |
| smoke_6_scripts | LOCAL shim/fixtures; no es Supabase | 2026-11-21T02:38:43Z | 2026-11-21T02:38:49Z | 0 |  | `/tmp/ct/docs/fase0/cierre_tecnico_fase0/scripts_validacion/resultados/bateria_final/smoke_stdout.txt` | e3b0c44298fc1c14 |
| escaner_sql | ESTÁTICA heurística | 2026-11-21T02:38:49Z | 2026-11-21T02:38:49Z | 0 | TOTAL=115 FAIL=0 | `/tmp/ct/docs/fase0/cierre_tecnico_fase0/scripts_validacion/resultados/bateria_final/escaner_sql_stdout.txt` | bf7b26abeb03bfbe |
| escaner_texto | ESTÁTICA heurística | 2026-11-21T02:38:49Z | 2026-11-21T02:38:49Z | 0 | TOTAL=571 FAIL=0 | `/tmp/ct/docs/fase0/cierre_tecnico_fase0/scripts_validacion/resultados/bateria_final/escaner_texto_stdout.txt` | 3f0f4784565c48ca |
| escaner_autoprueba | control negativo del escáner | 2026-11-21T02:38:49Z | 2026-11-21T02:38:49Z | 0 | TOTAL=26 FAIL=0 | `/tmp/ct/docs/fase0/cierre_tecnico_fase0/scripts_validacion/resultados/bateria_final/escaner_autoprueba_stdout.txt` | f6af63bdf8ac612f |

Comandos exactos: columna `comando` de `scripts_validacion/resultados/bateria_final/INDICE_BATERIA.csv`. Los pasos `smoke_6_scripts` y los controles negativos del manifiesto (`resultados/controles_negativos_manifiesto.txt`) se verifican además en `INFORME_RECONCILIACION_INTEGRAL.md`.

## Historial de fallos y correcciones (no se omiten)
Ronda anterior: (1) clúster sin `-k/-p`; (2) `\if … \else … \endif` en una línea; (3) adaptador de 22 funciones leía `(nombre, [])` como falso; (4) comparación `e in c` en T-409..T-422 (confundía I1 con I10/I11/I12) → igualdad exacta; (5) 04 v1 con 11 falsos PASS → v2; (6) 03 v1 con columna inexistente y sondas DELETE/TRUNCATE; (7) shim RLS no versionado; (8) 4 falsos positivos del escáner v1.
Esta ronda: (9) el verificador de manifiesto v1 omitía en silencio enlaces simbólicos, comparaba contra una lista permitida de «extras» sin separar la evidencia y no probaba la vía B → `ct_manifiesto.py` (36 controles negativos, incluida la vía B con `gh` simulado); (10) el HEAD final no podía contener la evidencia de su propia verificación → diseño de punto fijo (evidencia en `evidencia_verificacion/`, excluida y verificada con `--base`); (11) el contrato de error de 04 comparaba por prefijo de texto (aceptaría `RJ00` como `RJ003`) → SQLSTATE exacto (casos C23–C25); (12) el contrato de la autoprueba y el del plan eran distintos → propuesta única (`PROPUESTA_CONTRATO_ERRORES_R1_R9.md`); (13) el escáner v1 no analizaba el interior de `$$…$$` → corregido, con muestras; (14) falsos positivos del escáner v2 (palabra `EXECUTE` dentro de literales; teléfonos en UUID; muestras autocontenidas) → ajustados y probados; (15) ejecución previa con argumentos erróneos de script (sin efecto en datos).
Históricos heredados que se conservan: RV07 corrida 1 FAIL; SQL_ASCII 77/80 (DEF-ENV-01); corridas 1/2 del shim.

## Qué NO prueban
No prueban el esquema físico, RLS, privilegios, R1–R9 reales, concurrencia real ni comportamiento de Supabase. Todo PASS aquí es PASS_LOCAL / PASS_PROTOTYPE / PASS_STATIC / PASS_MODEL; **PASS_PHYSICAL = 0**. Ausencia de fallos no demuestra corrección: demuestra que las pruebas existentes no encuentran fallos.
