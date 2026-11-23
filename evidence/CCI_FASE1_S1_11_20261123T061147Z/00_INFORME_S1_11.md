# S1.11 — Cierre técnico de la Fase 1: anchos, navegadores, accesibilidad y CI (decisiones de Claude bajo delegación)

## Qué se hizo
- Pruebas de cierre en modo local: las 5 vistas en 7 anchos (320–1440): sin scroll horizontal, sin elementos fuera del viewport, controles ≥24 px, texto ≥16 px; axe (WCAG 2.2 AA) en todas las vistas con tema claro y oscuro sin errores de consola; recorrido solo con teclado.
- Defecto real encontrado y corregido: la vista Respaldo desbordaba (410 px en pantallas de 320–390 px) por el selector de archivo; se ajustó el CSS (`min-width:0`, ancho 100% del selector).
- CI (`.github/workflows/ci.yml`): ahora también corre en push a `main`; añade el paso "build de producción en modo local debe funcionar" y mantiene "producción con DEMO debe fallar". Solo lectura, sin secretos, sin despliegue.
- Decisiones aprobadas por delegación: el formato/límites/nombre del respaldo, que importar siempre reemplace, y `lastBackupAt` al generar el archivo.

## Verificación (logs en esta carpeta)
- typecheck, lint, format, secretos, build preview y build de producción local OK; 189 pruebas unitarias OK.
- Chrome real (Chrome for Testing 153): 72/72 en 3 corridas consecutivas.

## Límites
- Solo Chrome 153 disponible en este entorno: Edge, Firefox y Safari NO se probaron (hay que probarlos por separado; Playwright no pudo descargar navegadores).
- Sin dispositivos móviles reales ni lector de pantalla real; la accesibilidad se midió con axe (cubre solo parte de WCAG) y pruebas de teclado.
- El workflow de CI se publica con este commit; el resultado de su primera ejecución en GitHub se registra aparte si se consulta. Acciones @v4 sin anclar por SHA.
- Esto NO es la aceptación de la Fase 1: la aceptación requiere evidencia independiente y queda fuera de mi alcance.
