# Fase 3 — alcance y estado (2026-11-23)

Fuente: «Fase 3 — Inteligencia y auditoría creativa» (propuesta funcional recibida del propietario vía ChatGPT; **no aprobada para implementación** según el propio documento). Claude lo redactó como matriz; el propietario no lo ha validado. Por la delegación vigente, Claude decide qué construir, y se limita a lo que no depende de decisiones abiertas del documento.

| # | Función | Estado | Observación |
|---|---|---|---|
| 1 | Carga y gestión de recursos creativos | Construida (S3.3, límites provisionales) | Vista «Recursos»: subir, previsualizar y eliminar imágenes PNG/JPEG/WebP (máx. 5 MB, 200 recursos: SUPUESTOS; el propietario fijará formatos y tamaños a mano en `RESOURCE_LIMITS`). Guardadas sin modificar en IndexedDB v8; NO van en el respaldo JSON. Un recurso no es una Pieza creativa. Retención y relación con la Biblioteca pendientes. |
| 2 | OCR | Construida (S3.3) | tesseract.js 5.1.1 (spa+eng) en el navegador, con núcleo, worker y datos de idioma servidos desde la propia app (`public/ocr`, copiados en `postinstall`); sin CDN ni red. Lo detectado se muestra aparte de lo «validado por persona»; palabras con confianza < 60 (SUPUESTO) se marcan como dudosas y nunca se corrigen solas. Falta probar con banners reales y afinar umbral. |
| 3 | Análisis visual con IA | NO se construye (decisión de Claude bajo delegación) | La app es solo-navegador y sin red (sin cuentas, backend ni claves): un modelo de visión exigiría enviar imágenes a un servicio externo. Se sustituye por revisión determinista local (OCR + reglas + resolución mínima). Revocable: requiere decidir proveedor, privacidad de las imágenes y rúbrica. |
| 4 | Auditoría de Copy | Construida (S3.1, solo reglas deterministas) | Foto guardada de la revisión por reglas de la versión vigente del copy. No incluye variantes ni adaptaciones (límite del documento). No evalúa persuasión ni coherencia con IA. |
| 5 | Auditoría de Creative Piece | Construida (S3.4, solo reglas deterministas) | Vista «Piezas»: pieza = recurso + nombre + canal; se audita el texto validado (o el detectado, con aviso) con las reglas de Reglas. No se aplican las reglas de CTA ni de longitud de campo a imágenes. Hasta 50 auditorías por pieza y 500 piezas (SUPUESTOS). No evalúa diseño, colores ni logotipos. |
| 6 | Detección y registro de hallazgos | Construida (S3.1, S3.4) | En piezas cada hallazgo tiene origen (regla / OCR / revisión de imagen) y estado que decide una persona (abierto, resuelto, descartado, con nota y fecha). En auditorías de copy siguen siendo foto sin estados. |
| 7 | Puntuación | Parcial | Se usa la escala 0–100, pesos y rangos aprobados por el propietario el 2026-11-23 (Q-5). El documento recibido los llama «no aprobados»: contradicción a ratificar. No hay «dimensión no evaluable» ni cobertura mínima. |
| 8 | Comparación | Construida (S3.1, S3.4) | Cada auditoría se compara con la anterior (puntaje, hallazgos nuevos y que ya no aparecen), en copys y en piezas; tabla comparativa de la última auditoría de cada pieza. Falta comparar versiones de texto desde aquí y comparación visual de imágenes (requeriría IA). |
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

## Decisiones de Claude bajo delegación (2026-11-23, revocables) — S3.3
- Formatos PNG/JPEG/WebP, máx. 5 MB y 25 Mpx por imagen, 200 recursos y umbral de palabra dudosa 60 quedan como valores vigentes (ajustables en `RESOURCE_LIMITS`).
- Retención: las imágenes se conservan en IndexedDB hasta que la persona las elimine; no hay caducidad automática.
- El propietario pidió que las imágenes se guarden en IndexedDB (ya es así). Siguen fuera del respaldo JSON (límite de 5 MB). El propietario pidió además un respaldo de imágenes: S3.3b lo agrega como archivo aparte `cci-recursos-AAAA-MM-DD.json` (base64 + SHA-256, tope 150 MB por archivo: SUPUESTO); al restaurar solo agrega lo que falta.
- Despliegue de S3.3 autorizado por el propietario.

## S3.4 — Piezas, hallazgos y comparación (decisiones de Claude bajo delegación, 2026-11-23, revocables)
- Piezas y recursos viven solo en IndexedDB v9; NO van en el respaldo JSON de datos. «Respaldo» avisa cuántas imágenes y piezas no incluye. Su respaldo es el archivo `cci-recursos-*.json` v2 (imágenes + piezas con sus auditorías; el v1 se sigue aceptando). Tope 150 MB (aprobado por el propietario).
- No se puede eliminar una imagen usada por una pieza.
- Puntuación (función 7): misma escala y pesos aprobados (Q-5) aplicados a los hallazgos de la pieza. Siguen sin existir «dimensión no evaluable» ni cobertura mínima: pendiente.
- Pendiente del propietario: rúbrica visual, modelo de visión (si se quiere), catálogo de hallazgos, exportación y relación con la Biblioteca Creativa.

## S3.5 — Exportación (decisión de Claude bajo delegación, revocable)
CSV de las auditorías de copy mostradas (Auditorías) y de las auditorías de piezas (Piezas): una fila por hallazgo, con origen, estado y nota en piezas. Sigue pendiente la relación con la Biblioteca Creativa.

## S4.2 — Aprendizaje, medición y promociones (decisiones de Claude bajo delegación, 2026-11-24, revocables)
- Se añadieron las vistas Biblioteca, Medición, Promociones y Plantillas, el flujo por etapas con aprobación final y el recordatorio semanal al abrir la app.
- Conversión = conversiones / clics. Experimentos A/B: prueba z de dos proporciones, muestra mínima 100, sin ganador si p ≥ 0.05.
- Promociones: tolerancia de porcentaje 0.5 pp (Q-1); filas del CSV con el mismo nombre se unen.
- «Llamadas» sigue fuera del catálogo de canales (Q-2); el propietario lo ratificó el 2026-11-24. El respaldo completo en un solo archivo (S4.3) fue aprobado por el propietario.
- Sin IA generativa, sin análisis visual automático y sin envío de datos fuera del navegador.
