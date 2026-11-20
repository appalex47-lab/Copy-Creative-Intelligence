# REVISIÓN DE FUENTES FÍSICAS, K32, K45 Y K55 (V20)

**Versión:** V20 · **Fecha:** 2026-11-20 · **Fuente:** `ESPECIFICACION_TECNICA_G1_G5_G10.md` (definiciones de tablas, FK, CHECK, uniques), `herramientas/verificar_expediente.py` (K32, K45, K55 sin modificar), PostgreSQL temporal (`PE_POSTGRESQL_V20/`) · **Estado de verificación:** lectura estructural con análisis programático de columnas `*_id` contra el texto de las claves foráneas; el verificador publicado confirma K32/K45/K55 (59/59); no hay esquema físico real.

## 1. Método
Para cada una de las 13 tablas con bloque de definición propio (más `channel_formats`, definida en el bloque V20 de 3.14) se extrajeron las columnas `*_id` y `source_*` y se contrastó cada una con la sección «Claves foráneas», los CHECK y los triggers. Las que no figuraban se revisaron a mano.

## 2. Hallazgos y correcciones (V20)
| # | Tabla.columna | Defecto | Corrección en la especificación |
|---|---|---|---|
| 1 | `impact_evaluations.master_basis_creative_asset_id` | Sin FK ni mecanismo alternativo (la columna análoga de la adaptación sí tenía FK) | FK compuesta `(organization_id, master_piece_id, master_basis_creative_asset_id, master_basis_copy_version_id)` → `creative_assets(organization_id, piece_id, id, copy_version_id)` RESTRICT, MATCH SIMPLE |
| 2 | `impact_evaluations.master_changed_creative_asset_id` | Ídem | Ídem con `master_changed_copy_version_id` |
| 3 | `publication_attempts.master_declared_copy_version_id` | Sin FK ni justificación | FK `(organization_id, master_piece_id, master_declared_copy_version_id)` → `copy_versions(organization_id, piece_id, id)` |
| 4 | `publication_attempts.master_current_copy_version_id` | Ídem | Ídem |
| 5 | `publication_attempts.target_creative_asset_id` | Ídem | FK `(organization_id, piece_id, target_creative_asset_id, target_copy_version_id)` → `creative_assets(...)` MATCH SIMPLE |
| 6 | `brief_field_attributions.brief_id` | Sin FK: un `brief_id` podía discrepar del de `brief_version_id` | FK `(organization_id, brief_id, brief_version_id)` → `brief_versions(organization_id, brief_id, id)`; el destino `unique(organization_id, brief_id, id)` ya existía |
| 7 | `promotion_field_attributions.promotion_line_id` | Ídem | FK `(organization_id, promotion_line_id, promotion_snapshot_id)` → `promotion_snapshots(organization_id, promotion_line_id, id)`; destino ya existente |

Decisión de diseño: `publication_attempts.cited_versions` (jsonb, lo que el cliente citó) **no** lleva FK por diseño: es una evidencia del intento; las columnas resueltas por el servidor sí. No se añadió ninguna tabla, columna, permiso, rol ni transición; las FK reutilizan destinos únicos ya declarados. Son correcciones de integridad del diseño no aceptado; quedan sujetas a la aceptación formal de G-1/G-5/G-10.

Columnas revisadas que **no** requieren FK: `correlation_id` y `client_correlation_id` (identificadores de correlación generados, no referencias); `source_kind` (enumeración); `evidence_attribution_id` y `evidence_version_id` de `attribution_discard_resolutions` (mecanismo alternativo declarado: CHECK de igualdad con la atribución y trigger de versión; probado en PostgreSQL temporal, PG-AD-13 y PG-AD-14); las `source_*` de `contribution_events` y `used_asset_id`/`origin_asset_id` de `copy_version_provenance` tienen FK compuesta agregada (filas «columna agregada» del inventario, líneas ~1495–1500).

## 3. K32 (integridad referencial) — APRUEBA
Sin referencias polimórficas; cada columna `*_id` de las ocho tablas de procedencia, incluidas las `source_*`, tiene FK compuesta exacta (RS-01 a RS-xx). La corrección V20 amplía la cobertura a siete columnas adicionales de otras tablas. El verificador (sin modificar) sigue aprobando.

## 4. K45 (matriz semántica de relaciones) — APRUEBA
Matriz 4.4.10 con 27 mutaciones y 3 positivos ejecutados (30 resultados, dentro de los 366). Las FK nuevas de este apartado son relaciones adicionales; **no figuran en la matriz 4.4.10** porque pertenecen a tablas que esa matriz no modela (el modelo en memoria de K45 cubre procedencia y atribuciones). Limitación declarada: su efecto solo se prueba por lectura; no se añadió un caso a K45 porque el verificador no se modifica en esta pasada (ver pendiente en el informe).

## 5. K55 (consistencia modelo–especificación–pruebas) — APRUEBA
Sin duplicidades de reglas ni de escenarios (231 reglas únicas, 780 escenarios consecutivos, 1.592 pares regla↔escenario sin inconsistencia). Contradicción detectada y resuelta: el conteo de casos (363 frente a 366), ver `MATRIZ_PRUEBAS_22_FUNCIONES_366_CASOS.md`.

## 6. Inventario de fuentes físicas
Las catorce tablas nuevas (5 + 4 + 4 + 1) figuran en las líneas 38, 1301 (con `attribution_discard_resolutions`; fila 1270 en la numeración de V20) y 3656 de la especificación vigente. `version_contributors` reconstruye contribuyentes con las resoluciones aceptadas de `attribution_discard_resolutions` (referencia devuelta como causa del cambio de estado) y excluye resoluciones rechazadas; el conjunto E parte de las atribuciones activas; esta coherencia se prueba en memoria (K46/K47, ATTR-01..12) y las restricciones de la tabla en PostgreSQL temporal (PG-AD-01..20).

## 7. Qué no está verificado
Triggers de elegibilidad completa R1–R9 contra datos reales; RLS; privilegios; concurrencia; el esquema físico definitivo.
