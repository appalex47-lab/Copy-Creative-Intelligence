---
name: informe_cierre_g1_g5_g10
description: Informe de la revisión v13 de G-1, G-5 y G-10 (validación previa de la identidad exacta del asset de origen e integridad referencial de las relaciones source_*; K45, K46 y K47 conservados); diseño documental con pruebas de modelo en memoria; nada ejecutado en PostgreSQL
---

# INFORME — VALIDACIÓN PREVIA DEL ORIGEN E INTEGRIDAD REFERENCIAL source_* (revisión v13)

Sustituye al informe v12 (conservado en `historico/`). Diseño documental con pruebas de modelo en memoria: no se ejecutó SQL, código de producto, Supabase ni PostgreSQL. La «v13» de este documento es la revisión del diseño complementario; no es la Adenda v9 del propietario (PO-05).

## A. Dictamen ejecutivo

| Nivel | Estado | Alcance |
|---|---|---|
| 1. Fase 0 v3.3 | COMPLETADA Y ACEPTADA COMO LÍNEA BASE DOCUMENTAL, CON LIMITACIONES DOCUMENTADAS | No se reabre ni se modifica; SHA-256 `b5dccdc73a8103966ab1e1b1e84b2e7ead68cd736fba666ec71d0e790d51c1da` sin cambio |
| 2. Diseño complementario v13 (G-1, G-5, G-10) | COMPLETADO DOCUMENTALMENTE Y PREPARADO PARA ACEPTACIÓN FORMAL DEL PROPIETARIO, CON LIMITACIONES TÉCNICAS EXPLÍCITAS | Pendiente de aceptación formal del propietario; no validado técnicamente; la Adenda v9 sigue sin aceptar (PO-05) |
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
| K47 validación previa del origen (A54 a A65) | 12 | 12 | rechazo sin escritura, estado previo idéntico y E nulo en cada una; 20 pruebas de atomicidad aprobadas | OK |
| K47 procedencia e identidad del arte (A01 a A53) | 53 | 53 | 26/26 casos positivos de arte (P01 a P26) aprobados; 16/16 pruebas adversariales aprobadas | OK |
| FK01 a FK15 (K32, K44, K45 y K55) | 15 | 15 (lo calcula el verificador) | mutaciones estructurales sobre la especificación |  |
| Total estructural | 152 | 152 | más 25 mutaciones documentales M-01 a M-25 y 15 mutaciones FK01 a FK15 |  |


Los hallazgos de la v12 se corrigen en el diseño (secciones 4.4.14 y 4.4.15) y se comprueban con **pruebas de modelo en memoria y comprobaciones documentales**: antes de escribir, el motor demuestra que el evento original de carga, el uploader y su atribución directa pertenecen al asset raíz exacto (cadena organización → pieza → asset raíz → versión exacta → evento de carga → uploader → atribución) y rechaza con `ReutilizacionInvalida` sin dejar registros parciales; el auditor independiente (28 invariantes, sin funciones compartidas con el motor) reconstruye la cadena desde los registros y detecta el origen inconsistente aunque el motor lo acepte; cada columna `source_*` tiene una FK compuesta declarativa o una excepción individual justificada (K32, K44, K45 y K55); E falla de forma segura si algún vínculo no coincide; la inmutabilidad de resoluciones y la identidad del uploader de la v10 a la v12 no cambia; K45 y K46 se conservan. Cada mutación parte de un caso válido y se detecta por la condición esperada; el resultado esperado y el observado de cada una están en la auditoría. El hash del original de v3.3 se calcula sobre sus bytes cuando el archivo se indica con `--v33`; sin él, K48 queda PENDIENTE y el hash escrito es solo un registro histórico. Ninguna prueba se ejecutó en PostgreSQL ni Supabase. G-5 no se declara completamente cerrada ni validada técnicamente. No hay aceptación del propietario de esta revisión.

## B. Qué se corrigió

### H-01 La validación previa no probaba que el evento original de carga perteneciera al asset raíz exacto

| Concepto | Detalle |
|---|---|
| Defecto en la v12 | En la v12 `_origen_carga` tomaba el evento de los campos derivados guardados en el reutilizado y buscaba la atribución por el asset del propio evento; `_validar_reutilizacion` solo comprobaba que el evento perteneciera a algún asset de la organización. Un evento de carga de otro asset de la misma organización y pieza, con su propia atribución, se aceptaba como origen; tampoco se comparaban el actor, la versión de copy, la pieza ni la atribución con el uploader y la fila raíz. |
| Corrección | `_origen_carga` deriva la raíz recorriendo la cadena y comprueba contra los registros de esa raíz: evento de tipo `asset_uploader`, asset y versión exactos, organización, pieza y versión de copy, actor y actor autenticado igual al uploader original, membresía activa y una única atribución directa del uploader, del evento y del asset exactos. `_validar_reutilizacion` valida el origen, el reutilizador, la versión de copy de destino y los ciclos antes de escribir; un rechazo lanza `ReutilizacionInvalida` con la relación inválida y no deja registros parciales. |
| Documento y sección | ESPECIFICACION 4.4.15 |
| Reglas | IG5-102, IE-12 |
| Evidencia | Mutaciones K47-A54 a A65; casos positivos P21 a P26; ADV11 a ADV16; 20 pruebas de atomicidad con comparación del estado completo |
| Escenarios diseñados | T-541 a T-576 (36; ninguno ejecutado) |

### H-02 Las relaciones source_* quedaban fuera de K32 y K45 por exclusiones generales y sin integridad referencial declarativa

| Concepto | Detalle |
|---|---|
| Defecto en la v12 | El verificador de la v12 excluía de forma general las columnas `source_*` de K32 y K45 y la documentación afirmaba un ciclo de creación sin grafo de dependencias ni orden de inserción; la FK compuesta existía solo para `source_asset_version_id`. |
| Corrección | Cada columna `source_*` y cada columna de origen de `creative_assets` tiene una FK compuesta con `organization_id` y una clave única de destino (RS-01 a RS-07); solo RS-06 es DEFERRABLE INITIALLY DEFERRED por el ciclo de filas demostrado entre un asset y su evento de carga; K32, K44, K45 y K55 verifican columnas, orden, destino, acción, momento, pares exactos, inventario, matriz de ciclos, orden de inserción y la única excepción individual (el entero `source_asset_version` del modelo en memoria, con pruebas negativas específicas); FK01 a FK15 prueban que el verificador detecta su ausencia o corrupción. |
| Documento y sección | ESPECIFICACION 4.4.15 |
| Reglas | IG5-103, IE-12 |
| Evidencia | FK01 a FK15; K32, K44, K45 y K55 |
| Escenarios diseñados | T-577 a T-599 (23; ninguno ejecutado) |

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
| Reglas de integridad | 218 |
| Pruebas diseñadas | 599 (documental 269 / técnica futura ejecutable 281 / infraestructura real 49); **ninguna ejecutada**; cobertura regla↔escenario completa según el verificador |
| Tablas propuestas | 41 (27 históricas + 14 nuevas) |
| Verificación documental y estructural | 55 comprobaciones y 192 mutaciones del verificador publicado; resultado real en AUDITORIA_FINAL_G1_G5_G10.md, sección 3 |
| Pruebas estructurales ejecutadas | Modelo relacional de K45 (15 controles, 3 casos positivos), motor de K47 (12 escenarios A a L, comprobaciones U, S, X, R y RS, 26 casos positivos de arte, 16 pruebas adversariales, 20 pruebas de atomicidad de la reutilización con comparación del estado completo, 12 mutaciones de rechazo previo A54 a A65, 9 intentos directos contra el registro de resoluciones, 28 invariantes), modelo de K46 y 15 mutaciones estructurales FK01 a FK15 sobre las FK compuestas: todas en memoria o sobre el texto de la especificación, con datos ficticios; resultado real en la auditoría |
| Pruebas técnicas pendientes | Todas las de PostgreSQL, RLS, Supabase, transacciones, concurrencia, bloqueos y rollback: nada de eso se ejecutó; tampoco la unicidad, los triggers de independencia ni las FK compuestas de attribution_discard_resolutions |

## F. Pendientes

PO-05 y aceptación de la Adenda v9; aceptación formal de esta revisión; DG-09, DG-12, DG-16, DG-18, DG-19, DG-20; RP-01; P-01 a P-05; P-10; OD-13; G-9 completo; DEP-RET-01; valores reales de canal y formato; validación de infraestructura; pruebas reales de PostgreSQL, RLS y Supabase; pruebas reales de concurrencia, bloqueos y rollback; validación externa y operativa. Ninguno se resuelve en esta revisión.

## G. Integridad y GitHub

SHA-256 de v3.3: `b5dccdc73a8103966ab1e1b1e84b2e7ead68cd736fba666ec71d0e790d51c1da` (sin cambio). Publicación en `main` de `appalex47-lab/Copy-Creative-Intelligence`, carpeta `docs/fase0/`. Commit anterior `603b03963ea30797a28154d0e08e4cfa66f3ae53`. El commit nuevo y los SHA-256 de los cinco documentos se informan en el mensaje final.

## H. Declaración de alcance

Sin código de aplicación, sin SQL ejecutable, sin migraciones, sin recursos Supabase, sin infraestructura ni despliegue; v3.3 sin alterar; T-02 conserva sus 13 transiciones y no hay permisos nuevos (17 claves físicas); Fase 1 no iniciada; ninguna decisión del propietario se da por tomada y no se declara aceptación del propietario.
