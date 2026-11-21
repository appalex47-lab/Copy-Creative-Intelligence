# Resultados de pruebas completos (corrida final del árbol corregido)
397 filas. Guarda: `TOTAL=187 PASS=187 FAIL=0`. Adversarial clúster 1: {('corregido', 'PASS'): 136, ('corregido', 'PARTIAL'): 6, ('publicado', 'FAIL'): 18, ('publicado', 'PASS'): 6}. Matriz adversarial completa en `MATRIZ_ADVERSARIAL_COMPLETA.md` (ejecuciones del clúster 1; el clúster 2 repite los 166 casos).

| ID | Suite | Esperado | Observado | Estado | Evidencia |
|---|---|---|---|---|---|
| H01-cluster1-v20_pe | batería | TOTAL pruebas=63 PASS=63 FAIL=0 | TOTAL pruebas=63 PASS=63 FAIL=0 rc=0 | OK | evidencia/cluster1/INDICE_BATERIA.csv |
| H01-cluster1-v20_mutaciones | batería | TOTAL mutaciones=14 DETECTADAS=14 | TOTAL mutaciones=14 DETECTADAS=14 rc=0 | OK | evidencia/cluster1/INDICE_BATERIA.csv |
| H01-cluster1-extension_local | batería | TOTAL pruebas=80 PASS=80 FAIL=0 | TOTAL pruebas=80 PASS=80 FAIL=0 rc=0 | OK | evidencia/cluster1/INDICE_BATERIA.csv |
| H01-cluster1-concurrencia_local | batería | ^CC-01 .*23P01.*err=ERROR | CC-02 \| IG1-14 numeración de versión única bajo concurrencia \| esperado: B bloqu rc=0 | OK | evidencia/cluster1/INDICE_BATERIA.csv |
| H01-cluster1-dg19 | batería | TOTAL pruebas=63 PASS=63 FAIL=0 | DG-19 PK natural: TOTAL pruebas=63 PASS=63 FAIL=0 rc=0 | OK | evidencia/cluster1/INDICE_BATERIA.csv |
| H01-cluster1-hash_encadenado | batería | TOTAL=16 PASS=16 FAIL=0 | TOTAL=16 PASS=16 FAIL=0 rc=0 | OK | evidencia/cluster1/INDICE_BATERIA.csv |
| H01-cluster1-estatica_T47_T124 | batería | TOTAL=12 PASS=10 FAIL=0 SIN_DATOS=2 | TOTAL=12 PASS=10 FAIL=0 SIN_DATOS=2 rc=0 | OK | evidencia/cluster1/INDICE_BATERIA.csv |
| H01-cluster1-k47_por_escenario | batería | DETECTADAS=25 .*todas_detectadas_con_estado_inicial_valido=True | TOTAL mutaciones mapeadas=25 DETECTADAS=25 todas_detectadas_con_estado_inicial_v rc=0 | OK | evidencia/cluster1/INDICE_BATERIA.csv |
| H01-cluster1-t409_individual | batería | DETECTADAS=26 escenarios=14 .*todo_ok=True | TOTAL variantes=26 DETECTADAS=26 escenarios=14 (14 esperados) control_sin_altera rc=0 | OK | evidencia/cluster1/INDICE_BATERIA.csv |
| H01-cluster1-t409_repro_2a_corrida | batería | DETECTADAS=26 escenarios=14 .*todo_ok=True | TOTAL variantes=26 DETECTADAS=26 escenarios=14 (14 esperados) control_sin_altera rc=0 | OK | evidencia/cluster1/INDICE_BATERIA.csv |
| H01-cluster1-t409_repro_comparacion | batería | IDENTICO_BYTE_A_BYTE | IDENTICO_BYTE_A_BYTE rc=0 | OK | evidencia/cluster1/INDICE_BATERIA.csv |
| H01-cluster1-t409_correspondencia | batería | 14 .*0 no establecidas | 14 12 con coincidencia; 0 no establecidas rc=0 | OK | evidencia/cluster1/INDICE_BATERIA.csv |
| H01-cluster1-funciones_22 | batería | TOTAL funciones=22 casos_reportados=366 fallos=0 | TOTAL funciones=22 casos_reportados=366 fallos=0 rc=0 | OK | evidencia/cluster1/INDICE_BATERIA.csv |
| H01-cluster1-exc_modelo14 | batería | TOTAL entradas EXC en las 12 mutaciones=0 | TOTAL entradas EXC en las 12 mutaciones=0 rc=0 | OK | evidencia/cluster1/INDICE_BATERIA.csv |
| H01-cluster1-catalogo_except | batería | EQUIVALENCIA_RAMAS_MUERTAS=True | EQUIVALENCIA_RAMAS_MUERTAS=True rc=0 | OK | evidencia/cluster1/INDICE_BATERIA.csv |
| H01-cluster1-arnes_r1r9 | batería | TOTAL pruebas_arnes=28 PASS=28 FAIL=0 |  TOTAL pruebas_arnes=28 PASS=28 FAIL=0 rc=0 | OK | evidencia/cluster1/INDICE_BATERIA.csv |
| H01-cluster1-smoke_6_scripts | batería | SMOKE_RC=0 | SMOKE_RC=0 rc=0 | OK | evidencia/cluster1/INDICE_BATERIA.csv |
| H01-cluster1-aserciones_smoke | batería | TOTAL=12 PASS=12 FAIL=0 | TOTAL=12 PASS=12 FAIL=0 rc=0 | OK | evidencia/cluster1/INDICE_BATERIA.csv |
| H01-cluster1-guarda_destino | batería | TOTAL=187 PASS=187 FAIL=0 | TOTAL=187 PASS=187 FAIL=0 rc=0 | OK | evidencia/cluster1/INDICE_BATERIA.csv |
| H01-cluster1-escaner_sql | batería | TOTAL=176 FAIL=0 | TOTAL=176 FAIL=0 rc=0 | OK | evidencia/cluster1/INDICE_BATERIA.csv |
| H01-cluster1-escaner_texto | batería | ^TOTAL=[0-9]+ FAIL=0 | TOTAL=781 FAIL=0 rc=0 | OK | evidencia/cluster1/INDICE_BATERIA.csv |
| H01-cluster1-escaner_autoprueba | batería | TOTAL=39 FAIL=0 | TOTAL=39 FAIL=0 rc=0 | OK | evidencia/cluster1/INDICE_BATERIA.csv |
| H01-cluster2-v20_pe | batería | TOTAL pruebas=63 PASS=63 FAIL=0 | TOTAL pruebas=63 PASS=63 FAIL=0 rc=0 | OK | evidencia/cluster2/INDICE_BATERIA.csv |
| H01-cluster2-v20_mutaciones | batería | TOTAL mutaciones=14 DETECTADAS=14 | TOTAL mutaciones=14 DETECTADAS=14 rc=0 | OK | evidencia/cluster2/INDICE_BATERIA.csv |
| H01-cluster2-extension_local | batería | TOTAL pruebas=80 PASS=80 FAIL=0 | TOTAL pruebas=80 PASS=80 FAIL=0 rc=0 | OK | evidencia/cluster2/INDICE_BATERIA.csv |
| H01-cluster2-concurrencia_local | batería | ^CC-01 .*23P01.*err=ERROR | CC-02 \| IG1-14 numeración de versión única bajo concurrencia \| esperado: B bloqu rc=0 | OK | evidencia/cluster2/INDICE_BATERIA.csv |
| H01-cluster2-dg19 | batería | TOTAL pruebas=63 PASS=63 FAIL=0 | DG-19 PK natural: TOTAL pruebas=63 PASS=63 FAIL=0 rc=0 | OK | evidencia/cluster2/INDICE_BATERIA.csv |
| H01-cluster2-hash_encadenado | batería | TOTAL=16 PASS=16 FAIL=0 | TOTAL=16 PASS=16 FAIL=0 rc=0 | OK | evidencia/cluster2/INDICE_BATERIA.csv |
| H01-cluster2-estatica_T47_T124 | batería | TOTAL=12 PASS=10 FAIL=0 SIN_DATOS=2 | TOTAL=12 PASS=10 FAIL=0 SIN_DATOS=2 rc=0 | OK | evidencia/cluster2/INDICE_BATERIA.csv |
| H01-cluster2-k47_por_escenario | batería | DETECTADAS=25 .*todas_detectadas_con_estado_inicial_valido=True | TOTAL mutaciones mapeadas=25 DETECTADAS=25 todas_detectadas_con_estado_inicial_v rc=0 | OK | evidencia/cluster2/INDICE_BATERIA.csv |
| H01-cluster2-t409_individual | batería | DETECTADAS=26 escenarios=14 .*todo_ok=True | TOTAL variantes=26 DETECTADAS=26 escenarios=14 (14 esperados) control_sin_altera rc=0 | OK | evidencia/cluster2/INDICE_BATERIA.csv |
| H01-cluster2-t409_repro_2a_corrida | batería | DETECTADAS=26 escenarios=14 .*todo_ok=True | TOTAL variantes=26 DETECTADAS=26 escenarios=14 (14 esperados) control_sin_altera rc=0 | OK | evidencia/cluster2/INDICE_BATERIA.csv |
| H01-cluster2-t409_repro_comparacion | batería | IDENTICO_BYTE_A_BYTE | IDENTICO_BYTE_A_BYTE rc=0 | OK | evidencia/cluster2/INDICE_BATERIA.csv |
| H01-cluster2-t409_correspondencia | batería | 14 .*0 no establecidas | 14 12 con coincidencia; 0 no establecidas rc=0 | OK | evidencia/cluster2/INDICE_BATERIA.csv |
| H01-cluster2-funciones_22 | batería | TOTAL funciones=22 casos_reportados=366 fallos=0 | TOTAL funciones=22 casos_reportados=366 fallos=0 rc=0 | OK | evidencia/cluster2/INDICE_BATERIA.csv |
| H01-cluster2-exc_modelo14 | batería | TOTAL entradas EXC en las 12 mutaciones=0 | TOTAL entradas EXC en las 12 mutaciones=0 rc=0 | OK | evidencia/cluster2/INDICE_BATERIA.csv |
| H01-cluster2-catalogo_except | batería | EQUIVALENCIA_RAMAS_MUERTAS=True | EQUIVALENCIA_RAMAS_MUERTAS=True rc=0 | OK | evidencia/cluster2/INDICE_BATERIA.csv |
| H01-cluster2-arnes_r1r9 | batería | TOTAL pruebas_arnes=28 PASS=28 FAIL=0 |  TOTAL pruebas_arnes=28 PASS=28 FAIL=0 rc=0 | OK | evidencia/cluster2/INDICE_BATERIA.csv |
| H01-cluster2-smoke_6_scripts | batería | SMOKE_RC=0 | SMOKE_RC=0 rc=0 | OK | evidencia/cluster2/INDICE_BATERIA.csv |
| H01-cluster2-aserciones_smoke | batería | TOTAL=12 PASS=12 FAIL=0 | TOTAL=12 PASS=12 FAIL=0 rc=0 | OK | evidencia/cluster2/INDICE_BATERIA.csv |
| H01-cluster2-guarda_destino | batería | TOTAL=187 PASS=187 FAIL=0 | TOTAL=187 PASS=187 FAIL=0 rc=0 | OK | evidencia/cluster2/INDICE_BATERIA.csv |
| H01-cluster2-escaner_sql | batería | TOTAL=176 FAIL=0 | TOTAL=176 FAIL=0 rc=0 | OK | evidencia/cluster2/INDICE_BATERIA.csv |
| H01-cluster2-escaner_texto | batería | ^TOTAL=[0-9]+ FAIL=0 | TOTAL=751 FAIL=0 rc=0 | OK | evidencia/cluster2/INDICE_BATERIA.csv |
| H01-cluster2-escaner_autoprueba | batería | TOTAL=39 FAIL=0 | TOTAL=39 FAIL=0 rc=0 | OK | evidencia/cluster2/INDICE_BATERIA.csv |
| GD-00 | guarda_destino | esperado: dígitos | obtenido: huella md5=67e8231f | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-01 | guarda_destino | esperado: GUARDA OK modo=SI-CCI-DEV y rc=0 | obtenido: rc=0 guarda_ok=True | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-01 | guarda_destino | esperado: GUARDA OK modo=SI-CCI-DEV y rc=0 | obtenido: rc=0 guarda_ok=True | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-01 | guarda_destino | esperado: GUARDA OK modo=SI-CCI-DEV | obtenido: rc=0 guarda_ok=True | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-01 | guarda_destino | esperado: GUARDA OK modo=SI-CCI-DEV | obtenido: rc=3 guarda_ok=True | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-01 | guarda_destino | esperado: GUARDA OK modo=SI-CCI-DEV | obtenido: rc=0 guarda_ok=True | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-01 | guarda_destino | esperado: GUARDA OK modo=SI-CCI-DEV | obtenido: rc=0 guarda_ok=True | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-02 | guarda_destino | esperado: rechazo [G-PROD-RECHAZADO], rc!=0, sin datos | obtenido: rc=3 [G-PROD-RECHAZADO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-02 | guarda_destino | esperado: rechazo [G-PROD-RECHAZADO], rc!=0, sin datos | obtenido: rc=3 [G-PROD-RECHAZADO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-02 | guarda_destino | esperado: rechazo [G-PROD-RECHAZADO], rc!=0, sin datos | obtenido: rc=3 [G-PROD-RECHAZADO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-02 | guarda_destino | esperado: rechazo [G-PROD-RECHAZADO], rc!=0, sin datos | obtenido: rc=3 [G-PROD-RECHAZADO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-02 | guarda_destino | esperado: rechazo [G-PROD-RECHAZADO], rc!=0, sin datos | obtenido: rc=3 [G-PROD-RECHAZADO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-02 | guarda_destino | esperado: rechazo [G-PROD-RECHAZADO], rc!=0, sin datos | obtenido: rc=3 [G-PROD-RECHAZADO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-02b | guarda_destino | esperado: rechazo [G-PROD-RECHAZADO], rc!=0, sin datos | obtenido: rc=3 [G-PROD-RECHAZADO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-03a | guarda_destino | esperado: rechazo [G-DESTINO-DESCONOCIDO], rc!=0, sin datos | obtenido: rc=3 [G-DESTINO-DESCONOCIDO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-03a | guarda_destino | esperado: rechazo [G-DESTINO-DESCONOCIDO], rc!=0, sin datos | obtenido: rc=3 [G-DESTINO-DESCONOCIDO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-03a | guarda_destino | esperado: rechazo [G-DESTINO-DESCONOCIDO], rc!=0, sin datos | obtenido: rc=3 [G-DESTINO-DESCONOCIDO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-03a | guarda_destino | esperado: rechazo [G-DESTINO-DESCONOCIDO], rc!=0, sin datos | obtenido: rc=3 [G-DESTINO-DESCONOCIDO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-03a | guarda_destino | esperado: rechazo [G-DESTINO-DESCONOCIDO], rc!=0, sin datos | obtenido: rc=3 [G-DESTINO-DESCONOCIDO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-03a | guarda_destino | esperado: rechazo [G-DESTINO-DESCONOCIDO], rc!=0, sin datos | obtenido: rc=3 [G-DESTINO-DESCONOCIDO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-03b | guarda_destino | esperado: rechazo [G-DESTINO-DESCONOCIDO], rc!=0, sin datos | obtenido: rc=3 [G-DESTINO-DESCONOCIDO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-03b | guarda_destino | esperado: rechazo [G-DESTINO-DESCONOCIDO], rc!=0, sin datos | obtenido: rc=3 [G-DESTINO-DESCONOCIDO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-03b | guarda_destino | esperado: rechazo [G-DESTINO-DESCONOCIDO], rc!=0, sin datos | obtenido: rc=3 [G-DESTINO-DESCONOCIDO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-03b | guarda_destino | esperado: rechazo [G-DESTINO-DESCONOCIDO], rc!=0, sin datos | obtenido: rc=3 [G-DESTINO-DESCONOCIDO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-03b | guarda_destino | esperado: rechazo [G-DESTINO-DESCONOCIDO], rc!=0, sin datos | obtenido: rc=3 [G-DESTINO-DESCONOCIDO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-03b | guarda_destino | esperado: rechazo [G-DESTINO-DESCONOCIDO], rc!=0, sin datos | obtenido: rc=3 [G-DESTINO-DESCONOCIDO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-03c | guarda_destino | esperado: rechazo [G-DESTINO-DESCONOCIDO], rc!=0, sin datos | obtenido: rc=3 [G-DESTINO-DESCONOCIDO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-03c | guarda_destino | esperado: rechazo [G-DESTINO-DESCONOCIDO], rc!=0, sin datos | obtenido: rc=3 [G-DESTINO-DESCONOCIDO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-03c | guarda_destino | esperado: rechazo [G-DESTINO-DESCONOCIDO], rc!=0, sin datos | obtenido: rc=3 [G-DESTINO-DESCONOCIDO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-03c | guarda_destino | esperado: rechazo [G-DESTINO-DESCONOCIDO], rc!=0, sin datos | obtenido: rc=3 [G-DESTINO-DESCONOCIDO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-03c | guarda_destino | esperado: rechazo [G-DESTINO-DESCONOCIDO], rc!=0, sin datos | obtenido: rc=3 [G-DESTINO-DESCONOCIDO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-03c | guarda_destino | esperado: rechazo [G-DESTINO-DESCONOCIDO], rc!=0, sin datos | obtenido: rc=3 [G-DESTINO-DESCONOCIDO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-04 | guarda_destino | esperado: rechazo [G-PROD-RECHAZADO], rc!=0, sin datos | obtenido: rc=3 [G-PROD-RECHAZADO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-04 | guarda_destino | esperado: rechazo [G-PROD-RECHAZADO], rc!=0, sin datos | obtenido: rc=3 [G-PROD-RECHAZADO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-04 | guarda_destino | esperado: rechazo [G-PROD-RECHAZADO], rc!=0, sin datos | obtenido: rc=3 [G-PROD-RECHAZADO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-04 | guarda_destino | esperado: rechazo [G-PROD-RECHAZADO], rc!=0, sin datos | obtenido: rc=3 [G-PROD-RECHAZADO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-04 | guarda_destino | esperado: rechazo [G-PROD-RECHAZADO], rc!=0, sin datos | obtenido: rc=3 [G-PROD-RECHAZADO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-04 | guarda_destino | esperado: rechazo [G-PROD-RECHAZADO], rc!=0, sin datos | obtenido: rc=3 [G-PROD-RECHAZADO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-05 | guarda_destino | esperado: rechazo [G-IDENTIDAD-NO-VERIFICABLE], rc!=0, sin datos | obtenido: rc=3 [G-IDENTIDAD-NO-VERIFICABLE] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-05 | guarda_destino | esperado: rechazo [G-IDENTIDAD-NO-VERIFICABLE], rc!=0, sin datos | obtenido: rc=3 [G-IDENTIDAD-NO-VERIFICABLE] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-05 | guarda_destino | esperado: rechazo [G-IDENTIDAD-NO-VERIFICABLE], rc!=0, sin datos | obtenido: rc=3 [G-IDENTIDAD-NO-VERIFICABLE] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-05 | guarda_destino | esperado: rechazo [G-IDENTIDAD-NO-VERIFICABLE], rc!=0, sin datos | obtenido: rc=3 [G-IDENTIDAD-NO-VERIFICABLE] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-05 | guarda_destino | esperado: rechazo [G-IDENTIDAD-NO-VERIFICABLE], rc!=0, sin datos | obtenido: rc=3 [G-IDENTIDAD-NO-VERIFICABLE] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-05 | guarda_destino | esperado: rechazo [G-IDENTIDAD-NO-VERIFICABLE], rc!=0, sin datos | obtenido: rc=3 [G-IDENTIDAD-NO-VERIFICABLE] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-05b | guarda_destino | esperado: rechazo [G-IDENTIDAD-NO-VERIFICABLE], rc!=0, sin datos | obtenido: rc=3 [G-IDENTIDAD-NO-VERIFICABLE] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-06a | guarda_destino | esperado: rechazo [G-CONFIG-INCOMPLETA], rc!=0, sin datos | obtenido: rc=3 [G-CONFIG-INCOMPLETA] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-06a | guarda_destino | esperado: rechazo [G-CONFIG-INCOMPLETA], rc!=0, sin datos | obtenido: rc=3 [G-CONFIG-INCOMPLETA] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-06a | guarda_destino | esperado: rechazo [G-CONFIG-INCOMPLETA], rc!=0, sin datos | obtenido: rc=3 [G-CONFIG-INCOMPLETA] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-06a | guarda_destino | esperado: rechazo [G-CONFIG-INCOMPLETA], rc!=0, sin datos | obtenido: rc=3 [G-CONFIG-INCOMPLETA] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-06a | guarda_destino | esperado: rechazo [G-CONFIG-INCOMPLETA], rc!=0, sin datos | obtenido: rc=3 [G-CONFIG-INCOMPLETA] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-06a | guarda_destino | esperado: rechazo [G-CONFIG-INCOMPLETA], rc!=0, sin datos | obtenido: rc=3 [G-CONFIG-INCOMPLETA] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-06b | guarda_destino | esperado: rechazo [G-CONFIG-INCOMPLETA], rc!=0, sin datos | obtenido: rc=3 [G-CONFIG-INCOMPLETA] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-06c | guarda_destino | esperado: rechazo [G-CONFIG-INCOMPLETA], rc!=0, sin datos | obtenido: rc=3 [G-CONFIG-INCOMPLETA] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-06d | guarda_destino | esperado: rechazo [G-CONFIG-INVALIDA], rc!=0, sin datos | obtenido: rc=3 [G-CONFIG-INVALIDA] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-06e | guarda_destino | esperado: rechazo [G-CONFIG-INVALIDA], rc!=0, sin datos | obtenido: rc=3 [G-CONFIG-INVALIDA] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-07a | guarda_destino | esperado: rechazo [G-DESTINO-DESCONOCIDO], rc!=0, sin datos | obtenido: rc=3 [G-DESTINO-DESCONOCIDO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-07b | guarda_destino | esperado: rechazo [G-PROD-RECHAZADO], rc!=0, sin datos | obtenido: rc=3 [G-PROD-RECHAZADO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-07c | guarda_destino | esperado: rechazo [G-PROD-RECHAZADO], rc!=0, sin datos | obtenido: rc=3 [G-PROD-RECHAZADO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-07c | guarda_destino | esperado: rechazo [G-PROD-RECHAZADO], rc!=0, sin datos | obtenido: rc=3 [G-PROD-RECHAZADO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-07c | guarda_destino | esperado: rechazo [G-PROD-RECHAZADO], rc!=0, sin datos | obtenido: rc=3 [G-PROD-RECHAZADO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-07c | guarda_destino | esperado: rechazo [G-PROD-RECHAZADO], rc!=0, sin datos | obtenido: rc=3 [G-PROD-RECHAZADO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-07c | guarda_destino | esperado: rechazo [G-PROD-RECHAZADO], rc!=0, sin datos | obtenido: rc=3 [G-PROD-RECHAZADO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-07c | guarda_destino | esperado: rechazo [G-PROD-RECHAZADO], rc!=0, sin datos | obtenido: rc=3 [G-PROD-RECHAZADO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-07c2 | guarda_destino | esperado: rechazo [G-SEARCH-PATH-NO-SEGURO], rc!=0, sin datos | obtenido: rc=3 [G-SEARCH-PATH-NO-SEGURO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-07c2 | guarda_destino | esperado: rechazo [G-SEARCH-PATH-NO-SEGURO], rc!=0, sin datos | obtenido: rc=3 [G-SEARCH-PATH-NO-SEGURO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-07d | guarda_destino | esperado: rechazo [G-LOCAL-ROLES-PLATAFORMA], rc!=0, sin datos | obtenido: rc=3 [G-LOCAL-ROLES-PLATAFORMA] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-07d | guarda_destino | esperado: rechazo [G-LOCAL-ROLES-PLATAFORMA], rc!=0, sin datos | obtenido: rc=3 [G-LOCAL-ROLES-PLATAFORMA] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-07d | guarda_destino | esperado: rechazo [G-LOCAL-ROLES-PLATAFORMA], rc!=0, sin datos | obtenido: rc=3 [G-LOCAL-ROLES-PLATAFORMA] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-07d | guarda_destino | esperado: rechazo [G-LOCAL-ROLES-PLATAFORMA], rc!=0, sin datos | obtenido: rc=3 [G-LOCAL-ROLES-PLATAFORMA] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-07d | guarda_destino | esperado: rechazo [G-LOCAL-ROLES-PLATAFORMA], rc!=0, sin datos | obtenido: rc=3 [G-LOCAL-ROLES-PLATAFORMA] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-07d | guarda_destino | esperado: rechazo [G-LOCAL-ROLES-PLATAFORMA], rc!=0, sin datos | obtenido: rc=3 [G-LOCAL-ROLES-PLATAFORMA] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-07e | guarda_destino | esperado: rechazo [G-LOCAL-BASE], rc!=0, sin datos | obtenido: rc=3 [G-LOCAL-BASE] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-07e | guarda_destino | esperado: rechazo [G-LOCAL-BASE], rc!=0, sin datos | obtenido: rc=3 [G-LOCAL-BASE] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-07e | guarda_destino | esperado: rechazo [G-LOCAL-BASE], rc!=0, sin datos | obtenido: rc=3 [G-LOCAL-BASE] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-07e | guarda_destino | esperado: rechazo [G-LOCAL-BASE], rc!=0, sin datos | obtenido: rc=3 [G-LOCAL-BASE] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-07e | guarda_destino | esperado: rechazo [G-LOCAL-BASE], rc!=0, sin datos | obtenido: rc=3 [G-LOCAL-BASE] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-07e | guarda_destino | esperado: rechazo [G-LOCAL-BASE], rc!=0, sin datos | obtenido: rc=3 [G-LOCAL-BASE] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-08 | guarda_destino | esperado: rc!=0 [G-GUARDA-INTEGRIDAD] y sin datos | obtenido: rc=3 | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-08 | guarda_destino | esperado: rc!=0 [G-GUARDA-INTEGRIDAD] y sin datos | obtenido: rc=3 | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-08 | guarda_destino | esperado: rc!=0 [G-GUARDA-INTEGRIDAD] y sin datos | obtenido: rc=3 | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-08 | guarda_destino | esperado: rc!=0 [G-GUARDA-INTEGRIDAD] y sin datos | obtenido: rc=3 | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-08 | guarda_destino | esperado: rc!=0 [G-GUARDA-INTEGRIDAD] y sin datos | obtenido: rc=3 | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-08 | guarda_destino | esperado: rc!=0 [G-GUARDA-INTEGRIDAD] y sin datos | obtenido: rc=3 | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-13 | guarda_destino | esperado: rechazo [G-GUARDA-NO-EJECUTADA], rc!=0, sin datos | obtenido: rc=3 [G-GUARDA-NO-EJECUTADA] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-13 | guarda_destino | esperado: rechazo [G-GUARDA-NO-EJECUTADA], rc!=0, sin datos | obtenido: rc=3 [G-GUARDA-NO-EJECUTADA] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-13 | guarda_destino | esperado: rechazo [G-GUARDA-NO-EJECUTADA], rc!=0, sin datos | obtenido: rc=3 [G-GUARDA-NO-EJECUTADA] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-13 | guarda_destino | esperado: rechazo [G-GUARDA-NO-EJECUTADA], rc!=0, sin datos | obtenido: rc=3 [G-GUARDA-NO-EJECUTADA] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-13 | guarda_destino | esperado: rechazo [G-GUARDA-NO-EJECUTADA], rc!=0, sin datos | obtenido: rc=3 [G-GUARDA-NO-EJECUTADA] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-13 | guarda_destino | esperado: rechazo [G-GUARDA-NO-EJECUTADA], rc!=0, sin datos | obtenido: rc=3 [G-GUARDA-NO-EJECUTADA] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-13 | guarda_destino | esperado: rechazo [G-GUARDA-NO-EJECUTADA], rc!=0, sin datos | obtenido: rc=3 [G-GUARDA-NO-EJECUTADA] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-13 | guarda_destino | esperado: rechazo [G-GUARDA-NO-EJECUTADA], rc!=0, sin datos | obtenido: rc=3 [G-GUARDA-NO-EJECUTADA] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-13 | guarda_destino | esperado: rechazo [G-GUARDA-NO-EJECUTADA], rc!=0, sin datos | obtenido: rc=3 [G-GUARDA-NO-EJECUTADA] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-13 | guarda_destino | esperado: rechazo [G-GUARDA-NO-EJECUTADA], rc!=0, sin datos | obtenido: rc=3 [G-GUARDA-NO-EJECUTADA] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-13 | guarda_destino | esperado: rechazo [G-GUARDA-NO-EJECUTADA], rc!=0, sin datos | obtenido: rc=3 [G-GUARDA-NO-EJECUTADA] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-13 | guarda_destino | esperado: rechazo [G-GUARDA-NO-EJECUTADA], rc!=0, sin datos | obtenido: rc=3 [G-GUARDA-NO-EJECUTADA] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-13 | guarda_destino | esperado: rechazo [G-GUARDA-NO-EJECUTADA], rc!=0, sin datos | obtenido: rc=3 [G-GUARDA-NO-EJECUTADA] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-13 | guarda_destino | esperado: rechazo [G-GUARDA-NO-EJECUTADA], rc!=0, sin datos | obtenido: rc=3 [G-GUARDA-NO-EJECUTADA] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-13 | guarda_destino | esperado: rechazo [G-GUARDA-NO-EJECUTADA], rc!=0, sin datos | obtenido: rc=3 [G-GUARDA-NO-EJECUTADA] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-13 | guarda_destino | esperado: rechazo [G-GUARDA-NO-EJECUTADA], rc!=0, sin datos | obtenido: rc=3 [G-GUARDA-NO-EJECUTADA] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-13 | guarda_destino | esperado: rechazo [G-GUARDA-NO-EJECUTADA], rc!=0, sin datos | obtenido: rc=3 [G-GUARDA-NO-EJECUTADA] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-13 | guarda_destino | esperado: rechazo [G-GUARDA-NO-EJECUTADA], rc!=0, sin datos | obtenido: rc=3 [G-GUARDA-NO-EJECUTADA] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-14 | guarda_destino | esperado: rc!=0 y sin datos | obtenido: rc=3 | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-14 | guarda_destino | esperado: rc!=0 y sin datos | obtenido: rc=3 | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-14 | guarda_destino | esperado: rc!=0 y sin datos | obtenido: rc=3 | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-14 | guarda_destino | esperado: rc!=0 y sin datos | obtenido: rc=3 | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-14 | guarda_destino | esperado: rc!=0 y sin datos | obtenido: rc=3 | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-14 | guarda_destino | esperado: rc!=0 y sin datos | obtenido: rc=3 | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-15 | guarda_destino | esperado: SPVAL=public,pg_temp (comportamiento documentado) | obtenido: SPVAL=public,pg_temp | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-15 | guarda_destino | esperado: SPVAL=public,pg_temp (comportamiento documentado) | obtenido: SPVAL=public,pg_temp | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-15 | guarda_destino | esperado: SPVAL=public,pg_temp (comportamiento documentado) | obtenido: SPVAL=public,pg_temp | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-15 | guarda_destino | esperado: SPVAL=public,pg_temp (comportamiento documentado) | obtenido: SPVAL=public,pg_temp | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-15 | guarda_destino | esperado: SPVAL=public,pg_temp (comportamiento documentado) | obtenido: SPVAL=public,pg_temp | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-15 | guarda_destino | esperado: SPVAL=public,pg_temp (comportamiento documentado) | obtenido: SPVAL=public,pg_temp | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-19 | guarda_destino | esperado: rechazo [G-SEARCH-PATH-NO-SEGURO], rc!=0, sin datos | obtenido: rc=3 [G-SEARCH-PATH-NO-SEGURO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-19 | guarda_destino | esperado: rechazo [G-SEARCH-PATH-NO-SEGURO], rc!=0, sin datos | obtenido: rc=3 [G-SEARCH-PATH-NO-SEGURO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-19 | guarda_destino | esperado: rechazo [G-SEARCH-PATH-NO-SEGURO], rc!=0, sin datos | obtenido: rc=3 [G-SEARCH-PATH-NO-SEGURO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-19 | guarda_destino | esperado: rechazo [G-SEARCH-PATH-NO-SEGURO], rc!=0, sin datos | obtenido: rc=3 [G-SEARCH-PATH-NO-SEGURO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-19 | guarda_destino | esperado: rechazo [G-SEARCH-PATH-NO-SEGURO], rc!=0, sin datos | obtenido: rc=3 [G-SEARCH-PATH-NO-SEGURO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-19 | guarda_destino | esperado: rechazo [G-SEARCH-PATH-NO-SEGURO], rc!=0, sin datos | obtenido: rc=3 [G-SEARCH-PATH-NO-SEGURO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-19b | guarda_destino | esperado: GUARDA OK y sin HIJACK-INVOCADO | obtenido: guarda_ok=True hijack=False | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-19b | guarda_destino | esperado: GUARDA OK y sin HIJACK-INVOCADO | obtenido: guarda_ok=True hijack=False | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-19b | guarda_destino | esperado: GUARDA OK y sin HIJACK-INVOCADO | obtenido: guarda_ok=True hijack=False | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-19b | guarda_destino | esperado: GUARDA OK y sin HIJACK-INVOCADO | obtenido: guarda_ok=True hijack=False | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-19b | guarda_destino | esperado: GUARDA OK y sin HIJACK-INVOCADO | obtenido: guarda_ok=True hijack=False | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-19b | guarda_destino | esperado: GUARDA OK y sin HIJACK-INVOCADO | obtenido: guarda_ok=True hijack=False | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-21 | guarda_destino | esperado: rechazo [G-SEARCH-PATH-NO-SEGURO], rc!=0, sin datos | obtenido: rc=3 [G-SEARCH-PATH-NO-SEGURO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-21 | guarda_destino | esperado: rechazo [G-SEARCH-PATH-NO-SEGURO], rc!=0, sin datos | obtenido: rc=3 [G-SEARCH-PATH-NO-SEGURO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-21 | guarda_destino | esperado: rechazo [G-SEARCH-PATH-NO-SEGURO], rc!=0, sin datos | obtenido: rc=3 [G-SEARCH-PATH-NO-SEGURO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-21 | guarda_destino | esperado: rechazo [G-SEARCH-PATH-NO-SEGURO], rc!=0, sin datos | obtenido: rc=3 [G-SEARCH-PATH-NO-SEGURO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-21 | guarda_destino | esperado: rechazo [G-SEARCH-PATH-NO-SEGURO], rc!=0, sin datos | obtenido: rc=3 [G-SEARCH-PATH-NO-SEGURO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-21 | guarda_destino | esperado: rechazo [G-SEARCH-PATH-NO-SEGURO], rc!=0, sin datos | obtenido: rc=3 [G-SEARCH-PATH-NO-SEGURO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-21 | guarda_destino | esperado: rechazo [G-SEARCH-PATH-NO-SEGURO], rc!=0, sin datos | obtenido: rc=3 [G-SEARCH-PATH-NO-SEGURO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-21 | guarda_destino | esperado: rechazo [G-SEARCH-PATH-NO-SEGURO], rc!=0, sin datos | obtenido: rc=3 [G-SEARCH-PATH-NO-SEGURO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-21e | guarda_destino | esperado: rechazo [G-SEARCH-PATH-NO-SEGURO], rc!=0, sin datos | obtenido: rc=3 [G-SEARCH-PATH-NO-SEGURO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-21e | guarda_destino | esperado: rechazo [G-SEARCH-PATH-NO-SEGURO], rc!=0, sin datos | obtenido: rc=3 [G-SEARCH-PATH-NO-SEGURO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-21e | guarda_destino | esperado: rechazo [G-SEARCH-PATH-NO-SEGURO], rc!=0, sin datos | obtenido: rc=3 [G-SEARCH-PATH-NO-SEGURO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-21e | guarda_destino | esperado: rechazo [G-SEARCH-PATH-NO-SEGURO], rc!=0, sin datos | obtenido: rc=3 [G-SEARCH-PATH-NO-SEGURO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-21f | guarda_destino | esperado: GUARDA OK, rc=0 | obtenido: rc=0 | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-21f | guarda_destino | esperado: GUARDA OK, rc=0 | obtenido: rc=0 | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-21f | guarda_destino | esperado: GUARDA OK, rc=0 | obtenido: rc=0 | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-21f | guarda_destino | esperado: GUARDA OK, rc=0 | obtenido: rc=0 | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-21f | guarda_destino | esperado: GUARDA OK, rc=0 | obtenido: rc=0 | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-21f | guarda_destino | esperado: GUARDA OK, rc=0 | obtenido: rc=0 | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-21f | guarda_destino | esperado: GUARDA OK, rc=0 | obtenido: rc=0 | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-21f | guarda_destino | esperado: GUARDA OK, rc=0 | obtenido: rc=0 | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-21b | guarda_destino | esperado: rechazo [G-SEARCH-PATH-NO-SEGURO], rc!=0, sin datos | obtenido: rc=3 [G-SEARCH-PATH-NO-SEGURO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-21b | guarda_destino | esperado: rechazo [G-SEARCH-PATH-NO-SEGURO], rc!=0, sin datos | obtenido: rc=3 [G-SEARCH-PATH-NO-SEGURO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-21c | guarda_destino | esperado: rechazo [G-SEARCH-PATH-NO-SEGURO], rc!=0, sin datos | obtenido: rc=3 [G-SEARCH-PATH-NO-SEGURO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-21c | guarda_destino | esperado: rechazo [G-SEARCH-PATH-NO-SEGURO], rc!=0, sin datos | obtenido: rc=3 [G-SEARCH-PATH-NO-SEGURO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-21d | guarda_destino | esperado: rechazo [G-SEARCH-PATH-NO-SEGURO], rc!=0, sin datos | obtenido: rc=3 [G-SEARCH-PATH-NO-SEGURO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-21d | guarda_destino | esperado: rechazo [G-SEARCH-PATH-NO-SEGURO], rc!=0, sin datos | obtenido: rc=3 [G-SEARCH-PATH-NO-SEGURO] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-16 | guarda_destino | esperado: rechazo [G-GUARDA-NO-EJECUTADA], rc!=0, sin datos | obtenido: rc=3 [G-GUARDA-NO-EJECUTADA] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-16 | guarda_destino | esperado: rechazo [G-GUARDA-NO-EJECUTADA], rc!=0, sin datos | obtenido: rc=3 [G-GUARDA-NO-EJECUTADA] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-16 | guarda_destino | esperado: rechazo [G-GUARDA-NO-EJECUTADA], rc!=0, sin datos | obtenido: rc=3 [G-GUARDA-NO-EJECUTADA] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-16 | guarda_destino | esperado: rechazo [G-GUARDA-NO-EJECUTADA], rc!=0, sin datos | obtenido: rc=3 [G-GUARDA-NO-EJECUTADA] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-16 | guarda_destino | esperado: rechazo [G-GUARDA-NO-EJECUTADA], rc!=0, sin datos | obtenido: rc=3 [G-GUARDA-NO-EJECUTADA] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-16 | guarda_destino | esperado: rechazo [G-GUARDA-NO-EJECUTADA], rc!=0, sin datos | obtenido: rc=3 [G-GUARDA-NO-EJECUTADA] | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-17 | guarda_destino | esperado: el script corre (límite documentado, no es aprobación) | obtenido: rc=0 | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-17b | guarda_destino | esperado: rc!=0 [G-GUARDA-INTEGRIDAD] | obtenido: rc=3 | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-20 | guarda_destino | esperado: rc!=0 [G-GUARDA-INTEGRIDAD] | obtenido: rc=3 | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-20 | guarda_destino | esperado: rc!=0 [G-GUARDA-INTEGRIDAD] | obtenido: rc=3 | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-20 | guarda_destino | esperado: rc!=0 [G-GUARDA-INTEGRIDAD] | obtenido: rc=3 | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-20 | guarda_destino | esperado: rc!=0 [G-GUARDA-INTEGRIDAD] | obtenido: rc=3 | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-20 | guarda_destino | esperado: rc!=0 [G-GUARDA-INTEGRIDAD] | obtenido: rc=3 | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-20 | guarda_destino | esperado: rc!=0 [G-GUARDA-INTEGRIDAD] | obtenido: rc=3 | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-20 | guarda_destino | esperado: rc!=0 [G-GUARDA-INTEGRIDAD] | obtenido: rc=3 | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-20 | guarda_destino | esperado: rc!=0 [G-GUARDA-INTEGRIDAD] | obtenido: rc=3 | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-20 | guarda_destino | esperado: rc!=0 [G-GUARDA-INTEGRIDAD] | obtenido: rc=3 | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-20 | guarda_destino | esperado: rc!=0 [G-GUARDA-INTEGRIDAD] | obtenido: rc=3 | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-20 | guarda_destino | esperado: rc!=0 [G-GUARDA-INTEGRIDAD] | obtenido: rc=3 | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-20 | guarda_destino | esperado: rc!=0 [G-GUARDA-INTEGRIDAD] | obtenido: rc=3 | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-20 | guarda_destino | esperado: rc!=0 [G-GUARDA-INTEGRIDAD] | obtenido: rc=3 | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-20 | guarda_destino | esperado: rc!=0 [G-GUARDA-INTEGRIDAD] | obtenido: rc=3 | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-20 | guarda_destino | esperado: rc!=0 [G-GUARDA-INTEGRIDAD] | obtenido: rc=3 | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-20 | guarda_destino | esperado: rc!=0 [G-GUARDA-INTEGRIDAD] | obtenido: rc=3 | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-20 | guarda_destino | esperado: rc!=0 [G-GUARDA-INTEGRIDAD] | obtenido: rc=3 | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-20 | guarda_destino | esperado: rc!=0 [G-GUARDA-INTEGRIDAD] | obtenido: rc=3 | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-20 | guarda_destino | esperado: rc!=0 [G-GUARDA-INTEGRIDAD] | obtenido: rc=3 | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-20 | guarda_destino | esperado: rc!=0 [G-GUARDA-INTEGRIDAD] | obtenido: rc=3 | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-20 | guarda_destino | esperado: rc!=0 [G-GUARDA-INTEGRIDAD] | obtenido: rc=3 | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-20 | guarda_destino | esperado: rc!=0 [G-GUARDA-INTEGRIDAD] | obtenido: rc=3 | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-20 | guarda_destino | esperado: rc!=0 [G-GUARDA-INTEGRIDAD] | obtenido: rc=3 | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-20 | guarda_destino | esperado: rc!=0 [G-GUARDA-INTEGRIDAD] | obtenido: rc=3 | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-09 | guarda_destino | esperado: rc=0 y GUARDA OK | obtenido: rc=0 | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-11 | guarda_destino | esperado: guarda débil ACEPTA el destino PROD | obtenido: rc=0 | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-12 | guarda_destino | esperado: guarda anterior ACEPTA (vulnerable) | obtenido: rc=0 | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| GD-10 | guarda_destino | esperado: ambas vacías, sin números largos | obtenido: ok | PASS | evidencia/guarda_destino_187_arbol_final.txt |
| CTRL-cor-01/cluster2 | adversarial | llega al cuerpo | CUERPO EJECUTADO rc=0  | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| CTRL-cor-02/cluster2 | adversarial | llega al cuerpo | CUERPO EJECUTADO rc=0  | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| CTRL-cor-03/cluster2 | adversarial | llega al cuerpo | CUERPO EJECUTADO rc=0  | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| CTRL-cor-04/cluster2 | adversarial | llega al cuerpo | CUERPO EJECUTADO rc=3 ERROR:  syntax error at or near ":" | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| CTRL-cor-05A/cluster2 | adversarial | llega al cuerpo | CUERPO EJECUTADO rc=0  | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| CTRL-cor-05B/cluster2 | adversarial | llega al cuerpo | CUERPO EJECUTADO rc=0  | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| A-cor-01/cluster2 | adversarial | rechazo [G-GUARDA-NO-EJECUTADA] | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| A-cor-02/cluster2 | adversarial | rechazo [G-GUARDA-NO-EJECUTADA] | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| A-cor-03/cluster2 | adversarial | rechazo [G-GUARDA-NO-EJECUTADA] | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| A-cor-04/cluster2 | adversarial | rechazo [G-GUARDA-NO-EJECUTADA] | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| A-cor-05A/cluster2 | adversarial | rechazo [G-GUARDA-NO-EJECUTADA] | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| A-cor-05B/cluster2 | adversarial | rechazo [G-GUARDA-NO-EJECUTADA] | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| B-cor-01/cluster2 | adversarial | rechazo (el preflight borra cci_run; la guarda vacía no la regenera) | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| B-cor-02/cluster2 | adversarial | rechazo (el preflight borra cci_run; la guarda vacía no la regenera) | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| B-cor-03/cluster2 | adversarial | rechazo (el preflight borra cci_run; la guarda vacía no la regenera) | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| B-cor-04/cluster2 | adversarial | rechazo (el preflight borra cci_run; la guarda vacía no la regenera) | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| B-cor-05A/cluster2 | adversarial | rechazo (el preflight borra cci_run; la guarda vacía no la regenera) | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| B-cor-05B/cluster2 | adversarial | rechazo (el preflight borra cci_run; la guarda vacía no la regenera) | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| C-cor-01/cluster2 | adversarial | la 2.ª ejecución no hereda autorización: ejecuta SU guarda (copia veri | rc=0 guardas_ok=2 | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| C-cor-02/cluster2 | adversarial | la 2.ª ejecución no hereda autorización: ejecuta SU guarda (copia veri | rc=0 guardas_ok=2 | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| C-cor-03/cluster2 | adversarial | la 2.ª ejecución no hereda autorización: ejecuta SU guarda (copia veri | rc=0 guardas_ok=2 | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| C-cor-04/cluster2 | adversarial | la 2.ª ejecución no hereda autorización: ejecuta SU guarda (copia veri | rc=3 guardas_ok=2 | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| C-cor-05A/cluster2 | adversarial | la 2.ª ejecución no hereda autorización: ejecuta SU guarda (copia veri | rc=0 guardas_ok=2 | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| C-cor-05B/cluster2 | adversarial | la 2.ª ejecución no hereda autorización: ejecuta SU guarda (copia veri | rc=0 guardas_ok=2 | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| C2-cor-01/cluster2 | adversarial | el 2.º script no llega al cuerpo | rc=3 cuerpos=0 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| C2-cor-02/cluster2 | adversarial | el 2.º script no llega al cuerpo | rc=3 cuerpos=0 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| C2-cor-03/cluster2 | adversarial | el 2.º script no llega al cuerpo | rc=3 cuerpos=0 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| C2-cor-04/cluster2 | adversarial | el 2.º script no llega al cuerpo | rc=3 cuerpos=0 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| C2-cor-05A/cluster2 | adversarial | el 2.º script no llega al cuerpo | rc=3 cuerpos=0 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| C2-cor-05B/cluster2 | adversarial | el 2.º script no llega al cuerpo | rc=3 cuerpos=0 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| D-cor-01/cluster2 | adversarial | rechazo [G-GUARDA-NO-EJECUTADA] | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| D-cor-02/cluster2 | adversarial | rechazo [G-GUARDA-NO-EJECUTADA] | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| D-cor-03/cluster2 | adversarial | rechazo [G-GUARDA-NO-EJECUTADA] | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| D-cor-04/cluster2 | adversarial | rechazo [G-GUARDA-NO-EJECUTADA] | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| D-cor-05A/cluster2 | adversarial | rechazo [G-GUARDA-NO-EJECUTADA] | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| D-cor-05B/cluster2 | adversarial | rechazo [G-GUARDA-NO-EJECUTADA] | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| E1-cor-01/cluster2 | adversarial | rechazo [G-GUARDA-NO-EJECUTADA] | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| E1-cor-02/cluster2 | adversarial | rechazo [G-GUARDA-NO-EJECUTADA] | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| E1-cor-03/cluster2 | adversarial | rechazo [G-GUARDA-NO-EJECUTADA] | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| E1-cor-04/cluster2 | adversarial | rechazo [G-GUARDA-NO-EJECUTADA] | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| E1-cor-05A/cluster2 | adversarial | rechazo [G-GUARDA-NO-EJECUTADA] | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| E1-cor-05B/cluster2 | adversarial | rechazo [G-GUARDA-NO-EJECUTADA] | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| E1-cor-01/cluster2 | adversarial | rechazo [G-GUARDA-INTEGRIDAD] | rc=3 G-GUARDA-INTEGRIDAD | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| E1-cor-02/cluster2 | adversarial | rechazo [G-GUARDA-INTEGRIDAD] | rc=3 G-GUARDA-INTEGRIDAD | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| E1-cor-03/cluster2 | adversarial | rechazo [G-GUARDA-INTEGRIDAD] | rc=3 G-GUARDA-INTEGRIDAD | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| E1-cor-04/cluster2 | adversarial | rechazo [G-GUARDA-INTEGRIDAD] | rc=3 G-GUARDA-INTEGRIDAD | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| E1-cor-05A/cluster2 | adversarial | rechazo [G-GUARDA-INTEGRIDAD] | rc=3 G-GUARDA-INTEGRIDAD | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| E1-cor-05B/cluster2 | adversarial | rechazo [G-GUARDA-INTEGRIDAD] | rc=3 G-GUARDA-INTEGRIDAD | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| E2-cor-01/cluster2 | adversarial | PARTIAL: pasa (límite documentado: sin raíz de confianza externa no ha | CUERPO EJECUTADO rc=0  | PARTIAL | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| E2-cor-02/cluster2 | adversarial | PARTIAL: pasa (límite documentado: sin raíz de confianza externa no ha | CUERPO EJECUTADO rc=0  | PARTIAL | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| E2-cor-03/cluster2 | adversarial | PARTIAL: pasa (límite documentado: sin raíz de confianza externa no ha | CUERPO EJECUTADO rc=0  | PARTIAL | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| E2-cor-04/cluster2 | adversarial | PARTIAL: pasa (límite documentado: sin raíz de confianza externa no ha | CUERPO EJECUTADO rc=3 ERROR:  syntax error at or near ":" | PARTIAL | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| E2-cor-05A/cluster2 | adversarial | PARTIAL: pasa (límite documentado: sin raíz de confianza externa no ha | CUERPO EJECUTADO rc=0  | PARTIAL | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| E2-cor-05B/cluster2 | adversarial | PARTIAL: pasa (límite documentado: sin raíz de confianza externa no ha | CUERPO EJECUTADO rc=0  | PARTIAL | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| E2-cor-01/cluster2 | adversarial | rechazo [G-GUARDA-INTEGRIDAD] | rc=3 G-GUARDA-INTEGRIDAD | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| E2-cor-02/cluster2 | adversarial | rechazo [G-GUARDA-INTEGRIDAD] | rc=3 G-GUARDA-INTEGRIDAD | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| E2-cor-03/cluster2 | adversarial | rechazo [G-GUARDA-INTEGRIDAD] | rc=3 G-GUARDA-INTEGRIDAD | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| E2-cor-04/cluster2 | adversarial | rechazo [G-GUARDA-INTEGRIDAD] | rc=3 G-GUARDA-INTEGRIDAD | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| E2-cor-05A/cluster2 | adversarial | rechazo [G-GUARDA-INTEGRIDAD] | rc=3 G-GUARDA-INTEGRIDAD | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| E2-cor-05B/cluster2 | adversarial | rechazo [G-GUARDA-INTEGRIDAD] | rc=3 G-GUARDA-INTEGRIDAD | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| F-cor-01/cluster2 | adversarial | rechazo y sin autorización residual (la sesión termina) | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| F-cor-02/cluster2 | adversarial | rechazo y sin autorización residual (la sesión termina) | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| F-cor-03/cluster2 | adversarial | rechazo y sin autorización residual (la sesión termina) | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| F-cor-04/cluster2 | adversarial | rechazo y sin autorización residual (la sesión termina) | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| F-cor-05A/cluster2 | adversarial | rechazo y sin autorización residual (la sesión termina) | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| F-cor-05B/cluster2 | adversarial | rechazo y sin autorización residual (la sesión termina) | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| G-cor-01/cluster2 | adversarial | rechazo [G-GUARDA-NO-EJECUTADA] | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| G-cor-02/cluster2 | adversarial | rechazo [G-GUARDA-NO-EJECUTADA] | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| G-cor-03/cluster2 | adversarial | rechazo [G-GUARDA-NO-EJECUTADA] | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| G-cor-04/cluster2 | adversarial | rechazo [G-GUARDA-NO-EJECUTADA] | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| G-cor-05A/cluster2 | adversarial | rechazo [G-GUARDA-NO-EJECUTADA] | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| G-cor-05B/cluster2 | adversarial | rechazo [G-GUARDA-NO-EJECUTADA] | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| H-cor-01/cluster2 | adversarial | rechazo [G-GUARDA-INTEGRIDAD] | rc=3 G-GUARDA-INTEGRIDAD | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| H-cor-02/cluster2 | adversarial | rechazo [G-GUARDA-INTEGRIDAD] | rc=3 G-GUARDA-INTEGRIDAD | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| H-cor-03/cluster2 | adversarial | rechazo [G-GUARDA-INTEGRIDAD] | rc=3 G-GUARDA-INTEGRIDAD | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| H-cor-04/cluster2 | adversarial | rechazo [G-GUARDA-INTEGRIDAD] | rc=3 G-GUARDA-INTEGRIDAD | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| H-cor-05A/cluster2 | adversarial | rechazo [G-GUARDA-INTEGRIDAD] | rc=3 G-GUARDA-INTEGRIDAD | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| H-cor-05B/cluster2 | adversarial | rechazo [G-GUARDA-INTEGRIDAD] | rc=3 G-GUARDA-INTEGRIDAD | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| I1-cor-01-02-01/cluster2 | adversarial | cada ejecución pasa por su guarda y consume su propio marcador (3 GUAR | rc=0 guardas=3 cuerpos=3 | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| I2-cor-01-02-01/cluster2 | adversarial | cada ejecución pasa por su guarda y consume su propio marcador (3 GUAR | rc=0 guardas=3 cuerpos=3 | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| J-cor-01/cluster2 | adversarial | 2.º cliente rechazado [G-GUARDA-NO-EJECUTADA] | rc=3 cuerpos=0 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| J-cor-02/cluster2 | adversarial | 2.º cliente rechazado [G-GUARDA-NO-EJECUTADA] | rc=3 cuerpos=0 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| J-cor-03/cluster2 | adversarial | 2.º cliente rechazado [G-GUARDA-NO-EJECUTADA] | rc=3 cuerpos=0 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| J-cor-04/cluster2 | adversarial | 2.º cliente rechazado [G-GUARDA-NO-EJECUTADA] | rc=3 cuerpos=0 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| J-cor-05A/cluster2 | adversarial | 2.º cliente rechazado [G-GUARDA-NO-EJECUTADA] | rc=3 cuerpos=0 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| J-cor-05B/cluster2 | adversarial | 2.º cliente rechazado [G-GUARDA-NO-EJECUTADA] | rc=3 cuerpos=0 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| K-cor-01/cluster2 | adversarial | rechazo [G-GUARDA-NO-EJECUTADA] | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| K-cor-05A/cluster2 | adversarial | rechazo [G-GUARDA-NO-EJECUTADA] | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| K-cor-01/cluster2 | adversarial | rechazo [G-GUARDA-NO-EJECUTADA] | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| K-cor-05A/cluster2 | adversarial | rechazo [G-GUARDA-NO-EJECUTADA] | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| K-cor-01/cluster2 | adversarial | rechazo [G-GUARDA-NO-EJECUTADA] | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| K-cor-05A/cluster2 | adversarial | rechazo [G-GUARDA-NO-EJECUTADA] | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| K-cor-01/cluster2 | adversarial | rechazo [G-GUARDA-NO-EJECUTADA] | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| K-cor-05A/cluster2 | adversarial | rechazo [G-GUARDA-NO-EJECUTADA] | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| L-cor-01/cluster2 | adversarial | rechazo [G-GUARDA-NO-EJECUTADA] | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| L-cor-02/cluster2 | adversarial | rechazo [G-GUARDA-NO-EJECUTADA] | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| L-cor-03/cluster2 | adversarial | rechazo [G-GUARDA-NO-EJECUTADA] | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| L-cor-04/cluster2 | adversarial | rechazo [G-GUARDA-NO-EJECUTADA] | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| L-cor-05A/cluster2 | adversarial | rechazo [G-GUARDA-NO-EJECUTADA] | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| L-cor-05B/cluster2 | adversarial | rechazo [G-GUARDA-NO-EJECUTADA] | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| M-cor-01/cluster2 | adversarial | rechazo [G-GUARDA-NO-EJECUTADA] | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| M-cor-02/cluster2 | adversarial | rechazo [G-GUARDA-NO-EJECUTADA] | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| M-cor-03/cluster2 | adversarial | rechazo [G-GUARDA-NO-EJECUTADA] | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| M-cor-04/cluster2 | adversarial | rechazo [G-GUARDA-NO-EJECUTADA] | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| M-cor-05A/cluster2 | adversarial | rechazo [G-GUARDA-NO-EJECUTADA] | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| M-cor-05B/cluster2 | adversarial | rechazo [G-GUARDA-NO-EJECUTADA] | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| N-cor-01/cluster2 | adversarial | rechazo [G-GUARDA-NO-EJECUTADA] | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| N-cor-02/cluster2 | adversarial | rechazo [G-GUARDA-NO-EJECUTADA] | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| N-cor-03/cluster2 | adversarial | rechazo [G-GUARDA-NO-EJECUTADA] | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| N-cor-04/cluster2 | adversarial | rechazo [G-GUARDA-NO-EJECUTADA] | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| N-cor-05A/cluster2 | adversarial | rechazo [G-GUARDA-NO-EJECUTADA] | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| N-cor-05B/cluster2 | adversarial | rechazo [G-GUARDA-NO-EJECUTADA] | rc=3 G-GUARDA-NO-EJECUTADA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| WRAP-01-ok/cluster2 | adversarial | ejecuta: GUARDA OK, rc=0 | rc=0 GUARDA OK | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| WRAP-02-script-alterado/cluster2 | adversarial | NO EJECUTADO [V-ARCHIVO-ALTERADO], rc=3, sin GUARDA OK ni cuerpo | rc=3 V-ARCHIVO-ALTERADO | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| WRAP-03-guarda-alterada/cluster2 | adversarial | NO EJECUTADO [V-ARCHIVO-ALTERADO], rc=3, sin GUARDA OK ni cuerpo | rc=3 V-ARCHIVO-ALTERADO | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| WRAP-04-sums-regenerado/cluster2 | adversarial | NO EJECUTADO [V-SUMS-HASH-DISTINTO], rc=3, sin GUARDA OK ni cuerpo | rc=3 V-SUMS-HASH-DISTINTO | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| WRAP-05-hash-incorrecto/cluster2 | adversarial | NO EJECUTADO [V-SUMS-HASH-DISTINTO], rc=3, sin GUARDA OK ni cuerpo | rc=3 V-SUMS-HASH-DISTINTO | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| WRAP-06-hash-mal-formado/cluster2 | adversarial | NO EJECUTADO [V-HASH-INVALIDO], rc=3, sin GUARDA OK ni cuerpo | rc=3 V-HASH-INVALIDO | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| WRAP-07-hash-ausente/cluster2 | adversarial | NO EJECUTADO [V-HASH-INVALIDO], rc=3, sin GUARDA OK ni cuerpo | rc=3 V-HASH-INVALIDO | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| WRAP-08-guarda-vacia/cluster2 | adversarial | NO EJECUTADO [V-ARCHIVO-ALTERADO], rc=3, sin GUARDA OK ni cuerpo | rc=3 V-ARCHIVO-ALTERADO | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| WRAP-09-guarda-truncada/cluster2 | adversarial | NO EJECUTADO [V-ARCHIVO-ALTERADO], rc=3, sin GUARDA OK ni cuerpo | rc=3 V-ARCHIVO-ALTERADO | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| WRAP-10-guarda-ausente/cluster2 | adversarial | NO EJECUTADO [V-ARCHIVO-AUSENTE-O-SYMLINK], rc=3, sin GUARDA OK ni cue | rc=3 V-ARCHIVO-AUSENTE-O-SYMLINK | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| WRAP-11-symlink-guarda/cluster2 | adversarial | NO EJECUTADO [V-ARCHIVO-AUSENTE-O-SYMLINK], rc=3, sin GUARDA OK ni cue | rc=3 V-ARCHIVO-AUSENTE-O-SYMLINK | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| WRAP-12-symlink-script/cluster2 | adversarial | NO EJECUTADO [V-SYMLINK], rc=3, sin GUARDA OK ni cuerpo | rc=3 V-SYMLINK | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| WRAP-13-symlink-sums/cluster2 | adversarial | NO EJECUTADO [V-SUMS-AUSENTE], rc=3, sin GUARDA OK ni cuerpo | rc=3 V-SUMS-AUSENTE | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| WRAP-14-ruta-relativa/cluster2 | adversarial | ejecuta la guarda verificada (no la del cwd): GUARDA OK y sin PWNED-RO | rc=0 GUARDA OK | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| WRAP-15-PATH/cluster2 | adversarial | el ejecutor fija PATH: GUARDA OK sin PWNED-PATH | rc=0 GUARDA OK | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| WRAP-16-PSQLRC-BASH_ENV/cluster2 | adversarial | ignoradas: GUARDA OK sin PWNED | rc=0 GUARDA OK | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| WRAP-17-CCI_DIR-preestablecida/cluster2 | adversarial | el ejecutor las sobrescribe: GUARDA OK sin PWNED-ROGUE | rc=0 GUARDA OK | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| WRAP-18-PGOPTIONS-extra/cluster2 | adversarial | NO EJECUTADO [V-PGOPTIONS-NO-PERMITIDO], rc=3, sin GUARDA OK ni cuerpo | rc=3 V-PGOPTIONS-NO-PERMITIDO | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| WRAP-19-opcion-vcci_/cluster2 | adversarial | NO EJECUTADO [V-OPCION-NO-PERMITIDA], rc=3, sin GUARDA OK ni cuerpo | rc=3 V-OPCION-NO-PERMITIDA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| WRAP-19-opcion-csele/cluster2 | adversarial | NO EJECUTADO [V-OPCION-NO-PERMITIDA], rc=3, sin GUARDA OK ni cuerpo | rc=3 V-OPCION-NO-PERMITIDA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| WRAP-19-opcion-f/etc/cluster2 | adversarial | NO EJECUTADO [V-OPCION-NO-PERMITIDA], rc=3, sin GUARDA OK ni cuerpo | rc=3 V-OPCION-NO-PERMITIDA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| WRAP-19-opcion-1/cluster2 | adversarial | NO EJECUTADO [V-OPCION-NO-PERMITIDA], rc=3, sin GUARDA OK ni cuerpo | rc=3 V-OPCION-NO-PERMITIDA | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| WRAP-20-destino-aprobado/cluster2 | adversarial | ejecuta | rc=0 GUARDA OK | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| WRAP-21-destino-no-aprobado/cluster2 | adversarial | NO EJECUTADO [V-DESTINO-NO-APROBADO], rc=3, sin GUARDA OK ni cuerpo | rc=3 V-DESTINO-NO-APROBADO | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| WRAP-22-DEV-sin-lista/cluster2 | adversarial | NO EJECUTADO [V-DESTINO-NO-CONFIGURADO], rc=3, sin GUARDA OK ni cuerpo | rc=3 V-DESTINO-NO-CONFIGURADO | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| WRAP-23-TOCTOU/cluster2 | adversarial | nunca se ejecuta contenido malicioso (0 PWNED); cada corrida o ejecuta | rc=0 ejecuciones=25 ok=16 rechazadas=9 pwned=0 | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| WRAP-24-concurrencia/cluster2 | adversarial | las 6 terminan OK, cada una con su directorio privado y su marcador | rc=0 ok=6/6 | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| WRAP-25-interrupcion/cluster2 | adversarial | no quedan directorios privados residuales | rc=0 residuales=0 | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| WRAP-26-permisos/cluster2 | adversarial | NO EJECUTADO [V-PERMISOS], rc=3, sin GUARDA OK ni cuerpo | rc=3 V-PERMISOS | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| WRAP-27-script-ajeno/cluster2 | adversarial | NO EJECUTADO [V-SCRIPT-NO-RECONOCIDO], rc=3, sin GUARDA OK ni cuerpo | rc=3 V-SCRIPT-NO-RECONOCIDO | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| A-pub-01/cluster2 | adversarial | FAIL = defecto reproducido (el cuerpo se ejecuta) | CUERPO EJECUTADO rc=0  | FAIL | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| A-pub-02/cluster2 | adversarial | FAIL = defecto reproducido (el cuerpo se ejecuta) | CUERPO EJECUTADO rc=0  | FAIL | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| A-pub-03/cluster2 | adversarial | FAIL = defecto reproducido (el cuerpo se ejecuta) | CUERPO EJECUTADO rc=0  | FAIL | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| A-pub-04/cluster2 | adversarial | FAIL = defecto reproducido (el cuerpo se ejecuta) | CUERPO EJECUTADO rc=3 ERROR:  syntax error at or near ":" | FAIL | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| A-pub-05A/cluster2 | adversarial | FAIL = defecto reproducido (el cuerpo se ejecuta) | CUERPO EJECUTADO rc=0  | FAIL | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| A-pub-05B/cluster2 | adversarial | FAIL = defecto reproducido (el cuerpo se ejecuta) | CUERPO EJECUTADO rc=0  | FAIL | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| D-pub-01/cluster2 | adversarial | FAIL = defecto reproducido | CUERPO EJECUTADO rc=0  | FAIL | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| D-pub-02/cluster2 | adversarial | FAIL = defecto reproducido | CUERPO EJECUTADO rc=0  | FAIL | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| D-pub-03/cluster2 | adversarial | FAIL = defecto reproducido | CUERPO EJECUTADO rc=0  | FAIL | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| D-pub-04/cluster2 | adversarial | FAIL = defecto reproducido | CUERPO EJECUTADO rc=3 ERROR:  syntax error at or near ":" | FAIL | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| D-pub-05A/cluster2 | adversarial | FAIL = defecto reproducido | CUERPO EJECUTADO rc=0  | FAIL | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| D-pub-05B/cluster2 | adversarial | FAIL = defecto reproducido | CUERPO EJECUTADO rc=0  | FAIL | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| E1-pub-01/cluster2 | adversarial | FAIL = defecto reproducido | CUERPO EJECUTADO rc=0  | FAIL | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| E1-pub-02/cluster2 | adversarial | FAIL = defecto reproducido | CUERPO EJECUTADO rc=0  | FAIL | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| E1-pub-03/cluster2 | adversarial | FAIL = defecto reproducido | CUERPO EJECUTADO rc=0  | FAIL | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| E1-pub-04/cluster2 | adversarial | FAIL = defecto reproducido | CUERPO EJECUTADO rc=3 ERROR:  syntax error at or near ":" | FAIL | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| E1-pub-05A/cluster2 | adversarial | FAIL = defecto reproducido | CUERPO EJECUTADO rc=0  | FAIL | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| E1-pub-05B/cluster2 | adversarial | FAIL = defecto reproducido | CUERPO EJECUTADO rc=0  | FAIL | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| H-pub-01/cluster2 | adversarial | el árbol publicado ejecuta sin verificar integridad: el cuerpo se ejec | CUERPO EJECUTADO rc=0  | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| H-pub-02/cluster2 | adversarial | el árbol publicado ejecuta sin verificar integridad: el cuerpo se ejec | CUERPO EJECUTADO rc=0  | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| H-pub-03/cluster2 | adversarial | el árbol publicado ejecuta sin verificar integridad: el cuerpo se ejec | CUERPO EJECUTADO rc=0  | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| H-pub-04/cluster2 | adversarial | el árbol publicado ejecuta sin verificar integridad: el cuerpo se ejec | CUERPO EJECUTADO rc=3 ERROR:  syntax error at or near ":" | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| H-pub-05A/cluster2 | adversarial | el árbol publicado ejecuta sin verificar integridad: el cuerpo se ejec | CUERPO EJECUTADO rc=0  | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |
| H-pub-05B/cluster2 | adversarial | el árbol publicado ejecuta sin verificar integridad: el cuerpo se ejec | CUERPO EJECUTADO rc=0  | PASS | evidencia/adversarial/cluster2_adversarial_marcador_ejecutor.json |

# 18 categorías finales
| # | Categoría | Resultado |
|---|---|---|
| 1 | Guarda destino (GD) | TOTAL=187 PASS=187 FAIL=0 |
| 2 | Marcador adversarial A–O | 142 corregidos |
| 3 | Envoltorio WRAP-01…27 | PASS |
| 4 | Hash externo | WRAP/GD-20 |
| 5 | search_path / hijack | 0 hijack funciones |
| 6 | Operadores homónimos | residual 4/6 sin chequeo |
| 7 | Identidad DEV/PROD | 10 PASS/3 PARTIAL/1 NOT TESTED |
| 8 | Persistencia tras rechazo | sin cambios |
| 9 | Seis scripts por caso | ver matriz |
| 10 | Permutaciones | 24+3, iguales |
| 11 | Batería 22 pasos ×2 | 22/22 |
| 12 | Comparación clústeres | ver AUDITORIA_H01 |
| 13 | Escáner SQL | 176/176 |
| 14 | Autoprueba escáner | 39/39 |
| 15 | Escáner texto | FAIL=0 |
| 16 | Reconciliación H-02 | 58/58 |
| 17 | Consistencia informe/controles | 58/58, 7/7 |
| 18 | Manifiesto | verificado |
