#!/usr/bin/env python3
"""Funciones de lectura y evaluación de salidas crudas (V26). Módulo compartido por v26_construir.py y v26_validar.py.
No ejecuta nada contra GitHub: solo interpreta los archivos de salida archivados."""
import re

def rd(p):
    return open(p, encoding="utf-8", newline="").read()

def parse_pass_lines(path):
    """Líneas 'PASS | ...' / 'FAIL | ...' (excluye RESUMEN). Devuelve lista de (estado, texto completo, nº de línea)."""
    out = []
    for n, l in enumerate(rd(path).split("\n"), 1):
        m = re.match(r"(PASS|FAIL) \| (.*)", l)
        if m:
            out.append((m.group(1), m.group(2), n))
    return out

def parse_val25(path):
    """val25: 'PASS | P01 ...' -> {id: (estado, línea)}"""
    d = {}
    for st, txt, n in parse_pass_lines(path):
        m = re.match(r"([PQS]\d\d) ", txt)
        if m:
            d[m.group(1)] = (st, n)
    return d

def lines_by_id(path, pat):
    d = {}
    for n, l in enumerate(rd(path).split("\n"), 1):
        m = re.match(pat, l)
        if m:
            d[m.group(1)] = (l, n)
    return d

C25 = "f235768135175ce3fcd9405a3a4d3a3a68311d3e"
V24END = "b88bde038e331ba67899632ca4e09eebf2cde82d"
V23 = "8674114c69881ff1ebda3c5db1f89f2a4d6d31c6"
V20 = "ac84133b776cc73c0cb3416e51e2767039bb5132"
MAIN = "6a1af2424ef39e0960b8f7e09d4e19ec52e6f046"
H25 = "c3adaf97588ce3b8fef075a44aff6336f4e8c266"

def eval_R(path):
    """R01–R08 (verificaciones remotas de V24): {id: (PASS|FAIL, línea)}"""
    L = lines_by_id(path, r"(R0\d) ")
    r = {}
    def f(i, c): r[i] = ("PASS" if c else "FAIL", L[i][1])
    t = lambda i: L[i][0]
    f("R01", t("R01").endswith(": PASS") and V24END in t("R01"))
    f("R02", "padre=" + V23 in t("R02") and "archivos=257" in t("R02") and "fuera_de_expediente_v24=0" in t("R02"))
    f("R03", ": PASS (641 blobs; truncated=false)" in t("R03"))
    f("R04", "256 OK, 0 discrepancias, entradas=256" in t("R04"))
    m = re.search(r"rama=(\w+) árbol expediente_v23 en V24=(\w+) en V23=(\w+)", t("R05"))
    f("R05", bool(m) and m.group(1) == V23 and m.group(2) == m.group(3))
    f("R06", "V20=" + V20 in t("R06") and "main=" + MAIN in t("R06"))
    f("R07", t("R07").strip().endswith("PRs=0"))
    sizes = re.findall(r"\d+", t("R08").split("accesibles:")[1].split("bytes")[0])
    f("R08", len(sizes) == 5 and all(int(s) > 0 for s in sizes))
    return r

def eval_RV(path):
    """RV01–RV11: {id: (PASS|FAIL, línea)} (RV07 solo si aparece en la salida)."""
    txt = rd(path)
    L = lines_by_id(path, r"(RV\d\d)[ .]")
    r = {}
    def f(i, c): r[i] = ("PASS" if c else "FAIL", L[i][1])
    t = lambda i: L[i][0]
    if "RV01" in L:
        l = t("RV01")
        if "-> PASS" in l or "-> FAIL" in l:
            f("RV01", l.endswith("-> PASS"))
        else:
            m = re.search(r"ls-remote=(\w+) REST=(\w+) esperado=(\w+)", l); f("RV01", bool(m) and m.group(1) == m.group(2) == m.group(3) == C25)
    f("RV02", "padre del commit inicial: " + V24END + " (esperado " + V24END + "); nº de padres=1" in t("RV02"))
    f("RV03", "archivos bajo docs/fase0/expediente_final_v25/ en GitHub=275; árbol remoto = local: SI (916 blobs); truncado=false" in t("RV03"))
    f("RV04", "idéntico al local: SI; entradas=274; existen en el árbol remoto: 274" in t("RV04"))
    f("RV05", "274 OK, 0 discrepancias" in t("RV05"))
    l6 = t("RV06"); f("RV06", "matriz C=18 R=8 PASS=26 de 26" in l6 and "=False" not in l6 and l6.count("=True") == 5)
    f("RV08", "archivos del commit: 275; fuera de docs/fase0/expediente_final_v25/: 0; estados distintos de added: 0" in t("RV08"))
    m = re.search(r"V20=(\w+) V23=(\w+) V24=(\w+) main=(\w+)", t("RV09")); f("RV09", bool(m) and m.groups() == (V20, V23, V24END, MAIN))
    f("RV10", "PRs (todos los estados)=0" in t("RV10") and "ahead_by=7, behind_by=0" in t("RV10"))
    m = re.search(r"commit=(\d+); .*: (\w+) vs (\w+)", t("RV11")); f("RV11", bool(m) and m.group(1) == "0" and m.group(2) == m.group(3))
    m = re.search(r"^RESUMEN RV07: (\d+) comprobaciones, (\d+) PASS, (\d+) FAIL", txt, re.M)
    if m:
        n = [i for i, l in enumerate(txt.split("\n"), 1) if l.startswith("RESUMEN RV07")][0]
        r["RV07"] = ("PASS" if (m.group(3) == "0" and m.group(1) == m.group(2) == "7") else "FAIL", n)
    return r

def eval_W(path):
    L = lines_by_id(path, r"(W0\d) ")
    r = {}
    t = lambda i: L[i][0]
    r["W01"] = ("PASS" if "ls-remote=''" in t("W01") and '"message":"Not Found"' in t("W01") else "FAIL", L["W01"][1])
    r["W02"] = ("PASS" if all(x in t("W02") for x in ["main=" + MAIN, "V20=" + V20, "V23=" + V23, "V24=" + V24END, "V25=" + H25]) else "FAIL", L["W02"][1])
    r["W03"] = ("PASS" if "= árbol local de la base de V26: SI (917 blobs; truncado=false)" in t("W03") and "HEAD local de wt26=" + H25 in t("W03") else "FAIL", L["W03"][1])
    return r

def has_line(path, needle):
    for n, l in enumerate(rd(path).split("\n"), 1):
        if needle in l:
            return n
    return 0
