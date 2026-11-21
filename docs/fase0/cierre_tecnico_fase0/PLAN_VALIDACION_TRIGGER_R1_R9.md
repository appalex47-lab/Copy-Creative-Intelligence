# PLAN DE VALIDACIÓN DE R1–R9 (resolve_attribution_discard) — **NO EJECUTADO EN ENTORNO FÍSICO**

> **Resultado actual: NO VERIFICABLE EN ENTORNO FÍSICO.** La función, las tablas y los permisos físicos no existen en ningún entorno disponible. No se simula una implementación: una función de relleno ("stub") solo prueba el **arnés**, nunca la lógica R1–R9.

## 1. Fuente y texto original

Especificación (`ESPECIFICACION_TECNICA_G1_G5_G10.md`): R1–R9 en líneas 1585–1593 (R1 miembro activo; R2 `piece.review`; R3 no es el afectado; R4 no es el solicitante; R5 no es el actor del cambio; R6 no es contribuyente directo en la cadena; R7 no es contribuyente heredado activo; R8 no contribuyó a otra fuente de la cadena; R9 no es beneficiario directo ni indirecto). La función figura en la línea 3625: propietario `records_owner`, entradas «atribución, motivo, evidencia», permiso `piece.review`, registro nuevo en `attribution_discard_resolutions`, nunca retroactiva, fail-closed. Tabla `attribution_discard_resolutions`: línea 1118 y siguientes.

## 2. Brecha BRECHA-R1R9-01 (LR-21)

La especificación **no define** (a) SQLSTATE ni código de dominio para el rechazo de cada regla, (b) tipos de las entradas, (c) parámetro de resultado, (d) cómo recibe la función al solicitante y al evento motivador (R4, R5). Consecuencia: un rechazo observado **no puede ser PASS** de una regla concreta; queda PARTIAL.

**Propuesta técnica (NO aprobada; decide el propietario):** la función lanza `RAISE EXCEPTION USING ERRCODE='P0001', MESSAGE='R<n>:<nombre>'` con el nombre de la tabla de la línea 1585–1593 (p. ej. `R3:no_afectado`); permisos insuficientes siguen siendo `42501`. El script acepta el contrato por variables `code_r1..code_r9`, `code_rev` con formato `SQLSTATE[:prefijo]` (ej. `P0001:R3:no_afectado`). Con las variables vacías todo rechazo es PARTIAL.

## 3. Arnés (script `04_lib_clasificador.sql`) y su autoprueba

| Elemento | Comportamiento |
|---|---|
| Clasificación | OK · PERMISOS (42501) · FUNCION_INEXISTENTE (42883) · ESTRUCTURA · SINTAXIS · DOMINIO_CANDIDATO (P0001/23xxx) · ERROR_INESPERADO |
| Veredicto | error técnico → BLOCKED; inesperado → FAIL; rechazo de dominio → PASS solo si coincide el contrato; sin contrato → PARTIAL; precondición falsa → BLOCKED |
| Aislamiento | cada caso en sub-bloque, efecto revertido con excepción centinela `CC999`; sesión en ROLLBACK; comprobación final de residuos |

Autoprueba local (`ct_arnes_r1r9_autoprueba.sh`, 21/21 PASS): 18 casos de control (función inexistente, firma incorrecta, tabla ausente, permiso insuficiente, excepción inesperada, rechazo válido, contrato ausente, contrato distinto…), sin residuos, y **reproducción del defecto de v1** (11 falsos PASS con `intenta()`; ver `scripts_validacion/historico_defectos/`, SHA-256 `544372ad…c6a3`). Usa funciones de relleno que **no implementan R1–R9**.

## 4. Precondiciones que el script verifica (PRE-01..PRE-10)

Versión ≥13; función con firma exacta (`fn_regproc`, por defecto PROPUESTA `public.resolve_attribution_discard(uuid,text,text)`); propietario/SECURITY DEFINER informados; tablas y columnas; CHECK de `resolved_by`; trigger BEFORE INSERT; EXECUTE del rol de prueba; datos de prueba PRE-09a–f; contrato declarado. Si cualquiera es BLOCKED: los 11 casos quedan BLOCKED y el global es «NO VERIFICABLE EN ENTORNO FÍSICO».

## 5. Casos (11) cuando existan los objetos

| Caso | Regla | Dato de prueba (`-v`) | Esperado |
|---|---|---|---|
| R-POS | control positivo | `r_ok` | éxito (si no, los negativos quedan BLOCKED: no se pueden interpretar) |
| R1 | miembro activo | `r_nomember` | rechazo R1 |
| R2 | `piece.review` | `r_noreview` | rechazo R2 |
| R3 | no afectado | `affected` | rechazo R3 |
| R4 | no solicitante | `requester` | rechazo R4 |
| R5 | no actor del cambio | `change_actor` | rechazo R5 |
| R6 | no directo en cadena | `r_direct` | rechazo R6 |
| R7 | no heredado activo | `r_inherited` | rechazo R7 |
| R8 | no excluido otra fuente | `r_othersrc` | rechazo R8 |
| R9 | no beneficiario | `r_benef` | rechazo R9 |
| R-ev1 | evidencia faltante | `evidence` vacía | rechazo (`code_rev`) |

Criterio PASS (negativo): función existe y se ejecutó, el rechazo lo emitió la lógica (no un error técnico) y SQLSTATE/prefijo coinciden con el contrato. FAIL: la llamada tiene éxito o falla de modo inesperado. BLOCKED: precondición/permiso/dependencia. PARTIAL: rechazo sin contrato.

## 6. Qué NO se ha hecho / pendiente

No ejecutado contra CCI-DEV ni CCI-PROD. Pendiente del propietario: definir el contrato de error y la firma (BRECHA-R1R9-01); entregar datos de prueba. No verificado: que R1–R9 se evalúen en el orden correcto, la interacción con el trigger `t_adr_ins` real y los permisos reales de `authenticated`.
