# MATRIZ C01–C30 V16

Las definiciones son las del prompt de auditoría y no se modificaron. «Estado anterior» = auditoría del 2026-11-19; «Estado final» = esta misión (árbol local, sin commit).

| Criterio | Definición | Estado anterior | Estado final | Evidencia y justificación |
|---|---|---|---|---|
| C01 | HEAD remoto corresponde exactamente a V16. | APROBADO | APROBADO | git fetch/ls-remote al inicio: 6a1af24; HEAD local sin cambios al final. |
| C02 | V16 tiene como padre V15. | APROBADO | APROBADO | git log -1 --format=%P = ad34f1a5… |
| C03 | No existe divergencia inesperada. | APROBADO | APROBADO | 0 commits de divergencia con origin/main. |
| C04 | Diff V15 → V16 contiene un solo archivo. | APROBADO | APROBADO | git diff --stat: ROADMAP, +1/−1. |
| C05 | El único cambio es la corrección documental autorizada. | APROBADO | APROBADO | Cambio de palabras: v5 → v15. |
| C06 | Línea 15 identifica correctamente V15. | APROBADO | APROBADO | Línea 15 = «…G-10, v15)» (minúscula, convención del expediente). |
| C07 | Línea 157 conserva la referencia histórica a V5. | APROBADO | APROBADO | Texto intacto; en el árbol local está en la línea 159 por el párrafo añadido. |
| C08 | Se inspeccionaron íntegramente los documentos activos. | NO VERIFICABLE | NO VERIFICABLE | Escaneo programático de todas las líneas, pero sin lectura humana línea por línea de la especificación (AUDITORIA_INTEGRAL_V16.md). |
| C09 | Se auditó la totalidad de referencias de versión. | NO VERIFICABLE | APROBADO (con salvedad) | 1148 referencias halladas por búsqueda exhaustiva y clasificadas; formas alternativas de citar versión sondeadas (solo falsos positivos). Salvedad: la detección es por patrón y la clasificación automática es aproximada. |
| C10 | Existe matriz completa de clasificación de referencias. | APROBADO | APROBADO | MATRIZ_REFERENCIAS_V16.csv. |
| C11 | No hay inconsistencias activas sin resolver. | NO APROBADO | APROBADO SOLO EN LOCAL, con 1 ambigüedad abierta | HV-01 corregido en el árbol local (no publicado). HV-02 (PO-05 cita «addendum v3») sigue ambigua y sin resolver. |
| C12 | Especificación, auditoría, informe y roadmap son coherentes. | NO APROBADO | APROBADO SOLO EN LOCAL | Informe, auditoría, roadmap y registro distinguen V15 de V16 en el árbol local; la especificación identifica v15 y no menciona V16. |
| C13 | Registro histórico preservado. | APROBADO | APROBADO | Entradas v4–v15 intactas; nota V16 añadida al final. |
| C14 | Motor V15 intacto. | APROBADO | APROBADO | SHA-256 cc87236a… idéntico. |
| C15 | Verificador V15 intacto. | APROBADO | APROBADO | SHA-256 1acec85d… idéntico. |
| C16 | Pruebas V15 intactas. | APROBADO | APROBADO | Las pruebas viven en el motor y el verificador (mismos hashes). |
| C17 | Verificador integral ejecutado. | APROBADO | APROBADO | 2 corridas hoy sobre el árbol local: 59/59, 28/28, 300/300. |
| C18 | Regresión completa ejecutada o limitaciones identificadas. | APROBADO | APROBADO | Verificador + 21 funciones de prueba (hoy, individualmente, solo las 2 de pendiente C); resto vía verificador. Sin PostgreSQL/Supabase: identificado. |
| C19 | Primera ejecución independiente registrada. | APROBADO | APROBADO | REPORTE_REGRESION_V16.md, corrida 1. |
| C20 | Segunda ejecución independiente registrada. | APROBADO | APROBADO | Corrida 2. |
| C21 | Resultados reproducibles o diferencias explicadas. | APROBADO | APROBADO | Salidas idénticas byte a byte; la diferencia 299/300 sin --v33 está explicada. |
| C22 | No se contabilizaron pruebas no ejecutadas como aprobadas. | APROBADO | APROBADO | Las pruebas externas figuran como C. No ejecutable. |
| C23 | Integridad V3.3 preservada o limitación explícita. | APROBADO | APROBADO | SHA calculado del original = b5dccdc7…c1da. |
| C24 | Decisiones y puntos pendientes preservados. | APROBADO | APROBADO | Pendientes presentes y negada toda aceptación; PO-05 sin tocar. |
| C25 | No se modificó ningún archivo durante esta auditoría. | APROBADO (auditoría anterior) | NO APLICA / NO APROBADO | La misión actual autoriza ediciones locales: 4 documentos modificados y carpeta nueva. El criterio no se cumple literalmente y no se redefine. |
| C26 | No se creó V17 ni otro commit. | APROBADO | APROBADO | HEAD = 6a1af24; sin commits nuevos. |
| C27 | No se hizo push ni se alteró main. | APROBADO | APROBADO | Sin push; main remoto sin cambios. |
| C28 | No se integró la vista previa privada. | APROBADO | APROBADO | No se tocó. |
| C29 | No se cerraron G-1, G-5 ni G-10. | APROBADO | APROBADO | Siguen pendientes de aceptación formal. |
| C30 | Fase 1 permanece no iniciada y no autorizada. | APROBADO | APROBADO | Sin cambios. |

Resolución expresa: C08 NO VERIFICABLE; C09 APROBADO con salvedad; C11 y C12 aprobados solo en el árbol local (no publicado).
Resultado global: la validación integral continúa pendiente (C08, C25, publicación de la trazabilidad, HV-02 y todas las validaciones externas).

## Actualización V17 (estado separado en cuatro ejes)

| Criterio | Commit publicado 6a1af24 | Árbol local | Auditoría | Autorización de publicación |
|---|---|---|---|---|
| C08 | No aplica | Matriz estructural 231/231; lectura semántica regla a regla no realizada | NO VERIFICABLE | Ninguna |
| C09 | Referencias del commit sin V16 en trazabilidad | 1148 refs clasificadas; alcance de detección documentado | APROBADO con salvedad (alcance) | Ninguna |
| C11 | NO APROBADO (HV-01 sin nota de trazabilidad) | HV-01 corregido; HV-02 abierta; S1 corregido | NO APROBADO integral (HV-02 abierta) | Ninguna |
| C12 | NO APROBADO | Coherente tras nota V16 y S1 | APROBADO SOLO EN LOCAL | Ninguna |
| C25 | Definición intacta: «No se modificó ningún archivo durante esta auditoría» | Misión V16/V17 autoriza ediciones locales; modifica archivos | NO APLICA a trabajo con ediciones; APROBADO solo para la auditoría de solo lectura previa | Ninguna |

Los criterios aprobados en local no se cumplen en el commit remoto. V16 no se declara aceptado integralmente: C08 es no verificable y HV-02 está abierta.

## Actualización V18

| Criterio | Commit publicado 6a1af24 | Árbol local | Auditoría V18 | Autorización de publicación |
|---|---|---|---|---|
| C08 | No aplica | Matriz de 231 reglas A–E; 5 reglas E | **NO APROBADO** | Ninguna |
| C09 | Sin cambio | Sin cambio | APROBADO con salvedad (alcance documentado) | Ninguna |
| C11 | NO APROBADO | HV-02 abierta; S1 y S1b corregidos | NO APROBADO (HV-02) | Ninguna |
| C12 | NO APROBADO | Coherente (tras S1, S1b y nota V16) | APROBADO SOLO EN LOCAL | Ninguna |
| C25 | Definición intacta | La misión autoriza ediciones locales | NO APLICA a trabajo con ediciones | Ninguna |
| Pruebas (22 funciones) | — | 366/366 PASS en memoria | Individual en modelo; no es integración real | Ninguna |
| Validaciones externas (PostgreSQL, RLS, concurrencia, Storage, Edge) | — | No ejecutadas | NO VERIFICABLE | Ninguna |

V16 no se declara aceptado integralmente.

## Actualización V19

| Criterio | Commit publicado 6a1af24 | Árbol local | Auditoría V19 | Autorización de publicación |
|---|---|---|---|---|
| C08 | No aplica | 231 reglas con subclase; 780 escenarios con nivel | **NO APROBADO** (5 reglas E; 179 escenarios sin lectura semántica) | Ninguna |
| C09 | Sin cambio | Sin cambio | APROBADO con salvedad | Ninguna |
| C11 | NO APROBADO | HV-02 con fuente; sigue pendiente de decisión; tablas con 2 puntos abiertos | **NO APROBADO** | Ninguna |
| C12 | NO APROBADO | Coherente salvo la fila l.1270 (abierta) | APROBADO SOLO EN LOCAL, con la salvedad de l.1270 | Ninguna |
| C25 | Definición intacta | Edición local autorizada | NO APLICA | Ninguna |
| Modelo de tablas | — | 14 tablas y 27+14=41 confirmados; 2 puntos abiertos | NO RESUELTO | Ninguna |
| Validaciones externas | — | Sin ejecutar | NO VERIFICABLE | Ninguna |

## Nota V20 (2026-11-19) sobre el estado de publicación

Las expresiones «local», «no publicado» y «sin commit» de las secciones anteriores describen el estado en la fecha de cada sección (histórico, no se borra). Desde entonces V16–V19 se publicó en la rama `audit/fase0-v19-review` (commit `c6ef74be4db185ac3e4fd36810f24619e6f51fcf`); `main` sigue en V16. El trabajo V20 está en el árbol local sin commit. Estado vigente y cierre: `../expediente_final_v16_v19/`.
