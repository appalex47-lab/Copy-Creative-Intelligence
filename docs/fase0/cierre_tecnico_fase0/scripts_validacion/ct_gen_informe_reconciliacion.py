#!/usr/bin/env python3
# Uso: python3 -I -B ct_gen_informe_reconciliacion.py <dir_cierre>. Genera INFORME_RECONCILIACION_INTEGRAL.md desde resultados/reconciliacion_integral.txt.
import os, sys
c = sys.argv[1]; L = open(os.path.join(c, "scripts_validacion", "resultados", "reconciliacion_integral.txt"), encoding="utf-8").read().strip().splitlines()
o = ["# INFORME DE RECONCILIACIÓN INTEGRAL", "", "Generado con `scripts_validacion/ct_reconciliacion_integral.py` (sin base de datos); salida íntegra en `scripts_validacion/resultados/reconciliacion_integral.txt`. Cubre: LEEME, dictamen, informe de cierre, matrices (decisiones, limitaciones, escenarios, trazabilidad), resultados de la batería (índice con hashes), smoke de scripts, T-409..T-422, controles negativos del manifiesto, búsqueda global y nombres de archivo citados.", "",
     "## Resultado", "**%s**" % L[-1], "", "| Estado | Comprobación | Detalle |", "|---|---|---|"]
for l in L[:-1]:
    p = [x.strip().replace("|", "/") for x in l.split(" | ", 2)] + ["", ""]; o.append("| %s | %s | %s |" % tuple(p[:3]))
o += ["", "## Alcance", "La reconciliación comprueba coherencia entre documentos, matrices y salidas; no demuestra corrección funcional ni valida el esquema físico. La coincidencia del manifiesto con el árbol publicado se verifica con `ct_manifiesto.py` (vías A y B), no aquí."]
open(os.path.join(c, "INFORME_RECONCILIACION_INTEGRAL.md"), "w", encoding="utf-8").write("\n".join(o) + "\n")
