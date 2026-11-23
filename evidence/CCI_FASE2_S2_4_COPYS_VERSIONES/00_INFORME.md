# CCI Fase 2 · S2.4 — Copys con historial de versiones

Decisión bajo delegación (revocable): copys como versiones inmutables append-only.

## Qué entra
- Dominio `copy` (titular, cuerpo, descripción, CTA; límites; etiquetas ≤8) con versiones inmutables; recuperar una versión crea una versión NUEVA (`restoredFrom`).
- Variantes = otros copys del mismo brief; «Duplicar como variante».
- IndexedDB v4 (`copies`); respaldo `cci-backup` v3 (acepta v1–v3; copys deben referenciar briefs del mismo respaldo).
- Un brief con copys no se elimina (`conflict`, mensaje en pantalla).
- Pantalla «Copys» desde cada brief: crear, editar (guardar nueva versión; sin cambios no crea versión), historial con campos cambiados, recuperar, duplicar, eliminar con confirmación.
- Fecha local legible (`es-MX`) en actividad.

## Verificación ejecutada
- `npm run verify`: exit 0 (prettier, eslint 0 warnings, tsc, 234 pruebas unitarias, secretos, build).
- Playwright completo, 3 corridas consecutivas: 80/80 en cada una (Chrome 153 del sistema). Incluye `e2e/copies.spec.ts` con axe sin violaciones en vacío, formulario e historial.

## Límites declarados
- Sin prueba en Edge/Firefox/Safari/móvil/lector de pantalla.
- Comparación visual entre versiones es solo lista de campos cambiados (diff detallado: S2.7).
- No se probó la pestaña de solo lectura específicamente sobre copys (la guarda `writable()` está cubierta en pruebas unitarias del servicio).
- Fallo intermitente no reproducido de S2.3 sigue abierto.
