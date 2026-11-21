#!/usr/bin/env python3
# Verificador PROPIO de coherencia JSON/TXT/MD de la reconciliación. Uso: aud_consistencia.py <dir_dossier>
import json, os, re, sys
c = sys.argv[1]; R = os.path.join(c, "scripts_validacion/resultados"); J = json.load(open(os.path.join(R, "reconciliacion_integral.json"), encoding="utf-8"))
T = open(os.path.join(R, "reconciliacion_integral.txt"), encoding="utf-8").read(); M = open(os.path.join(c, "INFORME_RECONCILIACION_INTEGRAL.md"), encoding="utf-8").read(); f = []
n = len(J["comprobaciones"]); np_ = sum(x["estado"] == "PASS" for x in J["comprobaciones"]); nf = n - np_
mt = re.search(r"\*\*TOTAL=(\d+) PASS=(\d+) FAIL=(\d+)\*\*", M); tt = re.search(r"^TOTAL=(\d+) PASS=(\d+) FAIL=(\d+)$", T, re.M)
if (n, np_, nf) != (J["total"], J["pass"], J["fail"]): f.append("JSON interno")
if not tt or tuple(map(int, tt.groups())) != (n, np_, nf): f.append("TXT difiere de JSON")
if not mt or tuple(map(int, mt.groups())) != (n, np_, nf): f.append("MD difiere de JSON")
est_t = re.findall(r"^(PASS|FAIL) \| ", T, re.M); est_m = re.findall(r"^\| \d+ \| (PASS|FAIL) \|", M, re.M); est_j = [x["estado"] for x in J["comprobaciones"]]
if est_t != est_j: f.append("estados TXT != JSON")
if est_m != est_j: f.append("estados MD != JSON")
print("n=%d pass=%d fail=%d incoherencias=%s" % (n, np_, nf, f)); sys.exit(1 if f else 0)
