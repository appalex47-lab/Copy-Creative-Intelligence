#!/usr/bin/env python3
# ct_ext02_validar_supabase_dev.py — SONDA DE SOLO LECTURA para validar CCI-DEV (EXT-02). NO se ha ejecutado contra Supabase: sólo contra un clúster local (resultado etiquetado SIMULADO_LOCAL).
# Quién la ejecuta: el propietario (o quien él autorice) con credenciales de CCI-DEV que ÉL entrega. Jamás con credenciales de CCI-PROD: la sonda exige --proyecto-esperado y que el host contenga esa referencia
# (o --local para el clúster de prueba) y que CCI_EXT02_CONFIRMA_DEV=SI-ES-CCI-DEV. Variables de conexión estándar de libpq (PGHOST, PGPORT, PGUSER, PGPASSWORD, PGDATABASE, PGSSLMODE) las aporta el operador; nada se escribe en disco.
# Qué mide (cada punto -> PASS/FAIL/BLOCKED con evidencia): E1 identidad (version, current_user, base, system_identifier vía pg_control_system), E2 capacidades (rolsuper/createrole/createdb/bypassrls), E3 TEMP (crear tabla temporal, insertar, borrar al terminar),
# E4 PGOPTIONS a través del pooler (¿llegan -c cci.* a la sesión?), E5 modo del pooler (¿la sesión persiste entre transacciones? ¿mismo pid?), E6 visibilidad de pg_stat_activity/pg_blocking_pids (necesaria para 05A/05B), E7 RLS visible, E8 la sonda NO escribe objetos persistentes.
# Salida: JSON en stdout. rc 0 sólo si todos PASS; 3 si alguno FAIL/BLOCKED; 2 uso incorrecto.
import json, os, re, subprocess, sys
a = sys.argv[1:]; local = "--local" in a; pe = a[a.index("--proyecto-esperado") + 1] if "--proyecto-esperado" in a else ""
if os.environ.get("CCI_EXT02_CONFIRMA_DEV") != "SI-ES-CCI-DEV": print(json.dumps({"veredicto": "RECHAZADO", "codigo": "X-SIN-CONFIRMACION", "detalle": "exporte CCI_EXT02_CONFIRMA_DEV=SI-ES-CCI-DEV sólo si las credenciales son de CCI-DEV"})); sys.exit(2)
host = os.environ.get("PGHOST", "")
if not local and (not pe or pe not in host): print(json.dumps({"veredicto": "RECHAZADO", "codigo": "X-PROYECTO-NO-COINCIDE", "detalle": "--proyecto-esperado debe ser la referencia del proyecto CCI-DEV y aparecer en PGHOST"})); sys.exit(2)
if re.search(r"prod", host, re.I) or re.search(r"prod", os.environ.get("PGDATABASE", ""), re.I): print(json.dumps({"veredicto": "RECHAZADO", "codigo": "X-PARECE-PROD", "detalle": "el host o la base contienen 'prod'"})); sys.exit(2)
def q(sql, opts=None, extra=()):
    e = dict(os.environ); 
    if opts: e["PGOPTIONS"] = opts
    r = subprocess.run(["psql", "-X", "-qAt", "-v", "ON_ERROR_STOP=1", *extra, "-c", sql], capture_output=True, text=True, env=e, timeout=60); return r.returncode, (r.stdout + r.stderr).strip()
R = []
def p(i, desc, estado, ev): R.append({"id": i, "descripcion": desc, "estado": estado, "evidencia": ev})
rc, o = q("select version()||' | '||current_user||' | '||current_database()"); p("E1a", "conexión, versión, usuario, base", "PASS" if rc == 0 else "FAIL", o[:200])
rc, o = q("select system_identifier from pg_control_system()"); p("E1b", "pg_control_system() accesible (system_identifier para la identidad firmada)", "PASS" if rc == 0 and o.isdigit() else "BLOCKED", o[:120])
rc, o = q("select rolsuper::int::text||rolcreaterole::int::text||rolcreatedb::int::text||rolbypassrls::int::text||rolreplication::int::text from pg_roles where rolname=current_user"); p("E2", "atributos del rol (super,createrole,createdb,bypassrls,replication) — informativo; el operador real debe ser 00000", "PASS" if rc == 0 else "FAIL", o)
rc, o = q("create temp table pg_temp.cci_sonda(x int); insert into pg_temp.cci_sonda values (1); select count(*) from pg_temp.cci_sonda"); p("E3", "TEMP: crear/insertar/leer tabla temporal (los scripts de marcador la necesitan)", "PASS" if rc == 0 and o.endswith("1") else "FAIL", o[:150])
rc, o = q("select current_setting('cci.entorno', true)", opts="-c cci.entorno=CCI-DEV -c cci.validacion_autorizada=SI-CCI-DEV"); p("E4", "PGOPTIONS a través de la ruta de conexión (¿llega cci.entorno?)", "PASS" if rc == 0 and o == "CCI-DEV" else "BLOCKED", "recibido=%r rc=%d" % (o[:80], rc))
rc, o = q("select pg_backend_pid(); select pg_backend_pid(); begin; set local application_name='cci_sonda'; select current_setting('application_name'); commit;"); pids = re.findall(r"^\d+$", o, re.M)
p("E5a", "pid del backend entre sentencias de una misma invocación (sesión estable)", "PASS" if len(pids) >= 2 and pids[0] == pids[1] else "BLOCKED", "pids=%s" % pids[:2])
rc, o = q("set cci.sonda='a'; select current_setting('cci.sonda', true);"); rc2, o2 = q("select current_setting('cci.sonda', true)"); p("E5b", "una GUC de sesión NO sobrevive entre conexiones distintas (aislamiento esperado)", "PASS" if rc == 0 and o2 in ("", "None") else "FAIL", "misma conexión=%r otra conexión=%r" % (o[-4:], o2))
rc, o = q("select count(*) from pg_stat_activity where pid=pg_backend_pid()"); rc2, o2 = q("select pg_blocking_pids(pg_backend_pid())"); p("E6", "pg_stat_activity y pg_blocking_pids legibles (observador independiente de 05A/05B)", "PASS" if rc == 0 and o == "1" and rc2 == 0 else "BLOCKED", "%s | %s" % (o, o2))
rc, o = q("select count(*) from pg_class where relrowsecurity"); p("E7", "RLS: catálogo legible (informativo)", "PASS" if rc == 0 else "FAIL", o)
rc, o = q("select count(*) from pg_class where relname='cci_sonda' and relpersistence<>'t'"); p("E8", "la sonda no deja objetos persistentes", "PASS" if rc == 0 and o == "0" else "FAIL", o)
ok = all(x["estado"] == "PASS" for x in R); print(json.dumps({"veredicto": "PASS" if ok else "BLOQUEADO_O_FALLO", "modo": "SIMULADO_LOCAL" if local else "REAL_CCI_DEV", "checks": R}, ensure_ascii=False, indent=1)); sys.exit(0 if ok else 3)
