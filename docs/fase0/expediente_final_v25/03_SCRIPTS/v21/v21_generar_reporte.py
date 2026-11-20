#!/usr/bin/env python3
"""Genera REPORTE_VALIDACION_INTEGRAL_V21.md desde las salidas REALES archivadas (TSV de la batería, salidas del verificador, controles negativos, integridad).
Una prueba sin salida archivada se informa BLOCKED/«no ejecutada»; nunca se rellena. Uso: python3 -I v21_generar_reporte.py <dir docs/fase0>"""
import csv, hashlib, io, os, re, sys
D = os.path.abspath(sys.argv[1]); S = os.path.join(D, "expediente_final_v21", "salidas"); OUT = os.path.join(D, "expediente_final_v21", "REPORTE_VALIDACION_INTEGRAL_V21.md")
def rd(p): return open(p, encoding="utf-8", newline="").read()
def ex(p): return os.path.exists(p)
tsv = list(csv.DictReader(io.StringIO(rd(os.path.join(S, "RESULTADOS_BATERIA_V21.tsv")), newline=""), delimiter="\t"))
est = {r["id"]: r["estado"] for r in tsv}; c = {k: sum(1 for r in tsv if r["estado"] == k) for k in ("PASS", "FAIL", "BLOCKED")}
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def corte(s, n=170): s = s.replace("|", "/").replace("\n", " "); return s if len(s) <= n else s[:n - 1] + "…"
ver = {}
for i in (1, 2):
    p = os.path.join(S, "salida_verificador_V21_corrida%d.txt" % i)
    if ex(p):
        t = rd(p); m = re.search(r"RESUMEN: .*", t); d = re.search(r"DURACION_S=(\d+)", t)
        ver[i] = (m.group(0) if m else "sin RESUMEN", d.group(1) if d else "?", hashlib.sha256("\n".join(l for l in t.split("\n") if not l.startswith("DURACION_S=")).encode()).hexdigest())
neg = rd(os.path.join(S, "salida_controles_negativos_V21.txt")) if ex(os.path.join(S, "salida_controles_negativos_V21.txt")) else ""
mneg = re.search(r"TOTAL controles negativos=(\d+) DETECTADOS=(\d+)", neg)
integ = []
for i in (1, 2):
    p = os.path.join(S, "salida_integridad_V21_corrida%d.txt" % i)
    if ex(p) and re.search(r"RESUMEN INTEGRIDAD V21: .*", rd(p)): integ.append(re.search(r"RESUMEN INTEGRIDAD V21: .*", rd(p)).group(0))
def todos(ids): return all(est.get(i) == "PASS" for i in ids)
crit = [("Clasificaciones", "100% conciliadas", ["V21-A02", "V21-A03", "V21-A04", "V21-E01", "V21-E02"]), ("Conteos", "100% trazables", ["V21-A01", "V21-A05", "V21-A06", "V21-A07", "V21-A08", "V21-A09", "V21-A10", "V21-B01", "V21-B02", "V21-B03", "V21-B04", "V21-B06", "V21-C01", "V21-C02", "V21-C03"]),
        ("Referencias", "Sin referencias rotas", ["V21-F01", "V21-F02", "V21-F03", "V21-F04", "V21-F05", "V21-F06"]), ("Decisiones", "Sin decisiones inventadas", ["V21-E06", "V21-E07", "V21-E08"]),
        ("Estados", "Sin contradicciones", ["V21-E03", "V21-E04", "V21-E05"]), ("Evidencias", "Trazabilidad verificable", ["V21-A07", "V21-B02", "V21-B03", "V21-C03", "V21-G11"]), ("PostgreSQL", "Limitación correctamente documentada", ["V21-C04"]),
        ("Integridad", "SHA-256 verificado", None), ("Documentos históricos", "Identificados", ["V21-G01", "V21-G02"]), ("Regresión documental", "Sin fallos", ["V21-D01", "V21-D02", "V21-B05"]),
        ("Cambios funcionales", "Ninguno", ["V21-G04", "V21-G05", "V21-G06", "V21-G07"]), ("main", "Intacta", ["V21-G08", "V21-G09"])]
L = ["# REPORTE DE VALIDACIÓN INTEGRAL V21", "",
     "**Versión:** V21 · **Fecha:** 2026-11-20 · **Fuente:** salidas archivadas en `salidas/` (`RESULTADOS_BATERIA_V21.tsv`, `salida_bateria_V21_corrida1.txt` y `salida_bateria_V21_corrida2.txt`, `salida_verificador_V21_corrida1.txt` y `salida_verificador_V21_corrida2.txt`, `salida_controles_negativos_V21.txt`, `salida_integridad_V21_corrida1.txt` y `salida_integridad_V21_corrida2.txt`, terceras corridas de las 22 funciones y PostgreSQL) · **Estado de verificación:** cada resultado procede de una ejecución real; una prueba no ejecutada se declara BLOCKED y nunca PASS. Este reporte lo genera `scripts/v21_generar_reporte.py` desde esas salidas.", "",
     "V21 declara el expediente **técnicamente listo para revisión** únicamente si todos los criterios del apartado 3 pasan; no equivale a aceptación del propietario, a validación de infraestructura real ni a autorización de Fase 1.", "",
     "## 1. Resumen", "| Verificación | Resultado | Evidencia |", "|---|---|---|",
     "| Batería de cierre V21 (estructural, semántica, referencias, conteos, vigencia, ausencia de cambios funcionales) | %d pruebas: PASS %d, FAIL %d, BLOCKED %d | `salidas/RESULTADOS_BATERIA_V21.tsv`; dos corridas `salida_bateria_V21_corrida1.txt` y `salida_bateria_V21_corrida2.txt` |" % (len(tsv), c["PASS"], c["FAIL"], c["BLOCKED"])]
for i in (1, 2):
    if i in ver: L.append("| Regresión documental completa, corrida %d (copia limpia, `env -i`, `python3 -I`) | %s; duración %s s; hash sin duración `%s…` | `salidas/salida_verificador_V21_corrida%d.txt` |" % (i, corte(ver[i][0], 220), ver[i][1], ver[i][2][:16], i))
if 1 in ver and 2 in ver: L.append("| Comparación independiente de las dos corridas del verificador | %s | hashes de líneas sin duración |" % ("**idénticas**" if ver[1][2] == ver[2][2] else "**DIFIEREN**"))
L.append("| Controles negativos de la batería (defecto inyectado en copia → la prueba debe fallar) | %s | `salidas/salida_controles_negativos_V21.txt` |" % ("%s de %s detectados" % (mneg.group(2), mneg.group(1)) if mneg else "no ejecutados"))
L.append("| Integridad SHA-256 (manifiesto V21: hashlib + `sha256sum -c` + estructura + regenerable) | %s | `salidas/salida_integridad_V21_corrida1.txt` y `salidas/salida_integridad_V21_corrida2.txt` (fuera del manifiesto por construcción) |" % (" / ".join(integ) if integ else "no ejecutada"))
L += ["", "## 2. Resultado de cada prueba de la batería", "| Identificador | Objetivo | Entrada | Resultado esperado | Resultado obtenido | PASS/FAIL/BLOCKED | Evidencia | Observaciones |", "|---|---|---|---|---|---|---|---|"]
for r in tsv: L.append("| %s | %s | %s | %s | %s | **%s** | %s | %s |" % tuple(corte(r[k], 190 if k == "obtenido" else 130) for k in ("id", "objetivo", "entrada", "esperado", "obtenido", "estado", "evidencia", "observaciones")))
L += ["", "## 3. Criterios de aceptación V21", "| Criterio | Resultado requerido | Pruebas que lo respaldan | Resultado |", "|---|---|---|---|"]
okc = True
for n, req, ids in crit:
    if ids is None: ok = len(integ) == 2 and all("TODO PASS" in x for x in integ); ids_t = "verificación de integridad ×2"
    else: ok = todos(ids); ids_t = ", ".join(i.replace("V21-", "") for i in ids)
    okc &= ok; L.append("| %s | %s | %s | **%s** |" % (n, req, ids_t, "APROBADO" if ok else "NO APROBADO"))
L += ["", "**Dictamen computado: %s.**" % ("todos los criterios V21 aprobados" if okc else "NO todos los criterios aprobados"), "",
      "## 4. Qué no se ejecutó y por qué (limitaciones externas reales)",
      "- Pruebas contra un esquema físico real, RLS, privilegios, concurrencia real, Supabase/Storage y CCI-DEV/CCI-PROD: no existe esquema físico ni están autorizados; no se conectó ningún proyecto.",
      "- Trigger de elegibilidad R1–R9 en PostgreSQL: requiere las 12 tablas que el fixture no incluye.",
      "- HV-02 (PO-05 «v3» frente a Adenda v9): NO VERIFICABLE sin confirmación del propietario.", "",
      "El PostgreSQL temporal **no equivale** al esquema físico aprobado de CCI ni a una validación de Supabase.", ""]
open(OUT, "w", encoding="utf-8", newline="").write("\n".join(L)); print("reporte generado; criterios todos aprobados=%s" % okc)
