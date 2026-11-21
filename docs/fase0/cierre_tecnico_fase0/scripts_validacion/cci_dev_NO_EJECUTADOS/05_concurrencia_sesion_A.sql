-- ====================================================================================================
-- NO EJECUTADOS — REQUIEREN AUTORIZACIÓN Y CCI-DEV
-- Preparado en el cierre técnico de Fase 0; NO se ejecutó contra ningún proyecto Supabase. Prohibido en CCI-PROD.
-- Sólo el propietario puede autorizar su ejecución, y únicamente en CCI-DEV. Escribe dentro de una transacción
-- que termina SIEMPRE en ROLLBACK (no deja datos). Aun así, es una operación de escritura: requiere autorización.
-- ====================================================================================================
-- Sesión A de la prueba de concurrencia CONC-01 (ver 05_concurrencia_sesion_B.sql y PRUEBAS_RLS_PRIVILEGIOS_CONCURRENCIA.md). Variables: org, piece, reviewer_a.
\set ON_ERROR_STOP on
do $$ begin if coalesce(current_setting('cci.validacion_autorizada', true),'') <> 'SI-CCI-DEV' then raise exception 'NO EJECUTADO: requiere autorizacion expresa del propietario y proyecto CCI-DEV (cci.validacion_autorizada)'; end if; end $$;
begin;
-- PLANTILLA: operación que compite (ejemplo: asignación de revisor con vigencia; ajustar a la tabla real)
insert into public.piece_reviewer_assignments(id, organization_id, piece_id, reviewer_id, assigned_by, valid_during, reason) values (gen_random_uuid(), :'org', :'piece', :'reviewer_a', :'reviewer_a', tstzrange(now(), null, '[)'), 'concurrencia A');
select pg_sleep(5);   -- mantiene la fila sin confirmar mientras B intenta lo mismo
rollback;
