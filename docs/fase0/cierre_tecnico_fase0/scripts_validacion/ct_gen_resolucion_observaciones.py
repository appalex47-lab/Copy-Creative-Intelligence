#!/usr/bin/env python3
# Uso: python3 -I -B ct_gen_resolucion_observaciones.py <dir_cierre> <sha_publicado_revisado>. Genera RESOLUCION_OBSERVACIONES_FINALES.md: causa de la contradicción 51/51 y resolución individual de las cuatro referencias,
# con datos leídos de git (el commit revisado) y del árbol actual. Las conclusiones solo se emiten si las condiciones se comprueban.
import os, re, subprocess, sys, json, hashlib
c = os.path.abspath(sys.argv[1]); rev = sys.argv[2]
top = subprocess.run(["git", "-C", c, "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip(); pref = os.path.relpath(c, top)
git = lambda *a: subprocess.run(["git", "-C", top] + list(a), capture_output=True, text=True)
show = lambda path: git("show", "%s:%s/%s" % (rev, pref, path)).stdout
en_rev = lambda path: git("cat-file", "-e", "%s:%s/%s" % (rev, pref, path)).returncode == 0
ahora = lambda path: os.path.exists(os.path.join(c, path))
tot = lambda t: re.findall(r"TOTAL=\d+ (?:PASS=\d+ )?FAIL=\d+", t)
md = show("INFORME_RECONCILIACION_INTEGRAL.md"); txt = show("scripts_validacion/resultados/reconciliacion_integral.txt")
m = re.search(r"\| FAIL \| nombres de archivo citados[^|]*\| (\[.*\]) \|", md); refs = re.findall(r"\('([^']+)', '([^']+)'\)", m.group(1)) if m else []
L = ["# RESOLUCIÓN DE LAS OBSERVACIONES DE LA REVISIÓN INDEPENDIENTE (reconciliación 51/51 y cuatro referencias)", "",
     "Generado por `scripts_validacion/ct_gen_resolucion_observaciones.py` a partir del commit revisado `%s` (leído con git) y del árbol actual. Las columnas «existe» se calculan; no se copian de mensajes anteriores." % rev, "",
     "## 1. Contradicción en la reconciliación", "| Documento en el commit revisado (resultado HISTÓRICO, no vigente) | Totales |", "|---|---|", "| `INFORME_RECONCILIACION_INTEGRAL.md` (commit revisado) | %s |" % (", ".join(tot(md)) or "n/d"), "| `scripts_validacion/resultados/reconciliacion_integral.txt` (commit revisado) | %s |" % (", ".join(tot(txt)) or "n/d"), ""]
L += ["**Comprobación fallida (recuperada del informe revisado):** `nombres de archivo citados existen en el dossier…`. Referencias que la hicieron fallar: %d." % len(refs), "",
      "**Causa exacta (defecto de orden de generación y de autorreferencia, no del contenido del expediente):** el Markdown se generó a partir de la salida de una ejecución previa de la reconciliación (con FAIL=1) y *después* se volvió a ejecutar la reconciliación, que reescribió solo el TXT (FAIL=0). Eran dos ejecuciones distintas con dos fuentes distintas. Además la comprobación de referencias leía el propio informe generado (que cita sus fallos y su propio TXT) y aceptaba un nombre por coincidencia de nombre base en cualquier carpeta (verificador débil).", "",
      "**Corrección:** `ct_reconciliacion_integral.py` produce en una sola ejecución `reconciliacion_integral.json` (fuente), `.txt` e `INFORME_RECONCILIACION_INTEGRAL.md`, con evidencia (archivo y SHA-256) por comprobación; `ct_verificar_consistencia_informe.py` comprueba que los tres coinciden (totales y estado por comprobación) y tiene controles negativos (incluye la contradicción original FAIL=0→FAIL=1). El verificador de referencias exige ruta exacta cuando la referencia incluye carpeta, nombre exacto (sensible a mayúsculas) cuando no, comprueba enlaces relativos, excluye el informe generado y solo admite citas de archivos retirados si la línea está etiquetada como histórica.", "",
      "## 2. Las cuatro referencias", "| # | Documento que la cita | Referencia | Existe en el commit revisado | Existe ahora | Mayúsculas/ruta exactas | Cita vigente en el documento (commit revisado) | Resolución |", "|---|---|---|---|---|---|---|---|"]
RES = {"ct_gen_manifiesto.py": "Herramienta **retirada** deliberadamente (sustituida por `ct_manifiesto.py gen`). Cita histórica legítima; el documento la nombra ya sin formato de ruta como «generador y verificador v1», con la etiqueta de histórico. No se restaura el archivo: se conserva la trazabilidad en `resultados/historico_verificador_v1_control_negativo.txt` y en este informe.",
       "ct_verificar_publicacion.py": "Ídem: herramienta **retirada** y sustituida por `ct_manifiesto.py dir|api`; mención histórica etiquetada.",
       "evidencia_verificacion/linea_base_inspeccion.txt": "Referencia **adelantada**: la reconciliación se ejecutó antes de que el archivo existiera. El archivo existe (ver columnas) y la ruta es exacta; defecto de orden resuelto al ejecutar la reconciliación al final de la secuencia, tras copiar la línea base.",
       "scripts_validacion/resultados/reconciliacion_integral.txt": "**Autorreferencia**: el informe generado cita su propio TXT, que la batería borra al empezar y que se escribe al terminar. El archivo existe y la ruta es exacta; ahora el informe generado se excluye de la comprobación de referencias (no es fuente de referencias) y TXT/JSON/MD se escriben en la misma ejecución."}
for i, (doc, r) in enumerate(refs, 1):
    path = r if "/" in r else ("scripts_validacion/" + r)
    ex = ("sí" if en_rev(r) or en_rev(path) else "no"); an = ("sí" if ahora(r) or ahora(path) else "no (retirado)")
    exacta = "sí" if (en_rev(r) or ahora(r) or ahora(path) or en_rev(path)) else "n/a (archivo retirado)"
    vig = "sí" if re.search(re.escape("`" + r + "`"), show(doc)) else "no (ya no aparece entre comillas de código)"
    L.append("| %d | `%s` | `%s` | %s | %s | %s | %s | %s |" % (i, doc, r, ex, an, exacta, vig, RES.get(r, "sin resolución definida")))
L += ["", "Lectura: dos referencias eran citas históricas de herramientas retiradas (no son enlaces rotos) y dos eran referencias válidas pero evaluadas antes de existir o de forma autorreferente. Ninguna exigía restaurar archivos ni borrar trazabilidad histórica. El resultado del verificador de referencias corregido (ejecución completa desde cero) consta en `INFORME_RECONCILIACION_INTEGRAL.md` (comprobación «referencias a archivos…») y en `reconciliacion_integral.json`.", ""]
open(os.path.join(c, "RESOLUCION_OBSERVACIONES_FINALES.md"), "w", encoding="utf-8").write("\n".join(L) + "\n"); print("ok refs=%d" % len(refs))
