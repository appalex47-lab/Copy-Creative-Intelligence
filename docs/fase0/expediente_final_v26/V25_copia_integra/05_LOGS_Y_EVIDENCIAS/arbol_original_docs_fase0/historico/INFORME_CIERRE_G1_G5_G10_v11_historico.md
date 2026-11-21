---
name: informe_cierre_g1_g5_g10
description: Informe de la revisión v11 de G-1, G-5 y G-10 (identidad exacta de assets, uploader, eventos de carga y reutilización y atribuciones por versión; K45, K46 y K47 conservados); diseño documental con pruebas de modelo en memoria; nada ejecutado en PostgreSQL
---

# INFORME — INTEGRIDAD SEMÁNTICA DE ASSETS, UPLOADER, EVENTOS Y ATRIBUCIONES (revisión v11)

Sustituye al informe v10 (conservado en `historico/`). Diseño documental con pruebas de modelo en memoria: no se ejecutó SQL, código de producto, Supabase ni PostgreSQL. La «v11» de este documento es la revisión del diseño complementario; no es la Adenda v9 del propietario (PO-05).

## A. Dictamen ejecutivo

| Nivel | Estado | Alcance |
|---|---|---|
| 1. Fase 0 v3.3 | COMPLETADA Y ACEPTADA COMO LÍNEA BASE DOCUMENTAL, CON LIMITACIONES DOCUMENTADAS | No se reabre ni se modifica; SHA-256 `b5dccdc73a8103966ab1e1b1e84b2e7ead68cd736fba666ec71d0e790d51c1da` sin cambio |
| 2. Diseño complementario v11 (G-1, G-5, G-10) | COMPLETADO DOCUMENTALMENTE Y PREPARADO PARA ACEPTACIÓN FORMAL DEL PROPIETARIO, CON LIMITACIONES TÉCNICAS EXPLÍCITAS | Pendiente de aceptación formal del propietario; no validado técnicamente; la Adenda v9 sigue sin aceptar (PO-05) |
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
| K47 procedencia e identidad del arte (A01 a A37) | 37 | 37 | 14/14 casos positivos de arte (P01 a P14) aprobados; 5/5 pruebas adversariales aprobadas | OK |
| Total estructural | 124 | 124 | más 25 mutaciones documentales M-01 a M-25 |  |


Los hallazgos de la v10 se corrigen en el diseño (sección 4.4.13) y se comprueban con **pruebas de modelo en memoria**: identidad exacta del uploader, de los eventos de carga y reutilización y de las atribuciones por versión de asset, cierre en falso de E, evaluación de impacto y publicación, y un auditor independiente de 26 invariantes que reconstruye esas relaciones desde los registros; el registro de resoluciones inmutables de la v10 no cambia; K45 y K46 se conservan. Cada mutación parte de un caso válido y se detecta por la condición esperada; el resultado esperado y el observado de cada una están en la auditoría. El hash del original de v3.3 se calcula sobre sus bytes cuando el archivo se indica con `--v33`; sin él, K48 queda PENDIENTE y el hash escrito es solo un registro histórico. Ninguna prueba se ejecutó en PostgreSQL ni Supabase. G-5 no se declara completamente cerrada ni validada técnicamente. No hay aceptación del propietario de esta revisión.

## B. Qué se corrigió

### H-01 La identidad del uploader no se verificaba de forma estructural

| Concepto | Detalle |
|---|---|
| Defecto en la v10 | En la v10 un asset con arte podía declararse con procedencia completa sin comprobar que el uploader existiera, perteneciera a la organización del asset, tuviera membresía activa y fuera el actor autenticado de un evento de carga de la misma organización, pieza, asset exacto y versión; un evento o una atribución de otra versión, pieza u organización podía satisfacer la procedencia, y el reutilizador podía figurar como uploader. |
| Corrección | El motor identifica al uploader por relaciones estructuradas (`_id_uploader`): existencia, organización, membresía activa, evento de carga con organización, pieza, asset, versión de asset, versión de copy y actor autenticado coincidentes, y atribución directa del uploader en esa misma cadena; ante cualquier fallo la procedencia queda incompleta, E no es completo, la evaluación de impacto falla cerrada (`ProcedenciaIncompleta`) y la publicación se bloquea; nunca se sustituye al uploader por el reutilizador, el creador de la pieza, un administrador o el propietario. |
| Documento y sección | ESPECIFICACION 4.4.13 |
| Reglas | IG5-100, IE-12 |
| Evidencia | Mutaciones K47-A17 a A25 y A33 a A34; casos positivos P08 y P12 |
| Escenarios diseñados | T-466 a T-502 (37; ninguno ejecutado) |

### H-02 Las atribuciones no estaban atadas a la versión exacta del asset

| Concepto | Detalle |
|---|---|
| Defecto en la v10 | La atribución del arte se comparaba por asset y persona, sin exigir que la organización, la pieza, la versión de copy, la versión del asset, el evento y el actor de la cadena coincidieran; una atribución heredada podía carecer de antecesor verificable. |
| Corrección | Cada atribución de arte lleva asset, versión de asset y evento, y se valida la cadena organización, pieza, versión de copy, referencia exacta del asset, versión del asset, evento de carga, actor y atribución directa; el uploader original se conserva y el reutilizador se registra aparte; las atribuciones heredadas conservan su fuente original y exigen un antecesor verificable (I24 e I26). |
| Documento y sección | ESPECIFICACION 4.4.13 |
| Reglas | IG5-100, IE-12 |
| Evidencia | Mutaciones K47-A23 a A25 y A32; casos positivos P09, P11 y P12 |
| Escenarios diseñados | T-466 a T-502 (37; ninguno ejecutado) |

### H-03 La identidad del evento de reutilización no se verificaba

| Concepto | Detalle |
|---|---|
| Defecto en la v10 | El evento de reutilización no se comparaba con la organización, la pieza, el actor autenticado, el asset y la versión de asset exactos, ni con la versión de copy que incorpora la reutilización; una reutilización podía reemplazar al uploader original o compartir evento con otra. |
| Corrección | Cada reutilización tiene un evento propio con organización, pieza, actor autenticado, tipo, asset, versión de asset, versión de copy y evento de carga de origen; se conserva el uploader original; la cadena se recorre sin ciclos ni referencias ausentes (I25 e I26); los eventos anteriores no se sobrescriben. |
| Documento y sección | ESPECIFICACION 4.4.13 |
| Reglas | IG5-100, IE-12 |
| Evidencia | Mutaciones K47-A26 a A31, A35 y A36; casos positivos P10 y P13 |
| Escenarios diseñados | T-466 a T-502 (37; ninguno ejecutado) |

### H-04 Faltaban mutaciones, pruebas adversariales y casos positivos de identidad

| Concepto | Detalle |
|---|---|
| Defecto en la v10 | La v10 solo cubría A01 a A16 y 7 casos positivos; el auditor no se probaba contra un motor que acepta por error, y `no_aplica` podía ocultar un asset sin uploader o sin evento. |
| Corrección | Mutaciones K47-A17 a A37 (cada una con estado inicial válido, un único cambio efectivo, código específico, procedencia incompleta y E bloqueado), cinco pruebas adversariales (ADV1 a ADV5) en las que el motor acepta, el auditor independiente (I22 a I26) detecta y el sistema final bloquea E, la evaluación de impacto y la publicación, y los casos positivos P08 a P14, incluido `no_aplica` real. |
| Documento y sección | ESPECIFICACION 4.4.13 |
| Reglas | IG5-100, IE-12 |
| Evidencia | Verificador K47, K52, K53 y K54 |
| Escenarios diseñados | T-466 a T-502 (37; ninguno ejecutado) |

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
| Reglas de integridad | 215 |
| Pruebas diseñadas | 502 (documental 172 / técnica futura ejecutable 281 / infraestructura real 49); **ninguna ejecutada**; cobertura regla↔escenario completa según el verificador |
| Tablas propuestas | 41 (27 históricas + 14 nuevas) |
| Verificación documental y estructural | 53 comprobaciones y 149 mutaciones del verificador publicado; resultado real en AUDITORIA_FINAL_G1_G5_G10.md, sección 3 |
| Pruebas estructurales ejecutadas | Modelo relacional de K45 (15 controles, 3 casos positivos), motor de K47 (12 escenarios A a L, comprobaciones U, S, X, R y RS, 14 casos positivos de arte, 5 pruebas adversariales, 9 intentos directos contra el registro de resoluciones, 26 invariantes) y modelo de K46: todas en memoria, con datos ficticios; resultado real en la auditoría |
| Pruebas técnicas pendientes | Todas las de PostgreSQL, RLS, Supabase, transacciones, concurrencia, bloqueos y rollback: nada de eso se ejecutó; tampoco la unicidad, los triggers de independencia ni las FK compuestas de attribution_discard_resolutions |

## F. Pendientes

PO-05 y aceptación de la Adenda v9; aceptación formal de esta revisión; DG-09, DG-12, DG-16, DG-18, DG-19, DG-20; RP-01; P-01 a P-05; P-10; OD-13; G-9 completo; DEP-RET-01; valores reales de canal y formato; validación de infraestructura; pruebas reales de PostgreSQL, RLS y Supabase; pruebas reales de concurrencia, bloqueos y rollback; validación externa y operativa. Ninguno se resuelve en esta revisión.

## G. Integridad y GitHub

SHA-256 de v3.3: `b5dccdc73a8103966ab1e1b1e84b2e7ead68cd736fba666ec71d0e790d51c1da` (sin cambio). Publicación en `main` de `appalex47-lab/Copy-Creative-Intelligence`, carpeta `docs/fase0/`. Commit anterior `651c7307c0420fb09184ab6d39aebe60e3dee715`. El commit nuevo y los SHA-256 de los cinco documentos se informan en el mensaje final.

## H. Declaración de alcance

Sin código de aplicación, sin SQL ejecutable, sin migraciones, sin recursos Supabase, sin infraestructura ni despliegue; v3.3 sin alterar; T-02 conserva sus 13 transiciones y no hay permisos nuevos (17 claves físicas); Fase 1 no iniciada; ninguna decisión del propietario se da por tomada y no se declara aceptación del propietario.
