#!/usr/bin/env python3
"""Controles negativos de ct_manifiesto.py (vías A y B) en un entorno AISLADO (tempfile fuera del repositorio; se borra al terminar).
Vía B se prueba con un `gh` simulado que sirve el árbol manipulado con el mismo formato de la API de GitHub.
Uso: python3 -I -B ct_controles_negativos_manifiesto.py <dir_dossier_a_copiar> <salida.txt>"""
import os, sys, shutil, tempfile, subprocess, hashlib, json, base64, textwrap
src = os.path.abspath(sys.argv[1]); out = sys.argv[2]; here = os.path.dirname(os.path.abspath(__file__)); M = os.path.join(here, "ct_manifiesto.py")
tmp = tempfile.mkdtemp(prefix="ctneg_"); lines = []; fails = 0
FAKE = textwrap.dedent('''
    import sys, os, json, base64, hashlib
    root = sys.argv[1]; args = sys.argv[2:]; RUTA = "docs/fase0/cierre_tecnico_fase0"
    assert args[0] == "api"; ruta = args[1]
    def entries():
        for r, ds, fs in os.walk(root):
            for n in sorted(ds + fs):
                p = os.path.join(r, n)
                if os.path.isdir(p) and not os.path.islink(p): continue
                rel = os.path.relpath(p, root).replace(os.sep, "/")
                if os.path.islink(p): data = os.readlink(p).encode(); mode = "120000"
                else: data = open(p, "rb").read(); mode = "100755" if os.access(p, os.X_OK) else "100644"
                sha = hashlib.sha1(b"blob %d\\0" % len(data) + data).hexdigest()
                yield rel, mode, sha, data
    if "/commits/" in ruta: print(json.dumps({"sha": "f" * 40}))
    elif "/git/trees/" in ruta: print(json.dumps({"truncated": False, "tree": [{"path": RUTA + "/" + rel, "type": "blob", "mode": m, "sha": s} for rel, m, s, _ in entries()]}))
    elif "/git/blobs/" in ruta:
        s = ruta.rsplit("/", 1)[1]
        for rel, m, sh, d in entries():
            if sh == s: print(json.dumps({"content": base64.b64encode(d).decode()})); break
    else: sys.exit(2)
''')
open(os.path.join(tmp, "fake_gh.py"), "w").write(FAKE)
def fresh(name):
    d = os.path.join(tmp, name); shutil.copytree(src, d, symlinks=True); return d
def run(cmd): p = subprocess.run(cmd, capture_output=True, text=True); return p.returncode, p.stdout + p.stderr
def caso(nombre, manip, esperado_ok):
    global fails
    for via in ("A", "B"):
        d = fresh("c"); manip(d)
        if via == "A": rc, o = run([sys.executable, "-I", "-B", M, "dir", d])
        else: rc, o = run([sys.executable, "-I", "-B", M, "api", "x/y", "main", "--gh", "%s -I -B %s %s" % (sys.executable, os.path.join(tmp, "fake_gh.py"), d)])
        ok = (rc == 0) == esperado_ok; fails += (not ok)
        lines.append("%s | vía %s | %s | esperado=%s obtenido_rc=%d" % ("PASS" if ok else "FAIL", via, nombre, "ACEPTA" if esperado_ok else "RECHAZA", rc)); shutil.rmtree(d)
def mf(d): return os.path.join(d, "MANIFIESTO_SHA256_CIERRE.txt")
def rw(d, f):
    s = open(mf(d), encoding="utf-8", newline="").read(); open(mf(d), "w", encoding="utf-8", newline="").write(f(s))
first = lambda d: open(mf(d), encoding="utf-8").read().split("\n")[0]
Z = "0" * 64
caso("control positivo: copia íntegra", lambda d: None, True)
caso("evidencia_verificacion/ añadida (permitida)", lambda d: (os.makedirs(os.path.join(d, "evidencia_verificacion"), exist_ok=True), open(os.path.join(d, "evidencia_verificacion", "x.txt"), "w").write("ok")), True)
caso("archivo modificado (1 byte)", lambda d: open(os.path.join(d, "LEEME_CIERRE_TECNICO.md"), "ab").write(b"x"), False)
caso("archivo eliminado", lambda d: os.remove(os.path.join(d, "PLAN_VALIDACION_CCI_DEV.md")), False)
caso("archivo extra no declarado", lambda d: open(os.path.join(d, "EXTRA.txt"), "w").write("x"), False)
caso("hash del manifiesto alterado", lambda d: rw(d, lambda s: Z + s[64:]), False)
caso("entrada duplicada", lambda d: rw(d, lambda s: s + first(d) + "\n"), False)
caso("ruta absoluta en el manifiesto", lambda d: rw(d, lambda s: s + Z + "  /etc/passwd\n"), False)
caso("ruta con .. en el manifiesto", lambda d: rw(d, lambda s: s + Z + "  ../fuera\n"), False)
caso("manifiesto se lista a sí mismo", lambda d: rw(d, lambda s: s + Z + "  MANIFIESTO_SHA256_CIERRE.txt\n"), False)
caso("manifiesto desordenado", lambda d: rw(d, lambda s: "\n".join(reversed(s.rstrip("\n").split("\n"))) + "\n"), False)
caso("manifiesto con CRLF", lambda d: rw(d, lambda s: s.replace("\n", "\r\n")), False)
caso("manifiesto sin LF final", lambda d: rw(d, lambda s: s.rstrip("\n")), False)
caso("enlace simbólico en el dossier", lambda d: os.symlink("/etc/passwd", os.path.join(d, "enlace.txt")), False)
caso("__pycache__ en el dossier", lambda d: (os.makedirs(os.path.join(d, "__pycache__"), exist_ok=True), open(os.path.join(d, "__pycache__", "a.pyc"), "wb").write(b"x")), False)
def swap(d):  # intercambia el contenido de dos archivos (mismos nombres, hashes cruzados)
    a, b = os.path.join(d, "LEEME_CIERRE_TECNICO.md"), os.path.join(d, "DICTAMEN_PREPARACION_FASE0.md"); x, y = open(a, "rb").read(), open(b, "rb").read(); open(a, "wb").write(y); open(b, "wb").write(x)
caso("contenidos intercambiados entre dos archivos", swap, False)
# determinismo del generador
d1 = fresh("g1"); d2 = fresh("g2")
for d in (d1, d2): subprocess.run([sys.executable, "-I", "-B", M, "gen", d], capture_output=True)
a, b = open(mf(d1), "rb").read(), open(mf(d2), "rb").read(); ok = a == b and len(a) > 0; fails += (not ok)
lines.append("%s | generador determinista (dos generaciones idénticas byte a byte)" % ("PASS" if ok else "FAIL"))
ok2 = open(mf(d1), "rb").read() == open(mf(src) if False else os.path.join(src, "MANIFIESTO_SHA256_CIERRE.txt"), "rb").read(); lines.append("%s | el manifiesto regenerado coincide con el del dossier (informativo)" % ("PASS" if ok2 else "INFO_DIFIERE"))
# verificación --base con un repositorio git temporal
rp = os.path.join(tmp, "repo"); os.makedirs(rp); sub = os.path.join(rp, "docs/fase0/cierre_tecnico_fase0"); shutil.copytree(src, sub)
g = lambda *a: subprocess.run(["git", "-C", rp, "-c", "user.name=t", "-c", "user.email=t@t"] + list(a), capture_output=True, text=True, check=True).stdout.strip()
g("init", "-q"); g("add", "-A"); g("commit", "-qm", "c1"); base = g("rev-parse", "HEAD")
os.makedirs(os.path.join(sub, "evidencia_verificacion"), exist_ok=True); open(os.path.join(sub, "evidencia_verificacion", "r.txt"), "w").write("e"); g("add", "-A"); g("commit", "-qm", "c2")
rc, o = run([sys.executable, "-I", "-B", M, "dir", sub, "--repo", rp, "--base", base]); ok = rc == 0; fails += (not ok); lines.append("%s | --base: commit posterior que solo toca evidencia_verificacion/ (ACEPTA)" % ("PASS" if ok else "FAIL"))
open(os.path.join(sub, "LEEME_CIERRE_TECNICO.md"), "ab").write(b"x"); g("add", "-A"); g("commit", "-qm", "c3")
rc, o = run([sys.executable, "-I", "-B", M, "dir", sub, "--repo", rp, "--base", base]); ok = rc != 0; fails += (not ok); lines.append("%s | --base: commit posterior que cambia otro archivo (RECHAZA)" % ("PASS" if ok else "FAIL"))
shutil.rmtree(tmp)
res = "CONTROLES NEGATIVOS ct_manifiesto.py (entorno aislado en tempfile fuera del repositorio, eliminado al terminar)\n" + "\n".join(lines) + "\nTOTAL=%d FAIL=%d\n" % (len(lines), fails)
open(out, "w", encoding="utf-8").write(res); print(res); sys.exit(1 if fails else 0)
