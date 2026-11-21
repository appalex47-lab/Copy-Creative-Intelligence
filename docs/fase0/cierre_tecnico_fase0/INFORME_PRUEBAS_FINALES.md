# INFORME DE PRUEBAS FINALES (locales) — corrección final consolidada

Entorno: PostgreSQL 16.15 temporal (clúster UTF8 C.UTF-8, socket Unix, rol `cci_test`), Python con `-I -B`. **Ninguna prueba contra Supabase/CCI-DEV/CCI-PROD.** Los resultados íntegros están en `scripts_validacion/resultados/`.

## Resultados
| Prueba | Comando (resumen) | Resultado | Archivo | Naturaleza |
|---|---|---|---|---|
| Línea base V20 | `PE_POSTGRESQL_V20/ejecutar.sh` | 63/63 PASS | base_V20_pe_utf8.txt | fixture local |
| Mutaciones V20 | `mutaciones.sh` | 14/14 detectadas | base_V20_mutaciones_utf8.txt | fixture local |
| Extensión local | `local_ext/ejecutar_ext.sh` | 80/80 PASS | ext_utf8.txt | prototipos locales |
| Concurrencia local | `ct_concurrencia_local.sh` | CC-01, CC-02 PASS | concurrencia_local_utf8.txt | local |
| Experimento DG-19 | `ct_dg19_pk_experimento.sh` | 63/63 | dg19_pk_experimento.txt | local |
| Hash encadenado | `ct_hash_cadena_referencia.py --pg` | 16/16 | hash_cadena_referencia.txt | local (pgcrypto) |
| Revisión estática T-47/T-124 | `ct_revision_estatica_T47_T124.py` | 10 PASS, 2 SIN_DATOS | revision_estatica_T47_T124.txt | **estática, textual** |
| K47 por escenario | `ct_k47_por_escenario.py` | 25/25 detectadas | k47_por_escenario.csv/.txt | modelo en memoria; mapeo inferido |
| T-409..T-422 individual | `ct_t409_t422_individual.py` | 26/26 variantes, 14 escenarios | t409_t422_individual.csv/.txt | modelo en memoria |
| 22 funciones | `ct_reejecucion_22_funciones.py` | 366 evaluaciones, 0 fallos, 0 ids repetidos (354 fixtures distintos) | 22_funciones_reejecucion_local.txt, 22_funciones_conciliacion.csv | modelo en memoria |
| EXC en mutaciones modelo14 | `ct_exc_en_mutaciones_modelo14.py` | 0 EXC en 12 mutaciones | exc_en_mutaciones_modelo14.txt | modelo |
| Catálogo `except Exception` y ramas muertas | `ct_catalogo_except_y_ramas_muertas.py` | 23 bloques (19 seguros, 4 riesgo técnico); ramas muertas equivalentes | catalogo_* | AST + ejecución en memoria |
| Arnés R1–R9 | `ct_arnes_r1r9_autoprueba.sh` | 21/21 | arnes_r1r9_autoprueba_local.txt | **prueba el arnés; funciones de relleno** |
| Smoke de los 6 scripts | `ct_smoke_scripts_cci_dev_local.sh` | guardas 7/7; 03 shim defectuoso FAIL, corregido PASS (RLS-06 NOT VERIFIED); 04 NO VERIFICABLE; 05 B PASS (3,50 s), sin tabla BLOCKED | smoke_*.txt, 04_r1r9_local_bloqueado.txt | shim local, no Supabase |
| Escáner de seguridad SQL | `ct_escaner_seguridad_sql.py` | 64 comprobaciones, 0 FAIL; control negativo 8 FAIL | escaner_seguridad_*.txt | estático, heurístico |
| Verificador de manifiesto (control negativo) | `ct_verificar_publicacion.py dir` | 5 FAIL ante manipulación | verificador_control_negativo.txt | control |
| Reconciliación integral | `ct_reconciliacion_integral.py` | ver `INFORME_RECONCILIACION_INTEGRAL.md` | reconciliacion_integral.txt | documental |

## Historial de fallos y correcciones durante esta ronda (no se omiten)
1. Primer arranque del clúster sin opciones de socket/puerto: sin socket; reiniciado con `-k`/`-p`.
2. Meta-comando `\if :{?x} … \else \set … \endif` en una línea: error de psql; convertido a forma multilínea.
3. Adaptador de las 22 funciones: 3 fallos aparentes por leer `(nombre, [])` como falso; corregido (lista vacía = OK) → 366/0.
4. Comparación `e in c` en T-409..T-422 podía confundir I1 con I10/I11/I12; sustituida por igualdad exacta.
5. Script 04 v1: falso PASS en todo negativo (11 reproducidos); reescrito (v2) y conservado v1.
6. Script 03 v1: columna inexistente `approver` y sondas DELETE/TRUNCATE ejecutables; corregido.
7. Shim RLS previo no versionado; reconstruido y versionado.
8. Escáner de seguridad: 4 FAIL iniciales, todos falsos positivos del escáner (palabras TRUNCATE/GRANT dentro de literales y nombres `role_table_grants`; comparación de posiciones entre texto con y sin comentarios). Verificado a mano y corregido el escáner (no los scripts); el control negativo confirma que sigue detectando.
9. Varias invocaciones con argumentos erróneos (rutas/socket) sin efecto en datos; repetidas con los argumentos correctos.
10. Histórico heredado: RV07 corrida 1 FAIL y SQL_ASCII 77/80 se conservan (ver LR-03, LR-11).

## Qué NO prueban estas pruebas
No prueban el esquema físico, RLS, privilegios, R1–R9 reales, concurrencia real ni comportamiento de Supabase. Todo `PASS` aquí es PASS_LOCAL / PASS_PROTOTYPE / PASS_STATIC / PASS_MODEL, **no** aceptación física.
