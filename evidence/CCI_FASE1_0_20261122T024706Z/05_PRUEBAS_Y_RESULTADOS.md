# Pruebas y resultados (ejecutadas realmente; logs en `logs/*.log.txt`)
Entorno: Node 22.23.4, npm 10.9.9. `npm ci` OK (0 vulnerabilidades reportadas).
| Prueba | Resultado |
| --- | --- |
| typecheck (`tsc -b`) | PASS |
| ESLint | PASS |
| Prettier (solo rutas de app) | PASS |
| Vitest: 4 archivos, 19 pruebas (unitarias, componentes, arquitectura, secretos) | PASS |
| check:secrets (rutas de app) | PASS |
| build producción | PASS (dist ~224 kB JS) |
| `npm run verify` encadenado | PASS |
| dev server HTTP | 200 |
| preview HTTP | 200 |
| Sin dependencia Supabase (package.json y node_modules) | PASS (0 menciones; sin `node_modules/@supabase`) |
| DEMO identificado | PASS (prueba de App: aviso y nota) |
| Docs previas intactas | PASS (git diff: solo README.md; 0 borrados) |
Versiones exactas: react/react-dom 19.3.1, typescript 6.0.3, vite 8.3.8, @vitejs/plugin-react 6.3.0, vitest 5.1.1, jsdom 31.0.1, @testing-library/react 16.3.3, /dom 10.4.2, /jest-dom 8.0.0, eslint 10.15.0, @eslint/js 10.0.1, typescript-eslint 8.73.0, eslint-plugin-react-hooks 7.1.1, eslint-plugin-react-refresh 0.5.8, globals 17.14.0, prettier 3.10.1, @types/react 19.3.0, @types/react-dom 19.3.0, @types/node 22.20.5. package-lock sha256 `9a4e14a2…97aa47`.
Warnings: ninguno de código; vitest sugiere `isolate:false` (informativo).
NO ejecutado: pruebas en navegador real/E2E, accesibilidad automatizada, verificación visual responsive en dispositivo, `npm audit` contra registro, CI. Comprobación de integridad de `evidencia/` solo por conteo (31 archivos) y ausencia de operaciones sobre ella; no hay hash previo.
