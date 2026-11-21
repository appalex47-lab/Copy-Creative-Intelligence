#!/usr/bin/env python3
# Revisión ESTÁTICA (sólo lectura) de T-47 y T-124 sobre los documentos fuente. Uso: python3 -I -B ct_revision_estatica_T47_T124.py <directorio_arbol_original_docs_fase0>
import re, sys, os
d = sys.argv[1]; docs = ["ESPECIFICACION_TECNICA_G1_G5_G10.md", "ROADMAP_Y_TRAZABILIDAD_G1_G5_G10.md", "AUDITORIA_FINAL_G1_G5_G10.md", "INFORME_CIERRE_G1_G5_G10.md"]
L = {n: open(os.path.join(d, n), encoding="utf-8").read().split("\n") for n in docs}
R = []
def t(i, desc, ok, det=""): R.append((i, desc, "PASS" if ok else "FAIL", det))
# ---------- T-124 (DG-16): menciones a los umbrales 30 y 10 caracteres en los cuatro documentos
pat = re.compile(r"(\b30\b|\b10\b)\s*caracteres|char_length\s*\([^)]*\)\s*>=\s*(30|10)", re.I)
ok_words = re.compile(r"propuesta|pendiente|no es restricción|sin carácter obligatorio|no hay CHECK|DG-16|T-03|retiraron|no se impone|no obligatori|no aprobad", re.I)
menciones = {n: [(i + 1, l) for i, l in enumerate(L[n]) if pat.search(l)] for n in docs}
for n in docs:
    ms = menciones[n]; malas = [(i, l[:140]) for i, l in ms if not ok_words.search(l)]
    refs = sum(1 for l in L[n] if re.search(r"DG-16|umbral", l, re.I))
    if not ms: R.append(("T124-" + n[:4], "%s: 0 menciones a los umbrales 30/10 caracteres (%d líneas con DG-16/umbral): no hay contradicción, pero tampoco contraste" % (n, refs), "SIN_DATOS", ""))
    else: t("T124-" + n[:4], "%s: %d menciones a los umbrales; todas con calificador de propuesta/pendiente" % (n, len(ms)), len(malas) == 0, "sin calificador: %s" % malas[:3] if malas else "")
check_activos = [(n, i, l[:140]) for n in docs for i, l in menciones[n] if re.search(r"\bCHECK\b", l) and re.search(r"char_length", l) and not re.search(r"no |sin |retir|propuest|pendiente", l, re.I)]
t("T124-CHECK", "ningún documento presenta un CHECK de longitud mínima 30/10 como vigente", not check_activos, str(check_activos[:3]))
sp = "\n".join(L[docs[0]])
t("T124-IP05", "IP-05 y IG5-09 de la especificación declaran el umbral como propuesta pendiente de T-03/DG-16", bool(re.search(r"\| IP-05 \|[^\n]*propuestas pendientes de T-03", sp)) and bool(re.search(r"\| IG5-09 \|[^\n]*propuesta pendiente de T-03", sp)))
t("T124-DG16", "la tabla de decisiones marca DG-16 como DIFERIDA y 'propuestas, no aprobadas'", bool(re.search(r"\| DG-16 \|[^\n]*DIFERIDA[^\n]*no aprobadas", sp)))
# ---------- T-47: 17 claves, 13 transiciones, 27 tablas, sin cambios
cl = [l for l in L[docs[0]] if re.search(r"17 claves", l)]; tr = [l for l in L[docs[0]] if re.search(r"13 transiciones", l)]
t("T47-17", "la especificación afirma 17 claves físicas sin cambio (%d líneas) y ninguna afirma otro número" % len(cl), len(cl) >= 5 and not any(re.search(r"\b(16|18|19|20) claves", l) for l in L[docs[0]]))
t("T47-13", "la especificación afirma 13 transiciones de T-02 sin cambio (%d líneas) y ninguna afirma otro número" % len(tr), len(tr) >= 5 and not any(re.search(r"\b(12|14|15) transiciones", l) for l in L[docs[0]]))
t("T47-RP", "role_permissions figura como «Sin cambio» en la tabla de ampliaciones", any(re.search(r"\| role_permissions \|[^|]*\| Sin cambio \|", l) for l in L[docs[0]]))
nueva = [(i + 1, l[:140]) for i, l in enumerate(L[docs[0]]) if re.search(r"(clave 18|decimoctava clave|transición 14|nueva transición)", l, re.I) and not re.search(r"no |sin |ninguna|sin crear", l, re.I)]
t("T47-NEG", "no hay una afirmación positiva de clave 18 ni transición 14 (sólo negaciones)", not nueva, str(nueva[:3]))
t("T47-27", "27 tablas base + 14 nuevas = 41 (declarado en la matriz del modelo)", bool(re.search(r"27 tablas", sp)) and bool(re.search(r"14 tablas nuevas|Catorce tablas|catorce tablas", sp)))
LIM = "La revisión es de coherencia TEXTUAL entre documentos; no comprueba una base de datos ni que los CHECK/permisos físicos existan."
for r in R: print(" | ".join(r))
print("TOTAL=%d PASS=%d FAIL=%d SIN_DATOS=%d" % (len(R), sum(r[2] == "PASS" for r in R), sum(r[2] == "FAIL" for r in R), sum(r[2] == "SIN_DATOS" for r in R))); print("LÍMITE:", LIM)
