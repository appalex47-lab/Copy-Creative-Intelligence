-- SMOKE LOCAL (no es el esquema real): tabla mínima piece_reviewer_assignments con exclusión por rango, sólo para ejecutar las plantillas 05_A/05_B en PostgreSQL TEMPORAL LOCAL (base cci_conc_smoke).
\set ON_ERROR_STOP on
do $$ begin if not (current_database() = 'cci_conc_smoke' and inet_server_addr() is null and coalesce(current_setting('cci.entorno', true),'') = 'LOCAL-TEMPORAL') then raise exception 'NO EJECUTADO: smoke solo local'; end if; end $$;
create extension if not exists btree_gist;
create table public.piece_reviewer_assignments(id uuid primary key, organization_id uuid not null, piece_id uuid not null, reviewer_id uuid not null, assigned_by uuid not null, valid_during tstzrange not null, reason text not null,
  exclude using gist (organization_id with =, piece_id with =, valid_during with &&));
