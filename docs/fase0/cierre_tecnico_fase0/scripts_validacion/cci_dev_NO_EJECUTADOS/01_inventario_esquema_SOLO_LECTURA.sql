-- ====================================================================================================
-- NO EJECUTADOS — REQUIEREN AUTORIZACIÓN Y CCI-DEV
-- Este archivo fue PREPARADO en el cierre técnico de Fase 0 y NO se ha ejecutado contra ningún proyecto Supabase.
-- Prohibido en CCI-PROD. Sólo el propietario puede autorizar su ejecución, y únicamente en CCI-DEV.
-- Guarda: falla si no se declara explícitamente la autorización (set cci.validacion_autorizada='SI-CCI-DEV').
-- ====================================================================================================
-- Tipo: SOLO LECTURA (catálogos del sistema). No crea, modifica ni borra nada.
\set ON_ERROR_STOP on
do $$ begin if coalesce(current_setting('cci.validacion_autorizada', true),'') <> 'SI-CCI-DEV' then raise exception 'NO EJECUTADO: requiere autorizacion expresa del propietario y proyecto CCI-DEV (cci.validacion_autorizada)'; end if; end $$;
begin read only;
-- INV-01 tablas del esquema public
select c.relname as tabla, c.relkind, c.relrowsecurity as rls_activa, c.relforcerowsecurity as rls_forzada from pg_class c join pg_namespace n on n.oid=c.relnamespace where n.nspname='public' and c.relkind in ('r','p') order by 1;
-- INV-02 columnas, tipos, nulabilidad y defaults
select table_name, ordinal_position, column_name, data_type, udt_name, is_nullable, column_default, character_maximum_length from information_schema.columns where table_schema='public' order by 1,2;
-- INV-03 restricciones PK/FK/UNIQUE/CHECK/EXCLUDE con definición
select conrelid::regclass as tabla, conname, contype, pg_get_constraintdef(oid) as definicion, convalidated, condeferrable, condeferred from pg_constraint where connamespace='public'::regnamespace order by 1,3,2;
-- INV-04 índices
select schemaname, tablename, indexname, indexdef from pg_indexes where schemaname='public' order by 2,3;
-- INV-05 triggers (no internos)
select event_object_table as tabla, trigger_name, action_timing, event_manipulation, action_statement from information_schema.triggers where trigger_schema='public' order by 1,2,4;
-- INV-06 funciones: propietario, seguridad (SECURITY DEFINER), search_path, volatilidad
select p.proname, pg_get_userbyid(p.proowner) as propietario, p.prosecdef as security_definer, p.proconfig as config, p.provolatile, pg_get_function_identity_arguments(p.oid) as args from pg_proc p where p.pronamespace='public'::regnamespace order by 1;
-- INV-07 dependencias entre tablas (FK) como grafo
select conrelid::regclass as hija, confrelid::regclass as padre, conname from pg_constraint where contype='f' and connamespace='public'::regnamespace order by 1,2;
-- INV-08 extensiones y versión
select extname, extversion from pg_extension order by 1; select version();
-- INV-09 verificación de recuentos esperados por diseño: 41 tablas (27 base + 14 nuevas)
select count(*) as tablas_public from pg_class c join pg_namespace n on n.oid=c.relnamespace where n.nspname='public' and c.relkind='r';
-- INV-10 columnas *_id sin FK (patrón de los defectos corregidos en V20)
select c.table_name, c.column_name from information_schema.columns c where c.table_schema='public' and c.column_name like '%\_id' escape '\' and not exists (select 1 from pg_constraint k join pg_attribute a on a.attrelid=k.conrelid and a.attnum = any(k.conkey) where k.contype='f' and k.conrelid=(quote_ident(c.table_schema)||'.'||quote_ident(c.table_name))::regclass and a.attname=c.column_name) order by 1,2;
rollback;
