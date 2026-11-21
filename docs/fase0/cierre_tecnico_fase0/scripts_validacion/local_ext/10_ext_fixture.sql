-- EXTENSIÓN LOCAL DEL CIERRE TÉCNICO — PROTOTIPOS DE DISEÑO EN PostgreSQL TEMPORAL. NO ES MIGRACIÓN NI ESQUEMA FÍSICO.
-- Se carga SOBRE 01_fixture.sql (V20, sin modificarlo). Las tablas *_x son prototipos para demostrar la viabilidad
-- de la regla de diseño; no equivalen a las tablas reales de la especificación ni a Supabase.
create table impact_evaluations_x(
  id uuid not null, organization_id uuid not null,
  adaptation_piece_id uuid not null, adaptation_copy_version_id uuid not null, adaptation_asset_key text not null,
  master_piece_id uuid not null, master_basis_copy_version_id uuid not null, master_basis_art text not null,
  master_changed_copy_version_id uuid not null, master_changed_art text not null,
  supersedes_evaluation_id uuid null,
  primary key(id), unique(organization_id,id),
  unique(organization_id,adaptation_piece_id,adaptation_copy_version_id,adaptation_asset_key,master_piece_id,master_basis_copy_version_id,master_basis_art,master_changed_copy_version_id,master_changed_art,id),
  foreign key (organization_id,adaptation_piece_id,adaptation_copy_version_id,adaptation_asset_key,master_piece_id,master_basis_copy_version_id,master_basis_art,master_changed_copy_version_id,master_changed_art,supersedes_evaluation_id)
    references impact_evaluations_x(organization_id,adaptation_piece_id,adaptation_copy_version_id,adaptation_asset_key,master_piece_id,master_basis_copy_version_id,master_basis_art,master_changed_copy_version_id,master_changed_art,id),
  check (supersedes_evaluation_id is distinct from id));
-- Citas de aprobación (prototipo C2/C3, IG5-27): FK compuesta a la aprobación de la pieza y versión exactas.
alter table approvals add column decision text not null default 'aprobada';
alter table approvals add unique(organization_id,piece_id,copy_version_id,id);
create table approval_citations_x(
  id uuid primary key, organization_id uuid not null, piece_id uuid not null, copy_version_id uuid not null, approval_id uuid not null,
  foreign key (organization_id,piece_id,copy_version_id,approval_id) references approvals(organization_id,piece_id,copy_version_id,id));
-- Autores por versión (prototipo de contribuyentes directos) y regla aprobador-contribuyente con herencia (IG1-12, T-80, T-10).
create table version_authors_x(organization_id uuid not null, version_id uuid not null, user_id uuid not null, primary key(organization_id,version_id,user_id),
  foreign key (organization_id,version_id) references copy_versions(organization_id,id));
create function contributors_x(p_org uuid, p_version uuid) returns setof uuid language sql stable as $$
  with recursive c(v) as (select p_version union select cv.source_version_id from copy_versions cv join c on cv.id=c.v and cv.organization_id=p_org where cv.source_version_id is not null)
  select distinct a.user_id from version_authors_x a join c on a.version_id=c.v and a.organization_id=p_org $$;
create function trg_approval_indep_x() returns trigger language plpgsql as $$ begin
  if new.approver in (select contributors_x(new.organization_id,new.copy_version_id)) then raise exception 'APROBADOR_CONTRIBUYENTE' using errcode='P0001'; end if; return new; end $$;
create table approvals_indep_x(like approvals including all);
create trigger t_appr_indep before insert on approvals_indep_x for each row execute function trg_approval_indep_x();
alter table approvals_indep_x add foreign key (organization_id,piece_id,copy_version_id) references copy_versions(organization_id,piece_id,id);
-- IG1-09 (prototipo): arte por versión de copy y referencia compuesta desde la versión de la adaptación
create table assets_x(id uuid not null, organization_id uuid not null, piece_id uuid not null, copy_version_id uuid not null, primary key(id), unique(organization_id,copy_version_id,id),
  foreign key (organization_id,piece_id,copy_version_id) references copy_versions(organization_id,piece_id,id));
create table adaptation_art_refs_x(id uuid primary key, organization_id uuid not null, adaptation_version_id uuid not null, source_copy_version_id uuid not null, source_asset_id uuid not null,
  foreign key (organization_id,adaptation_version_id) references copy_versions(organization_id,id),
  foreign key (organization_id,source_copy_version_id,source_asset_id) references assets_x(organization_id,copy_version_id,id));
