#!/usr/bin/env python3
"""Escáner ESTÁTICO (heurístico) de seguridad. NO conecta a ninguna base. No sustituye una revisión humana.
Uso (python3 -I -B):
  ct_escaner_seguridad_sql.py sql <dir_sql> [salida.txt]       # 6 scripts + biblioteca
  ct_escaner_seguridad_sql.py texto <dir_dossier> [salida.txt]  # secretos, credenciales, datos personales, rutas/enlaces inseguros en TODO el dossier
  ct_escaner_seguridad_sql.py autoprueba <salida.txt>           # controles negativos: cada comprobación detecta su defecto en muestras aisladas (tempfile)"""
import re, sys, os, glob, tempfile, shutil
EMAIL_OK = {"noreply@anthropic.com", "t@t"}
def strip(s):
    s = re.sub(r"/\*.*?\*/", "", s, flags=re.S); return "\n".join(re.sub(r"--.*$", "", l) for l in s.splitlines())
def sinlit(code):
    # Los cuerpos entre $$...$$ / $tag$...$tag$ (DO, funciones, SQL de prueba) SE CONSIDERAN CÓDIGO (se escanean); solo se vacían los literales '...'.
    c = re.sub(r"\$\w*\$", " ", code); return re.sub(r"'(?:[^']|'')*'", "''", c)
def escanear_sql(base, raw):
    lib = base.startswith("04_lib"); code = strip(raw); low = code.lower(); nol = sinlit(code).lower(); R = []
    def c(n, ok, d=""): R.append((n, bool(ok), d))
    if base.startswith("00_guarda"):   # archivo de guarda compartido (H-03): se exige identidad efectiva, listas literales, rechazo de PROD y fallo seguro
        cs = set(re.findall(r"current_setting\('([^']+)'", raw))
        c("guarda: identidad efectiva del servidor (pg_control_system)", "pg_control_system" in raw)
        c("guarda: allowlist DEV y denylist PROD literales", "dev_allow" in raw and "prod_deny" in raw)
        c("guarda: allowlist/denylist no se leen de variables de sesión (solo cci.validacion_autorizada y cci.entorno)", cs <= {"cci.validacion_autorizada", "cci.entorno"} and len(cs) == 2)
        c("guarda: rechaza PROD aunque se declare DEV", "G-PROD-RECHAZADO" in raw and "= any(prod_deny)" in raw)
        c("guarda: rechaza destino desconocido y falla cerrada si la identidad no es verificable", "G-DESTINO-DESCONOCIDO" in raw and "G-IDENTIDAD-NO-VERIFICABLE" in raw)
        c("guarda: configuración incompleta o inválida rechazada", "G-CONFIG-INCOMPLETA" in raw and "G-CONFIG-INVALIDA" in raw)
        c("guarda: modo local exige socket Unix, base ^cci_ y ausencia de roles de plataforma", "inet_server_addr" in raw and "^cci_" in raw and "supabase_admin" in raw)
        c("guarda: anti-suplantación (search_path fijo a pg_catalog)", "set_config('search_path','pg_catalog" in raw)
        c("guarda: mensajes sin secretos (solo huella md5 truncada)", "md5(sysid)" in raw and not re.search(r"raise (exception|notice)[^;]*,\s*sysid\b", code, flags=re.I))
    elif not lib:
        inc = re.search(r"^\s*\\ir\s+00_guarda_destino\.sql\s*$", code, re.M)   # índices sobre el código sin comentarios (mismo espacio que low)
        pos = [i for i in (low.find("insert into"), low.find("update "), low.find("pg_sleep"), low.find("delete from")) if i >= 0]
        c("guarda de destino incluida (\\ir 00_guarda_destino.sql)", inc)
        c("guarda antes de cualquier SQL de datos", inc and (not pos or inc.start() < min(pos)))
        c("\\set ON_ERROR_STOP on", "\\set on_error_stop on" in raw.lower())
        c("\\set ON_ERROR_STOP on antes de la guarda (si falta el archivo de guarda el script aborta)", inc and 0 <= low.find("\\set on_error_stop on") < inc.start())
    c("sin COMMIT", not re.search(r"(^|;)\s*commit\s*(;|$)", low, re.M))
    c("sin DDL/DCL peligroso (DROP/TRUNCATE/ALTER/GRANT/REVOKE/CREATE ROLE|EXTENSION|DATABASE|SCHEMA)", not re.search(r"(?<![\w_])(drop\s+(table|schema|database|role|function|trigger|policy)|truncate|alter\s+(table|role|system|database)|grant\s|revoke\s|create\s+(role|extension|database|schema))", nol))
    c("escrituras solo con ROLLBACK", (not re.search(r"\b(insert\s+into|update\s+\w|delete\s+from)", nol)) or "rollback" in low)
    c("sin metacomandos de conexión/shell (\\c, \\connect, \\!, \\copy, \\o)", not re.search(r"^\s*\\(c|connect|!|copy|o|w)\b", code, re.M))
    c("sin refs de proyecto/URL/secretos/JWT", not re.search(r"(eyJ[A-Za-z0-9_-]{20,}|supabase\.(co|com)|sk-[A-Za-z0-9]{20,}|postgres(ql)?://\S+:\S+@|[a-z]{20}\.supabase|service_role_key|password\s*=)", raw, re.I))
    c("sin objetos permanentes (create table/function/trigger/view/index fuera de pg_temp/temp)", not re.search(r"create\s+(or\s+replace\s+)?(table|function|trigger|view|index|unique\s+index)\s+(?!pg_temp|temp|if\s)", nol))
    c("sin LOCK TABLE ni FOR UPDATE/SHARE (bloqueos de producción)", not re.search(r"\block\s+table\b|\bfor\s+(no\s+key\s+)?(update|share)\b", nol))
    c("pg_sleep acotado (<= 10 s)", all(float(x) <= 10 for x in re.findall(r"pg_sleep\(\s*([\d.]+)\s*\)", low)))
    # SQL dinámico
    dyn = re.findall(r"execute\s+format\((.{0,400}?)\)\s*(?:into|using|;)", code, flags=re.S | re.I)
    c("SQL dinámico: format() solo con %I/%L (sin %s sin comillas)", not any(re.search(r"%s", d) for d in dyn), "format(%s) en: " + ",".join(d[:40] for d in dyn if "%s" in d))
    c("SQL dinámico: sin EXECUTE con concatenación '||'", not re.search(r"(?<![\w'])execute\s+[^;]*\|\|", nol, flags=re.I))
    c("SET ROLE solo con %I (nunca literal ni concatenación)", not re.search(r"set\s+(local\s+)?role\s+(?!%i|%\w)", re.sub(r"\$(\w*)\$", "", code), flags=re.I) or "set local role %I" in code)
    # excepciones: WHEN OTHERS solo para clasificar (sqlstate registrado) o exención documentada
    oth = [m.start() for m in re.finditer(r"when\s+others\s+then", code, flags=re.I)]
    malos = []
    for i in oth:
        frag = code[i:i + 260].lower()
        if not ("sqlstate" in frag or "reset role" in code[max(0, i - 120):i].lower()):
            malos.append(code[i:i + 60].replace("\n", " "))
    c("WHEN OTHERS solo clasifica/registra SQLSTATE (o exención documentada de RESET ROLE)", not malos, "; ".join(malos[:3]))
    c("WHEN OTHERS nunca convierte el error en PASS", not re.search(r"when\s+others\s+then[^;]{0,200}'pass'", code, flags=re.I))
    return R
def escanear_texto(rel, data):
    R = []
    def c(n, ok, d=""): R.append((n, bool(ok), d))
    t = data.decode("utf-8", "replace")
    c("sin JWT/claves/tokens", not re.search(r"(eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{10,}|sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{30,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----)", t))
    c("sin cadenas de conexión con credenciales", not re.search(r"postgres(ql)?://[^\s:@/]+:[^\s@/]+@", t))
    em = [e for e in re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", t) if e not in EMAIL_OK]
    c("sin correos electrónicos (datos personales)", not em, ",".join(em[:3]))
    c("sin teléfonos", not re.search(r"(?<![\w.-])(\+\d{1,3}[ ]?)?\(?\d{2,3}\)?[ ]\d{3,4}[ ]\d{4}(?![\w.-])", t))
    c("sin refs de proyecto Supabase (formato ref.supabase.co)", not re.search(r"[a-z0-9]{20}\.supabase\.(co|com)", t))
    return R
def correr_sql(d):
    res = []
    for f in sorted(glob.glob(os.path.join(d, "*.sql"))):
        raw = open(f, encoding="utf-8").read()
        res += [(os.path.basename(f),) + r for r in escanear_sql(os.path.basename(f), raw)]
    return res
def correr_texto(d):
    res = []; prob = []
    for r, ds, fs in os.walk(d, followlinks=False):
        for n in list(ds):
            if os.path.islink(os.path.join(r, n)): prob.append(os.path.relpath(os.path.join(r, n), d)); ds.remove(n)
        for n in fs:
            p = os.path.join(r, n); rel = os.path.relpath(p, d).replace(os.sep, "/")
            if os.path.islink(p): prob.append(rel); continue
            if rel.endswith(".pyc") or "__pycache__" in rel: prob.append(rel); continue
            if os.path.basename(p).startswith("escaner_seguridad_texto"): continue   # salidas de este mismo escáner: se excluyen para que el total no dependa de su presencia
            res += [(rel,) + r_ for r_ in escanear_texto(rel, open(p, "rb").read())]
    res.append(("(árbol)", "sin enlaces simbólicos ni artefactos de Python", not prob, ",".join(prob[:3])))
    return res
def imprimir(res, out):
    fails = sum(1 for r in res if not r[2]); L = ["%s | %s | %s | %s" % ("PASS" if r[2] else "FAIL", r[0], r[1], r[3]) for r in res] + ["TOTAL=%d FAIL=%d" % (len(res), fails)]
    print("\n".join(l for l in L if not l.startswith("PASS") or len(L) < 3 or l.startswith("TOTAL")))
    if out: open(out, "w", encoding="utf-8").write("\n".join(L) + "\n")
    return fails
def autoprueba(out):
    # cada muestra debe disparar EXACTAMENTE la comprobación indicada (y el control limpio ninguna)
    J = "ey" + "J"; AT = "@"
    G = "\\ir 00_guarda_destino.sql\n"
    base = "\\set ON_ERROR_STOP on\n" + G
    muestras = {
     "limpia": (base + "begin read only;\nselect 1;\nrollback;\n", None),
     "COMMIT": (base + "begin;\ncommit;\n", "sin COMMIT"),
     "DROP": (base + "drop table public.x;\n", "sin DDL/DCL peligroso"),
     "TRUNCATE": (base + "truncate public.x;\n", "sin DDL/DCL peligroso"),
     "DROP dentro de DO": (base + "do $$ begin drop table public.x; end $$;\nrollback;\n", "sin DDL/DCL peligroso"),
     "TRUNCATE en SQL de prueba $q$": (base + "select $q$truncate public.x$q$;\nrollback;\n", "sin DDL/DCL peligroso"),
     "GRANT": (base + "grant all on public.x to anon;\n", "sin DDL/DCL peligroso"),
     "insert sin rollback": (base + "insert into t values (1);\n", "escrituras solo con ROLLBACK"),
     "metacomando \\c": (base + "\\c produccion\nselect 1;\nrollback;\n", "sin metacomandos"),
     "JWT": (base + "select '" + J + "hbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9';\nrollback;\n", "sin refs de proyecto"),
     "objeto permanente": (base + "create table public.nueva(id int);\nrollback;\n", "sin objetos permanentes"),
     "FOR UPDATE": (base + "select 1 from t for update;\nrollback;\n", "sin LOCK TABLE"),
     "pg_sleep largo": (base + "select pg_sleep(60);\nrollback;\n", "pg_sleep acotado"),
     "format %s": (base + "do $$ begin execute format('select %s', 1); end $$;\nrollback;\n", "SQL dinámico: format()"),
     "EXECUTE concatenado": (base + "do $$ begin execute 'select ' || 1; end $$;\nrollback;\n", "SQL dinámico: sin EXECUTE"),
     "WHEN OTHERS silencioso": (base + "do $$ begin perform 1; exception when others then null; end $$;\nrollback;\n", "WHEN OTHERS solo clasifica"),
     "WHEN OTHERS => PASS": (base + "do $$ begin perform 1; exception when others then insert into r values ('PASS'); end $$;\nrollback;\n", "WHEN OTHERS nunca"),
     "sin guarda": ("\\set ON_ERROR_STOP on\nbegin read only;\nselect 1;\nrollback;\n", "guarda de destino incluida"),
     "guarda con SQL antes": ("\\set ON_ERROR_STOP on\ninsert into t values (1);\n" + G + "rollback;\n", "guarda antes de cualquier SQL"),
     "sin ON_ERROR_STOP": (G + "begin read only;\nselect 1;\nrollback;\n", "\\set ON_ERROR_STOP on"),
    }
    L = []; fails = 0
    for nom, (sql, esperado) in muestras.items():
        R = escanear_sql("99_muestra.sql", sql); fallos = [n for n, ok, d in R if not ok]
        ok = (not fallos) if esperado is None else any(f.startswith(esperado) for f in fallos)
        fails += (not ok); L.append("%s | SQL | %s | esperado=%s fallos_detectados=%d" % ("PASS" if ok else "FAIL", nom, esperado or "ninguno", len(fallos)))
    GOOD = ("do $guarda$ declare a text := coalesce(current_setting('cci.validacion_autorizada', true),''); e text := coalesce(current_setting('cci.entorno', true),''); dev_allow text[] := array[]::text[]; prod_deny text[] := array[]::text[]; sysid text; fp text;\n"
            "begin perform pg_catalog.set_config('search_path','pg_catalog, pg_temp',true); if a = '' then raise exception 'NO EJECUTADO [G-CONFIG-INCOMPLETA]'; end if; raise exception 'NO EJECUTADO [G-CONFIG-INVALIDA]';\n"
            "begin select system_identifier::text into sysid from pg_catalog.pg_control_system(); exception when others then sysid := null; fp := sqlstate; end; if sysid is null then raise exception 'NO EJECUTADO [G-IDENTIDAD-NO-VERIFICABLE]'; end if;\n"
            "fp := left(md5(sysid), 8); if sysid = any(prod_deny) then raise exception 'NO EJECUTADO [G-PROD-RECHAZADO] %', fp; end if; if not (sysid = any(dev_allow)) then raise exception 'NO EJECUTADO [G-DESTINO-DESCONOCIDO]'; end if;\n"
            "if inet_server_addr() is not null or current_database() !~ '^cci_' or exists (select 1 from pg_catalog.pg_roles where rolname = 'supabase_admin') then raise exception 'x'; end if; end $guarda$;\n")
    mg = {"limpia": (GOOD, None), "sin identidad efectiva": (GOOD.replace("pg_control_system", "otra_fuente"), "guarda: identidad efectiva"), "sin denylist": (GOOD.replace("prod_deny", "x_deny"), "guarda: allowlist DEV y denylist"),
          "allowlist desde variable de sesión": (GOOD.replace("sysid is null", "sysid is null or current_setting('cci.dev_allow', true) <> ''") + "select current_setting('cci.dev_allow', true);\n", "guarda: allowlist/denylist no se leen"),
          "sin rechazo de PROD": (GOOD.replace("G-PROD-RECHAZADO", "G-X"), "guarda: rechaza PROD"), "sin fallo cerrado": (GOOD.replace("G-IDENTIDAD-NO-VERIFICABLE", "G-X"), "guarda: rechaza destino desconocido"),
          "sin validar configuración": (GOOD.replace("G-CONFIG-INVALIDA", "G-X"), "guarda: configuración incompleta"), "sin controles locales": (GOOD.replace("supabase_admin", "otro"), "guarda: modo local"),
          "sin anti-suplantación": (GOOD.replace("set_config('search_path','pg_catalog", "set_config('otra','pg_catalog"), "guarda: anti-suplantación"), "mensaje con identificador completo": (GOOD.replace("%', fp;", "%', sysid;"), "guarda: mensajes sin secretos")}
    for nom, (sql, esperado) in mg.items():
        R = escanear_sql("00_guarda_destino.sql", sql); fallos = [n for n, ok, d in R if not ok]
        ok = (not fallos) if esperado is None else any(f.startswith(esperado) for f in fallos)
        fails += (not ok); L.append("%s | GUARDA | %s | esperado=%s fallos_detectados=%d%s" % ("PASS" if ok else "FAIL", nom, esperado or "ninguno", len(fallos), (" (" + ",".join(fallos[:2]) + ")") if (esperado is None and fallos) else ""))
    textos = {"limpio": (b"nada sensible\n", None), "JWT": (("token " + J + "hbGciOiJIUzI1NiIsInR5cCI6.abcdefghijk1234\n").encode(), "sin JWT"), "URI con credenciales": (("postgresql:" + "//usr:pass" + AT + "host/db\n").encode(), "sin cadenas"),
              "correo": (("contacto juan" + AT + "empresa.com\n").encode(), "sin correos"), "teléfono": (("llamar 55" + " 1234" + " 5678\n").encode(), "sin teléfonos"), "project ref": (("abcdefghijklmnopqrst" + ".supabase" + ".co\n").encode(), "sin refs")}
    for nom, (b, esperado) in textos.items():
        R = escanear_texto("x.txt", b); fallos = [n for n, ok, d in R if not ok]; ok = (not fallos) if esperado is None else any(f.startswith(esperado) for f in fallos)
        fails += (not ok); L.append("%s | TEXTO | %s | esperado=%s" % ("PASS" if ok else "FAIL", nom, esperado or "ninguno"))
    tmp = tempfile.mkdtemp(prefix="ctesc_")
    try:
        open(os.path.join(tmp, "a.txt"), "w").write("x"); os.symlink("/etc/passwd", os.path.join(tmp, "enlace"))
        R = correr_texto(tmp); ok = any((not r[2]) and r[1].startswith("sin enlaces") for r in R); fails += (not ok); L.append("%s | ÁRBOL | enlace simbólico detectado" % ("PASS" if ok else "FAIL"))
    finally: shutil.rmtree(tmp)
    s = "AUTOPRUEBA DEL ESCÁNER (muestras aisladas en memoria/tempfile)\n" + "\n".join(L) + "\nTOTAL=%d FAIL=%d\n" % (len(L), fails)
    print(s); open(out, "w", encoding="utf-8").write(s); return fails
if __name__ == "__main__":
    m = sys.argv[1]
    if m == "sql": sys.exit(1 if imprimir(correr_sql(sys.argv[2]), sys.argv[3] if len(sys.argv) > 3 else None) else 0)
    if m == "texto": sys.exit(1 if imprimir(correr_texto(sys.argv[2]), sys.argv[3] if len(sys.argv) > 3 else None) else 0)
    if m == "autoprueba": sys.exit(1 if autoprueba(sys.argv[2]) else 0)
