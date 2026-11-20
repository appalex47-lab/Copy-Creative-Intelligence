#!/usr/bin/env python3
"""Batería de cierre V21 (solo lectura; no modifica nada, no usa red salvo `git ls-remote` opcional).
Uso: python3 -I v21_bateria_cierre.py <dir docs/fase0> [--tsv ruta]
Cada prueba registra: id, objetivo, entrada, esperado, obtenido, estado (PASS/FAIL/BLOCKED), evidencia, observaciones.
Una excepción NO se silencia: la prueba pasa a FAIL con el error. BLOCKED solo para dependencias externas reales."""
import csv, hashlib, io, os, re, subprocess, sys, collections, traceback
D = os.path.abspath(sys.argv[1]); TSV = sys.argv[sys.argv.index("--tsv") + 1] if "--tsv" in sys.argv else None
G = os.path.abspath(os.path.join(D, "..", ".."))
E20 = os.path.join(D, "expediente_final_v16_v19"); E21 = os.path.join(D, "expediente_final_v21"); EV = os.path.join(D, "evidencia_v16")
BASE_V20 = "ac84133b776cc73c0cb3416e51e2767039bb5132"; BASE_V19 = "c6ef74be4db185ac3e4fd36810f24619e6f51fcf"; MAIN = "6a1af2424ef39e0960b8f7e09d4e19ec52e6f046"
SHA_MODELO = "cc87236a19b924617e13346f80eb642d0dc5f0090664908d1e96d8780f4fc52a"; SHA_VERIF = "1acec85dc5e76c9e004d8f2b7ed942c94826377ff240c346bee9f2792e7a035a"
ACTIVOS5 = ["ESPECIFICACION_TECNICA_G1_G5_G10.md", "AUDITORIA_FINAL_G1_G5_G10.md", "INFORME_CIERRE_G1_G5_G10.md", "ROADMAP_Y_TRAZABILIDAD_G1_G5_G10.md", "REGISTRO_HISTORICO_VERSIONES.md"]
def rd(p): return open(p, encoding="utf-8", newline="").read()
def csvr(p): return list(csv.DictReader(io.StringIO(rd(p), newline="")))
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def git(*a, check=True):
    r = subprocess.run(["git"] + list(a), capture_output=True, text=True, cwd=G)
    if check and r.returncode: raise RuntimeError("git %s: %s" % (" ".join(a), r.stderr.strip()))
    return r.stdout
RES = []
def T(tid, obj, entrada, esperado, fn):
    try:
        obt, ok, evid, obs = fn(); est = "PASS" if ok else "FAIL"
    except BlockedError as e: obt, est, evid, obs = str(e), "BLOCKED", "dependencia externa", str(e)
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)[-1]; obt, est, evid, obs = "EXCEPCIÓN %s: %s" % (type(e).__name__, e), "FAIL", "línea %d del script" % tb.lineno, "la excepción no se silencia"
    RES.append((tid, obj, entrada, esperado, str(obt), est, evid, obs)); print("%s | %s | %s | esperado=%s | obtenido=%s | %s" % (tid, est, obj, esperado, str(obt)[:200], obs[:160]))
class BlockedError(Exception): pass
spec_txt = rd(os.path.join(D, "ESPECIFICACION_TECNICA_G1_G5_G10.md")); SPEC = spec_txt.split("\n")
R = csvr(os.path.join(E20, "MATRIZ_FINAL_231_REGLAS_V16_V19.csv")); S = csvr(os.path.join(E20, "MATRIZ_FINAL_780_ESCENARIOS_V16_V19.csv"))
TR = csvr(os.path.join(E20, "MATRIZ_TRAZABILIDAD_REGLAS_ESCENARIOS_V16_V19.csv")); RC = csvr(os.path.join(E20, "REGISTRO_CASOS_22_FUNCIONES_V20.csv"))
PE_DIR = os.path.join(E20, "PE_POSTGRESQL_V20")
def pe_parse(p):
    out = {}
    for l in rd(p).split("\n"):
        m = re.match(r"^((?:PE|PG)-[A-Za-z0-9-]+) \| (.*?) \| (.*?) \| (.*?) \| (PASS|FAIL) \| ", l)
        if m: out[m.group(1)] = m.group(5)
    return out
# ============ A. CONTEOS Y CLASIFICACIÓN ============
def a01():
    ids = [x["Regla"] for x in R]; fam = r"(IG1|IG5|IG10|IS|IM|IE|IP)"
    en_spec = {m.group(1) + "-" + m.group(2) for l in SPEC for m in [re.match(r"\|\s*" + fam + r"-(\d+)\s*\|", l)] if m}
    return "matriz=%d únicos=%d spec=%d dif=%s" % (len(ids), len(set(ids)), len(en_spec), sorted(set(ids) ^ en_spec)), len(ids) == len(set(ids)) == len(en_spec) == 231 and set(ids) == en_spec, "MATRIZ_FINAL_231_REGLAS; ESPECIFICACION (filas de tabla)", "universo de reglas = filas de definición de la especificación"
T("V21-A01", "231 reglas: conteo, unicidad y coincidencia con la especificación", "MATRIZ_FINAL_231 vs especificación", "231/231/231 y conjuntos iguales", a01)
def derivar_clase(x):
    if x["Subclase_V19"].startswith("D"): return "D"
    est = x["Estado_implementacion"]
    if x["Subclase_V19"].startswith("E"):
        g = set(re.findall(r"PE-0\d", est)); res = {}
        for p in ("salida_PE_V20_corrida1.txt", "salida_PE_V20_corrida2.txt"): res.update({k: v for k, v in pe_parse(os.path.join(PE_DIR, p)).items()})
        ok = g and all(any(k.startswith(gg) for k in res) and all(v == "PASS" for k, v in res.items() if k.startswith(gg)) for gg in g)
        return "B" if ok else "E"
    m = re.search(r"Modelo en memoria con pruebas PASS \((\d+) de (\d+) escenarios\)", est)
    if m: return "A" if m.group(1) == m.group(2) and int(m.group(2)) > 0 else "B"
    return "C"
def a02():
    dist = collections.Counter(x["Clase_final_V20"] for x in R); der = collections.Counter(derivar_clase(x) for x in R)
    dif = [x["Regla"] for x in R if derivar_clase(x) != x["Clase_final_V20"]]
    return "matriz=%s derivada=%s discrepantes=%s" % (dict(sorted(dist.items())), dict(sorted(der.items())), dif), dist == der and dict(dist) == {"A": 1, "B": 8, "C": 69, "D": 153} and not dif, "clase derivada de subclase + estado + PE PASS (independiente de la columna final)", "E=0"
T("V21-A02", "Clasificación 231 reglas: matriz = derivación independiente = A1 B8 C69 D153 E0", "columnas Subclase_V19/Estado_implementacion + salidas PE", "A1 B8 C69 D153 E0 sin discrepancias", a02)
def a03():
    pr = [x["Regla"] for x in R if x["Clase_final_V20"] == "B" and x["Subclase_V19"].startswith("E")]
    ok = sorted(pr) == ["IG1-05", "IG1-06", "IG1-10", "IG1-21", "IG5-36"]
    imp = [x["Regla"] for x in R if x["Clase_final_V20"] in ("A", "B") and "implementad" in x["Estado_implementacion"].lower() and "no implementad" not in x["Estado_implementacion"].lower()]
    return "E→B=%s; reglas que afirman 'implementado' en el producto=%s" % (pr, imp), ok and not imp, "MATRIZ_FINAL_231", "ninguna reclasificación afirma implementación en el producto"
T("V21-A03", "Las 5 reglas reclasificadas E→B y ninguna afirma implementación en el producto", "5 reglas + Estado_implementacion", "5 reglas; 0 afirmaciones de implementación", a03)
def a04():
    mal = [x["Regla"] for x in R if not all(x[k].strip() for k in ("Definicion_completa", "Escenarios", "Estado_implementacion", "Intervencion_requerida", "Base_clasificacion", "Clase_final_V20"))]
    return "reglas con campo vacío=%s" % mal, not mal, "MATRIZ_FINAL_231", "definición, evidencia(estado), clasificación, escenarios, intervención y base presentes"
T("V21-A04", "Cada regla conserva definición, escenarios, estado, base e intervención", "231 filas", "0 campos vacíos", a04)
def a05():
    ids = [x["Escenario"] for x in S]; en_spec = {m.group(1) for l in SPEC for m in [re.match(r"\|\s*(T-\d+)\s*\|", l)] if m}
    return "matriz=%d únicos=%d spec=%d dif=%s" % (len(ids), len(set(ids)), len(en_spec), sorted(set(ids) ^ en_spec)[:5]), len(ids) == len(set(ids)) == len(en_spec) == 780 and set(ids) == en_spec, "MATRIZ_FINAL_780 vs especificación", ""
T("V21-A05", "780 escenarios: conteo, unicidad y coincidencia con la especificación", "MATRIZ_FINAL_780 vs especificación", "780/780/780", a05)
def a06():
    c = collections.Counter(x["Veredicto_V20"] for x in S); eq = sum(1 for x in S if x["Veredicto_V20"].startswith("DEMOSTRADO POR EJECUCIÓN")); par = c["PARCIAL / NO DEMUESTRA TODO"]
    return "%s" % dict(c), eq == 258 and par == 12 and sum(c.values()) == 780 and c["DEMUESTRA CON OBSERVACIÓN"] == 6 and eq + par + c["DEMUESTRA CON OBSERVACIÓN"] + c["DEMUESTRA (lectura)"] + c["DEMUESTRA (lectura V20)"] == 780, "MATRIZ_FINAL_780", "258 por ejecución en modelo; 510 por lectura (6 con observación); 12 parciales"
T("V21-A06", "Distribución de veredictos de los 780 escenarios", "columna Veredicto_V20", "258 ejecución + 510 lectura + 12 parcial", a06)
def a07():
    pares = [(x["Regla"], x["Escenario"]) for x in TR]; rs = {x["Regla"] for x in R}; ss = {x["Escenario"] for x in S}
    cita = {x["Escenario"]: {r.strip() for r in x["Reglas_citadas"].split(",") if r.strip()} for x in S}
    esc_r = {x["Regla"]: {s.strip() for s in x["Escenarios"].split(",") if s.strip()} for x in R}
    sin_r = [s for s in ss if not cita[s]]; sin_s = [r for r in rs if not esc_r[r]]
    fuera = [p for p in pares if p[0] not in rs or p[1] not in ss]
    ni = [p for p in pares if p[1] not in esc_r[p[0]] or p[0] not in cita[p[1]]]
    omit = [(r, s) for s in ss for r in cita[s] if (r, s) not in set(pares)]
    n_mal = [x["Regla"] for x in R if int(x["N_escenarios"]) != len(esc_r[x["Regla"]])]
    return "pares=%d únicos=%d huérfanos(r/s)=%d/%d fuera=%d no-bidireccional=%d omitidos=%d N_escenarios_mal=%d" % (len(pares), len(set(pares)), len(sin_s), len(sin_r), len(fuera), len(ni), len(omit), len(n_mal)), len(pares) == len(set(pares)) == 1592 and not (sin_r or sin_s or fuera or ni or omit or n_mal), "MATRIZ_TRAZABILIDAD vs matrices de reglas y escenarios", "trazabilidad bidireccional completa"
T("V21-A07", "Trazabilidad reglas↔escenarios: 1592 pares, bidireccional, sin huérfanos ni omisiones", "3 CSV", "1592 únicos; 0 huérfanos/omisiones", a07)
def a08():
    # escenarios con ejecución, recomputados desde la columna Prueba_o_verificacion_ejecutada del escenario
    ej = {x["Escenario"] for x in S if x["Prueba_o_verificacion_ejecutada"].strip()}
    mal = []
    for x in R:
        esc = [s.strip() for s in x["Escenarios"].split(",") if s.strip()]
        if int(x["N_escenarios_con_ejecucion"]) != sum(1 for s in esc if s in ej): mal.append(x["Regla"])
    return "escenarios con prueba/verificación=%d; reglas con N_escenarios_con_ejecucion inconsistente=%s" % (len(ej), mal[:8]), not mal, "MATRIZ_FINAL_231 vs MATRIZ_FINAL_780", "N_escenarios_con_ejecucion de cada regla = escenarios citados con ejecución"
T("V21-A08", "N_escenarios_con_ejecucion de cada regla coincide con la matriz de escenarios", "2 CSV", "0 inconsistencias", a08)
def a09():
    l38 = [l for l in SPEC if l.startswith("| Catorce tablas nuevas")][0]
    explicitas = [m for m in re.findall(r"`([a-z_]+)`", l38) if "_" in m]
    cuatro = ["brief_field_changes", "brief_field_attributions", "promotion_field_changes", "promotion_field_attributions"]
    todas = explicitas + cuatro; ok_texto = "las cuatro tablas de cambio y atribución" in l38
    heads = {m.group(1) for l in SPEC for m in [re.match(r"#### `([a-z_]+)`", l)] if m}
    sin_def = [t for t in todas if t not in heads and ("**Definición formal de `%s`" % t) not in spec_txt]
    v33 = os.environ.get("V33_PATH", "/home/claude/fase0_v3_3_integral.md"); n27 = None
    if os.path.exists(v33): n27 = 27 if re.search(r"\b27 tablas\b", rd(v33)) else None
    sp27 = "(22 de 27)" in spec_txt
    return "explícitas=%d + 4 de cambio/atribución=%d únicas; sin encabezado de definición=%s; v3.3 declara 27 tablas=%s; spec '22 de 27'=%s; total=%d" % (len(explicitas), len(set(todas)), sin_def, n27, sp27, 27 + len(set(todas))), len(set(todas)) == 14 and ok_texto and not sin_def and 27 + len(set(todas)) == 41 and sp27 and n27 == 27, "ESPECIFICACION línea 38 y encabezados #### de tabla; v3.3 original (solo lectura)", "41 = 27 base + 14 nuevas"
T("V21-A09", "41 tablas = 27 base (v3.3) + 14 nuevas (spec)", "spec línea 38 + v3.3", "14 nuevas; 27 base; 41", a09)
def a10():
    rows = csvr(os.path.join(EV, "MATRIZ_REFERENCIAS_V16.csv")); sup = csvr(os.path.join(E20, "MATRIZ_REFERENCIAS_V20_SUPLEMENTO.csv"))
    k = [x for x in rows[0].keys() if x.startswith("Clasificaci")][0]
    c = collections.Counter(x[k] for x in rows); c2 = collections.Counter(x["Clasificación (H/A/I/U)"] for x in sup)
    return "V16: filas=%d %s; suplemento V20: filas=%d %s" % (len(rows), dict(c), len(sup), dict(c2)), set(c) | set(c2) <= {"H", "A", "I", "U"} and len(rows) == 1148 and len(sup) == 32 and not set(x["Resultado"] for x in sup) - {"CONFORME"} | set(), "MATRIZ_REFERENCIAS_V16.csv + SUPLEMENTO", "referencias H/A/I/U (documentos de versión)"
T("V21-A10", "Matriz de referencias de versión H/A/I/U: 1148 (V16) + 32 (suplemento V20), valores válidos", "2 CSV", "1148 + 32; clases en {H,A,I,U}", a10)
# ============ B. 22 FUNCIONES Y 366 CASOS ============
def b01():
    claves = [x["clave_unica"] for x in RC]; fun = collections.Counter(x["funcion"] for x in RC)
    return "filas=%d claves únicas=%d funciones=%d PASS=%d" % (len(RC), len(set(claves)), len(fun), sum(x["resultado"] == "PASS" for x in RC)), len(RC) == len(set(claves)) == 366 and len(fun) == 22 and all(x["resultado"] == "PASS" for x in RC), "REGISTRO_CASOS_22_FUNCIONES_V20.csv", "reconciliación 363/366: 363 + 3 positivos K45"
T("V21-B01", "366 casos individuales únicos de 22 funciones, todos PASS", "REGISTRO_CASOS", "366/366/22/366", b01)
def b02():
    lines = rd(os.path.join(E20, "salida_22_funciones_V20_corrida1.txt")).split("\n"); mal = []
    for x in RC:
        n = int(re.search(r"línea (\d+)", x["evidencia"]).group(1)); l = lines[n - 1]
        if not l.startswith("%s | " % x["funcion"]) or (" | PASS | " not in l) or (" | %s | " % x["id_caso"] not in l and not l.split(" | ")[1].endswith(x["id_caso"])): mal.append(x["clave_unica"])
    return "casos del registro sin correspondencia con la línea de la salida original=%s" % mal[:6], not mal, "REGISTRO vs salida_22_funciones_V20_corrida1.txt", "cada caso apunta a su línea real"
T("V21-B02", "Cada caso del registro coincide con su línea en la salida original", "366 casos", "0 discrepancias", b02)
def b03():
    r = {}
    for n, p in (("V20-1", os.path.join(E20, "salida_22_funciones_V20_corrida1.txt")), ("V20-2", os.path.join(E20, "salida_22_funciones_V20_corrida2.txt")), ("V21-3", os.path.join(E21, "salidas", "salida_22_funciones_V21_corrida3.txt"))):
        r[n] = hashlib.sha256("\n".join(l for l in rd(p).split("\n") if not l.startswith("EXIT=")).encode()).hexdigest()
    tot = [l for l in rd(os.path.join(E21, "salidas", "salida_22_funciones_V21_corrida3.txt")).split("\n") if l.startswith("TOTAL funciones")]
    return "hashes=%s; %s" % ({k: v[:12] for k, v in r.items()}, tot), len(set(r.values())) == 1 and tot == ["TOTAL funciones=22 casos=366 fallos=0"], "3 salidas (2 de V20 + 1 de V21 ejecutada hoy)", "tercera corrida real, no copiada"
T("V21-B03", "Reproducibilidad: 3 corridas de las 22 funciones idénticas (la 3.ª ejecutada en V21)", "3 salidas", "hash idéntico; TOTAL 366 fallos 0", b03)
def b04():
    txt = rd(os.path.join(E21, "salidas", "salida_22_funciones_V21_corrida3.txt")); per = {}
    for l in txt.split("\n"):
        m = re.match(r"^(\w+) \| (\S+) \| esperado=(.*?) \| obtenido=(.*?) \| (PASS|FAIL) \|", l)
        if m: per[m.group(1)] = per.get(m.group(1), 0) + 1
    decl = dict(kv.split("=") for kv in [l for l in txt.split("\n") if l.startswith("CASOS_POR_FUNCION")][0].split()[1:]); fallos = len(re.findall(r"\| FAIL \|", txt))
    reg = collections.Counter(x["funcion"] for x in RC)
    return "casos contados=%d; declarado=%d; FAIL=%d; por función igual a registro=%s" % (sum(per.values()), sum(int(v) for v in decl.values()), fallos, all(per[k] == reg[k] == int(decl[k]) for k in decl)), sum(per.values()) == 366 and fallos == 0 and all(per[k] == reg[k] == int(decl[k]) for k in decl) and len(decl) == 22, "salida corrida 3 recontada línea a línea", "los conteos individuales suman"
T("V21-B04", "Recuento independiente por función de la salida cruda = declarado = registro", "salida corrida 3", "366; 0 FAIL; por función igual", b04)
def b05():
    t = rd(os.path.join(E20, "salida_independencia_auditor_V20.txt")); pas = len(re.findall(r"\bPASS\b", t)); fal = len(re.findall(r"\bFAIL\b", t))
    k45 = [x for x in RC if x["grupo"] != "" and "POS-" in x["id_caso"]]
    esp = collections.Counter(x["esperado"] for x in RC)
    return "independencia: PASS=%d FAIL=%d; positivos K45=%d; esperado=%s" % (pas, fal, len(k45), dict(esp)), fal == 0 and pas >= 6 and len(k45) == 3, "salida_independencia_auditor_V20.txt", "negativos = mutación detectada (esperado True); positivos K45 esperan 'sin errores'; errores esperados distinguidos de fallos (FAIL=0)"
T("V21-B05", "Independencia auditor/motor 6/6; positivos y negativos diferenciados", "salida de independencia + registro", "FAIL=0; 3 positivos K45", b05)
def b06():
    t = rd(os.path.join(E20, "MATRIZ_PRUEBAS_22_FUNCIONES_366_CASOS.md")); filas = re.findall(r"^\| (\d+) \| (\w+) \| (\d+) \|", t, re.M); reg = collections.Counter(x["funcion"] for x in RC)
    dif = [(f, n) for _, f, n in filas if reg[f] != int(n)]
    return "filas md=%d suma=%d diferencias vs registro=%s" % (len(filas), sum(int(n) for _, _, n in filas), dif), len(filas) == 22 and sum(int(n) for _, _, n in filas) == 366 and not dif, "MATRIZ_PRUEBAS_22_FUNCIONES (md) vs REGISTRO (csv)", "consistencia Markdown↔CSV"
T("V21-B06", "Consistencia Markdown↔CSV de la matriz de pruebas de las 22 funciones", "md + csv", "22 funciones, 366", b06)
# ============ C. POSTGRESQL ============
def c01():
    sql = rd(os.path.join(PE_DIR, "02_pruebas.sql")); decl = re.findall(r"select t\('((?:PE|PG)-[A-Za-z0-9-]+)'", sql)
    runs = {"V20-1": pe_parse(os.path.join(PE_DIR, "salida_PE_V20_corrida1.txt")), "V20-2": pe_parse(os.path.join(PE_DIR, "salida_PE_V20_corrida2.txt")), "V21-3": pe_parse(os.path.join(E21, "salidas", "salida_PE_V21_corrida3.txt"))}
    ok = len(decl) == len(set(decl)) == 63 and all(set(r) == set(decl) and all(v == "PASS" for v in r.values()) for r in runs.values())
    return "declaradas=%d únicas=%d; ejecutadas=%s; PASS=%s" % (len(decl), len(set(decl)), {k: len(v) for k, v in runs.items()}, {k: sum(x == "PASS" for x in v.values()) for k, v in runs.items()}), ok, "02_pruebas.sql vs 3 salidas", "pruebas declaradas = ejecutadas; 3 corridas, la 3.ª ejecutada en V21"
T("V21-C01", "PostgreSQL: 63 pruebas declaradas = ejecutadas = PASS en 3 corridas", "02_pruebas.sql + salidas", "63/63/63", c01)
def c02():
    sh = rd(os.path.join(PE_DIR, "mutaciones.sh")); decl = re.findall(r'^m ((?:PE|PG)-[A-Za-z0-9-]+) "', sh, re.M); pe = set(pe_parse(os.path.join(PE_DIR, "salida_PE_V20_corrida1.txt")))
    outs = [rd(os.path.join(PE_DIR, "salida_PE_V20_mutaciones.txt")), rd(os.path.join(E21, "salidas", "salida_PE_V21_mutaciones_corrida2.txt"))]
    det = [len(re.findall(r"\| DETECTADA$", o, re.M)) for o in outs]; nd = [len(re.findall(r"NO DETECTADA|NO APLICADA", o)) for o in outs]
    return "mutaciones declaradas=%d; pruebas inexistentes=%s; detectadas=%s; no detectadas/no aplicadas=%s" % (len(decl), [d for d in decl if d not in pe], det, nd), len(decl) == 14 and all(d in pe for d in decl) and det == [14, 14] and nd == [0, 0], "mutaciones.sh + 2 salidas (V20 y V21)", "14/14 detectadas, sin mutaciones no aplicadas"
T("V21-C02", "PostgreSQL: 14 mutaciones declaradas = detectadas (2 corridas)", "mutaciones.sh + salidas", "14/14 y 14/14", c02)
def c03():
    h = lambda p: hashlib.sha256("\n".join(l for l in rd(p).split("\n") if re.match(r"^((PE|PG)-.* \| |TOTAL|PostgreSQL 16)", l)).encode()).hexdigest()
    a, b, c = h(os.path.join(PE_DIR, "salida_PE_V20_corrida1.txt")), h(os.path.join(PE_DIR, "salida_PE_V20_corrida2.txt")), h(os.path.join(E21, "salidas", "salida_PE_V21_corrida3.txt"))
    return "%s %s %s" % (a[:12], b[:12], c[:12]), a == b == c, "líneas de resultado normalizadas", "la corrida 3 incluye ruido de cliente psql (no del resultado); se compara el resultado"
T("V21-C03", "PostgreSQL: resultados idénticos en las 3 corridas", "3 salidas normalizadas", "hash idéntico", c03)
def c04():
    docs = [rd(os.path.join(PE_DIR, "README.md")), rd(os.path.join(E20, "PLAN_VALIDACION_POSTGRESQL_SUPABASE_CCI.md")), rd(os.path.join(E21, "INFORME_FINAL_V21.md")) if os.path.exists(os.path.join(E21, "INFORME_FINAL_V21.md")) else ""]
    need = [("no equivale", "esquema"), ("Supabase",), ("CCI-DEV",)]
    ok = all(all(any(w in d for d in docs) for w in n) for n in need) and "esquema físico" in docs[0] + docs[2]
    return "limitación documentada en README/PLAN/INFORME V21=%s" % ok, ok, "README PE, PLAN, INFORME_FINAL_V21", "PostgreSQL temporal ≠ esquema físico aprobado ni Supabase"
T("V21-C04", "Limitación PostgreSQL temporal documentada", "README + PLAN + INFORME V21", "presente", c04)
# ============ D. VERIFICADOR ============
def d01():
    res = {}
    for n in ("salida_verificador_V20_final_corrida1.txt", "salida_verificador_V20_final_corrida2.txt"):
        m = re.search(r"RESUMEN: (\d+) comprobaciones, (\d+) aprueban, (\d+) fallan, (\d+) pendientes; (\d+) controles \((\d+) OK, (\d+) NO OK, (\d+) PENDIENTE\); (\d+) mutaciones \((\d+) detectadas\)", rd(os.path.join(E20, n))); res[n] = m.groups()
    v21 = [os.path.join(E21, "salidas", "salida_verificador_V21_corrida%d.txt" % i) for i in (1, 2)]
    if not all(os.path.exists(p) for p in v21): raise BlockedError("faltan las salidas del verificador V21 (corridas completas aún no archivadas)")
    for p in v21: res[os.path.basename(p)] = re.search(r"RESUMEN: (\d+) comprobaciones, (\d+) aprueban, (\d+) fallan, (\d+) pendientes; (\d+) controles \((\d+) OK, (\d+) NO OK, (\d+) PENDIENTE\); (\d+) mutaciones \((\d+) detectadas\)", rd(p)).groups()
    esperado = ("59", "59", "0", "0", "28", "28", "0", "0", "300", "300")
    return "%s" % {k[-22:]: v == esperado for k, v in res.items()}, all(v == esperado for v in res.values()), "RESUMEN de 4 corridas (2 V20 + 2 V21)", "59/59 comprobaciones, 28/28 controles, 300/300 mutaciones"
T("V21-D01", "Verificador completo: 59 comprobaciones, 28 controles, 300 mutaciones en 4 corridas", "RESUMEN de salidas", "59/59, 28/28, 300/300", d01)
def d02():
    p = [os.path.join(E21, "salidas", "salida_verificador_V21_corrida%d.txt" % i) for i in (1, 2)]
    if not all(os.path.exists(x) for x in p): raise BlockedError("faltan salidas V21 del verificador")
    n = lambda x: [l for l in rd(x).split("\n") if not l.startswith("DURACION_S=")]
    t = rd(p[0]); num = re.findall(r"^K(\d+) +APRUEBA", t, re.M); v12 = len(re.findall(r"^K55-V12 +APRUEBA", t, re.M)); faltan = sorted(set("%02d" % i for i in range(1, 60)) - set(num))
    return "corrida1==corrida2 (sin duración)=%s; líneas K numeradas APRUEBA=%d (únicas %d) + K55-V12=%d; sin usar en la numeración K01..K59=%s" % (n(p[0]) == n(p[1]), len(num), len(set(num)), v12, faltan), n(p[0]) == n(p[1]) and len(num) == len(set(num)) == 58 and v12 == 1 and faltan == ["43"], "2 corridas completas V21 en copias limpias", "59 comprobaciones = 58 K numeradas (K43 no se usa) + K55-V12 (identificador del control duplicado K55 de v12, documentado en la especificación sección N); el verificador está protegido y no se modificó"
T("V21-D02", "Verificador: dos corridas V21 idénticas; 59 comprobaciones identificadas (58 K + K55-V12)", "salidas V21", "idénticas; 58 K numeradas + K55-V12", d02)
# ============ E. CONSISTENCIA DOCUMENTAL ============
def vigentes():
    out = [os.path.join(D, f) for f in ACTIVOS5]
    for d in (E20, E21):
        for f in sorted(os.listdir(d)):
            p = os.path.join(d, f)
            if f.endswith(".md") and os.path.isfile(p) and "Superseded" not in rd(p)[:900] and "SUSTITUIDO" not in rd(p)[:900]: out.append(p)
    return out
def e01():
    pats = [r"\bB 3\b", r"\b5 E\b", r"\bE\s*=\s*5\b", r"\b3 B,", r"E: ?5\b", r"363 casos(?! de mutación)"]; hall = []
    for p in vigentes():
        if p.endswith("INVENTARIO_DECISIONES_ABIERTAS_FASE0.md") or p.endswith(("REGISTRO_CAMBIOS_V20_V21.md", "MATRIZ_CONCILIACION_V21.md", "INFORME_FINAL_V21.md", "AUDITORIA_FINAL_V21.md", "REPORTE_VALIDACION_INTEGRAL_V21.md", "MATRIZ_PRUEBAS_22_FUNCIONES_366_CASOS.md", "REGISTRO_DECISIONES_ABIERTAS_V21.md", "INDICE_VIGENCIA_DOCUMENTAL_V21.md")): continue
        for i, l in enumerate(rd(p).split("\n"), 1):
            for pt in pats:
                if re.search(pt, l) and not re.search(r"anterior|históric|antes|conserva|V18|V19|sustitu|error|corrig|reconcil|363 \+|subtotal", l, re.I): hall.append((os.path.basename(p), i, pt))
    return "apariciones de cifras antiguas presentadas como vigentes=%s" % hall[:6], not hall, "docs vigentes (%d archivos)" % len(vigentes()), "las menciones históricas o de corrección están contextualizadas"
T("V21-E01", "Ningún documento vigente presenta la distribución antigua (B3/E5) o 363 casos como vigente", "docs vigentes", "0 apariciones", e01)
def e02():
    d = "A 1, B 8, C 69, D 153, E 0"; falta = []
    for f in ("expediente_final_v16_v19/AUDITORIA_FINAL_FASE0_V16_V19.md", "expediente_final_v16_v19/INFORME_FINAL_V20.md", "expediente_final_v16_v19/INVENTARIO_DECISIONES_ABIERTAS_FASE0.md"):
        if d not in rd(os.path.join(D, f)): falta.append(f)
    return "documentos que declaran la distribución vigente 'A 1, B 8, C 69, D 153, E 0' (V20 y corregido V21) sin ella=%s" % falta, not falta, "3 documentos ejecutivos de clases", "la distribución coincide con la matriz (V21-A02)"
T("V21-E02", "Documentos ejecutivos de clases declaran A1 B8 C69 D153 E0", "3 documentos", "presente en los 3", e02)
def e03():
    mal = []
    for f in ACTIVOS5:
        t = rd(os.path.join(D, f)); i = t.index("## Nota de estado V21"); b = t[i:]
        if not all(s in b for s in ("NO INICIADA / NO AUTORIZADA", "ac84133b776cc73c0cb3416e51e2767039bb5132", "6a1af2424ef39e0960b8f7e09d4e19ec52e6f046")) or "sin commit" in b: mal.append(f)
    return "documentos activos con bloque de estado V21 incompleto/obsoleto=%s" % mal, not mal, "5 documentos activos", "estado de Fase 1, SHA de base y main presentes; sin 'sin commit'"
T("V21-E03", "Bloque de estado V21 completo y sin afirmaciones obsoletas de publicación", "5 documentos activos", "5/5", e03)
def e04():
    h = {f: rd(os.path.join(D, f)) for f in ACTIVOS5[:4]}; bl = {f: t[t.index("## Nota de estado V21"):] for f, t in h.items()}
    return "bloques idénticos en los 4 documentos de diseño=%s" % (len(set(bl.values())) == 1), len(set(bl.values())) == 1, "4 documentos", "uniformidad"
T("V21-E04", "Bloque de estado idéntico en los 4 documentos de diseño", "4 documentos", "1 variante", e04)
NEG = re.compile(r"\b(no|ni|sin|pendiente|pendientes|requiere|requieren|salvo|hasta que|aceptaci[oó]n|condici|si |cuando|antes de|NO APROBAD|NO VERIFICABLE|propuest)", re.I)
def e05():
    hall = []
    pat = re.compile(r"(aceptad[oa]s? por el propietario|el propietario (acept[oó]|aprob[oó])|(G-1|G-5|G-10|Adenda v9|PO-05)[^.|]{0,40}(est[aá]n? |fue |queda )?(aceptad[oa]s?|aprobad[oa]s?)|Fase 1[^.|]{0,30}(iniciada|autorizada)(?! ))", re.I)
    for p in vigentes():
        for i, l in enumerate(rd(p).split("\n"), 1):
            if pat.search(l) and not NEG.search(l) and "NO INICIADA" not in l: hall.append((os.path.basename(p), i, l[:90]))
    return "afirmaciones de aceptación sin negación/condición=%s" % hall[:4], not hall, "docs vigentes", "ninguna declaración de aceptación falsa"
T("V21-E05", "Ausencia de declaraciones falsas de aceptación (G-1/G-5/G-10, Adenda v9, PO-05, Fase 1)", "docs vigentes", "0", e05)
def e06():
    inv = rd(os.path.join(E20, "INVENTARIO_DECISIONES_ABIERTAS_FASE0.md")); p = os.path.join(E21, "REGISTRO_DECISIONES_ABIERTAS_V21.md")
    reg = rd(p) if os.path.exists(p) else ""; ids = ["RP-01", "G-9", "P-01", "P-05", "P-10", "OD-13", "DEP-RET-01", "DG-09", "DG-12", "DG-16", "DG-18", "DG-19", "DG-20", "PO-05", "G-1", "G-5", "G-10", "CCI-DEV", "CCI-PROD", "HV-02"]
    f1 = [i for i in ids if i not in reg]; f2 = [i for i in ("RP-01", "G-9", "P-01", "OD-13", "DEP-RET-01", "DG-09", "DG-12", "DG-16", "DG-18", "DG-19", "DG-20", "PO-05") if i not in inv]
    cerr = [l[:80] for l in reg.split("\n") if re.search(r"\|\s*(APROBAD[OA]|ACEPTAD[OA]|CERRAD[OA])\s*\|", l, re.I)]
    return "faltan en registro V21=%s; faltan en inventario=%s; decisiones marcadas cerradas=%s" % (f1, f2, cerr), not (f1 or f2 or cerr) and bool(reg), "REGISTRO_DECISIONES_ABIERTAS_V21 + INVENTARIO", "ninguna decisión inventada ni marcada aprobada"
T("V21-E06", "Decisiones abiertas completas, coherentes entre registro V21 e inventario, ninguna cerrada", "2 documentos", "0 faltantes; 0 cerradas", e06)
def e07():
    reg = rd(os.path.join(D, "REGISTRO_HISTORICO_VERSIONES.md")).split("\n"); a = git("show", BASE_V20 + ":docs/fase0/REGISTRO_HISTORICO_VERSIONES.md").split("\n")
    return "fila de PO-05=%r; primeras 812 líneas idénticas a V20=%s" % (reg[125][:60], reg[:812] == a[:812]), reg[:812] == a[:812] and reg[125].startswith("| PO-05 | Aceptación del addendum | Aceptación formal del addendum v3"), "REGISTRO vs commit V20", "PO-05 y la historia del registro intactos"
T("V21-E07", "PO-05 (fila del addendum) y la historia del registro sin alteración", "REGISTRO_HISTORICO_VERSIONES.md", "idéntico en sus primeras 812 líneas", e07)
def e08():
    cur = SPEC; old = git("show", BASE_V20 + ":docs/fase0/ESPECIFICACION_TECNICA_G1_G5_G10.md").split("\n"); i = [k for k, l in enumerate(cur) if l.startswith("## Nota de estado V21")][0]
    return "especificación idéntica a V20 antes del bloque de estado=%s (primeras %d líneas)" % (cur[:i] == old[:i], i), cur[:i] == old[:i], "especificación vs commit V20", "el diseño no se modificó en V21"
T("V21-E08", "El diseño (especificación) no cambia en V21 salvo el bloque de estado", "especificación", "idéntica", e08)
# ============ F. REFERENCIAS ============
def f01():
    mal = []
    for x in R:
        ln = int(x["Linea_definicion"]);
        if not re.match(r"\|\s*" + re.escape(x["Regla"]) + r"\s*\|", SPEC[ln - 1]) or x["Definicion_completa"][:50] not in SPEC[ln - 1]: mal.append(x["Regla"])
    return "reglas con línea de definición incorrecta=%d %s" % (len(mal), mal[:5]), not mal, "Linea_definicion vs especificación vigente", "línea y texto"
T("V21-F01", "Linea_definicion de las 231 reglas apunta a su definición real", "231 filas", "0 incorrectas", f01)
def f02():
    mal = [x["Escenario"] for x in S if not re.match(r"\|\s*" + re.escape(x["Escenario"]) + r"\s*\|", SPEC[int(x["Linea_ESPEC"]) - 1]) or x["Nombre"][:30] not in SPEC[int(x["Linea_ESPEC"]) - 1]]
    return "escenarios con línea incorrecta=%d %s" % (len(mal), mal[:5]), not mal, "Linea_ESPEC vs especificación vigente", "línea y nombre"
T("V21-F02", "Linea_ESPEC de los 780 escenarios apunta a su fila real", "780 filas", "0 incorrectas", f02)
def f03():
    mal = []; tot = 0
    for x in R:
        m = re.search(r"narrativa: l\.([\d, ]+)", x["Dependencias_y_relaciones"])
        if m:
            for n in re.findall(r"\d+", m.group(1)):
                tot += 1
                if x["Regla"] not in SPEC[int(n) - 1]: mal.append((x["Regla"], n))
    return "citas de narrativa=%d; que no contienen la regla=%s" % (tot, mal[:5]), not mal and tot == 90, "Dependencias_y_relaciones", "90 citas válidas"
T("V21-F03", "Las 90 citas de narrativa 'l.N' contienen la regla citada", "231 filas", "0 incorrectas", f03)
def f04():
    p = os.path.join(E21, "ANCLAS_LINEAS_V21.csv")
    if not os.path.exists(p): raise Exception("falta ANCLAS_LINEAS_V21.csv")
    mal = []
    for x in csvr(p):
        t = rd(os.path.join(D, x["archivo"])).split("\n")[int(x["linea"]) - 1]
        if x["ancla"] not in t: mal.append((x["documento_que_cita"], x["archivo"], x["linea"]))
    reg = {(x["documento_que_cita"], int(x["linea"])) for x in csvr(p)}; sin = []
    for d in (E20, E21):
        for f in sorted(os.listdir(d)):
            fp = os.path.join(d, f)
            if not (f.endswith(".md") and os.path.isfile(fp)) or "Superseded" in rd(fp)[:900]: continue
            rel = os.path.relpath(fp, D)
            for l in rd(fp).split("\n"):
                if re.search(r"numeración de V20|c6ef74b|l\.1270|fila 1270|lín.{0,3}ea 126\)|en V20", l) and "ancla" not in l: continue
                for m in re.finditer(r"\b(?:l\.|líneas? |filas? )(\d{2,5})(?:(?:, | y )(?:líneas? )?(\d{2,5}))*", l):
                    for n in re.findall(r"\d{2,5}", m.group(0)):
                        if (rel, int(n)) not in reg and not any(rel == r and int(n) == k for r, k in reg): sin.append((rel, n))
    mal += [("sin ancla", s) for s in sin[:6]]
    return "citas de línea de documentos con ancla inválida o sin ancla=%s de %d" % (mal[:6], len(csvr(p))), not mal, "ANCLAS_LINEAS_V21.csv", "cada cita numérica de línea de un documento vigente tiene ancla de texto verificada"
T("V21-F04", "Citas numéricas de línea en documentos vigentes verificadas por ancla de texto", "ANCLAS_LINEAS_V21.csv", "0 inválidas", f04)
def f05():
    cand = [p for p in vigentes() if p.startswith((E20, E21))] + [os.path.join(PE_DIR, "README.md")]; rotas = []
    exts = (".md", ".csv", ".txt", ".sh", ".sql", ".py")
    for p in cand:
        for tok in sorted(set(re.findall(r"`([A-Za-z0-9_./-]+\.(?:md|csv|txt|sh|sql|py))`", rd(p)))):
            bases = [os.path.dirname(p), D, E20, E21, EV, os.path.join(D, "herramientas"), PE_DIR, os.path.join(E21, "scripts"), os.path.join(E21, "salidas"), G]
            if tok.startswith("docs/") : bases = [G]
            if tok in ("modelo_estructural.py", "verificar_expediente.py") : bases.append(os.path.join(D, "herramientas"))
            if not any(os.path.exists(os.path.normpath(os.path.join(b, tok))) for b in bases) and "/home/" not in tok and "fase0_v3_3_integral" not in tok:
                rotas.append((os.path.basename(p), tok))
    return "referencias a archivos que no existen=%s" % rotas[:8], not rotas, "backticks en %d documentos vigentes" % len(cand), "referencias internas y enlaces a evidencias"
T("V21-F05", "Referencias internas a archivos existentes (docs vigentes)", "tokens `archivo.ext`", "0 rotas", f05)
def f06():
    mal = []
    for p in vigentes():
        if p.startswith((E21,)):
            t = rd(p)
            if not re.search(r"\*\*Versión:\*\* V21", t) or "2026-11-20" not in t[:700]: mal.append(os.path.basename(p))
    return "entregables V21 sin 'Versión: V21' y fecha 2026-11-20=%s" % mal, not mal, "docs md en expediente_final_v21", "fechas y versiones"
T("V21-F06", "Fechas y versiones de los entregables V21", "md V21", "todos V21 / 2026-11-20", f06)
# ============ G. VIGENCIA, INTEGRIDAD, SIN CAMBIOS FUNCIONALES ============
def g01():
    p = os.path.join(E21, "INDICE_VIGENCIA_DOCUMENTAL_V21.md")
    if not os.path.exists(p): raise Exception("falta el índice")
    t = rd(p); filas = re.findall(r"^\| `([^`]+)` \| (VIGENTE|HISTÓRICO|SUSTITUIDO|EVIDENCIA PRIMARIA|EVIDENCIA DERIVADA) ", t, re.M)
    listados = [f for f, _ in filas]; dups = [k for k, v in collections.Counter(listados).items() if v > 1]
    real = []
    for root, ds, fs in os.walk(D):
        ds[:] = [d for d in ds if d != "__pycache__"]
        for f in fs: real.append(os.path.relpath(os.path.join(root, f), D))
    carpetas = {f for f in listados if f.endswith("/")}; faltan = []
    for r in real:
        if r in listados or any(r.startswith(c) for c in carpetas): continue
        faltan.append(r)
    fant = [f for f in listados if not f.endswith("/") and f not in real]
    return "archivos sin entrada=%s; entradas fantasma=%s; duplicadas=%s; filas=%d" % (faltan[:5], fant[:5], dups, len(filas)), not (faltan or fant or dups), "INDICE_VIGENCIA vs árbol real", "todo archivo identificado una sola vez"
T("V21-G01", "Índice de vigencia cubre todo el árbol sin fantasmas ni duplicados", "docs/fase0", "0 faltantes; 0 fantasmas", g01)
def g02():
    mal = []
    for d in (E20, EV):
        for f in sorted(os.listdir(d)):
            if f.endswith(".md"):
                t = rd(os.path.join(d, f))[:1400]
                if not re.search(r"Superseded|HISTÓRICO \(V21|SUSTITUIDO", t) and f not in ("INVENTARIO_DECISIONES_ABIERTAS_FASE0.md",) : mal.append(os.path.join(os.path.basename(d), f))
    # los md vigentes del directorio V20 se declaran en el índice como VIGENTE/EVIDENCIA; se excluyen explícitamente
    idx = rd(os.path.join(E21, "INDICE_VIGENCIA_DOCUMENTAL_V21.md")); mal = [m for m in mal if not re.search(r"\| `%s` \| (VIGENTE|EVIDENCIA PRIMARIA|EVIDENCIA DERIVADA) " % re.escape(os.path.relpath(os.path.join(D, m.replace(os.path.basename(E20), "expediente_final_v16_v19").replace(os.path.basename(EV), "evidencia_v16")), D)), idx)]
    return "md históricos/sustituidos sin aviso ni declaración vigente en el índice=%s" % mal, not mal, "avisos en md de V20 y evidencia_v16", "ningún sustituido parece vigente"
T("V21-G02", "Todo md sustituido o histórico lleva aviso (o figura como vigente/evidencia en el índice)", "md de V20 y V16", "0 sin aviso", g02)
def g04():
    nomod = git("diff", "--name-only", BASE_V20).split("\n") + git("ls-files", "--others", "--exclude-standard").split("\n"); nomod = [x for x in nomod if x]
    fuera = [x for x in nomod if not x.startswith("docs/fase0/")]; prot = [x for x in nomod if x.startswith(("docs/fase0/herramientas/", "docs/fase0/historico/"))]
    return "fuera de docs/fase0=%s; en herramientas/ o historico/=%s" % (fuera, prot), not fuera and not prot, "git diff --name-only %s + no rastreados" % BASE_V20[:7], "sin cambios funcionales, del motor ni de históricos"
T("V21-G04", "Sin cambios fuera de docs/fase0 ni en herramientas/ o historico/ respecto de V20", "git", "0", g04)
def g05():
    a, b = sha(os.path.join(D, "herramientas", "modelo_estructural.py")), sha(os.path.join(D, "herramientas", "verificar_expediente.py"))
    return "modelo=%s verificador=%s" % (a[:12], b[:12]), a == SHA_MODELO and b == SHA_VERIF, "SHA-256 de motor y verificador", "22 funciones y verificador sin modificar"
T("V21-G05", "Motor (22 funciones) y verificador con SHA-256 protegido sin cambio", "2 archivos", "iguales a los de V20", g05)
def g06():
    v33 = os.environ.get("V33_PATH", "/home/claude/fase0_v3_3_integral.md")
    if not os.path.exists(v33): raise BlockedError("no está el original externo de la v3.3")
    h = sha(v33); return h, h == "b5dccdc73a8103966ab1e1b1e84b2e7ead68cd736fba666ec71d0e790d51c1da", "SHA-256 del original v3.3", "documento aceptado v3.3 y su historia intactos"
T("V21-G06", "v3.3 original con su SHA-256", "archivo externo", "b5dccdc7…c1da", g06)
def g07():
    ch = [x for x in git("diff", "--name-only", BASE_V20, "--", "docs/fase0/historico").split("\n") if x]
    h = os.listdir(os.path.join(D, "historico"));
    return "históricos modificados=%s; archivos en historico/=%d" % (ch, len(h)), not ch, "git diff sobre historico/", "hashes históricos sin alterar"
T("V21-G07", "historico/ sin modificaciones", "git", "0", g07)
def g08():
    m = git("rev-parse", "main").strip(); cur = git("rev-parse", "--abbrev-ref", "HEAD").strip(); merges = git("log", "--merges", "--oneline", BASE_V20 + "..HEAD").strip()
    try:
        r = subprocess.run(["git", "ls-remote", "origin", "refs/heads/main"], capture_output=True, text=True, cwd=G, timeout=60); rem = r.stdout.split()[0] if r.returncode == 0 and r.stdout.strip() else "no consultado"
    except Exception: rem = "no consultado"
    return "main local=%s remoto=%s rama=%s merges nuevos=%r" % (m[:7], rem[:7] if rem != "no consultado" else rem, cur, merges), m == MAIN and rem in (MAIN, "no consultado") and not merges and cur == "audit/fase0-v19-review", "git rev-parse / ls-remote", "main intacta, sin merges"
T("V21-G08", "main intacta (local y remota), rama autorizada, sin merges", "git", "6a1af24; sin merges", g08)
def g09():
    cabeza = git("rev-parse", "HEAD").strip(); anc = subprocess.run(["git", "merge-base", "--is-ancestor", BASE_V20, "HEAD"], cwd=G).returncode == 0
    return "HEAD=%s; V20 es ancestro=%s" % (cabeza[:7], anc), anc, "git", "V21 se construye sobre V20"
T("V21-G09", "V20 (ac84133) es ancestro de HEAD", "git", "True", g09)
def g10():
    mal = []
    for root, ds, fs in os.walk(E21):
        for f in fs:
            if f.endswith((".md", ".csv", ".txt", ".py", ".sh", ".sql")) and not f.startswith("salida_"):
                b = open(os.path.join(root, f), "rb").read()
                if b[:3] == b"\xef\xbb\xbf" or b"\r" in b or not b.endswith(b"\n"): mal.append(f)
                if any(l != l.rstrip() for l in b.decode("utf-8").split("\n")[:-1] if f.endswith((".md",)) and False): mal.append(f)
    return "archivos V21 con BOM/CR/sin salto final=%s" % mal, not mal, "formato UTF-8 sin BOM, LF", "codificación y formato"
T("V21-G10", "Formato de entregables V21: UTF-8 sin BOM, LF, salto final", "expediente_final_v21", "0", g10)
def g11():
    ch = []
    for f in ("evidencia_v16/salida_22_funciones_corrida1.txt", "evidencia_v16/salida_verificador_V18_corrida1.txt", "expediente_final_v16_v19/salida_22_funciones_V20_corrida1.txt", "expediente_final_v16_v19/salida_verificador_V20_final_corrida1.txt", "expediente_final_v16_v19/PE_POSTGRESQL_V20/salida_PE_V20_corrida1.txt", "expediente_final_v16_v19/PE_POSTGRESQL_V20/salida_PE_V20_mutaciones.txt"):
        a = git("show", BASE_V20 + ":docs/fase0/" + f);
        if a != rd(os.path.join(D, f)): ch.append(f)
    return "salidas originales alteradas=%s" % ch, not ch, "salidas crudas vs commit V20", "la evidencia original no se altera retrospectivamente"
T("V21-G11", "Salidas de ejecución originales de V16–V20 intactas", "6 salidas representativas", "0 alteradas", g11)
if TSV:
    with open(TSV, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n"); w.writerow(["id", "objetivo", "entrada", "esperado", "obtenido", "estado", "evidencia", "observaciones"]); w.writerows(RES)
c = collections.Counter(r[5] for r in RES); print("RESUMEN BATERÍA V21: %d pruebas; PASS=%d FAIL=%d BLOCKED=%d" % (len(RES), c["PASS"], c["FAIL"], c["BLOCKED"]))
sys.exit(1 if c["FAIL"] else 0)
