# Copy & Creative Intelligence — Fase 0: documento integral de referencia v3.3

Estado: versión corregida tras la auditoría A-01 del v3.2. NO está aceptada. No se inició la Fase 1. No se creó infraestructura, código, SQL ni llamadas a Cohere. Fecha: 2026-11-15.

## 0. Identificación y control documental

| Documento | Papel | Estado |
|---|---|---|
| `fase0_v3_3_integral.md` (este archivo) | Documento integral de REFERENCIA vigente | Incluye el cuerpo técnico completo (Anexo C) |
| `fase0_v3_2_integral_definitivo.md` | Versión anterior | Intacta, sustituida documentalmente por esta |
| `fase0_v3_1_integral.md`, `anexo_consolidacion_fase0_v3.md` | Versiones y anexos anteriores | Sustituidos documentalmente; se conservan sin cambios |
| `correcciones_fase0_v3.md` | Correcciones A–E | Incorporado como Anexo B (con un ajuste, CC-04) |
| Google Docs rev 68 | Maestro HISTÓRICO | Intacto; su texto íntegro se copia en el Anexo C |

Regla de precedencia: el Anexo C es copia textual de rev 68 y puede contener frases superadas. Donde discrepe del cuerpo de este documento, la fe de erratas del Anexo C y las secciones 1–13, prevalecen estas últimas.

### Control de cambios frente a v3.2
| ID | Cambio | Motivo (auditoría) | Decisión previa que lo autoriza |
|---|---|---|---|
| CC-01 | Se incorpora el cuerpo técnico del maestro rev 68 como Anexo C (texto íntegro) | La v3.2 no contenía descubrimiento, arquitectura frontend/backend, módulos, estrategia de IA, plan de pruebas ni la matriz de permisos por rol: dependía del maestro «histórico» (H-01) | Copia sin cambios de contenido ya existente |
| CC-02 | A-01 queda definido (13.1) y se aclara que no aprueba T-01..T-12 (sección 7, Anexo B) | El maestro y el Anexo B decían que las T-01..T-10 «se aceptan con la Fase 0», contra tu instrucción de no aprobarlas (H-02) | Tu instrucción: propuestas no aprobadas |
| CC-03 | Se agregan condiciones de la Fase 1 sobre T-01, T-09 y T-10 (13.2) | Son las propuestas que 1.6 y 1.8 necesitan | Derivado de la matriz de la sección 7 |
| CC-04 | Se corrige en el Anexo B la frase sobre tabla de unión (ya hecho en v3.2) y se aclara su encabezado de propuestas | Coherencia con la sección 5 | Sección 5 |
| CC-05 | Se agrega la procedencia de las 7 tablas de apoyo (sección 4) | Trazabilidad (H-07) | Dato del maestro |
| CC-06 | Se agrega la fe de erratas del Anexo C | Frases superadas en rev 68 | — |

No se cambió ninguna decisión aprobada ni se agregó o eliminó ninguna tabla.

Lectura directa en esta sesión: v3.2 (archivo de 64 558 bytes, 2026-11-15 19:09), v3.1, anexo, correcciones y el maestro rev 68, exportado completo a Markdown (99 187 caracteres, 877 líneas; el conector no lo modificó). El texto literal de tu aprobación de D-01..D-08 solo existe en el chat.

## 1. Comparación contra el maestro rev 68

| # | Tema | Maestro rev 68 | v3.2 | Resolución |
|---|---|---|---|---|
| 1 | Subfase 0.8 | Aparece en el roadmap (marcada como actual) y en el Registro de cambios (C-09) | No es subfase oficial; el roadmap de Fase 0 es 0.1–0.7 | Criterio adoptado por ti. Maestro sin modificar; corrección preparada en 2.2 |
| 2 | T-11 y T-12 | No existen (llega a T-10) | Existen como propuestas no aprobadas | Se agregan solo en este documento |
| 3 | P-11 | No existe | No existe (se había propuesto en v3.1) | Eliminado; sustituido por validación funcional en Fase 4 (sección 5) |
| 4 | Promoción y varias campañas | T-07 deja abierta la necesidad de una tabla de unión | Se resuelve con Campaña → Brief → `promotion_code`, con una condición | Sección 5; el maestro queda con el texto anterior hasta una actualización autorizada |
| 5 | Subfases de las fases 3, 6 y 9 | Las listas de alcance traen más elementos que las subfases numeradas del prompt original (p. ej. Fase 3: 10 elementos para 3.1–3.9) | Se conserva la numeración original y se asigna cada elemento extra a una subfase | Mapeo propuesto en la sección 8 (no es decisión aprobada) |
| 6 | Estado de la Fase 0 | «COMPLETADA CON LIMITACIONES DOCUMENTADAS» | Igual; es dictamen técnico, no aceptación | Sin cambio |

Equivalencia: lo anterior se comprobó leyendo las secciones (roadmap, registro de cambios, matriz de decisiones, modelo de datos, T-07), no solo por títulos. Límite: no releí cada celda de las tablas del maestro.

## 2. Ajustes, corrección preparada y discrepancias

### 2.1 Ajuste en el Anexo B
La copia del Anexo B incluida aquí cambia una frase: donde decía que la relación de una promoción con varias campañas «haría falta una tabla de unión», ahora remite a la sección 5. El archivo `correcciones_fase0_v3.md` original no se tocó.

### 2.2 Corrección preparada para el maestro (NO aplicada; requiere tu autorización)
1. Roadmap: quitar la fila 0.8; cerrar la Fase 0 en 0.7; mover la marca de «subfase actual».
2. Registro de cambios C-09: reformular como actividad de revisión, no como subfase.
3. Matriz de decisiones: agregar T-11 y T-12 como PROPUESTA TÉCNICA.
4. Modelo de datos (T-07, `promotion_rules`) y resumen de campañas: sustituir «tabla de unión» por la solución de la sección 5.
5. Roadmap de las fases 3, 6 y 9: alinear las listas con la numeración original (sección 8).

### 2.3 Registro de discrepancias
| ID | Discrepancia | Estado |
|---|---|---|
| DISC-1 | 0.8 en el maestro | ABIERTA hasta actualización autorizada del maestro; resuelta en este documento |
| DISC-2 | T-11/T-12 ausentes del maestro | ABIERTA (igual) |
| DISC-3 | Texto de T-07 sobre tabla de unión | ABIERTA (igual) |
| DISC-4 | Numeración de subfases 3, 6, 9 | ABIERTA; mapeo propuesto |
| DISC-5 | P-11 en v3.1 | RESUELTA: eliminado |
| DISC-6 | Anexo anterior y v3.1 como documentos vigentes | RESUELTA: sustituidos documentalmente |

## 3. Cinco niveles de evidencia

Ningún componente sube de nivel sin la evidencia que el nivel exige. El nivel 1 es solo diseño documental.

| Nivel | Qué significa | Evidencia que exige | Permite considerar realizado | NO permite afirmar | Cómo se documenta | Para avanzar |
|---|---|---|---|---|---|---|
| 1 Diseñado | Descrito en el documento | Texto revisado y consistente | La definición y la auditoría documental | Que funciona, compila o es seguro | Sección del documento y matrices | Tu autorización de la fase que lo implementa |
| 2 Implementado | Existe código o migración | Código en control de versiones | La construcción | Que sea correcto o corra | Commit y lista de archivos | Ejecutar la suite local |
| 3 Probado en local | Pruebas automáticas corren en entorno local | Registro reproducible (comando, resultado, fecha, versión) | Comportamiento en local | Comportamiento con servicios reales | Informe de pruebas | Disponer de servicios reales autorizados |
| 4 Probado con servicios reales | Probado con Supabase, Cohere o hosting reales | Ejecución real con registros | Funciona en esas condiciones | Uso en producción o cumplimiento | Informe con entorno, fecha y límites | Tu revisión |
| 5 Validado por el propietario | Tú lo aceptaste | Aceptación expresa registrada | Aceptado por ti | Ausencia de defectos o aptitud para producción | Registro de decisión | — |

Confirmación expresa: todos los componentes siguen en nivel 1 porque no existe evidencia adicional.

| Componente | Nivel | Qué NO se hizo |
|---|---|---|
| Arquitectura y estructura | 1 | Nada construido |
| Modelo de datos (27 tablas) | 1 | No se ejecutó SQL |
| RLS, funciones y triggers | 1 | No se probaron políticas reales |
| Storage, exportación y recuperación | 1 | No se probaron |
| Servicio de IA y Cohere | 1 | Cero llamadas |
| Scoring y bloqueos | 1 | Las cifras se calcularon aparte; no hay motor ejecutable |
| Frontend y UX | 1 | Solo diseño |
| Plan de pruebas | 1 | Docker, Playwright, Deno y CLI de Supabase sin verificar |
| Infraestructura y repositorio | No existen | — |
| D-01..D-08 | 5 (decisiones, no componentes) | — |

## 4. Inventario de las 27 tablas

Procedencia de las 7 de apoyo (según el maestro rev 68, sección Modelo de datos): tres ya estaban propuestas por el autor desde versiones anteriores (`audit_rubric_versions`, `channel_rules`, `ai_quotas`) y cuatro nacen de tus decisiones (`role_permissions` y `membership_permission_grants` de D-04, `commercial_block_exceptions` de D-07, `validation_settings_versions` de D-06). Las tres primeras son propuestas del autor que nunca se aprobaron expresamente como tablas, y coinciden con las de justificación débil o diferible señaladas abajo.

Verificación: las 27 tablas del maestro corresponden a las 20 del prompt original más 7 de apoyo; no se agregó ni eliminó ninguna en la consolidación. Los 27 nombres aparecen en el maestro rev 68 (comprobación de presencia, no de contenido). Módulo = fase que primero la usa.

### Las 20 del diseño original
| Tabla | Función | Relaciones principales | Módulo | Necesidad | Riesgo de duplicidad |
|---|---|---|---|---|---|
| organizations | Raíz del aislamiento multi-tenant | Padre de todas | 1 | Alta | Ninguno |
| profiles | Datos de la persona | 1:1 con usuario de Auth | 1 | Alta | Bajo |
| memberships | Persona en organización con roles | organizations, profiles | 1 | Alta | Ninguno |
| brand_guidelines | Cabecera de la guía de marca | brand_guideline_versions | 2 | Media | MEDIO: casi redundante con su tabla de versiones (T-10) |
| brand_guideline_versions | Guía versionada | brand_guidelines | 2 | Alta | Bajo |
| campaigns | Agrupa el trabajo | briefs, piezas, promociones | 1–2 | Alta | Ninguno |
| briefs | Brief de 16 campos | campaigns, copy_versions | 2 | Alta | Bajo |
| creative_assets | Arte subido | creative_pieces, copy_versions | 3 | Alta | Bajo |
| creative_pieces | Pieza, estado y versión vigente | campaigns, briefs, versiones | 1 y 6 | Alta | Ninguno |
| copy_versions | Texto versionado, inmutable | creative_pieces, briefs | 2 | Alta | Ninguno |
| audits | Resultado de auditoría | versiones, ai_runs, rúbrica, ajustes | 3 | Alta | Ninguno |
| audit_findings | Hallazgos y su revisión | audits | 3 | Alta | Ninguno |
| approvals | Decisión humana sobre versión exacta | versiones, audits | 6 | Alta | Ninguno |
| comments | Comentarios y solicitudes de cambio | creative_pieces, audit_findings | 6 | Media | Bajo |
| promotion_rules | Reglas de promoción por SKU | campaigns | 4 | Alta | Medio (ver sección 5) |
| performance_metrics | Métricas por pieza y variante | creative_pieces | 8 | Alta | Bajo |
| ab_tests | Pruebas A/B | creative_pieces, métricas | 8 | Media | Bajo |
| ai_runs | Registro de llamadas a IA | organizations, profiles | 2 | Alta | Bajo frente a ai_quotas |
| ai_prompt_versions | Prompts versionados | organizations | 2 | Alta | Ninguno |
| activity_logs | Auditoría general | Referencia genérica | 1 | Alta | Ninguno |

### Las 7 de apoyo (agregadas en el diseño v2/v3, no estaban en el prompt original)
| Tabla | Función | Necesidad funcional | Riesgo de duplicidad | Hallazgo |
|---|---|---|---|---|
| role_permissions | Permisos por rol | Alta: sin ella los roles quedan en código (D-04) | Bajo | Justificada |
| membership_permission_grants | Permisos por persona | Alta: P-05 y `block.exception.grant` por persona | Bajo frente a role_permissions (uno es por rol, otro por persona) | Justificada |
| commercial_block_exceptions | Excepciones a bloqueos confirmados | Alta: D-07 pide excepción identificada, revocable y auditada | Medio frente a `audit_findings` (podría guardarse allí, pero obligaría a reescribir el hallazgo) | Justificada |
| audit_rubric_versions | Pesos, rangos y cobertura versionados | Alta: auditorías reproducibles | MEDIO frente a validation_settings_versions | Justificada; podría fusionarse con la siguiente, perdiendo el check de suma 100. Decisión de Fase 1 |
| validation_settings_versions | Tolerancia y precisión versionadas | Alta: D-06 | Medio (ver arriba) | Ídem |
| channel_rules | Reglas por canal | Media: las exige 5.2; no se usa hasta la Fase 5 | Bajo | Justificada, pero diferible |
| ai_quotas | Topes de IA | Media: D-03 pide control de costos | MEDIO frente a `ai_runs` y a columnas en `organizations` | Debilmente justificada: podrían ser columnas de la organización; la tabla es defendible solo si habrá topes por función |

Hallazgos sin modificar el modelo: ninguna tabla queda sin justificación, pero tres tienen justificación débil o diferible (brand_guidelines, ai_quotas, channel_rules) y una pareja puede fusionarse (rúbrica y ajustes). Se dejan como decisión para la Fase 1; no cambié el modelo.

## 5. Promociones y campañas

### 5.1 Solución evaluada: Campaña → Brief → `promotion_code`
Según el maestro: `campaigns` 1→N `briefs`; cada brief tiene `promotion_code` opcional; `promotion_rules` tiene una fila por promoción y SKU, agrupadas por `promotion_code`, con una FK a campaña y sin versión ni inmutabilidad.

| Requisito | ¿Lo permite? | Condición o límite |
|---|---|---|
| Una campaña con varios briefs | Sí | Es la relación 1→N existente |
| Un brief asociado a una promoción | Sí | Un código por brief |
| Varias campañas con una misma promoción | Sí, con condición | La FK de campaña en `promotion_rules` no debe ser obligatoria ni exclusiva: se trataría como «campaña de origen» opcional. Si siguiera obligatoria, usar la misma promoción en otra campaña exigiría duplicar filas (rompe «evitar duplicidad») |
| Trazabilidad | Parcial | Pieza → brief de origen (opcional) → promoción. Una pieza sin brief queda sin enlace |
| Reportes por campaña y promoción | Sí, con consultas | Se obtienen uniendo campañas, briefs y `promotion_rules` por (organización, `promotion_code`); no hay FK real, así que la integridad depende de un trigger |
| Duplicidad y ambigüedad | Riesgo medio | Los datos de cabecera (fechas, condiciones) se repiten en cada fila de SKU y pueden contradecirse; `promotion_rules` es editable, así que una edición posterior cambiaría la base de auditorías pasadas si no se guarda un instante de los datos |

### 5.2 Caso que no se resuelve con las 27 tablas (decisión del propietario si aplica)
Caso C-1: un brief que necesite dos promociones a la vez (p. ej. un banner con dos ofertas). Con un `promotion_code` por brief no cabe. Consecuencia: habría que separar en dos briefs/piezas (operativo) o permitir varios códigos por brief, lo que exigiría un arreglo de códigos validado por trigger o una tabla de unión (no se agrega ninguna). Esto es un caso a confirmar con la operación real; no lo registro como pendiente independiente.

### 5.3 Estado y validación
T-11 se conserva como PROPUESTA TÉCNICA NO APROBADA: usar Campaña → Brief → `promotion_code`, con campaña de origen opcional en `promotion_rules`, trigger que valide que el código del brief exista en la misma organización, y un instante (snapshot) de la promoción guardado en la auditoría. No agregué tablas ni creé P-11.

Validación funcional que se hará en la Fase 4 (4.1 y 4.7), con criterios:
1. Una promoción usada en dos campañas no duplica filas.
2. Un brief sin código y una pieza sin brief se manejan con una advertencia, no con error.
3. El trigger rechaza un `promotion_code` inexistente o de otra organización.
4. Filas del mismo código con fechas distintas generan una incoherencia marcada.
5. Editar una promoción no cambia el resultado de auditorías pasadas.
6. El reporte por campaña y promoción coincide con el conteo manual de un caso de prueba.
7. Se evalúa el caso C-1 con datos reales.

## 6. Matriz de decisiones D-01 a D-08

| ID | Decisión | Estado | Ubicación en el maestro rev 68 |
|---|---|---|---|
| D-01 | Independencia total de RevNavigator | APROBADA | Registro de decisiones; Matriz |
| D-02 | Organización y proyecto de Supabase exclusivos | APROBADA; creación pendiente (P-01) | Ídem; Crear la organización y el proyecto |
| D-03 | Cohere solo en desarrollo y pruebas; proveedor desacoplado | APROBADA | Registro; Estrategia de IA |
| D-04 | Cinco roles, varios por persona, permisos por clave en backend y frontend | APROBADA | Registro; Seguridad y RLS |
| D-05 | Cobertura mínima 60 %; el puntaje no aprueba; un bloqueo confirmado impide aprobar | APROBADA PROVISIONALMENTE | Registro; Motores determinísticos |
| D-06 | Tolerancia inicial 0.5 pp, configurable | APROBADA como valor inicial | Registro; Precios, redondeo y descuentos |
| D-07 | Excepciones con permiso, justificación, responsable y auditoría | APROBADA | Registro; Bloqueos y excepciones |
| D-08 | Aprobaciones humanas y trazables | APROBADA | Registro; Separación de funciones |

R-01..R-05 (INCORPORADAS POR INSTRUCCIÓN) están en el Anexo B (A a E).

## 7. Matriz de propuestas técnicas T-01 a T-12

Ninguna está aprobada. Aceptar la Fase 0 (A-01) NO aprueba ninguna de ellas: cada una se aprueba, modifica o rechaza con tu decisión expresa, en la fase en que se evalúa (columna «Se evalúa en»). Esto corrige la redacción del Anexo B y del maestro rev 68, que decían que se aceptaban con la Fase 0 (ver CC-02).

| ID | Propuesta | Justificación | Impacto | Riesgo | Se evalúa en | Estado |
|---|---|---|---|---|---|---|
| T-01 | Matriz de 17 permisos (`finding.confirm`, `piece.publish` nuevos) | La v2 dejaba sin permiso confirmar hallazgos y publicar | Seguridad y roles | Permisos de más o de menos | 1.6 | NO APROBADA |
| T-02 | Tabla de transiciones de estado | La v2 no definía quién ejecuta cada transición | Workflow | Estados bloqueados | 6.1 | NO APROBADA |
| T-03 | Motivo escrito de al menos 30 caracteres en excepciones y descartes | Evitar justificaciones vacías | Auditoría | Fricción | 6.5 | NO APROBADA |
| T-04 | Contribuyentes: autor del copy y quien subió el arte | Dar sentido a «creó o modificó» | Aprobaciones | Casos de borde | 6.5 | NO APROBADA |
| T-05 | Misma independencia al confirmar, descartar y conceder excepciones | Coherencia con la separación de funciones | Equipos pequeños | Bloqueo operativo | 6.5 | NO APROBADA (recomendación) |
| T-06 | Revocar una excepción usada devuelve la pieza a Pendiente de aprobación | Mantener la aprobación válida | Workflow | Reprocesos | 6.5 | NO APROBADA |
| T-07 | `promotion_rules` por promoción y SKU con `promotion_code` | Evaluar «hasta N %» entre SKU | Promociones | Datos repetidos por SKU | 4.1 | NO APROBADA |
| T-08 | Notas enteras 0–10; rangos con límite inferior incluido sobre el puntaje redondeado | Cubrir todos los valores | Scoring | Notas decimales rechazadas | 3.7 | NO APROBADA |
| T-09 | FK compuestas y exportación en dos partes | Integridad entre organizaciones y límite de 2 s de CPU | Datos y Storage | No probada | 1.8 y 9.8 | NO APROBADA |
| T-10 | Conservar `brand_guidelines` y revisarla | Decidir si la cabecera sobra | Datos | Duplicidad | 1.8 | NO APROBADA |
| T-11 | Campaña → Brief → `promotion_code` con campaña de origen opcional, trigger y snapshot | Resolver promociones compartidas sin tabla nueva | Promociones y reportes | Caso C-1; sin FK real | 4.1 y 4.7 | NO APROBADA |
| T-12 | Subfase 0.8 como oficial | Dar nombre a la revisión final | Roadmap | Alterar el roadmap aprobado | Ahora (decisión tuya) | NO APROBADA; 0.8 no es oficial |

## 8. Roadmap completo de las fases 0 a 9

Fuente: identificadores y nombres, del prompt original; alcance por fase, del maestro rev 68; el detalle por subfase (objetivo, entregables, dependencias, criterios, riesgos) lo derivé yo de esas dos fuentes y del diseño, y es PROPUESTA hasta que lo apruebes. Criterios generales de cierre de cualquier fase (prompt original): funcionalidad implementada, pruebas ejecutadas, errores críticos corregidos, sin regresiones sin documentar, documentación actualizada, resultado verificable. Ninguna fase posterior está autorizada; todas las futuras están PENDIENTE.

Mapeo propuesto de los elementos extra del maestro: Fase 3: clasificación de afirmaciones y estados de hallazgos de IA → 3.4; «diseño y UX» → 3.5 y 3.6. Fase 6: aprobaciones con separación de funciones, confirmación y descarte de hallazgos y excepciones → 6.5 (con permisos en 6.7). Fase 9: pruebas integrales y de concurrencia → 9.5 y 9.6; exportación y recuperación → 9.8, probada en 9.5.

### Fase 0 — Discovery y arquitectura (0.1–0.7)
| ID | Nombre | Objetivo y alcance | Entregables | Dependencias | Aceptación | Riesgos | Estado |
|---|---|---|---|---|---|---|---|
| 0.1 | Inspección del entorno | Conocer qué hay disponible | Sección Línea base | — | Entorno descrito | Herramientas sin verificar | COMPLETADA CON LIMITACIONES |
| 0.2 | Definición de arquitectura | Capas, IA desacoplada, estructura | Arquitectura y estructura | 0.1 | Revisada y consistente | Es diseño | COMPLETADA |
| 0.3 | Modelo de datos | 27 tablas, relaciones, controles | Modelo, auditoría, matriz | 0.2 | Sin tablas nuevas; auditado | Sin SQL | COMPLETADA CON LIMITACIONES |
| 0.4 | Seguridad | RLS, permisos, separación de funciones | Seguridad y RLS | 0.3 | Matriz de 17 claves | RLS sin probar | COMPLETADA CON LIMITACIONES |
| 0.5 | Diseño de módulos | Módulos y transiciones | Diseño de módulos | 0.2 | Cobertura de módulos | Pantallas por detallar | COMPLETADA |
| 0.6 | Estrategia de pruebas | Qué y cómo probar | Plan de pruebas | 0.3–0.5 | Casos R-01..R-05 | Herramientas sin instalar | COMPLETADA CON LIMITACIONES |
| 0.7 | Registro de riesgos y dependencias | Riesgos y dependencias externas | Riesgos, Configuraciones | 0.1–0.6 | Riesgos con mitigación | Retención y respaldos sin determinar | COMPLETADA |

(Estados de 0.1–0.7 según el maestro; son dictamen técnico, no aceptación.)

### Fase 1 — Foundation & Command Center (requiere A-01 y tu autorización expresa)
| ID | Nombre | Objetivo y alcance | Entregables | Dependencias | Aceptación | Riesgos | Estado |
|---|---|---|---|---|---|---|---|
| 1.1 | Estructura del proyecto | Esqueleto modular con ES Modules, capas UI, dominio, servicios, IA | Repositorio base, README | A-01, P-02 | Arranca en local; refleja la estructura del maestro | Acoplar UI y dominio | PENDIENTE |
| 1.2 | Sistema visual | Tokens y componentes base | CSS y componentes | 1.1 | Sin elementos recargados | Inconsistencia | PENDIENTE |
| 1.3 | Navegación | Sidebar, header, rutas | Shell de la app | 1.2 | Navegación clara | Navegación confusa | PENDIENTE |
| 1.4 | Autenticación | Supabase Auth, sesiones, rutas protegidas | Login y sesión | 1.1, P-01 | Rutas protegidas probadas | Manejo de sesión | PENDIENTE |
| 1.5 | Organización y usuarios | organizations, profiles, memberships | Alta de organización y personas | 1.4, P-04 | Aislamiento entre organizaciones | Fuga entre organizaciones | PENDIENTE |
| 1.6 | Roles y permisos | role_permissions, permisos por persona, 17 claves | Funciones de permisos | 1.5 | Matriz probada en backend y frontend | Permisos solo en la interfaz | PENDIENTE |
| 1.7 | Supabase | Proyecto, Storage, secretos | Entorno configurado | P-01 | Sin credenciales en el repositorio | Plan gratuito | PENDIENTE |
| 1.8 | Migraciones | Esquema versionado y RLS de las tablas de la fase | Migraciones reproducibles | 1.6, 1.7 | Pruebas de aislamiento de las tablas creadas | Primer SQL real | PENDIENTE |
| 1.9 | Dashboard inicial | Command Center básico | Dashboard | 1.3, 1.8 | Carga sin datos | Exceso de tarjetas | PENDIENTE |

### Fase 2 — Copy Studio
| ID | Nombre | Objetivo y alcance | Entregables | Dependencias | Aceptación | Riesgos | Estado |
|---|---|---|---|---|---|---|---|
| 2.1 | Brief | Brief de 16 campos y su versión | Formulario y tabla | 1.8 | Validaciones y versiones | Formularios largos | PENDIENTE |
| 2.2 | Integración Cohere | Servicio de IA desacoplado, cuotas, registro | Servicio y ai_runs | P-03 | Llamadas registradas; sin claves en cliente | Límites de la clave de prueba | PENDIENTE |
| 2.3 | Generación de propuestas | Varias propuestas por brief | Generación | 2.1, 2.2 | Salida estructurada válida | Calidad variable | PENDIENTE |
| 2.4 | Fórmulas de copywriting | Fórmulas aplicables | Catálogo de fórmulas | 2.3 | Aplicación verificable | Sesgo hacia plantillas | PENDIENTE |
| 2.5 | Edición | Edición humana de copy | Editor | 2.3 | Cambios guardados como versión | Pérdida de cambios | PENDIENTE |
| 2.6 | Comparación | Comparar versiones | Vista de comparación | 2.5 | Diferencias correctas | Confusión de versiones | PENDIENTE |
| 2.7 | Versionado | Versiones inmutables con autor | copy_versions | 2.5 | Autor por trigger; sin edición de versiones | Autoría falsificable | PENDIENTE |
| 2.8 | Pruebas | Pruebas de la fase | Informe | 2.1–2.7 | Suite ejecutada | Mocks tomados por integración real | PENDIENTE |

### Fase 3 — Creative Auditor
| ID | Nombre | Objetivo y alcance | Entregables | Dependencias | Aceptación | Riesgos | Estado |
|---|---|---|---|---|---|---|---|
| 3.1 | Carga de imágenes | Subir artes con hash y MIME | creative_assets, Storage | 1.7, P-07 | Hash y MIME verificados; objeto inmutable | Archivos grandes | PENDIENTE |
| 3.2 | OCR | Extraer texto del arte | Resultado de OCR | 3.1 | Texto como inferencia, no como hecho | Cohere sin OCR confirmado | PENDIENTE |
| 3.3 | Integración de visión | Modelo de visión tras el servicio de IA | Adaptador de visión | 2.2 | Salida estructurada confirmada | Modelo de visión no confirmado | PENDIENTE |
| 3.4 | Auditoría textual | Hallazgos, clasificación de afirmaciones, estados de hallazgo | audit_findings | 3.2, 3.3 | R-01 y R-02 pasan | Falsos positivos | PENDIENTE |
| 3.5 | Auditoría visual | Hallazgos visuales | Auditoría visual | 3.3 | Hallazgos de IA no bloquean | Subjetividad | PENDIENTE |
| 3.6 | Auditoría UX | Legibilidad y UX | Auditoría UX | 3.3 | Notas con evidencia | Subjetividad | PENDIENTE |
| 3.7 | Scoring | Motor determinístico en JavaScript | Motor y rúbrica | 3.4–3.6 | Casos límite de R-05 pasan | Redondeo | PENDIENTE |
| 3.8 | Comparación de versiones | Comparar auditorías | Vista | 3.7 | Versión exacta por auditoría | Versiones mezcladas | PENDIENTE |
| 3.9 | Pruebas | Pruebas de la fase | Informe | 3.1–3.8 | Suite ejecutada | Mocks | PENDIENTE |

### Fase 4 — Promotion Validator
| ID | Nombre | Objetivo y alcance | Entregables | Dependencias | Aceptación | Riesgos | Estado |
|---|---|---|---|---|---|---|---|
| 4.1 | Modelo de promociones | promotion_rules y relación con campañas y briefs (T-07, T-11) | Tabla y relación | 1.8, P-06 | Validación funcional de la sección 5.3 | Caso C-1; sin FK real | PENDIENTE |
| 4.2 | Reglas matemáticas | Precios, descuentos, redondeo | Funciones deterministas | 4.1, P-06 | Tolerancia 0.5 pp aplicada | Redondeo | PENDIENTE |
| 4.3 | Validación de vigencias | Fechas y rangos | Validador | 4.1 | Incoherencias marcadas | Zonas horarias | PENDIENTE |
| 4.4 | Validación de condiciones | Condiciones y disponibilidad | Validador | 4.1 | Condiciones contrastadas | Texto ambiguo | PENDIENTE |
| 4.5 | Comparación de fuentes | Brief, regla y arte | Comparador | 4.2–4.4 | Diferencias reportadas | Fuentes incompletas | PENDIENTE |
| 4.6 | Bloqueos comerciales | Bloqueos del motor y confirmados | Bloqueos | 4.5 | Bloqueo confirmado impide aprobar | Falsos bloqueos | PENDIENTE |
| 4.7 | Pruebas | Pruebas de la fase | Informe | 4.1–4.6 | Suite y validación de promociones-campañas | Mocks | PENDIENTE |

### Fase 5 — Channel Adaptation
| ID | Nombre | Objetivo y alcance | Entregables | Dependencias | Aceptación | Riesgos | Estado |
|---|---|---|---|---|---|---|---|
| 5.1 | Modelos de canal | channel_rules por canal | Catálogo | 1.8 | Reglas por organización y canal | Reglas reales sin entregar | PENDIENTE |
| 5.2 | Reglas de extensión | Límites de longitud | Validador | 5.1 | Límites aplicados | Límites cambiantes | PENDIENTE |
| 5.3 | Adaptación | Adaptar copy por canal | Adaptador | 2.3, 5.1 | Versión por canal | Pérdida de sentido | PENDIENTE |
| 5.4 | Consistencia | Coherencia entre canales | Verificador | 5.3 | Diferencias señaladas | Falsas diferencias | PENDIENTE |
| 5.5 | Comparación multicanal | Vista comparativa | Vista | 5.3 | Comparación correcta | — | PENDIENTE |
| 5.6 | Pruebas | Pruebas de la fase | Informe | 5.1–5.5 | Suite ejecutada | Mocks | PENDIENTE |

### Fase 6 — Workflow & Approvals
| ID | Nombre | Objetivo y alcance | Entregables | Dependencias | Aceptación | Riesgos | Estado |
|---|---|---|---|---|---|---|---|
| 6.1 | Estados | Estados y transiciones (T-02) | transition_piece_status | 1.6 | Solo transiciones permitidas | Estados bloqueados | PENDIENTE |
| 6.2 | Asignaciones | Asignar piezas a personas | Asignaciones | 6.1 | Asignación auditada | — | PENDIENTE |
| 6.3 | Comentarios | Hilos y solicitudes de cambio | comments | 6.1 | Comentarios obligatorios donde corresponde | — | PENDIENTE |
| 6.4 | Correcciones | Ciclo de corrección con versión nueva | Flujo | 6.1–6.3 | Aprobación previa no se hereda | Reprocesos | PENDIENTE |
| 6.5 | Aprobaciones | Aprobación humana independiente, confirmación y descarte, excepciones | record_approval, review_finding, excepciones | 6.4, P-04, P-05 | R-02 y R-03 pasan; sin autoaprobación | Menos de dos personas capaces | PENDIENTE |
| 6.6 | Historial | Historial inmutable | activity_logs | 6.5 | Sin UPDATE ni DELETE | Volumen | PENDIENTE |
| 6.7 | Permisos | Permisos del flujo | Claves y políticas | 6.5 | Backend como autoridad | Permisos solo en UI | PENDIENTE |
| 6.8 | Pruebas | Pruebas de la fase | Informe | 6.1–6.7 | Suite ejecutada | Mocks | PENDIENTE |

### Fase 7 — Creative Library
| ID | Nombre | Objetivo y alcance | Entregables | Dependencias | Aceptación | Riesgos | Estado |
|---|---|---|---|---|---|---|---|
| 7.1 | Biblioteca | Repositorio de piezas aprobadas | Vista | 6.5 | Solo versiones identificadas | Volumen | PENDIENTE |
| 7.2 | Búsqueda | Búsqueda de piezas | Búsqueda | 7.1 | Resultados correctos | Rendimiento | PENDIENTE |
| 7.3 | Filtros | Filtros combinables | Filtros | 7.1 | Combinaciones correctas | — | PENDIENTE |
| 7.4 | Versionado | Historial de versiones | Vista | 7.1 | Versión exacta visible | — | PENDIENTE |
| 7.5 | Recuperación | Recuperar versiones y archivos | Función de recuperación | 7.4, T-09 | Recuperación con hash verificado | Exportación sin probar | PENDIENTE |
| 7.6 | Pruebas | Pruebas de la fase | Informe | 7.1–7.5 | Suite ejecutada | Mocks | PENDIENTE |

### Fase 8 — Performance Intelligence
| ID | Nombre | Objetivo y alcance | Entregables | Dependencias | Aceptación | Riesgos | Estado |
|---|---|---|---|---|---|---|---|
| 8.1 | Registro de métricas | performance_metrics | Captura | 1.8 | Valores NULL permitidos | Datos incompletos | PENDIENTE |
| 8.2 | Importación de datos | Importar métricas | Importador | 8.1 | Validación de datos | Formatos | PENDIENTE |
| 8.3 | Indicadores | Indicadores derivados | Cálculos | 8.1 | Fórmulas verificadas | Interpretación | PENDIENTE |
| 8.4 | Comparación de variantes | A/B | ab_tests | 8.3 | Causalidad solo si fue aleatorizado | Conclusiones falsas | PENDIENTE |
| 8.5 | Análisis de resultados | Lectura de resultados | Análisis | 8.3 | Sin afirmar causalidad no probada | — | PENDIENTE |
| 8.6 | Aprendizajes | Registrar aprendizajes | Registro | 8.5 | Trazables a datos | — | PENDIENTE |
| 8.7 | Pruebas | Pruebas de la fase | Informe | 8.1–8.6 | Suite ejecutada | Faltan datos reales | PENDIENTE |

### Fase 9 — Hardening & Release
| ID | Nombre | Objetivo y alcance | Entregables | Dependencias | Aceptación | Riesgos | Estado |
|---|---|---|---|---|---|---|---|
| 9.1 | Seguridad | Revisión de seguridad y RLS | Informe | 1–8 | Matriz de aislamiento completa | Hallazgos tardíos | PENDIENTE |
| 9.2 | Accesibilidad | Revisión de accesibilidad | Informe | 1–8 | Criterios definidos y cumplidos | — | PENDIENTE |
| 9.3 | Rendimiento | Tiempos y carga | Informe | 1–8 | Metas definidas | Hosting | PENDIENTE |
| 9.4 | Responsive | Pantallas pequeñas | Informe | 1–8 | Uso en móvil | — | PENDIENTE |
| 9.5 | Pruebas integrales | Flujo completo y recuperación | Informe | 1–8 | Flujos completos pasan | Mocks | PENDIENTE |
| 9.6 | Pruebas de concurrencia | Aprobaciones y cuotas simultáneas | Informe | 6.5 | Sin condiciones de carrera | Difícil de reproducir | PENDIENTE |
| 9.7 | Documentación | Documentación final | Documentos | 9.1–9.6 | Actualizada | — | PENDIENTE |
| 9.8 | Preparación de despliegue | Hosting, dominio, respaldos, exportación | Plan | P-09, P-10 | Plan aceptado | Plan gratuito sin respaldos | PENDIENTE |
| 9.9 | Auditoría de aceptación | Revisión final | Informe | 9.1–9.8 | Criterios de la fase | — | PENDIENTE |

## 9. Matriz de pendientes P-01 a P-10

Aceptación documental de la Fase 0 (A-01) ≠ preparación operativa para construir. Ninguno de los diez impide aceptar la arquitectura; todos impiden o limitan una fase posterior. Dos de ellos (P-07, P-08) son valores propuestos dentro del diseño: aceptar la Fase 0 sin decidirlos los deja como propuestas.

| ID | Qué falta | Por qué importa | Qué bloquea | Para cerrarlo | ¿Impide aceptar Fase 0? |
|---|---|---|---|---|---|
| P-01 | Organización y proyecto de Supabase propios | D-01/D-02: no mezclar con RevNavigator | 1.4, 1.7, 1.8 | Tu creación o autorización; sin credenciales en chat | No; bloquea Fase 1 |
| P-02 | Repositorio de GitHub y visibilidad | Sin repositorio no hay código versionado | 1.1 | Nombre, propietario, visibilidad | No; bloquea Fase 1 |
| P-03 | Clave de prueba de Cohere | La IA se prueba con ella | Fase 2 | Clave cargada como secreto, nunca en chat | No; bloquea Fase 2 |
| P-04 | Personas y roles (≥2 que puedan aprobar) | La separación de funciones exige dos personas | 1.5 recomendable, 6.5 necesario | Lista de personas y roles | No |
| P-05 | Permisos individuales para conceder excepciones | `block.exception.grant` es por persona | 6.5 | Quién puede, concedido con `org.manage` | No |
| P-06 | Moneda e impuestos | Comparar precios exige base fiscal | 4.1, 4.2 | Moneda base y si los precios incluyen impuestos | No |
| P-07 | Límite de imágenes (propuesta 10 MB) | Costos y límites de carga | 3.1 | Tu decisión | No |
| P-08 | Tope de tolerancia (propuesta 5 pp) | Evita tolerancias abusivas | 4.2 | Tu decisión | No |
| P-09 | Retención de datos y respaldos | Riesgo de datos y recuperación | 9.8 | Política y plan de Supabase | No |
| P-10 | Dominio y hosting definitivos | Limita la CSP y el despliegue | 9.8 | Tu decisión | No |

No agregué pendientes artificiales. A-01 es tu decisión, no un pendiente de la lista.

## 10. Matriz de consistencia A–E

Nombres de sección del maestro rev 68. Nivel 1 en todo.

| Área | A. Afirmaciones de IA | B. Hallazgos críticos de IA | C. Sin autoaprobación | D. Datos y seguridad | E. Scoring |
|---|---|---|---|---|---|
| Arquitectura | Estrategia de IA: Clasificación de afirmaciones | Motores determinísticos: Bloqueos y excepciones | Seguridad y RLS: Separación de funciones | Arquitectura objetivo | Motores: Puntaje de auditoría |
| Datos | `audit_findings`: kind_proposed, kind, verification_source, source_ref | `review_state` | `approvals`; `created_by`/`uploaded_by` | Auditoría final del modelo | `audit_rubric_versions`, `audits` |
| Backend | Contraste determinístico | `review_finding` | `record_approval` + trigger | security definer; `verify_assets_integrity` | Motor en JavaScript |
| Frontend | Insignia solo si la asigna el servidor | Aviso de hallazgos sin revisar | Botón «Aprobar» desactivado con explicación | URL firmada | Cobertura y «Evaluación incompleta» |
| Seguridad | La IA no escribe `kind` | `finding.confirm`, `finding.dismiss` | Sin INSERT/UPDATE/DELETE de cliente | Matriz de 17 claves | Rúbrica inmutable |
| Workflow | — | Flujo de estados y transiciones | Aprobación exige independencia | Nueva versión invalida la aprobación | El puntaje no cambia estados |
| Auditoría | Estados del hallazgo | `activity_logs` | Aprobaciones inmutables | Trazabilidad de excepciones | Versión de rúbrica y cobertura |
| Scoring | — | Bloqueo confirmado prevalece | — | — | Reglas 1–7, ejemplo 75.7, casos límite |
| Pruebas | Plan de pruebas R-01 | R-02 | R-03 | R-04 | R-05 |
| Documentación | Registro de cambios C-01..C-10 | Ídem | Ídem | Ídem | Ídem |

## 11. Riesgos y dependencias

| Riesgo o dependencia | Impacto | Estado |
|---|---|---|
| La Supabase conectada hoy pertenece a otra infraestructura (D-01/D-02) | Alto | Se mitiga con organización nueva (P-01) |
| Plan gratuito: 2 proyectos activos entre organizaciones, pausa tras inactividad, sin respaldos | Medio | Comprobar en el panel |
| Clave trial de Cohere: 1 000 llamadas al mes, 20 por minuto, no apta para producción | Medio | Diseño desacoplado (D-03) |
| Visión y salida estructurada de Cohere sin confirmar | Medio | NO VERIFICADO; condiciona Fase 3 |
| RLS, triggers y funciones sin probar | Alto | NO VERIFICADO |
| Organización con menos de dos personas capaces de aprobar | Medio | Efecto buscado de R-03; P-04 |
| Edge Functions con 2 s de CPU limitan la exportación | Medio | T-09; no probado |
| Retención de datos en Cohere y respaldos sin determinar | Medio | P-09 |
| Promoción compartida entre campañas sin FK real; caso C-1 | Medio | T-11; validación en Fase 4 |
| Hosting definitivo limita la CSP | Bajo | P-10 |

Dependencia entre fases: 1 → 2 → 3 y 4 → 5 → 6 → 7 → 8 → 9.

## 12. Limitaciones

No se ejecutó SQL; no se probó RLS; no se probó Storage ni la exportación y recuperación; no hubo llamadas a Cohere; el scoring no es un motor ejecutable y sus cifras se calcularon aparte; Docker, Playwright, Deno y la CLI de Supabase sin verificar; no existe infraestructura propia. Distinción: diseñado = sí; implementado = no; probado = no; validado por ti = solo D-01..D-08.

## 13. Criterios de aceptación documental y dictamen

| Criterio | Resultado |
|---|---|
| Decisiones D-01..D-08 sin cambios | Se cumple (contra su registro en el maestro) |
| 27 tablas, ninguna agregada ni eliminada | Se cumple |
| Cinco roles | Se cumple |
| Cobertura mínima 60 % y tolerancia 0.5 pp | Se cumple |
| Sin autoaprobación; corroboración humana de hallazgos de IA; excepciones auditables; aprobaciones por versión exacta | Se cumplen en diseño |
| Propuestas T-01..T-12 sin pasar por decisiones | Se cumple |
| P-01..P-10 abiertos | Se cumple |
| Roadmap completo con 0.1–0.7 como oficial | Se cumple en este documento; el maestro rev 68 aún muestra 0.8 |
| Niveles de evidencia | Todo en nivel 1 |

DICTAMEN DEL AUTOR (v3.2): LISTA CON LIMITACIONES DOCUMENTADAS. La auditoría independiente A-01 está en `expediente_auditoria_A01.md`.

| Limitación | ¿Impide la aceptación documental? |
|---|---|
| Todo es nivel 1 (sin SQL, RLS, Cohere, scoring, herramientas ni Storage probados) | No: es propio de una fase de diseño; sí impide afirmar que funciona |
| El maestro rev 68 conserva 0.8 y no incluye T-11/T-12 | No, si aceptas este documento como referencia; conviene actualizar el maestro con tu autorización |
| Caso C-1 y validación de promociones-campañas pendiente de Fase 4 | No |
| Detalle por subfase de las fases 1–9 derivado por mí | No, pero es propuesta hasta que lo apruebes |
| P-01..P-10 abiertos | No para aceptar la arquitectura; sí para iniciar fases |

### 13.1 Qué significa A-01
A-01 es la aceptación de ESTA documentación como línea base de arquitectura (diseño, nivel 1): el conjunto de las 27 tablas, las decisiones D-01..D-08, las correcciones A–E incorporadas por instrucción, el roadmap 0.1–0.7 y las fases 1–9, y la separación entre decidido, propuesto y pendiente. A-01 NO aprueba T-01..T-12, NO cierra P-01..P-10, NO autoriza construir y NO eleva ningún componente por encima del nivel 1.

### 13.2 Condiciones antes de iniciar la Fase 1
1. Tu aceptación A-01 (o tus correcciones).
2. Tu autorización expresa de la Fase 1.
3. P-01 y P-02 resueltos (organización y proyecto de Supabase; repositorio).
4. P-04 al menos con la lista inicial de personas, antes de 1.5.
5. Decisión tuya sobre T-01 antes de 1.6, y sobre T-09 y T-10 antes de 1.8 (son las propuestas que esas subfases necesitan; sin decisión se implementaría algo no aprobado).

Aceptación documental no autoriza construir. El autor no inició la Fase 1 ni tomó la decisión A-01 por ti.

---
# Anexo B — Correcciones obligatorias A–E (texto íntegro)

# Correcciones obligatorias de la revisión final — Fase 0 v3 (versión extendida)

Documento: Copy & Creative Intelligence — Fase 0: Discovery y Arquitectura, v2 → v3.
Este archivo contiene SOLO las correcciones A a E pedidas en la revisión final y su efecto en el resto del diseño. No es el documento completo.

Contexto que no cambia: decisiones D-01 a D-08 conservadas; 5 roles (admin, ecommerce, diseno, marketing, revisor_aprobador) con varios roles por persona; permisos por clave aplicados en backend (RLS y funciones) y frontend; 27 tablas (no se agrega ninguna); pesos de la rúbrica sin cambio; cobertura mínima 60 %; tolerancia inicial 0.5 puntos porcentuales; excepciones con permiso específico, justificación y auditoría; aprobaciones humanas y trazables.

Estados de cada elemento: APROBADA (decisión del propietario), INCORPORADA POR INSTRUCCIÓN (viene de la revisión final), PROPUESTA TÉCNICA (mía, sin aprobar), PENDIENTE DEL PROPIETARIO.

---

## A. Clasificación de afirmaciones de IA (R-01, INCORPORADA POR INSTRUCCIÓN)

Regla: la IA nunca puede certificarse a sí misma como fuente de un hecho verificado. Puede proponer hechos; solo el contraste contra fuentes confiables o reglas determinísticas permite clasificarlos como verificados.

| Clase | Definición | Quién la asigna | Efecto |
|---|---|---|---|
| Hecho verificado | Respaldado por una fuente identificable y contrastable: regla determinística, brief, regla de promoción, guía de marca vigente o fuente que una persona revisora cita | El servidor tras el contraste, o una persona con `finding.confirm` que cita la fuente | Puede fundamentar un bloqueo confirmado |
| Inferencia | Interpretación no confirmada (p. ej., texto que el modelo lee de una imagen) | La IA propone; el servidor asigna | Se muestra como tal; no bloquea |
| Recomendación | Sugerencia de mejora | La IA o una persona | No es un hecho; no bloquea |
| Pendiente de validación | Requiere comprobación: dato faltante o afirmación sin fuente | El servidor | No bloquea; pide revisión |

Cómo se aplica:
1. La IA devuelve cada afirmación con la clase que propone y la evidencia que usó (cita del texto, zona de la imagen o dato del brief). Se guarda en `kind_proposed`; no es la clase final.
2. El servidor asigna `kind`. Si la IA propone «hecho verificado» y el servidor no puede contrastarlo, lo guarda como «pendiente de validación», conserva la propuesta original y nunca lo sube a hecho.
3. Se contrastan por regla determinística: cifras, fechas y porcentajes contra brief y reglas de promoción; palabras prohibidas contra la guía de marca; extensión contra `channel_rules`. Todo lo demás queda como inferencia o pendiente hasta que una persona lo confirme y cite la fuente.
4. Lo que el modelo lee de una imagen es siempre inferencia hasta que una persona confirme la lectura.
5. Una fuente que la IA cite no cuenta mientras una persona no la compruebe. La IA no certifica cumplimiento regulatorio.
6. La base de datos rechaza guardar `kind` = hecho verificado sin `verification_source` distinta de `ia` y sin `source_ref` (check constraint).

Dónde quedó documentada:
- Arquitectura: principio «la IA propone y explica, y nunca se certifica a sí misma».
- Prompts: antes obligaban a la IA a «etiquetar» cada afirmación como hecho verificado (contradicción corregida). Ahora piden proponer la clase, adjuntar evidencia y omitir la zona si no se puede ubicar; la clase final la asigna el servidor.
- Modelo de datos, `audit_findings`: `kind_proposed`, `kind` (enums: hecho verificado, inferencia, recomendación, pendiente de validación), `verification_source`, `source_ref`.
- Auditoría/UI: la insignia «Hecho verificado» solo aparece si el servidor la asignó.
- Pruebas: la IA propone «hecho verificado» sin fuente → se guarda como pendiente; con contraste determinístico → hecho verificado con fuente; el check de la base rechaza `kind` = hecho sin fuente; texto leído de imagen → inferencia.

---

## B. Bloqueos críticos detectados por IA (R-02, INCORPORADA POR INSTRUCCIÓN)

Corrige a v2, que trataba un hallazgo crítico de IA igual que un bloqueo del motor. Un hallazgo de IA no corroborado NO bloquea la aprobación.

Cuatro estados de revisión (`audit_findings.review_state`, enum):

| Estado | Qué es | ¿Bloquea? | Cómo se llega |
|---|---|---|---|
| `confirmado_motor` | Bloqueo creado por regla determinística sobre datos que no provienen de la IA | Sí | Automático al validar; no se descarta: se corrige el dato o se concede una excepción |
| `propuesto_ia` | Hallazgo crítico propuesto por IA, no corroborado | No | Lo propone la IA; el servidor lo guarda como inferencia o pendiente |
| `confirmado_humano` | Hallazgo crítico de IA confirmado por una persona con `finding.confirm`, que cita la fuente | Sí; pasa a ser bloqueo con las reglas de D-07 | `review_finding(confirmar)` con motivo y fuente |
| `descartado` | Falso positivo descartado por persona con `finding.dismiss` | No | `review_finding(descartar)` con motivo obligatorio (mínimo propuesto 30 caracteres), responsable y auditoría |

Reglas:
- La pantalla de aprobación muestra de forma destacada los hallazgos `propuesto_ia`, y la aprobación guarda cuáles estaban sin revisar en ese momento (`approvals.unreviewed_ai_findings`).
- Confirmar o descartar exige permiso, motivo, responsable y fecha, y queda en el hallazgo y en `activity_logs`. El registro original nunca se borra ni se reescribe: solo cambia el estado de revisión, solo mediante la función `review_finding`.
- Se elimina el estado «resuelto» de v2 (contradecía que el hallazgo original no cambia): corregir genera una versión y una auditoría nuevas.
- Diferencias entre el texto de un arte (leído por IA) y el copy salen como `propuesto_ia` y pasan a bloqueo cuando una persona confirma la lectura.
- Descartar solo aplica a hallazgos de IA. Un bloqueo del motor no se descarta.
- Un bloqueo confirmado nunca desaparece solo (ni por puntaje, ni al re-auditar, ni con el tiempo). Si una versión corregida ya no incumple, su auditoría nueva no lo genera; el original queda en el historial de la versión anterior.
- Excepción (D-07) solo sobre bloqueos confirmados: permiso `block.exception.grant` (por persona, no por rol), justificación obligatoria, responsable identificado, auditoría; no modifica el hallazgo; vale para un hallazgo en una versión concreta y no se hereda; revocable con motivo, responsable y fecha. Veredicto: BLOQUEADO o BLOQUEADO con excepción vigente.
- Propuesta T-06: si se revoca una excepción que ya usó una aprobación, la pieza vuelve a Pendiente de aprobación; si ya estaba Publicada, solo se avisa al responsable.

Permisos: se agrega `finding.confirm` (solo Revisor / Aprobador). `finding.dismiss` se mantiene (solo Revisor / Aprobador).

Transiciones y funciones: nueva función `review_finding`; `transition_piece_status` y `record_approval` pasan a exigir «sin bloqueo confirmado sin excepción vigente» (los `propuesto_ia` no cuentan).

Pruebas: `propuesto_ia` no bloquea; confirmar o descartar sin permiso, sin motivo o sin fuente se rechaza; `confirmado_humano` bloquea y sigue D-07; descartar conserva el registro y su historial; un bloqueo del motor no se puede descartar.

---

## C. Separación de responsabilidades (R-03, INCORPORADA POR INSTRUCCIÓN)

Regla obligatoria: una persona no puede aprobar la misma versión de una pieza que creó o modificó, aunque tenga múltiples roles. Se valida en el backend y en la base de datos; la interfaz solo refleja el permiso y nunca sustituye el control del servidor. Una nueva modificación genera una nueva versión que requiere revisión y aprobación independientes.

Definiciones (PROPUESTA T-04, por validar):
- Versión de pieza = versión de copy (`copy_version_id`) + arte (`creative_asset_id`) vigentes al enviarla a aprobación.
- Contribuyen a la versión: quien creó su versión de copy (si la generó la IA, cuenta quien la pidió) y quien subió su arte.
- `created_by` y `uploaded_by` los escribe un trigger con `auth.uid()`; el cliente no los envía, por lo que no se pueden falsificar desde el navegador.
- El creador original de la pieza no queda excluido de aprobar versiones posteriores en las que no participó.

Controles:
| Capa | Control |
|---|---|
| Función `record_approval` | Rechaza con mensaje claro si quien decide contribuyó; valida además permiso, estado, bloqueos confirmados y excepciones |
| Trigger BEFORE INSERT en `approvals` | Segunda barrera: rechaza la fila si `decided_by` contribuyó, aunque se intente insertar sin pasar por la función |
| Permisos de tabla | El cliente no tiene INSERT directo en `approvals`; sin UPDATE ni DELETE para ningún rol |
| Interfaz | Desactiva «Aprobar» a quien contribuyó y explica por qué (ayuda, no control) |

Efectos:
- Nueva modificación de copy o arte → versión nueva → la pieza vuelve a corrección → exige revisión y aprobación independientes. La aprobación anterior no se hereda y queda en el historial inmutable.
- Cada organización necesita al menos dos personas (una crea, otra aprueba). El Admin no puede saltarse la regla.
- Recomendación mía, NO obligatoria (T-05): aplicar la misma independencia al confirmar/descartar hallazgos y al conceder excepciones sobre una versión en la que la persona contribuyó.
- Riesgo registrado: una organización con menos de dos personas capaces no puede aprobar nada (efecto buscado).

Corrige contradicciones de v2: la tabla de seguridad enviaba esta regla a Pendientes y los riesgos la dejaban como decisión del propietario.

Pruebas: contribuyente con cualquier combinación de los cinco roles es rechazado tanto por la función como por INSERT directo; modificación nueva exige otra aprobación independiente; aprobación previa no se hereda; autor no falsificable desde el cliente.

Transiciones de estado (PROPUESTA T-02; v2 no definía quién ejecuta cada una ni había permiso para publicar, inconsistencia corregida):
| De | A | Permiso | Condición |
|---|---|---|---|
| Borrador | En creación | copy.write o asset.upload | — |
| En creación | Pendiente de revisión | copy.write o asset.upload | Existe al menos una versión de copy |
| Pendiente de revisión | En corrección | piece.review | Comentario obligatorio |
| Pendiente de revisión | Pendiente de aprobación | piece.review | — |
| En corrección | Pendiente de revisión | copy.write o asset.upload | Hay versión nueva respecto de la revisada |
| Pendiente de aprobación | En corrección | piece.review o piece.approve | Comentario obligatorio |
| Pendiente de aprobación | Aprobado | piece.approve | Independencia; sin bloqueo confirmado sin excepción vigente; se inserta la aprobación con versión exacta |
| Pendiente de aprobación | Rechazado | piece.approve | Motivo obligatorio; misma independencia |
| Rechazado | En corrección | copy.write o asset.upload | Exige versión nueva antes de volver a revisión |
| Aprobado | Publicado | piece.publish (nueva) | La versión aprobada es la vigente |
| Aprobado | En corrección | copy.write o asset.upload | Todo cambio crea versión nueva; la aprobación anterior no se hereda |
| Aprobado | Pendiente de aprobación | Automática al revocar una excepción usada (T-06) | Si ya está Publicada, solo se avisa |
| Cualquiera menos Archivado | Archivado | piece.archive | Motivo; no se borra |

Matriz de permisos resultante (17 claves; PROPUESTA T-01; `finding.confirm` y `piece.publish` son nuevas):
content.read, comment.write, audit.run (todos los roles); campaign.write, copy.write, channel.adapt, metrics.write (Admin, Ecommerce, Marketing; promotion.write: Admin, Ecommerce); asset.upload (Admin, Diseño, Marketing); piece.review, piece.approve, finding.confirm, finding.dismiss (solo Revisor / Aprobador); piece.publish (Admin, Ecommerce, Marketing); piece.archive (Admin, Revisor); org.manage (solo Admin); block.exception.grant (ningún rol: concesión por persona por alguien con org.manage). Admin no aprueba por defecto.

---

## D. Auditoría final del modelo de datos (R-04, INCORPORADA POR INSTRUCCIÓN)

Revisión del diseño de las 27 tablas (no se ejecutó SQL). Resultado: no se agrega ninguna tabla; se corrigen columnas y reglas.

| Criterio | Hallazgo | Ajuste |
|---|---|---|
| Relaciones y FK | Un hijo podía apuntar a un padre de otra organización aunque RLS filtre lecturas | Cada padre con unique(organization_id, id) y FK compuesta con organization_id en los hijos (T-09) |
| Integridad de versiones | «Versión de pieza» no estaba definida; approvals y excepciones no la fijaban | Versión = copy_version_id + creative_asset_id; `creative_pieces` guarda la vigente; audits, audit_findings, approvals y excepciones guardan la exacta |
| Historial de auditorías | audits es solo inserción; el estado «resuelto» contradecía eso | Se elimina «resuelto»; corregir = versión y auditoría nuevas; review_state solo vía `review_finding`, con registro en activity_logs |
| Campañas, briefs, piezas, artes | Cadena implícita | campaigns 1→N briefs y piezas; la pieza guarda campaña y brief de origen opcional; copy_versions guarda brief y versión de brief usados; creative_assets pertenece a una pieza y a una versión de copy |
| Promociones, SKU, precios, descuentos, vigencias | Con una fila por promoción no se podía evaluar «hasta N %» entre varios SKU | `promotion_rules`: una fila por promoción y SKU, agrupadas por `promotion_code`, con campaña, moneda, base de impuestos y check de fechas (T-07). La relación de una promoción con varias campañas se trata en la sección 5 de este documento (T-11, propuesta no aprobada); no se agrega ninguna tabla |
| Excepciones ligadas al hallazgo y versión exactos | v2 decía «versión afectada» sin forzarla | FK compuesta (finding_id, piece_id, copy_version_id, creative_asset_id) a audit_findings, solo si review_state es confirmado_motor o confirmado_humano; trigger impide usarla en otra versión |
| Aprobaciones inmutables | Correcto con salvedad: `exception_ids` y `unreviewed_ai_findings` son arreglos sin FK | Trigger los valida al insertar; como aprobaciones y excepciones no se borran, no hay referencias rotas; sin UPDATE ni DELETE para ningún rol |
| Aislamiento por organización (RLS) | Correcto en diseño; sin probar | Prueba por tabla (27 de 27); FK compuestas; funciones security definer con search_path vacío; Storage por prefijo de organización |
| Integridad de archivos en Storage | Nada comparaba el objeto con su fila | SHA-256, bytes y MIME verificados por magic bytes al registrar; objeto inmutable (imagen nueva = fila y ruta nuevas); `verify_assets_integrity` compara filas, objetos y hashes y reporta huérfanos |
| Exportación y recuperación | Exportar archivos desde una Edge Function choca con los 2 s de CPU | Exportación en dos partes: JSON por tabla en orden de dependencias + manifiesto de archivos (ruta, tamaño, hash) con URLs firmadas que descarga el navegador; la importación crea registros nuevos marcados como importados y verifica el hash. No probado |

Columnas agregadas o cambiadas:
- `creative_pieces`: creador, campaña, brief de origen opcional, versión vigente (copy_version_id y creative_asset_id).
- `creative_assets`: pieza, quien subió, versión de copy a la que acompaña.
- `copy_versions`: `created_by` (también si el origen es IA), brief y versión de brief usados.
- `audits`: versión exacta auditada, cobertura; FK compuesta a la versión.
- `audit_findings`: `kind_proposed`, `kind`, `verification_source`, `source_ref`, `review_state`, responsable, fecha y motivo de revisión.
- `commercial_block_exceptions`: versión exacta y FK compuesta al hallazgo.
- `approvals`: versión exacta, auditoría considerada, `exception_ids`, `unreviewed_ai_findings`.
- `promotion_rules`: `promotion_code`, campaña. `briefs`: `promotion_code` opcional.

Duplicidades revisadas y justificación de las 7 tablas de apoyo:
- audit_rubric_versions: pesos, rangos y cobertura versionados, con check de suma 100. Fusionarla con validation_settings_versions ahorraría una tabla pero perdería ese check tipado; se mantienen separadas.
- validation_settings_versions: tolerancia y precisión de precios versionadas; cada auditoría guarda la versión usada.
- channel_rules: reglas de canal que exige el módulo 05; sin duplicado.
- ai_quotas: topes; ai_runs guarda el consumo; son cosas distintas.
- role_permissions: catálogo global de permisos por rol; sin ella los roles quedarían en código.
- membership_permission_grants: permisos por persona; role_permissions es por rol.
- commercial_block_exceptions: es un hecho aparte del hallazgo y es revocable; guardarla en audit_findings obligaría a reescribirlo.
- brand_guidelines (del prompt): cabecera casi redundante con brand_guideline_versions; se conserva y se decide en Fase 1 (T-10).

Matriz de las 27 tablas (tabla — propósito — relaciones principales — controles — fase propuesta):
1. organizations — raíz del aislamiento — padre de todas — RLS solo miembros; escribe org.manage — 1
2. profiles — datos de la persona — 1:1 auth.users — cada persona ve su perfil y el de miembros de sus organizaciones — 1
3. memberships — persona en organización con roles — organizations, profiles — RLS is_member; org.manage; roles no vacío — 1
4. role_permissions — permisos por rol (global) — usada por has_permission — lectura autenticada; solo migración — 1
5. membership_permission_grants — permisos por persona — memberships — solo org.manage concede; revocación con responsable; auditoría — 1
6. activity_logs — auditoría general — referencia genérica — escrita por triggers/funciones; sin UPDATE/DELETE — 1
7. campaigns — agrupa el trabajo — padre de briefs, piezas, promociones — RLS; campaign.write — 1
8. creative_pieces — pieza, estado, versión vigente — campaigns, briefs, copy_versions, creative_assets — estado solo vía transition_piece_status — 1 (estructura) y 6 (flujo)
9. brand_guidelines — cabecera de guía vigente — brand_guideline_versions — RLS; org.manage — 2
10. brand_guideline_versions — guía versionada — brand_guidelines — inmutable — 2
11. briefs — brief de 16 campos — campaigns — RLS; campaign.write; control de versión — 2
12. copy_versions — texto versionado — creative_pieces, briefs — inmutable; autor por trigger — 2
13. ai_runs — registro de llamadas a IA — organizations, profiles — escrito por funciones; sin secretos ni imágenes completas — 2
14. ai_prompt_versions — prompts versionados — organizations — inmutable; org.manage — 2
15. ai_quotas — topes de IA — organizations — org.manage; consume_ai_quota atómico — 2
16. creative_assets — arte subido — creative_pieces, copy_versions — asset.upload; hash y MIME verificados; objeto inmutable — 3
17. audit_rubric_versions — rúbrica versionada — organizations; la usa audits — inmutable; suma de pesos 100 — 3
18. audits — resultado de auditoría — copy_versions, creative_assets, ai_runs, rúbrica, ajustes — solo inserción; audit.run — 3
19. audit_findings — hallazgos y su revisión — audits — contenido inmutable; review_state solo vía review_finding — 3
20. promotion_rules — reglas de promoción por SKU — campaigns — promotion.write; checks de precios y fechas — 4
21. validation_settings_versions — tolerancia y precisión — organizations; las usa audits — inmutable; org.manage — 4
22. channel_rules — reglas por canal — organizations — RLS; org.manage — 5
23. comments — comentarios y solicitudes de cambio — creative_pieces, audit_findings (opcional) — comment.write; padre de la misma organización — 6
24. commercial_block_exceptions — excepciones a bloqueos confirmados — audit_findings (FK compuesta), memberships — solo inserción; block.exception.grant — 6
25. approvals — decisión humana sobre una versión — copy_versions, creative_assets, audits, personas — sin UPDATE/DELETE; trigger de independencia; piece.approve — 6
26. performance_metrics — métricas por pieza y variante — creative_pieces — metrics.write; unique por periodo — 8
27. ab_tests — pruebas A/B — creative_pieces, performance_metrics — metrics.write — 8
(Las columnas que apuntan a tablas de fases posteriores se agregan en la migración de la fase que crea la tabla destino.)

Pruebas: FK compuestas impiden referencias entre organizaciones y versiones; una excepción no se puede usar en otra versión; ningún rol actualiza ni borra aprobaciones; matriz de aislamiento RLS cubre las 27 tablas; hash/MIME coinciden con la fila; `verify_assets_integrity` detecta huérfanos; una ruta de otra organización se deniega; exportar y reimportar conserva hashes y marca registros como importados.

---

## E. Scoring (R-05, INCORPORADA POR INSTRUCCIÓN)

Se conservan los pesos (Claridad 15, Titular 15, Beneficio y persuasión 15, Propuesta comercial 15, CTA 10, UX y legibilidad 10, Coherencia de marca 10, Precisión comercial 10; suma 100) y la cobertura mínima de 60 % medida por peso evaluable. El parámetro vive en `audit_rubric_versions.min_coverage_pct` (60 por defecto). La cobertura por peso pasó de «pendiente de confirmación» a confirmada.

1. Cobertura: C = 100 × (suma de pesos de dimensiones evaluables) ÷ (suma de pesos de todas las dimensiones de la versión de rúbrica). Evaluable = nota válida 0–10. N/A = falta el dato que la sustenta (sin imagen, sin datos de promoción) o la IA no devolvió nota válida tras el reintento. N/A nunca vale 0.
2. Umbral: se cumple si C ≥ min_coverage_pct; el límite exacto cumple. Pesos enteros; no se redondea al comparar.
3. Normalización: Puntaje = 100 × Σ(peso × nota ÷ 10) ÷ Σ(pesos evaluables). N/A no suma ni resta. Notas enteras 0–10 (propuesta T-08). Se redondea a un decimal, mitad hacia arriba, y con ese valor se asigna el rango.
4. Por debajo del mínimo: veredicto «Evaluación incompleta»; sin rango; el puntaje no se presenta como resultado; se listan dimensiones evaluadas y faltantes. Si ninguna es evaluable no se divide: sin puntaje.
5. Rangos: ≥90 Excelente; 80 a <90 Bueno, ajustes menores; 70 a <80 Requiere correcciones; <70 Replanteamiento. Límite inferior incluido, superior excluido, sobre el puntaje redondeado (corrige el prompt, que dejaba sin cubrir valores como 89.5). Se muestran junto con la cobertura, p. ej. «75.7 · Requiere correcciones · cobertura 70 %».
6. El puntaje no sustituye la aprobación humana: no cambia estados, no aprueba ni rechaza; solo informa. Aprobar exige decisión humana trazable (D-08) aunque el puntaje sea 100 y la cobertura completa. Cumplir la cobertura mínima tampoco equivale a aprobar.
7. Un bloqueo confirmado (del motor o por revisión humana) prevalece: el veredicto visible es BLOQUEADO o BLOQUEADO con excepción vigente; el puntaje queda como dato informativo; la función de aprobación rechaza la acción sea cual sea puntaje o cobertura. Un hallazgo de IA sin confirmar no cambia ni veredicto ni puntaje.

Ejemplo calculado (verificado con cálculo aparte, no con un motor): Claridad 8, Titular 7, Beneficio 9, Propuesta 6, CTA 8; UX, Coherencia y Precisión N/A. Cobertura 70 %. Puntaje = 100 × (12 + 10.5 + 13.5 + 9 + 8) ÷ 70 = 75.7 → Requiere correcciones.

Casos límite (pruebas obligatorias; notas en 10 salvo indicación):
| Caso | Peso N/A | Cobertura | Resultado esperado |
|---|---|---|---|
| Todas evaluables | 0 | 100 % | Puntaje y rango |
| N/A UX y Precisión comercial | 20 | 80 % | Puntaje y rango |
| N/A CTA, UX, Coherencia y Precisión | 40 | 60 % exacto | Cumple; puntaje y rango |
| N/A Titular, UX, Coherencia y Precisión | 45 | 55 % | Evaluación incompleta, sin rango |
| Todas N/A | 100 | 0 % | Evaluación incompleta, sin puntaje, sin dividir por cero |
| Puntaje 89.9 y 90.0 | — | — | Bueno y Excelente |
| Puntaje 79.9 y 80.0 | — | — | Requiere correcciones y Bueno |
| Puntaje 69.9 y 70.0 | — | — | Replanteamiento y Requiere correcciones |
| Puntaje 89.95, 79.95, 69.95 | — | — | Se muestran 90.0, 80.0, 70.0 y toman el rango superior (prueba de la función de redondeo) |
| Puntaje 100 con bloqueo confirmado | — | cualquiera | BLOQUEADO; aprobación rechazada |
| Puntaje 100 sin bloqueo | — | 100 % | El estado no cambia solo; falta la decisión humana |

---

## Otras contradicciones corregidas (consecuencia de la auditoría de consistencia)
- Resumen y Registro decían que un hallazgo crítico de IA bloquea igual que uno del motor → corregido (B).
- Prompts obligaban a etiquetar «hecho verificado» → corregido (A).
- Autoaprobación en Pendientes/riesgos → ahora obligatoria (C).
- Transiciones sin permiso y sin permiso de publicar → tabla de transiciones.
- «Versión concreta» sin columnas en approvals/excepciones → corregido (D).
- Estado «resuelto» en hallazgos → eliminado (B, D).
- Cobertura por peso como pendiente → confirmada (E).
- promotion_rules sin agrupación de SKU → `promotion_code` (D).
- Exportación sin considerar 2 s de CPU de Edge Functions → JSON + manifiesto (D).

## Propuestas técnicas T-01..T-10, NO aprobadas (A-01 no las aprueba; la sección 7 añade T-11 y T-12)
T-01 matriz de 17 permisos; T-02 transiciones; T-03 motivo de mínimo 30 caracteres en excepciones y descartes; T-04 definición de contribuyentes; T-05 independencia al confirmar/descartar/conceder excepciones (recomendación); T-06 revocar excepción devuelve la pieza a Pendiente de aprobación; T-07 promotion_rules por promoción y SKU con promotion_code; T-08 notas enteras y rangos con límite inferior incluido; T-09 FK compuestas y exportación en dos partes; T-10 conservar brand_guidelines y revisarla en Fase 1.

## Pendientes del propietario
P-01 organización y proyecto de Supabase; P-02 repositorio de GitHub y visibilidad; P-03 clave de prueba de Cohere; P-04 personas y roles (al menos dos que puedan aprobar); P-05 permisos individuales para conceder excepciones; P-06 moneda e impuestos; P-07 límite de imágenes (propuesta: 10 MB por archivo); P-08 tope de tolerancia (propuesta: 5 puntos porcentuales); P-09 retención de datos y respaldos; P-10 dominio y hosting definitivos; A-01 aceptación formal de la Fase 0 v3.

## Lo que no está verificado
Todo es diseño en papel: no corrió ningún SQL, no hubo llamadas a Cohere, las cifras de puntaje se calcularon aparte (no con un motor), y no se verificaron Docker, Playwright, Deno, la CLI de Supabase ni la exportación de archivos.

---
# Anexo C — Cuerpo técnico del maestro rev 68 (copia textual)

Copia sin cambios del contenido de Google Docs rev 68, exportada el 2026-11-15. Es el desarrollo de: resumen, dictamen técnico, registro de cambios frente a v2, registro de decisiones, línea base del entorno, arquitectura objetivo, estructura del proyecto, diseño de módulos y transiciones, modelo de datos y su auditoría, seguridad y RLS con la matriz de permisos por rol, separación de funciones, estrategia de IA, motores determinísticos (puntaje, bloqueos, promociones, precios, métricas), sistema visual y UX, plan de pruebas, riesgos y dependencias, configuraciones, pasos de Supabase, roadmap, criterios de entrada, limitaciones y pendientes.

## Fe de erratas del Anexo C (frases superadas por las secciones 1–13)

| ID | Dónde en el Anexo C | Texto superado | Vigente |
|---|---|---|---|
| E-1 | Registro de cambios, C-09; Roadmap consolidado, fila 0.8 | 0.8 como subfase de la Fase 0, marcada como actual | Roadmap oficial 0.1–0.7; 0.8 no es oficial (T-12 no aprobada) |
| E-2 | Matriz de decisiones (párrafo inicial) y Pendientes (A-01) | R-01..R-05 «se aceptan con la Fase 0»; A-01 «incluye las propuestas técnicas T-01 a T-10» | A-01 = 13.1; las T no se aprueban con A-01 |
| E-3 | Informe de limitaciones L-11; Modelo de datos (promotion_rules) | «¿tabla de unión?» para promociones de varias campañas | Sección 5: Campaña → Brief → `promotion_code` (T-11, no aprobada); caso C-1 abierto |
| E-4 | Roadmap consolidado, filas de las fases 3, 6 y 9 | Listas de alcance con más elementos que subfases numeradas | Numeración original; mapeo propuesto en la sección 8 |
| E-5 | Matriz de decisiones | Llega solo a T-10 | T-01..T-12 en la sección 7 |
| E-6 | Dictamen técnico | «COMPLETADA CON LIMITACIONES DOCUMENTADAS» | Dictamen técnico del autor; no es aceptación |

---


Nov 15, 2026 · @Alejandro Escobar

## Resumen ejecutivo

Esta es la versión 3 de la Fase 0: conserva las decisiones D-01 a D-08, incorpora tu revisión final de consistencia y queda a la espera de tu aceptación formal; la Fase 1 no empieza hasta que la autorices de forma expresa.

- **Cambios de fondo:** cinco roles con permisos por clave aplicados en la base de datos y en la interfaz, excepciones a bloqueos comerciales con responsable, justificación y auditoría, y tolerancia y cobertura configurables y versionadas. El esquema tiene 27 tablas y la v3 no agrega ninguna. La v3 añade la clasificación de afirmaciones de IA, la distinción entre bloqueo confirmado y hallazgo de IA sin corroborar, la separación obligatoria entre quien crea y quien aprueba, la auditoría del modelo de datos y las reglas de cobertura del puntaje.
- **Independencia:** repositorio, organización y proyecto de Supabase propios, sin nada compartido con RevNavigator.
- **Cohere:** solo desarrollo y pruebas con clave de prueba, que Cohere no permite usar en producción ni con fines comerciales. Su página de precios no publica tarifas de los modelos vigentes, así que todavía no hay un costo estimado confiable.
- **Alcance real:** no se creó infraestructura, no se pidió ni se usó ninguna credencial y no se escribió código. Solo se consultó documentación y se listó Supabase en modo lectura.
- **Antes de la Fase 1:** crear la organización y el proyecto de Supabase (pasos en el documento), un repositorio nuevo y la clave de prueba de Cohere, y resolver los puntos de la sección Pendientes.

## Dictamen técnico de la Fase 0

**Dictamen:** la Fase 0 cumple el criterio de cierre y puede declararse técnicamente **COMPLETADA CON LIMITACIONES DOCUMENTADAS** (en el roadmap, el estado COMPLETADA CON LIMITACIONES). No está ACEPTADA POR EL USUARIO y este documento no autoriza la Fase 1.

| Criterio de cierre | Resultado | Sustento |
| --- | --- | --- |
| La arquitectura es coherente | Cumple | Revisé las 13 áreas que pediste y corregí las contradicciones que encontré (sección siguiente) |
| Las decisiones aprobadas están incorporadas | Cumple | D-01 a D-08 en el registro, con su efecto en datos, RLS, permisos, pruebas y roadmap |
| Las contradicciones están resueltas | Cumple con una salvedad | La coherencia la comprobé leyendo el documento y con cálculos de apoyo; no hay SQL ni código que la pruebe |
| Las propuestas están diferenciadas de las decisiones | Cumple | La matriz de decisiones separa APROBADA, INCORPORADA POR INSTRUCCIÓN, PROPUESTA TÉCNICA y PENDIENTE DEL PROPIETARIO |
| Las limitaciones están documentadas | Cumple | Informe de limitaciones no resueltas |
| Las dependencias externas están identificadas | Cumple | Riesgos y dependencias, Configuraciones y Pasos de Supabase |
| La Fase 1 tiene criterios claros de entrada | Cumple | Sección Criterios de entrada de la Fase 1 |

Lo que este dictamen no afirma: que el diseño funcione. El esquema, las políticas RLS, las funciones y los triggers son diseño en papel; ninguna prueba se ejecutó y Cohere no recibió una sola llamada. Esa evidencia se produce desde la Fase 1.

## Registro de cambios frente a v2

| ID | Qué cambió | Dónde | Origen |
| --- | --- | --- | --- |
| C-01 | Nueva regla: la IA nunca se certifica como fuente de un hecho verificado; propone la clase y el servidor la asigna tras contrastar | Arquitectura, Estrategia de IA, Modelo de datos, Plan de pruebas | Revisión final, punto A |
| C-02 | Cuatro estados de revisión de hallazgos; un hallazgo crítico de IA no corroborado ya no bloquea (v2 lo trataba igual que un bloqueo del motor) | Bloqueos comerciales, Modelo de datos, Seguridad, Pruebas | Revisión final, punto B |
| C-03 | Separación de funciones obligatoria, validada en la función y en un trigger de la base | Seguridad y RLS, Modelo de datos, Pruebas | Revisión final, punto C |
| C-04 | Auditoría de las 27 tablas: sin tablas nuevas; columnas de versión exacta, claves foráneas compuestas y matriz de tablas | Modelo de datos | Revisión final, punto D |
| C-05 | Reglas de cobertura, normalización, N/A, rangos y casos límite; cobertura por peso confirmada | Motores determinísticos | Revisión final, punto E |
| C-06 | Matriz de permisos con 17 claves: se añaden finding.confirm y piece.publish (propuestas mías) | Seguridad y RLS | Consecuencia de B y del flujo |
| C-07 | Tabla de transiciones de estado con el permiso de cada una | Diseño de módulos | Inconsistencia hallada |
| C-08 | Riesgos, configuraciones y pendientes reordenados según tu lista de 10 puntos operativos | Riesgos, Configuraciones, Pendientes | Revisión final, punto 4 |
| C-09 | Subfase 0.8, notas por fase en el roadmap y criterios de entrada de la Fase 1 | Roadmap | Revisión final, punto 7 |
| C-10 | Diagrama de arquitectura con el papel de la IA y de la base actualizado | Arquitectura objetivo | Entregable 6 |

Contradicciones encontradas y corregidas:

1. El Resumen y el Registro decían que un hallazgo crítico de IA impide aprobar igual que uno del motor; contradice el punto B. Corregido.
2. Los prompts obligaban a la IA a etiquetar cada afirmación como «hecho verificado»; contradice el punto A. Ahora la IA propone y el servidor asigna.
3. La tabla de seguridad enviaba la regla de separación entre quien crea y quien aprueba a Pendientes, y los riesgos la dejaban como decisión tuya; ahora es obligatoria.
4. Las transiciones de estado no decían quién las ejecuta ni con qué permiso, y no había permiso para publicar. Corregido con la tabla de transiciones.
5. `approvals` y `commercial_block_exceptions` hablaban de una «versión concreta» sin columnas que la fijaran, y «versión de pieza» no estaba definida. Corregido.
6. `audit_findings` tenía un estado «resuelto» que choca con que el hallazgo original nunca cambia; se sustituye por los cuatro estados de revisión.
7. La cobertura por peso figuraba como pendiente de tu confirmación; tu revisión final la confirma.
8. La pregunta de si alguien con varios roles aprueba su trabajo figuraba como pendiente; el punto C la resuelve.
9. `promotion_rules` no podía agrupar los SKU de una misma promoción, lo que impide evaluar «hasta N %». Corregido con `promotion_code`.
10. La exportación hablaba de «registros y archivos» sin considerar el límite de 2 s de CPU de las Edge Functions; ahora se divide en JSON y manifiesto de archivos.

## Registro de decisiones

El registro nace en esta versión con tus ocho decisiones del 15 de noviembre de 2026. Las propuestas que aún no has resuelto siguen en la sección Pendientes.

| ID | Decisión | Estado | Efecto en el diseño |
| --- | --- | --- | --- |
| D-01 | Independencia total de RevNavigator: ni vista previa privada, ni repositorio, frontend, backend, base de datos o infraestructura compartidos | APROBADA | Repositorio, organización y proyecto de Supabase propios; ningún recurso compartido |
| D-02 | Organización nueva de Supabase y, dentro de ella, un proyecto exclusivo | APROBADA; la creación espera tu autorización expresa | Pasos y requisitos en la sección Crear la organización y el proyecto de Supabase |
| D-03 | Cohere solo en desarrollo y pruebas, sin plan de producción; arquitectura desacoplada del proveedor | APROBADA | Clave de prueba; protocolo de verificación; interfaz `ai-client` intacta |
| D-04 | Cinco roles (Admin, Ecommerce, Diseño, Marketing, Revisor / Aprobador), con más de un rol por persona; permisos en frontend y backend | APROBADA | `memberships.roles` es un arreglo; permisos por clave en `role_permissions`; RLS por permiso |
| D-05 | Cobertura mínima de 60 % de las dimensiones evaluables; no equivale a aprobación; un hallazgo comercial crítico impide aprobar aunque el puntaje sea alto | APROBADA PROVISIONALMENTE | Parámetro `min_coverage_pct` en la versión de rúbrica; medido por peso evaluable (aclarado en la revisión final) |
| D-06 | Tolerancia de descuento de 0.5 puntos porcentuales, configurable en Ajustes; documentar redondeo y manejo de precios | APROBADA como valor inicial | Tabla `validation_settings_versions`; reglas en la sección Motores determinísticos |
| D-07 | Los bloqueos críticos no se eliminan solos; una excepción exige permiso específico, justificación obligatoria, responsable identificado y registro de auditoría, y no borra el hallazgo | APROBADA | Tabla `commercial_block_exceptions`; permiso `block.exception.grant`; aplica a bloqueos confirmados, del motor o por revisión humana (aclarado en v3) |
| D-08 | Todas las aprobaciones son humanas y trazables | APROBADA | `approvals` solo de inserción; `decided_by` es una persona con el permiso `piece.approve` que no creó ni modificó esa versión (aclarado en v3) |

Qué cambió en el diseño por estas decisiones:

| Área | Cambio |
| --- | --- |
| Modelo de datos | De 23 a 27 tablas: se agregan `role_permissions`, `membership_permission_grants`, `commercial_block_exceptions` y `validation_settings_versions`; `memberships.roles` pasa a arreglo; `audit_findings`, `audits` y `approvals` ganan columnas |
| RLS | Las políticas verifican permisos con `has_permission(org, permiso)` y no nombres de rol |
| Arquitectura | Las capas no cambian; se agregan las funciones de base de datos `my_permissions`, `grant_block_exception` y `revoke_block_exception`, y la independencia de RevNavigator queda como principio |
| Seguridad | Matriz de permisos, doble aplicación (base de datos e interfaz), auditoría de excepciones |
| Roadmap | Fase 1 crea roles y permisos; Fase 2 usa clave de prueba; Fase 4 calcula bloqueos; Fase 6 incorpora excepciones y aprobación con excepción |
| Pruebas | Una prueba por permiso y por rol; pruebas del ciclo completo de excepciones |

Inconsistencias de la versión 1 que se corrigieron:

- Los seis roles propuestos se sustituyen por los cinco que aprobaste.
- Desaparece la exigencia de una clave de Cohere de producción antes de la Fase 2.
- «Bloqueo levantable con justificación firmada o corrigiendo datos» queda como dos caminos regulados: corregir y revalidar, o una excepción con permiso específico; nunca algo automático.
- La cobertura mínima se aclara como porcentaje del peso evaluable y no del número de dimensiones; tu revisión final lo confirmó.
- Un hallazgo crítico de la IA pasó de solo pedir revisión (v1) a bloquear igual que uno del motor (v2). La revisión final de v3 lo corrige: no bloquea hasta que una persona lo confirme.
- El diagrama de arquitectura mostraba 20 tablas y 3 de apoyo; ahora 27.
- Admin ya no aprueba por defecto: aprobar es del rol Revisor / Aprobador, aunque un Admin puede recibir ese rol de forma trazable.

### Matriz de decisiones aprobadas y pendientes

Cuatro estados distintos: APROBADA es una decisión tuya; INCORPORADA POR INSTRUCCIÓN viene de tu revisión final y se acepta con la Fase 0; PROPUESTA TÉCNICA es mía y no está aprobada; PENDIENTE DEL PROPIETARIO espera tu decisión o tu acción.

| ID | Elemento | Estado |
| --- | --- | --- |
| D-01 | Independencia total de RevNavigator | APROBADA |
| D-02 | Organización y proyecto de Supabase exclusivos | APROBADA; creación pendiente (P-01) |
| D-03 | Cohere solo en desarrollo y pruebas; proveedor desacoplado | APROBADA |
| D-04 | Cinco roles, varios por persona, permisos por clave en backend y frontend | APROBADA |
| D-05 | Cobertura mínima de 60 %; el puntaje no aprueba; un bloqueo comercial confirmado impide aprobar | APROBADA PROVISIONALMENTE |
| D-06 | Tolerancia inicial de 0.5 puntos porcentuales, configurable en Ajustes | APROBADA como valor inicial |
| D-07 | Excepciones con permiso específico, justificación, responsable y auditoría | APROBADA |
| D-08 | Aprobaciones humanas y trazables | APROBADA |
| R-01 | La IA nunca se certifica como fuente de hechos verificados | INCORPORADA POR INSTRUCCIÓN |
| R-02 | Cuatro estados de hallazgo; la IA no corroborada no bloquea | INCORPORADA POR INSTRUCCIÓN |
| R-03 | Quien crea o modifica una versión no puede aprobarla | INCORPORADA POR INSTRUCCIÓN |
| R-04 | Auditoría de las 27 tablas sin agregar tablas por comodidad | INCORPORADA POR INSTRUCCIÓN |
| R-05 | Pesos conservados y cobertura de 60 % medida por peso evaluable | INCORPORADA POR INSTRUCCIÓN |
| T-01 | Matriz de 17 permisos, con finding.confirm y piece.publish nuevos | PROPUESTA TÉCNICA |
| T-02 | Tabla de transiciones de estado | PROPUESTA TÉCNICA |
| T-03 | Motivo escrito de al menos 30 caracteres en excepciones y descartes | PROPUESTA TÉCNICA |
| T-04 | Contribuyentes de una versión: autor del copy y quien subió el arte; el creador original de la pieza no queda excluido de versiones posteriores en las que no participó | PROPUESTA TÉCNICA |
| T-05 | Aplicar la misma independencia al confirmar, descartar y conceder excepciones | PROPUESTA TÉCNICA (recomendación) |
| T-06 | Revocar una excepción usada por una aprobación devuelve la pieza a Pendiente de aprobación | PROPUESTA TÉCNICA |
| T-07 | `promotion_rules` con una fila por promoción y SKU, agrupadas por `promotion_code` | PROPUESTA TÉCNICA |
| T-08 | Notas enteras de 0 a 10; rangos con límite inferior incluido sobre el puntaje redondeado | PROPUESTA TÉCNICA |
| T-09 | Claves foráneas compuestas y exportación en dos partes (JSON y manifiesto de archivos) | PROPUESTA TÉCNICA |
| T-10 | Conservar `brand_guidelines` como cabecera y revisarla en la Fase 1 | PROPUESTA TÉCNICA |
| P-01 | Organización y proyecto de Supabase | PENDIENTE DEL PROPIETARIO |
| P-02 | Repositorio de GitHub y su visibilidad | PENDIENTE DEL PROPIETARIO |
| P-03 | Clave de prueba de Cohere | PENDIENTE DEL PROPIETARIO |
| P-04 | Personas y asignación de roles | PENDIENTE DEL PROPIETARIO |
| P-05 | Permisos individuales para conceder excepciones | PENDIENTE DEL PROPIETARIO |
| P-06 | Moneda y tratamiento de impuestos | PENDIENTE DEL PROPIETARIO |
| P-07 | Límite máximo de imágenes | PENDIENTE DEL PROPIETARIO |
| P-08 | Tope de la tolerancia configurable | PENDIENTE DEL PROPIETARIO |
| P-09 | Retención de datos y respaldos | PENDIENTE DEL PROPIETARIO |
| P-10 | Dominio y hosting definitivo | PENDIENTE DEL PROPIETARIO |
| A-01 | Aceptación formal de la Fase 0 v3 | PENDIENTE DEL PROPIETARIO |

## Línea base del entorno

El entorno está vacío y no existe un backend dedicado para esta app: la única organización de Supabase conectada es la de RevNavigator, y el prompt prohíbe reutilizar su infraestructura. La estructura se crea desde cero.

| Elemento | Estado | Evidencia |
| --- | --- | --- |
| Directorio de trabajo | Vacío, sin código previo | Solo archivos de configuración del usuario del sistema |
| Repositorio Git | No existe | `git rev-parse` responde que no es un repositorio |
| Runtimes | Node 22.23.4, npm 10.9.9, Python 3.13, psql 16.15, gh 2.89 | Versiones leídas en el shell |
| Deno y Supabase CLI | No instalados | Necesarios para probar Edge Functions y migraciones en local |
| Conector de Supabase | Conectado, solo lectura verificada | Listado de organizaciones y proyectos respondió |
| Organización de Supabase | Una sola: RevNavigator | Dos proyectos: «pruebas» (INACTIVE, creado 2026-10-01) y «Revnavigator» (ACTIVE\_HEALTHY, creado 2026-10-04), ambos en us-west-2, Postgres 17 |
| Proyecto Supabase para esta app | No existe | Ninguno de los dos proyectos se tocó |
| Cohere | No verificado | No hay clave de Cohere en el entorno; no se hizo ninguna llamada |
| Red del entorno | Salida por proxy con lista de permitidos | Estado del proxy leído; los sitios fuera de la lista pueden fallar |

No se creó, modificó ni consultó el contenido de ningún proyecto de Supabase: solo se listaron. No sé qué plan tiene la organización de RevNavigator, y importa: el plan gratuito permite dos proyectos activos entre todas las organizaciones donde eres propietario o administrador. «pruebas» está inactivo y no cuenta; «Revnavigator» sí. Los detalles están en la sección Crear la organización y el proyecto de Supabase.

## Arquitectura objetivo

La app es estática, los datos y los permisos viven en Supabase y la IA solo se alcanza a través de Edge Functions.

&#91;embedded content: arquitectura objetivo · navegador, Supabase y Cohere\]

Cada flecha es una solicitud con la sesión del usuario. La de IA pasa por AI Service, que valida el JWT, aplica cuotas, registra la ejecución en `ai_runs` y es el único que llama a Cohere; también lee Storage mediante URLs firmadas.

Principios que no cambian entre fases:

- **Independencia total (D-01):** esta app no comparte con RevNavigator repositorio, vista previa, frontend, backend, base de datos, claves ni organización de Supabase. Ningún código se copia ni se importa de allá.
- **PostgreSQL es la fuente de verdad.** IndexedDB es opcional y solo como caché de lectura; no guarda aprobaciones ni nada que deba ser consistente. Propongo dejarlo fuera hasta la Fase 7.
- **Permisos en dos capas (D-04):** la base de datos decide con RLS y funciones; la interfaz lee `my_permissions` solo para ocultar o desactivar lo que no se puede hacer. Ocultar un botón nunca es el control. La separación entre quien crea o modifica una versión y quien la aprueba también la impone la base de datos.
- **Respaldos propios:** exportación de la organización a JSON desde una función que respeta RLS, e importación que valida el esquema y crea registros nuevos marcados como importados, sin sobrescribir los existentes.
- **Cada número lo calcula JavaScript;** la IA solo propone y explica, y nunca se certifica a sí misma: un hecho es verificado solo si se contrasta contra una fuente identificable o una regla determinística (sección Clasificación de afirmaciones).
- **Proveedor de IA intercambiable (D-03):** los módulos conocen `ai-client`, no a Cohere; el modelo y el proveedor se configuran sin tocar los módulos.
- **Implementado, simulado y pendiente** son tres estados distintos y visibles en el roadmap; un mock nunca se presenta como integración real.

## Estructura del proyecto

Un solo repositorio con tres zonas separadas: la app estática (`app/`), el backend de Supabase (`supabase/`) y las pruebas (`tests/`). La lógica de negocio vive en motores puros sin DOM, para poder probarla sin navegador.

```text
copy-creative-intelligence/
├─ index.html                  # único HTML; carga app/main.js como módulo
├─ app/
│  ├─ main.js                  # arranque: sesión, router, layout
│  ├─ core/                    # router (hash), store, eventos, config, errores
│  ├─ services/                # supabase-client, auth, ai-client, storage
│  ├─ engines/                 # funciones puras: scoring, promotions, metrics, channels
│  ├─ modules/                 # un directorio por módulo 01–09
│  │  ├─ command-center/
│  │  ├─ copy-studio/
│  │  ├─ creative-auditor/
│  │  ├─ promotion-validator/
│  │  ├─ channel-adaptation/
│  │  ├─ workflow/
│  │  ├─ library/
│  │  ├─ performance/
│  │  └─ settings/
│  ├─ ui/                      # componentes compartidos: tabla, modal, filtros, comparador, toast
│  ├─ styles/                  # tokens.css, base.css, components.css
│  └─ vendor/                  # supabase-js fijado en una versión, copiado al repo
├─ supabase/
│  ├─ migrations/              # SQL versionado: 0001_*.sql, 0002_*.sql…
│  ├─ functions/
│  │  ├─ _shared/              # cors, auth, validación, límites, cliente Cohere
│  │  ├─ ai-generate/  ai-audit/  ai-adapt/  ai-compare/
│  │  └─ ...
│  ├─ seed/                    # datos de demostración, marcados como DEMO
│  └─ config.toml
├─ tests/                      # unit/, integration/, rls/, e2e/
├─ docs/                       # arquitectura, roadmap, runbook, informe por fase
└─ package.json                # solo herramientas de desarrollo; ninguna dependencia de runtime
```

Convenciones que se fijan desde Fase 1:

- **Contrato de módulo:** cada módulo exporta `mount(container, ctx)` y `unmount()`; el router solo conoce ese contrato.
- **Router por hash** (`#/copy-studio`), porque GitHub Pages no reescribe rutas.
- **Sin bundler:** ES Modules nativos; `supabase-js` se copia a `app/vendor/` fijado a una versión, en lugar de cargarlo de un CDN.
- **Render seguro:** todo texto que venga de la IA o de usuarios entra al DOM con `textContent` o un escapador único; nunca con `innerHTML` directo.
- **Capas:** `modules/` puede llamar a `services/` y `engines/`; `engines/` no importa nada del navegador ni de Supabase.

## Diseño de módulos

Cada módulo conoce la base y la IA solo a través de los servicios, funciones de base de datos y Edge Functions de esta tabla; ninguno llama a Cohere ni escribe en tablas ajenas por su cuenta.

| Módulo | Qué resuelve | Tablas principales | Servidor | Fase |
| --- | --- | --- | --- | --- |
| 01 Command Center | Indicadores, trabajo pendiente y actividad con filtros por periodo, canal, campaña, estado y responsable; todo sale de la base, sin cifras inventadas | `campaigns`, `creative_pieces`, `audits`, `activity_logs` | Consultas bajo RLS y una función de agregados | 1 |
| 02 Copy Studio | Brief de 16 campos, generación con las seis fórmulas, edición, comparación, duplicado y recuperación de versiones | `briefs`, `copy_versions`, `ai_runs` | `ai-generate`, `ai-compare` | 2 |
| 03 Creative Auditor | Carga de PNG, JPG, JPEG y WEBP; lectura del texto de la pieza con el modelo de visión; auditoría de copy, diseño, UX y comunicación comercial; puntaje; ANTES / DESPUÉS | `creative_assets`, `audits`, `audit_findings` | `ai-audit` | 3 |
| 04 Promotion Validator | Reglas matemáticas con la tolerancia configurada, vigencias, condiciones y cruce entre brief, copy y arte; los bloqueos se guardan como hallazgos | `promotion_rules`, `validation_settings_versions`, `audit_findings` | Ninguno obligatorio; explicación con IA opcional | 4 |
| 05 Channel Adaptation | Reglas por canal y adaptación que conserva oferta, beneficio, condiciones y vigencia; comparación entre canales | `channel_rules`, `copy_versions` | `ai-adapt` | 5 |
| 06 Workflow & Approvals | Nueve estados con transiciones por permiso, asignaciones, comentarios, solicitudes de cambio, aprobación humana con separación de funciones, confirmación o descarte de hallazgos de IA, excepciones a bloqueos confirmados e historial | `creative_pieces`, `comments`, `audit_findings, approvals`, `commercial_block_exceptions`, `activity_logs` | `transition_piece_status`, `record_approval`, review\_finding, `grant_block_exception`, `revoke_block_exception` | 6 |
| 07 Creative Library | Búsqueda de texto, ocho filtros y reutilización de piezas aprobadas | Todas las anteriores | Consultas bajo RLS | 7 |
| 08 Performance Intelligence | Registro y carga CSV de métricas por pieza y variante, indicadores calculados y comparación A/B | `performance_metrics`, `ab_tests` | Ninguno obligatorio; la importación se valida en el navegador y en la base | 8 |
| 09 Settings & Brand | Marca versionada, usuarios, cinco roles y permisos por persona, rúbrica, tolerancias de validación, cuotas y modelos de IA | `brand_guidelines`, `brand_guideline_versions`, `memberships`, `role_permissions`, `membership_permission_grants`, `audit_rubric_versions`, `validation_settings_versions`, `ai_prompt_versions`, `ai_quotas` | `invite-user`, `export-org`, `ai-status`, `my_permissions` | 1 para usuarios, roles, permisos y ajustes base; el resto con el módulo que lo usa |

Otras funciones de servidor: `consume_ai_quota` descuenta el consumo de IA de forma atómica; `has_permission` es la función con la que las políticas RLS verifican cada permiso; `ai-status` informa si Cohere está configurado.

### Flujo de estados y transiciones

Propuesta mía (T-02), pendiente de tu validación junto con la matriz de permisos. La v2 listaba los nueve estados sin decir quién ejecuta cada transición. Toda transición pasa por `transition_piece_status` y queda en `activity_logs` con quién y cuándo.

| De | A | Permiso requerido | Condición |
| --- | --- | --- | --- |
| Borrador | En creación | copy.write o asset.upload | Ninguna |
| En creación | Pendiente de revisión | copy.write o asset.upload | Existe al menos una versión de copy |
| Pendiente de revisión | En corrección | piece.review | Comentario obligatorio |
| Pendiente de revisión | Pendiente de aprobación | piece.review | Ninguna adicional |
| En corrección | Pendiente de revisión | copy.write o asset.upload | Existe una versión nueva respecto de la revisada |
| Pendiente de aprobación | En corrección | piece.review o piece.approve | Comentario obligatorio |
| Pendiente de aprobación | Aprobado | piece.approve | Quien decide no creó ni modificó esa versión; ningún bloqueo confirmado sin excepción vigente; se inserta la aprobación con la versión exacta |
| Pendiente de aprobación | Rechazado | piece.approve | Motivo obligatorio; mismas reglas de independencia |
| Rechazado | En corrección | copy.write o asset.upload | Reabre la pieza; exige versión nueva antes de volver a revisión |
| Aprobado | Publicado | piece.publish | La versión aprobada es la vigente |
| Aprobado | En corrección | copy.write o asset.upload | Cualquier cambio crea una versión nueva; la aprobación anterior queda en el historial y no se hereda |
| Aprobado | Pendiente de aprobación | Automática al revocar una excepción usada | Propuesta T-06; si la pieza ya está Publicada, solo se avisa al responsable |
| Cualquiera menos Archivado | Archivado | piece.archive | Motivo; la pieza no se borra |

## Modelo de datos

Son 27 tablas: las 20 del prompt más 7 de apoyo. Tres ya estaban propuestas (`audit_rubric_versions`, `channel_rules`, `ai_quotas`) y cuatro nacen de tus decisiones (`role_permissions`, `membership_permission_grants`, `commercial_block_exceptions`, `validation_settings_versions`). Toda tabla de negocio lleva `organization_id`; ninguna consulta del frontend filtra por organización por sí sola, lo hace RLS.

Reglas globales del esquema:

- Claves primarias `uuid` con `gen_random_uuid()`; `created_at` y `updated_at` en `timestamptz`; `updated_at` lo mantiene un trigger.
- Dinero en `numeric(12,2)` con columna `currency` (supuesto: MXN por defecto, por confirmar). Nunca `float`; los cálculos en JavaScript se hacen en centavos enteros.
- Versiones (`copy_versions`, `brand_guideline_versions`, `ai_prompt_versions`, `audit_rubric_versions`, `validation_settings_versions`) son inmutables: se inserta una nueva, no se edita.
- Aprobaciones, auditorías, hallazgos, excepciones y `activity_logs` no se borran: la app no tiene `DELETE` sobre ellos. Aprobaciones y auditorías tampoco se editan.
- Los valores faltantes se guardan como `NULL`, nunca como `0`, para que PENDIENTE DE VALIDACIÓN y N/A sean distinguibles de un cero real.
- Las métricas derivadas (CTR, CPA, ROAS) no se almacenan: se calculan en JavaScript a partir de los valores crudos.
- Permisos: `role_permissions` es global y solo cambia por migración. Una persona con varios roles tiene la unión de los permisos de todos ellos.
- Búsqueda de la biblioteca: columna `tsvector` en configuración `spanish` con índice GIN.

| Tabla | Qué guarda | Claves, restricciones e índices |
| --- | --- | --- |
| `organizations` | Organización, `slug`, ajustes | `slug` único |
| `profiles` | Datos del usuario; `id` = `auth.users.id` | Sin `organization_id`: es del usuario |
| `memberships` | Persona en una organización con uno o más roles | `unique(organization_id, user_id)`; `roles` es un arreglo no vacío del enum admin, ecommerce, diseno, marketing, revisor\_aprobador |
| `role_permissions` *(nueva)* | Qué permisos da cada rol | Global; `unique(role, permission)`; lectura para usuarios autenticados; sin escritura desde la app |
| `membership_permission_grants` *(nueva)* | Permisos específicos concedidos a una persona, como el de conceder excepciones | Registra quién concede y cuándo; la revocación lleva fecha y responsable; solo quien tiene `org.manage` concede |
| `brand_guidelines` | Guía de marca vigente | Apunta a su versión actual |
| `brand_guideline_versions` | Tono, vocabulario, palabras prohibidas, claims, colores, tipografías, logo | `unique(guideline_id, version)`; inmutable |
| `campaigns` | Nombre, categoría, objetivo, vigencia, responsable | Índice `(organization_id, start_date)` |
| `briefs` | Los 16 campos del brief de Copy Studio | FK a campaña; `version` entera; promotion\_code opcional |
| `creative_pieces` | Pieza por canal y formato, estado de flujo, responsable, creador, campaña, brief de origen opcional y versión vigente (copy\_version\_id y creative\_asset\_id) | Estado enum de 9 valores; índice `(organization_id, status)` |
| `creative_assets` | Imagen: pieza, quien la subió, versión de copy a la que acompaña, ruta en Storage, MIME, bytes, ancho, alto, hash SHA-256 | Checks de MIME y tamaño; `kind` original o corregido |
| `copy_versions` | Titular, subtítulo, cuerpo, CTA, fórmula usada, origen (IA, humano, importado), autor (created\_by, también cuando el origen es IA: quien la pidió), brief y versión de brief usados | `unique(piece_id, version)`; `parent_version_id`; inmutable |
| `audits` | Versión exacta auditada (copy\_version\_id y creative\_asset\_id), rúbrica, ajustes de validación, modelo, prompt, resultado original y normalizado, cobertura, puntaje, veredicto, indicador de bloqueo comercial | FK a `ai_runs`, `audit_rubric_versions` y `validation_settings_versions`; FK compuesta a la versión auditada; solo inserción |
| `audit_findings` | Hallazgo con dimensión, severidad, clase propuesta por la IA (kind\_proposed), clase final asignada por el servidor (kind), fuente de verificación, zona opcional, origen (ia, motor\_reglas, humano), código de regla, marca de crítico comercial y estado de revisión (review\_state) | kind y kind\_proposed son enum (hecho verificado, inferencia, recomendación, pendiente de validación); check: kind = hecho verificado exige verification\_source distinta de ia y source\_ref; review\_state es enum (confirmado\_motor, propuesto\_ia, confirmado\_humano, descartado); confirmar o descartar exige responsable, fecha y motivo; el contenido no se edita ni se borra; cambia de estado solo con review\_finding; zona NULL si no se conoce |
| `commercial_block_exceptions` *(nueva)* | Excepción a un bloqueo confirmado: hallazgo, pieza, versión exacta (copy\_version\_id y creative\_asset\_id), responsable, justificación, fecha | FK compuesta (finding\_id, piece\_id, copy\_version\_id, creative\_asset\_id) a audit\_findings, solo si review\_state es confirmado\_motor o confirmado\_humano; justificación obligatoria (mínimo propuesto: 30 caracteres); no modifica el hallazgo; solo vale para esa versión; revocación con fecha, responsable y motivo; solo inserción de cada excepción |
| `approvals` | Decisión humana sobre una versión exacta (copy\_version\_id y creative\_asset\_id), con la auditoría considerada, las excepciones aplicadas (exception\_ids) y los hallazgos de IA sin revisar en ese momento (unreviewed\_ai\_findings) | Solo inserción; `decided_by` es una persona con `piece.approve` que no creó ni modificó esa versión: lo valida record\_approval y un trigger BEFORE INSERT; los arreglos de identificadores los valida un trigger al insertar |
| `comments` | Comentarios y solicitudes de cambio | `parent_id` para hilos |
| `promotion_rules` | Una fila por promoción y SKU: campaña, promotion\_code que agrupa los SKU de una promoción, precios, descuento declarado, fechas, condiciones, disponibilidad, si el precio incluye impuestos | Checks: precios no negativos, fin no anterior a inicio; las incoherencias se **marcan**, no se bloquean al guardar |
| `validation_settings_versions` *(nueva)* | Tolerancia de descuento en puntos porcentuales, decimales de precio y base de impuestos | Inmutable; tolerancia con tope propuesto de 5 puntos; cada auditoría guarda la versión usada |
| `performance_metrics` | Impresiones, clics, sesiones, conversiones, pedidos, ventas, inversión por pieza y variante | Valores `NULL` permitidos; `unique` por pieza, variante, canal y periodo |
| `ab_tests` | Hipótesis, variantes A y B, diseño, ganadora | Campo de diseño: causalidad solo si fue aleatorizado |
| `ai_runs` | Cada llamada a IA: función, proveedor, modelo, prompt, tokens, costo estimado, latencia, estado | Sin secretos ni imágenes completas; base de los límites de consumo |
| `ai_prompt_versions` | Plantilla, esquema de salida, modelo por defecto | `unique(key, version)`; inmutable |
| `activity_logs` | Quién hizo qué y cuándo, incluidas concesiones de permisos y excepciones | Escrito por triggers y funciones, nunca por el cliente |
| `audit_rubric_versions` *(propuesta)* | Ponderaciones, rangos, cobertura mínima (`min_coverage_pct`, 60 por defecto) y reglas de bloqueo | Inmutable; la suma de pesos debe dar 100 |
| `channel_rules` *(propuesta)* | Extensión, tono, estructura y CTA por canal | Una fila por organización y canal |
| `ai_quotas` *(propuesta)* | Tope diario y mensual de llamadas y costo | Lo consulta cada función de IA antes de llamar al proveedor |

El estado de `creative_pieces` se cambia solo con la función `transition_piece_status`, que valida la transición permitida (tabla de transiciones) y el permiso de quien la pide. Para pasar a Aprobado exige además que quien decide tenga `piece.approve`, que no haya creado ni modificado esa versión, que no quede ningún bloqueo confirmado (del motor o confirmado por una persona) sin excepción vigente para ella, y que la aprobación guarde la versión exacta, las excepciones aplicadas y los hallazgos de IA sin revisar. Un hallazgo de IA sin confirmar no bloquea. Un puntaje alto nunca cambia el estado.

### Auditoría final del modelo de datos

Revisé las 27 tablas contra los diez criterios de tu revisión final. Es una revisión del diseño, no de un esquema ejecutado: no corrió ningún SQL. Resultado: no se agrega ninguna tabla; se corrigen columnas y reglas.

| Criterio | Hallazgo | Ajuste |
| --- | --- | --- |
| Relaciones y claves foráneas | Un hijo podía apuntar a un padre de otra organización; RLS filtra lecturas pero no impide guardar la referencia | Cada padre tiene unique(organization\_id, id) y cada hijo una clave foránea compuesta con organization\_id (propuesta T-09) |
| Integridad de versiones | La versión de una pieza no estaba definida y approvals y las excepciones no la fijaban | Versión de pieza = copy\_version\_id más creative\_asset\_id cuando hay arte; creative\_pieces guarda la vigente; audits, audit\_findings, approvals y excepciones guardan la exacta; autor y quien sube se escriben por trigger con auth.uid(), no los envía el cliente |
| Historial de auditorías | audits es solo inserción y re-auditar crea otra fila; el estado «resuelto» de los hallazgos contradecía eso | Se elimina «resuelto»; la corrección genera una versión y una auditoría nuevas; el estado de revisión lo cambia solo review\_finding y cada cambio queda en activity\_logs |
| Campañas, briefs, piezas y artes | La cadena estaba implícita | campaigns 1→N briefs y piezas; la pieza guarda su campaña y, opcional, el brief de origen; copy\_versions guarda brief y versión de brief usados; creative\_assets pertenece a una pieza y a una versión de copy |
| Promociones, SKU, precios, descuentos y vigencias | Con una fila por promoción no se podía evaluar «hasta N %» entre varios SKU | Una fila por promoción y SKU, agrupadas por promotion\_code, con campaña, moneda, base de impuestos y vigencia con check de fechas. Queda abierto: si una pieza debe vincular promociones de varias campañas haría falta una tabla de unión; no se agrega ahora |
| Excepciones ligadas al hallazgo y la versión exactos | La v2 decía «versión afectada» sin forzarla | Clave foránea compuesta al hallazgo, la pieza y la versión; solo sobre hallazgos confirmados; un trigger impide usarla en otra versión |
| Aprobaciones inmutables | Correcto, con una salvedad: exception\_ids y unreviewed\_ai\_findings son arreglos y no tienen clave foránea | Un trigger los valida al insertar; como ni aprobaciones ni excepciones se borran, la referencia no puede quedar rota; sin UPDATE ni DELETE para ningún rol |
| Aislamiento por organización | Correcto en diseño; sin probar | Prueba por tabla (27 de 27), claves compuestas y funciones security definer con search\_path vacío |
| Integridad de archivos en Storage | Nada comparaba el objeto con su fila | Hash SHA-256, bytes y MIME verificados por magic bytes al registrar; el objeto no se reemplaza (una imagen nueva es otra fila y otra ruta); `verify_assets_integrity` compara filas, objetos y hashes y reporta huérfanos |
| Exportación y recuperación | Exportar archivos desde una Edge Function choca con los 2 s de CPU | Exportación en dos partes: JSON por tabla en orden de dependencias y un manifiesto de archivos con ruta, tamaño y hash, con URLs firmadas que descarga el navegador; la importación crea registros nuevos marcados como importados y verifica el hash de cada archivo. No probado |

Duplicidades revisadas y justificación de las siete tablas de apoyo:

| Tabla | Justificación | ¿Duplica algo? |
| --- | --- | --- |
| audit\_rubric\_versions | Pesos, rangos y cobertura versionados, con check de suma 100 | No. Fusionarla con validation\_settings\_versions ahorraría una tabla pero perdería ese check tipado; se mantienen separadas |
| validation\_settings\_versions | Tolerancia y precisión de precios versionadas; cada auditoría guarda la versión | No |
| channel\_rules | Reglas de canal que exige el módulo 05 | No |
| ai\_quotas | Topes de consumo; ai\_runs guarda el consumo | No; son cosas distintas |
| role\_permissions | Catálogo global de permisos por rol; sin ella los roles quedarían en el código | No |
| membership\_permission\_grants | Permisos concedidos a una persona | No; role\_permissions es por rol |
| commercial\_block\_exceptions | Una excepción es un hecho aparte del hallazgo y es revocable; guardarla en audit\_findings obligaría a reescribirlo | No |
| brand\_guidelines (del prompt) | Cabecera que solo apunta a la versión vigente; se detecta como casi redundante con brand\_guideline\_versions | Posible; se conserva por estar en el prompt y se decide en la Fase 1 (T-10) |

Matriz de las 27 tablas. La fase es la propuesta en la que se crea la tabla; las columnas que apuntan a tablas posteriores se agregan en la migración de la fase que crea la tabla destino.

| Tabla | Propósito | Relaciones | Controles de seguridad | Fase |
| --- | --- | --- | --- | --- |
| organizations | Raíz del aislamiento | Padre de todas las tablas de negocio | RLS: solo miembros; escritura con org.manage | 1 |
| profiles | Datos de la persona | 1:1 con auth.users | Cada persona ve su perfil y el de miembros de sus organizaciones | 1 |
| memberships | Persona en una organización con roles | organizations, profiles | RLS por is\_member; escritura con org.manage; roles no vacío | 1 |
| role\_permissions | Permisos por rol, global | Lo usa has\_permission | Lectura autenticada; solo cambia por migración | 1 |
| membership\_permission\_grants | Permisos por persona | memberships | Solo org.manage concede; revocación con responsable; auditoría | 1 |
| activity\_logs | Auditoría general | Referencia genérica a cualquier tabla | Escrita por triggers y funciones; sin UPDATE ni DELETE | 1 |
| campaigns | Agrupa el trabajo | Padre de briefs, piezas y promociones | RLS; campaign.write | 1 |
| creative\_pieces | Pieza, estado y versión vigente | campaigns, briefs, copy\_versions, creative\_assets | RLS; el estado solo cambia con transition\_piece\_status | 1 (estructura) y 6 (flujo) |
| brand\_guidelines | Cabecera de la guía vigente | brand\_guideline\_versions | RLS; org.manage | 2 |
| brand\_guideline\_versions | Guía de marca versionada | brand\_guidelines | Inmutable; RLS | 2 |
| briefs | Brief de 16 campos | campaigns; padre de copy\_versions | RLS; campaign.write; control de versión | 2 |
| copy\_versions | Texto versionado | creative\_pieces, briefs | Inmutable; autor escrito por trigger | 2 |
| ai\_runs | Registro de cada llamada a IA | organizations, profiles | Lo escriben las funciones; sin secretos ni imágenes completas | 2 |
| ai\_prompt\_versions | Prompts versionados | organizations | Inmutable; org.manage | 2 |
| ai\_quotas | Topes de IA | organizations | org.manage; consume\_ai\_quota atómico | 2 |
| creative\_assets | Arte subido | creative\_pieces, copy\_versions | RLS; asset.upload; hash y MIME verificados; objeto inmutable; Storage por prefijo de organización | 3 |
| audit\_rubric\_versions | Rúbrica versionada | organizations; la usa audits | Inmutable; suma de pesos 100; org.manage | 3 |
| audits | Resultado de una auditoría | copy\_versions, creative\_assets, ai\_runs, rúbrica y ajustes | Solo inserción; audit.run | 3 |
| audit\_findings | Hallazgos y su revisión | audits | Contenido inmutable; review\_state solo con review\_finding; finding.confirm y finding.dismiss | 3 |
| promotion\_rules | Reglas de promoción por SKU | campaigns | RLS; promotion.write; checks de precios y fechas | 4 |
| validation\_settings\_versions | Tolerancia y precisión | organizations; las usa audits | Inmutable; org.manage | 4 |
| channel\_rules | Reglas por canal | organizations | RLS; org.manage | 5 |
| comments | Comentarios y solicitudes de cambio | creative\_pieces, audit\_findings opcional | RLS; comment.write; el padre debe ser de la misma organización | 6 |
| commercial\_block\_exceptions | Excepciones a bloqueos confirmados | audit\_findings (clave compuesta), memberships | Solo inserción; block.exception.grant; revocación con motivo | 6 |
| approvals | Decisión humana sobre una versión | copy\_versions, creative\_assets, audits, personas | Sin UPDATE ni DELETE; trigger de independencia; piece.approve | 6 |
| performance\_metrics | Métricas por pieza y variante | creative\_pieces | RLS; metrics.write; unique por periodo | 8 |
| ab\_tests | Pruebas A/B | creative\_pieces, performance\_metrics | RLS; metrics.write | 8 |

## Seguridad y RLS

La seguridad descansa en tres piezas: la clave de Cohere existe solo como secreto de las Edge Functions, cada fila está protegida por RLS por organización y toda acción sensible se valida en el servidor. La clave pública (anon) viaja en el navegador por diseño; solo es segura si RLS está activo en todas las tablas, y una prueba automática lo verificará en cada fase.

| Amenaza | Control |
| --- | --- |
| Fuga de la clave de Cohere | Secreto de Supabase (`COHERE_API_KEY`), nunca en el repositorio ni en el navegador; `.gitignore` y revisión de secretos antes de cada commit |
| Mezcla con RevNavigator | Proyecto, claves, repositorio y vista previa propios (D-01); ninguna clave ni código se reutiliza |
| Acceso a datos de otra organización | RLS en todas las tablas con funciones `is_member(org)` y `has_permission(org, permiso)` definidas como `security definer`, con `search_path` vacío e índice en `memberships(user_id, organization_id)` |
| Roles o permisos manipulados desde el cliente | Los permisos se leen de `memberships`, `role_permissions` y `membership_permission_grants` en la base, nunca de `user_metadata`, que el usuario puede editar |
| Interfaz que solo oculta botones | Cada acción se valida en el servidor; la interfaz usa `my_permissions` únicamente para no mostrar lo que fallaría (D-04) |
| Uso indebido de excepciones a bloqueos | Permiso específico concedido por persona y no por rol, justificación obligatoria, responsable identificado, validez solo para esa versión, hallazgo original intacto y registro en `activity_logs` (D-07) |
| Acumulación de privilegios con varios roles | Los permisos se suman y esa suma es visible en Ajustes; la separación entre quien crea o modifica una versión y quien la aprueba es obligatoria y la valida la base de datos (sección Separación de funciones) |
| Edge Function usada con el JWT de otro | Cada función valida el JWT, crea el cliente con ese token para que RLS aplique y usa `service_role` solo para escribir `ai_runs` y `activity_logs` |
| Registro abierto | Alta solo por invitación de un Admin; registro público desactivado |
| Archivos maliciosos | Bucket privado `creative-assets`; solo PNG, JPG, JPEG y WEBP; sin SVG; límite de tamaño en el bucket y en la función; verificación de firma binaria (magic bytes) antes de enviar a la IA |
| Acceso a imágenes ajenas | Ruta `{org_id}/{pieza}/{uuid}.{ext}` y políticas sobre `storage.objects` que exigen que el primer segmento sea una organización del usuario; URLs firmadas de corta duración |
| Abuso y costo descontrolado de IA | Cuotas por usuario y organización en `ai_quotas`, conteo en `ai_runs`, tope de tamaño de solicitud y tiempo de espera; el cliente nunca elige el modelo libremente |
| XSS por texto generado | Todo texto de IA o de usuario entra al DOM como texto, nunca como HTML |
| Llamadas desde sitios no autorizados | CORS limitado al dominio de GitHub Pages y al de desarrollo |
| Datos sensibles en logs o prompts | Los logs no incluyen secretos ni cuerpos completos; los prompts no deben llevar datos personales de clientes ni de pacientes |
| Aprobación falsificada | Aprobar solo mediante función de base de datos que valida el permiso `piece.approve`, el estado, que quien aprueba no haya creado ni modificado esa versión y la ausencia de bloqueo confirmado sin excepción; un trigger en approvals repite la verificación; la tabla `approvals` no admite `UPDATE` ni `DELETE` (D-08) |

Dos límites que conviene conocer desde ahora:

- **Cabeceras de seguridad:** GitHub Pages no permite configurar cabeceras HTTP. La política CSP se aplicará con una etiqueta `<meta>`, que no cubre `frame-ancestors`. Para tener cabeceras completas habría que usar otro hosting estático.
- **Procesamiento de imágenes:** las Edge Functions de Supabase no admiten librerías como `sharp`, así que las imágenes se redimensionan en el navegador antes de subirlas.

Los cinco roles son decisión tuya (D-04). La matriz de abajo, qué permiso da cada uno, es mi propuesta (17 claves; finding.confirm y piece.publish son nuevas en la v3) y falta tu validación. Cada persona puede tener varios roles y recibe la unión de sus permisos. Admin no aprueba por defecto, y el permiso para conceder excepciones no pertenece a ningún rol: lo concede un Admin a una persona concreta.

| Permiso (clave) | Admin | Ecommerce | Diseño | Marketing | Revisor / Aprobador |
| --- | --- | --- | --- | --- | --- |
| Leer el contenido de la organización (content.read) | Sí | Sí | Sí | Sí | Sí |
| Comentar (comment.write) | Sí | Sí | Sí | Sí | Sí |
| Lanzar auditorías de IA (audit.run) | Sí | Sí | Sí | Sí | Sí |
| Crear y editar campañas y briefs (campaign.write) | Sí | Sí | No | Sí | No |
| Crear y editar copy (copy.write) | Sí | Sí | No | Sí | No |
| Subir artes y versiones corregidas (asset.upload) | Sí | No | Sí | Sí | No |
| Registrar reglas de promoción (promotion.write) | Sí | Sí | No | No | No |
| Adaptar a canales (channel.adapt) | Sí | Sí | No | Sí | No |
| Registrar métricas y pruebas A/B (metrics.write) | Sí | Sí | No | Sí | No |
| Revisar y pedir cambios (piece.review) | No | No | No | No | Sí |
| Aprobar o rechazar (piece.approve), sujeto a la separación de funciones | No | No | No | No | Sí |
| Confirmar un hallazgo crítico de IA, que pasa a ser bloqueo (finding.confirm) — nueva en v3 | No | No | No | No | Sí |
| Descartar un hallazgo de IA como falso positivo (finding.dismiss) | No | No | No | No | Sí |
| Publicar una pieza aprobada (piece.publish) — nueva en v3 | Sí | Sí | No | Sí | No |
| Archivar piezas (piece.archive) | Sí | No | No | No | Sí |
| Administrar usuarios, roles, marca, rúbrica, tolerancias, cuotas y modelos (org.manage) | Sí | No | No | No | No |
| Conceder una excepción a un bloqueo (block.exception.grant) | Ningún rol; concesión por persona |  |  |  |  |

La IA nunca figura como autor de una aprobación: `decided_by` siempre es una persona. Ninguna persona puede aprobar la versión que creó o modificó, tenga los roles que tenga.

### Separación de funciones en las aprobaciones

**Regla obligatoria (R-03):** una persona no puede aprobar la misma versión de una pieza que creó o modificó, aunque tenga varios roles. Se valida en el backend y en la base de datos; la interfaz solo refleja el permiso y nunca sustituye el control del servidor.

Definiciones que uso (T-04, por validar): la versión de una pieza es la versión de copy más el arte vigentes al enviarla a aprobación. Contribuyen a esa versión quien creó su versión de copy (también cuando el texto lo generó la IA: cuenta quien lo pidió) y quien subió su arte. El autor y quien sube se escriben por trigger con `auth.uid()`; el navegador no los envía, así que no se pueden falsificar desde el cliente.

| Capa | Control |
| --- | --- |
| Función `record_approval` | Rechaza con un mensaje claro si quien decide contribuyó a la versión; además valida el permiso, el estado, los bloqueos confirmados y las excepciones |
| Trigger BEFORE INSERT en `approvals` | Segunda barrera: rechaza la fila si `decided_by` contribuyó, aunque alguien intente insertar sin pasar por la función |
| Permisos de tabla | El cliente no tiene INSERT directo en `approvals`; la tabla no tiene UPDATE ni DELETE para ningún rol |
| Interfaz | Desactiva «Aprobar» a quien contribuyó y explica por qué; es ayuda, no control |

Nueva modificación: cualquier cambio de copy o de arte crea una versión nueva, devuelve la pieza a corrección y exige revisión y aprobación independientes. Una aprobación anterior no se hereda y permanece en el historial inmutable.

Efecto operativo: cada organización necesita al menos dos personas, una que cree y otra que apruebe. Un Admin no puede saltarse la regla.

Recomendación mía, no obligatoria (T-05): aplicar la misma independencia al confirmar o descartar hallazgos y al conceder excepciones sobre una versión en la que la persona contribuyó.

Amenazas nuevas que cubre esta sección y la de clasificación:

| Amenaza | Control |
| --- | --- |
| Autoaprobación por una persona con varios roles | Función y trigger de independencia; autor escrito por trigger |
| La IA se presenta como fuente de un hecho verificado | La IA propone la clase y el servidor la asigna; check en la base de datos; contraste determinístico |
| Descarte o confirmación de un hallazgo sin control | Permiso específico, motivo, responsable, fecha y registro en activity\_logs; el hallazgo original nunca se borra |

## Estrategia de IA

Todo acceso a IA pasa por una capa AI Service: el navegador llama a una Edge Function por tarea, y la función habla con un proveedor a través de una interfaz común (`generateText`, `generateStructured`, `analyzeImage`). Cohere es la primera implementación; cambiar de proveedor no toca los módulos. Ningún modelo está elegido todavía, porque no hay una clave real con la que comprobar qué modelos están habilitados.

Lo que la documentación oficial de Cohere confirma al 15 de noviembre de 2026:

| Tema | Dato verificado | Fuente |
| --- | --- | --- |
| Modelos con imagen de entrada | `command-a-plus-05-2026` (contexto de 128K, salida de 64K), `command-a-vision-07-2025` (128K y 8K) y `c4ai-aya-vision-32b` (16K y 4K) | [Models](https://docs.cohere.com/docs/models) |
| Modelos sin imagen | `command-a-03-2025` (256K de contexto, 8K de salida), `command-a-reasoning-08-2025`, `command-r-plus-08-2024` y otros; `c4ai-aya-vision-8b` fue retirado el 4 de abril de 2026 | [Models](https://docs.cohere.com/docs/models) |
| Command A+ | Entrada de texto e imagen; salidas estructuradas; disponible en producción mediante Model Vault | [Command A+](https://docs.cohere.com/docs/command-a-plus) |
| Command A Vision | Sin uso de herramientas; para producción hay que contactar a ventas | [Command A Vision](https://docs.cohere.com/docs/command-a-vision) |
| Imágenes | PNG, JPEG, WEBP y GIF sin animar; hasta 20 imágenes o 20 MB por solicitud; data URL en base64 y URL HTTP/HTTPS; parámetro `detail` en `low`, `high` o `auto` | [Image inputs](https://docs.cohere.com/docs/image-inputs) |
| Límites de uso | Clave de prueba: 1,000 llamadas al mes; 20 solicitudes por minuto en Command A+, A Vision y Command A. Producción: 500 por minuto en Command A; en Command A+ y A Vision, contactar a ventas | [Rate limits](https://docs.cohere.com/docs/rate-limits) |
| Tipo de clave | La clave de prueba es gratuita, limitada y no puede usarse para producción ni fines comerciales; la de producción es de pago y se solicita aparte | [Pricing](https://cohere.com/pricing) |
| Precios | La página de precios no lista tarifas de Command A+, Command A ni A Vision; solo de modelos antiguos | [Pricing](https://cohere.com/pricing) |
| Salida estructurada | JSON Schema con `response_format`; no admite `minimum`, `maximum`, `minItems`, `maxItems`, `minLength` ni `maxLength`; la página lista Command A+, Command A y Command R, y no menciona los modelos de visión | [Structured outputs](https://docs.cohere.com/docs/structured-outputs) |
| Edge Functions | 2 s de CPU por solicitud, 256 MB de memoria, 150 s de espera sin respuesta, función de hasta 20 MB empaquetada con la CLI | [Supabase limits](https://supabase.com/docs/guides/functions/limits) |

Tres decisiones de diseño que salen de esos datos:

- **El JSON de la IA no se da por bueno.** El esquema no puede imponer rangos (por ejemplo, 0 a 10 por dimensión) y no está confirmado para visión. Cada función valida la respuesta con su propio validador; si falla, hace un solo reintento de reparación y, si vuelve a fallar, devuelve un error claro. Nunca se recorta ni se corrige un valor fuera de rango en silencio.
- **Las imágenes viajan por URL, no por base64.** Con 2 s de CPU, convertir imágenes grandes a base64 dentro de la función es un riesgo. Se propone pasar a Cohere una URL firmada y de corta vida del bucket privado. Que Cohere pueda leer esas URLs no está probado: se comprueba en la prueba V5, con base64 como alternativa.
- **Solo desarrollo y pruebas (D-03).** Con 1,000 llamadas al mes y 20 solicitudes por minuto se puede probar, pero no trabajar a diario, y Cohere no permite usar la clave de prueba en producción ni con fines comerciales. La app no se usa para el trabajo real del equipo hasta que exista una clave de producción, que es una decisión futura tuya.

Cada llamada sigue el mismo recorrido:

1. Validar el JWT y el rol del usuario.
2. Revisar `ai_quotas` contra `ai_runs`; si se agotó, responder con el motivo.
3. Validar entrada: tamaño, tipo y esquema.
4. Armar el prompt desde la versión activa en `ai_prompt_versions`.
5. Llamar al proveedor con tiempo límite; un reintento con espera solo ante 429 o 5xx.
6. Validar y normalizar la salida.
7. Registrar en `ai_runs` modelo, prompt, tokens, costo estimado, latencia y estado.
8. Responder con los datos y los metadatos: modelo, versión de prompt, id de la ejecución.

Prompts versionados (clave y tarea): `copy.generate`, `copy.analyze`, `copy.compare`, `audit.text`, `audit.image`, `channel.adapt`, `promo.explain`. Todos piden a la IA proponer la clase de cada afirmación (nunca asignarla), adjuntar la evidencia que usó y omitir la zona de la pieza cuando no pueda ubicarla; la clase final la asigna el servidor (sección Clasificación de afirmaciones).

**Cohere no configurado:** una función `ai-status` informa si la integración está activa. Si no lo está, la interfaz muestra «Integración pendiente» y puede cargar datos de demostración con una marca DEMO visible. Esos datos no se guardan como auditorías ni copies reales, y no se registra ninguna ejecución de IA.

**Costos:** Cohere no publica tarifas de los modelos vigentes, solo de modelos antiguos, y las fuentes de terceros difieren, así que no hay un costo estimado confiable. Cada ejecución guarda tokens de entrada y salida; el costo estimado será tokens de entrada × tarifa de entrada + tokens de salida × tarifa de salida, con una tabla de tarifas que carga el Admin y que queda vacía hasta tener la tarifa de Cohere. Con la clave de prueba las llamadas son gratuitas pero limitadas.

### Clasificación de afirmaciones

**Regla (R-01):** la IA nunca puede certificarse a sí misma como fuente de un hecho verificado. Puede proponer hechos, pero solo el contraste contra fuentes confiables o reglas determinísticas permite clasificarlos como verificados.

| Clase | Definición | Quién la asigna | Efecto |
| --- | --- | --- | --- |
| Hecho verificado | Respaldado por una fuente identificable y contrastable: una regla determinística, el brief, la regla de promoción, la guía de marca vigente o una fuente que una persona revisora cita | El servidor tras el contraste, o una persona con finding.confirm que cita la fuente | Puede fundamentar un bloqueo confirmado |
| Inferencia | Interpretación no confirmada, como el texto que el modelo lee de una imagen | La IA propone; el servidor asigna | Se muestra como tal; no bloquea |
| Recomendación | Sugerencia de mejora | La IA o una persona | No es un hecho; no bloquea |
| Pendiente de validación | Requiere comprobación: dato faltante o afirmación sin fuente | El servidor | No bloquea; pide revisión |

Cómo se aplica:

1. La IA devuelve cada afirmación con la clase que propone y la evidencia que usó (cita del texto, zona de la imagen o dato del brief). Esa clase se guarda como `kind_proposed` y no es la clase final.
2. El servidor asigna `kind`. Si la IA propone «hecho verificado» y el servidor no puede contrastarlo, lo guarda como pendiente de validación y conserva la propuesta original; nunca lo sube a hecho.
3. Se contrastan por regla determinística las cifras, fechas y porcentajes contra el brief y las reglas de promoción, las palabras prohibidas contra la guía de marca y la extensión contra las reglas de canal. Todo lo demás sigue como inferencia o pendiente hasta que una persona lo confirme y cite la fuente.
4. Lo que el modelo lee de una imagen es siempre inferencia hasta que una persona confirme la lectura.
5. Una fuente que la IA cite no cuenta mientras una persona no la compruebe. La IA no certifica cumplimiento regulatorio.
6. La base de datos rechaza guardar `kind` = hecho verificado sin `verification_source` distinta de ia y sin `source_ref`.

Dónde queda documentada: principio de arquitectura, prompts (arriba), columnas de `audit_findings`, insignias de la interfaz, exportación de auditorías y casos del plan de pruebas.

### Verificación de Cohere en desarrollo

Propuesta de partida, por confirmar: `command-a-plus-05-2026` para texto y visión (una sola configuración) y `command-a-03-2025` como alternativa de texto. Los umbrales de éxito son propuestas mías. Todas las pruebas usan piezas y briefs ficticios que preparo yo; con una clave de prueba no se usan datos reales ni regulados.

| ID | Qué se comprueba | Cómo | Criterio de éxito propuesto |
| --- | --- | --- | --- |
| V1 | Qué modelos habilita tu clave | Una llamada mínima a cada modelo candidato | Responden `command-a-plus-05-2026`, `command-a-vision-07-2025` y `command-a-03-2025`, o se documenta cuáles no |
| V2 | Salida estructurada con texto | 20 solicitudes por tarea con JSON Schema | 95 % válidas a la primera y 100 % tras un reintento de reparación |
| V3 | Lectura de imágenes | 10 piezas ficticias en PNG, JPG y WEBP, con precio, porcentaje y vigencia conocidos, usando `detail` en `low`, `high` y `auto` | Se reporta la coincidencia exacta de precios, porcentajes y fechas; umbral por acordar contigo |
| V4 | Visión con salida estructurada | Las mismas piezas con JSON Schema | Si no es válida a la primera con regularidad, se usa solo el validador propio |
| V5 | Imagen por URL firmada o por base64 | La misma pieza por las dos vías | Si Cohere no lee la URL firmada, se usa base64 con tope de tamaño |
| V6 | Límites reales | Ráfagas de solicitudes y conteo contra el tope mensual | Se documenta cuándo responde 429 y que el reintento con espera lo supera |
| V7 | Latencia | 20 llamadas por tarea | Se reportan mediana y percentil 95; deben caber en los 150 s de la Edge Function |
| V8 | Calidad en español de México | Briefs ficticios de distintas categorías | Tu revisión: sin claims inventados y tono adecuado |
| V9 | Consumo y costo | Tokens observados por tarea | Se reporta el consumo; el costo en dinero queda pendiente de la tarifa de Cohere |

## Motores determinísticos

Tres motores en `app/engines/`, escritos como funciones puras en JavaScript, deciden los números: el puntaje de auditoría, la validación de promociones y las métricas. La IA aporta texto y notas por dimensión; nunca la fórmula final ni un cálculo.

### Puntaje de auditoría

Cada dimensión recibe una nota de 0 a 10 o N/A. El puntaje se normaliza sobre las dimensiones evaluables, de modo que una dimensión sin datos no suma ni resta:

```latex
\text{Puntaje} = 100 \times \frac{\sum_{i \in E} w_i \cdot (s_i / 10)}{\sum_{i \in E} w_i}
```

Donde `E` es el conjunto de dimensiones evaluables, `w_i` su peso y `s_i` su nota.

| Dimensión | Peso | Quién aporta la nota (propuesta) |
| --- | --- | --- |
| Claridad | 15 | IA sobre el texto |
| Titular | 15 | IA sobre el texto |
| Beneficio y persuasión | 15 | IA sobre el texto |
| Propuesta comercial | 15 | IA sobre el texto y el brief |
| CTA | 10 | IA sobre el texto |
| UX y legibilidad | 10 | IA con visión; N/A si no hay imagen |
| Coherencia de marca | 10 | IA contra la versión vigente de la guía |
| Precisión comercial | 10 | Validador de promociones; N/A si no hay datos de promoción |

Los pesos suman 100 y viven en `audit_rubric_versions`, no en el código.

| Rango | Veredicto |
| --- | --- |
| 90 o más | Excelente |
| 80 hasta menos de 90 | Bueno, ajustes menores |
| 70 hasta menos de 80 | Requiere correcciones |
| Menos de 70 | Replanteamiento |

El prompt escribe los rangos como 80–89 y 70–79, lo que deja sin cubrir valores como 89.5. Propongo límite inferior incluido y superior excluido, aplicado sobre el puntaje redondeado a un decimal, que es el que ve la persona.

**Cobertura mínima (D-05, aprobada provisionalmente).** Se mide por peso evaluable, y tu revisión final lo confirma. El valor vive en `audit_rubric_versions.min_coverage_pct` (60 por defecto). Así se calcula y se presenta:

1. **Cobertura.** C = 100 × suma de los pesos de las dimensiones evaluables ÷ suma de los pesos de todas las dimensiones de la versión de rúbrica. Una dimensión es evaluable si tiene una nota válida de 0 a 10; es N/A si falta el dato que la sustenta (sin imagen, sin datos de promoción) o si la IA no devolvió una nota válida tras el reintento. N/A nunca vale 0.
2. **Umbral.** Se cumple si C ≥ min\_coverage\_pct; el límite exacto cumple. Los pesos son enteros y la comparación no redondea.
3. **Normalización.** Puntaje = 100 × suma de (peso × nota ÷ 10) ÷ suma de los pesos evaluables. Una dimensión N/A no suma ni resta. Las notas son enteras de 0 a 10 (propuesta T-08). El puntaje se redondea a un decimal, mitad hacia arriba, y con ese valor se asigna el rango.
4. **Por debajo del mínimo.** El veredicto es «Evaluación incompleta»: no se muestra rango, el puntaje no se presenta como resultado y se listan las dimensiones evaluadas y las que faltan. Si ninguna es evaluable no se divide y no hay puntaje.
5. **Presentación de rangos.** Puntaje, rango y cobertura juntos, por ejemplo «75.7 · Requiere correcciones · cobertura 70 %». El límite inferior del rango se incluye y el superior se excluye.
6. **El puntaje no sustituye la aprobación humana.** No cambia estados, no aprueba ni rechaza; solo informa. Aprobar exige una decisión humana trazable (D-08) aunque el puntaje sea 100 y la cobertura completa. Cumplir la cobertura mínima tampoco equivale a aprobar.
7. **Un bloqueo confirmado prevalece.** Con un bloqueo confirmado (del motor o por revisión humana) el veredicto visible es BLOQUEADO o BLOQUEADO con excepción vigente, el puntaje queda como dato informativo y la función de aprobación rechaza la acción sea cual sea el puntaje o la cobertura. Un hallazgo de IA sin confirmar no cambia ni el veredicto ni el puntaje.

Ejemplo calculado: se evalúan Claridad 8, Titular 7, Beneficio y persuasión 9, Propuesta comercial 6 y CTA 8; UX y legibilidad, Coherencia de marca y Precisión comercial quedan N/A. Cobertura = 70 %. Puntaje = 100 × (12 + 10.5 + 13.5 + 9 + 8) ÷ 70 = 75.7, rango Requiere correcciones. Verifiqué las cifras con un cálculo aparte; todavía no existe el motor que las reproduzca.

Casos límite que se vuelven pruebas obligatorias (todas las notas en 10 salvo que se indique):

| Caso | Peso N/A | Cobertura | Resultado esperado |
| --- | --- | --- | --- |
| Todas evaluables | 0 | 100 % | Puntaje y rango |
| N/A UX y Precisión comercial | 20 | 80 % | Puntaje y rango |
| N/A CTA, UX, Coherencia y Precisión | 40 | 60 % exacto | Cumple; puntaje y rango |
| N/A Titular, UX, Coherencia y Precisión | 45 | 55 % | Evaluación incompleta, sin rango |
| Todas N/A | 100 | 0 % | Evaluación incompleta, sin puntaje y sin dividir por cero |
| Puntaje 89.9 y 90.0 | — | — | Bueno y Excelente |
| Puntaje 79.9 y 80.0 | — | — | Requiere correcciones y Bueno |
| Puntaje 69.9 y 70.0 | — | — | Replanteamiento y Requiere correcciones |
| Puntaje 89.95, 79.95 y 69.95 | — | — | Se muestran 90.0, 80.0 y 70.0 y toman el rango superior (prueba de la función de redondeo) |
| Puntaje 100 con un bloqueo confirmado | — | cualquiera | BLOQUEADO; la aprobación se rechaza |
| Puntaje 100 sin bloqueo | — | 100 % | El estado no cambia solo; falta la decisión humana |

### Bloqueos comerciales, hallazgos de IA y excepciones

Un hallazgo comercial crítico impide aprobar la pieza aunque el puntaje sea alto (D-05), pero solo cuando está confirmado. Cada hallazgo está en uno de cuatro estados de revisión (R-02), y el estado decide si bloquea. La interfaz los muestra con cuatro insignias con texto.

| Estado (review\_state) | Qué es | ¿Bloquea la aprobación? | Cómo se llega |
| --- | --- | --- | --- |
| Bloqueo confirmado por motor determinístico (confirmado\_motor) | Lo crea una regla determinística sobre datos que no provienen de la IA | Sí | Automático al validar; no se descarta: se corrige el dato o se concede una excepción |
| Hallazgo crítico propuesto por IA, no corroborado (propuesto\_ia) | La IA sospecha un incumplimiento comercial crítico | No | Lo propone la IA; el servidor lo guarda como inferencia o pendiente de validación |
| Hallazgo crítico de IA confirmado por revisión humana (confirmado\_humano) | Una persona con finding.confirm verificó el incumplimiento y citó la fuente | Sí; pasa a ser bloqueo con las reglas de D-07 | review\_finding con motivo y fuente |
| Falso positivo descartado por persona autorizada (descartado) | Una persona con finding.dismiss determinó que no hay incumplimiento | No | review\_finding con motivo obligatorio (mínimo propuesto de 30 caracteres), responsable y auditoría |

- Un hallazgo de IA no corroborado no bloquea. La pantalla de aprobación lo muestra de forma destacada y la aprobación guarda cuáles estaban sin revisar en ese momento (`unreviewed_ai_findings`), para que la decisión sea trazable.
- Confirmar o descartar exige el permiso, un motivo y deja responsable y fecha en el propio hallazgo y en `activity_logs`. El registro original no se borra ni se reescribe: solo cambia su estado de revisión, mediante `review_finding`, y cada cambio queda en el historial.
- Lo que la IA lee de una imagen (precio, porcentaje o fecha del arte) es inferencia: una diferencia con el copy sale como hallazgo propuesto por IA y pasa a bloqueo cuando una persona confirma la lectura.
- Descartar solo aplica a hallazgos de IA. Un bloqueo del motor no se descarta: si la causa es un dato mal cargado, se corrige el dato y se revalida, lo que genera una auditoría nueva.
- Un bloqueo confirmado nunca desaparece solo: ni al subir el puntaje, ni al re-auditar, ni con el paso del tiempo. Si una versión corregida ya no incumple, su auditoría nueva no lo genera; el original queda en el historial de la versión anterior.
- Excepción (D-07) a un bloqueo confirmado: exige el permiso `block.exception.grant`, justificación obligatoria, responsable identificado y registro de auditoría. El hallazgo original sigue abierto y visible. Vale para un hallazgo en una versión concreta y no se hereda; se puede revocar con motivo, responsable y fecha.
- Veredicto: BLOQUEADO, o BLOQUEADO con excepción vigente. La aprobación guarda las excepciones aplicadas.
- Propuesta T-06: si se revoca una excepción que ya usó una aprobación, la pieza vuelve a Pendiente de aprobación; si ya estaba Publicada, solo se avisa a su responsable. El registro de la aprobación no se altera.

### Validador de promociones

| Regla | Resultado |
| --- | --- |
| Descuento calculado = (regular − promocional) / regular × 100 difiere del declarado más de la tolerancia (aprobada como valor inicial: 0.5 puntos porcentuales, configurable en Ajustes) | Bloqueo |
| Precio promocional mayor que el regular | Bloqueo |
| Fecha de fin anterior a la de inicio, o vigencia ya vencida | Bloqueo |
| El copy dice «hasta N %» y ningún producto participante llega a N % | Bloqueo |
| Fechas, porcentajes o precios del copy distintos de la regla o del brief | Bloqueo |
| Fechas, porcentajes o precios del arte distintos del copy | Hallazgo marcado como inferencia, porque el texto del arte lo extrae la IA |
| Campo obligatorio vacío, incluida la disponibilidad | PENDIENTE DE VALIDACIÓN, nunca un valor supuesto |

Los números, fechas y porcentajes del copy se extraen con expresiones regulares probadas, no con IA.

### Precios, redondeo y descuentos

Reglas de la decisión D-06:

1. **Entrada:** los precios se leen como texto y se convierten a centavos enteros, con formato es-MX (coma de miles, punto decimal). Un valor con más de dos decimales o que no sea número queda PENDIENTE DE VALIDACIÓN; nunca se redondea en silencio.
2. **Moneda e impuestos:** una moneda por organización (supuesto: MXN). `promotion_rules` registra si el precio incluye impuestos; si falta ese dato, comparar precios de fuentes distintas queda PENDIENTE DE VALIDACIÓN.
3. **Cálculo:** descuento = (precio regular − precio promocional) / precio regular × 100, con aritmética entera sobre centavos. No se redondea antes de comparar.
4. **Comparación:** el descuento declarado es correcto si la diferencia absoluta con el calculado es menor o igual que la tolerancia. El límite exacto se acepta.
5. **Redondeo de presentación:** un decimal, mitad hacia arriba, solo para mostrar y nunca para decidir.
6. **«Hasta N %»:** N se compara con el mayor descuento calculado entre los productos participantes, con la misma tolerancia; cada producto se evalúa por separado.
7. **Precios en copy y arte:** se comparan al centavo contra la regla, sin tolerancia; la tolerancia solo aplica a porcentajes.
8. **Configuración:** la tolerancia se cambia en Ajustes con el permiso `org.manage`, como una versión nueva (tope propuesto de 5 puntos). Cada auditoría guarda la versión que usó, y cambiarla no altera auditorías anteriores.

Ejemplos con la tolerancia inicial de 0.5 puntos, para que se pueda comprobar a mano:

| Precio regular | Precio promocional | Calculado | Declarado | Diferencia | Resultado |
| --- | --- | --- | --- | --- | --- |
| $1,250.00 | $1,000.00 | 20.0 % | 20 % | 0.0 | Correcto |
| $1,000.00 | $804.00 | 19.6 % | 20 % | 0.4 | Correcto |
| $1,000.00 | $795.00 | 20.5 % | 20 % | 0.5 | Correcto, en el límite |
| $1,000.00 | $806.00 | 19.4 % | 20 % | 0.6 | Bloqueo |

### Métricas de rendimiento

| Métrica | Fórmula |
| --- | --- |
| CTR | clics / impresiones × 100 |
| Conversión | conversiones / sesiones × 100 |
| CPC | inversión / clics |
| CPA | inversión / conversiones |
| ROAS | ventas atribuidas / inversión |

Si el denominador es cero o falta un dato, el resultado es «—» y nunca 0. Los datos incoherentes (más clics que impresiones) se marcan, no se descartan. En las pruebas A/B se muestra la diferencia con su incertidumbre, y no se declara ganadora ni se atribuye causalidad si la prueba no está registrada como aleatorizada.

## Sistema visual y UX

La interfaz es neutra y sobria: una paleta gris, un solo color de acento y colores de estado solo para estados. Los colores de la marca configurados en Ajustes aparecen únicamente dentro de las vistas previas de piezas, nunca en la interfaz de la app. Los valores exactos de color se fijan en Fase 1 con una pantalla de muestra para tu revisión.

| Elemento | Decisión |
| --- | --- |
| Tokens | Variables CSS en `tokens.css`: color, tipografía, espacio, radio y elevación; ningún valor suelto en los módulos |
| Tipografía | Una familia de sistema; texto base de 15 px, mínimo de 13 px, interlineado de 1.5 |
| Espaciado y forma | Escala de 4 px; radio de 8 px; bordes de 1 px; sombras solo en modales y menús |
| Navegación | Sidebar con los 9 módulos en el orden del prompt; header con selector de organización, búsqueda, estado de la integración de IA y menú de usuario |
| Escritorio (1200 px o más) | Sidebar fija de 240 px, tablas completas, comparadores lado a lado |
| Tablet (768 a 1199 px) | Sidebar reducida a íconos, filtros en un panel desplegable |
| Móvil (menos de 768 px) | Menú en cajón, tablas convertidas en tarjetas, objetivos táctiles de 44 px; lectura, revisión y aprobación funcionan, la edición larga es secundaria |
| Accesibilidad | Contraste AA (4.5:1 en texto), foco visible, navegación por teclado, etiquetas en todos los campos, estados que no dependen solo del color |
| Estados de pieza | 9 chips con texto: Borrador, En creación, Pendiente de revisión, En corrección, Pendiente de aprobación, Aprobado, Rechazado, Publicado, Archivado |
| Naturaleza de cada afirmación | 4 insignias distintas con ícono y texto: Hecho verificado, Inferencia, Recomendación, Pendiente de validación; la de Hecho verificado solo aparece si el servidor la asignó, nunca porque la IA lo diga |
| Datos de demostración | Banner fijo y marca DEMO en cada elemento; no se mezclan con datos reales |
| Carga y errores | Esqueletos en tablas; en llamadas a IA, indicador con tiempo transcurrido y botón de cancelar; errores con causa y siguiente paso, sin códigos crudos |
| Estados vacíos | Explican qué va ahí y ofrecen la acción para crearlo |

Componentes compartidos que se construyen una vez en `app/ui/`: tabla con orden, filtros y paginación desde el servidor; barra de filtros; modal y diálogo de confirmación; aviso temporal; comparador de textos; comparador ANTES / DESPUÉS de imágenes; lista de hallazgos; medidor de puntaje. El Command Center evita el exceso de tarjetas: una fila corta de indicadores, una lista de trabajo pendiente y una actividad reciente.

No se planea modo oscuro, porque el prompt no lo pide.

Los permisos se reflejan en la interfaz: lo que el usuario no puede hacer se oculta o se desactiva con una explicación breve, y los roles de cada persona son visibles en su perfil. Esa capa es solo ayuda; el servidor rechaza igualmente cualquier acción sin permiso.

## Plan de pruebas

Cada fase termina con las diez comprobaciones del prompt, y el informe separa tres clases de evidencia: **real** (se ejecutó contra el sistema verdadero), **con mock** (se ejecutó contra una simulación) y **no ejecutado**. Una prueba con mock nunca se reporta como integración real.

| Capa | Qué cubre | Herramienta | Estado en este entorno |
| --- | --- | --- | --- |
| Unitarias | Motores de puntaje, promociones y métricas; extractores de números y fechas; validadores de respuestas de IA | `node:test`, integrado en Node 22 | Node 22.23.4 verificado |
| Funciones de borde | Autenticación, cuotas, validación, manejo de errores del proveedor | `deno test` con respuestas de Cohere grabadas | Deno no instalado |
| RLS y permisos | Por cada tabla, un usuario de la organización A no lee, inserta, edita ni borra filas de la B; cada rol hace solo lo suyo; ninguna tabla queda sin RLS | Scripts SQL con `psql` sobre un Supabase local o un proyecto de pruebas | `psql` 16.15 verificado; Supabase CLI no instalado; cliente de Docker presente, demonio sin verificar |
| Integración | Navegador, Edge Functions, base y Storage trabajando juntos | Supabase local o proyecto de pruebas | Pendiente de decidir dónde (ver Configuraciones) |
| Funcionales de extremo a extremo | Flujos completos: brief a copy, subir arte a auditoría, enviar a aprobación | Playwright o Chrome automatizado | Google Chrome for Testing 153 presente; Playwright sin verificar |
| Cohere real | Una prueba de humo manual por tarea de IA con clave real, registrada en `ai_runs` | Script manual | Bloqueada hasta tener clave |
| Regresión | Se repiten todas las suites de fases anteriores | Mismo ejecutor | Desde Fase 2 |
| Accesibilidad y rendimiento | Contraste, teclado, lector de pantalla; tiempos de carga | axe-core y Lighthouse, más revisión manual | Fase 9 |
| Concurrencia | Dos usuarios editando la misma pieza, aprobaciones simultáneas, cuotas de IA bajo carga | Pruebas de integración con peticiones paralelas | Fase 9 |

Decisiones de diseño que vuelven comprobables esos casos:

- **Edición concurrente:** cada actualización de pieza o brief envía la versión que leyó; si cambió, el servidor responde con conflicto y la app lo muestra, en lugar de sobrescribir en silencio.
- **Cuotas de IA:** el consumo se descuenta con una operación atómica en la base, para que dos solicitudes simultáneas no excedan el tope.
- **Datos de prueba:** las semillas llevan una marca DEMO y viven solo en el entorno de pruebas.
- **Permisos (D-04):** una prueba por cada permiso y cada rol, y por combinaciones de roles, que intenta la acción directamente contra la API y no solo por la interfaz; además, otra que confirma que la suma de permisos de varios roles es la esperada.
- **Excepciones y aprobaciones (D-07, D-08):** ciclo completo: bloqueo, intento de aprobar, excepción sin permiso rechazada, excepción sin justificación rechazada, excepción válida, aprobación con excepción registrada, revocación y hallazgo original intacto.
- **Redondeo (D-06):** los cuatro ejemplos de la sección de precios y descuentos son casos de prueba obligatorios, junto con los límites de la tolerancia.
- **Clasificación de afirmaciones (R-01):** si la IA propone «hecho verificado» sin fuente, se guarda como pendiente de validación; con contraste determinístico se guarda como hecho verificado con su fuente; la base rechaza kind = hecho verificado sin fuente; un texto leído de una imagen queda como inferencia.
- **Hallazgos de IA (R-02):** uno propuesto no bloquea; confirmar o descartar sin permiso, sin motivo o sin fuente se rechaza; uno confirmado bloquea y sigue las reglas de D-07; descartar conserva el registro y su historial; un bloqueo del motor no se puede descartar.
- **Separación de funciones (R-03):** quien contribuyó a una versión, con cualquier combinación de los cinco roles, no puede aprobarla ni por la función ni con un INSERT directo; una modificación nueva exige otra aprobación independiente; la aprobación previa no se hereda; el autor no se puede falsificar desde el cliente.
- **Modelo de datos (R-04):** las claves compuestas impiden referencias entre organizaciones y entre versiones; una excepción no se puede usar en otra versión; ningún rol puede actualizar ni borrar aprobaciones; la matriz de aislamiento por RLS cubre las 27 tablas.
- **Storage y recuperación:** hash y MIME coinciden con la fila; `verify_assets_integrity` detecta huérfanos; una ruta de otra organización se deniega; exportar y reimportar conserva los hashes y marca los registros como importados.
- **Puntaje (R-05):** los casos límite de cobertura y de redondeo de la sección de puntaje; un puntaje 100 con bloqueo sigue BLOQUEADO y un puntaje 100 sin bloqueo no cambia el estado.

Una fase se da por lista cuando cumple los seis criterios de aceptación del prompt y entrega el informe A a L. COMPLETADA no es lo mismo que ACEPTADA POR EL USUARIO: la aceptación es tuya y no se da por supuesta.

## Riesgos y dependencias

Los dos riesgos que pueden detener el avance son la infraestructura de Supabase, que hoy solo existe dentro de la organización de RevNavigator, y los límites de la clave de prueba de Cohere. La columna Impacto es mi valoración, no un dato medido.

| Riesgo | Impacto | Mitigación |
| --- | --- | --- |
| La organización de Supabase conectada hoy es la de RevNavigator; usarla mezclaría infraestructuras que D-01 manda separar | Alto | Organización y proyecto nuevos y dedicados (D-02), creados por ti o con tu autorización expresa |
| El plan gratuito de Supabase permite dos proyectos activos entre todas tus organizaciones, y no sé qué plan tiene la de RevNavigator | Medio | Comprobar en el panel el plan y los proyectos activos antes de crear el nuevo |
| El plan gratuito pausa el proyecto tras una semana sin actividad y no incluye respaldos | Medio | Aceptable en desarrollo; antes de uso real, plan de pago en una organización aparte (no se mezclan planes en una organización) |
| La clave de prueba de Cohere: 1,000 llamadas al mes y no se puede usar en producción ni con fines comerciales | Alto | Solo desarrollo y pruebas con material ficticio (D-03); la clave de producción es una decisión futura tuya |
| Cohere no publica precios de los modelos vigentes | Medio | Tabla de tarifas vacía hasta tenerla; se reporta el consumo en tokens |
| La salida estructurada no está confirmada para los modelos de visión | Medio | Validador propio, un reintento de reparación y error claro; se prueba en V4 |
| Límites de las Edge Functions: 2 s de CPU, 256 MB, sin sharp | Medio | Redimensionar en el navegador, pasar imágenes por URL firmada, no procesar imágenes en la función |
| Costo de IA sin control | Medio | Cuotas, tabla de tarifas cargada por el Admin, registro por ejecución |
| La IA inventa precios, condiciones o ubicaciones en la pieza | Alto | Números y fechas por motores determinísticos, clase de cada afirmación asignada por el servidor, zona vacía si no se conoce, aprobación humana obligatoria |
| La IA se presenta como fuente de un hecho verificado | Alto | La IA propone y el servidor asigna la clase; check en la base de datos; contraste determinístico; pruebas de R-01 |
| Claims de salud o regulatorios en las piezas | Alto | La IA no certifica cumplimiento regulatorio; los claims permitidos viven en la guía de marca y la revisión regulatoria es humana |
| Excepciones a bloqueos concedidas con demasiada facilidad | Alto | Permiso por persona, justificación obligatoria, vigencia por versión, auditoría y reporte de excepciones en el Command Center |
| Hallazgos críticos de IA sin revisar que llegan a la aprobación | Medio | No bloquean, pero se muestran destacados y la aprobación guarda cuáles estaban sin revisar; reporte en el Command Center |
| Falsos positivos de IA que alargan la revisión | Bajo a medio | Descarte con permiso, motivo y auditoría; el registro nunca se borra |
| Una persona con varios roles aprueba su propio trabajo | Medio | Mitigado por regla obligatoria: la función de aprobación y un trigger de la base lo impiden (R-03) |
| Una organización con menos de dos personas capaces de crear y aprobar no puede aprobar nada | Medio | Efecto buscado de R-03; se pide al menos dos personas (P-04) y no hay excepción para el Admin |
| Datos personales en prompts | Medio | Advertencia en los formularios y exclusión de campos personales; los logs no guardan cuerpos completos |
| Retención y uso de datos por parte de Cohere | Por determinar | Revisar los términos de la cuenta antes de enviar material real; no verificado (P-09) |
| Exportar y recuperar archivos choca con los límites de las Edge Functions | Medio | Exportación en JSON más manifiesto de archivos con hash y descarga desde el navegador; prueba de recuperación en Fase 9; no probado |
| Filas de `creative_assets` y objetos de Storage desalineados | Medio | Hash, objetos inmutables y `verify_assets_integrity` |
| Impuestos en los precios sin definir | Medio | `promotion_rules` registra la base de impuestos; sin ese dato, PENDIENTE DE VALIDACIÓN (P-06) |
| GitHub Pages con repositorio privado depende del plan de GitHub; con plan gratuito el repositorio debe ser público | Medio | Decidir entre repositorio público (el frontend no lleva secretos), un plan que permita privado u otro hosting (P-02, P-10) |
| GitHub Pages no permite cabeceras HTTP | Bajo a medio | CSP por meta; si se exige más, cambiar de hosting estático |
| Texto pequeño en imágenes se lee mal | Medio | detail: high, imágenes con buena resolución, lecturas marcadas como inferencia |
| Alcance de 9 módulos y 10 fases | Medio | Fases con aceptación explícita; nada se inicia sin tu aprobación |

Dependencias externas, en el orden en que se necesitan:

1. Organización y proyecto de Supabase nuevos y dedicados, con nombre y región elegidos (P-01). Antes de Fase 1.
2. Repositorio nuevo en GitHub, independiente del de RevNavigator (P-02). Antes de Fase 1.
3. Instalar Deno y la CLI de Supabase en el entorno de desarrollo y confirmar que el demonio de Docker funciona. Fase 1.
4. Clave de prueba de Cohere cargada como secreto, para las pruebas V1 a V9 (P-03). Fase 2 para texto, Fase 3 para visión.
5. Decisión sobre retención de datos y respaldos, antes de usar material real (P-09).
6. Dominio y hosting definitivos, para configurar CORS, las URL de redirección de Auth y las cabeceras de seguridad (P-10). Fase 9; en desarrollo se usa la dirección de pruebas.

## Configuraciones que requieren tu intervención

Ningún paso necesita que escribas una clave en el chat. Las credenciales las cargas tú directamente en el panel de Supabase o con su CLI, y yo solo verifico que el sistema responde.

| ID | Qué se necesita | Cuándo | Cómo | Recomendación mía (no aprobada) |
| --- | --- | --- | --- | --- |
| P-01 | Organización y proyecto de Supabase nuevos y dedicados (D-02): nombre, región y plan | Antes de Fase 1 | Los creas tú siguiendo la sección siguiente, o me autorizas de forma expresa; crear el proyecto puede tener costo | Región más cercana a tus usuarios; plan gratuito solo para desarrollo |
| P-02 | Repositorio nuevo en GitHub (D-01): nombre y visibilidad | Antes de Fase 1 | Lo creas tú o me autorizas; no se hace commit ni push sin tu orden | Privado si tu plan permite Pages con repositorio privado; si no, público, porque el frontend no lleva secretos |
| P-03 | Clave de prueba de Cohere (D-03), solo para desarrollo | Fase 2 para texto, Fase 3 para visión | La guardas tú como secreto COHERE\_API\_KEY en Supabase; nunca se pega en el chat; yo solo hago las pruebas V1 a V9 | Pruebas solo con material ficticio |
| P-04 | Personas que usarán la app y sus roles de los cinco aceptados (D-04) | Fase 1 | Lista de correos y roles; las invitaciones salen del panel | Al menos dos personas distintas, una que cree y otra que apruebe |
| P-05 | Quién tendrá el permiso individual para conceder excepciones | Fase 1 para la estructura, Fase 6 para el uso | Nombres de las personas | Una o dos personas, sin que el Admin lo tenga por defecto |
| P-06 | Moneda (supuesto MXN), zona horaria (supuesto America/Mexico\_City) y tratamiento de impuestos | Fase 1 | Confirmar o corregir | Registrar por promoción si el precio incluye impuestos, sin valor por defecto |
| P-07 | Límite máximo de imágenes | Fase 3 | Decidir el número | 10 MB por archivo tras redimensionar y una imagen por auditoría de imagen; Cohere acepta hasta 20 MB por solicitud (dato verificado) |
| P-08 | Tope de la tolerancia configurable en Ajustes (D-06) | Fase 4 | Decidir el número | 5 puntos porcentuales |
| P-09 | Retención de datos y respaldos | Antes de usar material real | Revisar los términos de Cohere y el plan de Supabase | Plan con respaldos o exportación propia periódica; periodo de retención por definir contigo |
| P-10 | Dominio y hosting definitivo | Fase 9 | Decidir hosting y dirección | GitHub Pages para desarrollo; hosting con cabeceras para datos reales |
| — | Tope mensual de gasto en IA y, si Cohere te lo comunica, precio por millón de tokens | Fase 2 | Lo cargas en Ajustes o me lo dices | — |
| — | Guía de marca inicial: tono, vocabulario, palabras prohibidas, claims permitidos, colores, tipografías y logo | Fase 1 para estructura, Fase 2 para contenido | Archivos o texto en el chat | — |
| — | Reglas reales por canal: extensiones, formatos y CTA | Fase 5 | Documento o ejemplos de piezas aprobadas | — |

## Crear la organización y el proyecto de Supabase

Pasos y requisitos para D-02. No se ha creado nada: la organización conectada hoy en mis herramientas es la de RevNavigator y no se usa.

1. **Revisar tu cuenta.** En el panel de Supabase, confirma qué plan tiene cada organización y cuántos proyectos activos tienes; el plan gratuito permite dos proyectos activos entre todas tus organizaciones.
2. **Crear la organización.** Nombre sugerido: Copy & Creative Intelligence. Elige tipo y plan; cada organización tiene un solo plan, por eso conviene aparte si luego pasa a pago.
3. **Crear el proyecto dentro de ella.** Nombre, región (la más cercana a tus usuarios, que decides tú) y una contraseña de base de datos que guardas en tu gestor de contraseñas y que no se comparte en el chat.
4. **Configurar Auth.** Alta solo por invitación (registro abierto desactivado) y la dirección de pruebas del sitio como URL de redirección. La definitiva se configura en Fase 9.
5. **Cargar el secreto de Cohere.** Tú guardas `COHERE_API_KEY` como secreto de las Edge Functions. Yo nunca la veo.
6. **Pasarme solo lo público.** La URL del proyecto y su clave publicable. Nunca la clave de servicio ni la contraseña de la base.
7. **Autorizar el uso.** Dime el identificador del proyecto y qué te autorizo a hacer en él (migraciones, funciones). Hasta entonces no creo ni modifico nada.

Quedan sin verificar: el costo exacto de tu plan y si la organización nueva comparte facturación con las existentes.

## Roadmap consolidado

La Fase 0 consolidada (v3) es técnicamente COMPLETADA CON LIMITACIONES DOCUMENTADAS y espera tu aceptación formal; ninguna otra fase ha empezado.

&#91;embedded content: roadmap · 10 fases, una aceptación entre cada una\]

COMPLETADA no equivale a ACEPTADA POR EL USUARIO: ninguna fase tiene ese estado todavía. La tabla detalla la Fase 0 subfase por subfase y resume las siguientes.

| Fase | Subfase | Descripción | Estado | Evidencia | Limitaciones | Actual |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 0.1 | Inspección del entorno | COMPLETADA CON LIMITACIONES | Sección Línea base del entorno | Docker, Playwright, Deno y la CLI de Supabase sin verificar; Cohere sin clave |  |
| 0 | 0.2 | Definición de arquitectura | COMPLETADA | Secciones Arquitectura objetivo y Estructura del proyecto | Es diseño; nada construido |  |
| 0 | 0.3 | Modelo de datos | COMPLETADA CON LIMITACIONES | Sección Modelo de datos, auditoría y matriz de 27 tablas | No se ejecutó SQL; falta tu validación de las tablas |  |
| 0 | 0.4 | Seguridad | COMPLETADA CON LIMITACIONES | Sección Seguridad y RLS, con separación de funciones | RLS, permisos y triggers sin probar; CSP limitada por el hosting |  |
| 0 | 0.5 | Diseño de módulos | COMPLETADA | Sección Diseño de módulos, con transiciones de estado | Pantallas detalladas se diseñan en cada fase |  |
| 0 | 0.6 | Estrategia de pruebas | COMPLETADA CON LIMITACIONES | Sección Plan de pruebas | Herramientas por instalar; entorno de pruebas sin decidir |  |
| 0 | 0.7 | Riesgos y dependencias | COMPLETADA | Secciones Riesgos y dependencias, Configuraciones y Pasos de Supabase | Dos riesgos por determinar: retención de datos en Cohere y respaldos |  |
| 0 | 0.8 | Revisión final y consolidación (v3) | COMPLETADA CON LIMITACIONES | Dictamen técnico, Registro de cambios, Matriz de decisiones, Informe de limitaciones | Revisión documental; nada se ejecutó | Sí: espera tu aceptación |
| 1 | 1.1 a 1.9 | Estructura, sistema visual, navegación, autenticación, organización y usuarios, roles y permisos, Supabase, migraciones, dashboard inicial | PENDIENTE | — | Requiere la organización y el proyecto nuevos de Supabase (P-01) y el repositorio nuevo (P-02) |  |
| 2 | 2.1 a 2.8 | Brief, Cohere, propuestas, fórmulas, edición, comparación, versionado, pruebas | PENDIENTE | — | Requiere la clave de prueba de Cohere (P-03); sin uso en producción |  |
| 3 | 3.1 a 3.9 | Carga de imágenes, OCR, visión, auditoría de texto, clasificación de afirmaciones, estados de hallazgos de IA, diseño y UX, puntaje, comparación, pruebas | PENDIENTE | — | Requiere un modelo de visión habilitado en la clave de prueba, confirmar la salida estructurada (V4) y el límite de imágenes (P-07) |  |
| 4 | 4.1 a 4.7 | Modelo de promociones, reglas, vigencias, condiciones, comparación de fuentes, bloqueos confirmados y excepciones, pruebas | PENDIENTE | — | Tolerancia aprobada (D-06); faltan el tope (P-08) y los impuestos (P-06) |  |
| 5 | 5.1 a 5.6 | Modelos de canal, extensión, adaptación, consistencia, comparación, pruebas | PENDIENTE | — | Requiere las reglas reales por canal |  |
| 6 | 6.1 a 6.8 | Estados, asignaciones, comentarios, correcciones, aprobaciones humanas con separación de funciones (D-08), confirmación y descarte de hallazgos, excepciones, historial, permisos, pruebas | PENDIENTE | — | Roles aceptados (D-04); faltan las personas y roles (P-04) y los permisos de excepción (P-05) |  |
| 7 | 7.1 a 7.6 | Biblioteca, búsqueda, filtros, versionado, recuperación, pruebas | PENDIENTE | — | — |  |
| 8 | 8.1 a 8.7 | Métricas, importación, indicadores, variantes, análisis, aprendizajes, pruebas | PENDIENTE | — | Requiere datos reales de resultados |  |
| 9 | 9.1 a 9.9 | Seguridad, accesibilidad, rendimiento, responsive, pruebas integrales y de concurrencia, exportación y recuperación, documentación, despliegue, auditoría de aceptación | PENDIENTE | — | Requiere el dominio y hosting definitivos (P-10) y la decisión de retención y respaldos (P-09) |  |

## Criterios de entrada de la Fase 1

La Fase 1 entrega las subfases 1.1 a 1.9 del roadmap y crea ocho tablas: organizations, profiles, memberships, role\_permissions, membership\_permission\_grants, activity\_logs, campaigns y creative\_pieces. No empieza hasta que se cumplan todos estos criterios y la autorices de forma expresa.

| # | Criterio de entrada | Quién | Estado |
| --- | --- | --- | --- |
| 1 | Aceptación formal de la Fase 0 v3 y autorización expresa de la Fase 1 (A-01) | Tú | Pendiente |
| 2 | Organización y proyecto de Supabase creados, con su URL y su clave publicable (P-01) | Tú, o yo con tu autorización | Pendiente |
| 3 | Repositorio nuevo creado, con su visibilidad decidida (P-02) | Tú, o yo con tu autorización | Pendiente |
| 4 | Lista inicial de personas y roles, con al menos dos personas capaces de aprobar (P-04) | Tú | Pendiente |
| 5 | Moneda y zona horaria confirmadas (P-06) | Tú | Pendiente |
| 6 | Hosting de pruebas decidido (P-10) | Tú | Pendiente |
| 7 | Deno, CLI de Supabase y Docker instalados y verificados | Yo, con tu autorización | Pendiente |

No se necesitan para entrar a la Fase 1: la clave de Cohere (Fase 2), el contenido de la guía de marca (Fase 2) y las reglas de canal (Fase 5).

## Informe de limitaciones no resueltas

| ID | Limitación | Efecto | Cómo se resuelve |
| --- | --- | --- | --- |
| L-01 | Nada se ejecutó: esquema, RLS, funciones, triggers y claves compuestas son diseño en papel | No sé si se implementan tal cual | Fase 1: migraciones y pruebas contra Supabase local o el proyecto de pruebas |
| L-02 | Cohere sin una sola llamada: modelos habilitados, salida estructurada con visión, URLs firmadas y latencia | Las pruebas V1 a V9 no tienen resultados | Clave de prueba (P-03) |
| L-03 | Sin costo estimado confiable de Cohere | La tabla de tarifas queda vacía | Tarifa publicada o la de tu contrato |
| L-04 | La clave de prueba no puede usarse en producción ni con fines comerciales | La app no sirve para el trabajo real del equipo | Decisión futura tuya sobre un plan de producción |
| L-05 | Docker, Playwright, Deno y la CLI de Supabase sin verificar | Pruebas locales y de extremo a extremo sin comprobar | Fase 1, con tu autorización |
| L-06 | GitHub Pages no permite cabeceras de seguridad | CSP por meta, sin frame-ancestors | P-10 |
| L-07 | Sin documentar el límite del cuerpo de solicitud de las Edge Functions; exportación de archivos por manifiesto sin probar | Puede cambiar el diseño de carga y exportación | Pruebas en las Fases 3 y 9 |
| L-08 | Retención de datos de Cohere, respaldos y facturación de Supabase sin verificar | Riesgo si se usan datos reales | P-09 |
| L-09 | Pantallas, colores y textos de la interfaz sin diseñar | Sin revisión visual | Fase 1, con una pantalla de muestra |
| L-10 | Las cifras de puntaje, cobertura y descuentos se calcularon aparte y no con un motor | Los ejemplos todavía no son pruebas | Pruebas unitarias desde las Fases 3 y 4 |
| L-11 | Dos preguntas abiertas de diseño: promociones de varias campañas en una pieza (¿tabla de unión?) y la cabecera brand\_guidelines | Podrían cambiar una tabla | Fase 4 y Fase 1 |

## Pendientes

Son once decisiones o acciones tuyas (P-01 a P-10 y la aceptación) y ocho cosas que no verifiqué; la Fase 1 no empieza hasta que aceptes la Fase 0 y la autorices de forma expresa.

Por decidir o validar tú:

- [ ] P-01 Organización y proyecto de Supabase: crearlos con los pasos del documento o autorizarme de forma expresa.
- [ ] P-02 Repositorio de GitHub: nombre, visibilidad y si tu plan permite Pages con repositorio privado.
- [ ] P-03 Clave de prueba de Cohere guardada por ti como secreto; sin ella la Fase 2 solo corre con datos de demostración.
- [ ] P-04 Personas y asignación de roles, con al menos dos personas capaces de aprobar.
- [ ] P-05 Quién recibirá el permiso individual para conceder excepciones.
- [ ] P-06 Moneda, zona horaria y tratamiento de impuestos de los precios.
- [ ] P-07 Límite máximo de imágenes (propongo 10 MB por archivo y una imagen por auditoría de imagen).
- [ ] P-08 Tope de la tolerancia configurable (propongo 5 puntos porcentuales).
- [ ] P-09 Retención de datos y respaldos.
- [ ] P-10 Dominio y hosting definitivos.
- [ ] A-01 Aceptación formal de la Fase 0 v3, que incluye las propuestas técnicas T-01 a T-10 y las 27 tablas.

Lo que no verifiqué:

- Ninguna llamada real a Cohere: no hay clave, y no sé qué modelos habilita tu cuenta.
- Que la salida estructurada funcione con modelos de visión, y que Cohere pueda leer URLs firmadas de Storage.
- Todo el diseño técnico (esquema, políticas RLS, funciones, triggers y claves compuestas) está en papel: no se ejecutó ningún SQL ni se creó nada en Supabase.
- El contenido de los dos proyectos existentes de Supabase: solo se listaron y no se tocaron.
- Si el demonio de Docker funciona, si Playwright se instala y si Deno y la CLI de Supabase se pueden descargar desde este entorno.
- Los precios de Cohere: no hay tarifa pública para los modelos vigentes y ninguna fuente es de tu contrato.
- El límite de tamaño del cuerpo de solicitud de las Edge Functions, y que la exportación de archivos por manifiesto funcione dentro de sus límites.
- Los términos de retención de datos de Cohere, los respaldos y la facturación de tu plan de Supabase, y si GitHub Pages sirve repositorios privados en tu plan.
