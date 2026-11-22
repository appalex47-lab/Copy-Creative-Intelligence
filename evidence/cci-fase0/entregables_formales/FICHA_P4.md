# Ficha P4 — Modelo de entidades del dominio (solo entidades; el alcance del MVP es Q-4)
Estado: **PARCIAL (2026-11-22; actualizado tras P4.1 y Q-7)** — lo pendiente está en `DECISIONES_P4_PENDIENTES.md`. Antes: P4.1 PENDIENTE (ver `LISTA_ORIGINAL_18_ENTIDADES.md`); P4.2 → (b); P4.3 respondida (Evento de actividad aprobada como entidad propuesta, Etiqueta y Perfil local aprobadas, Colección pendiente); P4.4 aplazado a Q-7; P4.5 posición preliminar. Detalle literal: `REGISTRO_DECISIONES_RESUELTAS.md`. P5 no se presenta hasta resolver P4 y Q-7.
**Nota:** el cuerpo de esta ficha es el planteamiento original; donde difiera, mandan las respuestas del propietario y `LISTA_ORIGINAL_18_ENTIDADES.md` (que corrige mi presentación de la lista). Por tu regla de separar dimensiones independientes, P4 se divide en cinco puntos que puedes responder **uno por uno**.
**Pregunta general:** ¿Apruebas las entidades, relaciones y responsabilidades de `05_MODELO_DOMINIO_CCI.md` y `06_MODELO_DATOS_CCI.md`?
## Contexto
- Tu instrucción enumera 18 entidades sin atributos ni clasificación. Tras P1 (sin identidad/organización/membresía/roles) y P3 (el vocabulario de `docs/fase0` es consultable, no vinculante), el modelo propuesto tiene **17 entidades de tu lista (con BrandRule y CommercialRule fusionadas) + 3 añadidas por mí**. Nada se implementa.
- La columna «Clase» (MVP/F3/F4/F5) depende de Q-4 y de las fases; **P4 no la aprueba**, solo entidades, relaciones y responsabilidades.
## P4.1 — Las entidades de tu lista (correspondencia)
| Tu entidad | Mi nombre | Fase prevista | Vocabulario histórico (referencia no vinculante) |
|---|---|---|---|
| Campaign | Campaña | 1–2 | `campaigns` |
| Brief | Brief | 2 | `briefs`, `brief_versions` |
| Product / Offer | Producto / Oferta | 2 (4 para validación) | sin equivalente claro por nombre |
| Copy / CopyVariant | Copy / Variante | 2 | `copy_versions` |
| ContentVersion | Versión (inmutable) | 2 | `copy_versions` |
| CreativeAsset | Pieza creativa | 3 | `creative_pieces`, `creative_assets` |
| CreativeAudit / AuditFinding | Auditoría / Hallazgo | 3 | `audits`, `audit_findings` |
| BrandRule / CommercialRule | **Regla (fusionada)** | 2–4 | `brand_guidelines`, `promotion_rules` |
| Channel / ChannelAdaptation | Canal / Adaptación | 4 | `channel_formats` |
| Approval | Aprobación (humana, usuario único) | 5 | `approvals` |
| PerformanceRecord / Metric | Resultado / Métrica (calculada) | 5 | `performance_metrics` |
| ApplicationSettings | Configuración | 1 | — |
**Opciones:** (a) aprobar la correspondencia y las responsabilidades tal cual; (b) aprobar con cambios por entidad; (c) rechazar. **Recomendación:** (a), con (b) donde quieras ajustar atributos. Consecuencia: define los almacenes de IndexedDB (`07`) y las pruebas de Fase 1–2; (c) bloquea el esquema inicial.
## P4.2 — `BrandRule` y `CommercialRule`: ¿una entidad o dos?
Tu lista tiene dos; mi propuesta las **fusionó** en `Regla` con ámbito. Fue una decisión mía, sin consultarte.
- (a) Una sola `Regla` con ámbito: menos tablas; mezcla reglas de marca (tono, palabras) con comerciales (tolerancias, condiciones) que tienen dueños y fases distintos.
- (b) **Dos entidades como en tu lista:** `ReglaDeMarca` (Fase 2–3) y `ReglaComercial` (Fase 4); el formato por canal vive en `Canal`.
**Recomendación razonada: (b)**: respeta tu lista y sus fases; Fase 2 solo necesita la de marca. Criterio mío, no verificado.
## P4.3 — Entidades que añadí y no están en tu lista
- **Evento de actividad:** necesaria para la «actividad real» del Command Center (R-011). Recomendación: aprobar.
- **Etiqueta** (y **Colección** en Fase 5): R-023 exige etiquetar y buscar en Copy Studio. **Corrección mía:** antes situé las etiquetas en Fase 5; deben estar en Fase 2 (ya corregido en `05` y `07`). Recomendación: aprobar.
- **Perfil local:** deriva de tu decisión P1; un nombre visible opcional. Recomendación: aprobar como tal.
Opciones por cada una: aprobar / rechazar / diferir. Rechazar una implica resolver su necesidad de otra forma (p. ej. el Command Center sin actividad real).
## P4.4 — Campaña y F11-D5
F11-D5 retiró `Project` sin `Campaign`; tu instrucción incluye `Campaña`. Esa tensión es la decisión **Q-7**, que sigue sin respuesta. Mientras no se decida, **la entidad Campaña no puede aprobarse en firme** (es padre de Brief, Oferta, Pieza y Resultado). Recomendación: responder Q-7 antes de cerrar este punto; el resto de P4 no depende de ello.
## P4.5 — Convenciones transversales del modelo
`id` UUID v4 generado en el cliente · fechas ISO-8601 UTC · `revision` entero para control optimista · borrado lógico con `archivedAt` · importes en enteros de unidad menor + moneda · lo desconocido es `null`, nunca un valor inventado · `Versión` inmutable con hash. Opciones: aprobar / cambiar. Recomendación: aprobar; son decisiones técnicas con efecto en migraciones y respaldo (`07`, `08`).
## Documentos y módulos afectados
`05`, `06`, `07`, `03` (R-005), `12` (AC1-05), `10_DEFINICION_MVP_CCI.md`, `INDICE_ANTECEDENTES_HISTORICOS.md`. Módulos: todos; Command Center y Copy Studio primero.
## Relación con decisiones anteriores
P1 (sin identidad/roles) y P3 (vocabulario no vinculante) ya resueltas; Q-7 (F11-D5) pendiente; Q-4 (MVP) pendiente y separada; F11-D5 sigue vigente hasta Q-7.
## Dependencias y efecto de no decidir
Antecede a P5 y a la aprobación 0.3. Sin respuesta, Fase 1 no puede crear el esquema inicial.
## Respuesta (por punto)
`P4.1 → … | P4.2 → (a)/(b) | P4.3 → Evento: … Etiqueta: … Perfil: … | P4.4 → (aplazado a Q-7) | P4.5 → …` — **pendiente**.

> **Nota fechada 2026-11-22 (auditoría cruzada):** «P4.4 aplazado a Q-7»: Q-7 se resolvió (a) y cerró P4.4. Estado vigente y fuente: `entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md`; P4.A 9/18 a la fecha de esta nota (**vigente actual: 18/18**, ratificación B1; ver `REGISTRO_DECISIONES_RESUELTAS.md`); D-1…D-8 resueltas en su alcance. Este documento se conserva como evidencia histórica.

> **Nota fechada 2026-11-22 15:56 (ratificación del propietario «Confirmo todo» sobre la propuesta maestra B1–B10; el texto original no se altera):** P4 quedó **RESUELTA** por la ratificación (P4.A 18/18, P4.B, P4.C, P4.E); el estado «PARCIAL» de esta ficha es antecedente. Fuente y texto literal: `entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md`, sección «Ratificación de la propuesta maestra de cierre de Fase 0 (B1–B10)». Aprobaciones 0.1–0.7, aceptación de Fase 0 y autorización de Fase 1 siguen pendientes.
