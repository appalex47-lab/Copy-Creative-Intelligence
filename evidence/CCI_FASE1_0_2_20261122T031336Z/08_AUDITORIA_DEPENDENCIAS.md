# Auditoría de dependencias (registro oficial de npm, ejecutada)
`npm audit` (todas las dependencias): **0 vulnerabilidades** (info/low/moderate/high/critical = 0; 262 dependencias: 4 prod, 259 dev, 34 opcionales). `npm audit --omit=dev`: 0. Logs: `logs/npm_audit.txt`, `.json`.
`npm outdated`: solo `@types/node` 22.20.5 (latest 26.6.6) y `typescript` 6.0.3 (latest 7.0.2). No se actualizan: `@types/node` se mantiene en la línea del Node 22 que exige `engines`; TypeScript 7 es incompatible con el peer de typescript-eslint 8.73 (`<6.1.0`). Sin actualizaciones masivas ni cambios de versión mayor.
`npm ls --all`: exit 0 (solo dependencias opcionales de plataforma no instaladas, esperado).
Dependencias nuevas (devDependencies, versiones exactas): `@playwright/test` 1.65.1 y `@axe-core/playwright` 4.14.0 (transitivas: playwright-core, axe-core). Reproducibilidad: `npm ci` desde copia limpia OK.
Limitación: `npm audit` refleja la base de avisos en el momento de ejecución.
Resultado: PASS.
