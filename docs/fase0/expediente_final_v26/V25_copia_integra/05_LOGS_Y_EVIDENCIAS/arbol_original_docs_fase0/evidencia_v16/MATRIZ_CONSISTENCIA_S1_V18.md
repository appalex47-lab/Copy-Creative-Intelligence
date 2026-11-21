# MATRIZ DE CONSISTENCIA S1 — LAS 14 TABLAS NUEVAS (V18)

> **Documento HISTÓRICO (V21, 2026-11-20):** evidencia de la etapa V16–V19 conservada tal como se produjo. Sus estados de publicación («local», «sin commit», «no publicado»), cifras (p. ej. 363 casos), clasificaciones de reglas (esquema V18/V19) y números de línea corresponden a la fecha de cada documento y **no** son el estado vigente. Estado vigente y fuente de verdad de cada dato: `../expediente_final_v21/INDICE_VIGENCIA_DOCUMENTAL_V21.md` y `../expediente_final_v21/MATRIZ_CONCILIACION_V21.md`.

Trabajo documental local posterior a V16; no publicado. Detalle por tabla en `MATRIZ_CONSISTENCIA_S1_V18.csv`. No se modificó el modelo ni el verificador.

**Confirmado**
- Las 14 tablas, con nombres exactos, sin duplicados: piece_classification_events, piece_reviewer_assignments, impact_evaluations, publication_attempts, channel_formats (v4); brief_versions, promotion_snapshots, contribution_events, copy_version_provenance (v5); brief_field_changes, brief_field_attributions, promotion_field_changes, promotion_field_attributions (v6); attribution_discard_resolutions (v7). 5 + 4 + 4 + 1 = 14; 27 históricas + 14 = 41.
- Línea 3620 (S1, corregida en V17): enumera 5 + 4 + 4 + 1 = 14, incluye attribution_discard_resolutions.
- Línea 624 (orden de creación) lista las 9 de v5–v7 con subfase; INFORME l.173 enumera las 14 completas.
- attribution_discard_resolutions: definida en ESPEC l.1089, creada en 5.3, citada en IG5-92 a IG5-98 y en la fila 78 de funciones (l.4905).

**Hallazgo nuevo S1b (corregido solo en local en V18):** la línea 38 decía «Catorce tablas nuevas» pero enumeraba 9 nombres + «las cuatro tablas de cambio y atribución» = 13 (omitía attribution_discard_resolutions). Se añadió el nombre; cambio de una frase, sin tocar decisiones.

**Observaciones sin corregir (no son contradicciones)**
- `channel_formats` no tiene tabla de columnas propia; su estructura se infiere de la FK compuesta y de IG1-22, IG1-26 y IG1-30 (ESPEC l.131, 269). Requiere decisión del propietario/diseño si se quiere una definición explícita antes de Fase 1.
- La fila «Fuentes físicas» (ESPEC l.1270) lista 9 fuentes sin attribution_discard_resolutions, mientras la fila 78 (l.4905) sí la incluye como fuente de `version_contributors`. Se deja como observación: podría ser intencional (fuente de procedencia vs. fuente de exclusión).
- Representación en el modelo en memoria: solo 6 de las 14 tablas aparecen por nombre en `modelo_estructural.py` (brief_versions, promotion_snapshots, contribution_events, copy_version_provenance, brief_field_attributions, promotion_field_attributions). Las otras 8 son diseño documental; no hay SQL ni migraciones. No se alteró el modelo para igualar la documentación.

## Actualización V19: auditoría de tablas (local; no publicado)

**`channel_formats` — clasificación: A, tabla física** (nueva). Evidencia textual: ESPEC l.38 la cuenta entre las catorce tablas nuevas; l.3603 («channel_formats es tabla nueva»); l.3620 (cinco nuevas de la v4); §3.14 («cuesta una tabla más»; creada en la subfase 1.8 antes de la primera pieza; l.3453); clave y destino de la FK `(organization_id, channel, format)` (l.131, IG1-22, IG1-26); baja lógica con `active = false` (IG1-29, l.357). No es lógica, embebida ni solo conceptual.
**Columnas obtenibles de la fuente existente (sin inventar):** organization_id, channel, format, active (IG1-29), retired_at y la trazabilidad created_by/created_at (§3.14, alternativa elegida; l.340 y l.357). No existen tipos ni una tabla de columnas formal. Se deja sin definir: requiere decisión de diseño/propietario antes de Fase 1.

**Fila «Fuentes físicas» (l.1270) — por qué omite `attribution_discard_resolutions`.** La fila pertenece al contrato de `version_contributors` (§4.4.5) y lista nueve fuentes. El control C-03 del verificador (l.331) la compara con «los bloques de las ocho tablas de 4.4.4», que explica que la lista esté acotada a esas tablas. Pero el procedimiento del mismo contrato (paso 8) y la categoría 3 sí leen/aplican `attribution_discard_resolutions`, y la fila 78 de funciones (l.4905), AUDITORIA l.127 y ROADMAP l.133 la incluyen como fuente. Conclusión: **discrepancia de representación dentro del contrato, sin prueba de que sea intencional.** No se corrigió: la fila está acotada por un control protegido (C-03/K12/K15/K16) y el verificador no se puede modificar; decisión de diseño pendiente. Corrección propuesta: añadir la tabla a la fila y adaptar C-03.

**27 + 14 = 41:** 22 reutilizables sin cambio (22 nombres contados en l.3620) + 5 con cambio (creative_pieces, copy_versions, channel_rules, creative_assets, approvals) = 27; 14 nuevas (5+4+4+1); total 41 (l.3620). Consistente.

**Representaciones contrastadas (14 tablas):** l.38 (corregida en V18), l.624, l.3620, l.1270, l.4905, INFORME l.173, AUDITORIA l.127, ROADMAP l.133, modelo en memoria (6 de 14 por nombre) y verificador. Discrepancias abiertas: solo la fila 1270. El modelo no se modificó. **El modelo de tablas NO se declara resuelto:** quedan channel_formats sin columnas formales y la fila 1270 sin decidir.

## Nota V20 (2026-11-19) sobre el estado de publicación

Las expresiones «local», «no publicado» y «sin commit» de las secciones anteriores describen el estado en la fecha de cada sección (histórico, no se borra). Desde entonces V16–V19 se publicó en la rama `audit/fase0-v19-review` (commit `c6ef74be4db185ac3e4fd36810f24619e6f51fcf`); `main` sigue en V16. El trabajo V20 está en el árbol local sin commit. Estado vigente y cierre: `../expediente_final_v16_v19/`.
