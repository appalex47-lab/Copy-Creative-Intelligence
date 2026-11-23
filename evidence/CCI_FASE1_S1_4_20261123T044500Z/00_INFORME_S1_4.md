# S1.4 — Repositorios y adaptador IndexedDB (decisiones de Claude bajo delegación)

## Hecho
- `src/repositories/contracts.ts`: contratos `ActivityRepository` y `ProfileRepository` (un fallo nunca se representa como dato vacío; fallos de almacenamiento → `unavailable` sin detalle interno).
- `src/adapters/memory/`: repositorios en memoria (referencia de comportamiento).
- `src/adapters/indexeddb/`: esquema v1 (almacenes `activity` con índice `at`, `profile`, `meta` con `schemaVersion`), repositorios y apertura/borrado de la base.
- **Un solo contrato, dos implementaciones (AC1-06):** `tests/support/repositoryContract.ts` (9 casos, sin dependencia de Vitest) se ejecuta contra memoria en Vitest y contra **IndexedDB real en Chrome** mediante un arnés (`e2e/idb.html`, fuera del build).
- Prueba por AST: `indexedDB`/`IDB*` solo dentro de `src/adapters/indexeddb/`.
- **Prueba de mutación:** invertir el sentido del cursor (`prev`→`next`) hizo fallar el contrato en el navegador por el orden; se restauró.

## Resultados
Vitest 148 pruebas; Playwright 37/37 en 3 corridas consecutivas (Chrome for Testing 153); typecheck, lint, formato, secretos y build sin errores.

## SUPUESTOS míos (reversibles)
El perfil local vive en IndexedDB (almacén `profile`, clave `local`); límite de lectura 1–500, por defecto 50; un registro de actividad corrupto se omite al listar en vez de romper la lista; el orden en empate es `id` descendente.

## No hecho todavía
Migraciones v0→v1→v2 con semillas y rechazo de una base de versión mayor (S1.5); conexión de la interfaz a los repositorios (el Resumen aún usa el adaptador DEMO); coordinación entre pestañas; cuota y almacenamiento persistente; códigos de error de persistencia dedicados (S1.7); Web Locks sin verificar.
