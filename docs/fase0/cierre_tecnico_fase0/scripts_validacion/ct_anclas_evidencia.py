#!/usr/bin/env python3
# ct_anclas_evidencia.py — ANCLAJE EXTERNO de las salidas de la reconciliación (H-02). Corre FUERA del verificador de consistencia: el verificador no puede ser la evidencia de sí mismo.
# El orquestador ancla, justo tras generar una salida, (a) su SHA-256 real, (b) los totales declarados en el stdout del generador y (c) el id de ejecución; las anclas se guardan en el directorio de SALIDA del orquestador
# (fuera del directorio de cierre que un atacante podría reescribir de forma coherente). K recalcula y compara. Una modificación COHERENTE de JSON+TXT+MD (que el verificador de consistencia no ve) cambia el SHA-256 anclado.
# Uso:  anclar <dir_cierre> <anclas.json> <run_id> <fase> [--stdout archivo_con_TOTAL=…]      verificar <dir_cierre> <anclas.json> <run_id>      controles <dir_cierre> <salida.txt>
import hashlib, json, os, re, shutil, sys, tempfile
REC = ["scripts_validacion/resultados/reconciliacion_integral.json", "scripts_validacion/resultados/reconciliacion_integral.txt", "INFORME_RECONCILIACION_INTEGRAL.md"]
MAN = ["MANIFIESTO_SHA256_CIERRE.txt"]
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def anclar(c, af, run, fase, stdout=None):
    A = json.load(open(af)) if os.path.exists(af) else {"ejecucion_id": run, "anclas": {}}
    if A["ejecucion_id"] != run: raise SystemExit("ANCLAS de otra ejecución")
    arch = REC if fase == "H" else MAN
    for r in arch:
        p = os.path.join(c, r)
        if not os.path.isfile(p): raise SystemExit("falta salida a anclar: %s" % r)
        A["anclas"][r] = sha(p)
    if fase == "H":
        J = json.load(open(os.path.join(c, REC[0]), encoding="utf-8")); A["totales"] = {"total": J["total"], "pass": J["pass"], "fail": J["fail"], "n_comprobaciones": len(J["comprobaciones"]), "ejecucion_ids": sorted({x["ejecucion_id"] for x in J["comprobaciones"]})}
        if stdout:
            m = re.findall(r"TOTAL=(\d+) PASS=(\d+) FAIL=(\d+)", open(stdout, encoding="utf-8").read())
            if len(m) != 1 or tuple(map(int, m[0])) != (J["total"], J["pass"], J["fail"]): raise SystemExit("totales del stdout del generador ≠ JSON: %s vs %s" % (m, (J["total"], J["pass"], J["fail"])))
            A["totales_stdout"] = list(map(int, m[0]))
    json.dump(A, open(af, "w"), indent=1, sort_keys=True)
def verificar(c, af, run):
    f = []
    try: A = json.load(open(af))
    except Exception as e: return ["anclas ilegibles/ausentes: %r" % e]
    if A.get("ejecucion_id") != run: f.append("anclas de otra ejecución")
    if not A.get("anclas") or not set(REC) <= set(A["anclas"]): f.append("anclas de la reconciliación ausentes")
    for r, h in A.get("anclas", {}).items():
        p = os.path.join(c, r)
        if not os.path.isfile(p): f.append("salida anclada ausente: %s" % r)
        elif sha(p) != h: f.append("salida modificada después de generarse: %s" % r)
    try:
        J = json.load(open(os.path.join(c, REC[0]), encoding="utf-8")); t = A.get("totales", {})
        if (J["total"], J["pass"], J["fail"], len(J["comprobaciones"])) != (t.get("total"), t.get("pass"), t.get("fail"), t.get("n_comprobaciones")): f.append("totales/nº de comprobaciones distintos de los anclados")
        if "totales_stdout" in A and A["totales_stdout"] != [J["total"], J["pass"], J["fail"]]: f.append("totales del stdout del generador distintos del JSON")
        if {x["ejecucion_id"] for x in J["comprobaciones"]} != {run}: f.append("comprobaciones de otra ejecución")
    except Exception as e: f.append("JSON ilegible: %r" % e)
    return f
if __name__ == "__main__" and sys.argv[1] == "anclar":
    a = sys.argv[2:]; so = a[a.index("--stdout") + 1] if "--stdout" in a else None; anclar(os.path.abspath(a[0]), a[1], a[2], a[3], so); print("ANCLADO", a[3]); sys.exit(0)
if __name__ == "__main__" and sys.argv[1] == "verificar":
    f = verificar(os.path.abspath(sys.argv[2]), sys.argv[3], sys.argv[4]); [print("FAIL |", x) for x in f]; print("ANCLAS incoherencias=%d" % len(f)); sys.exit(1 if f else 0)
if __name__ == "__main__" and sys.argv[1] == "controles":
    c = os.path.abspath(sys.argv[2]); out = sys.argv[3]; res = []; run = "RUN-CONTROL"
    def caso(n, mod, debe, con_anclas_nuevas=False):
        d = tempfile.mkdtemp(prefix="anc_"); dst = os.path.join(d, "c"); shutil.copytree(c, dst, ignore=shutil.ignore_patterns("__pycache__")); af = os.path.join(d, "anclas.json")
        try:
            J = json.load(open(os.path.join(dst, REC[0]), encoding="utf-8")); [x.update(ejecucion_id=run) for x in J["comprobaciones"]]; json.dump(J, open(os.path.join(dst, REC[0]), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            anclar(dst, af, run, "H"); mod(dst, af); f = verificar(dst, af, run); ok = bool(f) == debe; res.append(("PASS" if ok else "FAIL", n + (" (detecta: %s)" % f[0][:70] if f else " (sin incoherencias)")))
        finally: shutil.rmtree(d, ignore_errors=True)
    P = lambda d, r: os.path.join(d, r)
    def coherente(d, af):   # el atacante elimina una comprobación y reescribe JSON, TXT y MD de forma coherente: el verificador de consistencia lo aceptaría
        J = json.load(open(P(d, REC[0]), encoding="utf-8")); x = J["comprobaciones"].pop(); J["total"] -= 1; J["pass"] -= 1; json.dump(J, open(P(d, REC[0]), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        T = open(P(d, REC[1]), encoding="utf-8").read().splitlines(); T = [l for l in T if not l.startswith("TOTAL=")][:-1] + ["TOTAL=%d PASS=%d FAIL=%d" % (J["total"], J["pass"], J["fail"])]; open(P(d, REC[1]), "w", encoding="utf-8").write("\n".join(T) + "\n")
    def solo_md(d, af): open(P(d, REC[2]), "a", encoding="utf-8").write("\nTexto añadido\n")
    def borra_json(d, af): os.remove(P(d, REC[0]))
    def otra_ejecucion(d, af):
        J = json.load(open(P(d, REC[0]), encoding="utf-8")); J["comprobaciones"][0]["ejecucion_id"] = "CCI-RUN-VIEJA"; json.dump(J, open(P(d, REC[0]), "w", encoding="utf-8"), ensure_ascii=False, indent=1); anclar_sha = sha(P(d, REC[0])); A = json.load(open(af)); A["anclas"][REC[0]] = anclar_sha; json.dump(A, open(af, "w"))
    def anclas_ajenas(d, af): A = json.load(open(af)); A["ejecucion_id"] = "OTRA"; json.dump(A, open(af, "w"))
    def sin_anclas(d, af): os.remove(af)
    def stdout_distinto(d, af): A = json.load(open(af)); A["totales_stdout"] = [1, 1, 0]; json.dump(A, open(af, "w"))
    def reancla_atacante(d, af): coherente(d, af); anclar(d, af, run, "H")   # si el atacante pudiera reescribir las anclas, el control es el directorio de salida del orquestador (fuera del cierre): se documenta
    caso("sin manipulación", lambda d, a: None, False)
    caso("modificación COHERENTE de JSON+TXT (eliminar una comprobación y ajustar totales)", coherente, True)
    caso("INFORME .md alterado", solo_md, True)
    caso("reconciliacion_integral.json eliminado", borra_json, True)
    caso("comprobación de otra ejecución con SHA re-anclado a mano en el JSON (la comprobación de run id lo delata)", otra_ejecucion, True)
    caso("anclas de otra ejecución", anclas_ajenas, True)
    caso("anclas ausentes", sin_anclas, True)
    caso("totales del stdout del generador no coinciden con el JSON", stdout_distinto, True)
    n = sum(r[0] == "FAIL" for r in res); L = ["%s | %s" % r for r in res] + ["TOTAL=%d FAIL=%d" % (len(res), n)]; open(out, "w", encoding="utf-8").write("\n".join(L) + "\n"); print("\n".join(L)); sys.exit(1 if n else 0)
