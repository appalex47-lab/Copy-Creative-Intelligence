#!/usr/bin/env python3
"""Genera INDICE_VIGENCIA_DOCUMENTAL_V21.md a partir del árbol real (todo archivo bajo docs/fase0/ queda identificado una sola vez).
Las clasificaciones son curadas aquí (reglas explícitas por ruta); un archivo sin regla hace fallar el script, para que ningún archivo quede sin estado.
Uso: python3 -I v21_generar_indice.py <dir docs/fase0>"""
import os, re, subprocess, sys
D = os.path.abspath(sys.argv[1]); G = os.path.abspath(os.path.join(D, "..", ".."))
OUT = os.path.join(D, "expediente_final_v21", "INDICE_VIGENCIA_DOCUMENTAL_V21.md")
def git(*a): return subprocess.run(["git"] + list(a), capture_output=True, text=True, cwd=G).stdout
tocados = {l[len("docs/fase0/"):] for l in (git("diff", "--name-only", "ac84133b776cc73c0cb3416e51e2767039bb5132") + git("ls-files", "--others", "--exclude-standard")).split("\n") if l.startswith("docs/fase0/")}
V21 = "expediente_final_v21/"; V20 = "expediente_final_v16_v19/"; EV = "evidencia_v16/"
# (patrón exacto o prefijo con /, estado, tipo, fuente de verdad, sustituye a, sustituido por, motivo)
R = []
def r(ruta, estado, tipo, fuente, sustituye="—", sustituido="—", motivo=""): R.append((ruta, estado, tipo, fuente, sustituye, sustituido, motivo))
ACT = "Documento activo"
r("ESPECIFICACION_TECNICA_G1_G5_G10.md", "VIGENTE", ACT, "Diseño complementario G-1/G-5/G-10 (revisión v15; **no aceptado**)", "`historico/ESPECIFICACION_…_v*_historica.md`", "—", "Solo se actualizó el bloque de estado final (V21); el diseño no cambió")
r("AUDITORIA_FINAL_G1_G5_G10.md", "VIGENTE", ACT, "Auditoría del diseño (revisión v15)", "`historico/AUDITORIA_FINAL_…_v*_historica.md`", "—", "Bloque de estado V21")
r("INFORME_CIERRE_G1_G5_G10.md", "VIGENTE", ACT, "Informe de cierre del diseño (revisión v15)", "`historico/INFORME_CIERRE_…_v*_historico.md`", "—", "Bloque de estado V21")
r("ROADMAP_Y_TRAZABILIDAD_G1_G5_G10.md", "VIGENTE", ACT, "Hoja de ruta y trazabilidad (revisión v15)", "`historico/ROADMAP_Y_TRAZABILIDAD_…_v*_historico.md`", "—", "Bloque de estado V21")
r("REGISTRO_HISTORICO_VERSIONES.md", "VIGENTE", "Registro histórico y de decisiones", "Historia de versiones y decisiones pendientes (fila PO-05, línea 126: intacta)", "—", "—", "Entrada V21 añadida al final; el resto no se tocó")
r("historico/", "HISTÓRICO", "Versiones anteriores (v3–v14) de los documentos activos", "Cada versión es evidencia de su época; la vigente es el documento activo homólogo", "—", "Documento activo homólogo", "Conservado sin cambios (SHA-256 verificado frente a V20)")
r("herramientas/modelo_estructural.py", "VIGENTE", "Herramienta protegida (22 funciones de ejecución)", "Modelo en memoria; SHA-256 `cc87236a…c52a`", "—", "—", "Sin modificar en V21")
r("herramientas/verificar_expediente.py", "VIGENTE", "Herramienta protegida (verificador)", "Verificador; SHA-256 `1acec85d…035a`", "—", "—", "Sin modificar en V21")
# evidencia_v16
for f in ("AUDITORIA_INTEGRAL_V16.md", "EVIDENCIA_PRUEBAS_INDIVIDUALES_V16.md", "INVENTARIO_HALLAZGOS_Y_CORRECCIONES_V16.md", "MATRIZ_C01_C30_V16.md", "REPORTE_REGRESION_V16.md", "TRAZABILIDAD_V15_V16.md", "VALIDACION_SERVICIOS_EXTERNOS_V16.md"):
    r(EV + f, "HISTÓRICO", "Evidencia de etapa V16", "Su época (V16); sin valor de estado vigente", "—", "`" + V21 + "MATRIZ_CONCILIACION_V21.md` e informes V21", "Aviso HISTÓRICO añadido en V21; contenido sin cambios")
r(EV + "INVENTARIO_22_FUNCIONES_V18.md", "HISTÓRICO", "Inventario V18 de las 22 funciones", "Su época (V18, contaba 363)", "—", "`" + V20 + "MATRIZ_PRUEBAS_22_FUNCIONES_366_CASOS.md`", "Cifra 363 sustituida por 366 (V20); aviso añadido en V21")
r(EV + "MATRIZ_CONSISTENCIA_S1_V18.md", "HISTÓRICO", "Consistencia S1 (14 tablas) V18", "Su época (V18); números de línea de la especificación de entonces", "—", "`" + V20 + "MATRIZ_MODELO_DATOS_FINAL.md`", "Aviso añadido en V21")
r(EV + "MATRIZ_CONSISTENCIA_S1_V18.csv", "EVIDENCIA DERIVADA", "Matriz CSV de las 14 tablas (V18)", "Fuente declarada de `MATRIZ_MODELO_DATOS_FINAL.md`", "—", "—", "Sin cambios")
r(EV + "MATRIZ_ESCENARIOS_V19.csv", "HISTÓRICO", "Matriz de escenarios V19", "Su época (V19)", "—", "`" + V20 + "MATRIZ_FINAL_780_ESCENARIOS_V16_V19.csv`", "Sustituida por la matriz final")
r(EV + "MATRIZ_SEMANTICA_REGLAS_V17.csv", "HISTÓRICO", "Matriz semántica de reglas V17", "Su época (V17)", "—", "`" + V20 + "MATRIZ_FINAL_231_REGLAS_V16_V19.csv`", "Sustituida por la matriz final")
r(EV + "MATRIZ_REFERENCIAS_V16.csv", "EVIDENCIA PRIMARIA", "Matriz de 1148 referencias de versión (H/A/I/U)", "Fuente de las 1148 referencias; recomputada por V21-A10", "—", "—", "Sin cambios; el suplemento V20 añade 32")
r(EV + ".gitattributes", "VIGENTE", "Configuración de formato", "Política de formato de salidas crudas", "—", "—", "Sin cambios")
r(EV + "instrumentar_22_funciones_v18.py", "SUSTITUIDO", "Script de instrumentación V18", "Contaba 363 (no sumaba los 3 positivos de K45)", "—", "`" + EV + "instrumentar_22_funciones_v20.py`", "Conservado como evidencia del origen del 363")
r(EV + "instrumentar_pruebas_individuales.py", "HISTÓRICO", "Script de pruebas individuales V16", "Su época (V16)", "—", "`" + EV + "instrumentar_22_funciones_v20.py`", "Conservado")
for f in ("instrumentar_22_funciones_v20.py", "independencia_auditor_v20.py", "pruebas_estructurales_v20.py"):
    r(EV + f, "VIGENTE", "Script de validación (solo lectura)", "Produce las salidas de V20 reejecutadas en V21", "—", "—", "Sin cambios")
for f in sorted(os.listdir(os.path.join(D, "evidencia_v16"))):
    if f.startswith("salida_"): r(EV + f, "EVIDENCIA PRIMARIA", "Salida cruda de ejecución (histórica)", "La ejecución que registra; no se altera", "—", "—", "Conservada sin cambios")
# expediente V20
r(V20 + "AUDITORIA_FINAL_FASE0_V16_V19.md", "SUSTITUIDO", "Auditoría final V20", "—", "—", "`" + V21 + "AUDITORIA_FINAL_V21.md`", "Cadena V19→V20→V21; aviso en el archivo")
r(V20 + "INFORME_CIERRE_FASE0_V16_V19.md", "SUSTITUIDO", "Informe de cierre V20", "—", "—", "`" + V21 + "INFORME_FINAL_V21.md`", "Cadena V19→V20→V21; aviso en el archivo")
r(V20 + "MATRIZ_FINAL_C01_C30_V16_V19.md", "SUSTITUIDO", "Matriz C01–C30", "—", "—", "`" + V21 + "REPORTE_VALIDACION_INTEGRAL_V21.md` (criterios V21)", "Aviso en el archivo")
r(V20 + "INFORME_FINAL_V20.md", "SUSTITUIDO", "Informe final V20", "—", "`" + V20 + "INFORME_CIERRE_FASE0_V16_V19.md`", "`" + V21 + "INFORME_FINAL_V21.md`", "Aviso V21 añadido; contenido V20 sin cambios")
r(V20 + "MATRIZ_ACEPTACION_V20_C01_C32.md", "SUSTITUIDO", "Criterios C01–C32 (V20)", "—", "`" + V20 + "MATRIZ_FINAL_C01_C30_V16_V19.md`", "`" + V21 + "REPORTE_VALIDACION_INTEGRAL_V21.md`", "Aviso V21 añadido; contenido V20 sin cambios")
r(V20 + "MANIFIESTO_EVIDENCIAS_SHA256.txt", "SUSTITUIDO", "Manifiesto SHA-256 del commit V20", "Describe el árbol de `ac84133`; varios archivos cambiaron después", "—", "`" + V21 + "MANIFIESTO_EVIDENCIAS_SHA256_V21.txt`", "Línea de aviso añadida; hashes V20 sin cambios")
r(V20 + "INVENTARIO_DECISIONES_ABIERTAS_FASE0.md", "VIGENTE", "Inventario de decisiones por familia de reglas (corregido en V21)", "Detalle por familia de reglas D; la fuente de verdad de las decisiones es `" + V21 + "REGISTRO_DECISIONES_ABIERTAS_V21.md`", "—", "—", "Corregida la distribución de clases y DG-20 (D-01, D-02)")
for f in ("MATRIZ_FINAL_231_REGLAS_V16_V19.csv", "MATRIZ_FINAL_780_ESCENARIOS_V16_V19.csv"):
    r(V20 + f, "VIGENTE", "Matriz fuente de verdad (clasificación / escenarios)", "Fuente de verdad de " + ("clases de las 231 reglas" if "231" in f else "los 780 escenarios"), "`evidencia_v16/` matrices V17/V19", "—", "Líneas de la especificación recalculadas en V21 (D-03..D-05)")
r(V20 + "MATRIZ_TRAZABILIDAD_REGLAS_ESCENARIOS_V16_V19.csv", "VIGENTE", "Matriz de trazabilidad", "Fuente de verdad de los 1592 pares regla↔escenario", "—", "—", "Sin cambios; verificada por V21-A07")
r(V20 + "MATRIZ_REFERENCIAS_V20_SUPLEMENTO.csv", "EVIDENCIA DERIVADA", "Suplemento de referencias V20", "32 referencias añadidas en V20", "—", "—", "Sin cambios")
r(V20 + "REGISTRO_CASOS_22_FUNCIONES_V20.csv", "EVIDENCIA DERIVADA", "Registro de los 366 casos", "Derivado de las salidas crudas; verificado contra ellas (V21-B02)", "—", "—", "Sin cambios")
for f, t in (("MATRIZ_HV02_PO05_EVIDENCIA.md", "Evidencia de HV-02 / PO-05 (NO VERIFICABLE sin el propietario)"), ("MATRIZ_MODELO_DATOS_FINAL.md", "Conteo reconciliado de tablas (41)"), ("MATRIZ_PRUEBAS_22_FUNCIONES_366_CASOS.md", "Matriz de pruebas de las 22 funciones"), ("REVISION_FUENTES_FISICAS_K32_K45_K55_V20.md", "Revisión de fuentes físicas"), ("PLAN_VALIDACION_POSTGRESQL_SUPABASE_CCI.md", "Plan de validación (limitación externa)"), ("REPORTE_FORMATO_Y_INTEGRIDAD.md", "Reporte de formato"), ("REPORTE_REGRESION_FINAL.md", "Reporte de regresión V20 (complementado por el reporte V21)")):
    r(V20 + f, "VIGENTE", "Evidencia derivada / informe", t, "—", "—", "Citas de línea corregidas en V21 donde aplicaba")
r(V20 + ".gitattributes", "VIGENTE", "Configuración de formato", "Política de formato de salidas crudas", "—", "—", "Sin cambios")
for f in ("01_fixture.sql", "02_pruebas.sql", "ejecutar.sh", "mutaciones.sh"):
    r(V20 + "PE_POSTGRESQL_V20/" + f, "VIGENTE", "Fixture / script PostgreSQL temporal", "Fixture derivado del diseño; **no** es el esquema físico", "—", "—", "Sin cambios; reejecutado en V21")
r(V20 + "PE_POSTGRESQL_V20/README.md", "VIGENTE", "README del fixture", "Alcance y límites del fixture", "—", "—", "Nombre de archivo corregido (D-10)")
for f in ("salida_PE_V20_corrida1.txt", "salida_PE_V20_corrida2.txt", "salida_PE_V20_mutaciones.txt"):
    r(V20 + "PE_POSTGRESQL_V20/" + f, "EVIDENCIA PRIMARIA", "Salida cruda de ejecución", "La ejecución que registra", "—", "—", "Sin cambios")
r(V20 + "PE_POSTGRESQL_V20/salida_corrida0_arnes_con_2_FAIL_historica.txt", "EVIDENCIA PRIMARIA", "Corrida 0 del arnés (2 FAIL por errores del arnés, corregidos y documentados)", "Historial del arnés; no es el resultado vigente", "—", "`salida_PE_V20_corrida1.txt`", "Conservada como evidencia histórica")
for f in sorted(os.listdir(os.path.join(D, "expediente_final_v16_v19"))):
    if f.startswith("salida_"): r(V20 + f, "EVIDENCIA PRIMARIA", "Salida cruda de ejecución (V20)", "La ejecución que registra", "—", "—", "Sin cambios")
# expediente V21
V21F = {"INFORME_FINAL_V21.md": ("INFORME EJECUTIVO", "Informe final V21", "`" + V20 + "INFORME_FINAL_V20.md`"), "AUDITORIA_FINAL_V21.md": ("INFORME EJECUTIVO", "Auditoría final V21", "`" + V20 + "AUDITORIA_FINAL_FASE0_V16_V19.md`"),
        "MATRIZ_CONCILIACION_V21.md": ("Matriz de conciliación", "Cifras y clases recomputadas desde la evidencia primaria", "—"), "INDICE_VIGENCIA_DOCUMENTAL_V21.md": ("Índice de vigencia", "Este índice (generado por `scripts/v21_generar_indice.py`)", "—"),
        "REGISTRO_DECISIONES_ABIERTAS_V21.md": ("REGISTRO DE DECISIONES", "Decisiones abiertas y limitaciones externas; fuente de verdad", "`" + V20 + "INVENTARIO_DECISIONES_ABIERTAS_FASE0.md` (parcial)"),
        "REPORTE_VALIDACION_INTEGRAL_V21.md": ("Informe de validación", "Resultados de la batería, regresión y criterios V21", "`" + V20 + "MATRIZ_ACEPTACION_V20_C01_C32.md`"), "REGISTRO_CAMBIOS_V20_V21.md": ("Registro de cambios", "Defectos corregidos V20→V21", "—"),
        "MANIFIESTO_EVIDENCIAS_SHA256_V21.txt": ("Manifiesto de integridad", "SHA-256 de todo el árbol (procedimiento en `scripts/v21_manifiesto.py`)", "`" + V20 + "MANIFIESTO_EVIDENCIAS_SHA256.txt`"), "ANCLAS_LINEAS_V21.csv": ("Evidencia derivada", "Citas de línea fijadas a texto verificable", "—")}
for f, (t, fu, sus) in V21F.items(): r(V21 + f, "VIGENTE", t, fu, sus, "—", "Entregable V21")
for f in ("v21_bateria_cierre.py", "v21_controles_negativos.py", "v21_corregir_lineas.py", "v21_manifiesto.py", "v21_generar_indice.py", "v21_generar_reporte.py"):
    if os.path.exists(os.path.join(D, "expediente_final_v21", "scripts", f)): r(V21 + "scripts/" + f, "VIGENTE", "Script de validación V21", "Produce/valida la evidencia V21", "—", "—", "Entregable V21")
r(V21 + "salidas/", "EVIDENCIA PRIMARIA", "Salidas completas de la ejecución V21", "Salidas crudas de las ejecuciones hechas en V21", "—", "—", "Generadas en V21; no se editan")
def clasificar(rel):
    for x in R:
        if x[0] == rel or (x[0].endswith("/") and rel.startswith(x[0])): return x
    return None
real = []
for root, ds, fs in os.walk(D):
    ds[:] = [d for d in ds if d != "__pycache__"]
    for f in fs: real.append(os.path.relpath(os.path.join(root, f), D).replace(os.sep, "/"))
sin = sorted(f for f in real if clasificar(f) is None)
if sin: raise SystemExit("archivos sin clasificar: %s" % sin)
def meta(rel, tipo):
    p = os.path.join(D, rel); ver, fec = "—", None
    if rel.endswith(".md") and os.path.isfile(p):
        m = re.search(r"\*\*Versión:\*\* ([^·\n]+?) ·", open(p, encoding="utf-8").read(2500)); ver = m.group(1).strip() if m else "—"
        m2 = re.search(r"\*\*Fecha:\*\* ([0-9-]+)", open(p, encoding="utf-8").read(2500)); fec = m2.group(1) if m2 else None
    if ver == "—":
        m = re.search(r"[_.-][Vv](\d{1,2})(?=[._])", os.path.basename(rel)); ver = "V" + m.group(1) if m else "—"
    if fec is None:
        fec = git("log", "-1", "--format=%cs", "--", "docs/fase0/" + rel).strip() or "2026-11-20"
    if rel in tocados: fec = "2026-11-20 (editado en V21)"
    return ver, fec
L = ["# ÍNDICE DE VIGENCIA DOCUMENTAL V21", "",
     "**Versión:** V21 · **Fecha:** 2026-11-20 · **Fuente:** árbol real de `docs/fase0/` en la rama `audit/fase0-v19-review` (base V20 `ac84133b776cc73c0cb3416e51e2767039bb5132`), generado por `scripts/v21_generar_indice.py` · **Estado de verificación:** la prueba V21-G01 comprueba que todo archivo del árbol tiene entrada, sin entradas inexistentes ni duplicadas; V21-G02 que cada sustituido o histórico lleva aviso.", "",
     "Estados: **VIGENTE** (fuente actual para lo que cubre), **SUSTITUIDO** (reemplazado por otro documento; no es fuente vigente), **HISTÓRICO** (evidencia de su época; sus cifras o estados pueden diferir de los actuales), **EVIDENCIA PRIMARIA** (salida cruda o fuente original de una cifra; no se edita), **EVIDENCIA DERIVADA** (calculada a partir de la primaria). Las salidas crudas de ejecución son evidencia primaria y se conservan tal como se produjeron aunque correspondan a versiones anteriores: **una cifra que aparezca solo en un documento HISTÓRICO o SUSTITUIDO no es el resultado vigente** (p. ej. 363 casos, 3 B / 5 E, «sin commit», números de línea anteriores a V21).", "",
     "Cadena de sustitución de los informes de cierre: V19 (`INFORME_CIERRE_…`, `AUDITORIA_FINAL_…`, `MATRIZ_FINAL_C01_C30`) → V20 (`INFORME_FINAL_V20`, `MATRIZ_ACEPTACION_V20_C01_C32`) → **V21** (`INFORME_FINAL_V21`, `AUDITORIA_FINAL_V21`, `REPORTE_VALIDACION_INTEGRAL_V21`).", "",
     "| Documento | Estado | Tipo | Versión | Fecha | Fuente de verdad | Sustituye a | Sustituido por | Motivo del cambio |", "|---|---|---|---|---|---|---|---|---|"]
visto = set()
for rel in sorted(real, key=lambda x: x.encode()):
    c = clasificar(rel); key = c[0]
    if c[0].endswith("/"):
        if key in visto: continue
        visto.add(key); ver, fec = "—", "—"; nombre = key
        if key == "historico/": ver, fec = "v3–v14", "2026-11 (conservado)"
        else: ver, fec = "V21", "2026-11-20"
    else:
        ver, fec = meta(rel, c[2]); nombre = rel
    L.append("| `%s` | %s | %s | %s | %s | %s | %s | %s | %s |" % (nombre, c[1], c[2], ver, fec, c[3], c[4], c[5], c[6]))
L += ["", "## Autorreferencia", "Este índice, el manifiesto y las salidas de `salidas/` forman parte del árbol que describen; el manifiesto no contiene su propio hash ni el de las salidas de la verificación de integridad (`salidas/salida_integridad_V21*.txt`), por construcción.", ""]
open(OUT, "w", encoding="utf-8", newline="").write("\n".join(L))
print("índice generado: %d archivos reales, %d filas" % (len(real), len(L) - 12))
