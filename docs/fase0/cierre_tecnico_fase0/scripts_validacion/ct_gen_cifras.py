#!/usr/bin/env python3
# Uso: python3 -I -B ct_gen_cifras.py <dir_cierre>. Fuente única de cifras: calcula cada cifra DESDE los resultados/matrices (nunca a mano) y escribe
# resultados/cifras_definitivas.json e INFORME_CIFRAS_DEFINITIVAS.md (cifra, valor, fuente, SHA-256 de la fuente). Los documentos narrativos no deben contradecirlas (lo comprueba la reconciliación).
import csv, json, os, re, sys, hashlib, collections
c = os.path.abspath(sys.argv[1]); R = os.path.join(c, "scripts_validacion", "resultados"); B = os.path.join(R, "bateria_final"); F = []
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def add(k, v, fuente, nota=""): F.append({"cifra": k, "valor": v, "fuente": os.path.relpath(fuente, c) if os.path.isabs(fuente) else fuente, "sha256_fuente": sha(fuente if os.path.isabs(fuente) else os.path.join(c, fuente)), "nota": nota})
rd = lambda p: list(csv.DictReader(open(p, encoding="utf-8"))); tx = lambda p: open(p, encoding="utf-8").read()
P = lambda *a: os.path.join(c, *a)
idx = {r["paso"]: r for r in rd(os.path.join(B, "INDICE_BATERIA.csv"))}; I = os.path.join(B, "INDICE_BATERIA.csv")
ft = tx(os.path.join(R, "escaner_seguridad_texto_final.txt")); mt = re.search(r"^TOTAL=(\d+) FAIL=(\d+)", ft, re.M); add("escaner_texto_final_total", int(mt.group(1)), os.path.join(R, "escaner_seguridad_texto_final.txt"), "repetición sobre el árbol final (tras generar informes)"); add("escaner_texto_final_FAIL", int(mt.group(2)), os.path.join(R, "escaner_seguridad_texto_final.txt"))
add("pasos_bateria", len(idx), I); add("pasos_bateria_OK", sum(r["estado"] == "OK" for r in idx.values()), I)
m = lambda paso, rx: re.search(rx, idx[paso]["resumen"])
for k, paso, rx in (("V20_pruebas_PASS", "v20_pe", r"PASS=(\d+)"), ("V20_mutaciones_detectadas", "v20_mutaciones", r"DETECTADAS=(\d+)"), ("extension_PASS", "extension_local", r"PASS=(\d+)"), ("DG19_PASS", "dg19", r"PASS=(\d+)"), ("hash_PASS", "hash_encadenado", r"PASS=(\d+)"),
                    ("K47_mapeadas_detectadas", "k47_por_escenario", r"DETECTADAS=(\d+)"), ("T409_variantes_detectadas", "t409_individual", r"DETECTADAS=(\d+)"), ("arnes_R1R9_PASS", "arnes_r1r9", r"PASS=(\d+)"),
                    ("escaner_sql_total", "escaner_sql", r"TOTAL=(\d+)"), ("escaner_texto_total", "escaner_texto", r"TOTAL=(\d+)"), ("escaner_autoprueba_total", "escaner_autoprueba", r"TOTAL=(\d+)"), ("evaluaciones_22_funciones", "funciones_22", r"casos_reportados=(\d+)")):
    add(k, int(m(paso, rx).group(1)), I, "paso %s de la batería" % paso)
for k, paso, rx in (("aserciones_smoke_total", "aserciones_smoke", r"TOTAL=(\d+)"), ("aserciones_smoke_PASS", "aserciones_smoke", r"PASS=(\d+)"), ("guarda_destino_total", "guarda_destino", r"TOTAL=(\d+)"), ("guarda_destino_PASS", "guarda_destino", r"PASS=(\d+)"), ("guarda_destino_FAIL", "guarda_destino", r"FAIL=(\d+)")):
    add(k, int(m(paso, rx).group(1)), I, "paso %s de la batería" % paso)
for k, paso in (("escaner_sql_FAIL", "escaner_sql"), ("escaner_texto_FAIL", "escaner_texto"), ("escaner_autoprueba_FAIL", "escaner_autoprueba"), ("arnes_FAIL", "arnes_r1r9")): add(k, int(m(paso, r"FAIL=(\d+)").group(1)), I)
f22 = tx(os.path.join(B, "22_stdout.txt")); cas = dict(re.findall(r"(\w+)=(\d+)", re.search(r"CASOS_POR_FUNCION (.*)", f22).group(1))); llama = "pruebas_atomicidad llama a correr_mutaciones_rechazo: True" in f22.replace("La función ", "")
add("fixtures_distintos_22_funciones", int(m("funciones_22", r"casos_reportados=(\d+)").group(1)) - (int(cas["correr_mutaciones_rechazo"]) if llama else 0), os.path.join(B, "22_stdout.txt"), "evaluaciones − casos de correr_mutaciones_rechazo, que pruebas_atomicidad invoca (doble conteo); la derivación solo vale si la llamada está comprobada (True)")
ex = rd(os.path.join(R, "catalogo_except_exception.csv")); k = collections.Counter(x["Clasificacion"].split(":")[0] for x in ex)
add("bloques_except_Exception", len(ex), os.path.join(R, "catalogo_except_exception.csv")); add("except_SEGURO", k["SEGURO"], os.path.join(R, "catalogo_except_exception.csv")); add("except_RIESGO_TECNICO", k["RIESGO_TECNICO"], os.path.join(R, "catalogo_except_exception.csv"))
lim = rd(P("MATRIZ_LIMITACIONES_RESIDUALES.csv")); v = collections.Counter(x["Vigencia"] for x in lim)
add("limitaciones_total", len(lim), "MATRIZ_LIMITACIONES_RESIDUALES.csv"); [add("limitaciones_" + q, v[q], "MATRIZ_LIMITACIONES_RESIDUALES.csv") for q in ("VIGENTE", "PARCIALMENTE_RESUELTA", "RESUELTA")]
dec = rd(P("REGISTRO_DECISIONES_RECOMENDADAS.csv")); add("decisiones_total", len(dec), "REGISTRO_DECISIONES_RECOMENDADAS.csv"); add("decisiones_aprobadas", sum(d["Estado_aprobacion"] != "REQUIERE_APROBACION_DEL_PROPIETARIO" for d in dec), "REGISTRO_DECISIONES_RECOMENDADAS.csv", "0 = ninguna aprobada")
e = rd(P("MATRIZ_12_ESCENARIOS_PARCIALES.csv")); ke = collections.Counter(x["Resultado"] for x in e); add("escenarios_parciales_total", len(e), "MATRIZ_12_ESCENARIOS_PARCIALES.csv"); [add("escenarios_" + q, ke[q], "MATRIZ_12_ESCENARIOS_PARCIALES.csv") for q in ("PASS_PROTOTYPE", "PASS_STATIC", "PARTIAL")]; add("escenarios_PASS_PHYSICAL", ke["PASS_PHYSICAL"], "MATRIZ_12_ESCENARIOS_PARCIALES.csv")
add("trazabilidad_filas", len(rd(P("MATRIZ_TRAZABILIDAD_MAESTRA.csv"))), "MATRIZ_TRAZABILIDAD_MAESTRA.csv")
mf = tx(P("MANIFIESTO_SHA256_CIERRE.txt")).splitlines(); add("manifiesto_entradas", len(mf), "MANIFIESTO_SHA256_CIERRE.txt", "el manifiesto se regenera después de este archivo; la reconciliación final y la verificación A/B comprueban la coincidencia")
open(os.path.join(R, "cifras_definitivas.json"), "w", encoding="utf-8").write(json.dumps({"cifras": F}, ensure_ascii=False, indent=1, sort_keys=True) + "\n")
L = ["# INFORME DE CIFRAS DEFINITIVAS", "", "Generado por `scripts_validacion/ct_gen_cifras.py` desde los resultados y matrices (no se copian números de mensajes anteriores). Fuente estructurada: `scripts_validacion/resultados/cifras_definitivas.json`. Si una cifra de un documento narrativo difiere de esta tabla, la tabla prevalece y la reconciliación lo marca como FAIL.", "",
     "Las cifras de verificación remota (HEAD, archivos y hashes verificados por las vías A/B) no pueden constar aquí (dependen del commit que contiene este archivo): están en `evidencia_verificacion/` (fixed point; ver `INFORME_HASHES_MANIFIESTO.md`).", "", "| Cifra | Valor | Fuente | SHA-256 de la fuente (12) | Nota |", "|---|---|---|---|---|"]
for x in F: L.append("| %s | %s | `%s` | %s | %s |" % (x["cifra"], x["valor"], x["fuente"], x["sha256_fuente"][:12], x["nota"]))
open(P("INFORME_CIFRAS_DEFINITIVAS.md"), "w", encoding="utf-8").write("\n".join(L) + "\n"); print("cifras:", len(F))

# bloque generado en LEEME (entre marcadores): cifras reales, no copiadas a mano
V = {x["cifra"]: x["valor"] for x in F}; lp = os.path.join(c, "LEEME_CIERRE_TECNICO.md"); t = open(lp, encoding="utf-8").read()
blk = ("<!-- CIFRAS:INICIO -->\n_Generado por `ct_gen_cifras.py` desde `resultados/cifras_definitivas.json`; todo resultado es LOCAL/PROTOTIPO/ESTÁTICO: PASS_PHYSICAL = %d._\n\n"
 "- PostgreSQL 16 temporal: V20 %d pruebas PASS y %d mutaciones detectadas; extensión %d PASS; DG-19 %d PASS; hash encadenado %d PASS; concurrencia local CC-01/CC-02 (ver batería); arnés R1–R9 %d PASS (prueba el arnés, no R1–R9).\n"
 "- Modelo en memoria: K47 %d mapeadas detectadas; T-409..T-422 %d variantes detectadas; 22 funciones: %d evaluaciones, %d fixtures distintos; %d bloques `except Exception` (%d SEGURO, %d RIESGO_TECNICO).\n"
 "- Escáneres estáticos: SQL %d comprobaciones (%d FAIL), texto %d en la batería y %d en el árbol final (%d FAIL), autoprueba %d (%d FAIL).\n"
 "- Smoke de los 6 scripts: %d aserciones de contenido (%d PASS). Guarda DEV/PROD (H-03): %d pruebas (%d PASS, %d FAIL) sobre los 6 scripts.\n"
 "- Batería: %d pasos, %d con estado OK (rc=0 **y** contenido esperado). Manifiesto: %d entradas.\n"
 "- Limitaciones: %d (vigentes %d, parcialmente resueltas %d, resueltas %d). Decisiones: %d (aprobadas: %d). Escenarios parciales: %d (PASS_PROTOTYPE %d, PASS_STATIC %d, PARTIAL %d). Trazabilidad: %d filas.\n"
 "- Reconciliación integral y verificación A/B: `INFORME_RECONCILIACION_INTEGRAL.md`, `evidencia_verificacion/`.\n<!-- CIFRAS:FIN -->") % (
 V["escenarios_PASS_PHYSICAL"], V["V20_pruebas_PASS"], V["V20_mutaciones_detectadas"], V["extension_PASS"], V["DG19_PASS"], V["hash_PASS"], V["arnes_R1R9_PASS"], V["K47_mapeadas_detectadas"], V["T409_variantes_detectadas"], V["evaluaciones_22_funciones"], V["fixtures_distintos_22_funciones"],
 V["bloques_except_Exception"], V["except_SEGURO"], V["except_RIESGO_TECNICO"], V["escaner_sql_total"], V["escaner_sql_FAIL"], V["escaner_texto_total"], V["escaner_texto_final_total"], V["escaner_texto_final_FAIL"], V["escaner_autoprueba_total"], V["escaner_autoprueba_FAIL"], V["aserciones_smoke_total"], V["aserciones_smoke_PASS"], V["guarda_destino_total"], V["guarda_destino_PASS"], V["guarda_destino_FAIL"], V["pasos_bateria"], V["pasos_bateria_OK"], V["manifiesto_entradas"],
 V["limitaciones_total"], V["limitaciones_VIGENTE"], V["limitaciones_PARCIALMENTE_RESUELTA"], V["limitaciones_RESUELTA"], V["decisiones_total"], V["decisiones_aprobadas"], V["escenarios_parciales_total"], V["escenarios_PASS_PROTOTYPE"], V["escenarios_PASS_STATIC"], V["escenarios_PARTIAL"], V["trazabilidad_filas"])
t = re.sub(r"<!-- CIFRAS:INICIO -->.*?<!-- CIFRAS:FIN -->", lambda _: blk, t, flags=re.S); open(lp, "w", encoding="utf-8").write(t)
