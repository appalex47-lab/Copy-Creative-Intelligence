#!/usr/bin/env python3
# Uso: python3 -I -B ct_gen_manifiesto.py <dir_dossier>. Escribe MANIFIESTO_SHA256_CIERRE.txt (formato sha256sum -c, rutas relativas).
# Excluye: el propio manifiesto, INFORME_PUBLICACION_GITHUB.md (documenta la publicación posterior), __pycache__/*.pyc.
import hashlib, os, sys
d = os.path.abspath(sys.argv[1]); EXCL = {"MANIFIESTO_SHA256_CIERRE.txt", "INFORME_PUBLICACION_GITHUB.md"}
files = []
for r, ds, fs in os.walk(d):
    ds[:] = [x for x in ds if x != "__pycache__"]
    for f in fs:
        rel = os.path.relpath(os.path.join(r, f), d).replace(os.sep, "/")
        if rel in EXCL or f.endswith(".pyc") or os.path.islink(os.path.join(r, f)): continue
        files.append(rel)
files.sort()
assert len(files) == len(set(files))
with open(os.path.join(d, "MANIFIESTO_SHA256_CIERRE.txt"), "w", encoding="utf-8") as o:
    for rel in files:
        o.write("%s  %s\n" % (hashlib.sha256(open(os.path.join(d, rel), "rb").read()).hexdigest(), rel))
print(len(files), "archivos")
