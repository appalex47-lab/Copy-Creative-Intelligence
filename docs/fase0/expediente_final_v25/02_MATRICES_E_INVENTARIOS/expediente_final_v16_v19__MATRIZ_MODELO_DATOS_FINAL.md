# MATRIZ DEL MODELO DE DATOS FINAL (V20)

**Versión:** V20 · **Fecha:** 2026-11-20 · **Fuente:** `ESPECIFICACION_TECNICA_G1_G5_G10.md` (líneas 38, 1301 y 3656 de la especificación vigente —en V20 se citaban como 38, 1270 y 3620, numeración anterior a las últimas ediciones— y sección de `channel_formats`) y `MATRIZ_CONSISTENCIA_S1_V18.csv` · **Estado de verificación:** conteo y nombres verificados por lectura cruzada; el SQL no existe ni se ejecutó.

## Conteo reconciliado
- Tablas base de v3.3 (intactas): **27**.
- Tablas nuevas de G-1/G-5/G-10: **14** → 27 + 14 = **41**.
- Composición de las 14 (5 + 4 + 4 + 1): (1) `piece_classification_events`, `piece_reviewer_assignments`, `impact_evaluations`, `publication_attempts`, `channel_formats`; (2) `brief_versions`, `contribution_events`, `copy_version_provenance`, `promotion_snapshots`; (3) las cuatro tablas de cambio y atribución por campo material; (4) `attribution_discard_resolutions`.
- La línea 38 y la línea 3656 enumeran las 14; la fila 1301 («Fuentes físicas»; fila 1270 en la numeración de V20) omitía `attribution_discard_resolutions` y se corrigió en V20 («solo resoluciones aceptadas; paso 8 del procedimiento e IG5-92»).

## `channel_formats` (definición formal derivada, V20)
Columnas: `organization_id` uuid, `channel` text, `format` text, `active` boolean, `retired_at` timestamptz NULL, `created_at`, `created_by` (cada una marcada LITERAL o DERIVADA en la especificación). Restricciones: unicidad por organización/canal/formato, FK a `channel_rules`, FK derivada a `memberships`, CHECK de normalización, sin DELETE, RLS. **No determinados (no inventados):** clave primaria, índices, valores reales de canales y formatos (DG-19, pendiente de la organización).

## Límites
Sin SQL, migraciones, RLS, triggers ni infraestructura. La verificación de FK y restricciones es documental (FK01–FK41 y T-359..T-372 cruzados por lectura).

## Correcciones de integridad V20 (columnas `*_id` sin FK)
Una prueba estructural nueva (`evidencia_v16/pruebas_estructurales_v20.py`) detectó, sobre la especificación de c6ef74b, siete columnas sin FK ni mecanismo alternativo: `impact_evaluations.master_basis_creative_asset_id` y `master_changed_creative_asset_id`; `publication_attempts.target_creative_asset_id`, `master_declared_copy_version_id` y `master_current_copy_version_id`; `brief_field_attributions.brief_id`; `promotion_field_attributions.promotion_line_id`. Se añadieron FK compuestas (todas con `organization_id`, destinos únicos ya declarados), dos filas al contrato 4.4.9 y dos aristas al diagrama. Detalle y justificación de las excepciones (correlaciones, enumeraciones, CHECK/trigger alternativos): `REVISION_FUENTES_FISICAS_K32_K45_K55_V20.md`. Resultado sobre la especificación corregida: 4/4 pruebas (incluye 3 controles negativos); K14, K26, K32, K44, K45 y K55 del verificador siguen aprobando.

## Ejecución en PostgreSQL temporal
`attribution_discard_resolutions` (20 pruebas) y `channel_formats` (15 pruebas) se probaron con un fixture mínimo (`PE_POSTGRESQL_V20/`): 63/63 PASS en total con PE-01..PE-05, 14/14 mutaciones detectadas. No es el esquema físico aprobado.
