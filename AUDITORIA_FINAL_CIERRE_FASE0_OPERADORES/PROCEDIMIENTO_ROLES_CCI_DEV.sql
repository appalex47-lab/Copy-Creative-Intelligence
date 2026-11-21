-- PROCEDIMIENTO_ROLES_CCI_DEV.sql — PLANTILLA. NO EJECUTADO. NO se concede nada real: los nombres entre <…> los define el propietario.
-- Debe ejecutarlo un ADMINISTRADOR de CCI-DEV (no un operador), una sola vez, con aprobación escrita del propietario. NO ejecutar en CCI-PROD.
-- La guarda (00_guarda_destino.sql, modo DEV) exige: session_user = current_user; rol existente sin SUPERUSER/CREATEROLE/CREATEDB/BYPASSRLS/REPLICATION;
-- pertenencia (directa o indirecta) a cci_operador; NO pertenencia a cci_custodio ni cci_administrador (separación de funciones). Deniega por defecto.
-- CIERRE DE OPERADORES (AUD-OP-01): además exige, con comprobaciones EFECTIVAS (has_schema_privilege/has_database_privilege/pg_has_role): el operador SIN CREATE en public ni en la base, SIN
-- membresía (ni NOINHERIT) de roles privilegiados, NINGÚN otro rol no superusuario con CREATE en public, y ningún operador/cast ajeno en public. Ejecute la sección ENDURECIMIENTO antes de validar.
begin;
create role cci_operador nologin;        -- grupo: quien puede EJECUTAR los 6 scripts de validación (solo lectura/ROLLBACK)
create role cci_custodio nologin;        -- grupo: quien aprueba el SHA-256 del conjunto (no ejecuta scripts)
create role cci_administrador nologin;   -- grupo: quien administra roles/esquema de CCI-DEV (no ejecuta scripts)
-- Operadores NOMBRADOS (placeholders): un rol de login por persona, sin privilegios elevados.
-- create role <operador_1> login nosuperuser nocreaterole nocreatedb nobypassrls noreplication password <se entrega por canal seguro, no en este archivo>;
-- grant cci_operador to <operador_1>;
-- Privilegios mínimos que necesitan los scripts (sólo lectura de catálogos; 03/04 trabajan en transacciones con ROLLBACK):
grant connect on database <base_cci_dev> to cci_operador;
grant usage on schema public to cci_operador;
-- Los scripts 03/04/05 requieren fixtures y permisos adicionales sobre el esquema físico aprobado: DEFINIR cuando exista (L04/L05).
-- ENDURECIMIENTO (AUD-OP-01; el administrador, una sola vez, con aprobación del propietario; ajustar a los roles reales de la plataforma):
revoke create on schema public from public;
revoke create on database <base_cci_dev> from public;
revoke create on schema public from cci_operador;
-- Roles de plataforma con CREATE residual en public (p. ej. anon/authenticated/service_role en Supabase: NO VERIFICADO aquí; compruebe con la consulta de abajo y revoque lo que no sea imprescindible):
-- revoke create on schema public from anon, authenticated, service_role;
-- Operadores/casts de usuario en public (debe ser 0, salvo operadores con símbolo no estándar de extensiones como btree_gist): mueva las extensiones a otro esquema o elimínelos.
commit;
-- Verificación posterior (el administrador la ejecuta y guarda la salida como evidencia):
--   select rolname, rolsuper, rolcreaterole, rolcreatedb, rolbypassrls, rolreplication from pg_roles where rolname like 'cci\_%' or rolname = '<operador_1>';
--   select pg_has_role('<operador_1>','cci_operador','member'), pg_has_role('<operador_1>','cci_custodio','member'), pg_has_role('<operador_1>','cci_administrador','member');
--   -- esperado: t, f, f
--   -- CIERRE DE OPERADORES: todo lo siguiente debe devolver 0 filas / f:
--   select r.rolname from pg_roles r where not r.rolsuper and r.rolname !~ '^pg_' and has_schema_privilege(r.oid,'public','CREATE') and not pg_has_role(r.oid,'pg_database_owner','member');
--   select has_schema_privilege('<operador_1>','public','CREATE'), has_database_privilege('<operador_1>','<base_cci_dev>','CREATE');   -- esperado: f, f
--   select o.oprname from pg_operator o join pg_namespace n on n.oid=o.oprnamespace where n.nspname='public';   -- sólo símbolos no estándar de extensiones
--   select count(*) from pg_cast where oid >= 16384;   -- esperado 0
