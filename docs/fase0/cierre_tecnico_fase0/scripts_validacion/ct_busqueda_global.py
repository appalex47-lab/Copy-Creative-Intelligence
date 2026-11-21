#!/usr/bin/env python3
# Uso: python3 -I -B ct_busqueda_global.py <dir_dossier> <salida.txt>. Búsqueda global (criterio de cierre 15) + referencias obsoletas.
import os, re, sys, collections
d, out = sys.argv[1], sys.argv[2]
SELF = {"scripts_validacion/ct_busqueda_global.py", "scripts_validacion/ct_reconciliacion_integral.py", "scripts_validacion/ct_escaner_seguridad_sql.py", "scripts_validacion/ct_manifiesto.py", "scripts_validacion/ct_controles_negativos_manifiesto.py"}
MARC = re.compile(r"(#|--|//|/\*)\s*(TODO|FIXME)\b|\b(TODO|FIXME)\s*[:(]")
CERO = ["INCONSISTENTE", "NO CONCILIADO", "REFERENCIA ROTA", "HASH INCORRECTO", "ARCHIVO FALTANTE", "ARCHIVO EXTRA", "EVIDENCIA AUSENTE", "ESTADO CONTRADICTORIO", "FALSO FAIL"]
EXPL = ["PENDIENTE", "NO VERIFICADO", "FALSO PASS"]
# referencias obsoletas: patrón → se permite solo en líneas históricas
OBS = {r"\b21/21\b": "arnés 21/21 (ahora 28/28)", r"\b64 comprobaciones\b": "escáner v1 (64)", r"\b(28 limitaciones|\(28\))": "28 limitaciones (ahora 27 tras fusionar 1 duplicada)", r"\b94/94\b": "verificación de 182b832", r"\b96/96\b": "manifiesto previo", r"\b51 archivos\b": "manifiesto inicial", r"sin commit,? push ni merge": "estado inicial", r"ct_gen_manifiesto|ct_verificar_publicacion": "herramientas sustituidas por ct_manifiesto.py"}
HIST = re.compile(r"hist[oó]ric|ronda anterior|versi[oó]n anterior|v1\b|inicial|superad|e6caebf|182b832|490db22|antes|anterior|reportad|detect[oó]|sustituid", re.I)
res = collections.defaultdict(list); obs = []; marc = []
for r, ds, fs in os.walk(d):
    for n in fs:
        p = os.path.join(r, n); rel = os.path.relpath(p, d).replace(os.sep, "/")
        if rel.startswith("evidencia_verificacion/") or rel.startswith("scripts_validacion/resultados/") or rel.endswith(".pyc"): continue
        try: t = open(p, encoding="utf-8").read()
        except Exception: continue
        for i, l in enumerate(t.splitlines(), 1):
            if rel not in SELF and MARC.search(l): marc.append((rel, i, l.strip()[:100]))
            for k in CERO + EXPL:
                if k in l and rel not in SELF: res[k].append(rel)
            if rel not in SELF:
                for pat, why in OBS.items():
                    if re.search(pat, l) and not HIST.search(l): obs.append((rel, i, why, l.strip()[:110]))
L = ["BÚSQUEDA GLOBAL (excluye resultados/, evidencia_verificacion/ y los scripts que contienen los patrones como definición)"]; f = 0
def c(ok, n, det=""):
    global f; L.append("%s | %s | %s" % ("PASS" if ok else "FAIL", n, det)); f += (not ok)
c(not marc, "marcadores TODO/FIXME de código: 0", str(marc[:3]))
for k in CERO: c(not res[k], "«%s»: 0 apariciones" % k, ",".join(sorted(set(res[k]))[:4]))
for k in EXPL: L.append("INFO | «%s»: %d apariciones en %d archivos (descripciones de limitaciones/estados/pruebas negativas, con justificación en las matrices)" % (k, len(res[k]), len(set(res[k]))))
c(not obs, "sin referencias obsoletas fuera de contexto histórico", "; ".join("%s:%d %s" % o[:3] for o in obs[:6]))
L.append("TOTAL_FAIL=%d" % f); open(out, "w", encoding="utf-8").write("\n".join(L) + "\n"); print("\n".join(L)); sys.exit(1 if f else 0)
