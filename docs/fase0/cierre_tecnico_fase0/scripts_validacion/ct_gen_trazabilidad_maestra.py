#!/usr/bin/env python3
# Uso: python3 -I -B ct_gen_trazabilidad_maestra.py <dir_cierre>. Genera MATRIZ_TRAZABILIDAD_MAESTRA.csv.
# Solo relaciones EXPLICITAS (el id aparece literalmente en el texto de la fuente citada) o marcadas INFERIDA/NO_ESTABLECIDA. No inventa relaciones.
import csv, re, sys, os
c = sys.argv[1]
rd = lambda n: list(csv.DictReader(open(os.path.join(c, n), encoding="utf-8")))
fun = rd("MATRIZ_FUNCION_REGLA_ESCENARIO_PRUEBA.csv"); dec = rd("REGISTRO_DECISIONES_RECOMENDADAS.csv"); lim = rd("MATRIZ_LIMITACIONES_RESIDUALES.csv")
mod = open(os.path.join(c, "MATRIZ_MODELO_LOGICO_FISICO.md"), encoding="utf-8").read().splitlines()
tablas = [l for l in mod if re.match(r"\| \d+ \| ", l)]
def dec_text(d): return " ".join(d.values())
def refs(idr):
    pat = re.compile(r"(?<![\w-])" + re.escape(idr) + r"(?![\w-])")
    ds = [d["ID"] for d in dec if pat.search(dec_text(d))]
    ls = [l["ID"] for l in lim if pat.search(" ".join(l.values()))]
    ts = [re.split(r"\|", t)[2].strip() for t in tablas if pat.search(t)]
    return ds, ls, ts
FIS = "NO_DEFINIDO: requiere esquema físico CCI-DEV (LR de validación física)"
rows = []
for f in fun:
    r = f["Regla"]; idr = r if re.match(r"^(IG|IS|IM|IE)\d*-?\d+$", r) else ""
    ds, ls, ts = refs(idr) if idr else ([], [], [])
    rows.append({
        "Tipo_fila": "REGLA_FUNCION",
        "Requisito": r,
        "Decision": ";".join(ds) if ds else "NO_ESTABLECIDA_EN_LAS_FUENTES_DEL_CIERRE",
        "Funcion": f["Funcion"] + " (modelo_estructural.py l.%s-%s)" % (f["Linea_ini"], f["Linea_fin"]),
        "Tabla_u_objeto_fisico": ";".join(ts) if ts else FIS,
        "Prueba": "%s casos; escenarios muestra: %s" % (f["Casos"], f["Escenarios_muestra"] or "n/a"),
        "Evidencia": f["Prueba_evidencia"] + "; scripts_validacion/resultados/22_funciones_conciliacion.csv",
        "Estado": "PASS_LOCAL_PROTOTIPO (V26 %s; re-ejecutado en este cierre)" % f["Resultado_V26"] if f["Resultado_V26"] else "PASS_LOCAL_PROTOTIPO",
        "Limitacion": ";".join(ls) if ls else "LR de validación física pendiente (ver MATRIZ_LIMITACIONES_RESIDUALES.csv)",
        "Tipo_relacion": ("EXPLICITA(regla→función por tabla de V26)" if idr else "SIN_ID_DE_REGLA") + ("; decisión/tabla: EXPLICITA por texto" if (ds or ts) else "; decisión/tabla: NO_ESTABLECIDA"),
        "Referencia_verificable": "MATRIZ_FUNCION_REGLA_ESCENARIO_PRUEBA.csv fila %s/%s" % (f["Funcion"], r),
    })
for d in dec:
    ids = sorted(set(re.findall(r"\b(?:IG\d+|IS|IM|IE)-\d+\b", dec_text(d))))
    ls = [l["ID"] for l in lim if re.search(r"(?<![\w-])" + re.escape(d["ID"]) + r"(?![\w-])", " ".join(l.values()))]
    rows.append({
        "Tipo_fila": "DECISION", "Requisito": ";".join(ids) if ids else "NO_CITA_REGLAS_POR_ID",
        "Decision": d["ID"] + " – " + d["Nombre"], "Funcion": "NO_APLICA (decisión; relación a funciones NO_ESTABLECIDA salvo coincidencia de regla)",
        "Tabla_u_objeto_fisico": FIS, "Prueba": d["Pruebas_necesarias"][:200],
        "Evidencia": "REGISTRO_DECISIONES_RECOMENDADAS.csv: " + (d["Evidencia_local_de_este_cierre"] or "")[:200],
        "Estado": d["Estado_tecnico"] + " / " + d["Estado_aprobacion"], "Limitacion": ";".join(ls) or "ver MATRIZ_LIMITACIONES_RESIDUALES.csv",
        "Tipo_relacion": "EXPLICITA por texto de la fuente (ids de regla citados); resto NO_ESTABLECIDA",
        "Referencia_verificable": "REGISTRO_DECISIONES_RECOMENDADAS.csv fila " + d["ID"]})
cols = list(rows[0].keys())
with open(os.path.join(c, "MATRIZ_TRAZABILIDAD_MAESTRA.csv"), "w", newline="", encoding="utf-8") as o:
    w = csv.DictWriter(o, cols); w.writeheader(); w.writerows(rows)
print("filas", len(rows), "regla-función", len(fun), "decisiones", len(dec))
