---
name: roadmap_trazabilidad_g1_g5_g10
description: Roadmap y trazabilidad actualizados con la propuesta de cierre de G-1, G-5 y G-10; los estados de las subfases no cambian
---

# ROADMAP Y TRAZABILIDAD — PROPUESTA DE CIERRE DE G-1, G-5 Y G-10

Complementa la Adenda v9 (no aceptada) sin reemplazarla ni alterar versiones históricas. **Ninguna subfase cambia de estado**: el diseño aquí propuesto no se ha implementado ni validado técnicamente y Fase 1 no está autorizada.

## 1. Trazabilidad de brechas

| Brecha | Qué es | Estado en v9 | Estado tras esta propuesta | Subfase | Decisiones |
|---|---|---|---|---|---|
| G-1 | Vínculo maestra–adaptación y versión de origen | Pendiente (sin estructura) | Consolidada en diseño técnico v2: autorreferencia compuesta de un nivel, versión de origen por versión, canal, formato y clave | 5.3 y 2.7 (columnas desde 1.x y 2.x) | DG-01 a DG-03, DG-14 y DG-15 (aprobadas) |
| G-2 | Atributo de canal y formato | Pendiente | Consolidada en diseño v2: columnas con tipos, relación con channel_rules (allowed_formats) y clave de adaptación | 1.8 y 5.1 | DG-01 |
| G-3 | Autoría heredada | Pendiente | Consolidada en diseño v2: contribuyentes calculados desde la versión de origen | 5.3 y 6.5 | DG-01 |
| G-4 | Registro de la clasificación | Pendiente | Consolidada en diseño v2: piece_classification_events | 5.3 y 6.5 | DG-01, DG-03 |
| G-5 | Registro de la evaluación de impacto | Pendiente (sin estructura) | Consolidada en diseño técnico v2: impact_evaluations con par exacto, elegibilidad por FK compuesta y función, y cadena de correcciones | 5.4 y 6.5 | DG-04 a DG-07 (aprobadas); DG-17 |
| G-6 | Decisión de conservar o reabrir la aprobación | Pendiente | Cubierta por G-5: la acción posterior queda en la evaluación y la reapertura usa T-02 #11; sin estado propio | 5.4 y 6.5 | DG-05 |
| G-7 | Control obligatorio de publicación | Mecanismo conceptual | Precisado (C1 a C9) y sustentado por G-1, G-5 y G-10; validación técnica pendiente | 6.1, 6.5 y 6.8 | DG-05 |
| G-8 | Notificaciones | Pendiente | Sin cambio | 2.7 y 6.6 | — |
| G-9 | Asignaciones explícitas | Pendiente | Parcial: solo el revisor asignado (piece_reviewer_assignments, DG-07); **G-9 completo sigue abierto** | 5.3 y 6.5 | DG-07 |
| G-10 | Registro de intentos de publicación bloqueados | Pendiente / parcial | Consolidada en diseño técnico v2: publication_attempts con IG10-01 reformulada y cuatro escenarios de fallo | 6.1, 6.6 y 2.7 | DG-08, 10, 11, 13 (aprobadas); DG-09 y DG-12 (diferidas) |
| PT | Verificación técnica de que no hay escritura directa | Pendiente | Diseño de privilegios y guarda de trigger; verificación técnica pendiente (T-39) | 6.1 y 6.8 | — |

«Consolidada en diseño técnico v2» significa que existe una solución completa y coherente, con tus decisiones incorporadas; **no** que esté aceptada formalmente ni validada técnicamente.

## 2. Dependencia nueva

**DEP-RET-01:** no existe procedimiento operativo para retirar contenido externo cuando una pieza se reemplaza o archiva; el diseño no lo resuelve ni inventa un estado o transición.

## 3. Subfases que reciben contenido de diseño

| Subfase | Tema | Contenido de diseño |
|---|---|---|
| 1.8 | Integridad entre organizaciones (T-09) | Decidir la garantía de un nivel y las FK compuestas nuevas |
| 2.7 | Trazabilidad y auditoría | Punteros en activity_logs; capacidad (DA-01) |
| 5.1 | Canal y formato | Columnas channel y format (G-2) |
| 5.3 | Adaptación | Vínculo, clasificación, asignación de revisor |
| 5.4 | Consistencia entre adaptaciones | Evaluación de impacto |
| 6.1 | Workflow | Ampliación de transition_piece_status y guarda |
| 6.5 | Independencia y aprobación | Contribución heredada; evaluación |
| 6.6 | Auditoría del flujo | publication_attempts; protección |
| 6.8 | Pruebas | Matriz de 73 pruebas |

Los nombres de subfase son los de la Adenda v9; no se renombró ni se agregó ninguna (76 subfases, sin subfase 77).

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
| 1.8 | Migraciones | Esquema versionado y RLS de las tablas de la fase | Migraciones reproducibles | Pruebas de aislamiento de las tablas creadas | 1.6, 1.7 | Primer SQL real | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | T-04 (PO-08): modelo conceptual antes de 1.8; durante 1.8, trazabilidad base implementada y validada en su alcance real (activity_logs es el mecanismo de eventos disponible antes de 2.7: DA-01); T-09 plan de migración; herramientas (Q1). |
| 1.9 | Dashboard inicial | Command Center básico | Dashboard | Carga sin datos | 1.3, 1.8 | Exceso de tarjetas | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | Command Center básico: no entrega notificaciones (v3.3); DA-02: sin evento propio. |

#### Fase 2 — Copy Studio

| ID | Nombre | Objetivo | Entregables | Criterios de aceptación | Dependencias | Riesgos | Estado | Limitaciones conocidas | Decisiones que deben estar resueltas antes |
|---|---|---|---|---|---|---|---|---|---|
| 2.1 | Brief | Brief de 16 campos y su versión | Formulario y tabla | Validaciones y versiones | 1.8 | Formularios largos | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | P-03 antes de Fase 2; T-04: aportaciones de Brief trazadas y probadas durante 2.1, antes de habilitar el flujo; PO-16 para versiones de brief; DA-02: notificaciones de Brief (pendiente de asignación). |
| 2.2 | Integración Cohere | Servicio de IA desacoplado, cuotas, registro | Servicio y ai_runs | Llamadas registradas; sin claves en cliente | P-03 | Límites de la clave de prueba | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | P-03; PO-11: solo registra llamadas; DA-02 N-03 (cuota de IA). |
| 2.3 | Generación de propuestas | Varias propuestas por brief | Generación | Salida estructurada válida | 2.1, 2.2 | Calidad variable | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | DA-01: procedencia de propuestas de copy generadas, trazada y probada antes de habilitar 2.3 con los mecanismos definidos (activity_logs, ai_runs); PO-16; DA-02. |
| 2.4 | Fórmulas de copywriting | Fórmulas aplicables | Catálogo de fórmulas | Aplicación verificable | 2.3 | Sesgo hacia plantillas | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | Ninguna decisión específica de esta matriz; ver dependencias. |
| 2.5 | Edición | Edición humana de copy | Editor | Cambios guardados como versión | 2.3 | Pérdida de cambios | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | DA-01: modificaciones, adaptaciones manuales y aportaciones sobre el copy trazadas desde 2.5 (DD-1, DD-2); PO-16. |
| 2.6 | Comparación | Comparar versiones | Vista de comparación | Diferencias correctas | 2.5 | Confusión de versiones | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | Ninguna decisión específica de esta matriz; ver dependencias. |
| 2.7 | Versionado | Versiones inmutables con autor | copy_versions | Autor por trigger; sin edición de versiones | 2.5 | Autoría falsificable | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | DA-01; PO-16; adaptaciones: relación de versiones entre pieza maestra y adaptación (G-1, G-3). PO-20: relación de versiones maestra–adaptación (G-1) y trazabilidad de la evaluación (G-5). |
| 2.8 | Pruebas | Pruebas de la fase | Informe | Suite ejecutada | 2.1–2.7 | Mocks tomados por integración real | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | DA-02: validación técnica de las notificaciones de Brief y Copy (subfase de pruebas existente). |

#### Fase 3 — Creative Auditor

| ID | Nombre | Objetivo | Entregables | Criterios de aceptación | Dependencias | Riesgos | Estado | Limitaciones conocidas | Decisiones que deben estar resueltas antes |
|---|---|---|---|---|---|---|---|---|---|
| 3.1 | Carga de imágenes | Subir artes con hash y MIME | creative_assets, Storage | Hash y MIME verificados; objeto inmutable | 1.7, P-07 | Archivos grandes | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | P-07 validada técnicamente; T-04: aportaciones de carga de assets trazadas y probadas antes de habilitar ese flujo; PO-16 (herencia entre versiones de arte: sin subfase asignada); DA-02. |
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
| 4.1 | Modelo de promociones | promotion_rules y relación con campañas y briefs (T-07, T-11) | Tabla y relación | Validación funcional de la sección 5.3 | 1.8, P-06 | Caso C-1; sin FK real | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | P-06 impuestos; T-07 esquema y validaciones; T-04: aportaciones de datos promocionales trazadas y probadas antes de habilitar ese flujo; PO-16 (sin subfase para herencia); DA-02. |
| 4.2 | Reglas matemáticas | Precios, descuentos, redondeo | Funciones deterministas | Tolerancia 0.5 pp aplicada | 4.1, P-06 | Redondeo | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | P-08: casos de prueba y valor autorizado. |
| 4.3 | Validación de vigencias | Fechas y rangos | Validador | Incoherencias marcadas | 4.1 | Zonas horarias | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | Ninguna decisión específica de esta matriz; ver dependencias. |
| 4.4 | Validación de condiciones | Condiciones y disponibilidad | Validador | Condiciones contrastadas | 4.1 | Texto ambiguo | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | Ninguna decisión específica de esta matriz; ver dependencias. |
| 4.5 | Comparación de fuentes | Brief, regla y arte | Comparador | Diferencias reportadas | 4.2–4.4 | Fuentes incompletas | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | Ninguna decisión específica de esta matriz; ver dependencias. |
| 4.6 | Bloqueos comerciales | Bloqueos del motor y confirmados | Bloqueos | Bloqueo confirmado impide aprobar | 4.5 | Falsos bloqueos | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | DA-02 N-05: bloqueo comercial confirmado (D-05). |
| 4.7 | Pruebas | Pruebas de la fase | Informe | Suite y validación de promociones-campañas | 4.1–4.6 | Mocks | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | DA-02: validación técnica de las notificaciones de promociones. |

#### Fase 5 — Channel Adaptation

| ID | Nombre | Objetivo | Entregables | Criterios de aceptación | Dependencias | Riesgos | Estado | Limitaciones conocidas | Decisiones que deben estar resueltas antes |
|---|---|---|---|---|---|---|---|---|---|
| 5.1 | Modelos de canal | channel_rules por canal | Catálogo | Reglas por organización y canal | 1.8 | Reglas reales sin entregar | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | Atributo de canal (G-2); canal por organización; G-2. |
| 5.2 | Reglas de extensión | Límites de longitud | Validador | Límites aplicados | 5.1 | Límites cambiantes | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | Ninguna decisión específica de esta matriz; ver dependencias. |
| 5.3 | Adaptación | Adaptar copy por canal | Adaptador | Versión por canal | 2.3, 5.1 | Pérdida de sentido | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | T-04: adaptación por canal trazada y probada antes de habilitar 5.3; PO-20 (evaluación de impacto, dependencia de aprobación, declaración de independencia); G-1, G-3, G-4; sin tabla ni columna nueva. |
| 5.4 | Consistencia | Coherencia entre canales | Verificador | Diferencias señaladas | 5.3 | Falsas diferencias | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | DA-02 N-06 y N-22; PO-20: evaluación de impacto de la maestra (G-5). PO-21: evaluación de impacto por el revisor asignado independiente (sin estado nuevo). |
| 5.5 | Comparación multicanal | Vista comparativa | Vista | Comparación correcta | 5.3 | — | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | Comparación multicanal: no genera notificación; usa la relación maestra–adaptación (G-1). |
| 5.6 | Pruebas | Pruebas de la fase | Informe | Suite ejecutada | 5.1–5.5 | Mocks | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | DA-02: validación técnica de las notificaciones de Fase 5. |

#### Fase 6 — Workflow & Approvals

| ID | Nombre | Objetivo | Entregables | Criterios de aceptación | Dependencias | Riesgos | Estado | Limitaciones conocidas | Decisiones que deben estar resueltas antes |
|---|---|---|---|---|---|---|---|---|---|
| 6.1 | Estados | Estados y transiciones (T-02) | transition_piece_status | Solo transiciones permitidas | 1.6 | Estados bloqueados | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | T-02 (13 transiciones verificadas contra v3.3; aplican a cada adaptación independiente); PO-13; AR-01; DA-02 N-09 a N-11, N-16, N-17 y N-22; G-7: control obligatorio de publicación en transition_piece_status (condiciones C1 a C9) y G-10 (registro del intento bloqueado). |
| 6.2 | Asignaciones | Asignar piezas a personas | Asignaciones | Asignación auditada | 6.1 | — | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | Asignación de responsable, revisor y aprobador: D-02; destinatarios de PO-19; DA-02 N-07. PO-20: revisor asignado que confirma la independencia; regla D (asignaciones explícitas, G-9). |
| 6.3 | Comentarios | Hilos y solicitudes de cambio | comments | Comentarios obligatorios donde corresponde | 6.1 | — | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | Solicitudes de cambio como evento informativo a contribuyentes (N-08); DA-02. |
| 6.4 | Correcciones | Ciclo de corrección con versión nueva | Flujo | Aprobación previa no se hereda | 6.1–6.3 | Reprocesos | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | Ninguna decisión específica de esta matriz; ver dependencias. |
| 6.5 | Aprobaciones | Aprobación humana independiente, confirmación y descarte, excepciones | record_approval, review_finding, excepciones | R-02 y R-03 pasan; sin autoaprobación | 6.4, P-04, P-05 | Menos de dos personas capaces | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | T-03, T-05, T-06, OD-06, OD-09, OD-10; P-05; PO-10, PO-12, PO-15, PO-16, PO-18; PO-14, PO-17, PO-19, AR-01; DA-02 N-12 a N-15. PO-20: decisión sobre cada adaptación afectada (G-6). G-7: verificación de aprobación de la maestra y de la adaptación antes de publicar. |
| 6.6 | Historial | Historial inmutable | activity_logs | Sin UPDATE ni DELETE | 6.5 | Volumen | NO INICIADA, NO AUTORIZADA (v3.3: PENDIENTE) | Nivel 1: diseño sin ejecutar (L-01). Restricción P-09: solo datos DEMO. | Historial inmutable: trazabilidad de eventos de notificación según DA-02 (sin afirmar que cubre entrega). G-10: trazabilidad de intentos de publicación bloqueados. |
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

