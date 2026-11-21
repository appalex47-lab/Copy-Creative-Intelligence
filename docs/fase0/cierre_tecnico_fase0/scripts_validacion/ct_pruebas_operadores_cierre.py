#!/usr/bin/env python3
# Uso: python3 -I -B ct_pruebas_operadores_cierre.py <socket> <puerto> <salida.json>   (PostgreSQL TEMPORAL LOCAL; nunca Supabase)
# Auditoría adversarial de OPERADORES y PRIVILEGIOS EFECTIVOS (operación de cierre AUD-OP-01). Escenarios A–J + privilegios P.
# Cada ataque se ejecuta contra DOS árboles: VULN (guarda SIN los controles nuevos = guarda del commit 404f5adc; CONTROL POSITIVO: el ataque debe funcionar) y NEW (guarda actual; CONTROL NEGATIVO: debe bloquearlo).
# Un ataque "ejecutado" = el operador hostil se invocó de verdad (HIJACK-OP en la salida del servidor) o su efecto lateral se observó; "bloqueado" = rechazo NO EJECUTADO [G-…] antes de cualquier instrucción del script.
# No se declara PASS por la mera existencia del objeto malicioso ni porque el script terminara sin error. Los roles son FIXTURES locales; no se concede nada real.
import hashlib, json, os, re, shutil, subprocess, sys, tempfile, threading, time
SOCK, PORT, OUT = sys.argv[1:4]; HERE = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.join(HERE, "cci_dev_NO_EJECUTADOS")
LOC = "-c cci.validacion_autorizada=SI-LOCAL-TEMPORAL -c cci.entorno=LOCAL-TEMPORAL"; DEV = "-c cci.validacion_autorizada=SI-CCI-DEV -c cci.entorno=CCI-DEV"
U = "00000000-0000-0000-0000-0000000000"
TMP = tempfile.mkdtemp(prefix="cci_opc.")
SEIS = ["01_inventario_esquema_SOLO_LECTURA", "02_rls_privilegios_SOLO_LECTURA", "03_pruebas_rls_ROLLBACK", "04_trigger_r1_r9_ROLLBACK", "05_concurrencia_sesion_A", "05_concurrencia_sesion_B"]
def sh(a, db="postgres", user="cci_test", opts="", env=None, timeout=180):
    e = dict(os.environ, PGHOST=SOCK, PGPORT=PORT, PGUSER=user, PGOPTIONS=opts); e.update(env or {})
    r = subprocess.run(["psql", "-X", "-d", db] + a, env=e, capture_output=True, text=True, timeout=timeout); return r.returncode, r.stdout + r.stderr
def scr(sql):
    fd, pth = tempfile.mkstemp(suffix=".sql", dir=TMP); os.write(fd, (sql + "\n").encode()); os.close(fd); return pth
def q(sql, db="postgres"): return sh(["-qAt", "-v", "ON_ERROR_STOP=1", "-c", sql], db=db)
def qs(sql, db="postgres"): return q(sql, db)[1].strip()
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
# ---- árboles
def region(s, name): return re.sub(r"^[ ]*-- @@%s_INI@@.*?^[ ]*-- @@%s_FIN@@\n" % (name, name), "", s, flags=re.S | re.M)
def arbol(nombre, f):
    d = os.path.join(TMP, nombre); shutil.copytree(SRC, d); g = os.path.join(d, "00_guarda_destino.sql"); s = open(g, encoding="utf-8").read(); s = f(s); open(g, "w", encoding="utf-8").write(s); return d
sysid = qs("select system_identifier from pg_control_system()")
def vuln(s):  # = guarda del commit 404f5adc (sin los controles de operadores ni de privilegios efectivos)
    s = region(region(s, "OP_CHECK"), "PRIV_CHECK"); s = s.replace("  nfo int; nrc int; roles_c int;\n", "")
    return "\n".join(l for l in s.split("\n") if not l.startswith("--   G-OPERADOR-CREATE-EN-PUBLIC /") and not l.startswith("--   G-OPERADOR-AJENO-EN-SEARCH-PATH /"))
def nopin(s):  # sin ningún blindaje de search_path (ni chequeo ni pin de sesión): configuración totalmente vulnerable
    s = vuln(s); s = region(s, "SP_CHECK"); return re.sub(r"-- BLINDAJE DE SESIÓN.*?\\gset\n", "", s, flags=re.S)
def devallow(s, db): return s.replace("array[]::text[];  -- @@DEV_ALLOW@@", "array['%s|%s']::text[];  -- @@DEV_ALLOW@@" % (sysid, db))
T_NEW = arbol("new", lambda s: s); T_VULN = arbol("vuln", vuln); T_NOPIN = arbol("nopin", nopin)
DB_DEV = "cci_opc_dev"
T_NEWD = arbol("newd", lambda s: devallow(s, DB_DEV)); T_VULND = arbol("vulnd", lambda s: devallow(vuln(s), DB_DEV))
EQUIV = {}
try:   # prueba de que VULN es exactamente la guarda publicada en 404f5adc
    top = subprocess.run(["git", "-C", HERE, "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    old = subprocess.run(["git", "-C", top, "show", "404f5adc69d6db4b30ceae79912fd3a9ef533cce:docs/fase0/cierre_tecnico_fase0/scripts_validacion/cci_dev_NO_EJECUTADOS/00_guarda_destino.sql"], capture_output=True).stdout
    EQUIV = {"vuln_sha256": sha(os.path.join(T_VULN, "00_guarda_destino.sql")), "guarda_404f5adc_sha256": hashlib.sha256(old).hexdigest()}; EQUIV["identica"] = EQUIV["vuln_sha256"] == EQUIV["guarda_404f5adc_sha256"]
except Exception as ex: EQUIV = {"identica": None, "nota": "NOT_TESTED: sin acceso a git (%s)" % ex}
# ---- bases y fixtures
for r in ("anon", "authenticated", "service_role"): q("do $$ begin if not exists (select 1 from pg_roles where rolname='%s') then create role %s nologin; end if; end $$" % (r, r))
for d in ("cci_opc_shim", "cci_opc_conc", DB_DEV): q("drop database if exists " + d); q("create database " + d)
sh(["-q", "-v", "ON_ERROR_STOP=1", "-v", "variante=corregida", "-f", os.path.join(HERE, "local_ext", "30_shim_rls_fixture_LOCAL.sql")], db="cci_opc_shim")
sh(["-q", "-v", "ON_ERROR_STOP=1", "-f", os.path.join(HERE, "local_ext", "31_conc_smoke_fixture_LOCAL.sql")], db="cci_opc_conc")
DBS = ("cci_opc_shim", "cci_opc_conc")
CN = [0]
def limpia():
    for db in DBS + (DB_DEV,):
        sh(["-q", "-f", scr("set search_path = pg_catalog;\nselect 'drop function ' || p.oid::regprocedure || ' cascade' from pg_proc p where p.pronamespace::oid operator(pg_catalog.=) 'public'::regnamespace::oid and p.proname like 'hf%' \\gexec\ndrop type if exists public.ct cascade;\ndrop domain if exists public.dt cascade;\ndrop schema if exists evil cascade;\ndrop table if exists public.hf_efecto;")], db=db)
    for sc in ("alter role cci_test reset search_path", "alter database cci_opc_shim reset search_path", "alter role cci_test in database cci_opc_shim reset search_path"): q(sc)
def op(db, o, l, r, ret=None, esq="public", cuerpo=None):
    """planta un operador hostil; devuelve la firma. cuerpo=None: lanza HIJACK-OP."""
    CN[0] += 1; fn = "hf%d" % CN[0]; ret = ret or ("text" if o == "||" else "boolean")
    b = cuerpo or "raise exception 'HIJACK-OP %s %s %s %s'" % (o, l, r, esq)
    f = "create function %s.%s(%s, %s) returns %s language plpgsql as $b$ begin %s; end $b$" % (esq, fn, l, r, ret, b)
    return f, "create operator %s.%s (leftarg = %s, rightarg = %s, function = %s.%s)" % (esq, o, l, r, esq, fn)
def planta(db, lst, **kw):
    sqls = []
    for t in lst:
        f, o = op(db, *t, **kw); sqls += [f, o]
    rc, o = sh(["-q", "-v", "ON_ERROR_STOP=1", "-f", scr(";\n".join(sqls))], db=db); return rc, o
# ---- ejecución de los 6 scripts
def corre(tree, sc, opts, user="cci_test", dbs=DBS):
    env = {"CCI_DIR": tree, "CCI_GUARDA_SHA256_APROBADO": sha(os.path.join(tree, "00_guarda_destino.sql"))}; f = os.path.join(tree, sc + ".sql")
    if sc.startswith("05"):
        P = ["-v", "ON_ERROR_STOP=1", "-v", "org=%s01" % U, "-v", "piece=%s02" % U, "-v", "reviewer_a=%s0a" % U, "-v", "reviewer_b=%s0b" % U, "-f", f]
        if sc.endswith("A"):
            out = []; th = threading.Thread(target=lambda: out.append(sh(P, dbs[1], user, opts, env))); th.start(); time.sleep(1.5)
            sh(P[:-1] + [os.path.join(tree, "05_concurrencia_sesion_B.sql")], dbs[1], user, opts, env); th.join(); return out[0]
        return sh(P, dbs[1], user, opts, env)
    base = ["-v", "ON_ERROR_STOP=1", "-v", "org_a=a0000000-0000-0000-0000-000000000001", "-v", "org_b=a0000000-0000-0000-0000-000000000002", "-v", "uid_a=a0000000-0000-0000-0000-0000000000a1", "-v", "uid_x=a0000000-0000-0000-0000-0000000000c1"]
    if sc.startswith("04"): base += [x for i in range(1) for x in ("-v", "org=%s01" % U, "-v", "attr=%s02" % U, "-v", "affected=%s03" % U, "-v", "requester=%s04" % U, "-v", "change_actor=%s05" % U, "-v", "r_ok=%s06" % U, "-v", "r_nomember=%s07" % U, "-v", "r_noreview=%s08" % U, "-v", "r_direct=%s09" % U, "-v", "r_inherited=%s10" % U, "-v", "r_othersrc=%s11" % U, "-v", "r_benef=%s12" % U)]
    return sh(base + ["-f", f], dbs[0], user, opts, env)
EJ = []
def barre(cid, cat, arbolnom, tree, opts, desc, pre, esquema, firmas, tipos, scripts=SEIS):
    res = []
    for sc in scripts:
        rc, o = corre(tree, sc, opts)
        hij = sorted(set(re.findall(r"HIJACK-(?:OP|FN)[^\n]*", o))); rej = re.search(r"NO EJECUTADO \[(G-[A-Z-]+)\]", o)
        r = {"id": "%s/%s/%s" % (cid, arbolnom, sc[:2] + (sc[-1] if sc.startswith("05") else "")), "caso": cid, "categoria": cat, "arbol": arbolnom, "script": sc, "descripcion": desc, "precondicion": pre, "rol_efectivo": "cci_test (superusuario LOCAL; fixture)", "esquema_objeto": esquema, "firma_operador": firmas, "tipos_entrada": tipos, "search_path_efectivo": ("(configuración heredada/PGOPTIONS: ver opciones) " + opts.replace(LOC, "").strip()) or "por defecto", "operador_resuelto_ejecutado": "; ".join(h[:90] for h in hij[:3]) or "ninguno hostil (catálogo)", "ejecutado": bool(hij), "rechazado": rej.group(1) if rej else "", "rc": rc, "guarda_ok": "GUARDA OK" in o}
        EJ.append(r); res.append(r)
    return res
CASOS = []
def caso(cid, cat, desc, vuln_res, new_res, esperado_vuln, extra=""):
    hv = sorted({r["script"][:2] + (r["script"][-1] if r["script"].startswith("05") else "") for r in vuln_res if r["ejecutado"]}); hn = [r for r in new_res if r["ejecutado"]]
    rech = sorted({r["rechazado"] for r in new_res if r["rechazado"]})
    ok_new = not hn and all(r["rechazado"] or not r["ejecutado"] for r in new_res)
    ok_vuln = True if esperado_vuln is None else (bool(hv) if esperado_vuln else not hv)
    CASOS.append({"id": cid, "categoria": cat, "descripcion": desc, "control_positivo_VULN_scripts_secuestrados": hv, "esperado_en_VULN": ("ataque funciona" if esperado_vuln else "ataque no se ejecuta (orden del search_path)" if esperado_vuln is False else "informativo"), "control_positivo_ok": ok_vuln, "NEW_ataques_ejecutados": len(hn), "NEW_rechazos": rech, "estado": "PASS" if (ok_new and ok_vuln) else "FAIL", "nota": extra})
    print("%s | %s | VULN secuestra=%s | NEW ejecutados=%d rechazos=%s | %s" % ("PASS" if (ok_new and ok_vuln) else "FAIL", cid, hv, len(hn), rech, desc[:80]))
def ataque(cid, cat, desc, setup, esperado_vuln, esquema="public", firmas="", tipos="", opts=LOC, trees=None, extra=""):
    limpia(); setup()
    v = barre(cid, cat, "VULN", T_VULN, opts, desc, "objetos hostiles instalados ANTES de ejecutar", esquema, firmas, tipos)
    n = barre(cid, cat, "NEW", T_NEW, opts, desc, "objetos hostiles instalados ANTES de ejecutar", esquema, firmas, tipos)
    caso(cid, cat, desc, v, n, esperado_vuln, extra); limpia()
def inst(lst, **kw):
    def f():
        for db in DBS:
            rc, o = planta(db, lst, **kw)
            if rc: print("ERROR instalando", lst[:2], o[-200:]); raise SystemExit(2)
    return f
TIPOS = ["text", "name", "varchar", "bpchar", '"char"', "oid", "int2", "int4", "int8", "bool", "regclass", "regnamespace", "uuid", "regtype", "numeric", "jsonb"]
# ================= A: homónimos exactos en public (pierden por el orden: pg_catalog primero)
A = [("=", "text", "text"), ("=", "name", "name"), ("||", "text", "text"), ("~", "text", "text"), ("!~", "text", "text"), ("=", "oid", "oid"), ("=", "int4", "int4"), ("<>", "text", "text")]
ataque("A-01", "A homónimos exactos en public", "operadores con la MISMA firma que los de pg_catalog creados en public", inst(A), False, firmas=", ".join("%s(%s,%s)" % t for t in A), tipos="text/name/oid/int4")
# ================= B: más específicos (ganan a pg_catalog)
B = [("=", "oid", "regnamespace"), ("=", "regnamespace", "oid"), ("=", "regclass", "oid"), ("=", "oid", "regclass")]
ataque("B-01", "B firma más específica", "= (oid, regnamespace) y variantes con tipos reg* en public", inst(B), True, firmas=", ".join("%s(%s,%s)" % t for t in B), tipos="oid/regnamespace/regclass")
def sweep():
    for db in DBS:
        sql = []
        for o in ("=", "<>", "||", "<", "~", "!~", "~~", "!~~"):
            for l in TIPOS:
                for r in TIPOS:
                    f, c = op(db, o, l, r); sql += [f, c]
        rc, out = sh(["-q", "-v", "ON_ERROR_STOP=1", "-f", scr(";\n".join(sql))], db=db)
        if rc: print("ERROR sweep", out[-200:]); raise SystemExit(2)
ataque("B-02", "B firma más específica", "BARRIDO: 8 operadores × 16×16 tipos en public (2048 firmas por base)", sweep, True, firmas="{=,<>,||,<,~,!~,~~,!~~} × 16×16 tipos", tipos=", ".join(TIPOS))
# ================= C: resolución mediante conversiones implícitas
C = [("=", "oid", "int8"), ("=", "int4", "int8"), ("=", "name", "varchar"), ("=", '"char"', "text"), ("||", "text", "int4"), ("<>", "text", "varchar"), ("~~", "name", "text"), ("=", "bpchar", "text"), ("=", "regclass", "text"), ("=", "regnamespace", "text")]
ataque("C-01", "C conversión implícita", "operadores cuyas firmas sólo coinciden tras conversiones implícitas de los operandos de los scripts", inst(C), None, firmas=", ".join("%s(%s,%s)" % t for t in C), tipos="oid/int4/int8/name/varchar/char/text/reg*", extra="informativo: el resultado en VULN depende de qué operandos usan los scripts; el criterio es NEW=0")
# ================= D: tipos personalizados, dominios y casts
def tipos():
    for db in DBS:
        rc, o = sh(["-q", "-v", "ON_ERROR_STOP=1", "-c", "create type public.ct as (a text); create domain public.dt as int4; create function public.hfd1(public.ct, public.ct) returns boolean language plpgsql as $b$ begin raise exception 'HIJACK-OP = ct ct'; end $b$; create operator public.= (leftarg=public.ct, rightarg=public.ct, function=public.hfd1); create function public.hfd2(public.dt, public.dt) returns boolean language plpgsql as $b$ begin raise exception 'HIJACK-OP = dt dt'; end $b$; create operator public.= (leftarg=public.dt, rightarg=public.dt, function=public.hfd2); create function public.hfd3(text) returns public.ct language plpgsql as $b$ begin raise exception 'HIJACK-FN cast text->ct'; end $b$; create cast (text as public.ct) with function public.hfd3(text) as implicit; create function public.hfd4(int4) returns public.dt language sql as 'select $1::public.dt'; create cast (int4 as public.dt) with function public.hfd4(int4) as implicit"], db=db)
        if rc: print("ERROR tipos", o[-300:]); raise SystemExit(2)
ataque("D-01", "D tipos personalizados", "tipo compuesto y dominio en public con operadores propios + casts implícitos de usuario", tipos, None, firmas="=(ct,ct), =(dt,dt), cast text→ct IMPLICIT, cast int4→dt IMPLICIT", tipos="ct/dt/text/int4", extra="informativo en VULN; en NEW la guarda rechaza el operador ajeno o el cast ajeno")
# ================= E: operadores que ejecutan funciones auxiliares con efectos y devuelven el valor correcto (ataque silencioso)
def aux():
    cu = "raise notice 'HIJACK-OP-AUX efecto lateral ejecutado'; perform pg_catalog.set_config('cci.pwned','1',false); return $1::oid operator(pg_catalog.=) $2::oid"
    for db in DBS:
        f, c = op(db, "=", "oid", "regnamespace", cuerpo=cu); rc, o = sh(["-q", "-v", "ON_ERROR_STOP=1", "-c", f + "; " + c], db=db)
        if rc: print("ERROR aux", o[-300:]); raise SystemExit(2)
ataque("E-01", "E función auxiliar", "= (oid, regnamespace) que ejecuta una función auxiliar con efecto lateral y devuelve el resultado CORRECTO (el script no falla: ataque silencioso)", aux, True, firmas="=(oid,regnamespace) → set_config + notice, devuelve el valor real", tipos="oid/regnamespace")
# ================= F: antes/después de fijar el search_path; G: objetos temporales; H: SET/SET LOCAL/PGOPTIONS/configuración heredada; J: resolución real
def probe(tree, cuerpo, opts=LOC, db="cci_opc_shim", nombre="01_probe"):
    d = os.path.join(TMP, "pr_" + os.path.basename(tree)); shutil.rmtree(d, ignore_errors=True); shutil.copytree(tree, d)
    open(os.path.join(d, nombre + ".sql"), "w", encoding="utf-8").write("\\set ON_ERROR_STOP on\n\\set cci_script '01'\n\\ir 00_preflight_guarda.sql\n\\set cci_script '01'\n\\ir 00_verificar_marcador.sql\n" + cuerpo + "\n")
    return sh(["-v", "ON_ERROR_STOP=1", "-f", os.path.join(d, nombre + ".sql")], db=db, opts=opts, env={"CCI_DIR": d, "CCI_GUARDA_SHA256_APROBADO": sha(os.path.join(d, "00_guarda_destino.sql"))})
J = ("create temp view cci_j as select 'pg_catalog'::regnamespace::oid = 'pg_catalog'::regnamespace as x;\n"
     "select 'RESOLVIO=' || n.nspname || '.' || o.oprname || '(' || o.oprleft::regtype || ',' || o.oprright::regtype || ')' as r from pg_depend d join pg_operator o on o.oid = d.refobjid join pg_namespace n on n.oid = o.oprnamespace where d.refclassid = 'pg_operator'::regclass and d.objid = (select w.oid from pg_rewrite w where w.ev_class = 'cci_j'::regclass);\n"
     "select 'SP_EFECTIVO=' || pg_catalog.current_setting('search_path');")
def resuelto(o):
    m = re.search(r"RESOLVIO=(\S+)", o); s = re.search(r"SP_EFECTIVO=(.+)", o)
    return (m.group(1) if m else ("pg_catalog(objeto fijado: sin pg_depend)" if s else "")), (s.group(1).strip() if s else "")
PROB = []
def pr(cid, cat, desc, tree_nom, tree, body, esperado, opts=LOC, pre=""):
    rc, o = probe(tree, body, opts); res, sp = resuelto(o); rej = re.search(r"NO EJECUTADO \[(G-[A-Z-]+)\]", o)
    cumple = esperado(res, rej.group(1) if rej else "", o); PROB.append({"id": "%s/%s" % (cid, tree_nom), "caso": cid, "categoria": cat, "arbol": tree_nom, "descripcion": desc, "precondicion": pre, "operador_resuelto": res or "(sin resolución: el script no llegó a ejecutarse)", "search_path_efectivo": sp or "n/d", "rechazado": rej.group(1) if rej else "", "rc": rc, "estado": "PASS" if cumple else "FAIL"})
    print("%s | %s/%s | resuelto=%s sp=%s rechazo=%s" % ("PASS" if cumple else "FAIL", cid, tree_nom, res, sp, rej.group(1) if rej else ""))
def en_pub(db="cci_opc_shim"): planta(db, [("=", "oid", "regnamespace")])
# J-01: sin ataque: el operador realmente resuelto es el de pg_catalog (línea base)
limpia(); pr("J-01", "J resolución real", "línea base sin objetos hostiles: operador realmente resuelto", "NEW", T_NEW, J, lambda r, c, o: r.startswith("pg_catalog"))
# J-02: ataque presente ANTES: VULN resuelve a public (el ataque es real), NEW lo rechaza
limpia(); en_pub()
pr("J-02", "J resolución real", "operador = (oid,regnamespace) en public instalado antes", "VULN", T_VULN, J, lambda r, c, o: r == "public.=(oid,regnamespace)", pre="public.=(oid,regnamespace) instalado")
pr("J-02", "J resolución real", "ídem", "NEW", T_NEW, J, lambda r, c, o: c == "G-OPERADOR-AJENO-EN-SEARCH-PATH" and r == "", pre="public.=(oid,regnamespace) instalado")
# F-01: creado DESPUÉS de superar la guarda y fijar el search_path (por la propia sesión)
limpia()
pl = "create function public.hff(oid, regnamespace) returns boolean language sql as 'select true'; create operator public.= (leftarg=oid, rightarg=regnamespace, function=public.hff);\n"
pr("F-01", "F creado tras fijar search_path", "el operador se crea DESPUÉS de la guarda, dentro de la misma sesión, por un rol con CREATE (superusuario local)", "VULN", T_VULN, pl + J, lambda r, c, o: r == "public.=(oid,regnamespace)", pre="sesión con CREATE en public")
limpia()
pr("F-01", "F creado tras fijar search_path", "ídem (límite: un rol que YA puede crear en public lo logra; por eso el control real es el privilegio, ver P-*)", "NEW", T_NEW, pl + J, lambda r, c, o: r == "public.=(oid,regnamespace)", pre="sesión con CREATE en public (superusuario local; la guarda LOCAL no puede impedirlo)")
limpia()
# G: objetos temporales
gt = "create function pg_temp.hft(oid, regnamespace) returns boolean language plpgsql as $b$ begin raise exception 'HIJACK-OP temp'; end $b$;\ncreate operator pg_temp.= (leftarg = oid, rightarg = regnamespace, function = pg_temp.hft);\ncreate temp table pg_namespace(oid int);\ncreate temp table pg_class(oid int);\n" + J
for nom, t in (("VULN", T_VULN), ("NEW", T_NEW)): pr("G-01", "G objetos temporales", "operador y tablas TEMPORALES homónimas (pg_temp.=(oid,regnamespace), pg_temp.pg_namespace, pg_temp.pg_class) creados tras la guarda", nom, t, gt, lambda r, c, o: r.startswith("pg_catalog"), pre="objetos en pg_temp de la sesión")
limpia()
# H: search_path hostil por PGOPTIONS / configuración heredada / SET posterior
def evil():
    for db in DBS: q("create schema if not exists evil", db); planta(db, [("=", "oid", "regnamespace")], esq="evil")
limpia(); evil()
EVOPT = LOC + " -c search_path=evil,pg_catalog,public"
for nom, t in (("NOPIN", T_NOPIN), ("VULN", T_VULN), ("NEW", T_NEW)):
    esp = (lambda r, c, o: r == "evil.=(oid,regnamespace)") if nom == "NOPIN" else (lambda r, c, o: c == "G-SEARCH-PATH-NO-SEGURO" and r == "")
    pr("H-01", "H PGOPTIONS", "PGOPTIONS search_path=evil,pg_catalog,public con operador hostil en evil (NOPIN = sin ningún blindaje: control positivo)", nom, t, J, esp, opts=EVOPT)
q("alter role cci_test set search_path = evil, pg_catalog, public")
for nom, t in (("NOPIN", T_NOPIN), ("NEW", T_NEW)):
    esp = (lambda r, c, o: r == "evil.=(oid,regnamespace)") if nom == "NOPIN" else (lambda r, c, o: c == "G-SEARCH-PATH-NO-SEGURO" and r == "")
    pr("H-02", "H configuración heredada", "ALTER ROLE … SET search_path (configuración heredada por el rol)", nom, t, J, esp)
q("alter role cci_test reset search_path"); q("alter database cci_opc_shim set search_path = evil, pg_catalog, public")
for nom, t in (("NOPIN", T_NOPIN), ("NEW", T_NEW)):
    esp = (lambda r, c, o: r == "evil.=(oid,regnamespace)") if nom == "NOPIN" else (lambda r, c, o: c == "G-SEARCH-PATH-NO-SEGURO" and r == "")
    pr("H-03", "H configuración heredada", "ALTER DATABASE … SET search_path (configuración heredada por la base)", nom, t, J, esp)
q("alter database cci_opc_shim reset search_path")
for nom, t in (("NEW", T_NEW),):
    pr("H-04", "H SET posterior", "SET search_path (sesión) DESPUÉS de la guarda: límite del blindaje; no es alcanzable por los scripts (aserción estática H-05)", nom, t, "set search_path = evil, public;\n" + J, lambda r, c, o: r == "evil.=(oid,regnamespace)", pre="código del propio operador tras la guarda")
    pr("H-04b", "H SET LOCAL", "SET LOCAL search_path dentro de una transacción tras la guarda (ídem)", nom, t, "begin;\nset local search_path = evil, public;\n" + J + "\nrollback;", lambda r, c, o: r == "evil.=(oid,regnamespace)", pre="código del propio operador tras la guarda")
limpia()
# H-05 aserción estática: ningún script ejecutable (salvo la guarda y la maniobra de comprobación) cambia search_path / role / session authorization
est = []; PERMITIDO = {"00_verificar_marcador.sql": [r"search_path"], "04_lib_clasificador.sql": [r"set\s+local\s+role", r"reset\s+role"]}   # permitido y documentado: set_config LOCAL de pg_catalog en el verificador; suplantación de roles fixture (RLS) con SET LOCAL ROLE
USOS = []
for f in sorted(os.listdir(SRC)):
    if f.endswith(".sql") and f != "00_guarda_destino.sql":
        t = "\n".join(re.sub(r"--.*$", "", l) for l in open(os.path.join(SRC, f), encoding="utf-8").read().split("\n"))
        for l in t.split("\n"):
            for pat in (r"search_path", r"set\s+(local\s+)?role", r"reset\s+role", r"set\s+session\s+authorization", r"create\s+(or\s+replace\s+)?(operator|cast|type|domain)\b"):
                if re.search(pat, l, re.I):
                    if any(re.search(x, l, re.I) for x in PERMITIDO.get(f, [])): USOS.append("%s: %s" % (f, l.strip()[:110]))
                    else: est.append("%s: %s" % (f, l.strip()[:110]))
ESTATICO = {"id": "H-05", "descripcion": "ningún script ejecutable cambia search_path/rol ni crea operadores/casts/tipos (fuera de la guarda)", "hallazgos": est, "usos_permitidos_documentados": USOS, "estado": "PASS" if not est else "FAIL"}
print("%s | H-05 | %s" % (ESTATICO["estado"], est or "sin hallazgos"))
# I: funciones homónimas de las del propio control de privilegios (calificadas con pg_catalog)
# ================= P: privilegios efectivos (modo DEV, roles fixture)
for r in ("cci_operador", "cci_custodio", "cci_administrador"): q("drop role if exists %s" % r)
PR = []
def rol(n, attrs="", miembro=()):
    q("drop owned by %s cascade" % n, DB_DEV) if qs("select 1 from pg_roles where rolname='%s'" % n) else None; q("drop role if exists %s" % n)
    q("create role %s login %s" % (n, attrs)); [q("grant %s to %s" % (m, n)) for m in miembro]
q("create role cci_operador nologin; create role cci_custodio nologin; create role cci_administrador nologin")
q("revoke create on schema public from public", DB_DEV); q("revoke all on database %s from public; grant connect, temp on database %s to public" % (DB_DEV, DB_DEV))
def dev(tree, user, opts=DEV + " -c client_min_messages=log", db=DB_DEV):
    d = os.path.join(TMP, "dv_" + os.path.basename(tree)); shutil.rmtree(d, ignore_errors=True); shutil.copytree(tree, d)
    open(os.path.join(d, "01_probe.sql"), "w", encoding="utf-8").write("\\set ON_ERROR_STOP on\n\\set cci_script '01'\n\\ir 00_preflight_guarda.sql\n\\set cci_script '01'\n\\ir 00_verificar_marcador.sql\n\\echo CANARIO-CUERPO-EJECUTADO\n")
    return sh(["-v", "ON_ERROR_STOP=1", "-f", os.path.join(d, "01_probe.sql")], db=db, user=user, opts=opts, env={"CCI_DIR": d, "CCI_GUARDA_SHA256_APROBADO": sha(os.path.join(d, "00_guarda_destino.sql"))})
def pcase(pid, desc, setup, user, codigo, teardown=None, vuln_acepta=True):
    for s in setup: q(s, DB_DEV) if s.startswith("DB:") is False else None
    rn, on = dev(T_NEWD, user); rv, ov = dev(T_VULND, user)
    rejn = re.search(r"NO EJECUTADO \[(G-[A-Z-]+)\]", on); vulnok = "GUARDA OK" in ov and "CANARIO-CUERPO-EJECUTADO" in ov
    if codigo is None: ok = ("GUARDA OK" in on and "CANARIO-CUERPO-EJECUTADO" in on); esp = "operador legítimo ACEPTADO (sin regresión)"
    else: ok = bool(rejn) and rejn.group(1) == codigo and "CANARIO-CUERPO-EJECUTADO" not in on; esp = "rechazo %s sin canario" % codigo
    okv = (vulnok if vuln_acepta else True) if codigo is not None else True
    PR.append({"id": pid, "descripcion": desc, "rol_efectivo": user, "esperado_NEW": esp, "observado_NEW": (rejn.group(1) if rejn else ("GUARDA OK" if "GUARDA OK" in on else "otro: " + on[-120:].replace("\n", " "))), "control_positivo_VULN_acepta_al_rol": vulnok, "estado": "PASS" if (ok and okv) else "FAIL"})
    print("%s | %s | NEW=%s | VULN acepta=%s | %s" % ("PASS" if (ok and okv) else "FAIL", pid, PR[-1]["observado_NEW"], vulnok, desc[:70]))
    for s in (teardown or []): q(s, DB_DEV)
rol("t_ok", "", ["cci_operador"]); pcase("P-00", "línea base: operador legítimo (miembro de cci_operador, sin CREATE en public/base)", [], "t_ok", None)
pcase("P-01", "CREATE en public por concesión directa", ["grant create on schema public to t_ok"], "t_ok", "G-OPERADOR-CREATE-EN-PUBLIC", ["revoke create on schema public from t_ok"])
pcase("P-02", "CREATE en public concedido a PUBLIC (efectivo para todos los roles)", ["grant create on schema public to public"], "t_ok", "G-OPERADOR-CREATE-EN-PUBLIC", ["revoke create on schema public from public"])
rol("t_grp", "", []); q("alter role t_grp nologin"); rol("t_herd", "", ["cci_operador", "t_grp"])
pcase("P-03", "CREATE en public HEREDADO por pertenencia (INHERIT) a un grupo", ["grant create on schema public to t_grp"], "t_herd", "G-OPERADOR-CREATE-EN-PUBLIC", ["revoke create on schema public from t_grp"])
rol("t_noinh", "noinherit", ["cci_operador", "t_grp"])
pcase("P-04", "grupo con CREATE en public con el operador NOINHERIT (podría recuperarlo con SET ROLE; además un rol ajeno con CREATE queda detectado)", ["grant create on schema public to t_grp"], "t_noinh", "G-PUBLIC-CREATE-AJENO", ["revoke create on schema public from t_grp"])
q("create role t_su_grp nologin superuser"); rol("t_nosu", "noinherit", ["cci_operador", "t_su_grp"])
pcase("P-05", "operador NOINHERIT miembro de un rol SUPERUSER (recupera todo con SET ROLE)", [], "t_nosu", "G-OPERADOR-MEMBRESIA-PRIVILEGIADA")
q("create role t_cr_grp nologin createrole"); rol("t_cr_m", "", ["cci_operador"]); q("grant t_cr_grp to t_cr_m")
pcase("P-06", "miembro (heredando) de un rol CREATEROLE: efectivo e indirecto", [], "t_cr_m", "G-OPERADOR-MEMBRESIA-PRIVILEGIADA")
rol("t_db", "", ["cci_operador"]); pcase("P-07", "CREATE sobre la BASE (permite crear esquemas auxiliares, p. ej. uno con su propio nombre)", ["grant create on database %s to t_db" % DB_DEV], "t_db", "G-OPERADOR-CREATE-EN-BASE", ["revoke create on database %s from t_db" % DB_DEV])
rol("t_own", "", ["cci_operador"]); pcase("P-08", "operador PROPIETARIO del esquema public (CREATE implícito por propiedad)", ["alter schema public owner to t_own"], "t_own", "G-OPERADOR-CREATE-EN-PUBLIC", ["alter schema public owner to pg_database_owner"])
rol("t_otro", "", []); pcase("P-09", "OTRO rol (no el operador) con CREATE en public puede plantar operadores entre la comprobación y la ejecución", ["grant create on schema public to t_otro"], "t_ok", "G-PUBLIC-CREATE-AJENO", ["revoke create on schema public from t_otro"])
q("alter default privileges for role t_ok in schema public grant all on tables to t_ok; alter default privileges in schema public grant all on functions to public", DB_DEV)
pcase("P-10", "ALTER DEFAULT PRIVILEGES sobre tablas/funciones de public NO confiere CREATE sobre el esquema (informativo: el operador sigue aceptado)", [], "t_ok", None, ["alter default privileges for role t_ok in schema public revoke all on tables from t_ok", "alter default privileges in schema public revoke all on functions from public"])
q("select 1")
# P-11: E2E: con CREATE en public, el operador AUTORIZADO introduce el operador hostil y secuestra el script (control positivo del hallazgo de privilegios); NEW lo bloquea antes
q("grant create on schema public to t_ok", DB_DEV); q("grant usage on schema public to t_ok", DB_DEV)
rc, o = sh(["-q", "-v", "ON_ERROR_STOP=1", "-c", "create function public.hfe(oid, regnamespace) returns boolean language plpgsql as $b$ begin raise exception 'HIJACK-OP e2e'; end $b$; create operator public.= (leftarg=oid, rightarg=regnamespace, function=public.hfe)"], db=DB_DEV, user="t_ok")
creo = rc == 0
d = os.path.join(TMP, "e2e"); shutil.rmtree(d, ignore_errors=True); shutil.copytree(T_VULND, d)
open(os.path.join(d, "01_probe.sql"), "w", encoding="utf-8").write("\\set ON_ERROR_STOP on\n\\set cci_script '01'\n\\ir 00_preflight_guarda.sql\n\\set cci_script '01'\n\\ir 00_verificar_marcador.sql\n" + J + "\n")
rcv, ov = sh(["-v", "ON_ERROR_STOP=1", "-f", os.path.join(d, "01_probe.sql")], db=DB_DEV, user="t_ok", opts=DEV + " -c client_min_messages=log", env={"CCI_DIR": d, "CCI_GUARDA_SHA256_APROBADO": sha(os.path.join(d, "00_guarda_destino.sql"))})
rn, on = dev(T_NEWD, "t_ok")
e2e_ok = creo and resuelto(ov)[0] == "public.=(oid,regnamespace)" and re.search(r"NO EJECUTADO \[G-OPERADOR-CREATE-EN-PUBLIC\]", on) is not None
PR.append({"id": "P-11", "descripcion": "E2E: operador AUTORIZADO con CREATE residual en public crea el operador y, con la guarda anterior, el siguiente script resuelve al operador hostil; con la guarda nueva se rechaza antes", "rol_efectivo": "t_ok", "esperado_NEW": "rechazo G-OPERADOR-CREATE-EN-PUBLIC", "observado_NEW": (re.search(r"NO EJECUTADO \[(G-[A-Z-]+)\]", on) or [0, "GUARDA OK"])[1], "control_positivo_VULN_acepta_al_rol": creo and resuelto(ov)[0] == "public.=(oid,regnamespace)", "estado": "PASS" if e2e_ok else "FAIL", "evidencia": {"creo_operador": creo, "VULN_operador_resuelto": resuelto(ov)[0]}})
print("%s | P-11 | creó=%s VULN resolvió=%s NEW=%s" % ("PASS" if e2e_ok else "FAIL", creo, resuelto(ov)[0], PR[-1]["observado_NEW"]))
q("drop operator if exists public.= (oid, regnamespace) cascade; revoke create on schema public from t_ok", DB_DEV); q("do $$ declare r record; begin for r in select p.oid::regprocedure x from pg_proc p where p.proname='hfe' loop execute 'drop function '||r.x||' cascade'; end loop; end $$", DB_DEV)
# P-12: después de la corrección, el operador sin CREATE intenta crear el operador tras la guarda -> permission denied
d = os.path.join(TMP, "p12"); shutil.rmtree(d, ignore_errors=True); shutil.copytree(T_NEWD, d)
open(os.path.join(d, "01_probe.sql"), "w", encoding="utf-8").write("\\set ON_ERROR_STOP on\n\\set cci_script '01'\n\\ir 00_preflight_guarda.sql\n\\set cci_script '01'\n\\ir 00_verificar_marcador.sql\ncreate function public.hfx(oid, regnamespace) returns boolean language sql as 'select true';\n")
rc, o = sh(["-v", "ON_ERROR_STOP=1", "-f", os.path.join(d, "01_probe.sql")], db=DB_DEV, user="t_ok", opts=DEV + " -c client_min_messages=log", env={"CCI_DIR": d, "CCI_GUARDA_SHA256_APROBADO": sha(os.path.join(d, "00_guarda_destino.sql"))})
ok12 = "GUARDA OK" in o and "permission denied for schema public" in o
PR.append({"id": "P-12", "descripcion": "tras superar la guarda, el operador (sin CREATE) intenta crear una función/operador en public: rechazado por PostgreSQL", "rol_efectivo": "t_ok", "esperado_NEW": "permission denied for schema public", "observado_NEW": "permission denied" if ok12 else o[-150:].replace("\n", " "), "control_positivo_VULN_acepta_al_rol": True, "estado": "PASS" if ok12 else "FAIL"})
print("%s | P-12 | %s" % ("PASS" if ok12 else "FAIL", PR[-1]["observado_NEW"]))
# P-13: pg_temp: el operador tiene TEMP (necesario para el marcador) pero un operador en pg_temp NO se resuelve (G-01)
PR.append({"id": "P-13", "descripcion": "CREATE/TEMP en pg_temp: el operador conserva TEMP (lo necesita el marcador); la resolución ignora pg_temp para operadores (ver G-01)", "rol_efectivo": "t_ok", "esperado_NEW": "TEMP concedido; sin efecto sobre la resolución", "observado_NEW": "TEMP=%s; ver G-01" % qs("select pg_catalog.has_database_privilege('t_ok','%s','TEMP')" % DB_DEV), "control_positivo_VULN_acepta_al_rol": True, "estado": "PASS" if (qs("select pg_catalog.has_database_privilege('t_ok','%s','TEMP')" % DB_DEV) == "t" and all(p["estado"] == "PASS" for p in PROB if p["caso"] == "G-01")) else "FAIL"})
print(PR[-1]["estado"], "| P-13")
# volcado de privilegios efectivos (comprobaciones del servidor, no de las declaraciones originales)
VOL = []
for rn_ in qs("select string_agg(rolname, ',' order by rolname) from pg_roles where rolname !~ '^pg_'").split(","):
    f = qs("select concat_ws('|', rolsuper, rolcreaterole, rolcreatedb, rolbypassrls, rolreplication, rolinherit, pg_catalog.has_schema_privilege(oid,'public','CREATE'), pg_catalog.has_schema_privilege(oid,'public','USAGE'), pg_catalog.has_database_privilege(oid,'%s','CREATE'), pg_catalog.has_database_privilege(oid,'%s','TEMP'), (select string_agg(r2.rolname, ',' order by r2.rolname) from pg_roles r2 where r2.oid <> pg_roles.oid and pg_catalog.pg_has_role(pg_roles.oid, r2.oid, 'member') and r2.rolname !~ '^pg_')) from pg_roles where rolname='%s'" % (DB_DEV, DB_DEV, rn_), DB_DEV).split("|")
    if len(f) == 11: VOL.append(dict(zip(["rol", "super", "createrole", "createdb", "bypassrls", "replication", "inherit", "CREATE_public_efectivo", "USAGE_public_efectivo", "CREATE_base_efectivo", "TEMP_base_efectivo", "miembro_de_efectivo"], [rn_] + f)))
OWN = qs("select pg_catalog.pg_get_userbyid(nspowner) from pg_namespace where nspname='public'", DB_DEV); DACL = qs("select coalesce(string_agg(pg_catalog.pg_get_userbyid(defaclrole)||':'||defaclobjtype||':'||defaclacl::text, '; '),'(ninguno)') from pg_default_acl", DB_DEV)
# limpieza de roles fixture
for r in ("t_ok", "t_grp", "t_herd", "t_noinh", "t_su_grp", "t_nosu", "t_cr_grp", "t_cr_m", "t_db", "t_own", "t_otro"): q("drop owned by %s cascade" % r, DB_DEV); q("drop role if exists %s" % r)
for r in ("cci_operador", "cci_custodio", "cci_administrador"): q("drop role if exists %s" % r)
for d in DBS + (DB_DEV,): q("drop database if exists " + d)
shutil.rmtree(TMP, ignore_errors=True)
todo = CASOS + PROB + PR + [ESTATICO]
tot = len(todo); okn = sum(1 for c in todo if c["estado"] == "PASS"); fail = tot - okn
json.dump({"equivalencia_VULN_con_guarda_404f5adc": EQUIV, "casos_barrido": CASOS, "ejecuciones": EJ, "resolucion_real_J_F_G_H": PROB, "privilegios_P": PR, "estatico_H05": ESTATICO, "volcado_privilegios_efectivos": VOL, "propietario_public": OWN, "default_acl": DACL}, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("EQUIVALENCIA VULN==404f5adc:", EQUIV.get("identica"))
print("TOTAL=%d PASS=%d FAIL=%d" % (tot, okn, fail))
sys.exit(0 if (fail == 0 and EQUIV.get("identica") is not False) else 1)
