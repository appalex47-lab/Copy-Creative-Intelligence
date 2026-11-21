# INFORME DE RECONCILIACIÓN INTEGRAL

Generado con `scripts_validacion/ct_reconciliacion_integral.py` (sin base de datos); salida íntegra en `scripts_validacion/resultados/reconciliacion_integral.txt`. Cubre: LEEME, dictamen, informe de cierre, matrices (decisiones, limitaciones, escenarios, trazabilidad), resultados de la batería (índice con hashes), smoke de scripts, T-409..T-422, controles negativos del manifiesto, búsqueda global y nombres de archivo citados.

## Resultado
**TOTAL=51 FAIL=1**

| Estado | Comprobación | Detalle |
|---|---|---|
| PASS | CSV bien formado MATRIZ_12_ESCENARIOS_PARCIALES.csv | 12 filas x 19 cols |
| PASS | CSV bien formado MATRIZ_FUNCION_REGLA_ESCENARIO_PRUEBA.csv | 33 filas x 10 cols |
| PASS | CSV bien formado MATRIZ_LIMITACIONES_RESIDUALES.csv | 27 filas x 13 cols |
| PASS | CSV bien formado MATRIZ_TRAZABILIDAD_MAESTRA.csv | 54 filas x 21 cols |
| PASS | CSV bien formado REGISTRO_DECISIONES_RECOMENDADAS.csv | 21 filas x 24 cols |
| PASS | CSV bien formado 22_funciones_conciliacion.csv | 23 filas x 4 cols |
| PASS | CSV bien formado catalogo_except_exception.csv | 23 filas x 4 cols |
| PASS | CSV bien formado k47_por_escenario.csv | 25 filas x 7 cols |
| PASS | CSV bien formado t409_t422_correspondencia.csv | 14 filas x 12 cols |
| PASS | CSV bien formado t409_t422_individual.csv | 26 filas x 8 cols |
| PASS | decisiones: las 20 pendientes exigidas están en el registro | faltan=[] |
| PASS | decisiones: sin ids duplicados; total 21 (20 + HV-02) | 21 |
| PASS | decisiones: columnas de consecuencias y estado actual completas |  |
| PASS | decisiones: todas REQUIERE_APROBACION_DEL_PROPIETARIO (ninguna aprobada) |  |
| PASS | limitaciones: 27 ids únicos (LR-28 fusionada en LR-05) | 27 |
| PASS | limitaciones: vigencia declarada en todas (18 VIGENTE, 5 RESUELTA, 4 PARCIALMENTE_RESUELTA) | {'VIGENTE': 18, 'RESUELTA': 5, 'PARCIALMENTE_RESUELTA': 4} |
| PASS | limitaciones: acción concreta y dependencia en todas |  |
| PASS | 12 escenarios: 5 PASS_PROTOTYPE, 1 PASS_STATIC, 6 PARTIAL | {'PASS_PROTOTYPE': 5, 'PARTIAL': 6, 'PASS_STATIC': 1} |
| PASS | 12 escenarios: aceptación física PENDIENTE en todos |  |
| PASS | 22 funciones: 22 filas, 366 casos, 0 fallos |  |
| PASS | matriz función-regla cubre las 22 funciones | 22 |
| PASS | T-409..T-422: 26 variantes DETECTADA, 14 escenarios |  |
| PASS | trazabilidad: 54 filas con referencia verificable y relación declarada |  |
| PASS | trazabilidad: niveles de evidencia en vocabulario permitido en cada relación |  |
| PASS | V20 63/63 |  |
| PASS | V20 mutaciones 14/14 |  |
| PASS | extensión 80/80 |  |
| PASS | DG-19 63/63 |  |
| PASS | hash 16/16 |  |
| PASS | arnés 28/28 |  |
| PASS | escáner sql 0 FAIL |  |
| PASS | escáner texto 0 FAIL |  |
| PASS | escáner autoprueba 26/26 |  |
| PASS | 04 local = NO VERIFICABLE |  |
| PASS | concurrencia CC-01/CC-02 PASS |  |
| PASS | DICTAMEN_PREPARACION_FASE0.md: cifras 63/63, 14/14, 80/80, 366, 354, 26, 21/21 presentes |  |
| PASS | INFORME_CIERRE_TECNICO_FASE0.md: cifras 63/63, 14/14, 80/80, 366, 354, 26, 21/21 presentes |  |
| PASS | LEEME no afirma «sin commit» como estado actual |  |
| PASS | ningún documento declara aceptada Fase 0 ni autorizada Fase 1 |  |
| PASS | ningún documento marca decisión como APROBADA |  |
| PASS | batería: 20 pasos, todos rc=0 | 20 |
| PASS | batería: cada salida existe y su SHA-256 coincide con el índice | [] |
| PASS | smoke: guardas abortan (6 scripts) y base 'postgres' rechazada |  |
| PASS | smoke 03: defectuosa → FAIL; corregida → PASS |  |
| PASS | smoke 05: sesiones A/B ejecutadas con resultado PASS |  |
| PASS | T-409: 2ª corrida idéntica byte a byte |  |
| PASS | T-409..T-422: correspondencia con nivel de evidencia explícito (14 escenarios) |  |
| PASS | manifiesto: controles negativos 36/36, 0 FAIL |  |
| PASS | búsqueda global sin FAIL |  |
| PASS | herramientas antiguas eliminadas |  |
| FAIL | nombres de archivo citados existen en el dossier (o son fuentes V26 externas listadas) | [('INFORME_HASHES_MANIFIESTO.md', 'ct_gen_manifiesto.py'), ('INFORME_HASHES_MANIFIESTO.md', 'ct_verificar_publicacion.py'), ('INFORME_PUBLICACION_GITHUB.md', 'evidencia_verificacion/linea_base_inspeccion.txt'), ('INFORME_RECONCILIACION_INTEGRAL.md', 'scripts_validacion/resultados/reconciliacion_integral.txt')] |

## Alcance
La reconciliación comprueba coherencia entre documentos, matrices y salidas; no demuestra corrección funcional ni valida el esquema físico. La coincidencia del manifiesto con el árbol publicado se verifica con `ct_manifiesto.py` (vías A y B), no aquí.
