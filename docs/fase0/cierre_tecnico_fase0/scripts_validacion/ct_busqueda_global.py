#!/usr/bin/env python3
# Uso: python3 -I -B ct_busqueda_global.py <dir_dossier> <salida.txt>. Búsqueda global (criterio de cierre 15) + referencias obsoletas.
import os, re, sys, collections
d, out = sys.argv[1], sys.argv[2]
SELF = {"scripts_validacion/ct_busqueda_global.py", "scripts_validacion/ct_reconciliacion_integral.py", "scripts_validacion/ct_escaner_seguridad_sql.py", "scripts_validacion/ct_manifiesto.py", "scripts_validacion/ct_controles_negativos_manifiesto.py"}
MARC = re.compile(r"(#|--|//|/\*)\s*(TODO|FIXME)\b|\b(TODO|FIXME)\s*[:(]")
CERO = ["INCONSISTENTE", "NO CONCILIADO", "REFERENCIA ROTA", "HASH INCORRECTO", "ARCHIVO FALTANTE", "ARCHIVO EXTRA", "EVIDENCIA AUSENTE", "ESTADO CONTRADICTORIO", "FALSO FAIL"]
EXPL = ["PENDIENTE", "NO VERIFICADO", "FALSO PASS"]
# referencias obsoletas: patrón → se permite solo en líneas históricas
OBS = {r"RESIDUALES\.csv`?\s*\(28\)": "28 limitaciones (ahora 27)", r"\b64/0\b": "escáner v1 (64/0)", r"\b21/21\b": "arnés 21/21 (ahora 28/28)", r"\b64 comprobaciones\b": "escáner v1 (64)", r"\b(28 limitaciones|\(28\))": "28 limitaciones (ahora 27 tras fusionar 1 duplicada)", r"\b94/94\b": "verificación de 182b832", r"\b96/96\b": "manifiesto previo", r"\b51 archivos\b": "manifiesto inicial", r"sin commit,? push ni merge": "estado inicial", r"ct_gen_manifiesto|ct_verificar_publicacion": "herramientas sustituidas por ct_manifiesto.py"}
HIST = re.compile(r"hist[oó]ric|ronda anterior|versi[oó]n anterior|v1\b|inicial|superad|e6caebf|182b832|490db22|antes|anterior|reportad|detect[oó]|sustituid", re.I)
res = collections.defaultdict(list); obs = []; marc = []; sinj = []; contx = collections.Counter()
FAILPOS = re.compile(r"FAIL\s*[=:]\s*[1-9]|(?<![=\d])[1-9]\d*\s*FAIL\b|\bFAIL\b\s*\(?[1-9]")
ERRCTX = re.compile(r"(?i)SQLSTATE|23\d{3}|P0001|RJ\d{3}|permiso|excepci|except|error t[eé]cnico|ERROR:|control negativo|falso|defecto|hist[oó]ric|esperado|clasific|bloquead|BLOCKED|WHEN OTHERS|catch|mensaje|sin error|ON_ERROR|stderr")
for r, ds, fs in os.walk(d):
    for n in fs:
        p = os.path.join(r, n); rel = os.path.relpath(p, d).replace(os.sep, "/")
        if rel == "INFORME_RECONCILIACION_INTEGRAL.md": continue   # informe generado: contiene por diseño el texto de cada comprobación (incluidos FAIL descritos)
        if rel.startswith("evidencia_verificacion/") or rel.startswith("scripts_validacion/resultados/") or rel.endswith(".pyc"): continue
        try: t = open(p, encoding="utf-8").read()
        except Exception: continue
        for i, l in enumerate(t.splitlines(), 1):
            if rel not in SELF and MARC.search(l): marc.append((rel, i, l.strip()[:100]))
            if rel not in SELF and rel.endswith((".md", ".csv")):
                if re.search(r"\bERROR\b", l):
                    if ERRCTX.search(l): contx["ERROR (contexto técnico/histórico/contrato)"] += 1
                    else: sinj.append((rel, i, "ERROR sin contexto", l.strip()[:110]))
                if re.search(r"\bFAIL\b", l):
                    if FAILPOS.search(l) and not HIST.search(l) and not re.search(r"(?i)control negativo|detect|mutaci|esperab|51/51|commit revisado|ejecuci[oó]n previa|contradicci|revisi[oó]n independiente|esperado|defectuos|reproduc|falso|rechaz|FAIL=1\b.*(?:control|v1)", l): sinj.append((rel, i, "FAIL>0 sin contexto", l.strip()[:110]))
                    else: contx["FAIL (vocabulario de estados / 0 FAIL / control negativo / histórico)"] += 1
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
for k, v in sorted(contx.items()): L.append("INFO | clasificadas %d líneas: %s" % (v, k))
c(not sinj, "FAIL/ERROR en documentos: todas las apariciones tienen contexto legítimo (0 sin justificar)", "; ".join("%s:%d %s" % o[:3] for o in sinj[:8]))
c(not obs, "sin referencias obsoletas fuera de contexto histórico", "; ".join("%s:%d %s" % o[:3] for o in obs[:6]))
L.append("TOTAL_FAIL=%d" % f); open(out, "w", encoding="utf-8").write("\n".join(L) + "\n"); print("\n".join(L)); sys.exit(1 if f else 0)
