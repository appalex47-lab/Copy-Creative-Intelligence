---
name: auditoria_final_g1_g5_g10
description: Auditoría final de la revisión v7 de G-1, G-5 y G-10 (matriz de 28 controles, verificador publicado con resultado real, auditoría integral de 28 puntos, riesgos residuales)
---

# AUDITORÍA FINAL — G-1, G-5 Y G-10 (revisión v7)

Documental. Las pruebas son diseños, no ejecuciones; el diseño no está validado técnicamente.

## 0. Estado y niveles de evidencia

| Nivel | Estado | Alcance |
|---|---|---|
| 1. Fase 0 v3.3 | COMPLETADA Y ACEPTADA COMO LÍNEA BASE DOCUMENTAL, CON LIMITACIONES DOCUMENTADAS | No se reabre ni se modifica; SHA-256 `b5dccdc73a8103966ab1e1b1e84b2e7ead68cd736fba666ec71d0e790d51c1da` sin cambio |
| 2. Diseño complementario v7 (G-1, G-5, G-10) | PREPARADA PARA ACEPTACIÓN FORMAL DEL PROPIETARIO, CON LIMITACIONES DOCUMENTADAS | Pendiente de aceptación formal del propietario; no validado técnicamente; la Adenda v9 sigue sin aceptar (PO-05) |
| 3. Fase 1 | NO INICIADA / NO AUTORIZADA | Requiere autorización expresa; este diseño no la concede |


| Nivel de evidencia | Significado | Alcance |
|---|---|---|
| Diseñado | La regla o el escenario está escrito en la especificación | Nada ejecutado |
| Verificado documentalmente | El verificador publicado comprobó coherencia entre los documentos: IDs, referencias, cifras, contratos, orden, estados | Resultado reproducible; no prueba que el diseño funcione en PostgreSQL |
| Validado técnicamente | Ejecución real contra PostgreSQL, RLS y Supabase con las pruebas de la matriz | **Pendiente**: ningún control ni escenario alcanza este nivel |


## 1. Hallazgos de la v6 y su corrección

| Hallazgo | Defecto | Corrección (resumen) | Referencia | Reglas | Escenarios |
|---|---|---|---|---|---|
| H-01 Hash de v3.3 registrado pero no calculado | El control K25 comparaba el hash escrito en los documentos con otro texto; un hash registrado se presentaba como comprobado sin calcular el SHA-256 del archivo original. | K48 calcula el SHA-256 sobre los bytes del archivo original de v3.3 (`--v33 RUTA`) y lo compara con `b5dccdc73a8103966ab1e1b1e84b2e7ead68cd736fba666ec71d0e790d51c1da`; si no coincide, FALLA; si el arc… | AUDITORIA 3; REGISTRO | IE-10 | T-373 a T-375 |
| H-02 Un cambio textual podía retirar a un contribuyente anterior | Las reglas v6 marcaban como históricas las atribuciones heredadas cuando un campo era sustituido o eliminado, y la comparación de texto, el hash o retained_segments = 0 podían excluir a un contribuyente real (T-299). | Principio de conservación (IG5-90): una atribución activa se conserva aunque el campo se modifique, sustituya o elimine; la clasificación técnica (sin_cambio, introducido, modificado, sustituido, elim… | ESPECIFICACION 4.4.4 y 4.4.8 | IG5-72, IG5-90 a IG5-94 | T-336 a T-354 |
| H-03 Las relaciones parecían válidas con solo contener organization_id | El verificador v6 comprobaba que las FK incluyeran organization_id, no que sus columnas, orden, destino, tipos, versión, origen del evento y actor fueran correctos. | Verificación semántica por FK (IG5-80, IE-09): longitud y orden de columnas, PK o UNIQUE de destino idéntica, tipos, organization_id, versión, entidad, origen del evento, actor, asset ligado a la vers… | ESPECIFICACION 4.4.9; AUDITORIA 3 | IG5-80 a IG5-84, IE-09, IE-11 | T-355 a T-372 |

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
| 74 | 5.3 | tabla (estructura) | attribution_discard_resolutions | brief_field_attributions, copy_version_provenance, memberships, promotion_field_attributions |
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

## 3. Verificador documental y matriz de controles

Una sola herramienta publicada, `docs/fase0/herramientas/verificar_expediente.py`, produce cada resultado. Cada control cita las comprobaciones que lo sustentan: un control es OK solo si todas aprueban; si una falla es NO OK; si no existe la comprobación es PENDIENTE. El nivel máximo alcanzable es «Verificado documentalmente».

| Concepto | Detalle |
|---|---|
| Archivo | docs/fase0/herramientas/verificar_expediente.py |
| Comando | `python3 docs/fase0/herramientas/verificar_expediente.py --md` (también `--json`, `--dir RUTA`, `--sin-mutaciones` y `--v33 RUTA`) |
| Dependencias | Python 3.8 o superior; solo biblioteca estándar; no accede a red, base de datos ni servicios |
| Entrada | Los cinco documentos activos, los archivos de `historico/` (SHA-256 del manifiesto del registro) y, opcionalmente con `--v33 RUTA`, el archivo original de la línea base v3.3 |
| Salida | Un resultado por comprobación (APRUEBA, FALLA o PENDIENTE), la matriz de 28 controles con 10 campos y la auditoría integral de 28 puntos; código de salida 1 si algo falla |
| Número de comprobaciones | 48 |
| Reproducibilidad | La comprobación K41 ejecuta todo dos veces y compara; el bloque siguiente se genera con `--md` y se puede regenerar y comparar. El verificador ignora el bloque al analizar para no depender de su propio resultado |
| Controles negativos | K42 inyecta en copias en memoria 22 mutaciones (M-01 a M-14: relaciones, actor, asset, versión, antecesor, resoluciones y sustitución textual; M-15 a M-21: ID duplicado, regla sin escenario, referencia inexistente, cifra, fórmula, error ausente y dependencia posterior; M-22: un bit alterado en una copia temporal del original de v3.3) y exige que la comprobación correspondiente falle |
| Hash de v3.3 (K48) | El archivo original de v3.3 no está en el repositorio; el bloque siguiente se generó indicando su ruta con `--v33`, por lo que K48 calculó su SHA-256 y lo comparó con `b5dccdc73a8103966ab1e1b1e84b2e7ead68cd736fba666ec71d0e790d51c1da`. Una ejecución sin `--v33` deja K48 en PENDIENTE_ARCHIVO_ORIGINAL_NO_DISPONIBLE y no declara el hash como comprobado: el hash escrito en el registro es solo un registro histórico (K25) |
| Limitaciones | Análisis sintáctico de Markdown: no ejecuta SQL, no valida PostgreSQL ni RLS, no renderiza Mermaid (solo compara aristas y cuenta pasos) y no prueba la semántica de negocio; es verificación documental, no validación técnica |

### Resultado real del verificador

<!-- VERIFICADOR:INICIO -->
**Comprobaciones ejecutadas: 48. Aprobadas: 48. Fallidas: 0. Pendientes: 0.** Controles: 28; OK: 28; NO OK: 0; PENDIENTE: 0. Mutaciones negativas: 22; detectadas: 22; no detectadas: 0.

| Comprobación | Resultado | Descripción | Regla | Documento y sección |
|---|---|---|---|---|
| K01 | APRUEBA | Los cinco documentos activos existen y no están vacíos | IE-08 | todos |
| K02 | APRUEBA | IDs de reglas únicos (208 reglas) y con el mismo texto en la definición y en la cobertura | IE-08 | ESPECIFICACION 11 |
| K03 | APRUEBA | IDs de escenarios únicos y consecutivos (375 escenarios) | IE-08 | ESPECIFICACION 11 |
| K04 | APRUEBA | Todo escenario tiene ID, requisito, datos iniciales, acción, resultado esperado, resultado prohibido, criterio, nivel y reglas | IE-07 | ESPECIFICACION 11 |
| K05 | APRUEBA | Todo escenario referencia solo reglas existentes | IE-08 | ESPECIFICACION 11 |
| K06 | APRUEBA | Toda regla tiene al menos un escenario (cobertura 208 de 208) | IE-08 | ESPECIFICACION 11 |
| K07 | APRUEBA | Todo escenario está asociado a al menos una regla | IE-08 | ESPECIFICACION 11 |
| K08 | APRUEBA | La tabla de cobertura regla-escenario de la especificación coincide con las referencias de los escenarios | IE-08 | ESPECIFICACION 11 |
| K09 | APRUEBA | Cifras recalculadas desde los archivos (208 reglas, 375 escenarios, 41 tablas, 14 nuevas) y coincidentes en los cinco documentos | IE-06 | ESPECIFICACION 11.1; INFORME |
| K10 | APRUEBA | La fórmula del conjunto excluido E es idéntica en todos los documentos (10 apariciones) | IG5-56 | ESPECIFICACION 4.4.3 |
| K11 | APRUEBA | Existe una sola definición de contribuyente (figuras A a F en 4.4.3) y no se redefine en otros documentos | IG5-40 | ESPECIFICACION 4.4.3 |
| K12 | APRUEBA | Los diez errores de procedencia están en el contrato de version_contributors y cada uno aparece en al menos un escenario | IG5-78 | ESPECIFICACION 4.4.5 |
| K13 | APRUEBA | Los 26 escenarios mínimos de H-02 existen (26 escenarios H-02, con datos, versiones, actores, acción, esperado, prohibido, regla y nivel) | IG5-69 a IG5-79 | ESPECIFICACION 4.4.8 |
| K14 | APRUEBA | Contrato de integridad (53 relaciones): 10 campos completos por fila, toda FK de las nueve tablas de procedencia figura en él y toda FK incluye organization_id | IG5-80 | ESPECIFICACION 4.4.9 |
| K15 | APRUEBA | Las nueve tablas de procedencia tienen bloque de definición y fila en el orden de creación; sin tablas repetidas (41 tablas) | IG5-80 | ESPECIFICACION 4.4.4; 14.1 |
| K16 | APRUEBA | Orden de creación: ninguna tabla, función o trigger depende de un objeto posterior y ninguna FK apunta a una tabla creada después (100 pasos) | IE-08 (H-01 de la v4) | ESPECIFICACION 14.1 |
| K17 | APRUEBA | La secuencia de subfases de creación es idéntica en especificación, roadmap y auditoría | H-01 v4 | ROADMAP 3; AUDITORIA 2 |
| K18 | APRUEBA | El roadmap conserva las 76 subfases, sin duplicados ni subfase 77, y toda subfase del orden de creación existe en él | Roadmap v9 | ROADMAP |
| K19 | APRUEBA | Las 17 claves físicas permanecen: las claves citadas están entre las 17, las 17 figuran en la especificación y ninguna frase crea permisos ni roles | P8 | ESPECIFICACION 10.1 |
| K20 | APRUEBA | T-02 conserva 13 transiciones: sin transición #14 o posterior, sin estados ni transiciones nuevos | P8, IP-01 | ESPECIFICACION 1 y 2 |
| K21 | APRUEBA | Las decisiones y limitaciones pendientes del propietario se conservan visibles (14 elementos) en especificación, informe y registro | IG5-48 | ESPECIFICACION 12.3; INFORME |
| K22 | APRUEBA | Estados: v3.3 aceptada como línea base, v7 preparada para aceptación formal, Fase 1 no iniciada; ningún documento declara aceptación del propietario de la v7 | IE-04 | todos |
| K23 | APRUEBA | Ningún documento afirma validación técnica ni pruebas técnicas ejecutadas (toda mención está negada o pendiente) | IE-05 | todos |
| K24 | APRUEBA | La atribución no usa IA, similitud, embeddings ni inferencias probabilísticas como autoridad (toda mención está negada) y IG5-70 define la regla determinista | IG5-43, IG5-70 | ESPECIFICACION 4.4.8 |
| K25 | APRUEBA | Los archivos históricos conservan su SHA-256 registrado en el manifiesto (20 archivos) y el registro cita el hash aceptado de v3.3 con b5dccdc7 (registro histórico; la comprobación criptográfica del original es K48) | IE-04 | REGISTRO manifiesto |
| K26 | APRUEBA | El diagrama de relaciones (31 aristas) coincide con las relaciones del contrato de integridad | IG5-80 | ESPECIFICACION 4.4.4 |
| K27 | APRUEBA | Sin contradicciones con las versiones anteriores en los documentos activos (patrones de fuentes, errores y pendientes obsoletos) | IE-08 | todos |
| K28 | APRUEBA | Registro histórico: entradas ordenadas por revisión hasta la v7 con el commit previo 6ad464d… y manifiesto de históricos | IE-04 | REGISTRO |
| K29 | APRUEBA | La especificación documenta la herramienta publicada, su comando y sus límites | IE-08 | ESPECIFICACION 11.2; AUDITORIA 3 |
| K30 | APRUEBA | El flujo integrado de 4.4.7 tiene los 19 pasos en el orden obligatorio | IG5-88 | ESPECIFICACION 4.4.7 |
| K31 | APRUEBA | Los niveles de evidencia están definidos (Diseñado, Verificado documentalmente, Validado técnicamente) y IE-05 a IE-08 existen | IE-05 | AUDITORIA 1 |
| K32 | APRUEBA | Las ocho tablas de procedencia no tienen referencias polimórficas, cada columna *_id está cubierta por una FK compuesta (salvo las declaradas) y ninguna apunta al último o al actual | IG5-81, IG5-62 | ESPECIFICACION 4.4.4 |
| K33 | APRUEBA | Inmutabilidad: el contrato la define para las trece tablas, IS-13, IG5-85 e IG5-87 existen y 4 escenarios de H-03 intentan modificar, borrar o truncar | IS-13 | ESPECIFICACION 4.4.9 |
| K34 | APRUEBA | DT-02: IG5-45 limita la exclusión al proponente de la clasificación vigente, IG5-68 protege a quien confirma o revierte y 12 escenarios lo cubren | IG5-45, IG5-68 | ESPECIFICACION 4.4.6 |
| K35 | APRUEBA | Sin autovalidación, autoevaluación ni asignación automática a Admin: IG5-55, IG5-67, IG5-57 e IS-14 y 5 escenarios de Admin | IG5-55, IG5-57, IG5-67, IS-14 | ESPECIFICACION 4.4.3 |
| K36 | APRUEBA | Fail-closed: IG5-64 e IG5-78 bloquean evaluación, independencia y aprobación o publicación sin excepción de Admin; IG5-89 impide reutilizar evaluaciones; 7 escenarios de bloqueo | IG5-64, IG5-78, IG5-89 | ESPECIFICACION 4.4.5 |
| K37 | APRUEBA | Las reglas de contribución directa, herencia de copy y procedencia de copy y arte existen y tienen escenarios (10 reglas) | IG5-49 a IG5-54, IG5-83, IG5-84 | ESPECIFICACION 4.4.3 y 4.4.9 |
| K38 | APRUEBA | H-02: 12 campos de brief y 9 de promoción catalogados, regla de segmentos (IG5-70), cálculo de atribuciones (IG5-72), historial (IG5-73), dos algoritmos de 10 pasos y reglas IG5-69 a IG5-79 | IG5-69 a IG5-79 | ESPECIFICACION 4.4.8 |
| K39 | APRUEBA | Reglas de G-7 (C1 a C9) y de G-10 (37 reglas IG10) presentes con cobertura | IG10-* | ESPECIFICACION 5 y 6.2 |
| K44 | APRUEBA | Integridad estructural de 103 relaciones: longitud, orden exacto de columnas, organization_id, PK o UNIQUE de destino con las mismas columnas, tipos compatibles, contrato igual a los bloques, sin relaciones rotas ni circulares | IG5-80, IE-09 | ESPECIFICACION 4.4.4 y 4.4.9 |
| K45 | APRUEBA | Integridad semántica: versión, entidad y origen del evento, actor, asset ligado a la versión exacta de copy, cadena de la misma entidad y antecesor obligatorio | IG5-81 a IG5-84, IS-16, IE-09 | ESPECIFICACION 4.4.4 y 4.4.9 |
| K46 | APRUEBA | Resolución independiente de descarte: afectado y solicitante no resuelven, evidencia y motivo no vacíos, fuente única, autoridad de revisión, resolutor desde el backend y una sola resolución aceptada por atribución | IG5-92, IG5-93 | ESPECIFICACION 4.4.4 y 4.4.8 |
| K47 | APRUEBA | Ninguna regla, algoritmo ni escenario retira a un contribuyente por sustitución, eliminación, hash o retained_segments = 0 | IG5-72, IG5-90, IG5-91 | ESPECIFICACION 4.4.8 |
| K49 | APRUEBA | H-02 v7: reglas IG5-90 a IG5-94 con cobertura y los 16 escenarios obligatorios (19 escenarios de atribución v7) | IG5-90 a IG5-94 | ESPECIFICACION 4.4.8 |
| K48 | APRUEBA | Hash de la línea base v3.3 calculado sobre los bytes de «fase0_v3_3_integral.md»: b5dccdc73a8103966ab1e1b1e84b2e7ead68cd736fba666ec71d0e790d51c1da; esperado b5dccdc73a8103966ab1e1b1e84b2e7ead68cd736fba666ec71d0e790d51c1da; COINCIDE | IE-10 | REGISTRO; AUDITORIA 3 |
| K40 | APRUEBA | La matriz define 28 controles con ID estable único, regla, sección, evidencia, procedimiento, resultado, estado y nivel; ninguno es OK sin comprobaciones aprobadas | IE-06, IE-07 | AUDITORIA 3 |
| K41 | APRUEBA | Reproducibilidad: dos ejecuciones sobre los mismos archivos producen los mismos resultados individuales | IE-08 | AUDITORIA 3 |
| K42 | APRUEBA | Controles negativos: 22 mutaciones introducidas en copias en memoria, 22 detectadas, 0 no detectadas | IE-08, IE-11 | AUDITORIA 3 |

**Mutaciones negativas.** Cada una parte de un estado inicial válido, introduce la modificación en una copia en memoria, nombra el control que debe detectarla y espera rechazo.

| ID | Defecto | Estado inicial | Modificación introducida | Control | Esperado | Resultado real |
|---|---|---|---|---|---|---|
| M-01 | FK con organización incorrecta | válido (K44 APRUEBA) | En brief_versions → briefs, la primera columna local pasa de organization_id a created_by | K44 | rechazo | RECHAZADA por K44 |
| M-02 | FK con columnas destino en orden incorrecto | válido (K44 APRUEBA) | En brief_field_attributions → brief_field_changes se invierte el orden de las dos últimas columnas referenciadas | K44 | rechazo | RECHAZADA por K44 |
| M-03 | FK sin clave única de destino | válido (K44 APRUEBA) | Se elimina de contribution_events la clave única (organization_id, id, brief_version_id, contributor_id) | K44 | rechazo | RECHAZADA por K44 |
| M-04 | Evento de brief asociado a atribución promocional | válido (K45 APRUEBA) | La atribución de brief referencia la columna promotion_snapshot_id del evento | K45 | rechazo | RECHAZADA por K45 |
| M-05 | Actor de evento distinto del actor de atribución | válido (K45 APRUEBA) | La columna de actor de la atribución pasa de contributor_id a created_by | K45 | rechazo | RECHAZADA por K45 |
| M-06 | Asset no utilizado asociado a una versión | válido (K45 APRUEBA) | La FK de procedencia al arte pierde copy_version_id | K45 | rechazo | RECHAZADA por K45 |
| M-07 | Asset de otra organización | válido (K44 APRUEBA) | La FK de procedencia al arte pierde organization_id | K44 | rechazo | RECHAZADA por K44 |
| M-08 | Versión de brief de otro brief | válido (K45 APRUEBA) | La cadena de brief_versions pierde brief_id | K45 | rechazo | RECHAZADA por K45 |
| M-09 | Snapshot de otra promoción | válido (K45 APRUEBA) | La cadena de promotion_snapshots pierde promotion_line_id | K45 | rechazo | RECHAZADA por K45 |
| M-10 | Atribución heredada sin antecesor | válido (K45 APRUEBA) | Se elimina de brief_field_attributions la restricción que exige previous_attribution_id en las heredadas | K45 | rechazo | RECHAZADA por K45 |
| M-11 | Resolución de descarte realizada por el contribuyente afectado | válido (K46 APRUEBA) | Se elimina la restricción resolved_by <> affected_contributor_id | K46 | rechazo | RECHAZADA por K46 |
| M-12 | Resolución realizada por quien solicitó la exclusión | válido (K46 APRUEBA) | Se elimina la restricción resolved_by <> requested_by | K46 | rechazo | RECHAZADA por K46 |
| M-13 | Resolución sin evidencia | válido (K46 APRUEBA) | Se elimina la restricción de evidencia y motivo no vacíos | K46 | rechazo | RECHAZADA por K46 |
| M-14 | Sustitución textual que retira automáticamente al contribuyente anterior | válido (K47 APRUEBA) | En la tabla de cálculo de atribuciones la fila «sustituido» pasa las activas anteriores a históricas | K47 | rechazo | RECHAZADA por K47 |
| M-15 | ID de regla duplicado | válido (K02 APRUEBA) | Se repite la fila de IG5-69 | K02 | rechazo | RECHAZADA por K02 |
| M-16 | Regla sin escenario | válido (K06 APRUEBA) | Se retira IG5-83 de todos los escenarios | K06 | rechazo | RECHAZADA por K06 |
| M-17 | Referencia a una regla inexistente | válido (K05 APRUEBA) | T-01 referencia IG5-999 | K05 | rechazo | RECHAZADA por K05 |
| M-18 | Cifra incorrecta en el resumen | válido (K09 APRUEBA) | Pruebas totales pasa a 1 | K09 | rechazo | RECHAZADA por K09 |
| M-19 | Fórmula de E distinta | válido (K10 APRUEBA) | Se retira el término P de una aparición | K10 | rechazo | RECHAZADA por K10 |
| M-20 | Código de error de procedencia ausente | válido (K12 APRUEBA) | BRIEF_CHAIN_INCONSISTENTE desaparece del contrato | K12 | rechazo | RECHAZADA por K12 |
| M-21 | Dependencia posterior en el orden de creación | válido (K16 APRUEBA) | La subfase 2.1 depende de promotion_snapshots (4.x) | K16 | rechazo | RECHAZADA por K16 |
| M-22 | Archivo v3.3 con un byte alterado | válido (K48 APRUEBA) | Se invierte un bit en una copia temporal del original y se calcula su SHA-256 | K48 | rechazo | RECHAZADA por K48 |

**Matriz de los 28 controles.**

| ID | Control | Regla exacta | Documento y sección | Evidencia concreta | Procedimiento | Resultado real | Estado | Nivel de evidencia | Observación |
|---|---|---|---|---|---|---|---|---|---|
| C-01 | No existen dos definiciones distintas de contribuyente | IG5-40: una sola definición A a F | ESPECIFICACION 4.4.3 | IG5-40; T-165 a T-178 (v4) y escenarios DT-01 | Contar las figuras de 4.4.3 y buscar tablas de definición en los otros cuatro documentos | K11 pasa | OK | Verificado documentalmente | Verificación documental; no es validación técnica |
| C-02 | La fórmula E es idéntica en todos los documentos | IG5-56 | ESPECIFICACION 4.4.3 y 4.4.6 | IG5-05, IG5-56 | Extraer cada aparición de la fórmula y compararla con la forma canónica | K10 pasa | OK | Verificado documentalmente | Verificación documental; no es validación técnica |
| C-03 | version_contributors tiene fuentes físicas definidas | IG5-42, IG5-65 | ESPECIFICACION 4.4.5 | Fila «Fuentes físicas» del contrato; bloques de las ocho tablas en 4.4.4 | Comprobar que cada fuente tiene bloque de definición y fila en el orden de creación anterior a 5.3 | K15 pasa; K16 pasa; K12 pasa | OK | Verificado documentalmente | Verificación documental; no es validación técnica |
| C-04 | Todas las referencias de versión son exactas | IG5-62, IG5-79, IG5-85 | ESPECIFICACION 4.4.4 y 4.4.9 | Contrato de integridad: filas de copy_versions y de provenance | Verificar que toda FK incluye organization_id y que ninguna columna apunta al último o al actual | K14 pasa; K32 pasa | OK | Verificado documentalmente | Verificación documental; no es validación técnica |
| C-05 | No existen referencias polimórficas sin integridad | IG5-81 | ESPECIFICACION 4.4.4 y 4.4.9 | CHECK de exactamente un origen; FK tipadas | Comprobar que cada columna *_id de las ocho tablas está cubierta por una FK y que no hay columnas de tipo-referencia genéricas | K32 pasa | OK | Verificado documentalmente | Verificación documental; no es validación técnica |
| C-06 | No hay posibilidad de modificar o borrar evidencia histórica | IS-13, IG5-87 | ESPECIFICACION 4.4.9 | Fila «Inmutabilidad de los registros»; escenarios H-03 | Comprobar la fila del contrato, las reglas y los escenarios de UPDATE, DELETE y TRUNCATE | K33 pasa | OK | Verificado documentalmente | Verificación documental; no es validación técnica |
| C-07 | La herencia no depende de IA ni de similitud semántica | IG5-43, IG5-70 | ESPECIFICACION 4.4.3 y 4.4.8 | IG5-70 («sin IA, embeddings, similitud») | Buscar menciones de similitud o embeddings no negadas | K24 pasa | OK | Verificado documentalmente | Verificación documental; no es validación técnica |
| C-08 | La exclusión de DT-02 se limita al proponente de la clasificación vigente | IG5-45 | ESPECIFICACION 4.4.6 | IG5-45; escenarios de DT-02 | Comprobar la regla y los escenarios del proponente | K34 pasa | OK | Verificado documentalmente | Verificación documental; no es validación técnica |
| C-09 | No se excluye automáticamente a quien confirma o revierte una clasificación | IG5-68 | ESPECIFICACION 4.4.6 | IG5-68; escenarios T-174 y de DT-02 | Comprobar la regla y los escenarios de confirmación y reversión | K34 pasa | OK | Verificado documentalmente | Verificación documental; no es validación técnica |
| C-10 | No existe autovalidación | IG5-55, IG5-67 | ESPECIFICACION 4.4.3 | IG5-55, IG5-67 y sus escenarios | Comprobar reglas y escenarios de exclusión y confirmación propias | K35 pasa | OK | Verificado documentalmente | Verificación documental; no es validación técnica |
| C-11 | No existe autoevaluación | IG5-56, IS-14 | ESPECIFICACION 4.4.3 y 4.4.6 | IG5-56, IS-14 y sus escenarios | Comprobar reglas y escenarios de evaluación propia | K35 pasa | OK | Verificado documentalmente | Verificación documental; no es validación técnica |
| C-12 | No hay asignación automática a Admin | IG5-57, IS-14 | ESPECIFICACION 4.4.3 y 8.7 | IG5-57, IS-14 y sus escenarios | Comprobar reglas y escenarios de Admin | K35 pasa | OK | Verificado documentalmente | Verificación documental; no es validación técnica |
| C-13 | No se permite evaluación con procedencia incompleta | IG5-64, IG5-78 | ESPECIFICACION 4.4.5 | Diez errores; escenario «procedencia incompleta que bloquea» | Comprobar los diez errores, su bloqueo y los escenarios | K12 pasa; K13 pasa; K36 pasa | OK | Verificado documentalmente | Verificación documental; no es validación técnica |
| C-14 | No se permite publicación con evaluación obsoleta | IG5-66, IG5-68, IG5-89 | ESPECIFICACION 4.4.7 | IG5-89; escenarios de integración | Comprobar reglas y escenarios de evaluación obsoleta | K36 pasa | OK | Verificado documentalmente | Verificación documental; no es validación técnica |
| C-15 | No se crearon permisos nuevos | P8 | ESPECIFICACION 2 y 10.1 | 17 claves físicas | Comparar las claves citadas con las 17 de v3.3 | K19 pasa | OK | Verificado documentalmente | Verificación documental; no es validación técnica |
| C-16 | No se crearon estados nuevos | P8 | ESPECIFICACION 2 | Estados de T-02 sin cambio | Buscar frases que creen estados | K20 pasa | OK | Verificado documentalmente | Verificación documental; no es validación técnica |
| C-17 | No se crearon transiciones nuevas | P8, IP-01 | ESPECIFICACION 2 | 13 transiciones | Buscar transición #14 o posterior | K20 pasa | OK | Verificado documentalmente | Verificación documental; no es validación técnica |
| C-18 | No se modificaron las 13 transiciones T-02 | IP-01 | ESPECIFICACION 2 | IP-01 y declaración de 13 transiciones | Comprobar la declaración y la regla IP-01 | K20 pasa | OK | Verificado documentalmente | Verificación documental; no es validación técnica |
| C-19 | No se modificaron las 17 claves físicas | P8 | ESPECIFICACION 10.1 | 17 claves presentes | Comprobar que las 17 claves figuran y ninguna otra | K19 pasa | OK | Verificado documentalmente | Verificación documental; no es validación técnica |
| C-20 | El roadmap respeta las dependencias | IE-08 | ROADMAP 3 y 4 | 76 subfases; orden de creación | Contar subfases y comprobar la existencia de las del orden de creación | K18 pasa; K16 pasa | OK | Verificado documentalmente | Verificación documental; no es validación técnica |
| C-21 | Las FK respetan el orden de creación | H-01 de la v4 | ESPECIFICACION 14.1 | Orden de creación | Comprobar que ninguna FK apunta a una tabla creada después | K16 pasa; K17 pasa | OK | Verificado documentalmente | Verificación documental; no es validación técnica |
| C-22 | Cada regla tiene al menos un escenario | IE-08 | ESPECIFICACION 11 | Cobertura regla-escenario | Calcular los escenarios de cada regla | K06 pasa; K08 pasa | OK | Verificado documentalmente | Verificación documental; no es validación técnica |
| C-23 | Cada escenario referencia reglas existentes | IE-08 | ESPECIFICACION 11 | Columna Reglas de cada escenario | Buscar referencias inexistentes y escenarios sin regla | K05 pasa; K07 pasa | OK | Verificado documentalmente | Verificación documental; no es validación técnica |
| C-24 | Los IDs son únicos | IE-08 | ESPECIFICACION 11 | IDs de reglas y de escenarios | Buscar duplicados y huecos | K02 pasa; K03 pasa; K04 pasa | OK | Verificado documentalmente | Verificación documental; no es validación técnica |
| C-25 | Las cifras se recalculan desde los archivos, no se copian | IE-06 | ESPECIFICACION 11.1; INFORME | Resumen 11.1 y tabla del informe | Recalcular y comparar con cada documento | K09 pasa | OK | Verificado documentalmente | Verificación documental; no es validación técnica |
| C-26 | Los diagramas Mermaid representan el modelo actualizado | IG5-80 | ESPECIFICACION 4.4.4 y 4.4.7 | Diagrama ER y flujo de 19 pasos | Comparar las aristas del ER con el contrato y contar los pasos del flujo (el renderizado visual no se verifica) | K26 pasa; K30 pasa | OK | Verificado documentalmente | Verificación documental; no es validación técnica |
| C-27 | No hay contradicciones entre especificación, informe, auditoría y roadmap | IE-08 | todos | Patrones de contradicción; secuencia de subfases; estados | Buscar patrones obsoletos y comparar estados y secuencias | K27 pasa; K17 pasa; K22 pasa | OK | Verificado documentalmente | Verificación documental; no es validación técnica |
| C-28 | No se declara validación técnica inexistente | IE-05 | todos | Negación de toda validación técnica | Buscar afirmaciones de validación técnica no negadas | K23 pasa; K31 pasa | OK | Verificado documentalmente | Verificación documental; no es validación técnica |

**Auditoría integral final (28 puntos).**

| # | Punto auditado | Comprobaciones | Resultado |
|---|---|---|---|
| 1 | Los 28 controles de auditoría | K40 | OK (verificado documentalmente) |
| 2 | Reglas de contribución directa | K11, K37 | OK (verificado documentalmente) |
| 3 | Herencia de contribuyentes de copy | K37, K14 | OK (verificado documentalmente) |
| 4 | Herencia de contribuyentes de brief | K13, K38 | OK (verificado documentalmente) |
| 5 | Herencia de contribuyentes de promociones | K13, K38 | OK (verificado documentalmente) |
| 6 | Procedencia exacta de assets | K14, K37 | OK (verificado documentalmente) |
| 7 | Integridad de contribution_events | K14, K32 | OK (verificado documentalmente) |
| 8 | Integridad de copy_version_provenance | K14, K37 | OK (verificado documentalmente) |
| 9 | Referencias inmutables de copy_versions | K14, K33 | OK (verificado documentalmente) |
| 10 | Completitud de version_contributors | K12, K38 | OK (verificado documentalmente) |
| 11 | Errores de procedencia incompleta | K12 | OK (verificado documentalmente) |
| 12 | Fail-closed | K36, K12 | OK (verificado documentalmente) |
| 13 | Exclusión del proponente de independencia vigente | K34 | OK (verificado documentalmente) |
| 14 | Elegibilidad del evaluador | K34, K35 | OK (verificado documentalmente) |
| 15 | Ausencia de autoevaluación | K35 | OK (verificado documentalmente) |
| 16 | Reglas de G-7 | K39 | OK (verificado documentalmente) |
| 17 | Reglas de G-10 | K39 | OK (verificado documentalmente) |
| 18 | Unicidad e integridad de IDs | K02, K03, K04 | OK (verificado documentalmente) |
| 19 | Cobertura regla-escenario | K06, K07, K08 | OK (verificado documentalmente) |
| 20 | Coherencia entre especificación, informe, auditoría y roadmap | K09, K17, K22, K27 | OK (verificado documentalmente) |
| 21 | Orden de dependencias de las 76 subfases | K16, K18 | OK (verificado documentalmente) |
| 22 | Ausencia de permisos nuevos | K19 | OK (verificado documentalmente) |
| 23 | Ausencia de transiciones nuevas | K20 | OK (verificado documentalmente) |
| 24 | Preservación de decisiones pendientes | K21 | OK (verificado documentalmente) |
| 25 | Preservación de v3.3 | K25, K22, K48 | OK (verificado documentalmente) |
| 26 | Ausencia de afirmaciones de validación técnica no ejecutada | K23 | OK (verificado documentalmente) |
| 27 | Ausencia de contradicciones con v3, v4 y v5 | K27 | OK (verificado documentalmente) |
| 28 | Integridad del registro histórico | K25, K28 | OK (verificado documentalmente) |

**Auditoría final v7 (14 verificaciones).**

| # | Verificación | Comprobaciones | Resultado |
|---|---|---|---|
| 1 | Ejecutar el verificador documental | K01 | OK (verificado documentalmente) |
| 2 | Ejecutar todas las mutaciones negativas | K42 | OK (verificado documentalmente) |
| 3 | Cada defecto es detectado | K42 | OK (verificado documentalmente) |
| 4 | 28 controles de auditoría | K40 | OK (verificado documentalmente) |
| 5 | SHA-256 de v3.3 calculado sobre el original (o limitación real) | K48 | OK (verificado documentalmente) |
| 6 | Reconstrucción de contribuyentes por campo | K13, K38, K47, K49 | OK (verificado documentalmente) |
| 7 | Independencia de las resoluciones | K46, K49 | OK (verificado documentalmente) |
| 8 | Relaciones y claves compuestas | K44, K45 | OK (verificado documentalmente) |
| 9 | Escenarios de G-1, G-5 y G-10 | K39, K13, K49 | OK (verificado documentalmente) |
| 10 | IDs y referencias | K02, K03, K04, K05, K06, K07, K08 | OK (verificado documentalmente) |
| 11 | 76 subfases | K18 | OK (verificado documentalmente) |
| 12 | 17 claves de permisos y 13 transiciones T-02 | K19, K20 | OK (verificado documentalmente) |
| 13 | Decisiones pendientes sin alterar | K21 | OK (verificado documentalmente) |
| 14 | Coherencia entre los cinco documentos activos | K09, K17, K22, K27 | OK (verificado documentalmente) |
<!-- VERIFICADOR:FIN -->

## 4. Errores hallados y corregidos durante la v7

| Error | Corrección |
|---|---|
| La mutación M-18 (cifra incorrecta) parecía no detectada solo porque el estado inicial no era válido (el registro de la v6 aún no tenía la entrada v7) | El registro se regenera con la entrada v7 y el verificador exige estado inicial válido para contar una mutación como detectada |
| El catálogo de claves de destino omitía creative_pieces y approvals, por lo que K44 reportaba destinos inexistentes | Se agregaron ambas tablas históricas (con is_adaptation boolean) al catálogo de la sección 4.4.9 |
| La primera versión de K45 trataba como error la FK de las filas de cambio hacia la versión (organization_id, brief_id, versión) y no encontraba la FK al antecesor de las atribuciones | Se corrigieron las dos reglas semánticas; las mutaciones M-08, M-09 y M-10 siguen detectándose |
| K32 señalaba source_kind de attribution_discard_resolutions como referencia polimórfica | La columna es un discriminador de tres FK tipadas con num_nonnulls = 1; K32 lo admite solo si esa restricción existe |
| Un error de clave (checks) en K32 tras ampliar el análisis de entidades | Corregido; K32 usa el texto del bloque de la entidad |

Ninguna herramienta interna se usa como evidencia: toda cifra de este documento procede del verificador publicado.

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
| RR-27 | DT-01, PC-02 y DT-02 se resuelven en el diseño complementario v6 (definición operativa, representación física y elegibilidad del proponente), pero no están aceptadas por el propietario ni validadas técnicamente |
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
| RR-40 | La regla de segmentos (una línea no vacía por segmento) puede sobreatribuir: una línea idéntica conservada por un cambio de formato mantiene al autor anterior como contribuyente activo |
| RR-41 | La normalización NFKC, de saltos de línea y de espacios depende de funciones de PostgreSQL y de la configuración regional no verificadas |
| RR-42 | verify_field_provenance recorre la cadena completa y recalcula las atribuciones: su costo crece con el número de versiones |
| RR-43 | La alcanzabilidad del arte heredado (reused_from_asset_id) se impone por trigger, no por FK declarativa |
| RR-44 | El verificador publicado analiza texto Markdown con reglas sintácticas: no ejecuta SQL, no renderiza Mermaid y no valida semántica de negocio |
| RR-45 | Un nombre de tabla con formato distinto al esperado por el verificador podría omitirse de una comprobación |

## 6. Estado por brecha

| Brecha | Estado |
|---|---|
| G-1 | Diseño documental completo; preparado para aceptación formal |
| G-5 | Diseño documental completo; no declarada plenamente cerrada: sin aceptación ni validación técnica |
| G-10 | Diseño documental completo; sin aceptación ni validación técnica |

Ninguna está aceptada ni validada técnicamente.
