# Informe de regresión

Ejecución evaluada `CCI-RUN-20261121T232214Z-422150a8` (2026-11-21T23:22:14Z, 455.0 s) sobre `2c516414ebc3271b166a2ebc1d1079618002883e`, clústeres nuevos y vacíos, árbol Git limpio, hashes y anclas regenerados. Anterior (referencia): `CCI-RUN-20261121T223416Z-67eb098f` sobre `cd8689b55e2f7c06b2756596d0f449bb2c2ce5b6`.

## Resultado del orquestador
**FASE0_BLOCKED** (exit 2): 67 PASS, 0 FAIL, 10 BLOCKED, 1 NOT_TESTED. Dependencias externas pendientes: ID-13, EXT-03, EXT-01, EXT-02, EXT-04-L04, EXT-04-L05, EXT-04-L06, EXT-04-L07, EXT-04-L08. Ningún BLOCKED/NOT_TESTED se convirtió en PASS.

## Comparación paso a paso con la ejecución anterior
- Pasos anteriores: 77; pasos actuales: 78; pasos nuevos: [('C', 'operadores_y_privilegios_efectivos')]; pasos retirados: [].
- Pasos cuyo estado cambió: 1 → [('C', 'operadores_y_privilegios_efectivos', '(nuevo)', 'PASS')].
- El único paso nuevo es `C/operadores_y_privilegios_efectivos` (39/39). Todos los demás conservan su estado (PASS/BLOCKED) y su resumen.

## Cambios en la auditoría de search_path (misma suite, mismo corpus)
| Grupo | Anterior (404f5adc) | Actual |
|---|---|---|
| SPD1 | hijack_op=0 hijack_fn=0 rechazos=6 de 6 | hijack_op=0 hijack_fn=0 rechazos=6 de 6 |
| SPD2 | hijack_op=0 hijack_fn=0 rechazos=0 de 6 | hijack_op=0 hijack_fn=0 rechazos=0 de 6 |
| SPD4 | hijack_op=0 hijack_fn=0 rechazos=0 de 6 | hijack_op=0 hijack_fn=0 rechazos=6 de 6 |
| SPD6 | hijack_op=0 hijack_fn=0 rechazos=6 de 6 | hijack_op=0 hijack_fn=0 rechazos=6 de 6 |
| SPD7 | hijack_op=0 hijack_fn=0 rechazos=0 de 6 | hijack_op=0 hijack_fn=0 rechazos=0 de 6 |

Explicación: SPD1/SPD2/SPD6/SPD7 no cambian (0 secuestros). **SPD4** (homónimos en `public`) pasa de «ejecutado sin secuestro» a «rechazado por G-OPERADOR-AJENO-EN-SEARCH-PATH» porque ahora la guarda detecta los operadores plantados; sigue sin haber secuestros. Los resultados históricos del expediente anterior (`AUDITORIA_FINAL_CIERRE_FASE0_RESOLUCION/`) se conservan intactos.

## Regresiones detectadas durante el trabajo y corregidas
| Detalle | Causa | Corrección |
|---|---|---|
| smoke_6_scripts: SMOKE_RC=3 con G-OPERADOR-AJENO-EN-SEARCH-PATH (12 operadores) | btree_gist legítima en public (usada por las exclusiones de CCI) detectada como operador ajeno | tolerar sólo operadores de extensión con símbolo no estándar; K-01 (extensión hostil) y K-02 (btree_gist) lo prueban |
| guarda_destino GD-15 (6 fallos) | la constancia afirmaba el search_path previo | actualizada al blindaje de sesión |
| reconciliacion_integral: alcance fuera de docs/fase0/cierre_tecnico_fase0 | la rama contiene ARTEFACTOS_REVISION_PUBLICACION/ (artefactos de publicación autorizados) | admitido en la lista EXTRA, documentado |
| H-05 estático | usos legítimos de search_path (marcador) y SET LOCAL ROLE (clasificador) marcados como hallazgo | lista de usos permitidos y documentados; cualquier otro uso falla |

Nota de transparencia: durante el desarrollo se confirmó (commit) un conjunto de documentos generados de una ejecución previa fallida (`INFORME_*`, `MANIFIESTO_SHA256_CIERRE.txt`, JSON de la suite) antes de la ejecución evaluada; la ejecución evaluada los regeneró desde cero y el expediente actual refleja únicamente esa ejecución.

## Suites individuales (de la ejecución evaluada)
| Etapa | Paso | Estado | Resumen |
|---|---|---|---|
| B | bat_escaner_sql | PASS |  |
| B | bat_escaner_autoprueba | PASS |  |
| B | bat_escaner_texto | PASS |  |
| B | meta_orquestador_fallos_inducidos | PASS |  |
| C | bat___precondicion_roles | PASS |  |
| C | bat_guarda_destino | PASS |  |
| C | adversarial_marcador_y_ejecutor | PASS |  |
| C | search_path_hijack | PASS |  |
| C | identidad_dev_prod_ag18 | PASS |  |
| C | autorizacion_operadores | PASS |  |
| C | operadores_y_privilegios_efectivos | PASS |  |
| C | identidad_firmada_ag18_clones | PASS |  |
| C | aprobacion_firmada_y_cadena_dev | PASS |  |
| C | validador_listas_ext03 | PASS |  |
| C | sonda_ext02_simulada_local | PASS |  |
| D | bat_v20_pe | PASS |  |
| D | bat_v20_mutaciones | PASS |  |
| D | bat_extension_local | PASS |  |
| D | bat_dg19 | PASS |  |
| D | bat_hash_encadenado | PASS |  |
| E | bat___precondicion_roles | PASS |  |
| E | bat_smoke_6_scripts | PASS |  |
| E | bat_aserciones_smoke | PASS |  |
| F | bat_estatica_T47_T124 | PASS |  |
| F | bat_k47_por_escenario | PASS |  |
| F | bat_t409_individual | PASS |  |
| F | bat_t409_repro_2a_corrida | PASS |  |
| F | bat_t409_repro_comparacion | PASS |  |
| F | bat_t409_correspondencia | PASS |  |
| F | bat_funciones_22 | PASS |  |
| F | bat_exc_modelo14 | PASS |  |
| F | bat_catalogo_except | PASS |  |
| F | bat_arnes_r1r9 | PASS |  |
| G | bat_concurrencia_local | PASS |  |
| G | permutaciones_orden | PASS |  |
| G | secuencia_05A_05B_observador_independiente | PASS |  |

