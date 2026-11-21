# PROPUESTA DE CONTRATO DE ERRORES PARA R1–R9 (BRECHA-R1R9-01) — **NO APROBADA**

> **Estado: PROPUESTA TÉCNICA. No es parte de la especificación ni está aprobada por el propietario.** La especificación (`ESPECIFICACION_TECNICA_G1_G5_G10.md`, R1–R9 en l.1585–1593; función en l.3625) no define SQLSTATE, código de dominio, tipos de entrada, parámetro de resultado ni cómo recibe la función al solicitante y al evento motivador. Esta propuesta resuelve todo lo resoluble sin inventar el contrato: lo propone, lo prueba **en el arnés local** (con funciones de relleno) y deja la decisión al propietario.

## 1. Alternativas

| Alt. | Mecanismo | Discriminación de la regla | Fragilidad | Efecto en Supabase/PostgREST (**no verificado**) | Consecuencias |
|---|---|---|---|---|---|
| A | `ERRCODE 'P0001'` + `MESSAGE 'R3:no_afectado'` | Solo por texto del mensaje | Alta: `P0001` es el código de cualquier `RAISE EXCEPTION`; un error técnico con texto parecido se confunde; el texto puede cambiar sin avisar | `P0001` llega como error de aplicación con el mensaje | Cambio mínimo, pero las pruebas dependen de un texto; un fallo interno con `RAISE` genérico puede parecer rechazo (el arnés lo bloquea solo si el prefijo no coincide) |
| **B (recomendada)** | SQLSTATE propio por regla: clase `RJ`, `RJ001`…`RJ009` (R1…R9) y `RJ010` (evidencia ausente); mensaje descriptivo libre | **Por SQLSTATE exacto**, independiente del texto | Baja: un código por regla; `P0001`, `23xxx`, `42501` conservan su significado | PostgREST devuelve el SQLSTATE en el cuerpo de error y suele mapear códigos desconocidos a HTTP 400; el comportamiento exacto en Supabase **no se verificó** | Requiere que la función los emita (`RAISE … USING ERRCODE='RJ003'`); el cliente debe conocer 10 códigos; fácil de probar y de monitorizar |
| C | `P0001` + `DETAIL='regla=R3'` estructurado | Por campo `DETAIL` | Media: depende de capturar `PG_EXCEPTION_DETAIL`; el arnés actual no lo captura | `DETAIL` visible solo si el cliente lo propaga | Más cambios en el arnés; sin ventaja frente a B |
| D | Reutilizar códigos estándar (`42501` para R1/R2, `23514` para R3/R4…) | Parcial | Alta: confunde autorización con elegibilidad y con restricciones de tabla; varias reglas comparten código | Los códigos estándar tienen tratamiento propio en PostgREST (p. ej. 403/409) | Imposible distinguir R3 de R4; no recomendada |

## 2. Decisión técnica recomendada (propuesta B)

| Regla | Texto original (spec) | SQLSTATE propuesto | Mensaje sugerido |
|---|---|---|---|
| R1 | El resolutor es miembro activo de la organización de la resolución | `RJ001` | `R1:miembro_activo` |
| R2 | El resolutor tiene `piece.review` | `RJ002` | `R2:piece_review` |
| R3 | No es el contribuyente afectado | `RJ003` | `R3:no_afectado` |
| R4 | No es quien solicitó la resolución | `RJ004` | `R4:no_solicitante` |
| R5 | No es quien ejecutó la modificación material que motivó la solicitud | `RJ005` | `R5:no_actor_del_cambio` |
| R6 | No es contribuyente directo del campo en ninguna versión de la cadena | `RJ006` | `R6:no_directo_en_cadena` |
| R7 | No es contribuyente heredado activo del campo | `RJ007` | `R7:no_heredado_activo` |
| R8 | No contribuyó a otra fuente de la cadena | `RJ008` | `R8:no_excluido_otra_fuente` |
| R9 | No es beneficiario directo ni indirecto | `RJ009` | `R9:no_beneficiario` |
| (evidencia) | La función recibe «atribución, motivo, evidencia» (l.3625) | `RJ010` | `EV:evidencia_ausente` |

Reglas de diseño que acompañan a la propuesta: (1) `42501` queda reservado para falta de privilegio de ejecución; (2) `P0001` **no** se usa para rechazo de negocio; (3) los errores técnicos (`42883`, `42P01`, `22xxx`, etc.) se propagan con su propio SQLSTATE y el arnés los clasifica como BLOCKED/FAIL, nunca como rechazo; (4) la función es atómica y *fail-closed* (l.3625): ante cualquier error no se persiste nada; (5) orden de evaluación determinista R1→R9 (la especificación no lo fija: **también es decisión pendiente**); los datos de prueba deben violar **una sola** regla.

## 3. Diferencia entre rechazo esperado y error técnico (aplicada por el arnés)

`pg_temp.clase()` + `pg_temp.veredicto()` (`04_lib_clasificador.sql`): `42501` PERMISOS; `42883` FUNCION_INEXISTENTE; `42P01`/`42703`… ESTRUCTURA; sintaxis; **DOMINIO_CANDIDATO** = `P0001`, `23xxx` o clase `RJ`; resto ERROR_INESPERADO. Un caso negativo es PASS solo si la clase es DOMINIO_CANDIDATO **y** el SQLSTATE coincide **exactamente** con el contrato declarado (y el prefijo de mensaje, si el contrato lo incluye). Sin contrato: PARTIAL. (Defecto corregido en esta ronda: la comparación anterior era por prefijo de texto y habría aceptado `RJ00` como contrato de `RJ003`.)

## 4. Casos de prueba

Arnés local (stubs que **no** implementan R1–R9; 28/28 PASS en la ronda final): C19 (RJ003 = RJ003 → PASS), C20 (RJ004 cuando se esperaba RJ003 → FAIL), C21 (`P0001` con el mismo texto → FAIL), C22 (clase RJ sin contrato → PARTIAL), C23 (contrato `RJ00` no acepta `RJ003`), C24/C25 (SQLSTATE + prefijo de mensaje). Físico (cuando exista la función): los 11 casos de `04_trigger_r1_r9_ROLLBACK.sql` ejecutados con `-v code_r1=RJ001 … -v code_r9=RJ009 -v code_rev=RJ010`.

## 5. Consecuencias

*Si el propietario aprueba B:* se fija el contrato en la especificación; la función debe emitir los códigos; el script 04 pasa de PARTIAL a PASS/FAIL por regla; se añaden los códigos a la documentación de cliente. *Si no se aprueba (o se elige A/C/D):* el arnés admite cualquier contrato con formato `SQLSTATE[:prefijo]` (variables `code_*`); mientras no haya contrato, todo rechazo observado es PARTIAL y R1–R9 **no puede** declararse verificada. *Si no se decide:* R1–R9 permanece NO VERIFICABLE EN ENTORNO FÍSICO.

## 6. Pendiente del propietario / no verificado
Aprobar o modificar la propuesta (códigos, orden de evaluación, firma `resolve_attribution_discard`, entradas del solicitante y del evento). No verificado: emisión real de estos códigos, su tratamiento por Supabase/PostgREST y por el cliente.
