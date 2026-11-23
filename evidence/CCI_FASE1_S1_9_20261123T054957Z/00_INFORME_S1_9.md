# S1.9 — Centro de comando sobre IndexedDB y política de producción (decisiones de Claude bajo delegación)

## Qué se hizo
- Resumen (Inicio) muestra actividad REAL de IndexedDB (más nueva primero) o el estado vacío honesto; nunca datos inventados.
- Nuevo `activity.record(kind)`: se anota `app_opened` (una vez por carga, también bajo StrictMode), `profile_changed` y `setting_changed` solo tras un cambio correcto; un cambio rechazado no anota nada; si no se puede anotar, el cambio igual vale. El evento guarda solo tipo y hora (nunca contenido).
- Política de producción (decisión mía, reversible): producción solo arranca/compila con `VITE_DATA_MODE=local` explícito; DEMO queda rechazado por la política de entorno y, además, el adaptador DEMO y el aviso DEMO se eliminan del bundle de producción (AC1-11), comprobado en el bundle.
- DEMO no registra actividad.

## Verificación (logs en esta carpeta)
- typecheck, lint, format, secretos, build OK; 178 pruebas unitarias OK (incluye 2 pruebas de build: producción-local sin marca ni aviso DEMO; control: preview SÍ los contiene).
- Chrome real: 56/56 en 3 corridas consecutivas (nuevas: persistencia y orden de actividad tras recargar, sin contenido del usuario, validación rechazada no anota, axe).
- Mutación: omitir el registro tras guardar hace fallar la prueba de navegador.
- Corrección durante el trabajo: la prueba de build heredaba NODE_ENV=test de Vitest y empaquetaba React en desarrollo; se limpia NODE_ENV. La guarda usa `import.meta.env.MODE` (no PROD, que sería verdadero también en preview).

## Supuestos míos (reversibles)
Eventos anotados (3 de los 6 tipos; los otros llegan en S1.10/S1.8 según corresponda); el evento de la propia carga puede no verse hasta la siguiente carga (se lista en paralelo); producción exige modo local explícito.

## No verificado
Despliegue real (P10 abierto); Edge/Firefox/Safari; rendimiento con muchos eventos; que `app_opened` crezca sin límite (no hay purga; se lista con límite por defecto 50).
