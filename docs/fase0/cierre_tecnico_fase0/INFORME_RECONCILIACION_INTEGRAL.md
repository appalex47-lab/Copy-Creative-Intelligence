# INFORME DE RECONCILIACIÓN INTEGRAL

Generado con `scripts_validacion/ct_reconciliacion_integral.py` (sin base de datos); salida íntegra en `scripts_validacion/resultados/reconciliacion_integral.txt`. Cada fila: estado | comprobación | detalle.

## 1. Resultado
**TOTAL=34 FAIL=0**

| Estado \| Comprobación \| Detalle |
|---|
| PASS | CSV bien formado MATRIZ_12_ESCENARIOS_PARCIALES.csv | 12 filas x 13 cols |
| PASS | CSV bien formado MATRIZ_FUNCION_REGLA_ESCENARIO_PRUEBA.csv | 33 filas x 10 cols |
| PASS | CSV bien formado MATRIZ_LIMITACIONES_RESIDUALES.csv | 28 filas x 9 cols |
| PASS | CSV bien formado MATRIZ_TRAZABILIDAD_MAESTRA.csv | 54 filas x 11 cols |
| PASS | CSV bien formado REGISTRO_DECISIONES_RECOMENDADAS.csv | 21 filas x 21 cols |
| PASS | CSV bien formado 22_funciones_conciliacion.csv | 23 filas x 4 cols |
| PASS | CSV bien formado catalogo_except_exception.csv | 23 filas x 4 cols |
| PASS | CSV bien formado k47_por_escenario.csv | 25 filas x 7 cols |
| PASS | CSV bien formado t409_t422_individual.csv | 26 filas x 8 cols |
| PASS | decisiones: las 20 pendientes exigidas están en el registro | faltan=[] |
| PASS | decisiones: sin ids duplicados; total 21 (20 + HV-02) | 21 |
| PASS | decisiones: todas REQUIERE_APROBACION_DEL_PROPIETARIO (ninguna aprobada) |  |
| PASS | limitaciones: 28 ids únicos | 28 |
| PASS | 12 escenarios: 5 PASS_PROTOTYPE, 1 PASS_STATIC, 6 PARTIAL | {'PASS_PROTOTYPE': 5, 'PARTIAL': 6, 'PASS_STATIC': 1} |
| PASS | 12 escenarios: aceptación física PENDIENTE en todos |  |
| PASS | 22 funciones: 22 filas, 366 casos, 0 fallos |  |
| PASS | matriz función-regla cubre las 22 funciones | 22 |
| PASS | T-409..T-422: 26 variantes DETECTADA, 14 escenarios |  |
| PASS | trazabilidad: 54 filas con referencia verificable y relación declarada |  |
| PASS | V20 63/63 |  |
| PASS | V20 mutaciones 14/14 |  |
| PASS | extensión 80/80 |  |
| PASS | DG-19 63/63 |  |
| PASS | hash 16/16 |  |
| PASS | arnés 21/21 |  |
| PASS | escáner 0 FAIL |  |
| PASS | 04 local = NO VERIFICABLE |  |
| PASS | concurrencia CC-01/CC-02 PASS |  |
| PASS | DICTAMEN_PREPARACION_FASE0.md: cifras 63/63, 14/14, 80/80, 366, 354, 26, 21/21 presentes |  |
| PASS | INFORME_CIERRE_TECNICO_FASE0.md: cifras 63/63, 14/14, 80/80, 366, 354, 26, 21/21 presentes |  |
| PASS | LEEME no afirma «sin commit» como estado actual |  |
| PASS | ningún documento declara aceptada Fase 0 ni autorizada Fase 1 |  |
| PASS | ningún documento marca decisión como APROBADA |  |
| PASS | nombres de archivo citados existen en el dossier (o son fuentes V26 externas listadas) | [] |

## 2. Cifras reconciliadas (fuente única)
| Concepto | Valor | Fuente |
|---|---|---|
| Reglas / escenarios / funciones-casos / tablas / claves / transiciones | 231 / 780 / 22 funciones, 366 evaluaciones (354 fixtures distintos) / 41 / 17 / 13 | V26 (inalterado) + `22_funciones_conciliacion.csv` |
| Mutaciones K47 (modelo) / mapeadas a T-409..T-422 | 36 / 25 (mapeo inferido) | `AUDITORIA_FINAL_G1_G5_G10.md`, `EXPEDIENTE_T409_T422.md` |
| Variantes individuales T-409..T-422 | 26 en 14 escenarios | `t409_t422_individual.csv` |
| Escenarios PARCIAL | 12 → 5 PASS_PROTOTYPE, 1 PASS_STATIC, 6 PARTIAL; aceptación física pendiente en los 12 | `MATRIZ_12_ESCENARIOS_PARCIALES.csv` |
| Decisiones | 21 (20 exigidas + HV-02), todas REQUIERE_APROBACION_DEL_PROPIETARIO | `REGISTRO_DECISIONES_RECOMENDADAS.csv` |
| Limitaciones | 28 | `MATRIZ_LIMITACIONES_RESIDUALES.csv` |
| Scripts CCI-DEV | 6 (+1 biblioteca), todos NO EJECUTADOS | `cci_dev_NO_EJECUTADOS/` |

## 3. Discrepancias encontradas y tratamiento
1. «366 casos» contaba evaluaciones, no fixtures distintos (`pruebas_atomicidad` invoca `correr_mutaciones_rechazo`): documentado como 366 evaluaciones / 354 fixtures (LR-23).
2. LEEME decía «sin commit ni push»: ahora distingue estado actual de histórico.
3. DEF-F01..F05 pasan a DEF-F01..F06 con clasificación (0 defectos funcionales).
4. Manifiesto anterior con autoinclusión y 51 archivos: regenerado (ver `INFORME_HASHES_MANIFIESTO.md`).
5. Comprobación de ids EX/PE/PG citados: los resultados fuente (base V20, extensión) tienen los totales 63/63 y 80/80 en esta ronda.

## 4. Trazabilidad
`MATRIZ_TRAZABILIDAD_MAESTRA.csv` (54 filas: 33 regla→función y 21 decisiones). Solo relaciones **explícitas** (id literal en la fuente) o declaradas «NO_ESTABLECIDA»/«INFERIDA»; **no se inventan relaciones**: ninguna decisión del registro cita por id una regla que una función cubra, y el esquema físico no existe, por lo que la columna de objeto físico queda «NO_DEFINIDO: requiere CCI-DEV» salvo coincidencias textuales con la matriz de tablas.

## 5. Decisiones: verificación contra el registro
Las 20 decisiones exigidas (G-1, G-5, G-10, DG-19, DG-20, DG-12, DG-16, DG-18, G-9, RP-01, P-01..P-05, P-10, PO-05, DG-09, DEP-RET-01, OD-13) están en el registro, más HV-02. No se inventan política de retención, responsables reales, infraestructura, catálogo real de canales/formatos, umbrales no aprobados, contenido de la Adenda v9 ni de OD-13 (texto fuente no disponible en el repositorio). Cada decisión separa recomendación técnica, decisión del propietario, evidencia necesaria, dependencias de CCI-DEV y datos no disponibles (ver `INFORME_DECISIONES_ARQUITECTONICAS.md`).

## 6. Límite
Reconciliación textual y numérica; no valida el contenido físico.
