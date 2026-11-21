# INFORME DE CIFRAS DEFINITIVAS

Generado por `scripts_validacion/ct_gen_cifras.py` desde los resultados y matrices (no se copian números de mensajes anteriores). Fuente estructurada: `scripts_validacion/resultados/cifras_definitivas.json`. Si una cifra de un documento narrativo difiere de esta tabla, la tabla prevalece y la reconciliación lo marca como FAIL.

Las cifras de verificación remota (HEAD, archivos y hashes verificados por las vías A/B) no pueden constar aquí (dependen del commit que contiene este archivo): están en `evidencia_verificacion/` (fixed point; ver `INFORME_HASHES_MANIFIESTO.md`).

| Cifra | Valor | Fuente | SHA-256 de la fuente (12) | Nota |
|---|---|---|---|---|
| escaner_texto_final_total | 706 | `scripts_validacion/resultados/escaner_seguridad_texto_final.txt` | 9eef7dd7947f | repetición sobre el árbol final (tras generar informes) |
| escaner_texto_final_FAIL | 0 | `scripts_validacion/resultados/escaner_seguridad_texto_final.txt` | 9eef7dd7947f |  |
| pasos_bateria | 21 | `scripts_validacion/resultados/bateria_final/INDICE_BATERIA.csv` | cef35c08aa8e |  |
| pasos_bateria_OK | 21 | `scripts_validacion/resultados/bateria_final/INDICE_BATERIA.csv` | cef35c08aa8e |  |
| V20_pruebas_PASS | 63 | `scripts_validacion/resultados/bateria_final/INDICE_BATERIA.csv` | cef35c08aa8e | paso v20_pe de la batería |
| V20_mutaciones_detectadas | 14 | `scripts_validacion/resultados/bateria_final/INDICE_BATERIA.csv` | cef35c08aa8e | paso v20_mutaciones de la batería |
| extension_PASS | 80 | `scripts_validacion/resultados/bateria_final/INDICE_BATERIA.csv` | cef35c08aa8e | paso extension_local de la batería |
| DG19_PASS | 63 | `scripts_validacion/resultados/bateria_final/INDICE_BATERIA.csv` | cef35c08aa8e | paso dg19 de la batería |
| hash_PASS | 16 | `scripts_validacion/resultados/bateria_final/INDICE_BATERIA.csv` | cef35c08aa8e | paso hash_encadenado de la batería |
| K47_mapeadas_detectadas | 25 | `scripts_validacion/resultados/bateria_final/INDICE_BATERIA.csv` | cef35c08aa8e | paso k47_por_escenario de la batería |
| T409_variantes_detectadas | 26 | `scripts_validacion/resultados/bateria_final/INDICE_BATERIA.csv` | cef35c08aa8e | paso t409_individual de la batería |
| arnes_R1R9_PASS | 28 | `scripts_validacion/resultados/bateria_final/INDICE_BATERIA.csv` | cef35c08aa8e | paso arnes_r1r9 de la batería |
| escaner_sql_total | 115 | `scripts_validacion/resultados/bateria_final/INDICE_BATERIA.csv` | cef35c08aa8e | paso escaner_sql de la batería |
| escaner_texto_total | 661 | `scripts_validacion/resultados/bateria_final/INDICE_BATERIA.csv` | cef35c08aa8e | paso escaner_texto de la batería |
| escaner_autoprueba_total | 26 | `scripts_validacion/resultados/bateria_final/INDICE_BATERIA.csv` | cef35c08aa8e | paso escaner_autoprueba de la batería |
| evaluaciones_22_funciones | 366 | `scripts_validacion/resultados/bateria_final/INDICE_BATERIA.csv` | cef35c08aa8e | paso funciones_22 de la batería |
| escaner_sql_FAIL | 0 | `scripts_validacion/resultados/bateria_final/INDICE_BATERIA.csv` | cef35c08aa8e |  |
| escaner_texto_FAIL | 0 | `scripts_validacion/resultados/bateria_final/INDICE_BATERIA.csv` | cef35c08aa8e |  |
| escaner_autoprueba_FAIL | 0 | `scripts_validacion/resultados/bateria_final/INDICE_BATERIA.csv` | cef35c08aa8e |  |
| arnes_FAIL | 0 | `scripts_validacion/resultados/bateria_final/INDICE_BATERIA.csv` | cef35c08aa8e |  |
| fixtures_distintos_22_funciones | 354 | `scripts_validacion/resultados/bateria_final/22_stdout.txt` | cac467d3949f | evaluaciones − casos de correr_mutaciones_rechazo, que pruebas_atomicidad invoca (doble conteo); la derivación solo vale si la llamada está comprobada (True) |
| bloques_except_Exception | 23 | `scripts_validacion/resultados/catalogo_except_exception.csv` | 4676d57a15db |  |
| except_SEGURO | 19 | `scripts_validacion/resultados/catalogo_except_exception.csv` | 4676d57a15db |  |
| except_RIESGO_TECNICO | 4 | `scripts_validacion/resultados/catalogo_except_exception.csv` | 4676d57a15db |  |
| limitaciones_total | 27 | `MATRIZ_LIMITACIONES_RESIDUALES.csv` | f32ba48eca31 |  |
| limitaciones_VIGENTE | 18 | `MATRIZ_LIMITACIONES_RESIDUALES.csv` | f32ba48eca31 |  |
| limitaciones_PARCIALMENTE_RESUELTA | 4 | `MATRIZ_LIMITACIONES_RESIDUALES.csv` | f32ba48eca31 |  |
| limitaciones_RESUELTA | 5 | `MATRIZ_LIMITACIONES_RESIDUALES.csv` | f32ba48eca31 |  |
| decisiones_total | 21 | `REGISTRO_DECISIONES_RECOMENDADAS.csv` | f94ae7d26d41 |  |
| decisiones_aprobadas | 0 | `REGISTRO_DECISIONES_RECOMENDADAS.csv` | f94ae7d26d41 | 0 = ninguna aprobada |
| escenarios_parciales_total | 12 | `MATRIZ_12_ESCENARIOS_PARCIALES.csv` | cb1e8cd98cf4 |  |
| escenarios_PASS_PROTOTYPE | 5 | `MATRIZ_12_ESCENARIOS_PARCIALES.csv` | cb1e8cd98cf4 |  |
| escenarios_PASS_STATIC | 1 | `MATRIZ_12_ESCENARIOS_PARCIALES.csv` | cb1e8cd98cf4 |  |
| escenarios_PARTIAL | 6 | `MATRIZ_12_ESCENARIOS_PARCIALES.csv` | cb1e8cd98cf4 |  |
| escenarios_PASS_PHYSICAL | 0 | `MATRIZ_12_ESCENARIOS_PARCIALES.csv` | cb1e8cd98cf4 |  |
| trazabilidad_filas | 54 | `MATRIZ_TRAZABILIDAD_MAESTRA.csv` | bf838417d196 |  |
| manifiesto_entradas | 133 | `MANIFIESTO_SHA256_CIERRE.txt` | ff3e385d72f0 | el manifiesto se regenera después de este archivo; la reconciliación final y la verificación A/B comprueban la coincidencia |
