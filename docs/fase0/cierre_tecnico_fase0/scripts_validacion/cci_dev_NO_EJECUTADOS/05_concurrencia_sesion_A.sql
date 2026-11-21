-- ====================================================================================================
-- NO EJECUTADO CONTRA CCI-DEV NI CCI-PROD — REQUIERE AUTORIZACIÓN Y CCI-DEV
-- PLANTILLA (v2): CONC-01 asignación de revisor concurrente (G-9, exclusión por rango). Depende de public.piece_reviewer_assignments con las columnas
--   (id, organization_id, piece_id, reviewer_id, assigned_by, valid_during tstzrange, reason): diseño PROPUESTO (G-9 recomendado, NO aprobado) y aún inexistente.
-- Escritura: se inserta una fila no confirmada y la sesión termina en ROLLBACK (sin residuos). Requiere autorización por ser escritura.
-- Uso: lanzar A; 1–2 s después lanzar B (otra conexión). Variables: org, piece, reviewer_a (A), reviewer_b (B). Datos de PRUEBA preexistentes.
-- Resultado: A informa SESION_A_LISTA (con su pid y xid) o BLOCKED. A NO valida a B ni B a A: el veredicto final lo emite ct_verificar_05.py con un OBSERVADOR independiente (pg_stat_activity/pg_blocking_pids desde otra conexión); B informa PASS (esperó el rollback de A: bloqueo por la restricción de exclusión), FAIL (no esperó: restricción
--   inefectiva) o BLOCKED (error técnico). La prueba de que B recibe 23P01 si A hiciera COMMIT queda como variante manual NO automatizada (NOT VERIFIED).
-- ====================================================================================================
\set ON_ERROR_STOP on
\set cci_script '05A'
-- Guarda de destino compartida (H-03): 00_preflight_guarda.sql (hash externo + ejecución de la copia verificada de 00_guarda_destino.sql) y 00_verificar_marcador.sql (marcador por ejecución)
\ir 00_preflight_guarda.sql
\set cci_script '05A'
\ir 00_verificar_marcador.sql
\ir 04_lib_clasificador.sql
select pg_catalog.to_regclass('public.piece_reviewer_assignments') is not null as tabla_ok \gset
\if :tabla_ok
\else
  \echo 'BLOCKED: public.piece_reviewer_assignments no existe; prueba NO VERIFICABLE EN ENTORNO FÍSICO'
  \quit
\endif
begin;
set local lock_timeout = '10s'; set local statement_timeout = '30s';
set local application_name = 'cci_05A';   -- identificación VERIFICABLE por un observador independiente (pg_stat_activity); no es evidencia por sí sola
select o_clase, o_sqlstate, case when o_clase = 'OK' then 'SESION_A_LISTA' else 'BLOCKED' end as sesion_a, pg_catalog.pg_backend_pid() as pid_a, pg_catalog.txid_current() as xid_a
from pg_temp.ejecuta(pg_catalog.format('insert into public.piece_reviewer_assignments(id, organization_id, piece_id, reviewer_id, assigned_by, valid_during, reason) values (pg_catalog.gen_random_uuid(), %L, %L, %L, %L, pg_catalog.tstzrange(pg_catalog.now(), null, ''[)''), ''concurrencia A'')', :'org', :'piece', :'reviewer_a', :'reviewer_a'), null, null, null, false);
select pg_catalog.pg_sleep(5);   -- mantiene la fila sin confirmar mientras B intenta lo mismo
rollback;
