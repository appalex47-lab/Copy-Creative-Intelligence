-- ====================================================================================================
-- NO EJECUTADO CONTRA CCI-DEV NI CCI-PROD — REQUIERE AUTORIZACIÓN Y CCI-DEV
-- Versión 2 (corrección consolidada). Pruebas de RLS y de privilegios. Escritura: NINGUNA persistente; las sondas de escritura usan `where false` o
-- fallan por privilegio, y cada caso se revierte (excepción centinela). Cambios respecto de la v1: precondiciones, clasificación de errores
-- (un error técnico no es PASS), resultados por tabla, no-vacuidad (PASS sólo si había datos de otra organización que filtrar), sondas sin efecto
-- (la v1 podía ejecutar DELETE/TRUNCATE reales dentro de la transacción) y columna `approver` sustituida por una sonda independiente de columnas.
-- Variables (psql -v): org_a, org_b, uid_a (miembro de org_a), uid_b (miembro de org_b), uid_x (sin membresía). Datos de PRUEBA preexistentes (no se crean aquí).
-- ====================================================================================================
\set ON_ERROR_STOP on
-- Guarda de destino compartida (H-03): ver 00_guarda_destino.sql
\ir 00_guarda_destino.sql
do $v$ begin if pg_catalog.to_regclass('pg_temp.cci_guarda_ok') is null then raise exception 'NO EJECUTADO [G-GUARDA-NO-EJECUTADA] la guarda 00_guarda_destino.sql no se ejecutó completa'; end if; end $v$;
\ir 04_lib_clasificador.sql
select pg_catalog.set_config('cci.org_a', :'org_a', false), pg_catalog.set_config('cci.org_b', :'org_b', false), pg_catalog.set_config('cci.uid_a', :'uid_a', false), pg_catalog.set_config('cci.uid_x', :'uid_x', false) \gset
create temp table pre(id text, descripcion text, estado text, detalle text);
create temp table tablas_org as select table_name::text as t from information_schema.columns where table_schema = 'public' and column_name = 'organization_id' and table_name in (select table_name from information_schema.tables where table_schema='public' and table_type='BASE TABLE');
insert into pre values ('PRE-01','roles anon y authenticated existen', case when (select pg_catalog.count(*) from pg_roles where rolname in ('anon','authenticated')) = 2 then 'OK' else 'BLOCKED' end, '');
insert into pre values ('PRE-02','el usuario actual puede asumir authenticated y anon', case when pg_catalog.pg_has_role(current_user,'authenticated','MEMBER') and pg_catalog.pg_has_role(current_user,'anon','MEMBER') then 'OK' else 'BLOCKED' end, 'current_user='||current_user);
insert into pre select 'PRE-03','hay tablas con organization_id (conjunto evaluado)', case when pg_catalog.count(*) > 0 then 'OK' else 'BLOCKED' end, 'tablas='||pg_catalog.count(*) from tablas_org;
do $$ declare n_b bigint := 0; n_a bigint := 0; r record; c bigint;
begin
  for r in select t from tablas_org loop
    execute pg_catalog.format('select count(*) from public.%I where organization_id = %L', r.t, pg_catalog.current_setting('cci.org_b')) into c; n_b := n_b + c;
    execute pg_catalog.format('select count(*) from public.%I where organization_id = %L', r.t, pg_catalog.current_setting('cci.org_a')) into c; n_a := n_a + c;
  end loop;
  insert into pre values ('PRE-04','existen filas de org_b y de org_a (sin ellas RLS-01/02/04 serían vacuas)', case when n_a > 0 and n_b > 0 then 'OK' else 'PARTIAL' end, 'filas_org_a='||n_a||' filas_org_b='||n_b);
exception when others then insert into pre values ('PRE-04','conteo de filas de prueba','BLOCKED', sqlstate||':'||pg_catalog.left(sqlerrm,100)); end $$;
select * from pre order by id;
select exists(select 1 from pre where estado = 'BLOCKED') as pre_bloqueado, exists(select 1 from pre where id = 'PRE-04' and estado = 'PARTIAL') as vacuo \gset
create temp table rls_t(id text, tabla text, esperado text, clase text, sqlstate text, msg text, veredicto text);
\if :pre_bloqueado
  \echo 'BATERÍA BLOQUEADA por precondiciones: NO VERIFICABLE (ningún caso evaluado)'
\else
begin;
set local lock_timeout = '5s'; set local statement_timeout = '60s';
-- RLS-01 lectura cruzada (uid_a no ve filas de otra organización). 42501 = denegado por privilegio (también seguro). Otro error: BLOCKED/FAIL, nunca PASS.
insert into rls_t select 'RLS-01', t.t, 'sin fuga', c.o_clase, c.o_sqlstate, c.o_msg,
  case when c.o_clase in ('OK','PERMISOS') then 'PASS' when c.o_clase = 'DOMINIO_CANDIDATO' and c.o_msg like 'FUGA:%' then 'FAIL' when c.o_clase in ('ESTRUCTURA','SINTAXIS','FUNCION_INEXISTENTE') then 'BLOCKED' else 'FAIL' end
from tablas_org t cross join lateral pg_temp.ejecuta(pg_catalog.format($d$do $x$ declare n bigint; begin select pg_catalog.count(*) into n from public.%I where organization_id <> %L; if n > 0 then raise exception 'FUGA:%%', n using errcode='P0001'; end if; end $x$$d$, t.t, pg_catalog.current_setting('cci.org_a')), 'authenticated', pg_catalog.current_setting('cci.uid_a')::uuid, null, true) c;
-- RLS-02 usuario sin membresía no ve filas
insert into rls_t select 'RLS-02', t.t, '0 filas', c.o_clase, c.o_sqlstate, c.o_msg,
  case when c.o_clase in ('OK','PERMISOS') then 'PASS' when c.o_clase = 'DOMINIO_CANDIDATO' and c.o_msg like 'FUGA:%' then 'FAIL' when c.o_clase in ('ESTRUCTURA','SINTAXIS','FUNCION_INEXISTENTE') then 'BLOCKED' else 'FAIL' end
from tablas_org t cross join lateral pg_temp.ejecuta(pg_catalog.format($d$do $x$ declare n bigint; begin select pg_catalog.count(*) into n from public.%I; if n > 0 then raise exception 'FUGA:%%', n using errcode='P0001'; end if; end $x$$d$, t.t), 'authenticated', pg_catalog.current_setting('cci.uid_x')::uuid, null, true) c;
-- RLS-03 anon no lee tablas de negocio
insert into rls_t select 'RLS-03', t.t, '0 filas', c.o_clase, c.o_sqlstate, c.o_msg,
  case when c.o_clase in ('OK','PERMISOS') then 'PASS' when c.o_clase = 'DOMINIO_CANDIDATO' and c.o_msg like 'FUGA:%' then 'FAIL' when c.o_clase in ('ESTRUCTURA','SINTAXIS','FUNCION_INEXISTENTE') then 'BLOCKED' else 'FAIL' end
from tablas_org t cross join lateral pg_temp.ejecuta(pg_catalog.format($d$do $x$ declare n bigint; begin select pg_catalog.count(*) into n from public.%I; if n > 0 then raise exception 'FUGA:%%', n using errcode='P0001'; end if; end $x$$d$, t.t), 'anon', null, null, true) c;
-- RLS-04 escritura cruzada: uid_a intenta modificar filas de org_b (debe afectar 0 filas o ser denegado)
insert into rls_t select 'RLS-04', t.t, '0 filas afectadas o 42501', c.o_clase, c.o_sqlstate, c.o_msg,
  case when c.o_clase in ('OK','PERMISOS') then 'PASS' when c.o_clase = 'DOMINIO_CANDIDATO' and c.o_msg like 'FUGA_ESCRITURA:%' then 'FAIL' when c.o_clase in ('ESTRUCTURA','SINTAXIS','FUNCION_INEXISTENTE') then 'BLOCKED' else 'FAIL' end
from tablas_org t cross join lateral pg_temp.ejecuta(pg_catalog.format($d$do $x$ declare n bigint; begin update public.%I set organization_id = organization_id where organization_id = %L; get diagnostics n = row_count; if n > 0 then raise exception 'FUGA_ESCRITURA:%%', n using errcode='P0001'; end if; end $x$$d$, t.t, pg_catalog.current_setting('cci.org_b')), 'authenticated', pg_catalog.current_setting('cci.uid_a')::uuid, null, true) c;
-- RLS-05 escalada: authenticated no tiene escritura directa en tablas de control/evidencia (sondas sin efecto: where false / has_table_privilege). Se exige 42501.
insert into rls_t select 'RLS-05'||v.k, v.tabla, '42501', c.o_clase, c.o_sqlstate, c.o_msg,
  case when pg_catalog.to_regclass('public.'||v.tabla) is null then 'BLOCKED' else pg_temp.veredicto('DENEGADO', c.o_clase, c.o_sqlstate, c.o_msg, '', true) end
from (values ('a','role_permissions','insert into public.role_permissions select * from public.role_permissions where false'),
             ('b','approvals','update public.approvals set organization_id = organization_id where false'),
             ('c','activity_logs','delete from public.activity_logs where false'),
             ('d','attribution_discard_resolutions',$q$do $x$ begin if pg_catalog.has_table_privilege('authenticated','public.attribution_discard_resolutions','TRUNCATE') then raise exception 'TIENE_TRUNCATE' using errcode='P0001'; else raise exception 'sin privilegio TRUNCATE' using errcode='42501'; end if; end $x$$q$),
             ('e','membership_permission_grants','insert into public.membership_permission_grants select * from public.membership_permission_grants where false')) v(k, tabla, sqltxt)
cross join lateral pg_temp.ejecuta(v.sqltxt, 'authenticated', pg_catalog.current_setting('cci.uid_a')::uuid, null, true) c;
-- RLS-06 inserción cruzada: NO VERIFICADA genéricamente (requiere conocer columnas obligatorias de cada tabla tras INV-02)
insert into rls_t values ('RLS-06','(todas)','INSERT cruzado rechazado','', '', 'no implementado genéricamente: requiere datos por tabla', 'NOT VERIFIED');
\echo '=== DETALLE POR TABLA ==='
select id, tabla, clase, sqlstate, veredicto, pg_catalog.left(msg,50) as msg from rls_t where veredicto <> 'PASS' order by id, tabla;
\echo '=== RESUMEN POR PRUEBA ==='
select id, pg_catalog.count(*) as casos, pg_catalog.count(*) filter (where veredicto='PASS') as pass, pg_catalog.count(*) filter (where veredicto='FAIL') as fail, pg_catalog.count(*) filter (where veredicto='BLOCKED') as blocked, pg_catalog.count(*) filter (where veredicto='NOT VERIFIED') as nv,
  case when pg_catalog.count(*) filter (where veredicto='FAIL') > 0 then 'FAIL' when pg_catalog.count(*) filter (where veredicto='BLOCKED') > 0 then 'BLOCKED' when pg_catalog.bool_and(veredicto = 'NOT VERIFIED') then 'NOT VERIFIED'
       when id in ('RLS-01','RLS-02','RLS-04') and :'vacuo'::boolean then 'PARTIAL (vacua: faltan filas de prueba)' else 'PASS' end as resultado
from rls_t group by id order by id;
rollback;
\endif
