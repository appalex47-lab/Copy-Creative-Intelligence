#!/usr/bin/env python3
# Uso: python3 -I -B ct_verificar_publicacion.py <modo> <dir_dossier_descargado> [repo rama]
#  modo "dir": recalcula SHA-256 de un directorio ya descargado (p.ej. git clone fresco) contra su manifiesto.
#  modo "api": descarga cada archivo por la API de GitHub (gh api, contenido base64) y recalcula; <dir> = carpeta de referencia solo para listar el manifiesto del REMOTO (se descarga también).
# Comprobaciones: rutas inseguras/absolutas/duplicadas, el manifiesto no se lista a sí mismo, archivos faltantes, extra (solo se permiten MANIFIESTO e INFORME_PUBLICACION_GITHUB.md), hashes.
import hashlib, os, sys, json, base64, subprocess, re
RUTA = "docs/fase0/cierre_tecnico_fase0"; PERM_EXTRA = {"MANIFIESTO_SHA256_CIERRE.txt", "INFORME_PUBLICACION_GITHUB.md"}
def seguro(p): return not (p.startswith("/") or ".." in p.split("/") or "\\" in p or re.match(r"^[A-Za-z]:", p) or p == "")
def parse(txt):
    out = []
    for l in txt.splitlines():
        m = re.match(r"^([0-9a-f]{64})  (.+)$", l)
        if not m: raise SystemExit("línea de manifiesto inválida: %r" % l)
        out.append((m.group(1), m.group(2)))
    return out
def revisar(entradas, lista_archivos, leer):
    fails = 0; rutas = [p for _, p in entradas]
    def r(ok, n, d=""):
        nonlocal fails; print("%s | %s | %s" % ("PASS" if ok else "FAIL", n, d)); fails += (not ok)
    r(len(rutas) == len(set(rutas)), "sin rutas duplicadas en el manifiesto", str(len(rutas)))
    r(all(seguro(p) for p in rutas), "sin rutas absolutas o inseguras")
    r("MANIFIESTO_SHA256_CIERRE.txt" not in rutas, "el manifiesto no se lista a sí mismo")
    falt = [p for p in rutas if p not in lista_archivos]; extra = [p for p in lista_archivos if p not in rutas and p not in PERM_EXTRA]
    r(not falt, "sin archivos faltantes", str(falt[:5])); r(not extra, "sin archivos extra no declarados", str(extra[:5]))
    mal = [p for h, p in entradas if p in lista_archivos and hashlib.sha256(leer(p)).hexdigest() != h]
    r(not mal, "SHA-256 recalculado coincide en los %d archivos" % len(rutas), str(mal[:5]))
    print("TOTAL_ENTRADAS=%d FAIL=%d" % (len(rutas), fails)); return fails
modo, d = sys.argv[1], sys.argv[2]
if modo == "dir":
    lista = []
    for r_, ds, fs in os.walk(d):
        ds[:] = [x for x in ds if x != "__pycache__"]
        lista += [os.path.relpath(os.path.join(r_, f), d).replace(os.sep, "/") for f in fs]
    ent = parse(open(os.path.join(d, "MANIFIESTO_SHA256_CIERRE.txt"), encoding="utf-8").read())
    sys.exit(1 if revisar(ent, set(lista), lambda p: open(os.path.join(d, p), "rb").read()) else 0)
else:
    repo, rama = sys.argv[3], sys.argv[4]
    tree = json.loads(subprocess.check_output(["gh", "api", "repos/%s/git/trees/%s?recursive=1" % (repo, rama)]))
    assert not tree.get("truncated"), "árbol truncado"
    blobs = {t["path"][len(RUTA) + 1:]: t["sha"] for t in tree["tree"] if t["type"] == "blob" and t["path"].startswith(RUTA + "/")}
    cache = {}
    def leer(p):
        if p not in cache:
            j = json.loads(subprocess.check_output(["gh", "api", "repos/%s/git/blobs/%s" % (repo, blobs[p])]))
            cache[p] = base64.b64decode(j["content"])
        return cache[p]
    ent = parse(leer("MANIFIESTO_SHA256_CIERRE.txt").decode("utf-8"))
    sys.exit(1 if revisar(ent, set(blobs), leer) else 0)
