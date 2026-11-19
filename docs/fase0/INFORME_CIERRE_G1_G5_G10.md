---
name: informe_cierre_g1_g5_g10
description: Informe de la revisión v12 de G-1, G-5 y G-10 (identidad exacta del asset de origen en las reutilizaciones; K45, K46 y K47 conservados); diseño documental con pruebas de modelo en memoria; nada ejecutado en PostgreSQL
---

# INFORME — IDENTIDAD EXACTA DEL ASSET DE ORIGEN EN REUTILIZACIONES (revisión v12)

Sustituye al informe v11 (conservado en `historico/`). Diseño documental con pruebas de modelo en memoria: no se ejecutó SQL, código de producto, Supabase ni PostgreSQL. La «v12» de este documento es la revisión del diseño complementario; no es la Adenda v9 del propietario (PO-05).

## A. Dictamen ejecutivo

| Nivel | Estado | Alcance |
|---|---|---|
| 1. Fase 0 v3.3 | COMPLETADA Y ACEPTADA COMO LÍNEA BASE DOCUMENTAL, CON LIMITACIONES DOCUMENTADAS | No se reabre ni se modifica; SHA-256 `b5dccdc73a8103966ab1e1b1e84b2e7ead68cd736fba666ec71d0e790d51c1da` sin cambio |
| 2. Diseño complementario v12 (G-1, G-5, G-10) | COMPLETADO DOCUMENTALMENTE Y PREPARADO PARA ACEPTACIÓN FORMAL DEL PROPIETARIO, CON LIMITACIONES TÉCNICAS EXPLÍCITAS | Pendiente de aceptación formal del propietario; no validado técnicamente; la Adenda v9 sigue sin aceptar (PO-05) |
| 3. Fase 1 | NO INICIADA / NO AUTORIZADA | Requiere autorización expresa; este diseño no la concede |


**Niveles de evidencia usados en este expediente.**

| Nivel de evidencia | Significado | Alcance |
|---|---|---|
| Diseñado | La regla o el escenario está escrito en la especificación | Nada ejecutado |
| Verificado documentalmente | El verificador publicado comprobó coherencia entre los documentos: IDs, referencias, cifras, contratos, orden, estados | Resultado reproducible; no prueba que el diseño funcione en PostgreSQL |
| Validado técnicamente | Ejecución real contra PostgreSQL, RLS y Supabase con las pruebas de la matriz | **Pendiente**: ningún control ni escenario alcanza este nivel |


**Resultado de la verificación (calculado por el verificador publicado).**

| Control | Mutaciones | Detectadas | Casos positivos | Resultado |
|---|---|---|---|---|
| K45 | 27 | 27 | 3 casos positivos aprobados | OK |
| K46 | 12 | 12 | resolutores elegibles aceptados | OK |
| K47 | 36 | 36 | 12/12 escenarios A a L y comprobaciones U, S, X y R aprobados | OK |
| K47 resoluciones inmutables | 12 | 12 | escenario RS y 9 intentos directos rechazados | OK |
| K47 procedencia e identidad del arte (A01 a A53) | 53 | 53 | 20/20 casos positivos de arte (P01 a P20) aprobados; 10/10 pruebas adversariales aprobadas | OK |
| Total estructural | 140 | 140 | más 25 mutaciones documentales M-01 a M-25 |  |


Los hallazgos de la v11 se corrigen en el diseño (sección 4.4.14) y se comprueban con **pruebas de modelo en memoria**: cada reutilización identifica por referencias explícitas el asset de origen, su versión exacta, su evento original de carga, su uploader y su atribución original, y un auditor independiente de 28 invariantes, sin funciones compartidas con el motor, las reconstruye desde las instantáneas; E falla de forma segura si algún vínculo no coincide; la inmutabilidad de resoluciones y la identidad del uploader de la v10 y la v11 no cambian; K45 y K46 se conservan. Cada mutación parte de un caso válido y se detecta por la condición esperada; el resultado esperado y el observado de cada una están en la auditoría. El hash del original de v3.3 se calcula sobre sus bytes cuando el archivo se indica con `--v33`; sin él, K48 queda PENDIENTE y el hash escrito es solo un registro histórico. Ninguna prueba se ejecutó en PostgreSQL ni Supabase. G-5 no se declara completamente cerrada ni validada técnicamente. No hay aceptación del propietario de esta revisión.

## B. Qué se corrigió

### H-01 La identidad del asset de origen en las reutilizaciones no se demostraba por referencias explícitas

| Concepto | Detalle |
|---|---|
| Defecto en la v11 | En la v11 el evento de reutilización guardaba solo el asset y un número entero de versión del origen: otro asset de la misma organización o pieza con el mismo número de versión, otro evento de carga del mismo uploader o otra versión del mismo origen se aceptaban como el origen correcto; el evento no identificaba el asset de origen, su versión exacta, su evento original de carga ni la atribución original del uploader. |
| Corrección | Cada reutilización registra los campos explícitos `source_asset_id`, `source_asset_version_id`, `source_upload_event_id`, `source_uploader_id` y `source_attribution_id` (además de organización, pieza, versión de copy, asset y versión reutilizados, actor y actor autenticado); `registrar_asset` valida el origen completo antes de escribir y falla sin registros parciales (`ReutilizacionInvalida`); `_id_reutilizacion` y `_id_origen` comprueban cada vínculo contra el registro referenciado. |
| Documento y sección | ESPECIFICACION 4.4.14 |
| Reglas | IG5-101, IE-12 |
| Evidencia | Mutaciones K47-A33 a A41 y A46 a A48; casos positivos P15 a P19; 8 pruebas de atomicidad |
| Escenarios diseñados | T-503 a T-540 (38; ninguno ejecutado) |

### H-02 El auditor no distinguía identidad de coincidencia de atributos

| Concepto | Detalle |
|---|---|
| Defecto en la v11 | El auditor comparaba el número de versión del origen; no podía detectar referencias intercambiadas entre assets, eventos o versiones con atributos coincidentes, ni la pérdida del vínculo con el evento original de carga. |
| Corrección | El auditor independiente (I27 e I28) reconstruye la identidad desde las instantáneas sin llamar a funciones del motor (se inspecciona su código): compara `source_asset_id`, `source_asset_version_id` y `source_upload_event_id` contra los registros reales, el uploader y la atribución originales, la organización, la pieza y la versión de copy, y detecta registros intercambiados y vínculos perdidos. |
| Documento y sección | ESPECIFICACION 4.4.14 |
| Reglas | IG5-101, IE-12 |
| Evidencia | Mutaciones K47-A42 a A45; caso positivo P20; K55 |
| Escenarios diseñados | T-503 a T-540 (38; ninguno ejecutado) |

### H-03 Faltaban pruebas adversariales de identidad exacta

| Concepto | Detalle |
|---|---|
| Defecto en la v11 | No había pruebas que alteraran solo la referencia del origen manteniendo iguales los demás campos posibles. |
| Corrección | Cinco pruebas adversariales nuevas (ADV6 a ADV10): asset distinto con igual número de versión, evento de carga distinto del mismo uploader, versión distinta del mismo origen, asset de otra pieza y asset de otra organización con identificadores coincidentes; en cada una el motor acepta, el auditor detecta y E, la evaluación de impacto y la publicación se bloquean. |
| Documento y sección | ESPECIFICACION 4.4.14 |
| Reglas | IG5-101, IE-12 |
| Evidencia | ADV6 a ADV10 |
| Escenarios diseñados | T-503 a T-540 (38; ninguno ejecutado) |

## C. Modelo y relaciones

| Elemento | Detalle |
|---|---|
| Tablas | 27 históricas sin cambio; 14 nuevas propuestas: `piece_classification_events`, `piece_reviewer_assignments`, `impact_evaluations`, `publication_attempts`, `channel_formats`, `brief_versions`, `promotion_snapshots`, `contribution_events`, `copy_version_provenance`, `brief_field_changes`, `brief_field_attributions`, `promotion_field_changes`, `promotion_field_attributions`, `attribution_discard_resolutions` |
| Orden definitivo | 1.8 → 2.x → 2.1 → 2.3 → 2.5 → 2.7 → 3.x → 4.x → 5.1 → 5.3 → 6.x → 6.1 → 6.5 → 6.6 → 8.x |
| Atribución por campo | 12 campos materiales de brief y 9 de promoción; una fila de cambio por campo y versión; las atribuciones se conservan siempre; solo una resolución aceptada de `attribution_discard_resolutions` (independiente y con evidencia) las vuelve históricas; el historial no se reactiva |
| Integridad | Toda FK es compuesta e incluye organization_id; contribution_events lleva exactamente un origen tipado (origin_kind); copy_version_provenance valida nueve condiciones; copy_versions fija sus referencias de forma inmutable; el actor viene de la identidad autenticada en el backend |
| Funciones | create_brief_version, create_promotion_snapshot, create_copy_version, verify_field_provenance (interna), version_contributors y las anteriores; escritura solo por funciones del propietario cci_records_owner con search_path fijo; SECURITY DEFINER no se toma como prueba de seguridad |
| Límites | IS-11: superusuario, propietario, desactivación de triggers y edición manual no los impide el diseño |

## D. Fórmula de contribuyentes y elegibilidad

**E = Ctr(V-A) ∪ Inh(V-A) ∪ ⋃ Ctr(v) para v ∈ [V-D, V-B] ∪ P.** La fórmula, la exclusión del proponente de la clasificación vigente (DT-02) y la ausencia de autoevaluación y de asignación automática a Admin no cambian respecto de la v6. **Una atribución activa no se retira por sustitución, eliminación, diferencia de hash ni retained_segments = 0:** solo una resolución independiente con evidencia la vuelve histórica (IG5-90 a IG5-94); el afectado, el solicitante y el autor de la modificación no pueden resolver. Ante cualquiera de los diez errores de procedencia se bloquean la evaluación, la confirmación de independencia y la aprobación o publicación que dependan de ella, sin excepción de Admin; la ausencia de evidencia no es ausencia de contribuyente.

## E. Verificación

| Concepto | Resultado |
|---|---|
| Reglas de integridad | 216 |
| Pruebas diseñadas | 540 (documental 210 / técnica futura ejecutable 281 / infraestructura real 49); **ninguna ejecutada**; cobertura regla↔escenario completa según el verificador |
| Tablas propuestas | 41 (27 históricas + 14 nuevas) |
| Verificación documental y estructural | 54 comprobaciones y 165 mutaciones del verificador publicado; resultado real en AUDITORIA_FINAL_G1_G5_G10.md, sección 3 |
| Pruebas estructurales ejecutadas | Modelo relacional de K45 (15 controles, 3 casos positivos), motor de K47 (12 escenarios A a L, comprobaciones U, S, X, R y RS, 20 casos positivos de arte, 10 pruebas adversariales, 8 pruebas de atomicidad de la reutilización, 9 intentos directos contra el registro de resoluciones, 28 invariantes) y modelo de K46: todas en memoria, con datos ficticios; resultado real en la auditoría |
| Pruebas técnicas pendientes | Todas las de PostgreSQL, RLS, Supabase, transacciones, concurrencia, bloqueos y rollback: nada de eso se ejecutó; tampoco la unicidad, los triggers de independencia ni las FK compuestas de attribution_discard_resolutions |

## F. Pendientes

PO-05 y aceptación de la Adenda v9; aceptación formal de esta revisión; DG-09, DG-12, DG-16, DG-18, DG-19, DG-20; RP-01; P-01 a P-05; P-10; OD-13; G-9 completo; DEP-RET-01; valores reales de canal y formato; validación de infraestructura; pruebas reales de PostgreSQL, RLS y Supabase; pruebas reales de concurrencia, bloqueos y rollback; validación externa y operativa. Ninguno se resuelve en esta revisión.

## G. Integridad y GitHub

SHA-256 de v3.3: `b5dccdc73a8103966ab1e1b1e84b2e7ead68cd736fba666ec71d0e790d51c1da` (sin cambio). Publicación en `main` de `appalex47-lab/Copy-Creative-Intelligence`, carpeta `docs/fase0/`. Commit anterior `7916115e3476fdb07f5c3bf1c3e35ef9f0ae927a`. El commit nuevo y los SHA-256 de los cinco documentos se informan en el mensaje final.

## H. Declaración de alcance

Sin código de aplicación, sin SQL ejecutable, sin migraciones, sin recursos Supabase, sin infraestructura ni despliegue; v3.3 sin alterar; T-02 conserva sus 13 transiciones y no hay permisos nuevos (17 claves físicas); Fase 1 no iniciada; ninguna decisión del propietario se da por tomada y no se declara aceptación del propietario.
