# Resultados de regresión (ejecutados; logs en `logs/`)
Node 22.23.4 / npm 10.9.9.
| Prueba | Resultado |
| --- | --- |
| typecheck | PASS (exit 0) |
| ESLint (src, tests, scripts, configs) | PASS |
| Prettier (rutas de app) | PASS |
| Vitest 11 archivos / 79 pruebas | PASS |
| check:secrets (desde el repo y desde otro cwd) | PASS |
| build | PASS |
| `npm run verify` | PASS |
| dev server HTTP | 200 |
| preview HTTP | 200 |
| Escenarios de error (Result fallido, excepción, reintento, boundary, composición) | PASS (pruebas de componente) |
| DEMO sin autenticación ni persistencia (`Object.keys(identity)` = solo `getCurrentIdentity`; solo lectura; aviso DEMO) | PASS (pruebas existentes) |
| Sin dependencia Supabase | PASS |
| docs/fase0, evidencia/, AUDITORIA_*, expediente 1.0: intactos | PASS (git diff limpio; diff -r contra respaldo) |
Hash JS del build final: ver `logs/` (`8c3f31760d7854af…`, cambió respecto al build anterior porque cambió el código). Warnings: ninguno de código.
No ejecutado: E2E/navegador real, accesibilidad automatizada, `npm audit`, verificación visual.
