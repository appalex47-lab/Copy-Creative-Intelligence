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
-- Guarda (idéntica en los 6 scripts)
do $$ declare a text := coalesce(current_setting('cci.validacion_autorizada', true),''); e text := coalesce(current_setting('cci.entorno', true),'');
begin
  if a = 'SI-CCI-DEV' and e = 'CCI-DEV' then null;
  elsif a = 'SI-LOCAL-TEMPORAL' and e = 'LOCAL-TEMPORAL' and current_database() ~ '^cci_' and inet_server_addr() is null then null;
  else raise exception 'NO EJECUTADO: requiere autorizacion expresa del propietario y proyecto CCI-DEV (cci.validacion_autorizada + cci.entorno), o ejecucion local temporal por socket Unix'; end if; end $$;
\ir 04_lib_clasificador.sql
select to_regclass('public.piece_reviewer_assignments') is not null as tabla_ok \gset
\if :tabla_ok
\else
  \echo 'BLOCKED: public.piece_reviewer_assignments no existe; prueba NO VERIFICABLE EN ENTORNO FÍSICO'
  \quit
\endif
begin;
set local lock_timeout = '10s'; set local statement_timeout = '30s';
select o_clase, o_sqlstate, case when o_clase = 'OK' then 'SESION_A_LISTA' else 'BLOCKED' end as sesion_a
from pg_temp.ejecuta(format('insert into public.piece_reviewer_assignments(id, organization_id, piece_id, reviewer_id, assigned_by, valid_during, reason) values (gen_random_uuid(), %L, %L, %L, %L, tstzrange(now(), null, ''[)''), ''concurrencia A'')', :'org', :'piece', :'reviewer_a', :'reviewer_a'), null, null, null, false);
select pg_sleep(5);   -- mantiene la fila sin confirmar mientras B intenta lo mismo
rollback;
