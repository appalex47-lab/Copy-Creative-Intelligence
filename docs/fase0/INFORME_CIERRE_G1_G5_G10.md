---
name: informe_cierre_g1_g5_g10
description: Informe de la revisión v8 de G-1, G-5 y G-10 (K45, K46 y K47: correspondencias semánticas, independencia del resolutor y conservación estructural de atribuciones); diseño documental; nada ejecutado
---

# INFORME — CIERRE DE K46, K45 Y K47 (revisión v8)

Sustituye al informe v7 (conservado en `historico/`). Solo diseño documental: no se ejecutó SQL, código, Supabase, PostgreSQL ni pruebas técnicas.

## A. Dictamen ejecutivo

| Nivel | Estado | Alcance |
|---|---|---|
| 1. Fase 0 v3.3 | COMPLETADA Y ACEPTADA COMO LÍNEA BASE DOCUMENTAL, CON LIMITACIONES DOCUMENTADAS | No se reabre ni se modifica; SHA-256 `b5dccdc73a8103966ab1e1b1e84b2e7ead68cd736fba666ec71d0e790d51c1da` sin cambio |
| 2. Diseño complementario v8 (G-1, G-5, G-10) | COMPLETADO DOCUMENTALMENTE Y PREPARADO PARA ACEPTACIÓN FORMAL DEL PROPIETARIO, CON LIMITACIONES TÉCNICAS EXPLÍCITAS | Pendiente de aceptación formal del propietario; no validado técnicamente; la Adenda v9 sigue sin aceptar (PO-05) |
| 3. Fase 1 | NO INICIADA / NO AUTORIZADA | Requiere autorización expresa; este diseño no la concede |


**Niveles de evidencia usados en este expediente.**

| Nivel de evidencia | Significado | Alcance |
|---|---|---|
| Diseñado | La regla o el escenario está escrito en la especificación | Nada ejecutado |
| Verificado documentalmente | El verificador publicado comprobó coherencia entre los documentos: IDs, referencias, cifras, contratos, orden, estados | Resultado reproducible; no prueba que el diseño funcione en PostgreSQL |
| Validado técnicamente | Ejecución real contra PostgreSQL, RLS y Supabase con las pruebas de la matriz | **Pendiente**: ningún control ni escenario alcanza este nivel |


Los tres hallazgos se corrigen en el diseño y se comprueban **documentalmente** con el verificador publicado y sus 65 mutaciones negativas (todas detectadas; resultado real en la auditoría). El hash del original de v3.3 se calcula sobre sus bytes cuando el archivo se indica con `--v33`; sin él, K48 queda PENDIENTE y el hash escrito es solo un registro histórico. Ninguna prueba se ejecutó. G-5 no se declara completamente cerrada ni validada técnicamente. No hay aceptación del propietario de esta revisión.

## B. Qué se corrigió

### K46 La independencia del resolutor no se demostraba de forma integral

| Concepto | Detalle |
|---|---|
| Defecto en la v7 | La v7 comprobaba que el resolutor no fuera el afectado ni el solicitante, que tuviera piece.review y que hubiera motivo y evidencia, pero no demostraba que tampoco fuera el editor que ejecutó la sustitución, contribuyente del campo en otra versión de la cadena, heredero activo ni excluido por otra fuente de la cadena. |
| Corrección | Reglas R1 a R9 (IG5-95) calculadas sobre el conjunto completo de contribuyentes y eventos de la cadena; la resolución registra además el evento motivador, el actor del cambio y la evidencia ligada a la misma atribución y versión; sin persona elegible la resolución falla cerrada. El verificador reconstruye un caso de referencia (organización, fuente, cadena, campo, atribución, afectado, evento, actor, solicitante, resolutor, evidencia y resultado) y ejecuta 12 mutaciones. |
| Documento y sección | ESPECIFICACION 4.4.4, 4.4.8 y 4.4.10 |
| Reglas | IG5-92, IG5-95, IE-12 |
| Evidencia | Verificador K46 y mutaciones K46-M01 a K46-M12 |
| Escenarios diseñados | T-376 a T-388 (13; ninguno ejecutado) |

### K45 La coherencia entre tipo de contribución, origen y fuente no se demostraba

| Concepto | Detalle |
|---|---|
| Defecto en la v7 | La v7 validaba relaciones y referencias, pero no demostraba que contribution_type correspondiera a origin_kind, a la tabla y fila de origen, a la pieza, la versión, el campo, el evento, el actor y la atribución que lo referencia. |
| Corrección | Matriz de correspondencias (4.4.10 A) con los nombres físicos del modelo, condiciones S1 a S12 y regla explícita de reutilización de asset (IG5-96). El verificador la convierte en una estructura, la contrasta con las restricciones de contribution_events y la evalúa sobre un caso de referencia con 14 mutaciones. |
| Documento y sección | ESPECIFICACION 4.4.4 y 4.4.10 |
| Reglas | IG5-81 a IG5-84, IG5-96, IE-12 |
| Evidencia | Verificador K45 y mutaciones K45-M01 a K45-M14 |
| Escenarios diseñados | T-389 a T-403 (15; ninguno ejecutado) |

### K47 La conservación de atribuciones se comprobaba sobre todo con búsquedas de texto

| Concepto | Detalle |
|---|---|
| Defecto en la v7 | K47 dependía de expresiones regulares y de fragmentos literales; no demostraba que las cinco clasificaciones, las resoluciones y E fueran coherentes entre brief, promoción y copy. |
| Corrección | Tablas de efectos por clasificación y fuente y por evento del ciclo (4.4.10 C y D, IG5-97). El verificador las convierte en filas, simula las cinco clasificaciones sobre las tres fuentes y comprueba 12 invariantes (conservación, incorporación del actor, alcance de la resolución, E, no reescritura, igualdad entre fuentes y ausencia de decisión por similitud) con 14 mutaciones. |
| Documento y sección | ESPECIFICACION 4.4.8 y 4.4.10 |
| Reglas | IG5-72, IG5-90, IG5-91, IG5-97, IE-12 |
| Evidencia | Verificador K47 y mutaciones K47-M01 a K47-M14 |
| Escenarios diseñados | T-404 a T-422 (19; ninguno ejecutado) |

### Consistencia Título erróneo de la entrada v7 del registro y estado de cierre

| Concepto | Detalle |
|---|---|
| Defecto en la v7 | La entrada v7 del registro decía «posterior a la v7» y la v7 declaraba un estado de preparación con comprobaciones que no cubrían los defectos anteriores. |
| Corrección | Título corregido («posterior a la v6»); K50 exige que cada entrada de revisión suceda a la anterior; estados y conteos se recalculan desde el expediente; el estado de cierre solo se declara si K45, K46 y K47 detectan todas sus mutaciones. |
| Documento y sección | REGISTRO; AUDITORIA 3 |
| Reglas | IE-04 |
| Evidencia | Verificador K50, K51 |
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
| Verificación documental | 50 comprobaciones del verificador publicado; resultado real en AUDITORIA_FINAL_G1_G5_G10.md, sección 3 |
| Pruebas técnicas no ejecutadas | Todas: no hay PostgreSQL, RLS, Supabase ni concurrencia real ejecutados; tampoco la unicidad, los triggers de independencia ni las FK compuestas de attribution_discard_resolutions |

## F. Pendientes

PO-05 y aceptación de la Adenda v9; aceptación formal de esta revisión; DG-09, DG-12, DG-16, DG-18, DG-19, DG-20; RP-01; P-01 a P-05; P-10; OD-13; G-9 completo; DEP-RET-01; valores reales de canal y formato; validación de infraestructura; pruebas reales de PostgreSQL, RLS y Supabase; pruebas reales de concurrencia, bloqueos y rollback; validación externa y operativa. Ninguno se resuelve en esta revisión.

## G. Integridad y GitHub

SHA-256 de v3.3: `b5dccdc73a8103966ab1e1b1e84b2e7ead68cd736fba666ec71d0e790d51c1da` (sin cambio). Publicación en `main` de `appalex47-lab/Copy-Creative-Intelligence`, carpeta `docs/fase0/`. Commit anterior `abd65bc15819c8d52eeb03f9af6e65e457551dce`. El commit nuevo y los SHA-256 de los cinco documentos se informan en el mensaje final.

## H. Declaración de alcance

Sin código de aplicación, sin SQL ejecutable, sin migraciones, sin recursos Supabase, sin infraestructura ni despliegue; v3.3 sin alterar; T-02 conserva sus 13 transiciones y no hay permisos nuevos (17 claves físicas); Fase 1 no iniciada; ninguna decisión del propietario se da por tomada y no se declara aceptación del propietario.
