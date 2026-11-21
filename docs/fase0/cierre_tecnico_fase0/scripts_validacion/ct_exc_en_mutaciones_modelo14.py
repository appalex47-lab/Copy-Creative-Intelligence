#!/usr/bin/env python3
# Comprueba si en correr_mutaciones_modelo14 alguna «detección» procede de una EXCEPCIÓN capturada por _baterias14 (entrada 'EXC') en lugar de un fallo localizado.
# Uso: python3 -I -B ct_exc_en_mutaciones_modelo14.py <modelo_estructural.py>. No modifica el modelo (parchea y restaura en memoria, igual que la función original).
import importlib.util, sys
sys.dont_write_bytecode = True
sp = importlib.util.spec_from_file_location("ms", sys.argv[1]); M = importlib.util.module_from_spec(sp); sp.loader.exec_module(M)
base = M._baterias14(); print("BASE: baterías=%d fallos=%d EXC=%d" % (len(base), sum(not x[2] for x in base), sum(x[1] == "EXC" for x in base)))
tot = 0
for mid, desc, fab in M.K56_MUT:
    obj, nom, nuevo = fab(); viejo = getattr(obj, nom); setattr(obj, nom, nuevo)
    try: r = M._baterias14()
    finally: setattr(obj, nom, viejo)
    f = [x for x in r if not x[2]]; exc = [x for x in f if x[1] == "EXC"]; loc = [x for x in f if x[1] != "EXC"]; tot += len(exc)
    print("%s | fallos_localizados=%d | EXC=%d | detección_solo_por_EXC=%s" % (mid, len(loc), len(exc), bool(exc) and not loc))
print("TOTAL entradas EXC en las 12 mutaciones=%d" % tot)
