# Verificación ejecutada en esta fase (primera mano)
Objeto: instantánea exacta del commit `ffb47bc319db0806250bcecf91d390fa59fa0d70` (obtenida con `git archive` en una copia temporal fuera del repositorio; `package-lock.json` idéntico al del `node_modules` preexistente, enlazado por symlink; **no se instaló nada**). Entorno: Node v22.23.4, npm 10.9.9, Google Chrome for Testing 153.0.8010.12 (Playwright `channel: 'chrome'`), Linux. Fecha: 2026-11-22.
| Comando | Estado | Resultado exacto | Log |
|---|---|---|---|
| `npm run typecheck` | **aprobada** | exit 0 | `logs/typecheck.log` |
| `npm run lint` | **aprobada** | exit 0 (`--max-warnings 0`) | `logs/lint.log` |
| `npm run format:check` | **aprobada** | exit 0 | `logs/format_check.log` |
| `npm run check:secrets` | **aprobada** | exit 0 (heurístico) | `logs/check_secrets.log` |
| `npm run test:run` | **aprobada** | 13 archivos, **162 pruebas aprobadas / 162** | `logs/test_run.log` |
| `npm run build` (preview) | **aprobada** | exit 0 | `logs/build.log` |
| `npm run build:production` | **aprobada como fallo esperado** | exit 1: «Configuración de entorno rechazada (production)…» | `logs/build_production_esperado_FALLO.log` |
| `npm run test:e2e` corrida 1 | **aprobada** | 29 aprobadas / 29, 20.8 s | `logs/e2e_corrida1.log` |
| `npm run test:e2e` corrida 2 | **aprobada** | 29 / 29, 19.8 s | `logs/e2e_corrida2.log` |
| `npm run test:e2e` corrida 3 | **aprobada** | 29 / 29, 19.9 s | `logs/e2e_corrida3.log` |
Resumen de tiempos y exit codes: `logs/resumen_1.txt`.
## Limitaciones
- Corresponde a **una máquina**, Chrome for Testing 153 (no Firefox/WebKit/Edge); 3 corridas E2E no demuestran ausencia total de intermitencia (reserva causal ya documentada en el expediente E2E).
- `npm audit` y CI en un runner real: **no ejecutados**.
- La infraestructura verificada no prueba ninguna funcionalidad de producto (no existe).
- No se generaron capturas nuevas; las existentes están en `evidence/CCI_FASE1_0_2_20261122T031336Z/capturas/` (15 PNG).
## Reproducción
`git archive <commit> | tar -x -C <dir>`; enlazar `node_modules` instalado con el mismo `package-lock.json` (o `npm ci` en un entorno autorizado); `npm run typecheck && npm run lint && npm run format:check && npm run check:secrets && npm run test:run && npm run build`; `npm run build:production` debe fallar; `CI=true npm run test:e2e` ×3.
Nota: los logs contienen rutas temporales de la copia de verificación (p. ej. `/tmp/f0_verify`); son rutas del entorno, no datos sensibles.
