# MATRIZ DISEÑO LÓGICO → ESQUEMA TEMPORAL → ESQUEMA FÍSICO ESPERADO

**Alcance.** Revisión del fixture PostgreSQL temporal de V20 (63/63 pruebas, 14/14 mutaciones; `03_SCRIPTS/PE_POSTGRESQL_V20/`) más la extensión local de este cierre (`scripts_validacion/local_ext/`). **No se afirma equivalencia con Supabase real.** «Esquema físico esperado» = lo que CCI-DEV deberá mostrar al inventariar (plan en `PLAN_VALIDACION_CCI_DEV.md`); no existe todavía.

## 1. Qué es el fixture (verificado por lectura de `01_fixture.sql`, 87 líneas)

- **Motor:** PostgreSQL 16.15 en clúster temporal local, un único rol superusuario `cci_test` (sin RLS, sin roles de aplicación, sin `GRANT/REVOKE`). Base `cci_v20_test`.
- **Tablas presentes (11 + 1 de resultados):** `organizations`, `memberships`, `channel_rules`, `channel_formats`, `creative_pieces`, `copy_versions`, `approvals`, `impact_evaluations`, `brief_field_attributions`, `contribution_events`, `attribution_discard_resolutions` (+ `resultados`).
- **Triggers presentes (6):** `t_master` (master_piece_id inmutable), `t_cf_upd` (channel_formats sin UPDATE/DELETE), `t_cv_imm` (copy_versions inmutable), `t_adr_ins` (validación al insertar resolución), `t_adr_imm` (resoluciones inmutables), `t_adr_trunc` (sin TRUNCATE).
- **Políticas RLS:** ninguna. **Privilegios:** ninguno. **Funciones de negocio:** ninguna (sólo funciones de trigger y el ayudante `t()`).
- **Columnas simplificadas:** el fixture omite columnas de la especificación (p. ej. `copy_versions` sin contenido, `approvals` sin `decision` ni fecha, `impact_evaluations` sin `kind`, `supersedes_evaluation_id`, `idempotency_key`, `correlation_id`, `request_fingerprint`).

## 2. Restricciones probadas y no probadas por el fixture V20

| Tipo | Probadas (evidencia V20) | No probadas |
|---|---|---|
| FK compuestas con `organization_id` | maestra↔adaptación de la misma org (PE-01a/b); versión derivada de versión inexistente / de otra pieza (PE-01c/d); aprobación ligada a (pieza, versión) (PE-04); par evaluado con 3 FK (PE-05); atribuciones y resoluciones (PG-AD-16..19) | FK a `campaigns`, `briefs`, `audits`, `creative_assets` y las otras 12 tablas nuevas |
| UNIQUE | (org,canal,formato) (PG-CF-03); (org,pieza,versión_no); par de 9 columnas (PE-05); resolución aceptada única por atribución (PG-AD-04, índice parcial) | unicidad de `idempotency_key`, `request_fingerprint` |
| CHECK | master≠id (PE-02d); normalización de canal/formato (PG-CF-04..07, 11..15); autorreferencia de resolución (PG-AD-20) | CHECK de rangos, de `decision`, de longitudes mínimas (no aprobadas) |
| Triggers de inmutabilidad | master (PE-02); versiones (PE-03); channel_formats; resoluciones (PG-AD-15, mutación MUT-14) | trigger de elegibilidad R1–R9 (IG5-95 limitado: sólo 3 pruebas PG-AD-08..10), triggers T-02 de transición de estado, `asset_match`, `record_approval`, independencia del aprobador |
| Índices | índice parcial `u_adr_aceptada` (mutación MUT-13 lo quita y se detecta) | rendimiento, índices para RLS |
| RLS / roles / privilegios | **nada** | **todo** |
| Concurrencia | nada en V20 | todo (este cierre añade 2 pruebas locales: CC-01, CC-02) |

## 3. Qué depende de triggers, políticas o privilegios (no extrapolable desde el fixture)

1. **Triggers:** las pruebas «P0001:INMUTABLE» demuestran que el trigger del fixture funciona, no que el trigger real (que será `SECURITY DEFINER`, con propietario `cci_records_owner`) esté bien definido.
2. **Políticas RLS:** el rol del fixture es superusuario y *se salta* RLS; ninguna prueba V20 puede decir nada sobre aislamiento entre organizaciones por política.
3. **Privilegios:** «sin INSERT/UPDATE/DELETE para anon/authenticated/service_role» (IG5-98, DG-20) sólo es comprobable con roles reales.

## 4. Qué sí puede extrapolarse (con cautela)

Semántica estándar de PostgreSQL: FK compuestas (MATCH SIMPLE: una columna nula en la FK desactiva la comprobación — relevante para `supersedes_evaluation_id` y `replaces_piece_id`), UNIQUE, CHECK, exclusión por rango y orden de evaluación de triggers. Reserva: la versión mayor de PostgreSQL de CCI-DEV no está verificada (el fixture usa 16.15), y el comportamiento de `locale`/`collation` puede diferir; el clúster local de este cierre se recreó en **UTF8 (C.UTF-8)** porque el primero era SQL_ASCII y falseaba pruebas de texto multibyte (EX-DG16f/g fallaban allí).

## 5. Matriz de las 41 tablas (27 base + 14 nuevas)

Estados: `PROBADO_FIXTURE` (prueba V20 PASS en el fixture), `PROBADO_PROTOTIPO_LOCAL` (prototipo de este cierre, tabla `*_x`, no equivalente a la tabla real), `SIN_PRUEBA` (no hay tabla temporal), `SOLO_DISEÑO`.

| # | Tabla (diseño lógico) | Esquema temporal | Esquema físico esperado en CCI-DEV | Prueba | Evidencia | Estado |
|---|---|---|---|---|---|---|
| 1 | organizations | presente (sólo `id`) | PK id; RLS sólo miembros | FK desde todo | PE-01 | PROBADO_FIXTURE (columnas), SIN_PRUEBA (RLS) |
| 2 | profiles | ausente | 1:1 con `auth.users` | — | — | SIN_PRUEBA |
| 3 | memberships | presente (PK org,user; `activo`) | + roles no vacío; RLS `is_member` | FK compuestas desde resoluciones y prototipos | PG-AD-16..19; EX-G9i/j | PROBADO_FIXTURE (FK); la FK no comprueba `activo` (EX-G9j) |
| 4 | role_permissions | ausente | 17 claves; lectura autenticada | revisión estática T-47 | ct_revision_estatica | SOLO_DISEÑO |
| 5 | membership_permission_grants | ausente | sólo `org.manage` concede | — | — | SIN_PRUEBA |
| 6 | activity_logs | ausente | sin UPDATE/DELETE | — | — | SIN_PRUEBA |
| 7 | campaigns | ausente | padre de briefs/piezas | — | — | SIN_PRUEBA |
| 8 | creative_pieces | presente (parcial: master, canal, formato, estado) | + campaign_id, brief, versión vigente; estado sólo vía `transition_piece_status` | PE-01, PE-02 | 10 pruebas PE | PROBADO_FIXTURE (maestra/adaptación); estado SIN_PRUEBA |
| 9 | brand_guidelines | ausente | — | — | — | SIN_PRUEBA |
| 10 | brand_guideline_versions | ausente | inmutable | — | — | SIN_PRUEBA |
| 11 | briefs | ausente | 16 campos | — | — | SIN_PRUEBA |
| 12 | copy_versions | presente (parcial) | + contenido, autor por trigger, master_copy_version_id, master_creative_asset_id | PE-01c/d/e, PE-03; EX-T03, EX-T06 | PE + EX | PROBADO_FIXTURE / PROTOTIPO_LOCAL (arte) |
| 13 | ai_runs | ausente | sin secretos | — | — | SIN_PRUEBA |
| 14 | ai_prompt_versions | ausente | inmutable | — | — | SIN_PRUEBA |
| 15 | ai_quotas | ausente | `consume_ai_quota` atómico | — | — | SIN_PRUEBA (concurrencia) |
| 16 | creative_assets | ausente (prototipo `assets_x`) | hash/MIME; inmutable | EX-T03e/f | EX | PROBADO_PROTOTIPO_LOCAL |
| 17 | audit_rubric_versions | ausente | pesos suman 100 | — | — | SIN_PRUEBA |
| 18 | audits | ausente | sólo inserción | — | — | SIN_PRUEBA |
| 19 | audit_findings | ausente | revisión vía `review_finding` | — | — | SIN_PRUEBA |
| 20 | promotion_rules | ausente | CHECK de precios y fechas | — | — | SIN_PRUEBA |
| 21 | validation_settings_versions | ausente | inmutable | — | — | SIN_PRUEBA |
| 22 | channel_rules | presente (parcial) | RLS; `org.manage` | PG-CF-08/09 | PG-CF | PROBADO_FIXTURE (FK) |
| 23 | comments | ausente | — | — | — | SIN_PRUEBA |
| 24 | commercial_block_exceptions | ausente | FK compuesta a audit_findings | — | — | SIN_PRUEBA |
| 25 | approvals | presente (sin `decision`) | + `decision` CHECK (DG-20), unique(org,id,copy_version_id), trigger de independencia | PE-04; EX-T78, EX-T80, EX-DG20 | PE + EX | PROBADO_FIXTURE / PROTOTIPO_LOCAL |
| 26 | performance_metrics | ausente | unique por periodo | — | — | SIN_PRUEBA |
| 27 | ab_tests | ausente | — | — | — | SIN_PRUEBA |
| 28 | piece_classification_events | ausente | — | — | — | SIN_PRUEBA |
| 29 | piece_reviewer_assignments | ausente (prototipo `_x`) | historial inmutable con vigencia (G-9) | EX-G9a..j; CC-01 | EX + CC | PROBADO_PROTOTIPO_LOCAL |
| 30 | impact_evaluations | presente (parcial) | + supersedes, kind, idempotency_key… | PE-05a..i; EX-T137..T140 | PE + EX | PROBADO_FIXTURE (par) / PROTOTIPO_LOCAL (sustitución) |
| 31 | publication_attempts | ausente | FK a assets y versiones | — | — | SIN_PRUEBA |
| 32 | channel_formats | presente (completa en columnas derivadas; sin PK) | PK no determinada (DG-19) | PG-CF-01..15 | PG-CF | PROBADO_FIXTURE |
| 33 | brief_versions | ausente | inmutable, cadena | — | — | SIN_PRUEBA |
| 34 | contribution_events | presente (3 columnas) | tipo, campo, origen | PG-AD | PG-AD | PROBADO_FIXTURE (mínimo) |
| 35 | copy_version_provenance | ausente | FK a assets | — | — | SIN_PRUEBA |
| 36 | promotion_snapshots | ausente | `integrity_status` | — | — | SIN_PRUEBA |
| 37 | brief_field_changes | ausente | — | — | — | SIN_PRUEBA |
| 38 | brief_field_attributions | presente (5 columnas) | + previous_attribution_id, estado | PG-AD | PG-AD | PROBADO_FIXTURE (mínimo) |
| 39 | promotion_field_changes | ausente | — | — | — | SIN_PRUEBA |
| 40 | promotion_field_attributions | ausente | — | — | — | SIN_PRUEBA |
| 41 | attribution_discard_resolutions | presente (completa en el fixture) | trigger R1–R9 completo | PG-AD-01..20 | PG-AD | PROBADO_FIXTURE (R1–R9 parcial: IG5-95 en 3 pruebas) |

**Conteo (contado por script sobre esta tabla):** 41 tablas de diseño; 11 con reflejo en el fixture V20; 2 más sólo con prototipo local (`creative_assets`, `piece_reviewer_assignments`); **28 sin ninguna prueba** (incluida `role_permissions`, sólo revisada de forma estática). Además, `approvals` e `impact_evaluations` ganan columnas/prototipos en la extensión local.

## 6. Diferencias diseño ↔ fixture que merecen atención

1. `channel_formats`: el fixture **no** define PK (la especificación tampoco la determina); ver recomendación DG-19 en `REGISTRO_DECISIONES_RECOMENDADAS.csv`.
2. `approvals` del fixture no distingue aprobación de rechazo: EX-T78d prueba que la FK sola admite citar una fila con otro valor; DG-20 lo cierra con CHECK.
3. FK con columna nula (`MATCH SIMPLE`): `supersedes_evaluation_id` nulo desactiva la FK; la sustitución «del mismo par» sólo se garantiza cuando no es nulo (comportamiento intencionado, no un defecto).
4. La especificación afirma «sin borrado»; el fixture lo logra con triggers, no con privilegios: ambos son necesarios.

## 7. Veredicto de la revisión

El fixture es evidencia **válida y suficiente para la semántica de FK/UNIQUE/CHECK/triggers de las 11 tablas que modela**, e **insuficiente** para RLS, privilegios, funciones `SECURITY DEFINER`, concurrencia y el 68 % de las tablas (28 de 41). No debe citarse como validación del esquema ni de Supabase.
