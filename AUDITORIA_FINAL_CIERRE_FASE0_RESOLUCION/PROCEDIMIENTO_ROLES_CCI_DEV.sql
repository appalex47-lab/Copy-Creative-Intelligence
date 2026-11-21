-- PROCEDIMIENTO_ROLES_CCI_DEV.sql — PLANTILLA. NO EJECUTADO. NO se concede nada real: los nombres entre <…> los define el propietario.
-- Debe ejecutarlo un ADMINISTRADOR de CCI-DEV (no un operador), una sola vez, con aprobación escrita del propietario. NO ejecutar en CCI-PROD.
-- La guarda (00_guarda_destino.sql, modo DEV) exige: session_user = current_user; rol existente sin SUPERUSER/CREATEROLE/CREATEDB/BYPASSRLS/REPLICATION;
-- pertenencia (directa o indirecta) a cci_operador; NO pertenencia a cci_custodio ni cci_administrador (separación de funciones). Deniega por defecto.
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
commit;
-- Verificación posterior (el administrador la ejecuta y guarda la salida como evidencia):
--   select rolname, rolsuper, rolcreaterole, rolcreatedb, rolbypassrls, rolreplication from pg_roles where rolname like 'cci\_%' or rolname = '<operador_1>';
--   select pg_has_role('<operador_1>','cci_operador','member'), pg_has_role('<operador_1>','cci_custodio','member'), pg_has_role('<operador_1>','cci_administrador','member');
--   -- esperado: t, f, f
