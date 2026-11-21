#!/usr/bin/env python3
# Uso: python3 -I -B ct_aserciones_smoke.py <dir_resultados> [salida.txt]. Aserciones sobre las salidas del smoke de los 6 scripts CCI-DEV (LOCAL; no es Supabase).
# Un rc=0 de psql no prueba nada por sí solo: aquí se exige el contenido esperado (guardas, veredictos, BLOCKED, residuos).
import os, re, sys
R = sys.argv[1]; out = sys.argv[2] if len(sys.argv) > 2 else None; res = []
t = lambda f: open(os.path.join(R, f), encoding="utf-8").read()
def a(n, ok): res.append(("PASS" if ok else "FAIL", n))
g = t("smoke_guardas.txt"); a("guardas: los 6 scripts abortan sin autorización (6 líneas 'abortado: SI')", len(re.findall(r"^GUARDA 0[1-5]_\w+ sin autorizacion -> abortado: SI", g, re.M)) == 6)
a("guarda: base 'postgres' (no cci_) en modo local aborta", "base 'postgres' (no cci_) con modo local -> abortado: SI" in g)
c = t("smoke_codigos.txt"); a("códigos de salida de las 6 ejecuciones = 0 (necesario, no suficiente)", all(("%s rc=0" % k) in c for k in ("01", "02", "03-defectuosa", "03-corregida", "04", "05")))
for f in ("smoke_01_inventario.txt", "smoke_02_rls_inventario.txt"):
    s = t(f); a("%s: salida no vacía (>100 líneas) y sin ERROR" % f, len(s.splitlines()) > 100 and not re.search(r"(?i)\berror\b", s))
d = t("smoke_03_rls_shim_defectuosa.txt"); a("03 defectuoso: detecta fuga (≥1 FAIL, FUGA)", len(re.findall(r"\| FAIL", d)) >= 1 and "FUGA" in d)
k = t("smoke_03_rls_shim_corregida.txt"); a("03 corregido: 0 FAIL, ≥8 PASS y RLS-06 NOT VERIFIED", not re.search(r"\| FAIL", k) and len(re.findall(r"\| PASS", k)) >= 8 and "NOT VERIFIED" in k)
q = t("04_r1r9_local_bloqueado.txt"); a("04: NO VERIFICABLE EN ENTORNO FÍSICO y sin residuos", "NO VERIFICABLE EN ENTORNO FÍSICO" in q and "PASS: sin residuos" in q)
a("05 sesión A y B: ejecutadas con PASS", "PASS" in t("smoke_05_sesion_A.txt") or "OK" in t("smoke_05_sesion_A.txt")); a("05 sesión B: PASS", "PASS" in t("smoke_05_sesion_B.txt"))
a("05 sin tabla: BLOCKED (no PASS)", "BLOCKED" in t("smoke_05_sin_tabla.txt") and "PASS" not in t("smoke_05_sin_tabla.txt"))
fail = sum(r[0] == "FAIL" for r in res); lines = ["%s | %s" % r for r in res] + ["TOTAL=%d PASS=%d FAIL=%d" % (len(res), len(res) - fail, fail)]
print("\n".join(lines))
if out: open(out, "w", encoding="utf-8").write("\n".join(lines) + "\n")
sys.exit(1 if fail else 0)
