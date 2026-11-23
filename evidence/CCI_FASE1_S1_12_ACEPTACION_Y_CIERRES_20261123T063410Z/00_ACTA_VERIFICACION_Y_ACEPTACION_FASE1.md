# Acta de verificación y aceptación de la Fase 1 (decisión de Claude bajo delegación, revocable)

**Fundamento:** el propietario delegó la aceptación («Tú la debes hacer», 2026-11-23 00:26) tras la delegación general del 21:28/21:43. **Naturaleza:** verificación PROPIA (no independiente); por eso la aceptación es **CON RESERVAS** y el propietario puede revocarla o exigir una revisión externa.

**Resultado: Fase 1 ACEPTADA CON RESERVAS.** Estado verificado: commit de `main` que incluye este acta; 193 pruebas unitarias; 75 pruebas E2E en Chrome real, 3 corridas consecutivas 75/75; CI real de GitHub verde (run 45123455827 y posteriores).

## Criterios AC1-01…AC1-14
| Criterio | Resultado | Evidencia |
|---|---|---|
| AC1-01 sin fetch/XHR/WebSocket/SDK (AST) | Cumple | S1.1: `tests/networkApis.test.ts`, `tests/support/networkApis.ts` |
| AC1-02 tsc/ESLint/Prettier sin errores | Cumple | `logs/verificacion_estatica.log` (cada subfase) |
| AC1-03 navegación, foco, enlace de salto, E2E | Cumple | `e2e/app.spec.ts`, `e2e/closing.spec.ts` (teclado); intermitencia diagnosticada y corregida (S1.2) |
| AC1-04 componentes con pruebas y axe | Cumple | S1.2: `componentes.test.tsx`, `e2e/components.spec.ts` |
| AC1-05 dominio con validadores y pruebas | Cumple | S1.3: `domainFase1.test.ts`; también `backup.test.ts`, `storageInfo.test.ts` |
| AC1-06 IndexedDB solo por adaptador; repositorios probados en memoria y navegador real | Cumple | S1.4: `tests/indexedDbIsolation.test.ts`, contrato compartido, `e2e/indexeddb.spec.ts` |
| AC1-07 migraciones v0→v1→v2, versión mayor rechazada sin escribir | Cumple | S1.5: 4 pruebas en IndexedDB real + mutaciones |
| AC1-08 cada código de persistencia con mensaje, prueba y UI | Cumple (6 códigos: unavailable, blocked, quota, newer_schema, failed, read_only) | S1.7 y S1.12 |
| AC1-09 preferencias en Local Storage validadas, lista permitida | Cumple | S1.6: `preferencesStore.test.ts`, `tests/localStorageIsolation.test.ts` |
| AC1-10 pantalla de almacenamiento (uso/cuota/persistencia) | Cumple (valores reales del navegador o «No disponible») | S1.8 |
| AC1-11 Command Center desde IndexedDB, vacío explícito, sin DEMO en producción | Cumple | S1.9: bundle de producción sin adaptador/aviso DEMO (`tests/buildGuard.test.ts`) |
| AC1-12 persistencia tras recarga; sin estado parcial tras transacción abortada | Cumple | S1.10: `e2e/indexeddb.spec.ts` (aborto a mitad), `e2e/backup.spec.ts` |
| AC1-13 responsive y axe | Cumple en Chrome (7 anchos, 5 vistas, ambos temas) | S1.11: `e2e/closing.spec.ts` |
| AC1-14 perfil local opcional sin organización/membresía/roles | Cumple | `src` sin esas entidades (verificado por búsqueda); S1.3/S1.6 |

## Decisiones resueltas que Fase 1 debía honrar
- P9 (producción = persistencia local real, DEMO identificado): cumplida (S1.9).
- **P12 (una pestaña escribe, las demás solo lectura, con aviso visible y recuperación del permiso):** estaba **sin implementar**; se implementó en S1.12 con Web Locks, falla conservadora sin Web Locks, sin «robar» el control; probado con dos pestañas reales (3 pruebas E2E + 4 unitarias + mutación).
- P11 (Chrome primario completo; Edge validación específica; Firefox sujeto a pruebas; Safari mejor esfuerzo): **solo Chrome 153 verificado** (ver reservas).
- P13 (dependencias mínimas, `AppErrorCode` solo con errores reales): no se añadieron dependencias de ejecución; los códigos nuevos corresponden a fallos observables reales.

## Reservas (por qué es «con reservas»)
1. Verificación no independiente (la hizo quien implementó).
2. Edge, Firefox y Safari sin probar; móviles reales y lector de pantalla real sin probar; axe cubre solo parte de WCAG.
3. Revisión humana de textos y del tema oscuro pendiente.
4. P12: solo se probó con Chrome; Web Locks no verificado en otros navegadores; no hay prueba del caso «el navegador mata la pestaña escritora».
5. El respaldo no está cifrado (P7 aplazado) y su suma SHA-256 detecta daños, no manipulación.
6. Documentación de arquitectura vieja (p. ej. `docs/decisions/DECISIONES.md`, D3 Supabase) sin actualizar (S1-D04); `evidence/cci-fase0` no refleja las rondas posteriores al 21:28.
7. La aceptación no despliega nada ni autoriza la Fase 2.
