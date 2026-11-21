---
name: informe_cierre_g1_g5_g10
description: Informe de la revisión v5 de G-1, G-5 y G-10 (DT-01, PC-02 y DT-02); diseño documental corregido y preparado para aceptación formal; nada ejecutado
---

# INFORME — CIERRE DE DT-01, PC-02 Y DT-02 (revisión v5)

Sustituye al informe v4 (conservado en `historico/`). Solo diseño documental (nivel de evidencia 1): no se ejecutó SQL, código, Supabase ni infraestructura. Estas reglas son el diseño complementario definido en las instrucciones de esta revisión: no alteran el expediente histórico, no aprueban T-04 de v3.3 retroactivamente y no aceptan la Adenda v9.

## A. Dictamen ejecutivo

| Nivel | Estado | Alcance |
|---|---|---|
| 1. Fase 0 v3.3 | COMPLETADA Y ACEPTADA COMO LÍNEA BASE DOCUMENTAL, CON LIMITACIONES DOCUMENTADAS | No se reabre ni se modifica; SHA-256 `b5dccdc73a8103966ab1e1b1e84b2e7ead68cd736fba666ec71d0e790d51c1da` sin cambio |
| 2. Diseño técnico complementario (G-1, G-5, G-10, v5) | DISEÑO TÉCNICO DOCUMENTAL CORREGIDO Y PREPARADO PARA ACEPTACIÓN FORMAL, CON LIMITACIONES DOCUMENTADAS | Pendiente de aceptación formal del propietario; no validado técnicamente; DT-01, PC-02 y DT-02 resueltas en el diseño, sin aceptación; G-5 no se declara cerrada |
| 3. Fase 1 | NO INICIADA / NO AUTORIZADA | Requiere autorización expresa; el diseño complementario no la concede |


G-1, G-5 y G-10 no se declaran aceptadas ni validadas técnicamente. **G-5 no se declara completamente cerrada**: aunque toda fuente de contribución tiene representación en el diseño, la aceptación del propietario y la validación técnica siguen pendientes, y el diseño falla cerrado (fail-closed) si falta una fuente.

## B. Qué se corrigió

### DT-01 Definición operativa de contribuyente

| Concepto | Detalle |
|---|---|
| Problema | La definición de contribuyente mezclaba autoría, contribución material, intervención administrativa y herencia, y dejaba el umbral de aportación sustantiva abierto. |
| Solución | Definición única A–F: autoría de copy, edición material con normalización exclusiva (NFKC, saltos de línea, espacios), brief con once campos materiales, datos promocionales con nueve, arte exacto y herencia por procedencia con ocho reglas; sin porcentajes, embeddings ni IA; en duda se conserva la atribución (PO-16). Fórmula E = Ctr(V-A) ∪ Inh(V-A) ∪ ⋃ Ctr(v) para v ∈ [V-D, V-B] ∪ P. |
| Ubicación exacta | Spec 4.4.3 |
| Reglas | IG5-42, IG5-43, IG5-46, IG5-49, IG5-50, IG5-51, IG5-52, IG5-53, IG5-54, IG5-55, IG5-56, IG5-61, IG5-63, IG5-64, IS-13 |
| Pruebas diseñadas | T-202 a T-226 (25; ninguna ejecutada) |
| Verificación | Controles documentales por script (ver la auditoría); sigue pendiente la validación técnica real |

### PC-02 Representación física de las contribuciones

| Concepto | Detalle |
|---|---|
| Problema | version_contributors no tenía fuentes físicas para brief, datos promocionales ni procedencia heredada. |
| Solución | Cuatro entidades propias: brief_versions (2.1), contribution_events (2.1, con orígenes tipados y FK compuestas), copy_version_provenance (2.3) y promotion_snapshots (4.x); copy_versions fija brief_version_id y promotion_snapshot_id exactos; contrato de version_contributors con seis códigos de error y bloqueo fail-closed; inmutabilidad por triggers, propietario cci_records_owner y privilegios mínimos; activity_logs no es fuente. |
| Ubicación exacta | Spec 4.4.4, 4.4.5, 14.1 |
| Reglas | IG5-42, IG5-45, IG5-52, IG5-53, IG5-54, IG5-56, IG5-57, IG5-58, IG5-59, IG5-60, IG5-61, IG5-62, IG5-63, IG5-64, IG5-65, IG5-67, IG5-68, IS-12, IS-13, IS-14 |
| Pruebas diseñadas | T-227 a T-268 (42; ninguna ejecutada) |
| Verificación | Controles documentales por script (ver la auditoría); sigue pendiente la validación técnica real |

### DT-02 Elegibilidad del proponente de la clasificación

| Concepto | Detalle |
|---|---|
| Problema | No estaba decidido si el proponente de la clasificación vigente puede evaluar el impacto. |
| Solución | No puede, por adaptación y mientras su clasificación esté vigente; quien confirma o revierte no queda excluido por ello; el proponente no confirma su propia propuesta; se revalida bajo bloqueo; sin permiso, estado ni transición nuevos. |
| Ubicación exacta | Spec 4.4.6 |
| Reglas | IG5-45, IG5-56, IG5-57, IG5-64, IG5-67, IG5-68, IS-14 |
| Pruebas diseñadas | T-251 a T-262 (12; ninguna ejecutada) |
| Verificación | Controles documentales por script (ver la auditoría); sigue pendiente la validación técnica real |

### Integración Flujo único DT-01, PC-02 y DT-02

| Concepto | Detalle |
|---|---|
| Problema | Las tres decisiones debían formar un flujo único. |
| Solución | Flujo de 13 pasos y condiciones de registro de la evaluación; un cambio de versión obliga a recalcular E y una evaluación anterior no se reutiliza. |
| Ubicación exacta | Spec 4.4.7 |
| Reglas | IG5-40, IG5-42, IG5-45, IG5-47, IG5-48, IG5-52, IG5-53, IG5-54, IG5-56, IG5-57, IG5-59, IG5-63, IG5-64, IG5-66, IG5-68, IS-14 |
| Pruebas diseñadas | T-263 a T-274 (12; ninguna ejecutada) |
| Verificación | Controles documentales por script (ver la auditoría); sigue pendiente la validación técnica real |

## C. Modelo y arquitectura

| Elemento | Detalle |
|---|---|
| Tablas | 27 históricas sin cambio; 9 nuevas propuestas: `piece_classification_events`, `piece_reviewer_assignments`, `impact_evaluations`, `publication_attempts`, `channel_formats`, `brief_versions`, `promotion_snapshots`, `contribution_events`, `copy_version_provenance` (36 propuestas en total) |
| Relaciones nuevas | contribution_events → brief_versions, copy_versions, creative_assets y promotion_snapshots (cada una con FK compuesta y exactamente un origen); copy_version_provenance → copy_versions (versión y origen), contribution_events y memberships; copy_versions → brief_versions y promotion_snapshots; promotion_snapshots → promotion_rules |
| Orden definitivo | 1.8 → 2.x → 2.1 → 2.3 → 2.5 → 2.7 → 3.x → 4.x → 5.1 → 5.3 → 6.x → 6.1 → 6.5 → 6.6 → 8.x |
| Funciones nuevas | create_brief_version, record_contribution_event (interna), create_copy_version, detect_material_change, verify_version_chain, register_asset_contribution, create_promotion_snapshot, version_contributors, exclude_inherited_attribution |
| Privilegios | Tablas con RLS activada y sin privilegios al nacer; escritura solo por funciones del propietario cci_records_owner con search_path fijo; triggers de inmutabilidad; sin privilegio implícito para Admin |
| Límites | IS-11: superusuario, propietario, desactivación de triggers y edición manual no los impide el diseño; SECURITY DEFINER no se toma como prueba de seguridad |

## D. Fórmula de contribuyentes y elegibilidad

**E = Ctr(V-A) ∪ Inh(V-A) ∪ ⋃ Ctr(v) para v ∈ [V-D, V-B] ∪ P.** Puede evaluar quien (1) es miembro activo, (2) tiene `piece.review`, (3) está asignado y su asignación sigue vigente, (4) no pertenece a E, (5) no está impedido por DG-06 y (6) mantiene todo al guardar, revalidado bajo bloqueo. Sin persona elegible no hay evaluación ni publicación.

## E. Verificación

| Concepto | Resultado |
|---|---|
| Reglas de integridad | 173 |
| Pruebas diseñadas | 274 (documental 22 / técnica futura ejecutable 203 / infraestructura real 49); **ninguna ejecutada**; cobertura regla↔prueba completa |
| Verificaciones automáticas | 0 comprobaciones documentales por script, 0 fallas (detalle en la auditoría) |
| Diagramas | Bloques Mermaid con sintaxis validada (mermaid 10 y jsdom, parseo; no se verificó el renderizado visual), incluido el diagrama de relaciones de PC-02 generado desde el modelo |
| Errores hallados y corregidos | Ver la auditoría, sección 3 |
| Pruebas técnicas no ejecutadas | Todas: no hay PostgreSQL, RLS, Supabase ni concurrencia real ejecutados |

## F. Pendientes

PO-05 y aceptación de la Adenda v9; aceptación formal de DT-01, PC-02 y DT-02; DG-09, DG-12, DG-16, DG-18, DG-19, DG-20; RP-01; P-01 a P-05; P-10; OD-13; G-9 completo; DEP-RET-01; valores reales de canales y formatos (DEP-CAT-01); validación de infraestructura, PostgreSQL, RLS y Supabase; pruebas reales de concurrencia, bloqueos y rollback.

**Limitaciones y riesgos (RR):**

| ID | Limitación |
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

## G. Integridad y GitHub

SHA-256 de v3.3: `b5dccdc73a8103966ab1e1b1e84b2e7ead68cd736fba666ec71d0e790d51c1da` (sin cambio). Publicación en `main` de `appalex47-lab/Copy-Creative-Intelligence`, carpeta `docs/fase0/`. Commit anterior `9febdafb61125586d7937250b4f63bcd214d6c0c`. El commit nuevo y los SHA-256 publicados se informan en el mensaje final (no se autorreferencian aquí).

## H. Declaración de alcance

Sin código, sin SQL ejecutable, sin migraciones, sin recursos Supabase, sin infraestructura ni despliegue; v3.3 sin alterar; Fase 1 no iniciada; ninguna decisión del propietario se da por aceptada; Adenda v9 sin aceptar.
