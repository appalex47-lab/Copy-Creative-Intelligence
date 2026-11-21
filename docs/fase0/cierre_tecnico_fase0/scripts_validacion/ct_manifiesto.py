#!/usr/bin/env python3
"""Manifiesto SHA-256 del dossier: generación y verificación (vía A: directorio/clon; vía B: API de GitHub).
Uso (python3 -I -B):
  ct_manifiesto.py gen <dir_dossier>
  ct_manifiesto.py dir <dir_dossier> [--repo <dir_repo_git> --base <sha>] [--detalle <archivo>]
  ct_manifiesto.py api <owner/repo> <rama_o_sha> [--base <sha>] [--gh <comando_gh>] [--detalle <archivo>]
Diseño de punto fijo: un archivo no puede contener el hash de su propio commit ni la evidencia de la verificación de su propio árbol.
Por eso el manifiesto lista TODOS los archivos del dossier salvo: (1) sí mismo y (2) el directorio evidencia_verificacion/ (evidencia generada
DESPUÉS de verificar el commit de contenido). Con --base <sha> se comprueba además que, entre ese commit de contenido y el HEAD, solo cambió ese directorio.
No hay otras exclusiones: pyc, __pycache__, enlaces simbólicos y archivos no regulares son ERROR (no se omiten en silencio)."""
import hashlib, os, re, sys, json, base64, subprocess
MANIF = "MANIFIESTO_SHA256_CIERRE.txt"; EVID = "evidencia_verificacion/"; RUTA = "docs/fase0/cierre_tecnico_fase0"
def sha(b): return hashlib.sha256(b).hexdigest()
def seguro(p): return bool(p) and not (p.startswith("/") or "\\" in p or re.match(r"^[A-Za-z]:", p) or any(x in ("..", ".", "") for x in p.split("/")) or "\x00" in p or p != p.strip())
def excluido(p): return p == MANIF or p.startswith(EVID)
def parse(txt):
    if not txt.endswith("\n") or "\r" in txt: raise ValueError("el manifiesto debe terminar en LF y no contener CR")
    out = []
    for l in txt.split("\n")[:-1]:
        m = re.match(r"^([0-9a-f]{64})  (.+)$", l)
        if not m: raise ValueError("línea inválida: %r" % l)
        out.append((m.group(1), m.group(2)))
    return out
def listar_dir(d):
    res = []; prob = []
    for r, ds, fs in os.walk(d, followlinks=False):
        for n in list(ds):
            if os.path.islink(os.path.join(r, n)): prob.append("enlace simbólico (dir): " + os.path.relpath(os.path.join(r, n), d)); ds.remove(n)
        for n in fs:
            p = os.path.join(r, n); rel = os.path.relpath(p, d).replace(os.sep, "/")
            if os.path.islink(p) or not os.path.isfile(p): prob.append("no regular/enlace: " + rel); continue
            if "__pycache__" in rel.split("/") or rel.endswith(".pyc"): prob.append("artefacto de Python: " + rel)
            res.append(rel)
    return sorted(res), prob
def gen(d):
    files, prob = listar_dir(d)
    if prob: raise SystemExit("ERROR: " + "; ".join(prob))
    f = [x for x in files if not excluido(x)]
    assert all(seguro(x) for x in f) and len(f) == len(set(f))
    with open(os.path.join(d, MANIF), "w", encoding="utf-8", newline="\n") as o:
        for x in f: o.write("%s  %s\n" % (sha(open(os.path.join(d, x), "rb").read()), x))
    print("generado: %d entradas" % len(f))
def revisar(ent, txt_raw, arbol, leer, prob, detalle):
    """arbol: set de rutas del dossier (incluye manifiesto y evidencia); leer(p)->bytes"""
    fails = 0; out = []
    def r(ok, n, d=""):
        nonlocal fails; out.append("%s | %s | %s" % ("PASS" if ok else "FAIL", n, d)); fails += (not ok)
    rutas = [p for _, p in ent]
    r(not prob, "sin enlaces simbólicos, no regulares ni artefactos de Python", "; ".join(prob[:5]))
    r(rutas == sorted(rutas), "manifiesto ordenado de forma determinista (orden bytewise de rutas)")
    r(len(rutas) == len(set(rutas)), "sin rutas duplicadas", str(len(rutas)))
    r(all(seguro(p) for p in rutas), "sin rutas absolutas, relativas inseguras ni con caracteres de control", str([p for p in rutas if not seguro(p)][:5]))
    r(MANIF not in rutas and not any(p.startswith(EVID) for p in rutas), "el manifiesto no se lista a sí mismo ni lista la evidencia posterior")
    r(MANIF in arbol, "el manifiesto está en el árbol")
    esperado = sorted(p for p in arbol if not excluido(p))
    falt = [p for p in rutas if p not in arbol]; extra = [p for p in esperado if p not in set(rutas)]
    r(not falt, "ninguna entrada del manifiesto falta en el árbol", str(falt[:5])); r(not extra, "ningún archivo del árbol queda sin entrada (salvo manifiesto y %s)" % EVID, str(extra[:5]))
    mal = []
    for h, p in ent:
        if p in arbol:
            ok = sha(leer(p)) == h; out.append("  %s %s %s" % ("OK " if ok else "MAL", h[:16], p)); mal += [] if ok else [p]
    r(not mal, "SHA-256 recalculado sobre los bytes reales coincide en %d/%d entradas" % (len(rutas) - len(mal), len(rutas)), str(mal[:5]))
    r(len(rutas) == len(esperado), "entradas (%d) = archivos sujetos a verificación (%d)" % (len(rutas), len(esperado)))
    out.append("TOTAL_ENTRADAS=%d ARCHIVOS_EN_ARBOL=%d EXCLUIDOS_DECLARADOS=%d FAIL=%d" % (len(rutas), len(arbol), len(arbol) - len(esperado), fails))
    return fails, out
def main(a):
    modo = a[0]
    if modo == "gen": return gen(a[1])
    opt = {}; pos = []; i = 1
    while i < len(a):
        if a[i].startswith("--"): opt[a[i][2:]] = a[i + 1]; i += 2
        else: pos.append(a[i]); i += 1
    cab = []
    if modo == "dir":
        d = os.path.abspath(pos[0]); files, prob = listar_dir(d)
        head = ""
        if "repo" in opt:
            head = subprocess.check_output(["git", "-C", opt["repo"], "rev-parse", "HEAD"], text=True).strip()
        cab.append("VIA=A (directorio/clon) DIR=%s HEAD=%s" % (d, head or "n/d"))
        ent = parse(open(os.path.join(d, MANIF), encoding="utf-8", newline="").read())
        fails, out = revisar(ent, None, set(files), lambda p: open(os.path.join(d, p), "rb").read(), prob, None)
        if "base" in opt:
            nombres = subprocess.check_output(["git", "-C", opt["repo"], "diff", "--name-only", opt["base"], "HEAD"], text=True).split()
            fuera = [n for n in nombres if not n.startswith(RUTA + "/" + EVID)]
            out.append("%s | entre el commit de contenido %s y HEAD solo cambió %s (%d rutas; fuera: %s)" % ("PASS" if not fuera else "FAIL", opt["base"][:10], EVID, len(nombres), fuera[:5])); fails += bool(fuera)
    else:
        repo, ref = pos[0], pos[1]; gh = opt.get("gh", "gh").split()
        api = lambda ruta: json.loads(subprocess.check_output(gh + ["api", ruta]))
        head = api("repos/%s/commits/%s" % (repo, ref))["sha"]
        cab.append("VIA=B (API de GitHub; blobs descargados) REPO=%s REF=%s HEAD=%s" % (repo, ref, head))
        tree = api("repos/%s/git/trees/%s?recursive=1" % (repo, head)); assert not tree.get("truncated")
        blobs = {}; prob = []
        for t in tree["tree"]:
            if t["path"].startswith(RUTA + "/"):
                rel = t["path"][len(RUTA) + 1:]
                if t["type"] == "blob":
                    if t["mode"] not in ("100644", "100755"): prob.append("modo %s (enlace/no regular): %s" % (t["mode"], rel))
                    if "__pycache__" in rel.split("/") or rel.endswith(".pyc"): prob.append("artefacto de Python: " + rel)
                    blobs[rel] = t["sha"]
        cache = {}
        def leer(p):
            if p not in cache: cache[p] = base64.b64decode(api("repos/%s/git/blobs/%s" % (repo, blobs[p]))["content"])
            return cache[p]
        ent = parse(leer(MANIF).decode("utf-8"))
        fails, out = revisar(ent, None, set(blobs), leer, prob, None)
        if "base" in opt:
            cmp_ = api("repos/%s/compare/%s...%s" % (repo, opt["base"], head)); nombres = [f["filename"] for f in cmp_["files"]]
            fuera = [n for n in nombres if not n.startswith(RUTA + "/" + EVID)]
            out.append("%s | entre el commit de contenido %s y HEAD solo cambió %s (%d rutas; fuera: %s)" % ("PASS" if not fuera else "FAIL", opt["base"][:10], EVID, len(nombres), fuera[:5])); fails += bool(fuera)
    txt = "\n".join(cab + out) + "\nRESULTADO=%s\n" % ("OK" if not fails else "FALLO")
    if "detalle" in opt: open(opt["detalle"], "w", encoding="utf-8").write(txt)
    print("\n".join(l for l in (cab + out) if not l.startswith("  ")) + "\nRESULTADO=%s" % ("OK" if not fails else "FALLO")); return 1 if fails else 0
if __name__ == "__main__": sys.exit(main(sys.argv[1:]) or 0)
