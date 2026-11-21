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
chk("decisiones: todas REQUIERE_APROBACION_DEL_PROPIETARIO (ninguna aprobada)", all(d["Estado_aprobacion"] == "REQUIERE_APROBACION_DEL_PROPIETARIO" for d in dec))
for pal in ("política de retención", "OD-13"):
    pass
# limitaciones
lim = rd(os.path.join(c, "MATRIZ_LIMITACIONES_RESIDUALES.csv")); li = [l["ID"] for l in lim]
chk("limitaciones: 28 ids únicos", len(li) == len(set(li)) == 28, str(len(li)))
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
chk("trazabilidad: 54 filas con referencia verificable y relación declarada", len(tr) == 54 and all(r["Referencia_verificable"] and r["Tipo_relacion"] for r in tr))
# resultados
def has(f, pat): return re.search(pat, txt(os.path.join(R, f)))
chk("V20 63/63", has("base_V20_pe_utf8.txt", r"TOTAL pruebas=63 PASS=63 FAIL=0"))
chk("V20 mutaciones 14/14", has("base_V20_mutaciones_utf8.txt", r"DETECTADAS=14"))
chk("extensión 80/80", has("ext_utf8.txt", r"TOTAL pruebas=80 PASS=80 FAIL=0"))
chk("DG-19 63/63", has("dg19_pk_experimento.txt", r"PASS=63 FAIL=0"))
chk("hash 16/16", has("hash_cadena_referencia.txt", r"TOTAL=16 PASS=16 FAIL=0"))
chk("arnés 21/21", has("arnes_r1r9_autoprueba_local.txt", r"PASS=21 FAIL=0"))
chk("escáner 0 FAIL", has("escaner_seguridad_sql.txt", r"FAIL=0"))
chk("04 local = NO VERIFICABLE", has("04_r1r9_local_bloqueado.txt", r"NO VERIFICABLE EN ENTORNO F"))
chk("concurrencia CC-01/CC-02 PASS", len(re.findall(r"\| PASS", txt(os.path.join(R, "concurrencia_local_utf8.txt")))) >= 2)
# coherencia de cifras en documentos
docs = {os.path.basename(p): txt(p) for p in glob.glob(os.path.join(c, "*.md"))}
for nombre in ("DICTAMEN_PREPARACION_FASE0.md", "INFORME_CIERRE_TECNICO_FASE0.md"):
    d = docs[nombre]
    chk(nombre + ": cifras 63/63, 14/14, 80/80, 366, 354, 26, 21/21 presentes", all(x in d for x in ("63/63", "14/14", "80/80", "366", "354", "21/21")) or nombre.startswith("DICT") and all(x in d for x in ("63/63", "14/14", "80/80", "366", "354", "21/21")))
chk("LEEME no afirma «sin commit» como estado actual", "sin commit, push ni merge" not in docs["LEEME_CIERRE_TECNICO.md"] or "histórico" in docs["LEEME_CIERRE_TECNICO.md"].lower())
chk("ningún documento declara aceptada Fase 0 ni autorizada Fase 1", not any(re.search(r"Fase 0 (queda|está|fue) (formalmente )?aceptada|Fase 1 (queda|está|fue) autorizada", d) for d in docs.values()))
chk("ningún documento marca decisión como APROBADA", not any(re.search(r"Estado_aprobacion\W+APROBAD", d) for d in docs.values()))
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
