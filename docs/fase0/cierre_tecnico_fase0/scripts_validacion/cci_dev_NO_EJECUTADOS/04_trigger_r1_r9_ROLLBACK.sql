-- ====================================================================================================
-- NO EJECUTADO CONTRA CCI-DEV NI CCI-PROD — REQUIERE AUTORIZACIÓN Y CCI-DEV
-- Versión 2 (corrección consolidada): sustituye la v1, cuyo ayudante intenta() capturaba cualquier excepción y las pruebas negativas daban PASS
-- a cualquier resultado distinto de 'OK' (falsos PASS por función inexistente, permisos o estructura). La v1 se conserva en
-- ../historico_defectos/04_trigger_r1_r9_ROLLBACK_v1_CON_DEFECTO.sql.txt como evidencia del defecto.
-- ESTADO: PLANTILLA EJECUTABLE. Depende de una implementación física (public.resolve_attribution_discard, tablas y permisos) que HOY NO EXISTE
--   en ningún entorno. Sin ella el resultado es: NO VERIFICABLE EN ENTORNO FÍSICO (batería BLOQUEADA). No se simula la implementación.
-- Escritura: ninguna persistente. Cada caso se ejecuta en un sub-bloque cuyo efecto se revierte (excepción centinela) y la sesión termina en ROLLBACK;
--   al final se comprueba que el recuento de resoluciones no cambió (sin residuos).
-- Modo de uso (propietario, sólo CCI-DEV): PGOPTIONS="-c cci.validacion_autorizada=SI-CCI-DEV -c cci.entorno=CCI-DEV" psql ... -v org=.. -v attr=.. (ver variables abajo)
-- ====================================================================================================
-- Variables obligatorias (psql -v): org, attr (atribución a excluir), affected (contribuyente afectado de attr), requester, change_actor,
--   r_ok (cumple R1–R9), r_nomember (R1), r_noreview (R2), r_direct (R6), r_inherited (R7), r_othersrc (R8), r_benef (R9). Son datos de PRUEBA del propietario.
-- Variables opcionales:
--   fn_regproc  = firma esperada. Por defecto 'public.resolve_attribution_discard(uuid,text,text)'  [PROPUESTA: la especificación (línea 3625) lista las entradas "atribución, motivo, evidencia" sin tipos ni parámetro de resultado]
--   fn_call     = plantilla format() de la llamada, con tres %L (atribución, motivo, evidencia). Por defecto 'select public.resolve_attribution_discard(%L::uuid, %L, %L)'
--   exec_role   = rol con el que se llama (por defecto authenticated)
--   code_r1..code_r9, code_rev = contrato de error esperado 'SQLSTATE[:prefijo del mensaje]'. POR DEFECTO VACÍOS: la especificación NO define SQLSTATE ni código de dominio
--                 para R1–R9 (BRECHA BRECHA-R1R9-01). Con el contrato vacío, un rechazo observado sólo puede ser PARTIAL, nunca PASS.
\set ON_ERROR_STOP on
\set cci_script '04'
-- Guarda de destino compartida (H-03): identidad efectiva del servidor + allowlist/denylist literales; ver 00_guarda_destino.sql (falla de forma segura).
\ir 00_preflight_guarda.sql
\set cci_script '04'
\ir 00_verificar_marcador.sql
\if :{?fn_regproc}
\else
  \set fn_regproc 'public.resolve_attribution_discard(uuid,text,text)'
\endif
\if :{?fn_call}
\else
  \set fn_call 'select public.resolve_attribution_discard(%L::uuid, %L, %L)'
\endif
\if :{?exec_role}
\else
  \set exec_role authenticated
\endif
\if :{?reason}
\else
  \set reason 'motivo de prueba'
\endif
\if :{?evidence}
\else
  \set evidence 'evidencia de prueba que cita la atribucion y la version'
\endif
\if :{?code_r1}
\else
  \set code_r1 ''
\endif
\if :{?code_r2}
\else
  \set code_r2 ''
\endif
\if :{?code_r3}
\else
  \set code_r3 ''
\endif
\if :{?code_r4}
\else
  \set code_r4 ''
\endif
\if :{?code_r5}
\else
  \set code_r5 ''
\endif
\if :{?code_r6}
\else
  \set code_r6 ''
\endif
\if :{?code_r7}
\else
  \set code_r7 ''
\endif
\if :{?code_r8}
\else
  \set code_r8 ''
\endif
\if :{?code_r9}
\else
  \set code_r9 ''
\endif
\if :{?code_rev}
\else
  \set code_rev ''
\endif
-- Biblioteca del arnés (objetos pg_temp; sin datos de negocio)
\ir 04_lib_clasificador.sql
select pg_catalog.set_config('cci.org', :'org', false), pg_catalog.set_config('cci.attr', :'attr', false), pg_catalog.set_config('cci.fn_regproc', :'fn_regproc', false), pg_catalog.set_config('cci.fn_call', :'fn_call', false),
       pg_catalog.set_config('cci.reason', :'reason', false), pg_catalog.set_config('cci.evidence', :'evidence', false), pg_catalog.set_config('cci.exec_role', :'exec_role', false),
       pg_catalog.set_config('cci.r_ok', :'r_ok', false), pg_catalog.set_config('cci.r_nomember', :'r_nomember', false), pg_catalog.set_config('cci.affected', :'affected', false),
       pg_catalog.set_config('cci.requester', :'requester', false), pg_catalog.set_config('cci.change_actor', :'change_actor', false) \gset
select case when pg_catalog.to_regclass('public.attribution_discard_resolutions') is null then -1 else (pg_catalog.xpath('/row/c/text()', pg_catalog.query_to_xml('select pg_catalog.count(*) as c from public.attribution_discard_resolutions', false, true, '')))[1]::text::bigint end as pre_count \gset
create temp table pre(id text, descripcion text, estado text, detalle text);
-- ====== PRECONDICIONES (autocommit; sólo lectura de catálogos y de datos de prueba) ======
do $$ declare fn oid; falt text; v_n int; v_def text;
begin
  insert into pre values ('PRE-01','versión PostgreSQL >= 13 (gen_random_uuid en el núcleo; capacidades usadas por el diseño)', case when pg_catalog.current_setting('server_version_num')::int >= 130000 then 'OK' else 'BLOCKED' end, pg_catalog.current_setting('server_version'));
  fn := pg_catalog.to_regprocedure(pg_catalog.current_setting('cci.fn_regproc'));
  insert into pre values ('PRE-02','la función existe con la firma exacta esperada', case when fn is not null then 'OK' else 'BLOCKED' end, pg_catalog.current_setting('cci.fn_regproc') || case when fn is null then ' NO EXISTE' else '' end);
  if fn is not null then
    insert into pre select 'PRE-03','propietario/seguridad de la función (diseño: records_owner; INFORMATIVO)','INFO', 'owner='||pg_catalog.pg_get_userbyid(p.proowner)||' security_definer='||p.prosecdef||' config='||coalesce(p.proconfig::text,'(ninguna)') from pg_proc p where p.oid = fn;
  end if;
  select pg_catalog.string_agg(t, ',') into falt from pg_catalog.unnest(array['attribution_discard_resolutions','memberships','brief_field_attributions','promotion_field_attributions','copy_version_provenance','contribution_events','role_permissions','membership_permission_grants']) t where pg_catalog.to_regclass('public.'||t) is null;
  insert into pre values ('PRE-04','tablas requeridas existen', case when falt is null then 'OK' else 'BLOCKED' end, coalesce('faltan: '||falt,'todas presentes'));
  select pg_catalog.string_agg(c, ',') into falt from pg_catalog.unnest(array['id','organization_id','source_kind','brief_attribution_id','promotion_attribution_id','copy_provenance_id','field_key','affected_contributor_id','requested_by','resolved_by','reason','evidence','trigger_event_id','change_actor_id','evidence_attribution_id','evidence_version_id','outcome','previous_resolution_id','record_seal','resolved_at','created_by','created_at']) c
    where not exists (select 1 from information_schema.columns where table_schema='public' and table_name='attribution_discard_resolutions' and column_name = c);
  insert into pre values ('PRE-05','columnas de attribution_discard_resolutions (especificación línea 1118+)', case when falt is null then 'OK' else 'BLOCKED' end, coalesce('faltan: '||falt,'todas presentes'));
  select pg_catalog.count(*) filter (where pg_catalog.pg_get_constraintdef(oid) ~ 'resolved_by\s*<>\s*affected_contributor_id'), pg_catalog.count(*) filter (where pg_catalog.pg_get_constraintdef(oid) ~ 'resolved_by\s*<>\s*requested_by') into v_n, falt
    from pg_constraint where conrelid = pg_catalog.to_regclass('public.attribution_discard_resolutions') and contype = 'c';
  insert into pre values ('PRE-06','CHECK resolved_by<>affected_contributor_id y resolved_by<>requested_by (R3/R4 reforzadas por tabla)', case when v_n >= 1 and falt::int >= 1 then 'OK' else 'BLOCKED' end, 'afectado='||v_n||' solicitante='||falt);
  select pg_catalog.count(*) into v_n from pg_trigger where tgrelid = pg_catalog.to_regclass('public.attribution_discard_resolutions') and not tgisinternal and (tgtype & 2) = 2 and (tgtype & 4) = 4;
  insert into pre values ('PRE-07','trigger BEFORE INSERT en attribution_discard_resolutions (sello y created_by)', case when v_n >= 1 then 'OK' else 'BLOCKED' end, 'triggers='||v_n);
  insert into pre values ('PRE-08','el usuario actual puede asumir exec_role y exec_role tiene EXECUTE sobre la función', case when fn is not null and pg_catalog.pg_has_role(current_user, pg_catalog.current_setting('cci.exec_role'), 'MEMBER') and pg_catalog.has_function_privilege(pg_catalog.current_setting('cci.exec_role'), fn, 'EXECUTE') then 'OK' else 'BLOCKED' end,
    'exec_role='||pg_catalog.current_setting('cci.exec_role'));
exception when others then
  insert into pre values ('PRE-ERR','error al evaluar precondiciones','BLOCKED', sqlstate||':'||pg_catalog.left(sqlerrm,120));
end $$;
-- Datos de prueba (sólo si las tablas existen)
do $$ declare ok_att boolean := false; v_n int; v_aff uuid; v_mem_ok boolean; v_mem_no boolean; v_acc int;
begin
  if pg_catalog.to_regclass('public.brief_field_attributions') is null or pg_catalog.to_regclass('public.memberships') is null or pg_catalog.to_regclass('public.attribution_discard_resolutions') is null then
    insert into pre values ('PRE-09','datos de prueba verificables','BLOCKED','tablas ausentes: no se pueden verificar los datos de prueba'); return; end if;
  execute 'select pg_catalog.count(*), pg_catalog.min(contributor_id::text)::uuid from public.brief_field_attributions where organization_id = $1 and id = $2' into v_n, v_aff using pg_catalog.current_setting('cci.org')::uuid, pg_catalog.current_setting('cci.attr')::uuid;
  insert into pre values ('PRE-09a','la atribución attr existe en la organización (fuente brief; otras fuentes: ajustar)', case when v_n = 1 then 'OK' else 'BLOCKED' end, 'filas='||v_n);
  insert into pre values ('PRE-09b','affected coincide con el contribuyente de attr', case when v_aff = pg_catalog.current_setting('cci.affected')::uuid then 'OK' else 'BLOCKED' end, 'contribuyente='||coalesce(v_aff::text,'NULL'));
  execute 'select exists(select 1 from public.memberships where organization_id=$1 and user_id=$2), exists(select 1 from public.memberships where organization_id=$1 and user_id=$3)' into v_mem_ok, v_mem_no using pg_catalog.current_setting('cci.org')::uuid, pg_catalog.current_setting('cci.r_ok')::uuid, pg_catalog.current_setting('cci.r_nomember')::uuid;
  insert into pre values ('PRE-09c','r_ok es miembro y r_nomember NO es miembro de la organización', case when v_mem_ok and not v_mem_no then 'OK' else 'BLOCKED' end, 'r_ok_miembro='||v_mem_ok||' r_nomember_miembro='||v_mem_no);
  insert into pre values ('PRE-09d','r_ok distinto de affected, requester y change_actor', case when pg_catalog.current_setting('cci.r_ok') not in (pg_catalog.current_setting('cci.affected'), pg_catalog.current_setting('cci.requester'), pg_catalog.current_setting('cci.change_actor')) then 'OK' else 'BLOCKED' end, '');
  select pg_catalog.count(*) into v_acc from public.attribution_discard_resolutions where organization_id = pg_catalog.current_setting('cci.org')::uuid and outcome = 'aceptada' and (brief_attribution_id = pg_catalog.current_setting('cci.attr')::uuid or promotion_attribution_id = pg_catalog.current_setting('cci.attr')::uuid or copy_provenance_id = pg_catalog.current_setting('cci.attr')::uuid);
  insert into pre values ('PRE-09e','no existe ya una resolución aceptada para attr (evita falsos rechazos por índice único)', case when v_acc = 0 then 'OK' else 'BLOCKED' end, 'aceptadas='||v_acc);
  insert into pre values ('PRE-09f','requester/change_actor/r_noreview/r_direct/r_inherited/r_othersrc/r_benef: coherencia con R2,R4–R9 NO verificable genéricamente (la especificación no lista las entradas de solicitud/evento)','INFO','declarado por el propietario');
exception when others then
  insert into pre values ('PRE-09-ERR','error al evaluar datos de prueba','BLOCKED', sqlstate||':'||pg_catalog.left(sqlerrm,120));
end $$;
insert into pre values ('PRE-10','contrato de error declarado (code_*): sin contrato el rechazo es PARTIAL, nunca PASS', 'INFO', 'declarados: ' || (select pg_catalog.count(*) from (values (:'code_r1'),(:'code_r2'),(:'code_r3'),(:'code_r4'),(:'code_r5'),(:'code_r6'),(:'code_r7'),(:'code_r8'),(:'code_r9'),(:'code_rev')) v(c) where c <> '') || ' de 10');
select exists(select 1 from pre where estado = 'BLOCKED') as pre_bloqueado \gset
select * from pre order by id;
create temp table r_res(id text, regla text, tipo text, esperado text, clase text, sqlstate text, msg text, post text, veredicto text, nota text);
\if :pre_bloqueado
  -- ====== BATERÍA BLOQUEADA: nada se ejecuta; ningún caso puede ser PASS ======
  insert into r_res(id, regla, tipo, esperado, veredicto, nota) values
    ('R-POS','control positivo: todas las reglas se cumplen','POS','éxito','BLOCKED','precondición no cumplida'),
    ('R1-neg','R1 miembro activo','NEG',:'code_r1','BLOCKED','precondición no cumplida'), ('R2-neg','R2 piece.review','NEG',:'code_r2','BLOCKED','precondición no cumplida'),
    ('R3-neg','R3 no afectado','NEG',:'code_r3','BLOCKED','precondición no cumplida'), ('R4-neg','R4 no solicitante','NEG',:'code_r4','BLOCKED','precondición no cumplida'),
    ('R5-neg','R5 no actor del cambio','NEG',:'code_r5','BLOCKED','precondición no cumplida'), ('R6-neg','R6 no directo en cadena','NEG',:'code_r6','BLOCKED','precondición no cumplida'),
    ('R7-neg','R7 no heredado activo','NEG',:'code_r7','BLOCKED','precondición no cumplida'), ('R8-neg','R8 no excluido por otra fuente','NEG',:'code_r8','BLOCKED','precondición no cumplida'),
    ('R9-neg','R9 no beneficiario','NEG',:'code_r9','BLOCKED','precondición no cumplida'), ('R-ev1','evidencia vacía (fail-closed)','NEG',:'code_rev','BLOCKED','precondición no cumplida');
  select * from r_res order by id;
  select 'RESULTADO GLOBAL: NO VERIFICABLE EN ENTORNO FÍSICO (batería BLOQUEADA por precondiciones; ningún caso evaluado)' as resultado;
\else
  begin;
  set local lock_timeout = '5s'; set local statement_timeout = '30s';
  -- Control positivo PRIMERO: demuestra que la función existe, se ejecuta y registra la resolución cuando se cumplen R1–R9. Se revierte.
  insert into r_res(id, regla, tipo, esperado, clase, sqlstate, msg, post, veredicto)
  select 'R-POS','control positivo: todas las reglas se cumplen','POS','éxito', c.o_clase, c.o_sqlstate, c.o_msg, c.o_post, pg_temp.veredicto('POS', c.o_clase, c.o_sqlstate, c.o_msg, '', true)
  from pg_temp.ejecuta(pg_catalog.format(pg_catalog.current_setting('cci.fn_call'), pg_catalog.current_setting('cci.attr'), pg_catalog.current_setting('cci.reason'), pg_catalog.current_setting('cci.evidence')), pg_catalog.current_setting('cci.exec_role'), :'r_ok'::uuid,
       pg_catalog.format('select (pg_catalog.count(*) = 1)::text from public.attribution_discard_resolutions where organization_id = %L and resolved_by = %L and (brief_attribution_id = %L or promotion_attribution_id = %L or copy_provenance_id = %L)', :'org', :'r_ok', :'attr', :'attr', :'attr'), true) c;
  update r_res set veredicto = 'FAIL', nota = 'la función retornó sin error pero no registró exactamente una resolución del resolutor' where id = 'R-POS' and clase = 'OK' and post is distinct from 'true';
  -- Casos negativos: se ejecutan siempre DESPUÉS del control positivo y cada uno se revierte.
  insert into r_res(id, regla, tipo, esperado, clase, sqlstate, msg, veredicto)
  select v.id, v.regla, 'NEG', v.esperado, c.o_clase, c.o_sqlstate, c.o_msg, pg_temp.veredicto('NEG', c.o_clase, c.o_sqlstate, c.o_msg, v.esperado, true)
  from (values
    ('R1-neg','R1 miembro activo', :'code_r1', :'r_nomember'::uuid, :'evidence'), ('R2-neg','R2 piece.review', :'code_r2', :'r_noreview'::uuid, :'evidence'),
    ('R3-neg','R3 no afectado', :'code_r3', :'affected'::uuid, :'evidence'), ('R4-neg','R4 no solicitante', :'code_r4', :'requester'::uuid, :'evidence'),
    ('R5-neg','R5 no actor del cambio', :'code_r5', :'change_actor'::uuid, :'evidence'), ('R6-neg','R6 no directo en cadena', :'code_r6', :'r_direct'::uuid, :'evidence'),
    ('R7-neg','R7 no heredado activo', :'code_r7', :'r_inherited'::uuid, :'evidence'), ('R8-neg','R8 no excluido por otra fuente', :'code_r8', :'r_othersrc'::uuid, :'evidence'),
    ('R9-neg','R9 no beneficiario', :'code_r9', :'r_benef'::uuid, :'evidence'), ('R-ev1','evidencia vacía (fail-closed)', :'code_rev', :'r_ok'::uuid, '')) v(id, regla, esperado, uid, ev)
  cross join lateral pg_temp.ejecuta(pg_catalog.format(pg_catalog.current_setting('cci.fn_call'), pg_catalog.current_setting('cci.attr'), pg_catalog.current_setting('cci.reason'), v.ev), pg_catalog.current_setting('cci.exec_role'), v.uid, null, true) c;
  -- Si el control positivo no es PASS, ningún rechazo puede atribuirse a una regla: BLOCKED.
  update r_res set veredicto = 'BLOCKED', nota = 'control positivo no PASS: el rechazo no es atribuible a la regla' where tipo = 'NEG' and not exists (select 1 from r_res p where p.id = 'R-POS' and p.veredicto = 'PASS');
  update r_res set nota = 'rechazo observado; contrato de error NO definido por la especificación (BRECHA-R1R9-01): no se puede confirmar que la causa sea la regla' where tipo = 'NEG' and veredicto = 'PARTIAL';
  select id, regla, tipo, esperado, clase, sqlstate, pg_catalog.left(msg,60) as msg, veredicto, nota from r_res order by id;
  select veredicto, pg_catalog.count(*) from r_res group by 1 order by 1;
  rollback;
\endif
-- Sin residuos: el recuento posterior al ROLLBACK debe ser igual al anterior
select case when pg_catalog.to_regclass('public.attribution_discard_resolutions') is null then -1 else (pg_catalog.xpath('/row/c/text()', pg_catalog.query_to_xml('select pg_catalog.count(*) as c from public.attribution_discard_resolutions', false, true, '')))[1]::text::bigint end as post_count \gset
select case when :pre_count = -1 then 'NO APLICA (tabla inexistente: nada que comprobar)' when :pre_count = :post_count then 'PASS: sin residuos (filas antes = después = '||:post_count||')' else 'FAIL: RESIDUOS (antes '||:pre_count||', después '||:post_count||')' end as residuos;
