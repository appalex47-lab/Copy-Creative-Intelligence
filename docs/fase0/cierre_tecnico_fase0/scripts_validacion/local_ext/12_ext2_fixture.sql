-- EXTENSIÓN LOCAL 2 (decisiones): prototipos DG-20, DG-18, G-9, DG-16. TEMPORAL; no es migración ni esquema físico. Requiere btree_gist en el clúster LOCAL.
create extension if not exists btree_gist;
-- DG-20: approvals con decision (prototipo de la «ampliación mínima»)
create table approvals_dg20_x(
  id uuid primary key, organization_id uuid not null, piece_id uuid not null, copy_version_id uuid not null, approver uuid not null,
  decision text not null check (decision = 'aprobada'),
  unique(organization_id,id,copy_version_id),
  foreign key (organization_id,piece_id,copy_version_id) references copy_versions(organization_id,piece_id,id));
create table cit_dg20_x(id int primary key, o uuid not null, a uuid not null, v uuid not null, foreign key (o,a,v) references approvals_dg20_x(organization_id,id,copy_version_id));
-- Migración segura: tabla heredada sin la columna, con una fila; añadir la columna con DEFAULT y luego el CHECK
create table approvals_legacy_x(id uuid primary key, organization_id uuid not null, piece_id uuid not null, copy_version_id uuid not null, approver uuid not null);
-- DG-18: creative_pieces con replaces_piece_id (prototipo en tabla aparte para no alterar el fixture V20)
create table pieces_dg18_x(
  id uuid primary key, organization_id uuid not null references organizations(id), state text not null default 'Borrador',
  replaces_piece_id uuid null, unique(organization_id,id),
  foreign key (organization_id,replaces_piece_id) references pieces_dg18_x(organization_id,id) on delete restrict,
  check (replaces_piece_id is distinct from id));
create function trg_replaces_inmutable_x() returns trigger language plpgsql as $$ begin
  if new.replaces_piece_id is distinct from old.replaces_piece_id then raise exception 'REPLACES_INMUTABLE' using errcode='P0001'; end if; return new; end $$;
create trigger t_replaces before update on pieces_dg18_x for each row execute function trg_replaces_inmutable_x();
-- G-9: piece_reviewer_assignments con vigencia (prototipo)
create table piece_reviewer_assignments_x(
  id uuid primary key, organization_id uuid not null, piece_id uuid not null, reviewer_id uuid not null, assigned_by uuid not null,
  valid_during tstzrange not null, reason text not null,
  unique(organization_id,id),
  foreign key (organization_id,piece_id) references creative_pieces(organization_id,id),
  foreign key (organization_id,reviewer_id) references memberships(organization_id,user_id),
  foreign key (organization_id,assigned_by) references memberships(organization_id,user_id),
  check (not isempty(valid_during) and lower(valid_during) is not null and lower_inc(valid_during) and not upper_inc(valid_during)),
  check (char_length(btrim(reason)) > 0),
  exclude using gist (organization_id with =, piece_id with =, valid_during with &&));
create function trg_pra_x() returns trigger language plpgsql as $$ begin
  if tg_op='DELETE' then raise exception 'ASIGNACION_INMUTABLE' using errcode='P0001'; end if;
  if (new.id,new.organization_id,new.piece_id,new.reviewer_id,new.assigned_by,new.reason) is distinct from (old.id,old.organization_id,old.piece_id,old.reviewer_id,old.assigned_by,old.reason)
     or lower(new.valid_during) is distinct from lower(old.valid_during) or upper(old.valid_during) is not null or upper(new.valid_during) is null then
     raise exception 'ASIGNACION_INMUTABLE' using errcode='P0001'; end if; return new; end $$;
create trigger t_pra before update or delete on piece_reviewer_assignments_x for each row execute function trg_pra_x();
-- DG-16: función de «texto no vacío» robusta (prototipo) frente a btrim
create function texto_no_vacio_x(t text) returns boolean language sql immutable as $$ select t is null or t !~ E'^[\\s\\u00a0\\u200b-\\u200d\\u2060\\ufeff]*$' $$;
create table justificaciones_x(id serial primary key, j_btrim text check (char_length(btrim(j_btrim))>0), j_robusto text check (texto_no_vacio_x(j_robusto)), j_min30 text check (char_length(btrim(j_min30)) >= 30));
-- DG-16 (recomendación): longitud en caracteres SIGNIFICATIVOS (excluye espacios Unicode/ceros de ancho cero)
create function longitud_significativa_x(t text) returns int language sql immutable as $$ select char_length(regexp_replace(t, E'[\\s\\u00a0\\u200b-\\u200d\\u2060\\ufeff]', '', 'g')) $$;
create table justificaciones2_x(id serial primary key, j text check (longitud_significativa_x(j) >= 30));
