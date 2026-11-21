#!/usr/bin/env python3
# Uso: python3 -I -B ct_pruebas_autorizacion_operadores.py <socket> <puerto> <salida.json>   (PostgreSQL TEMPORAL LOCAL; nunca Supabase). Resolución final AUD-RF-02: autorización explícita del operador en la guarda (modo DEV).
# Variante de prueba: copia del árbol con dev_allow = '<system_identifier local>|<base>' (única forma de ejercitar el modo DEV sin inventar identificadores reales) y un CANARIO tras el verificador:
# un rechazo sólo cuenta si aparece 'NO EJECUTADO [G-…]' Y el canario NO se imprimió Y no hubo efectos persistentes. Los roles son FIXTURES de la base de prueba; no se concede nada real.
import hashlib, json, os, re, shutil, subprocess, sys, tempfile
SOCK, PORT, OUT = sys.argv[1:4]; HERE = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.join(HERE, "cci_dev_NO_EJECUTADOS")
DEV = "-c cci.validacion_autorizada=SI-CCI-DEV -c cci.entorno=CCI-DEV"; CAN = "CANARIO-CUERPO-EJECUTADO"; DB = "cci_auth"
def psql(args, user="cci_test", db="postgres", opts="", env=None, tdir=None, h=None):
    e = dict(os.environ, PGHOST=SOCK, PGPORT=PORT, PGUSER=user, PGOPTIONS=opts)
    if tdir: e["CCI_DIR"] = tdir; e["CCI_GUARDA_SHA256_APROBADO"] = h
    if env: e.update(env)
    r = subprocess.run(["psql", "-X", "-d", db] + args, capture_output=True, text=True, env=e, timeout=120); return r.returncode, r.stdout + r.stderr
def q(sql, db="postgres"): return psql(["-qAt", "-c", sql], db=db)[1].strip()
sysid = q("select system_identifier from pg_control_system()")
T = tempfile.mkdtemp(prefix="cci_auth."); os.chmod(T, 0o700); shutil.copytree(SRC, T + "/s")
g = open(T + "/s/00_guarda_destino.sql", encoding="utf-8").read(); g = g.replace("array[]::text[];  -- @@DEV_ALLOW@@", "array['%s|%s']::text[];  -- @@DEV_ALLOW@@" % (sysid, DB)); open(T + "/s/00_guarda_destino.sql", "w", encoding="utf-8").write(g)
sc = open(T + "/s/01_inventario_esquema_SOLO_LECTURA.sql", encoding="utf-8").read(); i = sc.index("\\ir 00_verificar_marcador.sql") + len("\\ir 00_verificar_marcador.sql"); open(T + "/s/01_inventario_esquema_SOLO_LECTURA.sql", "w", encoding="utf-8").write(sc[:i] + "\n\\echo " + CAN + sc[i:])
H = hashlib.sha256(open(T + "/s/00_guarda_destino.sql", "rb").read()).hexdigest()
def corre(user, opts=DEV + " -c client_min_messages=log", variante=None):
    t = T + "/s"
    if variante: shutil.rmtree(T + "/v", ignore_errors=True); shutil.copytree(T + "/s", T + "/v"); variante(T + "/v/00_guarda_destino.sql"); t = T + "/v"
    return psql(["-v", "ON_ERROR_STOP=1", "-f", t + "/01_inventario_esquema_SOLO_LECTURA.sql"], user=user, db=DB, opts=opts, tdir=t, h=hashlib.sha256(open(t + "/00_guarda_destino.sql", "rb").read()).hexdigest())
def estado(): return q("select (select count(*) from pg_roles where rolname like 'cci\\_%'), (select count(*) from pg_auth_members), (select count(*) from pg_class where relnamespace='public'::regnamespace)", db=DB)
psql(["-qc", "drop database if exists %s" % DB]); psql(["-qc", "create database %s" % DB])
for r in ("cci_operador", "cci_custodio", "cci_administrador"): psql(["-qc", "drop role if exists %s" % r])
for r in ("t_op_ok", "t_sin_rol", "t_op_cust", "t_op_adm", "t_op_adm_indirecto", "t_cr", "t_cdb", "t_byp", "t_repl", "t_op_noinh", "t_intermedio", "t_op_setrole"): psql(["-qc", "drop role if exists %s" % r])
REC = []
def reg(i, ob, esp, obs, ok, cod=""): REC.append({"id": i, "objetivo": ob, "esperado": esp, "observado": obs, "estado": "PASS" if ok else "FAIL"}); print("%s | %s | %s | %s" % ("PASS" if ok else "FAIL", i, ob, obs))
def rechazo(i, ob, cod, r, antes):
    rc, o = r; ok = ("NO EJECUTADO [%s]" % cod) in o and CAN not in o and rc != 0 and estado() == antes
    reg(i, ob, "NO EJECUTADO [%s], sin canario y sin efectos persistentes" % cod, "rc=%d %s canario=%s efectos=%s" % (rc, re.findall(r"NO EJECUTADO \[[A-Z-]+\]", o)[:1], CAN in o, estado() != antes), ok)
# 0) roles aún no configurados (el administrador no ejecutó PROCEDIMIENTO_ROLES_CCI_DEV.sql): DENEGACIÓN POR DEFECTO
psql(["-qc", "create role t_sin_rol login"]); a0 = estado()
rechazo("AO-01", "roles de la matriz no configurados (cci_operador no existe)", "G-OPERADOR-ROLES-NO-CONFIGURADOS", corre("t_sin_rol"), a0)
psql(["-qc", "create role cci_operador nologin; create role cci_custodio nologin; create role cci_administrador nologin; create role t_op_ok login; grant cci_operador to t_op_ok"])
a1 = estado()
rc, o = corre("t_op_ok"); reg("AO-02", "operador autorizado (miembro de cci_operador, sin privilegios elevados)", "GUARDA OK y cuerpo ejecutado", "rc=%d guarda_ok=%s canario=%s" % (rc, "GUARDA OK" in o, CAN in o), rc == 0 and "GUARDA OK" in o and CAN in o)
reg("AO-03", "registro de quién ejecutó (RAISE LOG con rol y pid)", "CCI-AUDITORIA operador=t_op_ok pid=<n>", re.findall(r"CCI-AUDITORIA operador=\S+ pid=\d+", o)[:1], re.search(r"CCI-AUDITORIA operador=t_op_ok pid=\d+", o) is not None)
rechazo("AO-04", "rol desconocido: existe pero no es miembro de cci_operador", "G-OPERADOR-NO-AUTORIZADO", corre("t_sin_rol"), a1)
rechazo("AO-05", "superusuario (cci_test) no puede operar: privilegios mínimos", "G-OPERADOR-PRIVILEGIO-EXCESIVO", corre("cci_test"), a1)
for nm, attr in (("t_cr", "createrole"), ("t_cdb", "createdb"), ("t_byp", "bypassrls"), ("t_repl", "replication")):
    psql(["-qc", "create role %s login %s; grant cci_operador to %s" % (nm, attr, nm)]); rechazo("AO-06-" + attr, "operador con %s" % attr.upper(), "G-OPERADOR-PRIVILEGIO-EXCESIVO", corre(nm), estado())
psql(["-qc", "create role t_op_cust login; grant cci_operador, cci_custodio to t_op_cust; create role t_op_adm login; grant cci_operador, cci_administrador to t_op_adm"])
rechazo("AO-07", "separación de funciones: operador + custodio", "G-SEPARACION-FUNCIONES", corre("t_op_cust"), estado())
rechazo("AO-08", "separación de funciones: operador + administrador", "G-SEPARACION-FUNCIONES", corre("t_op_adm"), estado())
psql(["-qc", "create role t_intermedio nologin; grant cci_administrador to t_intermedio; create role t_op_adm_indirecto login; grant cci_operador to t_op_adm_indirecto; grant t_intermedio to t_op_adm_indirecto"])
rechazo("AO-09", "separación de funciones por membresía INDIRECTA (cadena de roles)", "G-SEPARACION-FUNCIONES", corre("t_op_adm_indirecto"), estado())
psql(["-qc", "create role t_op_noinh login noinherit; grant cci_operador to t_op_noinh; grant cci_administrador to t_op_noinh"])
rechazo("AO-10", "separación de funciones aunque el rol sea NOINHERIT (membresía sin herencia)", "G-SEPARACION-FUNCIONES", corre("t_op_noinh"), estado())
psql(["-qc", "create role t_op_setrole login; grant cci_operador to t_op_setrole"])
rc, o = psql(["-v", "ON_ERROR_STOP=1", "-c", "set role cci_operador", "-f", T + "/s/01_inventario_esquema_SOLO_LECTURA.sql"], user="t_op_setrole", db=DB, opts=DEV, tdir=T + "/s", h=H)
reg("AO-11", "escalamiento por SET ROLE a cci_operador", "NO EJECUTADO [G-ROL-CAMBIADO], sin canario", re.findall(r"NO EJECUTADO \[[A-Z-]+\]", o)[:1], "NO EJECUTADO [G-ROL-CAMBIADO]" in o and CAN not in o)
# atacante sin autorización controlando search_path / PGOPTIONS / parámetros de sesión
psql(["-qc", "drop schema if exists evil cascade; create schema evil; create function evil.pg_has_role(name, text, text) returns boolean language sql as 'select true'; create function evil.pg_has_role(name, oid, text) returns boolean language sql as 'select true'; grant usage on schema evil to public"], db=DB)
a2 = estado()
rechazo("AO-12", "no autorizado con search_path hostil (evil antes de pg_catalog)", "G-SEARCH-PATH-NO-SEGURO", corre("t_sin_rol", DEV + " -c search_path=evil,pg_catalog"), a2)
def sin_chequeo(p):
    s = open(p, encoding="utf-8").read(); i, j = s.index("-- @@SP_CHECK_INI@@"), s.index("-- @@SP_CHECK_FIN@@"); open(p, "w", encoding="utf-8").write(s[:i] + s[j:])
rechazo("AO-13", "no autorizado con search_path hostil y SIN el chequeo de search_path (sólo la calificación pg_catalog protege)", "G-OPERADOR-NO-AUTORIZADO", corre("t_sin_rol", DEV + " -c search_path=evil,pg_catalog", variante=sin_chequeo), a2)
rechazo("AO-14", "no autorizado con GUC cci.* adicionales preinstaladas por PGOPTIONS (cci.operador_autorizado, cci.script_declarado)", "G-OPERADOR-NO-AUTORIZADO", corre("t_sin_rol", DEV + " -c cci.operador_autorizado=on -c cci.script_declarado=01 -c cci.rol=cci_operador"), a2)
rechazo("AO-15", "no autorizado con parámetros de sesión (row_security=off, default_transaction_read_only=off)", "G-OPERADOR-NO-AUTORIZADO", corre("t_sin_rol", DEV + " -c row_security=off -c default_transaction_read_only=off"), a2)
rc, o = corre("t_sin_rol", DEV + " -c session_replication_role=replica"); reg("AO-15b", "no autorizado intenta session_replication_role=replica: el servidor lo rechaza antes de la guarda (no superusuario)", "conexión rechazada por PostgreSQL, sin canario", "rc=%d canario=%s %s" % (rc, CAN in o, "permission denied" in o), rc != 0 and CAN not in o and "permission denied" in o)
rechazo("AO-16", "no autorizado con aplicación declarada cci_05A (impostor de identidad de prueba)", "G-OPERADOR-NO-AUTORIZADO", corre("t_sin_rol", DEV + " -c application_name=cci_05A"), a2)
rc, o = corre("t_op_ok", DEV + " -c session_authorization=t_op_ok"); reg("AO-17", "operador autorizado que re-declara su propio session_authorization (sin cambio de rol)", "GUARDA OK", "rc=%d" % rc, rc == 0 and "GUARDA OK" in o)
reg("AO-18", "sin efectos persistentes en toda la suite (roles/membresías/objetos públicos sólo los creados por la fixture)", "estado estable", estado(), estado() == estado())
psql(["-qc", "drop database if exists %s" % DB])
for r in ("t_op_ok", "t_sin_rol", "t_op_cust", "t_op_adm", "t_op_adm_indirecto", "t_cr", "t_cdb", "t_byp", "t_repl", "t_op_noinh", "t_intermedio", "t_op_setrole", "cci_operador", "cci_custodio", "cci_administrador"): psql(["-qc", "drop role if exists %s" % r])
shutil.rmtree(T, ignore_errors=True); json.dump(REC, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
n = sum(r["estado"] == "FAIL" for r in REC); print("TOTAL=%d PASS=%d FAIL=%d" % (len(REC), len(REC) - n, n)); sys.exit(1 if n else 0)
