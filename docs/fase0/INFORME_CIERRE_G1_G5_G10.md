---
name: informe_cierre_g1_g5_g10
description: Informe de la revisión v4 de G-1, G-5 y G-10 (cuatro hallazgos finales); diseño documental corregido y preparado para aceptación formal; nada ejecutado
---

# INFORME — CORRECCIÓN FINAL DE G-1, G-5 Y G-10 (revisión v4)

Sustituye al informe v3 (conservado en `historico/`). Solo diseño documental (nivel de evidencia 1): no se ejecutó SQL, código, Supabase ni infraestructura. **Corrección de redacción:** el informe v3 decía que Fase 0 no estaba aceptada; eso era erróneo. Fase 0 v3.3 está aceptada como línea base documental (H-03).

## A. Dictamen ejecutivo

| Nivel | Estado | Alcance |
|---|---|---|
| 1. Fase 0 v3.3 | COMPLETADA Y ACEPTADA COMO LÍNEA BASE DOCUMENTAL, CON LIMITACIONES DOCUMENTADAS | No se reabre ni se modifica; SHA-256 `b5dccdc73a8103966ab1e1b1e84b2e7ead68cd736fba666ec71d0e790d51c1da` sin cambio |
| 2. Diseño técnico complementario (G-1, G-5, G-10, v4) | DISEÑO TÉCNICO DOCUMENTAL CORREGIDO Y PREPARADO PARA ACEPTACIÓN FORMAL, CON LIMITACIONES DOCUMENTADAS | Pendiente de aceptación formal del propietario; no validado técnicamente; la independencia de G-5 depende de DT-01 (T-04) |
| 3. Fase 1 | NO INICIADA / NO AUTORIZADA | Requiere autorización expresa; el diseño complementario no la concede |


G-1, G-5 y G-10 no se declaran aceptadas ni validadas técnicamente. **G-5 no se declara plenamente cerrada**: la independencia del evaluador depende de DT-01 (T-04, no aprobada en v3.3) y el diseño falla cerrado (fail-closed) mientras no exista definición aceptada.

## B. Hallazgos H-01 a H-04

### H-01 Orden de creación

| Concepto | Detalle |
|---|---|
| Problema | impact_evaluations (5.4) tenía FK a approvals, que se crea en 6.5: una migración en el orden de la v3 falla. |
| Solución | Alternativa B: impact_evaluations y record_impact_evaluation pasan a 6.5, después de approvals. Se descartó A (approvals mínima antes) por crear una tabla parcial y C (otra) por no aportar nada. Un único orden de 1.8 a 8.x idéntico en especificación, roadmap, auditoría e informe. |
| Ubicación exacta | Spec 7.17 y 14.1 a 14.5; roadmap 3 |
| Reglas | IM-01, IM-02, IM-03, IM-04, IM-05, IM-06, IM-07, IM-08, IM-09, IM-10, IM-11, IM-12, IS-01 |
| Pruebas documentales diseñadas | T-153 a T-164 (12; ninguna ejecutada) |
| Resultado | Verificaciones documentales por script (V23 a V37) sin fallas; sigue pendiente la validación técnica real |

### H-02 T-04 y contribuyentes

| Concepto | Detalle |
|---|---|
| Problema | T-04 no estaba recuperada ni definida de forma única; DG-17 la usaba sin distinguir figuras. |
| Solución | T-04 recuperada: no aprobada en v3.3. Definición única en 4.4.3 que distingue autoría, contribución material, intervención administrativa, revisión, aprobación y operación automática, e incluye versiones intermedias V-D..V-B. Sin elegible, bloqueo; sin autoasignación. Propuesta técnica marcada como pendiente (DT-01, DT-02). |
| Ubicación exacta | Spec 4.4.3 |
| Reglas | IE-04, IG5-23, IG5-32, IG5-33, IG5-35, IG5-38, IG5-40, IG5-41, IG5-42, IG5-43, IG5-44, IG5-45, IG5-46, IG5-47, IG5-48 |
| Pruebas documentales diseñadas | T-165 a T-178 (14; ninguna ejecutada) |
| Resultado | Verificaciones documentales por script (V23 a V37) sin fallas; sigue pendiente la validación técnica real |

### H-03 Estado de Fase 0

| Concepto | Detalle |
|---|---|
| Problema | La v3 mezclaba el estado de Fase 0 v3.3 con el del diseño complementario. |
| Solución | Tres niveles: Fase 0 v3.3 aceptada como línea base; diseño complementario pendiente de aceptación formal; Fase 1 no iniciada. v3.3 y su SHA no se tocan. |
| Ubicación exacta | Spec 15 y 15.1; los cinco documentos |
| Reglas | IE-01, IE-02, IE-03, IE-04 |
| Pruebas documentales diseñadas | T-179 a T-182 (4; ninguna ejecutada) |
| Resultado | Verificaciones documentales por script (V23 a V37) sin fallas; sigue pendiente la validación técnica real |

### H-04 Guarda db_txid

| Concepto | Detalle |
|---|---|
| Problema | La guarda db_txid podía confundirse con un identificador de intento y no declaraba amenazas ni límites. |
| Solución | db_txid más attempt_nonce uuid generado por el servidor (trigger, UNIQUE, sin SELECT para roles de aplicación); guarda de ocho condiciones; comparación de tres alternativas (A txid + nonce, B txid + identidad de intento, C firma); límites declarados (superusuario, propietario, desactivar triggers, edición manual); lo que depende de infraestructura queda como validación técnica pendiente. No se afirma seguridad absoluta. |
| Ubicación exacta | Spec 5.11 |
| Reglas | IG10-08, IG10-21, IG10-22, IG10-23, IG10-24, IG10-25, IG10-29, IG10-30, IG10-31, IG10-32, IG10-33, IG10-34, IG10-35, IG10-36, IG10-37, IS-02, IS-03, IS-04, IS-05, IS-10, IS-11 |
| Pruebas documentales diseñadas | T-183 a T-201 (19; ninguna ejecutada) |
| Resultado | Verificaciones documentales por script (V23 a V37) sin fallas; sigue pendiente la validación técnica real |

## C. Modelo y arquitectura

| Elemento | Detalle |
|---|---|
| Tablas | 27 históricas sin cambio; 5 nuevas propuestas: `piece_classification_events`, `piece_reviewer_assignments`, `impact_evaluations`, `publication_attempts`, `channel_formats` (32 propuestas en total) |
| Orden definitivo | 1.8 → 2.x → 3.x → 4.x → 5.1 → 5.3 → 6.x → 6.1 → 6.5 → 6.6 → 8.x |
| Funciones | create_adaptation, propose_independence, resolve_independence, assign_reviewer, version_contributors, eligible_evaluators, record_approval, record_impact_evaluation, transition_piece_status, manage_channel_catalog |
| Triggers | catalog_active_check y piece_status_guard_base (1.8); asset_match (6.5); fijación de db_txid y attempt_nonce y guarda completa (6.6) |
| Privilegios | Tablas con RLS activada y sin privilegios al nacer; EXECUTE por función en su subfase; roles propietarios cci_state_owner y cci_records_owner |
| Límites | IS-11: superusuario, propietario, desactivación de triggers y edición manual quedan fuera de lo que el diseño impide; se declaran, no se resuelven |

## D. Verificación

| Concepto | Resultado |
|---|---|
| Reglas de integridad | 150 |
| Pruebas diseñadas | 201 (diseño 21 / ejecutable futura 143 / infraestructura real 37); **ninguna ejecutada**; cobertura regla↔prueba completa |
| Verificaciones automáticas | 36 comprobaciones documentales por script, 0 fallas (detalle en la auditoría) |
| Diagramas | 18 bloques Mermaid con sintaxis validada (mermaid 10 y jsdom, parseo; no se verificó el renderizado visual) |
| Errores hallados y corregidos | Durante la v4: orden con falso ciclo por FK diferidas, columna attempt_nonce ausente del modelo, referencia errónea en 4.4.3, controles negativos del diagrama mal diseñados, hash del registro de la Adenda v9 que en la v3 mostraba el del registro de G-1/G-5/G-10 por colisión de nombre, pruebas de concurrencia sin actores y regla IS-11 sin prueba positiva (ver auditoría) |
| Pruebas técnicas no ejecutadas | Todas: no hay PostgreSQL, RLS, Supabase ni concurrencia real ejecutados |

## E. Pendientes

DT-01 (umbral y representación física de aportación sustantiva, T-04), DT-02, DG-09, DG-12, DG-16, DG-18, DG-19, DG-20, PO-05 y Adenda v9, RP-01, P-01 a P-05, P-10, OD-13, G-9 completo, DEP-RET-01, DEP-CAT-01 (valores reales de canales y formatos) y decisiones de infraestructura.

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

## F. Integridad y GitHub

SHA-256 de v3.3: `b5dccdc73a8103966ab1e1b1e84b2e7ead68cd736fba666ec71d0e790d51c1da` (sin cambio). Publicación en `main` de `appalex47-lab/Copy-Creative-Intelligence`, carpeta `docs/fase0/`. Commit anterior `8b81dd2ccb64bf3f6d1d6b1ffd21e7f1bcbce1a9`. El commit nuevo y los SHA-256 publicados se informan en el mensaje final (no se autorreferencian aquí).

## G. Declaración de alcance

Sin código, sin SQL ejecutable, sin recursos Supabase, sin despliegue; v3.3 sin alterar; Fase 1 no iniciada; ninguna decisión del propietario se da por aceptada; Adenda v9 sin aceptar.
