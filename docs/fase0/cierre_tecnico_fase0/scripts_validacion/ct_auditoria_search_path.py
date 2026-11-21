#!/usr/bin/env python3
# Uso: python3 -I -B ct_auditoria_search_path.py <socket> <puerto> <arbol_corregido_dir> <arbol_publicado_dir> <salida.json>   (PostgreSQL TEMPORAL LOCAL; nunca Supabase)
# (1) AUDITORÍA ESTÁTICA: toda llamada con forma nombre( que NO esté calificada y cuyo nombre exista como función de pg_catalog (en cada archivo ejecutable).
# (2) AUDITORÍA DINÁMICA: se instala un homónimo malicioso de CADA función de pg_catalog usada por los scripts (todas las sobrecargas) y de operadores comunes, y se ejecutan los 6 scripts
#     bajo search_path hostil y con los objetos hostiles en 'public'. Un homónimo invocado = 'HIJACK-FN'/'HIJACK-OP' en la salida.
import json, os, re, shutil, subprocess, sys, tempfile, threading, time, hashlib
SOCK, PORT, NEW, OLDS, OUT = sys.argv[1:6]
OLDL = [x.split("=", 1) for x in OLDS.split(",")]   # etiqueta=ruta de árboles anteriores (p. ej. d365a16=…,e0b1d81=…)
HERE = os.path.dirname(os.path.abspath(__file__))
SEIS = ["01_inventario_esquema_SOLO_LECTURA", "02_rls_privilegios_SOLO_LECTURA", "03_pruebas_rls_ROLLBACK", "04_trigger_r1_r9_ROLLBACK", "05_concurrencia_sesion_A", "05_concurrencia_sesion_B"]
LOC = "-c cci.validacion_autorizada=SI-LOCAL-TEMPORAL -c cci.entorno=LOCAL-TEMPORAL"; U = "00000000-0000-0000-0000-0000000000"
def sh(a, db="postgres", opts="", env=None, cwd=None, timeout=120):
    e = dict(os.environ, PGHOST=SOCK, PGPORT=PORT, PGUSER="cci_test", PGOPTIONS=opts); e.update(env or {})
    r = subprocess.run(["psql", "-X", "-d", db] + a, env=e, capture_output=True, text=True, cwd=cwd, timeout=timeout); return r.returncode, r.stdout + r.stderr
def q(sql, db="postgres"): return sh(["-qAt", "-v", "ON_ERROR_STOP=1", "-c", sql], db=db)
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
ARCH = ["00_guarda_destino.sql", "00_preflight_guarda.sql", "00_verificar_marcador.sql", "04_lib_clasificador.sql"] + [s + ".sql" for s in SEIS]
SINT = {"coalesce", "nullif", "greatest", "least", "row", "array", "exists", "any", "all", "in", "values", "cast", "not", "and", "or", "when", "then", "else", "case", "select", "from", "where", "with", "on", "as", "using", "by", "over", "filter", "within", "group", "between", "like", "is", "end", "if", "loop", "for", "foreach", "raise", "perform", "return", "returns", "table", "setof", "unnest_syntax", "extract", "position"}   # extract(... from ...) y position(... in ...) son formas especiales de la gramática (se resuelven a pg_catalog sin search_path)
def sin_comentarios(t): return "\n".join(re.sub(r"--.*$", "", l) if not l.lstrip().startswith("\\") else l for l in t.split("\n"))
rc, o = q("select string_agg(distinct proname, ',') from pg_proc where pronamespace='pg_catalog'::regnamespace"); CAT = set(o.strip().split(","))
estatico = []; usadas = set()
for tree, etq in [(NEW, "corregido")] + [(pth, "anterior:" + lb) for lb, pth in OLDL]:
    for f in ARCH:
        p = os.path.join(tree, f)
        if not os.path.exists(p): continue
        t = sin_comentarios(open(p, encoding="utf-8").read())
        for m in re.finditer(r"(?<![\w.$\"'/])([a-z_][a-z0-9_]*)\s*\(", t):
            n = m.group(1)
            if n in CAT and n not in SINT: estatico.append({"arbol": etq, "archivo": f, "funcion": n, "tipo": "SIN CALIFICAR"})
        for m in re.finditer(r"pg_catalog\.([a-z_][a-z0-9_]*)\s*\(", t): usadas.add(m.group(1)) if etq == "corregido" else None
        for n in re.findall(r"(?<![\w.$\"'])([a-z_][a-z0-9_]*)\s*\(", t):
            if n in CAT and n not in SINT: usadas.add(n)
from collections import Counter
agr = Counter((e["arbol"], e["funcion"]) for e in estatico)
def ddl_evil(db, esq, funcs=True, ops_=True):
    q("create schema if not exists %s" % esq, db)
    if not funcs: nombres = "''"
    else: nombres = ",".join("'%s'" % n for n in sorted(usadas))
    rc, o = q("select format('create function %s.%%I(%%s) returns %%s language plpgsql as $b$ begin raise exception ''HIJACK-FN %%s''; end $b$', proname, pg_get_function_identity_arguments(oid), pg_get_function_result(oid), proname) from pg_proc where pronamespace='pg_catalog'::regnamespace and proname in (%s) and prokind='f' and proargtypes::text not like '%%2276%%'" % (esq, nombres), db)
    ok = fall = 0; faltan = set()
    for l in o.strip().split("\n"):
        if not l.strip(): continue
        r, oo = q(l, db)
        if r == 0: ok += 1
        else: fall += 1; faltan.add(re.search(r"function %s\.(\w+)" % esq, l).group(1) if re.search(r"function %s\.(\w+)" % esq, l) else "?")
    # agregadas usadas con homónimo posible
    for agg, args, st in (("count", "*", "bigint"), ("string_agg", "text, text", "text")):
        if funcs and agg in usadas:
            q("create function %s.sf_%s(a %s, b text, c text default null) returns %s language plpgsql as $b$ begin raise exception 'HIJACK-FN %s'; end $b$" % (esq, agg, st, st, agg), db)
            r, oo = q("create aggregate %s.%s(%s) (sfunc = %s.sf_%s, stype = %s)" % (esq, agg, args, esq, agg, st), db) if agg == "string_agg" else q("create function %s.sfc(bigint) returns bigint language plpgsql as $b$ begin raise exception 'HIJACK-FN count'; end $b$; create aggregate %s.count(*) (sfunc = %s.sfc, stype = bigint, initcond = '0')" % (esq, esq, esq), db)
            ok += 1 if r == 0 else 0
    # operadores
    ops = 0
    for op, l, r_, ret in [] if not ops_ else [("||", "text", "text", "text"), ("=", "text", "text", "boolean"), ("<>", "text", "text", "boolean"), ("~", "text", "text", "boolean"), ("!~", "text", "text", "boolean"), ("=", "name", "name", "boolean"), ("=", "oid", "oid", "boolean"), ("=", "integer", "integer", "boolean"), ("||", "text", "unknown", "text")]:
        fn = "op_%d" % ops; ops += 1
        q("create function %s.%s(%s, %s) returns %s language plpgsql as $b$ begin raise exception 'HIJACK-OP %s'; end $b$" % (esq, fn, l, r_, ret, op.replace("'", "")), db)
        q("create operator %s.%s (leftarg = %s, rightarg = %s, function = %s.%s)" % (esq, op, l, r_, esq, fn), db)
    return ok, fall, sorted(faltan), ops
def fixtures():
    for d in ("cci_ap_shim", "cci_ap_conc"): q("drop database if exists " + d); q("create database " + d)
    sh(["-q", "-v", "ON_ERROR_STOP=1", "-v", "variante=corregida", "-f", os.path.join(HERE, "local_ext", "30_shim_rls_fixture_LOCAL.sql")], db="cci_ap_shim", opts=LOC)
    sh(["-q", "-v", "ON_ERROR_STOP=1", "-f", os.path.join(HERE, "local_ext", "31_conc_smoke_fixture_LOCAL.sql")], db="cci_ap_conc", opts=LOC)
def corre(tree, sc, opts, nuevo=True):
    env = {"CCI_DIR": tree, "CCI_GUARDA_SHA256_APROBADO": sha(os.path.join(tree, "00_guarda_destino.sql"))} if nuevo else {}
    f = os.path.join(tree, sc + ".sql")
    if sc.startswith("05"):
        P = ["-v", "ON_ERROR_STOP=1", "-v", "org=%s01" % U, "-v", "piece=%s02" % U, "-v", "reviewer_a=%s0a" % U, "-v", "reviewer_b=%s0b" % U, "-f", f]
        if sc.endswith("A"):
            out = []; th = threading.Thread(target=lambda: out.append(sh(P, "cci_ap_conc", opts, env))); th.start(); time.sleep(1.5); rb = sh(["-v", "ON_ERROR_STOP=1", "-v", "org=%s01" % U, "-v", "piece=%s02" % U, "-v", "reviewer_a=%s0a" % U, "-v", "reviewer_b=%s0b" % U, "-f", os.path.join(tree, "05_concurrencia_sesion_B.sql")], "cci_ap_conc", opts, env); th.join(); return out[0]
        return sh(P, "cci_ap_conc", opts, env)
    base = ["-v", "ON_ERROR_STOP=1", "-v", "org_a=a0000000-0000-0000-0000-000000000001", "-v", "org_b=a0000000-0000-0000-0000-000000000002", "-v", "uid_a=a0000000-0000-0000-0000-0000000000a1", "-v", "uid_x=a0000000-0000-0000-0000-0000000000c1"]
    if sc.startswith("04"): base += [x for i in range(1) for x in ("-v", "org=%s01" % U, "-v", "attr=%s02" % U, "-v", "affected=%s03" % U, "-v", "requester=%s04" % U, "-v", "change_actor=%s05" % U, "-v", "r_ok=%s06" % U, "-v", "r_nomember=%s07" % U, "-v", "r_noreview=%s08" % U, "-v", "r_direct=%s09" % U, "-v", "r_inherited=%s10" % U, "-v", "r_othersrc=%s11" % U, "-v", "r_benef=%s12" % U)]
    return sh(base + ["-f", f], "cci_ap_shim", opts, env)
def sin_check(tree):
    d = tempfile.mkdtemp(prefix="ap_"); t = os.path.join(d, "s"); shutil.copytree(tree, t); g = os.path.join(t, "00_guarda_destino.sql"); s = open(g, encoding="utf-8").read(); s = re.sub(r"  -- @@SP_CHECK_INI@@.*?-- @@SP_CHECK_FIN@@\n", "", s, flags=re.S); open(g, "w", encoding="utf-8").write(s); return t
DIN = []; R = {}
fixtures()
def instala(esq, funcs=True, ops_=True):
    r = {}
    for db in ("cci_ap_shim", "cci_ap_conc"): r[db] = ddl_evil(db, esq, funcs, ops_)
    return r
inst = instala("evil", True, False); R["instalacion_evil_funciones"] = {k: {"funciones_ok": v[0], "fallidas": v[1], "sin_homonimo": v[2]} for k, v in inst.items()}
NEWSC = sin_check(NEW)
def barrido(etq, tree, opts, nuevo, cid, desc):
    for sc in SEIS:
        rc, o = corre(tree, sc, opts, nuevo)
        fn = "HIJACK-FN" in o; op = "HIJACK-OP" in o; rej = bool(re.search(r"ERROR:\s+NO EJECUTADO \[(G-[A-Z-]+)\]", o)); code = (re.search(r"\[(G-[A-Z-]+)\]", o) or [0, ""])[1]
        DIN.append({"id": "%s-%s" % (cid, sc[:2] + (sc[-1] if sc.startswith("05") else "")), "escenario": desc, "arbol": etq, "script": sc, "rc": rc, "guarda_ok": "GUARDA OK" in o, "rechazo": code if rej else "", "hijack_funcion": fn, "hijack_operador": op, "salida_error": (re.search(r"ERROR:[^\n]{0,90}", o) or [""])[0]})
barrido("corregido", NEW, LOC + " -c search_path=evil,pg_catalog,public", True, "SPD1", "search_path hostil (evil primero) con homónimos de TODAS las funciones de pg_catalog usadas (73 funciones, todas las sobrecargas)")
barrido("corregido-sin-chequeo", NEWSC, LOC + " -c search_path=evil,pg_catalog,public", True, "SPD2", "mismo ataque con el chequeo de search_path de la guarda ELIMINADO (aísla la calificación pg_catalog.)")
for lb, pth in OLDL: barrido("anterior:" + lb, pth, LOC + " -c search_path=evil,pg_catalog,public", False, "SPD3-" + lb, "mismo ataque (funciones) contra el árbol anterior " + lb)
for db in ("cci_ap_shim", "cci_ap_conc"): q("drop schema evil cascade", db)
inst = instala("evil", False, True); R["instalacion_evil_operadores"] = {k: {"operadores": v[3]} for k, v in inst.items()}
barrido("corregido", NEW, LOC + " -c search_path=evil,pg_catalog,public", True, "SPD6", "search_path hostil con homónimos de OPERADORES (||, =, <>, ~, !~ sobre text/name/oid/int)")
barrido("corregido-sin-chequeo", NEWSC, LOC + " -c search_path=evil,pg_catalog,public", True, "SPD7", "operadores hostiles con el chequeo de search_path ELIMINADO: los operadores NO van calificados; los cubre el blindaje de sesión de la guarda (search_path de sesión = pg_catalog, public, pg_temp)")
for lb, pth in OLDL: barrido("anterior:" + lb, pth, LOC + " -c search_path=evil,pg_catalog,public", False, "SPD8-" + lb, "operadores hostiles contra el árbol anterior " + lb)
# homónimos en public (esquema permitido): sólo se prueba lo que la calificación puede cubrir
for db in ("cci_ap_shim", "cci_ap_conc"): q("drop schema evil cascade", db)
inst2 = instala("public"); R["instalacion_public"] = {k: {"funciones_ok": v[0], "fallidas": v[1], "operadores": v[3]} for k, v in inst2.items()}
barrido("corregido", NEW, LOC, True, "SPD4", "homónimos de funciones y operadores creados en 'public' (permitido por el chequeo); search_path por defecto")
for lb, pth in OLDL: barrido("anterior:" + lb, pth, LOC, False, "SPD5-" + lb, "ídem contra el árbol anterior " + lb + " (homónimos en public)")
for d in ("cci_ap_shim", "cci_ap_conc"): q("drop database if exists " + d)
shutil.rmtree(os.path.dirname(NEWSC), ignore_errors=True)
R["estatico"] = [{"arbol": a, "funcion": f, "ocurrencias": n} for (a, f), n in sorted(agr.items())]; R["dinamico"] = DIN; R["funciones_catalogo_usadas"] = sorted(usadas)
json.dump(R, open(OUT, "w"), ensure_ascii=False, indent=1)
print("estatico sin calificar:", {k: sum(n for (a, f), n in agr.items() if a == k) for k in set(a for a, f in agr)}); print("instalacion", R["instalacion_evil_funciones"], R["instalacion_evil_operadores"], R["instalacion_public"])
for etq in sorted(set(d["id"].rsplit("-", 1)[0] for d in DIN)):
    xs = [d for d in DIN if d["id"].rsplit("-", 1)[0] == etq]; print(etq, xs[0]["arbol"], "funcion_hijack=%d operador_hijack=%d rechazos=%d guarda_ok=%d de %d" % (sum(d["hijack_funcion"] for d in xs), sum(d["hijack_operador"] for d in xs), sum(bool(d["rechazo"]) for d in xs), sum(d["guarda_ok"] for d in xs), len(xs)))
