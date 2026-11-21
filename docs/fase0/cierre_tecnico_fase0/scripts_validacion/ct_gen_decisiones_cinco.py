#!/usr/bin/env python3
# Uso: python3 -I -B ct_gen_decisiones_cinco.py <dir_cierre>. Inserta/actualiza (idempotente) en INFORME_DECISIONES_ARQUITECTONICAS.md la tabla que separa 5 elementos por decisión.
import csv, os, re, sys
c = sys.argv[1]; dec = list(csv.DictReader(open(os.path.join(c, "REGISTRO_DECISIONES_RECOMENDADAS.csv"), encoding="utf-8")))
NO_DISP = {  # datos no disponibles: sólo lo ya establecido en MATRIZ_LIMITACIONES_RESIDUALES.csv
 "DG-19": "catálogo real de canales/formatos (LR-14)", "DG-09": "política de retención (LR-15)", "DEP-RET-01": "procedimiento de retiro externo y responsable (LR-15)",
 "OD-13": "texto de OD-13 (LR-16)", "PO-05": "texto de la Adenda v9 (LR-16)", "HV-02": "confirmación de que PO-05 se refiere a la v9 (LR-17)",
 "RP-01": "nombres reales de responsables (LR-19)", "P-04": "nombres reales de responsables (LR-19)", "P-05": "nombres reales de responsables (LR-19)",
 "P-01": "organización/proyectos Supabase (LR-20)", "P-02": "infraestructura (LR-20)", "P-03": "infraestructura (LR-20)", "P-10": "infraestructura (LR-20)",
 "DG-16": "umbrales no aprobados (30/10) como valores definitivos"}
def corto(t, n=160): t = re.sub(r"\s+", " ", t).strip(); return t if len(t) <= n else t[:n - 1] + "…"
L = ["## 0. Separación de los cinco elementos por decisión", "",
     "Fuente: `REGISTRO_DECISIONES_RECOMENDADAS.csv`. *CCI-DEV* = si la evidencia necesaria incluye validación en el esquema/entorno físico. Ninguna decisión está aprobada.", "",
     "| ID | 1. Recomendación técnica | 2. Decisión del propietario | 3. Evidencia necesaria | 4. Dependencia de CCI-DEV | 5. Datos no disponibles |", "|---|---|---|---|---|---|"]
for d in dec:
    ev = d["Pruebas_necesarias"]; dev = "Sí" if re.search(r"CCI-DEV|físic|real", ev, re.I) else "No identificada en el registro"
    L.append("| %s | %s | %s | %s | %s | %s |" % (d["ID"], corto(d["Recomendacion_tecnica"]).replace("|", "/"), corto(d["Decision_requerida_del_propietario"]).replace("|", "/"), corto(ev).replace("|", "/"), dev, NO_DISP.get(d["ID"], "ninguno identificado")))
L += ["", "No se inventan política de retención, responsables reales, infraestructura, catálogo real, umbrales no aprobados ni el contenido de la Adenda v9/OD-13; si el texto fuente no está disponible, se declara.", ""]
p = os.path.join(c, "INFORME_DECISIONES_ARQUITECTONICAS.md"); s = open(p, encoding="utf-8").read()
s = re.sub(r"## 0\. Separación de los cinco elementos por decisión.*?(?=\n## G-1 )", "", s, flags=re.S)
s = s.replace("\n## G-1 ", "\n" + "\n".join(L) + "\n## G-1 ", 1)
open(p, "w", encoding="utf-8").write(s); print("ok", len(dec))
