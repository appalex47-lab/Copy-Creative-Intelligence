# S3.3 — Recursos visuales y OCR (Fase 3, funciones 1 y 2)

Resultado: `npm run verify` con código de salida 0; Playwright 90/90 en 3 corridas consecutivas.

## Qué se construyó
- Vista «Recursos»: agregar imagen (PNG/JPEG/WebP), vista previa del original sin modificar, OCR, texto «Detectado por OCR (no validado)» y texto «Validado por persona» (campos distintos), eliminar con confirmación.
- OCR con tesseract.js 5.1.1 (spa+eng) en el navegador. Worker, núcleo WASM y datos de idioma se sirven desde `public/ocr` (copiados por `scripts/copy-ocr-assets.mjs` en `postinstall`; carpeta fuera de git). El navegador no hizo ninguna petición externa en la prueba E2E.
- IndexedDB v8: almacén `resources` (blob + metadatos + OCR). No forma parte del respaldo JSON v7.
- Palabras con confianza < 60 se marcan como dudosas; nunca se completan ni corrigen.

## SUPUESTOS de Claude (reversibles; formatos y tamaños los fijará el propietario a mano)
PNG/JPEG/WebP, máx. 5 MB y 25 Mpx por imagen, 200 recursos, umbral 60, ampliación en memoria a ~3200 px de ancho (la copia ampliada nunca se guarda).
Todos están en `RESOURCE_LIMITS` (`src/domain/resource.ts`).

## No verificado
Precisión del OCR con banners reales; rendimiento en celulares; despliegue (no se desplegó).

## S3.3b — Respaldo de imágenes
Archivo aparte `cci-recursos-*.json` (base64 + SHA-256; tope 150 MB, SUPUESTO). Restaurar solo agrega lo que falta. Verify 0; Playwright 91/91 x3. No verificado: respaldos de cientos de MB en celular.
