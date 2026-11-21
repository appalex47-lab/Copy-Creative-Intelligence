-- ====================================================================================================
-- NO EJECUTADO CONTRA CCI-DEV NI CCI-PROD — REQUIERE AUTORIZACIÓN Y CCI-DEV
-- Preparado en el cierre técnico de Fase 0. Prohibido en CCI-PROD. Sólo el propietario puede autorizar su ejecución, y únicamente en CCI-DEV:
--   PGOPTIONS="-c cci.validacion_autorizada=SI-CCI-DEV -c cci.entorno=CCI-DEV" psql ... -f <este archivo>
-- Estados de resultado: PASS, FAIL, BLOCKED, PARTIAL, NOT VERIFIED. Un error técnico (permisos, estructura, sintaxis, función inexistente) NUNCA es PASS.
-- Tipo: SOLO LECTURA. Inventario de políticas RLS, grants y privilegios efectivos (PRIV-01..PRIV-07). Es un INVENTARIO: no emite PASS/FAIL; sus salidas se evalúan contra PRUEBAS_RLS_PRIVILEGIOS_CONCURRENCIA.md.
-- ====================================================================================================
\set ON_ERROR_STOP on
-- Guarda (idéntica en los 6 scripts). Nota: ninguna guarda puede probar que la base sea CCI-DEV y no CCI-PROD; la identificación del proyecto la hace el propietario.
do $$ declare a text := coalesce(current_setting('cci.validacion_autorizada', true),''); e text := coalesce(current_setting('cci.entorno', true),'');
begin
  if a = 'SI-CCI-DEV' and e = 'CCI-DEV' then null;
  elsif a = 'SI-LOCAL-TEMPORAL' and e = 'LOCAL-TEMPORAL' and current_database() ~ '^cci_' and inet_server_addr() is null then null;
  else raise exception 'NO EJECUTADO: requiere autorizacion expresa del propietario y proyecto CCI-DEV (cci.validacion_autorizada + cci.entorno), o ejecucion local temporal por socket Unix'; end if; end $$;
begin read only;
-- PRIV-01 políticas RLS
select schemaname, tablename, policyname, permissive, roles, cmd, qual, with_check from pg_policies where schemaname='public' order by 2,3;
-- PRIV-02 tablas sin RLS activa
select c.relname from pg_class c join pg_namespace n on n.oid=c.relnamespace where n.nspname='public' and c.relkind='r' and not c.relrowsecurity order by 1;
-- PRIV-03 grants por rol y tabla
select grantee, table_name, privilege_type, is_grantable from information_schema.role_table_grants where table_schema='public' and grantee in ('anon','authenticated','service_role','PUBLIC') order by 2,1,3;
-- PRIV-04 privilegios efectivos de cada rol de aplicación sobre cada tabla (matriz S/I/U/D/T)
select c.relname as tabla, r.rolname, has_table_privilege(r.oid,c.oid,'SELECT') s, has_table_privilege(r.oid,c.oid,'INSERT') i, has_table_privilege(r.oid,c.oid,'UPDATE') u, has_table_privilege(r.oid,c.oid,'DELETE') d, has_table_privilege(r.oid,c.oid,'TRUNCATE') t from pg_class c join pg_namespace n on n.oid=c.relnamespace cross join pg_roles r where n.nspname='public' and c.relkind='r' and r.rolname in ('anon','authenticated','service_role') order by 1,2;
-- PRIV-05 privilegios EXECUTE sobre funciones públicas
select p.proname, r.rolname, has_function_privilege(r.oid,p.oid,'EXECUTE') as puede_ejecutar from pg_proc p cross join pg_roles r where p.pronamespace='public'::regnamespace and r.rolname in ('anon','authenticated','service_role') order by 1,2;
-- PRIV-06 pertenencia a roles y atributos peligrosos
select rolname, rolsuper, rolbypassrls, rolcanlogin, rolinherit from pg_roles where rolname in ('anon','authenticated','service_role','authenticator','postgres','cci_records_owner') order by 1;
-- PRIV-07 privilegios por defecto (ALTER DEFAULT PRIVILEGES)
select pg_get_userbyid(defaclrole) as rol, defaclnamespace::regnamespace, defaclobjtype, defaclacl from pg_default_acl order by 1;
rollback;
