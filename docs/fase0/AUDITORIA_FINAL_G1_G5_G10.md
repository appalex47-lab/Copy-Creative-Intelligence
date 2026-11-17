---
name: auditoria_final_g1_g5_g10
description: Auditoría final de la revisión v5 de G-1, G-5 y G-10 (28 controles con evidencia, verificador y resultados, riesgos residuales)
---

# AUDITORÍA FINAL — G-1, G-5 Y G-10 (revisión v5)

Documental. Las pruebas son diseños, no ejecuciones; el diseño no está validado técnicamente.

## 0. Estado por nivel

| Nivel | Estado | Alcance |
|---|---|---|
| 1. Fase 0 v3.3 | COMPLETADA Y ACEPTADA COMO LÍNEA BASE DOCUMENTAL, CON LIMITACIONES DOCUMENTADAS | No se reabre ni se modifica; SHA-256 `b5dccdc73a8103966ab1e1b1e84b2e7ead68cd736fba666ec71d0e790d51c1da` sin cambio |
| 2. Diseño técnico complementario (G-1, G-5, G-10, v5) | DISEÑO TÉCNICO DOCUMENTAL CORREGIDO Y PREPARADO PARA ACEPTACIÓN FORMAL, CON LIMITACIONES DOCUMENTADAS | Pendiente de aceptación formal del propietario; no validado técnicamente; DT-01, PC-02 y DT-02 resueltas en el diseño, sin aceptación; G-5 no se declara cerrada |
| 3. Fase 1 | NO INICIADA / NO AUTORIZADA | Requiere autorización expresa; el diseño complementario no la concede |


## 1. Hallazgos, causa raíz y corrección

| Hallazgo | Problema | Causa raíz | Corrección (resumen) | Referencia | Reglas | Pruebas |
|---|---|---|---|---|---|---|
| DT-01 Definición operativa de contribuyente | La definición de contribuyente mezclaba autoría, contribución material, intervención administrativa y herencia, y dejaba el umbral de aportación sustantiva abierto. | T-04 sin aprobar y sin definición operativa | Definición única A–F: autoría de copy, edición material con normalización exclusiva (NFKC, saltos de línea, espacios), brief con once campos materiales, datos promocional… | Spec 4.4.3 | IG5-42, IG5-43, IG5-46, IG5-49, IG5-50, IG5-51, IG5-52, IG5-53, IG5-54, IG5-55, IG5-56, IG5-61, IG5-63, IG5-64, IS-13 | T-202 a T-226 |
| PC-02 Representación física de las contribuciones | version_contributors no tenía fuentes físicas para brief, datos promocionales ni procedencia heredada. | Faltaban fuentes físicas versionadas | Cuatro entidades propias: brief_versions (2.1), contribution_events (2.1, con orígenes tipados y FK compuestas), copy_version_provenance (2.3) y promotion_snapshots (4.x)… | Spec 4.4.4, 4.4.5, 14.1 | IG5-42, IG5-45, IG5-52, IG5-53, IG5-54, IG5-56, IG5-57, IG5-58, IG5-59, IG5-60, IG5-61, IG5-62, IG5-63, IG5-64, IG5-65, IG5-67, IG5-68, IS-12, IS-13, IS-14 | T-227 a T-268 |
| DT-02 Elegibilidad del proponente de la clasificación | No estaba decidido si el proponente de la clasificación vigente puede evaluar el impacto. | Decisión del proponente sin resolver | No puede, por adaptación y mientras su clasificación esté vigente; quien confirma o revierte no queda excluido por ello; el proponente no confirma su propia propuesta; se… | Spec 4.4.6 | IG5-45, IG5-56, IG5-57, IG5-64, IG5-67, IG5-68, IS-14 | T-251 a T-262 |
| Integración Flujo único DT-01, PC-02 y DT-02 | Las tres decisiones debían formar un flujo único. | Tres decisiones tratadas por separado | Flujo de 13 pasos y condiciones de registro de la evaluación; un cambio de versión obliga a recalcular E y una evaluación anterior no se reutiliza.… | Spec 4.4.7 | IG5-40, IG5-42, IG5-45, IG5-47, IG5-48, IG5-52, IG5-53, IG5-54, IG5-56, IG5-57, IG5-59, IG5-63, IG5-64, IG5-66, IG5-68, IS-14 | T-263 a T-274 |

## 2. Orden único de creación

Secuencia: **1.8 → 2.x → 2.1 → 2.3 → 2.5 → 2.7 → 3.x → 4.x → 5.1 → 5.3 → 6.x → 6.1 → 6.5 → 6.6 → 8.x**

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
| 25 | 2.1 | función | record_contribution_event (interna; solo invocable por las funciones del propietario cci_records_owner; sin EXECUTE para roles de aplicación) | contribution_events |
| 26 | 2.1 | trigger | BEFORE INSERT sobre brief_versions: created_by = auth.uid(), version_number, snapshot_hash; BEFORE UPDATE, DELETE y TRUNCATE: rechazo (inmutable) | brief_versions |
| 27 | 2.1 | trigger | BEFORE UPDATE, DELETE y TRUNCATE sobre contribution_events: rechazo; la corrección es un evento nuevo | contribution_events |
| 28 | 2.1 | función | create_brief_version (única ruta de escritura de brief_versions; registra brief_editor cuando cambia un campo material) | brief_versions, briefs, contribution_events |
| 29 | 2.1 | habilitación | Políticas RLS y privilegios de brief_versions y contribution_events | tablas y funciones anteriores |
| 30 | 2.3 | tabla (estructura) | copy_versions | brief_versions, briefs, creative_pieces |
| 31 | 2.3 | tabla (estructura) | copy_version_provenance | contribution_events, copy_versions, memberships |
| 32 | 2.3 | columna agregada | contribution_events.copy_version_id | contribution_events |
| 33 | 2.3 | columna agregada | contribution_events.copy_version_piece_id | contribution_events |
| 34 | 2.3 | FK agregada | contribution_events → copy_versions | contribution_events, copy_versions |
| 35 | 2.3 | FK diferida | creative_pieces → copy_versions | creative_pieces, copy_versions |
| 36 | 2.3 | función | create_copy_version (versión inmutable de copy; fija brief_version_id; registra copy_author y la procedencia directa) | copy_versions, brief_versions, contribution_events, copy_version_provenance |
| 37 | 2.3 | trigger | BEFORE UPDATE, DELETE y TRUNCATE sobre copy_version_provenance: rechazo; coherencia de la procedencia | copy_version_provenance |
| 38 | 2.3 | habilitación | Políticas RLS y privilegios de copy_version_provenance | tablas y funciones anteriores |
| 39 | 2.5 | función | detect_material_change (interna): normalización NFKC, saltos de línea, espacios repetidos y extremos; decide copy_editor y la herencia; en duda conserva la atribución anterior | copy_versions, contribution_events, copy_version_provenance |
| 40 | 2.7 | función | verify_version_chain (interna): cadena exacta de versiones y orden de versión de la maestra; VERSION_CHAIN_INCONSISTENTE | copy_versions |
| 41 | 3.x | tabla (estructura) | creative_assets | copy_versions, creative_pieces |
| 42 | 3.x | tabla (estructura) | audit_rubric_versions | — |
| 43 | 3.x | tabla (estructura) | audits | ai_runs, audit_rubric_versions, copy_versions, creative_assets |
| 44 | 3.x | tabla (estructura) | audit_findings | audits |
| 45 | 3.x | columna agregada | contribution_events.asset_copy_version_id | contribution_events |
| 46 | 3.x | columna agregada | contribution_events.asset_piece_id | contribution_events |
| 47 | 3.x | columna agregada | contribution_events.creative_asset_id | contribution_events |
| 48 | 3.x | FK diferida | copy_versions → creative_assets | copy_versions, creative_assets |
| 49 | 3.x | FK agregada | contribution_events → creative_assets | contribution_events, creative_assets |
| 50 | 3.x | FK diferida | creative_pieces → creative_assets | creative_pieces, creative_assets |
| 51 | 3.x | función | register_asset_contribution: asset_uploader al cargar o reemplazar arte (identidad del servidor) | creative_assets, contribution_events |
| 52 | 4.x | tabla (estructura) | promotion_rules | campaigns |
| 53 | 4.x | tabla (estructura) | promotion_snapshots | memberships, promotion_rules |
| 54 | 4.x | tabla (estructura) | validation_settings_versions | — |
| 55 | 4.x | columna agregada | contribution_events.promotion_snapshot_id | contribution_events |
| 56 | 4.x | columna agregada | copy_versions.promotion_snapshot_id | copy_versions |
| 57 | 4.x | FK agregada | copy_versions → promotion_snapshots | copy_versions, promotion_snapshots |
| 58 | 4.x | FK agregada | contribution_events → promotion_snapshots | contribution_events, promotion_snapshots |
| 59 | 4.x | FK diferida | audits → validation_settings_versions | audits, validation_settings_versions |
| 60 | 4.x | función | create_promotion_snapshot (única ruta de escritura de promotion_snapshots; registra promotion_editor cuando cambia un campo material) | promotion_snapshots, promotion_rules, contribution_events |
| 61 | 4.x | trigger | BEFORE INSERT sobre promotion_snapshots: created_by = auth.uid(), snapshot_hash; BEFORE UPDATE, DELETE y TRUNCATE: rechazo (inmutable) | promotion_snapshots |
| 62 | 4.x | habilitación | Políticas RLS y privilegios de promotion_snapshots | tablas y funciones anteriores |
| 63 | 5.1 | columnas | Columnas anulables de reglas (extensión, tono, estructura, CTA) agregadas a channel_rules | channel_rules |
| 64 | 5.3 | tabla (estructura) | piece_classification_events | creative_pieces, memberships |
| 65 | 5.3 | tabla (estructura) | piece_reviewer_assignments | creative_pieces, memberships |
| 66 | 5.3 | función | create_adaptation | creative_pieces, copy_versions, channel_formats |
| 67 | 5.3 | función | version_contributors (interna, STABLE): conjunto de contribuyentes, evidencias, completitud y error; lee solo fuentes físicas versionadas | copy_versions, brief_versions, promotion_snapshots, creative_assets, contribution_events, copy_version_provenance |
| 68 | 5.3 | función | exclude_inherited_attribution: resolución documentada de una persona independiente que excluye una atribución heredada (fila nueva de procedencia; nunca retroactiva) | copy_version_provenance, contribution_events, memberships |
| 69 | 5.3 | función | eligible_evaluators | piece_reviewer_assignments, memberships, copy_versions, creative_assets, piece_classification_events, contribution_events, copy_version_provenance |
| 70 | 5.3 | función | propose_independence | piece_classification_events, creative_pieces |
| 71 | 5.3 | función | resolve_independence | piece_classification_events, piece_reviewer_assignments |
| 72 | 5.3 | función | assign_reviewer | piece_reviewer_assignments, memberships |
| 73 | 5.3 | habilitación | Políticas RLS y privilegios de piece_classification_events y piece_reviewer_assignments | tablas y funciones anteriores |
| 74 | 6.x | tabla (estructura) | comments | audit_findings, creative_pieces |
| 75 | 6.x | tabla (estructura) | commercial_block_exceptions | audit_findings, memberships |
| 76 | 6.1 | función | transition_piece_status (T-02 sin la transición a Publicado habilitada) | creative_pieces, comments, memberships |
| 77 | 6.5 | tabla (estructura) | approvals | audits, copy_versions, creative_assets, memberships |
| 78 | 6.5 | tabla (estructura) | impact_evaluations | approvals, copy_versions, creative_assets, creative_pieces, memberships, piece_reviewer_assignments |
| 79 | 6.5 | trigger | BEFORE INSERT sobre approvals: coherencia del arte (4.13) | approvals, creative_assets |
| 80 | 6.5 | función | record_approval (ampliada) | approvals, copy_versions, creative_assets, audits, memberships |
| 81 | 6.5 | función | record_impact_evaluation | impact_evaluations, approvals, piece_reviewer_assignments, memberships |
| 82 | 6.5 | habilitación | Políticas RLS y privilegios de approvals e impact_evaluations | tablas y funciones anteriores |
| 83 | 6.6 | tabla (estructura) | publication_attempts | approvals, copy_versions, creative_pieces, impact_evaluations, memberships |
| 84 | 6.6 | trigger | BEFORE INSERT sobre publication_attempts: db_txid, attempted_at, attempt_nonce, actor (5.11) | publication_attempts |
| 85 | 6.6 | trigger | Sustituye el cuerpo de piece_status_guard por la guarda de ocho condiciones (5.11) | publication_attempts, approvals, impact_evaluations, memberships, creative_pieces |
| 86 | 6.6 | función | transition_piece_status ampliada: habilita la transición a Publicado (#10) | publication_attempts, approvals, impact_evaluations, creative_pieces |
| 87 | 6.6 | habilitación | Políticas RLS y privilegios de publication_attempts y la transición a Publicado | tablas y funciones anteriores |
| 88 | 8.x | tabla (estructura) | performance_metrics | creative_pieces |
| 89 | 8.x | tabla (estructura) | ab_tests | creative_pieces, performance_metrics |

## 3. Controles de auditoría integral (28) y verificador documental

Cada control apunta a la verificación del script que lo comprueba; un control no se da por cumplido por haberse mencionado en un documento.

| # | Control | Resultado | Evidencia (verificación) |
|---|---|---|---|
| 1 | No existen dos definiciones distintas de contribuyente | OK | V37 |
| 2 | La fórmula E es idéntica en todos los documentos | OK | V37 |
| 3 | version_contributors tiene fuentes físicas definidas | OK | V38 |
| 4 | Todas las referencias de versión son exactas | OK | V39 |
| 5 | No existen referencias polimórficas sin integridad | OK | V40 |
| 6 | No hay posibilidad de modificar o borrar evidencia histórica | OK | V41 |
| 7 | La herencia no depende de IA ni de similitud semántica | OK | V42 |
| 8 | La exclusión de DT-02 se limita al proponente de la clasificación vigente | OK | V43 |
| 9 | No se excluye automáticamente a quien confirma o revierte una clasificación | OK | V43 |
| 10 | No existe autovalidación | OK | V44 |
| 11 | No existe autoevaluación | OK | V44 |
| 12 | No hay asignación automática a Admin | OK | V44 |
| 13 | No se permite evaluación con procedencia incompleta | OK | V45, V38 |
| 14 | No se permite publicación con evaluación obsoleta | OK | V45 |
| 15 | No se crearon permisos nuevos | OK | V46 |
| 16 | No se crearon estados nuevos | OK | V46 |
| 17 | No se crearon transiciones nuevas | OK | V46, V30 |
| 18 | No se modificaron las 13 transiciones T-02 | OK | V30, V46 |
| 19 | No se modificaron las 17 claves físicas | OK | V30, V46 |
| 20 | El roadmap respeta las dependencias | OK | V25, V53 |
| 21 | Las FK respetan el orden de creación | OK | V23, V24, V52 |
| 22 | Cada regla tiene al menos una prueba | OK | V06 |
| 23 | Cada prueba referencia reglas existentes | OK | V04, V05, V34 |
| 24 | Los IDs son únicos | OK | V01, V35 |
| 25 | Las cifras de reglas y pruebas se recalculan, no se copian de la v4 | OK | V47, V16 |
| 26 | Los diagramas Mermaid representan el modelo actualizado | OK | V48, V17, V26 |
| 27 | No hay contradicciones entre especificación, informe, auditoría y roadmap | OK | V18, V49, V29 |
| 28 | No se declara validación técnica inexistente | OK | V33, V36, V50 |

| Concepto | Detalle |
|---|---|
| Nombre | g_verify.py con g_verify_v4.py y g_verify_v5.py, v4_plan.py y v4_check.py (herramienta de verificación; no es código de aplicación y no se publica en el repositorio, que solo admite .md) |
| Comando | python3 g_verify.py (desde el directorio de trabajo; mermaid 10 y jsdom para el parseo de diagramas) |
| Número de comprobaciones | 0 |
| Errores finales | 0 |
| Errores hallados y corregidos | Ver la lista de la sección 4 |
| Limitaciones | Heurísticas sobre texto; no ejecuta SQL ni valida PostgreSQL; el renderizado visual de Mermaid no se verificó; los controles negativos cubren defectos de H-01 y no todos los posibles |

### Resultados de las verificaciones

| Verificación | Resultado | Descripción |
|---|---|---|
| — | — | ejecutar g_verify.py |

## 4. Errores hallados y corregidos durante la v5

| Error | Corrección |
|---|---|
| Variable global D sobrescrita por un identificador de las pruebas nuevas (rompía el recuento por nivel) | Se renombró |
| Hash del registro de la Adenda v9 en la tabla de línea base | Se fija con el hash original al iniciar (corregido en la v4) |

## 5. Riesgos residuales

| ID | Riesgo |
|---|---|
| RR-01 | La FK declarativa de un solo nivel con columnas generadas no está verificada |
| RR-02 | Todo es diseño: ninguna restricción, trigger ni función se ejecutó |
| RR-03 | Si falla la inserción del registro, no hay fila confirmada del intento; la evidencia de plataforma, si existe, no es un registro confirmado y su conservación no está verificada |
| RR-04 | Un superusuario o propietario de la base puede alterar cualquier tabla |
| RR-05 | Los bytes de un arte no son transaccionales con la base (C8) |
| RR-06 | No hay análisis semántico: el juicio de impacto es humano |
| RR-07 | Equipos pequeños pueden no tener un revisor elegible |
| RR-08 | El costo de verificar C1 a C9 en cada publicación no está medido |
| RR-09 | La suficiencia de activity_logs sigue sin demostrarse (DA-01) |
| RR-10 | Retiro de contenido externo sin procedimiento (DEP-RET-01) |
| RR-11 | Los privilegios por defecto de Supabase pueden conceder escritura amplia |
| RR-12 | Una pieza escrita por IA cuenta como autoría de quien la pidió (T-04) |
| RR-13 | Los dos propietarios de funciones y la revocación de EXECUTE no se han comprobado en Supabase |
| RR-14 | auth.uid() depende de la sesión de la solicitud: quien tenga credenciales de administración de la base puede fijar otra identidad |
| RR-15 | Los tiempos de espera, cancelaciones y pérdidas de conexión abortan toda la transacción y no dejan fila |
| RR-16 | La conservación y el contenido de los registros de la plataforma no están verificados |
| RR-17 | approvals.decision es una ampliación propuesta (DG-20): v3.3 no distingue aprobación de rechazo en la fila |
| RR-18 | Los umbrales de 30 y 10 caracteres son propuestas pendientes de T-03 |
| RR-19 | La versión de PostgreSQL del proyecto de Supabase no está verificada; pg_current_xact_id requiere la 13 o posterior |
| RR-20 | El comportamiento real de los bloqueos y del orden de bloqueo no se probó |
| RR-21 | T-04 de v3.3 no fue aprobada; la definición operativa de contribuyente de esta revisión (4.4.3) es diseño complementario y no una aprobación retroactiva |
| RR-22 | Los valores reales de canales y formatos no existen: sin catálogo cargado no se crean piezas |
| RR-23 | Tras una restauración, un clon o una recuperación a un punto anterior, un db_txid guardado podría repetirse; attempted_at no es un identificador |
| RR-24 | El orden de versión de la maestra (columna de copy_versions) no está fijado en v3.3 |
| RR-25 | El valor de pg_current_xact_id dentro de un savepoint o bloque EXCEPTION no está verificado |
| RR-26 | La FK no distingue «sin arte» de «otro arte» con columnas anulables |
| RR-27 | DT-01, PC-02 y DT-02 se resuelven en el diseño complementario v5 (definición operativa, representación física y elegibilidad del proponente), pero no están aceptadas por el propietario ni validadas técnicamente |
| RR-28 | El superusuario, el propietario de las tablas, la desactivación de triggers y la edición manual de datos no los impide este diseño |
| RR-29 | La disponibilidad y la fuente aleatoria de gen_random_uuid() en la versión de PostgreSQL de Supabase no están verificadas (en PostgreSQL 13 o posterior es una función del núcleo) |
| RR-30 | La variable local de la transacción que lleva el nonce a la guarda puede ser escrita por quien tenga acceso SQL |
| RR-31 | Los privilegios por columna (sin SELECT sobre attempt_nonce) y los roles propietarios no están verificados en Supabase |
| RR-32 | version_contributors depende de brief_versions, promotion_snapshots, contribution_events y copy_version_provenance, que se crean en 2.1, 2.3 y 4.x; una versión creada antes de que existan sus fuentes no tiene procedencia |
| RR-33 | El orden de creación se verificó contra el modelo de esta revisión y a nivel de tabla contra las 27 tablas de v3.3, cuyas columnas exactas v3.3 no define |
| RR-34 | La normalización Unicode NFKC en la base de datos y la del servidor de aplicación podrían diferir, y la disponibilidad de normalize(text, NFKC) en la versión de PostgreSQL de Supabase no está verificada |
| RR-35 | v3.3 no enumera las columnas de contenido evaluable de copy_versions ni de los campos de brief y de datos promocionales físicamente |
| RR-36 | El costo del recorrido de la cadena de versiones y de la procedencia en version_contributors no está medido |
| RR-37 | La resolución independiente de una exclusión de atribución reutiliza piece.review (clave existente) porque el encargo no define otra facultad |
| RR-38 | creative_assets.reused_from_asset_id es una columna propuesta que v3.3 no define; sin ella no se puede determinar la herencia del arte reutilizado |
| RR-39 | Saber si una versión de copy usa datos promocionales (y por tanto exige promotion_snapshot_id) depende de la Fase 4, no definida en v3.3 |

## 6. Estado por brecha

| Brecha | Estado |
|---|---|
| G-1 | Diseño documental completo; preparado para aceptación formal |
| G-5 | Diseño documental completo; no declarada plenamente cerrada: sin aceptación ni validación técnica; fail-closed si falta una fuente |
| G-10 | Diseño documental completo con límites declarados; preparado para aceptación formal |

Ninguna está aceptada ni validada técnicamente.
