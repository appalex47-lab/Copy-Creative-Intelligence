-- ====================================================================================================
-- SHIM LOCAL DE RLS (NO ES SUPABASE, NO ES EL ESQUEMA REAL). Sólo para probar el ARNÉS de 03_pruebas_rls_ROLLBACK.sql en PostgreSQL TEMPORAL LOCAL.
-- Reconstruye el shim usado en el cierre técnico (antes no estaba versionado: brecha corregida). Base cci_shim, socket Unix, cci.entorno=LOCAL-TEMPORAL.
-- Variante (psql -v variante=defectuosa|corregida): 'defectuosa' deja la tabla fuga_t SIN RLS y con SELECT para anon/authenticated (el script 03 debe dar FAIL);
-- 'corregida' activa RLS en fuga_t y retira el acceso anónimo (el script 03 debe dar PASS). Un PASS aquí NO valida ninguna política real de CCI.
-- ====================================================================================================
\set ON_ERROR_STOP on
do $$ begin if not (current_database() = 'cci_shim' and inet_server_addr() is null and coalesce(current_setting('cci.entorno', true),'') = 'LOCAL-TEMPORAL') then raise exception 'NO EJECUTADO: shim solo local (cci_shim, socket Unix, cci.entorno=LOCAL-TEMPORAL)'; end if; end $$;
drop schema public cascade; create schema public;
do $$ declare r text; begin foreach r in array array['anon','authenticated','service_role'] loop if not exists (select 1 from pg_roles where rolname = r) then execute format('create role %I nologin', r); end if; end loop; end $$;
grant usage on schema public to anon, authenticated;
create table memberships(organization_id uuid, user_id uuid);
create table organizations(id uuid);
create table role_permissions(id int);
create table membership_permission_grants(id int, organization_id uuid);
create table approvals(id int primary key, organization_id uuid, approver uuid);
create table activity_logs(id int, organization_id uuid);
create table attribution_discard_resolutions(id int, organization_id uuid);
create table fuga_t(id int, organization_id uuid);
create function is_member(o uuid) returns boolean language sql stable security definer as $$ select exists(select 1 from memberships m where m.organization_id = o and m.user_id = (current_setting('request.jwt.claims', true)::json->>'sub')::uuid) $$;
grant execute on function is_member(uuid) to anon, authenticated;
insert into memberships values ('a0000000-0000-0000-0000-000000000001','a0000000-0000-0000-0000-0000000000a1'), ('a0000000-0000-0000-0000-000000000002','a0000000-0000-0000-0000-0000000000b1');
insert into approvals values (1,'a0000000-0000-0000-0000-000000000001',null), (2,'a0000000-0000-0000-0000-000000000002',null);
insert into activity_logs values (1,'a0000000-0000-0000-0000-000000000001'), (2,'a0000000-0000-0000-0000-000000000002');
insert into attribution_discard_resolutions values (1,'a0000000-0000-0000-0000-000000000001'), (2,'a0000000-0000-0000-0000-000000000002');
insert into membership_permission_grants values (1,'a0000000-0000-0000-0000-000000000001');
insert into fuga_t values (1,'a0000000-0000-0000-0000-000000000001'), (2,'a0000000-0000-0000-0000-000000000002');
alter table memberships enable row level security; alter table approvals enable row level security; alter table activity_logs enable row level security;
alter table attribution_discard_resolutions enable row level security; alter table membership_permission_grants enable row level security;
create policy p_m on memberships using (is_member(organization_id)); create policy p_a on approvals using (is_member(organization_id));
create policy p_l on activity_logs using (false); create policy p_r on attribution_discard_resolutions using (false); create policy p_g on membership_permission_grants using (false);
grant select on memberships, approvals, activity_logs, attribution_discard_resolutions to authenticated;
\if :{?variante}
\else
  \set variante corregida
\endif
select :'variante' = 'defectuosa' as def \gset
\if :def
  grant select on fuga_t to authenticated, anon;       -- DEFECTO deliberado: sin RLS y con acceso anónimo
\else
  alter table fuga_t enable row level security; create policy p_f on fuga_t using (is_member(organization_id)); grant select on fuga_t to authenticated;
\endif
