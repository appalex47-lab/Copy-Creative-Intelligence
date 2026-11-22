# 04 — Códigos R1–R9 vs `AppErrorCode`

**Validado contra un diseño no aprobado.** F6 (`PROPUESTA_CONTRATO_ERRORES_R1_R9.md`) está declarada «NO APROBADA».

## Qué son R1–R9 (F3 l.1585–1593; F6)
Nueve **reglas de elegibilidad del resolutor** de una función de base de datos (`resolve_attribution_discard`, trigger BEFORE INSERT sobre `attribution_discard_resolutions`, IG5-95). Son rechazos de negocio emitidos por PostgreSQL, no errores de la interfaz. F3 no define SQLSTATE, código de dominio ni firma; F6 lo **propone**: alternativa B (recomendada, no aprobada) = SQLSTATE propio `RJ001…RJ009` (R1…R9) y `RJ010` (evidencia ausente); alternativas A (`P0001` + texto), C (`P0001` + `DETAIL`), D (códigos estándar).

## Comparación
| Aspecto | R1–R9 (F6) | `AppErrorCode` actual |
|---|---|---|
| Capa | Base de datos (función/trigger) | Contrato de servicios de la UI |
| Operación | Escritura: resolver un descarte de atribución | Lectura (listados e identidad) |
| Códigos | 9 reglas (+ evidencia ausente) | `not_found`, `not_implemented`, `unavailable`, `invalid_configuration`, `validation_error` |
| Solapamiento | Ninguno directo | — |
| Estado | Propuesta no aprobada; orden de evaluación R1→R9 también pendiente | Provisional de la app |

## Resultado
- **Estado: SIN_DISEÑO para el contrato de errores de la UI** y **PENDIENTE_DE_DECISIÓN** para R1–R9 (F6: «Pendiente del propietario»: aprobar/modificar códigos, orden de evaluación, firma de la función, entradas del solicitante y del evento).
- **No hay discrepancia que corregir en los 5 códigos actuales** por causa de R1–R9: operan en capas distintas. Cuando exista una operación de escritura que invoque la función, la UI necesitará **mapear** SQLSTATE→código de dominio (p. ej. `RJ003`→«regla no cumplida»). Esa necesidad es una **brecha futura (no de 1.1-B)**: hoy no hay servicio de escritura (T25).
- Posible adición futura (no propuesta como cambio inmediato): un código de aplicación para «regla de negocio rechazada» (`business_rule_rejected`) con el identificador de regla, y otro para «permiso denegado» (`42501`, F6 lo reserva para privilegio de ejecución). Requiere aprobar F6 primero.
- Ante falla del servidor, F3 exige atomicidad y *fail-closed* (según F6); coherente con la regla del contrato actual «un fallo nunca se representa como lista vacía».
- **No verificado:** emisión real de los códigos, su tratamiento por Supabase/PostgREST (F6 lo declara no verificado) y si F3 contiene otro contrato de errores que no leí.
