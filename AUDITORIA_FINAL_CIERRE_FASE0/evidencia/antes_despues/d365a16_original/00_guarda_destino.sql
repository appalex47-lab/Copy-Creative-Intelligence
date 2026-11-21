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
--   G-CONFIG-INCOMPLETA     falta cci.validacion_autorizada o cci.entorno
--   G-CONFIG-INVALIDA       el par declarado no es (SI-CCI-DEV,CCI-DEV) ni (SI-LOCAL-TEMPORAL,LOCAL-TEMPORAL)
--   G-IDENTIDAD-NO-VERIFICABLE  no se pudo leer la identidad efectiva (p. ej. pg_control_system() sin permiso)
--   G-PROD-RECHAZADO        el clúster está en prod_deny: se rechaza AUNQUE el operador declare DEV
--   G-DESTINO-DESCONOCIDO   (modo DEV) 'system_identifier|base' no está en dev_allow
--   G-LOCAL-NO-SOCKET / G-LOCAL-BASE / G-LOCAL-ROLES-PLATAFORMA  (modo local) exige socket Unix, base ^cci_ y ausencia de roles supabase_*
--   G-GUARDA-NO-EJECUTADA   (la emite cada script, no este archivo) tras \ir este archivo no dejó el marcador cci.guarda_ok='1': guarda vacía, truncada o neutralizada
-- ====================================================================================================
do $guarda$
declare
  a text := coalesce(pg_catalog.current_setting('cci.validacion_autorizada', true),''); e text := coalesce(pg_catalog.current_setting('cci.entorno', true),'');
  dev_allow text[] := array[]::text[];  -- @@DEV_ALLOW@@  (vacío: el propietario añade 'system_identifier|base' de CCI-DEV)
  prod_deny text[] := array[]::text[];  -- @@PROD_DENY@@  (vacío: el propietario añade el 'system_identifier' de CCI-PROD)
  sysid text; dbn text := pg_catalog.current_database(); ident text; plat int; fp text; err text;
begin
  perform pg_catalog.set_config('cci.guarda_ok','',false);   -- marcador de sesión (AUD-G1): se limpia al inicio y sólo se fija en '1' si TODAS las reglas pasan
  perform pg_catalog.set_config('search_path','pg_catalog, pg_temp',true);   -- anti-suplantación: ningún objeto del operador (p. ej. public.pg_control_system) puede sustituir a los del catálogo
  if a = '' or e = '' then raise exception 'NO EJECUTADO [G-CONFIG-INCOMPLETA]: falta cci.validacion_autorizada y/o cci.entorno'; end if;
  if not ((a = 'SI-CCI-DEV' and e = 'CCI-DEV') or (a = 'SI-LOCAL-TEMPORAL' and e = 'LOCAL-TEMPORAL')) then raise exception 'NO EJECUTADO [G-CONFIG-INVALIDA]: par de variables no reconocido'; end if;
  begin select system_identifier::text into sysid from pg_catalog.pg_control_system();
  exception when others then sysid := null; err := sqlstate; end;
  if sysid is null or dbn is null or sysid = '' then raise exception 'NO EJECUTADO [G-IDENTIDAD-NO-VERIFICABLE]: no se pudo leer la identidad efectiva del servidor (sqlstate=%)', coalesce(err,'sin_fila'); end if;
  ident := sysid || '|' || dbn; fp := left(md5(sysid), 8);
  select count(*) into plat from pg_catalog.pg_roles where rolname in ('supabase_admin','supabase_auth_admin','supabase_storage_admin','supabase_read_only_user','pgbouncer');
  if sysid = any(prod_deny) then raise exception 'NO EJECUTADO [G-PROD-RECHAZADO]: el clúster destino (huella %) está en la lista de PRODUCCIÓN; se rechaza aunque se declare DEV', fp; end if;
  if a = 'SI-CCI-DEV' then
    if not (ident = any(dev_allow)) then raise exception 'NO EJECUTADO [G-DESTINO-DESCONOCIDO]: el destino (huella %) no está en la allowlist de CCI-DEV autorizados', fp; end if;
  else
    if inet_server_addr() is not null then raise exception 'NO EJECUTADO [G-LOCAL-NO-SOCKET]: el modo local exige socket Unix (huella %)', fp; end if;
    if dbn !~ '^cci_' then raise exception 'NO EJECUTADO [G-LOCAL-BASE]: el modo local exige base ^cci_ (huella %)', fp; end if;
    if plat > 0 then raise exception 'NO EJECUTADO [G-LOCAL-ROLES-PLATAFORMA]: la base tiene roles de plataforma supabase_* (huella %); no es un clúster local temporal', fp; end if;
  end if;
  perform pg_catalog.set_config('cci.guarda_ok','1',false);
  raise notice 'GUARDA OK modo=% huella=%', a, fp;
end $guarda$;
