# INFORME DE RECONCILIACIÓN INTEGRAL

Generado por `scripts_validacion/ct_reconciliacion_integral.py` en una sola ejecución a partir de la misma lista estructurada: `resultados/reconciliacion_integral.json` (fuente), `resultados/reconciliacion_integral.txt` y este informe. La coincidencia entre los tres se verifica con `ct_verificar_consistencia_informe.py` (con control negativo).

- Generado: 2026-11-21T05:07:13Z UTC = 2026-11-20T23:07:13-0600 (CST) — hora tomada del reloj del entorno; no verificada contra una fuente externa.
- Commit base del árbol de trabajo: `bdd4a6d78a68ede6e6f68391e4c2eebbcc34503a` (el árbol puede contener cambios sin commit; el commit publicado se identifica en `evidencia_verificacion/`).

## Resultado
**TOTAL=56 PASS=56 FAIL=0**

| # | Estado | Comprobación | Detalle | Evidencia (archivo : SHA-256, 12 primeros) |
|---|---|---|---|---|
| 1 | PASS | CSV bien formado MATRIZ_12_ESCENARIOS_PARCIALES.csv | 12 filas x 19 cols | (cálculo sobre el árbol) |
| 2 | PASS | CSV bien formado MATRIZ_FUNCION_REGLA_ESCENARIO_PRUEBA.csv | 33 filas x 10 cols | (cálculo sobre el árbol) |
| 3 | PASS | CSV bien formado MATRIZ_LIMITACIONES_RESIDUALES.csv | 27 filas x 13 cols | (cálculo sobre el árbol) |
| 4 | PASS | CSV bien formado MATRIZ_TRAZABILIDAD_MAESTRA.csv | 54 filas x 21 cols | (cálculo sobre el árbol) |
| 5 | PASS | CSV bien formado REGISTRO_DECISIONES_RECOMENDADAS.csv | 21 filas x 24 cols | (cálculo sobre el árbol) |
| 6 | PASS | CSV bien formado 22_funciones_conciliacion.csv | 23 filas x 4 cols | (cálculo sobre el árbol) |
| 7 | PASS | CSV bien formado catalogo_except_exception.csv | 23 filas x 4 cols | (cálculo sobre el árbol) |
| 8 | PASS | CSV bien formado k47_por_escenario.csv | 25 filas x 7 cols | (cálculo sobre el árbol) |
| 9 | PASS | CSV bien formado t409_t422_correspondencia.csv | 14 filas x 12 cols | (cálculo sobre el árbol) |
| 10 | PASS | CSV bien formado t409_t422_individual.csv | 26 filas x 8 cols | (cálculo sobre el árbol) |
| 11 | PASS | decisiones: las 20 pendientes exigidas están en el registro | faltan=[] | `REGISTRO_DECISIONES_RECOMENDADAS.csv`: f94ae7d26d41 |
| 12 | PASS | decisiones: sin ids duplicados; total 21 (20 + HV-02) | 21 | (cálculo sobre el árbol) |
| 13 | PASS | decisiones: columnas de consecuencias y estado actual completas |  | (cálculo sobre el árbol) |
| 14 | PASS | decisiones: todas REQUIERE_APROBACION_DEL_PROPIETARIO (ninguna aprobada) |  | (cálculo sobre el árbol) |
| 15 | PASS | limitaciones: 27 ids únicos (LR-28 fusionada en LR-05) | 27 | `MATRIZ_LIMITACIONES_RESIDUALES.csv`: f32ba48eca31 |
| 16 | PASS | limitaciones: vigencia declarada en todas (18 VIGENTE, 5 RESUELTA, 4 PARCIALMENTE_RESUELTA) | {'VIGENTE': 18, 'RESUELTA': 5, 'PARCIALMENTE_RESUELTA': 4} | (cálculo sobre el árbol) |
| 17 | PASS | limitaciones: acción concreta y dependencia en todas |  | (cálculo sobre el árbol) |
| 18 | PASS | 12 escenarios: 5 PASS_PROTOTYPE, 1 PASS_STATIC, 6 PARTIAL | {'PASS_PROTOTYPE': 5, 'PARTIAL': 6, 'PASS_STATIC': 1} | `MATRIZ_12_ESCENARIOS_PARCIALES.csv`: cb1e8cd98cf4 |
| 19 | PASS | 12 escenarios: aceptación física PENDIENTE en todos |  | (cálculo sobre el árbol) |
| 20 | PASS | 22 funciones: 22 filas, 366 casos, 0 fallos |  | `scripts_validacion/resultados/22_funciones_conciliacion.csv`: 3a5c3296a50e |
| 21 | PASS | matriz función-regla cubre las 22 funciones | 22 | `MATRIZ_FUNCION_REGLA_ESCENARIO_PRUEBA.csv`: 937768defe89 |
| 22 | PASS | T-409..T-422: 26 variantes DETECTADA, 14 escenarios |  | `scripts_validacion/resultados/t409_t422_individual.csv`: 108e0d7b2f12 |
| 23 | PASS | trazabilidad: 54 filas con referencia verificable y relación declarada |  | `MATRIZ_TRAZABILIDAD_MAESTRA.csv`: bf838417d196 |
| 24 | PASS | trazabilidad: niveles de evidencia en vocabulario permitido en cada relación |  | (cálculo sobre el árbol) |
| 25 | PASS | V20 63/63 |  | `scripts_validacion/resultados/base_V20_pe_utf8.txt`: cdf6aeb213bc |
| 26 | PASS | V20 mutaciones 14/14 |  | `scripts_validacion/resultados/base_V20_mutaciones_utf8.txt`: 5ff31240b365 |
| 27 | PASS | extensión 80/80 |  | `scripts_validacion/resultados/ext_utf8.txt`: 54f6941ea7d3 |
| 28 | PASS | DG-19 63/63 |  | `scripts_validacion/resultados/dg19_pk_experimento.txt`: 02cd7664a397 |
| 29 | PASS | hash 16/16 |  | `scripts_validacion/resultados/hash_cadena_referencia.txt`: ce96f96482d2 |
| 30 | PASS | arnés 28/28 |  | `scripts_validacion/resultados/arnes_r1r9_autoprueba_local.txt`: 200fa4e5808f |
| 31 | PASS | escáner sql 0 FAIL |  | `scripts_validacion/resultados/escaner_seguridad_sql.txt`: ca3578dba772 |
| 32 | PASS | escáner texto 0 FAIL |  | `scripts_validacion/resultados/escaner_seguridad_texto.txt`: 30ac7f9fae76 |
| 33 | PASS | escáner texto repetido sobre el árbol final: 0 FAIL |  | `scripts_validacion/resultados/escaner_seguridad_texto_final.txt`: 9eef7dd7947f |
| 34 | PASS | escáner autoprueba 26/26 |  | `scripts_validacion/resultados/escaner_seguridad_autoprueba.txt`: 36c78c5cbbec |
| 35 | PASS | 04 local = NO VERIFICABLE |  | `scripts_validacion/resultados/04_r1r9_local_bloqueado.txt`: a1943b5aded5 |
| 36 | PASS | concurrencia CC-01/CC-02 PASS |  | `scripts_validacion/resultados/concurrencia_local_utf8.txt`: 907f6a36d5f7 |
| 37 | PASS | DICTAMEN_PREPARACION_FASE0.md: cifras 63/63, 14/14, 80/80, 366, 354, 26, 21/21 presentes |  | `DICTAMEN_PREPARACION_FASE0.md`: 6c2e8d9f6e80 |
| 38 | PASS | INFORME_CIERRE_TECNICO_FASE0.md: cifras 63/63, 14/14, 80/80, 366, 354, 26, 21/21 presentes |  | `INFORME_CIERRE_TECNICO_FASE0.md`: f753d8d6c5c8 |
| 39 | PASS | LEEME no afirma «sin commit» como estado actual |  | `LEEME_CIERRE_TECNICO.md`: 7f72a0f5b10f |
| 40 | PASS | ningún documento declara aceptada Fase 0 ni autorizada Fase 1 |  | `DICTAMEN_PREPARACION_FASE0.md`: 6c2e8d9f6e80<br>`EXPEDIENTE_T409_T422.md`: 67a94d7569d0<br>`INFORME_AUDITORIA_FECHAS_HORAS.md`: b9be09575b8a<br>`INFORME_CIERRE_TECNICO_FASE0.md`: f753d8d6c5c8<br>`INFORME_CIFRAS_DEFINITIVAS.md`: da63b2e8eaca<br>`INFORME_DECISIONES_ARQUITECTONICAS.md`: e822d92fbf2a<br>`INFORME_HASHES_MANIFIESTO.md`: 6109471bce01<br>`INFORME_PRUEBAS_FINALES.md`: 369c6671e711<br>`INFORME_PUBLICACION_GITHUB.md`: d0f83dd1ffbf<br>`INFORME_RECONCILIACION_INTEGRAL.md`: 96b66852d58b<br>`INFORME_REVISION_SCRIPTS_CCI_DEV.md`: 50f433de881e<br>`INFORME_SEGURIDAD_SCRIPTS.md`: efa07ac1ba35<br>`LEEME_CIERRE_TECNICO.md`: 7f72a0f5b10f<br>`MATRIZ_MODELO_LOGICO_FISICO.md`: 0091288b6717<br>`PLAN_VALIDACION_CCI_DEV.md`: 072a525b5215<br>`PLAN_VALIDACION_TRIGGER_R1_R9.md`: 941d73739586<br>`PROPUESTA_CONTRATO_ERRORES_R1_R9.md`: 6d7e206052de<br>`PROPUESTA_GUARDA_DEV_PROD.md`: 7e2df57ba9ed<br>`PRUEBAS_RLS_PRIVILEGIOS_CONCURRENCIA.md`: c16fd5224df2<br>`RESOLUCION_OBSERVACIONES_FINALES.md`: 0ae001852c4c<br>`REVISION_22_FUNCIONES.md`: a8c0f65a8d77 |
| 41 | PASS | ningún documento marca decisión como APROBADA |  | `DICTAMEN_PREPARACION_FASE0.md`: 6c2e8d9f6e80<br>`EXPEDIENTE_T409_T422.md`: 67a94d7569d0<br>`INFORME_AUDITORIA_FECHAS_HORAS.md`: b9be09575b8a<br>`INFORME_CIERRE_TECNICO_FASE0.md`: f753d8d6c5c8<br>`INFORME_CIFRAS_DEFINITIVAS.md`: da63b2e8eaca<br>`INFORME_DECISIONES_ARQUITECTONICAS.md`: e822d92fbf2a<br>`INFORME_HASHES_MANIFIESTO.md`: 6109471bce01<br>`INFORME_PRUEBAS_FINALES.md`: 369c6671e711<br>`INFORME_PUBLICACION_GITHUB.md`: d0f83dd1ffbf<br>`INFORME_RECONCILIACION_INTEGRAL.md`: 96b66852d58b<br>`INFORME_REVISION_SCRIPTS_CCI_DEV.md`: 50f433de881e<br>`INFORME_SEGURIDAD_SCRIPTS.md`: efa07ac1ba35<br>`LEEME_CIERRE_TECNICO.md`: 7f72a0f5b10f<br>`MATRIZ_MODELO_LOGICO_FISICO.md`: 0091288b6717<br>`PLAN_VALIDACION_CCI_DEV.md`: 072a525b5215<br>`PLAN_VALIDACION_TRIGGER_R1_R9.md`: 941d73739586<br>`PROPUESTA_CONTRATO_ERRORES_R1_R9.md`: 6d7e206052de<br>`PROPUESTA_GUARDA_DEV_PROD.md`: 7e2df57ba9ed<br>`PRUEBAS_RLS_PRIVILEGIOS_CONCURRENCIA.md`: c16fd5224df2<br>`RESOLUCION_OBSERVACIONES_FINALES.md`: 0ae001852c4c<br>`REVISION_22_FUNCIONES.md`: a8c0f65a8d77 |
| 42 | PASS | batería: 21 pasos, todos rc=0 Y estado=OK (rc=0 solo no basta: se exige el contenido esperado) | [] | `scripts_validacion/resultados/bateria_final/INDICE_BATERIA.csv`: cef35c08aa8e |
| 43 | PASS | batería: cada salida existe y su SHA-256 coincide con el índice | [] | (cálculo sobre el árbol) |
| 44 | PASS | smoke de los 6 scripts: aserciones de contenido 11/11, 0 FAIL (guardas, 03 defectuoso/corregido, 04 NO VERIFICABLE, 05 BLOCKED) |  | `scripts_validacion/resultados/aserciones_smoke.txt`: 339f81b06381 |
| 45 | PASS | T-409: 2ª corrida idéntica byte a byte |  | `scripts_validacion/resultados/bateria_final/t409_repro_cmp.txt`: 50a86dd8d804 |
| 46 | PASS | T-409..T-422: correspondencia con nivel de evidencia explícito (14 escenarios) |  | `scripts_validacion/resultados/t409_t422_correspondencia.csv`: b31056815d4c |
| 47 | PASS | manifiesto: controles negativos 36/36, 0 FAIL |  | `scripts_validacion/resultados/controles_negativos_manifiesto.txt`: 5b3c9dd17fe4 |
| 48 | PASS | búsqueda global sin FAIL |  | `scripts_validacion/resultados/busqueda_global.txt`: cbde8ca164a3 |
| 49 | PASS | herramientas antiguas eliminadas |  | (cálculo sobre el árbol) |
| 50 | PASS | cifras definitivas: generadas, batería 21/21 OK, decisiones aprobadas = 0, PASS_PHYSICAL = 0 |  | `scripts_validacion/resultados/cifras_definitivas.json`: f1440f717e72 |
| 51 | PASS | cifras: limitaciones 27 = vigentes+parciales+resueltas; decisiones 21; escenarios 12; fixtures 354 de 366 evaluaciones |  | (cálculo sobre el árbol) |
| 52 | PASS | manifiesto: nº de entradas (133) = cifra generada y = archivos sujetos a verificación |  | `MANIFIESTO_SHA256_CIERRE.txt`: 386d57676793 |
| 53 | PASS | cifras de los documentos narrativos coinciden con cifras_definitivas.json (limitaciones, decisiones, arnés, fixtures, evaluaciones) | [] | `LEEME_CIERRE_TECNICO.md`: 7f72a0f5b10f<br>`DICTAMEN_PREPARACION_FASE0.md`: 6c2e8d9f6e80<br>`INFORME_CIERRE_TECNICO_FASE0.md`: f753d8d6c5c8<br>`INFORME_PUBLICACION_GITHUB.md`: d0f83dd1ffbf<br>`INFORME_HASHES_MANIFIESTO.md`: 6109471bce01<br>`INFORME_PRUEBAS_FINALES.md`: 369c6671e711 |
| 54 | PASS | alcance: contra V26 no hay archivos modificados/eliminados/añadidos fuera de docs/fase0/cierre_tecnico_fase0 (tracked: 0, sin seguimiento: 0) | [] | (cálculo sobre el árbol) |
| 55 | PASS | alcance: herramientas protegidas (modelo_estructural.py, verificar_expediente.py) idénticas a V26 |  | (cálculo sobre el árbol) |
| 56 | PASS | referencias a archivos (166) y enlaces relativos resuelven; las citas históricas están etiquetadas | [] | `DICTAMEN_PREPARACION_FASE0.md`: 6c2e8d9f6e80<br>`EXPEDIENTE_T409_T422.md`: 67a94d7569d0<br>`INFORME_AUDITORIA_FECHAS_HORAS.md`: b9be09575b8a<br>`INFORME_CIERRE_TECNICO_FASE0.md`: f753d8d6c5c8<br>`INFORME_CIFRAS_DEFINITIVAS.md`: da63b2e8eaca<br>`INFORME_DECISIONES_ARQUITECTONICAS.md`: e822d92fbf2a<br>`INFORME_HASHES_MANIFIESTO.md`: 6109471bce01<br>`INFORME_PRUEBAS_FINALES.md`: 369c6671e711<br>`INFORME_PUBLICACION_GITHUB.md`: d0f83dd1ffbf<br>`INFORME_RECONCILIACION_INTEGRAL.md`: 96b66852d58b<br>`INFORME_REVISION_SCRIPTS_CCI_DEV.md`: 50f433de881e<br>`INFORME_SEGURIDAD_SCRIPTS.md`: efa07ac1ba35<br>`LEEME_CIERRE_TECNICO.md`: 7f72a0f5b10f<br>`MATRIZ_MODELO_LOGICO_FISICO.md`: 0091288b6717<br>`PLAN_VALIDACION_CCI_DEV.md`: 072a525b5215<br>`PLAN_VALIDACION_TRIGGER_R1_R9.md`: 941d73739586<br>`PROPUESTA_CONTRATO_ERRORES_R1_R9.md`: 6d7e206052de<br>`PROPUESTA_GUARDA_DEV_PROD.md`: 7e2df57ba9ed<br>`PRUEBAS_RLS_PRIVILEGIOS_CONCURRENCIA.md`: c16fd5224df2<br>`RESOLUCION_OBSERVACIONES_FINALES.md`: 0ae001852c4c<br>`REVISION_22_FUNCIONES.md`: a8c0f65a8d77 |

## Alcance
La reconciliación comprueba coherencia entre documentos, matrices y salidas; no demuestra corrección funcional ni valida el esquema físico. La coincidencia del manifiesto con el árbol publicado se verifica con `ct_manifiesto.py` (vías A y B), no aquí.
