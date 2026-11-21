#!/usr/bin/env python3
# Re-ejecuta las 22 funciones de modelo_estructural.py (sin modificarlo) y CONCILIA los 366 casos: por función, identificadores únicos, solapamientos entre funciones y fallos.
# Uso: python3 -I -B ct_reejecucion_22_funciones.py <docs/fase0> [salida_detalle.txt] [salida_conciliacion.csv]
import importlib.util, sys, csv, os, collections
sys.dont_write_bytecode = True
d = sys.argv[1]; out_txt = sys.argv[2] if len(sys.argv) > 2 else None; out_csv = sys.argv[3] if len(sys.argv) > 3 else None
def carga(n, ruta):
    sp = importlib.util.spec_from_file_location(n, ruta); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
MS = carga("modelo_estructural", os.path.join(d, "herramientas", "modelo_estructural.py")); VE = carga("verificar_expediente", os.path.join(d, "herramientas", "verificar_expediente.py"))
P = VE.parse_4410(open(os.path.join(d, "ESPECIFICACION_TECNICA_G1_G5_G10.md"), encoding="utf-8").read())
NOM = "pruebas_guarda pruebas_atomicidad correr_mutaciones_rechazo correr_adversariales correr_escenarios correr_mutaciones_k47 correr_mutaciones_resoluciones correr_mutaciones_assets correr_positivos_arte correr_mutaciones_k45 correr_mutaciones_cadena correr_adversariales_cadena correr_mutaciones_atribucion pruebas_atomicidad14 pruebas_E14 correr_mutaciones_av correr_mutaciones_cf correr_mutaciones_ac correr_positivos15 correr_adversariales15 pruebas_atomicidad15 correr_mutaciones_modelo14".split()
def normaliza(n, r, i):
    """Devuelve (id_caso, ok, descripción). Cada función tiene su propia convención de resultado; el 'ok' es el que el propio modelo declara."""
    if isinstance(r, tuple):   # (descripción, bool) o, en los positivos de K45, (nombre, lista_de_violaciones): OK = lista vacía
        ok = (not r[1]) if isinstance(r[1], list) else bool(r[1])
        return ("%s#%02d" % (n, i + 1), ok, str(r[0])[:90])
    ok = r.get("ok", r.get("det")); return (str(r.get("id", "%s#%02d" % (n, i + 1))), bool(ok), str(r.get("mut", r.get("nombre", "")))[:90])
filas = []; por_fn = collections.OrderedDict()
for n in NOM:
    f = getattr(MS, n); res = f(P["matriz"]) [0] if n == "correr_mutaciones_k45" else f()
    por_fn[n] = [normaliza(n, x, i) for i, x in enumerate(res)]
# k45 devuelve 30 = 27 mutaciones + 3 positivos: se añaden los positivos (segunda componente)
mk45, pos45 = MS.correr_mutaciones_k45(P["matriz"]); por_fn["correr_mutaciones_k45"] = [normaliza("correr_mutaciones_k45", x, i) for i, x in enumerate(list(mk45) + list(pos45))]
total = sum(len(v) for v in por_fn.values()); fallos = [(n, c) for n, v in por_fn.items() for c in v if not c[1]]
ids = collections.Counter(c[0] for v in por_fn.values() for c in v)
dup_ids = {k: v for k, v in ids.items() if v > 1}
lineas = []
for n, v in por_fn.items():
    for c in v: lineas.append("%s | %s | obtenido_ok=%s | %s | %s" % (n, c[0], c[1], "PASS" if c[1] else "FAIL", c[2]))
lineas.append("TOTAL funciones=%d casos_reportados=%d fallos=%d" % (len(por_fn), total, len(fallos)))
lineas.append("CASOS_POR_FUNCION " + " ".join("%s=%d" % (n, len(v)) for n, v in por_fn.items()))
print("\n".join(lineas[-2:]))
# Conciliación: unicidad de identificadores y solapamientos documentados
sol = []
at = {c[0]: c for c in por_fn["pruebas_atomicidad"]}; rech = por_fn["correr_mutaciones_rechazo"]
print("Identificadores repetidos entre funciones: %d" % len(dup_ids))
# pruebas_atomicidad (20) declara 8 propios + 12 de correr_mutaciones_rechazo: se comprueba por descripción (las mutaciones de rechazo A54..A65 aparecen en ambas)
desc_at = [c[2] for c in por_fn["pruebas_atomicidad"]]; desc_rech = [c[2] for c in rech]
print("pruebas_atomicidad: %d casos; correr_mutaciones_rechazo: %d casos; casos de pruebas_atomicidad cuyo texto coincide con una mutación de rechazo: %d" % (len(desc_at), len(desc_rech), sum(1 for a in desc_at if any(a[:40] == b[:40] for b in desc_rech))))
fuente_atom = open(os.path.join(d, "herramientas", "modelo_estructural.py"), encoding="utf-8").read()
i0 = fuente_atom.index("def pruebas_atomicidad():"); i1 = fuente_atom.index("\ndef ", i0 + 10); cuerpo = fuente_atom[i0:i1]
print("La función pruebas_atomicidad llama a correr_mutaciones_rechazo: %s" % ("correr_mutaciones_rechazo" in cuerpo))
if out_txt: open(out_txt, "w", encoding="utf-8").write("\n".join(lineas) + "\n")
if out_csv:
    with open(out_csv, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh); w.writerow(["Funcion", "Casos_reportados", "Casos_PASS", "Casos_FAIL"]); [w.writerow([n, len(v), sum(c[1] for c in v), sum(not c[1] for c in v)]) for n, v in por_fn.items()]
        w.writerow(["TOTAL_REPORTADO", total, total - len(fallos), len(fallos)])
