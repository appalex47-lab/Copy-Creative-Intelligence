-- ====================================================================================================
-- 00_guarda_destino.sql — GUARDA DE DESTINO DEV/PROD (hallazgo H-03). Se incluye con \ir al inicio de los 6 scripts; NO es un script autónomo.
-- Diseño: la identidad del destino se obtiene DEL SERVIDOR (system_identifier del clúster + nombre de la base + roles de plataforma), nunca de lo que
-- declare el operador. Las variables de sesión (cci.validacion_autorizada / cci.entorno) solo expresan la INTENCIÓN del operador y no bastan.
-- ALLOWLIST (dev_allow, formato 'system_identifier|base') y DENYLIST (prod_deny, formato 'system_identifier') son LITERALES versionados en este archivo:
-- no se leen de variables de sesión ni de PGOPTIONS, así que cambiarlas exige un cambio revisable en git (decisión del propietario).
-- Estado: ambas listas están VACÍAS a propósito (el propietario no ha entregado los identificadores reales de CCI-DEV/CCI-PROD; no se inventan) =>
-- el modo CCI-DEV rechaza TODO destino (DESTINO-DESCONOCIDO) hasta que el propietario registre el identificador de CCI-DEV. Falla de forma segura.
-- Cómo obtener el identificador (solo lectura, en cada proyecto): select system_identifier from pg_catalog.pg_control_system();
-- Reglas (en este orden; la primera que falla aborta con 'NO EJECUTADO [CÓDIGO]'; el mensaje no incluye secretos, solo una huella md5 truncada):
--   G-SEARCH-PATH-NO-SEGURO el search_path efectivo del llamador contiene esquemas distintos de pg_catalog/public/pg_temp/"$user", "$user" apunta a un esquema existente, o public/pg_temp preceden a pg_catalog
--   G-ROL-CAMBIADO / G-OPERADOR-DESCONOCIDO / G-OPERADOR-PRIVILEGIO-EXCESIVO / G-OPERADOR-ROLES-NO-CONFIGURADOS / G-OPERADOR-NO-AUTORIZADO / G-SEPARACION-FUNCIONES  (modo DEV; autorización del operador, ver MATRIZ_AUTORIZACION_OPERADORES.md)
--   G-OPERADOR-CREATE-EN-PUBLIC / G-OPERADOR-CREATE-EN-BASE / G-PUBLIC-CREATE-AJENO  (modo DEV; privilegios EFECTIVOS: el operador y ningún rol no superusuario puede crear objetos en public; el operador tampoco en la base)
--   G-OPERADOR-AJENO-EN-SEARCH-PATH / G-CAST-AJENO  (todos los modos; operadores en public/temporales o casts de usuario alteran la resolución de operadores)
--   G-CONFIG-INCOMPLETA     falta cci.validacion_autorizada o cci.entorno
--   G-CONFIG-INVALIDA       el par declarado no es (SI-CCI-DEV,CCI-DEV) ni (SI-LOCAL-TEMPORAL,LOCAL-TEMPORAL)
--   G-IDENTIDAD-NO-VERIFICABLE  no se pudo leer la identidad efectiva (p. ej. pg_control_system() sin permiso)
--   G-PROD-RECHAZADO        el clúster está en prod_deny: se rechaza AUNQUE el operador declare DEV
--   G-DESTINO-DESCONOCIDO   (modo DEV) 'system_identifier|base' no está en dev_allow
--   G-LOCAL-NO-SOCKET / G-LOCAL-BASE / G-LOCAL-ROLES-PLATAFORMA  (modo local) exige socket Unix, base ^cci_ y ausencia de roles supabase_*
--   G-GUARDA-INTEGRIDAD / G-GUARDA-NO-EJECUTADA   (las emiten 00_preflight_guarda.sql y 00_verificar_marcador.sql, no este archivo): hash externo no coincide, o no hay marcador de ESTA ejecución para ESTE script (ver cabeceras de esos archivos)
-- ====================================================================================================
do $guarda$
declare
  a text := coalesce(pg_catalog.current_setting('cci.validacion_autorizada', true),''); e text := coalesce(pg_catalog.current_setting('cci.entorno', true),'');
  dev_allow text[] := array[]::text[];  -- @@DEV_ALLOW@@  (vacío: el propietario añade 'system_identifier|base' de CCI-DEV)
  prod_deny text[] := array[]::text[];  -- @@PROD_DENY@@  (vacío: el propietario añade el 'system_identifier' de CCI-PROD)
  sysid text; dbn text := pg_catalog.current_database(); ident text; plat int; fp text; err text;
  so_super bool; so_crole bool; so_cdb bool; so_byp bool; so_repl bool;
  nfo int; nrc int; roles_c int;
  sp0 text := pg_catalog.current_setting('search_path'); ent text; n int := 0; ipc int := 0; ipub int := 0; ipt int := 0;   -- search_path EFECTIVO del llamador (ALTER ROLE/DATABASE, PGOPTIONS, SET) capturado ANTES de blindar el del bloque
begin
  perform pg_catalog.set_config('search_path','pg_catalog, pg_temp',true);   -- anti-suplantación: ningún objeto del operador (p. ej. public.pg_control_system) puede sustituir a los del catálogo
  -- @@SP_CHECK_INI@@ (cierre definitivo, AUD-CIERRE-04) el script NO se ejecuta bajo un search_path hostil: el del bloque es local y las instrucciones posteriores usan el del llamador
  foreach ent in array pg_catalog.string_to_array(sp0, ',') loop
    ent := pg_catalog.btrim(ent); n := n + 1;
    if ent = 'pg_catalog' then ipc := n; elsif ent in ('public','"public"') then ipub := n; elsif ent = 'pg_temp' then ipt := n; end if;
    if ent not in ('pg_catalog','public','pg_temp','"$user"','"public"') then raise exception 'NO EJECUTADO [G-SEARCH-PATH-NO-SEGURO]: el search_path del llamador contiene un esquema no permitido (%); sólo pg_catalog, public, pg_temp y "$user"', ent; end if;
    if ent = '"$user"' and exists (select 1 from pg_catalog.pg_namespace where nspname = current_user) then raise exception 'NO EJECUTADO [G-SEARCH-PATH-NO-SEGURO]: existe un esquema con el nombre del rol y "$user" está en el search_path'; end if;
  end loop;
  if ipc > 0 and ((ipub > 0 and ipub < ipc) or (ipt > 0 and ipt < ipc)) then raise exception 'NO EJECUTADO [G-SEARCH-PATH-NO-SEGURO]: public o pg_temp preceden a pg_catalog en el search_path (los operadores/funciones de esos esquemas ganarían a los del catálogo)'; end if;
  -- @@SP_CHECK_FIN@@
  if a = '' or e = '' then raise exception 'NO EJECUTADO [G-CONFIG-INCOMPLETA]: falta cci.validacion_autorizada y/o cci.entorno'; end if;
  if not ((a = 'SI-CCI-DEV' and e = 'CCI-DEV') or (a = 'SI-LOCAL-TEMPORAL' and e = 'LOCAL-TEMPORAL')) then raise exception 'NO EJECUTADO [G-CONFIG-INVALIDA]: par de variables no reconocido'; end if;
  begin select system_identifier::text into sysid from pg_catalog.pg_control_system();
  exception when others then sysid := null; err := sqlstate; end;
  if sysid is null or dbn is null or sysid = '' then raise exception 'NO EJECUTADO [G-IDENTIDAD-NO-VERIFICABLE]: no se pudo leer la identidad efectiva del servidor (sqlstate=%)', coalesce(err,'sin_fila'); end if;
  ident := sysid || '|' || dbn; fp := pg_catalog.left(pg_catalog.md5(sysid), 8);
  select pg_catalog.count(*) into plat from pg_catalog.pg_roles where rolname in ('supabase_admin','supabase_auth_admin','supabase_storage_admin','supabase_read_only_user','pgbouncer');
  if sysid = any(prod_deny) then raise exception 'NO EJECUTADO [G-PROD-RECHAZADO]: el clúster destino (huella %) está en la lista de PRODUCCIÓN; se rechaza aunque se declare DEV', fp; end if;
  if a = 'SI-CCI-DEV' then
    if not (ident = any(dev_allow)) then raise exception 'NO EJECUTADO [G-DESTINO-DESCONOCIDO]: el destino (huella %) no está en la allowlist de CCI-DEV autorizados', fp; end if;
    -- AUTORIZACIÓN DEL OPERADOR (resolución final, AUD-RF-02): denegación por defecto. Se evalúa con session_user (no cambia con SET ROLE) y con funciones calificadas de pg_catalog; no usa GUC ni variables del cliente.
    if session_user <> current_user then raise exception 'NO EJECUTADO [G-ROL-CAMBIADO]: el rol efectivo difiere del rol de la sesión (SET ROLE/SECURITY DEFINER); el operador debe ejecutar con su propio rol'; end if;
    select r.rolsuper, r.rolcreaterole, r.rolcreatedb, r.rolbypassrls, r.rolreplication into so_super, so_crole, so_cdb, so_byp, so_repl from pg_catalog.pg_roles r where r.rolname = session_user;
    if not found then raise exception 'NO EJECUTADO [G-OPERADOR-DESCONOCIDO]: el rol de la sesión no existe en pg_roles'; end if;
    if so_super or so_crole or so_cdb or so_byp or so_repl then raise exception 'NO EJECUTADO [G-OPERADOR-PRIVILEGIO-EXCESIVO]: el operador no puede tener SUPERUSER, CREATEROLE, CREATEDB, BYPASSRLS ni REPLICATION (privilegios mínimos)'; end if;
    if not exists (select 1 from pg_catalog.pg_roles where rolname = 'cci_operador') then raise exception 'NO EJECUTADO [G-OPERADOR-ROLES-NO-CONFIGURADOS]: no existe el rol cci_operador; el administrador debe crear la matriz de roles (PROCEDIMIENTO_ROLES_CCI_DEV.sql)'; end if;
    if not pg_catalog.pg_has_role(session_user, 'cci_operador', 'member') then raise exception 'NO EJECUTADO [G-OPERADOR-NO-AUTORIZADO]: el rol de la sesión no es miembro de cci_operador'; end if;
    if exists (select 1 from pg_catalog.pg_roles x where x.rolname in ('cci_custodio','cci_administrador') and pg_catalog.pg_has_role(session_user, x.oid, 'member')) then raise exception 'NO EJECUTADO [G-SEPARACION-FUNCIONES]: el operador no puede ser a la vez custodio o administrador'; end if;
    -- @@PRIV_CHECK_INI@@ (cierre de operadores, AUD-OP-01) PRIVILEGIOS EFECTIVOS (has_*_privilege: incluyen herencia, PUBLIC y propiedad): el operador no puede crear objetos que alteren la resolución de nombres
    if pg_catalog.has_schema_privilege(session_user, 'public', 'CREATE') then raise exception 'NO EJECUTADO [G-OPERADOR-CREATE-EN-PUBLIC]: el rol de la sesión tiene CREATE efectivo sobre el esquema public (podría introducir operadores/funciones/tipos que alteren los scripts); el administrador debe revocarlo (PROCEDIMIENTO_ROLES_CCI_DEV.sql)'; end if;
    if pg_catalog.has_database_privilege(session_user, dbn, 'CREATE') then raise exception 'NO EJECUTADO [G-OPERADOR-CREATE-EN-BASE]: el rol de la sesión tiene CREATE efectivo sobre la base (podría crear esquemas auxiliares, p. ej. uno con su propio nombre); el administrador debe revocarlo'; end if;
    select pg_catalog.count(*) into roles_c from pg_catalog.pg_roles x where not x.rolsuper and x.rolname !~ '^pg_' and pg_catalog.has_schema_privilege(x.oid, 'public', 'CREATE') and not pg_catalog.pg_has_role(x.oid, 'pg_database_owner', 'member');
    if roles_c > 0 then raise exception 'NO EJECUTADO [G-PUBLIC-CREATE-AJENO]: % rol(es) no superusuario con CREATE efectivo sobre public pueden plantar operadores entre la comprobación y la ejecución; el administrador debe revocarlo', roles_c; end if;
    if exists (select 1 from pg_catalog.pg_roles x where (x.rolsuper or x.rolcreaterole or x.rolcreatedb or x.rolbypassrls or x.rolreplication) and x.oid <> (select r2.oid from pg_catalog.pg_roles r2 where r2.rolname = session_user) and pg_catalog.pg_has_role(session_user, x.oid, 'member')) then raise exception 'NO EJECUTADO [G-OPERADOR-MEMBRESIA-PRIVILEGIADA]: el rol de la sesión es miembro (aunque sea NOINHERIT, directa o indirecta) de un rol con SUPERUSER/CREATEROLE/CREATEDB/BYPASSRLS/REPLICATION y podría recuperarlo con SET ROLE'; end if;
    -- @@PRIV_CHECK_FIN@@
    raise log 'CCI-AUDITORIA operador=% pid=% app=% destino_huella=%', session_user, pg_catalog.pg_backend_pid(), pg_catalog.current_setting('application_name'), fp;
  else
    if pg_catalog.inet_server_addr() is not null then raise exception 'NO EJECUTADO [G-LOCAL-NO-SOCKET]: el modo local exige socket Unix (huella %)', fp; end if;
    if dbn !~ '^cci_' then raise exception 'NO EJECUTADO [G-LOCAL-BASE]: el modo local exige base ^cci_ (huella %)', fp; end if;
    if plat > 0 then raise exception 'NO EJECUTADO [G-LOCAL-ROLES-PLATAFORMA]: la base tiene roles de plataforma supabase_* (huella %); no es un clúster local temporal', fp; end if;
  end if;
  -- @@OP_CHECK_INI@@ (cierre de operadores, AUD-OP-01) NINGÚN operador ajeno al catálogo en los esquemas que el blindaje deja en el search_path (public, temporales) ni casts definidos por usuarios: una firma más específica en public gana a pg_catalog (demostrado: = (oid, regnamespace))
  select pg_catalog.count(*) into nfo from pg_catalog.pg_operator o join pg_catalog.pg_namespace n on n.oid = o.oprnamespace where n.nspname = 'public' or n.nspname ~ '^pg_temp_' or n.nspname ~ '^pg_toast_temp_';
  if nfo > 0 then raise exception 'NO EJECUTADO [G-OPERADOR-AJENO-EN-SEARCH-PATH]: existen % operador(es) definidos en public o esquemas temporales; podrían sustituir a los de pg_catalog en los scripts', nfo; end if;
  select pg_catalog.count(*) into nrc from pg_catalog.pg_cast c where c.oid >= 16384::oid;
  if nrc > 0 then raise exception 'NO EJECUTADO [G-CAST-AJENO]: existen % cast(s) definidos por usuarios; alteran la resolución de operadores por conversión implícita', nrc; end if;
  -- @@OP_CHECK_FIN@@
  raise notice 'GUARDA OK modo=% huella=%', a, fp;
end $guarda$;
-- BLINDAJE DE SESIÓN (resolución del límite SPD7): sólo tras superar la guarda se fija el search_path de la SESIÓN a pg_catalog primero; los operadores sin calificar de los scripts ya no se resuelven en esquemas del llamador. (public queda por detrás: los homónimos exactos de pg_catalog ganan por orden.)
select pg_catalog.set_config('search_path','pg_catalog, public, pg_temp',false) as _cci_sp_pin \gset
-- MARCADOR POR EJECUCIÓN (cierre definitivo). Sólo se llega aquí si TODAS las comprobaciones anteriores pasaron. cci_script lo declara el script que nos incluye.
\if :{?cci_script}
\else
do $x$ begin raise exception 'NO EJECUTADO [G-GUARDA-NO-EJECUTADA] la guarda se incluyó sin declarar cci_script'; end $x$;
\endif
\unset cci_run
select pg_catalog.replace(pg_catalog.gen_random_uuid()::text, '-', '') as cci_run \gset
select pg_catalog.format('create temp table pg_temp.%I (script text not null, pid int not null, usado boolean not null default false)', pg_catalog.concat('cci_g_', :'cci_run')) \gexec
select pg_catalog.format('insert into pg_temp.%I values (%L, pg_catalog.pg_backend_pid(), false)', pg_catalog.concat('cci_g_', :'cci_run'), :'cci_script') \gexec
