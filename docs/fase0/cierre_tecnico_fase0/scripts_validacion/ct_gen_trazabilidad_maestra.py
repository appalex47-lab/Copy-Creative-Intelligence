#!/usr/bin/env python3
# Uso: python3 -I -B ct_gen_trazabilidad_maestra.py <dir_cierre> <ESPECIFICACION_TECNICA_G1_G5_G10.md>
# Genera MATRIZ_TRAZABILIDAD_MAESTRA.csv. Cada relación lleva un nivel explícito: DEMOSTRADA / INFERIDA / NO ESTABLECIDA / PENDIENTE DE VALIDACIÓN FÍSICA / PENDIENTE DE APROBACIÓN.
# Una relación es DEMOSTRADA solo si el identificador/nombre aparece literalmente en la fuente citada o si fue ejecutada. No se rellenan huecos con supuestos.
import csv, re, sys, os, collections
c, spec = sys.argv[1], sys.argv[2]
rd = lambda n: list(csv.DictReader(open(os.path.join(c, n), encoding="utf-8")))
fun = rd("MATRIZ_FUNCION_REGLA_ESCENARIO_PRUEBA.csv"); dec = rd("REGISTRO_DECISIONES_RECOMENDADAS.csv"); lim = rd("MATRIZ_LIMITACIONES_RESIDUALES.csv")
mod = open(os.path.join(c, "MATRIZ_MODELO_LOGICO_FISICO.md"), encoding="utf-8").read().splitlines()
TAB = {}
for l in mod:
    m = re.match(r"\| (\d+) \| (\w+) \| (.*?) \| (.*?) \| (.*?) \| (.*?) \| (.*?) \|$", l)
    if m: TAB[m.group(2)] = {"fisico": m.group(4), "estado": m.group(7)}
REGLA = {}
for l in open(spec, encoding="utf-8"):
    m = re.match(r"^\| ((?:IG|IS|IM|IE)\d*-\d+) \| (.*?) \|", l)
    if m and m.group(1) not in REGLA: REGLA[m.group(1)] = m.group(2)
tablas_en = lambda t: sorted(n for n in TAB if re.search(r"(?<![\w])" + re.escape(n) + r"(?![\w])", t))
def dec_txt(d): return " ".join(d.values())
wb = lambda idr: re.compile(r"(?<![\w-])" + re.escape(idr) + r"(?![\w-])")
EJEC = "ct_reejecucion_22_funciones.py → scripts_validacion/resultados/22_funciones_reejecucion_local.txt y bateria_final/ (PostgreSQL no usado: modelo en memoria)"
rows = []
for f in fun:
    r = f["Regla"]; idr = r if r in REGLA else ""
    txt = REGLA.get(r, "")
    ts = tablas_en(txt) if txt else []
    ds_exp = [d["ID"] for d in dec if idr and wb(idr).search(dec_txt(d))]
    ds_inf = [d["ID"] for d in dec if ts and d["ID"] not in ds_exp and any(wb(t).search(dec_txt(d)) for t in ts)]
    ls = [l["ID"] for l in lim if (idr and wb(idr).search(" ".join(l.values()))) or any(wb(d).search(" ".join(l.values())) for d in ds_exp)]
    nreg = "DEMOSTRADA (texto literal en la especificación)" if idr else "NO ESTABLECIDA (la función no cita regla por id: invariante K56-M)"
    ndec = ("DEMOSTRADA (id de la regla citado en la decisión): " + ";".join(ds_exp)) if ds_exp else (("INFERIDA (la decisión y la regla nombran el mismo objeto): " + ";".join(ds_inf)) if ds_inf else "NO ESTABLECIDA")
    nobj = ("DEMOSTRADA (nombre de tabla literal en el texto de la regla): " + ";".join(ts)) if ts else "NO ESTABLECIDA"
    fis = "; ".join("%s: %s" % (t, TAB[t]["fisico"]) for t in ts) if ts else "NO DEFINIDO"
    rows.append({
        "Tipo_fila": "REGLA_FUNCION", "Requisito": r if idr else "(sin id de regla)", "Decision_asociada": ";".join(ds_exp + ds_inf) or "NO ESTABLECIDA", "Nivel_requisito_decision": ndec,
        "Regla_de_negocio": (txt[:220] + ("…" if len(txt) > 220 else "")) or "NO ESTABLECIDA", "Nivel_requisito_regla": nreg,
        "Funcion": "%s (modelo_estructural.py l.%s-%s)" % (f["Funcion"], f["Linea_ini"], f["Linea_fin"]), "Nivel_regla_funcion": "DEMOSTRADA (tabla de V26: MATRIZ_FUNCION_REGLA_ESCENARIO_PRUEBA.csv)" if idr else "NO ESTABLECIDA",
        "Objeto_logico": ";".join(ts) or "NO ESTABLECIDO", "Nivel_objeto_logico": nobj,
        "Objeto_fisico_esperado": fis, "Nivel_objeto_fisico": "PENDIENTE DE VALIDACIÓN FÍSICA" if ts else "NO ESTABLECIDA",
        "Prueba": "%s evaluaciones de la función; escenarios (muestra): %s" % (f["Casos"], f["Escenarios_muestra"] or "n/a"), "Nivel_prueba": "DEMOSTRADA (la función y sus casos existen y fueron ejecutados)",
        "Ejecucion": EJEC, "Evidencia": f["Prueba_evidencia"] + "; resultados/22_funciones_conciliacion.csv",
        "Estado": "PASS_MODEL (modelo en memoria, local); V26: %s; aceptación física PENDIENTE" % f["Resultado_V26"],
        "Limitacion": ";".join(ls) or "LR-07;LR-09 (validación física pendiente)", "Nivel_limitacion": "DEMOSTRADA (id citado en la limitación)" if ls else "INFERIDA (limitación general de validación física)",
        "Responsable_siguiente_accion": ("Propietario (decisión " + ";".join(ds_exp) + ") y CCI-DEV") if ds_exp else "CCI-DEV (validación física, plan E2–E8); propietario para aprobar decisiones",
        "Referencia_verificable": "MATRIZ_FUNCION_REGLA_ESCENARIO_PRUEBA.csv fila %s/%s" % (f["Funcion"], r)})
for d in dec:
    ids = sorted(set(re.findall(r"\b(?:IG\d+|IS|IM|IE)-\d+\b", dec_txt(d))) & set(REGLA)); ts = tablas_en(dec_txt(d))
    fs = sorted({x["Funcion"] for x in fun if x["Regla"] in ids})
    ls = [l["ID"] for l in lim if wb(d["ID"]).search(" ".join(l.values()))]
    rows.append({
        "Tipo_fila": "DECISION", "Requisito": ";".join(ids) or "NO CITA REGLAS POR ID", "Decision_asociada": d["ID"] + " – " + d["Nombre"], "Nivel_requisito_decision": "PENDIENTE DE APROBACIÓN (" + d["Estado_aprobacion"] + ")",
        "Regla_de_negocio": "; ".join("%s: %s" % (i, REGLA[i][:90]) for i in ids[:3]) or "NO ESTABLECIDA", "Nivel_requisito_regla": "DEMOSTRADA (id literal en el registro)" if ids else "NO ESTABLECIDA",
        "Funcion": ";".join(fs) or "NO ESTABLECIDA", "Nivel_regla_funcion": "DEMOSTRADA (regla→función por tabla de V26)" if fs else "NO ESTABLECIDA",
        "Objeto_logico": ";".join(ts) or "NO ESTABLECIDO", "Nivel_objeto_logico": "DEMOSTRADA (nombre de tabla literal en el registro)" if ts else "NO ESTABLECIDA",
        "Objeto_fisico_esperado": "; ".join("%s: %s" % (t, TAB[t]["fisico"]) for t in ts) or "NO DEFINIDO", "Nivel_objeto_fisico": "PENDIENTE DE VALIDACIÓN FÍSICA" if ts else "NO ESTABLECIDA",
        "Prueba": d["Pruebas_necesarias"][:220], "Nivel_prueba": "DEMOSTRADA (texto del registro)", "Ejecucion": "Evidencia local: " + (d["Evidencia_local_de_este_cierre"] or "ninguna")[:160], "Evidencia": "REGISTRO_DECISIONES_RECOMENDADAS.csv fila " + d["ID"],
        "Estado": d["Estado_tecnico"] + " / " + d["Estado_aprobacion"], "Limitacion": ";".join(ls) or "ver MATRIZ_LIMITACIONES_RESIDUALES.csv", "Nivel_limitacion": "DEMOSTRADA (id citado)" if ls else "INFERIDA",
        "Responsable_siguiente_accion": "Propietario (aprobar/decidir)" + ("; CCI-DEV (validar)" if re.search(r"CCI-DEV|físic", d["Pruebas_necesarias"], re.I) else ""), "Referencia_verificable": "REGISTRO_DECISIONES_RECOMENDADAS.csv fila " + d["ID"]})
cols = list(rows[0]); 
with open(os.path.join(c, "MATRIZ_TRAZABILIDAD_MAESTRA.csv"), "w", newline="", encoding="utf-8") as o:
    w = csv.DictWriter(o, cols); w.writeheader(); w.writerows(rows)
k = collections.Counter((r["Tipo_fila"], r["Requisito"], r["Funcion"]) for r in rows if r["Tipo_fila"] == "REGLA_FUNCION" or r["Funcion"] != "NO ESTABLECIDA")
dup = [x for x, n in k.items() if n > 1]
print("filas", len(rows), "regla-función", len(fun), "decisiones", len(dec), "duplicadas", len(dup), "reglas con texto", sum(1 for r in rows if r["Nivel_requisito_regla"].startswith("DEMOSTRADA")), "decisión DEMOSTRADA", sum(1 for r in rows if r["Nivel_requisito_decision"].startswith("DEMOSTRADA")), "INFERIDA", sum(1 for r in rows if r["Nivel_requisito_decision"].startswith("INFERIDA")))
