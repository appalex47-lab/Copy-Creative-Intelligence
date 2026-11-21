-- ====================================================================================================
-- NO EJECUTADO CONTRA CCI-DEV NI CCI-PROD — REQUIERE AUTORIZACIÓN Y CCI-DEV (cuando se use con 04_trigger_r1_r9_ROLLBACK.sql)
-- BIBLIOTECA DEL ARNÉS (sólo objetos TEMPORALES pg_temp; no toca tablas de negocio). Se incluye con \ir desde 04 y desde la autoprueba local.
-- Propósito: distinguir sin ambigüedad (a) rechazo esperado por regla de negocio, (b) error de permisos, (c) función/dependencia inexistente,
--            (d) error de estructura, (e) error de sintaxis, (f) error inesperado. Un caso negativo sólo puede ser PASS si el rechazo es de dominio
--            Y coincide con el contrato esperado declarado. Estados de veredicto: PASS, FAIL, BLOCKED, PARTIAL, NOT VERIFIED.
-- Los objetos pg_temp desaparecen al cerrar la sesión.
-- ====================================================================================================
-- Clasifica un error (SQLSTATE + mensaje) en una clase técnica.
create or replace function pg_temp.clase(p_sqlstate text, p_msg text) returns text language sql immutable as $f$
  select case
    when p_sqlstate is null then 'OK'
    when p_sqlstate = '42501' then 'PERMISOS'
    when p_sqlstate = '42883' then 'FUNCION_INEXISTENTE'            -- undefined_function: la función, o una función de la que depende, no existe / firma incorrecta
    when p_sqlstate in ('42P01','42703','42704','42P02','42P10','42804','42P07','42710','3F000','42P16') then 'ESTRUCTURA'
    when p_sqlstate in ('42601','42000','42P18','42P19','42611','42602','42622') then 'SINTAXIS'
    when p_sqlstate = 'P0001' or p_sqlstate like '23%' or p_sqlstate like 'RJ%' then 'DOMINIO_CANDIDATO'   -- posible rechazo de negocio (RJ%: clase PROPUESTA en PROPUESTA_CONTRATO_ERRORES_R1_R9.md, no aprobada); sólo cuenta si coincide con el contrato esperado
    else 'ERROR_INESPERADO' end $f$;
-- Ejecuta una sentencia como (rol, uid) dentro de un sub-bloque con excepción; nunca propaga el error: lo devuelve clasificado.
-- p_post: sentencia opcional (devuelve un valor) evaluada DESPUÉS de p_sql y ANTES de deshacer, para comprobar el efecto (p. ej. que se registró la fila).
-- p_deshacer: si es true, TODO efecto de p_sql y p_post se revierte (sub-transacción) mediante una excepción centinela 'CC999'; el llamador no deja residuos.
create or replace function pg_temp.ejecuta(p_sql text, p_rol text, p_uid uuid, p_post text default null, p_deshacer boolean default true, out o_clase text, out o_sqlstate text, out o_msg text, out o_post text) language plpgsql as $f$
begin
  begin
    if p_rol is not null then execute format('set local role %I', p_rol); end if;
    if p_uid is not null then perform set_config('request.jwt.claims', json_build_object('sub', p_uid, 'role', coalesce(p_rol,'authenticated'))::text, true); end if;
    execute p_sql;
    o_clase := 'OK'; o_sqlstate := null; o_msg := null;
    if p_post is not null then execute p_post into o_post; end if;
    if p_deshacer then raise exception 'deshacer' using errcode = 'CC999'; end if;
  exception
    when sqlstate 'CC999' then null;   -- centinela propio: el resultado ya está guardado en o_*
    when others then o_sqlstate := sqlstate; o_msg := left(sqlerrm, 200); o_clase := pg_temp.clase(sqlstate, sqlerrm);
  end;
  begin reset role; exception when others then null; end;   -- reset role no debe enmascarar el resultado
end $f$;
-- Veredicto. p_tipo: 'DENEGADO' (se exige 42501), 'NEG' (se espera rechazo de negocio), 'POS' (se espera éxito), 'ERR_PERM' (se espera error de permisos).
-- p_esperado: contrato esperado 'SQLSTATE[:prefijo del mensaje]' ('' si la especificación no lo define). p_precond: false => BLOCKED.
create or replace function pg_temp.veredicto(p_tipo text, p_clase text, p_sqlstate text, p_msg text, p_esperado text, p_precond boolean default true) returns text language sql immutable as $f$
  select case
    when not coalesce(p_precond,false) then 'BLOCKED'
    when p_tipo = 'POS' then case p_clase when 'OK' then 'PASS' when 'ERROR_INESPERADO' then 'FAIL' when 'DOMINIO_CANDIDATO' then 'FAIL' else 'BLOCKED' end
    when p_tipo = 'DENEGADO' then case when p_clase = 'PERMISOS' then 'PASS' when p_clase in ('OK','ERROR_INESPERADO','DOMINIO_CANDIDATO') then 'FAIL' else 'BLOCKED' end   -- se exige denegación 42501 (diseño: sin escritura directa)
    when p_tipo = 'ERR_PERM' then case when p_clase = 'PERMISOS' then 'PARTIAL' when p_clase = 'OK' then 'FAIL' when p_clase = 'ERROR_INESPERADO' then 'FAIL' else 'BLOCKED' end
    when p_tipo = 'NEG' then case
        when p_clase = 'OK' then 'FAIL'                                   -- la regla no rechazó
        when p_clase = 'ERROR_INESPERADO' then 'FAIL'
        when p_clase in ('PERMISOS','FUNCION_INEXISTENTE','ESTRUCTURA','SINTAXIS') then 'BLOCKED'   -- fallo técnico: JAMÁS es PASS
        when p_clase = 'DOMINIO_CANDIDATO' then case
            when coalesce(p_esperado,'') = '' then 'PARTIAL'              -- rechazo observado pero la especificación no define el contrato: no se puede atribuir a la regla
            when p_sqlstate = split_part(p_esperado, ':', 1) and (position(':' in p_esperado) = 0 or starts_with(coalesce(p_msg,''), substr(p_esperado, position(':' in p_esperado) + 1))) then 'PASS'   -- SQLSTATE EXACTO; el prefijo de mensaje solo se exige si el contrato lo declara
            else 'FAIL' end
        else 'FAIL' end
    else 'NOT VERIFIED' end $f$;
