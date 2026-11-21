#!/usr/bin/env python3
"""Mapa de referencias a archivos de los documentos de la copia V25 (V26). Uso: python3 -I v26_mapa_referencias.py <expediente_final_v26> <salida.csv>
Resuelve cada referencia entre comillas invertidas a un archivo dentro del paquete (sin modificar ningún documento)."""
import os, re, sys, csv, collections
X = os.path.abspath(sys.argv[1]); V = X + "/V25_copia_integra"; out = sys.argv[2]
allf = [os.path.relpath(os.path.join(a, f), V) for a, _, x in os.walk(V) for f in x]
base = collections.defaultdict(list)
for p in allf: base[os.path.basename(p)].append(p)
corr = {}
for r in csv.DictReader(open(V + "/08_INTEGRIDAD_Y_MANIFIESTOS/CORRESPONDENCIA_RUTAS_ORIGEN.csv", encoding="utf-8", newline="")):
    corr[r["ruta_original_en_repositorio_o_externa"]] = r["ruta_en_paquete"]
EXT = "md|csv|txt|py|sh|patch|tsv|zip|json"
SKIP = ("04_RESULTADOS", "05_LOGS", "03_SCRIPTS", "06_DIFF", "02_MATRICES")
docs = []
for p in allf:
    if p.endswith(tuple("." + e for e in EXT.split("|"))) and not p.startswith(SKIP) and "MANIFIESTO" not in p and "SHA256SUMS" not in p and "inventario" not in p.lower() and not p.startswith("MATRIZ_CAMBIOS") and not p.startswith("evidencia_reconstruccion_V25/historico") :
        docs.append(p)
rows = []
for d in sorted(docs):
    t = open(V + "/" + d, encoding="utf-8", errors="replace").read()
    for ref in sorted(set(re.findall(r"`([\w./\-]+\.(?:" + EXT + r"))`", t))):
        cands = [os.path.normpath(os.path.join(os.path.dirname(d), ref)), os.path.normpath(ref)]
        st = None; res = []
        for c in cands:
            if c in allf: st, res = "EXACTA", [c]; break
        if st is None:
            for k in (ref, "docs/fase0/" + ref, ref.replace("../", ""), "docs/fase0/" + ref.replace("../", "")):
                if k in corr: st, res = "POR_CORRESPONDENCIA_RUTAS_ORIGEN", [corr[k]]; break
        if st is None and ref.endswith("CCI_FASE0_EXPEDIENTE_V21_V23.zip"):
            st, res = "EXTERNA_AL_EXPEDIENTE", ["(ZIP de entrega en docs/fase0/entregas/ de la rama audit/fase0-v23-review; no forma parte del expediente)"]
        if st is None and re.match(r"(\.\./)?REPORTE_PUBLICACION_V2[45]_GITHUB\.md$", ref):
            st, res = "EXTERNA_AL_EXPEDIENTE_COPIADA", ["V25_publicacion/REPORTE_PUBLICACION_V25_GITHUB.md" if "V25" in ref else "V25_copia_integra/V24_publicacion/REPORTE_PUBLICACION_V24_GITHUB.md"]
        if st is None:
            b = base.get(os.path.basename(ref), [])
            if len(b) == 1: st, res = "POR_NOMBRE_UNICO", b
            elif len(b) > 1: st, res = "POR_NOMBRE_VARIAS_COPIAS", sorted(b)[:3]
        if st is None: st, res = "NO_RESUELTA", []
        rows.append([d, ref, st, " | ".join(res), len(res)])
with open(out, "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, lineterminator="\n"); w.writerow(["documento", "referencia", "estado", "resolucion_en_el_paquete", "n_candidatos_mostrados"]); w.writerows(rows)
c = collections.Counter(r[2] for r in rows); print("referencias=%d" % len(rows), dict(c))
for r in rows:
    if r[2] == "NO_RESUELTA": print("NO_RESUELTA:", r[0], r[1])
