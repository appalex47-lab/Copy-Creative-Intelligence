# S1.6 — Perfil local, preferencias y tema (decisiones de Claude bajo delegación)

## Qué se hizo
- Modo de datos real `local` (IndexedDB para perfil/actividad + Local Storage solo para preferencias). Se activa con `VITE_DATA_MODE=local`; el modo por defecto sigue siendo `demo` y producción sin ese valor sigue rechazada.
- Pantalla "Perfil y preferencias": nombre visible opcional (validado, máx. 60, sin caracteres de control; mostrado escapado) y tema (sistema/claro/oscuro) que persiste y se aplica al arrancar.
- Local Storage solo en `src/adapters/localstorage/` (prueba AST nueva); la UI no puede importar `adapters/` (regla nueva con pruebas).
- Tokens de color con variante oscura; título "(DEMO)" y aviso solo en modo demo; página de conexión muestra el modo real.

## Verificación (ver logs en esta carpeta)
- typecheck, lint, format:check, check:secrets, build: OK. Vitest: 161 pruebas OK.
- Playwright en Chrome real: 48/48 en 3 corridas consecutivas (7 pruebas nuevas: persistencia tras recargar, borrado, validación/escape, tema persistente, axe claro/oscuro, anchos 320–1440).
- Mutación comprobada: forzar el tema 'system' al arrancar hace fallar la prueba de persistencia del tema.
- El test de teclado existente se ajustó (hay un botón de navegación más): 3 Shift+Tab en lugar de 2.

## Supuestos míos (reversibles)
Límite 60 caracteres del nombre; temas system/light/dark; clave `cci.prefs.v1`; vista `ajustes`.

## No verificado
Solo Chrome for Testing 153; sin Edge/Firefox/Safari; contraste en oscuro solo con axe; no hay revisión visual humana; CI de GitHub no ejecutado; sin despliegue.
