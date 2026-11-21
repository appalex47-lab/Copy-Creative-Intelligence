# PRUEBAS DE RLS, PRIVILEGIOS Y CONCURRENCIA — DISEÑO DE PRUEBAS (NO EJECUTADAS EN CCI-DEV)

Complementa `PLAN_VALIDACION_CCI_DEV.md`. Todas las pruebas de este documento están **preparadas, no ejecutadas** contra Supabase; lo ejecutado localmente se indica por separado en cada sección.

## 1. Pruebas de RLS

Modelo de acceso (de la especificación): aislamiento por organización (`organization_id`); lectura para miembros; escritura sólo por funciones autorizadas en tablas críticas.

| ID | Prueba | Roles | Esperado | Script | Estado |
|---|---|---|---|---|---|
| RLS-01 | Lectura cruzada: ningún usuario de la org A ve filas de la org B en **ninguna** tabla con `organization_id` (consulta dinámica) | authenticated (uid_a) | 0 filas ajenas | `03` | NO_EJECUTADO (probado en shim) |
| RLS-02 | Usuario autenticado sin membresía no ve filas | authenticated (uid_x) | 0 filas | `03` | NO_EJECUTADO (shim) |
| RLS-03 | `anon` no lee tablas de negocio | anon | 0 filas o 42501 | `03` | NO_EJECUTADO (shim) |
| RLS-04 | Escritura cruzada: INSERT/UPDATE/DELETE de uid_a sobre filas de org_b | authenticated | error o 0 filas | `03` (plantilla) | NO_EJECUTADO |
| RLS-05a..d | Escalada: sin INSERT en `role_permissions`, sin UPDATE en `approvals`, sin DELETE en `activity_logs`, sin TRUNCATE en tablas inmutables | authenticated | 42501 | `03` | NO_EJECUTADO (shim) |
| RLS-06 | Separación de roles: un usuario sin la clave `piece.approve` no ejecuta `record_approval`; uno que la tiene sí (los roles que la tienen se leen de `role_permissions`; no se asume aquí) | authenticated con distintos roles | según `role_permissions` | por escribir | NO_EJECUTADO |
| RLS-07 | Registros propios vs ajenos dentro de la misma organización: lectura permitida a miembros, edición sólo del autor donde aplique | authenticated | según política | por escribir | NO_EJECUTADO |
| RLS-08 | CRUD completo por tabla (matriz S/I/U/D) contra la matriz de aislamiento de la especificación (27 tablas v3.3 + 14) | cada rol | igual a la matriz | `02` PRIV-04 | NO_EJECUTADO |
| RLS-09 | Casos negativos: JWT sin `sub`, `sub` inexistente, rol alterado en claims | authenticated | 0 filas / 42501 | por escribir | NO_EJECUTADO |

**Hallazgo de diseño local relevante:** una FK compuesta no sustituye a RLS (las FK se comprueban con privilegios del propietario de la tabla; no filtran lectura). Por eso RLS-01 debe ejecutarse sobre *todas* las tablas.

## 2. Pruebas de privilegios

| ID | Prueba | Esperado | Script |
|---|---|---|---|
| PRIV-01..07 | Inventario: políticas, grants, matriz S/I/U/D/T efectiva, EXECUTE, atributos de roles, privilegios por defecto | Coincide con el diseño: mínimo privilegio; escritura directa sólo para propietarios de funciones | `02` |
| PRIV-08 | Acceso directo vs vía función: `authenticated` no puede INSERT directo en `approvals`; sí vía `record_approval` | 42501 directo; OK vía función | por escribir |
| PRIV-09 | Separación administrativa vs operativa: `org.manage` sólo concede permisos; no aprueba piezas por cargo (IG5-95: ni Admin ni propietario obtienen independencia por su cargo) | rechazo R-reglas | `04` |
| PRIV-10 | Funciones `SECURITY DEFINER`: `search_path` fijo; sin ejecución para `anon` | Cumple | `01` INV-06, `02` PRIV-05 |
| PRIV-11 | `service_role` sin acceso directo a tablas con escritura restringida (la especificación lo exige para `approvals`) | Cumple | `02` |

## 3. Pruebas de concurrencia

| ID | Escenario | Mecanismo bajo prueba | Esperado | Evidencia local |
|---|---|---|---|---|
| CONC-01 | Dos asignaciones de revisor solapadas para la misma pieza (G-9) | EXCLUDE USING gist | B se bloquea y luego falla con 23P01; una fila | **CC-01 PASS local** (PG16 UTF8, espera ≈2 s) |
| CONC-02 | Dos versiones con la misma numeración (IG1-14) | UNIQUE(org,piece,version_no) | B se bloquea y falla con 23505 | **CC-02 PASS local** |
| CONC-03 | Dos resoluciones `aceptada` para la misma atribución | índice parcial `u_adr_aceptada` | segunda falla con 23505 | no ejecutado (probar con A/B en CCI-DEV) |
| CONC-04 | Dos aprobaciones simultáneas de la misma versión (ciclo con revocación) | transición T-02 + independencia | una sola transición válida; sin estado intermedio | no ejecutado |
| CONC-05 | Actualización conflictiva de estado de pieza (lost update) | `transition_piece_status` con bloqueo de fila (`FOR UPDATE`) o versión optimista | la segunda ve el estado nuevo y falla | no ejecutado |
| CONC-06 | Idempotencia: misma `idempotency_key` con mismo/otro `request_fingerprint` (evaluaciones) | UNIQUE(idempotency_key) | mismo → misma fila; otro → rechazo | no ejecutado |
| CONC-07 | Consumo de cuota de IA (`consume_ai_quota`) concurrente | UPDATE atómico condicional | nunca supera el tope | no ejecutado |
| CONC-08 | Rollback: fallo a mitad de una operación compuesta (reutilización de asset) no deja filas parciales | transacción de la función | estado idéntico | modelo en memoria PASS (20+11+8); físico NO_EJECUTADO |
| CONC-09 | Deadlock: dos sesiones que actualizan dos filas en orden inverso | orden de bloqueo definido | una aborta con 40P01; el cliente reintenta | no ejecutado |
| CONC-10 | Lectura durante escritura (aislamiento READ COMMITTED vs REPEATABLE READ) para el cálculo de E | snapshot consistente | E calculado sobre un snapshot | no ejecutado |

Procedimiento de dos sesiones: lanzar A (`05_concurrencia_sesion_A.sql`), esperar 1–2 s, lanzar B; registrar tiempos de bloqueo y códigos. Todas las operaciones terminan en ROLLBACK.

## 4. Límites

Las pruebas locales CC-01/CC-02 demuestran que los mecanismos de PostgreSQL 16 (EXCLUDE, UNIQUE) bloquean como se espera; **no** demuestran la configuración de Supabase (pooler en modo transacción, timeouts, versión de Postgres) ni las funciones reales.
