---
name: auditoria_final_g1_g5_g10
description: Auditoría final de la revisión v15 de G-1, G-5 y G-10 (matriz de 28 controles, verificador publicado con resultado real, pruebas estructurales de K45, K46 y K47, auditoría integral de 28 puntos, riesgos residuales)
---

# AUDITORÍA FINAL — G-1, G-5 Y G-10 (revisión v15)

Distinción de versiones: el diseño técnico complementario vigente es la v15; la corrección documental V16 (commit `6a1af2424ef39e0960b8f7e09d4e19ec52e6f046`, padre `ad34f1a50c6b90f9fc880a2172141c7de6b8838a`) solo cambió la línea 15 del roadmap (de v5 a v15) y no es una revisión del diseño ni de las pruebas. Esta auditoría describe el diseño v15; no se reejecuta ni se redefine por V16.

Los escenarios de diseño (T-xx) no están ejecutados. Se ejecutan pruebas de modelo en memoria (K45, K46, K47) y comprobaciones documentales; ninguna es una prueba en PostgreSQL ni Supabase y el diseño no está validado técnicamente.

## 0. Estado y niveles de evidencia

| Nivel | Estado | Alcance |
|---|---|---|
| 1. Fase 0 v3.3 | COMPLETADA Y ACEPTADA COMO LÍNEA BASE DOCUMENTAL, CON LIMITACIONES DOCUMENTADAS | No se reabre ni se modifica; SHA-256 `b5dccdc73a8103966ab1e1b1e84b2e7ead68cd736fba666ec71d0e790d51c1da` sin cambio |
| 2. Diseño complementario v15 (G-1, G-5, G-10) | COMPLETADO DOCUMENTALMENTE Y PREPARADO PARA ACEPTACIÓN FORMAL DEL PROPIETARIO, CON LIMITACIONES TÉCNICAS EXPLÍCITAS | Pendiente de aceptación formal del propietario; no validado técnicamente; la Adenda v9 sigue sin aceptar (PO-05) |
| 3. Fase 1 | NO INICIADA / NO AUTORIZADA | Requiere autorización expresa; este diseño no la concede |


| Nivel de evidencia | Significado | Alcance |
|---|---|---|
| Diseñado | La regla o el escenario está escrito en la especificación | Nada ejecutado |
| Verificado documentalmente | El verificador publicado comprobó coherencia entre los documentos: IDs, referencias, cifras, contratos, orden, estados | Resultado reproducible; no prueba que el diseño funcione en PostgreSQL |
| Validado técnicamente | Ejecución real contra PostgreSQL, RLS y Supabase con las pruebas de la matriz | **Pendiente**: ningún control ni escenario alcanza este nivel |


## 1. Hallazgos de la v14 y su corrección

| Hallazgo | Defecto | Corrección (resumen) | Referencia | Reglas | Escenarios |
|---|---|---|---|---|---|
| H-01 El asset_version del evento propio de reutilización no se validaba contra la versión exacta del asset de destino | `Motor._verificar_reutilizado` y `Motor._datos_evento` de la v14 comprobaban `source_asset_version` pero no que `asset_version` coincidiera con la versión exacta del asset que produjo el evento: una corrupción en cualquier eslabón se aceptaba y el evento del destino guardaba la versión del origen. | `Motor._chk_asset_version` valida por identidad exacta (`asset_version_id`) en todos los eslabones; `registrar_asset` escribe la versión 1 del destino; `source_asset_version` se valida aparte; las 15 … | ESPECIFICACION 4.4.17 A, B y C | IG5-111, IE-12 | T-727 a T-734 |
| H-02 El campo del evento propio no se validaba como «arte» en cada eslabón | La v14 no comprobaba el campo del evento propio en la reconstrucción de la cadena: un evento vinculado a otro campo (por ejemplo headline o precio), ausente o nulo se aceptaba. | `Motor._chk_campo` y `Motor._campos_permitidos` exigen campo = arte en reutilizaciones, cargas modificadas y raíz, antes de escribir y también después de construida una cadena posterior.… | ESPECIFICACION 4.4.17 C y F | IG5-112, IE-12 | T-735 a T-742 |
| H-03 El rechazo no identificaba el vínculo, el evento, el campo, lo esperado ni lo hallado | Un rechazo no permitía distinguir qué relación fallaba ni descartar que otra excepción lo hubiera provocado. | `ReutilizacionInvalida.detalles` informa eslabón, evento, campo, esperado, hallado y motivo; `mensaje_usuario` no expone datos internos; una excepción ajena nunca cuenta como detección; mutaciones com… | ESPECIFICACION 4.4.17 D y G | IG5-113, IE-12 | T-743 a T-748 |
| H-04 Faltaban suites negativas con doce condiciones por mutación | Las mutaciones de la v14 no exigían, juntas, estado inicial válido, cambio real, rechazo, causa concreta, ausencia de asset, evento, atribución y relación parciales, estado completo idéntico, procedencia incompleta, E no completo y bloqueo de impacto, aprobación y publicación. | AV-01 a AV-08, CF-01 a CF-08 y AC-01 a AC-06, cada una con las doce condiciones; ninguna se acepta por una excepción ajena.… | ESPECIFICACION 4.4.17 E, F y G | IG5-111 a IG5-114 | T-727 a T-748 |
| H-05 Faltaban casos positivos de las nuevas validaciones | Sin casos válidos no se demuestra que las validaciones no bloqueen relaciones correctas. | AP-01 a AP-08: cadenas de dos y tres niveles, versiones iguales de assets distintos, reutilización tras una modificación, uploader original distinto, atribución directa exacta, campo arte en todos los… | ESPECIFICACION 4.4.17 H | IG5-111 a IG5-113 | T-749 a T-756 |
| H-06 El auditor independiente no comparaba asset_version ni campo por eslabón | Un motor que aceptaba una corrupción de esas referencias no era detectado por el auditor. | `_hall_cadena` compara asset_version y campo por eslabón sin funciones del motor (`_compartidas()` vacío); ADV15-01 a ADV15-08 fuerzan la aceptación y exigen detección, E bloqueado y fallo cerrado de … | ESPECIFICACION 4.4.17 I | IG5-115 | T-757 a T-764 |
| H-07 La atomicidad no se probaba con instantánea completa en cada momento de fallo | Un fallo en la validación de asset_version, campo, actor o atribución, o durante el registro, no comparaba el estado completo ni los datos derivados. | AT15-01 a AT15-08 inyectan el fallo en ocho momentos, comparan el estado completo y los datos derivados y repiten sin fallo con un registro válido.… | ESPECIFICACION 4.4.17 J | IG5-114 | T-765 a T-772 |
| H-08 El identificador K55 estaba asignado a dos controles del verificador | Un identificador repetido impedía citar y mutar cada control de forma inequívoca. | El segundo control pasa a K55-V12 sin eliminar ninguna condición; equivalencia documentada; K58 exige identificadores únicos y que los documentos citen K55-V12; K57-D09 reintroduce el duplicado y es d… | ESPECIFICACION 4.4.17 N | IG5-116 | T-777 a T-777 |
| H-09 La comparación estructural no cubría las nuevas validaciones ni las suites | Las validaciones, el auditor, las suites AV, CF, AC y AP y la cobertura debían contrastarse con el modelo y el documento. | K56 ejecuta las doce baterías y verifica la estructura del código (validaciones existentes e invocadas, auditor sin llamadas al motor, pruebas históricas conservadas, sin skip ni xfail); K57 compara r… | ESPECIFICACION 4.4.17 K, L y M | IG5-116 | T-773 a T-776 |
| H-10 La regresión debía conservar todas las pruebas históricas y ser reproducible | Una corrección no debe reducir cobertura ni producir resultados distintos entre ejecuciones. | Se conservan CHAIN, ADVC, ATTR, AT14, E14, K45, K46, K47, FK y K57-D01 a K57-D12; dos ejecuciones limpias con `env -i` producen salidas --md y --json idénticas.… | ESPECIFICACION 4.4.17 O; AUDITORIA 3 | IG5-116 | T-779 a T-779 |
| H-11 Los documentos debían describir la v15 sin contradicciones | Especificación, informe, auditoría, roadmap, registro y herramientas debían contar lo mismo. | Los cinco documentos se regeneran con las mismas cifras; se conservan las copias históricas v14 y las anteriores con su SHA-256 en el manifiesto.… | todos | IG5-116, IE-12 | T-780 a T-780 |

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

## 3. Verificador documental y matriz de controles

Una sola herramienta publicada, `docs/fase0/herramientas/verificar_expediente.py`, produce cada resultado. Cada control cita las comprobaciones que lo sustentan: un control es OK solo si todas aprueban; si una falla es NO OK; si no existe la comprobación es PENDIENTE. El nivel máximo alcanzable es «Verificado documentalmente».

| Concepto | Detalle |
|---|---|
| Archivo | docs/fase0/herramientas/verificar_expediente.py |
| Comando | `python3 docs/fase0/herramientas/verificar_expediente.py --md` (también `--json`, `--dir RUTA`, `--sin-mutaciones` y `--v33 RUTA`) |
| Dependencias | Python 3.8 o superior; solo biblioteca estándar; el módulo `docs/fase0/herramientas/modelo_estructural.py` (modelo relacional de K45 y motor de K47) debe estar junto al verificador; no accede a red, base de datos ni servicios |
| Entrada | Los cinco documentos activos, los archivos de `historico/` (SHA-256 del manifiesto del registro) y, opcionalmente con `--v33 RUTA`, el archivo original de la línea base v3.3 |
| Salida | Un resultado por comprobación (APRUEBA, FALLA o PENDIENTE), la matriz de 28 controles con 10 campos y la auditoría integral de 28 puntos; código de salida 1 si algo falla |
| Número de comprobaciones | 59 |
| Reproducibilidad | La comprobación K41 ejecuta todo dos veces y compara; el bloque siguiente se genera con `--md` y se puede regenerar y comparar. El verificador ignora el bloque al analizar para no depender de su propio resultado |
| Controles negativos | K42 ejecuta 300 mutaciones, cada una desde un estado válido y con un único cambio, y exige que el control correspondiente la rechace con la condición esperada: M-01 a M-25 (relaciones, actor, asset, versión, antecesor, resoluciones, sustitución textual, estructura del expediente y un bit alterado en una copia del original de v3.3), K46-M01 a K46-M12 (independencia del resolutor sobre un caso con cadena), K45-M01 a K45-M27 (un cambio en un registro del modelo relacional, detectado por C01 a C15) y K47-M01 a K47-M36 (un fallo inyectado en una operación del motor, detectado por el auditor independiente por I1 a I12), K47-R01 a K47-R12 (un registro de resoluciones alterado fuera del motor, con el sello recalculado cuando procede, detectado por I13 a I15 con la condición específica) y K47-A01 a K47-A53 (una procedencia o identidad de arte alterada o incompleta, detectada por I1, I6, I16 a I28 con la condición específica; las de A17 en adelante exigen además procedencia incompleta, E no completo y E bloqueado), K47-A54 a K47-A65 (una reutilización cuya relación del origen se altera, rechazada por el motor antes de escribir con la relación identificada, sin registros parciales, con el estado completo idéntico y E nulo) FK01 a FK41 (una FK compuesta de las relaciones source_* eliminada, corrompida o excepcionada sin justificación en la especificación, detectada por K32, K44, K45 o K55), CHAIN-01 a CHAIN-24 (un eslabón intermedio de la cadena alterado, rechazado antes de escribir con el eslabón identificado), ATTR-01 a ATTR-12 (una atribución o resolución alterada, detectada por el auditor), K56-M01 a K56-M12 (una defensa del código del modelo degradada temporalmente en memoria, detectada por al menos una prueba), AV-01 a AV-08, CF-01 a CF-08 y AC-01 a AC-06 (un asset_version, un campo o ambos corruptos en el evento propio de un eslabón, rechazados antes de escribir con el eslabón, el evento y el campo identificados) y K57-D01 a K57-D12 (una tabla, cifra o referencia del documento alterada, detectada por K55 o K57). Una mutación cuyo estado inicial no es válido, que no cambia el caso, que termina en excepción o que solo se detecta por otro código no cuenta como detectada |
| Modelo estructural | `docs/fase0/herramientas/modelo_estructural.py`: tablas del modelo relacional de K45 (organizaciones, miembros, piezas, versiones de brief, snapshots, versiones de copy, assets, eventos y atribuciones); motor de K47 con las operaciones crear versión, introducir, modificar, sustituir y eliminar campo, heredar, registrar, rechazar y aplicar resolución, cambiar clasificación, reconstruir procedencia, calcular E y comprobar completitud (desde la v14, además, reconstrucción de la cadena completa vínculo por vínculo, atomicidad de 19 operaciones; desde la v15, validación de asset_version y campo en cada evento propio, diagnóstico estructurado y atomicidad con instantánea completa en ocho momentos; asignación, confirmación y publicación con elegibilidad del evaluador E1 a E7); auditor independiente de I1 a I28 con reconstrucción de la identidad del origen, eventos y antecesores desde los registros, sin funciones del motor; cierre en falso de E (`calcular_E_verificado`); dieciséis pruebas adversariales y veinte de atomicidad con comparación del estado completo, doce mutaciones de rechazo previo, y comprobaciones estructurales de las FK compuestas source_* (RS-01 a RS-08, inventario, ciclos y orden de inserción); registro de resoluciones de solo agregado con sello SHA-256 y cadena de reconsideración; asset con uploader, evento de carga, reutilizador y cadena de reutilización. Datos ficticios; todo en memoria |
| Hash de v3.3 (K48) | El archivo original de v3.3 no está en el repositorio; el bloque siguiente se generó indicando su ruta con `--v33`, por lo que K48 calculó su SHA-256 y lo comparó con `b5dccdc73a8103966ab1e1b1e84b2e7ead68cd736fba666ec71d0e790d51c1da`. Una ejecución sin `--v33` deja K48 en PENDIENTE_ARCHIVO_ORIGINAL_NO_DISPONIBLE y no declara el hash como comprobado: el hash escrito en el registro es solo un registro histórico (K25) |
| Limitaciones | Análisis sintáctico de Markdown: no ejecuta SQL, no valida PostgreSQL ni RLS, no renderiza Mermaid (solo compara aristas y cuenta pasos) y no prueba la semántica de negocio; es verificación documental, no validación técnica |

### Resultado real del verificador

<!-- VERIFICADOR:INICIO -->
**Comprobaciones ejecutadas: 59. Aprobadas: 59. Fallidas: 0. Pendientes: 0.** Controles: 28; OK: 28; NO OK: 0; PENDIENTE: 0. Mutaciones negativas: 300; detectadas: 300; no detectadas: 0.

| Comprobación | Resultado | Descripción | Regla | Documento y sección |
|---|---|---|---|---|
| K01 | APRUEBA | Los cinco documentos activos existen y no están vacíos | IE-08 | todos |
| K02 | APRUEBA | IDs de reglas únicos (231 reglas) y con el mismo texto en la definición y en la cobertura | IE-08 | ESPECIFICACION 11 |
| K03 | APRUEBA | IDs de escenarios únicos y consecutivos (780 escenarios) | IE-08 | ESPECIFICACION 11 |
| K04 | APRUEBA | Todo escenario tiene ID, requisito, datos iniciales, acción, resultado esperado, resultado prohibido, criterio, nivel y reglas | IE-07 | ESPECIFICACION 11 |
| K05 | APRUEBA | Todo escenario referencia solo reglas existentes | IE-08 | ESPECIFICACION 11 |
| K06 | APRUEBA | Toda regla tiene al menos un escenario (cobertura 231 de 231) | IE-08 | ESPECIFICACION 11 |
| K07 | APRUEBA | Todo escenario está asociado a al menos una regla | IE-08 | ESPECIFICACION 11 |
| K08 | APRUEBA | La tabla de cobertura regla-escenario de la especificación coincide con las referencias de los escenarios | IE-08 | ESPECIFICACION 11 |
| K09 | APRUEBA | Cifras recalculadas desde los archivos (231 reglas, 780 escenarios, 41 tablas, 14 nuevas) y coincidentes en los cinco documentos | IE-06 | ESPECIFICACION 11.1; INFORME |
| K10 | APRUEBA | La fórmula del conjunto excluido E es idéntica en todos los documentos (10 apariciones) | IG5-56 | ESPECIFICACION 4.4.3 |
| K11 | APRUEBA | Existe una sola definición de contribuyente (figuras A a F en 4.4.3) y no se redefine en otros documentos | IG5-40 | ESPECIFICACION 4.4.3 |
| K12 | APRUEBA | Los diez errores de procedencia están en el contrato de version_contributors y cada uno aparece en al menos un escenario | IG5-78 | ESPECIFICACION 4.4.5 |
| K13 | APRUEBA | Los 26 escenarios mínimos de H-02 existen (26 escenarios H-02, con datos, versiones, actores, acción, esperado, prohibido, regla y nivel) | IG5-69 a IG5-79 | ESPECIFICACION 4.4.8 |
| K14 | APRUEBA | Contrato de integridad (65 relaciones): 10 campos completos por fila, toda FK de las nueve tablas de procedencia figura en él y toda FK incluye organization_id | IG5-80 | ESPECIFICACION 4.4.9 |
| K15 | APRUEBA | Las nueve tablas de procedencia tienen bloque de definición y fila en el orden de creación; sin tablas repetidas (41 tablas) | IG5-80 | ESPECIFICACION 4.4.4; 14.1 |
| K16 | APRUEBA | Orden de creación: ninguna tabla, función o trigger depende de un objeto posterior y ninguna FK apunta a una tabla creada después (100 pasos) | IE-08 (H-01 de la v4) | ESPECIFICACION 14.1 |
| K17 | APRUEBA | La secuencia de subfases de creación es idéntica en especificación, roadmap y auditoría | H-01 v4 | ROADMAP 3; AUDITORIA 2 |
| K18 | APRUEBA | El roadmap conserva las 76 subfases, sin duplicados ni subfase 77, y toda subfase del orden de creación existe en él | Roadmap v9 | ROADMAP |
| K19 | APRUEBA | Las 17 claves físicas permanecen: las claves citadas están entre las 17, las 17 figuran en la especificación y ninguna frase crea permisos ni roles | P8 | ESPECIFICACION 10.1 |
| K20 | APRUEBA | T-02 conserva 13 transiciones: sin transición #14 o posterior, sin estados ni transiciones nuevos | P8, IP-01 | ESPECIFICACION 1 y 2 |
| K21 | APRUEBA | Las decisiones y limitaciones pendientes del propietario se conservan visibles (14 elementos) en especificación, informe y registro | IG5-48 | ESPECIFICACION 12.3; INFORME |
| K22 | APRUEBA | Estados: v3.3 aceptada como línea base, v15 completada documentalmente y preparada para aceptación formal, Fase 1 no iniciada; ningún documento declara aceptación del propietario de la v15 | IE-04 | todos |
| K23 | APRUEBA | Ningún documento afirma validación técnica ni pruebas técnicas ejecutadas (toda mención está negada o pendiente) | IE-05 | todos |
| K24 | APRUEBA | La atribución no usa IA, similitud, embeddings ni inferencias probabilísticas como autoridad (toda mención está negada) y IG5-70 define la regla determinista | IG5-43, IG5-70 | ESPECIFICACION 4.4.8 |
| K25 | APRUEBA | Los archivos históricos conservan su SHA-256 registrado en el manifiesto (52 archivos) y el registro cita el hash aceptado de v3.3 con b5dccdc7 (registro histórico; la comprobación criptográfica del original es K48) | IE-04 | REGISTRO manifiesto |
| K26 | APRUEBA | El diagrama de relaciones (34 aristas) coincide con las relaciones del contrato de integridad | IG5-80 | ESPECIFICACION 4.4.4 |
| K27 | APRUEBA | Sin contradicciones con las versiones anteriores en los documentos activos (patrones de fuentes, errores y pendientes obsoletos) | IE-08 | todos |
| K28 | APRUEBA | Registro histórico: entradas ordenadas por revisión hasta la v15 con el commit previo 1d14e51… (v14 sobre d4044c2…, v13 sobre 603b039…, v12 sobre 7916115…, v11 sobre 651c730…, v10 sobre 638ca8c… y v9 sobre a6b36b9…) y manifiesto de históricos | IE-04 | REGISTRO |
| K29 | APRUEBA | La especificación documenta la herramienta publicada, su comando y sus límites | IE-08 | ESPECIFICACION 11.2; AUDITORIA 3 |
| K30 | APRUEBA | El flujo integrado de 4.4.7 tiene los 19 pasos en el orden obligatorio | IG5-88 | ESPECIFICACION 4.4.7 |
| K31 | APRUEBA | Los niveles de evidencia están definidos (Diseñado, Verificado documentalmente, Validado técnicamente) y IE-05 a IE-08 existen | IE-05 | AUDITORIA 1 |
| K32 | APRUEBA | Las ocho tablas de procedencia no tienen referencias polimórficas, cada columna *_id (incluidas todas las source_*) está cubierta por una FK compuesta exacta (RS-01 a RS-08: columnas, destino, acción y momento) o por una excepción individual justificada con verificador K45, sin exclusiones generales, y ninguna apunta al último o al actual | IG5-81, IG5-62 | ESPECIFICACION 4.4.4 |
| K33 | APRUEBA | Inmutabilidad: el contrato la define para las trece tablas, IS-13, IG5-85 e IG5-87 existen y 4 escenarios de H-03 intentan modificar, borrar o truncar | IS-13 | ESPECIFICACION 4.4.9 |
| K34 | APRUEBA | DT-02: IG5-45 limita la exclusión al proponente de la clasificación vigente, IG5-68 protege a quien confirma o revierte y 12 escenarios lo cubren | IG5-45, IG5-68 | ESPECIFICACION 4.4.6 |
| K35 | APRUEBA | Sin autovalidación, autoevaluación ni asignación automática a Admin: IG5-55, IG5-67, IG5-57 e IS-14 y 5 escenarios de Admin | IG5-55, IG5-57, IG5-67, IS-14 | ESPECIFICACION 4.4.3 |
| K36 | APRUEBA | Fail-closed: IG5-64 e IG5-78 bloquean evaluación, independencia y aprobación o publicación sin excepción de Admin; IG5-89 impide reutilizar evaluaciones; 17 escenarios de bloqueo | IG5-64, IG5-78, IG5-89 | ESPECIFICACION 4.4.5 |
| K37 | APRUEBA | Las reglas de contribución directa, herencia de copy y procedencia de copy y arte existen y tienen escenarios (10 reglas) | IG5-49 a IG5-54, IG5-83, IG5-84 | ESPECIFICACION 4.4.3 y 4.4.9 |
| K38 | APRUEBA | H-02: 12 campos de brief y 9 de promoción catalogados, regla de segmentos (IG5-70), cálculo de atribuciones (IG5-72), historial (IG5-73), dos algoritmos de 10 pasos y reglas IG5-69 a IG5-79 | IG5-69 a IG5-79 | ESPECIFICACION 4.4.8 |
| K39 | APRUEBA | Reglas de G-7 (C1 a C9) y de G-10 (37 reglas IG10) presentes con cobertura | IG10-* | ESPECIFICACION 5 y 6.2 |
| K44 | APRUEBA | Integridad estructural de 117 relaciones: longitud, orden exacto de columnas, organization_id, PK o UNIQUE de destino con las mismas columnas, tipos compatibles, contrato igual a los bloques, sin relaciones rotas ni circulares salvo los ciclos declarados en la matriz de 4.4.15 con su orden de inserción | IG5-80, IE-09 | ESPECIFICACION 4.4.4 y 4.4.9 |
| K45 | APRUEBA | Integridad semántica sobre un modelo relacional con identidad propia (organizaciones, miembros, piezas, versiones de brief, snapshots, versiones de copy, assets, eventos, atribuciones, herencia y reutilización): 15 controles C01 a C15 evaluados sobre las relaciones reales, matriz de correspondencias de 4.4.10 (S1 a S12) contrastada con los nombres físicos, 3 casos positivos sin falsos positivos, 27 mutaciones detectadas cada una por su código y, para las relaciones source_* RS-01 a RS-08, los pares exactos origen-destino (asset lógico, versión exacta, evento de carga, uploader y atribución), la prueba negativa de cada excepción y la ausencia de identidad por número de versión | IG5-81 a IG5-84, IG5-96, IS-16, IE-09, IE-12 | ESPECIFICACION 4.4.4, 4.4.9 y 4.4.10 |
| K46 | APRUEBA | Resolución independiente de descarte: afectado, solicitante y actor del cambio no resuelven, evidencia ligada a la misma atribución y versión, autoridad de revisión, identidad autenticada, independencia respecto de todos los contribuyentes y eventos de la cadena (R1 a R9), fail-closed sin resolutor elegible, cada resolutor elegible aceptado (sin falsos positivos) y 12 mutaciones detectadas | IG5-92, IG5-93, IG5-95, IE-12 | ESPECIFICACION 4.4.4, 4.4.8 y 4.4.10 |
| K47 | APRUEBA | Conservación estructural: motor en memoria con atribuciones individuales, versiones inmutables, resoluciones y E calculado recorriendo las atribuciones reales; 12 escenarios (A a L), el escenario de resoluciones inmutables (RS) y comprobaciones de uniformidad entre fuentes y de independencia de la similitud aprobados; registro de resoluciones sellado y de solo agregado con 9 intentos directos de alteración rechazados; procedencia del arte por versión de copy con identidad exacta de uploader, evento de carga, atribución y reutilización, 20 casos positivos (P01 a P20), 10 pruebas adversariales en las que el motor acepta, el auditor detecta y E se bloquea y 8 pruebas de atomicidad de la reutilización; identidad exacta del asset de origen por referencias explícitas (asset, versión, evento de carga, uploader y atribución original); auditor independiente de 28 invariantes (I1 a I28); tabla C de 4.4.10 igual al comportamiento observado del motor; 36 mutaciones previas, 12 de resoluciones inmutables (R01 a R12) y 53 de assets (A01 a A53) detectadas; además ninguna regla, algoritmo ni escenario retira por sustitución, eliminación, hash o retained_segments = 0 | IG5-72, IG5-90, IG5-91, IG5-97, IE-12 | ESPECIFICACION 4.4.8 y 4.4.10 |
| K52 | APRUEBA | Cobertura estructural v12: controles C01 a C15 con mutación (15/15), invariantes I1 a I28 con mutación (28/28), escenarios A a L aprobados (12/12), comprobaciones U, S, X, R y RS aprobadas, 20 casos positivos de arte, 10 pruebas adversariales, 9 intentos directos contra el registro de resoluciones rechazados, fixtures iniciales válidos y ninguna mutación con excepción | IG5-95 a IG5-99, IE-12 | ESPECIFICACION 4.4.10, 4.4.11 y 4.4.12 |
| K50 | APRUEBA | Registro histórico: cada entrada de revisión sucede a la anterior (vN posterior a vN-1; 12 entradas) | IE-04 | REGISTRO |
| K51 | APRUEBA | Cobertura v8: IG5-95, IG5-96, IG5-97 e IE-12 con escenarios (resolutor 13, correspondencias 15, conservación 19) | IG5-95 a IG5-97, IE-12 | ESPECIFICACION 4.4.10 y 11 |
| K53 | APRUEBA | Cobertura v10: IG5-98, IG5-99 e IE-12 con escenarios (resoluciones inmutables 17, arte 26) y la sección 4.4.12 documenta I13 a I21, las 12 mutaciones de resoluciones, las 16 de assets (A01 a A16) y los 7 casos positivos (P01 a P07) | IG5-98, IG5-99, IE-12 | ESPECIFICACION 4.4.12 |
| K54 | APRUEBA | Cobertura v11: IG5-100 e IE-12 con escenarios (identidad de assets 37) y la sección 4.4.13 documenta I22 a I26, las 21 mutaciones de la v11 (A17 a A32 y A49 a A53), los casos positivos P08 a P14 y las 5 pruebas adversariales | IG5-100, IE-12 | ESPECIFICACION 4.4.13 |
| K55 | APRUEBA | Cobertura v13: IG5-102, IG5-103 e IE-12 con escenarios (validación previa del origen 36, integridad referencial source_* 50); sección 4.4.15 con el inventario de columnas source_*, las relaciones RS-01 a RS-08, las seis soluciones evaluadas, la matriz de ciclos, el orden de inserción, las excepciones individuales, las mutaciones A54 a A65, los casos P21 a P26, las pruebas ADV11 a ADV16 y las mutaciones FK01 a FK15; las matrices del documento coinciden con el modelo y con las pruebas, y el verificador no contiene exclusiones generales de columnas source_* | IG5-102, IG5-103, IE-12 | ESPECIFICACION 4.4.15 |
| K56 | APRUEBA | Cobertura v14 y ejecución v15 de las baterías del modelo (detalle v15 en K59): validación vínculo por vínculo de la cadena (CHAIN 24/24), motor forzado frente al auditor independiente (ADVC 24/24), conservación de atribuciones y resoluciones (ATTR 12/12), atomicidad de las operaciones (AT14 11/11), E y elegibilidad del evaluador (E14 6/6) y 12 mutaciones del propio código (K56-M); el auditor no comparte funciones con el motor; reglas IG5-104 a IG5-110 con escenarios | IG5-104 a IG5-109 | ESPECIFICACION 4.4.16 |
| K57 | APRUEBA | Comparación estructural v14: cada regla IG5-104 a IG5-110 se traza a su implementación existente en el modelo, a pruebas existentes del conjunto ejecutado y a su verificador; cada prueba del conjunto ejecutado se cita; la matriz de auditoría (12 defectos), el orden de 14 pasos, las tablas de pruebas y la auditoría de 20 puntos por relación (RS-01 a RS-08) coinciden con lo calculado por el modelo y el verificador | IG5-110, IG5-109 | ESPECIFICACION 4.4.16 |
| K59 | APRUEBA | Cobertura v15: reglas IG5-111 a IG5-116 con escenarios, sección 4.4.17 con las suites AV-01 a AV-08, CF-01 a CF-08, AC-01 a AC-06, AP-01 a AP-08, ADV15-01 a ADV15-08, AT15-01 a AT15-08, K56-M09 a K56-M12 y D-13 a D-18, las 15 validaciones del evento propio, los límites de PostgreSQL y Supabase y un mensaje al usuario sin datos internos | IG5-111 a IG5-116 | ESPECIFICACION 4.4.17 |
| K58 | APRUEBA | Identidad única y estable de los controles: ningún identificador se repite en la ejecución ni en el código del verificador, K55 y K55-V12 se emiten una sola vez cada uno y la equivalencia documentada en 4.4.17 coincide con el modelo; los documentos citan K55-V12 | IG5-116 | ESPECIFICACION 4.4.17 |
| K55-V12 | APRUEBA | Cobertura v12 (control histórico antes identificado también como K55; equivalencia documentada en 4.4.17): IG5-101 e IE-12 con escenarios (identidad de origen 38), sección 4.4.14 con I27 e I28, las 16 mutaciones A33 a A48, los casos positivos P15 a P20 y las 5 pruebas adversariales nuevas; el modelo contiene los campos explícitos de identidad del origen en cada evento de reutilización, el auditor no usa funciones del motor (inspección del código), la reutilización inválida no deja registros parciales, se conservan las pruebas de la v11 y no hay skip ni xfail | IG5-101, IE-12 | ESPECIFICACION 4.4.14 |
| K49 | APRUEBA | H-02 v7: reglas IG5-90 a IG5-94 con cobertura y los 16 escenarios obligatorios (19 escenarios de atribución v7) | IG5-90 a IG5-94 | ESPECIFICACION 4.4.8 |
| K48 | APRUEBA | Hash de la línea base v3.3 calculado sobre los bytes de «fase0_v3_3_integral.md»: b5dccdc73a8103966ab1e1b1e84b2e7ead68cd736fba666ec71d0e790d51c1da; esperado b5dccdc73a8103966ab1e1b1e84b2e7ead68cd736fba666ec71d0e790d51c1da; COINCIDE | IE-10 | REGISTRO; AUDITORIA 3 |
| K40 | APRUEBA | La matriz define 28 controles con ID estable único, regla, sección, evidencia, procedimiento, resultado, estado y nivel; ninguno es OK sin comprobaciones aprobadas | IE-06, IE-07 | AUDITORIA 3 |
| K41 | APRUEBA | Reproducibilidad: dos ejecuciones sobre los mismos archivos producen los mismos resultados individuales | IE-08 | AUDITORIA 3 |
| K42 | APRUEBA | Controles negativos: 300 mutaciones introducidas en copias en memoria, 300 detectadas, 0 no detectadas | IE-08, IE-11 | AUDITORIA 3 |

**Mutaciones negativas (regresión completa).** Cada una parte de un estado inicial válido, aplica un único cambio identificable, ejecuta el control que debe detectarlo y registra el resultado esperado y el observado. Un veredicto DETECTADA exige además que el estado inicial sea válido y que el cambio modifique realmente el caso.

| ID | Regla probada | Estado inicial válido | Mutación aplicada | Resultado esperado | Resultado observado | Veredicto |
|---|---|---|---|---|---|---|
| M-01 | K44 (IG5-80, IE-09) | válido (K44 APRUEBA) | En brief_versions → briefs, la primera columna local pasa de organization_id a created_by | rechazo por K44 | RECHAZADA por K44 | DETECTADA |
| M-02 | K44 (IG5-80, IE-09) | válido (K44 APRUEBA) | En brief_field_attributions → brief_field_changes se invierte el orden de las dos últimas columnas referenciadas | rechazo por K44 | RECHAZADA por K44 | DETECTADA |
| M-03 | K44 (IG5-80, IE-09) | válido (K44 APRUEBA) | Se elimina de contribution_events la clave única (organization_id, id, brief_version_id, contributor_id) | rechazo por K44 | RECHAZADA por K44 | DETECTADA |
| M-04 | K45 (IG5-81 a IG5-84, IG5-96, IS-16, IE-09, IE-12) | válido (K45 APRUEBA) | La atribución de brief referencia la columna promotion_snapshot_id del evento | rechazo por K45 | RECHAZADA por K45 | DETECTADA |
| M-05 | K45 (IG5-81 a IG5-84, IG5-96, IS-16, IE-09, IE-12) | válido (K45 APRUEBA) | La columna de actor de la atribución pasa de contributor_id a created_by | rechazo por K45 | RECHAZADA por K45 | DETECTADA |
| M-06 | K45 (IG5-81 a IG5-84, IG5-96, IS-16, IE-09, IE-12) | válido (K45 APRUEBA) | La FK de procedencia al arte pierde copy_version_id | rechazo por K45 | RECHAZADA por K45 | DETECTADA |
| M-07 | K44 (IG5-80, IE-09) | válido (K44 APRUEBA) | La FK de procedencia al arte pierde organization_id | rechazo por K44 | RECHAZADA por K44 | DETECTADA |
| M-08 | K45 (IG5-81 a IG5-84, IG5-96, IS-16, IE-09, IE-12) | válido (K45 APRUEBA) | La cadena de brief_versions pierde brief_id | rechazo por K45 | RECHAZADA por K45 | DETECTADA |
| M-09 | K45 (IG5-81 a IG5-84, IG5-96, IS-16, IE-09, IE-12) | válido (K45 APRUEBA) | La cadena de promotion_snapshots pierde promotion_line_id | rechazo por K45 | RECHAZADA por K45 | DETECTADA |
| M-10 | K45 (IG5-81 a IG5-84, IG5-96, IS-16, IE-09, IE-12) | válido (K45 APRUEBA) | Se elimina de brief_field_attributions la restricción que exige previous_attribution_id en las heredadas | rechazo por K45 | RECHAZADA por K45 | DETECTADA |
| M-11 | K46 (IG5-92, IG5-93, IG5-95, IE-12) | válido (K46 APRUEBA) | Se elimina la restricción resolved_by <> affected_contributor_id | rechazo por K46 | RECHAZADA por K46 | DETECTADA |
| M-12 | K46 (IG5-92, IG5-93, IG5-95, IE-12) | válido (K46 APRUEBA) | Se elimina la restricción resolved_by <> requested_by | rechazo por K46 | RECHAZADA por K46 | DETECTADA |
| M-13 | K46 (IG5-92, IG5-93, IG5-95, IE-12) | válido (K46 APRUEBA) | Se elimina la restricción de evidencia y motivo no vacíos | rechazo por K46 | RECHAZADA por K46 | DETECTADA |
| M-14 | K47 (IG5-72, IG5-90, IG5-91, IG5-97, IE-12) | válido (K47 APRUEBA) | En la tabla de cálculo de atribuciones la fila «sustituido» pasa las activas anteriores a históricas | rechazo por K47 | RECHAZADA por K47 | DETECTADA |
| M-23 | K46 (IG5-92, IG5-93, IG5-95, IE-12) | válido (K46 APRUEBA) | Se elimina de la resolución la restricción resolved_by <> change_actor_id | rechazo por K46 | RECHAZADA por K46 | DETECTADA |
| M-24 | K46 (IG5-92, IG5-93, IG5-95, IE-12) | válido (K46 APRUEBA) | Se elimina el trigger de elegibilidad del resolutor (R1 a R9) | rechazo por K46 | RECHAZADA por K46 | DETECTADA |
| M-25 | K46 (IG5-92, IG5-93, IG5-95, IE-12) | válido (K46 APRUEBA) | Se elimina la restricción evidence_attribution_id = atribución informada | rechazo por K46 | RECHAZADA por K46 | DETECTADA |
| M-15 | K02 (IE-08) | válido (K02 APRUEBA) | Se repite la fila de IG5-69 | rechazo por K02 | RECHAZADA por K02 | DETECTADA |
| M-16 | K06 (IE-08) | válido (K06 APRUEBA) | Se retira IG5-83 de todos los escenarios | rechazo por K06 | RECHAZADA por K06 | DETECTADA |
| M-17 | K05 (IE-08) | válido (K05 APRUEBA) | T-01 referencia IG5-999 | rechazo por K05 | RECHAZADA por K05 | DETECTADA |
| M-18 | K09 (IE-06) | válido (K09 APRUEBA) | Pruebas totales pasa a 1 | rechazo por K09 | RECHAZADA por K09 | DETECTADA |
| M-19 | K10 (IG5-56) | válido (K10 APRUEBA) | Se retira el término P de una aparición | rechazo por K10 | RECHAZADA por K10 | DETECTADA |
| M-20 | K12 (IG5-78) | válido (K12 APRUEBA) | BRIEF_CHAIN_INCONSISTENTE desaparece del contrato | rechazo por K12 | RECHAZADA por K12 | DETECTADA |
| M-21 | K16 (IE-08 (H-01 de la v4)) | válido (K16 APRUEBA) | La subfase 2.1 depende de promotion_snapshots (4.x) | rechazo por K16 | RECHAZADA por K16 | DETECTADA |
| FK01 | K32 (IG5-81, IG5-62) | válido (K32 APRUEBA) | Se retira del contrato la FK compuesta de source_asset_version_id hacia creative_assets | rechazo por K32 | RECHAZADA por K32 | DETECTADA |
| FK02 | K32 (IG5-81, IG5-62) | válido (K32 APRUEBA) | Se retira del contrato la FK compuesta de lineage_parent_asset_id hacia creative_assets | rechazo por K32 | RECHAZADA por K32 | DETECTADA |
| FK03 | K44 (IG5-80, IE-09) | válido (K44 APRUEBA) | La FK RS-01 pierde organization_id en las columnas locales y en las de destino | rechazo por K44 | RECHAZADA por K44 | DETECTADA |
| FK04 | K44 (IG5-80, IE-09) | válido (K44 APRUEBA) | En RS-01 se invierten las dos últimas columnas de destino | rechazo por K44 | RECHAZADA por K44 | DETECTADA |
| FK05 | K44 (IG5-80, IE-09) | válido (K44 APRUEBA) | Se elimina de contribution_events la clave única (organization_id, id, creative_asset_id, contributor_id) destino de RS-02 | rechazo por K44 | RECHAZADA por K44 | DETECTADA |
| FK06 | K44 (IG5-80, IE-09) | válido (K44 APRUEBA) | La columna source_attribution_relation de contribution_events pasa de text a uuid | rechazo por K44 | RECHAZADA por K44 | DETECTADA |
| FK07 | K32 (IG5-81, IG5-62) | válido (K32 APRUEBA) | Se retira la FK RS-02 de source_upload_event_id | rechazo por K32 | RECHAZADA por K32 | DETECTADA |
| FK08 | K32 (IG5-81, IG5-62) | válido (K32 APRUEBA) | Se retira la FK RS-03 de source_attribution_id | rechazo por K32 | RECHAZADA por K32 | DETECTADA |
| FK09 | K44 (IG5-80, IE-09) | válido (K44 APRUEBA) | La FK diferida RS-06 pierde organization_id | rechazo por K44 | RECHAZADA por K44 | DETECTADA |
| FK10 | K32 (IG5-81, IG5-62) | válido (K32 APRUEBA) | RS-01 deja de incluir source_asset_id y asset_lineage_id | rechazo por K32 | RECHAZADA por K32 | DETECTADA |
| FK11 | K45 (IG5-81 a IG5-84, IG5-96, IS-16, IE-09, IE-12) | válido (K45 APRUEBA) | En RS-01 source_asset_id y source_asset_version_id cambian de posición | rechazo por K45 | RECHAZADA por K45 | DETECTADA |
| FK12 | K45 (IG5-81 a IG5-84, IG5-96, IS-16, IE-09, IE-12) | válido (K45 APRUEBA) | En RS-03 source_uploader_id y source_upload_event_id cambian de posición | rechazo por K45 | RECHAZADA por K45 | DETECTADA |
| FK13 | K32 (IG5-81, IG5-62) | válido (K32 APRUEBA) | RS-01 pasa de ON DELETE RESTRICT a ON DELETE SET NULL | rechazo por K32 | RECHAZADA por K32 | DETECTADA |
| FK14 | K32 (IG5-81, IG5-62) | válido (K32 APRUEBA) | La excepción source_asset_version (entero) pierde la referencia a K45 | rechazo por K32 | RECHAZADA por K32 | DETECTADA |
| FK15 | K45 (IG5-81 a IG5-84, IG5-96, IS-16, IE-09, IE-12) | válido (K45 APRUEBA) | La prueba negativa de la excepción referencia K47-A99 | rechazo por K45 | RECHAZADA por K45 | DETECTADA |
| FK16 | K32 (IG5-81, IG5-62) | válido (K32 APRUEBA) | Se retira del contrato la FK compuesta RS-05 (reused_from_asset_id y raíz) | rechazo por K32 | RECHAZADA por K32 | DETECTADA |
| FK17 | K32 (IG5-81, IG5-62) | válido (K32 APRUEBA) | Se retira del contrato la FK diferida RS-06 | rechazo por K32 | RECHAZADA por K32 | DETECTADA |
| FK18 | K32 (IG5-81, IG5-62) | válido (K32 APRUEBA) | Se retira del contrato la FK RS-07 del evento de reutilización | rechazo por K32 | RECHAZADA por K32 | DETECTADA |
| FK19 | K32 (IG5-81, IG5-62) | válido (K32 APRUEBA) | Se retira del contrato la FK RS-08 (evento de carga de origen = upload_event_id de la raíz) | rechazo por K32 | RECHAZADA por K32 | DETECTADA |
| FK20 | K32 (IG5-81, IG5-62) | válido (K32 APRUEBA) | RS-02 pierde source_uploader_id y contributor_id | rechazo por K32 | RECHAZADA por K32 | DETECTADA |
| FK21 | K32 (IG5-81, IG5-62) | válido (K32 APRUEBA) | RS-03 pierde source_attribution_relation y relation | rechazo por K32 | RECHAZADA por K32 | DETECTADA |
| FK22 | K32 (IG5-81, IG5-62) | válido (K32 APRUEBA) | RS-03 pierde source_root_asset_version_id y origin_asset_id | rechazo por K32 | RECHAZADA por K32 | DETECTADA |
| FK23 | K44 (IG5-80, IE-09) | válido (K44 APRUEBA) | En RS-08 se invierten id y upload_event_id en el destino | rechazo por K44 | RECHAZADA por K44 | DETECTADA |
| FK24 | K44 (IG5-80, IE-09) | válido (K44 APRUEBA) | Se elimina de creative_assets la clave única (organization_id, id, root_asset_version_id) | rechazo por K44 | RECHAZADA por K44 | DETECTADA |
| FK25 | K44 (IG5-80, IE-09) | válido (K44 APRUEBA) | Se elimina de creative_assets la clave única (organization_id, id, upload_event_id) | rechazo por K44 | RECHAZADA por K44 | DETECTADA |
| FK26 | K44 (IG5-80, IE-09) | válido (K44 APRUEBA) | RS-02 pierde organization_id en origen y destino | rechazo por K44 | RECHAZADA por K44 | DETECTADA |
| FK27 | K32 (IG5-81, IG5-62) | válido (K32 APRUEBA) | RS-07 pierde piece_id y copy_version_piece_id | rechazo por K32 | RECHAZADA por K32 | DETECTADA |
| FK28 | K32 (IG5-81, IG5-62) | válido (K32 APRUEBA) | RS-06 pierde copy_version_id y asset_copy_version_id | rechazo por K32 | RECHAZADA por K32 | DETECTADA |
| FK29 | K32 (IG5-81, IG5-62) | válido (K32 APRUEBA) | RS-05 usa lineage_parent_asset_id en lugar de reused_from_asset_id | rechazo por K32 | RECHAZADA por K32 | DETECTADA |
| FK30 | K32 (IG5-81, IG5-62) | válido (K32 APRUEBA) | RS-07 usa previous_asset_id en lugar de reused_from_asset_id | rechazo por K32 | RECHAZADA por K32 | DETECTADA |
| FK31 | K32 (IG5-81, IG5-62) | válido (K32 APRUEBA) | RS-06 usa reuse_event_id en lugar de upload_event_id | rechazo por K32 | RECHAZADA por K32 | DETECTADA |
| FK32 | K45 (IG5-81 a IG5-84, IG5-96, IS-16, IE-09, IE-12) | válido (K45 APRUEBA) | RS-02 intercambia source_upload_event_id y source_uploader_id | rechazo por K45 | RECHAZADA por K45 | DETECTADA |
| FK33 | K45 (IG5-81 a IG5-84, IG5-96, IS-16, IE-09, IE-12) | válido (K45 APRUEBA) | RS-03 intercambia source_attribution_id y source_uploader_id | rechazo por K45 | RECHAZADA por K45 | DETECTADA |
| FK34 | K32 (IG5-81, IG5-62) | válido (K32 APRUEBA) | RS-03 apunta a brief_field_attributions | rechazo por K32 | RECHAZADA por K32 | DETECTADA |
| FK35 | K32 (IG5-81, IG5-62) | válido (K32 APRUEBA) | RS-02 pasa de ON DELETE RESTRICT a ON DELETE CASCADE | rechazo por K32 | RECHAZADA por K32 | DETECTADA |
| FK36 | K32 (IG5-81, IG5-62) | válido (K32 APRUEBA) | RS-01 agrega ON UPDATE CASCADE | rechazo por K32 | RECHAZADA por K32 | DETECTADA |
| FK37 | K44 (IG5-80, IE-09) | válido (K44 APRUEBA) | En la reutilización, el paso 2 referencia un registro del paso 2 | rechazo por K44 | RECHAZADA por K44 | DETECTADA |
| FK38 | K32 (IG5-81, IG5-62) | válido (K32 APRUEBA) | RS-05 pasa a DEFERRABLE INITIALLY DEFERRED sin ciclo de filas | rechazo por K32 | RECHAZADA por K32 | DETECTADA |
| FK39 | K32 (IG5-81, IG5-62) | válido (K32 APRUEBA) | La excepción pierde el mecanismo alternativo | rechazo por K32 | RECHAZADA por K32 | DETECTADA |
| FK40 | K45 (IG5-81 a IG5-84, IG5-96, IS-16, IE-09, IE-12) | válido (K45 APRUEBA) | La excepción pierde la prueba negativa | rechazo por K45 | RECHAZADA por K45 | DETECTADA |
| FK41 | K32 (IG5-81, IG5-62) | válido (K32 APRUEBA) | Se elimina unique(organization_id, reuse_event_id) de creative_assets | rechazo por K32 | RECHAZADA por K32 | DETECTADA |
| K57-D01 | K57 (IG5-110, IG5-109) | válido (K57 APRUEBA) | La regla IG5-104 cita `Motor.reconstruir_cadena_inexistente` | rechazo por K57 | RECHAZADA por K57 | DETECTADA |
| K57-D02 | K57 (IG5-110, IG5-109) | válido (K57 APRUEBA) | La regla IG5-104 cita CHAIN-25 | rechazo por K57 | RECHAZADA por K57 | DETECTADA |
| K57-D03 | K57 (IG5-110, IG5-109) | válido (K57 APRUEBA) | D-05 pierde su verificación independiente | rechazo por K57 | RECHAZADA por K57 | DETECTADA |
| K57-D04 | K57 (IG5-110, IG5-109) | válido (K57 APRUEBA) | Se elimina el paso 14 del orden de validación | rechazo por K57 | RECHAZADA por K57 | DETECTADA |
| K57-D05 | K57 (IG5-110, IG5-109) | válido (K57 APRUEBA) | CHAIN: 24 pasa a CHAIN: 23 | rechazo por K57 | RECHAZADA por K57 | DETECTADA |
| K57-D06 | K57 (IG5-110, IG5-109) | válido (K57 APRUEBA) | La matriz del documento muestra NO donde el cálculo da sí | rechazo por K57 | RECHAZADA por K57 | DETECTADA |
| K57-D07 | K55 (IG5-102, IG5-103, IE-12) | válido (K55 APRUEBA) | RS-08 cita CHAIN-99 | rechazo por K55 | RECHAZADA por K55 | DETECTADA |
| K57-D08 | K57 (IG5-110, IG5-109) | válido (K57 APRUEBA) | Se elimina la fila D-12 | rechazo por K57 | RECHAZADA por K57 | DETECTADA |
| K57-D09 | K58 (IG5-116) | válido (K58 APRUEBA) | La fila K55-V12 de la equivalencia vuelve a llamarse K55 | rechazo por K58 | RECHAZADA por K58 | DETECTADA |
| K57-D10 | K57 (IG5-110, IG5-109) | válido (K57 APRUEBA) | Se elimina la fila AV-08 de la tabla de asset_version | rechazo por K57 | RECHAZADA por K57 | DETECTADA |
| K57-D11 | K57 (IG5-110, IG5-109) | válido (K57 APRUEBA) | Se elimina la validación de asset_version del evento propio | rechazo por K57 | RECHAZADA por K57 | DETECTADA |
| K57-D12 | K57 (IG5-110, IG5-109) | válido (K57 APRUEBA) | AV: 8 pasa a AV: 7 | rechazo por K57 | RECHAZADA por K57 | DETECTADA |
| K46-M01 | IG5-95 (R_R3) | válido: resolución aceptada por R, 2 elegibles | el resolutor es el contribuyente afectado | rechazo con R_R3; la atribución permanece activa | rechazada con R_R2, R_R3, R_R6, R_R7; atribución activa | DETECTADA |
| K46-M02 | IG5-95 (R_R4) | válido: resolución aceptada por R, 2 elegibles | el resolutor es el solicitante | rechazo con R_R4; la atribución permanece activa | rechazada con R_R4; atribución activa | DETECTADA |
| K46-M03 | IG5-95 (R_R5) | válido: resolución aceptada por R, 2 elegibles | el resolutor es el editor que ejecutó la sustitución | rechazo con R_R5; la atribución permanece activa | rechazada con R_R5, R_R6, R_R7, R_R9; atribución activa | DETECTADA |
| K46-M04 | IG5-95 (R_R6) | válido: resolución aceptada por R, 2 elegibles | el resolutor contribuyó al mismo campo en una versión anterior | rechazo con R_R6; la atribución permanece activa | rechazada con R_R6; atribución activa | DETECTADA |
| K46-M05 | IG5-95 (R_R7) | válido: resolución aceptada por R, 2 elegibles | el resolutor heredó una contribución activa | rechazo con R_R7; la atribución permanece activa | rechazada con R_R7, R_R9; atribución activa | DETECTADA |
| K46-M06 | IG5-95 (R_R8) | válido: resolución aceptada por R, 2 elegibles | el resolutor es contribuyente de otra fuente de la cadena | rechazo con R_R8; la atribución permanece activa | rechazada con R_R8; atribución activa | DETECTADA |
| K46-M07 | IG5-95 (R_R1) | válido: resolución aceptada por R, 2 elegibles | el resolutor no pertenece a la organización | rechazo con R_R1; la atribución permanece activa | rechazada con R_R1; atribución activa | DETECTADA |
| K46-M08 | IG5-95 (R_R2) | válido: resolución aceptada por R, 2 elegibles | el resolutor no tiene piece.review | rechazo con R_R2; la atribución permanece activa | rechazada con R_R2; atribución activa | DETECTADA |
| K46-M09 | IG5-95 (EVIDENCIA_VACIA) | válido: resolución aceptada por R, 2 elegibles | la evidencia está vacía | rechazo con EVIDENCIA_VACIA; la atribución permanece activa | rechazada con EVIDENCIA_VACIA; atribución activa | DETECTADA |
| K46-M10 | IG5-95 (EVIDENCIA_OTRA_ATRIBUCION) | válido: resolución aceptada por R, 2 elegibles | la evidencia apunta a otra atribución o versión | rechazo con EVIDENCIA_OTRA_ATRIBUCION; la atribución permanece activa | rechazada con EVIDENCIA_OTRA_ATRIBUCION, EVIDENCIA_OTRA_VERSION; atribución activa | DETECTADA |
| K46-M11 | IG5-95 (ACTOR_NO_AUTENTICADO) | válido: resolución aceptada por R, 2 elegibles | el actor de la resolución no coincide con la identidad autenticada | rechazo con ACTOR_NO_AUTENTICADO; la atribución permanece activa | rechazada con ACTOR_NO_AUTENTICADO; atribución activa | DETECTADA |
| K46-M12 | IG5-95 (SIN_RESOLUTOR_ELEGIBLE) | válido: resolución aceptada por R, 2 elegibles | no existe ningún resolutor elegible | rechazo con SIN_RESOLUTOR_ELEGIBLE; la atribución permanece activa | rechazada con R_R2, SIN_RESOLUTOR_ELEGIBLE; atribución activa | DETECTADA |
| K45-M01 | IG5-96 (C04) | válido: modelo relacional con 6 eventos y 9 atribuciones, 0 violaciones | brief_editor con origen de promoción | rechazo con C04 | rechazado con C04, C08 | DETECTADA |
| K45-M02 | IG5-96 (C04) | válido: modelo relacional con 6 eventos y 9 atribuciones, 0 violaciones | promotion_editor con origen de brief | rechazo con C04 | rechazado con C04, C08 | DETECTADA |
| K45-M03 | IG5-96 (C04) | válido: modelo relacional con 6 eventos y 9 atribuciones, 0 violaciones | copy_editor con origen de asset | rechazo con C04 | rechazado con C04, C12 | DETECTADA |
| K45-M04 | IG5-96 (C04) | válido: modelo relacional con 6 eventos y 9 atribuciones, 0 violaciones | asset_uploader con origen de copy | rechazo con C04 | rechazado con C04, C13 | DETECTADA |
| K45-M05 | IG5-96 (C07) | válido: modelo relacional con 6 eventos y 9 atribuciones, 0 violaciones | actor del evento distinto del actor de la atribución | rechazo con C07 | rechazado con C07 | DETECTADA |
| K45-M06 | IG5-96 (C01) | válido: modelo relacional con 6 eventos y 9 atribuciones, 0 violaciones | evento de otra organización | rechazo con C01 | rechazado con C01 | DETECTADA |
| K45-M07 | IG5-96 (C02) | válido: modelo relacional con 6 eventos y 9 atribuciones, 0 violaciones | evento de otra pieza | rechazo con C02 | rechazado con C02, C03 | DETECTADA |
| K45-M08 | IG5-96 (C08) | válido: modelo relacional con 6 eventos y 9 atribuciones, 0 violaciones | versión de origen de la atribución distinta de la del evento | rechazo con C08 | rechazado con C08 | DETECTADA |
| K45-M09 | IG5-96 (C09) | válido: modelo relacional con 6 eventos y 9 atribuciones, 0 violaciones | campo material inexistente en la versión | rechazo con C09 | rechazado con C09, C10 | DETECTADA |
| K45-M10 | IG5-96 (C04) | válido: modelo relacional con 6 eventos y 9 atribuciones, 0 violaciones | atribución de brief que referencia un evento de promoción | rechazo con C04 | rechazado con C04, C08, C09, C10 | DETECTADA |
| K45-M11 | IG5-96 (C14) | válido: modelo relacional con 6 eventos y 9 atribuciones, 0 violaciones | reutilizador registrado como uploader original | rechazo con C14 | rechazado con C08, C10, C13, C14 | DETECTADA |
| K45-M12 | IG5-96 (C10) | válido: modelo relacional con 6 eventos y 9 atribuciones, 0 violaciones | procedencia heredada sin versión de origen | rechazo con C10 | rechazado con C08, C10 | DETECTADA |
| K45-M13 | IG5-96 (C03) | válido: modelo relacional con 6 eventos y 9 atribuciones, 0 violaciones | evento cuya versión de origen no existe | rechazo con C03 | rechazado con C03, C08 | DETECTADA |
| K45-M14 | IG5-96 (C04) | válido: modelo relacional con 6 eventos y 9 atribuciones, 0 violaciones | combinación inherited_contributor con origen de asset no permitida | rechazo con C04 | rechazado con C04, C10 | DETECTADA |
| K45-M15 | IG5-96 (C03) | válido: modelo relacional con 6 eventos y 9 atribuciones, 0 violaciones | evento y atribución declaran P2 pero la versión física de copy pertenece a P1 | rechazo con C03 | rechazado con C02, C03, C11 | DETECTADA |
| K45-M16 | IG5-96 (C03) | válido: modelo relacional con 6 eventos y 9 atribuciones, 0 violaciones | evento de brief apunta a una versión de brief de otra pieza | rechazo con C03 | rechazado con C03, C08 | DETECTADA |
| K45-M17 | IG5-96 (C02) | válido: modelo relacional con 6 eventos y 9 atribuciones, 0 violaciones | atribución de promoción apunta a un snapshot de otra pieza | rechazo con C02 | rechazado con C02, C08 | DETECTADA |
| K45-M18 | IG5-96 (C02) | válido: modelo relacional con 6 eventos y 9 atribuciones, 0 violaciones | atribución de asset declara una pieza distinta a la del copy que usa el arte | rechazo con C02 | rechazado con C02, C11, C13 | DETECTADA |
| K45-M19 | IG5-96 (C13) | válido: modelo relacional con 6 eventos y 9 atribuciones, 0 violaciones | asset reutilizado vinculado a una versión de copy distinta de la que declara la atribución | rechazo con C13 | rechazado con C13 | DETECTADA |
| K45-M20 | IG5-96 (C01) | válido: modelo relacional con 6 eventos y 9 atribuciones, 0 violaciones | evento de asset uploader de otra organización aunque el asset reutilizado es válido | rechazo con C01 | rechazado con C01 | DETECTADA |
| K45-M21 | IG5-96 (C11) | válido: modelo relacional con 6 eventos y 9 atribuciones, 0 violaciones | atribución heredada con origen válido pero relación de herencia hacia otra cadena | rechazo con C11 | rechazado con C10, C11 | DETECTADA |
| K45-M22 | IG5-96 (C08) | válido: modelo relacional con 6 eventos y 9 atribuciones, 0 violaciones | cambia la versión física de origen del evento manteniendo ids aparentemente válidos | rechazo con C08 | rechazado con C08 | DETECTADA |
| K45-M23 | IG5-96 (C05) | válido: modelo relacional con 6 eventos y 9 atribuciones, 0 violaciones | origin_kind brief con la columna tipada de copy | rechazo con C05 | rechazado con C05, C06, C08 | DETECTADA |
| K45-M24 | IG5-96 (C06) | válido: modelo relacional con 6 eventos y 9 atribuciones, 0 violaciones | copy_version_id apunta al identificador de un asset | rechazo con C06 | rechazado con C06, C08 | DETECTADA |
| K45-M25 | IG5-96 (C12) | válido: modelo relacional con 6 eventos y 9 atribuciones, 0 violaciones | el asset original lo cargó una persona distinta del actor del evento | rechazo con C12 | rechazado con C12 | DETECTADA |
| K45-M26 | IG5-96 (C15) | válido: modelo relacional con 6 eventos y 9 atribuciones, 0 violaciones | versión de copy de P1 referencia una versión de brief de otra organización | rechazo con C15 | rechazado con C15 | DETECTADA |
| K45-M27 | IG5-96 (C13) | válido: modelo relacional con 6 eventos y 9 atribuciones, 0 violaciones | la atribución de asset reutilizado usa un asset de la misma versión cuya cadena de reutilización no llega al asset del evento | rechazo con C13 | rechazado con C13 | DETECTADA |
| K47-M01 | IG5-97 (I1) | válido: escenario ejecutado sobre el motor, 0 violaciones del auditor | sustituir_campo retira automáticamente la atribución anterior | violación I1 | detectada por I1, I15 · «una atribución activa anterior no sigue activa en la versión nueva: [('A', 'copy', 'headline', 'e1')]» | DETECTADA |
| K47-M02 | IG5-97 (I1) | válido: escenario ejecutado sobre el motor, 0 violaciones del auditor | eliminar_campo retira automáticamente la atribución anterior | violación I1 | detectada por I1, I15 · «una atribución activa anterior no sigue activa en la versión nueva: [('A', 'copy', 'headline', 'e1')]» | DETECTADA |
| K47-M03 | IG5-97 (I1) | válido: escenario ejecutado sobre el motor, 0 violaciones del auditor | modificar_campo pierde una atribución previa | violación I1 | detectada por I1, I15 · «una atribución activa anterior no sigue activa en la versión nueva: [('A', 'copy', 'headline', 'e1')]» | DETECTADA |
| K47-M04 | IG5-97 (I2) | válido: escenario ejecutado sobre el motor, 0 violaciones del auditor | introducir_campo no incorpora al actor | violación I2 | detectada por I2 · «el actor no se incorporó» | DETECTADA |
| K47-M05 | IG5-97 (I5) | válido: escenario ejecutado sobre el motor, 0 violaciones del auditor | el cálculo de E excluye a la persona afectada por una resolución rechazada | violación I5 | detectada por I5, I7 · «una resolución rechazada o inválida modificó atribuciones o E» | DETECTADA |
| K47-M06 | IG5-97 (I3) | válido: escenario ejecutado sobre el motor, 0 violaciones del auditor | la resolución aceptada retira otra atribución distinta | violación I3 | detectada por I15, I3, I7 · «la resolución retiró ['t3', 't5'] en lugar de solo la referenciada» | DETECTADA |
| K47-M07 | IG5-97 (I10) | válido: escenario ejecutado sobre el motor, 0 violaciones del auditor | la resolución aceptada altera una versión histórica | violación I10 | detectada por I10 · «una versión, atribución, evento o estado anterior fue modificado o eliminado» | DETECTADA |
| K47-M08 | IG5-97 (I10) | válido: escenario ejecutado sobre el motor, 0 violaciones del auditor | crear_version omite una atribución heredada | violación I10 | detectada por I1, I10 · «la versión nueva no hereda todas las atribuciones activas» | DETECTADA |
| K47-M09 | IG5-97 (I8) | válido: escenario ejecutado sobre el motor, 0 violaciones del auditor | una cadena de copy incompleta se presenta como completa | violación I8 | detectada por I20, I8 · «procedencia incompleta presentada como completa o con E parcial» | DETECTADA |
| K47-M10 | IG5-97 (I7) | válido: escenario ejecutado sobre el motor, 0 violaciones del auditor | una resolución válida elimina de E a quien conserva otra atribución activa | violación I7 | detectada por I7 · «E del motor distinto del E recalculado sobre las atribuciones reales» | DETECTADA |
| K47-M11 | IG5-97 (I9) | válido: escenario ejecutado sobre el motor, 0 violaciones del auditor | la sustitución difiere entre copy y brief | violación I9 | detectada por I9 · «las fuentes no aplican la misma regla» | DETECTADA |
| K47-M12 | IG5-97 (I9) | válido: escenario ejecutado sobre el motor, 0 violaciones del auditor | la eliminación difiere entre brief y promoción | violación I9 | detectada por I9 · «las fuentes no aplican la misma regla» | DETECTADA |
| K47-M13 | IG5-97 (I11) | válido: escenario ejecutado sobre el motor, 0 violaciones del auditor | la similitud textual determina el descarte | violación I11 | detectada por I11 · «el resultado sobre las atribuciones depende de la similitud del texto» | DETECTADA |
| K47-M14 | IG5-97 (I12) | válido: escenario ejecutado sobre el motor, 0 violaciones del auditor | cambiar la clasificación retira atribuciones sin resolución | violación I12 | detectada por I12, I15 · «el cambio de clasificación alteró atribuciones o estados» | DETECTADA |
| K47-M15 | IG5-97 (I7) | válido: escenario ejecutado sobre el motor, 0 violaciones del auditor | resolución válida retira a quien conserva otra atribución activa en otro campo | violación I7 | detectada por I15, I3, I7 · «salió de E una persona que conserva otra atribución activa» | DETECTADA |
| K47-M16 | IG5-97 (I7) | válido: escenario ejecutado sobre el motor, 0 violaciones del auditor | resolución válida retira a quien conserva una contribución activa en otra fuente | violación I7 | detectada por I15, I3, I7 · «salió de E una persona que conserva otra atribución activa» | DETECTADA |
| K47-M17 | IG5-97 (I3) | válido: escenario ejecutado sobre el motor, 0 violaciones del auditor | resolver una atribución retira todas las atribuciones de la persona | violación I3 | detectada por I15, I3, I7 · «la resolución retiró ['t2', 't3', 't5'] en lugar de solo la referenciada» | DETECTADA |
| K47-M18 | IG5-97 (I5) | válido: escenario ejecutado sobre el motor, 0 violaciones del auditor | una resolución rechazada cambia el estado de una atribución | violación I5 | detectada por I15, I5 · «una resolución rechazada o inválida modificó atribuciones o E» | DETECTADA |
| K47-M19 | IG5-97 (I5) | válido: escenario ejecutado sobre el motor, 0 violaciones del auditor | una resolución con evidencia de otra versión modifica E | violación I5 | detectada por I4, I5 · «una resolución rechazada o inválida modificó atribuciones o E» | DETECTADA |
| K47-M20 | IG5-97 (I10) | válido: escenario ejecutado sobre el motor, 0 violaciones del auditor | crear_version omite una atribución heredada de segunda generación | violación I10 | detectada por I1, I10 · «la versión nueva no hereda todas las atribuciones activas» | DETECTADA |
| K47-M21 | IG5-97 (I6) | válido: escenario ejecutado sobre el motor, 0 violaciones del auditor | una atribución histórica desaparece de la evidencia | violación I6 | detectada por I10, I6 · «una atribución, un asset o un registro histórico desapareció de la evidencia» | DETECTADA |
| K47-M22 | IG5-97 (I8) | válido: escenario ejecutado sobre el motor, 0 violaciones del auditor | la cadena de brief está incompleta pero E aparece como completo | violación I8 | detectada por I8 · «procedencia incompleta presentada como completa o con E parcial» | DETECTADA |
| K47-M23 | IG5-97 (I8) | válido: escenario ejecutado sobre el motor, 0 violaciones del auditor | la cadena de promoción está incompleta pero E aparece como completo | violación I8 | detectada por I8 · «procedencia incompleta presentada como completa o con E parcial» | DETECTADA |
| K47-M24 | IG5-97 (I3) | válido: escenario ejecutado sobre el motor, 0 violaciones del auditor | la resolución retira un campo distinto del que declara | violación I3 | detectada por I15, I3, I6 · «la resolución retiró ['t7'] en lugar de solo la referenciada» | DETECTADA |
| K47-M25 | IG5-97 (I7) | válido: escenario ejecutado sobre el motor, 0 violaciones del auditor | quien contribuye a dos fuentes sale de E al resolver solo una | violación I7 | detectada por I7 · «E del motor distinto del E recalculado sobre las atribuciones reales» | DETECTADA |
| K47-M26 | IG5-97 (I10) | válido: escenario ejecutado sobre el motor, 0 violaciones del auditor | la resolución válida reescribe un registro anterior en lugar de agregar uno nuevo | violación I10 | detectada por I10 · «una versión, atribución, evento o estado anterior fue modificado o eliminado» | DETECTADA |
| K47-M27 | IG5-97 (I4) | válido: escenario ejecutado sobre el motor, 0 violaciones del auditor | se acepta una resolución cuyo resolutor incumple la independencia (R1 a R9 no se aplican) | violación I4 | detectada por I4, I5 · «una resolución aceptada incumple sus condiciones: ['R2', 'R5', 'R6']» | DETECTADA |
| K47-M28 | IG5-97 (I4) | válido: escenario ejecutado sobre el motor, 0 violaciones del auditor | el motor no evalúa la regla R1 del resolutor (membresía activa) | violación I4 | detectada por I4 · «los motivos de rechazo del motor ['R2'] difieren de los recalculados por el auditor ['R1', 'R2']» | DETECTADA |
| K47-M29 | IG5-97 (I4) | válido: escenario ejecutado sobre el motor, 0 violaciones del auditor | el motor no evalúa la regla R2 del resolutor (piece.review) | violación I4 | detectada por I4, I5 · «una resolución aceptada incumple sus condiciones: ['R2']» | DETECTADA |
| K47-M30 | IG5-97 (I4) | válido: escenario ejecutado sobre el motor, 0 violaciones del auditor | el motor no evalúa la regla R3 del resolutor (afectado) | violación I4 | detectada por I4 · «los motivos de rechazo del motor ['R2', 'R6', 'R7', 'R9'] difieren de los recalculados por el auditor ['R2', '» | DETECTADA |
| K47-M31 | IG5-97 (I4) | válido: escenario ejecutado sobre el motor, 0 violaciones del auditor | el motor no evalúa la regla R4 del resolutor (solicitante) | violación I4 | detectada por I4, I5 · «una resolución aceptada incumple sus condiciones: ['R4']» | DETECTADA |
| K47-M32 | IG5-97 (I4) | válido: escenario ejecutado sobre el motor, 0 violaciones del auditor | el motor no evalúa la regla R5 del resolutor (actor del cambio) | violación I4 | detectada por I4 · «los motivos de rechazo del motor ['R2', 'R6', 'R9'] difieren de los recalculados por el auditor ['R2', 'R5', '» | DETECTADA |
| K47-M33 | IG5-97 (I4) | válido: escenario ejecutado sobre el motor, 0 violaciones del auditor | el motor no evalúa la regla R6 del resolutor (contribuyente directo de la cadena) | violación I4 | detectada por I4 · «los motivos de rechazo del motor ['R7', 'R9'] difieren de los recalculados por el auditor ['R6', 'R7', 'R9']» | DETECTADA |
| K47-M34 | IG5-97 (I4) | válido: escenario ejecutado sobre el motor, 0 violaciones del auditor | el motor no evalúa la regla R7 del resolutor (contribuyente heredado activo) | violación I4 | detectada por I4 · «los motivos de rechazo del motor ['R6', 'R9'] difieren de los recalculados por el auditor ['R6', 'R7', 'R9']» | DETECTADA |
| K47-M35 | IG5-97 (I4) | válido: escenario ejecutado sobre el motor, 0 violaciones del auditor | el motor no evalúa la regla R8 del resolutor (contribuyente de otra fuente de la cadena) | violación I4 | detectada por I4, I5 · «una resolución aceptada incumple sus condiciones: ['R8']» | DETECTADA |
| K47-M36 | IG5-97 (I4) | válido: escenario ejecutado sobre el motor, 0 violaciones del auditor | el motor no evalúa la regla R9 del resolutor (beneficiario) | violación I4 | detectada por I4 · «los motivos de rechazo del motor ['R6', 'R7'] difieren de los recalculados por el auditor ['R6', 'R7', 'R9']» | DETECTADA |
| K47-R01 | IG5-98 (I13) | válido: escenario RS con tres resoluciones selladas y cadena de reconsideración, 0 violaciones | modificar el resultado de una resolución existente | violación I13 con la condición «resultado» | detectada por I13, I15 · «la resolución r2 fue modificada (campos: resultado, sello)» | DETECTADA |
| K47-R02 | IG5-98 (I13) | válido: escenario RS con tres resoluciones selladas y cadena de reconsideración, 0 violaciones | modificar la evidencia de una resolución existente | violación I13 con la condición «evidencia» | detectada por I13 · «la resolución r2 fue modificada (campos: evidencia, sello)» | DETECTADA |
| K47-R03 | IG5-98 (I13) | válido: escenario RS con tres resoluciones selladas y cadena de reconsideración, 0 violaciones | modificar el resolutor de una resolución existente | violación I13 con la condición «resolutor» | detectada por I13 · «la resolución r2 fue modificada (campos: auth_uid, resolutor, sello)» | DETECTADA |
| K47-R04 | IG5-98 (I13) | válido: escenario RS con tres resoluciones selladas y cadena de reconsideración, 0 violaciones | modificar el solicitante de una resolución existente | violación I13 con la condición «solicitante» | detectada por I13 · «la resolución r2 fue modificada (campos: sello, solicitante)» | DETECTADA |
| K47-R05 | IG5-98 (I15) | válido: escenario RS con tres resoluciones selladas y cadena de reconsideración, 0 violaciones | cambiar la atribución afectada por una resolución | violación I15 con la condición «no corresponde» | detectada por I13, I14, I15 · «la baja de t3 cita la resolución r2, que no existe, no fue aceptada o no corresponde a esa atribución» | DETECTADA |
| K47-R06 | IG5-98 (I13) | válido: escenario RS con tres resoluciones selladas y cadena de reconsideración, 0 violaciones | cambiar la versión afectada por una resolución | violación I13 con la condición «version_evidencia» | detectada por I13 · «la resolución r2 fue modificada (campos: sello, version_evidencia)» | DETECTADA |
| K47-R07 | IG5-98 (I13) | válido: escenario RS con tres resoluciones selladas y cadena de reconsideración, 0 violaciones | eliminar una resolución histórica | violación I13 con la condición «eliminada» | detectada por I13, I14 · «la resolución histórica r1 fue eliminada» | DETECTADA |
| K47-R08 | IG5-98 (I13) | válido: escenario RS con tres resoluciones selladas y cadena de reconsideración, 0 violaciones | reemplazar una resolución usando el mismo ID | violación I13 con la condición «reemplazada con el mismo ID» | detectada por I13, I14, I15 · «la resolución r1 fue reemplazada con el mismo ID (campos: auth_uid, evidencia, resolutor, resultado, sello, se» | DETECTADA |
| K47-R09 | IG5-98 (I15) | válido: escenario RS con tres resoluciones selladas y cadena de reconsideración, 0 violaciones | convertir una resolución rechazada en aceptada | violación I15 con la condición «aceptada» | detectada por I15, I3, I6 · «la resolución aceptada r3 no tiene exactamente una baja registrada para su atribución» | DETECTADA |
| K47-R10 | IG5-98 (I15) | válido: escenario RS con tres resoluciones selladas y cadena de reconsideración, 0 violaciones | reutilizar una resolución aceptada para otra atribución | violación I15 con la condición «cita la resolución r2» | detectada por I15, I5 · «la baja de t9 cita la resolución r2, que no existe, no fue aceptada o no corresponde a esa atribución» | DETECTADA |
| K47-R11 | IG5-98 (I14) | válido: escenario RS con tres resoluciones selladas y cadena de reconsideración, 0 violaciones | alterar la cadena de reconsideraciones | violación I14 con la condición «otra atribución» | detectada por I13, I14 · «la cadena de r2 referencia un registro de otra atribución u organización» | DETECTADA |
| K47-R12 | IG5-98 (I14) | válido: escenario RS con tres resoluciones selladas y cadena de reconsideración, 0 violaciones | reescribir una resolución anterior para simular una decisión posterior | violación I14 con la condición «anterior fue alterado» | detectada por I13, I14, I15 · «el sello del registro anterior de r2 no coincide con el contenido actual (el anterior fue alterado)» | DETECTADA |
| K47-A01 | IG5-99 (I16) | válido: escenario de arte ejecutado sobre el motor, 0 violaciones del auditor | una versión usa un asset sin uploader | violación I16 con la condición «uploader» | detectada por I16, I23, I24 · «cv1: asset a1 sin uploader registrado» | DETECTADA |
| K47-A02 | IG5-99 (I16) | válido: escenario de arte ejecutado sobre el motor, 0 violaciones del auditor | una versión usa un asset sin evento de carga | violación I16 con la condición «evento de carga» | detectada por I16, I23 · «cv1: asset a1 sin evento de carga válido» | DETECTADA |
| K47-A03 | IG5-99 (I19) | válido: escenario de arte ejecutado sobre el motor, 0 violaciones del auditor | el asset pertenece a otra organización | violación I19 con la condición «organización» | detectada por I19, I24, I25, I27 · «ca: el asset a2 pertenece a otra organización» | DETECTADA |
| K47-A04 | IG5-99 (I19) | válido: escenario de arte ejecutado sobre el motor, 0 violaciones del auditor | el asset pertenece a otra pieza sin relación válida | violación I19 con la condición «pieza» | detectada por I19, I24, I25, I27 · «ca: el asset a2 pertenece a otra pieza sin relación válida» | DETECTADA |
| K47-A05 | IG5-99 (I18) | válido: escenario de arte ejecutado sobre el motor, 0 violaciones del auditor | la reutilización apunta a otra versión de copy | violación I18 con la condición «versión de copy» | detectada por I17, I18, I24, I25, I27 · «ca: el asset a2 no corresponde a esta versión de copy (cvm)» | DETECTADA |
| K47-A06 | IG5-99 (I17) | válido: escenario de arte ejecutado sobre el motor, 0 violaciones del auditor | el reutilizador sustituye al uploader original | violación I17 con la condición «uploader original» | detectada por I17, I26, I28 · «ca: el uploader original del asset a2 no coincide con el origen» | DETECTADA |
| K47-A07 | IG5-99 (I17) | válido: escenario de arte ejecutado sobre el motor, 0 violaciones del auditor | asset reutilizado sin evento de reutilización | violación I17 con la condición «evento de reutilización» | detectada por I17, I25 · «ca: asset a2 sin evento de reutilización válido» | DETECTADA |
| K47-A08 | IG5-99 (I19) | válido: escenario de arte ejecutado sobre el motor, 0 violaciones del auditor | asset heredado sin referencia al origen | violación I19 con la condición «sin referencia» | detectada por I19, I26, I27, I28 · «ca: asset reutilizado a2 sin referencia al origen» | DETECTADA |
| K47-A09 | IG5-99 (I19) | válido: escenario de arte ejecutado sobre el motor, 0 violaciones del auditor | la cadena de assets contiene un ciclo | violación I19 con la condición «ciclo» | detectada por I10, I17, I19, I27, I28 · «ca: ciclo en la cadena de assets a2 → a1 → a2» | DETECTADA |
| K47-A10 | IG5-99 (I19) | válido: escenario de arte ejecutado sobre el motor, 0 violaciones del auditor | el asset de origen no existe | violación I19 con la condición «inexistente» | detectada por I19, I26, I27, I28 · «ca: asset de origen a_x inexistente» | DETECTADA |
| K47-A11 | IG5-99 (I1) | válido: escenario de arte ejecutado sobre el motor, 0 violaciones del auditor | un asset modificado pierde la atribución anterior | violación I1 con la condición «retiró» | detectada por I1, I15 · «una operación de contenido retiró atribuciones» | DETECTADA |
| K47-A12 | IG5-99 (I1) | válido: escenario de arte ejecutado sobre el motor, 0 violaciones del auditor | un asset sustituido elimina la atribución anterior automáticamente | violación I1 con la condición «retiró» | detectada por I1, I15 · «una operación de contenido retiró atribuciones» | DETECTADA |
| K47-A13 | IG5-99 (I6) | válido: escenario de arte ejecutado sobre el motor, 0 violaciones del auditor | un asset eliminado borra su historial | violación I6 con la condición «desapareció» | detectada por I1, I10, I19, I28, I6 · «una atribución, un asset o un registro histórico desapareció de la evidencia» | DETECTADA |
| K47-A14 | IG5-99 (I20) | válido: escenario de arte ejecutado sobre el motor, 0 violaciones del auditor | un arte incompleto permite declarar E completo | violación I20 con la condición «arte» | detectada por I16, I20, I23, I24, I8 · «la procedencia del arte es incompleta pero el motor declara E completo: cv1: asset a1 sin uploader registrado» | DETECTADA |
| K47-A15 | IG5-99 (I21) | válido: escenario de arte ejecutado sobre el motor, 0 violaciones del auditor | el cálculo de E omite a los contribuyentes del arte | violación I21 con la condición «omite» | detectada por I21, I7 · «E omite a un contribuyente del arte: ['U']» | DETECTADA |
| K47-A16 | IG5-99 (I20) | válido: escenario de arte ejecutado sobre el motor, 0 violaciones del auditor | la ausencia de registros de arte se acepta como no_aplica | violación I20 con la condición «no declara» | detectada por I20, I8 · «la procedencia del arte es incompleta pero el motor declara E completo: cv2: la versión no declara el estado d» | DETECTADA |
| K47-A17 | IG5-100 (I22) | válido: escenario de arte ejecutado sobre el motor, 0 violaciones del auditor | el uploader pertenece a otra organización | violación I22 con la condición «otra organización»; procedencia incompleta y E no completo | detectada por I22 · «cv1: el uploader U de a1 pertenece a otra organización»; E bloqueado | DETECTADA |
| K47-A18 | IG5-100 (I22) | válido: escenario de arte ejecutado sobre el motor, 0 violaciones del auditor | el uploader tiene membresía inactiva | violación I22 con la condición «membresía inactiva»; procedencia incompleta y E no completo | detectada por I22 · «cv1: el uploader U de a1 tiene membresía inactiva»; E bloqueado | DETECTADA |
| K47-A19 | IG5-100 (I23) | válido: escenario de arte ejecutado sobre el motor, 0 violaciones del auditor | el evento de carga pertenece a otra organización | violación I23 con la condición «otra organización»; procedencia incompleta y E no completo | detectada por I23 · «cv1: el evento de carga de a1 pertenece a otra organización»; E bloqueado | DETECTADA |
| K47-A20 | IG5-100 (I23) | válido: escenario de arte ejecutado sobre el motor, 0 violaciones del auditor | el evento de carga pertenece a otra pieza | violación I23 con la condición «otra pieza»; procedencia incompleta y E no completo | detectada por I23 · «cv1: el evento de carga de a1 pertenece a otra pieza»; E bloqueado | DETECTADA |
| K47-A21 | IG5-100 (I23) | válido: escenario de arte ejecutado sobre el motor, 0 violaciones del auditor | el evento de carga corresponde a otra versión del asset | violación I23 con la condición «otra versión del asset»; procedencia incompleta y E no completo | detectada por I23 · «cv2: el evento de carga de a1b corresponde a otra versión del asset»; E bloqueado | DETECTADA |
| K47-A22 | IG5-100 (I23) | válido: escenario de arte ejecutado sobre el motor, 0 violaciones del auditor | el actor del evento de carga no es el uploader | violación I23 con la condición «no es el uploader»; procedencia incompleta y E no completo | detectada por I16, I23 · «cv1: el actor del evento de carga de a1 no es el uploader»; E bloqueado | DETECTADA |
| K47-A23 | IG5-100 (I24) | válido: escenario de arte ejecutado sobre el motor, 0 violaciones del auditor | la atribución directa corresponde a otra versión de copy | violación I24 con la condición «versión de copy»; procedencia incompleta y E no completo | detectada por I10, I18, I19, I24, I27 · «ca: la atribución directa del uploader de a1 no corresponde a la versión de copy, pieza u organización exactas»; E bloqueado | DETECTADA |
| K47-A24 | IG5-100 (I24) | válido: escenario de arte ejecutado sobre el motor, 0 violaciones del auditor | la atribución directa corresponde a otra pieza | violación I24 con la condición «pieza»; procedencia incompleta y E no completo | detectada por I10, I24, I27 · «ca: la atribución directa del uploader de a1 no corresponde a la versión de copy, pieza u organización exactas»; E bloqueado | DETECTADA |
| K47-A25 | IG5-100 (I24) | válido: escenario de arte ejecutado sobre el motor, 0 violaciones del auditor | la atribución directa corresponde a otra organización | violación I24 con la condición «organización»; procedencia incompleta y E no completo | detectada por I10, I24, I26, I27 · «ca: la atribución directa del uploader de a1 no corresponde a la versión de copy, pieza u organización exactas»; E bloqueado | DETECTADA |
| K47-A26 | IG5-100 (I25) | válido: escenario de arte ejecutado sobre el motor, 0 violaciones del auditor | el evento de reutilización pertenece a otra organización | violación I25 con la condición «otra organización»; procedencia incompleta y E no completo | detectada por I25, I27 · «ca: el evento de reutilización de a2 pertenece a otra organización»; E bloqueado | DETECTADA |
| K47-A27 | IG5-100 (I25) | válido: escenario de arte ejecutado sobre el motor, 0 violaciones del auditor | el evento de reutilización pertenece a otra pieza | violación I25 con la condición «otra pieza»; procedencia incompleta y E no completo | detectada por I25, I27 · «ca: el evento de reutilización de a2 pertenece a otra pieza»; E bloqueado | DETECTADA |
| K47-A28 | IG5-100 (I25) | válido: escenario de arte ejecutado sobre el motor, 0 violaciones del auditor | el evento de reutilización identifica a otro actor | violación I25 con la condición «otro actor»; procedencia incompleta y E no completo | detectada por I17, I25, I27 · «ca: el evento de reutilización de a2 identifica a otro actor»; E bloqueado | DETECTADA |
| K47-A29 | IG5-100 (I25) | válido: escenario de arte ejecutado sobre el motor, 0 violaciones del auditor | el evento de reutilización referencia otra versión de asset | violación I25 con la condición «otra versión de asset»; procedencia incompleta y E no completo | detectada por I25, I27 · «ca: el evento de reutilización de a2 referencia otra versión de asset (la versión del asset de destino no coin»; E bloqueado | DETECTADA |
| K47-A30 | IG5-100 (I25) | válido: escenario de arte ejecutado sobre el motor, 0 violaciones del auditor | la reutilización no referencia la versión exacta de copy | violación I25 con la condición «versión exacta de copy»; procedencia incompleta y E no completo | detectada por I17, I25, I27 · «ca: el evento de reutilización de a2 no referencia la versión exacta de copy»; E bloqueado | DETECTADA |
| K47-A31 | IG5-100 (I17) | válido: escenario de arte ejecutado sobre el motor, 0 violaciones del auditor | la reutilización intenta reemplazar al uploader original | violación I17 con la condición «figura como uploader»; procedencia incompleta y E no completo | detectada por I17 · «ca: el reutilizador figura como uploader de a2»; E bloqueado | DETECTADA |
| K47-A32 | IG5-100 (I26) | válido: escenario de arte ejecutado sobre el motor, 0 violaciones del auditor | la atribución heredada de asset carece de antecesor verificable | violación I26 con la condición «antecesor verificable»; procedencia incompleta y E no completo | detectada por I26 · «ca: la atribución heredada t8 carece de antecesor verificable»; E bloqueado | DETECTADA |
| K47-A49 | IG5-100 (I23) | válido: escenario de arte ejecutado sobre el motor, 0 violaciones del auditor | el evento de carga corresponde a otra versión de copy | violación I23 con la condición «otra versión de copy»; procedencia incompleta y E no completo | detectada por I23 · «cv2: el evento de carga de a1b corresponde a otra versión de copy»; E bloqueado | DETECTADA |
| K47-A50 | IG5-100 (I25) | válido: escenario de arte ejecutado sobre el motor, 0 violaciones del auditor | el reutilizador tiene membresía inactiva | violación I25 con la condición «membresía inactiva»; procedencia incompleta y E no completo | detectada por I25 · «ca: membresía inactiva o ajena del reutilizador W»; E bloqueado | DETECTADA |
| K47-A51 | IG5-100 (I25) | válido: escenario de arte ejecutado sobre el motor, 0 violaciones del auditor | dos reutilizaciones comparten el mismo evento | violación I25 con la condición «evento propio»; procedencia incompleta y E no completo | detectada por I17, I24, I25, I27 · «ca: la reutilización de a2 no tiene evento propio»; E bloqueado | DETECTADA |
| K47-A52 | IG5-100 (I23) | válido: escenario de arte ejecutado sobre el motor, 0 violaciones del auditor | el actor autenticado del evento de carga no es el uploader | violación I23 con la condición «autenticado»; procedencia incompleta y E no completo | detectada por I23 · «cv1: el actor autenticado del evento de carga de a1 no es el uploader»; E bloqueado | DETECTADA |
| K47-A53 | IG5-100 (I20) | válido: escenario de arte ejecutado sobre el motor, 0 violaciones del auditor | no_aplica oculta un asset registrado | violación I20 con la condición «no_aplica»; procedencia incompleta y E no completo | detectada por I20 · «cv1: declara no_aplica pero registra arte o un asset»; E bloqueado | DETECTADA |
| K47-A33 | IG5-101 (I27) | válido: escenario de arte ejecutado sobre el motor, 0 violaciones del auditor | el evento referencia otro asset de origen de la misma organización | violación I27 con la condición «número de versión distinto»; procedencia incompleta y E no completo | detectada por I27 · «ca2: el evento de reutilización de a2 referencia otro asset de origen de número de versión distinto (axb en lu»; E bloqueado | DETECTADA |
| K47-A34 | IG5-101 (I27) | válido: escenario de arte ejecutado sobre el motor, 0 violaciones del auditor | el evento referencia otro asset con el mismo número de versión | violación I27 con la condición «mismo número de versión»; procedencia incompleta y E no completo | detectada por I27 · «ca2: el evento de reutilización de a2 referencia otro asset de origen con el mismo número de versión (ax en lu»; E bloqueado | DETECTADA |
| K47-A35 | IG5-101 (I27) | válido: escenario de arte ejecutado sobre el motor, 0 violaciones del auditor | el evento referencia otra versión del mismo asset original | violación I27 con la condición «otra versión del mismo asset de origen»; procedencia incompleta y E no completo | detectada por I27 · «ca2: el evento de reutilización de a2 referencia otra versión del mismo asset de origen (a1 en lugar de a1b)»; E bloqueado | DETECTADA |
| K47-A36 | IG5-101 (I27) | válido: escenario de arte ejecutado sobre el motor, 0 violaciones del auditor | el evento referencia un evento de carga de otro asset | violación I27 con la condición «evento de carga de otro asset»; procedencia incompleta y E no completo | detectada por I27 · «ca2: el evento de reutilización de a2 referencia el evento de carga de otro asset»; E bloqueado | DETECTADA |
| K47-A37 | IG5-101 (I27) | válido: escenario de arte ejecutado sobre el motor, 0 violaciones del auditor | el evento referencia otro evento de carga del mismo asset, de otra versión | violación I27 con la condición «evento de carga de otra versión»; procedencia incompleta y E no completo | detectada por I27 · «ca2: el evento de reutilización de a2 referencia el evento de carga de otra versión del mismo asset de origen»; E bloqueado | DETECTADA |
| K47-A38 | IG5-101 (I27) | válido: escenario de arte ejecutado sobre el motor, 0 violaciones del auditor | el evento referencia otro uploader original | violación I27 con la condición «otro uploader original»; procedencia incompleta y E no completo | detectada por I27 · «ca2: el evento de reutilización de a2 referencia otro uploader original (Z en lugar de U)»; E bloqueado | DETECTADA |
| K47-A39 | IG5-101 (I27) | válido: escenario de arte ejecutado sobre el motor, 0 violaciones del auditor | el asset reutilizado apunta a un origen distinto del declarado por el evento | violación I27 con la condición «distinto del declarado»; procedencia incompleta y E no completo | detectada por I17, I26, I27, I28 · «ca2: el asset reutilizado a2 apunta a un origen (ax) distinto del declarado (a1)»; E bloqueado | DETECTADA |
| K47-A40 | IG5-101 (I27) | válido: escenario de arte ejecutado sobre el motor, 0 violaciones del auditor | el evento apunta al origen correcto pero a una versión incorrecta | violación I27 con la condición «versión de origen incorrecta»; procedencia incompleta y E no completo | detectada por I27 · «ca2: el evento de reutilización de a2 referencia una versión de origen incorrecta (7 en lugar de 1)»; E bloqueado | DETECTADA |
| K47-A41 | IG5-101 (I27) | válido: escenario de arte ejecutado sobre el motor, 0 violaciones del auditor | el evento apunta al asset correcto pero a otro evento que no es el de carga | violación I27 con la condición «que no es de carga»; procedencia incompleta y E no completo | detectada por I27 · «ca2: el evento de reutilización de a2 referencia como evento de carga un evento que no es de carga (copy_autho»; E bloqueado | DETECTADA |
| K47-A42 | IG5-101 (I28) | válido: escenario de arte ejecutado sobre el motor, 0 violaciones del auditor | se intercambian dos assets con idéntico número de versión | violación I28 con la condición «están intercambiados»; procedencia incompleta y E no completo | detectada por I10, I16, I17, I23, I24, I27, I28 · «ca2: los eventos de carga de a1 y ax están intercambiados»; E bloqueado | DETECTADA |
| K47-A43 | IG5-101 (I28) | válido: escenario de arte ejecutado sobre el motor, 0 violaciones del auditor | se intercambian dos eventos de carga de la misma organización y pieza | violación I28 con la condición «la clave no coincide con su identificador»; procedencia incompleta y E no completo | detectada por I10, I16, I23, I27, I28 · «ca2: el evento e3 está intercambiado: la clave no coincide con su identificador (e7)»; E bloqueado | DETECTADA |
| K47-A44 | IG5-101 (I27) | válido: escenario de arte ejecutado sobre el motor, 0 violaciones del auditor | el origen pertenece a otra pieza | violación I27 con la condición «otra pieza»; procedencia incompleta y E no completo | detectada por I10, I19, I23, I24, I27 · «ca2: el origen de a2 pertenece a otra pieza que su versión de copy y su evento»; E bloqueado | DETECTADA |
| K47-A45 | IG5-101 (I27) | válido: escenario de arte ejecutado sobre el motor, 0 violaciones del auditor | el origen pertenece a otra organización | violación I27 con la condición «otra organización»; procedencia incompleta y E no completo | detectada por I10, I19, I22, I23, I24, I27 · «ca2: el origen de a2 pertenece a otra organización»; E bloqueado | DETECTADA |
| K47-A46 | IG5-101 (I27) | válido: escenario de arte ejecutado sobre el motor, 0 violaciones del auditor | el evento de reutilización referencia otra versión de copy | violación I27 con la condición «otra versión de copy de la misma pieza»; procedencia incompleta y E no completo | detectada por I17, I25, I27 · «ca2: el evento de reutilización de a2 referencia otra versión de copy de la misma pieza (ca2)»; E bloqueado | DETECTADA |
| K47-A47 | IG5-101 (I27) | válido: escenario de arte ejecutado sobre el motor, 0 violaciones del auditor | el actor autenticado no coincide con el reutilizador registrado | violación I27 con la condición «no coincide con el reutilizador registrado»; procedencia incompleta y E no completo | detectada por I25, I27 · «ca2: el actor autenticado del evento de reutilización de a2 no coincide con el reutilizador registrado»; E bloqueado | DETECTADA |
| K47-A48 | IG5-101 (I28) | válido: escenario de arte ejecutado sobre el motor, 0 violaciones del auditor | la cadena de reutilización pierde el vínculo con el evento original de carga | violación I28 con la condición «pierde el vínculo»; procedencia incompleta y E no completo | detectada por I17, I28 · «cc: la cadena de reutilización de a3 pierde el vínculo con el evento original de carga»; E bloqueado | DETECTADA |
| CHAIN-01 | IG5-104 (CHAIN) | válido: cadena de tres niveles aceptada, cero violaciones del auditor y E completo | asset inmediato incorrecto, raíz correcta (el eslabón a3 apunta a a1 saltando a a2) | rechazo del motor con «origen» y el eslabón a3; sin registros parciales, estado previo idéntico y E bloqueado | rechazada: [eslabón a3] el campo source_asset_id del evento propio no corresponde a: el asset de origen (origen inmediato o raíz) (esperado a1, hallado a2); [eslabón a3] el campo so; E bloqueado | DETECTADA |
| CHAIN-02 | IG5-104 (CHAIN) | válido: cadena de tres niveles aceptada, cero violaciones del auditor y E completo | versión inmediata incorrecta, raíz correcta (el evento de a3 declara otra versión del origen) | rechazo del motor con «versión» y el eslabón a3; sin registros parciales, estado previo idéntico y E bloqueado | rechazada: [eslabón a3] el campo source_asset_version del evento propio no corresponde a: la versión del asset de origen (versión) (origen inmediato o raíz) (esperado 1, hallado 7); E bloqueado | DETECTADA |
| CHAIN-03 | IG5-104 (CHAIN) | válido: cadena de tres niveles aceptada, cero violaciones del auditor y E completo | evento propio de reutilización de otro eslabón (a3 usa el evento de a2) | rechazo del motor con «evento propio» y el eslabón a3; sin registros parciales, estado previo idéntico y E bloqueado | rechazada: [eslabón a3] el evento propio corresponde a otro asset (a2) y no a este eslabón [evento e23; campo asset; esperado ('a3', 'a3'); hallado ('a2', 'a2')]; [eslabón a3] el ev; E bloqueado | DETECTADA |
| CHAIN-04 | IG5-104 (CHAIN) | válido: cadena de tres niveles aceptada, cero violaciones del auditor y E completo | evento original correcto en la raíz pero referencia intermedia incorrecta (a2 referencia el evento de carga de otro asset) | rechazo del motor con «evento de carga» y el eslabón a2; sin registros parciales, estado previo idéntico y E bloqueado | rechazada: [eslabón a2] el campo source_upload_event_id del evento propio no corresponde a: el evento de carga original (evento de carga) (origen inmediato o raíz) (esperado e3, hal; E bloqueado | DETECTADA |
| CHAIN-05 | IG5-104 (CHAIN) | válido: cadena de tres niveles aceptada, cero violaciones del auditor y E completo | uploader correcto en la raíz y referencia intermedia a otra persona (a2) | rechazo del motor con «uploader» y el eslabón a2; sin registros parciales, estado previo idéntico y E bloqueado | rechazada: [eslabón a2] el campo source_uploader_id del evento propio no corresponde a: el uploader original (uploader) (origen inmediato o raíz) (esperado U, hallado Z); E bloqueado | DETECTADA |
| CHAIN-06 | IG5-104 (CHAIN) | válido: cadena de tres niveles aceptada, cero violaciones del auditor y E completo | atribución raíz correcta pero referencia intermedia a otra atribución (a2) | rechazo del motor con «atribución» y el eslabón a2; sin registros parciales, estado previo idéntico y E bloqueado | rechazada: [eslabón a2] el campo source_attribution_id del evento propio no corresponde a: la atribución directa original (atribución) (origen inmediato o raíz) (esperado t4, hallad; E bloqueado | DETECTADA |
| CHAIN-07 | IG5-104 (CHAIN) | válido: cadena de tres niveles aceptada, cero violaciones del auditor y E completo | asset intermedio de otra organización (a2) | rechazo del motor con «organización» y el eslabón a2; sin registros parciales, estado previo idéntico y E bloqueado | rechazada: [eslabón a3] el origen inmediato a2 pertenece a otra organización; [eslabón a2] el asset pertenece a otra organización; [eslabón a2] el origen inmediato a1 pertenece a ot; E bloqueado | DETECTADA |
| CHAIN-08 | IG5-104 (CHAIN) | válido: cadena de tres niveles aceptada, cero violaciones del auditor y E completo | asset intermedio de otra pieza (a2) | rechazo del motor con «pieza» y el eslabón a2; sin registros parciales, estado previo idéntico y E bloqueado | rechazada: [eslabón a2] la pieza del asset no coincide con la pieza de su versión de copy; [eslabón a2] el evento propio pertenece a otra pieza [evento e23; campo pieza; esperado 'P; E bloqueado | DETECTADA |
| CHAIN-09 | IG5-104 (CHAIN) | válido: cadena de tres niveles aceptada, cero violaciones del auditor y E completo | versión de copy del asset intermedio incorrecta (a2) | rechazo del motor con «versión de copy» y el eslabón a2; sin registros parciales, estado previo idéntico y E bloqueado | rechazada: [eslabón a2] la pieza del asset no coincide con la pieza de su versión de copy; [eslabón a2] la versión de copy no usa este asset en el campo arte (versión de copy) [even; E bloqueado | DETECTADA |
| CHAIN-10 | IG5-104 (CHAIN) | válido: cadena de tres niveles aceptada, cero violaciones del auditor y E completo | actor autenticado incorrecto en el evento del eslabón intermedio (a2) | rechazo del motor con «actor autenticado» y el eslabón a2; sin registros parciales, estado previo idéntico y E bloqueado | rechazada: [eslabón a2] el actor autenticado del evento propio no coincide con el actor del eslabón [evento e23; campo auth; esperado 'W'; hallado 'Z']; E bloqueado | DETECTADA |
| CHAIN-11 | IG5-104 (CHAIN) | válido: cadena de tres niveles aceptada, cero violaciones del auditor y E completo | cadena con referencia circular (a2 apunta a a3) | rechazo del motor con «ciclo» y el eslabón a2; sin registros parciales, estado previo idéntico y E bloqueado | rechazada: [eslabón a2] la referencia a a3 cierra un ciclo: la cadena de origen de a3 no es verificable (ciclo); E bloqueado | DETECTADA |
| CHAIN-12 | IG5-104 (CHAIN) | válido: cadena de tres niveles aceptada, cero violaciones del auditor y E completo | cadena con dos raíces posibles (a2 con origen y versión previa) | rechazo del motor con «ambigua» y el eslabón a2; sin registros parciales, estado previo idéntico y E bloqueado | rechazada: [eslabón a2] la cadena es ambigua: el asset reutilizado declara a la vez origen y versión anterior; E bloqueado | DETECTADA |
| CHAIN-13 | IG5-104 (CHAIN) | válido: cadena de tres niveles aceptada, cero violaciones del auditor y E completo | referencia faltante en un eslabón intermedio (a2 sin origen) | rechazo del motor con «referencia» y el eslabón a2; sin registros parciales, estado previo idéntico y E bloqueado | rechazada: [eslabón a2] falta la referencia al asset de origen del asset reutilizado; E bloqueado | DETECTADA |
| CHAIN-14 | IG5-104 (CHAIN) | válido: cadena de tres niveles aceptada, cero violaciones del auditor y E completo | referencia duplicada: la atribución directa del reutilizador de a2 está duplicada | rechazo del motor con «duplicada» y el eslabón a2; sin registros parciales, estado previo idéntico y E bloqueado | rechazada: [eslabón a2] la atribución directa del reutilizador está duplicada (duplicada); E bloqueado | DETECTADA |
| CHAIN-15 | IG5-104 (CHAIN) | válido: cadena de tres niveles aceptada, cero violaciones del auditor y E completo | datos de la raíz correctos y campos source_* intermedios intercambiados entre a2 y a3 | rechazo del motor con «source_asset_version_id» y el eslabón a2; sin registros parciales, estado previo idéntico y E bloqueado | rechazada: [eslabón a3] el campo source_asset_id del evento propio no corresponde a: el asset de origen (origen inmediato o raíz) (esperado a2, hallado a1); [eslabón a3] el campo so; E bloqueado | DETECTADA |
| CHAIN-16 | IG5-104 (CHAIN) | válido: cadena de tres niveles aceptada, cero violaciones del auditor y E completo | asset modificado que pierde la raíz original (a1b sin versión anterior) | rechazo del motor con «versión anterior» y el eslabón a1b; sin registros parciales, estado previo idéntico y E bloqueado | rechazada: [eslabón a1b] falta la versión anterior del asset modificado: la cadena pierde su raíz original; E bloqueado | DETECTADA |
| CHAIN-17 | IG5-104 (CHAIN) | válido: cadena de tres niveles aceptada, cero violaciones del auditor y E completo | reutilización de una versión anterior en lugar de la exacta (a2 referencia la versión a1 y a1b es la vigente del origen) | rechazo del motor con «versión» y el eslabón a2; sin registros parciales, estado previo idéntico y E bloqueado | rechazada: [eslabón a2] el campo source_asset_version_id del evento propio no corresponde a: la versión referenciada no es el origen inmediato exacto (versión) (origen inmediato o r; E bloqueado | DETECTADA |
| CHAIN-18 | IG5-104 (CHAIN) | válido: cadena de tres niveles aceptada, cero violaciones del auditor y E completo | evento de carga válido de otro asset con el mismo número de versión (a2 referencia el de ax) | rechazo del motor con «evento de carga» y el eslabón a2; sin registros parciales, estado previo idéntico y E bloqueado | rechazada: [eslabón a2] el campo source_upload_event_id del evento propio no corresponde a: el evento de carga original (evento de carga) (origen inmediato o raíz) (esperado e3, hal; E bloqueado | DETECTADA |
| CHAIN-19 | IG5-104 (CHAIN) | válido: cadena de tres niveles aceptada, cero violaciones del auditor y E completo | evento de reutilización válido de otro asset (a3 usa el de ay) | rechazo del motor con «evento propio» y el eslabón a3; sin registros parciales, estado previo idéntico y E bloqueado | rechazada: [eslabón a3] el evento propio corresponde a otro asset (ay) y no a este eslabón [evento e36; campo asset; esperado ('a3', 'a3'); hallado ('ay', 'ay')]; [eslabón a3] el ev; E bloqueado | DETECTADA |
| CHAIN-20 | IG5-104 (CHAIN) | válido: cadena de tres niveles aceptada, cero violaciones del auditor y E completo | cadena de tres niveles con corrupción solo en el nivel intermedio (el evento de a2 pertenece a otra versión de copy) | rechazo del motor con «versión de copy» y el eslabón a2; sin registros parciales, estado previo idéntico y E bloqueado | rechazada: [eslabón a2] el evento propio corresponde a otra versión de copy [evento e23; campo version; esperado 'ca'; hallado 'cvu']; E bloqueado | DETECTADA |
| CHAIN-21 | IG5-104 (CHAIN) | válido: cadena de tres niveles aceptada, cero violaciones del auditor y E completo | eslabón modificado intermedio con el evento de carga de otro asset (a1b usa el de ax) | rechazo del motor con «evento propio» y el eslabón a1b; sin registros parciales, estado previo idéntico y E bloqueado | rechazada: [eslabón a1b] el evento propio corresponde a otro asset (ax) y no a este eslabón [evento e11; campo asset; esperado ('a1b', 'a1'); hallado ('ax', 'ax')]; [eslabón a1b] el; E bloqueado | DETECTADA |
| CHAIN-22 | IG5-104 (CHAIN) | válido: cadena de tres niveles aceptada, cero violaciones del auditor y E completo | eslabón modificado intermedio con otro editor que el del evento (a1b declara al uploader Z) | rechazo del motor con «actor» y el eslabón a1b; sin registros parciales, estado previo idéntico y E bloqueado | rechazada: [eslabón a1b] el actor del evento propio no coincide con el actor del eslabón [evento e7; campo actor; esperado 'Z'; hallado 'D']; [eslabón a1b] el actor autenticado del ; E bloqueado | DETECTADA |
| CHAIN-23 | IG5-104 (CHAIN) | válido: cadena de tres niveles aceptada, cero violaciones del auditor y E completo | eslabón modificado intermedio con número de versión que no sigue al anterior (a1b declara la versión 3) | rechazo del motor con «versión anterior» y el eslabón a1b; sin registros parciales, estado previo idéntico y E bloqueado | rechazada: [eslabón a1b] la versión anterior no es la versión exacta inmediatamente anterior del mismo asset (versión anterior); [eslabón a1b] el evento propio corresponde a otra ve; E bloqueado | DETECTADA |
| CHAIN-24 | IG5-104 (CHAIN) | válido: cadena de tres niveles aceptada, cero violaciones del auditor y E completo | eslabón modificado intermedio con la atribución directa del editor duplicada (a1b) | rechazo del motor con «duplicada» y el eslabón a1b; sin registros parciales, estado previo idéntico y E bloqueado | rechazada: [eslabón a1b] la atribución directa del editor de la versión está duplicada (duplicada); E bloqueado | DETECTADA |
| AV-01 | IG5-111 (AV) | válido: reutilización aceptada, cero violaciones del auditor independiente y E completo | asset_version del evento propio del último eslabón (a3) cambia a una versión inexistente | rechazo con el campo asset_version del eslabón a3; sin asset, evento, atribución ni relación parcial, estado completo idéntico, procedencia incompleta, E nulo y sin impacto, aprobación ni publicación | rechazada: [eslabón a3] el evento propio corresponde a otra versión del asset (asset_version) [evento e28; campo asset_version; esperado 1; hallado 7]; [eslabón ; E bloqueado | DETECTADA |
| AV-02 | IG5-111 (AV) | válido: reutilización aceptada, cero violaciones del auditor independiente y E completo | asset_version del evento propio de un eslabón intermedio (a2) cambia a una versión inexistente | rechazo con el campo asset_version del eslabón a2; sin asset, evento, atribución ni relación parcial, estado completo idéntico, procedencia incompleta, E nulo y sin impacto, aprobación ni publicación | rechazada: [eslabón a2] el evento propio corresponde a otra versión del asset (asset_version) [evento e23; campo asset_version; esperado 1; hallado 5]; [eslabón ; E bloqueado | DETECTADA |
| AV-03 | IG5-111 (AV) | válido: reutilización aceptada, cero violaciones del auditor independiente y E completo | asset_version de a3 usa un número de versión existente pero perteneciente a otro asset (el de la modificación a1b) | rechazo con el campo asset_version del eslabón a3; sin asset, evento, atribución ni relación parcial, estado completo idéntico, procedencia incompleta, E nulo y sin impacto, aprobación ni publicación | rechazada: [eslabón a3] el evento propio corresponde a otra versión del asset (asset_version) [evento e28; campo asset_version; esperado 1; hallado 2]; [eslabón ; E bloqueado | DETECTADA |
| AV-04 | IG5-111 (AV) | válido: reutilización aceptada, cero violaciones del auditor independiente y E completo | el evento propio de la modificación intermedia a1b usa la versión anterior del mismo asset (1 en lugar de 2) | rechazo con el campo asset_version del eslabón a1b; sin asset, evento, atribución ni relación parcial, estado completo idéntico, procedencia incompleta, E nulo y sin impacto, aprobación ni publicación | rechazada: [eslabón a1b] el evento propio corresponde a otra versión del asset (asset_version) [evento e7; campo asset_version; esperado 2; hallado 1]; [eslabón ; E bloqueado | DETECTADA |
| AV-05 | IG5-111 (AV) | válido: reutilización aceptada, cero violaciones del auditor independiente y E completo | asset_version intercambiado entre dos eventos válidos (la modificación a1b y la reutilización a5) | rechazo con el campo asset_version del eslabón a5; sin asset, evento, atribución ni relación parcial, estado completo idéntico, procedencia incompleta, E nulo y sin impacto, aprobación ni publicación | rechazada: [eslabón a5] el evento propio corresponde a otra versión del asset (asset_version) [evento e41; campo asset_version; esperado 1; hallado 2]; [eslabón ; E bloqueado | DETECTADA |
| AV-06 | IG5-111 (AV) | válido: reutilización aceptada, cero violaciones del auditor independiente y E completo | asset_version de a5 guarda la versión del origen (2) en lugar de la del destino (1), con la raíz y las demás referencias correctas | rechazo con el campo asset_version del eslabón a5; sin asset, evento, atribución ni relación parcial, estado completo idéntico, procedencia incompleta, E nulo y sin impacto, aprobación ni publicación | rechazada: [eslabón a5] el evento propio corresponde a otra versión del asset (asset_version) [evento e41; campo asset_version; esperado 1; hallado 2]; [eslabón ; E bloqueado | DETECTADA |
| AV-07 | IG5-111 (AV) | válido: reutilización aceptada, cero violaciones del auditor independiente y E completo | asset_version del evento propio de una modificación intermedia (a1b) cambia a otro número | rechazo con el campo asset_version del eslabón a1b; sin asset, evento, atribución ni relación parcial, estado completo idéntico, procedencia incompleta, E nulo y sin impacto, aprobación ni publicación | rechazada: [eslabón a1b] el evento propio corresponde a otra versión del asset (asset_version) [evento e7; campo asset_version; esperado 2; hallado 9]; [eslabón ; E bloqueado | DETECTADA |
| AV-08 | IG5-111 (AV) | válido: reutilización aceptada, cero violaciones del auditor independiente y E completo | asset_version de a3 se altera después de construir la cadena (a4 ya registrada) | rechazo con el campo asset_version del eslabón a3; sin asset, evento, atribución ni relación parcial, estado completo idéntico, procedencia incompleta, E nulo y sin impacto, aprobación ni publicación | rechazada: [eslabón a3] el evento propio corresponde a otra versión del asset (asset_version) [evento e28; campo asset_version; esperado 1; hallado 4]; [eslabón ; E bloqueado | DETECTADA |
| CF-01 | IG5-112 (CF) | válido: reutilización aceptada, cero violaciones del auditor independiente y E completo | el campo del evento propio del último eslabón (a3) cambia de arte a otro campo (precio) | rechazo con el campo campo del eslabón a3; sin asset, evento, atribución ni relación parcial, estado completo idéntico, procedencia incompleta, E nulo y sin impacto, aprobación ni publicación | rechazada: [eslabón a3] el campo del evento propio no es un campo permitido (campo no permitido) [evento e28; campo campo; esperado 'arte'; hallado 'precio']; E bloqueado | DETECTADA |
| CF-02 | IG5-112 (CF) | válido: reutilización aceptada, cero violaciones del auditor independiente y E completo | el campo del evento propio de un eslabón intermedio (a2) cambia de arte a otro campo (precio) | rechazo con el campo campo del eslabón a2; sin asset, evento, atribución ni relación parcial, estado completo idéntico, procedencia incompleta, E nulo y sin impacto, aprobación ni publicación | rechazada: [eslabón a2] el campo del evento propio no es un campo permitido (campo no permitido) [evento e23; campo campo; esperado 'arte'; hallado 'precio']; E bloqueado | DETECTADA |
| CF-03 | IG5-112 (CF) | válido: reutilización aceptada, cero violaciones del auditor independiente y E completo | se elimina el campo del evento propio de un eslabón intermedio (a2) | rechazo con el campo campo del eslabón a2; sin asset, evento, atribución ni relación parcial, estado completo idéntico, procedencia incompleta, E nulo y sin impacto, aprobación ni publicación | rechazada: [eslabón a2] el evento propio no declara el campo (campo ausente) [evento e23; campo campo; esperado 'arte'; hallado None]; E bloqueado | DETECTADA |
| CF-04 | IG5-112 (CF) | válido: reutilización aceptada, cero violaciones del auditor independiente y E completo | el campo del evento propio del último eslabón (a3) es nulo | rechazo con el campo campo del eslabón a3; sin asset, evento, atribución ni relación parcial, estado completo idéntico, procedencia incompleta, E nulo y sin impacto, aprobación ni publicación | rechazada: [eslabón a3] el evento propio no declara el campo (campo ausente) [evento e28; campo campo; esperado 'arte'; hallado None]; E bloqueado | DETECTADA |
| CF-05 | IG5-112 (CF) | válido: reutilización aceptada, cero violaciones del auditor independiente y E completo | el evento propio de la modificación a1b declara un campo permitido pero distinto de arte (headline) | rechazo con el campo campo del eslabón a1b; sin asset, evento, atribución ni relación parcial, estado completo idéntico, procedencia incompleta, E nulo y sin impacto, aprobación ni publicación | rechazada: [eslabón a1b] el evento propio no está vinculado al campo arte (otro campo) [evento e7; campo campo; esperado 'arte'; hallado 'headline']; E bloqueado | DETECTADA |
| CF-06 | IG5-112 (CF) | válido: reutilización aceptada, cero violaciones del auditor independiente y E completo | el campo se intercambia entre dos eventos válidos (la reutilización de a2 y la introducción de headline de la misma versión de copy) | rechazo con el campo campo del eslabón a2; sin asset, evento, atribución ni relación parcial, estado completo idéntico, procedencia incompleta, E nulo y sin impacto, aprobación ni publicación | rechazada: [eslabón a2] el evento propio no está vinculado al campo arte (otro campo) [evento e23; campo campo; esperado 'arte'; hallado 'headline']; E bloqueado | DETECTADA |
| CF-07 | IG5-112 (CF) | válido: reutilización aceptada, cero violaciones del auditor independiente y E completo | el campo de a3 se modifica después de construir la cadena (a4 ya registrada) | rechazo con el campo campo del eslabón a3; sin asset, evento, atribución ni relación parcial, estado completo idéntico, procedencia incompleta, E nulo y sin impacto, aprobación ni publicación | rechazada: [eslabón a3] el evento propio no está vinculado al campo arte (otro campo) [evento e28; campo campo; esperado 'arte'; hallado 'headline']; E bloqueado | DETECTADA |
| CF-08 | IG5-112 (CF) | válido: reutilización aceptada, cero violaciones del auditor independiente y E completo | todos los identificadores de a5 son correctos y solo cambia el campo (headline) | rechazo con el campo campo del eslabón a5; sin asset, evento, atribución ni relación parcial, estado completo idéntico, procedencia incompleta, E nulo y sin impacto, aprobación ni publicación | rechazada: [eslabón a5] el evento propio no está vinculado al campo arte (otro campo) [evento e41; campo campo; esperado 'arte'; hallado 'headline']; E bloqueado | DETECTADA |
| AC-01 | IG5-113 (AC) | válido: reutilización aceptada, cero violaciones del auditor independiente y E completo | asset_version incorrecto y campo correcto en a2 | rechazo con el campo asset_version del eslabón a2; sin asset, evento, atribución ni relación parcial, estado completo idéntico, procedencia incompleta, E nulo y sin impacto, aprobación ni publicación | rechazada: [eslabón a2] el evento propio corresponde a otra versión del asset (asset_version) [evento e23; campo asset_version; esperado 1; hallado 5]; [eslabón ; E bloqueado | DETECTADA |
| AC-02 | IG5-113 (AC) | válido: reutilización aceptada, cero violaciones del auditor independiente y E completo | asset_version correcto y campo incorrecto en a3 | rechazo con el campo campo del eslabón a3; sin asset, evento, atribución ni relación parcial, estado completo idéntico, procedencia incompleta, E nulo y sin impacto, aprobación ni publicación | rechazada: [eslabón a3] el evento propio no está vinculado al campo arte (otro campo) [evento e28; campo campo; esperado 'arte'; hallado 'headline']; E bloqueado | DETECTADA |
| AC-03 | IG5-113 (AC) | válido: reutilización aceptada, cero violaciones del auditor independiente y E completo | asset_version y campo incorrectos en a3 | rechazo con el campo asset_version y campo del eslabón a3; sin asset, evento, atribución ni relación parcial, estado completo idéntico, procedencia incompleta, E nulo y sin impacto, aprobación ni publicación | rechazada: [eslabón a3] el evento propio corresponde a otra versión del asset (asset_version) [evento e28; campo asset_version; esperado 1; hallado 5]; [eslabón ; E bloqueado | DETECTADA |
| AC-04 | IG5-113 (AC) | válido: reutilización aceptada, cero violaciones del auditor independiente y E completo | asset_version y campo incorrectos a la vez en el eslabón intermedio a5, con la raíz intacta | rechazo con el campo asset_version y campo del eslabón a5; sin asset, evento, atribución ni relación parcial, estado completo idéntico, procedencia incompleta, E nulo y sin impacto, aprobación ni publicación | rechazada: [eslabón a5] el evento propio corresponde a otra versión del asset (asset_version) [evento e41; campo asset_version; esperado 1; hallado 7]; [eslabón ; E bloqueado | DETECTADA |
| AC-05 | IG5-113 (AC) | válido: reutilización aceptada, cero violaciones del auditor independiente y E completo | asset_version y campo incorrectos en el último eslabón a6, con todos los anteriores correctos | rechazo con el campo asset_version y campo del eslabón a6; sin asset, evento, atribución ni relación parcial, estado completo idéntico, procedencia incompleta, E nulo y sin impacto, aprobación ni publicación | rechazada: [eslabón a6] el evento propio corresponde a otra versión del asset (asset_version) [evento e47; campo asset_version; esperado 1; hallado 7]; [eslabón ; E bloqueado | DETECTADA |
| AC-06 | IG5-113 (AC) | válido: reutilización aceptada, cero violaciones del auditor independiente y E completo | a2 y a2c (misma pieza P2, ambos en la versión 1) con las referencias de asset y versión cruzadas entre sus eventos | rechazo con el campo asset y asset_version_id del eslabón a2; sin asset, evento, atribución ni relación parcial, estado completo idéntico, procedencia incompleta, E nulo y sin impacto, aprobación ni publicación | rechazada: [eslabón a2] el evento propio corresponde a otro asset (a2c) y no a este eslabón [evento e23; campo asset; esperado ('a2', 'a2'); hallado ('a2c', 'a2'; E bloqueado | DETECTADA |
| ATTR-01 | IG5-107 (I13) | válido: escenario con resoluciones selladas y atribuciones conservadas, cero violaciones | resolución modificada después de su creación | violación I13 | I13 | DETECTADA |
| ATTR-02 | IG5-107 (I13 e I15) | válido: escenario con resoluciones selladas y atribuciones conservadas, cero violaciones | resolución eliminada | violación I13 e I15 | I13,I15 | DETECTADA |
| ATTR-03 | IG5-107 (I15) | válido: escenario con resoluciones selladas y atribuciones conservadas, cero violaciones | resolución duplicada para la misma atribución | violación I15 | I15 | DETECTADA |
| ATTR-04 | IG5-107 (rechazo del motor con R5 y aceptación forzada detectada (I4)) | válido: escenario con resoluciones selladas y atribuciones conservadas, cero violaciones | resolutor que fue el editor que sustituyó | violación rechazo del motor con R5 y aceptación forzada detectada (I4) | rechaza=True auditor=True ['I4', 'I5'] | DETECTADA |
| ATTR-05 | IG5-107 (rechazo del motor con R4 y aceptación forzada detectada (I4)) | válido: escenario con resoluciones selladas y atribuciones conservadas, cero violaciones | resolutor que fue el solicitante | violación rechazo del motor con R4 y aceptación forzada detectada (I4) | rechaza=True auditor=True ['I4', 'I5'] | DETECTADA |
| ATTR-06 | IG5-107 (rechazo del motor con R7 y aceptación forzada detectada (I4)) | válido: escenario con resoluciones selladas y atribuciones conservadas, cero violaciones | resolutor que heredó la contribución evaluada | violación rechazo del motor con R7 y aceptación forzada detectada (I4) | rechaza=True auditor=True | DETECTADA |
| ATTR-07 | IG5-107 (rechazo del motor con V11 y aceptación forzada detectada (I4)) | válido: escenario con resoluciones selladas y atribuciones conservadas, cero violaciones | evidencia ausente | violación rechazo del motor con V11 y aceptación forzada detectada (I4) | rechaza=True auditor=True ['I4', 'I5'] | DETECTADA |
| ATTR-08 | IG5-107 (rechazo del motor con V05 y aceptación forzada detectada (I4)) | válido: escenario con resoluciones selladas y atribuciones conservadas, cero violaciones | evidencia de otro campo | violación rechazo del motor con V05 y aceptación forzada detectada (I4) | rechaza=True auditor=True ['I4', 'I5'] | DETECTADA |
| ATTR-09 | IG5-107 (rechazo del motor con V06 y aceptación forzada detectada (I4)) | válido: escenario con resoluciones selladas y atribuciones conservadas, cero violaciones | evidencia de otra versión | violación rechazo del motor con V06 y aceptación forzada detectada (I4) | rechaza=True auditor=True ['I4', 'I5'] | DETECTADA |
| ATTR-10 | IG5-107 (I13 e I14) | válido: escenario con resoluciones selladas y atribuciones conservadas, cero violaciones | reconsideración que modifica el registro anterior | violación I13 e I14 | I13,I14 | DETECTADA |
| ATTR-11 | IG5-107 (I15) | válido: escenario con resoluciones selladas y atribuciones conservadas, cero violaciones | atribución histórica reactivada sin resolución | violación I15 | I15 | DETECTADA |
| ATTR-12 | IG5-107 (el motor conserva la atribución y el auditor detecta la eliminación (I1)) | válido: escenario con resoluciones selladas y atribuciones conservadas, cero violaciones | atribución activa eliminada por cero segmentos idénticos | violación el motor conserva la atribución y el auditor detecta la eliminación (I1) | motor conserva=True auditor=['I1', 'I15'] | DETECTADA |
| K56-M01 | IG5-110 (código del modelo) | válido: las baterías CHAIN, ADVC, ATTR, AT14, E14, AV, CF, AC, AP, ADV15 y AT15 aprueban | la validación de cada eslabón reutilizado pasa a ser un no-op (solo se mira la raíz, como en la v13) | al menos una batería falla | detectada por 39 pruebas: CHAIN:CHAIN-01, CHAIN:CHAIN-02, CHAIN:CHAIN-03, CHAIN:CHAIN-04 | DETECTADA |
| K56-M02 | IG5-110 (código del modelo) | válido: las baterías CHAIN, ADVC, ATTR, AT14, E14, AV, CF, AC, AP, ADV15 y AT15 aprueban | la reconstrucción ignora la ambigüedad origen/versión anterior | al menos una batería falla | detectada por 3 pruebas: CHAIN:CHAIN-12, CHAIN:CHAIN-13, CHAIN:CHAIN-16 | DETECTADA |
| K56-M03 | IG5-110 (código del modelo) | válido: las baterías CHAIN, ADVC, ATTR, AT14, E14, AV, CF, AC, AP, ADV15 y AT15 aprueban | la verificación final de la transacción deja de ejecutarse | al menos una batería falla | detectada por 1 pruebas: AT14:AT14-11 | DETECTADA |
| K56-M04 | IG5-110 (código del modelo) | válido: las baterías CHAIN, ADVC, ATTR, AT14, E14, AV, CF, AC, AP, ADV15 y AT15 aprueban | el auditor independiente de cadena no devuelve hallazgos | al menos una batería falla | detectada por 33 pruebas: ADVC:ADVC-01, ADVC:ADVC-02, ADVC:ADVC-03, ADVC:ADVC-04 | DETECTADA |
| K56-M05 | IG5-110 (código del modelo) | válido: las baterías CHAIN, ADVC, ATTR, AT14, E14, AV, CF, AC, AP, ADV15 y AT15 aprueban | el auditor de resoluciones filtra la reactivación de atribuciones históricas | al menos una batería falla | detectada por 1 pruebas: ATTR:ATTR-11 | DETECTADA |
| K56-M06 | IG5-110 (código del modelo) | válido: las baterías CHAIN, ADVC, ATTR, AT14, E14, AV, CF, AC, AP, ADV15 y AT15 aprueban | la elegibilidad del evaluador ignora su pertenencia a E (E4) | al menos una batería falla | detectada por 2 pruebas: AT14:AT14-09, E14:E14-04 | DETECTADA |
| K56-M07 | IG5-110 (código del modelo) | válido: las baterías CHAIN, ADVC, ATTR, AT14, E14, AV, CF, AC, AP, ADV15 y AT15 aprueban | registrar_asset se ejecuta sin la transacción (sin restauración ante fallo) | al menos una batería falla | detectada por 4 pruebas: AT14:AT14-01, AT14:AT14-02, AT14:AT14-11, AT15:AT15-08 | DETECTADA |
| K56-M08 | IG5-110 (código del modelo) | válido: las baterías CHAIN, ADVC, ATTR, AT14, E14, AV, CF, AC, AP, ADV15 y AT15 aprueban | la validación de una versión modificada pasa a ser un no-op | al menos una batería falla | detectada por 7 pruebas: CHAIN:CHAIN-21, CHAIN:CHAIN-22, CHAIN:CHAIN-23, CHAIN:CHAIN-24 | DETECTADA |
| K56-M09 | IG5-110 (código del modelo) | válido: las baterías CHAIN, ADVC, ATTR, AT14, E14, AV, CF, AC, AP, ADV15 y AT15 aprueban | la validación de asset_version del evento propio pasa a ser un no-op (v14: solo se comparaba source_asset_version) | al menos una batería falla | detectada por 13 pruebas: AV:AV-01, AV:AV-02, AV:AV-03, AV:AV-04 | DETECTADA |
| K56-M10 | IG5-110 (código del modelo) | válido: las baterías CHAIN, ADVC, ATTR, AT14, E14, AV, CF, AC, AP, ADV15 y AT15 aprueban | la validación del campo del evento propio pasa a ser un no-op (v14: no se comprobaba campo en la reconstrucción) | al menos una batería falla | detectada por 12 pruebas: CF:CF-01, CF:CF-02, CF:CF-03, CF:CF-04 | DETECTADA |
| K56-M11 | IG5-110 (código del modelo) | válido: las baterías CHAIN, ADVC, ATTR, AT14, E14, AV, CF, AC, AP, ADV15 y AT15 aprueban | el auditor independiente de cadena deja de comparar asset_version y campo | al menos una batería falla | detectada por 9 pruebas: ADVC:ADVC-02, ADVC:ADVC-17, AP:AP-08, ADV15:ADV15-01 | DETECTADA |
| K56-M12 | IG5-110 (código del modelo) | válido: las baterías CHAIN, ADVC, ATTR, AT14, E14, AV, CF, AC, AP, ADV15 y AT15 aprueban | la reconstrucción de la cadena no entrega el detalle estructurado de cada inconsistencia (eslabón, evento, campo, esperado, hallado) | al menos una batería falla | detectada por 22 pruebas: AV:AV-01, AV:AV-02, AV:AV-03, AV:AV-04 | DETECTADA |
| K47-A54 | IG5-102 (rechazo del motor con «corresponde a otro asset») | válido: fixture de reutilización exacta, 0 violaciones del auditor y E completo | el evento original de carga pertenece a otro asset de la misma organización y pieza | rechazo del motor con «corresponde a otro asset»; sin registros parciales, estado previo idéntico, E nulo, sin evaluación de impacto, aprobación ni publicación | rechazada: el evento original de carga corresponde a otro asset (au) y no al asset raíz a1; el evento original de carga de a1 corresponde a otra versión de copy;; E nulo en la pieza y la versión de destino | DETECTADA |
| K47-A55 | IG5-102 (rechazo del motor con «corresponde a otro asset») | válido: fixture de reutilización exacta, 0 violaciones del auditor y E completo | el evento original de carga pertenece a otro asset con el mismo número de versión | rechazo del motor con «corresponde a otro asset»; sin registros parciales, estado previo idéntico, E nulo, sin evaluación de impacto, aprobación ni publicación | rechazada: el evento original de carga corresponde a otro asset (ax) y no al asset raíz a1; el evento original de carga de a1 corresponde a otra versión de copy;; E nulo en la pieza y la versión de destino | DETECTADA |
| K47-A56 | IG5-102 (rechazo del motor con «otra versión del mismo asset») | válido: fixture de reutilización exacta, 0 violaciones del auditor y E completo | el evento original de carga es el de otra versión del mismo asset raíz | rechazo del motor con «otra versión del mismo asset»; sin registros parciales, estado previo idéntico, E nulo, sin evaluación de impacto, aprobación ni publicación | rechazada: el evento original de carga corresponde a otra versión del mismo asset (a1b) y no a la versión exacta de la raíz a1; el evento original de carga de a1; E nulo en la pieza y la versión de destino | DETECTADA |
| K47-A57 | IG5-102 (rechazo del motor con «pertenece a otro evento de carga») | válido: fixture de reutilización exacta, 0 violaciones del auditor y E completo | la atribución directa del uploader pertenece a otro evento de carga del mismo asset | rechazo del motor con «pertenece a otro evento de carga»; sin registros parciales, estado previo idéntico, E nulo, sin evaluación de impacto, aprobación ni publicación | rechazada: la atribución directa t4 pertenece a otro evento de carga (e7) y no al evento original de a1; E nulo en la pieza y la versión de destino | DETECTADA |
| K47-A58 | IG5-102 (rechazo del motor con «pertenece a otro asset») | válido: fixture de reutilización exacta, 0 violaciones del auditor y E completo | la atribución directa pertenece a otro asset de la misma organización | rechazo del motor con «pertenece a otro asset»; sin registros parciales, estado previo idéntico, E nulo, sin evaluación de impacto, aprobación ni publicación | rechazada: la atribución directa t4 pertenece a otro asset (au) y no al asset raíz a1; E nulo en la pieza y la versión de destino | DETECTADA |
| K47-A59 | IG5-102 (rechazo del motor con «pertenece a otro uploader») | válido: fixture de reutilización exacta, 0 violaciones del auditor y E completo | la atribución directa pertenece a otro uploader | rechazo del motor con «pertenece a otro uploader»; sin registros parciales, estado previo idéntico, E nulo, sin evaluación de impacto, aprobación ni publicación | rechazada: la atribución directa t4 pertenece a otro uploader (Z) y no al uploader original U; E nulo en la pieza y la versión de destino | DETECTADA |
| K47-A60 | IG5-102 (rechazo del motor con «no coincide con el uploader») | válido: fixture de reutilización exacta, 0 violaciones del auditor y E completo | el actor del evento de carga no coincide con el uploader declarado | rechazo del motor con «no coincide con el uploader»; sin registros parciales, estado previo idéntico, E nulo, sin evaluación de impacto, aprobación ni publicación | rechazada: el actor del evento original de carga de a1 no coincide con el uploader del asset raíz; E nulo en la pieza y la versión de destino | DETECTADA |
| K47-A61 | IG5-102 (rechazo del motor con «otra versión de copy») | válido: fixture de reutilización exacta, 0 violaciones del auditor y E completo | el evento de carga es correcto pero está asociado a otra versión de copy | rechazo del motor con «otra versión de copy»; sin registros parciales, estado previo idéntico, E nulo, sin evaluación de impacto, aprobación ni publicación | rechazada: el evento original de carga de a1 corresponde a otra versión de copy; la pieza y la versión de copy del asset de origen no coinciden con su evento pro; E nulo en la pieza y la versión de destino | DETECTADA |
| K47-A62 | IG5-102 (rechazo del motor con «otra pieza») | válido: fixture de reutilización exacta, 0 violaciones del auditor y E completo | el evento de carga es correcto pero está asociado a otra pieza | rechazo del motor con «otra pieza»; sin registros parciales, estado previo idéntico, E nulo, sin evaluación de impacto, aprobación ni publicación | rechazada: el evento original de carga de a1 pertenece a otra pieza; la pieza y la versión de copy del asset de origen no coinciden con su evento propio; E nulo en la pieza y la versión de destino | DETECTADA |
| K47-A63 | IG5-102 (rechazo del motor con «no tiene membresía activa») | válido: fixture de reutilización exacta, 0 violaciones del auditor y E completo | el uploader original no tiene membresía activa | rechazo del motor con «no tiene membresía activa»; sin registros parciales, estado previo idéntico, E nulo, sin evaluación de impacto, aprobación ni publicación | rechazada: el uploader original de a1 no tiene membresía activa; E nulo en la pieza y la versión de destino | DETECTADA |
| K47-A64 | IG5-102 (rechazo del motor con «no existe la atribución directa») | válido: fixture de reutilización exacta, 0 violaciones del auditor y E completo | evento de carga y uploader correctos pero la atribución directa no existe | rechazo del motor con «no existe la atribución directa»; sin registros parciales, estado previo idéntico, E nulo, sin evaluación de impacto, aprobación ni publicación | rechazada: no existe la atribución directa del uploader original del asset raíz a1; E nulo en la pieza y la versión de destino | DETECTADA |
| K47-A65 | IG5-102 (rechazo del motor con «corresponde a otro asset») | válido: fixture de reutilización exacta, 0 violaciones del auditor y E completo | la referencia al evento de carga se intercambia con la de otro asset después de construir la cadena | rechazo del motor con «corresponde a otro asset»; sin registros parciales, estado previo idéntico, E nulo, sin evaluación de impacto, aprobación ni publicación | rechazada: el evento original de carga corresponde a otro asset (ax) y no al asset raíz a1; el evento original de carga de a1 corresponde a otra versión de copy;; E nulo en la pieza y la versión de destino | DETECTADA |
| M-22 | K48 (IE-10) | válido (K48 APRUEBA) | Se invierte un bit en una copia temporal del original y se calcula su SHA-256 | rechazo por K48 | RECHAZADA por K48 | DETECTADA |

**Controles estructurales de K45 (C01 a C15) y su cobertura.** Se evalúan sobre las relaciones reales del modelo (joins por identificador), nunca por coincidencia de texto. Casos positivos: base: 0 violaciones; evento inherited_contributor sobre copy: 0 violaciones; segunda reutilización del mismo asset (a1 → a2 → a3): 0 violaciones.

| Control | Condición | Mutaciones que lo ejercen |
|---|---|---|
| C01 | la organización del evento, de la fuente y de la atribución coincide | K45-M06, K45-M20 |
| C02 | la pieza declarada por el evento y por la atribución coincide y es la de la versión atribuida | K45-M07, K45-M17, K45-M18 |
| C03 | la versión exacta de la fuente existe y pertenece a esa pieza | K45-M13, K45-M15, K45-M16 |
| C04 | el tipo de contribución corresponde al tipo de fuente (matriz autorizada) | K45-M01, K45-M02, K45-M03, K45-M04, K45-M10, K45-M14 |
| C05 | origin_kind corresponde a la columna física de origen (una sola columna tipada) | K45-M23 |
| C06 | la columna de origen apunta a una fila de la tabla correcta | K45-M24 |
| C07 | el actor de la atribución coincide con el actor del evento | K45-M05 |
| C08 | el evento corresponde a la versión exacta de origen de la atribución | K45-M08, K45-M22 |
| C09 | el campo material existe en esa versión y fuente | K45-M09 |
| C10 | la atribución heredada conserva fuente, evento, persona, campo y versión original | K45-M12 |
| C11 | la relación de herencia apunta a una atribución anterior de la misma cadena | K45-M21 |
| C12 | el asset original fue cargado por el uploader registrado | K45-M25 |
| C13 | el asset reutilizado existe y corresponde a la versión exacta de copy que lo usa | K45-M19, K45-M27 |
| C14 | el reutilizador no se convierte en uploader | K45-M11 |
| C15 | ninguna referencia cruza organizaciones o piezas | K45-M26 |

**Escenarios estructurales de K47 (12) y comprobaciones U, S, X y R.** Cada escenario ejecuta operaciones del motor sobre atribuciones individuales y un auditor independiente compara el estado anterior y el posterior; el resultado observado se compara con el esperado.

| ID | Escenario | Pasos auditados | Violaciones del auditor | Aserciones (esperado = observado) | Resultado |
|---|---|---|---|---|---|
| EA-A | conservación por sustitución | 3 | ninguna | E tras la sustitución contiene a A y a B → A, B; la atribución de A sigue activa tras la sustitución → activa; resolución independiente válida aceptada → True; E tras la resolución es solo B → B; la atribución de A queda histórica → historica | APROBADO |
| EA-B | conservación por eliminación | 3 | ninguna | E tras la eliminación contiene a A y a B → A, B; A permanece activa provisionalmente → activa; B se incorpora con atribución directa → True; el campo eliminado conserva su historial → True; una eliminación no material no incorpora al actor → False | APROBADO |
| EA-C | varias atribuciones de una persona | 4 | ninguna | la resolución válida se acepta → True; la atribución de headline de A pasa a histórica → historica; A permanece en E por su atribución activa de body → True; la atribución de body sigue activa → True | APROBADO |
| EA-D | varias fuentes | 4 | ninguna | la resolución del copy se acepta → True; la atribución del copy pasa a histórica → historica; A permanece en E por el brief → True; la atribución de A en el brief sigue activa → True | APROBADO |
| EA-E | resolución rechazada | 3 | ninguna | la resolución rechazada no cambia la atribución → activa; E no cambia → A, B; el resultado de la resolución es rechazada y definitivo → rechazada | APROBADO |
| EA-F | resolución inválida por evidencia de otra versión | 3 | ninguna | la resolución con evidencia de otra versión no se aplica → False; la atribución permanece activa → activa; E no cambia → A, B | APROBADO |
| EA-G | herencia | 4 | ninguna | v4 conserva las atribuciones activas de A y B como heredadas → ('A', 'headline', 'heredada'), ('B', 'body', 'heredada'); quien crea una versión sin cambio no se incorpora → False; todas las atribuciones anteriores siguen existiendo → True | APROBADO |
| EA-H | cadena incompleta | 1 | ninguna | la versión importada sin evidencia no produce un E completo → False; no se entrega un E parcial → None; la versión con procedencia sí produce E → A | APROBADO |
| EA-I | clasificación modificada | 3 | ninguna | la clasificación cambia → sustituido; E no cambia → A, B; la historia se conserva y se agrega un registro → 3; ninguna atribución quedó histórica → True | APROBADO |
| EA-J | resolución y contribución independiente | 3 | ninguna | la resolución se acepta → True; la atribución de headline de A queda histórica → historica; A permanece en E por su carga del asset → True; la atribución de asset de A sigue activa → True | APROBADO |
| EA-K | fuentes paralelas | 4 | ninguna | E de la adaptación incorpora copy, brief, promoción, asset y maestra → A, C, Pm, U, W; quien reutiliza el asset (W) no es el uploader del asset → U; el asset reutilizado conserva el evento del uploader original → True | APROBADO |
| EA-L | sin resolutor elegible | 3 | ninguna | no existe resolutor elegible → (vacío); la resolución no se aplica → False; la atribución permanece activa → activa; E no excluye a A → True | APROBADO |
| EA-U | uniformidad entre copy, brief y promoción | 0 | ninguna | las tres fuentes producen la misma firma estructural → True | APROBADO |
| EA-S | independencia de la similitud textual | 0 | ninguna | el resultado no depende de la similitud del texto → True | APROBADO |
| EA-X | resolutor no independiente rechazado | 3 | ninguna | el editor que ejecutó la sustitución no puede resolver → False; la atribución permanece activa → activa; E no cambia → A, B | APROBADO |
| EA-R | cada regla R1 a R9 impide resolver | 0 | ninguna | R1: el resolutor que incumple R1 no puede resolver → False; R1: el motivo de rechazo incluye R1 → True; R1: la atribución permanece activa → activa; R2: el resolutor que incumple R2 no puede resolver → False; R2: el motivo de rechazo incluye R2 → True; R2: la atribución permanece activa → activa; R3: el resolutor que incumple R3 no puede resolver → False; R3: el motivo de rechazo incluye R3 → True; R3: la atribución  | APROBADO |
| EA-RS | resoluciones inmutables y cadena de reconsideración | 6 | ninguna | la primera resolución sin evidencia nace rechazada y definitiva → rechazada, False; la reconsideración crea un registro nuevo que referencia al anterior → r1, aceptada, True; el registro rechazado original se conserva íntegro → {'id': 'r1', 'resultado': 'rechazada', 'seq': 20, 'motivos': ['V11'], 'version': 'v2', 'version_origen': 'v1', 'previo': None, 'previo_sello': None, 'org': 'X', 'atribucion': 't3', 'afectado': | APROBADO |

**Invariantes del auditor de K47 (I1 a I28).**

| Invariante | Qué comprueba | Mutaciones que lo ejercen |
|---|---|---|
| I1 | toda atribución activa anterior sigue activa en la versión nueva (ninguna clasificación retira) | K47-M01, K47-M02, K47-M03, K47-A11, K47-A12 |
| I2 | el actor se incorpora solo si hay contribución material | K47-M04 |
| I3 | una resolución aceptada retira exactamente la atribución referenciada | K47-M06, K47-M17, K47-M24 |
| I4 | una resolución aceptada cumple todas sus condiciones y R1 a R9 recalculadas por el auditor | K47-M27, K47-M28, K47-M29, K47-M30, K47-M31, K47-M32, K47-M33, K47-M34, K47-M35, K47-M36 |
| I5 | una resolución rechazada o inválida no cambia atribuciones, estados ni E | K47-M05, K47-M18, K47-M19 |
| I6 | la evidencia histórica se conserva | K47-M21, K47-A13 |
| I7 | E del motor igual a E recalculado y no sale quien conserva otra atribución activa | K47-M10, K47-M15, K47-M16, K47-M25 |
| I8 | una cadena incompleta no produce un E presentado como completo | K47-M09, K47-M22, K47-M23 |
| I9 | brief, promoción y copy aplican la misma regla | K47-M11, K47-M12 |
| I10 | versiones, atribuciones, eventos y estados anteriores no se reescriben; la versión nueva hereda todo lo activo | K47-M07, K47-M08, K47-M20, K47-M26 |
| I11 | el resultado no depende de la similitud del texto | K47-M13 |
| I12 | un cambio de clasificación no altera atribuciones ni historia | K47-M14 |
| I13 | inmutabilidad de las resoluciones: ninguna se modifica, reemplaza ni elimina; sello SHA-256 coincidente; resultado definitivo | K47-R01, K47-R02, K47-R03, K47-R04, K47-R06, K47-R07, K47-R08 |
| I14 | cadena de reconsideración: sin ciclos, anterior existente, de la misma atribución, rechazada, anterior en el tiempo y con sello intacto | K47-R11, K47-R12 |
| I15 | cada baja histórica cita una resolución aceptada de esa atribución exacta; una sola aceptada por atribución | K47-R05, K47-R09, K47-R10 |
| I16 | cada asset usado tiene uploader, evento de carga y atribución del uploader | K47-A01, K47-A02 |
| I17 | el reutilizador no sustituye al uploader original y su evento de reutilización está registrado | K47-A06, K47-A07, K47-A31 |
| I18 | el asset corresponde a la versión exacta de copy que lo usa | K47-A05 |
| I19 | cadena de reutilización sin ciclos, con origen existente y misma organización y pieza | K47-A03, K47-A04, K47-A08, K47-A09, K47-A10 |
| I20 | completitud del arte y declaración explícita de no_aplica | K47-A14, K47-A16, K47-A53 |
| I21 | E incluye a los contribuyentes del arte exacto | K47-A15 |
| I22 | identidad del uploader: organización y membresía activa | K47-A17, K47-A18 |
| I23 | evento de carga: organización, pieza, asset exacto, versión de asset, versión de copy, actor y actor autenticado | K47-A19, K47-A20, K47-A21, K47-A22, K47-A49, K47-A52 |
| I24 | atribución directa del uploader ligada a organización, pieza, versión de copy, asset, versión de asset y evento | K47-A23, K47-A24, K47-A25 |
| I25 | evento de reutilización: organización, pieza, actor, asset, versión de asset y de copy, evento propio, membresía | K47-A26, K47-A27, K47-A28, K47-A29, K47-A30, K47-A50, K47-A51 |
| I26 | atribuciones heredadas de asset con antecesor verificable en la cadena | K47-A32 |
| I27 | identidad exacta del origen: el evento de reutilización y el asset reutilizado referencian el asset, la versión, el evento de carga, el uploader y la atribución originales por identificador, con organización, pieza y actor autenticado coincidentes | K47-A33, K47-A34, K47-A35, K47-A36, K47-A37, K47-A38, K47-A39, K47-A40, K47-A41, K47-A44, K47-A45, K47-A46, K47-A47 |
| I28 | integridad de la cadena de origen: sin registros intercambiados y con vínculo íntegro al evento original de carga | K47-A42, K47-A43, K47-A48 |

**Casos positivos de arte (P01 a P20), pruebas adversariales e intentos directos contra el registro de resoluciones.**

| ID | Caso | Violaciones del auditor | Aserciones | Resultado |
|---|---|---|---|---|
| P01 | asset nuevo con uploader y evento de carga correctos | ninguna | 5 | APRUEBA |
| P02 | asset reutilizado con uploader y reutilizador diferenciados | ninguna | 5 | APRUEBA |
| P03 | asset modificado con conservación de atribuciones | ninguna | 4 | APRUEBA |
| P04 | versión sin arte declarada no_aplica | ninguna | 3 | APRUEBA |
| P05 | asset sustituido con conservación provisional | ninguna | 3 | APRUEBA |
| P06 | asset eliminado con historial conservado | ninguna | 3 | APRUEBA |
| P07 | reutilización encadenada completa | ninguna | 3 | APRUEBA |
| P08 | uploader válido con organización, pieza, evento y versión exactos | ninguna | 11 | APRUEBA |
| P09 | uploader original y reutilizador diferentes, ambos atribuidos | ninguna | 6 | APRUEBA |
| P10 | mismo asset reutilizado en dos versiones de copy con eventos independientes | ninguna | 5 | APRUEBA |
| P11 | atribución heredada válida con antecesor verificable | ninguna | 4 | APRUEBA |
| P12 | uploader original conservado tras modificar el asset | ninguna | 4 | APRUEBA |
| P13 | cadena de reutilización válida de más de dos versiones | ninguna | 4 | APRUEBA |
| P14 | ausencia real de arte declarada no_aplica | ninguna | 4 | APRUEBA |
| P15 | reutilización válida con identidad exacta del origen | ninguna | 15 | APRUEBA |
| P16 | dos assets distintos con el mismo número de versión | ninguna | 6 | APRUEBA |
| P17 | dos reutilizaciones del mismo asset original en dos piezas | ninguna | 29 | APRUEBA |
| P18 | cadena de tres niveles con eventos propios y uploader original conservado | ninguna | 7 | APRUEBA |
| P19 | reutilización y modificación posterior del asset reutilizado | ninguna | 6 | APRUEBA |
| P20 | motor y auditor reconstruyen la misma cadena sin compartir funciones | ninguna | 5 | APRUEBA |
| P21 | reutilización válida con asset raíz, versión, evento de carga, uploader y atribución exactos | ninguna | 9 | APRUEBA |
| P22 | dos assets de la misma organización y pieza con el mismo número de versión | ninguna | 20 | APRUEBA |
| P23 | dos eventos de carga válidos de assets distintos: intercambiarlos provoca rechazo | ninguna | 4 | APRUEBA |
| P24 | cadena de tres niveles con evento de carga y uploader de la raíz | ninguna | 11 | APRUEBA |
| P25 | reutilización válida con el auditor independiente coincidente | ninguna | 12 | APRUEBA |
| P26 | evento de carga y atribución válidos pero de otro asset: rechazo sin escritura | ninguna | 3 | APRUEBA |

| Prueba adversarial | El motor acepta | El auditor detecta | E bloqueado | Impacto falla | No publica | Resultado |
|---|---|---|---|---|---|---|
| ADV1: uploader de otra organización | sí | sí (I20, I22, I8) | sí | sí | sí | APRUEBA |
| ADV2: evento de carga de otra pieza | sí | sí (I20, I23, I8) | sí | sí | sí | APRUEBA |
| ADV3: evento de reutilización de otro actor | sí | sí (I17, I20, I25, I27, I8) | sí | sí | sí | APRUEBA |
| ADV4: atribución heredada sin antecesor | sí | sí (I20, I26, I8) | sí | sí | sí | APRUEBA |
| ADV5: uploader con membresía inactiva | sí | sí (I20, I22, I8) | sí | sí | sí | APRUEBA |
| ADV6: asset diferente con el mismo número de versión | sí | sí (I20, I27, I8) | sí | sí | sí | APRUEBA |
| ADV7: evento de carga diferente del mismo uploader | sí | sí (I20, I27, I8) | sí | sí | sí | APRUEBA |
| ADV8: versión de asset diferente del mismo origen | sí | sí (I20, I27, I8) | sí | sí | sí | APRUEBA |
| ADV9: asset de otra pieza con el mismo número de versión | sí | sí (I20, I27, I8) | sí | sí | sí | APRUEBA |
| ADV10: asset de otra organización con identificadores de versión coincidentes | sí | sí (I20, I27, I8) | sí | sí | sí | APRUEBA |
| ADV11: evento de carga de otro asset de la misma organización y pieza (A54) | sí | sí (I16, I20, I23, I24, I27, I28, I8) | sí | sí | sí | APRUEBA |
| ADV12: evento de carga de otro asset con el mismo número de versión (A55) | sí | sí (I16, I20, I23, I24, I27, I28, I8) | sí | sí | sí | APRUEBA |
| ADV13: atribución directa de otro evento de carga del mismo asset (A57) | sí | sí (I16, I20, I24, I8) | sí | sí | sí | APRUEBA |
| ADV14: atribución directa de otro asset de la misma organización (A58) | sí | sí (I16, I17, I18, I20, I24, I8) | sí | sí | sí | APRUEBA |
| ADV15: actor del evento de carga distinto del uploader declarado (A60) | sí | sí (I16, I20, I23, I27, I8) | sí | sí | sí | APRUEBA |
| ADV16: referencia al evento de carga intercambiada con otro asset (A65) | sí | sí (I16, I20, I23, I24, I27, I28, I8) | sí | sí | sí | APRUEBA |

| Prueba de atomicidad de la reutilización | Falla con ReutilizacionInvalida y no deja registros parciales |
|---|---|
| el asset de origen no existe | sí |
| el origen no tiene evento de carga | sí |
| el uploader original no tiene membresía activa | sí |
| no existe la atribución directa del uploader original | sí |
| el origen pertenece a otra organización | sí |
| la pieza del origen no coincide con su evento | sí |
| el reutilizador no es miembro activo | sí |
| el identificador del asset reutilizado ya existe | sí |
| A54: el evento original de carga pertenece a otro asset de la misma organización y pieza | sí |
| A55: el evento original de carga pertenece a otro asset con el mismo número de versión | sí |
| A56: el evento original de carga es el de otra versión del mismo asset raíz | sí |
| A57: la atribución directa del uploader pertenece a otro evento de carga del mismo asset | sí |
| A58: la atribución directa pertenece a otro asset de la misma organización | sí |
| A59: la atribución directa pertenece a otro uploader | sí |
| A60: el actor del evento de carga no coincide con el uploader declarado | sí |
| A61: el evento de carga es correcto pero está asociado a otra versión de copy | sí |
| A62: el evento de carga es correcto pero está asociado a otra pieza | sí |
| A63: el uploader original no tiene membresía activa | sí |
| A64: evento de carga y uploader correctos pero la atribución directa no existe | sí |
| A65: la referencia al evento de carga se intercambia con la de otro asset después de construir la cadena | sí |

| Intento directo | Rechazado con ResolucionInmutable y registro intacto |
|---|---|
| asignar un campo de una fila | sí |
| eliminar un campo de una fila | sí |
| actualizar una fila | sí |
| reemplazar una fila con el mismo ID | sí |
| eliminar una resolución | sí |
| vaciar el registro | sí |
| agregar con un ID existente | sí |
| modificar la evidencia histórica anidada | sí |
| volver a aplicar una resolución con el mismo ID | sí |

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

**Auditoría final (14 verificaciones).**

| # | Verificación | Comprobaciones | Resultado |
|---|---|---|---|
| 1 | Ejecutar el verificador documental | K01 | OK (verificado documentalmente) |
| 2 | Ejecutar todas las mutaciones negativas | K42 | OK (verificado documentalmente) |
| 3 | Cada defecto es detectado | K42 | OK (verificado documentalmente) |
| 4 | 28 controles de auditoría | K40 | OK (verificado documentalmente) |
| 5 | SHA-256 de v3.3 calculado sobre el original (o limitación real) | K48 | OK (verificado documentalmente) |
| 6 | Reconstrucción de contribuyentes por campo | K13, K38, K47, K49, K52 | OK (verificado documentalmente) |
| 7 | Independencia de las resoluciones | K46, K49, K52 | OK (verificado documentalmente) |
| 8 | Relaciones y claves compuestas | K44, K45, K52 | OK (verificado documentalmente) |
| 9 | Escenarios de G-1, G-5 y G-10 | K39, K13, K49 | OK (verificado documentalmente) |
| 10 | IDs y referencias | K02, K03, K04, K05, K06, K07, K08 | OK (verificado documentalmente) |
| 11 | 76 subfases | K18 | OK (verificado documentalmente) |
| 12 | 17 claves de permisos y 13 transiciones T-02 | K19, K20 | OK (verificado documentalmente) |
| 13 | Decisiones pendientes sin alterar | K21 | OK (verificado documentalmente) |
| 14 | Coherencia entre los cinco documentos activos | K09, K17, K22, K27 | OK (verificado documentalmente) |

**Criterios binarios de aceptación de la v15 (resultado calculado).**

| Criterio | Condición | Resultado |
|---|---|---|
| K45 | al menos 22 mutaciones, todas detectadas | 27/27 detectadas: CUMPLE |
| K46 | al menos 12 mutaciones, todas detectadas | 12/12 detectadas: CUMPLE |
| K47 (mutaciones previas) | al menos 26 mutaciones, todas detectadas | 36/36 detectadas: CUMPLE |
| K47 resoluciones inmutables (R01 a R12) | al menos 12 mutaciones, todas detectadas | 12/12 detectadas: CUMPLE |
| K47 procedencia del arte de la v10 (A01 a A16) | al menos 14 mutaciones, todas detectadas | 16/16 detectadas: CUMPLE |
| K47 identidad exacta de assets de la v11 (A17 a A32 y A49 a A53) | al menos 16 mutaciones, todas detectadas, con procedencia incompleta y E no completo | 21/21 detectadas: CUMPLE |
| K47 identidad exacta del asset de origen de la v12 (A33 a A48) | al menos 16 mutaciones, todas detectadas, con procedencia incompleta y E no completo | 16/16 detectadas: CUMPLE |
| K47 validación previa del origen de la v13 (A54 a A65) | las 12 mutaciones detectadas: rechazo por ReutilizacionInvalida con la relación identificada, sin registros parciales, estado previo idéntico, procedencia no completa, E nulo y sin evaluación de impacto, aprobación ni publicación | 12/12 detectadas: CUMPLE |
| Mutaciones estructurales FK01 a FK41 | las 41 mutaciones de K32, K44, K45 y K55 detectadas por su verificador, sin exclusiones generales de columnas source_* | 41/41 detectadas: CUMPLE |
| K56 cadena completa (CHAIN-01 a CHAIN-24) | las 24 mutaciones de eslabones detectadas con el eslabón identificado, sin registros parciales y con E bloqueado | 24/24 detectadas: CUMPLE |
| K56 atribuciones y resoluciones (ATTR-01 a ATTR-12) | las 12 mutaciones detectadas por el auditor independiente | 12/12 detectadas: CUMPLE |
| K56 asset_version del evento propio (AV-01 a AV-08) | las 8 mutaciones detectadas con el eslabón, el evento y el campo identificados | 8/8 detectadas: CUMPLE |
| K56 campo del evento propio (CF-01 a CF-08) | las 8 mutaciones detectadas con el eslabón, el evento y el campo identificados | 8/8 detectadas: CUMPLE |
| K56 asset_version y campo combinados (AC-01 a AC-06) | las 6 mutaciones detectadas, sin que una excepción ajena cuente como detección | 6/6 detectadas: CUMPLE |
| K56 mutaciones del código del modelo (K56-M01 a K56-M12) | cada defensa nueva degradada es detectada por al menos una prueba | 12/12 detectadas: CUMPLE |
| K57 mutaciones documentales de trazabilidad y de identidad de controles (K57-D01 a K57-D12) | las mutaciones del documento detectadas por K55, K57 o K58 | 12/12 detectadas: CUMPLE |
| K56 baterías de la v15 | AP 8/8 (relaciones válidas aceptadas sin falsos positivos), ADV15 8/8 (el motor forzado acepta y el auditor detecta asset_version y campo) y AT15 8/8 (instantánea completa en ocho momentos de fallo) | AP 8/8; ADV15 8/8; AT15 8/8: CUMPLE |
| K56 baterías ejecutadas | ADVC 24/24 (el motor forzado acepta y el auditor detecta), AT14 11/11, E14 6/6 y auditor sin funciones del motor | ADVC 24/24; AT14 11/11; E14 6/6; auditor: CUMPLE |
| Escenarios estructurales K47 | los 12 escenarios A a L aprobados sobre datos estructurados | 12/12 aprobados; U, S, X, R y RS: aprobados |
| Casos positivos de arte | los 26 casos positivos de arte aprobados (P01 a P26): reutilización exacta con cadena completa, dos assets con igual número de versión, dos reutilizaciones del mismo original, intercambio de eventos de carga válidos (rechazado), cadena de tres niveles, reutilización con modificación posterior, coincidencia con el auditor independiente sin funciones compartidas y rechazo sin escritura de un evento y una atribución válidos de otro asset | 26/26 aprobados: CUMPLE |
| Inmutabilidad del registro | los 9 intentos directos de alterar el registro de resoluciones se rechazan y lo dejan idéntico | 9/9 rechazados: CUMPLE |
| Pruebas adversariales | al menos 5 pruebas adversariales nuevas en las que el motor acepta, el auditor detecta y el sistema final bloquea E, la evaluación de impacto y la publicación | 16/16 aprobadas (11 nuevas): CUMPLE |
| Atomicidad de la reutilización | una reutilización con un elemento obligatorio ausente falla y no deja registros parciales | 20/20 aprobadas: CUMPLE |
| Independencia del auditor | el auditor reconstruye la identidad desde las instantáneas sin llamar a funciones del motor (inspección del código) | CUMPLE: ninguna función compartida |
| Casos positivos y falsos positivos | fixtures válidos aceptados y ninguna mutación con estado inicial inválido | CUMPLE; 222/222 mutaciones del modelo con estado inicial válido y cambio efectivo |
| Regresión | todas las comprobaciones y las mutaciones M-01 a M-25 anteriores pasan | 148/148 mutaciones anteriores; CUMPLE |
| Consistencia documental | cero contradicciones, cifras y estados coherentes | OK (verificado documentalmente) |
| Cobertura | reglas relevantes y controles estructurales cubiertos | OK (verificado documentalmente) |
| Integridad histórica | documentos protegidos sin alteración | OK (verificado documentalmente) |
| Permisos | 17 claves conservadas | OK (verificado documentalmente) |
| Workflow | 13 transiciones conservadas | OK (verificado documentalmente) |
| Roadmap | 76 subfases conservadas | OK (verificado documentalmente) |
| Hash | verificado sobre el original o declarado pendiente | OK (verificado documentalmente) |
| SQL e infraestructura | ninguna ejecución | OK (verificado documentalmente) |
| Fase 1 | no iniciada ni autorizada | OK (verificado documentalmente) |
| Alcance Git | solo docs/fase0/ | Fuera del alcance del verificador: se comprueba con git diff en la publicación |
<!-- VERIFICADOR:FIN -->

## 4. Errores hallados y corregidos durante la v15

| Error | Corrección |
|---|---|
| La v14 aceptaba un `asset_version` o un `campo` corruptos en el evento propio de cualquier eslabón y guardaba la versión del origen en el evento del destino | `Motor._chk_asset_version` y `Motor._chk_campo` validan por identidad exacta antes de escribir; AV-01 a AV-08, CF-01 a CF-08 y AC-01 a AC-06 |
| Al desarrollar la v15, K47-A29 falló porque el nuevo mensaje de rechazo cambió una condición que la prueba histórica exigía | Se restauró el texto «otra versión de asset» en `_id_reutilizacion` y `_hall_identidad`, sin tocar la prueba histórica |
| Al desarrollar la v15, AT15 aprobaba 2 de 8 porque los datos derivados se calculaban con el fallo inyectado ya activo | Los datos derivados se calculan antes de activar el fallo y se recalculan sin él tras la restauración |
| El identificador K55 estaba asignado a dos controles del verificador desde la v12 | El segundo pasa a K55-V12 sin eliminar ninguna condición; K58 exige identificadores únicos y K57-D09 reintroduce el duplicado |

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


## Nota de estado V20 (2026-11-19) — bloque uniforme en los cinco documentos activos

Esta nota no modifica ni reemplaza lo anterior; distingue seis estados que no deben confundirse.

| Estado | Situación |
|---|---|
| Histórico | Fase 0 v3.3 conservada como línea base documental (SHA-256 b5dccdc7…c1da, sin cambio); el diseño complementario vigente es la revisión v15; las notas V16 a V19 son trabajo de auditoría documental. |
| Publicación | Rama `audit/fase0-v19-review`, commit `c6ef74be4db185ac3e4fd36810f24619e6f51fcf` (V16–V19, padre `6a1af2424ef39e0960b8f7e09d4e19ec52e6f046`). `main` permanece en V16 (`6a1af24`). El trabajo V20 (`expediente_final_v16_v19/`) está solo en el árbol local, sin commit. Sin pull request ni merge. |
| Auditoría | Cierre integral V16–V20 (segunda pasada V20 con prompt de reconciliación) documentado en `expediente_final_v16_v19/` (231 reglas, 780 escenarios, 22 funciones / 366 casos, matriz C01–C30). Solo documental y en modelo en memoria. |
| Aceptación del propietario | Ni V15–V20, ni la Adenda v9 (PO-05), ni G-1, G-5 y G-10 están aceptados; todo sigue pendiente del propietario. |
| Integración | No integrado con la vista previa privada. |
| Producción | Sin despliegue, sin Supabase, sin migraciones ni esquema físico; solo un fixture SQL de prueba ejecutado en un PostgreSQL temporal aislado (`expediente_final_v16_v19/PE_POSTGRESQL_V20/`); Fase 1 NO INICIADA / NO AUTORIZADA. |

Limitaciones vigentes: 153 reglas condicionadas por diseño no aceptado (G-1, G-5, G-10); las 5 reglas antes con evidencia insuficiente (IG1-05, IG1-06, IG1-10, IG1-21, IG5-36) pasaron a B: PE-01 a PE-05 se ejecutaron en un PostgreSQL 16 temporal con un fixture derivado del diseño (63/63 PASS), sin esquema físico aprobado ni Supabase; 12 escenarios parciales; sin validación contra un esquema físico real, RLS, concurrencia ni Supabase; HV-02 (PO-05 «v3» frente a Adenda v9) no verificable sin confirmación del propietario; decisiones reservadas abiertas (RP-01, G-9, P-01 a P-05, P-10, OD-13, DEP-RET-01, DG-09, DG-12, DG-16, DG-18, DG-19, DG-20).
