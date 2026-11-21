# Limitaciones residuales (no se convierten en aprobación)

## BLOCKED — dependencia externa (impiden FASE0_READY_FOR_OWNER_ACCEPTANCE)
| ID | Qué falta exactamente | Detalle |
|---|---|---|
| ID-13 | validación real en Supabase (no autorizada ni disponible) | system_identifier/pg_control_system() y project ref desde SQL en Supabase |
| EXT-03 | listas de destinos DEV/PROD autorizados (@@DEV_ALLOW@@, @@PROD_DENY@@) vacías: el propietario debe aportar identificadores reales; no se inventan | 00_guarda_destino.sql |
| EXT-01 | custodio externo del hash aprobado (SHA256SUMS_CCI.txt / guarda) no definido; sin él la verificación de integridad no es protección operativa | variable CCI_HASH_CUSTODIO_EXTERNO_CONFIRMADO ausente |
| EXT-04 | 5 controles V26 NO VERIFICADO (L04–L08) requieren CCI-DEV o verificación del propietario | LR-01 VIGENTE |
| EXT-02 | compatibilidad con Supabase: TEMP, pg_control_system(), PGOPTIONS por pooler y project ref sólo verificables en un proyecto real (no autorizado) | MATRIZ_COMPATIBILIDAD_SUPABASE.md |

## PARTIAL — limitación estructural observada
| Origen | ID | Descripción |
|---|---|---|
| adversarial | E2-cor-01 | LIMITACIÓN ESTRUCTURAL; no es aprobación |
| adversarial | E2-cor-02 | LIMITACIÓN ESTRUCTURAL; no es aprobación |
| adversarial | E2-cor-03 | LIMITACIÓN ESTRUCTURAL; no es aprobación |
| adversarial | E2-cor-04 | LIMITACIÓN ESTRUCTURAL; no es aprobación |
| adversarial | E2-cor-05A | LIMITACIÓN ESTRUCTURAL; no es aprobación |
| adversarial | E2-cor-05B | LIMITACIÓN ESTRUCTURAL; no es aprobación |
| search_path | SPD7 | operadores no calificados: con el chequeo de search_path desactivado 4/6 scripts son secuestrables; sólo el chequeo los protege |
| identidad | ID-05 | LIMITACIÓN ESTRUCTURAL AG-18: system_identifier+base no distinguen un clon físico/restauración de su origen |
| identidad | ID-06 | seguro pero inservible: sin una identidad externa no se pueden distinguir |
| identidad | ID-10 | la protección es tan buena como la lista externa; una restauración sobre el MISMO endpoint no se distingue |
| orden | 05A-05B | 05A/05B dependen de la concurrencia entre ellas (A→B por diseño); no se declara independencia de orden |

## Clasificación del registro histórico de limitaciones
27 limitaciones en `MATRIZ_LIMITACIONES_RESIDUALES.csv`: 18 VIGENTE, 4 PARCIALMENTE_RESUELTA, 5 RESUELTA (sin cambio; ninguna BLOQUEADA nueva en el registro: los bloqueos de esta operación son las dependencias externas de arriba).
Otras: stdin no soportado; operadores sin calificar (sólo el chequeo de search_path los protege); guarda falsa + control del hash aprobado; AG-18 (clon físico); pooler sólo simulado; hash externo sin custodio.
