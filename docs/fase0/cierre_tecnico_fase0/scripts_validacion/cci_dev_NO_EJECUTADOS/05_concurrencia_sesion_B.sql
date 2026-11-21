-- ====================================================================================================
-- NO EJECUTADO CONTRA CCI-DEV NI CCI-PROD — REQUIERE AUTORIZACIÓN Y CCI-DEV
-- PLANTILLA (v2): CONC-01 asignación de revisor concurrente (G-9, exclusión por rango). Depende de public.piece_reviewer_assignments con las columnas
--   (id, organization_id, piece_id, reviewer_id, assigned_by, valid_during tstzrange, reason): diseño PROPUESTO (G-9 recomendado, NO aprobado) y aún inexistente.
-- Escritura: se inserta una fila no confirmada y la sesión termina en ROLLBACK (sin residuos). Requiere autorización por ser escritura.
-- Uso: lanzar A; 1–2 s después lanzar B (otra conexión). Variables: org, piece, reviewer_a (A), reviewer_b (B). Datos de PRUEBA preexistentes.
-- Resultado: A informa SESION_A_LISTA o BLOCKED; B informa PASS (esperó el rollback de A: bloqueo por la restricción de exclusión), FAIL (no esperó: restricción
--   inefectiva) o BLOCKED (error técnico). La prueba de que B recibe 23P01 si A hiciera COMMIT queda como variante manual NO automatizada (NOT VERIFIED).
-- ====================================================================================================
\set ON_ERROR_STOP on
\set cci_script '05B'
-- Guarda de destino compartida (H-03): 00_preflight_guarda.sql (hash externo + ejecución de la copia verificada de 00_guarda_destino.sql) y 00_verificar_marcador.sql (marcador por ejecución)
\ir 00_preflight_guarda.sql
\set cci_script '05B'
\ir 00_verificar_marcador.sql
\ir 04_lib_clasificador.sql
select pg_catalog.to_regclass('public.piece_reviewer_assignments') is not null as tabla_ok \gset
\if :tabla_ok
\else
  \echo 'BLOCKED: public.piece_reviewer_assignments no existe; prueba NO VERIFICABLE EN ENTORNO FÍSICO'
  \quit
\endif
-- PRECONDICIÓN INDEPENDIENTE (resolución final, AUD-RF-04): B no confía en la salida de A; exige que el SERVIDOR muestre OTRA sesión 'cci_05A' con transacción abierta y xid asignado.
select pg_catalog.count(*) > 0 as a_presente, coalesce(pg_catalog.min(pid), 0) as a_pid_observado from pg_catalog.pg_stat_activity
  where application_name = 'cci_05A' and datname = pg_catalog.current_database() and pid <> pg_catalog.pg_backend_pid() and backend_xid is not null and state in ('active','idle in transaction') \gset
\if :a_presente
\else
  \echo 'BLOCKED [05-A-NO-PRESENTE]: el servidor no muestra una sesión cci_05A con transacción abierta (o el rol no puede ver su xid); B no se ejecuta ni emite PASS'
  \quit
\endif
begin;
set local lock_timeout = '15s'; set local statement_timeout = '30s';
set local application_name = 'cci_05B';
select pg_catalog.pg_backend_pid() as pid_b \gset
select pg_catalog.clock_timestamp() as t0 \gset
create temp table res_b as select o_clase, o_sqlstate, o_msg from pg_temp.ejecuta(pg_catalog.format('insert into public.piece_reviewer_assignments(id, organization_id, piece_id, reviewer_id, assigned_by, valid_during, reason) values (pg_catalog.gen_random_uuid(), %L, %L, %L, %L, pg_catalog.tstzrange(pg_catalog.now(), null, ''[)''), ''concurrencia B'')', :'org', :'piece', :'reviewer_b', :'reviewer_b'), null, null, null, true);
select pg_catalog.round(extract(epoch from pg_catalog.clock_timestamp() - :'t0'::timestamptz)::numeric, 2) as espera_s, o_clase, o_sqlstate,
  case when o_clase = 'OK' and extract(epoch from pg_catalog.clock_timestamp() - :'t0'::timestamptz) >= 2 then 'ESPERO'
       when o_clase = 'OK' then 'NO_ESPERO'                  -- no esperó: la exclusión no bloqueó
       when o_sqlstate = '23P01' then 'CONFLICTO_TRAS_COMMIT_DE_A'  -- A ya confirmó: conflicto real, pero no es el escenario de esta plantilla
       when o_clase in ('PERMISOS','ESTRUCTURA','FUNCION_INEXISTENTE','SINTAXIS') then 'BLOCKED' else 'FAIL' end as veredicto_propio, :'pid_b' as pid_b, :'a_pid_observado' as a_pid_observado
from res_b;
rollback;
