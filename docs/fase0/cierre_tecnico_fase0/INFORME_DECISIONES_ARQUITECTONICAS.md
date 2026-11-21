# INFORME DE DECISIONES ARQUITECTÓNICAS

**Naturaleza:** recomendaciones técnicas. **Ninguna decisión está aprobada.** Todas llevan el estado de aprobación `REQUIERE_APROBACION_DEL_PROPIETARIO`. Claude no firma la Adenda v9, no acepta Fase 0 ni designa personas.

Fuente de datos: `REGISTRO_DECISIONES_RECOMENDADAS.csv` (21 filas, columnas de §10 del encargo). Evidencia local: `scripts_validacion/resultados/`.

| ID | Nombre | Estado técnico | Estado de aprobación |
|---|---|---|---|
| G-1 | Relación maestra–adaptación (IG1, 18 reglas clase D) | RECOMENDADO_REQUIERE_APROBACION | REQUIERE_APROBACION_DEL_PROPIETARIO |
| G-5 | Registro de evaluación de impacto, independencia y aprobación positiva (IG5, 78 reglas clase D) | RECOMENDADO_REQUIERE_APROBACION | REQUIERE_APROBACION_DEL_PROPIETARIO |
| G-10 | Registro de intentos de publicación e idempotencia (IG10, 26 reglas clase D) | RECOMENDADO_REQUIERE_APROBACION | REQUIERE_APROBACION_DEL_PROPIETARIO |
| DG-19 | Catálogo de canales y formatos (channel_rules + channel_formats) | RECOMENDADO_REQUIERE_APROBACION | REQUIERE_APROBACION_DEL_PROPIETARIO |
| DG-20 | Columna approvals.decision con CHECK = 'aprobada' | RECOMENDADO_REQUIERE_APROBACION | REQUIERE_APROBACION_DEL_PROPIETARIO |
| DG-09 | Política de retención de datos | PENDIENTE_DE_INFORMACION_EXTERNA | REQUIERE_APROBACION_DEL_PROPIETARIO |
| DEP-RET-01 | Dependencia de retención: retiro de contenido externo al reemplazar una pieza | NO_RESOLUBLE_EN_FASE_0 | REQUIERE_APROBACION_DEL_PROPIETARIO |
| DG-12 | Hash encadenado de registros | RECOMENDADO_REQUIERE_APROBACION | REQUIERE_APROBACION_DEL_PROPIETARIO |
| DG-16 | Umbrales de texto (30 y 10 caracteres) y T-03 | RECOMENDADO_REQUIERE_APROBACION | REQUIERE_APROBACION_DEL_PROPIETARIO |
| DG-18 | Columna opcional replaces_piece_id | RECOMENDADO_REQUIERE_APROBACION | REQUIERE_APROBACION_DEL_PROPIETARIO |
| G-9 | Historial de revisor asignado (piece_reviewer_assignments) | RECOMENDADO_REQUIERE_APROBACION | REQUIERE_APROBACION_DEL_PROPIETARIO |
| RP-01 | Responsable administrativo del nivel 3 | RECOMENDADO_REQUIERE_APROBACION | REQUIERE_APROBACION_DEL_PROPIETARIO |
| P-01 | Organización y proyecto de Supabase propios | PENDIENTE_DE_INFORMACION_EXTERNA | REQUIERE_APROBACION_DEL_PROPIETARIO |
| P-02 | Repositorio de GitHub y visibilidad | RECOMENDADO_REQUIERE_APROBACION | REQUIERE_APROBACION_DEL_PROPIETARIO |
| P-03 | Clave de prueba de Cohere | PENDIENTE_DE_INFORMACION_EXTERNA | REQUIERE_APROBACION_DEL_PROPIETARIO |
| P-04 | Personas y roles (≥2 que puedan aprobar) | PENDIENTE_DE_INFORMACION_EXTERNA | REQUIERE_APROBACION_DEL_PROPIETARIO |
| P-05 | Permisos individuales para conceder excepciones | PENDIENTE_DE_INFORMACION_EXTERNA | REQUIERE_APROBACION_DEL_PROPIETARIO |
| P-10 | Dominio y hosting definitivos | PENDIENTE_DE_INFORMACION_EXTERNA | REQUIERE_APROBACION_DEL_PROPIETARIO |
| OD-13 | Decisión original reservada OD-13 | PENDIENTE_DE_INFORMACION_EXTERNA | REQUIERE_APROBACION_DEL_PROPIETARIO |
| PO-05 | Aceptación de la Adenda v9 | RECOMENDADO_REQUIERE_APROBACION | REQUIERE_APROBACION_DEL_PROPIETARIO |
| HV-02 | Línea 126 del registro histórico menciona «addendum v3» mientras PO-05 se refiere a v9 | PENDIENTE_DE_INFORMACION_EXTERNA | REQUIERE_APROBACION_DEL_PROPIETARIO |


## 0. Separación de los cinco elementos por decisión

Fuente: `REGISTRO_DECISIONES_RECOMENDADAS.csv`. *CCI-DEV* = si la evidencia necesaria incluye validación en el esquema/entorno físico. Ninguna decisión está aprobada.

| ID | 1. Recomendación técnica | 2. Decisión del propietario | 3. Evidencia necesaria | 4. Dependencia de CCI-DEV | 5. Datos no disponibles |
|---|---|---|---|---|---|
| G-1 | B: aceptar §3 con tres correcciones menores (DG-19 PK natural, normalización por expresión regular, alinear nombres de columnas con v3.3). | Aceptar, aceptar con cambios o rechazar el diseño de §3 (G-1). | Inventario FK en CCI-DEV (INV-03), PE-01..04 sobre esquema físico, EX-T03/T06 adaptados. | Sí | ninguno identificado |
| G-5 | B: aceptar por bloques en ese orden; no declarar G-5 cerrado hasta validar el bloque 4 en CCI-DEV. | Aceptar el orden por bloques y decidir DT-01/DT-02. | PLAN_VALIDACION_TRIGGER_R1_R9.md; K47 físico (ATR); CONC-03/04. | Sí | ninguno identificado |
| G-10 | A: aceptar tal cual, con DG-09/DG-12 explícitamente diferidas y CONC-06 como prueba obligatoria. | Aceptar o rechazar el diseño de G-10. | CONC-06; pruebas_guarda físico; privilegios. | Sí | ninguno identificado |
| DG-19 | B: PRIMARY KEY (organization_id, channel, format). Normalización: CHECK `format ~ '^[a-z0-9_]{1,40}$'` (igual para canal) **si** el propietario confirma el alf… | Aceptar DG-19; confirmar alfabeto de canal/formato; la organización entrega el catálogo real. | PG-CF-01..15 sobre el esquema físico; EX-DG19c/d; inventario INV-03. | Sí | catálogo real de canales/formatos (LR-14) |
| DG-20 | A, con una condición de verificación: confirmar que el rechazo vive sólo en transiciones+comments/activity_logs (v3.3 lo respalda: T-02 «Pendiente de aprobació… | Aprobar o rechazar la ampliación mínima; confirmar que los rechazos no se almacenan en approvals. | EX-DG20a..h repetidas sobre el esquema físico; prueba de record_approval y de que ningún rol inserta directo. | Sí | ninguno identificado |
| DG-09 | A hasta que el propietario y quien corresponda legalmente fijen la política; mientras tanto documentar que no hay purga automática. Para B: la estructura técni… | Definir la política de retención (plazos y base legal) o mantenerla diferida. | N/A hasta que exista política. | No identificada en el registro | política de retención (LR-15) |
| DEP-RET-01 | Resolver DG-09 y designar responsable (RP-01 o equivalente) antes de decidir A/B; no añadir estados ni transiciones. | Definir procedimiento y responsable. | N/A. | No identificada en el registro | procedimiento de retiro externo y responsable (LR-15) |
| DG-12 | Diseño de referencia para 6.6 (no aprobado): SHA-256 sobre `versión_formato // hash_previo(32 bytes) // JSON canónico UTF-8` (claves ordenadas, sin espacios, N… | Decidir si DG-12 se adelanta; aprobar el formato canónico versionado; confirmar la ancla externa. | HC-01..HC-16 (local); en CCI-DEV: verificación de cadena sobre datos reales y prueba de manipulación como superusuario de PRUEBA. | Sí | ninguno identificado |
| DG-16 | 1) Corregir ahora la definición de «no vacío» a «contiene al menos un carácter significativo» (regex que excluya espacios Unicode, NBSP y caracteres de ancho c… | Decidir si se adoptan los umbrales 30/10 y cerrar T-03. | EX-DG16a..r sobre el esquema físico en UTF8. | Sí | umbrales no aprobados (30/10) como valores definitivos |
| DG-18 | B: `replaces_piece_id uuid NULL`, FK (organization_id, replaces_piece_id) → creative_pieces(organization_id, id) ON DELETE RESTRICT, CHECK (replaces_piece_id I… | Aprobar o rechazar la columna; decidir si la reemplazada debe estar Publicada. | EX-DG18a..i en el esquema físico; T-63. | Sí | ninguno identificado |
| G-9 | B con 1 revisor vigente por pieza: columnas id, organization_id, piece_id, reviewer_id, assigned_by, valid_during tstzrange (inicio inclusivo, fin exclusivo, n… | Definir quién puede registrar asignaciones y aceptar G-9. | EX-G9a..j, CC-01 sobre el esquema físico; privilegios de quién inserta. | Sí | ninguno identificado |
| RP-01 | Perfil (sin nombres): persona con membresía activa, capaz de acceder a CCI-PROD sólo mediante procedimientos aprobados, sin ser autora de las piezas que aprueb… | Designar a la persona (nombre real) y, si procede, un suplente. | Revisión de accesos en CCI-DEV (PRIV-06). | Sí | nombres reales de responsables (LR-19) |
| P-01 | A: dos proyectos independientes; el propietario los crea o autoriza; credenciales sólo por canal seguro. | Crear/autorizar la organización y los proyectos. | Confirmación de IDs de proyecto (P1 del plan CCI-DEV). | Sí | organización/proyectos Supabase (LR-20) |
| P-02 | Privado mientras haya diseño de seguridad sin publicar; el repositorio `appalex47-lab/Copy-Creative-Intelligence` ya existe y contiene la documentación de Fase… | Confirmar nombre, propietario y visibilidad. | — | No identificada en el registro | infraestructura (LR-20) |
| P-03 | Cargar como secreto del servidor (Edge Function secret), nunca en el cliente ni en chat; Claude no la solicita. | Proveer la clave por canal seguro cuando llegue Fase 2. | Revisión de secretos (sin credenciales en repositorio). | No identificada en el registro | infraestructura (LR-20) |
| P-04 | Al menos dos personas con `piece.approve` y que no contribuyan a las versiones que aprueban; la lista la aporta el propietario. | Entregar personas y roles. | R1–R9 con personas reales de prueba. | Sí | nombres reales de responsables (LR-19) |
| P-05 | A: lista mínima de personas, concedido con `org.manage`, con responsable y auditoría; sin concesión por cargo. | Indicar quién puede conceder excepciones. | Prueba de concesión y revocación con responsable. | No identificada en el registro | nombres reales de responsables (LR-19) |
| P-10 | Diferir a 9.8 (no bloquea Fase 1); mientras tanto CSP restrictiva por defecto. | Elegir dominio y hosting. | Revisión CSP en 9.8. | No identificada en el registro | infraestructura (LR-20) |
| OD-13 | Aportar la Adenda v9 (o la página de OD-13) para analizarla; no se infiere el contenido. | Entregar la Adenda v9 y decidir OD-13. | — | No identificada en el registro | texto de OD-13 (LR-16) |
| PO-05 | B o A **después** de revisar la Adenda v9 completa: la recomendación técnica es no aceptarla a ciegas, porque su texto no está en el expediente y las decisione… | Aceptar, aceptar con correcciones o rechazar la Adenda v9; confirmar que PO-05 se refiere hoy a v9. | — | No identificada en el registro | texto de la Adenda v9 (LR-16) |
| HV-02 | A (ya aplicada en V20/V26): no editar; el propietario confirma la correspondencia PO-05 = Adenda v9. Consecuencia: HV-02 queda NO VERIFICABLE hasta esa confirm… | Confirmar que PO-05 se refiere a la Adenda v9 (SHA-256 ccb1c546…). | — | No identificada en el registro | confirmación de que PO-05 se refiere a la v9 (LR-17) |

No se inventan política de retención, responsables reales, infraestructura, catálogo real, umbrales no aprobados ni el contenido de la Adenda v9/OD-13; si el texto fuente no está disponible, se declara.

## G-1 — Relación maestra–adaptación (IG1, 18 reglas clase D)

- **Fuente original:** ESPECIFICACION_TECNICA_G1_G5_G10.md §3 (línea 57) y tabla de estado (línea 5023); INVENTARIO_DECISIONES_ABIERTAS_FASE0.md
- **Texto original recuperado:** «Modelo técnico consistente en diseño: identidad, un nivel, versión de origen, arte, ciclo de vida del catálogo de canales y formatos desde 1.8, clave, clasificación, autoría heredada y conservación» (línea 5023). 153 reglas son clase D: IG5 78, IG10 26, IG1 18, IS 15, IM 9, IE 7.
- **Problema:** 18 reglas IG1 dependen de un diseño no aceptado: sin aceptación no hay base para migraciones.
- **Alternativas:** A) Aceptar el diseño de §3 tal cual. B) Aceptarlo con las correcciones de este cierre (PK de channel_formats, normalización robusta, nombre `decided_by`). C) Rediseñar la relación (p. ej. sin FK compuestas).
- **Recomendación técnica:** B: aceptar §3 con tres correcciones menores (DG-19 PK natural, normalización por expresión regular, alinear nombres de columnas con v3.3).
- **Justificación:** La semántica de FK compuestas, inmutabilidad y unicidad se demostró en PostgreSQL temporal (PE-01..04: 18/18; extensión EX-T03/T06: PASS).
- **Impactos:** funcional — Habilita adaptaciones de una maestra con versión y arte exactos. · datos — Nuevas columnas en creative_pieces/copy_versions y tabla channel_formats. · seguridad/integridad — Aislamiento por organization_id en cada FK; sin RLS probada. · migración — Migración aditiva en 1.8; sin datos históricos. · compatibilidad — Compatible con v3.3 (27 tablas intactas).
- **Dependencias:** DG-19; DG-18; G-5 (contribuyentes heredados). · **Reversibilidad:** Alta antes de migrar; media después (hay datos).
- **Pruebas necesarias:** Inventario FK en CCI-DEV (INV-03), PE-01..04 sobre esquema físico, EX-T03/T06 adaptados.
- **Evidencia local de este cierre:** EX-T03a..g, EX-T06a..d, CC-02 (todas PASS en PG16 UTF8).
- **Resuelto técnicamente vs. sólo propietario:** Técnicamente resuelto: diseño y correcciones. Sólo propietario: aceptar el diseño.
- **Estado técnico:** `RECOMENDADO_REQUIERE_APROBACION` · **Estado de aprobación:** `REQUIERE_APROBACION_DEL_PROPIETARIO`
- **Decisión requerida del propietario:** Aceptar, aceptar con cambios o rechazar el diseño de §3 (G-1).

## G-5 — Registro de evaluación de impacto, independencia y aprobación positiva (IG5, 78 reglas clase D)

- **Fuente original:** ESPECIFICACION_TECNICA_G1_G5_G10.md §4 (línea 405), línea 5024, IG5-48
- **Texto original recuperado:** G-5 «no se declara completamente cerrada» mientras la representación física de contribuciones (PC-02), la procedencia por campo (H-02), la integridad compuesta (H-03), la definición operativa (DT-01) y la elegibilidad del proponente (DT-02) no estén aceptadas ni validadas (IG5-48).
- **Problema:** El mayor bloque de reglas D; mezcla piezas ya demostrables por FK y piezas que exigen triggers y funciones.
- **Alternativas:** A) Aceptar todo G-5 de una vez. B) Aceptar por bloques: (1) aprobación positiva (DG-20), (2) par evaluado y cadena de evaluaciones, (3) contribuyentes (DT-01/PC-02), (4) elegibilidad R1–R9. C) Posponer G-5 a Fase 1.
- **Recomendación técnica:** B: aceptar por bloques en ese orden; no declarar G-5 cerrado hasta validar el bloque 4 en CCI-DEV.
- **Justificación:** Los bloques 1–2 ya se demuestran en prototipo local (EX-T78, EX-T137..T140, EX-DG20); el 3–4 dependen de tablas y funciones inexistentes.
- **Impactos:** funcional — Evaluación de impacto con independencia verificable. · datos — 5 tablas nuevas de contribución/atribución. · seguridad/integridad — Elegibilidad R1–R9 con falla cerrada; aprobación sin INSERT directo. · migración — Por subfases; el bloque 3 requiere decidir la representación física. · compatibilidad — Sin cambios en 17 claves ni 13 transiciones (T-47: PASS estático).
- **Dependencias:** DG-20, DG-12, G-9, RP-01. · **Reversibilidad:** Media: las tablas de evidencia son inmutables por diseño; corregir exige tablas/versiones nuevas.
- **Pruebas necesarias:** PLAN_VALIDACION_TRIGGER_R1_R9.md; K47 físico (ATR); CONC-03/04.
- **Evidencia local de este cierre:** EX-T78, EX-T80, EX-T10, EX-T137..T140b; CC-01.
- **Resuelto técnicamente vs. sólo propietario:** Técnicamente resuelto: orden de bloques y pruebas. Sólo propietario: aceptación y DT-01/DT-02.
- **Estado técnico:** `RECOMENDADO_REQUIERE_APROBACION` · **Estado de aprobación:** `REQUIERE_APROBACION_DEL_PROPIETARIO`
- **Decisión requerida del propietario:** Aceptar el orden por bloques y decidir DT-01/DT-02.

## G-10 — Registro de intentos de publicación e idempotencia (IG10, 26 reglas clase D)

- **Fuente original:** ESPECIFICACION_TECNICA_G1_G5_G10.md §5 (línea 2824) y línea 5025
- **Texto original recuperado:** «Registro e idempotencia con comportamiento de fallo honesto: db_txid con mecanismo PostgreSQL concreto, guarda de ocho condiciones, ruta única de publicación, política única de correlation_id y cuatro escenarios» (línea 5025).
- **Problema:** 26 reglas D sin implementación; dependen de DG-09 y DG-12 (diferidas).
- **Alternativas:** A) Aceptar sin hash ni retención (como está). B) Aceptar y exigir DG-12 antes de Fase 1. C) Rediseñar con cola externa.
- **Recomendación técnica:** A: aceptar tal cual, con DG-09/DG-12 explícitamente diferidas y CONC-06 como prueba obligatoria.
- **Justificación:** El diseño declara fallo honesto y no depende del hash; la idempotencia se valida con UNIQUE/fingerprint (prueba física pendiente).
- **Impactos:** funcional — Publicación con registro de intentos. · datos — Tabla publication_attempts. · seguridad/integridad — Guarda de 8 condiciones; sin escritura directa. · migración — Aditiva en la subfase de publicación. · compatibilidad — Compatible.
- **Dependencias:** DG-09, DG-12, G-5. · **Reversibilidad:** Media.
- **Pruebas necesarias:** CONC-06; pruebas_guarda físico; privilegios.
- **Evidencia local de este cierre:** Modelo en memoria: pruebas_guarda 9/9, atomicidad 20+11+8.
- **Resuelto técnicamente vs. sólo propietario:** Técnico: resuelto como diseño. Propietario: aceptar.
- **Estado técnico:** `RECOMENDADO_REQUIERE_APROBACION` · **Estado de aprobación:** `REQUIERE_APROBACION_DEL_PROPIETARIO`
- **Decisión requerida del propietario:** Aceptar o rechazar el diseño de G-10.

## DG-19 — Catálogo de canales y formatos (channel_rules + channel_formats)

- **Fuente original:** ESPECIFICACION_TECNICA_G1_G5_G10.md líneas 280, 332–345, 401–402, 4785
- **Texto original recuperado:** «Recomendación técnica única: channel_rules más la tabla channel_formats desde la subfase 1.8 (3.14)… RESUELTA técnicamente; sujeta a tu aceptación porque adelanta channel_rules y suma una tabla (32). Los valores reales… siguen PENDIENTES de la organización; no se inventan.»
- **Problema:** Falta PK, la normalización vigente (lower+btrim) deja pasar TAB/NBSP, y los valores iniciales no existen.
- **Alternativas:** A) PK sustituta `id uuid` + UNIQUE(org,canal,formato). B) PK natural (organization_id, channel, format). C) Dejar sólo UNIQUE (sin PK).
- **Recomendación técnica:** B: PRIMARY KEY (organization_id, channel, format). Normalización: CHECK `format ~ '^[a-z0-9_]{1,40}$'` (igual para canal) **si** el propietario confirma el alfabeto permitido (p. ej. ¿guion, tildes?). Valores iniciales: ninguno (la organización los registra con org.manage).
- **Justificación:** La clave es inmutable (trigger CANAL_FORMATO_INMUTABLE) y es la referencia de las FK compuestas de creative_pieces; una PK natural evita una columna y un índice redundantes. Probado: sustituir UNIQUE por PK mantiene 63/63 (ct_dg19_pk_experimento.sh).
- **Impactos:** funcional — Sin filas no se crean piezas (IG1-32). · datos — Tabla nueva; sin valores iniciales. · seguridad/integridad — Mejora la normalización; el CHECK actual admite 'reel<TAB>' (EX-DG19a/b). · migración — Aditiva en 1.8. · compatibilidad — Compatible con las FK de creative_pieces (misma tripleta).
- **Dependencias:** G-1; IG1-30..33. · **Reversibilidad:** Alta antes de datos; baja después (cambiar PK con FK dependientes).
- **Pruebas necesarias:** PG-CF-01..15 sobre el esquema físico; EX-DG19c/d; inventario INV-03.
- **Evidencia local de este cierre:** dg19_pk_experimento 63/63; EX-DG19a..d PASS.
- **Resuelto técnicamente vs. sólo propietario:** Técnico: estructura, PK y normalización (resuelto). Sólo propietario/organización: aceptar DG-19, alfabeto permitido y los canales y formatos reales (PENDIENTE DE INFORMACIÓN EXTERNA, no se inventan).
- **Estado técnico:** `RECOMENDADO_REQUIERE_APROBACION` · **Estado de aprobación:** `REQUIERE_APROBACION_DEL_PROPIETARIO`
- **Decisión requerida del propietario:** Aceptar DG-19; confirmar alfabeto de canal/formato; la organización entrega el catálogo real.

## DG-20 — Columna approvals.decision con CHECK = 'aprobada'

- **Fuente original:** ESPECIFICACION_TECNICA_G1_G5_G10.md líneas 127, 2778, 3646, 4786
- **Texto original recuperado:** «Campo approvals.decision; text; un único valor, `aprobada`. El rechazo no es un valor porque no se almacena en approvals… NOT NULL; CHECK (decision = 'aprobada')… approvals nace en 6.5 con la columna: no hay filas históricas que migrar.» Línea 127: el rechazo (T-02 #8), la solicitud de cambios (#4, #6) y el registro de revisión (#3) NO se guardan en approvals: son transiciones con comentario o motivo (comments y activity_logs).
- **Problema:** v3.3 describe approvals como «decisión humana sobre versión exacta» sin distinguir aprobación de rechazo (RR-17); sin discriminador, C2/C3 dependen de una convención del escritor.
- **Alternativas:** A) Ampliación mínima propuesta (decision con CHECK único valor). B) No añadir columna; confiar en la convención «toda fila es aprobación». C) Columna decision con valores {aprobada, rechazada} y guardar rechazos en approvals.
- **Recomendación técnica:** A, con una condición de verificación: confirmar que el rechazo vive sólo en transiciones+comments/activity_logs (v3.3 lo respalda: T-02 «Pendiente de aprobación→Rechazado, motivo obligatorio»). Alinear el nombre `decided_by` (v3.3) con la columna del fixture (`approver`).
- **Justificación:** Semántica inequívoca (un valor), compatible con el flujo T-02 (13 transiciones sin cambio), integridad por NOT NULL+CHECK+unique(org,id,copy_version_id), migración segura (la tabla nace con la columna), sin contradicción con estados existentes (rechazo no se almacena aquí). Pruebas: EX-DG20a..h PASS; EX-T78d prueba que sin CHECK una FK admite citar una fila con otro valor.
- **Impactos:** funcional — Aprobación positiva inequívoca para C2/C3. · datos — 1 columna NOT NULL. · seguridad/integridad — Evita aprobaciones ambiguas; no sustituye el trigger de independencia. · migración — Sin migración de datos si se crea en 6.5; EX-DG20f/g muestran la ruta si ya hubiera filas (DEFAULT + CHECK). · compatibilidad — Compatible con los estados; no cambia permisos.
- **Dependencias:** G-5; T-78. · **Reversibilidad:** Alta si no hay filas; media si las hay.
- **Pruebas necesarias:** EX-DG20a..h repetidas sobre el esquema físico; prueba de record_approval y de que ningún rol inserta directo.
- **Evidencia local de este cierre:** EX-DG20a..h (8/8 PASS).
- **Resuelto técnicamente vs. sólo propietario:** Técnico: resuelto (análisis y pruebas). Sólo propietario: aprobar la ampliación (orientación inicial del propietario: mantenerla; no se marca aprobada).
- **Estado técnico:** `RECOMENDADO_REQUIERE_APROBACION` · **Estado de aprobación:** `REQUIERE_APROBACION_DEL_PROPIETARIO`
- **Decisión requerida del propietario:** Aprobar o rechazar la ampliación mínima; confirmar que los rechazos no se almacenan en approvals.

## DG-09 — Política de retención de datos

- **Fuente original:** ESPECIFICACION_TECNICA_G1_G5_G10.md línea 40, 2955, 3002, 4768
- **Texto original recuperado:** «Retención de 24 meses | DIFERIDA; no se habilita borrado desde la aplicación y no se inventa política | 5.7 y IG10-18; se eliminó el plazo de la v1.» IG10-18: «Sin borrado desde la aplicación; no se define política de retención.»
- **Problema:** No hay política de retención; el diseño la deja diferida. El plazo de 24 meses de la v1 se eliminó y no debe reintroducirse sin decisión.
- **Alternativas:** A) Mantener diferida (sin borrado ni purga). B) Definir plazos por categoría (operativa, auditoría, evidencia) con base legal. C) Retención indefinida con exportación periódica.
- **Recomendación técnica:** A hasta que el propietario y quien corresponda legalmente fijen la política; mientras tanto documentar que no hay purga automática. Para B: la estructura técnica (columna `retention_until` o job de archivado) se diseña **después** del plazo, no antes.
- **Justificación:** Un plazo legal no es una decisión técnica y no hay fuente en el expediente; inventarlo sería fabricar un requisito.
- **Impactos:** funcional — Sin borrado ni archivo. · datos — Crecimiento indefinido de tablas inmutables. · seguridad/integridad — Evita pérdida accidental; no resuelve privacidad ni cumplimiento. · migración — Ninguna. · compatibilidad — Compatible.
- **Dependencias:** DEP-RET-01; P-09 (v3.3). · **Reversibilidad:** Alta.
- **Pruebas necesarias:** N/A hasta que exista política.
- **Evidencia local de este cierre:** Ninguna (no hay política que probar).
- **Resuelto técnicamente vs. sólo propietario:** NO resoluble técnicamente: depende de política y base legal. Técnico: documentar el límite.
- **Estado técnico:** `PENDIENTE_DE_INFORMACION_EXTERNA` · **Estado de aprobación:** `REQUIERE_APROBACION_DEL_PROPIETARIO`
- **Decisión requerida del propietario:** Definir la política de retención (plazos y base legal) o mantenerla diferida.

## DEP-RET-01 — Dependencia de retención: retiro de contenido externo al reemplazar una pieza

- **Fuente original:** ESPECIFICACION_TECNICA_G1_G5_G10.md líneas 3182, 3193, 3399
- **Texto original recuperado:** «No existe procedimiento operativo documentado, ni responsable, para retirar contenido externo cuando una pieza se reemplaza. Se identifica como dependencia; no se inventa un estado ni una transición.»
- **Problema:** Archivar una pieza en CCI no retira el contenido publicado en canales externos.
- **Alternativas:** A) Procedimiento operativo manual con responsable. B) Integración técnica con los canales. C) Aceptar la limitación.
- **Recomendación técnica:** Resolver DG-09 y designar responsable (RP-01 o equivalente) antes de decidir A/B; no añadir estados ni transiciones.
- **Justificación:** Sin política de retención ni responsable no hay base para un procedimiento.
- **Impactos:** funcional — Ninguno por ahora. · datos — Ninguno. · seguridad/integridad — Riesgo operativo: contenido obsoleto visible externamente. · migración — Ninguna. · compatibilidad — Compatible.
- **Dependencias:** DG-09, RP-01. · **Reversibilidad:** Alta.
- **Pruebas necesarias:** N/A.
- **Evidencia local de este cierre:** Ninguna.
- **Resuelto técnicamente vs. sólo propietario:** NO resoluble en Fase 0.
- **Estado técnico:** `NO_RESOLUBLE_EN_FASE_0` · **Estado de aprobación:** `REQUIERE_APROBACION_DEL_PROPIETARIO`
- **Decisión requerida del propietario:** Definir procedimiento y responsable.

## DG-12 — Hash encadenado de registros

- **Fuente original:** ESPECIFICACION_TECNICA_G1_G5_G10.md líneas 40, 3004, 3557, 4771
- **Texto original recuperado:** «DIFERIDA a la subfase 6.6; no es requisito del cierre del diseño actual.» Mitigación frente a un superusuario de la plataforma: «el hash encadenado opcional y la exportación periódica (DG-12, RR-04).»
- **Problema:** Sin hash, un superusuario de la plataforma puede alterar registros inmutables sin rastro; además el sello actual del fixture usa `concat_ws('|',…)`, que es ambiguo (DEF-DG12-01).
- **Alternativas:** A) Mantener diferido. B) Hash por registro (sello) con serialización canónica. C) Hash encadenado completo con ancla externa.
- **Recomendación técnica:** Diseño de referencia para 6.6 (no aprobado): SHA-256 sobre `versión_formato || hash_previo(32 bytes) || JSON canónico UTF-8` (claves ordenadas, sin espacios, NFC, nulls explícitos, timestamps ISO-8601 UTC con microsegundos y sufijo Z, sin floats), versión de formato como prefijo, génesis = 32 bytes cero, y **ancla externa** del último hash (exportación periódica) para detectar truncamiento. **Corregir ya** el sello del fixture a serialización no ambigua.
- **Justificación:** El defecto de colisión por separador es reproducible (EX-DG12a/b: PASS = colisión confirmada); la serialización JSON no colisiona (EX-DG12c). La implementación de referencia detecta modificación, borrado, reordenamiento e inserción (HC-06..HC-09) y coincide con pgcrypto (HC-16).
- **Impactos:** funcional — Evidencia de integridad verificable. · datos — Columnas `prev_hash`, `row_hash`, `hash_version` en las tablas de evidencia. · seguridad/integridad — Detección de manipulación; no la previene. · migración — Aditiva (columnas); el backfill de registros previos debe decidirse. · compatibilidad — Compatible con tablas inmutables.
- **Dependencias:** G-5, G-10, 6.6. · **Reversibilidad:** Media: el formato versionado permite evolucionar (v2) sin invalidar v1.
- **Pruebas necesarias:** HC-01..HC-16 (local); en CCI-DEV: verificación de cadena sobre datos reales y prueba de manipulación como superusuario de PRUEBA.
- **Evidencia local de este cierre:** ct_hash_cadena_referencia.py 16/16; EX-DG12a..c.
- **Resuelto técnicamente vs. sólo propietario:** Técnico: diseño de referencia resuelto. Propietario: aprobar el alcance (qué tablas, cuándo) y DG-12 sigue diferida.
- **Estado técnico:** `RECOMENDADO_REQUIERE_APROBACION` · **Estado de aprobación:** `REQUIERE_APROBACION_DEL_PROPIETARIO`
- **Decisión requerida del propietario:** Decidir si DG-12 se adelanta; aprobar el formato canónico versionado; confirmar la ancla externa.

## DG-16 — Umbrales de texto (30 y 10 caracteres) y T-03

- **Fuente original:** ESPECIFICACION_TECNICA_G1_G5_G10.md líneas 187, 426, 481, 4775
- **Texto original recuperado:** «DIFERIDA hasta resolver T-03; 30 y 10 caracteres son propuestas pendientes, no aprobadas | Se retiraron todos los CHECK de longitud mínima (solo no vacío).»
- **Problema:** La restricción vigente es «no vacío» y se implementa con btrim, que sólo recorta espacios U+0020: un texto de TAB, NBSP o ZWSP pasa (EX-DG16b/c/d; DEF-01). Los umbrales 30/10 son propuestas sin decisión.
- **Alternativas:** A) Mantener sólo «no vacío» (corregido). B) Adoptar 30/10 en caracteres significativos. C) Otros umbrales.
- **Recomendación técnica:** 1) Corregir ahora la definición de «no vacío» a «contiene al menos un carácter significativo» (regex que excluya espacios Unicode, NBSP y caracteres de ancho cero): técnicamente resuelto. 2) Si el propietario adopta umbrales: medir **caracteres significativos** (no bytes), con fronteras N−1 rechaza y N acepta; 30 para justificación y 10 para motivo sólo si lo decide el propietario (decisión de negocio faltante).
- **Justificación:** EX-DG16e..h (no vacío robusto) y EX-DG16n..r (frontera 29/30, 30 TAB, relleno con NBSP) PASS en UTF8.
- **Impactos:** funcional — Calidad mínima de justificaciones. · datos — CHECK sobre columnas de texto. · seguridad/integridad — Evita justificaciones vacías disfrazadas. · migración — Aditiva; filas existentes deben cumplir. · compatibilidad — Compatible.
- **Dependencias:** T-03, IP-05, IG5-09. · **Reversibilidad:** Alta (CHECK se puede reemplazar).
- **Pruebas necesarias:** EX-DG16a..r sobre el esquema físico en UTF8.
- **Evidencia local de este cierre:** EX-DG16a..r (18/18 PASS en UTF8; 2 FAIL esperables en SQL_ASCII, ver informe).
- **Resuelto técnicamente vs. sólo propietario:** Técnico: corrección de «no vacío» resuelta; umbrales: decisión de negocio faltante.
- **Estado técnico:** `RECOMENDADO_REQUIERE_APROBACION` · **Estado de aprobación:** `REQUIERE_APROBACION_DEL_PROPIETARIO`
- **Decisión requerida del propietario:** Decidir si se adoptan los umbrales 30/10 y cerrar T-03.

## DG-18 — Columna opcional replaces_piece_id

- **Fuente original:** ESPECIFICACION_TECNICA_G1_G5_G10.md líneas 117, 3191, 4784
- **Texto original recuperado:** «replaces_piece_id uuid NULL (opcional, sujeto a DG-18). Pieza anterior que esta pieza nueva reemplaza comercialmente (DG-15). Inmutable, FK compuesta, no autorreferente. Sin ella el diseño funciona; solo se pierde la trazabilidad estructural del reemplazo.»
- **Problema:** Decidir si se guarda estructuralmente el reemplazo comercial.
- **Alternativas:** A) No añadirla. B) Añadir columna nullable inmutable con FK compuesta y CHECK anti-autorreferencia. C) Tabla de historial de reemplazos (múltiples).
- **Recomendación técnica:** B: `replaces_piece_id uuid NULL`, FK (organization_id, replaces_piece_id) → creative_pieces(organization_id, id) ON DELETE RESTRICT, CHECK (replaces_piece_id IS DISTINCT FROM id), trigger de inmutabilidad. Un reemplazo por pieza (columna única); varias piezas pueden reemplazar la misma (fan-in), sin UNIQUE. Si se exige que la reemplazada esté Publicada/Archivada, añadir trigger (la FK no lo garantiza).
- **Justificación:** Probado: autorreferencia 23514, inexistente 23503, otra organización 23503, UPDATE/anulación P0001, ciclo imposible por inmutabilidad (EX-DG18f), DELETE de la reemplazada 23503; límites documentados (fan-in, sin condición de estado).
- **Impactos:** funcional — Trazabilidad de reemplazo. · datos — 1 columna NULL. · seguridad/integridad — Integridad por FK compuesta; sin riesgo nuevo. · migración — Aditiva. · compatibilidad — Compatible con T-63; no cambia T-02.
- **Dependencias:** G-1, DG-15. · **Reversibilidad:** Alta (columna opcional).
- **Pruebas necesarias:** EX-DG18a..i en el esquema físico; T-63.
- **Evidencia local de este cierre:** EX-DG18a..i (9/9 PASS).
- **Resuelto técnicamente vs. sólo propietario:** Técnico: diseño y pruebas. Propietario: aprobar o no la columna.
- **Estado técnico:** `RECOMENDADO_REQUIERE_APROBACION` · **Estado de aprobación:** `REQUIERE_APROBACION_DEL_PROPIETARIO`
- **Decisión requerida del propietario:** Aprobar o rechazar la columna; decidir si la reemplazada debe estar Publicada.

## G-9 — Historial de revisor asignado (piece_reviewer_assignments)

- **Fuente original:** ESPECIFICACION_TECNICA_G1_G5_G10.md líneas 415, 2309, 4766
- **Texto original recuperado:** «Historial inmutable de quién es el revisor asignado de una pieza o adaptación… quién puede registrarla sigue en G-9 (abierto): el modelo no comprueba esa autoridad y el diseño no la presupone.» DG-07: «Cierra solo la asignación de revisor: G-9 completo sigue abierto.»
- **Problema:** Falta decidir la autoridad que registra la asignación y el modelo de historial con vigencia.
- **Alternativas:** A) Fila por asignación con `assigned_at` y `unassigned_at` (sin exclusión). B) Rango de vigencia `tstzrange` con EXCLUDE por pieza (un revisor vigente a la vez). C) Permitir varios revisores simultáneos.
- **Recomendación técnica:** B con 1 revisor vigente por pieza: columnas id, organization_id, piece_id, reviewer_id, assigned_by, valid_during tstzrange (inicio inclusivo, fin exclusivo, no vacío), reason; EXCLUDE USING gist (organization_id, piece_id, valid_during &&); trigger: no DELETE, no cambiar campos, sólo cerrar el rango abierto; reasignación = cerrar + abrir contigua. Validar además membresía activa y permiso piece.review por trigger (la FK no lo hace: EX-G9j).
- **Justificación:** Probado: solapamiento 23P01, contigua OK, independencia por pieza, DELETE/UPDATE bloqueados, rango vacío rechazado, FK a membresía, y concurrencia real (CC-01: B espera ≈2 s y falla 23P01).
- **Impactos:** funcional — Ejecutor identificable de la evaluación y de la independencia. · datos — Tabla nueva con historial. · seguridad/integridad — Auditoría completa; falta decidir quién puede asignar. · migración — Aditiva (requiere btree_gist: verificar disponibilidad en CCI-DEV). · compatibilidad — Compatible con DG-07.
- **Dependencias:** G-5, R2/R9, RP-01. · **Reversibilidad:** Media.
- **Pruebas necesarias:** EX-G9a..j, CC-01 sobre el esquema físico; privilegios de quién inserta.
- **Evidencia local de este cierre:** EX-G9a..j (10/10 PASS), CC-01 PASS.
- **Resuelto técnicamente vs. sólo propietario:** Técnico: modelo resuelto. Sólo propietario: autoridad que asigna (org.manage u otra) y aceptación de G-9.
- **Estado técnico:** `RECOMENDADO_REQUIERE_APROBACION` · **Estado de aprobación:** `REQUIERE_APROBACION_DEL_PROPIETARIO`
- **Decisión requerida del propietario:** Definir quién puede registrar asignaciones y aceptar G-9.

## RP-01 — Responsable administrativo del nivel 3

- **Fuente original:** REGISTRO_HISTORICO_VERSIONES.md líneas 110, 117–118, 127
- **Texto original recuperado:** «Designar al responsable administrativo del nivel 3 con identidad real» (pendiente del propietario); «Responsable administrativo del nivel 3 (pendiente) | Designación de una persona responsable por el propietario.»
- **Problema:** Falta designar a una persona; técnicamente sólo se puede definir el perfil.
- **Alternativas:** A) Una persona con perfil definido. B) Rol compartido por dos personas (principio de separación). C) Dejar el nivel 3 sin responsable.
- **Recomendación técnica:** Perfil (sin nombres): persona con membresía activa, capaz de acceder a CCI-PROD sólo mediante procedimientos aprobados, sin ser autora de las piezas que aprueba; responsabilidades: custodiar credenciales de nivel 3, autorizar cambios de privilegios y migraciones, aprobar restauraciones, firmar la verificación de accesos; poderes: conceder `org.manage`, no puede aprobar piezas que contribuyó (IG5-95: el cargo no otorga independencia). Recomendar un suplente.
- **Justificación:** Es el único criterio técnico defendible sin inventar identidades ni canales.
- **Impactos:** funcional — Define quién puede operar el nivel 3. · datos — Ninguno. · seguridad/integridad — Evita acumulación de poder en una sola persona. · migración — Ninguna. · compatibilidad — Compatible con D-04/D-08.
- **Dependencias:** P-04, G-9. · **Reversibilidad:** Alta.
- **Pruebas necesarias:** Revisión de accesos en CCI-DEV (PRIV-06).
- **Evidencia local de este cierre:** Ninguna (decisión de personas).
- **Resuelto técnicamente vs. sólo propietario:** Técnico: perfil recomendado. NO se designa a nadie.
- **Estado técnico:** `RECOMENDADO_REQUIERE_APROBACION` · **Estado de aprobación:** `REQUIERE_APROBACION_DEL_PROPIETARIO`
- **Decisión requerida del propietario:** Designar a la persona (nombre real) y, si procede, un suplente.

## P-01 — Organización y proyecto de Supabase propios

- **Fuente original:** Fase 0 v3.3 §9 (línea 329)
- **Texto original recuperado:** «Organización y proyecto de Supabase propios | D-01/D-02: no mezclar con RevNavigator | bloquea 1.4, 1.7, 1.8 | Tu creación o autorización; sin credenciales en chat | No; bloquea Fase 1».
- **Problema:** Hay que mantener CCI-DEV y CCI-PROD como proyectos independientes y separados de RevNavigator.
- **Alternativas:** A) Dos proyectos (DEV y PROD) en una organización propia. B) Un proyecto con ramas. C) Reutilizar infraestructura existente (descartado por D-01/D-02).
- **Recomendación técnica:** A: dos proyectos independientes; el propietario los crea o autoriza; credenciales sólo por canal seguro.
- **Justificación:** Coincide con D-01/D-02 y con las restricciones de este cierre.
- **Impactos:** funcional — Habilita Fase 1. · datos — Ninguno. · seguridad/integridad — Aislamiento total de RevNavigator. · migración — N/A. · compatibilidad — —
- **Dependencias:** P-02. · **Reversibilidad:** Alta.
- **Pruebas necesarias:** Confirmación de IDs de proyecto (P1 del plan CCI-DEV).
- **Evidencia local de este cierre:** Ninguna.
- **Resuelto técnicamente vs. sólo propietario:** Sólo propietario.
- **Estado técnico:** `PENDIENTE_DE_INFORMACION_EXTERNA` · **Estado de aprobación:** `REQUIERE_APROBACION_DEL_PROPIETARIO`
- **Decisión requerida del propietario:** Crear/autorizar la organización y los proyectos.

## P-02 — Repositorio de GitHub y visibilidad

- **Fuente original:** Fase 0 v3.3 §9 (línea 330)
- **Texto original recuperado:** «Repositorio de GitHub y visibilidad | Sin repositorio no hay código versionado | 1.1 | Nombre, propietario, visibilidad».
- **Problema:** Define dónde vive el código.
- **Alternativas:** Público vs privado.
- **Recomendación técnica:** Privado mientras haya diseño de seguridad sin publicar; el repositorio `appalex47-lab/Copy-Creative-Intelligence` ya existe y contiene la documentación de Fase 0.
- **Justificación:** El expediente contiene diseño interno; la visibilidad pública no aporta valor ahora.
- **Impactos:** funcional — — · datos — — · seguridad/integridad — Evita exposición del diseño. · migración — — · compatibilidad — —
- **Dependencias:** P-01. · **Reversibilidad:** Alta.
- **Pruebas necesarias:** —
- **Evidencia local de este cierre:** Ninguna.
- **Resuelto técnicamente vs. sólo propietario:** Recomendación técnica emitida; decisión del propietario.
- **Estado técnico:** `RECOMENDADO_REQUIERE_APROBACION` · **Estado de aprobación:** `REQUIERE_APROBACION_DEL_PROPIETARIO`
- **Decisión requerida del propietario:** Confirmar nombre, propietario y visibilidad.

## P-03 — Clave de prueba de Cohere

- **Fuente original:** Fase 0 v3.3 §9 (línea 331)
- **Texto original recuperado:** «Clave de prueba de Cohere | La IA se prueba con ella | Fase 2 | Clave cargada como secreto, nunca en chat».
- **Problema:** Credencial necesaria en Fase 2.
- **Alternativas:** Clave de prueba en secreto de Supabase vs variable de entorno local.
- **Recomendación técnica:** Cargar como secreto del servidor (Edge Function secret), nunca en el cliente ni en chat; Claude no la solicita.
- **Justificación:** Regla D-01 y las prohibiciones de este cierre.
- **Impactos:** funcional — Habilita IA en Fase 2. · datos — — · seguridad/integridad — Evita fuga de credenciales. · migración — — · compatibilidad — —
- **Dependencias:** P-01. · **Reversibilidad:** Alta.
- **Pruebas necesarias:** Revisión de secretos (sin credenciales en repositorio).
- **Evidencia local de este cierre:** Ninguna.
- **Resuelto técnicamente vs. sólo propietario:** Sólo propietario (entrega de credencial).
- **Estado técnico:** `PENDIENTE_DE_INFORMACION_EXTERNA` · **Estado de aprobación:** `REQUIERE_APROBACION_DEL_PROPIETARIO`
- **Decisión requerida del propietario:** Proveer la clave por canal seguro cuando llegue Fase 2.

## P-04 — Personas y roles (≥2 que puedan aprobar)

- **Fuente original:** Fase 0 v3.3 §9 (línea 332)
- **Texto original recuperado:** «Personas y roles (≥2 que puedan aprobar) | La separación de funciones exige dos personas | 1.5 recomendable, 6.5 necesario | Lista de personas y roles».
- **Problema:** Sin dos aprobadores distintos no hay separación de funciones (D-08).
- **Alternativas:** A) Dos o más personas reales. B) Una persona más un suplente externo.
- **Recomendación técnica:** Al menos dos personas con `piece.approve` y que no contribuyan a las versiones que aprueban; la lista la aporta el propietario.
- **Justificación:** Lo exige la independencia (IG5-95, D-08).
- **Impactos:** funcional — Habilita 6.5. · datos — — · seguridad/integridad — Separación de funciones. · migración — — · compatibilidad — —
- **Dependencias:** RP-01. · **Reversibilidad:** Alta.
- **Pruebas necesarias:** R1–R9 con personas reales de prueba.
- **Evidencia local de este cierre:** Ninguna.
- **Resuelto técnicamente vs. sólo propietario:** Sólo propietario (nombres).
- **Estado técnico:** `PENDIENTE_DE_INFORMACION_EXTERNA` · **Estado de aprobación:** `REQUIERE_APROBACION_DEL_PROPIETARIO`
- **Decisión requerida del propietario:** Entregar personas y roles.

## P-05 — Permisos individuales para conceder excepciones

- **Fuente original:** Fase 0 v3.3 §9 (línea 333)
- **Texto original recuperado:** «Permisos individuales para conceder excepciones | block.exception.grant es por persona | 6.5 | Quién puede, concedido con org.manage».
- **Problema:** Quién puede conceder excepciones a bloqueos.
- **Alternativas:** A) Pocas personas explícitas. B) Por rol.
- **Recomendación técnica:** A: lista mínima de personas, concedido con `org.manage`, con responsable y auditoría; sin concesión por cargo.
- **Justificación:** v3.3 define el permiso como individual.
- **Impactos:** funcional — Excepciones controladas. · datos — membership_permission_grants. · seguridad/integridad — Mínimo privilegio. · migración — — · compatibilidad — —
- **Dependencias:** RP-01, P-04. · **Reversibilidad:** Alta.
- **Pruebas necesarias:** Prueba de concesión y revocación con responsable.
- **Evidencia local de este cierre:** Ninguna.
- **Resuelto técnicamente vs. sólo propietario:** Sólo propietario (personas).
- **Estado técnico:** `PENDIENTE_DE_INFORMACION_EXTERNA` · **Estado de aprobación:** `REQUIERE_APROBACION_DEL_PROPIETARIO`
- **Decisión requerida del propietario:** Indicar quién puede conceder excepciones.

## P-10 — Dominio y hosting definitivos

- **Fuente original:** Fase 0 v3.3 §9 (línea 338)
- **Texto original recuperado:** «Dominio y hosting definitivos | Limita la CSP y el despliegue | 9.8 | Tu decisión».
- **Problema:** Sin dominio no se fija la CSP definitiva.
- **Alternativas:** Decidir ahora vs en 9.8.
- **Recomendación técnica:** Diferir a 9.8 (no bloquea Fase 1); mientras tanto CSP restrictiva por defecto.
- **Justificación:** No afecta al esquema de datos.
- **Impactos:** funcional — Despliegue. · datos — — · seguridad/integridad — CSP. · migración — — · compatibilidad — —
- **Dependencias:** — · **Reversibilidad:** Alta.
- **Pruebas necesarias:** Revisión CSP en 9.8.
- **Evidencia local de este cierre:** Ninguna.
- **Resuelto técnicamente vs. sólo propietario:** Sólo propietario.
- **Estado técnico:** `PENDIENTE_DE_INFORMACION_EXTERNA` · **Estado de aprobación:** `REQUIERE_APROBACION_DEL_PROPIETARIO`
- **Decisión requerida del propietario:** Elegir dominio y hosting.

## OD-13 — Decisión original reservada OD-13

- **Fuente original:** REGISTRO_HISTORICO_VERSIONES.md línea 117; ESPEC línea 2564 (sólo menciones)
- **Texto original recuperado:** NO RECUPERABLE: el texto literal de OD-13 reside en la Adenda v9 (ADDENDUM_DECISIONES_PROPIETARIO_OD01_OD16.md, SHA-256 ccb1c546dfb62c1b…), que está FUERA del repositorio y no forma parte del expediente. Las fuentes revisadas sólo la listan como pendiente.
- **Problema:** No puede analizarse una decisión cuyo texto no está disponible.
- **Alternativas:** —
- **Recomendación técnica:** Aportar la Adenda v9 (o la página de OD-13) para analizarla; no se infiere el contenido.
- **Justificación:** Inventar su texto violaría la regla de no fabricar evidencia.
- **Impactos:** funcional — Desconocido. · datos — Desconocido. · seguridad/integridad — Desconocido. · migración — Desconocido. · compatibilidad — Desconocida.
- **Dependencias:** PO-05. · **Reversibilidad:** Desconocida.
- **Pruebas necesarias:** —
- **Evidencia local de este cierre:** Ninguna.
- **Resuelto técnicamente vs. sólo propietario:** NO se pudo analizar.
- **Estado técnico:** `PENDIENTE_DE_INFORMACION_EXTERNA` · **Estado de aprobación:** `REQUIERE_APROBACION_DEL_PROPIETARIO`
- **Decisión requerida del propietario:** Entregar la Adenda v9 y decidir OD-13.

## PO-05 — Aceptación de la Adenda v9

- **Fuente original:** MATRIZ_HV02_PO05_EVIDENCIA.md; ESPEC líneas 20–36
- **Texto original recuperado:** Adenda v9: «ESTADO: PREPARADO PARA ACEPTACIÓN FORMAL DEL PROPIETARIO. NO ACEPTADO. La aceptación (PO-05) corresponde exclusivamente al propietario.» (SHA-256 ccb1c546dfb62c1b). PO-05 es estable en v1–v9.
- **Problema:** Aceptar o devolver correcciones a la Adenda v9, que recoge PO-11 a PO-21.
- **Alternativas:** A) Aceptar tal cual. B) Aceptar con correcciones. C) Rechazar.
- **Recomendación técnica:** B o A **después** de revisar la Adenda v9 completa: la recomendación técnica es no aceptarla a ciegas, porque su texto no está en el expediente y las decisiones PO-11..PO-21 deben confirmarse una a una. Este cierre **no** la acepta ni sustituye al propietario.
- **Justificación:** Trazabilidad v1→v9 consistente y sin incoherencias salvo HV-02 (redacción histórica).
- **Impactos:** funcional — Cierre documental de Fase 0. · datos — — · seguridad/integridad — — · migración — — · compatibilidad — —
- **Dependencias:** HV-02, OD-13, RP-01. · **Reversibilidad:** Alta.
- **Pruebas necesarias:** —
- **Evidencia local de este cierre:** Matriz HV-02/PO-05 (V20).
- **Resuelto técnicamente vs. sólo propietario:** Sólo propietario.
- **Estado técnico:** `RECOMENDADO_REQUIERE_APROBACION` · **Estado de aprobación:** `REQUIERE_APROBACION_DEL_PROPIETARIO`
- **Decisión requerida del propietario:** Aceptar, aceptar con correcciones o rechazar la Adenda v9; confirmar que PO-05 se refiere hoy a v9.

## HV-02 — Línea 126 del registro histórico menciona «addendum v3» mientras PO-05 se refiere a v9

- **Fuente original:** MATRIZ_HV02_PO05_EVIDENCIA.md (hallazgo); REGISTRO_HISTORICO_VERSIONES.md línea 126
- **Texto original recuperado:** Registro histórico (línea 126): «Aceptación formal del addendum v3 (o correcciones)»; documentos vigentes: la Adenda v9 no está aceptada (PO-05).
- **Problema:** Referencia histórica desactualizada; no existe fuente primaria que declare que PO-05 hoy es v9.
- **Alternativas:** A) Dejar la línea como evidencia histórica y documentar la correspondencia. B) Editar la línea (descartado: alteraría evidencia).
- **Recomendación técnica:** A (ya aplicada en V20/V26): no editar; el propietario confirma la correspondencia PO-05 = Adenda v9. Consecuencia: HV-02 queda NO VERIFICABLE hasta esa confirmación.
- **Justificación:** La explicación histórica es consistente con las fuentes (la línea se redactó cuando la vigente era v3, commits 1134c3d/df5e227).
- **Impactos:** funcional — — · datos — — · seguridad/integridad — — · migración — — · compatibilidad — —
- **Dependencias:** PO-05. · **Reversibilidad:** Alta.
- **Pruebas necesarias:** —
- **Evidencia local de este cierre:** V20 HV-02/PO-05.
- **Resuelto técnicamente vs. sólo propietario:** Técnico: trazabilidad resuelta. Propietario: confirmar.
- **Estado técnico:** `PENDIENTE_DE_INFORMACION_EXTERNA` · **Estado de aprobación:** `REQUIERE_APROBACION_DEL_PROPIETARIO`
- **Decisión requerida del propietario:** Confirmar que PO-05 se refiere a la Adenda v9 (SHA-256 ccb1c546…).

## Hallazgos nuevos que surgen del análisis de decisiones

| ID | Hallazgo | Evidencia | Decisión relacionada |
|---|---|---|---|
| DEF-01 | El «no vacío» basado en `btrim` acepta TAB, NBSP y ZWSP | EX-DG16b/c/d | DG-16 |
| DEF-DG12-01 | `concat_ws('|',…)` en el sello de resolución es ambiguo (separador y NULL) | EX-DG12a/b | DG-12 |
| DEF-DG19-01 | El CHECK de normalización de canal/formato deja pasar TAB/NBSP finales | EX-DG19a/b | DG-19 |
| DEF-NAME-01 | El fixture usa `approver`; v3.3 y la especificación usan `decided_by` | lectura (spec 2 apariciones de `decided_by`, 0 de `approver`) | DG-20 |
| DEF-ENV-01 | El clúster local inicial era SQL_ASCII: dos pruebas multibyte fallaban (EX-DG16f/g) hasta recrearlo en UTF8; Supabase usa UTF8 | resultados/ext_sqlascii.txt vs ext_utf8.txt | todas |
