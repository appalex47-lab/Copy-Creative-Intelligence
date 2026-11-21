#!/usr/bin/env python3
# Auditoría independiente de integridad (código propio, no reutiliza ct_manifiesto.py). Uso: aud_integridad.py <clon> <salida.json>
import hashlib, json, os, re, subprocess, sys
r = os.path.abspath(sys.argv[1]); P = "docs/fase0/cierre_tecnico_fase0"; D = os.path.join(r, P); out = {}
files = sorted(os.path.relpath(os.path.join(dp, f), D).replace(os.sep, "/") for dp, _, fs in os.walk(D) for f in fs)
raw = open(os.path.join(D, "MANIFIESTO_SHA256_CIERRE.txt"), "rb").read(); out["manifiesto_CR"] = b"\r" in raw; lines = raw.decode().splitlines()
ent = []; bad_fmt = []
for l in lines:
    m = re.fullmatch(r"([0-9a-f]{64})  (\S.*)", l)
    if not m: bad_fmt.append(l)
    else: ent.append((m.group(2), m.group(1)))
paths = [e[0] for e in ent]
out["manifiesto_entradas"] = len(ent); out["lineas_mal_formadas"] = len(bad_fmt); out["duplicados"] = len(paths) - len(set(paths)); out["orden_bytewise"] = paths == sorted(paths, key=lambda p: p.encode())
out["rutas_inseguras"] = [p for p in paths if p.startswith("/") or ".." in p.split("/") or "\\" in p]
EXCL = ("MANIFIESTO_SHA256_CIERRE.txt",); excl = [f for f in files if f in EXCL or f.startswith("evidencia_verificacion/")]
out["archivos_en_arbol"] = len(files); out["excluidos"] = excl; out["excluidos_fuera_de_politica"] = [f for f in excl if not (f in EXCL or f.startswith("evidencia_verificacion/"))]
sujetos = [f for f in files if f not in excl]; out["faltantes_en_arbol"] = sorted(set(paths) - set(files)); out["extras_sin_listar"] = sorted(set(sujetos) - set(paths))
mal = [p for p, h in ent if p in files and hashlib.sha256(open(os.path.join(D, p), "rb").read()).hexdigest() != h]; out["hash_incorrecto"] = mal; out["hash_verificados"] = len(ent) - len(mal)
out["enlaces_simbolicos"] = [f for f in files if os.path.islink(os.path.join(D, f))]; out["pyc_pycache"] = [f for f in files if f.endswith(".pyc") or "__pycache__" in f]
# exclusiones: ¿ocultan algo? contenido de la carpeta excluida
out["evidencia_archivos"] = [f for f in files if f.startswith("evidencia_verificacion/")]
# SHA citados en documentos: existen como objetos?
def git(*a): return subprocess.run(["git", "-C", r] + list(a), capture_output=True, text=True)
shas = {}
for f in files:
    if f.endswith((".md", ".txt", ".csv")) and not f.startswith("scripts_validacion/resultados/bateria_final/"):
        for s in set(re.findall(r"\b[0-9a-f]{40}\b", open(os.path.join(D, f), encoding="utf-8", errors="replace").read())): shas.setdefault(s, []).append(f)
reales = {s: (git("cat-file", "-t", s).stdout.strip() or "NO_EXISTE_EN_CLON") for s in shas}
# los 40-hex que sean SHA-256 truncados no aplican (64); los de 40 que no son objeto git se listan
out["sha1_citados"] = {s: {"tipo_git": reales[s], "en": sorted(set(shas[s]))[:4]} for s in shas}
json.dump(out, open(sys.argv[2], "w"), indent=1, ensure_ascii=False, sort_keys=True)
print({k: (v if not isinstance(v, (list, dict)) else len(v)) for k, v in out.items()})
