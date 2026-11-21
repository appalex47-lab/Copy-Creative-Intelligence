#!/usr/bin/env python3
# Uso: python3 -I -B ct_t409_t422_correspondencia.py <dir_resultados> <salida.csv>
# Une (a) la ejecución de las 25 mutaciones K47 mapeadas (k47_por_escenario.csv) con (b) las 26 variantes individuales (t409_t422_individual.csv)
# y asigna un NIVEL de correspondencia por escenario. NO convierte inferencias en demostraciones.
import csv, os, re, sys
R, out = sys.argv[1], sys.argv[2]
k = list(csv.DictReader(open(os.path.join(R, "k47_por_escenario.csv"), encoding="utf-8"))); v = list(csv.DictReader(open(os.path.join(R, "t409_t422_individual.csv"), encoding="utf-8")))
inv = lambda s: set(re.findall(r"I\d+", s))
rows = []
for esc in sorted({x["Escenario"] for x in k} | {x["Escenario"] for x in v}, key=lambda e: int(e[2:])):
    ks = [x for x in k if x["Escenario"] == esc]; vs = [x for x in v if x["Escenario"] == esc]
    det_m = set().union(*[inv(x["Observacion"].split("·")[0]) for x in ks]) if ks else set()
    esp_v = {x["Invariante_esperado"] for x in vs}; obs_v = set().union(*[inv(x["Invariantes_observados"]) for x in vs]) if vs else set()
    nivel_c = "NO ESTABLECIDA (sin mutación K47 mapeada o sin variante individual)" if not (ks and vs) else (
        "INFERIDA con COINCIDENCIA EMPÍRICA DE INVARIANTE (la mutación K47-M y la variante individual son detectadas por la misma invariante; no se demuestra que sean la misma operación)" if esp_v & det_m else
        "INFERIDA sin coincidencia de invariante (las ejecuciones se detectan por invariantes distintas)")
    rows.append({"Escenario": esc, "Mutaciones_K47_mapeadas": ";".join(x["Mutacion"] for x in ks) or "—", "K47_ejecutada_detectada": ";".join(sorted({x["Resultado"] for x in ks})) or "—",
        "Invariantes_detectoras_K47": ",".join(sorted(det_m)) or "—", "Variantes_individuales_ejecutadas": len(vs), "Variantes_detectadas": sum(x["Resultado"] == "DETECTADA" for x in vs),
        "Invariantes_esperadas_variante": ",".join(sorted(esp_v)) or "—", "Invariantes_observadas_variante": ",".join(sorted(obs_v)) or "—",
        "Nivel_regla_a_K47M": "DEMOSTRADA (AUDITORIA_FINAL_G1_G5_G10.md l.356–391: M01..M36 → IG5-97)", "Nivel_escenario_a_tabla_C_D": "DEMOSTRADA por el texto del escenario y ejecutada individualmente (en memoria)" if vs else "NO ESTABLECIDA",
        "Nivel_escenario_a_mutacion_K47M": nivel_c, "Evidencia_fisica_que_falta": "Equivalente físico del K47 y de las tablas C/D en CCI-DEV (E8): no existe en este alcance"})
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, list(rows[0])); w.writeheader(); w.writerows(rows)
print(len(rows), sum(1 for r in rows if r["Nivel_escenario_a_mutacion_K47M"].startswith("INFERIDA con")), "con coincidencia;", sum(1 for r in rows if r["Nivel_escenario_a_mutacion_K47M"].startswith("NO")), "no establecidas")
# --- anexo en EXPEDIENTE_T409_T422.md (idempotente) ---
md = os.path.join(R, "..", "..", "EXPEDIENTE_T409_T422.md")
if os.path.exists(md):
    s = open(md, encoding="utf-8").read(); mk = "<!-- ANEXO_CORRESPONDENCIA -->"
    if mk in s: s = s[:s.index(mk)].rstrip() + "\n"
    A = [mk, "", "## Anexo: niveles de correspondencia ejecutados (corrección final)", "",
         "Generado por `scripts_validacion/ct_t409_t422_correspondencia.py` (une `k47_por_escenario.csv` y `t409_t422_individual.csv`; salida `resultados/t409_t422_correspondencia.csv`).", "",
         "| Escenario | K47-M mapeadas | Invariantes que detectan las K47-M | Variantes individuales (detectadas) | Invariante esperada / observada (variantes) | Nivel escenario→mutación K47-M |", "|---|---|---|---|---|---|"]
    for r in rows: A.append("| %s | %s | %s | %s (%s) | %s / %s | %s |" % (r["Escenario"], r["Mutaciones_K47_mapeadas"], r["Invariantes_detectoras_K47"], r["Variantes_individuales_ejecutadas"], r["Variantes_detectadas"], r["Invariantes_esperadas_variante"], r["Invariantes_observadas_variante"], r["Nivel_escenario_a_mutacion_K47M"].split(" (")[0]))
    A += ["", "**Lectura.** Regla→K47-M: DEMOSTRADA (tabla de AUDITORIA_FINAL). Escenario→alteración de la tabla C/D: DEMOSTRADA por el texto y ejecutada individualmente (26 variantes, en memoria). Escenario→K47-Mxx concreta: **INFERIDA**; la coincidencia de invariante es evidencia empírica adicional, **no** demostración de identidad de operación. Falta el equivalente físico (K47 y tablas C/D en CCI-DEV, etapa E8).", "",
          "**Reproducibilidad.** `ct_t409_t422_individual.py` se ejecuta dos veces en la batería final y las salidas deben ser idénticas byte a byte (`resultados/bateria_final/INDICE_BATERIA.csv`, columna `sha256_salida`; control `repro_t409` en el informe de pruebas finales)."]
    open(md, "w", encoding="utf-8").write(s.rstrip() + "\n\n" + "\n".join(A) + "\n")
