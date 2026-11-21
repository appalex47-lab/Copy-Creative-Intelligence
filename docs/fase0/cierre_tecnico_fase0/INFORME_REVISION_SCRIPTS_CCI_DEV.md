# REVISIÓN INDIVIDUAL DE LOS SEIS SCRIPTS CCI-DEV (v2)

**Estado de todos: NO EJECUTADOS contra CCI-DEV/CCI-PROD.** La revisión es estática + ejecución local (PostgreSQL 16.15 temporal, shim/fixtures locales). Nada de esto valida Supabase. Escáner: `ct_escaner_seguridad_sql.py` (115 comprobaciones SQL, 0 FAIL; autoprueba 26/26). Ver también `INFORME_SEGURIDAD_SCRIPTS.md`, `PROPUESTA_CONTRATO_ERRORES_R1_R9.md`, `PROPUESTA_GUARDA_DEV_PROD.md`.

## 1. Tabla de revisión (por script)

| Atributo | 01 inventario | 02 RLS/privilegios (lectura) | 03 pruebas RLS | 04 R1–R9 (+lib) | 05 A / 05 B |
|---|---|---|---|---|---|
| Tipo | `begin read only` … `rollback`; solo catálogos | ídem | escritura en transacción con `rollback`; sub-bloques revertidos | ídem; cada caso en sub-bloque revertido por excepción centinela `CC999` | A inserta fila sin confirmar, espera 5 s, `rollback`; B intenta lo mismo y mide la espera |
| Guarda | sí (compartida: `00_guarda_destino.sql`) | sí | sí | sí | sí (ambas) |
| Precondiciones | ninguna de datos | ninguna de datos | PRE: tablas, columnas, filas de **ambas** organizaciones (no vacuidad) | PRE-01..10: versión ≥13, función y firma exacta, tablas, columnas, CHECK, trigger BEFORE INSERT, EXECUTE del rol, datos PRE-09a–f, contrato | existe `piece_reviewer_assignments` (si no `\quit`+BLOCKED) |
| Dependencias | catálogos estándar | `pg_class`, `pg_policies`, `has_table_privilege` | tablas con `organization_id`, roles `anon/authenticated/service_role`, GUC `cci.org_a/b` | función `resolve_attribution_discard`, `brief_field_attributions`, `memberships`, `attribution_discard_resolutions`, roles | tabla + exclusión `valid_during` (`btree_gist`) |
| Permisos | lectura de catálogos | ídem | rol con SET ROLE a los tres roles de prueba | rol con EXECUTE sobre la función (PRE-08) | rol con INSERT en la tabla |
| Rollback / residuos | solo lectura | `rollback` final | `rollback` final | `rollback` + comprobación final de recuento (sin residuos) | `rollback` en A y en B |
| Idempotencia | sí (lectura) | sí | sí (sin efectos persistentes) | sí | sí si A y B terminan; reejecutar no deja filas |
| Clasificación de errores | n/a (sin PASS/FAIL) | n/a | `pg_temp.ejecuta`+`veredicto`: 42501 PERMISOS, estructura, sintaxis, dominio, inesperado | ídem; técnicos → BLOCKED, inesperado → FAIL | OK/23P01/técnico distinguidos |
| Estados | inventario | inventario | PASS/FAIL/BLOCKED/NOT VERIFIED (RLS-06) | PASS/FAIL/BLOCKED/PARTIAL; global «NO VERIFICABLE EN ENTORNO FÍSICO» si hay BLOCKED | PASS/FAIL/PARTIAL/BLOCKED |
| `WHEN OTHERS` | no | no | 1 (PRE-04 → BLOCKED con SQLSTATE; clasifica, no convierte en PASS) | lib: 1 (clasifica en `ejecuta`), 1 `reset role` (exención documentada), PRE y PRE-09 → BLOCKED | no |
| SQL dinámico | no | no | `format(%I,%L)` | `execute … using` (parametrizado) y `format(%L)`; **`fn_call` es plantilla del operador** | `format(%L)` |
| Riesgo de ejecución accidental en PROD | guarda por identidad efectiva (allowlist vacía = rechaza todo hasta que el propietario registre CCI-DEV; LR-22) | ídem | ídem + escribe en transacción | ídem | ídem; deja sesión abierta 5 s con fila sin confirmar |
| Falso PASS posible | no emite PASS | no emite PASS | RLS-01..04 PASS si no hay fuga **y** hay datos (no vacuo); sondas `where false` no ejecutan DML real | solo con función existente + SQLSTATE exacto del contrato; sin contrato → PARTIAL | PASS solo con espera ≥2 s |
| Falso FAIL posible | no | datos de prueba mal sembrados → FAIL de fuga (mitigado por PRE-04) | rol de prueba sin SET ROLE → BLOCKED, no FAIL | datos que violan >1 regla o el índice único (PRE-09e) → mensaje/código de otra regla = FAIL; mitigación: PRE-09 y datos de una sola regla | **B lanzada >~4 s tras A**: no hay espera → FAIL aunque la restricción funcione (documentado en el procedimiento) |
| Error técnico vs. rechazo de negocio | n/a | n/a | PERMISOS/ESTRUCTURA → BLOCKED | clase DOMINIO_CANDIDATO solo `P0001`/`23xxx`/`RJ%` y además contrato exacto | 23P01 = rechazo; otros = BLOCKED |
| Objeto/permiso/función inexistente | falla visible (error de catálogo) | ídem | BLOCKED (precondición) | BLOCKED (PRE) o BLOCKED por clase (42883/42P01/42501) | BLOCKED |
| Seguridad de controles negativos | n/a | n/a | sondas sin efecto | cada negativo se revierte; control positivo previo | sin efectos |

## 2. Comprobaciones específicas de `04_trigger_r1_r9` (todas demostradas con stubs en el arnés, 28/28)

Función inexistente → BLOCKED (C01); firma incorrecta → BLOCKED (C02); tabla inexistente dentro de la función → BLOCKED (C03); dependencia inexistente → BLOCKED (C13); permiso insuficiente → BLOCKED (C04); excepción inesperada → FAIL (C05); rechazo válido con contrato → PASS (C06, C11, C19, C25); contrato distinto → FAIL (C07, C20, C21, C23, C24); sin contrato → PARTIAL (C08, C22); la regla no rechazó → FAIL (C09); sintaxis → BLOCKED (C10); `P0001` técnico ajeno al contrato → FAIL (C12); precondición falsa → BLOCKED aunque el rechazo coincida (C16). Ningún resultado depende de capturar `WHEN OTHERS` sin clasificar: la única captura clasifica por SQLSTATE y devuelve el error, nunca PASS. **Esto prueba el arnés, no R1–R9.**

## 3. Defectos encontrados en esta revisión y corregidos
1. Contrato comparado por prefijo de texto (aceptaba `RJ00` como contrato de `RJ003`): corregido a SQLSTATE exacto (+ prefijo de mensaje solo si el contrato lo declara). Cubierto por C23–C25.
2. Clasificador sin clase de dominio propia: añadida la clase propuesta `RJ%` (sigue sin contrato aprobado → PARTIAL).
3. Plan R1–R9 y autoprueba usaban contratos de error distintos: unificados en una única propuesta.
4. El escáner no analizaba el interior de bloques `$$…$$`/DO (donde está la lógica): corregido y probado con muestras.

## 4. Riesgos residuales (no eliminables en este alcance)
Guarda por identidad efectiva, sin identificadores reales registrados (LR-22); `fn_call` es plantilla de confianza del operador; temporización de 05 (A/B); semántica real de RLS, `auth.uid()`, roles y privilegios de Supabase no probada; datos de prueba por regla (R2, R4–R9) no verificables genéricamente (PRE-09f).
