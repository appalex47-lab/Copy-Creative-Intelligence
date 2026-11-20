---
name: roadmap_trazabilidad_g1_g5_g10
description: Roadmap y trazabilidad de la revisión v15 de G-1, G-5 y G-10; orden único de creación con la representación física de contribuciones; estados de subfases sin cambio
---

# ROADMAP Y TRAZABILIDAD — REVISIÓN v15 DE G-1, G-5 Y G-10

Sustituye a la v14 (conservada en `historico/`). Complementa la Adenda v9 (no aceptada) sin reemplazarla ni alterar versiones históricas. **Ninguna subfase cambia de estado**; el diseño no se ha implementado ni validado técnicamente y Fase 1 no está autorizada.

La corrección documental V16 (commit `6a1af2424ef39e0960b8f7e09d4e19ec52e6f046`) solo cambió la línea 15 de este documento, de v5 a v15, para identificar la versión vigente del diseño complementario; no es una revisión del diseño. La referencia a la v5 de la sección 4 es histórica y se conserva.

## 0. Estado por nivel (H-03)

| Nivel | Estado | Alcance |
|---|---|---|
| 1. Fase 0 v3.3 | COMPLETADA Y ACEPTADA COMO LÍNEA BASE DOCUMENTAL, CON LIMITACIONES DOCUMENTADAS | No se reabre ni se modifica; SHA-256 `b5dccdc73a8103966ab1e1b1e84b2e7ead68cd736fba666ec71d0e790d51c1da` sin cambio |
| 2. Diseño técnico complementario (G-1, G-5, G-10, v15) | COMPLETADO DOCUMENTALMENTE Y PREPARADO PARA ACEPTACIÓN FORMAL DEL PROPIETARIO, CON LIMITACIONES TÉCNICAS EXPLÍCITAS | Pendiente de aceptación formal del propietario; no validado técnicamente; DT-01, PC-02 y DT-02 resueltas en el diseño, sin aceptación; G-5 no se declara cerrada |
| 3. Fase 1 | NO INICIADA / NO AUTORIZADA | Requiere autorización expresa; el diseño complementario no la concede |


## 1. Trazabilidad de brechas

| Brecha | Qué es | Estado en v9 | Estado tras esta revisión | Subfase | Decisiones |
|---|---|---|---|---|---|
| G-1 | Vínculo maestra–adaptación y versión de origen | Pendiente (sin estructura) | Diseño documental completo: autorreferencia compuesta, versión de origen, catálogo de canales y formatos desde 1.8 | 1.8, 2.7 y 5.3 | DG-01 a 03, 14, 15; DG-19 (sujeta a aceptación) |
| G-2 | Atributo de canal y formato | Pendiente | Diseño documental completo: FK compuesta a channel_formats; catálogo creado antes de las piezas | 1.8 y 5.1 | DG-19 |
| G-3 | Autoría heredada | Pendiente | Diseño documental completo: definición única de contribuyente (4.4.3), nueve fuentes físicas (4.4.4), contrato de version_contributors con diez errores (4.4.5), reconstrucción por campo material de brief y promoción (4.4.8, H-02) y contrato de integridad con claves compuestas (4.4.9, H-03); verificado documentalmente, sin validar técnicamente ni aceptar | 2.1, 2.3, 3.1, 4.1 y 5.3 | DG-01, DG-17; DT-01, PC-02, H-02 y H-03 (precisadas en el diseño, sujetas a aceptación) |
| G-4 | Registro de la clasificación | Pendiente | Diseño documental completo: piece_classification_events; el proponente vigente queda excluido de evaluar esa adaptación (DT-02) | 5.3 y 6.5 | DG-01, DG-03; DT-02 |
| G-5 | Registro de la evaluación de impacto | Pendiente (sin estructura) | Diseño documental completo: par exacto, cadena lineal, independencia con E = Ctr(V-A) ∪ Inh(V-A) ∪ ⋃ Ctr(v) para v ∈ [V-D, V-B] ∪ P, procedencia verificable y fail-closed si falta una fuente. **No se declara plenamente cerrada**: sin aceptación del propietario ni validación técnica. impact_evaluations nace en 6.5 | 6.5 | DG-04 a 07, DG-17, DG-20; DT-01, PC-02, DT-02 |
| G-6 | Decisión de conservar o reabrir la aprobación | Pendiente | Cubierta por G-5; la reapertura usa T-02 #11; sin estado propio | 6.5 | DG-05 |
| G-7 | Control obligatorio de publicación | Mecanismo conceptual | Precisado (C1 a C9) y sustentado por G-1, G-5 y G-10; validación técnica pendiente | 6.1, 6.5 y 6.8 | DG-05 |
| G-8 | Notificaciones | Pendiente | Sin cambio | 2.7 y 6.6 | — |
| G-9 | Asignaciones explícitas | Pendiente | Parcial: solo el revisor asignado (DG-07); **G-9 completo sigue abierto** | 5.3 y 6.5 | DG-07 |
| G-10 | Registro de intentos de publicación bloqueados | Pendiente / parcial | Diseño documental completo: publication_attempts con db_txid más attempt_nonce, guarda de ocho condiciones y límites declarados (5.11); el aislamiento real queda como validación técnica pendiente | 6.1, 6.6 y 2.7 | DG-08, 10, 11, 13; DG-09 y DG-12 diferidas |
| PT | Verificación técnica de que no hay escritura directa | Pendiente | Diseño de privilegios y guarda; verificación técnica pendiente | 6.1 y 6.8 | — |

«Diseño documental completo» significa una solución coherente y verificada por script en el plano documental; **no** aceptación formal ni validación técnica.

## 2. Dependencias

| ID | Dependencia | Responsable |
|---|---|---|
| DEP-RET-01 | No existe procedimiento operativo para retirar contenido externo; el diseño no lo resuelve | Operativa |
| DEP-CAT-01 | Los valores reales de canales y formatos no existen; sin ellos no se puede crear ninguna pieza (DG-19) | Propietario u organización; antes de 2.5 |
| DEP-T04-01 | T-04 de v3.3 no fue aprobada; DT-01, PC-02 y DT-02 son diseño complementario de esta revisión y requieren aceptación formal del propietario | Decisión del propietario |
| DEP-NORM-01 | La normalización NFKC en PostgreSQL y los campos exactos evaluables de copy, brief y datos promocionales se fijan al diseñar 2.1, 2.3, 2.5 y 4.1 (RR-34, RR-35) | Diseño de las subfases |
| DEP-ARTE-01 | creative_assets.reused_from_asset_id (RR-38) y el uso de piece.review para resolver exclusiones (RR-37) requieren aceptación | Decisión del propietario |
| DEP-VER-01 | El orden de versión de la maestra no está fijado en v3.3; el intervalo V-D a V-B depende de él | Diseño de 2.7 |

## 3. Orden único de creación (H-01)

Secuencia de subfases: **1.8 → 2.x → 2.1 → 2.3 → 2.5 → 2.7 → 3.x → 4.x → 5.1 → 5.3 → 6.x → 6.1 → 6.5 → 6.6 → 8.x**. Es la misma que figura en la especificación (7.17 y 14.1) y en la auditoría. La subfase 5.4 ya no crea ninguna tabla.

| Orden | Subfase | Tipo | Objeto | Depende de (ya creado) |
|---|---|---|---|---|
| 1 | 1.8 | tabla (estructura) | organizations | — |
| 2 | 1.8 | tabla (estructura) | profiles | — |
| 3 | 1.8 | tabla (estructura) | memberships | organizations, profiles |
| 4 | 1.8 | tabla (estructura) | role_permissions | — |
| 5 | 1.8 | tabla (estructura) | membership_permission_grants | memberships |
| 6 | 1.8 | tabla (estructura) | activity_logs | — |
| 7 | 1.8 | tabla (estructura) | campaigns | organizations |
| 8 | 1.8 | tabla (estructura) | channel_rules | — |
| 9 | 1.8 | tabla (estructura) | channel_formats | channel_rules, memberships |
| 10 | 1.8 | tabla (estructura) | creative_pieces | campaigns, channel_formats |
| 11 | 1.8 | rol | cci_state_owner y cci_records_owner (roles de base de datos) | — |
| 12 | 1.8 | función | manage_channel_catalog | channel_rules, channel_formats |
| 13 | 1.8 | trigger | BEFORE INSERT sobre creative_pieces: catálogo activo (3.14) | channel_formats, creative_pieces |
| 14 | 1.8 | trigger | BEFORE INSERT y BEFORE UPDATE OF status sobre creative_pieces, versión base: INSERT solo en borrador; UPDATE de status solo por cci_state_owner; nunca Publicado | creative_pieces |
| 15 | 1.8 | habilitación | Políticas RLS y privilegios de channel_rules y channel_formats | tablas y funciones anteriores |
| 16 | 2.x | tabla (estructura) | brand_guidelines | — |
| 17 | 2.x | tabla (estructura) | brand_guideline_versions | brand_guidelines |
| 18 | 2.x | tabla (estructura) | briefs | campaigns |
| 19 | 2.x | tabla (estructura) | ai_runs | profiles |
| 20 | 2.x | tabla (estructura) | ai_prompt_versions | — |
| 21 | 2.x | tabla (estructura) | ai_quotas | — |
| 22 | 2.x | FK diferida | creative_pieces → briefs | creative_pieces, briefs |
| 23 | 2.1 | tabla (estructura) | brief_versions | briefs, memberships |
| 24 | 2.1 | tabla (estructura) | contribution_events | brief_versions, memberships |
| 25 | 2.1 | tabla (estructura) | brief_field_changes | brief_versions, contribution_events, memberships |
| 26 | 2.1 | tabla (estructura) | brief_field_attributions | brief_field_changes, contribution_events, memberships |
| 27 | 2.1 | función | record_contribution_event (interna; solo invocable por las funciones del propietario cci_records_owner; sin EXECUTE para roles de aplicación) | contribution_events |
| 28 | 2.1 | trigger | BEFORE INSERT sobre brief_versions: created_by = auth.uid(), version_number, snapshot_hash; BEFORE UPDATE, DELETE y TRUNCATE: rechazo (inmutable) | brief_versions |
| 29 | 2.1 | trigger | BEFORE UPDATE, DELETE y TRUNCATE sobre contribution_events: rechazo; la corrección es un evento nuevo | contribution_events |
| 30 | 2.1 | función | create_brief_version (única ruta de escritura de brief_versions; en una sola transacción calcula las 12 filas de cambio por campo y las atribuciones, y registra brief_editor cuando cambia un campo material) | brief_versions, briefs, contribution_events, brief_field_changes, brief_field_attributions |
| 31 | 2.1 | trigger | BEFORE UPDATE, DELETE y TRUNCATE sobre brief_field_changes y brief_field_attributions: rechazo; BEFORE INSERT: created_by = auth.uid() y coherencia con la versión (IG5-71) | brief_field_changes, brief_field_attributions |
| 32 | 2.1 | habilitación | Políticas RLS y privilegios de brief_versions, contribution_events, brief_field_changes y brief_field_attributions | tablas y funciones anteriores |
| 33 | 2.3 | tabla (estructura) | copy_versions | brief_versions, briefs, creative_pieces |
| 34 | 2.3 | tabla (estructura) | copy_version_provenance | contribution_events, copy_versions, memberships |
| 35 | 2.3 | columna agregada | contribution_events.copy_version_id | contribution_events |
| 36 | 2.3 | columna agregada | contribution_events.copy_version_piece_id | contribution_events |
| 37 | 2.3 | FK agregada | contribution_events → copy_versions | contribution_events, copy_versions |
| 38 | 2.3 | FK diferida | creative_pieces → copy_versions | creative_pieces, copy_versions |
| 39 | 2.3 | función | create_copy_version (versión inmutable de copy; fija brief_version_id; registra copy_author y la procedencia directa) | copy_versions, brief_versions, contribution_events, copy_version_provenance |
| 40 | 2.3 | trigger | BEFORE UPDATE, DELETE y TRUNCATE sobre copy_version_provenance: rechazo; coherencia de la procedencia | copy_version_provenance |
| 41 | 2.3 | habilitación | Políticas RLS y privilegios de copy_version_provenance | tablas y funciones anteriores |
| 42 | 2.5 | función | detect_material_change (interna): normalización NFKC, saltos de línea, espacios repetidos y extremos; decide copy_editor y la herencia; en duda conserva la atribución anterior | copy_versions, contribution_events, copy_version_provenance |
| 43 | 2.7 | función | verify_version_chain (interna): cadena exacta de versiones y orden de versión de la maestra; VERSION_CHAIN_INCONSISTENTE | copy_versions |
| 44 | 3.x | tabla (estructura) | creative_assets | copy_versions, creative_pieces |
| 45 | 3.x | tabla (estructura) | audit_rubric_versions | — |
| 46 | 3.x | tabla (estructura) | audits | ai_runs, audit_rubric_versions, copy_versions, creative_assets |
| 47 | 3.x | tabla (estructura) | audit_findings | audits |
| 48 | 3.x | columna agregada | contribution_events.asset_copy_version_id | contribution_events |
| 49 | 3.x | columna agregada | contribution_events.asset_piece_id | contribution_events |
| 50 | 3.x | columna agregada | contribution_events.creative_asset_id | contribution_events |
| 51 | 3.x | columna agregada | copy_version_provenance.origin_asset_id | copy_version_provenance |
| 52 | 3.x | columna agregada | copy_version_provenance.used_asset_id | copy_version_provenance |
| 53 | 3.x | FK diferida | copy_versions → creative_assets | copy_versions, creative_assets |
| 54 | 3.x | FK agregada | contribution_events → creative_assets | contribution_events, creative_assets |
| 55 | 3.x | FK agregada | copy_version_provenance → creative_assets | copy_version_provenance, creative_assets |
| 56 | 3.x | FK diferida | creative_pieces → creative_assets | creative_pieces, creative_assets |
| 57 | 3.x | función | register_asset_contribution: asset_uploader al cargar o reemplazar arte (identidad del servidor) | creative_assets, contribution_events |
| 58 | 4.x | tabla (estructura) | promotion_rules | campaigns |
| 59 | 4.x | tabla (estructura) | promotion_snapshots | memberships, promotion_rules |
| 60 | 4.x | tabla (estructura) | promotion_field_changes | contribution_events, memberships, promotion_snapshots |
| 61 | 4.x | tabla (estructura) | promotion_field_attributions | contribution_events, memberships, promotion_field_changes |
| 62 | 4.x | tabla (estructura) | validation_settings_versions | — |
| 63 | 4.x | columna agregada | contribution_events.promotion_snapshot_id | contribution_events |
| 64 | 4.x | columna agregada | copy_versions.promotion_snapshot_id | copy_versions |
| 65 | 4.x | FK agregada | copy_versions → promotion_snapshots | copy_versions, promotion_snapshots |
| 66 | 4.x | FK agregada | contribution_events → promotion_snapshots | contribution_events, promotion_snapshots |
| 67 | 4.x | FK diferida | audits → validation_settings_versions | audits, validation_settings_versions |
| 68 | 4.x | función | create_promotion_snapshot (única ruta de escritura de promotion_snapshots; en una sola transacción calcula las 9 filas de cambio por campo y las atribuciones, y registra promotion_editor cuando cambia un campo material) | promotion_snapshots, promotion_rules, contribution_events, promotion_field_changes, promotion_field_attributions |
| 69 | 4.x | trigger | BEFORE INSERT sobre promotion_snapshots: created_by = auth.uid(), snapshot_hash; BEFORE UPDATE, DELETE y TRUNCATE: rechazo (inmutable) | promotion_snapshots |
| 70 | 4.x | trigger | BEFORE UPDATE, DELETE y TRUNCATE sobre promotion_field_changes y promotion_field_attributions: rechazo; BEFORE INSERT: created_by = auth.uid() y coherencia con el snapshot (IG5-71) | promotion_field_changes, promotion_field_attributions |
| 71 | 4.x | habilitación | Políticas RLS y privilegios de promotion_snapshots, promotion_field_changes y promotion_field_attributions | tablas y funciones anteriores |
| 72 | 5.1 | columnas | Columnas anulables de reglas (extensión, tono, estructura, CTA) agregadas a channel_rules | channel_rules |
| 73 | 5.3 | tabla (estructura) | piece_classification_events | creative_pieces, memberships |
| 74 | 5.3 | tabla (estructura) | attribution_discard_resolutions | brief_field_attributions, contribution_events, copy_version_provenance, memberships, promotion_field_attributions |
| 75 | 5.3 | tabla (estructura) | piece_reviewer_assignments | creative_pieces, memberships |
| 76 | 5.3 | función | create_adaptation | creative_pieces, copy_versions, channel_formats |
| 77 | 5.3 | función | verify_field_provenance (interna, STABLE): recorre la cadena de versiones de brief y de promoción, recalcula por campo las atribuciones esperadas y las compara con las filas; BRIEF_CHAIN_INCONSISTENTE, PROMOTION_CHAIN_INCONSISTENTE, BRIEF_FIELD_PROVENANCE_INCOMPLETE, PROMOTION_FIELD_PROVENANCE_INCOMPLETE | brief_versions, brief_field_changes, brief_field_attributions, promotion_snapshots, promotion_field_changes, promotion_field_attributions, contribution_events |
| 78 | 5.3 | función | version_contributors (interna, STABLE): conjunto de contribuyentes, evidencias, completitud y error; lee solo fuentes físicas versionadas | copy_versions, brief_versions, brief_field_changes, brief_field_attributions, promotion_snapshots, promotion_field_changes, promotion_field_attributions, creative_assets, contribution_events, copy_version_provenance, attribution_discard_resolutions |
| 79 | 5.3 | función | resolve_attribution_discard: resolución independiente de descarte de una atribución (registro nuevo en attribution_discard_resolutions; nunca retroactiva; fail-closed sin evidencia o sin resolutor elegible) | attribution_discard_resolutions, brief_field_attributions, promotion_field_attributions, copy_version_provenance, contribution_events, memberships |
| 80 | 5.3 | función | eligible_evaluators | piece_reviewer_assignments, memberships, copy_versions, creative_assets, piece_classification_events, contribution_events, copy_version_provenance |
| 81 | 5.3 | función | propose_independence | piece_classification_events, creative_pieces |
| 82 | 5.3 | función | resolve_independence | piece_classification_events, piece_reviewer_assignments |
| 83 | 5.3 | función | assign_reviewer | piece_reviewer_assignments, memberships |
| 84 | 5.3 | habilitación | Políticas RLS y privilegios de piece_classification_events y piece_reviewer_assignments | tablas y funciones anteriores |
| 85 | 6.x | tabla (estructura) | comments | audit_findings, creative_pieces |
| 86 | 6.x | tabla (estructura) | commercial_block_exceptions | audit_findings, memberships |
| 87 | 6.1 | función | transition_piece_status (T-02 sin la transición a Publicado habilitada) | creative_pieces, comments, memberships |
| 88 | 6.5 | tabla (estructura) | approvals | audits, copy_versions, creative_assets, memberships |
| 89 | 6.5 | tabla (estructura) | impact_evaluations | approvals, copy_versions, creative_assets, creative_pieces, memberships, piece_reviewer_assignments |
| 90 | 6.5 | trigger | BEFORE INSERT sobre approvals: coherencia del arte (4.13) | approvals, creative_assets |
| 91 | 6.5 | función | record_approval (ampliada) | approvals, copy_versions, creative_assets, audits, memberships |
| 92 | 6.5 | función | record_impact_evaluation | impact_evaluations, approvals, piece_reviewer_assignments, memberships |
| 93 | 6.5 | habilitación | Políticas RLS y privilegios de approvals e impact_evaluations | tablas y funciones anteriores |
| 94 | 6.6 | tabla (estructura) | publication_attempts | approvals, copy_versions, creative_pieces, impact_evaluations, memberships |
| 95 | 6.6 | trigger | BEFORE INSERT sobre publication_attempts: db_txid, attempted_at, attempt_nonce, actor (5.11) | publication_attempts |
| 96 | 6.6 | trigger | Sustituye el cuerpo de piece_status_guard por la guarda de ocho condiciones (5.11) | publication_attempts, approvals, impact_evaluations, memberships, creative_pieces |
| 97 | 6.6 | función | transition_piece_status ampliada: habilita la transición a Publicado (#10) | publication_attempts, approvals, impact_evaluations, creative_pieces |
| 98 | 6.6 | habilitación | Políticas RLS y privilegios de publication_attempts y la transición a Publicado | tablas y funciones anteriores |
| 99 | 8.x | tabla (estructura) | performance_metrics | creative_pieces |
| 100 | 8.x | tabla (estructura) | ab_tests | creative_pieces, performance_metrics |

Estructura no es operación: las tablas nacen con RLS activada y sin privilegios; las funciones y políticas se habilitan en la subfase indicada. Si una fase posterior no se ejecuta, las anteriores siguen siendo consistentes porque ninguna FK apunta hacia adelante. La reversión es deshabilitar (retirar EXECUTE y privilegios, restaurar el trigger base), no eliminar tablas con datos.

## 4. Cambios de subfase por la v5, la v6, la v7, la v8, la v11, la v12, la v13, la v14 y la v15 (la v7 agregó attribution_discard_resolutions y resolve_attribution_discard dentro de subfases existentes; la v8 agrega columnas a esa tabla y una unicidad en contribution_events dentro de las mismas subfases; la v11, la v12, la v13, la v14 y la v15 solo cambian el verificador, el modelo estructural, las secciones 4.4.11 a 4.4.17 y las FK y restricciones documentadas dentro de subfases existentes (RS-01 a RS-08; la v14 agrega RS-08 y una restricción única propia de creative_assets); no cambian subfases ni estados)

| Subfase | Tema | Contenido de diseño |
|---|---|---|
| 1.8 | Migraciones | Tablas base, catálogo, creative_pieces, roles propietarios, manage_channel_catalog y triggers base |
| 2.1 | Brief | brief_versions, brief_field_changes, brief_field_attributions, contribution_events (origen brief), create_brief_version y triggers de inmutabilidad |
| 2.3 | Generación de propuestas | copy_versions, copy_version_provenance, origen copy de contribution_events y create_copy_version |
| 2.5 | Edición | detect_material_change y herencia por procedencia |
| 2.7 | Versionado | verify_version_chain |
| 3.1 | Carga de imágenes | reused_from_asset_id, origen arte y register_asset_contribution |
| 4.1 | Modelo de promociones | promotion_snapshots, promotion_field_changes, promotion_field_attributions, origen promoción y create_promotion_snapshot |
| 5.1 | Modelos de canal | Solo columnas de reglas anulables |
| 5.3 | Adaptación | Clasificación, asignación, verify_field_provenance, version_contributors, exclusión de atribuciones y elegibilidad |
| 5.4 | Consistencia entre adaptaciones | Sin tablas propias; usa las evaluaciones de 6.5 |
| 6.1 | Workflow | transition_piece_status base; Publicado deshabilitado |
| 6.5 | Aprobaciones | approvals e impact_evaluations en el orden correcto; revalidación de procedencia y clasificación |
| 6.6 | Auditoría del flujo | publication_attempts, guarda completa y transición #10 |
| 6.8 | Pruebas | Matriz documental con 780 casos (ninguno ejecutado) |

**Distinción por subfase.** *Diseño documental*: esta revisión. *Preparación técnica*: tablas, funciones y triggers que cada subfase crearía; nada existe. *Implementación*: Fase 1 y siguientes, no iniciadas. *Validación real*: pruebas en PostgreSQL y Supabase, pendientes. Se adelanta copy_version_provenance a 2.3 y contribution_events a 2.1 por dependencia real (la primera operación que las necesita). Los nombres de subfase son los de la Adenda v9 (76 subfases, sin subfase 77).

## Roadmap consolidado (estados de la Adenda v9, sin cambio)

Situación: **Fase 0** (subfases 0.1–0.7) aceptada y cerrada como línea base documental v3.3, con limitaciones documentadas; **0.8 no es oficial ni está aprobada**. **Etapa de decisiones documentales PO/OD:** documentadas y pendientes de aceptación formal del propietario (el addendum no está aceptado). **Fase 1 y posteriores:** NO INICIADAS NI AUTORIZADAS para implementación. Las decisiones documentadas no son funcionalidades desarrolladas ni validadas técnicamente. No se oficializan subfases nuevas. Contenido tomado de v3.3 §8 (propuesta); las columnas «Limitaciones» y «Decisiones previas» se agregaron aquí.

#### Fase 0 — Discovery y arquitectura (0.1–0.7)

| ID | Nombre | Objetivo | Entregables | Criterios de aceptación | Dependencias | Riesgos | Estado | Limitaciones conocidas | Decisiones que deben estar resueltas antes |
|---|---|---|---|---|---|---|---|---|---|
| 0.1 | Inspección del entorno | Conocer qué hay disponible | Sección Línea base | Entorno descrito | — | Herramientas sin verificar | COMPLETADA CON LIMITACIONES (dictamen del maestro; fase aceptada como línea base documental v3.3) | Nivel 1: diseño sin ejecutar (L-01). | No aplica (Fase 0 cerrada). |
| 0.2 | Definición de arquitectura | Capas, IA desacoplada, estructura | Arquitectura y estructura | Revisada y consistente | 0.1 | Es diseño | COMPLETADA (dictamen del maestro; fase aceptada como línea base documental v3.3) | Nivel 1: diseño sin ejecutar (L-01). | No aplica (Fase 0 cerrada). |
| 0.3 | Modelo de datos | 27 tablas, relaciones, controles | Modelo, auditoría, matriz | Sin tablas nuevas; auditado | 0.2 | Sin SQL | COMPLETADA CON LIMITACIONES (dictamen del maestro; fase aceptada como línea base documental v3.3) | Nivel 1: diseño sin ejecutar (L-01). | No aplica (Fase 0 cerrada). |
| 0.4 | Seguridad | RLS, permisos, separación de funciones | Seguridad y RLS | Matriz de 17 claves | 0.3 | RLS sin probar | COMPLETADA CON LIMITACIONES (dictamen del maestro; fase aceptada como línea base documental v3.3) | Nivel 1: diseño sin ejecutar (L-01). | No aplica (Fase 0 cerrada). |
| 0.5 | Diseño de módulos | Módulos y transiciones | Diseño de módulos | Cobertura de módulos | 0.2 | Pantallas por detallar | COMPLETADA (dictamen del maestro; fase aceptada como línea base documental v3.3) | Nivel 1: diseño sin ejecutar (L-01). | No aplica (Fase 0 cerrada). |
| 0.6 | Estrategia de pruebas | Qué y cómo probar | Plan de pruebas | Casos R-01..R-05 | 0.3–0.5 | Herramientas sin instalar | COMPLETADA CON LIMITACIONES (dictamen del maestro; fase aceptada como línea base documental v3.3) | Nivel 1: diseño sin ejecutar (L-01). | No aplica (Fase 0 cerrada). |
| 0.7 | Registro de riesgos y dependencias | Riesgos y dependencias externas | Riesgos, Configuraciones | Riesgos con mitigación | 0.1–0.6 | Retención y respaldos sin determinar | COMPLETADA (dictamen del maestro; fase aceptada como línea base documental v3.3) | Nivel 1: diseño sin ejecutar (L-01). | No aplica (Fase 0 cerrada). |

#### Fase 1 — Foundation & Command Center (requiere A-01 y tu autorización expresa)

| ID | Nombre | Objetivo | Entregables | Criterios de aceptación | Dependencias | Riesgos | Estado | Limitaciones conocidas | Decisiones que deben estar resueltas antes |
|---|---|---|---|---|---|---|---|---|---|
| 1.1 | Estructura del proyecto | Esqueleto modular con ES Modules, capas UI, dominio, servicios, IA | Repositorio base, README | Arranca en local; refleja la estructura del maestro | A-01, P-02 | Acoplar UI y dominio | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | P-02 resuelta (OD-13, OD-16); autorización expresa de Fase 1. |
| 1.2 | Sistema visual | Tokens y componentes base | CSS y componentes | Sin elementos recargados | 1.1 | Inconsistencia | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | Ninguna decisión específica de esta matriz; ver dependencias. |
| 1.3 | Navegación | Sidebar, header, rutas | Shell de la app | Navegación clara | 1.2 | Navegación confusa | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | Ninguna decisión específica de esta matriz; ver dependencias. |
| 1.4 | Autenticación | Supabase Auth, sesiones, rutas protegidas | Login y sesión | Rutas protegidas probadas | 1.1, P-01 | Manejo de sesión | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | P-01 resuelta (OD-16). |
| 1.5 | Organización y usuarios | organizations, profiles, memberships | Alta de organización y personas | Aislamiento entre organizaciones | 1.4, P-04 | Fuga entre organizaciones | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | PO-01, PO-18 (membresía y elegibilidad del concedente); N-01 y N-02 de DA-02 (pendiente de diseño). |
| 1.6 | Roles y permisos | role_permissions, permisos por persona, 17 claves | Funciones de permisos | Matriz probada en backend y frontend | 1.5 | Permisos solo en la interfaz | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | T-01; OD-05 a OD-08; PO-02, PO-15 y PO-18 (delegation.manage y block.exception.revoke conceptuales; 17 claves sin cambio); PO-07; N-01. |
| 1.7 | Supabase | Proyecto, Storage, secretos | Entorno configurado | Sin credenciales en el repositorio | P-01 | Plan gratuito | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | P-01; PO-07 (nivel 2: verificar capacidades de la plataforma); herramientas verificadas si la estrategia lo requiere (Q1). |
| 1.8 | Migraciones | Esquema versionado y RLS de las tablas de la fase | Migraciones reproducibles | Pruebas de aislamiento de las tablas creadas | 1.6, 1.7 | Primer SQL real | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | T-04 (PO-08): modelo conceptual antes de 1.8; durante 1.8, trazabilidad base implementada y validada en su alcance real (activity_logs es el mecanismo de eventos disponible antes de 2.7: DA-01); T-09 plan de migración; herramientas (Q1). **Ajuste v4:** crea las tablas base, channel_rules (estructura mínima), channel_formats y creative_pieces con la FK al catálogo; los roles propietarios cci_state_owner y cci_records_owner; manage_channel_catalog; y los triggers catalog_active_check y piece_status_guard_base. Todo nace con RLS activada y sin privilegios (estructura, no operación). |
| 1.9 | Dashboard inicial | Command Center básico | Dashboard | Carga sin datos | 1.3, 1.8 | Exceso de tarjetas | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | Command Center básico: no entrega notificaciones (v3.3); DA-02: sin evento propio. |

#### Fase 2 — Copy Studio

| ID | Nombre | Objetivo | Entregables | Criterios de aceptación | Dependencias | Riesgos | Estado | Limitaciones conocidas | Decisiones que deben estar resueltas antes |
|---|---|---|---|---|---|---|---|---|---|
| 2.1 | Brief | Brief de 16 campos y su versión | Formulario y tabla | Validaciones y versiones | 1.8 | Formularios largos | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | P-03 antes de Fase 2; T-04: aportaciones de Brief trazadas y probadas durante 2.1, antes de habilitar el flujo; PO-16 para versiones de brief; DA-02: notificaciones de Brief (pendiente de asignación). **Ajuste v4:** diseño documental de brief_versions (inmutable, created_by = auth.uid()), de brief_field_changes y brief_field_attributions (atribución por campo material, H-02) y de contribution_events (append-only); preparación técnica: esas cuatro tablas, create_brief_version (12 filas de cambio y atribuciones por versión), record_contribution_event y los triggers de inmutabilidad; la implementación y la validación real siguen pendientes (Fase 1 no iniciada). |
| 2.2 | Integración Cohere | Servicio de IA desacoplado, cuotas, registro | Servicio y ai_runs | Llamadas registradas; sin claves en cliente | P-03 | Límites de la clave de prueba | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | P-03; PO-11: solo registra llamadas; DA-02 N-03 (cuota de IA). |
| 2.3 | Generación de propuestas | Varias propuestas por brief | Generación | Salida estructurada válida | 2.1, 2.2 | Calidad variable | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | DA-01: procedencia de propuestas de copy generadas, trazada y probada antes de habilitar 2.3 con los mecanismos definidos (activity_logs, ai_runs); PO-16; DA-02. **Ajuste v4:** crea copy_versions con brief_version_id exacto, copy_version_provenance (adelantada desde 2.7 porque la primera versión necesita su procedencia: dependencia real), la columna y FK de origen copy de contribution_events y create_copy_version (copy_author y procedencia directa). |
| 2.4 | Fórmulas de copywriting | Fórmulas aplicables | Catálogo de fórmulas | Aplicación verificable | 2.3 | Sesgo hacia plantillas | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | Ninguna decisión específica de esta matriz; ver dependencias. |
| 2.5 | Edición | Edición humana de copy | Editor | Cambios guardados como versión | 2.3 | Pérdida de cambios | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | DA-01: modificaciones, adaptaciones manuales y aportaciones sobre el copy trazadas desde 2.5 (DD-1, DD-2); PO-16. **Ajuste v4:** detect_material_change: normalización NFKC, saltos de línea, espacios repetidos y extremos; decide copy_editor y la herencia; en duda se conserva la atribución anterior. |
| 2.6 | Comparación | Comparar versiones | Vista de comparación | Diferencias correctas | 2.5 | Confusión de versiones | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | Ninguna decisión específica de esta matriz; ver dependencias. |
| 2.7 | Versionado | Versiones inmutables con autor | copy_versions | Autor por trigger; sin edición de versiones | 2.5 | Autoría falsificable | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | DA-01; PO-16; adaptaciones: relación de versiones entre pieza maestra y adaptación (G-1, G-3). PO-20: relación de versiones maestra–adaptación (G-1) y trazabilidad de la evaluación (G-5). **Ajuste v4:** verify_version_chain: cadena exacta de versiones y orden de versión de la maestra (VERSION_CHAIN_INCONSISTENTE); no crea tablas nuevas. |
| 2.8 | Pruebas | Pruebas de la fase | Informe | Suite ejecutada | 2.1–2.7 | Mocks tomados por integración real | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | DA-02: validación técnica de las notificaciones de Brief y Copy (subfase de pruebas existente). |

#### Fase 3 — Creative Auditor

| ID | Nombre | Objetivo | Entregables | Criterios de aceptación | Dependencias | Riesgos | Estado | Limitaciones conocidas | Decisiones que deben estar resueltas antes |
|---|---|---|---|---|---|---|---|---|---|
| 3.1 | Carga de imágenes | Subir artes con hash y MIME | creative_assets, Storage | Hash y MIME verificados; objeto inmutable | 1.7, P-07 | Archivos grandes | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | P-07 validada técnicamente; T-04: aportaciones de carga de assets trazadas y probadas antes de habilitar ese flujo; PO-16 (herencia entre versiones de arte: sin subfase asignada); DA-02. **Ajuste v4:** agrega a creative_assets reused_from_asset_id, la columna y FK de origen arte en contribution_events y register_asset_contribution (asset_uploader). |
| 3.2 | OCR | Extraer texto del arte | Resultado de OCR | Texto como inferencia, no como hecho | 3.1 | Cohere sin OCR confirmado | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | Ninguna decisión específica de esta matriz; ver dependencias. |
| 3.3 | Integración de visión | Modelo de visión tras el servicio de IA | Adaptador de visión | Salida estructurada confirmada | 2.2 | Modelo de visión no confirmado | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | Ninguna decisión específica de esta matriz; ver dependencias. |
| 3.4 | Auditoría textual | Hallazgos, clasificación de afirmaciones, estados de hallazgo | audit_findings | R-01 y R-02 pasan | 3.2, 3.3 | Falsos positivos | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | DA-02 N-04: aviso por auditoría con hallazgos pendientes de decisión. |
| 3.5 | Auditoría visual | Hallazgos visuales | Auditoría visual | Hallazgos de IA no bloquean | 3.3 | Subjetividad | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | Ninguna decisión específica de esta matriz; ver dependencias. |
| 3.6 | Auditoría UX | Legibilidad y UX | Auditoría UX | Notas con evidencia | 3.3 | Subjetividad | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | Ninguna decisión específica de esta matriz; ver dependencias. |
| 3.7 | Scoring | Motor determinístico en JavaScript | Motor y rúbrica | Casos límite de R-05 pasan | 3.4–3.6 | Redondeo | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | T-08: pruebas de equivalencia del cálculo entero (OD-12). |
| 3.8 | Comparación de versiones | Comparar auditorías | Vista | Versión exacta por auditoría | 3.7 | Versiones mezcladas | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | Ninguna decisión específica de esta matriz; ver dependencias. |
| 3.9 | Pruebas | Pruebas de la fase | Informe | Suite ejecutada | 3.1–3.8 | Mocks | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | DA-02: validación técnica de las notificaciones de assets y diseño. |

#### Fase 4 — Promotion Validator

| ID | Nombre | Objetivo | Entregables | Criterios de aceptación | Dependencias | Riesgos | Estado | Limitaciones conocidas | Decisiones que deben estar resueltas antes |
|---|---|---|---|---|---|---|---|---|---|
| 4.1 | Modelo de promociones | promotion_rules y relación con campañas y briefs (T-07, T-11) | Tabla y relación | Validación funcional de la sección 5.3 | 1.8, P-06 | Caso C-1; sin FK real | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | P-06 impuestos; T-07 esquema y validaciones; T-04: aportaciones de datos promocionales trazadas y probadas antes de habilitar ese flujo; PO-16 (sin subfase para herencia); DA-02. **Ajuste v4:** crea promotion_snapshots (inmutable), promotion_field_changes y promotion_field_attributions (atribución por campo, H-02), la columna y FK de origen promoción en contribution_events, copy_versions.promotion_snapshot_id con su FK y create_promotion_snapshot (promotion_editor). |
| 4.2 | Reglas matemáticas | Precios, descuentos, redondeo | Funciones deterministas | Tolerancia 0.5 pp aplicada | 4.1, P-06 | Redondeo | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | P-08: casos de prueba y valor autorizado. |
| 4.3 | Validación de vigencias | Fechas y rangos | Validador | Incoherencias marcadas | 4.1 | Zonas horarias | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | Ninguna decisión específica de esta matriz; ver dependencias. |
| 4.4 | Validación de condiciones | Condiciones y disponibilidad | Validador | Condiciones contrastadas | 4.1 | Texto ambiguo | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | Ninguna decisión específica de esta matriz; ver dependencias. |
| 4.5 | Comparación de fuentes | Brief, regla y arte | Comparador | Diferencias reportadas | 4.2–4.4 | Fuentes incompletas | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | Ninguna decisión específica de esta matriz; ver dependencias. |
| 4.6 | Bloqueos comerciales | Bloqueos del motor y confirmados | Bloqueos | Bloqueo confirmado impide aprobar | 4.5 | Falsos bloqueos | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | DA-02 N-05: bloqueo comercial confirmado (D-05). |
| 4.7 | Pruebas | Pruebas de la fase | Informe | Suite y validación de promociones-campañas | 4.1–4.6 | Mocks | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | DA-02: validación técnica de las notificaciones de promociones. |

#### Fase 5 — Channel Adaptation

| ID | Nombre | Objetivo | Entregables | Criterios de aceptación | Dependencias | Riesgos | Estado | Limitaciones conocidas | Decisiones que deben estar resueltas antes |
|---|---|---|---|---|---|---|---|---|---|
| 5.1 | Modelos de canal | channel_rules por canal | Catálogo | Reglas por organización y canal | 1.8 | Reglas reales sin entregar | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | Atributo de canal (G-2); canal por organización; G-2. **Ajuste v4:** solo agrega columnas anulables de reglas a channel_rules (ya existente); no crea tablas. |
| 5.2 | Reglas de extensión | Límites de longitud | Validador | Límites aplicados | 5.1 | Límites cambiantes | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | Ninguna decisión específica de esta matriz; ver dependencias. |
| 5.3 | Adaptación | Adaptar copy por canal | Adaptador | Versión por canal | 2.3, 5.1 | Pérdida de sentido | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | T-04: adaptación por canal trazada y probada antes de habilitar 5.3; PO-20 (evaluación de impacto, dependencia de aprobación, declaración de independencia); G-1, G-3, G-4; sin tabla ni columna nueva. **Ajuste v4:** crea piece_classification_events, piece_reviewer_assignments, attribution_discard_resolutions (resolución independiente de descarte, H-02 v7), create_adaptation, version_contributors, resolve_attribution_discard, verify_field_provenance (cadenas y atribuciones por campo de brief y promoción), eligible_evaluators, propose_independence, resolve_independence y assign_reviewer. **La trazabilidad de contribuciones solo está completa aquí porque sus fuentes (ocho tablas, más copy_versions y creative_assets) se crean antes (2.1, 2.3 y 4.1)**; si alguna fase previa no se ejecutó, version_contributors falla cerrado. |
| 5.4 | Consistencia | Coherencia entre canales | Verificador | Diferencias señaladas | 5.3 | Falsas diferencias | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | DA-02 N-06 y N-22; PO-20: evaluación de impacto de la maestra (G-5). PO-21: evaluación de impacto por el revisor asignado independiente (sin estado nuevo). |
| 5.5 | Comparación multicanal | Vista comparativa | Vista | Comparación correcta | 5.3 | — | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | Comparación multicanal: no genera notificación; usa la relación maestra–adaptación (G-1). |
| 5.6 | Pruebas | Pruebas de la fase | Informe | Suite ejecutada | 5.1–5.5 | Mocks | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | DA-02: validación técnica de las notificaciones de Fase 5. |

#### Fase 6 — Workflow & Approvals

| ID | Nombre | Objetivo | Entregables | Criterios de aceptación | Dependencias | Riesgos | Estado | Limitaciones conocidas | Decisiones que deben estar resueltas antes |
|---|---|---|---|---|---|---|---|---|---|
| 6.1 | Estados | Estados y transiciones (T-02) | transition_piece_status | Solo transiciones permitidas | 1.6 | Estados bloqueados | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | T-02 (13 transiciones verificadas contra v3.3; aplican a cada adaptación independiente); PO-13; AR-01; DA-02 N-09 a N-11, N-16, N-17 y N-22; G-7: control obligatorio de publicación en transition_piece_status (condiciones C1 a C9) y G-10 (registro del intento bloqueado). **Ajuste v4:** transition_piece_status en versión base, con el estado Publicado deshabilitado; sustituye al trigger base de 1.8 sin tocar datos. |
| 6.2 | Asignaciones | Asignar piezas a personas | Asignaciones | Asignación auditada | 6.1 | — | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | Asignación de responsable, revisor y aprobador: D-02; destinatarios de PO-19; DA-02 N-07. PO-20: revisor asignado que confirma la independencia; regla D (asignaciones explícitas, G-9). |
| 6.3 | Comentarios | Hilos y solicitudes de cambio | comments | Comentarios obligatorios donde corresponde | 6.1 | — | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | Solicitudes de cambio como evento informativo a contribuyentes (N-08); DA-02. |
| 6.4 | Correcciones | Ciclo de corrección con versión nueva | Flujo | Aprobación previa no se hereda | 6.1–6.3 | Reprocesos | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | Ninguna decisión específica de esta matriz; ver dependencias. |
| 6.5 | Aprobaciones | Aprobación humana independiente, confirmación y descarte, excepciones | record_approval, review_finding, excepciones | R-02 y R-03 pasan; sin autoaprobación | 6.4, P-04, P-05 | Menos de dos personas capaces | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | T-03, T-05, T-06, OD-06, OD-09, OD-10; P-05; PO-10, PO-12, PO-15, PO-16, PO-18; PO-14, PO-17, PO-19, AR-01; DA-02 N-12 a N-15. PO-20: decisión sobre cada adaptación afectada (G-6). G-7: verificación de aprobación de la maestra y de la adaptación antes de publicar. **Ajuste v4:** crea approvals (decision con CHECK = 'aprobada', unique(org,id,copy_version_id), asset_match), record_approval, impact_evaluations y record_impact_evaluation, que revalida bajo bloqueo la clasificación vigente, su proponente y la procedencia completa (IG5-68). impact_evaluations nace aquí y no en 5.4 (v4). |
| 6.6 | Historial | Historial inmutable | activity_logs | Sin UPDATE ni DELETE | 6.5 | Volumen | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | Historial inmutable: trazabilidad de eventos de notificación según DA-02 (sin afirmar que cubre entrega). G-10: trazabilidad de intentos de publicación bloqueados. **Ajuste v4:** crea publication_attempts, el trigger de db_txid y attempt_nonce, la guarda completa que sustituye a la base y habilita la transición #10 de transition_piece_status. |
| 6.7 | Permisos | Permisos del flujo | Claves y políticas | Backend como autoridad | 6.5 | Permisos solo en UI | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | Permisos del flujo; DA-02 (restricciones de acceso al contenido de notificaciones). |
| 6.8 | Pruebas | Pruebas de la fase | Informe | Suite ejecutada | 6.1–6.7 | Mocks | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | DA-02: validación de permisos, estados, destinatarios, independencia y trazabilidad de notificaciones (subfase de pruebas existente). |

#### Fase 7 — Creative Library

| ID | Nombre | Objetivo | Entregables | Criterios de aceptación | Dependencias | Riesgos | Estado | Limitaciones conocidas | Decisiones que deben estar resueltas antes |
|---|---|---|---|---|---|---|---|---|---|
| 7.1 | Biblioteca | Repositorio de piezas aprobadas | Vista | Solo versiones identificadas | 6.5 | Volumen | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | Ninguna decisión específica de esta matriz; ver dependencias. |
| 7.2 | Búsqueda | Búsqueda de piezas | Búsqueda | Resultados correctos | 7.1 | Rendimiento | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | Ninguna decisión específica de esta matriz; ver dependencias. |
| 7.3 | Filtros | Filtros combinables | Filtros | Combinaciones correctas | 7.1 | — | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | Ninguna decisión específica de esta matriz; ver dependencias. |
| 7.4 | Versionado | Historial de versiones | Vista | Versión exacta visible | 7.1 | — | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | Ninguna decisión específica de esta matriz; ver dependencias. |
| 7.5 | Recuperación | Recuperar versiones y archivos | Función de recuperación | Recuperación con hash verificado | 7.4, T-09 | Exportación sin probar | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | T-09; DA-02 N-18 (pendiente de diseño). |
| 7.6 | Pruebas | Pruebas de la fase | Informe | Suite ejecutada | 7.1–7.5 | Mocks | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | DA-02: validación técnica de las notificaciones de Fase 7. |

#### Fase 8 — Performance Intelligence

| ID | Nombre | Objetivo | Entregables | Criterios de aceptación | Dependencias | Riesgos | Estado | Limitaciones conocidas | Decisiones que deben estar resueltas antes |
|---|---|---|---|---|---|---|---|---|---|
| 8.1 | Registro de métricas | performance_metrics | Captura | Valores NULL permitidos | 1.8 | Datos incompletos | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | Ninguna decisión específica de esta matriz; ver dependencias. |
| 8.2 | Importación de datos | Importar métricas | Importador | Validación de datos | 8.1 | Formatos | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | DA-02 N-19 (pendiente de diseño). |
| 8.3 | Indicadores | Indicadores derivados | Cálculos | Fórmulas verificadas | 8.1 | Interpretación | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | DA-02 N-20 (alertas de rendimiento sin subfase; D-04). |
| 8.4 | Comparación de variantes | A/B | ab_tests | Causalidad solo si fue aleatorizado | 8.3 | Conclusiones falsas | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | Ninguna decisión específica de esta matriz; ver dependencias. |
| 8.5 | Análisis de resultados | Lectura de resultados | Análisis | Sin afirmar causalidad no probada | 8.3 | — | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | Ninguna decisión específica de esta matriz; ver dependencias. |
| 8.6 | Aprendizajes | Registrar aprendizajes | Registro | Trazables a datos | 8.5 | — | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | Ninguna decisión específica de esta matriz; ver dependencias. |
| 8.7 | Pruebas | Pruebas de la fase | Informe | Suite ejecutada | 8.1–8.6 | Faltan datos reales | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | DA-02: validación técnica de las notificaciones de Fase 8. |

#### Fase 9 — Hardening & Release

| ID | Nombre | Objetivo | Entregables | Criterios de aceptación | Dependencias | Riesgos | Estado | Limitaciones conocidas | Decisiones que deben estar resueltas antes |
|---|---|---|---|---|---|---|---|---|---|
| 9.1 | Seguridad | Revisión de seguridad y RLS | Informe | Matriz de aislamiento completa | 1–8 | Hallazgos tardíos | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | Ninguna decisión específica de esta matriz; ver dependencias. |
| 9.2 | Accesibilidad | Revisión de accesibilidad | Informe | Criterios definidos y cumplidos | 1–8 | — | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | Ninguna decisión específica de esta matriz; ver dependencias. |
| 9.3 | Rendimiento | Tiempos y carga | Informe | Metas definidas | 1–8 | Hosting | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | Ninguna decisión específica de esta matriz; ver dependencias. |
| 9.4 | Responsive | Pantallas pequeñas | Informe | Uso en móvil | 1–8 | — | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | Ninguna decisión específica de esta matriz; ver dependencias. |
| 9.5 | Pruebas integrales | Flujo completo y recuperación | Informe | Flujos completos pasan | 1–8 | Mocks | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | DA-02: validación integral de las notificaciones; D-05 sin subfase. |
| 9.6 | Pruebas de concurrencia | Aprobaciones y cuotas simultáneas | Informe | Sin condiciones de carrera | 6.5 | Difícil de reproducir | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | Ninguna decisión específica de esta matriz; ver dependencias. |
| 9.7 | Documentación | Documentación final | Documentos | Actualizada | 9.1–9.6 | — | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | Ninguna decisión específica de esta matriz; ver dependencias. |
| 9.8 | Preparación de despliegue | Hosting, dominio, respaldos, exportación | Plan | Plan aceptado | P-09, P-10 | Plan gratuito sin respaldos | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | P-09 política definitiva; P-10 hosting definitivo con cabeceras de seguridad; T-09 exportación. |
| 9.9 | Auditoría de aceptación | Revisión final | Informe | Criterios de la fase | 9.1–9.8 | — | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | Ninguna decisión específica de esta matriz; ver dependencias. |



## Nota de estado V21 (2026-11-20) — bloque uniforme en los cinco documentos activos

Esta nota no modifica ni reemplaza lo anterior; distingue seis estados que no deben confundirse.

| Estado | Situación |
|---|---|
| Histórico | Fase 0 v3.3 conservada como línea base documental (SHA-256 b5dccdc7…c1da, sin cambio); el diseño complementario vigente es la revisión v15; las notas V16 a V21 son trabajo de auditoría documental. |
| Publicación | Última publicación verificada: rama `audit/fase0-v19-review`, commit V20 `ac84133b776cc73c0cb3416e51e2767039bb5132` (padre `c6ef74be4db185ac3e4fd36810f24619e6f51fcf`, V16–V19). `main` permanece en V16 (`6a1af2424ef39e0960b8f7e09d4e19ec52e6f046`). El trabajo V21 (`expediente_final_v21/`) es posterior a ese commit; su publicación requiere autorización expresa del propietario y el estado vigente de publicación se consulta en el historial de la rama (este documento no puede contener el SHA de su propio commit). Sin pull request ni merge. |
| Auditoría | Cierre integral V16–V21 documentado en `expediente_final_v16_v19/` (evidencia V16–V20) y `expediente_final_v21/` (conciliación y validación V21; índice de vigencia en `INDICE_VIGENCIA_DOCUMENTAL_V21.md`): 231 reglas, 780 escenarios, 22 funciones / 366 casos, criterios C01–C32. Solo documental, en modelo en memoria y en un fixture PostgreSQL temporal. |
| Aceptación del propietario | Ni V15–V21, ni la Adenda v9 (PO-05), ni G-1, G-5 y G-10 están aceptados; todo sigue pendiente del propietario. |
| Integración | No integrado con la vista previa privada. |
| Producción | Sin despliegue, sin Supabase, sin migraciones ni esquema físico; solo un fixture SQL de prueba ejecutado en un PostgreSQL temporal aislado (`expediente_final_v16_v19/PE_POSTGRESQL_V20/`); Fase 1 NO INICIADA / NO AUTORIZADA. |

Limitaciones vigentes: 153 reglas condicionadas por diseño no aceptado (G-1, G-5, G-10); las 5 reglas antes con evidencia insuficiente (IG1-05, IG1-06, IG1-10, IG1-21, IG5-36) pasaron a B: PE-01 a PE-05 se ejecutaron en un PostgreSQL 16 temporal con un fixture derivado del diseño (63/63 PASS), sin esquema físico aprobado ni Supabase; 12 escenarios parciales; sin validación contra un esquema físico real, RLS, concurrencia ni Supabase; HV-02 (PO-05 «v3» frente a Adenda v9) no verificable sin confirmación del propietario; decisiones reservadas abiertas (RP-01, G-9, P-01 a P-05, P-10, OD-13, DEP-RET-01, DG-09, DG-12, DG-16, DG-18, DG-19, DG-20).
