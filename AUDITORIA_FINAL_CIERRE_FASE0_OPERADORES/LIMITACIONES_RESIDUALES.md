# Limitaciones residuales

## Técnicas que permanecen (no dependen de recursos externos)
| Limitación | Alcance | Mitigación |
|---|---|---|
| Un rol **superusuario** o el propietario de la base puede crear operadores tras la comprobación de la guarda (F-01: demostrado con superusuario local) | La guarda no puede defenderse de quien ya controla la base | Principio de mínimo privilegio: el operador no es superusuario ni propietario (comprobado en modo DEV); auditoría en servidor |
| Un homónimo de función/operador en `pg_catalog` no es creable por no superusuarios | — | — |
| Los controles del cliente (ejecutor, identidad firmada, aprobación) se saltan con `psql` directo si alguien controla la máquina del operador | Estructural | La guarda SQL, la autorización de operadores y los privilegios efectivos siguen aplicando; control del lado del servidor pendiente (EXT-02/L05) |
| La guarda rechaza extensiones con operadores de símbolo estándar y casts de usuario en la base (decisión conservadora) | Podría rechazar una base legítima con extensiones tipo `citext` en `public` | Mover la extensión a otro esquema; decisión del propietario |
| Los casts de usuario se rechazan globalmente (`pg_cast.oid >= 16384`) | Extensiones que añaden casts (p. ej. hstore, citext) | ídem |

## Dependientes de recursos externos (BLOQUEADO_CON_CAUSA_DEMOSTRADA; fichas en PLAN_DESBLOQUEO_EXTERNOS.md)
| ID | Qué falta |
|---|---|
| ID-13 | validación real en Supabase (no autorizada ni disponible) |
| EXT-03 | listas de destinos DEV/PROD autorizados: RECHAZADO [L-DEV-VACIA] dev_allow vacía: el propietario debe aportar al menos un 'system_identifier\|base' de CCI-DEV |
| EXT-01 | custodio externo del hash aprobado no definido: falta la aprobación firmada (CCI_APROBACION_CUSTODIO) y la clave pública con su SHA-256 (CCI_CUSTODIO_PUBKEY, CCI_CUSTODIO_PUBKEY_SHA256). El mecanismo criptográfico está probado con claves de prueba; NO hay custodio real |
| EXT-02 | compatibilidad con Supabase CCI-DEV (TEMP, pg_control_system(), PGOPTIONS por pooler, project ref, pooler): sólo verificable en CCI-DEV; la sonda existe y está probada en local (SIMULADO_LOCAL) |
| EXT-04-L04 | equivalencia del PostgreSQL temporal con el esquema físico aprobado (no existe esquema físico aprobado) |
| EXT-04-L05 | validación física en CCI-DEV |
| EXT-04-L06 | RLS, privilegios y concurrencia reales en CCI-DEV |
| EXT-04-L07 | trigger de elegibilidad R1–R9 en entorno físico |
| EXT-04-L08 | HV-02/PO-05: confirmación del propietario sobre la Adenda v9 (el documento no existe en el repositorio) |

## Limitaciones estructurales declaradas por las pruebas históricas (PARTIAL, clasificadas en el expediente anterior)
| Origen | ID | Descripción |
|---|---|---|
| adversarial | E2-cor-01 | LIMITACIÓN ESTRUCTURAL; no es aprobación |
| adversarial | E2-cor-02 | LIMITACIÓN ESTRUCTURAL; no es aprobación |
| adversarial | E2-cor-03 | LIMITACIÓN ESTRUCTURAL; no es aprobación |
| adversarial | E2-cor-04 | LIMITACIÓN ESTRUCTURAL; no es aprobación |
| adversarial | E2-cor-05A | LIMITACIÓN ESTRUCTURAL; no es aprobación |
| adversarial | E2-cor-05B | LIMITACIÓN ESTRUCTURAL; no es aprobación |
| identidad | ID-05 | LIMITACIÓN ESTRUCTURAL AG-18: system_identifier+base no distinguen un clon físico/restauración de su origen |
| identidad | ID-06 | seguro pero inservible: sin una identidad externa no se pueden distinguir |
| identidad | ID-10 | la protección es tan buena como la lista externa; una restauración sobre el MISMO endpoint no se distingue |
| orden | 05A-05B | 05A/05B dependen de la concurrencia entre ellas (A→B por diseño, deliberado); su veredicto lo emite un observador independiente (pg_stat_activity), no ellas mismas; no se declara independencia de orden |

## No verificado
Todo lo que requiere CCI-DEV/Supabase reales (roles de plataforma, pooler, PGOPTIONS por pooler, esquema físico, trigger físico); extensiones y sus operadores reales en CCI-DEV.
