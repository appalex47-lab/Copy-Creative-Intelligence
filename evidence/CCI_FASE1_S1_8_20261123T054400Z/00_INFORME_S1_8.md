# S1.8 — Pantalla de almacenamiento (decisiones de Claude bajo delegación)

## Qué se hizo
- Vista "Almacenamiento": espacio usado, cuota y persistencia (navigator.storage.estimate/persisted), con botón "Solicitar almacenamiento persistente" (deshabilitado si ya es persistente o el navegador no lo informa).
- Lo que el navegador no expone se muestra "No disponible" (nunca se inventan cifras; DEMO tampoco las inventa). Valores no confiables → null.
- Acceso a `navigator.storage` solo en `src/adapters/storage/`; la UI usa el servicio `storage`. Fallos usan el catálogo de S1.7.

## Verificación (logs en esta carpeta)
- typecheck, lint, format, secretos, build OK; 176 pruebas unitarias OK.
- Chrome real: 54/54 en 3 corridas. Nuevas: cifras reales sin NaN/undefined + axe; navegador sin `navigator.storage` → "No disponible" ×3; cifras simuladas (5.0 MB / 2.0 GB) y persistencia concedida.
- Mutación: mostrar "0 B" en lugar de "No disponible" hace fallar pruebas unitaria y de navegador.
- Prueba de teclado ajustada (4 Shift+Tab por el nuevo botón de navegación).

## Supuestos míos (reversibles)
Unidades binarias (KB=1024); textos; botón deshabilitado cuando persisted es null; solo se muestra, no se advierte por umbrales de uso.

## No verificado
Cifras reales en otros navegadores; que el navegador conceda la persistencia (la concesión real depende de heurísticas de cada navegador; solo se simuló); Edge/Firefox/Safari; revisión humana de textos.
