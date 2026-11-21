-- FIXTURE DE PRUEBA V20 — NO ES UNA MIGRACIÓN NI EL ESQUEMA FÍSICO APROBADO.
-- Subconjunto mínimo, derivado de la especificación, para ejecutar PE-01..PE-05 y las pruebas de
-- channel_formats y attribution_discard_resolutions en un PostgreSQL TEMPORAL y AISLADO. Sin RLS ni roles.
-- Limitaciones declaradas: sin trigger de elegibilidad completa R1–R9 (IG5-95), sin las otras 12 tablas nuevas.
create table organizations(id uuid primary key);
create table memberships(organization_id uuid not null references organizations(id), user_id uuid not null, activo boolean not null default true, primary key(organization_id,user_id));
create table channel_rules(organization_id uuid not null references organizations(id), channel text not null, active boolean not null default true, unique(organization_id,channel));
create table channel_formats(
  organization_id uuid not null, channel text not null, format text not null, active boolean not null default true,
  retired_at timestamptz null, created_at timestamptz not null default now(), created_by uuid not null,
  unique(organization_id,channel,format),
  foreign key (organization_id,channel) references channel_rules(organization_id,channel) on delete restrict,
  foreign key (organization_id,created_by) references memberships(organization_id,user_id),
  check (channel=lower(btrim(channel)) and char_length(channel) between 1 and 40),
  check (format=lower(btrim(format)) and char_length(format) between 1 and 40));
create table creative_pieces(
  id uuid primary key, organization_id uuid not null references organizations(id), master_piece_id uuid null,
  channel text not null, format text not null, state text not null default 'Borrador',
  unique(organization_id,id),
  foreign key (organization_id,master_piece_id) references creative_pieces(organization_id,id),
  foreign key (organization_id,channel,format) references channel_formats(organization_id,channel,format) on delete restrict,
  check (master_piece_id is distinct from id));
create function trg_master_inmutable() returns trigger language plpgsql as $$ begin
  if old.master_piece_id is not null and new.master_piece_id is distinct from old.master_piece_id then raise exception 'MASTER_INMUTABLE' using errcode='P0001'; end if; return new; end $$;
create trigger t_master before update on creative_pieces for each row execute function trg_master_inmutable();
create function trg_formato_inmutable() returns trigger language plpgsql as $$ begin
  if tg_op='DELETE' then raise exception 'SIN_DELETE' using errcode='P0001'; end if;
  if new.channel<>old.channel or new.format<>old.format then raise exception 'CANAL_FORMATO_INMUTABLE' using errcode='P0001'; end if;
  if old.active and not new.active and exists(select 1 from creative_pieces p where p.organization_id=old.organization_id and p.channel=old.channel and p.format=old.format and p.state not in ('Publicado','Archivado')) then raise exception 'RETIRO_CON_PIEZAS_ACTIVAS' using errcode='P0001'; end if;
  return new; end $$;
create trigger t_cf_upd before update or delete on channel_formats for each row execute function trg_formato_inmutable();
create table copy_versions(
  id uuid primary key, organization_id uuid not null, piece_id uuid not null, version_no int not null,
  source_piece_id uuid null, source_version_id uuid null,
  unique(organization_id,id), unique(organization_id,piece_id,id), unique(organization_id,piece_id,version_no),
  foreign key (organization_id,piece_id) references creative_pieces(organization_id,id),
  foreign key (organization_id,source_piece_id,source_version_id) references copy_versions(organization_id,piece_id,id));
create function trg_inmutable() returns trigger language plpgsql as $$ begin raise exception 'INMUTABLE' using errcode='P0001'; end $$;
create trigger t_cv_imm before update or delete on copy_versions for each row execute function trg_inmutable();
create table approvals(
  id uuid primary key, organization_id uuid not null, piece_id uuid not null, copy_version_id uuid not null, approver uuid not null,
  foreign key (organization_id,piece_id,copy_version_id) references copy_versions(organization_id,piece_id,id));
create table impact_evaluations(
  id uuid primary key, organization_id uuid not null,
  adaptation_piece_id uuid not null, adaptation_copy_version_id uuid not null, adaptation_asset_key text not null,
  master_piece_id uuid not null, master_basis_copy_version_id uuid not null, master_basis_art text not null,
  master_changed_copy_version_id uuid not null, master_changed_art text not null,
  unique(organization_id,adaptation_piece_id,adaptation_copy_version_id,adaptation_asset_key,master_piece_id,master_basis_copy_version_id,master_basis_art,master_changed_copy_version_id,master_changed_art),
  foreign key (organization_id,adaptation_piece_id,adaptation_copy_version_id) references copy_versions(organization_id,piece_id,id),
  foreign key (organization_id,master_piece_id,master_basis_copy_version_id) references copy_versions(organization_id,piece_id,id),
  foreign key (organization_id,master_piece_id,master_changed_copy_version_id) references copy_versions(organization_id,piece_id,id));
-- attribution_discard_resolutions (fuente 'brief' únicamente en este fixture)
create table brief_field_attributions(id uuid not null, organization_id uuid not null, field_key text not null, contributor_id uuid not null, version_id uuid not null, unique(organization_id,id,field_key,contributor_id), unique(organization_id,id));
create table contribution_events(id uuid not null, organization_id uuid not null, contributor_id uuid not null, unique(organization_id,id,contributor_id));
create table attribution_discard_resolutions(
  id uuid primary key, organization_id uuid not null, source_kind text not null, brief_attribution_id uuid, field_key text not null,
  affected_contributor_id uuid not null, requested_by uuid not null, resolved_by uuid not null, reason text not null, evidence text not null,
  trigger_event_id uuid not null, change_actor_id uuid not null, evidence_attribution_id uuid not null, evidence_version_id uuid not null,
  outcome text not null, previous_resolution_id uuid, record_seal text not null, resolved_at timestamptz not null default now(), created_by uuid not null,
  unique(organization_id,id),
  foreign key (organization_id,brief_attribution_id,field_key,affected_contributor_id) references brief_field_attributions(organization_id,id,field_key,contributor_id) on delete restrict,
  foreign key (organization_id,requested_by) references memberships(organization_id,user_id),
  foreign key (organization_id,resolved_by) references memberships(organization_id,user_id),
  foreign key (organization_id,created_by) references memberships(organization_id,user_id),
  foreign key (organization_id,trigger_event_id,change_actor_id) references contribution_events(organization_id,id,contributor_id),
  foreign key (organization_id,previous_resolution_id) references attribution_discard_resolutions(organization_id,id),
  check (source_kind in ('brief','promotion','copy','asset')), check (outcome in ('aceptada','rechazada')),
  check (num_nonnulls(brief_attribution_id)=1 and source_kind='brief'),
  check (resolved_by<>affected_contributor_id), check (resolved_by<>requested_by), check (resolved_by<>change_actor_id),
  check (char_length(btrim(reason))>=1 and char_length(btrim(evidence))>=1),
  check (created_by=resolved_by), check (evidence_attribution_id=brief_attribution_id), check (previous_resolution_id is distinct from id));
create unique index u_adr_aceptada on attribution_discard_resolutions(organization_id,brief_attribution_id) where outcome='aceptada';
create function trg_adr_ins() returns trigger language plpgsql as $$ declare p attribution_discard_resolutions; a brief_field_attributions; sello text; begin
  select * into a from brief_field_attributions where organization_id=new.organization_id and id=new.brief_attribution_id;
  if new.evidence_version_id is distinct from a.version_id then raise exception 'EVIDENCIA_OTRA_VERSION' using errcode='P0001'; end if;
  if new.previous_resolution_id is not null then
    select * into p from attribution_discard_resolutions where organization_id=new.organization_id and id=new.previous_resolution_id;
    if not found or p.brief_attribution_id is distinct from new.brief_attribution_id or p.outcome<>'rechazada' then raise exception 'PREVIA_INVALIDA' using errcode='P0001'; end if; end if;
  sello:=encode(sha256(convert_to(concat_ws('|',new.id,new.organization_id,new.brief_attribution_id,new.field_key,new.affected_contributor_id,new.requested_by,new.resolved_by,new.reason,new.evidence,new.trigger_event_id,new.change_actor_id,new.evidence_version_id,new.outcome,coalesce(new.previous_resolution_id::text,'')),'UTF8')),'hex');
  if new.record_seal is distinct from sello then raise exception 'SELLO_INVALIDO' using errcode='P0001'; end if; return new; end $$;
create trigger t_adr_ins before insert on attribution_discard_resolutions for each row execute function trg_adr_ins();
create trigger t_adr_imm before update or delete on attribution_discard_resolutions for each row execute function trg_inmutable();
create trigger t_adr_trunc before truncate on attribution_discard_resolutions for each statement execute function trg_inmutable();
create table resultados(n serial, id text, regla text, descripcion text, esperado text, obtenido text, resultado text);
create function t(p_id text, p_regla text, p_desc text, p_esperado text, p_sql text) returns void language plpgsql as $$ declare ob text; begin
  begin execute p_sql; ob:='OK'; exception when others then ob:=sqlstate||':'||left(sqlerrm,70); end;
  insert into resultados(id,regla,descripcion,esperado,obtenido,resultado) values(p_id,p_regla,p_desc,p_esperado,ob, case when ob=p_esperado or (p_esperado<>'OK' and ob like p_esperado||'%') then 'PASS' else 'FAIL' end); end $$;
