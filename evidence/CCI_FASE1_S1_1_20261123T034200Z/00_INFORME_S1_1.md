# S1.1 — Arquitectura por capas: informe de ejecución (parcial)

**Base:** `5bd5c2a`. **Perímetro:** autorización del 2026-11-22 20:59; S1.1 activada por la aprobación delegada registrada en `../CCI_FASE1_S1_0_DECISIONES_DELEGADAS_20261123T033116Z/`.

## Qué se hizo (solo pruebas y soporte de pruebas; ningún archivo de `src/` cambió)
1. **AC1-01:** `tests/support/networkApis.ts` y `tests/networkApis.test.ts`. Detector por AST de `fetch`, `XMLHttpRequest`, `WebSocket`, `EventSource`, `WebTransport`, `navigator.sendBeacon`, accesos por `window`/`globalThis`/`self` (incluido con corchetes), alias (`const f = fetch`) y módulos de clientes de red (axios, ky, ws, socket.io-client, `@supabase/*`, etc.). Escanea todo `src/` fuera de pruebas.
2. **Dirección de dependencias:** nueva regla en `tests/support/moduleReferences.ts`: el dominio no importa otras capas; los contratos solo importan dominio y contratos. Tres pruebas nuevas en `tests/moduleReferences.test.ts`.

## Resultados (logs en `logs/`)
- `tsc -b`, ESLint (`--max-warnings 0`), Prettier, `check:secrets`, build en modo preview: rc 0.
- Vitest: 141 pruebas pasan (base: 130; +11).
- **Prueba de mutación manual:** se plantó `fetch('/a')` en `src/lib/zz_mut.ts` y la prueba AC1-01 falló señalando `lib/zz_mut.ts:1 fetch`; el archivo se retiró y la rama quedó limpia.

## Qué NO se hizo / límites
- No se creó la capa de aplicación ni carpetas nuevas: sin casos de uso reales sería un cascarón vacío. Se difiere a S1.3, cuando haya dominio que orquestar (decisión mía; no aprobada por el propietario como tal).
- No se tocaron dominio, contratos, adaptadores, `AppErrorCode`, documentación ni configuración.
- Pruebas hechas por la misma sesión que las diseñó: sin revisión independiente. El detector es heurístico por nombres: no ve llamadas construidas dinámicamente (p. ej. `globalThis[nombre]`).
- CI no ejecutado.
