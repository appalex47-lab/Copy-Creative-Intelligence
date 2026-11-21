-- ====================================================================================================
-- AUTOPRUEBA LOCAL DEL ARNÉS de 04_trigger_r1_r9_ROLLBACK.sql. SOLO PostgreSQL TEMPORAL LOCAL (base cci_arnes_local, socket Unix). Nunca Supabase.
-- QUÉ DEMUESTRA: que el ARNÉS (clasificador y veredicto) no confunde fallos técnicos con rechazos de negocio. Son PRUEBAS DEL ARNÉS.
-- QUÉ NO DEMUESTRA: que R1–R9 funcionen. Las funciones de este archivo son STUBS del arnés que NO implementan R1–R9; no existe implementación física.
-- ====================================================================================================
\set ON_ERROR_STOP on
do $$ begin if not (current_database() = 'cci_arnes_local' and inet_server_addr() is null and coalesce(current_setting('cci.entorno', true),'') = 'LOCAL-TEMPORAL') then raise exception 'NO EJECUTADO: autoprueba solo local (cci_arnes_local, socket Unix, cci.entorno=LOCAL-TEMPORAL)'; end if; end $$;
create schema arnes_stub;
do $$ begin if not exists (select 1 from pg_roles where rolname='cci_arnes_noexec') then create role cci_arnes_noexec nologin; end if; end $$;
create table arnes_stub.res(id int, resolved_by uuid, constraint ck_dist check (id > 0));
-- STUBS (no implementan R1–R9)
create function arnes_stub.stub_dom(a uuid, t text, e text) returns void language plpgsql as $$ begin raise exception 'RESOLUTOR_NO_ELEGIBLE:R1' using errcode='P0001'; end $$;
create function arnes_stub.stub_tecnico_p0001(a uuid, t text, e text) returns void language plpgsql as $$ begin raise exception 'estado interno inconsistente' using errcode='P0001'; end $$;
create function arnes_stub.stub_ok(a uuid, t text, e text) returns void language plpgsql as $$ begin insert into arnes_stub.res values (1, a); end $$;
create function arnes_stub.stub_ok_sin_fila(a uuid, t text, e text) returns void language plpgsql as $$ begin null; end $$;
create function arnes_stub.stub_tabla_falta(a uuid, t text, e text) returns void language plpgsql as $$ begin perform 1 from arnes_stub.no_existe; end $$;
create function arnes_stub.stub_dep_falta(a uuid, t text, e text) returns void language plpgsql as $$ begin perform arnes_stub.dependencia_inexistente(); end $$;
create function arnes_stub.stub_div0(a uuid, t text, e text) returns void language plpgsql as $$ begin perform 1/0; end $$;
create function arnes_stub.stub_check(a uuid, t text, e text) returns void language plpgsql as $$ begin insert into arnes_stub.res values (0, a); end $$;
create function arnes_stub.stub_priv(a uuid, t text, e text) returns void language plpgsql as $$ begin null; end $$;
revoke all on function arnes_stub.stub_priv(uuid,text,text) from public; grant usage on schema arnes_stub to cci_arnes_noexec;
\ir ../cci_dev_NO_EJECUTADOS/04_lib_clasificador.sql
create temp table caso(id text, descr text, tipo text, sqltxt text, rol text, esperado text, precond boolean, v_esperado text, c_esperada text);
insert into caso values
 ('C01','función inexistente','NEG',$$select arnes_stub.no_existe(gen_random_uuid(),'m','e')$$,null,'P0001:RESOLUTOR_NO_ELEGIBLE:R1',true,'BLOCKED','FUNCION_INEXISTENTE'),
 ('C02','firma incorrecta (1 argumento)','NEG',$$select arnes_stub.stub_dom('x')$$,null,'P0001:RESOLUTOR_NO_ELEGIBLE:R1',true,'BLOCKED','FUNCION_INEXISTENTE'),
 ('C03','tabla/dependencia inexistente dentro de la función','NEG',$$select arnes_stub.stub_tabla_falta(gen_random_uuid(),'m','e')$$,null,'P0001:RESOLUTOR_NO_ELEGIBLE:R1',true,'BLOCKED','ESTRUCTURA'),
 ('C04','permiso insuficiente (EXECUTE revocado)','NEG',$$select arnes_stub.stub_priv(gen_random_uuid(),'m','e')$$,'cci_arnes_noexec','P0001:RESOLUTOR_NO_ELEGIBLE:R1',true,'BLOCKED','PERMISOS'),
 ('C05','excepción inesperada (división por cero)','NEG',$$select arnes_stub.stub_div0(gen_random_uuid(),'m','e')$$,null,'P0001:RESOLUTOR_NO_ELEGIBLE:R1',true,'FAIL','ERROR_INESPERADO'),
 ('C06','rechazo válido de negocio con contrato coincidente','NEG',$$select arnes_stub.stub_dom(gen_random_uuid(),'m','e')$$,null,'P0001:RESOLUTOR_NO_ELEGIBLE:R1',true,'PASS','DOMINIO_CANDIDATO'),
 ('C07','rechazo de negocio con código distinto del esperado','NEG',$$select arnes_stub.stub_dom(gen_random_uuid(),'m','e')$$,null,'P0001:RESOLUTOR_NO_ELEGIBLE:R2',true,'FAIL','DOMINIO_CANDIDATO'),
 ('C08','rechazo observado sin contrato definido','NEG',$$select arnes_stub.stub_dom(gen_random_uuid(),'m','e')$$,null,'',true,'PARTIAL','DOMINIO_CANDIDATO'),
 ('C09','la regla no rechazó (la función tuvo éxito)','NEG',$$select arnes_stub.stub_ok_sin_fila(gen_random_uuid(),'m','e')$$,null,'P0001:RESOLUTOR_NO_ELEGIBLE:R1',true,'FAIL','OK'),
 ('C10','error de sintaxis','NEG',$$selec 1$$,null,'P0001:RESOLUTOR_NO_ELEGIBLE:R1',true,'BLOCKED','SINTAXIS'),
 ('C11','rechazo por CHECK 23514 con contrato 23514','NEG',$$select arnes_stub.stub_check(gen_random_uuid(),'m','e')$$,null,'23514',true,'PASS','DOMINIO_CANDIDATO'),
 ('C12','P0001 técnico (mensaje ajeno al contrato) NO es rechazo de la regla','NEG',$$select arnes_stub.stub_tecnico_p0001(gen_random_uuid(),'m','e')$$,null,'P0001:RESOLUTOR_NO_ELEGIBLE',true,'FAIL','DOMINIO_CANDIDATO'),
 ('C13','dependencia de tipo función inexistente dentro de la función','NEG',$$select arnes_stub.stub_dep_falta(gen_random_uuid(),'m','e')$$,null,'P0001:RESOLUTOR_NO_ELEGIBLE:R1',true,'BLOCKED','FUNCION_INEXISTENTE'),
 ('C14','control positivo: éxito','POS',$$select arnes_stub.stub_ok(gen_random_uuid(),'m','e')$$,null,'',true,'PASS','OK'),
 ('C15','control positivo: error inesperado','POS',$$select arnes_stub.stub_div0(gen_random_uuid(),'m','e')$$,null,'',true,'FAIL','ERROR_INESPERADO'),
 ('C16','precondición incumplida fuerza BLOCKED aunque el rechazo coincida','NEG',$$select arnes_stub.stub_dom(gen_random_uuid(),'m','e')$$,null,'P0001:RESOLUTOR_NO_ELEGIBLE:R1',false,'BLOCKED','DOMINIO_CANDIDATO'),
 ('C17','prueba de permisos: 42501 observado (contrato no definido por la especificación)','ERR_PERM',$$select arnes_stub.stub_priv(gen_random_uuid(),'m','e')$$,'cci_arnes_noexec','',true,'PARTIAL','PERMISOS'),
 ('C18','prueba de permisos: se esperaba denegación y la llamada tuvo éxito','ERR_PERM',$$select arnes_stub.stub_ok_sin_fila(gen_random_uuid(),'m','e')$$,null,'',true,'FAIL','OK');
create temp table obs as select c.id, c.descr, c.tipo, c.v_esperado, c.c_esperada, x.o_clase, x.o_sqlstate, pg_temp.veredicto(c.tipo, x.o_clase, x.o_sqlstate, x.o_msg, c.esperado, c.precond) as v_obtenido,
   (select count(*) from arnes_stub.res) as filas_tras_caso
  from caso c cross join lateral pg_temp.ejecuta(c.sqltxt, c.rol, null, null, true) x order by c.id;
\echo '=== PRUEBAS DEL ARNÉS (no de la lógica R1–R9) ==='
select id, descr, c_esperada as clase_esperada, o_clase as clase_obtenida, v_esperado, v_obtenido, case when v_esperado = v_obtenido and c_esperada = o_clase then 'PASS' else 'FAIL' end as resultado_arnes from obs, (select 1) z where true order by id;
-- AR-19 aislamiento: los casos que escriben (stub_ok) no dejan filas tras deshacer
select 'AR-19 sin residuos tras casos con escritura (deshacer=true)' as prueba, case when (select count(*) from arnes_stub.res) = 0 then 'PASS' else 'FAIL' end as resultado_arnes;
-- AR-20 el post-chequeo informa del efecto antes de deshacer
select 'AR-20 o_post informa el efecto antes de deshacer' as prueba, case when (select o_post from pg_temp.ejecuta($$select arnes_stub.stub_ok('00000000-0000-0000-0000-000000000001','m','e')$$, null, null, $$select (count(*)=1)::text from arnes_stub.res$$, true)) = 'true' and (select count(*) from arnes_stub.res) = 0 then 'PASS' else 'FAIL' end as resultado_arnes;
-- AR-21 reproducción del DEFECTO ORIGINAL (v1): criterio 'PASS si resultado distinto de OK' frente al veredicto corregido
\echo '=== DEFECTO v1 REPRODUCIDO: falsos PASS del criterio original (obtenido <> OK => PASS) en casos NEG ==='
select id, descr, o_clase, 'PASS' as veredicto_v1_defectuoso, v_obtenido as veredicto_v2 from obs where tipo = 'NEG' and o_clase <> 'OK' and v_obtenido <> 'PASS' order by id;
select 'AR-21 falsos PASS que la v1 habría dado: ' || count(*) as prueba, case when count(*) >= 6 then 'PASS (defecto reproducido y neutralizado)' else 'FAIL' end as resultado_arnes from obs where tipo = 'NEG' and o_clase <> 'OK' and v_obtenido <> 'PASS';
\echo '=== TOTAL ==='
with a as (select count(*) n, count(*) filter (where v_esperado = v_obtenido and c_esperada = o_clase) p from obs),
     b as (select (select count(*) = 0 from arnes_stub.res)::int as ar19,
                  ((select o_post from pg_temp.ejecuta($$select arnes_stub.stub_ok('00000000-0000-0000-0000-000000000001','m','e')$$, null, null, $$select (count(*)=1)::text from arnes_stub.res$$, true)) = 'true' and (select count(*) = 0 from arnes_stub.res))::int as ar20,
                  ((select count(*) from obs where tipo = 'NEG' and o_clase <> 'OK' and v_obtenido <> 'PASS') >= 6)::int as ar21)
select 'TOTAL pruebas_arnes=' || (a.n + 3) || ' PASS=' || (a.p + b.ar19 + b.ar20 + b.ar21) || ' FAIL=' || (a.n + 3 - a.p - b.ar19 - b.ar20 - b.ar21) as resumen from a, b;
