# Limitaciones residuales (ninguna se convierte en aprobación; cada una tiene clasificación)

## BLOQUEADO_CON_CAUSA_DEMOSTRADA — dependencias externas (impiden FASE0_READY_FOR_OWNER_ACCEPTANCE)
| ID | Qué falta exactamente | Detalle |
|---|---|---|
| ID-13 | validación real en Supabase (no autorizada ni disponible) | system_identifier/pg_control_system() y project ref desde SQL en Supabase |
| EXT-03 | listas de destinos DEV/PROD autorizados: RECHAZADO [L-DEV-VACIA] dev_allow vacía: el propietario debe aportar al menos un 'system_identifier\|base' de CCI-DEV | 00_guarda_destino.sql (procedimiento: PLAN_DESBLOQUEO_EXTERNOS.md, EXT-03) |
| EXT-01 | custodio externo del hash aprobado no definido: falta la aprobación firmada (CCI_APROBACION_CUSTODIO) y la clave pública con su SHA-256 (CCI_CUSTODIO_PUBKEY, CCI_CUSTODIO_PUBKEY_SHA256). El mecanismo criptográfico está probado con claves de prueba; NO hay custodio real | variables CCI_APROBACION_CUSTODIO / CCI_CUSTODIO_PUBKEY* ausentes |
| EXT-02 | compatibilidad con Supabase CCI-DEV (TEMP, pg_control_system(), PGOPTIONS por pooler, project ref, pooler): sólo verificable en CCI-DEV; la sonda existe y está probada en local (SIMULADO_LOCAL) | ID-13: NOT_TESTED |
| EXT-04-L04 | equivalencia del PostgreSQL temporal con el esquema físico aprobado (no existe esquema físico aprobado) | MATRIZ_CONTROLES_V26.csv fila L04: NOT VERIFIED |
| EXT-04-L05 | validación física en CCI-DEV | MATRIZ_CONTROLES_V26.csv fila L05: NOT VERIFIED |
| EXT-04-L06 | RLS, privilegios y concurrencia reales en CCI-DEV | MATRIZ_CONTROLES_V26.csv fila L06: NOT VERIFIED |
| EXT-04-L07 | trigger de elegibilidad R1–R9 en entorno físico | MATRIZ_CONTROLES_V26.csv fila L07: NOT VERIFIED |
| EXT-04-L08 | HV-02/PO-05: confirmación del propietario sobre la Adenda v9 (el documento no existe en el repositorio) | MATRIZ_CONTROLES_V26.csv fila L08: NOT VERIFIED |

Cada una tiene su ficha de 10 campos en `PLAN_DESBLOQUEO_EXTERNOS.md`. Pasos `NOT_TESTED`: K/supabase_cci_dev_real_ext02.

## Limitaciones técnicas declaradas por las pruebas (estado PARTIAL en los resultados, clasificadas)
| Origen | ID | Descripción | Clasificación |
|---|---|---|---|
| adversarial | E2-cor-01 | LIMITACIÓN ESTRUCTURAL; no es aprobación | BLOQUEADO_CON_CAUSA_DEMOSTRADA (la guarda SQL sola no puede distinguir un clon físico; la defensa es la identidad firmada del ejecutor, cuya autoridad real falta) |
| adversarial | E2-cor-02 | LIMITACIÓN ESTRUCTURAL; no es aprobación | BLOQUEADO_CON_CAUSA_DEMOSTRADA (la guarda SQL sola no puede distinguir un clon físico; la defensa es la identidad firmada del ejecutor, cuya autoridad real falta) |
| adversarial | E2-cor-03 | LIMITACIÓN ESTRUCTURAL; no es aprobación | BLOQUEADO_CON_CAUSA_DEMOSTRADA (la guarda SQL sola no puede distinguir un clon físico; la defensa es la identidad firmada del ejecutor, cuya autoridad real falta) |
| adversarial | E2-cor-04 | LIMITACIÓN ESTRUCTURAL; no es aprobación | BLOQUEADO_CON_CAUSA_DEMOSTRADA (la guarda SQL sola no puede distinguir un clon físico; la defensa es la identidad firmada del ejecutor, cuya autoridad real falta) |
| adversarial | E2-cor-05A | LIMITACIÓN ESTRUCTURAL; no es aprobación | BLOQUEADO_CON_CAUSA_DEMOSTRADA (la guarda SQL sola no puede distinguir un clon físico; la defensa es la identidad firmada del ejecutor, cuya autoridad real falta) |
| adversarial | E2-cor-05B | LIMITACIÓN ESTRUCTURAL; no es aprobación | BLOQUEADO_CON_CAUSA_DEMOSTRADA (la guarda SQL sola no puede distinguir un clon físico; la defensa es la identidad firmada del ejecutor, cuya autoridad real falta) |
| search_path | SPD7 | operadores no calificados: con el chequeo de search_path desactivado 4/6 scripts son secuestrables; sólo el chequeo los protege | NO_RESUELTO (defensa en profundidad pendiente: calificar con OPERATOR(pg_catalog.…) los operadores de los 6 scripts; hoy sólo el chequeo de search_path, probado, los protege) |
| identidad | ID-05 | LIMITACIÓN ESTRUCTURAL AG-18: system_identifier+base no distinguen un clon físico/restauración de su origen | BLOQUEADO_CON_CAUSA_DEMOSTRADA |
| identidad | ID-06 | seguro pero inservible: sin una identidad externa no se pueden distinguir | BLOQUEADO_CON_CAUSA_DEMOSTRADA |
| identidad | ID-10 | la protección es tan buena como la lista externa; una restauración sobre el MISMO endpoint no se distingue | BLOQUEADO_CON_CAUSA_DEMOSTRADA |
| orden | 05A-05B | 05A/05B dependen de la concurrencia entre ellas (A→B por diseño, deliberado); su veredicto lo emite un observador independiente (pg_stat_activity), no ellas mismas; no se declara independencia de orden | RESUELTO_VERIFICADO (diseño deliberado; veredicto por observador independiente) |

Criterio de clasificación: se marca BLOQUEADO_CON_CAUSA_DEMOSTRADA sólo si la causa es estructural y el desbloqueo requiere un recurso externo (CCI-DEV real, servidor, custodio); **NO_RESUELTO** si el defecto/limitación es técnico y sigue abierto. No se usa PARTIAL para ocultar defectos.

## Límites estructurales adicionales (documentados, probados donde se indica)
| Límite | Causa demostrada | Mitigación existente | Clasificación |
|---|---|---|---|
| Quien controla la máquina del operador puede invocar `psql` sin pasar por `ejecutar_script_verificado.sh` y así saltarse identidad firmada, aprobación del custodio y auditoría del cliente | Los controles del cliente corren en el cliente | Preflight de la guarda (hash aprobado), autorización de operadores y separación de funciones en la guarda SQL, privilegios del rol, `RAISE LOG` del servidor | BLOQUEADO_CON_CAUSA_DEMOSTRADA (exige control del lado del servidor en CCI-DEV: roles, event triggers, pg_hba; EXT-02/L05) |
| Un clon físico de DEV que ocupa el endpoint exacto de DEV es indistinguible de DEV | Misma identidad física (E2E-09) | No es riesgo AG-18 (solo datos de DEV); reemitir token tras clonar | Aceptado y documentado (no es defecto) |
| Cambio de destino entre la verificación de identidad y la ejecución (p. ej. DNS) | La verificación es de una conexión previa | La guarda vuelve a leer `system_identifier` dentro de la sesión real y aplica allowlist/denylist | BLOQUEADO_CON_CAUSA_DEMOSTRADA (EXT-03: listas vacías) |
| 05A/05B dependen de la concurrencia entre ellas | Diseño deliberado (A retiene el bloqueo, B espera) | Observador independiente (`pg_stat_activity`/`pg_blocking_pids`); 15/15 incl. negativos | RESUELTO_VERIFICADO en lo local; real en CCI-DEV: EXT-04-L06 |
| Marcadores temporales de salidas propias en la etapa H (archivos que la propia ejecución crea y luego sobrescribe) | La reconciliación cita salidas que se generan después | Anclaje externo (SHA-256, totales del stdout, id de ejecución) fuera del directorio de cierre; verificación en I y K; controles negativos | RESUELTO_VERIFICADO |
