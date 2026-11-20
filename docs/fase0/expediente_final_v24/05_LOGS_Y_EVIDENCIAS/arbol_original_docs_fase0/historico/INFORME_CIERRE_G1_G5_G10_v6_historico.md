---
name: informe_cierre_g1_g5_g10
description: Informe de la revisión v6 de G-1, G-5 y G-10 (H-01 auditoría, H-02 reconstrucción por campo, H-03 integridad); diseño documental; nada ejecutado
---

# INFORME — CORRECCIÓN DE H-01, H-02 Y H-03 (revisión v6)

Sustituye al informe v5 (conservado en `historico/`). Solo diseño documental: no se ejecutó SQL, código, Supabase, PostgreSQL ni pruebas técnicas.

## A. Dictamen ejecutivo

| Nivel | Estado | Alcance |
|---|---|---|
| 1. Fase 0 v3.3 | COMPLETADA Y ACEPTADA COMO LÍNEA BASE DOCUMENTAL, CON LIMITACIONES DOCUMENTADAS | No se reabre ni se modifica; SHA-256 `b5dccdc73a8103966ab1e1b1e84b2e7ead68cd736fba666ec71d0e790d51c1da` sin cambio |
| 2. Diseño complementario v6 (G-1, G-5, G-10) | PREPARADA PARA ACEPTACIÓN FORMAL DEL PROPIETARIO, CON LIMITACIONES DOCUMENTADAS | Pendiente de aceptación formal del propietario; no validado técnicamente; la Adenda v9 sigue sin aceptar (PO-05) |
| 3. Fase 1 | NO INICIADA / NO AUTORIZADA | Requiere autorización expresa; este diseño no la concede |


**Niveles de evidencia usados en este expediente.**

| Nivel de evidencia | Significado | Alcance |
|---|---|---|
| Diseñado | La regla o el escenario está escrito en la especificación | Nada ejecutado |
| Verificado documentalmente | El verificador publicado comprobó coherencia entre los documentos: IDs, referencias, cifras, contratos, orden, estados | Resultado reproducible; no prueba que el diseño funcione en PostgreSQL |
| Validado técnicamente | Ejecución real contra PostgreSQL, RLS y Supabase con las pruebas de la matriz | **Pendiente**: ningún control ni escenario alcanza este nivel |


Los tres hallazgos se corrigen en el diseño y se comprueban **documentalmente** con el verificador publicado. Ninguna prueba se ejecutó. G-5 no se declara completamente cerrada ni validada técnicamente. No hay aceptación del propietario de esta revisión.

## B. Qué se corrigió

### H-01 Auditoría no reproducible

| Concepto | Detalle |
|---|---|
| Defecto en la v5 | La v5 declaraba 28 controles sin matriz individual, con una herramienta interna no publicada y sin separar diseño, verificación documental y validación técnica. |
| Corrección | Niveles de evidencia (IE-05 a IE-08); matriz de 28 controles con 10 campos; verificador publicado `herramientas/verificar_expediente.py` con resultado por comprobación, controles negativos y prueba de reproducibilidad; ningún OK sin comprobación aprobada. |
| Documento y sección | AUDITORIA 1 y 3; ESPECIFICACION 11.2 |
| Reglas | IE-05, IE-06, IE-07, IE-08 |
| Evidencia | Verificador: 42 comprobaciones, salida real en AUDITORIA 3 |
| Escenarios diseñados | T-320 a T-327 (8; ninguno ejecutado) |

### H-02 Reconstrucción no determinista por campo material de brief y promociones

| Concepto | Detalle |
|---|---|
| Defecto en la v5 | version_contributors atribuía por versión, no por campo: cambiar el descuento podía borrar a quien definió condiciones que permanecían, y no había contrato de completitud. |
| Corrección | Cuatro tablas inmutables (brief_field_changes, brief_field_attributions, promotion_field_changes, promotion_field_attributions); regla de segmentos determinista; cálculo de atribuciones por tipo de cambio; historial que no se reactiva; algoritmos de 10 pasos; contrato con cinco categorías y diez errores; fail-closed. |
| Documento y sección | ESPECIFICACION 4.4.4, 4.4.5, 4.4.8 |
| Reglas | IG5-69 a IG5-79 |
| Evidencia | Verificador K12, K13, K38 |
| Escenarios diseñados | T-275 a T-300 (26; ninguno ejecutado) |

### H-03 Integridad incompleta entre eventos, versiones, snapshots, assets y personas

| Concepto | Detalle |
|---|---|
| Defecto en la v5 | Las referencias no validaban organización, versión exacta, tipo de origen y actor a la vez; la procedencia podía asociarse a una fuente de otro tipo o de otra organización. |
| Corrección | Claves compuestas con organization_id; contribution_events con origin_kind y exactamente un origen tipado; copy_version_provenance con nueve condiciones; copy_versions con referencias fijadas; actor desde el backend; contrato de integridad de 10 columnas. |
| Documento y sección | ESPECIFICACION 4.4.4 y 4.4.9 |
| Reglas | IG5-80 a IG5-87, IS-15, IS-16 |
| Evidencia | Verificador K14, K15, K26, K32, K33 |
| Escenarios diseñados | T-301 a T-319 (19; ninguno ejecutado) |

### Integración Flujo de 19 pasos sin cambiar T-02

| Concepto | Detalle |
|---|---|
| Defecto en la v5 | El flujo de G-1, G-5 y G-10 no incorporaba la verificación de procedencia por campo. |
| Corrección | Orden lógico de 19 pasos; la evaluación de impacto no sustituye la aprobación humana; las 13 transiciones de T-02 no cambian. |
| Documento y sección | ESPECIFICACION 4.4.7 |
| Reglas | IG5-88, IG5-89 |
| Evidencia | Verificador K30 |
| Escenarios diseñados | T-328 a T-335 (8; ninguno ejecutado) |

## C. Modelo y relaciones

| Elemento | Detalle |
|---|---|
| Tablas | 27 históricas sin cambio; 13 nuevas propuestas: `piece_classification_events`, `piece_reviewer_assignments`, `impact_evaluations`, `publication_attempts`, `channel_formats`, `brief_versions`, `promotion_snapshots`, `contribution_events`, `copy_version_provenance`, `brief_field_changes`, `brief_field_attributions`, `promotion_field_changes`, `promotion_field_attributions` |
| Orden definitivo | 1.8 → 2.x → 2.1 → 2.3 → 2.5 → 2.7 → 3.x → 4.x → 5.1 → 5.3 → 6.x → 6.1 → 6.5 → 6.6 → 8.x |
| Atribución por campo | 12 campos materiales de brief y 9 de promoción; una fila de cambio por campo y versión; atribuciones activas e históricas; el historial no se reactiva |
| Integridad | Toda FK es compuesta e incluye organization_id; contribution_events lleva exactamente un origen tipado (origin_kind); copy_version_provenance valida nueve condiciones; copy_versions fija sus referencias de forma inmutable; el actor viene de la identidad autenticada en el backend |
| Funciones | create_brief_version, create_promotion_snapshot, create_copy_version, verify_field_provenance (interna), version_contributors y las anteriores; escritura solo por funciones del propietario cci_records_owner con search_path fijo; SECURITY DEFINER no se toma como prueba de seguridad |
| Límites | IS-11: superusuario, propietario, desactivación de triggers y edición manual no los impide el diseño |

## D. Fórmula de contribuyentes y elegibilidad

**E = Ctr(V-A) ∪ Inh(V-A) ∪ ⋃ Ctr(v) para v ∈ [V-D, V-B] ∪ P.** La fórmula, la exclusión del proponente de la clasificación vigente (DT-02) y la ausencia de autoevaluación y de asignación automática a Admin no cambian respecto de la v5. Ante cualquiera de los diez errores de procedencia se bloquean la evaluación, la confirmación de independencia y la aprobación o publicación que dependan de ella, sin excepción de Admin; la ausencia de evidencia no es ausencia de contribuyente.

## E. Verificación

| Concepto | Resultado |
|---|---|
| Reglas de integridad | 200 |
| Pruebas diseñadas | 335 (documental 33 / técnica futura ejecutable 253 / infraestructura real 49); **ninguna ejecutada**; cobertura regla↔escenario completa según el verificador |
| Tablas propuestas | 40 (27 históricas + 13 nuevas) |
| Verificación documental | 42 comprobaciones del verificador publicado; resultado real en AUDITORIA_FINAL_G1_G5_G10.md, sección 3 |
| Pruebas técnicas no ejecutadas | Todas: no hay PostgreSQL, RLS, Supabase ni concurrencia real ejecutados |

## F. Pendientes

PO-05 y aceptación de la Adenda v9; aceptación formal de esta revisión; DG-09, DG-12, DG-16, DG-18, DG-19, DG-20; RP-01; P-01 a P-05; P-10; OD-13; G-9 completo; DEP-RET-01; valores reales de canal y formato; validación de infraestructura; pruebas reales de PostgreSQL, RLS y Supabase; pruebas reales de concurrencia, bloqueos y rollback; validación externa y operativa. Ninguno se resuelve en esta revisión.

## G. Integridad y GitHub

SHA-256 de v3.3: `b5dccdc73a8103966ab1e1b1e84b2e7ead68cd736fba666ec71d0e790d51c1da` (sin cambio). Publicación en `main` de `appalex47-lab/Copy-Creative-Intelligence`, carpeta `docs/fase0/`. Commit anterior `bb0af02bd170ce9c62cfd0741d8604cd41cab55e`. El commit nuevo y los SHA-256 de los cinco documentos se informan en el mensaje final.

## H. Declaración de alcance

Sin código de aplicación, sin SQL ejecutable, sin migraciones, sin recursos Supabase, sin infraestructura ni despliegue; v3.3 sin alterar; T-02 conserva sus 13 transiciones y no hay permisos nuevos (17 claves físicas); Fase 1 no iniciada; ninguna decisión del propietario se da por tomada y no se declara aceptación del propietario.
