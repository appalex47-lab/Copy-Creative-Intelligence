#!/usr/bin/env python3
# Uso: python3 -I -B aud_comparar_clusteres.py <arbolA> <arbolB> <salida.txt>. Compara, paso a paso, las baterías ejecutadas en DOS clústeres nuevos e independientes.
# Normaliza SOLO lo que legítimamente difiere (marcas de tiempo, rutas del árbol, socket/puerto, system_identifier, pid) y exige igualdad del resto, byte a byte.
import csv, os, re, sys, hashlib
A, B, OUT = sys.argv[1:4]; A, B = os.path.abspath(A), os.path.abspath(B); S = "docs/fase0/cierre_tecnico_fase0/scripts_validacion/resultados/"
def norm(b, arbol, sock):
    t = b.decode("utf-8", "replace")
    t = t.replace(arbol, "<ARBOL>")
    t = re.sub(r"/tmp/aud/pg[A-Z]/sock", "<SOCK>", t); t = re.sub(r"\b5545[0-9]\b", "<PORT>", t)
    t = re.sub(r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{4})?", "<TS>", t)
    t = re.sub(r"\b\d{2}:\d{2}:\d{2}(\.\d+)?\b", "<HORA>", t); t = re.sub(r"\b77105\d{14}\b", "<SYSID>", t)
    t = re.sub(r"huella(=| md5=)[0-9a-f]{8}", "huella=<H>", t); t = re.sub(r"\(huella [0-9a-f]{8}\)", "(huella <H>)", t); t = re.sub(r"id=[0-9a-f]{8}", "id=<H>", t)
    t = re.sub(r"\b[0-9a-f]{12,64}\b", "<HEX>", t); t = re.sub(r"\d+(\.\d+)? ?ms\b", "<MS>", t); t = re.sub(r"\b(pid|PID)[= ]\d+", "pid=<N>", t)
    t = re.sub(r"\b\d+\.\d{2,3}\s?s\b", "<SEG>", t)
    return t
ia = list(csv.DictReader(open(A + "/" + S + "bateria_final/INDICE_BATERIA.csv", encoding="utf-8"))); ib = list(csv.DictReader(open(B + "/" + S + "bateria_final/INDICE_BATERIA.csv", encoding="utf-8")))
L = []; fails = 0
def reg(ok, n, d=""):
    global fails; fails += (not ok); L.append("%s | %s | %s" % ("PASS" if ok else "FAIL", n, d))
reg([r["paso"] for r in ia] == [r["paso"] for r in ib], "mismos pasos en el mismo orden (%d)" % len(ia))
for ra, rb in zip(ia, ib):
    iguales = ra["estado"] == rb["estado"] == "OK" and ra["resumen"] == rb["resumen"] and ra["rc"] == rb["rc"] == "0" and ra["esperado"] == rb["esperado"]
    K = "docs/fase0/cierre_tecnico_fase0"; pa = os.path.join(A, K, ra["salida"]); pb = os.path.join(B, K, rb["salida"])
    na = norm(open(pa, "rb").read(), A, ""); nb = norm(open(pb, "rb").read(), B, "")
    ok_sal = na == nb
    reg(iguales and ok_sal, "paso %s: estado/resumen/rc/esperado idénticos (%s) y salida idéntica tras normalizar marcas de tiempo/rutas/socket/identificadores (%s)" % (ra["paso"], ra["resumen"][:48], "idéntica" if ok_sal else "DIFIERE"))
# archivos de resultados deterministas que deben coincidir exactamente (sin normalizar)
for f in ("guarda_destino.txt", "aserciones_smoke.txt", "reconciliacion_integral.txt", "controles_negativos_manifiesto.txt", "controles_consistencia_informe.txt", "escaner_seguridad_sql.txt", "escaner_seguridad_autoprueba.txt"):
    a = open(A + "/" + S + f, "rb").read(); b = open(B + "/" + S + f, "rb").read(); na, nb = norm(a, A, ""), norm(b, B, "")
    reg(na == nb, "resultado %s idéntico en ambos clústeres (%s)" % (f, "SHA-256 bruto %s" % ("igual" if a == b else "distinto; tras normalizar igual" if na == nb else "DIFIERE")))
print("\n".join(L)); open(OUT, "w", encoding="utf-8").write("\n".join(L) + "\nTOTAL=%d PASS=%d FAIL=%d\n" % (len(L), len(L) - fails, fails)); print("TOTAL=%d PASS=%d FAIL=%d" % (len(L), len(L) - fails, fails)); sys.exit(1 if fails else 0)
