# 04 — Matriz de trazabilidad AC1-01…AC1-14 (S1.0)
> Estado = hecho observado en el commit base (`7bcba74`) con las pruebas existentes. Texto de los criterios: `12_CRITERIOS_ACEPTACION_FASES.md` del expediente (AC1-14 es propuesto, derivado de P1). **PROPUESTA de organización; no aprobada.** «Subfase» usa los nombres propuestos S1.x (solo S1.0 está autorizada; S1.1 y S1.2 condicionadas).

| Criterio | Qué exige | Estado en la base | Evidencia | Subfase | Bloqueos |
|---|---|---|---|---|---|
| AC1-01 | Sin `fetch`/XHR/WebSocket/SDK de servidor en `src/` (prueba por AST) | **Parcial:** `src` no usa esas APIs, pero **ninguna prueba lo impone** (la de AST solo aísla Supabase) | F-05; `logs/test_run.txt` | S1.1 | — |
| AC1-02 | `tsc -b`, ESLint, Prettier sin errores ni advertencias; estricto y `noUncheckedIndexedAccess` | **Cumple hoy** (rc 0 en los tres; ambos modos activos) | `logs/typecheck.txt`, `lint.txt`, `format_check.txt`; `tsconfig.app.json` | S1.1 (mantener) | — |
| AC1-03 | Navegación, gestión de foco y enlace de salto; E2E | **Parcial:** enlace de salto, foco al encabezado y pruebas E2E existen; prueba de foco visible intermitente (2/6) | F-06, F-09; `logs/e2e_run*.txt` | S1.2 | catálogo de vistas |
| AC1-04 | Componentes reutilizables con pruebas y sin violaciones axe | **Parcial:** 4 componentes; axe corre en E2E, no en jsdom | F-08 | S1.2 | — |
| AC1-05 | Dominio inicial con validadores y pruebas unitarias | **No cumple:** el dominio existente es el provisional de la era Supabase | F-01 | S1.3 (no autorizada) | S1-D01, S1-D08, S1-D10 |
| AC1-06 | IndexedDB solo mediante adaptador; repositorios probados contra memoria **y** navegador real | **No iniciado** | F-04 | S1.4 (no autorizada) | S1-D13 |
| AC1-07 | Migraciones v0→v1 y v1→v2 con semillas; base de versión mayor rechazada sin escribir | **No iniciado; no especificable** con la documentación (ver `05_`) | `05_` | S1.5 (no autorizada) | S1-D13 |
| AC1-08 | Cada `AppErrorCode` de persistencia con mensaje, prueba y UI | **No iniciado:** 5 códigos genéricos, ninguno de persistencia | F-02 | S1.7 (no autorizada) | S1-D12 |
| AC1-09 | Preferencias en Local Storage validadas; nada fuera de la lista permitida | **No iniciado** | F-04 | S1.6 (no autorizada) | S1-D09 |
| AC1-10 | Pantalla de almacenamiento con uso/cuota/persistencia del navegador; E2E | **No iniciado** | F-04 | S1.8 (no autorizada) | — |
| AC1-11 | Command Center solo desde IndexedDB, estado vacío explícito, sin DEMO en el build de producción | **No cumple:** no hay Command Center ni build de producción posible (rechazado por la política) | F-03, F-07; `logs/build_production.txt` | S1.9 (no autorizada) | S1-D02, S1-D03, S1-D07, S1-D08 |
| AC1-12 | Persistencia tras recarga/reinicio; sin estado parcial tras transacción abortada | **No iniciado** | F-04 | S1.10 (no autorizada) | S1-D13 |
| AC1-13 | Responsive y axe | **Parcial:** pruebas responsive y axe E2E existen en Chrome 153; anchos concretos no fijados por el expediente | `e2e/responsive.spec.ts`; F-12 | S1.2 / S1.11 | S1-D14 |
| AC1-14 | Perfil local opcional; sin organización, membresía ni roles | **No iniciado;** además el código actual tiene los tres conceptos (F-01) | F-01 | S1.6 (no autorizada) | S1-D01, S1-D10 |

**Cobertura:** de las pruebas exigidas a S1.1/S1.2 (AC1-01, 02, 03, 04 y parte de 13), solo AC1-02 cumple hoy; AC1-01, 03, 04 y 13 están parciales.
