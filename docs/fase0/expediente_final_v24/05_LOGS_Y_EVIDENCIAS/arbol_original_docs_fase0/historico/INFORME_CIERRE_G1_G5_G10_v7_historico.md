---
name: informe_cierre_g1_g5_g10
description: Informe de la revisión v7 de G-1, G-5 y G-10 (H-01 auditoría, H-02 reconstrucción por campo, H-03 integridad); diseño documental; nada ejecutado
---

# INFORME — CORRECCIÓN DE H-01, H-02 Y H-03 (revisión v7)

Sustituye al informe v6 (conservado en `historico/`). Solo diseño documental: no se ejecutó SQL, código, Supabase, PostgreSQL ni pruebas técnicas.

## A. Dictamen ejecutivo

| Nivel | Estado | Alcance |
|---|---|---|
| 1. Fase 0 v3.3 | COMPLETADA Y ACEPTADA COMO LÍNEA BASE DOCUMENTAL, CON LIMITACIONES DOCUMENTADAS | No se reabre ni se modifica; SHA-256 `b5dccdc73a8103966ab1e1b1e84b2e7ead68cd736fba666ec71d0e790d51c1da` sin cambio |
| 2. Diseño complementario v7 (G-1, G-5, G-10) | PREPARADA PARA ACEPTACIÓN FORMAL DEL PROPIETARIO, CON LIMITACIONES DOCUMENTADAS | Pendiente de aceptación formal del propietario; no validado técnicamente; la Adenda v9 sigue sin aceptar (PO-05) |
| 3. Fase 1 | NO INICIADA / NO AUTORIZADA | Requiere autorización expresa; este diseño no la concede |


**Niveles de evidencia usados en este expediente.**

| Nivel de evidencia | Significado | Alcance |
|---|---|---|
| Diseñado | La regla o el escenario está escrito en la especificación | Nada ejecutado |
| Verificado documentalmente | El verificador publicado comprobó coherencia entre los documentos: IDs, referencias, cifras, contratos, orden, estados | Resultado reproducible; no prueba que el diseño funcione en PostgreSQL |
| Validado técnicamente | Ejecución real contra PostgreSQL, RLS y Supabase con las pruebas de la matriz | **Pendiente**: ningún control ni escenario alcanza este nivel |


Los tres hallazgos se corrigen en el diseño y se comprueban **documentalmente** con el verificador publicado y sus 22 mutaciones negativas (todas detectadas; resultado real en la auditoría). El hash del original de v3.3 se calcula sobre sus bytes cuando el archivo se indica con `--v33`; sin él, K48 queda PENDIENTE y el hash escrito es solo un registro histórico. Ninguna prueba se ejecutó. G-5 no se declara completamente cerrada ni validada técnicamente. No hay aceptación del propietario de esta revisión.

## B. Qué se corrigió

### H-01 Hash de v3.3 registrado pero no calculado

| Concepto | Detalle |
|---|---|
| Defecto en la v6 | El control K25 comparaba el hash escrito en los documentos con otro texto; un hash registrado se presentaba como comprobado sin calcular el SHA-256 del archivo original. |
| Corrección | K48 calcula el SHA-256 sobre los bytes del archivo original de v3.3 (`--v33 RUTA`) y lo compara con `b5dccdc73a8103966ab1e1b1e84b2e7ead68cd736fba666ec71d0e790d51c1da`; si no coincide, FALLA; si el archivo no está disponible, queda PENDIENTE_ARCHIVO_ORIGINAL_NO_DISPONIBLE. K25 queda como registro histórico, distinto de la comprobación criptográfica. Una mutación (un bit alterado en una copia temporal) comprueba que K48 detecta la diferencia. |
| Documento y sección | AUDITORIA 3; REGISTRO |
| Reglas | IE-10 |
| Evidencia | Verificador K25, K48 y mutación M-22 |
| Escenarios diseñados | T-373 a T-375 (3; ninguno ejecutado) |

### H-02 Un cambio textual podía retirar a un contribuyente anterior

| Concepto | Detalle |
|---|---|
| Defecto en la v6 | Las reglas v6 marcaban como históricas las atribuciones heredadas cuando un campo era sustituido o eliminado, y la comparación de texto, el hash o retained_segments = 0 podían excluir a un contribuyente real (T-299). |
| Corrección | Principio de conservación (IG5-90): una atribución activa se conserva aunque el campo se modifique, sustituya o elimine; la clasificación técnica (sin_cambio, introducido, modificado, sustituido, eliminado) queda separada del estado de la atribución (IG5-91). Solo una resolución independiente, documentada y con evidencia (tabla `attribution_discard_resolutions`, IG5-92 a IG5-94) la vuelve histórica; el afectado, el solicitante y el autor de la modificación no pueden resolver; sin resolutor elegible el sistema falla cerrado. T-299 corregido. |
| Documento y sección | ESPECIFICACION 4.4.4 y 4.4.8 |
| Reglas | IG5-72, IG5-90 a IG5-94 |
| Evidencia | Verificador K46, K47, K49 y mutaciones M-11 a M-14 |
| Escenarios diseñados | T-336 a T-354 (19; ninguno ejecutado) |

### H-03 Las relaciones parecían válidas con solo contener organization_id

| Concepto | Detalle |
|---|---|
| Defecto en la v6 | El verificador v6 comprobaba que las FK incluyeran organization_id, no que sus columnas, orden, destino, tipos, versión, origen del evento y actor fueran correctos. |
| Corrección | Verificación semántica por FK (IG5-80, IE-09): longitud y orden de columnas, PK o UNIQUE de destino idéntica, tipos, organization_id, versión, entidad, origen del evento, actor, asset ligado a la versión exacta, antecesor y ausencia de ciclos; catálogo de claves de las tablas históricas referenciadas; 14 mutaciones negativas obligatorias (M-01 a M-14) con estado inicial, modificación, control y resultado. |
| Documento y sección | ESPECIFICACION 4.4.9; AUDITORIA 3 |
| Reglas | IG5-80 a IG5-84, IE-09, IE-11 |
| Evidencia | Verificador K44, K45 y mutaciones M-01 a M-10 |
| Escenarios diseñados | T-355 a T-372 (18; ninguno ejecutado) |

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
| Reglas de integridad | 208 |
| Pruebas diseñadas | 375 (documental 50 / técnica futura ejecutable 276 / infraestructura real 49); **ninguna ejecutada**; cobertura regla↔escenario completa según el verificador |
| Tablas propuestas | 41 (27 históricas + 14 nuevas) |
| Verificación documental | 48 comprobaciones del verificador publicado; resultado real en AUDITORIA_FINAL_G1_G5_G10.md, sección 3 |
| Pruebas técnicas no ejecutadas | Todas: no hay PostgreSQL, RLS, Supabase ni concurrencia real ejecutados; tampoco la unicidad, los triggers de independencia ni las FK compuestas de attribution_discard_resolutions |

## F. Pendientes

PO-05 y aceptación de la Adenda v9; aceptación formal de esta revisión; DG-09, DG-12, DG-16, DG-18, DG-19, DG-20; RP-01; P-01 a P-05; P-10; OD-13; G-9 completo; DEP-RET-01; valores reales de canal y formato; validación de infraestructura; pruebas reales de PostgreSQL, RLS y Supabase; pruebas reales de concurrencia, bloqueos y rollback; validación externa y operativa. Ninguno se resuelve en esta revisión.

## G. Integridad y GitHub

SHA-256 de v3.3: `b5dccdc73a8103966ab1e1b1e84b2e7ead68cd736fba666ec71d0e790d51c1da` (sin cambio). Publicación en `main` de `appalex47-lab/Copy-Creative-Intelligence`, carpeta `docs/fase0/`. Commit anterior `6ad464d5914acc15df658e1104a967d9a914309b`. El commit nuevo y los SHA-256 de los cinco documentos se informan en el mensaje final.

## H. Declaración de alcance

Sin código de aplicación, sin SQL ejecutable, sin migraciones, sin recursos Supabase, sin infraestructura ni despliegue; v3.3 sin alterar; T-02 conserva sus 13 transiciones y no hay permisos nuevos (17 claves físicas); Fase 1 no iniciada; ninguna decisión del propietario se da por tomada y no se declara aceptación del propietario.
