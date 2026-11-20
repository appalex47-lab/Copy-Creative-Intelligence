#!/usr/bin/env python3
"""V21: recalcula las referencias de línea a la especificación en las matrices de reglas y escenarios
a partir del TEXTO real de la especificación vigente (no por desplazamiento fijo).
Uso: python3 -I v21_corregir_lineas.py <dir fase0> [--aplicar]
MIGRACIÓN ÚNICA (V20→V21), ya aplicada: las referencias "narrativa: l.N" pasan de la especificación c6ef74b a la vigente y no es idempotente; la vigilancia permanente es la batería v21_bateria_cierre.py (pruebas R-*). Sin --aplicar solo informa. Con --aplicar reescribe los dos CSV (UTF-8, LF, sin BOM, mismo formato)."""
import csv, io, re, sys, os
D = sys.argv[1]; APLICAR = "--aplicar" in sys.argv
SPEC = open(os.path.join(D, "ESPECIFICACION_TECNICA_G1_G5_G10.md"), encoding="utf-8").read().split("\n")
E = os.path.join(D, "expediente_final_v16_v19")
def leer(f):
    t = open(os.path.join(E, f), encoding="utf-8", newline="").read(); return t, list(csv.reader(io.StringIO(t, newline="")))
def escribir(f, filas):
    o = io.StringIO(); csv.writer(o, lineterminator="\n").writerows(filas)
    open(os.path.join(E, f), "w", encoding="utf-8", newline="").write(o.getvalue())
def filas_tabla(idv):
    return [i + 1 for i, l in enumerate(SPEC) if re.match(r"\|\s*" + re.escape(idv) + r"\s*\|", l)]
def resolver(idv, anterior, texto=None):
    c = [i for i in filas_tabla(idv) if 0 <= i - anterior <= 40]
    if texto is not None: c = [i for i in c if texto[:50] in SPEC[i - 1]]
    if len(c) < 1: raise SystemExit("NO RESUELTA %s (anterior %s)" % (idv, anterior))
    return min(c, key=lambda i: i - anterior)
cambios = {"reglas": 0, "escenarios": 0, "narrativa": 0}
# --- reglas
t, R = leer("MATRIZ_FINAL_231_REGLAS_V16_V19.csv"); h = R[0]
iR, iL, iT, iDep = h.index("Regla"), h.index("Linea_definicion"), h.index("Definicion_completa"), h.index("Dependencias_y_relaciones")
mapa_offset = {}
for f in R[1:]:
    ant = int(f[iL]); nuevo = resolver(f[iR], ant, f[iT])
    mapa_offset[ant] = nuevo - ant
    if nuevo != ant: cambios["reglas"] += 1
    f[iL] = str(nuevo)
# --- escenarios
t2, S = leer("MATRIZ_FINAL_780_ESCENARIOS_V16_V19.csv"); h2 = S[0]
iE, iLn, iNom = h2.index("Escenario"), h2.index("Linea_ESPEC"), h2.index("Nombre")
for f in S[1:]:
    ant = int(f[iLn]); nuevo = resolver(f[iE], ant, f[iNom]); cambios["escenarios"] += nuevo != ant; f[iLn] = str(nuevo)
# --- referencias de narrativa "l.N": se calcularon contra la especificación del commit c6ef74b (V19); se trasladan por correspondencia de TEXTO (difflib) a la vigente
import subprocess, difflib
OLD = subprocess.run(["git", "show", "c6ef74be4db185ac3e4fd36810f24619e6f51fcf:docs/fase0/ESPECIFICACION_TECNICA_G1_G5_G10.md"], capture_output=True, text=True, check=True, cwd=D).stdout.split("\n")
sm = difflib.SequenceMatcher(None, OLD, SPEC, autojunk=False); L2N = {}
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        for k in range(i2 - i1): L2N[i1 + k + 1] = j1 + k + 1
def corregir_dep(idv, txt):
    def sub_lista(m):
        out = []
        for n in re.findall(r"\d+", m.group(0)):
            n = int(n)
            if n not in L2N: raise SystemExit("SIN CORRESPONDENCIA %s l.%d (línea modificada en V20)" % (idv, n))
            if idv not in SPEC[L2N[n] - 1]: raise SystemExit("NO CONTIENE %s la línea %d" % (idv, L2N[n]))
            out.append(str(L2N[n]))
        return "narrativa: l." + ", ".join(out)
    return re.sub(r"narrativa: l\.\d+(?:, ?\d+)*", sub_lista, txt)
for f in R[1:]:
    nv = corregir_dep(f[iR], f[iDep])
    if nv != f[iDep]: cambios["narrativa"] += 1; f[iDep] = nv
print("CAMBIOS", cambios)
if APLICAR: escribir("MATRIZ_FINAL_231_REGLAS_V16_V19.csv", R); escribir("MATRIZ_FINAL_780_ESCENARIOS_V16_V19.csv", S); print("APLICADO")
