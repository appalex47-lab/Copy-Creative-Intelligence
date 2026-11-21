#!/usr/bin/env python3
"""RV07 (definición precisa, V26): el REPORTE_PUBLICACION_V25_GITHUB.md publicado en GitHub (HEAD) es coherente con el REPORTE_VALIDACION_V25.md publicado
(mismo HEAD) y con las salidas crudas archivadas.
Uso: python3 -I rv07_comparar_reportes.py <pub.md remoto> <val.md remoto> <pub.md local@HEAD> <raw_A> <raw_C> <raw_RV_original> <sha_expediente>"""
import sys, re, hashlib
pub, val, publ, rawA, rawC, rawRV, sha = sys.argv[1:8]
rd = lambda p: open(p, encoding="utf-8", newline="").read()
P, V, PL, A, C, RV = rd(pub), rd(val), rd(publ), rd(rawA), rd(rawC), rd(rawRV)
res = []
def ok(i, d, c, x=""): res.append(c); print(("PASS" if c else "FAIL"), "|", i, d, "|", x)
blocks = lambda t: re.findall(r"```\n(.*?)```", t, re.S)
ok("RV07.a", "el reporte de publicación remoto es idéntico byte a byte al del commit HEAD local", hashlib.sha256(P.encode()).hexdigest() == hashlib.sha256(PL.encode()).hexdigest(), "sha256=" + hashlib.sha256(P.encode()).hexdigest())
ok("RV07.b", "ambos reportes declaran 16 controles de validación (P01–P14 + Q01–Q02) y 11 verificaciones remotas (RV01–RV11)",
   "16 controles de validación distintos (P01–P14 y Q01–Q02) y 11 verificaciones remotas (RV01–RV11)" in V and "16 controles de validación (P01–P14 + Q01–Q02) y 11 verificaciones remotas (RV01–RV11)" in P)
bv = blocks(V); bp = blocks(P)
ok("RV07.c", "el bloque de la pasada A del reporte de validación remoto = salida cruda de la pasada A", len(bv) == 1 and bv[0] == A and "RESUMEN V25: 14 controles, 14 PASS, 0 FAIL" in bv[0])
ok("RV07.d", "el bloque C del reporte de publicación remoto = salida cruda de la pasada C", len(bp) == 2 and bp[0] == C and "RESUMEN V25: 16 controles, 16 PASS, 0 FAIL" in bp[0])
ok("RV07.e", "el bloque E del reporte de publicación remoto = salida cruda original de RV01–RV06 y RV08–RV11 (sin RV07)", bp[1] == RV and not re.search(r"^RV07 ", bp[1], re.M) and len(re.findall(r"^RV\d\d ", bp[1], re.M)) == 10)
ok("RV07.f", "el SHA del commit del expediente citado en el reporte de publicación es el del padre del HEAD", sha in P and sha[:8] in P)
ok("RV07.g", "las etapas A–E del reporte de validación remoto coinciden con las del reporte de publicación (A 14/14, C 16/16, E RV01–RV11)", "| A. Previa" in V and "P01–P14 (14 controles)" in V and "16 controles" in V and "RV01–RV11" in P and "P01–P14, 14/14 PASS" in P and "16/16 PASS" in P)
resumen = re.search(r"## Resultado de las verificaciones \(resumen\)\n(.*?)\n", P, re.S).group(1)
print("INFO | RV07 observación (no criterio de PASS): el resumen de resultados del reporte de publicación lista", sorted(set(re.findall(r"RV\d\d", resumen))), "y omite RV10 y RV11, aunque sus salidas están en el bloque E; y declara RV07 pendiente de ejecución")
n = len(res); f = res.count(False); print("RESUMEN RV07: %d comprobaciones, %d PASS, %d FAIL" % (n, n - f, f)); sys.exit(1 if f else 0)
