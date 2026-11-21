#!/usr/bin/env python3
# Ejecución INDIVIDUAL de T-409..T-422 sobre las tablas C y D de 4.4.10 (las que los escenarios alteran) con el verificador K47 publicado (simular_k47 de verificar_expediente.py, sin modificarlo).
# Uso: python3 -I -B ct_t409_t422_individual.py <ruta_docs_fase0> [salida.csv]
# Alcance: verificador EN MEMORIA sobre las tablas del texto de la especificación; NO es el esquema físico. Las columnas de la tabla se alteran UNA a la vez (cambio único) y se compara con un control sin alterar y un control de no-op.
import sys, os, re, copy, csv, importlib.util
sys.dont_write_bytecode = True
d = sys.argv[1]; out = sys.argv[2] if len(sys.argv) > 2 else None
sp = importlib.util.spec_from_file_location("verificar_expediente", os.path.join(d, "herramientas", "verificar_expediente.py")); VE = importlib.util.module_from_spec(sp); sp.loader.exec_module(VE)
espec_txt = open(os.path.join(d, "ESPECIFICACION_TECNICA_G1_G5_G10.md"), encoding="utf-8").read()
P = VE.parse_4410(espec_txt); base = VE.simular_k47(P)
FUENTES = ["brief", "promoción", "copy"]
def fila_c(Q, f, c): return [r for r in Q["efec_clas"] if r["fuente"] == f and r["clas"] == c][0]
def fila_d(Q, e): return [r for r in Q["efec_evt"] if r["evento"] == e][0]
# escenario -> (alteraciones [(descripción, función de alteración)], prefijo(s) del invariante esperado)
def c_alt(clas, col, val, fuentes=FUENTES):
    return [("%s: fila %s/%s, %s := %s" % (col, f, clas, col, val), (lambda Q, f=f: fila_c(Q, f, clas).__setitem__(col, val)), 1) for f in fuentes]
def todas(clas, col, val):   # variante compensada: la MISMA alteración en las tres fuentes (I9 no puede detectarla; I1/I2 sí)
    def f(Q):
        for x in FUENTES: fila_c(Q, x, clas).__setitem__(col, val)
    return [("%s: las TRES fuentes a la vez, fila */%s, %s := %s" % (col, clas, col, val), f, 3)]
def d_alt(ev, col, val): return [("fila D '%s', %s := %s" % (ev, col, val), (lambda Q: fila_d(Q, ev).__setitem__(col, val)), 1)]
ESC = {
 "T-409": (c_alt("sustituido", "retira", "automática") + todas("sustituido", "retira", "automática"), ["I1"]),
 "T-410": (c_alt("eliminado", "retira", "automática") + todas("eliminado", "retira", "automática"), ["I1"]),
 "T-411": (c_alt("modificado", "conserva", "ninguna") + todas("modificado", "conserva", "ninguna"), ["I1"]),
 "T-412": (c_alt("introducido", "incorpora", "no") + todas("introducido", "incorpora", "no"), ["I2"]),
 "T-413": (d_alt("resolución rechazada", "efecto_e", "sale la persona afectada"), ["I5"]),
 "T-414": (d_alt("resolución aceptada", "retira", "todas las atribuciones del campo"), ["I3"]),
 "T-415": (d_alt("resolución aceptada", "reescribe", "sí"), ["I10"]),
 "T-416": (d_alt("versión nueva", "retira", "no hereda"), ["I10"]),
 "T-417": (d_alt("cadena incompleta", "efecto_e", "parcial"), ["I8"]),
 "T-418": (d_alt("resolución aceptada", "efecto_e", "sale siempre la persona"), ["I7"]),
 "T-419": (c_alt("sustituido", "conserva", "ninguna", ["copy"]), ["I9", "I1"]),     # «solo la fila sustituido de copy»
 "T-420": (c_alt("eliminado", "retira", "automática", ["promoción"]), ["I9", "I1"]), # «solo la fila eliminado de promoción»
 "T-421": (c_alt("sustituido", "similitud", "sí", ["copy"]), ["I11"]),
 "T-422": (d_alt("cambio de clasificación", "retira", "atribuciones"), ["I12"]),
}
lineas = espec_txt.split("\n"); filas = []; ok_global = base == []
print("CONTROL sin alterar: violaciones=%d %s" % (len(base), "OK" if not base else base[:2]))
# control de no-op: reasignar el valor actual no debe producir violaciones (la detección no es vacua)
Q = copy.deepcopy(P); fila_c(Q, "copy", "sustituido")["conserva"] = fila_c(P, "copy", "sustituido")["conserva"]; noop = VE.simular_k47(Q)
print("CONTROL no-op (mismo valor): violaciones=%d %s" % (len(noop), "OK" if not noop else noop[:2])); ok_global &= noop == []
for t, (alts, esperados) in ESC.items():
    ln = [i + 1 for i, l in enumerate(lineas) if l.startswith("| %s |" % t)][0]
    for desc, fn, *nc in alts:
        Q = copy.deepcopy(P); fn(Q)
        cambios = sum(1 for a, b in zip(P["efec_clas"] + P["efec_evt"], Q["efec_clas"] + Q["efec_evt"]) for k in a if a[k] != b[k])
        v = VE.simular_k47(Q); cods = sorted({x[0].split()[0] for x in v}); det = bool(v) and any(c == e for c in cods for e in esperados)
        esperado_cambios = nc[0] if nc else 1; ok_global &= det and cambios == esperado_cambios
        filas.append((t, ln, desc, cambios, "|".join(cods), "|".join(esperados), "DETECTADA" if det else "NO_DETECTADA", "cambios_esperados=%d cumplido=%s" % (esperado_cambios, cambios == esperado_cambios)))
        print("%s | l.%d | %s | cambios=%d | invariantes=%s | esperado=%s | %s" % (t, ln, desc, cambios, ",".join(cods), ",".join(esperados), "DETECTADA" if det else "NO_DETECTADA"))
print("TOTAL variantes=%d DETECTADAS=%d escenarios=%d (14 esperados) control_sin_alterar_ok=%s todo_ok=%s" % (len(filas), sum(f[6] == "DETECTADA" for f in filas), len({f[0] for f in filas}), base == [], ok_global))
if out:
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh); w.writerow(["Escenario", "Linea_ESPEC", "Alteracion_unica", "Celdas_cambiadas", "Invariantes_observados", "Invariante_esperado", "Resultado", "Cambio_unico"]); w.writerows(filas)
