# Fase 3 — alcance y estado (2026-11-23)

Fuente: «Fase 3 — Inteligencia y auditoría creativa» (propuesta funcional recibida del propietario vía ChatGPT; **no aprobada para implementación** según el propio documento). Claude lo redactó como matriz; el propietario no lo ha validado. Por la delegación vigente, Claude decide qué construir, y se limita a lo que no depende de decisiones abiertas del documento.

| # | Función | Estado | Observación |
|---|---|---|---|
| 1 | Carga y gestión de recursos creativos | No construida | Formatos, tamaño, almacenamiento y conservación pendientes (subfase 3.1 del documento). |
| 2 | OCR | No construida | Motor y umbrales pendientes. |
| 3 | Análisis visual con IA | No construida | Modelo de visión pendiente; IA-B aprobada pero sin construir. |
| 4 | Auditoría de Copy | Construida (S3.1, solo reglas deterministas) | Foto guardada de la revisión por reglas de la versión vigente del copy. No incluye variantes ni adaptaciones (límite del documento). No evalúa persuasión ni coherencia con IA. |
| 5 | Auditoría de Creative Piece | No construida | Requiere recursos visuales y la entidad Pieza. |
| 6 | Detección y registro de hallazgos | Parcial (S3.1) | Los hallazgos se guardan dentro de cada auditoría con origen «regla determinista». Falta tipo de origen explícito (IA/humano), estados y resolución. |
| 7 | Puntuación | Parcial | Se usa la escala 0–100, pesos y rangos aprobados por el propietario el 2026-11-23 (Q-5). El documento recibido los llama «no aprobados»: contradicción a ratificar. No hay «dimensión no evaluable» ni cobertura mínima. |
| 8 | Comparación | Parcial (S3.1) | Cada auditoría se compara con la anterior del mismo copy (puntaje, hallazgos nuevos y resueltos). Falta comparar versiones de texto desde aquí, piezas y recursos visuales. |
| 9 | Consulta y seguimiento | Construida (S3.1–S3.2, sin exportación) | Historial por copy y vista global «Auditorías» con filtros por resultado, canal, fechas y texto. Faltan exportación y relación con la Biblioteca Creativa (pendientes del documento). |

## Decisiones de Claude en S3.1 (revocables)
1. Una auditoría guardada es inmutable: nunca se edita; se puede eliminar con confirmación (el documento exige que una nueva no borre la anterior, y así es).
2. Un copy con auditorías no se borra (`conflict`) hasta eliminarlas.
3. Se guarda el resultado, no una referencia viva: nombre del copy, versión, canal, puntaje, veredicto, hallazgos y conteos de las reglas usadas.
4. Hasta 5 000 auditorías; sin retención automática.
5. Respaldo v7 (`audits`), IndexedDB v7.

## Pendiente de decisión del propietario (del documento)
Formatos y tamaño de archivos, OCR y umbrales, modelo de visión, rúbrica y dimensiones definitivas, cobertura mínima, catálogo y severidad de hallazgos, comparación visual, conservación y relación de auditorías con versiones.

## S3.2
Vista global «Auditorías» (solo lectura, filtros). No se construyeron recursos creativos, OCR, IA visual ni Creative Piece: dependen de decisiones abiertas (formatos/tamaño, motor OCR, modelo de visión) y los archivos no cabrían en el respaldo JSON de 5 MB sin una decisión de almacenamiento.
