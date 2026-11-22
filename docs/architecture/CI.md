# Integración continua (preparada, NO publicada)

Archivo: `.github/workflows/ci.yml`. Está en el árbol local sin versionar: **no está habilitado ni publicado**; GitHub no lo ejecutará hasta que se autorice y se publique. Sin credenciales, sin secretos, sin Supabase, sin despliegue ni publicación de paquetes; permisos `contents: read`.
Controles que se ejecutarían (jobs `verify` y `e2e`): `npm ci` (lockfile), TypeScript, ESLint (incluye scripts y configuración), Prettier, Vitest (unitarias, componentes, arquitectura por AST, secretos, guarda de build), check de secretos, build preview, comprobación de que el build de producción **falla**, y en otro job Playwright + axe + responsive en Chrome.
Sin verificar: el YAML se validó solo sintácticamente (no con `actionlint` ni en GitHub); las acciones usan etiquetas mayores (`@v4`) y no se comprobó su vigencia; se asume Chrome preinstalado en `ubuntu-latest`.
