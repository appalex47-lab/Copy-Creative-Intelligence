# Pruebas

`npm run typecheck`, `lint`, `format:check`, `test:run` (unitarias, de componentes y de arquitectura), `check:secrets`, `build`; `npm run verify` las encadena. `check:secrets` escanea los archivos de la raíz (incluidos `.env*`) y los directorios de la app, funciona desde cualquier directorio, acepta una ruta opcional (`node scripts/check-secrets.mjs <ruta>`) y nunca imprime valores. Las herramientas (formato, lint, secretos) se limitan a rutas de la app y no recorren `docs/`, `evidencia/` ni `AUDITORIA_*`. No hay pruebas contra backend ni E2E de navegador en esta fase.

## Navegador real (Fase 1.0.2)

`npm run test:e2e` (Playwright con el Google Chrome instalado, sin descargar navegadores; `CCI_CHROME_PATH` para otra ruta): arranque, navegación, teclado, foco visible, axe-core (WCAG 2.x A/AA y best-practice), estados de carga/error/reintento, Error Boundary, StrictMode, respuestas tardías y cambio de página, y responsive en 360/375/390/768/1024/1440 px con capturas (`CCI_EVIDENCE_DIR`). Usa el build preview (`vite preview`) y el servidor de desarrollo con el arnés `e2e/harness.html` (no forma parte del build). `npm audit` y `npm outdated` se ejecutan aparte.
