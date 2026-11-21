#!/usr/bin/env python3
# Uso: python3 -I -B ct_k47_por_escenario.py <ruta_herramientas> [salida.csv]. Ejecución LOCAL en memoria; no modifica modelo_estructural.py.
import sys, importlib.util, csv, os
h = sys.argv[1]; out = sys.argv[2] if len(sys.argv) > 2 else None
spec = importlib.util.spec_from_file_location("modelo_estructural", os.path.join(h, "modelo_estructural.py")); MS = importlib.util.module_from_spec(spec); sys.dont_write_bytecode = True; spec.loader.exec_module(MS)
MAP = {"T-409":["K47-M01"],"T-410":["K47-M02"],"T-411":["K47-M03"],"T-412":["K47-M04"],"T-413":["K47-M05","K47-M18","K47-M19"],"T-414":["K47-M06","K47-M17","K47-M24"],
       "T-415":["K47-M07","K47-M26"],"T-416":["K47-M08","K47-M20"],"T-417":["K47-M09","K47-M22","K47-M23"],"T-418":["K47-M10","K47-M15","K47-M16","K47-M25"],
       "T-419":["K47-M11"],"T-420":["K47-M12"],"T-421":["K47-M13"],"T-422":["K47-M14"]}
res = {r["id"]: r for r in MS.correr_mutaciones_k47()}
filas = []; ok = True
for t, ms in MAP.items():
    for m in ms:
        r = res[m]; filas.append((t, m, r["mut"], r["esp"], r["obs"], "DETECTADA" if r["det"] else "NO_DETECTADA", "válido_inicial=%s cambio=%s" % (r["valido"], r["cambio"])))
        ok &= bool(r["det"]) and bool(r["valido"]) and bool(r["cambio"])
for f in filas: print(" | ".join(map(str, f)))
print("TOTAL mutaciones mapeadas=%d DETECTADAS=%d todas_detectadas_con_estado_inicial_valido=%s ; total K47_MUT=%d" % (len(filas), sum(f[5] == "DETECTADA" for f in filas), ok, len(res)))
if out:
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh); w.writerow(["Escenario", "Mutacion", "Descripcion", "Invariante_esperado", "Observacion", "Resultado", "Condiciones"]); w.writerows(filas)
