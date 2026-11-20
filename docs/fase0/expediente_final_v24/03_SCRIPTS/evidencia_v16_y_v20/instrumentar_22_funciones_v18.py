#!/usr/bin/env python3
"""Instrumentación EXTERNA y de solo lectura (V18): imprime el resultado individual de cada caso de las 22 funciones
de ejecución de modelo_estructural.py. No modifica el modelo ni el verificador. Uso: python3 -I este.py <dir herramientas> <especificacion.md>"""
import importlib.util, sys, os
sys.dont_write_bytecode = True
H, SPEC = sys.argv[1], sys.argv[2]
sys.path.insert(0, H)
def load(n, p):
    s = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(s); sys.modules[n] = m; s.loader.exec_module(m); return m
V = load("verificar_expediente", os.path.join(H, "verificar_expediente.py")); MS = load("modelo_estructural_i", os.path.join(H, "modelo_estructural.py"))
spec = open(SPEC, encoding="utf-8").read()
F = ["pruebas_guarda","pruebas_atomicidad","correr_mutaciones_rechazo","correr_adversariales","correr_escenarios","correr_mutaciones_k47","correr_mutaciones_resoluciones","correr_mutaciones_assets","correr_positivos_arte","correr_mutaciones_k45","correr_mutaciones_cadena","correr_adversariales_cadena","correr_mutaciones_atribucion","pruebas_atomicidad14","pruebas_E14","correr_mutaciones_av","correr_mutaciones_cf","correr_mutaciones_ac","correr_positivos15","correr_adversariales15","pruebas_atomicidad15","correr_mutaciones_modelo14"]
tot = {}; fallos = 0
for f in F:
    if f == "correr_mutaciones_k45":
        mut, pos = MS.correr_mutaciones_k45(V.parse_4410(spec)["matriz"]); r = list(mut)
        for i, (nom, errs) in enumerate(pos): print("%s | POS-%02d | esperado=sin errores | obtenido=%s | %s | %s" % (f, i+1, "sin errores" if not errs else "%d errores" % len(errs), "PASS" if not errs else "FAIL", nom)); fallos += bool(errs)
    else: r = getattr(MS, f)()
    n = 0
    for i, x in enumerate(r, 1):
        if isinstance(x, tuple): nom, ok = x[0], bool(x[-1]); idc = "%02d" % i; flags = ""
        else:
            idc = x.get("id", "%02d" % i); nom = (x.get("nombre") or x.get("mut") or "")[:80]
            ok = bool(x["ok"]) if "ok" in x else bool(x.get("det"))
            flags = ",".join(k for k, v in x.items() if isinstance(v, bool) and not v)
        n += 1; fallos += (not ok)
        print("%s | %s | esperado=True | obtenido=%s | %s | %s%s" % (f, idc, ok, "PASS" if ok else "FAIL", nom, (" | flags_falsos=" + flags) if flags else ""))
    tot[f] = n
print("TOTAL funciones=%d casos=%d fallos=%d" % (len(F), sum(tot.values()), fallos))
print("CASOS_POR_FUNCION " + " ".join("%s=%d" % kv for kv in tot.items()))
sys.exit(1 if fallos else 0)
