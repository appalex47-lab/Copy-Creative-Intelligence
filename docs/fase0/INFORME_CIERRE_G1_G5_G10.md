---
name: informe_cierre_g1_g5_g10
description: Informe de la revisión v3 (siete correcciones) de G-1, G-5 y G-10; diseño técnico documental listo para aceptación formal; nada ejecutado
---

# INFORME — CORRECCIÓN Y CIERRE TÉCNICO DOCUMENTAL DE G-1, G-5 Y G-10 (revisión v3)

Sustituye al informe v2 (conservado en `historico/`). Solo diseño documental (nivel de evidencia 1): no se ejecutó SQL, código, Supabase ni infraestructura.

## A. Resultado

**COMPLETADO DOCUMENTALMENTE.** Las siete correcciones están resueltas en la especificación v3, el roadmap, el registro y la auditoría; las verificaciones documentales por script pasan (ver E). No están aceptadas ni validadas técnicamente.

## B. Estado de brechas

| Brecha | Estado | Contenido |
|---|---|---|
| G-1 | Resuelta documentalmente; lista para aceptación formal | Vínculo, clave, versión de origen y ciclo de vida de canales y formatos (DG-19, recomendación técnica sujeta a aceptación) |
| G-5 | Resuelta documentalmente; lista para aceptación formal | Aprobación positiva (DG-20, sujeta a aceptación), independencia DG-17 y cadena lineal por par |
| G-10 | Resuelta documentalmente; lista para aceptación formal | db_txid con mecanismo concreto, guarda de ocho condiciones, cuatro escenarios de fallo y política de correlation_id |

«Lista para aceptación formal» no es aceptación: la decisión es del propietario. G-9 completo sigue abierto.

## C. Siete correcciones

### C.1 G-5 aprobación positiva

| Concepto | Detalle |
|---|---|
| Problema | La v3.3 no tiene un campo que distinga una aprobación positiva de un rechazo o una solicitud de cambio, y C2/C3 no decían qué leían. |
| Solución | Extensión mínima DG-20: `approvals.decision` NOT NULL con CHECK = 'aprobada'. Rechazo, solicitud de cambio y registro de revisión son transiciones T-02 con comentario, no filas de `approvals`. Vigencia derivada de versión exacta (copia y arte con IS NOT DISTINCT FROM) y estado de la pieza; FK compuesta más trigger `asset_match`. |
| Dónde (spec v3) | 4.13, 3.4, 6.2 (C2/C3), 8.9 |
| Reglas | IG5-26, IG5-27, IG5-28, IG5-29, IG5-30 |
| Pruebas diseñadas | T-74 a T-84 (11, ninguna ejecutada) |
| Verificación | Comprobaciones documentales V01–V22 (ver E) |

### C.2 G-10 db_txid

| Concepto | Detalle |
|---|---|
| Problema | `db_txid` no tenía mecanismo ni tipo definidos. |
| Solución | Columna bigint NOT NULL fijada por trigger BEFORE INSERT con `(pg_current_xact_id())::text::bigint`, junto con `attempted_at = transaction_timestamp()`. Descartados `txid_current()`, `pg_current_xact_id_if_assigned()` y xid de 32 bits. Guarda de ocho condiciones en trigger propiedad de `cci_state_owner`. Subtransacciones sin verificar: la guarda falla cerrada. |
| Dónde (spec v3) | 5.10, 5.11, 4.x trigger, 7.14 |
| Reglas | IG10-01, IG10-19, IG10-20, IG10-22, IG10-23, IG10-24, IG10-25, IG10-26, IG10-27, IG10-29, IG10-30, IS-01, IS-02, IS-03, IS-04, IS-05, IS-08, IS-09 |
| Pruebas diseñadas | T-85 a T-104 (20, ninguna ejecutada) |
| Verificación | Comprobaciones documentales V01–V22 (ver E) |

### C.3 G-1 canales y formatos

| Concepto | Detalle |
|---|---|
| Problema | El ciclo de vida de canales y formatos dejaba piezas sin catálogo y una lista de formatos sin normalizar. |
| Solución | Se evaluaron tres alternativas y se eligió `channel_rules` (fuente de verdad del canal) más `channel_formats`, creados en 1.8 antes de la primera pieza; FK compuesta desde `creative_pieces`; inmutables en la pieza; retiro solo con `active=false` y sin piezas activas; `manage_channel_catalog` con org.manage. |
| Dónde (spec v3) | 3.14, 7.13, 8.9; roadmap 1.8 y 5.1 |
| Reglas | IG1-25, IG1-26, IG1-27, IG1-28, IG1-29, IG1-30, IG1-31, IG1-32, IG1-33 |
| Pruebas diseñadas | T-105 a T-119 (15, ninguna ejecutada) |
| Verificación | Comprobaciones documentales V01–V22 (ver E) |

### C.4 DG-16 longitudes

| Concepto | Detalle |
|---|---|
| Problema | Los umbrales de 30 y 10 caracteres estaban como CHECK obligatorios aunque T-03 no los decide. |
| Solución | Todos los CHECK de longitud mínima pasan a no vacío (>=1). 30 y 10 quedan como propuestas pendientes (IP-05). |
| Dónde (spec v3) | 3.x, 4.2, 12.3 |
| Reglas | IG5-09, IP-05 |
| Pruebas diseñadas | T-120 a T-124 (5, ninguna ejecutada) |
| Verificación | Comprobaciones documentales V01–V22 (ver E) |

### C.5 DG-17 independencia

| Concepto | Detalle |
|---|---|
| Problema | La independencia no consideraba a los contribuyentes de versiones intermedias de la maestra. |
| Solución | E = Ctr(V-A) ∪ Inh(V-A) ∪ ⋃ Ctr(v) para v en el intervalo [V-D, V-B] inclusive; revalidación bajo bloqueo; sin elegible, bloqueo operativo sin autoasignación. |
| Dónde (spec v3) | 4.4.2, 8.9 |
| Reglas | IG5-06, IG5-24, IG5-25, IG5-31, IG5-32, IG5-33, IG5-34, IG5-35 |
| Pruebas diseñadas | T-125 a T-135 (11, ninguna ejecutada) |
| Verificación | Comprobaciones documentales V01–V22 (ver E) |

### C.6 G-5 cadena de evaluaciones

| Concepto | Detalle |
|---|---|
| Problema | La sustitución de evaluaciones no estaba atada al par exacto ni protegida contra ramas, ciclos y duplicados. |
| Solución | Identidad de par de 9 columnas (con arte normalizado), FK compuesta de sustitución con 8 columnas de par, raíz única por par, único sucesor, CHECK supersedes<>id, solo inserción y bloqueo de la cabeza. |
| Dónde (spec v3) | 4.14, 7.15 |
| Reglas | IG5-13, IG5-36, IG5-37, IG5-38, IG5-39 |
| Pruebas diseñadas | T-136 a T-145 (10, ninguna ejecutada) |
| Verificación | Comprobaciones documentales V01–V22 (ver E) |

### C.7 correlation_id

| Concepto | Detalle |
|---|---|
| Problema | `correlation_id` mezclaba identificación, idempotencia y posible evidencia. |
| Solución | Siempre generado por el servidor; `client_correlation_id` opcional, validado y descartable; nunca evidencia ni autorización; independiente de `idempotency_key`; `request_fingerprint` rechaza claves reutilizadas con datos distintos. |
| Dónde (spec v3) | 5.12, 5.5 |
| Reglas | IG10-28, IG10-29, IS-05 |
| Pruebas diseñadas | T-146 a T-152 (7, ninguna ejecutada) |
| Verificación | Comprobaciones documentales V01–V22 (ver E) |

## D. Modelo resultante

| Tipo | Detalle |
|---|---|
| Existente (línea base) | 27 tablas históricas, 17 claves físicas, 13 transiciones de T-02, 76 subfases: sin cambio |
| Propuesto, nuevo | 5 tablas: `piece_classification_events`, `piece_reviewer_assignments`, `impact_evaluations`, `publication_attempts`, `channel_formats` (32 propuestas, sujetas a aceptación) |
| Propuesto, columnas o restricciones | creative_pieces, copy_versions, creative_assets, approvals (decision) y channel_rules |
| Propuesto, funciones | create_adaptation, propose_independence, resolve_independence, assign_reviewer, version_contributors, eligible_evaluators, record_approval, record_impact_evaluation, transition_piece_status, manage_channel_catalog (8.9) |

## E. Validación

| Concepto | Resultado |
|---|---|
| Reglas de integridad | 117 |
| Pruebas diseñadas | 152 (diseño 7 / ejecutable futura 117 / infraestructura real 28); **ninguna ejecutada** |
| Verificaciones documentales | 22 comprobaciones por script (`work/g_verify.py`): IDs, duplicados, integridad referencial, regla↔prueba, pruebas sin requisito, tablas/columnas/FK/tipos, dependencias del roadmap, conteos, sintaxis Mermaid, contradicciones y hashes protegidos |
| Diagramas | 17 bloques Mermaid; sintaxis validada con mermaid 10 y jsdom (parseo, no renderizado visual) |
| Errores hallados y corregidos | V14 y V15 del propio verificador durante la revisión (ver auditoría) |
| Límites | No son pruebas técnicas: no hay PostgreSQL, RLS ni Supabase ejecutados; el comportamiento de db_txid en subtransacciones y la versión de PostgreSQL de Supabase no están verificados |

## F. Pendientes

DG-09, DG-12, DG-18 (columna opcional `replaces_piece_id`), DG-19 y DG-20 (pendientes de aceptación), DG-16 (umbrales 30/10 ligados a T-03), T-04, P-01 a P-05, P-10, OD-13, PO-05 y Adenda v9, RP-01, G-9 completo, valores reales de canales y formatos (DEP-CAT-01), DEP-RET-01 y decisiones de infraestructura no autorizadas.

**Limitaciones reales (RR):**

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
| RR-21 | T-04 (definición de contribuyentes) está pendiente en v3.3; DG-17 y la independencia dependen de ella |
| RR-22 | Los valores reales de canales y formatos no existen: sin catálogo cargado no se crean piezas |
| RR-23 | Tras restaurar una copia lógica, un db_txid guardado podría repetirse |
| RR-24 | El orden de versión de la maestra (columna de copy_versions) no está fijado en v3.3 |
| RR-25 | El valor de pg_current_xact_id dentro de un savepoint o bloque EXCEPTION no está verificado |
| RR-26 | La FK no distingue «sin arte» de «otro arte» con columnas anulables |

## G. Integridad

SHA-256 de v3.3: `b5dccdc73a8103966ab1e1b1e84b2e7ead68cd736fba666ec71d0e790d51c1da` (sin cambio). Los documentos protegidos no se modificaron (comprobación V-hash en el verificador). Modificados: especificación, informe, roadmap, registro. Nuevo: `AUDITORIA_FINAL_G1_G5_G10.md`. Históricos v2 en `docs/fase0/historico/`.

## H. GitHub

Publicación en `main` de `appalex47-lab/Copy-Creative-Intelligence`, carpeta `docs/fase0/`. El SHA del commit y los hashes publicados se informan en el mensaje final (no se autorreferencian aquí).

## I. Estado de autorización

Documentos corregidos y publicados. G-1, G-5 y G-10 quedan listas para aceptación formal si el propietario acepta el diseño. No hay SQL, código ni recursos Supabase. Fase 1 no iniciada. Adenda v9 y Fase 0 no aceptadas en nombre del propietario.
