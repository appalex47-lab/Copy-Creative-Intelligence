#!/usr/bin/env python3
# Orquestador central FAIL-FAST de la validación de Fase 0.
# Uso (como root, en un repositorio git LIMPIO): python3 -I -B ct_orquestador_fase0.py <raiz_repo> <dir_salida>
# Máquina de estados por etapa: NOT_STARTED -> RUNNING -> PASSED | FAILED | BLOCKED. Un paso puede además quedar NOT_TESTED (no se ejecutó/ no es ejecutable aquí): NUNCA equivale a PASS y impide FASE0_READY. Una etapa sólo arranca si la anterior terminó PASSED; el primer FAIL/BLOCKED detiene todo y el
# proceso termina con código != 0. Todas las pruebas se ejecutan en ESTA ejecución (id único), en clústeres PostgreSQL nuevos creados aquí; no se reutiliza ningún resultado anterior
# y nada se puede marcar a mano como PASS (el estado de cada paso lo calcula este programa a partir de rc + contenido esperado). Un cambio en archivos críticos durante la ejecución invalida la corrida.
# Estado final: FASE0_READY_FOR_OWNER_ACCEPTANCE (exit 0) sólo si TODO PASS y sin BLOCKED; FASE0_BLOCKED (exit 2) si falta una dependencia externa; FASE0_FAILED (exit 1) si algo falla.
# NO equivale a aceptación formal del propietario. Nunca Supabase / CCI-DEV / CCI-PROD.
import csv, glob, hashlib, json, os, re, socket, subprocess, sys, time, uuid, shutil, tempfile
ROOT = os.path.abspath(sys.argv[1]); SAL = os.path.abspath(sys.argv[2])
CT = os.path.join(ROOT, "docs/fase0/cierre_tecnico_fase0"); SV = os.path.join(CT, "scripts_validacion"); R = os.path.join(SV, "resultados"); BF = os.path.join(R, "bateria_final"); CD = os.path.join(R, "cierre_definitivo")
SQLD = os.path.join(SV, "cci_dev_NO_EJECUTADOS"); PY = ["python3", "-I", "-B"]; BIN = "/usr/lib/postgresql/16/bin"
RUN = "CCI-RUN-%s-%s" % (time.strftime("%Y%m%dT%H%M%SZ", time.gmtime()), uuid.uuid4().hex[:8]); T0 = time.time()
ETAPAS = [("A", "Integridad del repositorio"), ("B", "Validación estática"), ("C", "Seguridad de la guarda"), ("D", "Pruebas PostgreSQL aisladas"), ("E", "RLS y privilegios"),
          ("F", "Triggers y funciones"), ("G", "Concurrencia"), ("H", "Reconciliación integral"), ("I", "Consistencia documental"), ("J", "Integridad de manifiestos"), ("K", "Verificación final")]
ESTADO = {l: "NOT_STARTED" for l, _ in ETAPAS}; PASOS = []; LIMITES = []; BLOQ = []; LOG = []; CL = {}
os.makedirs(SAL, exist_ok=True); os.makedirs(os.path.join(SAL, "pasos"), exist_ok=True)
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def log(m): LOG.append(m); print(m, flush=True)
def utc(): return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
CRIT = sorted(set(glob.glob(os.path.join(SQLD, "*.sql")) + [os.path.join(SQLD, "SHA256SUMS_CCI.txt")] + glob.glob(os.path.join(SV, "ct_*.py")) + glob.glob(os.path.join(SV, "ct_*.sh")) + glob.glob(os.path.join(SV, "*.sh")) + [os.path.abspath(__file__)]))
def hashes(): return {os.path.relpath(p, ROOT): sha(p) for p in CRIT}
H0 = hashes()
class Detener(Exception): pass
# Meta-prueba del orquestador (NO produce veredictos reales): CCI_ORQ_SIMULAR=1 sustituye CADA etapa por un paso trivial para ejercitar sólo la máquina de estados, los códigos de salida y la invalidación;
# CCI_ORQ_FALLO_EN=<ETAPA>:<FAIL|BLOCKED|EXC|MUTAR_CRITICO|NOT_TESTED> inyecta el fallo. En simulación el estado final es SIMULACION_* y NUNCA FASE0_READY_FOR_OWNER_ACCEPTANCE. La inyección sólo puede EMPEORAR un resultado.
SIM = os.environ.get("CCI_ORQ_SIMULAR") == "1"; INY = os.environ.get("CCI_ORQ_FALLO_EN", "")
def inyeccion(letra): return INY.split(":")[1] if INY.split(":")[0] == letra and ":" in INY else ""
def env_limpio(extra=None):
    e = {"PATH": "/usr/lib/postgresql/16/bin:/usr/local/bin:/usr/bin:/bin", "HOME": tempfile.gettempdir(), "LANG": "C.UTF-8", "CCI_RUN_ID": RUN}
    if extra: e.update(extra)
    return e
def paso(etapa, pid, cmd, rx=None, extra_env=None, chequeo=None, shell=False, cwd=None, timeout=3000):
    """Ejecuta UN paso; estado calculado: PASS sólo si rc==0, la salida contiene lo esperado y el chequeo adicional (si lo hay) pasa."""
    t = utc(); t1 = time.time(); fo = os.path.join(SAL, "pasos", "%s_%s.stdout.txt" % (etapa, pid)); fe = os.path.join(SAL, "pasos", "%s_%s.stderr.txt" % (etapa, pid))
    if INY.startswith(etapa + "/") and INY.split("/", 1)[1].split(":")[0] == pid: raise Detener("%s/%s: fallo inyectado" % (etapa, pid))
    try: p = subprocess.run(cmd, shell=shell, capture_output=True, text=True, env=env_limpio(extra_env), cwd=cwd or SV, timeout=timeout); rc = p.returncode; so, se = p.stdout, p.stderr
    except subprocess.TimeoutExpired as ex: rc, so, se = 124, (ex.stdout or b"").decode() if isinstance(ex.stdout, bytes) else (ex.stdout or ""), "TIMEOUT"
    open(fo, "w", encoding="utf-8").write(so); open(fe, "w", encoding="utf-8").write(se)
    ok = rc == 0 and (rx is None or re.search(rx, so + se, re.M) is not None); det = "" if ok else "rc=%d / salida sin lo esperado (%s)" % (rc, rx)
    if ok and chequeo:
        try: r = chequeo(so + se); ok = bool(r is True or (isinstance(r, tuple) and r[0])); det = "" if ok else (r[1] if isinstance(r, tuple) else "chequeo adicional no cumplido")
        except Exception as ex: ok = False; det = "chequeo falló: %r" % ex
    PASOS.append({"etapa": etapa, "id": pid, "comando": cmd if isinstance(cmd, str) else " ".join(cmd), "inicio_utc": t, "duracion_s": round(time.time() - t1, 1), "rc": rc, "esperado": rx, "estado": "PASS" if ok else "FAIL",
                  "detalle": det, "stdout": os.path.relpath(fo, SAL), "stdout_sha256": sha(fo), "stderr": os.path.relpath(fe, SAL), "stderr_sha256": sha(fe)})
    log("[%s] %-34s %s %s" % (etapa, pid, "PASS" if ok else "FAIL", det))
    LOG.append("----- stdout -----\n" + so[-1500:] + "\n----- stderr -----\n" + se[-600:])
    if not ok: raise Detener("%s/%s: %s" % (etapa, pid, det))
    return so
def battery(etapa, n):   # un paso de la batería (definición única en ct_bateria_final.sh), modo SOLO
    sock, port = CL["dev"]["sock"], CL["dev"]["port"]
    before = len(list(csv.DictReader(open(os.path.join(BF, "INDICE_BATERIA.csv"), encoding="utf-8"))))
    paso(etapa, "bat_" + n, ["bash", os.path.join(SV, "ct_bateria_final.sh"), sock, str(port)], extra_env={"CCI_PASO_SOLO": n}, rx=None if n != "__precondicion_roles" else None)
    rows = list(csv.DictReader(open(os.path.join(BF, "INDICE_BATERIA.csv"), encoding="utf-8")))
    if n.startswith("__"): return
    if len(rows) != before + 1 or rows[-1]["paso"] != n or rows[-1]["estado"] != "OK" or rows[-1]["rc"] != "0":
        PASOS[-1]["estado"] = "FAIL"; PASOS[-1]["detalle"] = "índice de batería: %s" % (rows[-1:] or "sin fila"); raise Detener("batería %s no OK: %s" % (n, rows[-1:]))
def etapa(letra, f):
    if SIM: f = sim_stub(letra)
    prev = [l for l, _ in ETAPAS][: [l for l, _ in ETAPAS].index(letra)]
    if any(ESTADO[p] != "PASSED" for p in prev): raise Detener("la etapa %s no puede comenzar: una etapa previa no terminó en PASSED" % letra)
    ESTADO[letra] = "RUNNING"; log("=== ETAPA %s: %s ===" % (letra, dict(ETAPAS)[letra]))
    try: f()
    except Detener: ESTADO[letra] = "FAILED"; raise
    h = hashes()
    if h != H0: ESTADO[letra] = "FAILED"; ch = [k for k in set(h) | set(H0) if h.get(k) != H0.get(k)]; raise Detener("archivos críticos modificados durante la ejecución (los resultados quedan invalidados): %s" % ch[:5])
    ESTADO[letra] = "PASSED"
def puertos_libres(n):
    for _ in range(50):
        b = puerto_libre()
        if b + n < 65000 and all(_libre(b + i) for i in range(n)): return b
    raise Detener("no hay %d puertos consecutivos libres" % n)
def _libre(p):
    s = socket.socket()
    try: s.bind(("127.0.0.1", p)); return True
    except OSError: return False
    finally: s.close()
def puerto_libre():
    s = socket.socket(); s.bind(("127.0.0.1", 0)); p = s.getsockname()[1]; s.close(); return p
def psql(c, sql, db="postgres"): return subprocess.run(["psql", "-h", c["sock"], "-p", str(c["port"]), "-U", "cci_test", "-d", db, "-qAtc", sql], capture_output=True, text=True, env=env_limpio()).stdout.strip()
def git(*a): return subprocess.run(["git", "-C", ROOT] + list(a), capture_output=True, text=True).stdout.strip()
# ---------------- etapas
def A():
    amb = [k for k in os.environ if k.startswith(("PG", "CCI_")) and k != "CCI_RUN_ID"]
    LOG.append("variables heredadas detectadas (se ignoran; los pasos usan entorno limpio): %s" % amb)
    paso("A", "arbol_git_limpio", "test -z \"$(git status --porcelain)\" && echo ARBOL_LIMPIO && git rev-parse HEAD", rx="ARBOL_LIMPIO", shell=True, cwd=ROOT)
    paso("A", "sha256sums_guarda_y_scripts", ["sha256sum", "-c", "--strict", "SHA256SUMS_CCI.txt"], rx="OK", cwd=SQLD, chequeo=lambda o: o.count(": OK") == 11 and "FAILED" not in o)
    paso("A", "ramas_protegidas_intactas", "git ls-remote origin | grep -E 'refs/heads/(main|audit/fase0-v26-review|audit/cierre-tecnico-fase0|audit/fase0-remediaciones-h01-h02-h03|audit/fase0-auditoria-final-publicacion|audit/fase0-cierre-definitivo)$'", shell=True, cwd=ROOT,
         chequeo=lambda o: all(x in o for x in ("6a1af2424ef39e0960b8f7e09d4e19ec52e6f046\trefs/heads/main", "439777c9ea7db464fe49299adfeb2112abfd285c\trefs/heads/audit/fase0-v26-review", "5b008485706bde3e9cf8407e71c0652cfd0497a5\trefs/heads/audit/cierre-tecnico-fase0", "d365a162e54809f3b8de9c77f5902a8ea131a97f\trefs/heads/audit/fase0-remediaciones-h01-h02-h03", "e0b1d8165d7584edd7fd03c2fa3c54fcce9d87e0\trefs/heads/audit/fase0-auditoria-final-publicacion")))
    base = os.path.join(tempfile.gettempdir(), RUN)
    for nm in ("dev", "prod"):
        port = puerto_libre(); d = os.path.join(base, nm); so = paso("A", "cluster_nuevo_" + nm, ["bash", os.path.join(SV, "ct_nuevo_cluster.sh"), d, str(port)], rx=r"sysid=\d+")
        CL[nm] = {"dir": d, "sock": os.path.join(d, "sock"), "port": port, "sysid": re.search(r"sysid=(\d+)", so).group(1)}
    ind = CL["dev"]["sysid"] != CL["prod"]["sysid"] and CL["dev"]["dir"] != CL["prod"]["dir"] and CL["dev"]["port"] != CL["prod"]["port"]
    vac = all(psql(CL[n], "select count(*) from pg_database where datname not in ('postgres','template0','template1')") == "0" and psql(CL[n], "select count(*) from pg_roles where rolname in ('anon','authenticated','service_role')") == "0" for n in CL)
    PASOS.append({"etapa": "A", "id": "clusteres_independientes_y_vacios", "comando": "system_identifier distintos, dirs/puertos distintos, sin bases ni roles Supabase", "rc": 0, "estado": "PASS" if ind and vac else "FAIL", "detalle": json.dumps({k: {"sysid": v["sysid"], "port": v["port"]} for k, v in CL.items()})})
    log("[A] clusteres independientes y vacios: %s" % ("PASS" if ind and vac else "FAIL"))
    if not (ind and vac): raise Detener("clústeres no independientes o no vacíos")
    # índice de la batería: nuevo, de esta ejecución
    shutil.rmtree(BF, ignore_errors=True); os.makedirs(BF)
    subprocess.run(["bash", "-c", "R='%s'; B='%s'; " % (R, BF) + "; ".join(l for l in open(os.path.join(SV, "ct_bateria_final.sh"), encoding="utf-8").read().split("\n") if l.startswith(("for f in base_V20", 'rm -f "$R"/reconciliacion')))], check=True)
    shutil.rmtree(CD, ignore_errors=True); os.makedirs(CD)
    open(os.path.join(BF, "INDICE_BATERIA.csv"), "w", encoding="utf-8").write("paso,comando,inicio_utc,fin_utc,inicio_local,fin_local,zona_local,rc,esperado,estado,resumen,salida,sha256_salida\n")
    open(os.path.join(BF, "ENTORNO.txt"), "w", encoding="utf-8").write("ejecucion_id=%s\ninicio_utc=%s\nHEAD=%s\nclusteres=%s\nzona=%s\n" % (RUN, utc(), git("rev-parse", "HEAD"), json.dumps({k: {"sysid": v["sysid"], "port": v["port"]} for k, v in CL.items()}), time.strftime("%Z")))
def B():
    for n in ("escaner_sql", "escaner_autoprueba", "escaner_texto"): battery("B", n)
    paso("B", "meta_orquestador_fallos_inducidos", PY + [os.path.join(SV, "ct_pruebas_orquestador_fallos.py"), ROOT, os.path.join(SAL, "pasos", "orquestador_meta_fallos.json")], rx=r"^TOTAL=49 PASS=49 FAIL=0$", timeout=1800)
def arboles_previos():
    out = {}
    for sha_, et in (("e0b1d8165d7584edd7fd03c2fa3c54fcce9d87e0", "e0b1d81"), ("d365a162e54809f3b8de9c77f5902a8ea131a97f", "d365a16")):
        d = os.path.join(tempfile.gettempdir(), RUN, "prev_" + et); os.makedirs(d, exist_ok=True)
        subprocess.run("git -C '%s' archive %s docs/fase0/cierre_tecnico_fase0/scripts_validacion/cci_dev_NO_EJECUTADOS | tar -x -C '%s'" % (ROOT, sha_, d), shell=True, check=True)
        out[et] = os.path.join(d, "docs/fase0/cierre_tecnico_fase0/scripts_validacion/cci_dev_NO_EJECUTADOS")
    return out
def C():
    sock, port = CL["dev"]["sock"], str(CL["dev"]["port"]); pv = arboles_previos()
    battery("C", "__precondicion_roles")   # los scripts 02 exigen los roles anon/authenticated/service_role (precondición determinista de la batería)
    battery("C", "guarda_destino")
    gd = open(os.path.join(R, "guarda_destino.txt"), encoding="utf-8").read()
    if not re.search(r"^TOTAL=187 PASS=187 FAIL=0$", gd, re.M): raise Detener("guarda_destino: se exigen 187/187")
    def adv(o):
        J = json.load(open(os.path.join(CD, "adversarial_marcador_ejecutor.json"))); cor = [r for r in J if r["arbol"] == "corregido"]; pub = [r for r in J if r["arbol"] == "publicado"]
        mal = [r["id"] for r in cor if r["estado"] not in ("PASS", "PARTIAL")]; parc = [r for r in cor if r["estado"] == "PARTIAL"]
        ataques = {c for c in ("A", "D", "E1") if all(r["estado"] == "FAIL" for r in pub if r["caso"] == c) and any(r["caso"] == c for r in pub)}
        for r in parc: LIMITES.append({"origen": "adversarial", "id": r["id"], "estado": "PARTIAL", "descripcion": r["nota"] or r["accion"]})
        return (not mal and len(cor) >= 130 and ataques == {"A", "D", "E1"} and all(r["estado"] == "PASS" for r in pub if r["caso"] == "H") and all(r["persistencia"].startswith("sin cambios") for r in cor if r["estado"] == "PASS"), "FAIL corregido=%s ataques_reproducidos=%s" % (mal, ataques))
    paso("C", "adversarial_marcador_y_ejecutor", PY + [os.path.join(SV, "ct_pruebas_adversariales_cierre.py"), sock, port, pv["e0b1d81"], os.path.join(CD, "adversarial_marcador_ejecutor.json")], rx="TOTAL", chequeo=adv)
    def sp(o):
        J = json.load(open(os.path.join(CD, "auditoria_search_path.json"))); D = J["dinamico"]
        ok1 = all(r["rechazo"] == "G-SEARCH-PATH-NO-SEGURO" and not r["hijack_funcion"] and not r["hijack_operador"] for r in D if r["id"].startswith(("SPD1", "SPD6")) and r["arbol"] == "corregido")
        ok2 = not any(r["hijack_funcion"] for r in D if r["arbol"] in ("corregido", "corregido-sin-chequeo", "anterior:e0b1d81"))
        base = sum(1 for r in D if r["id"].startswith("SPD3") and r["arbol"] == "anterior:d365a16" and r["hijack_funcion"]) >= 1   # el ataque se reproduce en la versión vulnerable
        est = [e for e in J["estatico"] if e["arbol"] == "corregido"]
        op = sum(1 for r in D if r["arbol"] == "corregido-sin-chequeo" and r["hijack_operador"])
        # SPD7 (resuelto): el blindaje de sesión de la guarda deja 0 scripts secuestrables por operadores aun SIN el chequeo de search_path
        baseop = sum(1 for r in D if r["id"].startswith("SPD8") and r["hijack_operador"]) >= 1   # control positivo: el ataque de operadores funciona contra versiones anteriores
        return (ok1 and ok2 and base and op == 0 and baseop and not est, "ok1=%s ok2=%s base=%s op_sin_chequeo=%d control_op=%s sin_calificar_corregido=%d" % (ok1, ok2, base, op, baseop, len(est)))
    paso("C", "search_path_hijack", PY + [os.path.join(SV, "ct_auditoria_search_path.py"), sock, port, SQLD, "e0b1d81=%s,d365a16=%s" % (pv["e0b1d81"], pv["d365a16"]), os.path.join(CD, "auditoria_search_path.json")], chequeo=sp)
    def idn(o):
        J = json.load(open(os.path.join(CD, "identidad.json"))); mal = [r["id"] for r in J if r["estado"] not in ("PASS", "PARTIAL", "NOT TESTED")]
        for r in J:
            if r["estado"] == "PARTIAL": LIMITES.append({"origen": "identidad", "id": r["id"], "estado": "PARTIAL", "descripcion": r["justificacion"]})
            if r["estado"] == "NOT TESTED": BLOQ.append({"id": r["id"], "dependencia": "validación real en Supabase (no autorizada ni disponible)", "detalle": r["ataque"]})
        return (not mal and sum(r["estado"] == "PASS" for r in J) >= 10, str(mal))
    dev, prod = CL["dev"], CL["prod"]; cl = os.path.join(tempfile.gettempdir(), RUN, "clon"); clp = puerto_libre()
    paso("C", "identidad_dev_prod_ag18", PY + [os.path.join(SV, "ct_pruebas_identidad_cierre.py"), dev["sock"], str(dev["port"]), prod["sock"], str(prod["port"]), cl, str(clp), os.path.join(CD, "identidad.json")], chequeo=idn)
    ops = os.path.join(CD, "autorizacion_operadores.json")
    paso("C", "autorizacion_operadores", PY + [os.path.join(SV, "ct_pruebas_autorizacion_operadores.py"), sock, port, ops], rx=r"^TOTAL=22 PASS=22 FAIL=0$")
    def opc(o):   # el control positivo exige que la guarda anterior sea idéntica a 404f5adc y que los ataques funcionen contra ella
        J = json.load(open(os.path.join(CD, "operadores_privilegios_cierre.json")))
        eq = J["equivalencia_VULN_con_guarda_404f5adc"].get("identica") is True
        cp = [c for c in J["casos_barrido"] if c["id"] in ("B-01", "B-02", "E-01")]
        return (eq and all(c["control_positivo_VULN_scripts_secuestrados"] for c in cp), "equivalencia=%s controles_positivos=%s" % (eq, [(c["id"], c["control_positivo_VULN_scripts_secuestrados"]) for c in cp]))
    paso("C", "operadores_y_privilegios_efectivos", PY + [os.path.join(SV, "ct_pruebas_operadores_cierre.py"), sock, port, os.path.join(CD, "operadores_privilegios_cierre.json")], rx=r"^TOTAL=39 PASS=39 FAIL=0$", chequeo=opc)
    pb = puertos_libres(4); wd = os.path.join(tempfile.gettempdir(), RUN, "ag18")
    paso("C", "identidad_firmada_ag18_clones", PY + [os.path.join(SV, "ct_pruebas_identidad_firmada.py"), wd, str(pb), os.path.join(CD, "identidad_firmada_ag18.json")], rx=r"^TOTAL=42 PASS=42 FAIL=0$")
    pb = puertos_libres(4); wd = os.path.join(tempfile.gettempdir(), RUN, "ext01")
    paso("C", "aprobacion_firmada_y_cadena_dev", PY + [os.path.join(SV, "ct_pruebas_ext01_y_e2e_dev.py"), wd, str(pb), os.path.join(CD, "aprobacion_firmada_ext01_cadena_dev.json")], rx=r"^TOTAL=36 PASS=36 FAIL=0$")
    paso("C", "validador_listas_ext03", PY + [os.path.join(SV, "ct_pruebas_validador_listas.py"), os.path.join(CD, "validador_listas_ext03.json")], rx=r"^TOTAL=34 PASS=34 FAIL=0$")
    paso("C", "sonda_ext02_simulada_local", PY + [os.path.join(SV, "ct_pruebas_ext02_sonda.py"), sock, port, os.path.join(CD, "sonda_ext02_local.json")], rx=r"^TOTAL=7 PASS=7 FAIL=0$")
def D():
    for n in ("v20_pe", "v20_mutaciones", "extension_local", "dg19", "hash_encadenado"): battery("D", n)
def E():
    battery("E", "__precondicion_roles")
    for n in ("smoke_6_scripts", "aserciones_smoke"): battery("E", n)
def F():
    for n in ("estatica_T47_T124", "k47_por_escenario", "t409_individual", "t409_repro_2a_corrida", "t409_repro_comparacion", "t409_correspondencia", "funciones_22", "exc_modelo14", "catalogo_except", "arnes_r1r9"): battery("F", n)
def G():
    battery("G", "concurrencia_local")
    paso("G", "permutaciones_orden", PY + [os.path.join(SV, "ct_permutaciones_scripts.py"), CL["dev"]["sock"], str(CL["dev"]["port"]), os.path.join(CD, "permutaciones.json")], chequeo=lambda o: (lambda J: all(J["todas_salidas_iguales"].values()) and J["sin_cambios_persistentes"] and J["permutaciones_01_04"] == 24)(json.load(open(os.path.join(CD, "permutaciones.json")))["resumen"]))
    paso("G", "secuencia_05A_05B_observador_independiente", PY + [os.path.join(SV, "ct_pruebas_05_secuencia.py"), CL["dev"]["sock"], str(CL["dev"]["port"]), os.path.join(CD, "secuencia_05.json")], rx=r"15/15|TOTAL=15 PASS=15 FAIL=0")
    LIMITES.append({"origen": "orden", "id": "05A-05B", "estado": "PARTIAL", "descripcion": "05A/05B dependen de la concurrencia entre ellas (A→B por diseño, deliberado); su veredicto lo emite un observador independiente (pg_stat_activity), no ellas mismas; no se declara independencia de orden"})
def ordenar_indice():
    decl = re.findall(r"^paso\s+(\w+)\s", open(os.path.join(SV, "ct_bateria_final.sh"), encoding="utf-8").read(), re.M); p = os.path.join(BF, "INDICE_BATERIA.csv")
    rows = list(csv.DictReader(open(p, encoding="utf-8"))); dic = {r["paso"]: r for r in rows}
    if sorted(dic) != sorted(decl) or len(rows) != len(decl): raise Detener("índice de batería incompleto/duplicado: faltan %s" % (set(decl) - set(dic)))
    w = csv.DictWriter(open(p, "w", encoding="utf-8", newline=""), fieldnames=list(rows[0].keys()), quoting=csv.QUOTE_MINIMAL, lineterminator="\n"); w.writeheader(); [w.writerow(dic[n]) for n in decl]
    open(os.path.join(BF, "ENTORNO.txt"), "a", encoding="utf-8").write("fin_utc=%s\nejecucion_id=%s\n" % (utc(), RUN))
def H():
    ordenar_indice()
    # Salidas que ESTA ejecución genera más adelante (reconciliación, controles, búsqueda global…) y que los generadores listan/citan: la limpieza de la batería las borró (no se heredan);
    # se crean como marcadores explícitos de esta ejecución y se sobrescriben con la salida real en H/I; K verifica que todo resultado pertenece a esta ejecución.
    SALIDAS_PROPIAS = ["reconciliacion_integral.json", "reconciliacion_integral.txt", "controles_consistencia_informe.txt", "controles_negativos_manifiesto.txt", "busqueda_global.txt"]
    for rel in git("ls-files", "-d", "--", "docs/fase0/cierre_tecnico_fase0").splitlines() + ["docs/fase0/cierre_tecnico_fase0/scripts_validacion/resultados/" + x for x in SALIDAS_PROPIAS]:
        p = os.path.join(ROOT, rel)
        if rel.startswith("docs/fase0/cierre_tecnico_fase0/scripts_validacion/resultados/") and not os.path.exists(p): os.makedirs(os.path.dirname(p), exist_ok=True); open(p, "w", encoding="utf-8").write("PENDIENTE_DE_GENERAR_EN_ESTA_EJECUCION %s\n" % RUN)
    for g in ("ct_gen_limitaciones.py", "ct_gen_trazabilidad_maestra.py", "ct_gen_informe_pruebas.py"):
        paso("H", g, PY + [os.path.join(SV, g), CT] + ([os.path.join(ROOT, "docs/fase0/ESPECIFICACION_TECNICA_G1_G5_G10.md")] if "trazab" in g else []))
    for i in (1, 2):
        for g, a in (("ct_gen_cifras.py", [CT]), ("ct_manifiesto.py", ["gen", CT]), ("ct_controles_negativos_manifiesto.py", [CT, os.path.join(R, "controles_negativos_manifiesto.txt")]), ("ct_gen_resolucion_observaciones.py", [CT, "5b008485706bde3e9cf8407e71c0652cfd0497a5"]), ("ct_gen_auditoria_fechas.py", [CT, "appalex47-lab/Copy-Creative-Intelligence"])):
            paso("H", "%s_pasada%d" % (g, i), PY + [os.path.join(SV, g)] + a)
    paso("H", "busqueda_global", PY + [os.path.join(SV, "ct_busqueda_global.py"), CT, os.path.join(R, "busqueda_global.txt")])
    subprocess.run(["git", "-C", ROOT, "add", "-N", "."], capture_output=True)
    paso("H", "reconciliacion_integral", PY + [os.path.join(SV, "ct_reconciliacion_integral.py"), CT], rx=r"TOTAL=\d+ PASS=\d+ FAIL=0")
    paso("H", "anclaje_externo_reconciliacion", PY + [os.path.join(SV, "ct_anclas_evidencia.py"), "anclar", CT, ANCLAS, RUN, "H", "--stdout", os.path.join(SAL, "pasos", "H_reconciliacion_integral.stdout.txt")], rx="ANCLADO H")
ANCLAS = os.path.join(SAL, "ANCLAS_EVIDENCIA.json")
def I():
    paso("I", "consistencia_informe", PY + [os.path.join(SV, "ct_verificar_consistencia_informe.py"), "verificar", CT], rx=r"incoherencias=0")
    paso("I", "anclas_verificadas_tras_H", PY + [os.path.join(SV, "ct_anclas_evidencia.py"), "verificar", CT, ANCLAS, RUN], rx=r"incoherencias=0")
    paso("I", "controles_negativos_anclas", PY + [os.path.join(SV, "ct_anclas_evidencia.py"), "controles", CT, os.path.join(SAL, "pasos", "controles_anclas.txt")], rx=r"TOTAL=\d+ FAIL=0")
    paso("I", "controles_negativos_consistencia", PY + [os.path.join(SV, "ct_verificar_consistencia_informe.py"), "controles", CT, os.path.join(R, "controles_consistencia_informe.txt")], rx=r"TOTAL=\d+ FAIL=0")
def J():
    paso("J", "manifiesto_regenerado", PY + [os.path.join(SV, "ct_manifiesto.py"), "gen", CT])
    paso("J", "manifiesto_verificado", PY + [os.path.join(SV, "ct_manifiesto.py"), "dir", CT], rx=r"RESULTADO=OK")
    paso("J", "anclaje_externo_manifiesto", PY + [os.path.join(SV, "ct_anclas_evidencia.py"), "anclar", CT, ANCLAS, RUN, "J"], rx="ANCLADO J")
def K():
    # 1) los resultados deben ser de ESTA ejecución
    J_ = json.load(open(os.path.join(R, "reconciliacion_integral.json"))); ids = {c["ejecucion_id"] for c in J_["comprobaciones"]}
    if ids != {RUN}: raise Detener("resultados heredados en la reconciliación: %s" % ids)
    if hashes() != H0: raise Detener("archivos críticos cambiaron durante la ejecución")
    ent = open(os.path.join(BF, "ENTORNO.txt")).read()
    if "ejecucion_id=" + RUN not in ent: raise Detener("batería de otra ejecución")
    PASOS.append({"etapa": "K", "id": "resultados_de_esta_ejecucion_e_integridad_de_critica", "comando": "ejecucion_id + SHA-256 de archivos críticos al inicio y al fin", "rc": 0, "estado": "PASS", "detalle": "%d archivos críticos sin cambios" % len(H0)}); log("[K] resultados de esta ejecución e integridad de archivos críticos: PASS")
    paso("K", "anclas_externas_intactas", PY + [os.path.join(SV, "ct_anclas_evidencia.py"), "verificar", CT, ANCLAS, RUN], rx=r"incoherencias=0")
    # 2) dependencias externas -> BLOCKED (nunca PASS). Cada una se levanta SÓLO si el insumo real del propietario existe y VALIDA automáticamente.
    vl = subprocess.run(PY + [os.path.join(SV, "ct_validar_listas_destinos.py"), "guarda", os.path.join(SQLD, "00_guarda_destino.sql"), "--requerir-no-vacias"], capture_output=True, text=True)
    PASOS.append({"etapa": "K", "id": "validador_listas_sobre_guarda_real", "comando": "ct_validar_listas_destinos.py guarda --requerir-no-vacias", "rc": vl.returncode, "estado": "PASS" if vl.returncode == 0 else "BLOCKED", "detalle": vl.stdout.strip()})
    if vl.returncode != 0: BLOQ.append({"id": "EXT-03", "dependencia": "listas de destinos DEV/PROD autorizados: %s" % vl.stdout.strip()[:160], "detalle": "00_guarda_destino.sql (procedimiento: PLAN_DESBLOQUEO_EXTERNOS.md, EXT-03)"})
    ap, kp, kh = os.environ.get("CCI_APROBACION_CUSTODIO", ""), os.environ.get("CCI_CUSTODIO_PUBKEY", ""), os.environ.get("CCI_CUSTODIO_PUBKEY_SHA256", ""); ext01 = False
    if ap and kp and kh:
        r = subprocess.run(["bash", os.path.join(SV, "ejecutar_script_verificado.sh"), ap, os.path.join(SQLD, "01_inventario_esquema_SOLO_LECTURA.sql"), "-h", CL["dev"]["sock"], "-p", str(CL["dev"]["port"]), "-U", "cci_test", "-d", "postgres", "-v", "org=x", "-v", "org_a=x", "-v", "org_b=x", "-v", "uid_a=x", "-v", "uid_x=x", "-v", "piece=x", "-v", "attr=x"],
                           capture_output=True, text=True, env=env_limpio({"PGOPTIONS": "-c cci.validacion_autorizada=SI-LOCAL-TEMPORAL -c cci.entorno=LOCAL-TEMPORAL", "CCI_CUSTODIO_PUBKEY": kp, "CCI_CUSTODIO_PUBKEY_SHA256": kh}))
        ext01 = r.returncode == 0 and "GUARDA OK" in r.stdout
        PASOS.append({"etapa": "K", "id": "aprobacion_custodio_real", "comando": "ejecutar_script_verificado.sh <aprobación firmada del custodio>", "rc": r.returncode, "estado": "PASS" if ext01 else "FAIL", "detalle": (r.stderr or r.stdout)[-160:]})
        if not ext01: raise Detener("la aprobación del custodio entregada NO valida: %s" % (r.stderr or r.stdout)[-160:])
    if not ext01: BLOQ.append({"id": "EXT-01", "dependencia": "custodio externo del hash aprobado no definido: falta la aprobación firmada (CCI_APROBACION_CUSTODIO) y la clave pública con su SHA-256 (CCI_CUSTODIO_PUBKEY, CCI_CUSTODIO_PUBKEY_SHA256). El mecanismo criptográfico está probado con claves de prueba; NO hay custodio real", "detalle": "variables CCI_APROBACION_CUSTODIO / CCI_CUSTODIO_PUBKEY* ausentes"})
    rep_, rsha = os.environ.get("CCI_EXT02_REPORTE", ""), os.environ.get("CCI_EXT02_REPORTE_SHA256", ""); ext02 = False
    if rep_ and os.path.isfile(rep_) and rsha == sha(rep_):
        try: d = json.load(open(rep_, encoding="utf-8")); ext02 = d.get("modo") == "REAL_CCI_DEV" and d.get("veredicto") == "PASS" and len(d.get("checks", [])) >= 10 and all(c["estado"] == "PASS" for c in d["checks"])
        except Exception: ext02 = False
    PASOS.append({"etapa": "K", "id": "supabase_cci_dev_real_ext02", "comando": "reporte de la sonda ct_ext02_validar_supabase_dev.py ejecutada por el propietario en CCI-DEV", "rc": 0, "estado": "PASS" if ext02 else "NOT_TESTED", "detalle": "reporte válido (atestación del propietario; el orquestador no puede verificar que provenga de Supabase real)" if ext02 else "no se aportó un reporte REAL_CCI_DEV con SHA-256 externo; ID-13 NOT_TESTED"})
    if not ext02: BLOQ.append({"id": "EXT-02", "dependencia": "compatibilidad con Supabase CCI-DEV (TEMP, pg_control_system(), PGOPTIONS por pooler, project ref, pooler): sólo verificable en CCI-DEV; la sonda existe y está probada en local (SIMULADO_LOCAL)", "detalle": "ID-13: NOT_TESTED"})
    v26 = {r["ID"]: r for r in csv.DictReader(open(os.path.join(ROOT, "docs/fase0/expediente_final_v26/MATRIZ_CONTROLES_V26.csv"), encoding="utf-8"))}
    desc = {"L04": "equivalencia del PostgreSQL temporal con el esquema físico aprobado (no existe esquema físico aprobado)", "L05": "validación física en CCI-DEV", "L06": "RLS, privilegios y concurrencia reales en CCI-DEV", "L07": "trigger de elegibilidad R1–R9 en entorno físico", "L08": "HV-02/PO-05: confirmación del propietario sobre la Adenda v9 (el documento no existe en el repositorio)"}
    for lid in ("L04", "L05", "L06", "L07", "L08"):
        if v26[lid]["Estado"].strip().upper() in ("NOT VERIFIED", "NO VERIFICADO", "NOT TESTED", "NO VERIFICABLE") or "NOT VERIF" in v26[lid]["Estado"].upper() or "NO VERIF" in v26[lid]["Estado"].upper(): BLOQ.append({"id": "EXT-04-" + lid, "dependencia": desc[lid], "detalle": "MATRIZ_CONTROLES_V26.csv fila %s: %s" % (lid, v26[lid]["Estado"])})
    for b in BLOQ: PASOS.append({"etapa": "K", "id": "dependencia_externa_" + b["id"], "comando": "compuerta de dependencias externas", "rc": 0, "estado": "BLOCKED", "detalle": b["dependencia"]}); log("[K] %s BLOCKED: %s" % (b["id"], b["dependencia"]))
    for x in PASOS:
        if x["estado"] == "NOT_TESTED": log("[K] %s NOT_TESTED: %s" % (x["id"], x["detalle"]))
    if BLOQ: raise BloqueadoExt()
class BloqueadoExt(Exception): pass
def sim_stub(letra):
    def f():
        modo = inyeccion(letra)
        if modo == "EXC": raise RuntimeError("excepción inesperada inyectada en la etapa %s" % letra)
        if modo == "MUTAR_CRITICO": open(CRIT[0], "ab").write(b"\n-- mutacion inyectada\n")
        PASOS.append({"etapa": letra, "id": "simulado", "comando": "SIMULACION (sin ejecución real)", "rc": 0, "estado": "NOT_TESTED" if modo == "NOT_TESTED" else ("FAIL" if modo == "FAIL" else ("BLOCKED" if modo == "BLOCKED" else "PASS")), "detalle": "simulación de la máquina de estados"})
        if modo == "FAIL": raise Detener("%s/simulado: fallo inyectado" % letra)
        if modo == "BLOCKED": BLOQ.append({"id": "SIM", "dependencia": "bloqueo inyectado", "detalle": ""}); raise BloqueadoExt()
    return f
FUN = {"A": A, "B": B, "C": C, "D": D, "E": E, "F": F, "G": G, "H": H, "I": I, "J": J, "K": K}
final = "FASE0_FAILED"; causa = ""
try:
    for l, _ in ETAPAS:
        try: etapa(l, FUN[l])
        except BloqueadoExt:
            ESTADO[l] = "BLOCKED"; final = "FASE0_BLOCKED"; causa = "dependencias externas pendientes: " + ", ".join(b["id"] for b in BLOQ); break
    else: final = "FASE0_READY_FOR_OWNER_ACCEPTANCE"
except Detener as ex: causa = str(ex); final = "FASE0_FAILED"; log("DETENIDO: " + causa)
except Exception as ex:   # una excepción NO prevista jamás termina en PASS ni se clasifica como rechazo de negocio: es FALLO TÉCNICO
    causa = "EXCEPCIÓN TÉCNICA no prevista: %r" % ex; final = "FASE0_FAILED"; log("DETENIDO: " + causa)
    for l, _ in ETAPAS:
        if ESTADO[l] == "RUNNING": ESTADO[l] = "FAILED"
finally:
    for n, c in CL.items():
        subprocess.run(["su", "postgres", "-c", "%s/pg_ctl -D %s/data -m fast stop >/dev/null 2>&1" % (BIN, c["dir"])])
pas = [p for p in PASOS if p["estado"] == "PASS"]; fal = [p for p in PASOS if p["estado"] == "FAIL"]; blo = [p for p in PASOS if p["estado"] == "BLOCKED"]
nt = [p for p in PASOS if p["estado"] == "NOT_TESTED"]; pend = [l for l, _ in ETAPAS if ESTADO[l] == "NOT_STARTED"]
if final == "FASE0_READY_FOR_OWNER_ACCEPTANCE" and nt and not (fal or blo or pend or BLOQ): final = "FASE0_BLOCKED"; causa = "pasos NOT_TESTED: no equivalen a PASS"
if final == "FASE0_READY_FOR_OWNER_ACCEPTANCE" and (fal or blo or nt or pend or BLOQ): final = "FASE0_FAILED"; causa = "inconsistencia interna del orquestador"
code = {"FASE0_READY_FOR_OWNER_ACCEPTANCE": 0, "FASE0_BLOCKED": 2}.get(final, 1)
if SIM: final = "SIMULACION_" + final[len("FASE0_"):]   # meta-prueba: jamás produce un veredicto real
J = {"ejecucion_id": RUN, "inicio_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(T0)), "fin_utc": utc(), "duracion_s": round(time.time() - T0, 1), "HEAD": git("rev-parse", "HEAD"), "rama": git("rev-parse", "--abbrev-ref", "HEAD"),
     "estado_final": final, "causa": causa, "codigo_salida": code, "estados_etapas": ESTADO, "etapas_pendientes": pend,
     "pasos_obligatorios": {"total_ejecutados": len(PASOS), "PASS": len(pas), "FAIL": len(fal), "BLOCKED": len(blo), "NOT_TESTED": len(nt), "pendientes_etapas_no_iniciadas": len(pend)},
     "clusteres": {k: {"sysid": v["sysid"], "port": v["port"]} for k, v in CL.items()}, "dependencias_externas_bloqueadas": BLOQ, "limitaciones_residuales_PARTIAL": LIMITES,
     "hashes_archivos_criticos_inicio": H0, "hashes_archivos_criticos_fin": hashes(), "pasos": PASOS}
open(os.path.join(SAL, "RESULTADO_ORQUESTADOR.json"), "w", encoding="utf-8").write(json.dumps(J, ensure_ascii=False, indent=1, sort_keys=True) + "\n")
open(os.path.join(SAL, "LOG_COMPLETO_EJECUCION.txt"), "w", encoding="utf-8").write("\n".join(LOG) + "\n")
print("ESTADO_FINAL=%s PASS=%d FAIL=%d BLOCKED=%d etapas_no_iniciadas=%s exit=%d %s" % (final, len(pas), len(fal), len(blo), pend, code, causa)); sys.exit(code)
