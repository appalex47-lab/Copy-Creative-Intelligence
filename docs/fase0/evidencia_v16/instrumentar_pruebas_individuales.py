#!/usr/bin/env python3
"""Expone los resultados individuales de pruebas_guarda() y pruebas_atomicidad() SIN modificar su lógica.
Importa herramientas/modelo_estructural.py tal cual, llama a las funciones y presenta cada par (nombre, resultado).
Uso: python3 -I instrumentar_pruebas_individuales.py RUTA_A_herramientas"""
import sys, importlib
sys.path.insert(0, sys.argv[1])
MS = importlib.import_module("modelo_estructural")
tot = fails = 0
for fn in ("pruebas_guarda", "pruebas_atomicidad"):
    try:
        res = getattr(MS, fn)()
    except Exception as ex:
        print("%s ERROR_AL_EJECUTAR %s: %s" % (fn, type(ex).__name__, str(ex)[:200])); fails += 1; continue
    for n, (nombre, ok) in enumerate(res, 1):
        tot += 1; fails += (0 if ok is True else 1)
        print("%s-%02d | esperado=True | obtenido=%s | %s | %s%s" % (fn, n, ok, "PASS" if ok is True else "FAIL", nombre, "" if ok is True else " | MENSAJE: el resultado no es True"))
    print("%s: %d casos" % (fn, len(res)))
print("TOTAL %d casos, %d PASS, %d FAIL" % (tot, tot - fails, fails))
sys.exit(1 if fails else 0)
