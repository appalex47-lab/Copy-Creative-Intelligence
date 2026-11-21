#!/usr/bin/env python3
# Uso: python3 -I -B ct_verificar_consistencia_informe.py verificar <dir_cierre> | controles <dir_cierre> <salida.txt>
# Comprueba que reconciliacion_integral.{json,txt} e INFORME_RECONCILIACION_INTEGRAL.md tienen exactamente los mismos totales y estados por comprobación,
# que cada evidencia citada existe y su SHA-256 coincide con los bytes actuales (salvo los archivos que la propia ejecución regenera: se declaran), y que TOTAL = PASS + FAIL.
import json, os, re, sys, hashlib, shutil, tempfile
def leer(c):
    R = os.path.join(c, "scripts_validacion", "resultados"); J = json.load(open(os.path.join(R, "reconciliacion_integral.json"), encoding="utf-8"))
    T = open(os.path.join(R, "reconciliacion_integral.txt"), encoding="utf-8").read().splitlines(); M = open(os.path.join(c, "INFORME_RECONCILIACION_INTEGRAL.md"), encoding="utf-8").read().splitlines()
    return J, T, M
def verificar(c):
    J, T, M = leer(c); fallos = []
    if J["total"] != J["pass"] + J["fail"] or J["total"] != len(J["comprobaciones"]): fallos.append("JSON: total != pass+fail o != nº de comprobaciones")
    if sum(1 for x in J["comprobaciones"] if x["estado"] == "FAIL") != J["fail"]: fallos.append("JSON: fail no coincide con los estados")
    tt = [l for l in T if l.startswith("TOTAL=")]
    if tt != ["TOTAL=%d PASS=%d FAIL=%d" % (J["total"], J["pass"], J["fail"])]: fallos.append("TXT: línea TOTAL difiere del JSON: %s" % tt)
    est_t = [l.split(" | ", 1)[0] for l in T if not l.startswith("TOTAL=")]
    if est_t != [x["estado"] for x in J["comprobaciones"]]: fallos.append("TXT: estados por comprobación difieren del JSON")
    mt = [l for l in M if l.startswith("**TOTAL=")]
    if mt != ["**TOTAL=%d PASS=%d FAIL=%d**" % (J["total"], J["pass"], J["fail"])]: fallos.append("MD: línea TOTAL difiere del JSON: %s" % mt)
    filas = [l for l in M if re.match(r"\| \d+ \| (PASS|FAIL) \|", l)]
    if [re.match(r"\| (\d+) \| (PASS|FAIL) \|", l).groups() for l in filas] != [(str(x["id"]), x["estado"]) for x in J["comprobaciones"]]: fallos.append("MD: filas (id, estado) difieren del JSON")
    ids = [x.get("id_unico") for x in J["comprobaciones"]]
    if len(ids) != len(set(ids)) or None in ids: fallos.append("IDs únicos duplicados o ausentes")
    if sorted(x["id"] for x in J["comprobaciones"]) != list(range(1, len(J["comprobaciones"]) + 1)): fallos.append("filas faltantes o numeración no continua")
    esperado = os.environ.get("CCI_RUN_ID")
    for x in J["comprobaciones"]:
        if x["estado"] == "PASS" and not x["evidencia"]: fallos.append("PASS con evidencia vacía: %s" % x.get("id_unico"))
        for k in ("fuente", "metodo", "ejecucion_id", "fecha_ejecucion_utc"):
            if not x.get(k): fallos.append("campo obligatorio vacío %s en %s" % (k, x.get("id_unico")))
        if esperado and x.get("ejecucion_id") != esperado: fallos.append("resultado heredado: %s pertenece a otra ejecución (%s != %s)" % (x.get("id_unico"), x.get("ejecucion_id"), esperado))
        if x["estado"] == "FAIL" and J["fail"] == 0: fallos.append("estado contradictorio: FAIL con fail=0")
    regen = ("INFORME_RECONCILIACION_INTEGRAL.md", "reconciliacion_integral", "MANIFIESTO_SHA256_CIERRE.txt")
    for x in J["comprobaciones"]:
        for e in x["evidencia"]:
            p = os.path.join(c, e["ruta"])
            if e["ruta"].startswith("virtual:"): continue
            if any(k in e["ruta"] for k in regen): continue
            if not os.path.exists(p): fallos.append("evidencia ausente: %s (comprobación %d)" % (e["ruta"], x["id"]))
            elif hashlib.sha256(open(p, "rb").read()).hexdigest() != e["sha256"]: fallos.append("evidencia modificada tras la reconciliación: %s (comprobación %d)" % (e["ruta"], x["id"]))
    return fallos, J
def copia(c):
    d = tempfile.mkdtemp(prefix="ctcons_"); dst = os.path.join(d, "c"); shutil.copytree(c, dst, ignore=shutil.ignore_patterns("__pycache__")); return d, dst
if sys.argv[1] == "verificar":
    f, J = verificar(os.path.abspath(sys.argv[2]))
    for x in f: print("FAIL |", x)
    print("CONSISTENCIA total=%d pass=%d fail=%d | incoherencias=%d" % (J["total"], J["pass"], J["fail"], len(f))); sys.exit(1 if f else 0)
c = os.path.abspath(sys.argv[2]); salida = sys.argv[3]; res = []
def caso(n, mod, debe_fallar):
    d, dst = copia(c)
    try:
        mod(dst); f, _ = verificar(dst); ok = bool(f) == debe_fallar; res.append(("PASS" if ok else "FAIL", n + (" (detecta: %s)" % f[0][:60] if f else " (sin incoherencias)")))
    finally: shutil.rmtree(d, ignore_errors=True)
R = lambda d: os.path.join(d, "scripts_validacion", "resultados", "reconciliacion_integral.%s")
M = lambda d: os.path.join(d, "INFORME_RECONCILIACION_INTEGRAL.md")
def sub(p, a, b):
    s = open(p, encoding="utf-8").read(); assert a in s, a; open(p, "w", encoding="utf-8").write(s.replace(a, b, 1))
J0, _, _ = leer(c)
caso("coherente: sin manipulación", lambda d: None, False)
caso("MD: FAIL=0 → FAIL=1 (la contradicción detectada en la revisión)", lambda d: sub(M(d), "FAIL=%d**" % J0["fail"], "FAIL=%d**" % (J0["fail"] + 1)), True)
caso("TXT: línea TOTAL alterada", lambda d: sub(R(d) % "txt", "TOTAL=%d " % J0["total"], "TOTAL=%d " % (J0["total"] + 1)), True)
caso("JSON: una comprobación pasa a FAIL", lambda d: sub(R(d) % "json", '"estado": "PASS"', '"estado": "FAIL"'), True)
caso("MD: estado de una fila alterado", lambda d: sub(M(d), "| 1 | PASS |", "| 1 | FAIL |"), True)
caso("evidencia: archivo citado modificado", lambda d: open(os.path.join(d, "MATRIZ_LIMITACIONES_RESIDUALES.csv"), "a", encoding="utf-8").write("x\n"), True)
def vacia(d):
    p = R(d) % "json"; J = json.load(open(p, encoding="utf-8")); J["comprobaciones"][3]["evidencia"] = []; json.dump(J, open(p, "w", encoding="utf-8"))
def dup(d):
    p = R(d) % "json"; J = json.load(open(p, encoding="utf-8")); J["comprobaciones"][4]["id_unico"] = J["comprobaciones"][3]["id_unico"]; json.dump(J, open(p, "w", encoding="utf-8"))
def hashmal(d):
    p = R(d) % "json"; J = json.load(open(p, encoding="utf-8"))
    for x in J["comprobaciones"]:
        for e in x["evidencia"]:
            if not e["ruta"].startswith("virtual:") and "reconciliacion" not in e["ruta"] and "MANIFIESTO" not in e["ruta"]: e["sha256"] = "0" * 64; json.dump(J, open(p, "w", encoding="utf-8")); return
def fila(d):
    p = R(d) % "json"; J = json.load(open(p, encoding="utf-8")); del J["comprobaciones"][7]; json.dump(J, open(p, "w", encoding="utf-8"))
def borra(d):
    for x in J0["comprobaciones"]:
        for e in x["evidencia"]:
            if "MATRIZ_TRAZABILIDAD_MAESTRA" in e["ruta"]: os.remove(os.path.join(d, e["ruta"])); return
caso("evidencia: archivo citado eliminado", borra, True)
caso("evidencia vacía en una comprobación PASS", vacia, True)
caso("ID único duplicado", dup, True)
caso("hash incorrecto en la evidencia", hashmal, True)
caso("fila faltante", fila, True)
os.environ["CCI_RUN_ID"] = "otra-ejecucion"; caso("resultado heredado (otra ejecución)", lambda d: None, True); os.environ.pop("CCI_RUN_ID")
n = sum(r[0] == "FAIL" for r in res); L = ["%s | %s" % r for r in res] + ["TOTAL=%d FAIL=%d" % (len(res), n)]
open(salida, "w", encoding="utf-8").write("\n".join(L) + "\n"); print("\n".join(L)); sys.exit(1 if n else 0)
