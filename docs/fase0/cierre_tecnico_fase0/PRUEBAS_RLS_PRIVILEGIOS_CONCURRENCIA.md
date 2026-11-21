# PRUEBAS RLS, PRIVILEGIOS Y CONCURRENCIA — v2 (**NO EJECUTADAS EN CCI-DEV**)

> Scripts v2 en `scripts_validacion/cci_dev_NO_EJECUTADOS/`. Guarda idéntica en los seis (`SI-CCI-DEV`+`CCI-DEV`, o modo local temporal por socket Unix con base `^cci_`). La guarda **no puede probar** que la base sea DEV y no PROD (LR-22).

## 1. RLS / privilegios (`03_pruebas_rls_ROLLBACK.sql`)

Defectos de v1 corregidos: usaba una columna inexistente (`approver`; el diseño usa `decided_by`, DEF-NAME-01) y las sondas DELETE/TRUNCATE podían ejecutarse. v2: precondiciones (tablas, columnas, datos de ambas organizaciones: sin ellas las pruebas serían vacuas), resultado **por tabla**, sondas de denegación sin efecto (`where false` o `has_table_privilege`).

| Prueba | Qué comprueba | Estado local (shim) |
|---|---|---|
| RLS-01 | lectura cruzada entre organizaciones | shim defectuoso FAIL; corregido PASS |
| RLS-02 | usuario sin membresía | defectuoso FAIL; corregido PASS |
| RLS-03 | `anon` | defectuoso FAIL; corregido PASS |
| RLS-04 | escritura cruzada | PASS en ambos |
| RLS-05a–e | denegación de DELETE/TRUNCATE/UPDATE/INSERT donde corresponde | PASS |
| RLS-06 | aislamiento por rol de aplicación | **NOT VERIFIED** (no implementado) |

El shim (`local_ext/30_shim_rls_fixture_LOCAL.sql`) simula roles; **no es Supabase** (sin `auth.uid()`, `authenticator`, políticas reales). Resultados: `resultados/smoke_03_rls_shim_*.txt`; las corridas 1/2 históricas (`shim_rls_corrida*.txt`) se conservan, aunque su shim no estaba versionado (LR-25).

## 2. Inventarios (`01`, `02`, solo lectura)

`begin read only`; devuelven catálogos; **no emiten PASS/FAIL**. Smoke local: `smoke_01_inventario.txt`, `smoke_02_rls_inventario.txt`.

## 3. Concurrencia (`05_concurrencia_sesion_A.sql` y `05_concurrencia_sesion_B.sql`)

Precondición: la tabla `piece_reviewer_assignments` existe (si no, `\quit` con BLOCKED). A inserta una asignación vigente, espera 5 s y revierte; B intenta lo mismo con `lock_timeout`/`statement_timeout`. PASS si B espera ≥2 s y luego recibe el error esperado; FAIL si no hay espera (no se serializó); PARTIAL si 23P01 sin espera medible; BLOCKED por errores técnicos. Smoke local (fixture `31_conc_smoke_fixture_LOCAL.sql`): B esperó 3,50 s → PASS; sin tabla → BLOCKED. CC-01/CC-02 locales: PASS (`concurrencia_local_utf8.txt`). CONC-03..06: sin script.

## 4. Pendiente / no verificado

Pendiente del propietario: autorización y proyecto CCI-DEV. No verificado: todo comportamiento en Supabase (roles, JWT, `auth.uid()`, políticas), concurrencia real, RLS-06.
