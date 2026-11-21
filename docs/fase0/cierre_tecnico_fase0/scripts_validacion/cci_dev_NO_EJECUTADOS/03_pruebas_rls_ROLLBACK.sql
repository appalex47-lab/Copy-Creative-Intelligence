-- ====================================================================================================
-- NO EJECUTADOS — REQUIEREN AUTORIZACIÓN Y CCI-DEV
-- Preparado en el cierre técnico de Fase 0; NO se ejecutó contra ningún proyecto Supabase. Prohibido en CCI-PROD.
-- Sólo el propietario puede autorizar su ejecución, y únicamente en CCI-DEV. Escribe dentro de una transacción
-- que termina SIEMPRE en ROLLBACK (no deja datos). Aun así, es una operación de escritura: requiere autorización.
-- ====================================================================================================
-- Variables (psql -v): org_a, org_b (uuid de dos organizaciones de PRUEBA), uid_a (miembro de org_a), uid_b (miembro de org_b), uid_x (sin membresía).
-- Prerrequisito: dos organizaciones de prueba con membresías creadas por el propietario o por la semilla de CCI-DEV (no se crean aquí).
\set ON_ERROR_STOP on
do $$ begin if coalesce(current_setting('cci.validacion_autorizada', true),'') <> 'SI-CCI-DEV' then raise exception 'NO EJECUTADO: requiere autorizacion expresa del propietario y proyecto CCI-DEV (cci.validacion_autorizada)'; end if; end $$;
select set_config('cci.org_a', :'org_a', false), set_config('cci.uid_a', :'uid_a', false), set_config('cci.uid_x', :'uid_x', false) \gset
begin;
create temp table rls_resultados(id text, descripcion text, esperado text, obtenido text, resultado text) on commit drop;
-- Ayudante: ejecuta una sentencia como un rol/usuario y devuelve el sqlstate o 'OK:<filas>'
create or replace function pg_temp.como(p_rol text, p_uid uuid, p_sql text) returns text language plpgsql as $f$
declare n bigint; begin
  execute format('set local role %I', p_rol);
  perform set_config('request.jwt.claims', json_build_object('sub', p_uid, 'role', p_rol)::text, true);
  begin execute p_sql; get diagnostics n = row_count; reset role; return 'OK:'||n;
  exception when others then reset role; return sqlstate; end; end $f$;
-- RLS-01 fuga lectura: como uid_a, ninguna tabla con organization_id devuelve filas de otra organización (dinámico sobre TODAS las tablas)
do $$ declare r record; n bigint; fuga text := ''; begin
  for r in select table_name from information_schema.columns where table_schema='public' and column_name='organization_id' loop
    begin
      execute format('set local role authenticated'); perform set_config('request.jwt.claims', json_build_object('sub', current_setting('cci.uid_a')::uuid, 'role','authenticated')::text, true);
      execute format('select count(*) from public.%I where organization_id <> %L', r.table_name, current_setting('cci.org_a')) into n; reset role;
      if n > 0 then fuga := fuga || r.table_name || '(' || n || ') '; end if;
    exception when others then reset role; if sqlstate <> '42501' then fuga := fuga || r.table_name || '(ERROR ' || sqlstate || ') '; end if; end;  -- 42501 = acceso denegado = correcto
  end loop;
  insert into rls_resultados values ('RLS-01','lectura cruzada entre organizaciones (todas las tablas)','sin fuga', coalesce(nullif(fuga,''),'sin fuga'), case when fuga='' then 'PASS' else 'FAIL' end); end $$;
-- RLS-02 usuario sin membresía no ve nada
do $$ declare r record; n bigint; v text := ''; begin
  for r in select table_name from information_schema.columns where table_schema='public' and column_name='organization_id' loop
    begin
      execute 'set local role authenticated'; perform set_config('request.jwt.claims', json_build_object('sub', current_setting('cci.uid_x')::uuid, 'role','authenticated')::text, true);
      execute format('select count(*) from public.%I', r.table_name) into n; reset role; if n>0 then v := v || r.table_name || ' '; end if;
    exception when others then reset role; if sqlstate <> '42501' then v := v || r.table_name || '(ERROR ' || sqlstate || ') '; end if; end;  -- 42501 = acceso denegado = correcto
  end loop;
  insert into rls_resultados values ('RLS-02','usuario sin membresía no lee ninguna fila','0 filas', coalesce(nullif(v,''),'0 filas'), case when v='' then 'PASS' else 'FAIL' end); end $$;
-- RLS-03 anon no lee ninguna tabla de negocio
do $$ declare r record; n bigint; v text := ''; begin
  for r in select table_name from information_schema.columns where table_schema='public' and column_name='organization_id' loop
    begin
      execute 'set local role anon'; execute format('select count(*) from public.%I', r.table_name) into n; reset role; if n>0 then v := v || r.table_name || ' '; end if;
    exception when others then reset role; if sqlstate <> '42501' then v := v || r.table_name || '(ERROR ' || sqlstate || ') '; end if; end;  -- 42501 = acceso denegado = correcto
  end loop;
  insert into rls_resultados values ('RLS-03','anon no lee tablas de negocio','0 filas', coalesce(nullif(v,''),'0 filas'), case when v='' then 'PASS' else 'FAIL' end); end $$;
-- RLS-04 escritura cruzada: INSERT/UPDATE/DELETE de uid_a sobre filas de org_b no afectan filas (debe fallar o afectar 0). PLANTILLA: ajustar tabla y columnas tras INV-02.
-- Ejemplo con una tabla con (id, organization_id): select pg_temp.como('authenticated', :'uid_a'::uuid, format('update public.<TABLA> set organization_id = organization_id where organization_id = %L', :'org_b'));  -- esperado 'OK:0'
-- RLS-05 escalada de privilegios: authenticated no puede modificar role_permissions ni membership_permission_grants ni asignarse org.manage
insert into rls_resultados select 'RLS-05a','authenticated no puede INSERT en role_permissions','42501', pg_temp.como('authenticated', :'uid_a'::uuid, 'insert into public.role_permissions default values'), '' ;
insert into rls_resultados select 'RLS-05b','authenticated no puede UPDATE en approvals','42501', pg_temp.como('authenticated', :'uid_a'::uuid, 'update public.approvals set approver = approver'), '';
insert into rls_resultados select 'RLS-05c','authenticated no puede DELETE en activity_logs','42501', pg_temp.como('authenticated', :'uid_a'::uuid, 'delete from public.activity_logs'), '';
insert into rls_resultados select 'RLS-05d','authenticated no puede TRUNCATE tablas inmutables','42501', pg_temp.como('authenticated', :'uid_a'::uuid, 'truncate public.attribution_discard_resolutions'), '';
update rls_resultados set resultado = case when obtenido = esperado then 'PASS' else 'FAIL' end where resultado = '';
select * from rls_resultados order by id;
rollback;
