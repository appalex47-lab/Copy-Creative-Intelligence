#!/usr/bin/env python3
"""Controles negativos de la batería V21: en una COPIA TEMPORAL del repositorio se introduce un defecto concreto y se exige que la prueba correspondiente pase a FAIL
(si no, la batería no detectaría esa clase de defecto). Nunca modifica el árbol real.
Uso: python3 -I v21_controles_negativos.py <raíz del repositorio> """
import os, re, shutil, subprocess, sys, tempfile
RAIZ = os.path.abspath(sys.argv[1]); F0 = "docs/fase0"; BAT = F0 + "/expediente_final_v21/scripts/v21_bateria_cierre.py"
def rd(p): return open(p, encoding="utf-8", newline="").read()
def wr(p, t): open(p, "w", encoding="utf-8", newline="").write(t)
def sub(p, a, b, count=1):
    t = rd(p); assert a in t, "no se encontró %r en %s" % (a[:50], p); wr(p, t.replace(a, b, count))
E20 = F0 + "/expediente_final_v16_v19"; E21 = F0 + "/expediente_final_v21"
def csv_edit(p, fn):
    L = rd(p).split("\n"); L = fn(L); wr(p, "\n".join(L))
M = []
def m(nid, desc, esperado, fn): M.append((nid, desc, esperado, fn))
m("N00", "SIN defecto (línea base): ninguna prueba que no dependa de la verificación de integridad debe fallar", "(ninguna)", lambda c: None)
def _n01(c):
    import csv, io
    p = c + "/" + E20 + "/MATRIZ_FINAL_231_REGLAS_V16_V19.csv"; raw = rd(p)
    rows = list(csv.reader(io.StringIO(raw, newline="")))
    for r in rows[1:]:
        if r[6] == "C": r[6] = "B"; break
    o = io.StringIO(newline=""); csv.writer(o, lineterminator="\n").writerows(rows); wr(p, o.getvalue())
m("N01", "una regla C pasa a B en la matriz", "V21-A02", _n01)
m("N02", "el inventario recupera la distribución antigua (3 B, 5 E)", "V21-E02", lambda c: sub(c + "/" + E20 + "/INVENTARIO_DECISIONES_ABIERTAS_FASE0.md", "A 1, B 8, C 69, D 153, E 0 (derivada", "A 1, B 3, C 69, D 153, E 5 (derivada"))
m("N03", "la línea de definición de una regla se desplaza +1", "V21-F01", lambda c: csv_edit(c + "/" + E20 + "/MATRIZ_FINAL_231_REGLAS_V16_V19.csv", lambda L: [re.sub(r"(,)(\d{3,4})(,[^,]*,[ABCE],)", lambda mm: mm.group(1) + str(int(mm.group(2)) + 1) + mm.group(3), l, count=1) if i == 40 else l for i, l in enumerate(L)]))
m("N04", "la línea de un escenario se desplaza", "V21-F02", lambda c: csv_edit(c + "/" + E20 + "/MATRIZ_FINAL_780_ESCENARIOS_V16_V19.csv", lambda L: [re.sub(r"(,)(3[0-9]{3,4}|4[0-9]{3})(,)", lambda mm: mm.group(1) + str(int(mm.group(2)) + 3) + mm.group(3), l, count=1) if i == 20 else l for i, l in enumerate(L)]))
m("N05", "se elimina un par de la trazabilidad", "V21-A07", lambda c: csv_edit(c + "/" + E20 + "/MATRIZ_TRAZABILIDAD_REGLAS_ESCENARIOS_V16_V19.csv", lambda L: L[:100] + L[101:]))
m("N06", "se duplica un caso del registro de las 22 funciones", "V21-B01", lambda c: csv_edit(c + "/" + E20 + "/REGISTRO_CASOS_22_FUNCIONES_V20.csv", lambda L: L[:50] + [L[49]] + L[50:]))
m("N07", "un caso del registro pasa a FAIL", "V21-B01", lambda c: csv_edit(c + "/" + E20 + "/REGISTRO_CASOS_22_FUNCIONES_V20.csv", lambda L: [l.replace(",PASS,", ",FAIL,", 1) if i == 30 else l for i, l in enumerate(L)]))
m("N08", "se altera una línea de la tercera corrida de las 22 funciones", "V21-B03", lambda c: sub(c + "/" + E21 + "/salidas/salida_22_funciones_V21_corrida3.txt", "pruebas_guarda | 01 | esperado=True | obtenido=True", "pruebas_guarda | 01 | esperado=True | obtenido=False"))
m("N09", "una prueba PostgreSQL pasa a FAIL en la corrida 3", "V21-C01", lambda c: sub(c + "/" + E21 + "/salidas/salida_PE_V21_corrida3.txt", "| PASS | ", "| FAIL | "))
m("N10", "se elimina una mutación de mutaciones.sh", "V21-C02", lambda c: csv_edit(c + "/" + E20 + "/PE_POSTGRESQL_V20/mutaciones.sh", lambda L: [l for l in L if not l.startswith("m PG-CF-12 ")]))
m("N11", "el informe V21 declara aceptado el diseño", "V21-E05", lambda c: wr(c + "/" + E21 + "/REGISTRO_CAMBIOS_V20_V21.md", rd(c + "/" + E21 + "/REGISTRO_CAMBIOS_V20_V21.md") + "\nG-1, G-5 y G-10 fueron aceptados por el propietario.\n"))
m("N12", "se modifica un byte del motor", "V21-G05", lambda c: wr(c + "/" + F0 + "/herramientas/modelo_estructural.py", rd(c + "/" + F0 + "/herramientas/modelo_estructural.py") + "\n#\n"))
m("N13", "se añade un archivo fuera de docs/fase0", "V21-G04", lambda c: wr(c + "/app_nueva.py", "print(1)\n"))
m("N14", "se altera un archivo histórico", "V21-G07", lambda c: wr(c + "/" + F0 + "/historico/" + sorted(os.listdir(c + "/" + F0 + "/historico"))[0], rd(c + "/" + F0 + "/historico/" + sorted(os.listdir(c + "/" + F0 + "/historico"))[0]) + "x\n"))
m("N15", "se reescribe la línea 126 (PO-05) del registro", "V21-E07", lambda c: sub(c + "/" + F0 + "/REGISTRO_HISTORICO_VERSIONES.md", "Aceptación formal del addendum v3", "Aceptación formal del addendum v9"))
m("N16", "una decisión abierta pasa a APROBADA", "V21-E06", lambda c: wr(c + "/" + E21 + "/REGISTRO_DECISIONES_ABIERTAS_V21.md", rd(c + "/" + E21 + "/REGISTRO_DECISIONES_ABIERTAS_V21.md") + "\n| DG-09 | retención | spec | APROBADA | x | y |\n"))
m("N17", "aparece un archivo sin entrada en el índice de vigencia", "V21-G01", lambda c: wr(c + "/" + F0 + "/expediente_final_v21/archivo_no_indexado.md", "x\n"))
m("N18", "una referencia a un archivo inexistente en un documento vigente", "V21-F05", lambda c: wr(c + "/" + E21 + "/MATRIZ_CONCILIACION_V21.md", rd(c + "/" + E21 + "/MATRIZ_CONCILIACION_V21.md") + "\nVer `NO_EXISTE_ESTE_ARCHIVO.md`.\n"))
m("N19", "un entregable V21 con versión equivocada", "V21-F06", lambda c: sub(c + "/" + E21 + "/REGISTRO_DECISIONES_ABIERTAS_V21.md", "**Versión:** V21", "**Versión:** V20"))
m("N20", "un documento sustituido pierde su aviso", "V21-G02", lambda c: sub(c + "/" + E20 + "/INFORME_FINAL_V20.md", "> **Superseded (V21, 2026-11-20):**", "> Nota (V21, 2026-11-20):"))
m("N21", "main se mueve en el repositorio", "V21-G08", lambda c: subprocess.run(["git", "branch", "-f", "main", "HEAD"], cwd=c, check=True, capture_output=True))
m("N22", "se modifica una línea de diseño de la especificación", "V21-E08", lambda c: sub(c + "/" + F0 + "/ESPECIFICACION_TECNICA_G1_G5_G10.md", "# ", "#  ", 1))
m("N23", "la ancla de una cita de línea deja de coincidir", "V21-F04", lambda c: sub(c + "/" + E21 + "/ANCLAS_LINEAS_V21.csv", "Decisiones DG-01 a DG-16", "Decisiones DG-01 a DG-99"))
m("N24", "se recorta la tabla de 14 tablas nuevas en la especificación (línea 38)", "V21-A09", lambda c: sub(c + "/" + F0 + "/ESPECIFICACION_TECNICA_G1_G5_G10.md", "las cuatro tablas de cambio y atribución por campo material y ", ""))
m("N25", "el bloque de estado de un documento activo vuelve a decir «sin commit»", "V21-E03", lambda c: sub(c + "/" + F0 + "/ROADMAP_Y_TRAZABILIDAD_G1_G5_G10.md", "Sin pull request ni merge. |", "El trabajo está sin commit. Sin pull request ni merge. |"))
n_ok = 0; n = 0
for nid, desc, esperado, fn in M:
    tmp = tempfile.mkdtemp(prefix="v21ctl_"); c = os.path.join(tmp, "r")
    try:
        shutil.copytree(RAIZ, c, symlinks=True)
        for ph in ("MANIFIESTO_EVIDENCIAS_SHA256_V21.txt", "salida_controles_negativos_V21.txt", "salida_integridad_V21_corrida1.txt", "salida_integridad_V21_corrida2.txt"):  # salidas que esta misma verificación produce: marcadores vacíos SOLO en la copia
            pp = os.path.join(c, E21, ph if ph.startswith("MANIF") else "salidas/" + ph)
            if not os.path.exists(pp): wr(pp, "")
        try: fn(c)
        except Exception as e: print("%s | NO APLICADA (%s) | %s | ERROR DEL ARNÉS" % (nid, desc, e)); n += 1; continue
        r = subprocess.run([sys.executable, "-I", os.path.join(c, BAT), os.path.join(c, F0)], capture_output=True, text=True, cwd=c, env=dict(os.environ))
        fallan = sorted(set(re.findall(r"^(V21-[A-Z]\d+) \| FAIL", r.stdout, re.M))); n += 1
        det = (esperado in fallan) if esperado != "(ninguna)" else not fallan; n_ok += det
        print("%s | %s | espera que falle %s | fallan=%s | %s" % (nid, desc, esperado, fallan, "DETECTADA" if det else "NO DETECTADA"))
    finally: shutil.rmtree(tmp, ignore_errors=True)
print("TOTAL controles negativos=%d DETECTADOS=%d" % (n, n_ok)); sys.exit(0 if n == n_ok else 1)
