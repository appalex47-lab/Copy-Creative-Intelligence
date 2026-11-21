-- ====================================================================================================
-- NO EJECUTADOS — REQUIEREN AUTORIZACIÓN Y CCI-DEV
-- Preparado en el cierre técnico de Fase 0; NO se ejecutó contra ningún proyecto Supabase. Prohibido en CCI-PROD.
-- Sólo el propietario puede autorizar su ejecución, y únicamente en CCI-DEV. Escribe dentro de una transacción
-- que termina SIEMPRE en ROLLBACK (no deja datos). Aun así, es una operación de escritura: requiere autorización.
-- ====================================================================================================
-- Sesión B (lanzar 1–2 s después que A). Esperado: B se BLOQUEA mientras A no termina; al hacer rollback A, B inserta; si A hiciera commit, B fallaría con 23P01.
\set ON_ERROR_STOP on
do $$ begin if coalesce(current_setting('cci.validacion_autorizada', true),'') <> 'SI-CCI-DEV' then raise exception 'NO EJECUTADO: requiere autorizacion expresa del propietario y proyecto CCI-DEV (cci.validacion_autorizada)'; end if; end $$;
begin;
insert into public.piece_reviewer_assignments(id, organization_id, piece_id, reviewer_id, assigned_by, valid_during, reason) values (gen_random_uuid(), :'org', :'piece', :'reviewer_b', :'reviewer_b', tstzrange(now(), null, '[)'), 'concurrencia B');
select now() as b_inserto_en;
rollback;
