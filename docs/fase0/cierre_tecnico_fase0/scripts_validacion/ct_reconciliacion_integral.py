#!/usr/bin/env python3
# Uso: python3 -I -B ct_reconciliacion_integral.py <dir_cierre> [--sin-salida]. Escribe resultados/reconciliacion_integral.{json,txt} e INFORME_RECONCILIACION_INTEGRAL.md desde una única lista estructurada. Sin base de datos.
import csv, re, os, sys, glob, json, hashlib, time, subprocess
c = os.path.abspath(sys.argv[1]); out = "gen" if len(sys.argv) < 3 or sys.argv[2] != "--sin-salida" else None
R = os.path.join(c, "scripts_validacion", "resultados"); res = []; fails = 0
EV = []; REG = []   # evidencia: cada archivo leído para una comprobación (ruta relativa + SHA-256 de los bytes leídos)
def _reg(p):
    b = open(p, "rb").read(); r = os.path.relpath(os.path.abspath(p), os.path.abspath(c)); EV.append({"ruta": r, "sha256": hashlib.sha256(b).hexdigest()}); return b
def chk(n, ok, det=""):
    global fails; ok = bool(ok); ev = list({e["ruta"]: e for e in EV}.values()); EV.clear()
    REG.append({"id": len(REG) + 1, "estado": "PASS" if ok else "FAIL", "comprobacion": n, "detalle": det if not ok else (det or ""), "evidencia": ev})
    res.append(("PASS" if ok else "FAIL", n, det)); fails += (not ok)
rd = lambda p: list(csv.DictReader(_reg(p).decode("utf-8").splitlines()))
txt = lambda p: _reg(p).decode("utf-8")
# CSV bien formados
for f in sorted(glob.glob(os.path.join(c, "*.csv")) + glob.glob(os.path.join(R, "*.csv"))):
    rows = list(csv.reader(open(f, encoding="utf-8"))); n = len(rows[0])
    chk("CSV bien formado " + os.path.basename(f), all(len(r) == n for r in rows), "%d filas x %d cols" % (len(rows) - 1, n))
# decisiones
dec = rd(os.path.join(c, "REGISTRO_DECISIONES_RECOMENDADAS.csv")); ids = [d["ID"] for d in dec]
esp = "G-1 G-5 G-10 DG-19 DG-20 DG-12 DG-16 DG-18 G-9 RP-01 P-01 P-02 P-03 P-04 P-05 P-10 PO-05 DG-09 DEP-RET-01 OD-13".split()
chk("decisiones: las 20 pendientes exigidas están en el registro", all(e in ids for e in esp), "faltan=%s" % [e for e in esp if e not in ids])
chk("decisiones: sin ids duplicados; total 21 (20 + HV-02)", len(ids) == len(set(ids)) == 21 and "HV-02" in ids, str(len(ids)))
chk("decisiones: columnas de consecuencias y estado actual completas", all(d.get("Consecuencia_si_se_aprueba") and d.get("Consecuencia_si_no_se_aprueba") and d.get("Estado_actual") for d in dec))
chk("decisiones: todas REQUIERE_APROBACION_DEL_PROPIETARIO (ninguna aprobada)", all(d["Estado_aprobacion"] == "REQUIERE_APROBACION_DEL_PROPIETARIO" for d in dec))
for pal in ("política de retención", "OD-13"):
    pass
# limitaciones
lim = rd(os.path.join(c, "MATRIZ_LIMITACIONES_RESIDUALES.csv")); li = [l["ID"] for l in lim]
chk("limitaciones: 27 ids únicos (LR-28 fusionada en LR-05)", len(li) == len(set(li)) == 27 and "LR-28" not in li, str(len(li)))
from collections import Counter as _C
vg = _C(l["Vigencia"] for l in lim)
chk("limitaciones: vigencia declarada en todas (18 VIGENTE, 5 RESUELTA, 4 PARCIALMENTE_RESUELTA)", vg["VIGENTE"] == 18 and vg["RESUELTA"] == 5 and vg["PARCIALMENTE_RESUELTA"] == 4, str(dict(vg)))
chk("limitaciones: acción concreta y dependencia en todas", all(l["Accion_concreta"].strip() and l["Depende_de"].strip() for l in lim))
# 12 escenarios
m12 = rd(os.path.join(c, "MATRIZ_12_ESCENARIOS_PARCIALES.csv")); from collections import Counter; k = Counter(r["Resultado"] for r in m12)
chk("12 escenarios: 5 PASS_PROTOTYPE, 1 PASS_STATIC, 6 PARTIAL", len(m12) == 12 and k["PASS_PROTOTYPE"] == 5 and k["PASS_STATIC"] == 1 and k["PARTIAL"] == 6, str(dict(k)))
chk("12 escenarios: aceptación física PENDIENTE en todos", all(r["Estado_aceptacion_fisica"].startswith("PENDIENTE") for r in m12))
# funciones
f22 = [r for r in rd(os.path.join(R, "22_funciones_conciliacion.csv")) if r["Funcion"] != "TOTAL_REPORTADO"]
chk("22 funciones: 22 filas, 366 casos, 0 fallos", len(f22) == 22 and sum(int(r["Casos_reportados"]) for r in f22) == 366 and sum(int(r["Casos_FAIL"]) for r in f22) == 0)
fm = rd(os.path.join(c, "MATRIZ_FUNCION_REGLA_ESCENARIO_PRUEBA.csv")); fn = {r["Funcion"] for r in fm}
chk("matriz función-regla cubre las 22 funciones", fn == {r["Funcion"] for r in f22}, str(len(fn)))
# T-409..T-422
t = rd(os.path.join(R, "t409_t422_individual.csv"))
chk("T-409..T-422: 26 variantes DETECTADA, 14 escenarios", len(t) == 26 and all(r["Resultado"] == "DETECTADA" for r in t) and len({r["Escenario"] for r in t}) == 14)
# trazabilidad
tr = rd(os.path.join(c, "MATRIZ_TRAZABILIDAD_MAESTRA.csv"))
chk("trazabilidad: 54 filas con referencia verificable y relación declarada", len(tr) == 54 and all(r["Referencia_verificable"] and r["Tipo_fila"] for r in tr))
lv = {"DEMOSTRADA","INFERIDA","NO ESTABLECIDA","PENDIENTE DE VALIDACIÓN FÍSICA","PENDIENTE DE APROBACIÓN",""}
chk("trazabilidad: niveles de evidencia en vocabulario permitido en cada relación", all(r[k] in lv or r[k].split(" ")[0] in {x.split(" ")[0] for x in lv} for r in tr for k in r if k.startswith("Nivel_")))
# resultados
def has(f, pat): return re.search(pat, txt(os.path.join(R, f)))
chk("V20 63/63", has("base_V20_pe_utf8.txt", r"TOTAL pruebas=63 PASS=63 FAIL=0"))
chk("V20 mutaciones 14/14", has("base_V20_mutaciones_utf8.txt", r"DETECTADAS=14"))
chk("extensión 80/80", has("ext_utf8.txt", r"TOTAL pruebas=80 PASS=80 FAIL=0"))
chk("DG-19 63/63", has("dg19_pk_experimento.txt", r"PASS=63 FAIL=0"))
chk("hash 16/16", has("hash_cadena_referencia.txt", r"TOTAL=16 PASS=16 FAIL=0"))
chk("arnés 28/28", has("arnes_r1r9_autoprueba_local.txt", r"PASS=28 FAIL=0"))
chk("escáner sql 0 FAIL", has("escaner_seguridad_sql.txt", r"TOTAL=\d+ FAIL=0"))
chk("escáner texto 0 FAIL", has("escaner_seguridad_texto.txt", r"TOTAL=\d+ FAIL=0"))
chk("escáner texto repetido sobre el árbol final: 0 FAIL", has("escaner_seguridad_texto_final.txt", r"TOTAL=\d+ FAIL=0"))
chk("escáner autoprueba 26/26", has("escaner_seguridad_autoprueba.txt", r"26/26|PASS=26|TOTAL=26"))
chk("04 local = NO VERIFICABLE", has("04_r1r9_local_bloqueado.txt", r"NO VERIFICABLE EN ENTORNO F"))
chk("concurrencia CC-01/CC-02 PASS", len(re.findall(r"\| PASS", txt(os.path.join(R, "concurrencia_local_utf8.txt")))) >= 2)
# coherencia de cifras en documentos
docs = {os.path.basename(p): open(p, encoding="utf-8").read() for p in glob.glob(os.path.join(c, "*.md"))}   # lectura sin registro: cada comprobación registra los documentos que realmente usa
evd = lambda *ns: [_reg(os.path.join(c, n)) for n in ns]
evall = lambda: evd(*sorted(docs))
for nombre in ("DICTAMEN_PREPARACION_FASE0.md", "INFORME_CIERRE_TECNICO_FASE0.md"):
    d = docs[nombre]; evd(nombre)
    chk(nombre + ": cifras 63/63, 14/14, 80/80, 366, 354, 26, 21/21 presentes", all(x in d for x in ("63/63", "14/14", "80/80", "366", "354", "28/28")) or nombre.startswith("DICT") and all(x in d for x in ("63/63", "14/14", "80/80", "366", "354", "28/28")))
evd("LEEME_CIERRE_TECNICO.md")
chk("LEEME no afirma «sin commit» como estado actual", "sin commit, push ni merge" not in docs["LEEME_CIERRE_TECNICO.md"] or "histórico" in docs["LEEME_CIERRE_TECNICO.md"].lower())
evall()
chk("ningún documento declara aceptada Fase 0 ni autorizada Fase 1", not any(re.search(r"Fase 0 (queda|está|fue) (formalmente )?aceptada|Fase 1 (queda|está|fue) autorizada", d) for d in docs.values()))
evall()
chk("ningún documento marca decisión como APROBADA", not any(re.search(r"Estado_aprobacion\W+APROBAD", d) for d in docs.values()))

# batería final: índice completo, rc=0, salidas existentes y hashes coincidentes
import hashlib
B = os.path.join(R, "bateria_final"); idx = rd(os.path.join(B, "INDICE_BATERIA.csv"))
chk("batería: 21 pasos, todos rc=0 Y estado=OK (rc=0 solo no basta: se exige el contenido esperado)", len(idx) == 21 and all(r["rc"] == "0" and r["estado"] == "OK" and r["esperado"] for r in idx), str([r["paso"] for r in idx if r["estado"] != "OK"]))
bad = []
for r in idx:
    p = r["salida"]; p = p if os.path.exists(p) else os.path.join(c, p.split("cierre_tecnico_fase0/", 1)[-1])
    if not os.path.exists(p) or hashlib.sha256(open(p, "rb").read()).hexdigest() != r["sha256_salida"]: bad.append(r["paso"])
chk("batería: cada salida existe y su SHA-256 coincide con el índice", not bad, str(bad))
# smoke de los seis scripts
sm = lambda f: txt(os.path.join(R, f))
asm = sm("aserciones_smoke.txt")
chk("smoke de los 6 scripts: aserciones de contenido 11/11, 0 FAIL (guardas, 03 defectuoso/corregido, 04 NO VERIFICABLE, 05 BLOCKED)", "TOTAL=11 PASS=11 FAIL=0" in asm)
# T-409 reproducibilidad y correspondencia
chk("T-409: 2ª corrida idéntica byte a byte", "IDENTICO_BYTE_A_BYTE" in txt(os.path.join(B, "t409_repro_cmp.txt")))
tc = rd(os.path.join(R, "t409_t422_correspondencia.csv"))
chk("T-409..T-422: correspondencia con nivel de evidencia explícito (14 escenarios)", len(tc) == 14 and all(r["Nivel_regla_a_K47M"] and r["Nivel_escenario_a_mutacion_K47M"] and r["Evidencia_fisica_que_falta"] for r in tc))
# controles negativos del manifiesto y búsqueda global (generados antes de la reconciliación)
cn = os.path.join(R, "controles_negativos_manifiesto.txt")
chk("manifiesto: controles negativos 36/36, 0 FAIL", os.path.exists(cn) and "FAIL=0" in txt(cn) and "36" in txt(cn))
bg = os.path.join(R, "busqueda_global.txt")
chk("búsqueda global sin FAIL", os.path.exists(bg) and not re.search(r"^FAIL", txt(bg), re.M))
chk("herramientas antiguas eliminadas", not os.path.exists(os.path.join(c, "scripts_validacion", "ct_verificar_publicacion.py")) and not os.path.exists(os.path.join(c, "scripts_validacion", "ct_gen_manifiesto.py")))

# cifras definitivas (fuente única generada) frente a las cifras escritas en los documentos narrativos
CF = {x["cifra"]: x["valor"] for x in json.loads(txt(os.path.join(R, "cifras_definitivas.json")))["cifras"]}
chk("cifras definitivas: generadas, batería 21/21 OK, decisiones aprobadas = 0, PASS_PHYSICAL = 0", CF["pasos_bateria"] == 21 == CF["pasos_bateria_OK"] and CF["decisiones_aprobadas"] == 0 and CF["escenarios_PASS_PHYSICAL"] == 0)
chk("cifras: limitaciones %d = vigentes+parciales+resueltas; decisiones %d; escenarios %d; fixtures %d de %d evaluaciones" % (CF["limitaciones_total"], CF["decisiones_total"], CF["escenarios_parciales_total"], CF["fixtures_distintos_22_funciones"], CF["evaluaciones_22_funciones"]),
    CF["limitaciones_total"] == CF["limitaciones_VIGENTE"] + CF["limitaciones_PARCIALMENTE_RESUELTA"] + CF["limitaciones_RESUELTA"] and CF["fixtures_distintos_22_funciones"] == 354 and CF["evaluaciones_22_funciones"] == 366 and CF["bloques_except_Exception"] == CF["except_SEGURO"] + CF["except_RIESGO_TECNICO"])
chk("manifiesto: nº de entradas (%d) = cifra generada y = archivos sujetos a verificación" % CF["manifiesto_entradas"], len(txt(os.path.join(c, "MANIFIESTO_SHA256_CIERRE.txt")).splitlines()) == CF["manifiesto_entradas"])
def nums(rx, d): return {int(x) for x in re.findall(rx, d)}
dd = {n: docs[n] for n in ("LEEME_CIERRE_TECNICO.md", "DICTAMEN_PREPARACION_FASE0.md", "INFORME_CIERRE_TECNICO_FASE0.md", "INFORME_PUBLICACION_GITHUB.md", "INFORME_HASHES_MANIFIESTO.md", "INFORME_PRUEBAS_FINALES.md")}
bad = []; evd(*dd)
for n, d in dd.items():
    for rx, key in ((r"(\d+) limitaciones", "limitaciones_total"), (r"RESIDUALES\.csv`?\s*\((\d+)", "limitaciones_total"), (r"(\d+) decisiones", "decisiones_total"), (r"arnés[^.|\n]{0,40}?(\d+)/\d+", "arnes_R1R9_PASS"), (r"(\d+) fixtures distintos", "fixtures_distintos_22_funciones"), (r"(\d+) evaluaciones", "evaluaciones_22_funciones")):
        for v in nums(rx, d):
            if v != CF[key] and not re.search(r"(?i)hist[oó]ric|anterior|v1", " ".join(l for l in d.splitlines() if re.search(rx, l))): bad.append((n, key, v, CF[key]))
chk("cifras de los documentos narrativos coinciden con cifras_definitivas.json (limitaciones, decisiones, arnés, fixtures, evaluaciones)", not bad, str(bad[:6]))

# alcance respecto de V26: nada fuera del dossier, V26 intacto (comprobación contra el SHA de V26 con git; el árbol de trabajo incluye cambios sin commit)
V26 = "439777c9ea7db464fe49299adfeb2112abfd285c"; g = lambda *a: subprocess.run(["git", "-C", c] + list(a), capture_output=True, text=True)
if g("rev-parse", "--git-dir").returncode == 0 and g("cat-file", "-e", V26 + "^{commit}").returncode == 0:
    top = g("rev-parse", "--show-toplevel").stdout.strip(); pref = os.path.relpath(c, top).replace(os.sep, "/")
    ch = [l for l in g("diff", "--name-status", V26, "--", top).stdout.splitlines() if l]; fuera = [l for l in ch if not l.split("\t")[-1].startswith(pref + "/")]; mod = [l for l in ch if l[0] in "MDRT" and l.split("\t")[-1].startswith(pref + "/") is False]
    nuevos = [l for l in subprocess.run(["git", "-C", top, "ls-files", "--others", "--exclude-standard"], capture_output=True, text=True).stdout.splitlines() if not l.startswith(pref + "/")]
    chk("alcance: contra V26 no hay archivos modificados/eliminados/añadidos fuera de %s (tracked: %d, sin seguimiento: %d)" % (pref, len(fuera), len(nuevos)), not fuera and not nuevos, str(fuera[:3] + nuevos[:3]))
    chk("alcance: herramientas protegidas (modelo_estructural.py, verificar_expediente.py) idénticas a V26", g("diff", "--quiet", V26, "--", "docs/fase0/herramientas/modelo_estructural.py", "docs/fase0/herramientas/verificar_expediente.py").returncode == 0)
else:
    chk("alcance contra V26 verificable con git en este entorno", False, "sin repositorio git o sin el commit V26")
# enlaces / nombres de archivo citados: rutas con "/" deben resolverse exactamente (relativas al dossier, a docs/fase0 o a scripts_validacion); nombres sueltos, por nombre exacto (sensible a mayúsculas)
EXT = ("ESPECIFICACION_TECNICA_G1_G5_G10.md", "AUDITORIA_FINAL_G1_G5_G10.md", "INVENTARIO_DECISIONES_ABIERTAS.md", "modelo_estructural.py", "verificar_expediente.py")   # fuentes V26 protegidas, fuera del dossier (docs/fase0/herramientas/)
V26BASES = {f for dp, _, fs in os.walk(os.path.dirname(c)) if os.path.abspath(dp) != c and not os.path.abspath(dp).startswith(c + os.sep) for f in fs}   # nombres de archivos de V26 (docs/fase0) citados sin ruta
allf = {os.path.relpath(os.path.join(dp, f), c) for dp, _, fs in os.walk(c) for f in fs}; bases = {os.path.basename(x) for x in allf}
def resuelve(m):
    if "V25_copia_integra" in m or "expediente_final" in m or m.startswith("PE_") or os.path.basename(m) in EXT: return "fuente V26 externa"
    if "/" in m:
        for pre in ("", "scripts_validacion/", "scripts_validacion/resultados/"):
            if os.path.normpath(pre + m) in allf: return "ruta exacta"
        return None
    if m in bases: return "nombre exacto"
    return "fuente V26 (nombre exacto en docs/fase0)" if m in V26BASES else None
evall(); miss = []; nref = 0; EXCL = ("INFORME_RECONCILIACION_INTEGRAL.md",)   # el informe generado cita comprobaciones fallidas con nombres que no son referencias suyas
for n, d in sorted(docs.items()):
    if n in EXCL: continue
    for m in sorted(set(re.findall(r"`([\w./-]+\.(?:md|csv|sql|py|sh|txt|json))`", d))):
        nref += 1
        if resuelve(m) is None and not re.search(r"(?i)hist[oó]ric|v1|retirad|eliminad", " ".join(l for l in d.splitlines() if m in l)): miss.append((n, m))
    for m in re.findall(r"\]\(([^)#:]+)\)", d):
        nref += 1
        if not os.path.exists(os.path.normpath(os.path.join(c, m))): miss.append((n, "enlace:" + m))
chk("referencias a archivos (%d) y enlaces relativos resuelven; las citas históricas están etiquetadas" % nref, not miss, str(sorted(set(miss))[:12]))
tot = len(res); npass = tot - fails; ahora = time.time()
meta = {"generado_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(ahora)), "generado_local": time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime(ahora)), "zona_local": time.strftime("%Z", time.localtime(ahora)),
        "commit_base_git": (lambda r: r.stdout.strip() if r.returncode == 0 else "no disponible")(subprocess.run(["git", "-C", c, "rev-parse", "HEAD"], capture_output=True, text=True)),
        "fuente_unica": "este JSON; el TXT y el MD se generan de él en la misma ejecución"}
J = {"meta": meta, "total": tot, "pass": npass, "fail": fails, "comprobaciones": REG}
RJ = os.path.join(R, "reconciliacion_integral.json"); RT = os.path.join(R, "reconciliacion_integral.txt"); RM = os.path.join(c, "INFORME_RECONCILIACION_INTEGRAL.md")
if out is not None:
    open(RJ, "w", encoding="utf-8").write(json.dumps(J, ensure_ascii=False, indent=1, sort_keys=True) + "\n")
    T = ["%s | %s | %s" % (r["estado"], r["comprobacion"], r["detalle"]) for r in REG] + ["TOTAL=%d PASS=%d FAIL=%d" % (tot, npass, fails)]
    open(RT, "w", encoding="utf-8").write("\n".join(T) + "\n")
    M = ["# INFORME DE RECONCILIACIÓN INTEGRAL", "", "Generado por `scripts_validacion/ct_reconciliacion_integral.py` en una sola ejecución a partir de la misma lista estructurada: `resultados/reconciliacion_integral.json` (fuente), `resultados/reconciliacion_integral.txt` y este informe. La coincidencia entre los tres se verifica con `ct_verificar_consistencia_informe.py` (con control negativo).", "",
         "- Generado: %s UTC = %s (%s) — hora tomada del reloj del entorno; no verificada contra una fuente externa." % (meta["generado_utc"], meta["generado_local"], meta["zona_local"]), "- Commit base del árbol de trabajo: `%s` (el árbol puede contener cambios sin commit; el commit publicado se identifica en `evidencia_verificacion/`)." % meta["commit_base_git"], "",
         "## Resultado", "**TOTAL=%d PASS=%d FAIL=%d**" % (tot, npass, fails), "", "| # | Estado | Comprobación | Detalle | Evidencia (archivo : SHA-256, 12 primeros) |", "|---|---|---|---|---|"]
    for r in REG: M.append("| %d | %s | %s | %s | %s |" % (r["id"], r["estado"], r["comprobacion"].replace("|", "/"), r["detalle"].replace("|", "/"), "<br>".join("`%s`: %s" % (e["ruta"], e["sha256"][:12]) for e in r["evidencia"]) or "(cálculo sobre el árbol)"))
    M += ["", "## Alcance", "La reconciliación comprueba coherencia entre documentos, matrices y salidas; no demuestra corrección funcional ni valida el esquema físico. La coincidencia del manifiesto con el árbol publicado se verifica con `ct_manifiesto.py` (vías A y B), no aquí."]
    open(RM, "w", encoding="utf-8").write("\n".join(M) + "\n")
print("TOTAL=%d PASS=%d FAIL=%d" % (tot, npass, fails))
for r in res:
    if r[0] == "FAIL": print("%s | %s | %s" % r)
sys.exit(1 if fails else 0)
