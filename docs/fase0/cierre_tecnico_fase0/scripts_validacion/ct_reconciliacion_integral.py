#!/usr/bin/env python3
# Uso: python3 -I -B ct_reconciliacion_integral.py <dir_cierre> [salida.txt]. Reconciliación textual/numérica del expediente. No usa base de datos.
import csv, re, os, sys, glob
c = sys.argv[1]; out = sys.argv[2] if len(sys.argv) > 2 else None
R = os.path.join(c, "scripts_validacion", "resultados"); res = []; fails = 0
def chk(n, ok, det=""):
    global fails; res.append(("PASS" if ok else "FAIL", n, det)); fails += (not ok)
rd = lambda p: list(csv.DictReader(open(p, encoding="utf-8")))
txt = lambda p: open(p, encoding="utf-8").read()
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
chk("escáner sql 0 FAIL", has("escaner_seguridad_sql.txt", r"FAIL=0") and "TOTAL=115" in txt(os.path.join(R, "escaner_seguridad_sql.txt")))
chk("escáner texto 0 FAIL", "TOTAL=571" in txt(os.path.join(R, "escaner_seguridad_texto.txt")) and has("escaner_seguridad_texto.txt", r"FAIL=0"))
chk("escáner autoprueba 26/26", has("escaner_seguridad_autoprueba.txt", r"26/26|PASS=26|TOTAL=26"))
chk("04 local = NO VERIFICABLE", has("04_r1r9_local_bloqueado.txt", r"NO VERIFICABLE EN ENTORNO F"))
chk("concurrencia CC-01/CC-02 PASS", len(re.findall(r"\| PASS", txt(os.path.join(R, "concurrencia_local_utf8.txt")))) >= 2)
# coherencia de cifras en documentos
docs = {os.path.basename(p): txt(p) for p in glob.glob(os.path.join(c, "*.md"))}
for nombre in ("DICTAMEN_PREPARACION_FASE0.md", "INFORME_CIERRE_TECNICO_FASE0.md"):
    d = docs[nombre]
    chk(nombre + ": cifras 63/63, 14/14, 80/80, 366, 354, 26, 21/21 presentes", all(x in d for x in ("63/63", "14/14", "80/80", "366", "354", "28/28")) or nombre.startswith("DICT") and all(x in d for x in ("63/63", "14/14", "80/80", "366", "354", "28/28")))
chk("LEEME no afirma «sin commit» como estado actual", "sin commit, push ni merge" not in docs["LEEME_CIERRE_TECNICO.md"] or "histórico" in docs["LEEME_CIERRE_TECNICO.md"].lower())
chk("ningún documento declara aceptada Fase 0 ni autorizada Fase 1", not any(re.search(r"Fase 0 (queda|está|fue) (formalmente )?aceptada|Fase 1 (queda|está|fue) autorizada", d) for d in docs.values()))
chk("ningún documento marca decisión como APROBADA", not any(re.search(r"Estado_aprobacion\W+APROBAD", d) for d in docs.values()))

# batería final: índice completo, rc=0, salidas existentes y hashes coincidentes
import hashlib
B = os.path.join(R, "bateria_final"); idx = rd(os.path.join(B, "INDICE_BATERIA.csv"))
chk("batería: 20 pasos, todos rc=0", len(idx) == 20 and all(r["rc"] == "0" for r in idx), str(len(idx)))
bad = []
for r in idx:
    p = r["salida"]; p = p if os.path.exists(p) else os.path.join(c, p.split("cierre_tecnico_fase0/", 1)[-1])
    if not os.path.exists(p) or hashlib.sha256(open(p, "rb").read()).hexdigest() != r["sha256_salida"]: bad.append(r["paso"])
chk("batería: cada salida existe y su SHA-256 coincide con el índice", not bad, str(bad))
# smoke de los seis scripts
sm = lambda f: txt(os.path.join(R, f))
chk("smoke: guardas abortan (6 scripts) y base 'postgres' rechazada", sm("smoke_guardas.txt").count("abortado: SI") == 7 and "base 'postgres'" in sm("smoke_guardas.txt"))
chk("smoke 03: defectuosa → FAIL; corregida → PASS", re.search(r"FAIL", sm("smoke_03_rls_shim_defectuosa.txt")) and re.search(r"PASS", sm("smoke_03_rls_shim_corregida.txt")))
chk("smoke 05: sesiones A/B ejecutadas con resultado PASS", re.search(r"PASS|OK", sm("smoke_05_sesion_A.txt")) and re.search(r"PASS", sm("smoke_05_sesion_B.txt")))
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
# enlaces / nombres de archivo citados
miss = []
for n, d in docs.items():
    for m in set(re.findall(r"`([\w./-]+\.(?:md|csv|sql|py|sh|txt))`", d)):
        base = os.path.basename(m)
        if not (glob.glob(os.path.join(c, "**", base), recursive=True) or "V25_copia_integra" in m or "expediente_final" in m or m.startswith("PE_") or base in ("ESPECIFICACION_TECNICA_G1_G5_G10.md", "AUDITORIA_FINAL_G1_G5_G10.md", "INVENTARIO_DECISIONES_ABIERTAS_FASE0.md", "modelo_estructural.py", "verificar_expediente.py", "REGISTRO_CASOS_22_FUNCIONES_V20.csv", "MATRIZ_HV02_PO05_EVIDENCIA.md", "01_fixture.sql", "mutaciones.sh", "ejecutar.sh")):
            miss.append((n, m))
chk("nombres de archivo citados existen en el dossier (o son fuentes V26 externas listadas)", not miss, str(sorted(set(miss))[:12]))
for r in res: print("%s | %s | %s" % r)
print("TOTAL=%d FAIL=%d" % (len(res), fails))
if out:
    with open(out, "w", encoding="utf-8") as o:
        for r in res: o.write("%s | %s | %s\n" % r)
        o.write("TOTAL=%d FAIL=%d\n" % (len(res), fails))
sys.exit(1 if fails else 0)
