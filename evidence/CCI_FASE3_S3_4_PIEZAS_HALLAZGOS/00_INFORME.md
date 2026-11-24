# S3.4 — Piezas creativas, hallazgos con estado, comparación y aviso de respaldo (cierre de Fase 3)
Resultado: `npm run verify` código 0; Playwright 93/93 en 3 corridas consecutivas.
- Vista «Piezas»: crear (nombre, canal, imagen de Recursos), auditar con reglas deterministas sobre el texto de la imagen, hallazgos con origen y estado (abierto/resuelto/descartado + nota), comparación con la auditoría anterior y tabla comparativa.
- IndexedDB v9 (`pieces`). Respaldo de imágenes v2 incluye piezas. «Respaldo» avisa lo que no incluye. Imagen en uso no se puede eliminar.
- Análisis visual con IA: NO construido (ver docs/decisions/FASE3_ALCANCE.md).
No verificado: precisión del OCR con banners reales; rendimiento en celular; despliegue.
