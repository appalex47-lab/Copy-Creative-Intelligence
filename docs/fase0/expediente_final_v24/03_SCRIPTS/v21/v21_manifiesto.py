#!/usr/bin/env python3
"""Manifiesto SHA-256 V21.
Generar:   python3 -I v21_manifiesto.py <dir docs/fase0> --generar
Verificar: python3 -I v21_manifiesto.py <dir docs/fase0> --verificar     (método 1: hashlib; método 2: sha256sum -c; + comprobaciones estructurales)
Reglas de construcción (reproducibles): se incluye todo archivo bajo docs/fase0/ en orden de ruta (bytes), salvo (a) el propio manifiesto (no puede contener su hash),
(b) salidas/salida_integridad_V21*.txt (resultado de verificar este manifiesto: no puede incluirse en lo que verifica), (c) __pycache__, *.pyc, .DS_Store y temporales (los archivos ocultos del expediente, p. ej. .gitattributes, SÍ se incluyen).
La primera línea de datos es el original externo v3.3 (se calcula si está disponible en V33_PATH o /home/claude/fase0_v3_3_integral.md)."""
import hashlib, os, subprocess, sys, re
D = os.path.abspath(sys.argv[1]); G = os.path.abspath(os.path.join(D, "..", ".."))
MAN = os.path.join(D, "expediente_final_v21", "MANIFIESTO_EVIDENCIAS_SHA256_V21.txt")
V33 = os.environ.get("V33_PATH", "/home/claude/fase0_v3_3_integral.md"); V33_SHA = "b5dccdc73a8103966ab1e1b1e84b2e7ead68cd736fba666ec71d0e790d51c1da"
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def excluido(rel):
    b = os.path.basename(rel)
    return (rel == "expediente_final_v21/MANIFIESTO_EVIDENCIAS_SHA256_V21.txt" or re.match(r"expediente_final_v21/salidas/salida_integridad_V21", rel) is not None
            or "__pycache__" in rel or b.endswith((".pyc", ".tmp", ".swp", "~")) or b == ".DS_Store")
def archivos():
    out = []
    for root, ds, fs in os.walk(D):
        ds[:] = [d for d in ds if d != "__pycache__"]
        for f in fs:
            rel = os.path.relpath(os.path.join(root, f), D).replace(os.sep, "/")
            if not excluido(rel): out.append(rel)
    return sorted(out, key=lambda r: r.encode("utf-8"))
def construir():
    L = ["# MANIFIESTO_EVIDENCIAS_SHA256_V21 — 2026-11-20",
         "# Fuente: sha256 de cada archivo bajo docs/fase0/ (rama audit/fase0-v19-review, base V20 ac84133b776cc73c0cb3416e51e2767039bb5132). Reglas y procedimiento de regeneración: cabecera de expediente_final_v21/scripts/v21_manifiesto.py.",
         "# El propio manifiesto y expediente_final_v21/salidas/salida_integridad_V21*.txt no se incluyen (no pueden contener su propio hash)."]
    L.append("%s  (original externo) fase0_v3_3_integral.md" % (sha(V33) if os.path.exists(V33) else V33_SHA))
    for r in archivos(): L.append("%s  %s" % (sha(os.path.join(D, r)), r))
    return "\n".join(L) + "\n"
def parsear(t):
    ent = []
    for l in t.split("\n"):
        if not l or l.startswith("#"): continue
        m = re.match(r"^([0-9a-f]{64})  (.+)$", l)
        if not m: raise SystemExit("línea inválida: %r" % l)
        ent.append((m.group(1), m.group(2)))
    return ent
if "--generar" in sys.argv:
    open(MAN, "w", encoding="utf-8", newline="").write(construir()); print("manifiesto generado: %d archivos" % (len(parsear(construir())) - 1))
elif "--verificar" in sys.argv:
    fallos = []; ok = lambda c, m: print(("PASS" if c else "FAIL"), "|", m) or (c or fallos.append(m))
    t = open(MAN, encoding="utf-8", newline="").read(); ent = parsear(t); rutas = [r for _, r in ent]
    ok(len(rutas) == len(set(rutas)), "sin entradas duplicadas (%d entradas)" % len(rutas))
    ext = [e for e in ent if "(original externo)" in e[1]]; ok(len(ext) == 1 and ext[0][0] == V33_SHA, "original externo v3.3 con SHA-256 b5dccdc7…c1da")
    arch = [e for e in ent if "(original externo)" not in e[1]]
    ok(all(os.path.isfile(os.path.join(D, r)) for _, r in arch), "no hay rutas inexistentes")
    ok(sorted(r for _, r in arch) == archivos(), "el manifiesto cubre exactamente los archivos relevantes (ni faltan ni sobran)")
    ok(not any(excluido(r) for _, r in arch) and not any(re.search(r"__pycache__|\.pyc$|\.tmp$|\.swp$", r) for _, r in arch), "no incluye al propio manifiesto, la salida de integridad ni temporales")
    # método 1: hashlib independiente
    m1 = [(h, r) for h, r in arch if sha(os.path.join(D, r)) != h]; ok(not m1, "método 1 (hashlib): %d discrepancias %s" % (len(m1), [r for _, r in m1][:3]))
    # método 2: sha256sum -c (herramienta externa)
    tmp = os.path.join("/tmp", "v21_sha256sum_check.txt"); open(tmp, "w", encoding="utf-8", newline="").write("".join("%s  %s\n" % (h, r) for h, r in arch))
    r2 = subprocess.run(["sha256sum", "-c", "--quiet", tmp], cwd=D, capture_output=True, text=True); ok(r2.returncode == 0, "método 2 (sha256sum -c): rc=%d %s" % (r2.returncode, r2.stdout.strip()[:120])); os.remove(tmp)
    # históricos: identidad frente al commit V20 (git) y frente al manifiesto V20
    BASE = "ac84133b776cc73c0cb3416e51e2767039bb5132"; mal = []
    for h, r in arch:
        if r.startswith("historico/"):
            b = subprocess.run(["git", "show", "%s:docs/fase0/%s" % (BASE, r)], capture_output=True, cwd=G).stdout
            if hashlib.sha256(b).hexdigest() != h: mal.append(r)
    ok(not mal, "archivos de historico/ idénticos a los del commit V20 (%d comprobados)" % sum(1 for _, r in arch if r.startswith("historico/")))
    # regenerable: reconstruir y comparar byte a byte
    ok(construir() == t, "el manifiesto es regenerable: la reconstrucción coincide byte a byte")
    print("RESUMEN INTEGRIDAD V21: %s" % ("TODO PASS" if not fallos else "FALLOS=%d" % len(fallos))); sys.exit(1 if fallos else 0)
else: print(__doc__)
