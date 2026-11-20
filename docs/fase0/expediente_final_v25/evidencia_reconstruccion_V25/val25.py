#!/usr/bin/env python3
"""Validación V25 (P01-P14 previa al manifiesto; Q01-Q02 solo si MANIFIESTO_SHA256_V25.txt existe). Uso: python3 -I val25.py <raiz del worktree>"""
import os, sys, re, csv, io, hashlib, subprocess
W = os.path.abspath(sys.argv[1]); V5 = W + "/docs/fase0/expediente_final_v25"; BASE = "b88bde038e331ba67899632ca4e09eebf2cde82d"; res = []
def ok(i, n, c, d=""): res.append(c); print(("PASS" if c else "FAIL"), "|", i, n, "|", d)
sh = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
rd = lambda p: open(p, encoding="utf-8", newline="").read()
def git(*a, raw=False):
    r = subprocess.run(["git"] + list(a), cwd=W, capture_output=True); return r.stdout if raw else r.stdout.decode()
cur = {os.path.relpath(os.path.join(a, f), V5): sh(os.path.join(a, f)) for a, _, x in os.walk(V5) for f in x}
v24 = [p for p in git("ls-tree", "-r", "--name-only", BASE, "docs/fase0/expediente_final_v24/", "docs/fase0/REPORTE_PUBLICACION_V24_GITHUB.md").split("\n") if p]
def rel(p): return p[len("docs/fase0/expediente_final_v24/"):] if p.startswith("docs/fase0/expediente_final_v24/") else "V24_publicacion/REPORTE_PUBLICACION_V24_GITHUB.md"
old = {rel(p): hashlib.sha256(git("show", BASE + ":" + p, raw=True)).hexdigest() for p in v24}
ident = sorted(k for k in old if cur.get(k) == old[k]); mod = sorted(k for k in old if k in cur and cur[k] != old[k]); aus = sorted(k for k in old if k not in cur); nue = sorted(set(cur) - set(old))
MOD = sorted(["REPORTE_VALIDACION_V24.md", "INFORME_CORRECCIONES_V24.md", "MATRIZ_OBSERVACIONES_V23_V24.md", "V24_publicacion/REPORTE_PUBLICACION_V24_GITHUB.md"])
ok("P01", "Faltantes: ningún archivo de V24 ausente en V25", not aus and len(old) == 258, "archivos V24=%d ausentes=%s" % (len(old), aus))
decl = re.findall(r"^\| `([^`]+)` \| .* \|$", rd(V5 + "/MATRIZ_CAMBIOS_V24_V25.md").split("## Nuevos en V25")[1].split("## Todos")[0], re.M)
falt = sorted(set(decl) - set(nue)); extra = sorted(set(nue) - set(decl)); man_ex = os.path.exists(V5 + "/MANIFIESTO_SHA256_V25.txt")
ok("P02", "Adicionales: los archivos nuevos son exactamente los 17 declarados en MATRIZ_CAMBIOS", len(decl) == 17 and not extra and (not falt if man_ex else falt in ([], ["MANIFIESTO_SHA256_V25.txt"])), "nuevos=%d adicionales=%s sin_crear=%s" % (len(nue), extra, falt))
low = [p.lower() for p in cur]; bad = [p for p in cur if p.startswith("/") or ".." in p.split("/") or "\\" in p or p != p.strip()]
ok("P03", "Rutas duplicadas (sin distinguir mayúsculas) o inseguras (absolutas, con .., con \\)", len(set(low)) == len(low) and not bad, "archivos=%d" % len(cur))
ok("P04", "Matriz de hashes V24→V25: idénticos/modificados/nuevos/ausentes", mod == MOD and not aus, "idénticos=%d modificados=%d nuevos=%d ausentes=%d" % (len(ident), len(mod), len(nue), len(aus)))
nota_ok = True
for f in MOD:
    t = rd(V5 + "/" + f); mk = "\n> **Nota de conciliación V25 (2026-11-20):**"
    if t.count(mk) != 1: nota_ok = False; continue
    i = t.index(mk); j = t.index("\n", i + 2) + 1
    if hashlib.sha256((t[:i] + t[j:]).encode("utf-8")).hexdigest() != old[f]: nota_ok = False
ok("P05", "Los 4 modificados son solo inserciones: quitando la nota V25 se recupera el archivo V24 byte a byte", nota_ok)
ev = [k for k in old if k.startswith(("03_SCRIPTS", "04_RESULTADOS", "05_LOGS", "02_MATRICES", "06_DIFF"))]
ok("P06", "Evidencias técnicas, scripts, resultados, matrices y diff de V24 sin alteración", all(cur.get(k) == old[k] for k in ev) and len(ev) == 234, "%d archivos" % len(ev))
hist = ["MANIFIESTO_SHA256_V24.txt", "00_LEEME/LEEME_EXPEDIENTE_V21.md", "08_INTEGRIDAD_Y_MANIFIESTOS/SHA256SUMS.txt"]
r = subprocess.run("sha256sum -c MANIFIESTO_SHA256_V24.txt 2>&1 | grep -v ': OK$'", shell=True, cwd=V5, capture_output=True, text=True).stdout.strip().split("\n")
fall = sorted(l.split(":")[0] for l in r if l.endswith("FAILED"))
ok("P07", "Históricos V24 intactos; el manifiesto V24 falla exactamente en los 3 archivos con nota V25 (esperado)", all(cur[k] == old[k] for k in hist) and fall == sorted(["REPORTE_VALIDACION_V24.md", "INFORME_CORRECCIONES_V24.md", "MATRIZ_OBSERVACIONES_V23_V24.md"]), "fallos=%s" % fall)
docs = {f: rd(V5 + "/" + f) for f in MOD + ["INFORME_CONCILIACION_CONTROLES_V25.md", "LEEME_V25.md", "REPORTE_VALIDACION_V25.md"]}
cons = all("18 controles" in docs[f] for f in docs if f not in ("LEEME_V25.md", "REPORTE_VALIDACION_V25.md")) and "18 controles distintos" in docs["LEEME_V25.md"] and "16/16 PASS" in docs["INFORME_CONCILIACION_CONTROLES_V25.md"] and "18/18 PASS" in docs["INFORME_CONCILIACION_CONTROLES_V25.md"] and "16 controles de validación distintos (P01–P14 y Q01–Q02)" in docs["REPORTE_VALIDACION_V25.md"]
ok("P08", "Cifra consolidada (18 controles distintos; 16 previa / 18 final; 8 remotos) presente y coherente en todos los documentos V25", cons)
rows = list(csv.DictReader(io.StringIO(rd(V5 + "/MATRIZ_CONTROLES_V25.csv"), newline="")))
okst = all(x["Estado"] in ("PASS", "FAIL", "BLOCKED", "NOT VERIFIED") for x in rows); evok = all(x["Estado"] != "PASS" or any(os.path.exists(V5 + "/" + t) for t in re.findall(r"evidencia_reconstruccion_V25/[\w.\-]+", x["Evidencia"])) for x in rows)
ok("P09", "Matriz de controles: 18 C + 8 R, estados válidos y cada PASS con evidencia existente", len(rows) == 26 and sum(x["ID"][0] == "C" for x in rows) == 18 and sum(x["ID"][0] == "R" for x in rows) == 8 and okst and evok)
E_ = V5 + "/evidencia_reconstruccion_V25/"
def parse(p): return [m.group(1) for m in (re.match(r"(PASS|FAIL) \|", l) for l in rd(E_ + p).split("\n")) if m]
A = parse("salida_val24_pasada_A_previa_manifiesto.txt"); C = parse("salida_val24_pasada_C_posterior_manifiesto.txt"); N = parse("reejecucion_V25_val24_sobre_V24.txt")
cr = [x for x in rows if x["ID"][0] == "C"]
ok("P10", "Estados de la matriz = salidas crudas archivadas (pasada A: 16, pasada C: 18, re-ejecución V25: 18)", len(A) == 16 and len(C) == 18 and len(N) == 18 and all(cr[i]["Estado"] == ("PASS" if C[i] == N[i] == "PASS" and (i >= 16 or A[i] == "PASS") else "FAIL") for i in range(18)))
def blk(t): return re.search(r"```\n(.*?)```", t, re.S).group(1)
ok("P11", "Los bloques embebidos en los reportes V24 (A en validación, C en publicación) = salidas crudas archivadas", blk(docs["REPORTE_VALIDACION_V24.md"]) == rd(E_ + "salida_val24_pasada_A_previa_manifiesto.txt") and blk(docs["V24_publicacion/REPORTE_PUBLICACION_V24_GITHUB.md"]) == rd(E_ + "salida_val24_pasada_C_posterior_manifiesto.txt"))
L = rd(V5 + "/LEEME_V25.md") + rd(V5 + "/INFORME_CONCILIACION_CONTROLES_V25.md"); ks = ["63/63", "14/14", "12 escenarios PARCIAL", "T-409", "indirectamente", "CCI-DEV", "RLS", "privilegios", "concurrencia", "esquema físico", "R1–R9", "HV-02", "PO-05", "G-1", "G-5", "G-10", "DG-19", "DG-20", "DG-09", "DG-12", "DG-16", "DG-18", "DEP-RET-01", "G-9", "RP-01", "P-01", "P-05", "P-10", "OD-13"]
fal = [k for k in ks if k not in L]; ok("P12", "Limitaciones y decisiones pendientes conservadas explícitamente", not fal, "faltan=%s" % fal)
st = git("status", "--porcelain", "-uall"); ok("P13", "Alcance: nada fuera de docs/fase0/ ni en herramientas/ o historico/ reales", not [l for l in st.split("\n") if l and " docs/fase0/" not in l] and not re.search(r" docs/fase0/(herramientas|historico)/", st))
lv = rd(V5 + "/LEEME_V25.md"); ok("P14", "LEEME_V25 explica V21 / V23 / V24 / V25 / no aceptación formal / no Fase 1 ni Supabase", all(k in lv for k in ["**V21:**", "**V22/V23:**", "**V24:**", "**V25:**", "no constituye aceptación formal de Fase 0", "No autoriza Fase 1 ni validaciones en Supabase"]))
if man_ex:
    m = [l.rstrip("\n").split("  ", 1) for l in open(V5 + "/MANIFIESTO_SHA256_V25.txt", encoding="utf-8")]; c2 = dict(cur); c2.pop("MANIFIESTO_SHA256_V25.txt")
    ok("Q01", "MANIFIESTO_SHA256_V25 cubre exactamente todos los archivos (salvo él mismo) y todos los hashes coinciden (hashlib)", {p: h for h, p in m} == c2 and len(m) == len(set(p for _, p in m)), "archivos=%d coincidencias=%d" % (len(m), sum(1 for h, p in m if c2.get(p) == h)))
    r = subprocess.run("sha256sum -c MANIFIESTO_SHA256_V25.txt", shell=True, cwd=V5, capture_output=True, text=True); ok("Q02", "sha256sum -c MANIFIESTO_SHA256_V25.txt desde expediente_final_v25/ (método independiente)", r.returncode == 0 and r.stdout.count(": OK") == len(m), "OK=%d" % r.stdout.count(": OK"))
n = len(res); f = res.count(False); print("RESUMEN V25: %d controles, %d PASS, %d FAIL" % (n, n - f, f)); sys.exit(1 if f else 0)
