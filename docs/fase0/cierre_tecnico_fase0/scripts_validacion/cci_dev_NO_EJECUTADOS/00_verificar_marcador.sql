-- ====================================================================================================
-- 00_verificar_marcador.sql — COMPRUEBA QUE LA GUARDA ÍNTEGRA SE EJECUTÓ EN ESTA EJECUCIÓN, PARA ESTE SCRIPT (cierre definitivo, AUD-CIERRE-01).
-- Mecanismo: la guarda, tras superar TODAS sus comprobaciones, genera un identificador aleatorio (gen_random_uuid, CSPRNG del servidor) y lo guarda en la
-- variable de psql cci_run (\gset; SQL no puede escribir variables de psql) y crea una tabla TEMPORAL con nombre derivado de ese identificador (imprevisible: no puede
-- preexistir) con una fila (script, pid, usado=false). Aquí se exige: cci_run definida; tabla de ESA ejecución; fila del mismo script y del mismo backend; y se CONSUME
-- (usado=true: de un solo uso). Después se borra cci_run. Consecuencias: tabla/GUC preinstalados, marcador de otra ejecución/otro script/otra sesión, marcador tras
-- error o rollback, o guarda vacía => rechazo. NO es una frontera contra quien pueda escribir la guarda/los scripts (ver LIMITACIONES).
-- ====================================================================================================
\if :{?cci_run}
\else
do $x$ begin raise exception 'NO EJECUTADO [G-GUARDA-NO-EJECUTADA] la guarda no generó el identificador de esta ejecución'; end $x$;
\endif
select pg_catalog.format($q$do $x$ declare n int; begin
  perform pg_catalog.set_config('search_path','pg_catalog, pg_temp',true);
  if pg_catalog.to_regclass(%L) is null then raise exception 'NO EJECUTADO [G-GUARDA-NO-EJECUTADA] no existe el marcador de esta ejecución'; end if;
  update pg_temp.%I set usado = true where script = %L and pid = pg_catalog.pg_backend_pid() and not usado;
  get diagnostics n = row_count;
  if n <> 1 then raise exception 'NO EJECUTADO [G-GUARDA-NO-EJECUTADA] marcador inválido para este script/sesión o ya consumido'; end if;
end $x$$q$, pg_catalog.concat('pg_temp.cci_g_', :'cci_run'), pg_catalog.concat('cci_g_', :'cci_run'), :'cci_script') as q \gexec
\unset cci_run
