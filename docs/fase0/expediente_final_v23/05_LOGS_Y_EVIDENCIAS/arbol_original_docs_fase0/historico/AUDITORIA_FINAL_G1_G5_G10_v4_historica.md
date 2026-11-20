---
name: auditoria_final_g1_g5_g10
description: Auditoría final de la revisión v4 de G-1, G-5 y G-10 (hallazgo, causa raíz, corrección, reglas, pruebas, verificador y resultados, riesgos residuales)
---

# AUDITORÍA FINAL — G-1, G-5 Y G-10 (revisión v4)

Documental. Las pruebas son diseños, no ejecuciones; el diseño no está validado técnicamente.

## 0. Estado por nivel

| Nivel | Estado | Alcance |
|---|---|---|
| 1. Fase 0 v3.3 | COMPLETADA Y ACEPTADA COMO LÍNEA BASE DOCUMENTAL, CON LIMITACIONES DOCUMENTADAS | No se reabre ni se modifica; SHA-256 `b5dccdc73a8103966ab1e1b1e84b2e7ead68cd736fba666ec71d0e790d51c1da` sin cambio |
| 2. Diseño técnico complementario (G-1, G-5, G-10, v4) | DISEÑO TÉCNICO DOCUMENTAL CORREGIDO Y PREPARADO PARA ACEPTACIÓN FORMAL, CON LIMITACIONES DOCUMENTADAS | Pendiente de aceptación formal del propietario; no validado técnicamente; la independencia de G-5 depende de DT-01 (T-04) |
| 3. Fase 1 | NO INICIADA / NO AUTORIZADA | Requiere autorización expresa; el diseño complementario no la concede |


## 1. Hallazgos, causa raíz y corrección

| Hallazgo | Problema | Causa raíz | Corrección (resumen) | Referencia | Reglas | Pruebas |
|---|---|---|---|---|---|---|
| H-01 Orden de creación | impact_evaluations (5.4) tenía FK a approvals, que se crea en 6.5: una migración en el orden de la v3 falla. | Se revisó solo la tabla de migración y no el orden de dependencias completo | Alternativa B: impact_evaluations y record_impact_evaluation pasan a 6.5, después de approvals. Se descartó A (approvals mínima antes) por crear una tabla parcial y C (ot… | Spec 7.17 y 14.1 a 14.5; roadmap 3 | IM-01, IM-02, IM-03, IM-04, IM-05, IM-06, IM-07, IM-08, IM-09, IM-10, IM-11, IM-12, IS-01 | T-153 a T-164 |
| H-02 T-04 y contribuyentes | T-04 no estaba recuperada ni definida de forma única; DG-17 la usaba sin distinguir figuras. | T-04 nunca aprobada y DG-17 sin definición única | T-04 recuperada: no aprobada en v3.3. Definición única en 4.4.3 que distingue autoría, contribución material, intervención administrativa, revisión, aprobación y operació… | Spec 4.4.3 | IE-04, IG5-23, IG5-32, IG5-33, IG5-35, IG5-38, IG5-40, IG5-41, IG5-42, IG5-43, IG5-44, IG5-45, IG5-46, IG5-47, IG5-48 | T-165 a T-178 |
| H-03 Estado de Fase 0 | La v3 mezclaba el estado de Fase 0 v3.3 con el del diseño complementario. | Se mezclaron tres estados distintos en una sola frase | Tres niveles: Fase 0 v3.3 aceptada como línea base; diseño complementario pendiente de aceptación formal; Fase 1 no iniciada. v3.3 y su SHA no se tocan.… | Spec 15 y 15.1; los cinco documentos | IE-01, IE-02, IE-03, IE-04 | T-179 a T-182 |
| H-04 Guarda db_txid | La guarda db_txid podía confundirse con un identificador de intento y no declaraba amenazas ni límites. | El identificador de transacción se trató como identidad del intento | db_txid más attempt_nonce uuid generado por el servidor (trigger, UNIQUE, sin SELECT para roles de aplicación); guarda de ocho condiciones; comparación de tres alternativ… | Spec 5.11 | IG10-08, IG10-21, IG10-22, IG10-23, IG10-24, IG10-25, IG10-29, IG10-30, IG10-31, IG10-32, IG10-33, IG10-34, IG10-35, IG10-36, IG10-37, IS-02, IS-03, IS-04, IS-05, IS-10, IS-11 | T-183 a T-201 |

## 2. Orden único de creación

Secuencia: **1.8 → 2.x → 3.x → 4.x → 5.1 → 5.3 → 6.x → 6.1 → 6.5 → 6.6 → 8.x**

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
| 19 | 2.x | tabla (estructura) | copy_versions | briefs, creative_pieces |
| 20 | 2.x | tabla (estructura) | ai_runs | profiles |
| 21 | 2.x | tabla (estructura) | ai_prompt_versions | — |
| 22 | 2.x | tabla (estructura) | ai_quotas | — |
| 23 | 2.x | FK diferida | creative_pieces → briefs | creative_pieces, briefs |
| 24 | 2.x | FK diferida | creative_pieces → copy_versions | creative_pieces, copy_versions |
| 25 | 3.x | tabla (estructura) | creative_assets | copy_versions, creative_pieces |
| 26 | 3.x | tabla (estructura) | audit_rubric_versions | — |
| 27 | 3.x | tabla (estructura) | audits | ai_runs, audit_rubric_versions, copy_versions, creative_assets |
| 28 | 3.x | tabla (estructura) | audit_findings | audits |
| 29 | 3.x | FK diferida | copy_versions → creative_assets | copy_versions, creative_assets |
| 30 | 3.x | FK diferida | creative_pieces → creative_assets | creative_pieces, creative_assets |
| 31 | 4.x | tabla (estructura) | promotion_rules | campaigns |
| 32 | 4.x | tabla (estructura) | validation_settings_versions | — |
| 33 | 4.x | FK diferida | audits → validation_settings_versions | audits, validation_settings_versions |
| 34 | 5.1 | columnas | Columnas anulables de reglas (extensión, tono, estructura, CTA) agregadas a channel_rules | channel_rules |
| 35 | 5.3 | tabla (estructura) | piece_classification_events | creative_pieces, memberships |
| 36 | 5.3 | tabla (estructura) | piece_reviewer_assignments | creative_pieces, memberships |
| 37 | 5.3 | función | create_adaptation | creative_pieces, copy_versions, channel_formats |
| 38 | 5.3 | función | version_contributors (interna) | copy_versions, creative_assets, activity_logs |
| 39 | 5.3 | función | eligible_evaluators | piece_reviewer_assignments, memberships, copy_versions, creative_assets |
| 40 | 5.3 | función | propose_independence | piece_classification_events, creative_pieces |
| 41 | 5.3 | función | resolve_independence | piece_classification_events, piece_reviewer_assignments |
| 42 | 5.3 | función | assign_reviewer | piece_reviewer_assignments, memberships |
| 43 | 5.3 | habilitación | Políticas RLS y privilegios de piece_classification_events y piece_reviewer_assignments | tablas y funciones anteriores |
| 44 | 6.x | tabla (estructura) | comments | audit_findings, creative_pieces |
| 45 | 6.x | tabla (estructura) | commercial_block_exceptions | audit_findings, memberships |
| 46 | 6.1 | función | transition_piece_status (T-02 sin la transición a Publicado habilitada) | creative_pieces, comments, memberships |
| 47 | 6.5 | tabla (estructura) | approvals | audits, copy_versions, creative_assets, memberships |
| 48 | 6.5 | tabla (estructura) | impact_evaluations | approvals, copy_versions, creative_assets, creative_pieces, memberships, piece_reviewer_assignments |
| 49 | 6.5 | trigger | BEFORE INSERT sobre approvals: coherencia del arte (4.13) | approvals, creative_assets |
| 50 | 6.5 | función | record_approval (ampliada) | approvals, copy_versions, creative_assets, audits, memberships |
| 51 | 6.5 | función | record_impact_evaluation | impact_evaluations, approvals, piece_reviewer_assignments, memberships |
| 52 | 6.5 | habilitación | Políticas RLS y privilegios de approvals e impact_evaluations | tablas y funciones anteriores |
| 53 | 6.6 | tabla (estructura) | publication_attempts | approvals, copy_versions, creative_pieces, impact_evaluations, memberships |
| 54 | 6.6 | trigger | BEFORE INSERT sobre publication_attempts: db_txid, attempted_at, attempt_nonce, actor (5.11) | publication_attempts |
| 55 | 6.6 | trigger | Sustituye el cuerpo de piece_status_guard por la guarda de ocho condiciones (5.11) | publication_attempts, approvals, impact_evaluations, memberships, creative_pieces |
| 56 | 6.6 | función | transition_piece_status ampliada: habilita la transición a Publicado (#10) | publication_attempts, approvals, impact_evaluations, creative_pieces |
| 57 | 6.6 | habilitación | Políticas RLS y privilegios de publication_attempts y la transición a Publicado | tablas y funciones anteriores |
| 58 | 8.x | tabla (estructura) | performance_metrics | creative_pieces |
| 59 | 8.x | tabla (estructura) | ab_tests | creative_pieces, performance_metrics |

## 3. Verificador documental

| Concepto | Detalle |
|---|---|
| Nombre | g_verify.py con g_verify_v4.py, v4_plan.py y v4_check.py (herramienta de verificación; no es código de aplicación y no se publica en el repositorio, que solo admite .md) |
| Comando | python3 g_verify.py (desde el directorio de trabajo; mermaid 10 y jsdom para el parseo de diagramas) |
| Número de comprobaciones | 36 |
| Errores finales | 0 |
| Errores hallados y corregidos | Orden con falso ciclo por FK diferidas; attempt_nonce ausente del modelo; referencia errónea en 4.4.3; control negativo del diagrama que no permutaba nodos; pruebas de concurrencia sin actores; IS-11 sin prueba positiva; hash del registro de la Adenda v9 en la tabla de línea base (en la v3 era el del registro de G; corregido con el hash original al iniciar) |
| Limitaciones | Heurísticas sobre texto; no ejecuta SQL ni valida PostgreSQL; el renderizado visual de Mermaid no se verificó; los controles negativos cubren los defectos de H-01 y no todos los posibles |

### Resultados

| Verificación | Resultado | Descripción |
|---|---|---|
| V01 | OK | IDs de reglas y pruebas únicos (150 reglas, 201 pruebas) |
| V02 | OK | Todas las reglas aparecen en la spec con el texto de la fuente |
| V03 | OK | La matriz de pruebas de la spec tiene exactamente las pruebas de la fuente, sin duplicados |
| V04 | OK | Toda prueba citada existe (T-12 en adelante) |
| V05 | OK | Toda regla citada existe |
| V06 | OK | Cada regla tiene prueba y cada prueba tiene regla (sin reglas sin prueba ni pruebas sin requisito) |
| V07 | OK | La tabla regla→pruebas de la spec coincide con la cobertura calculada |
| V08 | OK | Modelo: FK con origen, destino, aridad y clave única o primaria declarada |
| V09 | OK | Tipos de columnas origen y destino de las FK entre tablas nuevas coinciden |
| V10 | OK | Toda tabla nueva tiene clave primaria (5 tablas nuevas, 32 propuestas en total) |
| V11 | OK | Ningún CHECK del modelo impone 30 ni 10 caracteres (DG-16) |
| V12 | OK | Toda mención de 30 o 10 caracteres en documentos activos la trata como propuesta pendiente |
| V13 | OK | Cada una de las siete correcciones tiene al menos las pruebas pedidas |
| V14 | OK | Existen pruebas de concurrencia, aislamiento, permisos, abortos, idempotencia, versiones, par y canales |
| V15 | OK | Reglas críticas de seguridad con pruebas positivas y negativas (heurística sobre resultado esperado) |
| V16 | OK | El resumen de la spec (11.1) coincide con los conteos reales (150 reglas, 201 pruebas: 21/143/37; 18 diagramas) |
| V17 | OK | Diagramas Mermaid: 18 de 18 con sintaxis válida (mermaid 10 con jsdom; control negativo detecta el error); no se renderizaron visualmente |
| V18 | OK | Sin contradicciones entre documentos activos (patrones de la v2 residuales) |
| V19 | OK | SHA-256 de v3.3 intacto |
| V20 | OK | Documentos protegidos y demás archivos de la línea base sin cambios (78 comparados) |
| V21 | OK | Roadmap: 76 subfases distintas sin subfase 77 |
| V22 | OK | Roadmap: 1.8 crea el catálogo, 5.1 solo agrega columnas de reglas y 6.5 crea approvals e impact_evaluations |
| V23 | OK | H-01: orden topológico de creación; FK hacia tablas y columnas existentes en su momento; sin ciclos; funciones, triggers e índices coherentes (5 FK di |
| V24 | OK | H-01: controles negativos (cada defecto se detecta): FK hacia tabla todavía no creada=detectado; FK hacia columnas sin PK/UNIQUE=detectado; Dependenci |
| V25 | OK | H-01: tabla de orden idéntica en especificación, roadmap y auditoría; secuencia «1.8 → 2.x → 3.x → 4.x → 5.1 → 5.3 → 6.x → 6.1 → 6.5 → 6.6 → 8.x» en l |
| V26 | OK | H-01: el diagrama 7.17 reproduce la secuencia y las tablas del plan; ningún otro diagrama asigna impact_evaluations a 5.4 |
| V27 | OK | H-02: definición única de contribuyente (12 figuras), 13 escenarios con prueba, T-04 y DT-01 declarados con comportamiento fail-closed, ninguna afirma |
| V28 | OK | H-04: attempt_nonce uuid único en el modelo; reglas IG10-31 a IG10-37; 20 escenarios del encargo con prueba; 5.11 compara tres alternativas, declara l |
| V29 | OK | H-03: los cinco documentos distinguen Fase 0 v3.3 (aceptada como línea base), el diseño complementario (pendiente de aceptación formal) y Fase 1 (no i |
| V30 | OK | Los 17 permisos físicos y las 13 transiciones T-02 se citan sin cambio en los documentos activos |
| V31 | OK | correlation_id y idempotencia coherentes: columnas en ambas tablas, política única (IG10-28, IG10-29), sin afirmar que sea clave o evidencia |
| V32 | OK | Sin código, SQL ni archivos de infraestructura en los documentos ni en el árbol de Git (solo .md bajo docs/fase0/) |
| V33 | OK | Todos los documentos activos indican qué está diseñado y que no está validado técnicamente |
| V34 | OK | Referencias cruzadas: toda regla y prueba citada en los cinco documentos existe |
| V35 | OK | Sin identificadores RR duplicados en la especificación |
| V36 | OK | Pruebas: ninguna afirma haber sido ejecutada; las de concurrencia tienen actores, secuencia y resultado; las de rollback no prometen persistencia inex |

## 4. Riesgos residuales

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
| RR-21 | T-04 (definición de contribuyentes) está pendiente en v3.3; DG-17 y la independencia dependen de ella |
| RR-22 | Los valores reales de canales y formatos no existen: sin catálogo cargado no se crean piezas |
| RR-23 | Tras una restauración, un clon o una recuperación a un punto anterior, un db_txid guardado podría repetirse; attempted_at no es un identificador |
| RR-24 | El orden de versión de la maestra (columna de copy_versions) no está fijado en v3.3 |
| RR-25 | El valor de pg_current_xact_id dentro de un savepoint o bloque EXCEPTION no está verificado |
| RR-26 | La FK no distingue «sin arte» de «otro arte» con columnas anulables |
| RR-27 | T-04 solo está resuelta en su definición conceptual (OD-03, PO-08, PO-11, PO-16, aprobadas con condiciones): faltan el umbral de aportación sustantiva y la representación física de las contribuciones de brief, datos promocionales y herencia |
| RR-28 | El superusuario, el propietario de las tablas, la desactivación de triggers y la edición manual de datos no los impide este diseño |
| RR-29 | La disponibilidad y la fuente aleatoria de gen_random_uuid() en la versión de PostgreSQL de Supabase no están verificadas (en PostgreSQL 13 o posterior es una función del núcleo) |
| RR-30 | La variable local de la transacción que lleva el nonce a la guarda puede ser escrita por quien tenga acceso SQL |
| RR-31 | Los privilegios por columna (sin SELECT sobre attempt_nonce) y los roles propietarios no están verificados en Supabase |
| RR-32 | version_contributors no puede implementarse mientras no se defina la representación física de las contribuciones (PC-02; activity_logs no existe) |
| RR-33 | El orden de creación se verificó contra el modelo de esta revisión y a nivel de tabla contra las 27 tablas de v3.3, cuyas columnas exactas v3.3 no define |

## 5. Estado por brecha

| Brecha | Estado |
|---|---|
| G-1 | Diseño documental completo; preparado para aceptación formal |
| G-5 | Diseño documental completo salvo independencia, condicionada a DT-01 (T-04); no plenamente cerrada |
| G-10 | Diseño documental completo con límites declarados; preparado para aceptación formal |

Ninguna está aceptada ni validada técnicamente. Mientras DT-01 siga pendiente, la independencia de G-5 opera en modo fail-closed: sin conjunto determinable no hay evaluación válida.
