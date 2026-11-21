#!/usr/bin/env python3
# Uso: python3 -I -B ct_gen_decisiones_ext.py <dir_cierre>. Añade (idempotente) al registro columnas derivadas SOLO de campos ya existentes del propio registro:
# Consecuencia_si_se_aprueba, Consecuencia_si_no_se_aprueba, Estado_actual. No agrega hechos nuevos ni aprueba nada.
import csv, os, sys
p = os.path.join(sys.argv[1], "REGISTRO_DECISIONES_RECOMENDADAS.csv"); rows = list(csv.DictReader(open(p, encoding="utf-8")))
NEW = ["Consecuencia_si_se_aprueba", "Consecuencia_si_no_se_aprueba", "Estado_actual"]
cols = [c for c in rows[0] if c not in NEW] + NEW
cut = lambda t, n: " ".join(t.split())[:n] + ("…" if len(" ".join(t.split())) > n else "")
for r in rows:
    r["Consecuencia_si_se_aprueba"] = "Se adopta la recomendación técnica («%s»). Efecto funcional: %s Pruebas que quedan habilitadas: %s" % (cut(r["Recomendacion_tecnica"], 220), cut(r["Impacto_funcional"], 220), cut(r["Pruebas_necesarias"], 200))
    r["Consecuencia_si_no_se_aprueba"] = "El problema permanece abierto: %s Dependencias que siguen bloqueadas o sin base: %s Pruebas que no pueden cerrarse: %s" % (cut(r["Problema"], 220), cut(r["Dependencias"], 160), cut(r["Pruebas_necesarias"], 160))
    r["Estado_actual"] = "%s / %s (ninguna decisión aprobada; no se declara aprobada sin autorización expresa del propietario)" % (r["Estado_tecnico"], r["Estado_aprobacion"])
with open(p, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, cols); w.writeheader(); w.writerows(rows)
print(len(rows), "decisiones;", len(cols), "columnas")
