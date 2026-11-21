# PLAN DE VALIDACIÓN POR ETAPAS (LOCAL → CCI-DEV) — **NO EJECUTADO EN CCI-DEV**

> **Estado actual: las etapas E0–E1 están ejecutadas LOCALMENTE (PostgreSQL 16.15 temporal); las etapas E2–E8 están PREPARADAS y NO EJECUTADAS.** Nada se ha ejecutado contra Supabase, CCI-DEV ni CCI-PROD. Los scripts están en `scripts_validacion/cci_dev_NO_EJECUTADOS/` (v2, corrección consolidada). Este plan no autoriza ejecución: la autoriza el propietario por escrito.

## 0. Reglas de lectura de estados

`PASS` · `FAIL` · `BLOCKED` (precondición no satisfecha: función/tabla/permiso/versión ausente; **no es fallo ni éxito**) · `PARTIAL` (rechazo observado sin contrato de error declarado) · `NOT VERIFIED` (no implementado en el script). Un error técnico (permiso, función inexistente, estructura, sintaxis) **nunca** es PASS de una prueba negativa. Resultado global sin implementación física: **NO VERIFICABLE EN ENTORNO FÍSICO**.

## 1. Puertas de autorización (todas por el propietario)

| Puerta | Condición |
|---|---|
| P0 | Existe el esquema físico en CCI-DEV (migraciones aplicadas por decisión previa del propietario). Si no: E2–E8 = BLOCKED. |
| P1 | El propietario confirma por escrito el project ref de CCI-DEV y que es independiente de CCI-PROD y de RevNavigator. **Ninguna guarda de script puede probarlo** (LR-22). |
| P2 | Lectura de catálogos (E2, E3). |
| P3 | Escritura en transacción con ROLLBACK, con datos de prueba aislados (E4–E8). |
| P4 | Credenciales entregadas por el propietario por canal seguro; Claude no las pide ni las busca. |

## 2. Invocación de los scripts (solo CCI-DEV autorizado)

`PGOPTIONS="-c cci.validacion_autorizada=SI-CCI-DEV -c cci.entorno=CCI-DEV" psql "<cadena de conexión entregada por el propietario>" -v ON_ERROR_STOP=1 -f <script>` (y `-v` con los datos de prueba que cada script exige). Guardar la salida íntegra sin editar, el SHA-256 del script y la versión de PostgreSQL.

## 3. Etapas con criterios objetivos

Todas las filas heredan: *Evidencia a guardar* = salida íntegra del script + SHA-256 del script + `select version()` + marca de tiempo; *Rollback* = el script no persiste nada (sub-bloques con excepción centinela / `begin read only` / sesión terminada en ROLLBACK); *Riesgo común* = ejecutar contra el proyecto equivocado (mitigación: P1, guarda, rol sin privilegios permanentes de escritura).

### E0 — PostgreSQL local temporal (EJECUTADA)

| ID | Objetivo | Procedimiento | Resultado | Criterio |
|---|---|---|---|---|
| E0-1 | Base V20 | `PE_POSTGRESQL_V20/ejecutar.sh <socket> <puerto>` y `mutaciones.sh` | 63/63 PASS; 14/14 detectadas | PASS si 63/63 y 14/14 |
| E0-2 | Extensión local | `local_ext/ejecutar_ext.sh` | 80/80 PASS (UTF8) | PASS si 80/80 |
| E0-3 | Concurrencia local | `ct_concurrencia_local.sh` | CC-01, CC-02 PASS | PASS si espera ≥1,5 s y error 23P01/23505 |
| E0-4 | Arnés R1–R9 | `ct_arnes_r1r9_autoprueba.sh` | 28/28 (incl. reproducción de 11 falsos PASS de v1 y contrato RJ exacto) | PASS si 28/28; **prueba el arnés, no R1–R9** |
| E0-5 | Smoke de los 6 scripts en modo LOCAL-TEMPORAL | `ct_smoke_scripts_cci_dev_local.sh` | guardas 7/7; 03 sobre shim defectuoso=FAIL, corregido=PASS; 04=NO VERIFICABLE; 05 B espera ≥2 s PASS | **No equivale a Supabase** |
| E0-6 | Escáner estático de seguridad | `ct_escaner_seguridad_sql.py` | sql 115 / texto 571 comprobaciones, 0 FAIL; autoprueba 26/26 | PASS si 0 FAIL |

### E1 — Modelo en memoria (EJECUTADA)

22 funciones 366 evaluaciones/0 fallos; T-409..T-422 26/26 variantes; K47 25/25; hash 16/16. Ver `scripts_validacion/resultados/`. Evidencia de modelo/prototipo, **no** de esquema físico.

### E2 — Esquema físico CCI-DEV (inventario, solo lectura)

| ID | Objetivo | Precondiciones | Datos | Procedimiento | Esperado | PASS / FAIL / BLOCKED |
|---|---|---|---|---|---|---|
| E2-1 | Inventario de tablas y columnas | P0–P2 | ninguno | `01_inventario_esquema_SOLO_LECTURA.sql` | 41 tablas; columnas/tipos/nulabilidad de `MATRIZ_MODELO_LOGICO_FISICO.md` | PASS si 41 y sin divergencias; FAIL si falta/sobra una; BLOCKED si el esquema no existe |
| E2-2 | Restricciones (PK/FK compuestas/UNIQUE/CHECK/EXCLUDE) e índices | E2-1 | ninguno | mismo script | FK01–FK41; `u_adr_aceptada`; CHECK `resolved_by<>affected_contributor_id` y `resolved_by<>requested_by` | PASS si todas presentes |
| E2-3 | Funciones y triggers | E2-1 | ninguno | mismo script | firma exacta de `resolve_attribution_discard`; trigger BEFORE INSERT; `SECURITY DEFINER`, propietario y `search_path` registrados | PASS si coinciden; BLOCKED si la función no existe |
| E2-4 | Versión y extensiones | P2 | ninguno | mismo script | PostgreSQL ≥13; `btree_gist`, `pgcrypto` presentes | PASS si presentes; FAIL si falta alguna de las que el diseño exige |

### E3 — RLS y privilegios (solo lectura)

| ID | Objetivo | Procedimiento | Esperado | Criterio |
|---|---|---|---|---|
| E3-1 | RLS activa y forzada donde hay `organization_id` | `02_rls_privilegios_SOLO_LECTURA.sql` | `relrowsecurity` verdadero en todas | PASS/FAIL por tabla |
| E3-2 | Matriz S/I/U/D/T efectiva de `anon`/`authenticated`/`service_role` | idem | sin INSERT/UPDATE/DELETE/TRUNCATE directos en tablas de solo función (IG5-98, DG-20) | PASS si cumple; el script **solo inventaría**, el veredicto lo emite el revisor comparando con la matriz |

### E4 — RLS (comportamiento, con rollback)

| ID | Objetivo | Datos | Procedimiento | Esperado | Criterio |
|---|---|---|---|---|---|
| E4-1 | RLS-01..04: lectura cruzada, sin membresía, anon, escritura cruzada | filas de 2 organizaciones de prueba (PRE-04 exige ambas) | `03_pruebas_rls_ROLLBACK.sql` | 0 fugas; escritura cruzada rechazada con 42501 o 0 filas | PASS por tabla; FAIL si hay fuga; BLOCKED si falta tabla/columna/datos (no vacuo) |
| E4-2 | RLS-05a–e: denegación de DELETE/TRUNCATE/UPDATE en tablas de solo inserción | sin datos | idem | rechazo por privilegio | PASS si 42501/sin privilegio |
| E4-3 | RLS-06: aislamiento por rol de aplicación | — | **NOT VERIFIED** (no implementado genéricamente) | — | No cuenta como PASS |

### E5 — Privilegios y SECURITY DEFINER

Verificar con `02` + una revisión del propietario: `EXECUTE` solo para roles previstos, `search_path` fijo en funciones SECURITY DEFINER, propietario `cci_records_owner`. Criterio: PASS si coincide con `ESPECIFICACION_TECNICA`; **no hay script automático de veredicto** (declarado, no se simula).

### E6 — Triggers R1–R9

Ver `PLAN_VALIDACION_TRIGGER_R1_R9.md` (script `04` v2). Estado hoy: **NO VERIFICABLE EN ENTORNO FÍSICO**; con función real y contrato de error definido, 11 casos (control positivo + R1..R9 + R-ev1).

### E7 — Concurrencia

| ID | Objetivo | Procedimiento | Esperado | Criterio |
|---|---|---|---|---|
| E7-1 | CONC-01 G-9: exclusión de revisor vigente | `05_concurrencia_sesion_A.sql` en una sesión y, ≤2 s después, `05_concurrencia_sesion_B.sql` en otra | B espera ≥2 s y luego 23P01 o OK serializado; 1 fila | PASS si espera ≥2 s; FAIL si no hay espera; PARTIAL si 23P01 sin espera medible; BLOCKED si falta tabla |
| E7-2 | CONC-02 IG1-14: numeración única | variante local ya ejecutada (CC-02); versión física pendiente | 23505 | por escribir tras existir la tabla |
| E7-3 | CONC-03..06 | sin script | — | **NO EJECUTADO, sin script** |

### E8 — K47 físico y atribución

Equivalente físico de las 25 mutaciones de T-409..T-422 (script por escribir cuando existan las funciones de atribución). Hoy: **SIN SCRIPT**; evidencia solo en modelo.

## 4. Qué NO debe hacerse

No crear/alterar/borrar objetos permanentes; no ejecutar en CCI-PROD; no desplegar; no cambiar RLS ni privilegios; no reutilizar credenciales ni proyectos de RevNavigator; no iniciar Fase 1; no editar un script para obtener PASS sin versionarlo como nueva versión.

## 5. Pendiente del propietario / no verificado

Pendiente del propietario: P0–P4; project ref de CCI-DEV; definición del contrato de error de R1–R9 (BRECHA-R1R9-01). No verificado por Claude: cualquier comportamiento en Supabase; `auth.uid()`; roles reales; versión y extensiones reales; E2–E8.

## 6. Requisitos de entorno (a confirmar con el inventario; no se asumen)

| Elemento | Requisito | Origen / estado |
|---|---|---|
| PostgreSQL | ≥ 13 (precondición PRE-01 del script 04); la versión exacta de Supabase **no está especificada** en el expediente: registrar `select version()` | script 04; sin dato de Supabase (no inventado) |
| Extensiones | `btree_gist` (restricción de exclusión G-9) y `pgcrypto` (cadena hash DG-12) | uso en prototipos locales; su presencia en Supabase se verifica con el inventario 01 |
| Codificación | UTF8 (LR-11) | inventario |
| Roles | `anon`, `authenticated`, `service_role` (roles de prueba de 02/03), rol de ejecución `exec_role` (04), propietario `cci_records_owner` previsto en la especificación | confirmar en 02; los nombres reales de Supabase no se verificaron aquí |
| Tablas | las 41 de `MATRIZ_MODELO_LOGICO_FISICO.md` §5; mínimas por script: 03 (`organization_id` en tablas de negocio), 04 (`attribution_discard_resolutions`, `brief_field_attributions`, `memberships`), 05 (`piece_reviewer_assignments`) | inventario 01 |
| Funciones / triggers | `resolve_attribution_discard(uuid,text,text)` (firma PROPUESTA), trigger BEFORE INSERT en `attribution_discard_resolutions`, `transition_piece_status` | PRE de 04; la firma y el contrato de error son decisión pendiente |
| Datos de prueba | dos organizaciones de prueba con filas en cada una (PRE-04 de 03); usuarios r_ok, r_nomember, r_noreview, r_direct, r_inherited, r_othersrc, r_benef, affected, requester, change_actor, creados **solo** en CCI-DEV y marcados como prueba; ids propios, sin datos personales reales | variables `-v` de 04; los crea/entrega el propietario |

## 7. Casos positivos y negativos por script

03: positivos (usuario del org A lee solo A), negativos RLS-01..05. 04: positivo R-POS y negativos R1–R9, R-ev1. 05: positivo (A inserta y revierte), negativo (B bloqueada y luego 23P01). 01/02: sin casos (inventario).

## 8. Criterios de interrupción (detener la ejecución y no continuar)

(1) la guarda no coincide con el project ref confirmado (P1); (2) cualquier script informa una escritura persistente (recuento posterior ≠ anterior en 04); (3) aparece un error de conexión/bloqueo largo (`lock_timeout`) en tablas de producción; (4) un FAIL de fuga RLS (reportar y detener: no «arreglar» en el momento); (5) el entorno resulta ser CCI-PROD o un proyecto de RevNavigator; (6) falta la autorización escrita P0–P4. Tras interrumpir: `rollback`, cerrar sesiones, guardar la salida íntegra.

## 9. Procedimiento de limpieza

Los scripts no persisten datos (rollback). Verificación: recuento de filas de las tablas tocadas antes y después (04 lo hace; para 03/05 contar a mano). Los datos de prueba sembrados por el propietario se eliminan por el propietario con su propio procedimiento aprobado; este expediente no ejecuta borrados. Cerrar sesiones A/B de 05 y verificar con `pg_stat_activity` que no quedan transacciones abiertas.

## 10. Evidencias y criterios de aceptación globales

Por etapa: salida íntegra sin editar, SHA-256 del script (de `MANIFIESTO_SHA256_CIERRE.txt`), versión, fecha, project ref confirmado, identidad del ejecutor. Aceptación de E2–E8: todos los PASS aplicables sin FAIL ni BLOCKED inexplicado; PARTIAL y NOT VERIFIED se reportan como pendientes; ningún resultado se «mejora» editando el script (cambio = nueva versión del script con su historial). La aceptación **formal** de Fase 0 y la autorización de Fase 1 son decisiones exclusivas del propietario.

## 11. Qué se puede preparar documentalmente y qué requiere ejecución real

Preparable (hecho): scripts v2, arnés, propuestas (contrato R1–R9, guarda DEV/PROD), plan, criterios. Requiere ejecución real en CCI-DEV con autorización expresa: E2–E8 completas, la prueba de la guarda con el marcador de entorno, K47 físico y las funciones. CCI-PROD queda fuera de esta operación.

## 12. Aprobación requerida

Autorización escrita del propietario para: ejecutar E2–E3 (lectura), E4–E8 (escritura con rollback), el contrato de error de R1–R9, el mecanismo de marcador de entorno y la entrega de datos de prueba. Sin ella, todo permanece NO EJECUTADO.
