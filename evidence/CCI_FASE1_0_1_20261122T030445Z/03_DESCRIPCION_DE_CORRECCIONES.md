# Descripción de cada corrección
## 1. Detección de secretos (`scripts/check-secrets.mjs`)
- Escanea TODOS los archivos de la raíz (incl. dotfiles y `.env*`) + `src, tests, scripts, public, database, supabase, .github`; sigue sin recorrer `docs/`, `evidencia/`, `evidence/`, `AUDITORIA_*`.
- Detecta `.env`, `.env.local`, `.env.production`, etc. (en raíz y en directorios de la app); `.env.example` se escanea por contenido: pasa con valores vacíos/de ejemplo y falla con valores de aspecto real.
- Patrones nuevos: Cohere (por nombre de variable + valor ≥30), AWS, GitHub, Google API, Slack, sk-ant-, y asignación genérica `NOMBRE_(KEY|TOKEN|SECRET|PASSWORD…)=valor largo` con filtro de marcadores.
- Salida sin valores: solo archivo, línea y tipo. Independiente del cwd (raíz calculada desde la ubicación del script); acepta ruta opcional.
## 2. Control arquitectónico por AST (`tests/support/moduleReferences.ts`)
- Usa el AST de TypeScript (dependencia ya instalada): `import … from`, efecto lateral, `export … from`, `import x = require`, `import()` y `require()` (literal, concatenación, plantilla; prefijo estático si es parcial), `import type`, y literales `@supabase/*`. Ignora comentarios y cadenas de texto.
- Reglas: Supabase solo en `src/services/adapters/supabase/` (futuro, no existe); la interfaz no importa adaptadores, la fábrica ni `src/app` (alias o relativo) ni `import()` no resoluble; `src/app` no importa adaptadores.
- ESLint: `no-restricted-syntax` para `import()` de Supabase y excepción para el directorio del adaptador futuro.
## 3. Manejo de errores
- `useAsyncResource` (loading/success/error, captura `Result` fallido y excepciones, descarta respuestas tardías, reintento); `describeError`/`isRetryable` por código (el texto interno nunca se muestra; solo se registra el nombre del tipo de error).
- `HomePage` y `ConnectionPage` usan el hook; `ErrorNotice` (role=alert, botón Reintentar solo si es transitorio) y `LoadingNotice`; listas vacías legítimas se declaran ("ninguna"/"ninguno"), y un fallo ya no se disfraza de lista vacía.
- `ErrorBoundary` raíz (main.tsx) y por página (App); `createServices` lanza error explícito ante modo no soportado.
## 4. `src/types/`
`src/types/.gitkeep` versionable; documentación actualizada (también `lib` ya no figura como reservada).
Contratos de dominio sin cambios.
