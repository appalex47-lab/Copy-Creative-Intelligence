#!/usr/bin/env python3
"""Validación documental V26 (S01–S18 previa al manifiesto; S19–S20 solo en modo C con MANIFIESTO_SHA256_V26.txt).
Uso: python3 -I v26_validar.py <raiz del worktree> <A|C> [--prelim]
--prelim: no compara el bloque embebido de la pasada A (arranque del punto fijo documentado en INFORME_AUDITORIA_FINAL_V26.md)."""
import csv, hashlib, io, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v26_evaluar as ev, v26_registro as rg

W = os.path.abspath(sys.argv[1]); MODE = sys.argv[2]; PRELIM = "--prelim" in sys.argv
X = W + "/docs/fase0/expediente_final_v26"; V = X + "/V25_copia_integra"; E26 = X + "/evidencia_reconstruccion_V26/"
BASE = ev.H25; C25 = ev.C25
res = []
NAMES = {d["ID"]: d["Objetivo"] for d in rg.definiciones(X) if d["ID"].startswith("S")}
def ok(i, c, d=""):
    res.append(bool(c)); print(("PASS" if c else "FAIL"), "|", i, NAMES[i], "|", d)
sh = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
rd = ev.rd
def git(*a, raw=False):
    r = subprocess.run(["git"] + list(a), cwd=W, capture_output=True); return r.stdout if raw else r.stdout.decode()
allf = sorted(os.path.relpath(os.path.join(a, f), X) for a, _, x in os.walk(X) for f in x)
man_ex = os.path.exists(X + "/MANIFIESTO_SHA256_V26.txt")
rows = list(csv.DictReader(io.StringIO(rd(X + "/MATRIZ_CONTROLES_V26.csv"), newline="")))
exe = list(csv.DictReader(io.StringIO(rd(X + "/EJECUCIONES_CONTROLES_V26.csv"), newline="")))

# S01
cur = {os.path.relpath(os.path.join(a, f), V): sh(os.path.join(a, f)) for a, _, x in os.walk(V) for f in x}
pref = "docs/fase0/expediente_final_v25/"
tree = [p[len(pref):] for p in git("ls-tree", "-r", "--name-only", C25, pref).split("\n") if p]
dif = [p for p in tree if hashlib.sha256(git("show", C25 + ":" + pref + p, raw=True)).hexdigest() != cur.get(p)]
pubok = sh(X + "/V25_publicacion/REPORTE_PUBLICACION_V25_GITHUB.md") == hashlib.sha256(git("show", BASE + ":docs/fase0/REPORTE_PUBLICACION_V25_GITHUB.md", raw=True)).hexdigest()
ok("S01", sorted(tree) == sorted(cur) and not dif and len(tree) == 275 and pubok, "archivos=%d distintos=%s publicación V25 idéntica=%s" % (len(cur), dif, pubok))
# S02
m = [l.rstrip("\n").split("  ", 1) for l in open(V + "/MANIFIESTO_SHA256_V25.txt", encoding="utf-8")]
okm = {p: h for h, p in m} == {k: v for k, v in cur.items() if k != "MANIFIESTO_SHA256_V25.txt"} and len(m) == 274
r = subprocess.run("sha256sum -c MANIFIESTO_SHA256_V25.txt 2>&1 | grep -c ': OK$'", shell=True, cwd=V, capture_output=True, text=True).stdout.strip()
r2 = subprocess.run("sha256sum -c 08_INTEGRIDAD_Y_MANIFIESTOS/SHA256SUMS.txt 2>&1 | grep -c ': OK$'", shell=True, cwd=V, capture_output=True, text=True).stdout.strip()
r3 = subprocess.run("sha256sum -c MANIFIESTO_SHA256_V24.txt 2>&1 | grep 'FAILED$'", shell=True, cwd=V, capture_output=True, text=True).stdout.strip().split("\n")
f24 = sorted(l.split(":")[0] for l in r3)
ok("S02", okm and r == "274" and r2 == "252" and f24 == sorted(["INFORME_CORRECCIONES_V24.md", "MATRIZ_OBSERVACIONES_V23_V24.md", "REPORTE_VALIDACION_V24.md"]), "V25 hashlib=%s sha256sum OK=%s; SHA256SUMS interno OK=%s; manifiesto V24 fallos=%s" % (okm, r, r2, f24))
# S03
low = [p.lower() for p in allf]; bad = [p for p in allf if p.startswith("/") or ".." in p.split("/") or "\\" in p or p != p.strip()]
ok("S03", len(set(low)) == len(low) and not bad, "archivos=%d" % len(allf))
# S04
req = ["ID", "Version_origen", "Categoria", "Objetivo", "Entrada", "Resultado_esperado", "Resultado_obtenido", "Evidencia_exacta", "Ruta_evidencia", "Ejecucion_historica_o_nueva", "Fecha_ejecucion", "Estado", "Observaciones"]
ids = [r_["ID"] for r_ in rows]; ESTS = {"PASS", "FAIL", "BLOCKED", "NOT VERIFIED", "PARTIAL"}
vac = [r_["ID"] for r_ in rows for c in ["ID", "Version_origen", "Categoria", "Objetivo", "Entrada", "Resultado_esperado", "Resultado_obtenido", "Evidencia_exacta", "Ruta_evidencia", "Ejecucion_historica_o_nueva", "Estado"] if not r_[c].strip()]
ok("S04", rows and all(c in rows[0] for c in req) and len(set(ids)) == len(ids) and all(r_["Estado"] in ESTS for r_ in rows) and not vac, "filas=%d vacíos=%s" % (len(rows), sorted(set(vac))))
# S05
miss = []
for r_ in rows:
    if r_["Ruta_evidencia"].startswith("..") or int(r_["Ejecuciones"]) == 0 and r_["ID"][0] == "L":
        if r_["ID"] not in ("S19", "S20") and r_["ID"][0] != "L": miss.append(r_["ID"])
        if r_["ID"][0] == "L" and not os.path.exists(X + "/" + r_["Ruta_evidencia"]): miss.append(r_["ID"])
        continue
    if not os.path.exists(X + "/" + r_["Ruta_evidencia"]): miss.append(r_["ID"])
ok("S05", not miss, "filas=%d sin evidencia existente=%s" % (len(rows), miss))
# S06
errs = []; EX = {}
for x in exe: EX.setdefault(x["ID_control"], []).append(x)
cache = {}
def evalf(fn, ruta):
    k = (fn.__name__, ruta)
    if k not in cache: cache[k] = fn(X + "/" + ruta)
    return cache[k]
for x in exe:
    i = x["ID_control"]; ruta = x["Ruta_evidencia"]
    if i[0] == "S" or ruta.startswith(".."): continue
    p = X + "/" + ruta
    if not os.path.exists(p): errs.append(("sin archivo", x["ID_ejecucion"])); continue
    n = int(x["Linea"]); lines = rd(p).split("\n")
    if x["Texto_clave"] not in lines[n - 1]: errs.append(("texto", x["ID_ejecucion"])); continue
    if i[0] == "C" or i[0] in "PQ":
        if not lines[n - 1].startswith(x["Resultado"] + " |"): errs.append(("estado", x["ID_ejecucion"]))
    elif i[:2] == "RV":
        e = evalf(ev.eval_RV, ruta)
        if e[i] != (x["Resultado"], n): errs.append(("RV", x["ID_ejecucion"]))
    elif i[0] == "R":
        e = evalf(ev.eval_R, ruta)
        if e[i] != (x["Resultado"], n): errs.append(("R", x["ID_ejecucion"]))
    elif i[0] == "W":
        e = evalf(ev.eval_W, ruta)
        if e[i] != (x["Resultado"], n): errs.append(("W", x["ID_ejecucion"]))
    elif i[:2] == "HT":
        if x["Resultado"] != ("PARTIAL" if i == "HT10" else "PASS"): errs.append(("HT", x["ID_ejecucion"]))
st = {r_["ID"]: r_["Estado"] for r_ in rows}
for r_ in rows:
    i = r_["ID"]; xs = EX.get(i, [])
    if int(r_["Ejecuciones"]) != len(xs): errs.append(("n ejecuciones", i))
    if r_["Estado"] == "PASS" and not any(x["Resultado"] == "PASS" for x in xs): errs.append(("PASS sin ejecución PASS", i))
    if xs and r_["Estado"] != xs[-1]["Resultado"]: errs.append(("estado != última ejecución", i))
    if not xs and r_["Estado"] not in ("PARTIAL", "NOT VERIFIED", "BLOCKED"): errs.append(("sin ejecución y estado", i))
ids_x = [x["ID_ejecucion"] for x in exe]
if len(set(ids_x)) != len(ids_x): errs.append(("ID_ejecucion duplicado", ""))
ok("S06", not errs, "ejecuciones=%d errores=%s" % (len(exe), errs[:5]))
# S07
def cifras(rows, exe):
    c = lambda k: sum(r_["Estado"] == k for r_ in rows); e = lambda k: sum(x["Resultado"] == k for x in exe)
    return {"Total de controles únicos": len(rows), "Total de ejecuciones": len(exe), "Controles PASS": c("PASS"), "Controles FAIL": c("FAIL"), "Controles BLOCKED": c("BLOCKED"),
            "Controles NOT VERIFIED": c("NOT VERIFIED"), "Controles PARTIAL": c("PARTIAL"), "Ejecuciones PASS": e("PASS"), "Ejecuciones FAIL": e("FAIL"), "Ejecuciones BLOCKED": e("BLOCKED"),
            "Ejecuciones NOT VERIFIED": e("NOT VERIFIED"), "Ejecuciones PARTIAL": e("PARTIAL")}
ref = cifras(rows, exe); bad7 = []
for f in ["LEEME_V26.md", "INFORME_AUDITORIA_FINAL_V26.md", "INFORME_CONCILIACION_CONTROLES_V26.md", "REPORTE_VALIDACION_V26.md", "REPORTE_VERIFICACION_REMOTA_V26.md"]:
    t = rd(X + "/" + f); b = re.search(r"<!-- CONCILIACION:INICIO -->(.*?)<!-- CONCILIACION:FIN -->", t, re.S)
    if not b: bad7.append((f, "sin bloque")); continue
    got = {k: int(v) for k, v in re.findall(r"^\| ([^|]+?) \| (\d+) \|$", b.group(1), re.M)}
    if got != ref: bad7.append((f, {k: (got.get(k), ref[k]) for k in ref if got.get(k) != ref[k]}))
ok("S07", not bad7, "cifras=%s; discrepancias=%s" % ({k: v for k, v in list(ref.items())[:7]}, bad7))
# S08
refs = []
docs26 = ["LEEME_V26.md", "INFORME_AUDITORIA_FINAL_V26.md", "INFORME_CONCILIACION_CONTROLES_V26.md", "MATRIZ_CAMBIOS_V25_V26.md", "REPORTE_VALIDACION_V26.md", "REPORTE_VERIFICACION_REMOTA_V26.md"]
EXTERNOS = {"MANIFIESTO_SHA256_V26.txt"} if not man_ex else set()
EXTERNOS |= {"docs/fase0/REPORTE_PUBLICACION_V26_GITHUB.md", "REPORTE_PUBLICACION_V26_GITHUB.md", "../REPORTE_PUBLICACION_V26_GITHUB.md", "CCI_FASE0_EXPEDIENTE_V21_V23.zip", "REPORTE_PUBLICACION_V25_GITHUB.md"}
for f in docs26:
    for rf in sorted(set(re.findall(r"`([\w./\-]+\.(?:md|csv|txt|py|sh|patch|tsv|zip|json))`", rd(X + "/" + f)))):
        if rf in EXTERNOS: continue
        if not any(os.path.exists(os.path.join(b, rf)) for b in (X, V, E26, E26 + "historico_V25_no_archivado")): refs.append((f, rf))
tmp = "/tmp/pub/v26/mapa_regenerado.csv"
subprocess.run([sys.executable, "-I", E26 + "v26_mapa_referencias.py", X, tmp], capture_output=True)
mapa_ok = os.path.exists(tmp) and rd(tmp) == rd(X + "/MAPA_REFERENCIAS_V26.csv") and "NO_RESUELTA" not in rd(tmp)
ok("S08", not refs and mapa_ok, "referencias V26 rotas=%s; mapa regenerado idéntico y sin NO_RESUELTA=%s" % (refs[:4], mapa_ok))
# S09
ALLOW = {ev.MAIN, ev.V20, ev.V23, "8be8acecffce64e2a4660383bc8d5306a303c9c1", ev.V24END, "a1dfedb867a79386fd165cbb6fc2859057658705", C25, ev.H25}
bad9 = []
for f in docs26 + ["MATRIZ_CONTROLES_V26.csv", "EJECUCIONES_CONTROLES_V26.csv"]:
    for s in set(re.findall(r"\b[0-9a-f]{40}\b", rd(X + "/" + f))):
        tipo = git("cat-file", "-t", s).strip()
        if not ((s in ALLOW and tipo == "commit") or (s == "0824c738f14c313b5f25149016a4622fe85fdeef" and tipo == "tree")): bad9.append((f, s[:8]))
ok("S09", not bad9, "SHA citados (commits y el árbol expediente_v23 de la salida R05) verificados contra el repositorio; discrepancias=%s" % bad9)
# S10
def blk(t): return re.findall(r"```\n(.*?)```", t, re.S)
H = X + "/evidencia_reconstruccion_V26/historico_V25_no_archivado/"
b10 = []
bv = blk(rd(V + "/REPORTE_VALIDACION_V25.md")); bp = blk(rd(X + "/V25_publicacion/REPORTE_PUBLICACION_V25_GITHUB.md"))
if not (len(bv) == 1 and bv[0] == rd(H + "val25_pasada_A_previa_manifiesto.txt")): b10.append("V25 A")
if not (len(bp) == 2 and bp[0] == rd(H + "val25_pasada_C_posterior_manifiesto.txt") and bp[1] == rd(H + "remoto_RV_V25_salida_original_sin_RV07.txt")): b10.append("V25 C/E")
bv4 = blk(rd(V + "/REPORTE_VALIDACION_V24.md")); bp4 = blk(rd(V + "/V24_publicacion/REPORTE_PUBLICACION_V24_GITHUB.md"))
if not (len(bv4) >= 1 and bv4[0] == rd(V + "/evidencia_reconstruccion_V25/salida_val24_pasada_A_previa_manifiesto.txt")): b10.append("V24 A")
if not any(b == rd(V + "/evidencia_reconstruccion_V25/salida_val24_pasada_C_posterior_manifiesto.txt") for b in bp4): b10.append("V24 C")
if not PRELIM:
    a = E26 + "salida_val26_pasada_A_previa_manifiesto.txt"
    bvv = blk(rd(X + "/REPORTE_VALIDACION_V26.md"))
    if not (os.path.exists(a) and len(bvv) == 1 and bvv[0] == rd(a)): b10.append("V26 A")
rr = blk(rd(X + "/REPORTE_VERIFICACION_REMOTA_V26.md"))
exp = [rd(E26 + "reejecucion_V26_R01_R08.txt"), rd(E26 + "reejecucion_V26_RV01_RV11_corrida2.txt"), rd(E26 + "reejecucion_V26_W01_W03_previo.txt")]
if rr != exp: b10.append("V26 remota")
ok("S10", not b10, "bloques embebidos comparados con las salidas crudas; discrepancias=%s%s" % (b10, " (modo --prelim: bloque A de V26 no comparado)" if PRELIM else ""))
# S11
L = rd(X + "/LEEME_V26.md") + rd(X + "/INFORME_AUDITORIA_FINAL_V26.md"); ks = ["12 escenarios PARCIAL", "T-409", "indirectamente", "63/63", "14/14", "CCI-DEV", "RLS", "privilegios", "concurrencia", "R1–R9", "HV-02", "PO-05"]
dec = ["PO-05", "G-1", "G-5", "G-10", "DG-19", "DG-20", "DG-09", "DG-12", "DG-16", "DG-18", "DEP-RET-01", "G-9", "RP-01", "P-01 a P-05", "P-10", "OD-13"]
fal = [k for k in ks + dec if k not in L]
ok("S11", not fal, "faltan=%s" % fal)
# S12
lv = rd(X + "/LEEME_V26.md"); k12 = ["**V21:**", "**V22/V23:**", "**V24:**", "**V25:**", "**V26:**", "no constituye aceptación formal", "Fase 1", "Supabase", "salvo él mismo", "estado histórico", "estado actual de publicación"]
ok("S12", all(k in lv for k in k12), "faltan=%s" % [k for k in k12 if k not in lv])
# S13
b13 = []
for d in rg.definiciones(X):
    if "ht" in d:
        for ruta, ver in d["ht"][1]:
            if not ev.has_line(X + "/" + ruta, d["ht"][0]): b13.append((d["ID"], ruta.split("/")[-1]))
    if "needle" in d and not ev.has_line(X + "/" + rg.LIM, d["needle"]): b13.append((d["ID"], "LIM"))
ok("S13", not b13, "líneas-resumen y limitaciones verificadas; faltan=%s" % b13)
# S14
clave = [(r_["Version_origen"], r_["Objetivo"]) for r_ in rows]
ok("S14", len(set(clave)) == len(clave) and all(x["ID_control"] in set(ids) for x in exe) and len(rows) == len(set(ids)), "controles=%d ejecuciones=%d" % (len(rows), len(exe)))
# S15
stt = git("status", "--porcelain", "-uall").split("\n"); stt = [l for l in stt if l]
no = [l for l in stt if not l.startswith("?? docs/fase0/expediente_final_v26/")]
nuevo_ok = git("diff", "--name-only", BASE).strip() == "" if git("rev-parse", "HEAD").strip() == BASE else all(l.split("\t")[0] == "A" for l in git("diff", "--name-status", BASE, "HEAD").split("\n") if l)
fuera = [l for l in git("diff", "--name-only", BASE, "HEAD").split("\n") if l and not l.startswith("docs/fase0/")]
ok("S15", not no and nuevo_ok and not fuera and not re.search(r"docs/fase0/(herramientas|historico)/", "\n".join(stt)), "entradas en git status=%d fuera de alcance=%s" % (len(stt), no[:3]))
# S16
exp16 = {"main": ev.MAIN, "audit/fase0-v19-review": ev.V20, "audit/fase0-v23-review": ev.V23, "audit/fase0-v24-review": ev.V24END, "audit/fase0-v25-review": ev.H25}
b16 = []
for b, s in exp16.items():
    rm = git("ls-remote", "origin", "refs/heads/" + b).split("\t")[0]
    if rm != s: b16.append(("remoto", b))
    if b != "main" and git("rev-parse", b).strip() != s: b16.append(("local", b))
if subprocess.run(["git", "merge-base", "--is-ancestor", BASE, "HEAD"], cwd=W).returncode != 0: b16.append("base")
ok("S16", not b16, "main, V20, V23, V24 y V25 verificados en remoto y local; discrepancias=%s" % b16)
# S17
ex17 = [x for x in exe if x["ID_control"] == "RV07" and x["Resultado"] == "FAIL"]
ok("S17", all(st.get(i) in ("PARTIAL", "NOT VERIFIED") for i in ["L01", "L02", "L03", "L04", "L05", "L06", "L07", "L08", "HT10"]) and ref["Controles FAIL"] == 0 and ref["Controles BLOCKED"] == 0 and len(ex17) == 1 and ref["Ejecuciones FAIL"] == 1, "PARTIAL=%d NOT VERIFIED=%d ejecución FAIL de RV07=%d" % (ref["Controles PARTIAL"], ref["Controles NOT VERIFIED"], len(ex17)))
# S18
need = docs26 + ["MATRIZ_CONTROLES_V26.csv", "EJECUCIONES_CONTROLES_V26.csv", "MAPA_REFERENCIAS_V26.csv", "evidencia_reconstruccion_V26/v26_validar.py", "evidencia_reconstruccion_V26/v26_construir.py", "evidencia_reconstruccion_V26/v26_registro.py", "evidencia_reconstruccion_V26/v26_evaluar.py"]
falt = [f for f in need if not os.path.exists(X + "/" + f)]
sec = rd(X + "/MATRIZ_CAMBIOS_V25_V26.md").split("## Nuevos en V26")[1]
decl = set(re.findall(r"^\| `([^`]+)` \|", sec, re.M)); act = {p for p in allf if not p.startswith("V25_copia_integra/")}
decl_esp = decl if man_ex else decl - {"MANIFIESTO_SHA256_V26.txt"}
ok("S18", not falt and "salvo él mismo" in lv and ("MANIFIESTO_SHA256_V26.txt" in lv) and decl_esp == act, "faltan=%s; declarados sin existir=%s; existentes sin declarar=%s" % (falt, sorted(decl_esp - act), sorted(act - decl_esp)))
if MODE == "C":
    if not man_ex:
        print("FAIL | S19/S20 requieren MANIFIESTO_SHA256_V26.txt"); res.extend([False, False])
    else:
        mm = [l.rstrip("\n").split("  ", 1) for l in open(X + "/MANIFIESTO_SHA256_V26.txt", encoding="utf-8")]
        curx = {p: sh(X + "/" + p) for p in allf if p != "MANIFIESTO_SHA256_V26.txt"}
        NAMES["S19"] = [d["Objetivo"] for d in rg.definiciones(X) if d["ID"] == "S19"][0]; NAMES["S20"] = [d["Objetivo"] for d in rg.definiciones(X) if d["ID"] == "S20"][0]
        ok("S19", {p: h for h, p in mm} == curx and len(mm) == len(set(p for _, p in mm)), "archivos=%d coincidencias=%d" % (len(curx), sum(1 for h, p in mm if curx.get(p) == h)))
        r = subprocess.run("sha256sum -c MANIFIESTO_SHA256_V26.txt", shell=True, cwd=X, capture_output=True, text=True)
        ok("S20", r.returncode == 0 and r.stdout.count(": OK") == len(curx), "OK=%d" % r.stdout.count(": OK"))
n = len(res); f = res.count(False); print("RESUMEN V26: %d controles, %d PASS, %d FAIL" % (n, n - f, f)); sys.exit(1 if f else 0)
