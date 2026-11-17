# EXTRACCIÓN SELECTIVA LITERAL — entrega v2

Texto copiado sin resumir de `ESPECIFICACION_TECNICA_G1_G5_G10.md` e `INFORME_CIERRE_G1_G5_G10.md`. Cada bloque indica su archivo de origen y líneas. No se modificó ningún archivo original.



# PARTE 1.1 — Modelo de datos: tablas nuevas y cambios a existentes



---
<!-- ESPECIFICACION · líneas 103-184 · literal -->

### 3.4 Entidades y atributos

Ajustes a tablas existentes y tablas nuevas de G-1:

| Tabla o función | Cambio | Tipo de cambio | Detalle |
|---|---|---|---|
| creative_pieces | master_piece_id uuid NULL | Columna nueva | NULL = pieza que no es adaptación (puede ser una maestra con adaptaciones o una pieza sin ellas); NO NULL = adaptación (candidata o independiente). Inmutable una vez asignada |
| creative_pieces | is_adaptation boolean NOT NULL, generada como (master_piece_id IS NOT NULL) | Columna nueva (generada) | Sustituye al nombre «is_master» de la v1: una pieza con master_piece_id NULL no es necesariamente maestra. «Maestra» es un rol derivado: pieza que tiene al menos una adaptación |
| creative_pieces | master_ref_is_adaptation boolean, generada (false si master_piece_id no es NULL; NULL si lo es) | Columna nueva (generada) | Valor constante que permite la FK compuesta de un solo nivel (ver 3.4) |
| creative_pieces | channel text NOT NULL, format text NOT NULL | Columnas nuevas o ajuste | v3.3 dice «pieza por canal y formato» sin fijar columnas ni tipos. Tipo: texto normalizado (minúsculas, sin espacios en los extremos, no vacío, máximo 40 caracteres). No se inventa un catálogo de valores: los canales y formatos reales siguen pendientes (v3.3: reglas reales por canal sin entregar). Aplican a todas las piezas, no solo a adaptaciones |
| creative_pieces | adaptation_key text NOT NULL DEFAULT '' | Columna nueva | Normalizada (minúsculas; letras, dígitos, guion y guion bajo; máximo 40). Vacía en piezas sin maestra (CHECK). La clave vacía es la adaptación principal del canal y formato |
| creative_pieces | replaces_piece_id uuid NULL (opcional, sujeto a DG-18) | Columna nueva opcional | Pieza anterior que esta pieza nueva reemplaza comercialmente (DG-15). Inmutable, FK compuesta, no autorreferente. Sin ella el diseño funciona; solo se pierde la trazabilidad estructural del reemplazo |
| creative_pieces | unique(organization_id, id, is_adaptation) | Restricción | Destino de la FK compuesta de un solo nivel |
| creative_pieces | unique parcial (organization_id, master_piece_id, channel, format, adaptation_key) WHERE master_piece_id IS NOT NULL AND status <> Archivado | Restricción + índice | Impide dos adaptaciones activas con la misma clave en el mismo canal y formato; claves distintas sí conviven (DG-14). «Archivado» es el valor del enum de estados |
| creative_pieces | CHECK: master_piece_id <> id; (master_piece_id IS NOT NULL) OR adaptation_key = '' | Restricción | No autorreferencia; la clave solo tiene sentido en adaptaciones |
| copy_versions | master_piece_id, master_copy_version_id, master_creative_asset_id (las tres NULL en piezas sin maestra) | Columnas nuevas | uuid. Versión exacta de la maestra de la que deriva esta versión; inmutables porque copy_versions es inmutable |
| copy_versions | unique(organization_id, piece_id, id) | Restricción | Destino de FK compuestas desde adaptaciones, evaluaciones e intentos |
| creative_assets | unique(organization_id, piece_id, id, copy_version_id) | Restricción | Destino de la FK compuesta que valida que el arte acompaña a esa versión de copy |
| approvals | unique(organization_id, id, copy_version_id) | Restricción | Destino de FK compuestas desde impact_evaluations y publication_attempts. Si approvals también guarda rechazos, esas FK deben incluir una columna constante de decisión «aprobada»; v3.3 no fija ese nombre y debe confirmarse al diseñar 6.x |
| channel_rules | allowed_formats text[] NOT NULL (propuesta) | Columna nueva (se crea con la tabla en Fase 5) | v3.3 describe channel_rules como extensión, tono, estructura y CTA por canal, con una fila por organización y canal, sin formatos. Se propone una lista de formatos permitidos por canal; los valores reales siguen pendientes (DG-19) |
| channel_rules | unique(organization_id, channel) | Restricción (ya implícita: una fila por organización y canal) | Destino de la FK compuesta desde creative_pieces (organization_id, channel), agregada en la migración de la Fase 5 |
| transition_piece_status (función) | Ampliación de la rama «Publicado» | Ajuste de función existente | Incorpora C1 a C9, el registro del intento y el bloqueo de estado (ver 6) |
| role_permissions | — | Sin cambio | Las 17 claves físicas no cambian; ninguna operación nueva requiere una clave 18 |
| activity_logs | — | Sin cambio | Sigue siendo auditoría general; no es la fuente de verdad de los registros nuevos |

#### `piece_classification_events`

**Propósito:** Historial inmutable de la clasificación de una pieza con maestra: propuesta de independencia, confirmación o no confirmación, y reversión a variación interna. **Brecha:** G-1 (y G-4). **Fase propuesta:** 5.3. **Estado:** aprobada conceptualmente (DG-01), sujeta a la aceptación de esta especificación.

| Columna | Tipo | NULL | Descripción |
|---|---|---|---|
| id | uuid | NO | PK |
| organization_id | uuid | NO | Aislamiento |
| piece_id | uuid | NO | Pieza candidata o adaptación |
| seq | integer | NO | Orden por pieza, desde 1 |
| event_type | text | NO | propuesta \| confirmacion \| no_confirmada \| reversion |
| proposal_event_id | uuid | SÍ | Solo en confirmacion y no_confirmada: la propuesta que responden |
| actor_id | uuid | NO | Lo escribe el servidor con auth.uid() |
| justification | text | NO | Mínimo 30 caracteres (propuesta alineada con T-03, no aprobada) |
| created_at | timestamptz | NO | now() del servidor |

**Clave primaria:** `id`.

**Claves foráneas:**

| Columnas | Referencia | Borrado |
|---|---|---|
| (organization_id, piece_id) | creative_pieces(organization_id, id) | RESTRICT |
| (organization_id, actor_id) | memberships(organization_id, user_id) | RESTRICT |
| (organization_id, proposal_event_id) | piece_classification_events(organization_id, id) | RESTRICT |

**Restricciones únicas:**

- unique(organization_id, id)
- unique(piece_id, seq)
- unique(proposal_event_id) donde event_type IN ('confirmacion','no_confirmada')

**Restricciones CHECK:**

- event_type IN ('propuesta','confirmacion','no_confirmada','reversion')
- (event_type IN ('confirmacion','no_confirmada')) = (proposal_event_id IS NOT NULL)
- char_length(btrim(justification)) >= 30
- seq >= 1

**Índices:**

- (organization_id, piece_id, seq DESC)
- (organization_id, event_type, created_at DESC)

Claves foráneas e integridad de los ajustes a tablas existentes:

| Tabla | Restricción | Borrado | Nota |
|---|---|---|---|
| creative_pieces | (organization_id, master_piece_id) → creative_pieces(organization_id, id) | RESTRICT | Misma organización; maestra existente |
| creative_pieces | Un solo nivel: la maestra referenciada no puede ser una adaptación | — | FK compuesta (organization_id, master_piece_id, master_ref_is_adaptation) → creative_pieces(organization_id, id, is_adaptation): la columna hija vale «falso» cuando hay maestra (NULL si no la hay, y entonces la FK no aplica), de modo que solo se puede apuntar a una pieza cuyo is_adaptation sea falso. Opción B: trigger. Que PostgreSQL admita columnas generadas como destino y origen de esta FK **no está verificado**; se decide en 1.8 (T-09) y la prueba T-04 cubre ambas opciones |
| copy_versions | (organization_id, master_piece_id, master_copy_version_id) → copy_versions(organization_id, piece_id, id) | RESTRICT | La versión de origen existe y pertenece a esa maestra |
| copy_versions | (organization_id, master_piece_id, master_creative_asset_id, master_copy_version_id) → creative_assets(organization_id, piece_id, id, copy_version_id) | RESTRICT (MATCH SIMPLE) | El arte de origen acompaña a esa versión; se omite si no hay arte |
| copy_versions | CHECK: (master_piece_id IS NULL) = (master_copy_version_id IS NULL); el arte de origen exige versión de origen | — | Todo o nada |
| copy_versions | Trigger BEFORE INSERT: master_piece_id de la versión = master_piece_id de su pieza; la pieza debe tener maestra | — | Regla entre tablas que una FK no expresa (IG1-11) |
| creative_pieces | Trigger BEFORE UPDATE: master_piece_id inmutable; una maestra con adaptaciones no pasa a adaptación | — | IG1-06 e IG1-07 |
| creative_pieces | Trigger en #7 y #10: una pieza con maestra sin clasificación independiente vigente no avanza | — | IG1-16; se implementa dentro de transition_piece_status |


---
<!-- ESPECIFICACION · líneas 251-261 · literal -->

### 3.12 Resumen de cambios de G-1

| Tipo | Elementos |
|---|---|
| Tabla nueva | `piece_classification_events`; `piece_reviewer_assignments` (compartida con G-5) |
| Columnas nuevas | creative_pieces: master_piece_id, is_adaptation, master_ref_is_adaptation, channel, format, adaptation_key (y replaces_piece_id si se aprueba DG-18); channel_rules: allowed_formats; copy_versions: master_piece_id, master_copy_version_id, master_creative_asset_id |
| Relaciones nuevas | pieza → maestra (autorreferencia compuesta); versión → versión de maestra; versión → arte de maestra |
| Restricciones | CHECK de no autorreferencia y todo-o-nada; únicos compuestos; un único parcial de adaptaciones activas; triggers de inmutabilidad y coherencia |
| Índices | Los de 3.8 |
| Ajustes a existentes | unique compuestos en copy_versions, creative_assets, approvals; ampliación de transition_piece_status |


---
<!-- ESPECIFICACION · líneas 262-276 · literal -->

### 3.13 Canal, formato, identidad de la clave y revisión de G-1

| Requisito de la revisión | Resolución |
|---|---|
| Tipos de channel y format | Texto normalizado (minúsculas, sin espacios en los extremos, no vacío, máximo 40 caracteres) en `creative_pieces`, para todas las piezas. No se fija un catálogo: los canales y formatos reales siguen pendientes (v3.3: reglas reales por canal sin entregar) |
| Relación con channel_rules | v3.3 define channel_rules como una fila por organización y canal con extensión, tono, estructura y CTA; **no** tiene formatos. Se propone `allowed_formats` en channel_rules y una FK compuesta (organization_id, channel) desde creative_pieces; el formato se valida con un trigger contra `allowed_formats` (una FK no expresa pertenencia a un arreglo). La alternativa de una tabla de formatos por canal sería una quinta tabla y no se propone |
| Desfase de fases | creative_pieces nace en la Fase 1 y channel_rules en la 5: la FK se agrega en la migración de la Fase 5, tras cargar en channel_rules los canales que ya usen las piezas; antes de eso `channel` y `format` son texto normalizado sin FK |
| Identidad y unicidad de adaptation_key | Normalizada; vacía en piezas sin maestra; la vacía es la adaptación principal. Único parcial entre adaptaciones no archivadas del mismo (maestra, canal, formato, clave). Claves distintas conviven (DG-14); al archivar una adaptación su clave queda libre |
| Una sola jerarquía | FK compuesta con is_adaptation (o trigger), master_piece_id inmutable y una maestra con adaptaciones no pasa a adaptación |
| Integridad de la versión de origen | FK compuesta (organización, maestra, versión) hacia copy_versions; la versión de la adaptación no se puede apuntar a otra pieza ni a una versión inexistente |
| Arte de origen y su versión | FK compuesta con copy_version_id hacia creative_assets: el arte acompaña exactamente a esa versión |
| Organización | Todas las FK incluyen organization_id |
| Conservación histórica | RESTRICT, sin DELETE de la aplicación, versiones inmutables y archivo en lugar de borrado |
| Nombre is_master | **Se reemplaza por `is_adaptation`**: una pieza con master_piece_id NULL puede ser una maestra o una pieza sin adaptaciones, así que «is_master» describía mal su función. «Maestra» pasa a ser un rol derivado (pieza con al menos una adaptación) |


---
<!-- ESPECIFICACION · líneas 279-408 · literal -->

### 4.1 Modelo de datos

La evaluación es una **actividad de revisión** (PO-21 A), no un estado ni una transición. Se registra en `impact_evaluations`, que une exactamente: la versión evaluada de la adaptación (V-A) y su aprobación histórica, el par de versiones de la maestra (V-D, de la que derivó la adaptación, y V-B, la versión aprobada posterior) con su aprobación, el evaluador y la asignación que lo acredita, el resultado, la justificación, la evidencia, la fecha, la acción posterior y la cadena de reemplazo.

**Precisión propuesta a G-7 (DG-05):** la evaluación se hace sobre versiones **aprobadas** de la maestra, no sobre borradores. Mientras la maestra se corrige (T-02 #11) deja de estar aprobada y C3 ya bloquea; cuando se aprueba de nuevo, V-B queda definida y se evalúa V-D → V-B. Así el par es inmutable y no se evalúa un texto que luego cambiaría.

#### `piece_reviewer_assignments`

**Propósito:** Historial inmutable de quién es el revisor asignado de una pieza o adaptación; necesario para que la evaluación de impacto y la confirmación de independencia tengan un ejecutor identificable. **Brecha:** G-5 (dependencia) y parte de G-9. **Fase propuesta:** 5.3. **Estado:** aprobada conceptualmente (DG-01), sujeta a la aceptación de esta especificación.

| Columna | Tipo | NULL | Descripción |
|---|---|---|---|
| id | uuid | NO | PK |
| organization_id | uuid | NO | Aislamiento |
| piece_id | uuid | NO | Pieza o adaptación |
| seq | integer | NO | Orden por pieza |
| action | text | NO | asignado \| retirado |
| reviewer_id | uuid | NO | Persona asignada o retirada |
| assigned_by | uuid | NO | Quien registra; auth.uid() del servidor |
| reason | text | NO | Mínimo 10 caracteres (propuesta) |
| created_at | timestamptz | NO | now() del servidor |

**Clave primaria:** `id`.

**Claves foráneas:**

| Columnas | Referencia | Borrado |
|---|---|---|
| (organization_id, piece_id) | creative_pieces(organization_id, id) | RESTRICT |
| (organization_id, reviewer_id) | memberships(organization_id, user_id) | RESTRICT |
| (organization_id, assigned_by) | memberships(organization_id, user_id) | RESTRICT |

**Restricciones únicas:**

- unique(organization_id, id)
- unique(piece_id, seq)
- unique(organization_id, piece_id, id)
- unique(organization_id, piece_id, id, reviewer_id, action)

**Restricciones CHECK:**

- action IN ('asignado','retirado')
- char_length(btrim(reason)) >= 10
- seq >= 1

**Índices:**

- (organization_id, piece_id, seq DESC)
- (organization_id, reviewer_id, created_at DESC)

#### `impact_evaluations`

**Propósito:** Registro permanente e inmutable de cada evaluación humana de impacto de un cambio de la maestra sobre una versión aprobada de una adaptación independiente. **Brecha:** G-5. **Fase propuesta:** 5.4 y 6.5. **Estado:** aprobada conceptualmente (DG-01), sujeta a la aceptación de esta especificación.

| Columna | Tipo | NULL | Descripción |
|---|---|---|---|
| id | uuid | NO | PK |
| organization_id | uuid | NO | Aislamiento |
| adaptation_piece_id | uuid | NO | Adaptación evaluada |
| adaptation_copy_version_id | uuid | NO | Versión de copy de la adaptación evaluada |
| adaptation_creative_asset_id | uuid | SÍ | Arte de esa versión, si existe |
| adaptation_approval_id | uuid | NO | Aprobación histórica relacionada; no se modifica |
| master_piece_id | uuid | NO | Maestra (debe coincidir con la de la adaptación) |
| master_basis_copy_version_id | uuid | NO | Versión de la maestra de la que derivó la adaptación evaluada (V-D) |
| master_basis_creative_asset_id | uuid | SÍ | Arte de V-D, si existe |
| master_changed_copy_version_id | uuid | NO | Versión aprobada posterior de la maestra que se evalúa (V-B) |
| master_changed_creative_asset_id | uuid | SÍ | Arte de V-B, si existe |
| master_approval_id | uuid | NO | Aprobación de esa versión de la maestra |
| evaluator_id | uuid | NO | Persona evaluadora; auth.uid() del servidor |
| evaluator_assignment_id | uuid | NO | Asignación que acredita al evaluador como revisor asignado |
| evaluator_assignment_action | text | NO | Constante «asignado»: permite que la FK exija una fila de asignación, no de retiro |
| evaluator_review_permission_verified | boolean | NO | Constante verdadero: constancia de que la función comprobó piece.review (no es la garantía; lo es la función) |
| result | text | NO | sin_impacto_material \| requiere_revision \| invalida \| desconocido |
| follow_up_action | text | NO | Acción posterior determinada por el resultado |
| justification | text | NO | Mínimo 30 caracteres |
| dimension_findings | jsonb | NO | Siete dimensiones evaluadas (evidencia mínima) |
| unknown_reason | text | SÍ | Obligatoria si el resultado es desconocido |
| evidence_refs | jsonb | SÍ | Referencias adicionales (comentarios, auditorías, artes) por tipo e id |
| kind | text | NO | inicial \| segunda_evaluacion \| correccion |
| supersedes_evaluation_id | uuid | SÍ | Evaluación que esta reemplaza en vigencia, sin borrarla |
| correction_reason | text | SÍ | Obligatoria si kind no es inicial |
| evaluated_at | timestamptz | NO | now() del servidor |
| correlation_id | uuid | NO | Correlación de la operación |
| idempotency_key | text | NO | Evita duplicar la operación |

**Clave primaria:** `id`.

**Claves foráneas:**

| Columnas | Referencia | Borrado |
|---|---|---|
| (organization_id, adaptation_piece_id) | creative_pieces(organization_id, id) | RESTRICT |
| (organization_id, adaptation_piece_id, adaptation_copy_version_id) | copy_versions(organization_id, piece_id, id) | RESTRICT |
| (organization_id, adaptation_piece_id, adaptation_creative_asset_id, adaptation_copy_version_id) | creative_assets(organization_id, piece_id, id, copy_version_id) | RESTRICT (MATCH SIMPLE: se omite si el arte es NULL) |
| (organization_id, adaptation_approval_id, adaptation_copy_version_id) | approvals(organization_id, id, copy_version_id) | RESTRICT |
| (organization_id, master_piece_id, master_basis_copy_version_id) | copy_versions(organization_id, piece_id, id) | RESTRICT |
| (organization_id, master_piece_id, master_changed_copy_version_id) | copy_versions(organization_id, piece_id, id) | RESTRICT |
| (organization_id, master_approval_id, master_changed_copy_version_id) | approvals(organization_id, id, copy_version_id) | RESTRICT |
| (organization_id, evaluator_id) | memberships(organization_id, user_id) | RESTRICT |
| (organization_id, adaptation_piece_id, evaluator_assignment_id, evaluator_id, evaluator_assignment_action) | piece_reviewer_assignments(organization_id, piece_id, id, reviewer_id, action) | RESTRICT |
| (organization_id, supersedes_evaluation_id) | impact_evaluations(organization_id, id) | RESTRICT |

**Restricciones únicas:**

- unique(organization_id, id)
- unique(organization_id, evaluator_id, idempotency_key)
- unique(supersedes_evaluation_id) donde no es NULL
- unique parcial de raíz por par: (adaptation_piece_id, adaptation_copy_version_id, COALESCE(adaptation_creative_asset_id, uuid nulo), master_basis_copy_version_id, COALESCE(master_basis_creative_asset_id, uuid nulo), master_changed_copy_version_id, COALESCE(master_changed_creative_asset_id, uuid nulo)) donde supersedes_evaluation_id IS NULL

**Restricciones CHECK:**

- result IN ('sin_impacto_material','requiere_revision','invalida','desconocido')
- follow_up_action coherente con result: sin_impacto_material -> conservar_aprobacion; requiere_revision o invalida -> nueva_version_y_workflow; desconocido -> evaluacion_humana_pendiente
- (kind = 'inicial') = (supersedes_evaluation_id IS NULL)
- kind IN ('inicial','segunda_evaluacion','correccion')
- kind = 'inicial' OR char_length(btrim(correction_reason)) >= 30
- char_length(btrim(justification)) >= 30
- result <> 'desconocido' OR char_length(btrim(unknown_reason)) >= 30
- las dos versiones de la maestra son distintas (copia o arte)
- dimension_findings válido según la función validadora (siete dimensiones; coherencia con result)
- evaluator_assignment_action = 'asignado'
- evaluator_review_permission_verified = true

**Índices:**

- (organization_id, adaptation_piece_id, adaptation_copy_version_id)
- (organization_id, master_piece_id, master_changed_copy_version_id)
- (organization_id, evaluator_id, evaluated_at DESC)
- (organization_id, result, evaluated_at DESC)


---
<!-- ESPECIFICACION · líneas 553-630 · literal -->

### 5.1 Modelo de datos

#### `publication_attempts`

**Propósito:** Registro permanente e inmutable de cada intento de publicación (permitido o bloqueado) con el resultado de cada condición C1 a C9. **Brecha:** G-10. **Fase propuesta:** 6.1, 6.6 y 2.7. **Estado:** aprobada conceptualmente (DG-01), sujeta a la aceptación de esta especificación.

| Columna | Tipo | NULL | Descripción |
|---|---|---|---|
| id | uuid | NO | PK |
| organization_id | uuid | NO | Aislamiento |
| correlation_id | uuid | NO | Correlación de la solicitud: la envía el cliente (formato uuid validado) o la genera el servidor; no es única ni se usa como clave |
| idempotency_key | text | NO | Obligatoria en la solicitud |
| actor_id | uuid | NO | auth.uid(); nunca un parámetro |
| actor_publish_permission | boolean | NO | Si tenía piece.publish en el instante del intento |
| attempted_at | timestamptz | NO | now() del servidor |
| piece_id | uuid | NO | Pieza o adaptación que se intentó publicar |
| piece_kind | text | NO | sin_relacion \| maestra \| adaptacion |
| channel | text | SÍ | Canal de la pieza |
| target_copy_version_id | uuid | SÍ | Versión vigente evaluada (V-A); NULL si no se pudo resolver |
| target_creative_asset_id | uuid | SÍ | Arte de V-A |
| master_piece_id | uuid | SÍ | Maestra, si hay vínculo |
| master_declared_copy_version_id | uuid | SÍ | V-D declarada por la adaptación |
| master_reference_copy_version_id | uuid | SÍ | V-B: versión aprobada de la maestra de referencia |
| master_current_copy_version_id | uuid | SÍ | V-C: versión vigente de la maestra |
| cited_versions | jsonb | NO | V-E: versiones citadas por el cliente tal como llegaron |
| adaptation_approval_id | uuid | SÍ | Aprobación de V-A si se encontró |
| master_approval_id | uuid | SÍ | Aprobación de V-B si se encontró |
| impact_evaluation_id | uuid | SÍ | Evaluación vigente considerada |
| result | text | NO | permitido \| bloqueado |
| primary_block_category | text | SÍ | Categoría principal por orden de precedencia |
| block_categories | text[] | NO | Todas las categorías aplicables |
| condition_results | jsonb | NO | Un elemento por condición C1 a C9 |
| blocking_rule_refs | text[] | NO | Reglas incumplidas |
| verification_complete | boolean | NO | false si alguna condición no pudo verificarse |
| error_code | text | SÍ | Código controlado; nunca texto de excepción ni datos sensibles |
| db_txid | bigint | NO | Identificador de la transacción de base de datos (valor por defecto del servidor); permite a la guarda comprobar que la fila es de la misma transacción |
| request_origin | text | NO | app \| api |
| app_version | text | SÍ | Versión de la aplicación |

**Clave primaria:** `id`.

**Claves foráneas:**

| Columnas | Referencia | Borrado |
|---|---|---|
| (organization_id, piece_id) | creative_pieces(organization_id, id) | RESTRICT |
| (organization_id, actor_id) | memberships(organization_id, user_id) | RESTRICT |
| (organization_id, piece_id, target_copy_version_id) | copy_versions(organization_id, piece_id, id) | RESTRICT |
| (organization_id, master_piece_id, master_reference_copy_version_id) | copy_versions(organization_id, piece_id, id) | RESTRICT |
| (organization_id, adaptation_approval_id, target_copy_version_id) | approvals(organization_id, id, copy_version_id) | RESTRICT |
| (organization_id, master_approval_id, master_reference_copy_version_id) | approvals(organization_id, id, copy_version_id) | RESTRICT |
| (organization_id, impact_evaluation_id) | impact_evaluations(organization_id, id) | RESTRICT |

**Restricciones únicas:**

- unique(organization_id, id)
- unique(organization_id, actor_id, idempotency_key)
- unique(db_txid, piece_id) donde result = permitido (una publicación permitida por pieza y transacción)

**Restricciones CHECK:**

- result IN ('permitido','bloqueado')
- result = 'bloqueado' IMPLIES primary_block_category IS NOT NULL
- result = 'permitido' IMPLIES (primary_block_category IS NULL AND block_categories = '{}' AND verification_complete)
- result = 'permitido' IMPLIES todas las condiciones en cumple o no_aplica (función validadora)
- block_categories contenido en las nueve categorías permitidas
- primary_block_category pertenece a block_categories
- error_code IS NULL OR primary_block_category = 'error_tecnico'
- verification_complete = false IMPLIES result = 'bloqueado'
- piece_kind IN ('sin_relacion','maestra','adaptacion')

**Índices:**

- (organization_id, piece_id, attempted_at DESC)
- (organization_id, correlation_id)
- (organization_id, result, primary_block_category, attempted_at DESC)
- (organization_id, actor_id, attempted_at DESC)


---
<!-- ESPECIFICACION · líneas 1080-1117 · literal -->

## 9. Impacto en las 27 tablas

| Requisito | Tabla actual relacionada | Capacidad existente | Brecha | Cambio requerido |
|---|---|---|---|---|
| Identidad de maestra y adaptación | creative_pieces | Pieza por canal y formato, con estado y versión vigente | Sin vínculo a maestra; columnas de canal y formato sin tipos (G-2) | Columnas master_piece_id, is_adaptation, master_ref_is_adaptation, channel, format, adaptation_key y restricciones |
| Canal y formato válidos | channel_rules | Una fila por organización y canal; extensión, tono, estructura y CTA | No define formatos | allowed_formats y unique(organización, canal) al crear la tabla en la Fase 5; FK desde creative_pieces |
| Versión exacta de la maestra de origen | copy_versions | Versiones inmutables; parent_version_id solo dentro de una pieza | No hay versión de origen entre piezas | Tres columnas y FK compuestas |
| Arte de origen | creative_assets | Arte por versión con hash SHA-256 | Sin FK compuesta que valide arte y copy | unique(organization_id, piece_id, id, copy_version_id) |
| Integridad entre organizaciones | Todas (T-09, no aprobada) | FK compuestas propuestas | T-09 sin aprobar | Mismo patrón en las tablas nuevas; si T-09 no se aprueba, se mantiene en estas |
| Autoría heredada | copy_versions.created_by; creative_assets (quien sube) | Autoría por versión (T-04) | No hay herencia desde la maestra | Cálculo derivado; sin columnas |
| Clasificación y su historial | activity_logs | Auditoría general e inmutable | No demuestra contenido ni impone «distinto del proponente» | piece_classification_events |
| Revisor asignado | memberships, role_permissions | Roles y permisos por clave | Sin asignación por pieza (D-02) | piece_reviewer_assignments |
| Aprobación ligada a la versión exacta | approvals | Inmutable, versión exacta, independencia (record_approval y trigger) | Falta clave de destino compuesta | unique(organization_id, id, copy_version_id) |
| Registro de evaluación de impacto | activity_logs | Genérico | Sin estructura (G-5) | impact_evaluations |
| Control de publicación | creative_pieces.status y transition_piece_status | Única vía de cambio de estado; #10 solo pide que la versión aprobada sea la vigente | No verifica maestra, evaluación ni registra intentos | Ampliar la función; guarda de trigger |
| Bloqueos comerciales | audit_findings, commercial_block_exceptions | Hallazgo confirmado y excepción por versión | Ninguna | Se reutiliza para C7 |
| Integridad de artes | creative_assets, verify_assets_integrity | Hash y verificación | No es transaccional con Storage | C8 con límite declarado |
| Registro de intentos | activity_logs | Registra transiciones | No demuestra intentos rechazados ni sobrevive a una reversión (G-10) | publication_attempts |
| Permisos | role_permissions (17 claves) | channel.adapt, piece.review, piece.publish, org.manage | Ninguna | Sin claves nuevas |
| Aislamiento y lectura | RLS por organization_id | Aislamiento por organización | Tablas nuevas | Mismo patrón |
| Notificaciones | Matriz de notificaciones (N-22) | Definidas con limitación | Ninguna estructural | Sin cambio |

**Reutilizable sin cambio (22 de 27):** organizations, profiles, memberships, role_permissions, membership_permission_grants, brand_guidelines, brand_guideline_versions, campaigns, briefs, audits, audit_findings, comments, promotion_rules, performance_metrics, ab_tests, ai_runs, ai_prompt_versions, activity_logs, audit_rubric_versions, validation_settings_versions, ai_quotas y commercial_block_exceptions. **Con cambio:** creative_pieces y copy_versions (columnas), channel_rules (una columna y una única), creative_assets y approvals (solo una restricción única) y la función transition_piece_status. **Nuevas:** 4. Total propuesto: **31 tablas**; las 27 permanecen como línea base histórica.

**Justificación de cada elemento nuevo:**

| Elemento | Por qué es necesario |
|---|---|
| piece_classification_events | Historial con restricción de proponente distinto y secuencia; no cabe en activity_logs genérico |
| piece_reviewer_assignments | Sin asignación no hay «revisor asignado»; una columna perdería el historial de reasignaciones que prueba la independencia |
| impact_evaluations | Evidencia ligada a un par exacto de versiones con claves y CHECK; no cabe en comments ni en activity_logs |
| publication_attempts | Debe sobrevivir a la no publicación; activity_logs no demuestra intentos rechazados ni su persistencia |
| master_piece_id, is_adaptation, master_ref_is_adaptation | Vínculo y garantía de un nivel |
| replaces_piece_id (opcional, DG-18) | Trazabilidad estructural de una pieza nueva que reemplaza a una Publicada |
| allowed_formats en channel_rules | Validar el formato de cada pieza contra su canal |
| channel, format, adaptation_key | Identificar canal y formato (G-2) y distinguir adaptaciones múltiples |
| master_copy_version_id y master_creative_asset_id en copy_versions | Versión exacta de origen; sin ellas no existen V-D ni contribuciones heredadas |


# PARTE 1.2 — Reglas de integridad G-1, G-5 y G-10



---
<!-- ESPECIFICACION · líneas 199-227 · literal -->

### 3.7 Reglas de integridad de G-1

| ID | Regla |
|---|---|
| IG1-01 | Toda pieza, maestra o adaptación, es una fila de creative_pieces con identidad, estado, responsable y versiones propias |
| IG1-02 | master_piece_id es NULL en una maestra o pieza sin adaptaciones y NO NULL en una adaptación |
| IG1-03 | CHECK: master_piece_id distinto del id de la propia pieza |
| IG1-04 | Un solo nivel: la maestra referenciada no puede ser a su vez una adaptación (FK compuesta con is_adaptation, o trigger si la FK no es viable) |
| IG1-05 | Maestra y adaptación son de la misma organización (FK compuesta con organization_id) |
| IG1-06 | master_piece_id es inmutable una vez asignado |
| IG1-07 | Una maestra que tiene adaptaciones no puede convertirse en adaptación |
| IG1-08 | Cada versión de copy de una adaptación guarda la versión exacta de la maestra de origen y debe existir en esa maestra (FK compuesta) |
| IG1-09 | El arte de origen debe acompañar a esa versión de copy de la maestra (FK compuesta con copy_version_id) |
| IG1-10 | El vínculo de cada versión es inmutable porque copy_versions es inmutable |
| IG1-11 | El master_piece_id de la versión coincide con el de su pieza (trigger) |
| IG1-12 | Los contribuyentes de una versión de adaptación incluyen, por derivación y sin copiarlos, los de la versión de maestra de origen |
| IG1-13 | Una maestra admite varias adaptaciones; solo se impiden duplicados activos con el mismo canal, formato y clave |
| IG1-14 | Cada adaptación tiene su estado y sus versiones; T-02 se aplica por pieza |
| IG1-15 | Una adaptación es independiente solo si su último evento de clasificación es una confirmación |
| IG1-16 | Una adaptación no independiente no pasa por T-02 #7 ni #10 |
| IG1-17 | Quien propone la independencia no la confirma; confirma el revisor asignado con piece.review |
| IG1-18 | El historial de clasificación es de solo inserción con secuencia contigua por pieza |
| IG1-19 | La reversión a variación interna no borra aprobaciones ni versiones |
| IG1-20 | Ninguna pieza, versión ni arte con dependientes se borra (RESTRICT); se archiva |
| IG1-22 | channel y format son texto normalizado y no vacío; el canal tiene FK compuesta a channel_rules (se agrega en la Fase 5) y el formato debe estar en allowed_formats del canal (trigger) |
| IG1-23 | adaptation_key normalizada; vacía en piezas sin maestra; única entre adaptaciones activas del mismo canal y formato; claves distintas conviven |
| IG1-24 | Una nueva versión comercial de una pieza Publicada es una pieza nueva; la anterior y su historial se conservan (DG-15) |
| IG1-21 | La aprobación sigue ligada a la versión exacta; aprobar la maestra no aprueba la adaptación ni al revés |


---
<!-- ESPECIFICACION · líneas 444-460 · literal -->

#### 4.4.1 Elegibilidad: qué garantiza cada mecanismo

Ninguna FK aislada garantiza la elegibilidad: las FK garantizan identidad y correspondencia; la vigencia, el permiso y la independencia dependen de datos que cambian y se comprueban en la función bajo bloqueo, repetidos por un trigger BEFORE INSERT.

| Garantía requerida | Cómo se obtiene | Tipo de mecanismo | Regla |
|---|---|---|---|
| La asignación corresponde a la adaptación evaluada | FK compuesta (organización, adaptation_piece_id, evaluator_assignment_id) hacia piece_reviewer_assignments(organization_id, piece_id, id) | FK | IG5-21 |
| El evaluador coincide con el usuario asignado y la fila es de asignación | La misma FK, ampliada con evaluator_id y la columna constante «asignado» hacia unique(organización, pieza, id, revisor, acción) | FK + UNIQUE + CHECK de la constante | IG5-22 |
| La asignación está vigente al evaluar | Se compara con la última fila de la secuencia de esa pieza, bajo bloqueo de la fila de la adaptación | Función transaccional + trigger | IG5-23 |
| El evaluador tiene piece.review | Se lee de los roles de su membresía con esa fila bloqueada `FOR SHARE`; `evaluator_review_permission_verified` solo deja constancia | Función transaccional + trigger | IG5-24 |
| No es contribuyente de V-A, incluida la herencia | `version_contributors` sobre V-A y su versión de origen | Función + trigger | IG5-05 |
| No es contribuyente de V-B ni evalúa su propia modificación | `version_contributors` sobre V-B | Función + trigger | IG5-05, IG5-06 |
| La reasignación conserva la historia | Tabla de solo inserción con secuencia contigua por pieza; ninguna fila se edita | UNIQUE(piece_id, seq) + trigger + privilegios | IG5-08 |
| Evaluación ligada a versiones exactas aprobadas | FK compuestas a copy_versions, creative_assets y approvals | FK | IG5-01, IG5-02 |
| Una corrección no elimina ni modifica la anterior | Fila nueva con supersedes; la anterior no se toca; sin UPDATE ni DELETE | FK + UNIQUE + CHECK + trigger + privilegios | IG5-12, IG5-13 |
| Si la persona levanta su propio dictamen | Debe ser otra persona (DG-06) | Función + trigger | IG5-15 |


---
<!-- ESPECIFICACION · líneas 480-509 · literal -->

### 4.7 Reglas de integridad de G-5

| ID | Regla |
|---|---|
| IG5-01 | La evaluación registra la versión evaluada de la adaptación y el par exacto de versiones de la maestra (origen V-D y aprobada V-B) |
| IG5-02 | Solo se evalúa una versión de adaptación con aprobación y una versión de maestra con aprobación (FK compuestas a approvals) |
| IG5-03 | Solo existe evaluación de un par cuando V-D es distinta de V-B |
| IG5-04 | El evaluador es el revisor asignado vigente y tiene piece.review |
| IG5-05 | El evaluador no es contribuyente de la versión de la adaptación (incluida la contribución heredada) ni de la versión de la maestra evaluada |
| IG5-06 | No hay autoevaluación |
| IG5-07 | Sin revisor elegible no se registra evaluación y la publicación sigue bloqueada; no pasa autoridad a Admin, propietario ni otro rol |
| IG5-08 | La reasignación del revisor crea una asignación nueva y conserva la anterior |
| IG5-09 | Evidencia mínima: siete dimensiones, justificación de al menos 30 caracteres y motivo cuando el resultado es desconocido |
| IG5-10 | El resultado es coherente con las dimensiones (todas no afectadas, alguna afectada o alguna desconocida) |
| IG5-11 | La acción posterior la determina el resultado (CHECK) |
| IG5-12 | Las evaluaciones son de solo inserción |
| IG5-13 | Una segunda evaluación o una corrección es una fila nueva que reemplaza en vigencia a la anterior, con motivo, sin borrarla |
| IG5-14 | La evaluación vigente es la cabeza de la cadena; no hay ramas; una ambigüedad bloquea |
| IG5-15 | Una evaluación que levanta un bloqueo (de desfavorable o desconocida a sin impacto) la hace una persona distinta del evaluador reemplazado |
| IG5-16 | Una evaluación sobre una versión de la maestra que dejó de ser la aprobada vigente se rechaza al confirmar, bajo bloqueo |
| IG5-17 | La evaluación no cambia el estado de ninguna pieza, no inserta aprobaciones y no crea transiciones |
| IG5-18 | El estado de resolución se deriva y no se almacena |
| IG5-19 | Idempotencia por evaluador y clave |
| IG5-20 | Sobre una adaptación ya Publicada la evaluación deja evidencia y aviso, sin transición |
| IG5-21 | La asignación que acredita al evaluador es de la adaptación evaluada (FK compuesta con piece_id) |
| IG5-22 | El evaluador es el revisor de esa asignación y la fila es de asignación, no de retiro (FK compuesta con constante) |
| IG5-23 | La asignación es la vigente (última de la secuencia) al momento de evaluar; se comprueba bajo bloqueo (función y trigger, no FK) |
| IG5-24 | El evaluador tiene piece.review al momento de evaluar; se comprueba con la fila de membresía bloqueada |
| IG5-25 | Reasignación, evaluación, cambio de la maestra y publicación usan el mismo orden de bloqueo y revalidan lo que leyeron |


---
<!-- ESPECIFICACION · líneas 510-515 · literal -->

### 4.8 Reglas de auditoría

- Cada operación registra `correlation_id`, evaluador y fecha del servidor en la propia fila (fuente de verdad).
- Se escribe además una fila puntero en `activity_logs` (`impact.evaluated`, `reviewer.assigned`, `classification.event`) dentro de la misma transacción; su ausencia no invalida el registro, porque `activity_logs` es genérico y su suficiencia no está demostrada (DA-01).
- Un aviso N-22 se genera cuando el resultado exige una decisión humana; el aviso no concede permisos ni sustituye el registro (evento ≠ entrega).


---
<!-- ESPECIFICACION · líneas 647-650 · literal -->

### 5.3 Un intento, una fila

Cada solicitud **aceptada** genera como máximo **una** fila (permitido o bloqueado) con un elemento por condición en `condition_results` (`cumple`, `no_cumple`, `no_verificable`, `no_aplica` o `no_evaluada`, esta última solo si C1 falló). No hay filas por condición: se evalúa y registra todo en una operación. Registrar también los intentos permitidos (DG-10) da un libro completo y hace detectable una publicación sin fila. «Aceptada» significa: persona autenticada, miembro de la organización de la pieza, pieza visible para ella y solicitud con forma válida (pieza, versiones citadas y clave de idempotencia).


---
<!-- ESPECIFICACION · líneas 651-676 · literal -->

### 5.4 Reglas de integridad de G-10

| ID | Regla |
|---|---|
| IG10-01 | Toda solicitud autenticada, de un miembro de la organización y aceptada por el mecanismo de publicación termina en una de dos formas excluyentes: (a) exactamente una fila confirmada de publication_attempts, permitida o bloqueada, o (b) la transacción falla, sin publicación y sin fila confirmada |
| IG10-02 | Se evalúan todas las condiciones aplicables aunque una falle; si C1 falla, las demás se registran como no evaluadas para no revelar información |
| IG10-03 | El resultado es permitido solo si las nueve condiciones son cumple o no_aplica y la verificación está completa |
| IG10-04 | Una condición que no puede verificarse bloquea |
| IG10-05 | Actor, fecha y hora, y correlación los fija el servidor |
| IG10-06 | Idempotencia: la misma clave devuelve el resultado almacenado sin repetir efectos |
| IG10-07 | Un intento con otra clave sobre una pieza ya Publicada queda bloqueado y registrado |
| IG10-08 | La fila del intento permitido y el cambio de estado ocurren en la misma transacción |
| IG10-09 | Un intento bloqueado devuelve un resultado normal tras escribir su fila, sin lanzar excepción que la revierta |
| IG10-10 | Un error técnico dentro de la verificación se captura en un subbloque, se registra como error_tecnico y bloquea |
| IG10-11 | Si falla la inserción del registro falla toda la transacción: el estado no cambia y no existe fila confirmada; cualquier evidencia fuera de la transacción es evidencia de plataforma y no se presenta como fila de publication_attempts |
| IG10-12 | Ningún rol de aplicación escribe directamente en la tabla de intentos |
| IG10-13 | Un trigger rechaza status = publicado si no existe un intento permitido de la misma transacción para esa pieza y versión |
| IG10-14 | Los registros son de solo inserción por privilegios y por trigger |
| IG10-15 | El usuario ve categoría y motivos de su intento; el detalle completo solo lo ve org.manage; cada actor ve sus propios intentos |
| IG10-16 | Sin secretos: error_code controlado, sin texto de excepción, tokens ni dirección IP |
| IG10-17 | El registro no crea ni modifica aprobaciones ni evaluaciones; solo las referencia |
| IG10-18 | Sin borrado desde la aplicación; no se define política de retención (DG-09 diferida) |
| IG10-19 | Una solicitud sin autenticación o de una persona sin membresía no publica y no genera fila de negocio: es un evento de seguridad de plataforma; no se inventa un actor |
| IG10-20 | Una clave de idempotencia identifica una acción del usuario: repetirla devuelve el resultado almacenado; una acción nueva tras corregir condiciones usa una clave nueva; si no hubo fila confirmada, el reintento con la misma clave se evalúa desde cero |
| IG10-21 | La guarda del estado publicado comprueba una fila permitida de la misma transacción (db_txid), de la pieza y de la versión |


---
<!-- ESPECIFICACION · líneas 677-689 · literal -->

### 5.5 Idempotencia, correlación, errores y reintentos

| Elemento | Regla |
|---|---|
| idempotency_key | Obligatoria; la genera el cliente por **acción del usuario** (un clic en «Publicar»); alcance (organización, actor). Es lo que evita duplicados |
| correlation_id | Identifica una solicitud en la aplicación y en los registros de la plataforma; la envía el cliente (formato validado) o la genera el servidor. **No** es única ni sirve de clave; no sustituye a la clave de idempotencia |
| Misma clave y existe una fila | Se devuelve el resultado almacenado, con su correlación, sin repetir efectos |
| Misma clave y no existe fila (la transacción abortó) | Se evalúa desde cero: no hay resultado que reutilizar (IG10-20) |
| Reintento tras un resultado bloqueado | Con la misma clave devuelve el mismo bloqueo almacenado (evita que un reintento de red cambie el resultado). Tras corregir la causa, la interfaz usa una **clave nueva** |
| Misma clave con otra pieza o versiones citadas distintas | Se rechaza como solicitud inválida: la clave identifica otra acción; no genera fila |
| Doble clic con claves distintas | Bloqueo de la fila de la pieza; la segunda ve la pieza ya Publicada y queda bloqueada y registrada (T-45) |
| Errores | Se distinguen: bloqueo de negocio (fila bloqueada), error técnico capturado (fila bloqueada con error_tecnico y código controlado) y fallo de la transacción (sin fila; el cliente recibe un error genérico con la correlación que él envió) |


---
<!-- ESPECIFICACION · líneas 708-722 · literal -->

### 5.8 Registro y garantía de los intentos (corrige IG10-01, IG10-11 y la 5.8 de la v1)

**Contradicción corregida.** La v1 decía a la vez que cada solicitud deja una fila y que, si falla el registro, el intento «queda» en los registros de la plataforma. PostgreSQL no puede confirmar una fila de auditoría dentro de una transacción que abortó: si la transacción falla, ninguna de sus filas existe. La plataforma, a lo sumo, conserva evidencia **fuera** de la base transaccional, y eso no es una fila de `publication_attempts`.

**Formulación final de IG10-01:** «Toda solicitud autenticada, de un miembro de la organización y aceptada por el mecanismo de publicación termina en una de dos formas excluyentes: (a) exactamente una fila confirmada de `publication_attempts`, permitida o bloqueada, o (b) la transacción falla, sin publicación y sin fila confirmada».

**Justificación.** La fórmula que propusiste, «deja exactamente una fila confirmada, o no produce publicación», es correcta en lo esencial y la adopto, con dos precisiones: (1) debe decir que, en el segundo caso, **tampoco hay fila confirmada**, para que nadie interprete que el intento quedó registrado; (2) debe delimitar «aceptada» y excluir lo no autenticado o sin membresía, que no es un intento de negocio. Así la regla no promete evidencia imposible y conserva la garantía que importa: nunca hay publicación sin una fila permitida confirmada en la misma transacción.

| Escenario | Qué ocurre | Evidencia que queda | Límite o qué no se afirma |
|---|---|---|---|
| A. Solicitud autenticada y procesada | Se evalúan C1 a C9; se inserta exactamente una fila (permitida o bloqueada); si es permitida, el estado cambia en la misma transacción; el bloqueo devuelve un resultado normal para que la transacción confirme | Una fila confirmada de publication_attempts | La clave de idempotencia evita duplicados |
| B. Error técnico durante la validación | El error se captura en un subbloque (savepoint); la condición queda `no_verificable`; se inserta la fila con `error_tecnico`, la categoría y un `error_code` de una lista cerrada, y se bloquea | Una fila confirmada, sin texto de excepción | Solo cubre errores capturables; un tiempo de espera agotado, una cancelación o la pérdida de conexión abortan toda la transacción y caen en C |
| C. Falla la inserción de publication_attempts (o aborta la transacción) | La transacción falla: el estado **no** cambia a Publicado y no hay fila confirmada. El cliente recibe un error genérico y puede reintentar con la misma clave | Evidencia alternativa **si está disponible y no verificada**: la propia respuesta de error con la correlación enviada por el cliente y los registros de la plataforma (API y base de datos), cuya conservación y contenido no están comprobados. Ninguna se presenta como fila de publication_attempts ni aparece en la consulta de auditoría de intentos | No se crea una tabla de respaldo escrita fuera de la transacción: sería otro registro con otra garantía y no se propone |
| D. Sin autenticación o sin membresía | La función rechaza antes de la verificación; no se inserta fila; RLS no muestra la pieza a quien no es miembro | Evento de seguridad de plataforma (registros de autenticación y de la API), no un intento de publicación de negocio; su disponibilidad no está verificada | No se inventa un actor: `actor_id` es NOT NULL con FK a memberships, de modo que una fila sin persona miembro es estructuralmente imposible |


# PARTE 1.3 — `db_txid`: definición, tipo y uso

Apariciones literales (línea: texto completo). La definición de columna está en 5.1; la guarda, en IG10-13/IG10-21, 5.8 punto 8, 8.8 y T-70.

- **L588:** | db_txid | bigint | NO | Identificador de la transacción de base de datos (valor por defecto del servidor); permite a la guarda comprobar que la fila es de la misma transacción |

- **L610:** - unique(db_txid, piece_id) donde result = permitido (una publicación permitida por pieza y transacción)

- **L675:** | IG10-21 | La guarda del estado publicado comprueba una fila permitida de la misma transacción (db_txid), de la pieza y de la versión |

- **L698:** | Qué queda restringido | `condition_results` completo, `blocking_rule_refs`, `cited_versions`, `error_code`, `db_txid` y correlación |

- **L740:** 8. Inserta la fila de `publication_attempts`. Si es permitido, cambia el estado a Publicado (T-02 #10) y la guarda del trigger comprueba que existe esa fila permitida de la misma transacción (`db_txid`).

- **L1069:** | La única ruta que deja Publicado es la función transaccional autorizada | Único propietario con UPDATE(status) más guarda de trigger con db_txid | IS-01, IG10-21 | T-60, T-70 | Sí: roles y privilegios de Supabase |

- **L1224:** | T-70 | Guarda y transacción | Existe una fila permitida de otra transacción para la misma pieza | Intentar cambiar status a Publicado fuera de esa transacción | Rechazo por db_txid distinto | Reutilizar un permiso antiguo | La guarda compara db_txid, pieza y versión | Infraestructura real | IG10-21, IS-01 |

- **L1317:** | IG10-21 | La guarda del estado publicado comprueba una fila permitida de la misma transacción (db_txid), de la pieza y de la versión | T-60, T-70 |



# PARTE 1.4 — Constraints, FK, triggers y funciones de la publicación



---
<!-- ESPECIFICACION · líneas 727-790 · literal -->

## 6. Arquitectura integrada

### 6.1 Flujo de publicación de extremo a extremo

La arquitectura une las tres piezas: **G-1** identifica y relaciona (qué maestra, qué versión), **G-5** da la evidencia del impacto sobre versiones exactas, **G-10** registra cada intento y sus razones, y la **publicación** valida las tres antes de cambiar el estado. El flujo, en una sola transacción de base de datos:

1. El cliente envía la solicitud con la pieza, las versiones que cree estar publicando (V-E), una clave de idempotencia y, opcionalmente, un identificador de correlación. **No envía** actor, fecha ni resultado.
2. La ampliación de `transition_piece_status` toma el actor de `auth.uid()`. Sin persona autenticada o sin membresía rechaza **sin escribir fila de negocio** (escenario D de 5.8); no inventa actor.
3. Busca un intento previo con la misma clave y actor; si existe, devuelve su resultado almacenado sin repetir efectos; si la clave se usó para otra pieza o versiones, rechaza la solicitud.
4. Toma los bloqueos en el orden de 4.10: maestra (`FOR SHARE`), adaptación (`FOR UPDATE`), membresía del actor (`FOR SHARE`).
5. Lee del servidor V-A, V-B, V-C, V-D, aprobaciones, clasificación vigente, evaluación vigente, bloqueos y excepciones. Nada de lo enviado por el cliente se usa como dato, salvo V-E para compararlo.
6. Evalúa C1 a C9 en un subbloque con captura de errores. Cada condición termina en `cumple`, `no_cumple`, `no_verificable`, `no_aplica` o `no_evaluada` (solo tras fallar C1). Un error capturado deja la condición en `no_verificable` y el intento como `error_tecnico`.
7. Calcula el resultado: **permitido** solo si todas son `cumple` o `no_aplica` y la verificación está completa; si no, **bloqueado**, con todas las categorías y la principal por precedencia.
8. Inserta la fila de `publication_attempts`. Si es permitido, cambia el estado a Publicado (T-02 #10) y la guarda del trigger comprueba que existe esa fila permitida de la misma transacción (`db_txid`).
9. Escribe la fila puntero en `activity_logs` y confirma. Un bloqueo devuelve un resultado normal con categoría y motivos visibles, sin lanzar excepción.
10. Si falla la inserción de la fila, el cambio de estado o la transacción aborta (tiempo de espera, conexión), no hay publicación ni fila confirmada (escenario C de 5.8); el cliente reintenta con la misma clave.

Defensa en profundidad: aunque algo omitiera la función, la guarda del trigger y la revocación de privilegios impiden dejar `status = publicado` sin una fila permitida de la misma transacción.

### 6.2 Reglas de publicación: C1 a C9 precisadas

Precisan las condiciones conceptuales de G-7 (v9, no aceptada). Los cambios respecto de v9 están marcados en la sección 12 (DG-05).

| # | Condición (todas obligatorias) | Información | Categoría de bloqueo | Códigos de motivo |
|---|---|---|---|---|
| C1 | El actor tiene piece.publish, es miembro activo y no tiene impedimento de independencia | I9 | falta_de_permisos | SIN_PERMISO; IMPEDIMENTO_INDEPENDENCIA |
| C2 | La pieza está Aprobado en su versión vigente V-A y existe una aprobación de esa versión exacta (copy y arte) | I1, I2 | sin_aprobacion_adaptacion / inconsistencia_versiones | ESTADO_NO_APROBADO; SIN_APROBACION_V_A; APROBACION_DE_OTRA_VERSION |
| C3 | Si la pieza tiene maestra: la clasificación vigente es «independiente»; la maestra está Aprobado o Publicado con su versión vigente aprobada (V-B) y existe la aprobación de esa versión exacta | I3, I4 | sin_aprobacion_maestra / sin_aprobacion_adaptacion / imposibilidad_verificar | CLASIFICACION_NO_CONFIRMADA; MAESTRA_SIN_APROBACION; MAESTRA_NO_VIGENTE_APROBADA; VINCULO_NO_VERIFICABLE |
| C4 | Si V-D (versión de la maestra de origen de V-A) es distinta de V-B: existe una evaluación vigente de ese par | I5, I6 | evaluacion_pendiente | EVALUACION_INEXISTENTE; EVALUACION_AMBIGUA |
| C5 | La evaluación vigente del par no es «requiere revisión» ni «invalida» | I6 | evaluacion_desfavorable | EVALUACION_DESFAVORABLE |
| C6 | La evaluación vigente del par no es «desconocido» | I6 | evaluacion_pendiente | EVALUACION_DESCONOCIDA |
| C7 | No hay bloqueo comercial confirmado sin excepción vigente en V-A ni en V-B | I7 | bloqueo_comercial_critico | BLOQUEO_SIN_EXCEPCION |
| C8 | Los artes de V-A (y de V-B) existen, con hash y objeto registrados y sin resultado de integridad adverso | I8 | inconsistencia_versiones / imposibilidad_verificar | ARTE_INCONSISTENTE; INTEGRIDAD_NO_VERIFICABLE |
| C9 | Las versiones citadas en la solicitud (V-E) coinciden con V-A y V-B leídas del servidor | V-E | inconsistencia_versiones | VERSION_CITADA_DISTINTA |

| Regla | Alcance |
|---|---|
| Maestra con aprobación válida | La maestra está Aprobado o Publicado, su versión vigente es la aprobada y existe la aprobación de esa versión exacta. Como cualquier cambio sale de Aprobado por #11, el estado basta para saber si la aprobación sigue vigente |
| Cuándo hay que evaluar | Cuando la versión de origen V-D de la adaptación difiere de la versión aprobada V-B. Si la adaptación ya deriva de V-B no hay cambio que evaluar |
| Piezas sin relación | Una pieza sin maestra ni adaptaciones evalúa C3 a C6 como `no_aplica`; solo si no tiene `master_piece_id`. Una pieza con maestra y sin clasificación independiente vigente falla C3 |
| Maestra que se publica | C3 a C6 no aplican a una maestra: no depende de sus adaptaciones |
| Condición no verificable | Se trata como no cumplida (regla 8 de PO-20) |

### 6.3 Piezas publicadas (DG-15)

T-02 conserva sus 13 transiciones: **una pieza Publicada no se modifica**; solo admite #13 (Archivado). No se crea ninguna transición nueva.

| Concepto | Definición |
|---|---|
| Estado interno de la pieza | Es el estado de T-02 en la base de datos (Publicado, Archivado, etc.). Lo cambian solo las transiciones aprobadas |
| Disponibilidad en canales externos | Es si el contenido sigue visible en el canal. **El modelo no la representa ni la controla**: no hay integración con canales ni estado de retiro. No se presume que archivar o reemplazar una pieza retire el contenido externo |
| Dependencia identificada | **DEP-RET-01:** no existe procedimiento operativo documentado, ni responsable, para retirar contenido externo cuando una pieza se reemplaza. Se identifica como dependencia; no se inventa un estado ni una transición |

| Paso | Qué ocurre | Efecto o registro |
|---|---|---|
| 1 | Cambia una maestra que **no** está Publicada y tiene adaptaciones Publicadas (si la maestra estuviera Publicada no podría cambiar) | La maestra sale de Aprobado por #11 y crea una versión nueva |
| 2 | Las adaptaciones Publicadas conservan su estado, su artefacto, su versión y su aprobación histórica | Nada se modifica ni se elimina |
| 3 | Cuando la maestra vuelve a aprobarse, se registra la evaluación de impacto de cada adaptación aprobada afectada (IG5-20), también de las Publicadas | Evidencia en `impact_evaluations`; sin transición |
| 4 | Se genera el aviso N-22 al responsable cuando el resultado exige una decisión humana | Evento no es entrega (DA-01) |
| 5 | Se bloquean nuevas publicaciones de las demás adaptaciones mientras C3 a C6 no se cumplan | Registro en publication_attempts |
| 6 | Si hace falta una nueva versión comercial, se crea una **pieza nueva** (con su maestra o adaptaciones nuevas); si se aprueba DG-18, la pieza nueva guarda `replaces_piece_id` | Se aplican C1 a C9 a la pieza nueva |
| 7 | La pieza anterior se conserva con su historial y puede archivarse por #13 cuando corresponda | Archivar es un cambio interno; no retira contenido externo |
| 8 | El retiro externo, si se necesita, depende de DEP-RET-01 | Fuera del alcance de este diseño |


---
<!-- ESPECIFICACION · líneas 746-769 · literal -->

### 6.2 Reglas de publicación: C1 a C9 precisadas

Precisan las condiciones conceptuales de G-7 (v9, no aceptada). Los cambios respecto de v9 están marcados en la sección 12 (DG-05).

| # | Condición (todas obligatorias) | Información | Categoría de bloqueo | Códigos de motivo |
|---|---|---|---|---|
| C1 | El actor tiene piece.publish, es miembro activo y no tiene impedimento de independencia | I9 | falta_de_permisos | SIN_PERMISO; IMPEDIMENTO_INDEPENDENCIA |
| C2 | La pieza está Aprobado en su versión vigente V-A y existe una aprobación de esa versión exacta (copy y arte) | I1, I2 | sin_aprobacion_adaptacion / inconsistencia_versiones | ESTADO_NO_APROBADO; SIN_APROBACION_V_A; APROBACION_DE_OTRA_VERSION |
| C3 | Si la pieza tiene maestra: la clasificación vigente es «independiente»; la maestra está Aprobado o Publicado con su versión vigente aprobada (V-B) y existe la aprobación de esa versión exacta | I3, I4 | sin_aprobacion_maestra / sin_aprobacion_adaptacion / imposibilidad_verificar | CLASIFICACION_NO_CONFIRMADA; MAESTRA_SIN_APROBACION; MAESTRA_NO_VIGENTE_APROBADA; VINCULO_NO_VERIFICABLE |
| C4 | Si V-D (versión de la maestra de origen de V-A) es distinta de V-B: existe una evaluación vigente de ese par | I5, I6 | evaluacion_pendiente | EVALUACION_INEXISTENTE; EVALUACION_AMBIGUA |
| C5 | La evaluación vigente del par no es «requiere revisión» ni «invalida» | I6 | evaluacion_desfavorable | EVALUACION_DESFAVORABLE |
| C6 | La evaluación vigente del par no es «desconocido» | I6 | evaluacion_pendiente | EVALUACION_DESCONOCIDA |
| C7 | No hay bloqueo comercial confirmado sin excepción vigente en V-A ni en V-B | I7 | bloqueo_comercial_critico | BLOQUEO_SIN_EXCEPCION |
| C8 | Los artes de V-A (y de V-B) existen, con hash y objeto registrados y sin resultado de integridad adverso | I8 | inconsistencia_versiones / imposibilidad_verificar | ARTE_INCONSISTENTE; INTEGRIDAD_NO_VERIFICABLE |
| C9 | Las versiones citadas en la solicitud (V-E) coinciden con V-A y V-B leídas del servidor | V-E | inconsistencia_versiones | VERSION_CITADA_DISTINTA |

| Regla | Alcance |
|---|---|
| Maestra con aprobación válida | La maestra está Aprobado o Publicado, su versión vigente es la aprobada y existe la aprobación de esa versión exacta. Como cualquier cambio sale de Aprobado por #11, el estado basta para saber si la aprobación sigue vigente |
| Cuándo hay que evaluar | Cuando la versión de origen V-D de la adaptación difiere de la versión aprobada V-B. Si la adaptación ya deriva de V-B no hay cambio que evaluar |
| Piezas sin relación | Una pieza sin maestra ni adaptaciones evalúa C3 a C6 como `no_aplica`; solo si no tiene `master_piece_id`. Una pieza con maestra y sin clasificación independiente vigente falla C3 |
| Maestra que se publica | C3 a C6 no aplican a una maestra: no depende de sus adaptaciones |
| Condición no verificable | Se trata como no cumplida (regla 8 de PO-20) |


---
<!-- ESPECIFICACION · líneas 770-790 · literal -->

### 6.3 Piezas publicadas (DG-15)

T-02 conserva sus 13 transiciones: **una pieza Publicada no se modifica**; solo admite #13 (Archivado). No se crea ninguna transición nueva.

| Concepto | Definición |
|---|---|
| Estado interno de la pieza | Es el estado de T-02 en la base de datos (Publicado, Archivado, etc.). Lo cambian solo las transiciones aprobadas |
| Disponibilidad en canales externos | Es si el contenido sigue visible en el canal. **El modelo no la representa ni la controla**: no hay integración con canales ni estado de retiro. No se presume que archivar o reemplazar una pieza retire el contenido externo |
| Dependencia identificada | **DEP-RET-01:** no existe procedimiento operativo documentado, ni responsable, para retirar contenido externo cuando una pieza se reemplaza. Se identifica como dependencia; no se inventa un estado ni una transición |

| Paso | Qué ocurre | Efecto o registro |
|---|---|---|
| 1 | Cambia una maestra que **no** está Publicada y tiene adaptaciones Publicadas (si la maestra estuviera Publicada no podría cambiar) | La maestra sale de Aprobado por #11 y crea una versión nueva |
| 2 | Las adaptaciones Publicadas conservan su estado, su artefacto, su versión y su aprobación histórica | Nada se modifica ni se elimina |
| 3 | Cuando la maestra vuelve a aprobarse, se registra la evaluación de impacto de cada adaptación aprobada afectada (IG5-20), también de las Publicadas | Evidencia en `impact_evaluations`; sin transición |
| 4 | Se genera el aviso N-22 al responsable cuando el resultado exige una decisión humana | Evento no es entrega (DA-01) |
| 5 | Se bloquean nuevas publicaciones de las demás adaptaciones mientras C3 a C6 no se cumplan | Registro en publication_attempts |
| 6 | Si hace falta una nueva versión comercial, se crea una **pieza nueva** (con su maestra o adaptaciones nuevas); si se aprueba DG-18, la pieza nueva guarda `replaces_piece_id` | Se aplican C1 a C9 a la pieza nueva |
| 7 | La pieza anterior se conserva con su historial y puede archivarse por #13 cuando corresponda | Archivar es un cambio interno; no retira contenido externo |
| 8 | El retiro externo, si se necesita, depende de DEP-RET-01 | Fuera del alcance de este diseño |


---
<!-- ESPECIFICACION · líneas 1006-1018 · literal -->

### 8.2 Funciones de backend propuestas

| Función (nombre propuesto) | Qué hace | Permiso |
|---|---|---|
| create_adaptation | Crea la pieza candidata y su primera versión con el vínculo | channel.adapt |
| propose_independence / resolve_independence | Registra propuesta, confirmación, no confirmación o reversión | autor o responsable / piece.review asignado |
| assign_reviewer | Registra asignaciones y retiros | org.manage |
| record_impact_evaluation | Registra la evaluación con todas las validaciones | piece.review asignado |
| version_contributors / eligible_evaluators | Auxiliares de solo lectura que calculan contribuyentes y elegibles | internas |
| transition_piece_status (ampliada) | Verificación C1 a C9, registro del intento y cambio de estado | según la transición |

Todas son `SECURITY DEFINER` con `search_path` vacío y propietario dedicado; ninguna recibe el actor, la fecha ni el resultado como parámetro. Las existentes `record_approval`, `review_finding` y `verify_assets_integrity` no pueden publicar (R-4 de G-7).


---
<!-- ESPECIFICACION · líneas 1019-1026 · literal -->

### 8.3 Prevención de escrituras directas y de manipulación del actor

- `REVOKE` de INSERT, UPDATE, DELETE y TRUNCATE sobre las cuatro tablas nuevas a `anon`, `authenticated` y `service_role`; `REVOKE UPDATE (status)` sobre `creative_pieces` a los mismos roles. Los privilegios por defecto de Supabase conceden permisos amplios a esos roles en el esquema público: debe **verificarse y revocarse expresamente** (T-60, T-73; requieren infraestructura real).
- **Dos propietarios de funciones** (nombres propuestos; su creación y viabilidad en Supabase no están verificadas): `cci_state_owner`, dueño solo de `transition_piece_status`, con UPDATE sobre `status` e INSERT en `publication_attempts`; y `cci_records_owner`, dueño de las demás funciones (aprobación, hallazgos, clasificación, asignación, evaluación), con INSERT en sus tablas y **sin** UPDATE sobre `status` ni INSERT en `publication_attempts`. Así ninguna auxiliar puede publicar por privilegios, no solo por no contener el código.
- `REVOKE EXECUTE ... FROM PUBLIC`; EXECUTE de las funciones de usuario solo para `authenticated`. `service_role` no las ejecuta, y las funciones rechazan `auth.uid()` nulo.
- El actor se toma de `auth.uid()`; ninguna función recibe actor, fecha ni resultado. **Dependencia no verificada:** `auth.uid()` lee la identidad de la sesión de la solicitud; quien tenga credenciales de base de datos de administración puede fijarla. Por eso las credenciales de administración de la base no pueden estar en el navegador, en una Edge Function ni en la aplicación.
- El frontend usa solo la clave pública con la sesión del usuario. Una Edge Function que invoque estas funciones debe reenviar el token del usuario, no la clave de servicio: con la de servicio no puede ejecutarlas ni actualizar `status`.


---
<!-- ESPECIFICACION · líneas 1027-1030 · literal -->

### 8.4 Protección de registros históricos

Privilegios revocados, trigger que rechaza UPDATE y DELETE incluso al propietario de la función y RLS de solo lectura. Contra un superusuario de la plataforma, la mitigación es el hash encadenado opcional y la exportación periódica (DG-12, RR-04).


---
<!-- ESPECIFICACION · líneas 1031-1034 · literal -->

### 8.5 Concurrencia y bloqueo de versiones

Orden único de bloqueo y matriz de revalidación en 4.10: maestra, adaptaciones por `id`, membresía del actor. Las unicidades parciales y la clave de idempotencia son una segunda barrera. No se presupone aislamiento serializable.


---
<!-- ESPECIFICACION · líneas 1035-1046 · literal -->

### 8.6 Límites transaccionales y fallos parciales

| Situación | Comportamiento y límite |
|---|---|
| Límite de la transacción | Una llamada a una función es una transacción de PostgreSQL. Dos llamadas encadenadas desde una Edge Function son **dos** transacciones; una Edge Function no da atomicidad entre ellas ni con sistemas externos |
| Storage | Los bytes de un arte no están dentro de la transacción de la base. C8 comprueba filas, hash registrado y objeto, y el resultado de `verify_assets_integrity`; una alteración fuera de la aplicación solo se descarta si el bucket impide sobrescribir objetos (RR-05, prueba T-50) |
| Sistemas externos | El diseño no incluye publicación a canales externos. Si se agregara, requeriría un patrón de bandeja de salida y un estado intermedio no previsto en T-02; no se inventa |
| IA (Cohere) | No participa en ninguna condición; no hay análisis semántico automático |
| Verificación fallida | Bloquea; nunca se supone cumplida |
| Registro fallido | Falla toda la operación; ver 5.8 |
| Reintento | Con la misma clave devuelve el resultado almacenado |


---
<!-- ESPECIFICACION · líneas 520-542 · literal -->

### 4.10 Concurrencia de G-5: orden de bloqueo y revalidación

**Orden único de bloqueo** para toda operación que toque una adaptación: (1) la fila de la maestra `FOR SHARE` (o `FOR UPDATE` si la operación cambia la maestra); (2) la fila de la adaptación `FOR UPDATE`, y entre varias adaptaciones por `id` ascendente; (3) la fila de membresía del actor `FOR SHARE`; (4) las inserciones. La revocación de un permiso actualiza la membresía y no toma bloqueos de piezas, por lo que no puede formar un ciclo.

| Operación | Bloqueos | Qué revalida bajo bloqueo | Si cambió |
|---|---|---|---|
| Reasignación del revisor | Maestra FOR SHARE, adaptación FOR UPDATE | El nuevo revisor tiene piece.review; la secuencia no cambió desde la lectura | Si cambió, se rechaza y se reintenta con la secuencia nueva |
| Evaluación | Maestra FOR SHARE, adaptación FOR UPDATE, membresía FOR SHARE | La asignación sigue siendo la vigente; piece.review; independencia; V-B sigue siendo la versión aprobada vigente de la maestra; no hay cabeza nueva en la cadena | Rechazo con motivo; la persona evalúa el estado actual |
| Cambio de la maestra (nueva versión, #11, aprobación) | Maestra FOR UPDATE | Estado y versión vigente de la maestra al terminar | Las evaluaciones y publicaciones que esperaban revalidan al obtener su bloqueo |
| Publicación de una adaptación | Maestra FOR SHARE, adaptación FOR UPDATE, membresía FOR SHARE | C1 a C9 completas con los datos tal como están tras obtener los bloqueos | Resultado bloqueado y registrado, o permitido |
| Publicación de una maestra o pieza sin relación | Solo su fila FOR UPDATE | C1, C2, C7, C8 y C9 | Igual |
| Aprobación de una adaptación | Maestra FOR SHARE, adaptación FOR UPDATE | Independencia y clasificación vigente | Rechazo |

Otros escenarios:

| Escenario | Resolución |
|---|---|
| Dos evaluadores sobre el mismo par | Se serializan por la fila de la adaptación; el segundo choca con la raíz única y debe registrar una segunda evaluación a propósito |
| La maestra se aprueba en otra versión mientras se evalúa | Se rechaza por versión obsoleta (IG5-16) |
| Reintento de red | `unique(evaluador, idempotency_key)` devuelve la fila existente |
| Dos correcciones de la misma evaluación | `unique(supersedes_evaluation_id)`: una prospera |
| Límite | READ COMMITTED sin bloqueo de la fila relevante no basta; el diseño depende de los bloqueos explícitos y las restricciones, no del nivel de aislamiento |


---
<!-- ESPECIFICACION · líneas 995-1005 · literal -->

### 8.1 Responsabilidades: qué garantiza cada mecanismo y qué no

| Mecanismo | Garantiza | No garantiza |
|---|---|---|
| Restricciones (FK, CHECK, UNIQUE) | Integridad estructural: versiones existentes, misma organización, un solo nivel, cadenas sin ramas, resultados coherentes | Quién actúa, independencia, orden de operaciones ni reglas entre varias filas |
| Triggers | Reglas entre filas y tablas: coherencia de vínculos, inmutabilidad, protección del historial, guarda del estado publicado | Autorización por sí mismos; se pueden deshabilitar con privilegios altos |
| Funciones transaccionales de backend | La lógica de C1 a C9, bloqueos, actor, idempotencia y registro en una transacción | Atomicidad con sistemas externos; protegerse de un privilegio de superusuario |
| RLS | Aislamiento por organización y visibilidad de lectura | **La lógica de publicación**; no controla lo que una función de seguridad definer hace por dentro ni a los roles con BYPASSRLS |
| Privilegios (GRANT y REVOKE) | Que ningún rol de aplicación escriba directamente en los registros ni en `status` | La corrección de la función a la que sí se le concede |
| Aplicación y Edge Functions | Orquestación, mensajes, clave de idempotencia, correlación | Ninguna autoridad: nada que dependa de ellas es un control |


# PARTE 1.5 — Seguridad, permisos y RLS



---
<!-- ESPECIFICACION · líneas 1047-1062 · literal -->

### 8.7 Matriz de acceso por rol

Lo que el diseño **propone** conceder (todo lo demás está revocado). La verificación real de los privilegios exige infraestructura que no existe.

| Objeto | anon | authenticated | service_role | Propietario de funciones de estado (cci_state_owner) | Propietario de funciones de registros (cci_records_owner) | Roles internos de la plataforma (postgres, administración) |
|---|---|---|---|---|---|---|
| creative_pieces.status | Ninguno | SELECT por RLS; sin UPDATE | Sin UPDATE (revocado) | UPDATE (solo transition_piece_status) | Sin UPDATE | No se afirma control (RR-04) |
| creative_pieces, otras columnas | Ninguno | Según las políticas vigentes de v3.3 | Sin escritura directa | Lo necesario para la transición | Lo necesario para sus funciones | No restringido |
| publication_attempts | Ninguno | SELECT propio o con org.manage | Sin acceso de escritura; sin SELECT | INSERT | Sin INSERT | No restringido |
| impact_evaluations | Ninguno | SELECT según visibilidad de la adaptación | Sin escritura | Sin INSERT | INSERT | No restringido |
| piece_classification_events | Ninguno | SELECT según visibilidad de la pieza | Sin escritura | Sin INSERT | INSERT | No restringido |
| piece_reviewer_assignments | Ninguno | SELECT según visibilidad de la pieza | Sin escritura | Sin INSERT | INSERT | No restringido |
| approvals | Ninguno | SELECT según v3.3; sin escritura directa | Sin escritura | Lectura | INSERT (record_approval) | No restringido |
| EXECUTE de transition_piece_status | Ninguno | Sí | No | Propietaria | No | No restringido |
| EXECUTE de funciones de registros | Ninguno | Sí, con sus permisos de negocio | No | No | Propietaria | No restringido |


---
<!-- ESPECIFICACION · líneas 1063-1079 · literal -->

### 8.8 Demostración documental de las rutas de publicación

Es una demostración **sobre el diseño**: cada fila indica el mecanismo, la regla y la prueba, y si depende de infraestructura no verificada.

| Garantía | Mecanismo | Reglas | Pruebas | Depende de infraestructura no verificada |
|---|---|---|---|---|
| La única ruta que deja Publicado es la función transaccional autorizada | Único propietario con UPDATE(status) más guarda de trigger con db_txid | IS-01, IG10-21 | T-60, T-70 | Sí: roles y privilegios de Supabase |
| Ningún usuario actualiza status directamente | Revocación de UPDATE(status) a anon, authenticated y service_role | IS-02 | T-60 | Sí: privilegios por defecto |
| Ninguna función auxiliar publica | Propietario distinto sin UPDATE(status) ni INSERT en intentos | IS-03 | T-40, T-71 | Sí: creación de roles |
| La Edge Function no suplanta con una clave privilegiada | EXECUTE revocado a service_role; la función rechaza auth.uid() nulo | IS-04 | T-61 | Sí; y que las credenciales de administración no estén en la Edge Function |
| El actor sale de la identidad autenticada | auth.uid() dentro de la función; sin parámetro de actor | IS-05 | T-43 | Sí: modelo de sesión de la plataforma |
| Los registros no admiten escritura directa | Privilegios revocados más trigger | IS-06 | T-38, T-73 | Sí |
| RLS y privilegios se distinguen | RLS: lectura y aislamiento; privilegios y funciones: escritura y lógica | IS-07 | T-73 | No: es una distinción de diseño |
| C1 a C9 se verifican en backend | Dentro de la función, con datos del servidor | IS-08 | T-72 | No: diseño; Sí para probarlo |
| Una condición no verificable bloquea | Tres valores; solo cumple o no aplica permiten | IS-09 | T-33, T-46, T-50 | No |
| Un fallo de registro nunca habilita la publicación | Fila y estado en la misma transacción; guarda de trigger | IS-10, IG10-08 | T-34, T-57 | Sí: comportamiento real de la base |


---
<!-- ESPECIFICACION · líneas 516-519 · literal -->

### 4.9 Permisos de G-5

Ver matriz de permisos (sección 10). Resumen: asignar revisor `org.manage`; proponer independencia el autor o responsable; confirmar y evaluar `piece.review` con asignación e independencia; leer, quien puede ver la adaptación (RLS). Ninguna clave nueva.


---
<!-- ESPECIFICACION · líneas 690-700 · literal -->

### 5.6 Política de permisos y exposición

| Aspecto | Regla |
|---|---|
| Escribir | Nadie desde la aplicación: solo la función de transición (su propietario dedicado tiene la inserción) |
| Leer el propio intento | Cada actor ve sus filas: resultado, categoría, motivos y mensaje (DG-08) |
| Leer detalle completo | `org.manage`: condiciones, identificadores de versiones, aprobaciones y correlación (DG-08) |
| Qué se muestra al usuario | Categoría y códigos de motivo con mensaje, solo de datos que ya puede ver; no el contenido de justificaciones ajenas |
| Qué queda restringido | `condition_results` completo, `blocking_rule_refs`, `cited_versions`, `error_code`, `db_txid` y correlación |
| Sin secretos | No se guarda texto de excepciones, tokens, claves, dirección IP ni agente de usuario (DG-11) |


---
<!-- ESPECIFICACION · líneas 701-707 · literal -->

### 5.7 Retención y protección

- **Retención:** no se habilita borrado desde la aplicación y **no se define política de retención** (DG-09 diferida; no se propone plazo alguno). Cualquier depuración o archivo requiere una decisión futura expresa.
- **Protección:** privilegios revocados (anon, authenticated y service_role sin INSERT, UPDATE, DELETE ni TRUNCATE); trigger que rechaza UPDATE y DELETE; la función de transición es la única con inserción; RLS solo de lectura.
- **Hash encadenado:** diferido a la subfase 6.6 (DG-12); **no** es requisito de este diseño.
- **Límite honesto:** el propietario de la base o un superusuario de la plataforma puede alterar cualquier tabla; no se afirma protección contra ellos (RR-04).


---
<!-- ESPECIFICACION · líneas 1118-1148 · literal -->

## 10. Matriz de permisos y matriz RLS

### 10.1 Permisos

| Operación | Función propuesta | Permiso | Restricciones | Quién no puede |
|---|---|---|---|---|
| Crear adaptación | create_adaptation | channel.adapt (copy.write y asset.upload para el contenido) | Maestra de su organización y sin maestra propia | Quien no vea la maestra |
| Proponer independencia | propose_independence | Autor o responsable de la pieza (sin clave nueva) | No concede permisos | Cualquier otro |
| Confirmar, no confirmar o revertir | resolve_independence | piece.review del revisor asignado | Distinto del proponente; la reversión no procede si está Publicada | El proponente, Admin y el propietario por ese solo título |
| Asignar o retirar revisor | assign_reviewer | org.manage | El asignado debe tener piece.review; asignar no concede permisos | Quien no tenga org.manage |
| Evaluar impacto | record_impact_evaluation | piece.review y asignación vigente | Independiente de contribuyentes de V-A (con herencia) y de V-B; otro evaluador para levantar un bloqueo | Contribuyentes, Admin, propietario, cualquier rol sin asignación |
| Aprobar la adaptación | record_approval (existente) | piece.approve | Independencia con contribución heredada; la evaluación no la sustituye | Contribuyentes |
| Publicar | transition_piece_status | piece.publish | C1 a C9 | Cualquiera que incumpla una condición |
| Leer clasificaciones, asignaciones y evaluaciones | Consulta con RLS | content.read y visibilidad de la pieza | Mismos límites que la pieza | Otras organizaciones |
| Leer detalle de intentos | Consulta con RLS | org.manage; cada actor sus propios intentos | Sin clave nueva | Resto |
| Escribir en los registros | — | Ninguno | Solo las funciones | Todos los roles de aplicación |

Las 17 claves físicas quedan igual; ninguna operación requiere una clave 18. `delegation.manage` y `block.exception.revoke` siguen siendo capacidades conceptuales.

### 10.2 RLS

| Tabla | SELECT | INSERT | UPDATE | DELETE |
|---|---|---|---|---|
| piece_classification_events | Miembros que pueden ver la pieza (misma organización) | Sin política; solo la función | Sin política; privilegio revocado y trigger | Sin política; privilegio revocado y trigger |
| piece_reviewer_assignments | Ídem | Ídem | Ídem | Ídem |
| impact_evaluations | Miembros que pueden ver la adaptación | Ídem | Ídem | Ídem |
| publication_attempts | El propio actor, o quien tenga org.manage en la organización | Ídem | Ídem | Ídem |
| creative_pieces y copy_versions | Sin cambio de política | Sin cambio; las columnas de vínculo las valida la función y los triggers | master_piece_id inmutable; status solo por la función | Sin DELETE desde la aplicación |

RLS es **lectura y aislamiento**; la autoridad sobre la publicación es de la función, no de RLS (8.1).


# PARTE 1.6 — Pruebas nuevas (T-53 a T-73) y modificada (T-34)

| ID | Requisito cubierto | Condición inicial | Acción | Resultado esperado | Riesgo cubierto | Criterio de aceptación | Tipo | Reglas |
|---|---|---|---|---|---|---|---|---|
| T-34 | Fallo al registrar auditoría | Se fuerza una falla al insertar el intento | Publicar (que cumpliría todo) | Toda la transacción falla: A no queda Publicada y no existe fila confirmada | Publicar sin evidencia confirmada | Estado intacto; ninguna fila; la evidencia de plataforma, si existe, no se presenta como fila | Infraestructura real | IG10-08, IG10-11, IS-10, IG10-01 |
| T-53 | Evaluador con asignación de otra pieza | Revisor asignado a la adaptación A2, no a A1 | Registrar una evaluación de A1 citando la asignación de A2 | Rechazo por la FK compuesta con piece_id | Credencial de elegibilidad prestada | La FK falla; no queda fila | Ejecutable futura | IG5-21 |
| T-54 | Asignación retirada antes de evaluar | El revisor tuvo asignación y se registró su retiro | Evaluar citando la asignación antigua o la fila de retiro | Rechazo: no es una fila «asignado» ni es la vigente | Evaluar sin asignación vigente | Sin fila; el historial conserva ambas asignaciones | Ejecutable futura | IG5-22, IG5-23, IG5-08 |
| T-55 | Evaluador que perdió piece.review | La persona estaba asignada pero perdió el rol Revisor/Aprobador | Intentar evaluar | Rechazo por la comprobación de permiso bajo bloqueo de la membresía | Autoridad residual de una asignación | Sin fila; la asignación sigue en el historial | Ejecutable futura | IG5-24 |
| T-56 | Reasignación concurrente con evaluación | Evaluación en curso y reasignación del revisor simultáneas | Ejecutarlas a la vez | Se serializan por el mismo orden de bloqueo: gana una y la otra revalida; nunca queda una evaluación con asignación no vigente | Evaluación posterior a la reasignación | Resultado válido en cualquier orden; sin interbloqueo | Infraestructura real | IG5-25, IG5-23, IG5-08 |
| T-57 | Error de inserción de publication_attempts | Se fuerza una falla en la inserción del intento | Publicar un caso que cumpliría todo | La transacción falla: no hay Publicado ni fila confirmada. Si la plataforma conserva registros, la solicitud queda en ellos como evidencia de plataforma, nunca como fila de publication_attempts | Presentar evidencia externa como registro confirmado | Estado intacto; ninguna fila; la respuesta indica error y reintento | Infraestructura real | IG10-11, IG10-01, IS-10 |
| T-58 | Solicitud no autenticada | Llamada sin sesión válida | Intentar publicar | Rechazo; ninguna fila de negocio; evento de seguridad de la plataforma | Inventar un actor | No existe fila con actor nulo (actor_id es NOT NULL con FK) | Infraestructura real | IG10-19, IS-04, IS-05 |
| T-59 | Solicitud autenticada sin membresía | Usuario autenticado que no es miembro de la organización de la pieza | Intentar publicar | Rechazo; ninguna fila de negocio; RLS no le muestra la pieza | Publicar en otra organización | Sin fila y sin cambio de estado | Infraestructura real | IG10-19, IS-07 |
| T-60 | Llamada directa que intenta cambiar status | Sesión de usuario con piece.publish | UPDATE directo de creative_pieces.status | Rechazo por privilegios de columna; aunque se concediera, la guarda lo rechaza | Evadir C1 a C9 | Estado intacto | Infraestructura real | IS-02, IS-01, IG10-21 |
| T-61 | Edge Function que intenta utilizar identidad de servicio | Edge Function con la clave de servicio | Invocar la función de publicación o actualizar status | service_role no tiene EXECUTE ni UPDATE(status); la función rechaza auth.uid() nulo | Publicar «como sistema» | Rechazo en ambos caminos | Infraestructura real | IS-04, IS-02, IS-05 |
| T-62 | Publicación de una pieza cuya maestra cambió después de publicarse | A1 Publicada; la maestra M (no Publicada) cambia y se corrige | Intentar publicar A2, otra adaptación de M, y registrar la evaluación sobre A1 | A2 bloqueada por C3 a C6; A1 conserva su estado, artefacto y aprobación; la evaluación deja evidencia y aviso | Publicar con una maestra distinta de la aprobada | Sin transición nueva; 13 transiciones | Ejecutable futura | IP-02, IG5-20, IG5-17 |
| T-63 | Creación de nueva pieza tras una pieza publicada | M1 y A1 Publicadas | Crear M2 como nueva versión comercial y archivar M1 y A1 por #13 | M2 es otra pieza; M1 y A1 conservan versiones, aprobaciones e historial | Modificar una pieza Publicada | T-02 sin cambios; replaces_piece_id solo si se aprueba DG-18 | Ejecutable futura | IP-03, IP-01, IG1-24, IG1-20 |
| T-64 | Diferencia entre archivo interno y retiro de contenido externo | A1 Publicada y archivada por #13 | Consultar su estado interno y la disponibilidad externa | El archivo cambia el estado interno; no existe en el modelo ni se presume retiro externo; queda como dependencia operativa sin procedimiento documentado | Creer que archivar retira contenido | El diseño no afirma ningún retiro externo | Diseño | IP-04, IP-03 |
| T-65 | Canal y formato incompatibles con channel_rules | channel_rules del canal X con allowed_formats que no incluye F | Crear una pieza con canal X y formato F, o un canal inexistente | Rechazo por la FK del canal y por el trigger del formato | Piezas con canal o formato no definidos | Sin fila; con canal e formato válidos, se crea | Ejecutable futura | IG1-22 |
| T-66 | Dos adaptaciones con la misma clave | A1 activa con (M, canal, formato, clave k) | Crear A2 con la misma maestra, canal, formato y clave | Rechazo por el único parcial; con A1 archivada sí se permite | Adaptaciones indistinguibles | Violación de único; reaparece tras archivar | Ejecutable futura | IG1-23 |
| T-67 | Adaptaciones con claves diferentes en el mismo canal | A1 con clave a | Crear A2 con la clave b y la misma maestra, canal y formato | Conviven | Falsos rechazos | Dos filas activas | Ejecutable futura | IG1-23, IG1-13 |
| T-68 | Reintento tras una transacción abortada | La primera solicitud con clave k abortó sin fila | Reenviar con la misma clave k | Se evalúa desde cero y deja una fila | Quedar atrapado por una clave sin fila | Una fila; resultado actual | Ejecutable futura | IG10-20, IG10-01 |
| T-69 | Clave repetida con resultado bloqueado | Intento bloqueado con clave k; luego se corrige la causa | Reenviar con k; después con una clave nueva | Con k: el mismo resultado bloqueado almacenado; con la clave nueva: nueva evaluación | Que un reintento de red cambie el resultado, o que una corrección quede bloqueada | Dos filas con claves distintas | Ejecutable futura | IG10-20, IG10-06 |
| T-70 | Guarda y transacción | Existe una fila permitida de otra transacción para la misma pieza | Intentar cambiar status a Publicado fuera de esa transacción | Rechazo por db_txid distinto | Reutilizar un permiso antiguo | La guarda compara db_txid, pieza y versión | Infraestructura real | IG10-21, IS-01 |
| T-71 | Función auxiliar con intención de publicar | record_approval o review_finding bajo su propietario | Intentar UPDATE de status o INSERT en publication_attempts desde ellas | Rechazo por privilegios del propietario | Ruta alterna | Sin privilegio en el propietario de las auxiliares | Infraestructura real | IS-03, IS-01 |
| T-72 | Condiciones en la base de datos | Cliente que envía datos adulterados (versión, aprobación, resultado) | Publicar | Se ignoran; solo cuenta lo leído del servidor; V-E distinta bloquea por C9 | Confiar en el cliente | Ningún dato del cliente satisface una condición | Ejecutable futura | IS-08, IS-09, IS-05 |
| T-73 | RLS frente a privilegios | Usuario con política de lectura sobre las cuatro tablas | INSERT directo aunque la política lo permitiera | Rechazo por privilegio | Creer que RLS protege la escritura | Sin INSERT concedido; RLS solo SELECT | Infraestructura real | IS-07, IS-06 |



# PARTE 1.7 — Resumen de pruebas de la spec (11.1)



---
<!-- ESPECIFICACION · líneas 1229-1239 · literal -->

### 11.1 Resumen

| Concepto | Cantidad |
|---|---|
| Pruebas totales | 73 |
| Diseño | 4 |
| Ejecutable futura | 53 |
| Infraestructura real | 16 |
| Reglas de integridad | 84 |
| Reglas con al menos una prueba | 84 |


# PARTE 2.1 — Informe: decisiones DG, resumen de validación (84 reglas, 73 pruebas, 13 diagramas)



---
<!-- INFORME · líneas 20-42 · literal -->

## B. Decisiones incorporadas

| ID | Estado | Dónde se incorpora |
|---|---|---|
| DG-01 | APROBADA conceptualmente, sujeta a completar tipos, claves, restricciones y justificación | Completada en las secciones 3 a 5 y 9 (tipos de columnas, claves, únicos, CHECK, índices y justificación por elemento). Falta tu aceptación de la especificación |
| DG-02 | APROBADA | 3.4 y 3.13; reglas IG1-03 a IG1-07 |
| DG-03 | APROBADA | 3.1 y 3.6; IG1-15 y IG1-16 |
| DG-04 | APROBADA | 4.4 y 4.4.1; IG5-05 y IG5-06. El caso de versiones intermedias de la maestra no está en DG-04 (DG-17) |
| DG-05 | APROBADA | 4.1, 4.2; IG5-01 a IG5-03. Las precisiones de C3 a C5 (6.2) son consecuencia de DG-05; la v9 que contiene G-7 sigue sin aceptarse |
| DG-06 | APROBADA | 4.5; IG5-15 |
| DG-07 | APROBADA | `piece_reviewer_assignments`; 4.4. Cierra solo la asignación de revisor: **G-9 completo sigue abierto** |
| DG-08 | APROBADA | 5.6; IG10-15 |
| DG-09 | DIFERIDA; no se habilita borrado desde la aplicación y no se inventa política | 5.7 y IG10-18; se eliminó el plazo de la v1 |
| DG-10 | APROBADA | 5.3; IG10-01 y IG10-03 |
| DG-11 | APROBADA | 5.6; IG10-16 |
| DG-12 | DIFERIDA a la subfase 6.6; no es requisito del cierre del diseño actual | 5.7; fuera del modelo |
| DG-13 | APROBADA | C8 en 6.2; categorías inconsistencia_versiones e imposibilidad_verificar |
| DG-14 | APROBADA | 3.13; IG1-13 y IG1-23 |
| DG-15 | APROBADA | 6.3 y 7.12; IP-01 a IP-04; dependencia DEP-RET-01 para el retiro externo |
| DG-16 | DIFERIDA hasta resolver T-03; 30 y 10 caracteres siguen como **propuestas pendientes, no aprobadas** | Se marcan como propuestas en las tablas y reglas; ningún CHECK de longitud es decisión |

Ninguna decisión autoriza SQL, migraciones ni implementación. G-9 completo sigue abierto: DG-07 solo resuelve la asignación del revisor.


---
<!-- INFORME · líneas 84-94 · literal -->

## E. Validación

| Concepto | Resultado |
|---|---|
| Reglas de integridad | 84 (eran 59; +25) |
| Pruebas | 73 (eran 52; +21: las 15 solicitadas y 6 adicionales) |
| Diseño / Ejecutable futura / Infraestructura real | 4 / 53 / 16 |
| Cobertura | Toda regla tiene al menos una prueba; las 27 pruebas mínimas del primer encargo siguen cubiertas; las 15 nuevas cubiertas |
| Verificación por script | FK con aridad y destino que coincide con una clave única o primaria declarada; categorías, condiciones y reglas; 13 diagramas |
| Pruebas ejecutadas | Ninguna: todo es verificación documental |


---
<!-- INFORME · líneas 95-106 · literal -->

## F. Decisiones y pendientes

**Pendientes que se mantienen:** DG-09 (retención, sin plazo), DG-12 (hash, a 6.6), DG-16 (umbrales 30 y 10 pendientes de T-03), RP-01, P-01 a P-05, P-10, OD-13, PO-05 y la aceptación de la Adenda v9; G-9 completo.

**Precisiones nuevas con valor por defecto:**

| ID | Precisión | Recomendación | Efecto de no decidir |
|---|---|---|---|
| DG-17 | Independencia respecto de los contribuyentes de las versiones **intermedias** de la maestra entre V-D y V-B | Incluirlos (más estricto y coherente con «no evaluar su propia modificación») | Si no decides, el diseño aplica DG-04 literal (solo V-A y V-B). No bloquea |
| DG-18 | Columna opcional `replaces_piece_id` para ligar la pieza nueva con la anterior (DG-15) | Aprobarla | Sin ella el reemplazo solo se reconstruye por campaña o texto; el diseño funciona igual. No bloquea |
| DG-19 | Representar los formatos permitidos como columna `allowed_formats` de channel_rules (no como quinta tabla) | Columna | Los valores reales de canales y formatos siguen pendientes; el diseño no inventa ningún catálogo. No bloquea |


# PARTE 2.2 — Informe: riesgos y limitaciones



---
<!-- INFORME · líneas 107-129 · literal -->

## G. Limitaciones reales

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
| RR-17 | La columna que distingue aprobaciones de rechazos en approvals no está fijada en v3.3 |
| RR-18 | Los umbrales de 30 y 10 caracteres son propuestas pendientes de T-03 |


# PARTE 2.3 — Informe: archivos e integridad



---
<!-- INFORME · líneas 130-137 · literal -->

## H. Archivos

| Tipo | Archivos |
|---|---|
| Actualizados | `ESPECIFICACION_TECNICA_G1_G5_G10.md` (v2), `INFORME_CIERRE_G1_G5_G10.md`, `ROADMAP_Y_TRAZABILIDAD_G1_G5_G10.md`, `REGISTRO_HISTORICO_VERSIONES.md` (entrada nueva) |
| Conservados como histórico | las tres versiones v1 con sufijo `_v1_historica` o `_v1_historico` |
| No modificados | v3.3, Adenda v9, control, matriz, trazabilidad, auditoría, matriz de notificaciones y las demás versiones históricas |


---
<!-- INFORME · líneas 138-145 · literal -->

## I. Integridad

SHA-256 de v3.3: `b5dccdc73a8103966ab1e1b1e84b2e7ead68cd736fba666ec71d0e790d51c1da` (igual).

Se compararon los archivos .md de la línea base previa (78, incluidas las copias v1). Sin diferencias no previstas: sí. Modificados previstos: `ESPECIFICACION_TECNICA_G1_G5_G10.md`, `REGISTRO_HISTORICO_VERSIONES.md`, `ROADMAP_Y_TRAZABILIDAD_G1_G5_G10.md`. Las tres copias v1 son idénticas a las versiones entregadas antes.

Las 17 claves, las 27 tablas históricas, las 13 transiciones de T-02 y las 76 subfases no cambian; no existe subfase 77.


---
# PARTE 2.4 — Diagramas (títulos literales de la sección 7 de la spec; el informe solo los cuenta en E)

5:### 7.1 Crear una adaptación
23:### 7.2 Aprobar una adaptación
42:### 7.3 Modificar una maestra
59:### 7.4 Evaluar impacto
79:### 7.5 Reabrir una adaptación
94:### 7.6 Intentar publicar sin aprobación
108:### 7.7 Intentar publicar con impacto desconocido
123:### 7.8 Publicar correctamente
139:### 7.9 Fallo técnico durante la validación
155:### 7.10 Falla la inserción del intento (escenario C)
171:### 7.11 Solicitud sin autenticación o sin membresía (escenario D)
185:### 7.12 Cambia la maestra con una adaptación ya publicada (DG-15)
- Diagrama ER: sección 3.3 de la spec (13.º bloque mermaid).
