# PLAN DE VALIDACIÓN DEL TRIGGER DE ELEGIBILIDAD R1–R9 (IG5-95) — **NO EJECUTADO EN CCI-DEV**

**Fuente de las reglas:** especificación, sección 4.4.10-B (líneas 1585–1593) e IG5-95. **Estado:** diseño sin implementación física; el fixture V20 implementa sólo parte (ver §2).

## 1. Las nueve reglas y sus dependencias (derivadas por el revisor)

| Regla | Condición (literal de la especificación) | Tablas / datos de los que depende (derivación del revisor) |
|---|---|---|
| R1 miembro_activo | Miembro activo de la organización de la resolución | `memberships` (`activo`, org) |
| R2 piece_review | Tiene `piece.review` | `role_permissions`, `membership_permission_grants`, `memberships` (roles) |
| R3 no_afectado | No es el contribuyente afectado | `brief_field_attributions` / `promotion_field_attributions` (contribuyente) |
| R4 no_solicitante | No es quien solicitó la resolución | la propia fila de resolución (`requested_by`) |
| R5 no_actor_del_cambio | No es quien ejecutó la modificación material | `brief_field_changes` / `promotion_field_changes` (actor), `contribution_events` |
| R6 no_directo_en_cadena | No es contribuyente directo del campo en ninguna versión de la cadena | `brief_versions`/`promotion_snapshots` (cadena), atribuciones directas |
| R7 no_heredado_activo | No es contribuyente heredado activo | atribuciones con `previous_attribution_id` (heredadas) |
| R8 no_excluido_otra_fuente | No contribuyó a otra fuente de la cadena (copy, brief, promoción o arte) | `copy_versions`, `copy_version_provenance`, `creative_assets`, `contribution_events` |
| R9 no_beneficiario | Sin atribución activa en el campo ni participación en la operación del evento | atribuciones activas, `contribution_events` |

**Tablas dependientes identificadas:** `memberships`, `role_permissions`, `membership_permission_grants`, `contribution_events`, `brief_field_changes`, `promotion_field_changes`, `brief_field_attributions`, `promotion_field_attributions`, `brief_versions`, `promotion_snapshots`, `copy_versions`, `attribution_discard_resolutions` = **12**; añadiendo `copy_version_provenance` y `creative_assets` (R8 con arte) serían 14. *El encargo habla de «12 tablas dependientes»; esa cifra no aparece en las fuentes que revisé, y mi derivación da 12 si se excluyen las dos tablas de arte.* Confirmar con el propietario técnico.

## 2. Qué existe hoy (fixture V20, `PG-AD-08..10`)

| Regla | Mecanismo en el fixture | Prueba V20 | Brecha |
|---|---|---|---|
| R1 | FK compuesta (organization_id, resolved_by) → memberships | PG-AD-16..19 (FK) | **No comprueba `activo=true`** (EX-G9j muestra el mismo límite en otra tabla) |
| R2 | ninguno | — | Falta |
| R3 | CHECK `resolved_by <> affected_contributor_id` | PG-AD-08 | Sólo la comparación directa |
| R4 | CHECK `resolved_by <> requested_by` | PG-AD-09 | idem |
| R5 | CHECK `resolved_by <> change_actor_id` | PG-AD-10 | idem |
| R6, R7, R8, R9 | ninguno | — | Faltan; requieren reconstruir la cadena completa (IG5-95: «con el conjunto completo de contribuyentes y eventos de la cadena») |
| Evidencia, versión, sello | trigger `t_adr_ins` (EVIDENCIA_OTRA_VERSION, PREVIA_INVALIDA, SELLO_INVALIDO) | PG-AD-01..07, 11..15 | El sello usa `concat_ws('|',…)`: **ambiguo** (DEF-DG12-01, EX-DG12a/b) |

**Hallazgo:** R3–R5 como CHECK son comparaciones de igualdad de una fila; no pueden expresar «independiente de todas las personas de la cadena». R6–R9 exigen trigger/función con lectura de otras tablas (y por tanto sujeta a concurrencia: el conjunto de contribuyentes puede cambiar entre la lectura y el INSERT).

## 3. Condiciones de activación

El trigger debe activarse en `BEFORE INSERT` sobre `attribution_discard_resolutions`. IG5-98 dice que la resolución nace con un resultado definitivo (aceptada o rechazada). **Pregunta abierta para el diseñador:** ¿R1–R9 se aplican también a las resoluciones rechazadas? El escenario T-423 (r1 rechazada por evidencia vacía, con un resolutor independiente R) sugiere que sí; la especificación leída no lo afirma de forma explícita, por lo que el plan prueba ambos resultados y deja la decisión al propietario técnico.

## 4. Casos de prueba (por regla: positivo, negativo, frontera)

| Regla | Negativo | Positivo | Frontera |
|---|---|---|---|
| R1 | resolutor sin membresía; resolutor con `activo=false` | miembro activo | membresía desactivada **después** de la solicitud y antes de resolver |
| R2 | sin `piece.review` | con `piece.review` por rol; por grant individual | permiso revocado entre solicitud y resolución |
| R3 | resolutor = afectado | otro | afectado con dos atribuciones (campo distinto) |
| R4 | resolutor = solicitante | otro | solicitante que también es miembro con permiso |
| R5 | resolutor = actor del cambio | otro | actor que cambió otra versión de la cadena |
| R6 | contribuyente directo en una versión intermedia | no contribuyente | contribuyente directo sólo en la primera versión de la cadena |
| R7 | heredado activo | heredado histórico (ya retirado) | heredado con atribución previa en otra fuente |
| R8 | contribuyó al copy / arte que fija la versión | sin contribución en otras fuentes | contribución sólo a la promoción |
| R9 | atribución activa en el campo; participó en el evento | sin vínculo | atribución activa en otro campo (no cuenta) |
| Transversales | evidencia vacía; evidencia de otra versión; `created_by ≠ auth.uid()`; ninguna persona elegible → falla cerrada | todas se cumplen (R-ok) | nulos en columnas de cadena; cadena incompleta → falla cerrada (no «elegible por defecto») |

Plantilla ejecutable (NO EJECUTADA): `scripts_validacion/cci_dev_NO_EJECUTADOS/04_trigger_r1_r9_ROLLBACK.sql`.

## 5. Pruebas de regresión

1. Re-ejecutar PG-AD-01..20 y las 14 mutaciones MUT sobre el esquema físico (adaptando el fixture) tras añadir R6–R9: ninguna debe cambiar de resultado.
2. Mutación nueva por regla: quitar la comprobación Rk del trigger y verificar que la prueba negativa Rk pasa a FAIL (patrón V20; evita pruebas que siempre pasan).
3. Equivalencia con el modelo en memoria: las mutaciones `K47-M27..M36` (R1..R9 y no aplicar R*) deben tener su equivalente físico.

## 6. Concurrencia

- **Condición de carrera principal:** dos resoluciones simultáneas (o una resolución y un cambio de atribuciones) con el mismo conjunto de contribuyentes: el trigger lee el conjunto y otro proceso lo modifica antes del INSERT. Mitigaciones a validar: bloqueo `FOR UPDATE`/`FOR SHARE` de las filas de atribución afectadas o aislamiento SERIALIZABLE; índice único parcial `u_adr_aceptada` como última barrera.
- Prueba CONC-03 (dos `aceptada` para la misma atribución) y variante con resolutores distintos.

## 7. Criterios de aceptación

1. Cada R1–R9: negativo → rechazo con el código/mensaje específico; positivo → OK.
2. Cadena incompleta o conjunto de contribuyentes no determinable → rechazo (falla cerrada).
3. Ninguna persona elegible → rechazo y la atribución permanece activa.
4. Mutación de cada Rk detectada (9/9).
5. Sin escritura directa de `authenticated`/`service_role` (sólo función con propietario `cci_records_owner`).
6. Resultados archivados con SHA-256 de scripts y salida íntegra.

## 8. Dependencias de decisión

IG5-95 es clase D (diseño no aceptado, G-5): este plan **no** convierte el diseño en aceptado. Depende también de DT-01/PC-02 (representación física de contribuciones) y de la autoridad que registra la asignación de revisor (G-9).
