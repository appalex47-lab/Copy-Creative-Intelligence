#!/usr/bin/env python3
# Uso: python3 -I -B ct_pruebas_guarda_destino.py <socket> <puerto> <salida.txt>. PostgreSQL TEMPORAL LOCAL (superusuario cci_test); NUNCA Supabase/CCI-DEV/CCI-PROD.
# Pruebas negativas y positivas de la guarda de destino DEV/PROD (H-03) sobre LOS 6 SCRIPTS. Las listas allow/deny se inyectan SOLO en copias temporales del directorio
# (el archivo versionado queda con listas vacías). Cada caso exige el CÓDIGO de rechazo esperado Y que no se haya emitido ningún resultado de datos tras el rechazo.
import os, re, shutil, subprocess, sys, tempfile
SOCK, PORT, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
HERE = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.join(HERE, "cci_dev_NO_EJECUTADOS")
SEIS = ["01_inventario_esquema_SOLO_LECTURA", "02_rls_privilegios_SOLO_LECTURA", "03_pruebas_rls_ROLLBACK", "04_trigger_r1_r9_ROLLBACK", "05_concurrencia_sesion_A", "05_concurrencia_sesion_B"]
DEV = "-c cci.validacion_autorizada=SI-CCI-DEV -c cci.entorno=CCI-DEV"; LOC = "-c cci.validacion_autorizada=SI-LOCAL-TEMPORAL -c cci.entorno=LOCAL-TEMPORAL"
VARS = ["-v", "org=x", "-v", "org_a=x", "-v", "org_b=x", "-v", "uid_a=x", "-v", "uid_x=x", "-v", "piece=x", "-v", "attr=x"]
res = []; tmps = []
def psql(args, opts, user="cci_test", db="postgres", sql=None, cwd=None):
    env = dict(os.environ, PGHOST=SOCK, PGPORT=PORT, PGUSER=user, PGOPTIONS=opts)
    r = subprocess.run(["psql", "-d", db, "-X", "-v", "ON_ERROR_STOP=1", "-P", "pager=off"] + args, env=env, capture_output=True, text=True, cwd=cwd)
    return r.returncode, r.stdout + r.stderr
def adm(sql, db="postgres"): return psql(["-qAt", "-c", sql], "", db=db)
def anota(i, desc, ok, esperado, obtenido): res.append(("PASS" if ok else "FAIL", i, desc, esperado, obtenido))
def variante(allow=(), deny=(), sin_guarda=False):
    d = tempfile.mkdtemp(prefix="gd_"); tmps.append(d); t = os.path.join(d, "s"); shutil.copytree(SRC, t)
    g = os.path.join(t, "00_guarda_destino.sql")
    if sin_guarda: os.remove(g); return t
    s = open(g, encoding="utf-8").read()
    s = s.replace("array[]::text[];  -- @@DEV_ALLOW@@", "array[%s]::text[];  -- @@DEV_ALLOW@@" % ",".join("'%s'" % a for a in allow)).replace("array[]::text[];  -- @@PROD_DENY@@", "array[%s]::text[];  -- @@PROD_DENY@@" % ",".join("'%s'" % a for a in deny))
    open(g, "w", encoding="utf-8").write(s); return t
def corre(dirv, script, opts, **kw): return psql(VARS + ["-f", os.path.join(dirv, script + ".sql")], opts, **kw)
SIN_DATOS = lambda o: not re.search(r"^\s*(BEGIN|tabla\s*\||table_name\s*\||\(\d+ rows?\))", o, re.M)   # ninguna salida de datos tras el rechazo
def rechaza(i, desc, dirv, opts, codigo, scripts=SEIS, **kw):
    for sc in scripts:
        rc, o = corre(dirv, sc, opts, **kw)
        ok = rc != 0 and ("[%s]" % codigo) in o and re.search(r"ERROR:\s+NO EJECUTADO", o) and SIN_DATOS(o) and "GUARDA OK" not in o
        anota(i, "%s — %s" % (desc, sc[:2] + sc[-1] if sc.startswith("05") else sc[:2]), ok, "rechazo [%s], rc!=0, sin datos" % codigo, "rc=%d %s" % (rc, (re.search(r"\[G-[A-Z-]+\]", o) or re.search(r"(GUARDA OK|ERROR[^\n]{0,60})", o) or re.search(r"$", o)).group(0)))
sysid = adm("select system_identifier from pg_control_system()")[1].strip()
adm("drop database if exists cci_gdev"); adm("create database cci_gdev"); adm("drop database if exists cci_prod_simulada"); adm("create database cci_prod_simulada")
adm("drop role if exists sin_permiso"); adm("create role sin_permiso login"); adm("drop role if exists supabase_admin")
try:
    anota("GD-00", "precondición: identidad efectiva legible (system_identifier numérico)", sysid.isdigit(), "dígitos", "huella md5=%s" % __import__("hashlib").md5(sysid.encode()).hexdigest()[:8])
    # GD-01 DEV autorizado: permitido
    v = variante(allow=[sysid + "|cci_gdev"])
    for sc in SEIS:
        rc, o = corre(v, sc, DEV, db="cci_gdev")
        guarda_ok = "GUARDA OK modo=SI-CCI-DEV" in o and "NO EJECUTADO" not in o
        if sc.startswith(("01", "02")): ok = guarda_ok and rc == 0 and not re.search(r"(?i)\berror\b", o)
        else: ok = guarda_ok   # 03-05 necesitan fixtures; basta con que la guarda PERMITA (el resto de la ejecución se prueba en el smoke local)
        anota("GD-01", "DEV autorizado (allowlist 'sysid|base') PERMITIDO — " + sc[:2] + (sc[-1] if sc.startswith("05") else ""), ok, "GUARDA OK modo=SI-CCI-DEV" + (" y rc=0" if sc.startswith(("01", "02")) else ""), "rc=%d guarda_ok=%s" % (rc, guarda_ok))
    # GD-02 PROD rechazado aunque se declare DEV y aunque esté también en la allowlist (peor caso)
    v = variante(allow=[sysid + "|cci_gdev"], deny=[sysid]); rechaza("GD-02", "PROD en denylist + allowlist + variables DEV", v, DEV, "G-PROD-RECHAZADO", db="cci_gdev")
    rechaza("GD-02b", "PROD en denylist con variables LOCAL", v, LOC, "G-PROD-RECHAZADO", scripts=SEIS[:1], db="cci_gdev")
    # GD-03 base desconocida
    rechaza("GD-03a", "allowlist vacía versionada (estado real del repositorio) + DEV declarado", SRC, DEV, "G-DESTINO-DESCONOCIDO", db="cci_gdev")
    v = variante(allow=[sysid + "|otra_base"]); rechaza("GD-03b", "clúster conocido pero base no listada", v, DEV, "G-DESTINO-DESCONOCIDO", db="cci_gdev")
    v = variante(allow=["1234567890123456789|cci_gdev"]); rechaza("GD-03c", "base con el mismo nombre en OTRO clúster (otro system_identifier)", v, DEV, "G-DESTINO-DESCONOCIDO", db="cci_gdev")
    # GD-04 variables DEV contra una base PROD (base simulada marcada como PROD; allowlist con su nombre para aislar el efecto de la denylist)
    v = variante(allow=[sysid + "|cci_prod_simulada"], deny=[sysid]); rechaza("GD-04", "variables DEV contra base PROD simulada", v, DEV, "G-PROD-RECHAZADO", db="cci_prod_simulada")
    # GD-05 identidad no verificable (sin permiso sobre pg_control_system): fallo seguro
    adm("revoke execute on function pg_control_system() from public", db="cci_gdev")   # los privilegios de pg_proc son POR BASE: se revoca en la base de prueba
    try:
        v = variante(allow=[sysid + "|cci_gdev"]); rechaza("GD-05", "identidad no verificable (rol sin EXECUTE en pg_control_system)", v, DEV, "G-IDENTIDAD-NO-VERIFICABLE", user="sin_permiso", db="cci_gdev")
        rechaza("GD-05b", "identidad no verificable en modo local", v, LOC, "G-IDENTIDAD-NO-VERIFICABLE", scripts=SEIS[:1], user="sin_permiso", db="cci_gdev")
    finally: adm("grant execute on function pg_control_system() to public", db="cci_gdev")
    # GD-06 configuración incompleta o inválida
    v = variante(allow=[sysid + "|cci_gdev"])
    rechaza("GD-06a", "sin ninguna variable", v, "", "G-CONFIG-INCOMPLETA", db="cci_gdev")
    rechaza("GD-06b", "solo cci.validacion_autorizada", v, "-c cci.validacion_autorizada=SI-CCI-DEV", "G-CONFIG-INCOMPLETA", scripts=SEIS[:1], db="cci_gdev")
    rechaza("GD-06c", "solo cci.entorno", v, "-c cci.entorno=CCI-DEV", "G-CONFIG-INCOMPLETA", scripts=SEIS[:1], db="cci_gdev")
    rechaza("GD-06d", "par inválido (SI-CCI-DEV + LOCAL-TEMPORAL)", v, "-c cci.validacion_autorizada=SI-CCI-DEV -c cci.entorno=LOCAL-TEMPORAL", "G-CONFIG-INVALIDA", scripts=SEIS[:1], db="cci_gdev")
    rechaza("GD-06e", "valor desconocido (PROD) en cci.entorno", v, "-c cci.validacion_autorizada=SI-CCI-DEV -c cci.entorno=CCI-PROD", "G-CONFIG-INVALIDA", scripts=SEIS[:1], db="cci_gdev")
    # GD-07 configuración manipulada / identidad simulada
    rechaza("GD-07a", "operador intenta inyectar allowlist por PGOPTIONS (cci.dev_allow) con el archivo versionado", SRC, DEV + " -c cci.dev_allow=%s|cci_gdev -c cci.prod_deny=" % sysid, "G-DESTINO-DESCONOCIDO", scripts=SEIS[:1], db="cci_gdev")
    v = variante(allow=[sysid + "|cci_gdev"], deny=[sysid]); rechaza("GD-07b", "operador intenta vaciar la denylist por PGOPTIONS (cci.prod_deny=)", v, DEV + " -c cci.prod_deny=", "G-PROD-RECHAZADO", scripts=SEIS[:1], db="cci_gdev")
    adm("create or replace function public.pg_control_system(out system_identifier bigint) returns bigint language sql as 'select 1::bigint'", db="cci_gdev")
    v = variante(allow=["1|cci_gdev"], deny=[sysid])
    rechaza("GD-07c", "identidad simulada: función public.pg_control_system() suplantada con search_path=public,pg_catalog", v, DEV + " -c search_path=public,pg_catalog", "G-PROD-RECHAZADO", db="cci_gdev")
    adm("drop function public.pg_control_system()", db="cci_gdev")
    adm("create role supabase_admin nologin")
    try: rechaza("GD-07d", "identidad simulada: rol de plataforma supabase_admin presente en modo local", SRC, LOC, "G-LOCAL-ROLES-PLATAFORMA", db="cci_gdev")
    finally: adm("drop role supabase_admin")
    rechaza("GD-07e", "modo local contra base no cci_ (postgres)", SRC, LOC, "G-LOCAL-BASE", db="postgres")
    # GD-08 guarda ausente: el script no debe operar
    v = variante(sin_guarda=True)
    for sc in SEIS:
        rc, o = corre(v, sc, LOC, db="cci_gdev"); anota("GD-08", "archivo de guarda ausente: el script aborta sin ejecutar datos — " + sc[:2] + (sc[-1] if sc.startswith("05") else ""), rc != 0 and SIN_DATOS(o) and "GUARDA OK" not in o, "rc!=0 y sin datos", "rc=%d" % rc)
    # GD-13 (AUD-G1) guarda vacía / sólo comentario / truncada antes del bloque DO: NINGÚN script debe operar sin guarda (el marcador cci.guarda_ok no queda en '1')
    g_orig = open(os.path.join(SRC, "00_guarda_destino.sql"), encoding="utf-8").read()
    for nom, contenido in [("vacía (0 bytes)", ""), ("sólo comentario", "-- vacío\n"), ("truncada antes del DO", g_orig.split("do $guarda$")[0])]:
        v = variante(); open(os.path.join(v, "00_guarda_destino.sql"), "w", encoding="utf-8").write(contenido)
        rechaza("GD-13", "guarda " + nom + " con variables DEV/LOCAL: el script rechaza [G-GUARDA-NO-EJECUTADA]", v, LOC, "G-GUARDA-NO-EJECUTADA", db="cci_gdev")
    # GD-14 (AUD-G3) ejecución por stdin con una guarda homónima VACÍA en el directorio actual: ningún script debe operar sin guarda
    rogue = tempfile.mkdtemp(prefix="gd_rogue_"); tmps.append(rogue); open(os.path.join(rogue, "00_guarda_destino.sql"), "w", encoding="utf-8").write("-- rogue vacío\n")
    for sc in SEIS:
        env = dict(os.environ, PGHOST=SOCK, PGPORT=PORT, PGUSER="cci_test", PGOPTIONS=LOC)
        r = subprocess.run(["psql", "-d", "cci_gdev", "-X", "-v", "ON_ERROR_STOP=1", "-P", "pager=off"] + VARS, env=env, capture_output=True, text=True, cwd=rogue, stdin=open(os.path.join(SRC, sc + ".sql"), encoding="utf-8"))
        o = r.stdout + r.stderr
        anota("GD-14", "stdin con guarda homónima vacía en el cwd: sin datos y sin GUARDA OK — " + sc[:2] + (sc[-1] if sc.startswith("05") else ""), r.returncode != 0 and SIN_DATOS(o) and "GUARDA OK" not in o, "rc!=0 y sin datos", "rc=%d" % r.returncode)
    # GD-15 (AUD-FINAL-01) el search_path blindado de la guarda es LOCAL a su bloque DO: tras la guarda rige el search_path del llamador (por diseño: las políticas RLS y funciones bajo prueba se resuelven con él)
    for sc in SEIS:
        v = variante(); f = os.path.join(v, sc + ".sql"); t = open(f, encoding="utf-8").read(); k = "pg_temp.cci_guarda_ok') is null then raise exception"
        i = t.index(k); j = t.index("\n", i) + 1; open(f, "w", encoding="utf-8").write(t[:j] + "select 'SPVAL=' || pg_catalog.current_setting('search_path') as sp;\n" + t[j:])
        rc, o = corre(v, sc, LOC + " -c search_path=evil,public,pg_temp", db="cci_gdev")
        m = re.search(r"SPVAL=(\S+)", o)
        anota("GD-15", "CONSTANCIA: tras la guarda rige el search_path del llamador (no persiste el de la guarda) — " + sc[:2] + (sc[-1] if sc.startswith("05") else ""), bool(m) and m.group(1) == "evil,public,pg_temp", "SPVAL=evil,public,pg_temp (comportamiento documentado)", m.group(0) if m else "sin SPVAL")
    # GD-19 (AUD-FINAL-01) las instrucciones POSTERIORES a la guarda no se dejan secuestrar por funciones homónimas en un esquema anterior del search_path (las funciones del catálogo van calificadas con pg_catalog.)
    adm("create schema if not exists evil", db="cci_gdev")
    for sig, ret in [("current_setting(text)", "text"), ("current_setting(text, boolean)", "text"), ("to_regclass(text)", "regclass"), ("pg_get_userbyid(oid)", "name"), ("has_table_privilege(text, text, text)", "boolean"), ("count(*)", "bigint")]:
        pass
    adm("create function evil.current_setting(text) returns text language plpgsql as $f$ begin raise exception 'HIJACK-INVOCADO'; end $f$", db="cci_gdev")
    adm("create function evil.current_setting(text, boolean) returns text language plpgsql as $f$ begin raise exception 'HIJACK-INVOCADO'; end $f$", db="cci_gdev")
    adm("create function evil.to_regclass(text) returns regclass language plpgsql as $f$ begin raise exception 'HIJACK-INVOCADO'; end $f$", db="cci_gdev")
    adm("create function evil.pg_get_userbyid(oid) returns name language plpgsql as $f$ begin raise exception 'HIJACK-INVOCADO'; end $f$", db="cci_gdev")
    adm("create function evil.format(text, variadic \"any\") returns text language plpgsql as $f$ begin raise exception 'HIJACK-INVOCADO'; end $f$", db="cci_gdev")
    for sc in SEIS:
        rc, o = corre(SRC, sc, LOC + " -c search_path=evil,pg_catalog", db="cci_gdev")
        anota("GD-19", "funciones homónimas en 'evil' antes de pg_catalog en el search_path del llamador: NO se invocan tras la guarda — " + sc[:2] + (sc[-1] if sc.startswith("05") else ""), "GUARDA OK" in o and "HIJACK-INVOCADO" not in o, "GUARDA OK y sin HIJACK-INVOCADO", "guarda_ok=%s hijack=%s" % ("GUARDA OK" in o, "HIJACK-INVOCADO" in o))
    adm("drop schema if exists evil cascade", db="cci_gdev")
    # GD-16 (AUD-FINAL-02) marcador no preinstalable: guarda vacía + PGOPTIONS cci.guarda_ok=1 -> los 6 scripts rechazan
    v = variante(); open(os.path.join(v, "00_guarda_destino.sql"), "w", encoding="utf-8").write("")
    rechaza("GD-16", "guarda vacía con PGOPTIONS cci.guarda_ok=1 (intento de falsificar el marcador)", v, LOC + " -c cci.guarda_ok=1", "G-GUARDA-NO-EJECUTADA", db="cci_gdev")
    # GD-17 LÍMITE ESTRUCTURAL documentado: una guarda SUSTITUIDA que crea el marcador sí pasa (sólo el hash externo/envoltorio lo detecta)
    v = variante(); open(os.path.join(v, "00_guarda_destino.sql"), "w", encoding="utf-8").write("create temp table pg_temp.cci_guarda_ok (ok boolean);\n")
    rc, o = corre(v, SEIS[0], DEV, db="cci_gdev"); anota("GD-17", "LÍMITE ESTRUCTURAL: guarda sustituida por una que sólo crea el marcador PASA el script (sin hash externo no hay defensa)", rc == 0 and "G-" not in o, "el script corre (límite documentado, no es aprobación)", "rc=%d" % rc)
    # GD-18 envoltorio con verificación de hash (control técnico externo)
    W = os.path.join(HERE, "ejecutar_script_verificado.sh"); import hashlib
    h = hashlib.sha256(open(os.path.join(SRC, "00_guarda_destino.sql"), "rb").read()).hexdigest()
    def wrap(args, d=SRC, sc=SEIS[0]):
        env = dict(os.environ, PGHOST=SOCK, PGPORT=PORT, PGUSER="cci_test", PGOPTIONS=LOC)
        r = subprocess.run(["bash", W] + args(d, sc), env=env, capture_output=True, text=True, cwd="/tmp"); return r.returncode, r.stdout + r.stderr
    rc, o = wrap(lambda d, sc: [h, os.path.join(d, sc + ".sql"), "-d", "cci_gdev"]); anota("GD-18a", "envoltorio con hash aprobado correcto: ejecuta y la guarda aprueba", rc == 0 and "GUARDA OK" in o, "rc=0 y GUARDA OK", "rc=%d" % rc)
    rc, o = wrap(lambda d, sc: ["0" * 64, os.path.join(d, sc + ".sql"), "-d", "cci_gdev"]); anota("GD-18b", "envoltorio con hash distinto: NO ejecuta", rc != 0 and "V-GUARDA-HASH-DISTINTO" in o and "GUARDA OK" not in o, "rc!=0 V-GUARDA-HASH-DISTINTO", "rc=%d" % rc)
    v = variante(allow=["1|cci_gdev"]); rc, o = wrap(lambda d, sc: [h, os.path.join(d, sc + ".sql"), "-d", "cci_gdev"], d=v); anota("GD-18c", "envoltorio: allowlist alterada (guarda manipulada) con el hash aprobado original: NO ejecuta", rc != 0 and "V-GUARDA-HASH-DISTINTO" in o, "rc!=0 V-GUARDA-HASH-DISTINTO", "rc=%d" % rc)
    v = variante(); open(os.path.join(v, "00_guarda_destino.sql"), "w", encoding="utf-8").write("create temp table pg_temp.cci_guarda_ok (ok boolean);\n"); rc, o = wrap(lambda d, sc: [h, os.path.join(d, sc + ".sql"), "-d", "cci_gdev"], d=v); anota("GD-18d", "envoltorio: guarda sustituida (forja el marcador): NO ejecuta (el hash lo detecta)", rc != 0 and "V-GUARDA-HASH-DISTINTO" in o, "rc!=0", "rc=%d" % rc)
    v = variante(sin_guarda=True); rc, o = wrap(lambda d, sc: [h, os.path.join(d, sc + ".sql"), "-d", "cci_gdev"], d=v); anota("GD-18e", "envoltorio: guarda ausente: NO ejecuta", rc != 0 and "V-GUARDA-AUSENTE" in o, "rc!=0", "rc=%d" % rc)
    for sc in SEIS:
        rc, o = wrap(lambda d, sc: [h, os.path.join(d, sc + ".sql"), "-d", "cci_gdev", "-v", "org=x", "-v", "org_a=x", "-v", "org_b=x", "-v", "uid_a=x", "-v", "uid_x=x", "-v", "piece=x", "-v", "attr=x"], sc=sc); anota("GD-18f", "envoltorio con guarda correcta y destino local legítimo: la guarda aprueba — " + sc[:2] + (sc[-1] if sc.startswith("05") else ""), "GUARDA OK" in o, "GUARDA OK", "rc=%d" % rc)
    # GD-09 control positivo local (smoke): modo local legítimo sigue permitido
    rc, o = corre(SRC, SEIS[0], LOC, db="cci_gdev"); anota("GD-09", "modo local temporal legítimo (socket, base cci_, sin roles de plataforma) PERMITIDO", rc == 0 and "GUARDA OK modo=SI-LOCAL-TEMPORAL" in o, "rc=0 y GUARDA OK", "rc=%d" % rc)
    # GD-11/12 controles de la propia prueba (mutaciones): una guarda débil DEBE dejar pasar el ataque; si no, la prueba no detectaría nada
    g0 = open(os.path.join(SRC, "00_guarda_destino.sql"), encoding="utf-8").read()
    v = variante(allow=["1|cci_gdev"], deny=[sysid]); gg = os.path.join(v, "00_guarda_destino.sql"); s0 = open(gg, encoding="utf-8").read()
    s0 = re.sub(r"  perform pg_catalog\.set_config\([^\n]*\n", "", s0).replace("pg_catalog.pg_control_system()", "pg_control_system()"); open(gg, "w", encoding="utf-8").write(s0)   # la guarda débil conserva el marcador (lo crea el propio DO): se aísla sólo la debilidad que se quiere demostrar
    adm("create or replace function public.pg_control_system(out system_identifier bigint) returns bigint language sql as 'select 1::bigint'", db="cci_gdev")
    rc, o = corre(v, SEIS[0], DEV + " -c search_path=public,pg_catalog", db="cci_gdev"); adm("drop function public.pg_control_system()", db="cci_gdev")
    anota("GD-11", "control: guarda SIN anti-suplantación es burlada por función suplantada (la prueba GD-07c detecta esa debilidad)", rc == 0 and "GUARDA OK" in o, "guarda débil ACEPTA el destino PROD", "rc=%d" % rc)
    v = variante(allow=[], deny=[sysid]); gg = os.path.join(v, "00_guarda_destino.sql")
    viejo = ("do $$ declare a text := coalesce(current_setting('cci.validacion_autorizada', true),''); e text := coalesce(current_setting('cci.entorno', true),'');\nbegin\n  if a = 'SI-CCI-DEV' and e = 'CCI-DEV' then null;\n"
             "  elsif a = 'SI-LOCAL-TEMPORAL' and e = 'LOCAL-TEMPORAL' and current_database() ~ '^cci_' and inet_server_addr() is null then null;\n  else raise exception 'NO EJECUTADO'; end if; end $$;\n")
    open(gg, "w", encoding="utf-8").write(viejo + "create temp table pg_temp.cci_guarda_ok (ok boolean);\n")
    rc, o = corre(v, SEIS[0], DEV, db="cci_gdev"); anota("GD-12", "control: la guarda ANTERIOR (solo variables declaradas) acepta DEV sobre un clúster que está en la denylist (vulnerabilidad H-03 original)", rc == 0 and "NO EJECUTADO" not in o, "guarda anterior ACEPTA (vulnerable)", "rc=%d" % rc)
    # GD-10 el repositorio no contiene identificadores reales ni secretos en la guarda; listas versionadas vacías
    g = open(os.path.join(SRC, "00_guarda_destino.sql"), encoding="utf-8").read()
    anota("GD-10", "listas versionadas vacías (no se inventan identificadores de CCI-DEV/CCI-PROD)", "array[]::text[];  -- @@DEV_ALLOW@@" in g and "array[]::text[];  -- @@PROD_DENY@@" in g and not re.search(r"\b\d{15,}\b", g), "ambas vacías, sin números largos", "ok" if "array[]::text[];  -- @@DEV_ALLOW@@" in g else "listas modificadas")
finally:
    adm("drop role if exists supabase_admin")
    for d in tmps: shutil.rmtree(d, ignore_errors=True)
    adm("drop database if exists cci_gdev"); adm("drop database if exists cci_prod_simulada"); adm("drop role if exists sin_permiso")
fail = sum(r[0] == "FAIL" for r in res)
L = ["%s | %s | %s | esperado: %s | obtenido: %s" % r for r in res] + ["TOTAL=%d PASS=%d FAIL=%d" % (len(res), len(res) - fail, fail)]
print("\n".join(L)); open(OUT, "w", encoding="utf-8").write("\n".join(L) + "\n"); sys.exit(1 if fail else 0)
