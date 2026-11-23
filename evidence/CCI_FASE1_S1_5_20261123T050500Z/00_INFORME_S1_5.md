# S1.5 — Migraciones de esquema (decisiones de Claude bajo delegación)

## Hecho (adaptador `src/adapters/indexeddb/`)
- Migraciones como pasos ordenados; `SCHEMA_VERSION` = número de pasos (hoy 2).
  - **v0 → v1:** instalación nueva (v0 = no existe la base): almacenes `activity` (índice `at`), `profile` y `meta`.
  - **v1 → v2:** índice `kind` en `activity`. **SUPUESTO técnico mío (S1-D13, reversible):** la documentación no define v2; elegí un cambio que no añade atributos de negocio y que prueba la migración con datos reales.
- Una base de versión **mayor** se rechaza sin escribir (mensaje dedicado; código `unavailable`, ver límites).
- Una migración que falla **aborta la transacción**: versión, índices y datos quedan como antes (sin estado parcial).

## Pruebas (IndexedDB real en Chrome; bases construidas a mano, independientes del adaptador)
- v0 → v2 en instalación nueva; v1 → v2 con semillas (datos y perfil conservados, índice nuevo funcional, lectura por el repositorio); base v3 rechazada con su contenido intacto; migración que lanza → rollback.
- **Mutaciones:** quitar el `abort` hizo fallar la prueba de rollback; saltar la migración v0 hizo fallar la de instalación nueva. Ambas restauradas.
- Resultado: Vitest 148; Playwright 41/41 en 3 corridas consecutivas; typecheck, lint, formato, secretos y build sin errores.

## Límites
- La base real de un usuario nunca existió en v0/v1 (la app base no persistía): las semillas son fixtures sintéticas.
- No se definió un código de error propio para «versión más reciente»: va con el catálogo de S1.7 (AC1-08: mensaje, prueba y UI por código).
- No se probó la apertura concurrente desde dos pestañas durante una migración (`onblocked`/`versionchange`) ni Web Locks.
