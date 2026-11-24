# S3.1 — Auditorías guardadas de Copy

Fecha: 2026-11-23. Autor: Claude, bajo delegación del propietario («ejecuta la siguiente fase»). Decisiones revocables.

## Qué se construyó
Foto inmutable de la revisión por reglas de la versión vigente de un Copy: versión, canal, puntaje, veredicto, hallazgos y conteo de reglas usadas. Historial por copy, comparación con la auditoría anterior (puntaje, hallazgos nuevos y resueltos), eliminación con confirmación, y bloqueo del borrado de un copy con auditorías. IndexedDB v7 y respaldo v7.

## Alcance respetado (documento de Fase 3)
Solo Copy: sin variantes ni adaptaciones. Sin aprobación ni certificación. Sin OCR, IA visual ni imágenes (decisiones pendientes). Ver docs/decisions/FASE3_ALCANCE.md.

## Verificación
`npm run verify` salida 0 (300 pruebas unitarias); Playwright 87/87 en 3 corridas consecutivas (incluye 1 prueba nueva con axe).

## No verificado
Despliegue (no se desplegó), uso en móvil real, rendimiento con miles de auditorías.
