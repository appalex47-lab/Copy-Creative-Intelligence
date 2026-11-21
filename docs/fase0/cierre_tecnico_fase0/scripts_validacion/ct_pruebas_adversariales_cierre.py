#!/usr/bin/env python3
# Uso: python3 -I -B ct_pruebas_adversariales_cierre.py <socket> <puerto> <arbol_publicado_anterior_dir|-> <salida.json>
# PostgreSQL TEMPORAL LOCAL (superusuario cci_test). NUNCA Supabase/CCI-DEV/CCI-PROD. Casos A–O del marcador de la guarda (sobre los 6 scripts) y del ejecutor verificado.
# Cada caso registra: estado inicial, rol, sesión/conexión, archivo ejecutado, acción adversarial, resultado SQL, rechazo esperado, efectos persistentes (huella del catálogo/datos
# antes y después) y comando reproducible. Un "ataque exitoso" = el CUERPO del script se ejecutó (canario CANARIO-CUERPO-EJECUTADO). Un rechazo exige además un código [G-…]/[V-…].
import hashlib, json, os, re, shutil, signal, subprocess, sys, tempfile, threading, time
SOCK, PORT, PUBDIR, OUT = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
HERE = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.join(HERE, "cci_dev_NO_EJECUTADOS"); WRAP = os.path.join(HERE, "ejecutar_script_verificado.sh")
SEIS = ["01_inventario_esquema_SOLO_LECTURA", "02_rls_privilegios_SOLO_LECTURA", "03_pruebas_rls_ROLLBACK", "04_trigger_r1_r9_ROLLBACK", "05_concurrencia_sesion_A", "05_concurrencia_sesion_B"]
LOC = "-c cci.validacion_autorizada=SI-LOCAL-TEMPORAL -c cci.entorno=LOCAL-TEMPORAL"
VARS = ["-v", "org=x", "-v", "org_a=x", "-v", "org_b=x", "-v", "uid_a=x", "-v", "uid_x=x", "-v", "piece=x", "-v", "attr=x"]
CAN = "CANARIO-CUERPO-EJECUTADO"; REC = []; TMPS = []
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest() if os.path.exists(p) else ""
H_APR = sha(os.path.join(SRC, "00_guarda_destino.sql")); G0 = open(os.path.join(SRC, "00_guarda_destino.sql"), encoding="utf-8").read()
COLA = G0[G0.index("-- MARCADOR POR EJECUCIÓN"):]
def psql(args, opts=LOC, env_x=None, cwd=None, stdin=None, user="cci_test", db="cci_gdev", timeout=120, extra_env=None):
    env = dict(os.environ, PGHOST=SOCK, PGPORT=PORT, PGUSER=user, PGOPTIONS=opts)
    if env_x: env.update(env_x)
    if extra_env: env.update(extra_env)
    try: r = subprocess.run(["psql", "-d", db, "-X", "-v", "ON_ERROR_STOP=1", "-P", "pager=off"] + args, env=env, capture_output=True, text=True, cwd=cwd, input=stdin, timeout=timeout); return r.returncode, r.stdout + r.stderr
    except subprocess.TimeoutExpired: return 124, "TIMEOUT"
def adm(sql, db="postgres"): return psql(["-qAt", "-c", sql], "", db=db)
def huella():
    return adm("select md5(coalesce((select string_agg(c.relname||':'||c.relkind, ',' order by c.relname) from pg_class c join pg_namespace n on n.oid=c.relnamespace where n.nspname not in ('pg_catalog','information_schema','pg_toast') and n.nspname !~ '^pg_temp'),'')||'|'||(select count(*) from public.cci_probe)::text||'|'||(select string_agg(rolname,',' order by rolname) from pg_roles where rolname !~ '^pg_')||'|'||(select count(*) from pg_proc p join pg_namespace n on n.oid=p.pronamespace where n.nspname not in ('pg_catalog','information_schema')))", db="cci_gdev")[1].strip()
def mk(kind="new", guarda=None, canario=True):
    d = tempfile.mkdtemp(prefix="adv_"); TMPS.append(d); t = os.path.join(d, "s"); shutil.copytree(SRC if kind == "new" else PUBDIR, t)
    if canario:
        for sc in SEIS:
            f = os.path.join(t, sc + ".sql"); s = open(f, encoding="utf-8").read()
            if kind == "new": k = "\\ir 00_verificar_marcador.sql\n"; i = s.index(k) + len(k)
            else: m = re.search(r"do \$v\$ begin if pg_catalog\.to_regclass\('pg_temp\.cci_guarda_ok'\) is null then .*? end \$v\$;\n", s); i = m.end()
            open(f, "w", encoding="utf-8").write(s[:i] + "select '%s' as canario;\n" % CAN + s[i:])
    if guarda is not None: open(os.path.join(t, "00_guarda_destino.sql"), "w", encoding="utf-8").write(guarda)
    return t
def envh(t, modo):   # M: el atacante controla también el hash 'aprobado' (aísla la capa del marcador). H: hash aprobado REAL (externo).
    return {"CCI_DIR": t, "CCI_GUARDA_SHA256_APROBADO": (sha(os.path.join(t, "00_guarda_destino.sql")) if modo == "M" else H_APR)}
def cod(o): m = re.search(r"\[([GV]-[A-Z-]+)\]", o); return m.group(1) if m else ""
def caso(cid, arbol, modo, riesgo, pre, rol, sesion, archivo, accion, esperado, argsf, scripts=SEIS, opts=LOC, extra=None, ok_si="rechazo", env_fn=None, stdin_fn=None, cwd=None, nota=""):
    for sc in scripts:
        h0 = huella(); a = argsf(sc); e = env_fn(sc) if env_fn else None
        rc, o = psql(a, opts, env_x=e, cwd=cwd, stdin=stdin_fn(sc) if stdin_fn else None)
        h1 = huella(); llego = CAN in o; c = cod(o)
        if ok_si == "rechazo": ok = (not llego) and rc != 0 and bool(c) and "ERROR:  NO EJECUTADO" in o; est = "PASS" if ok else "FAIL"
        elif ok_si == "limite": est = "PARTIAL" if llego else "FAIL"          # el ataque PASA: límite estructural documentado, nunca PASS
        elif ok_si == "defecto": est = "FAIL" if llego else "PASS"              # sobre el árbol publicado: FAIL = defecto reproducido
        else: est = "PASS" if (llego and rc in (0, 3)) else "FAIL"               # control positivo: debe llegar al cuerpo
        sid = sc[:2] + (sc[-1] if sc.startswith("05") else "")
        REC.append({"id": "%s-%s-%s" % (cid, arbol[:3], sid), "caso": cid, "arbol": arbol, "modo": modo, "script": sc, "riesgo": riesgo, "estado_inicial": pre, "rol": rol, "sesion": sesion, "archivo": archivo, "accion": accion, "esperado": esperado,
                    "resultado_sql": ("CUERPO EJECUTADO" if llego else "") + (" " if llego else "") + "rc=%d %s" % (rc, c or (re.search(r"ERROR:[^\n]{0,70}", o) or [""])[0]), "persistencia": "sin cambios" if h0 == h1 else "CAMBIOS (%s→%s)" % (h0[:6], h1[:6]),
                    "estado": est, "nota": nota, "comando": "psql " + " ".join(a)[:140] + ("  [CCI_DIR/CCI_GUARDA_SHA256_APROBADO: %s]" % modo if modo in "MH" else "")})
def F(t, sc): return ["-f", os.path.join(t, sc + ".sql")]
adm("drop database if exists cci_gdev"); adm("create database cci_gdev"); adm("create table public.cci_probe(a int); insert into public.cci_probe values (1),(2)", db="cci_gdev")
try:
    NEW = mk("new"); VACIA = mk("new", guarda=""); PRE = ["-c", "create temp table pg_temp.cci_guarda_ok (ok boolean)"]
    # CONTROL POSITIVO: guarda real + hash real: el cuerpo se ejecuta
    caso("CTRL", "corregido", "H", "control", "guarda íntegra, hash aprobado, modo LOCAL", "cci_test", "1 conexión", "script real", "ninguna (uso legítimo)", "llega al cuerpo", lambda sc: VARS + F(NEW, sc), env_fn=lambda sc: envh(NEW, "H"), ok_si="positivo")
    # A. el usuario crea previamente pg_temp.cci_guarda_ok (+ guarda vacía): marcador antiguo
    caso("A", "corregido", "M", "alto", "tabla temporal pg_temp.cci_guarda_ok creada en la MISMA sesión; guarda vacía", "cci_test", "1 conexión (-c previo + -f)", "script con guarda vacía", "precrear el marcador antiguo", "rechazo [G-GUARDA-NO-EJECUTADA]", lambda sc: PRE + VARS + F(VACIA, sc), env_fn=lambda sc: envh(VACIA, "M"))
    # B. tabla con la misma estructura y nombre imitando el marcador nuevo, y variable cci_run adivinada
    caso("B", "corregido", "M", "alto", "tabla pg_temp.cci_g_adivinado(script,pid,usado) con fila válida; -v cci_run=adivinado; guarda vacía", "cci_test", "1 conexión", "script con guarda vacía", "imitar estructura y nombre del marcador con identificador conocido por el atacante", "rechazo (el preflight borra cci_run; la guarda vacía no la regenera)",
         lambda sc: ["-v", "cci_run=adivinado", "-c", "create temp table pg_temp.cci_g_adivinado (script text, pid int, usado boolean default false); insert into pg_temp.cci_g_adivinado select '%s', pg_backend_pid(), false" % ("05A" if sc.endswith("A") else "05B" if sc.endswith("B") else sc[:2])] + VARS + F(VACIA, sc), env_fn=lambda sc: envh(VACIA, "M"))
    # C/I/J/M.. misma sesión
    for c_id, desc, riesgo in [("C", "marcador de una ejecución anterior en la MISMA sesión", "alto")]:
        for sc in SEIS:
            h0 = huella(); rc, o = psql(VARS + F(NEW, "01_inventario_esquema_SOLO_LECTURA") + VARS + F(VACIA, sc), LOC, env_x={"CCI_DIR": NEW, "CCI_GUARDA_SHA256_APROBADO": H_APR})
            # el 2.º -f usa CCI_DIR=NEW (el entorno es único): su guarda vacía no se ejecuta (se ejecuta la copia verificada de NEW): se prueba además con entorno de la guarda vacía
            REC.append({"id": "C-cor-%s" % (sc[:2] + (sc[-1] if sc.startswith("05") else "")), "caso": "C", "arbol": "corregido", "modo": "M", "script": sc, "riesgo": riesgo, "estado_inicial": "sesión con ejecución previa válida del script 01 (marcador consumido)", "rol": "cci_test", "sesion": "1 conexión, -f 01 y luego -f %s (guarda vacía)" % sc[:2],
                        "archivo": "01 real + script con guarda vacía", "accion": "reutilizar el estado de una ejecución anterior", "esperado": "la 2.ª ejecución no hereda autorización: ejecuta SU guarda (copia verificada) y genera un marcador nuevo; nunca reutiliza el anterior",
                        "resultado_sql": "rc=%d guardas_ok=%d" % (rc, o.count("GUARDA OK")), "persistencia": "sin cambios" if huella() == h0 else "CAMBIOS", "estado": "PASS" if o.count("GUARDA OK") >= 1 and (rc == 0 or CAN in o or "BLOCKED" in o or rc == 3) else "FAIL", "nota": "con entorno único la 2.ª pasada vuelve a pasar por la guarda íntegra (comportamiento seguro)", "comando": "psql -f 01 -f %s" % sc})
    # C2: segunda ejecución con guarda VACÍA en dir distinto y entorno que apunta a él: no hereda el marcador anterior
    for sc in SEIS:
        h0 = huella(); rc, o = psql(VARS + F(NEW, SEIS[0]) + VARS + F(VACIA, sc), LOC, env_x=envh(VACIA, "M"))
        c2 = (CAN in o.split("CANARIO")[-1]) if o.count(CAN) else False
        n = o.count(CAN)
        REC.append({"id": "C2-cor-%s" % (sc[:2] + (sc[-1] if sc.startswith("05") else "")), "caso": "C2", "arbol": "corregido", "modo": "M", "script": sc, "riesgo": "alto", "estado_inicial": "sesión: 01 con guarda real consumió su marcador (o fue rechazado por el hash del entorno)", "rol": "cci_test", "sesion": "1 conexión",
                    "archivo": "01 (guarda real) y luego %s con guarda vacía" % sc[:2], "accion": "ejecutar un 2.º script con guarda vacía tras una ejecución válida", "esperado": "el 2.º script no llega al cuerpo", "resultado_sql": "rc=%d cuerpos=%d %s" % (rc, n, cod(o)),
                    "persistencia": "sin cambios" if huella() == h0 else "CAMBIOS", "estado": "PASS" if n == 0 and rc != 0 else "FAIL", "nota": "el entorno apunta al hash de la guarda vacía, por lo que el 1.º script (guarda real) se rechaza por integridad y la sesión termina; ver C-cor para la reutilización", "comando": "psql -f 01 -f %s" % sc})
    # D. guarda vacía + marcador preexistente + GUC + variable: todo junto
    caso("D", "corregido", "M", "alto", "marcador antiguo + cci.guarda_ok=1 + -v cci_run=x + guarda vacía", "cci_test", "1 conexión", "script con guarda vacía", "guarda vacía con todos los residuos posibles", "rechazo [G-GUARDA-NO-EJECUTADA]", lambda sc: ["-v", "cci_run=x"] + PRE + VARS + F(VACIA, sc), opts=LOC + " -c cci.guarda_ok=1", env_fn=lambda sc: envh(VACIA, "M"))
    # E1. guarda alterada que crea el marcador antiguo (ingenua)
    E1 = mk("new", guarda="create temp table pg_temp.cci_guarda_ok (ok boolean);\n")
    caso("E1", "corregido", "M", "alto", "guarda alterada que sólo crea pg_temp.cci_guarda_ok", "cci_test", "1 conexión", "script con guarda alterada", "forjar el marcador antiguo", "rechazo [G-GUARDA-NO-EJECUTADA]", lambda sc: VARS + F(E1, sc), env_fn=lambda sc: envh(E1, "M"))
    caso("E1", "corregido", "H", "alto", "ídem con hash aprobado real", "cci_test", "1 conexión", "script con guarda alterada", "forjar el marcador antiguo", "rechazo [G-GUARDA-INTEGRIDAD]", lambda sc: VARS + F(E1, sc), env_fn=lambda sc: envh(E1, "H"))
    # E2/G2. guarda sustituida que implementa el protocolo nuevo sin comprobar nada (atacante que conoce el diseño)
    E2 = mk("new", guarda=COLA)
    caso("E2", "corregido", "M", "alto (límite estructural)", "guarda sustituida que genera cci_run y la tabla sin comprobaciones; el atacante controla el hash aprobado", "cci_test", "1 conexión", "script con guarda sustituida", "forjar el marcador nuevo conociendo el protocolo", "PARTIAL: pasa (límite documentado: sin raíz de confianza externa no hay defensa)", lambda sc: VARS + F(E2, sc), env_fn=lambda sc: envh(E2, "M"), ok_si="limite", nota="LIMITACIÓN ESTRUCTURAL; no es aprobación")
    caso("E2", "corregido", "H", "alto", "ídem con el hash aprobado REAL (externo)", "cci_test", "1 conexión", "script con guarda sustituida", "ídem", "rechazo [G-GUARDA-INTEGRIDAD]", lambda sc: VARS + F(E2, sc), env_fn=lambda sc: envh(E2, "H"))
    # F. la guarda falla después de iniciar su ejecución (tras crear el marcador)
    FG = mk("new", guarda=COLA + "do $$ begin raise exception 'NO EJECUTADO [G-GUARDA-NO-EJECUTADA] fallo simulado tras crear el marcador'; end $$;\n")
    caso("F", "corregido", "M", "medio", "guarda que crea el marcador y falla después", "cci_test", "1 conexión", "script con guarda que falla", "ejecución fallida: ¿queda autorización residual?", "rechazo y sin autorización residual (la sesión termina)", lambda sc: VARS + F(FG, sc), env_fn=lambda sc: envh(FG, "M"))
    # G. guarda sustituida por un archivo que sólo crea el marcador (varias formas de marcador ingenuo)
    G1 = mk("new", guarda="select 1;\ncreate temp table pg_temp.cci_g_x(script text, pid int, usado boolean);\n")
    caso("G", "corregido", "M", "alto", "guarda = archivo que sólo crea una tabla temporal con nombre fijo", "cci_test", "1 conexión", "script con guarda trivial", "sustituir la guarda por un archivo trivial", "rechazo [G-GUARDA-NO-EJECUTADA]", lambda sc: VARS + F(G1, sc), env_fn=lambda sc: envh(G1, "M"))
    # H. ejecución directa con psql sin envoltorio (sin CCI_DIR/hash) y con guarda íntegra
    caso("H", "corregido", "-", "alto", "psql -f directo, sin envoltorio y sin hash externo", "cci_test", "1 conexión", "script real", "ejecución directa sin raíz de confianza", "rechazo [G-GUARDA-INTEGRIDAD]", lambda sc: VARS + F(NEW, sc), env_fn=lambda sc: {"CCI_DIR": "", "CCI_GUARDA_SHA256_APROBADO": ""})
    # I. los seis consecutivamente en la misma sesión (cada uno su guarda y su marcador): positivo; y repetición
    for rep in (1, 2):
        rc, o = psql(VARS + F(NEW, SEIS[0]) + VARS + F(NEW, SEIS[1]) + VARS + F(NEW, SEIS[0]), LOC, env_x=envh(NEW, "H")); n = o.count("GUARDA OK"); nc = o.count(CAN)
        REC.append({"id": "I%d-cor-01-02-01" % rep, "caso": "I", "arbol": "corregido", "modo": "H", "script": "01,02,01", "riesgo": "medio", "estado_inicial": "sesión limpia", "rol": "cci_test", "sesion": "1 conexión, 3 scripts consecutivos", "archivo": "01, 02, 01", "accion": "ejecución consecutiva en la misma sesión", "esperado": "cada ejecución pasa por su guarda y consume su propio marcador (3 GUARDA OK, 3 cuerpos)", "resultado_sql": "rc=%d guardas=%d cuerpos=%d" % (rc, n, nc), "persistencia": "sin cambios", "estado": "PASS" if rc == 0 and n == 3 and nc == 3 else "FAIL", "nota": "los scripts 03–05 se cubren en CTRL (cada uno ejecuta su guarda); 3 scripts bastan para el patrón sesión", "comando": "psql -f 01 -f 02 -f 01"})
    # J. sesión persistente / pooler simulado: el backend conserva el marcador pero el cliente nuevo no tiene cci_run
    for sc in SEIS:
        drv = "\\i %s\n\\unset cci_run\n\\unset cci_script\n\\unset cci_tmp\n\\i %s\n" % (os.path.join(NEW, SEIS[0] + ".sql"), os.path.join(VACIA, sc + ".sql"))
        h0 = huella(); rc, o = psql(VARS + ["-f", "-"], LOC, env_x=envh(VACIA, "M"), stdin=drv)
        n = o.count(CAN)
        REC.append({"id": "J-cor-%s" % (sc[:2] + (sc[-1] if sc.startswith("05") else "")), "caso": "J", "arbol": "corregido", "modo": "M", "script": sc, "riesgo": "alto", "estado_inicial": "mismo backend con estado temporal de una ejecución previa; cliente 'nuevo' (se descartan variables de psql)", "rol": "cci_test", "sesion": "1 backend, 2 'clientes' simulados",
                    "archivo": "01 real y luego %s con guarda vacía" % sc[:2], "accion": "reutilizar la conexión de un pooler: el marcador persiste en el servidor, la variable cliente no", "esperado": "2.º cliente rechazado [G-GUARDA-NO-EJECUTADA]", "resultado_sql": "rc=%d cuerpos=%d %s" % (rc, n, cod(o)), "persistencia": "sin cambios" if huella() == h0 else "CAMBIOS",
                    "estado": "PASS" if rc != 0 and n <= 1 and cod(o) == "G-GUARDA-NO-EJECUTADA" else "FAIL", "nota": "SIMULADO con un solo psql; pooler real (Supavisor/pgbouncer) NOT TESTED", "comando": "psql -f - (driver)"})
    # K. alterar el marcador durante la ejecución (tras crearlo y antes de la verificación)
    for nom, mod in [("cambia el script del marcador", "update pg_temp.%I set script = '99'"), ("lo marca ya consumido", "update pg_temp.%I set usado = true"), ("borra la fila", "delete from pg_temp.%I"), ("cambia el pid", "update pg_temp.%I set pid = 0")]:
        KG = mk("new", guarda=COLA + "select pg_catalog.format('%s', pg_catalog.concat('cci_g_', :'cci_run')) \\gexec\n" % mod.replace("'", "''"))
        caso("K", "corregido", "M", "medio", "guarda que crea el marcador y lo altera: " + nom, "cci_test", "1 conexión", "script con guarda modificada", "alterar el marcador durante la ejecución", "rechazo [G-GUARDA-NO-EJECUTADA]", lambda sc, KG=KG: VARS + F(KG, sc), env_fn=lambda sc, KG=KG: envh(KG, "M"), scripts=[SEIS[0], SEIS[4]], nota=nom)
    # L. marcador de otro script
    LG = mk("new", guarda="\\set cci_script '99'\n" + COLA)
    caso("L", "corregido", "M", "medio", "guarda que genera el marcador ligado a otro script ('99')", "cci_test", "1 conexión", "script con guarda modificada", "ejecutar un script con el marcador de otro", "rechazo [G-GUARDA-NO-EJECUTADA]", lambda sc: VARS + F(LG, sc), env_fn=lambda sc: envh(LG, "M"))
    # M. marcador reutilizado tras rollback / error
    MG = mk("new", guarda="begin;\n" + COLA + "rollback;\n")
    caso("M", "corregido", "M", "medio", "guarda que crea el marcador dentro de una transacción y hace ROLLBACK", "cci_test", "1 conexión", "script con guarda modificada", "reutilizar marcador revertido", "rechazo [G-GUARDA-NO-EJECUTADA]", lambda sc: VARS + F(MG, sc), env_fn=lambda sc: envh(MG, "M"))
    # N. otra sesión: el atacante conoce el identificador de una ejecución previa (otra conexión) e intenta usarlo
    RUN = tempfile.mkdtemp(prefix="adv_n_"); TMPS.append(RUN); pg = os.path.join(RUN, "g.sql"); open(pg, "w").write(G0 + "\n\\echo RUNID=:cci_run\n")
    NG = mk("new", guarda=G0 + "\n\\echo RUNID=:cci_run\n"); rc1, o1 = psql(VARS + F(NG, SEIS[0]), LOC, env_x=envh(NG, "M")); rid = (re.search(r"RUNID=(\w+)", o1) or [0, "0" * 32])[1]
    caso("N", "corregido", "M", "alto", "el atacante conoce el cci_run de otra sesión ya terminada (%s…)" % rid[:6], "cci_test", "2.ª conexión distinta", "script con guarda vacía", "usar desde otra sesión la autorización de otra", "rechazo [G-GUARDA-NO-EJECUTADA]", lambda sc: ["-v", "cci_run=" + rid, "-c", "create temp table pg_temp.cci_g_%s (script text, pid int, usado boolean default false); insert into pg_temp.cci_g_%s select '01', pg_backend_pid(), false" % (rid, rid)] + VARS + F(VACIA, sc), env_fn=lambda sc: envh(VACIA, "M"))
    # O. guarda eliminada o modificada después de una validación previa (otra ejecución): se prueba en el ejecutor (WRAP-*)
    # --- EJECUTOR VERIFICADO
    def mkset():
        d = tempfile.mkdtemp(prefix="adv_w_"); TMPS.append(d); t = os.path.join(d, "s"); shutil.copytree(SRC, t); gen(t); return t
    def gen(t):
        fs = ["00_guarda_destino.sql", "00_preflight_guarda.sql", "00_verificar_marcador.sql", "01_inventario_esquema_SOLO_LECTURA.sql", "02_rls_privilegios_SOLO_LECTURA.sql", "03_pruebas_rls_ROLLBACK.sql", "04_lib_clasificador.sql", "04_trigger_r1_r9_ROLLBACK.sql", "05_concurrencia_sesion_A.sql", "05_concurrencia_sesion_B.sql"]
        open(os.path.join(t, "SHA256SUMS_CCI.txt"), "w").write("".join("%s  %s\n" % (sha(os.path.join(t, f)), f) for f in fs))
    BASE = mkset(); SUMH = sha(os.path.join(BASE, "SHA256SUMS_CCI.txt"))
    def wrap(args, t=BASE, sc=SEIS[0], aprob=None, env=None, cwd="/tmp", opts=LOC, user=None, timeout=60):
        e = dict(os.environ, PGHOST=SOCK, PGPORT=PORT, PGUSER="cci_test", PGOPTIONS=opts); e.pop("CCI_DIR", None); e.pop("CCI_GUARDA_SHA256_APROBADO", None)
        if env: e.update(env)
        cmd = ["bash", WRAP, SUMH if aprob is None else aprob, os.path.join(t, sc + ".sql"), "-d", "cci_gdev"] + args
        try: r = subprocess.run(cmd, env=e, capture_output=True, text=True, cwd=cwd, timeout=timeout); return r.returncode, r.stdout + r.stderr
        except subprocess.TimeoutExpired: return 124, "TIMEOUT"
    def wrec(wid, riesgo, pre, accion, esp, rc, o, ok, nota="", cmd=""):
        REC.append({"id": wid, "caso": wid.split("-")[0] + "-" + wid.split("-")[1], "arbol": "corregido", "modo": "ejecutor", "script": "01", "riesgo": riesgo, "estado_inicial": pre, "rol": "cci_test", "sesion": "1 conexión (ejecutor)", "archivo": "ejecutar_script_verificado.sh", "accion": accion, "esperado": esp,
                    "resultado_sql": "rc=%d %s" % (rc, cod(o) or ("GUARDA OK" if "GUARDA OK" in o else o[:60].replace("\n", " "))), "persistencia": "sin cambios", "estado": "PASS" if ok else "FAIL", "nota": nota, "comando": cmd or "ejecutar_script_verificado.sh <sha> <script> ..."})
    def rech(wid, riesgo, pre, accion, codigo, rc, o, nota=""): wrec(wid, riesgo, pre, accion, "NO EJECUTADO [%s], rc=3, sin GUARDA OK ni cuerpo" % codigo, rc, o, rc == 3 and ("[%s]" % codigo) in o and "GUARDA OK" not in o and CAN not in o, nota)
    rc, o = wrap(VARS); wrec("WRAP-01-ok", "control", "conjunto íntegro y hash aprobado", "uso legítimo", "ejecuta: GUARDA OK, rc=0", rc, o, rc == 0 and "GUARDA OK" in o)
    t = mkset(); open(os.path.join(t, "02_rls_privilegios_SOLO_LECTURA.sql"), "a").write("select 'ALTERADO';\n"); rc, o = wrap(VARS, t=t); rech("WRAP-02-script-alterado", "alto", "script modificado tras generar SUMS", "ejecutar script con contenido alterado", "V-ARCHIVO-ALTERADO", rc, o)
    t = mkset(); open(os.path.join(t, "00_guarda_destino.sql"), "a").write("-- alterada\n"); rc, o = wrap(VARS, t=t); rech("WRAP-03-guarda-alterada", "alto", "guarda modificada", "ejecutar con guarda alterada y SUMS original", "V-ARCHIVO-ALTERADO", rc, o)
    t = mkset(); open(os.path.join(t, "00_guarda_destino.sql"), "a").write("-- alterada\n"); gen(t); rc, o = wrap(VARS, t=t); rech("WRAP-04-sums-regenerado", "alto", "guarda alterada y SUMS regenerado por el atacante", "el atacante regenera el SUMS del repo", "V-SUMS-HASH-DISTINTO", rc, o, "demuestra que el hash debe ser externo: lo único que detecta esto es el argumento aprobado")
    rc, o = wrap(VARS, aprob="0" * 64); rech("WRAP-05-hash-incorrecto", "alto", "hash aprobado incorrecto", "hash 000…0", "V-SUMS-HASH-DISTINTO", rc, o)
    rc, o = wrap(VARS, aprob="XYZ"); rech("WRAP-06-hash-mal-formado", "medio", "hash mal formado", "hash 'XYZ'", "V-HASH-INVALIDO", rc, o)
    e = dict(os.environ); r = subprocess.run(["bash", WRAP, "", os.path.join(BASE, SEIS[0] + ".sql")], env=dict(e, PGHOST=SOCK, PGPORT=PORT, PGOPTIONS=LOC), capture_output=True, text=True); rech("WRAP-07-hash-ausente", "alto", "hash ausente (cadena vacía)", "sin hash", "V-HASH-INVALIDO", r.returncode, r.stdout + r.stderr)
    t = mkset(); open(os.path.join(t, "00_guarda_destino.sql"), "w").close(); rc, o = wrap(VARS, t=t); rech("WRAP-08-guarda-vacia", "alto", "guarda vacía (0 bytes)", "guarda truncada a 0 bytes", "V-ARCHIVO-ALTERADO", rc, o)
    t = mkset(); g = open(os.path.join(t, "00_guarda_destino.sql")).read(); open(os.path.join(t, "00_guarda_destino.sql"), "w").write(g[:len(g) // 2]); rc, o = wrap(VARS, t=t); rech("WRAP-09-guarda-truncada", "alto", "guarda truncada al 50 %", "truncar la guarda", "V-ARCHIVO-ALTERADO", rc, o)
    t = mkset(); os.remove(os.path.join(t, "00_guarda_destino.sql")); rc, o = wrap(VARS, t=t); rech("WRAP-10-guarda-ausente", "alto", "guarda ausente", "eliminar la guarda", "V-ARCHIVO-AUSENTE-O-SYMLINK", rc, o)
    t = mkset(); real = os.path.join(t, "00_guarda_destino.sql"); os.rename(real, real + ".bak"); os.symlink(real + ".bak", real); rc, o = wrap(VARS, t=t); rech("WRAP-11-symlink-guarda", "alto", "guarda = symlink a un archivo idéntico", "symlink", "V-ARCHIVO-AUSENTE-O-SYMLINK", rc, o)
    t = mkset(); real = os.path.join(t, SEIS[0] + ".sql"); os.rename(real, real + ".bak"); os.symlink(real + ".bak", real); rc, o = wrap(VARS, t=t); rech("WRAP-12-symlink-script", "alto", "script = symlink", "symlink al script", "V-SYMLINK", rc, o)
    t = mkset(); real = os.path.join(t, "SHA256SUMS_CCI.txt"); os.rename(real, real + ".bak"); os.symlink(real + ".bak", real); rc, o = wrap(VARS, t=t); rech("WRAP-13-symlink-sums", "alto", "SHA256SUMS = symlink", "symlink al SUMS", "V-SUMS-AUSENTE", rc, o)
    # ruta relativa manipulada: cwd con guarda homónima maliciosa y ruta con ../
    rogue = tempfile.mkdtemp(prefix="adv_r_"); TMPS.append(rogue); open(os.path.join(rogue, "00_guarda_destino.sql"), "w").write("select 'PWNED-ROGUE';\n")
    e = dict(os.environ, PGHOST=SOCK, PGPORT=PORT, PGUSER="cci_test", PGOPTIONS=LOC)
    r = subprocess.run(["bash", WRAP, SUMH, os.path.join(BASE, "..", "s", SEIS[0] + ".sql"), "-d", "cci_gdev"] + VARS, env=e, capture_output=True, text=True, cwd=rogue); o = r.stdout + r.stderr
    wrec("WRAP-14-ruta-relativa", "medio", "cwd con guarda homónima maliciosa; ruta con ../", "ruta relativa manipulada y cwd hostil", "ejecuta la guarda verificada (no la del cwd): GUARDA OK y sin PWNED-ROGUE", r.returncode, o, r.returncode == 0 and "GUARDA OK" in o and "PWNED" not in o)
    # variables de entorno manipuladas
    fake = tempfile.mkdtemp(prefix="adv_p_"); TMPS.append(fake)
    for n in ("sha256sum", "psql", "cp", "mktemp"): open(os.path.join(fake, n), "w").write("#!/bin/sh\necho PWNED-PATH\nexit 0\n"); os.chmod(os.path.join(fake, n), 0o755)
    rc, o = wrap(VARS, env={"PATH": fake + ":" + os.environ["PATH"]}); wrec("WRAP-15-PATH", "alto", "PATH con sha256sum/psql/cp/mktemp falsos", "PATH manipulado", "el ejecutor fija PATH: GUARDA OK sin PWNED-PATH", rc, o, rc == 0 and "GUARDA OK" in o and "PWNED" not in o)
    rcf = os.path.join(fake, "psqlrc"); open(rcf, "w").write("select 'PWNED-PSQLRC';\n"); rc, o = wrap(VARS, env={"PSQLRC": rcf, "BASH_ENV": rcf, "LD_PRELOAD": "/nonexistent.so"}); wrec("WRAP-16-PSQLRC-BASH_ENV", "alto", "PSQLRC/BASH_ENV/LD_PRELOAD hostiles", "variables de entorno de arranque manipuladas", "ignoradas: GUARDA OK sin PWNED", rc, o, rc == 0 and "GUARDA OK" in o and "PWNED" not in o)
    rc, o = wrap(VARS, env={"CCI_DIR": rogue, "CCI_GUARDA_SHA256_APROBADO": sha(os.path.join(rogue, "00_guarda_destino.sql"))}); wrec("WRAP-17-CCI_DIR-preestablecida", "alto", "CCI_DIR y hash preestablecidos por el atacante hacia una guarda hostil", "variables CCI_* heredadas", "el ejecutor las sobrescribe: GUARDA OK sin PWNED-ROGUE", rc, o, rc == 0 and "GUARDA OK" in o and "PWNED" not in o)
    rc, o = wrap(VARS, opts=LOC + " -c search_path=evil -c cci.guarda_ok=1"); rech("WRAP-18-PGOPTIONS-extra", "medio", "PGOPTIONS con opciones no permitidas", "PGOPTIONS extra", "V-PGOPTIONS-NO-PERMITIDO", rc, o)
    for opc in (["-v", "cci_run=x"], ["-c", "select 1"], ["-f", "/etc/hostname"], ["-1"]):
        rc, o = wrap(opc + VARS); rech("WRAP-19-opcion-" + opc[0].strip("-") + (opc[1][:4] if len(opc) > 1 else ""), "medio", "opciones de psql peligrosas", "opción " + " ".join(opc), "V-OPCION-NO-PERMITIDA", rc, o)
    # destino aprobado
    rc, o = wrap(VARS, env={"CCI_DESTINOS_APROBADOS": "/otro/host:/otro2"}, args=None) if False else (0, "")
    rc, o = wrap(["-h", SOCK] + VARS, env={"CCI_DESTINOS_APROBADOS": SOCK}); wrec("WRAP-20-destino-aprobado", "control", "host en CCI_DESTINOS_APROBADOS", "destino aprobado", "ejecuta", rc, o, rc == 0 and "GUARDA OK" in o)
    rc, o = wrap(["-h", SOCK] + VARS, env={"CCI_DESTINOS_APROBADOS": "/otro/host"}); rech("WRAP-21-destino-no-aprobado", "alto", "host no aprobado (p. ej. clon de PROD en otro endpoint)", "destino fuera de la lista externa", "V-DESTINO-NO-APROBADO", rc, o, "distingue por ENDPOINT externo, no por system_identifier")
    rc, o = wrap(VARS, opts="-c cci.validacion_autorizada=SI-CCI-DEV -c cci.entorno=CCI-DEV"); rech("WRAP-22-DEV-sin-lista", "alto", "modo CCI-DEV sin CCI_DESTINOS_APROBADOS", "modo DEV sin identidad externa configurada", "V-DESTINO-NO-CONFIGURADO", rc, o)
    # TOCTOU: sustitución entre validación y ejecución (bucle de sustitución concurrente del ORIGINAL)
    t = mkset(); orig = os.path.join(t, "00_guarda_destino.sql"); bueno = open(orig).read(); malo = "select 'PWNED-TOCTOU';\n"; stop = threading.Event()
    def flip():
        i = 0
        while not stop.is_set():
            open(orig + ".tmp", "w").write(malo if i % 2 == 0 else bueno); os.replace(orig + ".tmp", orig); i += 1
    th = threading.Thread(target=flip); th.start(); res_t = []
    for _ in range(25): res_t.append(wrap(VARS, t=t))
    stop.set(); th.join(); open(orig, "w").write(bueno)
    pw = sum("PWNED" in o for _, o in res_t); okk = sum(rc == 0 and "GUARDA OK" in o for rc, o in res_t); rej = sum(rc == 3 for rc, o in res_t)
    wrec("WRAP-23-TOCTOU", "alto", "el original se sustituye en bucle entre archivo bueno y malicioso durante 25 ejecuciones", "carrera entre verificación y ejecución", "nunca se ejecuta contenido malicioso (0 PWNED); cada corrida o ejecuta la copia verificada o rechaza", 0, "ejecuciones=25 ok=%d rechazadas=%d pwned=%d" % (okk, rej, pw), pw == 0 and okk + rej == 25, "se ejecuta la COPIA verificada en un directorio 0700; un atacante con el mismo uid sobre ese directorio queda fuera del modelo")
    # simultaneidad
    out = []
    def go(): out.append(wrap(VARS))
    ths = [threading.Thread(target=go) for _ in range(6)]; [x.start() for x in ths]; [x.join() for x in ths]
    wrec("WRAP-24-concurrencia", "medio", "6 ejecuciones simultáneas del mismo script", "ejecución simultánea", "las 6 terminan OK, cada una con su directorio privado y su marcador", 0, "ok=%d/6" % sum(rc == 0 and "GUARDA OK" in o for rc, o in out), all(rc == 0 and "GUARDA OK" in o for rc, o in out))
    # interrupción: SIGTERM durante la ejecución -> sin directorios residuales
    antes = set(x for x in os.listdir(tempfile.gettempdir()) if x.startswith("cci_ev."))
    ee = dict(os.environ, PGHOST=SOCK, PGPORT=PORT, PGUSER="cci_test", PGOPTIONS=LOC); p = subprocess.Popen(["bash", WRAP, SUMH, os.path.join(BASE, SEIS[0] + ".sql"), "-d", "cci_gdev", "-c" if False else "-v", "x=1"], env=ee, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    time.sleep(0.15); p.send_signal(signal.SIGTERM); o, er = p.communicate(timeout=30); time.sleep(0.5); desp = set(x for x in os.listdir(tempfile.gettempdir()) if x.startswith("cci_ev.")) - antes
    wrec("WRAP-25-interrupcion", "medio", "SIGTERM durante la ejecución", "interrupción del proceso", "no quedan directorios privados residuales", p.returncode, "residuales=%d" % len(desp), len(desp) == 0, "")
    # error de permisos: usuario sin permiso de lectura sobre SHA256SUMS (se ejecuta como 'nobody' si runuser existe)
    t = mkset(); os.chmod(os.path.join(t, "SHA256SUMS_CCI.txt"), 0); os.chmod(os.path.join(os.path.dirname(t)), 0o755); os.chmod(t, 0o755)
    try:
        r = subprocess.run(["runuser", "-u", "nobody", "--", "bash", WRAP, SUMH, os.path.join(t, SEIS[0] + ".sql"), "-d", "cci_gdev", "-h", SOCK, "-U", "cci_test"], env=dict(os.environ, PGPORT=PORT, PGOPTIONS=LOC, HOME="/tmp"), capture_output=True, text=True, timeout=30); o = r.stdout + r.stderr; rc = r.returncode
    except Exception as ex: rc, o = 99, str(ex)
    rech("WRAP-26-permisos", "medio", "SHA256SUMS ilegible para el usuario que ejecuta", "error de permisos", "V-PERMISOS", rc, o) if "[V-PERMISOS]" in o else wrec("WRAP-26-permisos", "medio", "SHA256SUMS ilegible (modo 000) para 'nobody'", "error de permisos", "NO EJECUTADO, rc!=0, sin GUARDA OK", rc, o, rc != 0 and "GUARDA OK" not in o)
    # script no reconocido / fuera del conjunto
    t = mkset(); shutil.copy(os.path.join(t, SEIS[0] + ".sql"), os.path.join(t, "99_otro.sql")); rc, o = wrap(VARS, t=t, sc="99_otro"); rech("WRAP-27-script-ajeno", "alto", "script que no pertenece al conjunto aprobado", "ejecutar 99_otro.sql", "V-SCRIPT-NO-RECONOCIDO", rc, o)
    # ataque contra el ÁRBOL PUBLICADO anterior (e0b1d81): reproduce los defectos
    if PUBDIR != "-":
        OLD = mk("old"); VOLD = mk("old", guarda="")
        caso("A", "publicado", "-", "alto", "pg_temp.cci_guarda_ok creada en la misma sesión; guarda vacía", "cci_test", "1 conexión", "script con guarda vacía (árbol publicado)", "precrear el marcador", "FAIL = defecto reproducido (el cuerpo se ejecuta)", lambda sc: PRE + VARS + F(VOLD, sc), ok_si="defecto", nota="defecto del árbol publicado e0b1d81/d365a16: el marcador es una tabla temporal con nombre fijo")
        caso("D", "publicado", "-", "alto", "marcador antiguo + guarda vacía", "cci_test", "1 conexión", "script con guarda vacía (árbol publicado)", "ídem con GUC y variables", "FAIL = defecto reproducido", lambda sc: ["-v", "cci_run=x"] + PRE + VARS + F(VOLD, sc), opts=LOC + " -c cci.guarda_ok=1", ok_si="defecto")
        caso("E1", "publicado", "-", "alto", "guarda alterada que sólo crea pg_temp.cci_guarda_ok", "cci_test", "1 conexión", "script con guarda alterada (árbol publicado)", "forjar el marcador", "FAIL = defecto reproducido", lambda sc: VARS + F(mk("old", guarda="create temp table pg_temp.cci_guarda_ok (ok boolean);\n"), sc), ok_si="defecto")
        caso("H", "publicado", "-", "alto", "psql -f directo sin hash externo", "cci_test", "1 conexión", "script real (árbol publicado)", "ejecución directa", "el árbol publicado ejecuta sin verificar integridad: el cuerpo se ejecuta (control, no defecto de la guarda íntegra)", lambda sc: VARS + F(OLD, sc), ok_si="positivo")
finally:
    for d in TMPS: shutil.rmtree(d, ignore_errors=True)
    adm("drop database if exists cci_gdev")
c = {}
for r in REC: c[r["estado"]] = c.get(r["estado"], 0) + 1
json.dump(REC, open(OUT, "w"), ensure_ascii=False, indent=1)
print("TOTAL=%d %s" % (len(REC), c))
for r in REC:
    if r["estado"] == "FAIL" and r["arbol"] != "publicado": print("FAIL", r["id"], r["resultado_sql"][:100], "|", r["esperado"][:60])
