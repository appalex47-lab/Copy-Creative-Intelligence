#!/usr/bin/env python3
# Uso: python3 -I -B ct_pruebas_guarda_destino.py <socket> <puerto> <salida.txt>. PostgreSQL TEMPORAL LOCAL (superusuario cci_test); NUNCA Supabase/CCI-DEV/CCI-PROD.
# Pruebas negativas y positivas de la guarda de destino DEV/PROD (H-03) sobre LOS 6 SCRIPTS. Las listas allow/deny se inyectan SOLO en copias temporales del directorio
# (el archivo versionado queda con listas vacías). Cada caso exige el CÓDIGO de rechazo esperado Y que no se haya emitido ningún resultado de datos tras el rechazo.
import hashlib, os, re, shutil, subprocess, sys, tempfile
SOCK, PORT, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
HERE = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.join(HERE, "cci_dev_NO_EJECUTADOS")
SEIS = ["01_inventario_esquema_SOLO_LECTURA", "02_rls_privilegios_SOLO_LECTURA", "03_pruebas_rls_ROLLBACK", "04_trigger_r1_r9_ROLLBACK", "05_concurrencia_sesion_A", "05_concurrencia_sesion_B"]
DEV = "-c cci.validacion_autorizada=SI-CCI-DEV -c cci.entorno=CCI-DEV"; LOC = "-c cci.validacion_autorizada=SI-LOCAL-TEMPORAL -c cci.entorno=LOCAL-TEMPORAL"
VARS = ["-v", "org=x", "-v", "org_a=x", "-v", "org_b=x", "-v", "uid_a=x", "-v", "uid_x=x", "-v", "piece=x", "-v", "attr=x"]
res = []; tmps = []
def psql(args, opts, user=None, db="postgres", sql=None, cwd=None, xenv=None):
    user = user or ("t_gd_op" if "cci.entorno=CCI-DEV" in opts else "cci_test")   # el modo DEV exige un operador autorizado (rol sin privilegios, miembro de cci_operador): fixture local
    env = dict(os.environ, PGHOST=SOCK, PGPORT=PORT, PGUSER=user, PGOPTIONS=opts)
    if xenv: env.update(xenv)
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
def h_guarda(d):
    f = os.path.join(d, "00_guarda_destino.sql"); return hashlib.sha256(open(f, "rb").read()).hexdigest() if os.path.exists(f) else ""
H_APROBADO = h_guarda(SRC)   # hash "aprobado" por el propietario para el archivo versionado (entregado FUERA del repo en producción)
def entorno(dirv, hash=None): return {"CCI_DIR": dirv, "CCI_GUARDA_SHA256_APROBADO": (hash if hash is not None else (h_guarda(dirv) or H_APROBADO))}
def sin_chequeo(v):
    g = os.path.join(v, "00_guarda_destino.sql"); s = re.sub(r"  -- @@SP_CHECK_INI@@.*?-- @@SP_CHECK_FIN@@\n", "", open(g, encoding="utf-8").read(), flags=re.S); open(g, "w", encoding="utf-8").write(s); return v
def corre(dirv, script, opts, hash=None, **kw): return psql(VARS + ["-f", os.path.join(dirv, script + ".sql")], opts, xenv=entorno(dirv, hash), **kw)
SIN_DATOS = lambda o: not re.search(r"^\s*(BEGIN|tabla\s*\||table_name\s*\||\(\d+ rows?\))", o, re.M)   # ninguna salida de datos tras el rechazo
def rechaza(i, desc, dirv, opts, codigo, scripts=SEIS, **kw):
    for sc in scripts:
        rc, o = corre(dirv, sc, opts, **kw)
        ok = rc != 0 and ("[%s]" % codigo) in o and re.search(r"ERROR:\s+NO EJECUTADO", o) and SIN_DATOS(o) and "GUARDA OK" not in o
        anota(i, "%s — %s" % (desc, sc[:2] + sc[-1] if sc.startswith("05") else sc[:2]), ok, "rechazo [%s], rc!=0, sin datos" % codigo, "rc=%d %s" % (rc, (re.search(r"\[G-[A-Z-]+\]", o) or re.search(r"(GUARDA OK|ERROR[^\n]{0,60})", o) or re.search(r"$", o)).group(0)))
sysid = adm("select system_identifier from pg_control_system()")[1].strip()
adm("drop database if exists cci_gdev"); adm("create database cci_gdev"); adm("drop database if exists cci_prod_simulada"); adm("create database cci_prod_simulada")
adm("drop role if exists t_gd_op"); adm("drop role if exists cci_operador"); adm("drop role if exists cci_custodio"); adm("drop role if exists cci_administrador"); adm("create role cci_operador nologin"); adm("create role cci_custodio nologin"); adm("create role cci_administrador nologin"); adm("create role t_gd_op login"); adm("grant cci_operador to t_gd_op")
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
    v = sin_chequeo(variante(allow=["1|cci_gdev"], deny=[sysid]))   # sin el chequeo de search_path: la calificación pg_catalog. por sí sola impide la suplantación (defensa en profundidad)
    rechaza("GD-07c", "identidad simulada: función public.pg_control_system() suplantada con search_path=public,pg_catalog (chequeo de search_path eliminado: sólo la calificación)", v, DEV + " -c search_path=public,pg_catalog", "G-PROD-RECHAZADO", db="cci_gdev")
    rechaza("GD-07c2", "la misma suplantación con la guarda íntegra: rechazada antes por [G-SEARCH-PATH-NO-SEGURO] (public precede a pg_catalog)", SRC, DEV + " -c search_path=public,pg_catalog", "G-SEARCH-PATH-NO-SEGURO", scripts=SEIS[:2], db="cci_gdev")
    adm("drop function public.pg_control_system()", db="cci_gdev")
    adm("create role supabase_admin nologin")
    try: rechaza("GD-07d", "identidad simulada: rol de plataforma supabase_admin presente en modo local", SRC, LOC, "G-LOCAL-ROLES-PLATAFORMA", db="cci_gdev")
    finally: adm("drop role supabase_admin")
    rechaza("GD-07e", "modo local contra base no cci_ (postgres)", SRC, LOC, "G-LOCAL-BASE", db="postgres")
    # GD-08 guarda ausente: el script no debe operar
    v = variante(sin_guarda=True)
    for sc in SEIS:
        rc, o = corre(v, sc, LOC, hash=H_APROBADO, db="cci_gdev"); anota("GD-08", "archivo de guarda ausente: el script aborta con [G-GUARDA-INTEGRIDAD] sin ejecutar datos — " + sc[:2] + (sc[-1] if sc.startswith("05") else ""), rc != 0 and "[G-GUARDA-INTEGRIDAD]" in o and SIN_DATOS(o) and "GUARDA OK" not in o, "rc!=0 [G-GUARDA-INTEGRIDAD] y sin datos", "rc=%d" % rc)
    # GD-13 (AUD-G1) guarda vacía / sólo comentario / truncada antes del bloque DO: NINGÚN script debe operar sin guarda (el marcador cci.guarda_ok no queda en '1')
    g_orig = open(os.path.join(SRC, "00_guarda_destino.sql"), encoding="utf-8").read()
    for nom, contenido in [("vacía (0 bytes)", ""), ("sólo comentario", "-- vacío\n"), ("truncada antes del DO", g_orig.split("do $guarda$")[0])]:
        v = variante(); open(os.path.join(v, "00_guarda_destino.sql"), "w", encoding="utf-8").write(contenido)
        rechaza("GD-13", "guarda " + nom + " con variables DEV/LOCAL: el script rechaza [G-GUARDA-NO-EJECUTADA]", v, LOC, "G-GUARDA-NO-EJECUTADA", db="cci_gdev")
    # GD-14 (AUD-G3) ejecución por stdin con una guarda homónima VACÍA en el directorio actual: ningún script debe operar sin guarda
    rogue = tempfile.mkdtemp(prefix="gd_rogue_"); tmps.append(rogue); open(os.path.join(rogue, "00_guarda_destino.sql"), "w", encoding="utf-8").write("-- rogue vacío\n")
    for sc in SEIS:
        env = dict(os.environ, PGHOST=SOCK, PGPORT=PORT, PGUSER="cci_test", PGOPTIONS=LOC, **entorno(SRC))
        r = subprocess.run(["psql", "-d", "cci_gdev", "-X", "-v", "ON_ERROR_STOP=1", "-P", "pager=off"] + VARS, env=env, capture_output=True, text=True, cwd=rogue, stdin=open(os.path.join(SRC, sc + ".sql"), encoding="utf-8"))
        o = r.stdout + r.stderr
        anota("GD-14", "stdin con guarda homónima vacía en el cwd: sin datos y sin GUARDA OK — " + sc[:2] + (sc[-1] if sc.startswith("05") else ""), r.returncode != 0 and SIN_DATOS(o) and "GUARDA OK" not in o, "rc!=0 y sin datos", "rc=%d" % r.returncode)
    # GD-15 (AUD-FINAL-01) el search_path blindado de la guarda es LOCAL a su bloque DO: tras la guarda rige el search_path del llamador (por diseño: las políticas RLS y funciones bajo prueba se resuelven con él)
    for sc in SEIS:
        v = variante(); f = os.path.join(v, sc + ".sql"); t = open(f, encoding="utf-8").read(); k = "\\ir 00_verificar_marcador.sql\n"
        i = t.index(k); j = i + len(k); open(f, "w", encoding="utf-8").write(t[:j] + "select 'SPVAL=' || pg_catalog.current_setting('search_path') as sp;\n" + t[j:])
        rc, o = corre(v, sc, LOC + " -c search_path=public,pg_temp", db="cci_gdev")
        m = re.search(r"SPVAL=(\S+)", o)
        anota("GD-15", "CONSTANCIA: tras la guarda rige el search_path del llamador (no persiste el de la guarda) — " + sc[:2] + (sc[-1] if sc.startswith("05") else ""), bool(m) and m.group(1) == "public,pg_temp", "SPVAL=public,pg_temp (comportamiento documentado)", m.group(0) if m else "sin SPVAL")
    # GD-19 (AUD-FINAL-01) las instrucciones POSTERIORES a la guarda no se dejan secuestrar por funciones homónimas en un esquema anterior del search_path (las funciones del catálogo van calificadas con pg_catalog.)
    adm("create schema if not exists evil", db="cci_gdev")
    for sig, ret in [("current_setting(text)", "text"), ("current_setting(text, boolean)", "text"), ("to_regclass(text)", "regclass"), ("pg_get_userbyid(oid)", "name"), ("has_table_privilege(text, text, text)", "boolean"), ("count(*)", "bigint")]:
        pass
    adm("create function evil.current_setting(text) returns text language plpgsql as $f$ begin raise exception 'HIJACK-INVOCADO'; end $f$", db="cci_gdev")
    adm("create function evil.current_setting(text, boolean) returns text language plpgsql as $f$ begin raise exception 'HIJACK-INVOCADO'; end $f$", db="cci_gdev")
    adm("create function evil.to_regclass(text) returns regclass language plpgsql as $f$ begin raise exception 'HIJACK-INVOCADO'; end $f$", db="cci_gdev")
    adm("create function evil.pg_get_userbyid(oid) returns name language plpgsql as $f$ begin raise exception 'HIJACK-INVOCADO'; end $f$", db="cci_gdev")
    adm("create function evil.format(text, variadic \"any\") returns text language plpgsql as $f$ begin raise exception 'HIJACK-INVOCADO'; end $f$", db="cci_gdev")
    rechaza("GD-19", "search_path hostil (evil antes de pg_catalog) con funciones homónimas: la guarda RECHAZA [G-SEARCH-PATH-NO-SEGURO] antes de que se ejecute nada del script", SRC, LOC + " -c search_path=evil,pg_catalog", "G-SEARCH-PATH-NO-SEGURO", db="cci_gdev")
    vsp = variante(); gsp = os.path.join(vsp, "00_guarda_destino.sql"); gtxt = re.sub(r"  -- @@SP_CHECK_INI@@.*?-- @@SP_CHECK_FIN@@\n", "", open(gsp, encoding="utf-8").read(), flags=re.S); open(gsp, "w", encoding="utf-8").write(gtxt)
    for sc in SEIS:
        rc, o = corre(vsp, sc, LOC + " -c search_path=evil,pg_catalog", db="cci_gdev")
        anota("GD-19b", "CONTROL DE DEFENSA EN PROFUNDIDAD: SIN el chequeo de search_path, las llamadas calificadas con pg_catalog. impiden por sí solas el secuestro por funciones homónimas — " + sc[:2] + (sc[-1] if sc.startswith("05") else ""), "GUARDA OK" in o and "HIJACK-INVOCADO" not in o, "GUARDA OK y sin HIJACK-INVOCADO", "guarda_ok=%s hijack=%s" % ("GUARDA OK" in o, "HIJACK-INVOCADO" in o))
    for etq, sp in [("esquema desconocido al final", "public,evil"), ("pg_temp primero y evil", "pg_temp,evil,pg_catalog"), ("entrada vacía y evil", "evil"), ("esquema con comillas", '"evil"')]:
        rechaza("GD-21", "search_path del llamador no permitido (" + etq + ")", SRC, LOC + " -c search_path=" + sp.replace('"', '\\"'), "G-SEARCH-PATH-NO-SEGURO", scripts=SEIS[:2], db="cci_gdev")
    for etq, sp in [("public antes que pg_catalog", "public,pg_catalog"), ("pg_temp antes que pg_catalog", "pg_temp,pg_catalog")]:
        rechaza("GD-21e", "search_path con orden inseguro (" + etq + ")", SRC, LOC + " -c search_path=" + sp, "G-SEARCH-PATH-NO-SEGURO", scripts=SEIS[:2], db="cci_gdev")
    for sp in ("pg_catalog,public,pg_temp", "pg_catalog,public", "public", "public,pg_temp"):
        for sc in SEIS[:2]:
            rc, o = corre(SRC, sc, LOC + " -c search_path=" + sp, db="cci_gdev"); anota("GD-21f", "search_path permitido '" + sp + "' NO se rechaza — " + sc[:2], rc == 0 and "GUARDA OK" in o, "GUARDA OK, rc=0", "rc=%d" % rc)
    adm("alter role cci_test in database cci_gdev set search_path = evil, public", db="cci_gdev")
    try: rechaza("GD-21b", "search_path fijado por ALTER ROLE ... IN DATABASE ... SET (no por PGOPTIONS)", SRC, LOC, "G-SEARCH-PATH-NO-SEGURO", scripts=SEIS[:2], db="cci_gdev")
    finally: adm("alter role cci_test in database cci_gdev reset search_path", db="cci_gdev")
    adm("alter database cci_gdev set search_path = evil, public", db="cci_gdev")
    try: rechaza("GD-21c", "search_path fijado por ALTER DATABASE ... SET", SRC, LOC, "G-SEARCH-PATH-NO-SEGURO", scripts=SEIS[:2], db="cci_gdev")
    finally: adm("alter database cci_gdev reset search_path", db="cci_gdev")
    adm("create schema cci_test", db="cci_gdev")
    try: rechaza("GD-21d", "'$user' apunta a un esquema existente con el nombre del rol (esquema controlable por el rol)", SRC, LOC + ' -c search_path=\\"$user\\",public', "G-SEARCH-PATH-NO-SEGURO", scripts=SEIS[:2], db="cci_gdev")
    finally: adm("drop schema cci_test", db="cci_gdev")
    adm("drop schema if exists evil cascade", db="cci_gdev")
    # GD-16 (AUD-FINAL-02) marcador no preinstalable: guarda vacía + PGOPTIONS cci.guarda_ok=1 -> los 6 scripts rechazan
    v = variante(); open(os.path.join(v, "00_guarda_destino.sql"), "w", encoding="utf-8").write("")
    rechaza("GD-16", "guarda vacía con PGOPTIONS cci.guarda_ok=1 (intento de falsificar el marcador)", v, LOC + " -c cci.guarda_ok=1", "G-GUARDA-NO-EJECUTADA", db="cci_gdev")
    # GD-17 LÍMITE ESTRUCTURAL documentado: una guarda SUSTITUIDA por otra que genera el marcador de ESTA ejecución sin comprobar nada pasa si quien la sustituye también
    # controla el hash "aprobado" (no hay raíz de confianza externa). Con el hash aprobado REAL (externo) la misma sustitución se rechaza (GD-17b).
    cola = g_orig[g_orig.index("-- MARCADOR POR EJECUCIÓN"):]
    v = variante(); open(os.path.join(v, "00_guarda_destino.sql"), "w", encoding="utf-8").write(cola)
    rc, o = corre(v, SEIS[0], DEV, db="cci_gdev"); anota("GD-17", "LÍMITE ESTRUCTURAL: guarda sustituida (sólo marcador) + hash 'aprobado' controlado por el mismo actor PASA (sin custodio externo no hay defensa)", rc == 0 and "G-" not in o, "el script corre (límite documentado, no es aprobación)", "rc=%d" % rc)
    rc, o = corre(v, SEIS[0], DEV, hash=H_APROBADO, db="cci_gdev"); anota("GD-17b", "la misma guarda sustituida con el hash aprobado REAL (externo): RECHAZADA [G-GUARDA-INTEGRIDAD]", rc != 0 and "[G-GUARDA-INTEGRIDAD]" in o and "GUARDA OK" not in o, "rc!=0 [G-GUARDA-INTEGRIDAD]", "rc=%d" % rc)
    # GD-20 ejecución directa sin hash externo / sin CCI_DIR / hash mal formado / hash de otro archivo: fallo cerrado
    for etq, x in [("sin CCI_GUARDA_SHA256_APROBADO", {"CCI_DIR": SRC, "CCI_GUARDA_SHA256_APROBADO": ""}), ("sin CCI_DIR", {"CCI_DIR": "", "CCI_GUARDA_SHA256_APROBADO": H_APROBADO}), ("hash de otro contenido", {"CCI_DIR": SRC, "CCI_GUARDA_SHA256_APROBADO": hashlib.sha256(b"otro").hexdigest()}), ("hash en mayúsculas", {"CCI_DIR": SRC, "CCI_GUARDA_SHA256_APROBADO": H_APROBADO.upper()})]:
        for sc in SEIS:
            rc, o = psql(VARS + ["-f", os.path.join(SRC, sc + ".sql")], LOC, db="cci_gdev", xenv=x)
            anota("GD-20", "ejecución directa " + etq + ": rechazo [G-GUARDA-INTEGRIDAD] — " + sc[:2] + (sc[-1] if sc.startswith("05") else ""), rc != 0 and "[G-GUARDA-INTEGRIDAD]" in o and SIN_DATOS(o) and "GUARDA OK" not in o, "rc!=0 [G-GUARDA-INTEGRIDAD]", "rc=%d" % rc)
    # GD-09 control positivo local (smoke): modo local legítimo sigue permitido
    rc, o = corre(SRC, SEIS[0], LOC, db="cci_gdev"); anota("GD-09", "modo local temporal legítimo (socket, base cci_, sin roles de plataforma) PERMITIDO", rc == 0 and "GUARDA OK modo=SI-LOCAL-TEMPORAL" in o, "rc=0 y GUARDA OK", "rc=%d" % rc)
    # GD-11/12 controles de la propia prueba (mutaciones): una guarda débil DEBE dejar pasar el ataque; si no, la prueba no detectaría nada
    g0 = open(os.path.join(SRC, "00_guarda_destino.sql"), encoding="utf-8").read()
    v = sin_chequeo(variante(allow=["1|cci_gdev"], deny=[sysid])); gg = os.path.join(v, "00_guarda_destino.sql"); s0 = open(gg, encoding="utf-8").read()
    s0 = re.sub(r"  perform pg_catalog\.set_config\([^\n]*\n", "", s0).replace("pg_catalog.pg_control_system()", "pg_control_system()"); open(gg, "w", encoding="utf-8").write(s0)   # la guarda débil conserva el marcador (lo crea el propio DO): se aísla sólo la debilidad que se quiere demostrar
    adm("create or replace function public.pg_control_system(out system_identifier bigint) returns bigint language sql as 'select 1::bigint'", db="cci_gdev")
    rc, o = corre(v, SEIS[0], DEV + " -c search_path=public,pg_catalog", db="cci_gdev"); adm("drop function public.pg_control_system()", db="cci_gdev")
    anota("GD-11", "control: guarda SIN anti-suplantación es burlada por función suplantada (la prueba GD-07c detecta esa debilidad)", rc == 0 and "GUARDA OK" in o, "guarda débil ACEPTA el destino PROD", "rc=%d" % rc)
    v = variante(allow=[], deny=[sysid]); gg = os.path.join(v, "00_guarda_destino.sql")
    viejo = ("do $$ declare a text := coalesce(current_setting('cci.validacion_autorizada', true),''); e text := coalesce(current_setting('cci.entorno', true),'');\nbegin\n  if a = 'SI-CCI-DEV' and e = 'CCI-DEV' then null;\n"
             "  elsif a = 'SI-LOCAL-TEMPORAL' and e = 'LOCAL-TEMPORAL' and current_database() ~ '^cci_' and inet_server_addr() is null then null;\n  else raise exception 'NO EJECUTADO'; end if; end $$;\n")
    open(gg, "w", encoding="utf-8").write(viejo + g0[g0.index("-- MARCADOR POR EJECUCIÓN"):])
    rc, o = corre(v, SEIS[0], DEV, db="cci_gdev"); anota("GD-12", "control: la guarda ANTERIOR (solo variables declaradas) acepta DEV sobre un clúster que está en la denylist (vulnerabilidad H-03 original)", rc == 0 and "NO EJECUTADO" not in o, "guarda anterior ACEPTA (vulnerable)", "rc=%d" % rc)
    # GD-10 el repositorio no contiene identificadores reales ni secretos en la guarda; listas versionadas vacías
    g = open(os.path.join(SRC, "00_guarda_destino.sql"), encoding="utf-8").read()
    anota("GD-10", "listas versionadas vacías (no se inventan identificadores de CCI-DEV/CCI-PROD)", "array[]::text[];  -- @@DEV_ALLOW@@" in g and "array[]::text[];  -- @@PROD_DENY@@" in g and not re.search(r"\b\d{15,}\b", g), "ambas vacías, sin números largos", "ok" if "array[]::text[];  -- @@DEV_ALLOW@@" in g else "listas modificadas")
finally:
    adm("drop role if exists supabase_admin")
    for d in tmps: shutil.rmtree(d, ignore_errors=True)
    adm("drop database if exists cci_gdev"); adm("drop database if exists cci_prod_simulada"); adm("drop role if exists sin_permiso"); adm("drop role if exists t_gd_op"); adm("drop role if exists cci_operador"); adm("drop role if exists cci_custodio"); adm("drop role if exists cci_administrador")
fail = sum(r[0] == "FAIL" for r in res)
L = ["%s | %s | %s | esperado: %s | obtenido: %s" % r for r in res] + ["TOTAL=%d PASS=%d FAIL=%d" % (len(res), len(res) - fail, fail)]
print("\n".join(L)); open(OUT, "w", encoding="utf-8").write("\n".join(L) + "\n"); sys.exit(1 if fail else 0)
