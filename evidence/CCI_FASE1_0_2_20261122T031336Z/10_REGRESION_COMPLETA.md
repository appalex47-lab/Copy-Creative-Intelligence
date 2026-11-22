# Regresión completa (ejecutada; logs en `logs/`)
Node 22.23.4, npm 10.9.9, Chrome 153. Primero en copia limpia (sin node_modules ni dist) y luego en el árbol de trabajo.
| Verificación | Estado |
| --- | --- |
| `npm ci` (copia limpia) | PASS |
| typecheck | PASS |
| ESLint (`eslint . --max-warnings 0`, incluye .mjs/.js) | PASS |
| Prettier | PASS |
| Vitest: 13 archivos / 130 pruebas (unitarias, componentes, arquitectura AST, secretos, guarda de build, DEMO, entorno, a11y semántica) | PASS |
| check:secrets | PASS (2 ZIP listados como no inspeccionados) |
| Verificación arquitectónica (AST) | PASS (dentro de Vitest) |
| `npm run verify` | PASS |
| build (preview) | PASS |
| `build:production` | FALLA por diseño (exit 1, mensaje claro) — comportamiento esperado |
| Navegador real (Playwright, 29 pruebas; ×3 = 87) | PASS |
| Accesibilidad automatizada (axe, 3 estados) | PASS (alcance automatizado) |
| Responsive (6 anchos × 2 páginas + error) | PASS |
| `npm audit` | PASS (0 vulnerabilidades) |
| CI en GitHub | NOT_TESTED (no publicado) |
| Lectores de pantalla / otros navegadores / dispositivos reales | NOT_TESTED |
| Supabase / SQL / despliegue | NOT_APPLICABLE (prohibido) |
Hash del JS del build preview (copia limpia): `c43d26afff1a14e3…`. Sin FAIL pendientes atribuibles a esta fase.
