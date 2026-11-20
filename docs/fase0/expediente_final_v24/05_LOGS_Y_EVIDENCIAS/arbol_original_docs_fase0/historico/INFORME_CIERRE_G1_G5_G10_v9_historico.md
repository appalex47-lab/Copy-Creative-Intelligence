---
name: informe_cierre_g1_g5_g10
description: Informe de la revisión v9 de G-1, G-5 y G-10 (K45, K46 y K47: integridad semántica relacional, independencia del resolutor y conservación estructural de atribuciones); diseño documental con pruebas de modelo en memoria; nada ejecutado en PostgreSQL
---

# INFORME — CORRECCIÓN ESTRUCTURAL DE K45 Y K47 (revisión v9)

Sustituye al informe v8 (conservado en `historico/`). Diseño documental con pruebas de modelo en memoria: no se ejecutó SQL, código de producto, Supabase ni PostgreSQL. La «v9» de este documento es la revisión del diseño complementario; no es la Adenda v9 del propietario (PO-05).

## A. Dictamen ejecutivo

| Nivel | Estado | Alcance |
|---|---|---|
| 1. Fase 0 v3.3 | COMPLETADA Y ACEPTADA COMO LÍNEA BASE DOCUMENTAL, CON LIMITACIONES DOCUMENTADAS | No se reabre ni se modifica; SHA-256 `b5dccdc73a8103966ab1e1b1e84b2e7ead68cd736fba666ec71d0e790d51c1da` sin cambio |
| 2. Diseño complementario v9 (G-1, G-5, G-10) | COMPLETADO DOCUMENTALMENTE Y PREPARADO PARA ACEPTACIÓN FORMAL DEL PROPIETARIO, CON LIMITACIONES TÉCNICAS EXPLÍCITAS | Pendiente de aceptación formal del propietario; no validado técnicamente; la Adenda v9 sigue sin aceptar (PO-05) |
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
| Total estructural | 75 | 75 | más 25 mutaciones documentales M-01 a M-25 |  |


Los hallazgos se corrigen en el diseño (sección 4.4.11) y se comprueban con **pruebas de modelo en memoria**: K45 sobre un modelo relacional, K47 sobre un motor de atribuciones con auditor independiente. Cada mutación parte de un caso válido y se detecta por la condición esperada; el resultado esperado y el observado de cada una están en la auditoría. El hash del original de v3.3 se calcula sobre sus bytes cuando el archivo se indica con `--v33`; sin él, K48 queda PENDIENTE y el hash escrito es solo un registro histórico. Ninguna prueba se ejecutó en PostgreSQL ni Supabase. G-5 no se declara completamente cerrada ni validada técnicamente. No hay aceptación del propietario de esta revisión.

## B. Qué se corrigió

### K45 La integridad semántica no se demostraba sobre relaciones reales

| Concepto | Detalle |
|---|---|
| Defecto en la v8 | La v8 evaluaba la correspondencia entre evento y atribución sobre etiquetas de un caso plano (un sello «origen:id» y el campo `piece` declarado) y no demostraba que la fuente física perteneciera a la misma pieza que declaran el evento y la atribución, ni que la reutilización del arte correspondiera a la versión exacta de copy que lo usa. |
| Corrección | Modelo relacional con entidades independientes (organizaciones, miembros, piezas, versiones de brief, snapshots, versiones de copy, assets, eventos, atribuciones, herencia y reutilización) y 15 controles C01 a C15 evaluados sobre las relaciones reales (4.4.11 A y B); la matriz de 4.4.10 se contrasta con los nombres físicos. Las 14 mutaciones de la v8 se reexpresan sobre el modelo y se agregan 13 (K45-M15 a K45-M22 y cinco que ejercen C05, C06, C12, C13 y C15): 27 mutaciones y 3 casos positivos. |
| Documento y sección | ESPECIFICACION 4.4.10 y 4.4.11 |
| Reglas | IG5-81 a IG5-84, IG5-96, IE-12 |
| Evidencia | Verificador K45 y mutaciones K45-M01 a K45-M27 |
| Escenarios diseñados | T-389 a T-403 (15; ninguno ejecutado) |

### K47 La conservación de atribuciones se leía en tablas, no se ejecutaba

| Concepto | Detalle |
|---|---|
| Defecto en la v8 | `simular_k47` leía celdas de tablas («todas», «ninguna», «solo la referenciada») y sus 14 mutaciones editaban el texto de una tabla; no demostraba que cada persona conservara sus atribuciones individuales a través de versiones y fuentes ni que E se obtuviera recorriendo atribuciones reales. |
| Corrección | Motor en memoria con atribuciones individuales, versiones inmutables, resoluciones y bitácora de estados que solo se agrega; las trece operaciones son funciones independientes; E se calcula recorriendo las atribuciones activas de las versiones exactas de cada fuente. Un auditor independiente comprueba 12 invariantes (I1 a I12) sobre el estado anterior y el posterior de cada operación; se ejecutan los 12 escenarios A a L y las comprobaciones U, S, X y R; la tabla de efectos de 4.4.10 se contrasta con el comportamiento observado del motor. Las 14 mutaciones de la v8 pasan a ser fallos inyectados en una operación del motor y se agregan 22 (36 en total, entre ellas una por cada regla R1 a R9). |
| Documento y sección | ESPECIFICACION 4.4.8, 4.4.10 y 4.4.11 |
| Reglas | IG5-72, IG5-90, IG5-91, IG5-97, IE-12 |
| Evidencia | Verificador K47 y mutaciones K47-M01 a K47-M36 |
| Escenarios diseñados | T-404 a T-422 (19; ninguno ejecutado) |

### K46 La independencia se probaba solo sobre un caso plano

| Concepto | Detalle |
|---|---|
| Defecto en la v8 | K46 conservaba sus 12 mutaciones pero no comprobaba que cada resolutor elegible fuera aceptado (falsos positivos) ni que R1 a R9 se aplicaran sobre la cadena del modelo estructural. |
| Corrección | K46 se conserva sin debilitar: 12 mutaciones; cada resolutor elegible del caso de referencia se acepta; el motor de K47 valida las condiciones V01 a V12 y R1 a R9 sobre su propia cadena y el auditor las recalcula con una implementación independiente (K47-M27 a K47-M36, K47-M19, escenarios F, L, X y R). |
| Documento y sección | ESPECIFICACION 4.4.10 y 4.4.11 |
| Reglas | IG5-92, IG5-95, IE-12 |
| Evidencia | Verificador K46 y mutaciones K46-M01 a K46-M12 |
| Escenarios diseñados | T-376 a T-388 (13; ninguno ejecutado) |

### Consistencia Estados y cifras de la v8 desactualizados respecto de la verificación estructural

| Concepto | Detalle |
|---|---|
| Defecto en la v8 | La v8 declaraba K45 y K47 aprobados con 14 mutaciones cada uno sobre un caso plano y un texto de tabla, y 65 mutaciones en total. |
| Corrección | Informe, auditoría, roadmap y registro se regeneran desde el verificador: el número de mutaciones, escenarios y controles sale de su ejecución; el registro declara superada la verificación de la v8; K52 exige cobertura de C01 a C15, de I1 a I12 y de los escenarios A a L. |
| Documento y sección | REGISTRO; AUDITORIA 3 |
| Reglas | IE-04 |
| Evidencia | Verificador K50, K51, K52 |
| Escenarios diseñados | T-376 a T-422 (47; ninguno ejecutado) |

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
| Reglas de integridad | 212 |
| Pruebas diseñadas | 422 (documental 92 / técnica futura ejecutable 281 / infraestructura real 49); **ninguna ejecutada**; cobertura regla↔escenario completa según el verificador |
| Tablas propuestas | 41 (27 históricas + 14 nuevas) |
| Verificación documental y estructural | 51 comprobaciones y 100 mutaciones del verificador publicado; resultado real en AUDITORIA_FINAL_G1_G5_G10.md, sección 3 |
| Pruebas estructurales ejecutadas | Modelo relacional de K45 (15 controles, 3 casos positivos), motor de K47 (12 escenarios A a L, comprobaciones U, S, X y R, 12 invariantes) y modelo de K46: todas en memoria, con datos ficticios; resultado real en la auditoría |
| Pruebas técnicas pendientes | Todas las de PostgreSQL, RLS, Supabase, transacciones, concurrencia, bloqueos y rollback: nada de eso se ejecutó; tampoco la unicidad, los triggers de independencia ni las FK compuestas de attribution_discard_resolutions |

## F. Pendientes

PO-05 y aceptación de la Adenda v9; aceptación formal de esta revisión; DG-09, DG-12, DG-16, DG-18, DG-19, DG-20; RP-01; P-01 a P-05; P-10; OD-13; G-9 completo; DEP-RET-01; valores reales de canal y formato; validación de infraestructura; pruebas reales de PostgreSQL, RLS y Supabase; pruebas reales de concurrencia, bloqueos y rollback; validación externa y operativa. Ninguno se resuelve en esta revisión.

## G. Integridad y GitHub

SHA-256 de v3.3: `b5dccdc73a8103966ab1e1b1e84b2e7ead68cd736fba666ec71d0e790d51c1da` (sin cambio). Publicación en `main` de `appalex47-lab/Copy-Creative-Intelligence`, carpeta `docs/fase0/`. Commit anterior `a6b36b955f9e3103174a6d49dd1ae5a7fa194e6c`. El commit nuevo y los SHA-256 de los cinco documentos se informan en el mensaje final.

## H. Declaración de alcance

Sin código de aplicación, sin SQL ejecutable, sin migraciones, sin recursos Supabase, sin infraestructura ni despliegue; v3.3 sin alterar; T-02 conserva sus 13 transiciones y no hay permisos nuevos (17 claves físicas); Fase 1 no iniciada; ninguna decisión del propietario se da por tomada y no se declara aceptación del propietario.
