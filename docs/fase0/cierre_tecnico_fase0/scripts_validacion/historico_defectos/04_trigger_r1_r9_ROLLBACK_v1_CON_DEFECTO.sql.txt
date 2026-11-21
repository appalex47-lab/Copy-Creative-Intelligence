-- ====================================================================================================
-- NO EJECUTADOS — REQUIEREN AUTORIZACIÓN Y CCI-DEV
-- Preparado en el cierre técnico de Fase 0; NO se ejecutó contra ningún proyecto Supabase. Prohibido en CCI-PROD.
-- Sólo el propietario puede autorizar su ejecución, y únicamente en CCI-DEV. Escribe dentro de una transacción
-- que termina SIEMPRE en ROLLBACK (no deja datos). Aun así, es una operación de escritura: requiere autorización.
-- ====================================================================================================
-- Variables (psql -v): org, attr (atribución a excluir), field, affected, requester, change_actor, trigger_event, evidence_version, prior_attr_other_source
-- Resolutores de prueba: r_ok (cumple R1..R9), r_nomember (R1), r_noreview (R2), r_affected=:affected (R3), r_requester=:requester (R4), r_actor=:change_actor (R5),
--   r_direct (R6), r_inherited (R7), r_othersrc (R8), r_benef (R9). Deben existir como datos de PRUEBA preparados por el propietario.
-- PLANTILLA: la lista de columnas sigue la definición de attribution_discard_resolutions de la especificación; ajustar al esquema real tras INV-02.
\set ON_ERROR_STOP on
do $$ begin if coalesce(current_setting('cci.validacion_autorizada', true),'') <> 'SI-CCI-DEV' then raise exception 'NO EJECUTADO: requiere autorizacion expresa del propietario y proyecto CCI-DEV (cci.validacion_autorizada)'; end if; end $$;
select set_config('cci.org', :'org', false), set_config('cci.attr', :'attr', false) \gset
begin;
create temp table r_res(id text, regla text, esperado text, obtenido text, resultado text) on commit drop;
create or replace function pg_temp.intenta(p_resolutor uuid, p_outcome text default 'aceptada', p_evidence text default 'evidencia de prueba') returns text language plpgsql as $f$
begin
  perform set_config('request.jwt.claims', json_build_object('sub', p_resolutor, 'role','authenticated')::text, true);
  begin
    -- Llamar a la función real de escritura autorizada (p. ej. public.resolve_attribution_discard) con los parámetros reales
    perform public.resolve_attribution_discard(current_setting('cci.org')::uuid, current_setting('cci.attr')::uuid, p_outcome, p_evidence);
    return 'OK';
  exception when others then return sqlstate || ':' || left(sqlerrm, 60); end; end $f$;
insert into r_res values ('R1-neg','R1 miembro activo','rechazo', pg_temp.intenta(:'r_nomember'::uuid), '');
insert into r_res values ('R2-neg','R2 piece.review','rechazo', pg_temp.intenta(:'r_noreview'::uuid), '');
insert into r_res values ('R3-neg','R3 no afectado','rechazo', pg_temp.intenta(:'affected'::uuid), '');
insert into r_res values ('R4-neg','R4 no solicitante','rechazo', pg_temp.intenta(:'requester'::uuid), '');
insert into r_res values ('R5-neg','R5 no actor del cambio','rechazo', pg_temp.intenta(:'change_actor'::uuid), '');
insert into r_res values ('R6-neg','R6 no directo en cadena','rechazo', pg_temp.intenta(:'r_direct'::uuid), '');
insert into r_res values ('R7-neg','R7 no heredado activo','rechazo', pg_temp.intenta(:'r_inherited'::uuid), '');
insert into r_res values ('R8-neg','R8 no excluido por otra fuente','rechazo', pg_temp.intenta(:'r_othersrc'::uuid), '');
insert into r_res values ('R9-neg','R9 no beneficiario','rechazo', pg_temp.intenta(:'r_benef'::uuid), '');
insert into r_res values ('R-ev1','evidencia vacía','rechazo', pg_temp.intenta(:'r_ok'::uuid, 'aceptada', ''), '');
insert into r_res values ('R-ok','todas las reglas se cumplen (positivo)','OK', pg_temp.intenta(:'r_ok'::uuid), '');
update r_res set resultado = case when (esperado='OK' and obtenido='OK') or (esperado='rechazo' and obtenido <> 'OK') then 'PASS' else 'FAIL' end;
select * from r_res order by id;
rollback;
