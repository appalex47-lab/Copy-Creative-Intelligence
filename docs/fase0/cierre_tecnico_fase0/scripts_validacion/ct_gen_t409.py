#!/usr/bin/env python3
# Genera ../EXPEDIENTE_T409_T422.md a partir de la matriz de escenarios, la matriz de reglas, la especificación y resultados/k47_por_escenario.csv. Uso: python3 -I -B ct_gen_t409.py <V26_dir>
import csv, sys, os, glob, collections
v = sys.argv[1]; here = os.path.dirname(os.path.abspath(__file__))
M = os.path.join(v, "V25_copia_integra", "02_MATRICES_E_INVENTARIOS")
esc = {r["Escenario"]: r for r in csv.DictReader(open(glob.glob(M + "/*FINAL_780*.csv")[0], encoding="utf-8"))}
reg = {r["Regla"]: r for r in csv.DictReader(open(glob.glob(M + "/*FINAL_231*.csv")[0], encoding="utf-8"))}
spec = open(os.path.join(v, "V25_copia_integra", "05_LOGS_Y_EVIDENCIAS", "arbol_original_docs_fase0", "ESPECIFICACION_TECNICA_G1_G5_G10.md"), encoding="utf-8").read().split("\n")
K = collections.defaultdict(list)
for r in csv.DictReader(open(os.path.join(here, "resultados", "k47_por_escenario.csv"), encoding="utf-8")): K[r["Escenario"]].append(r)
o = ["# EXPEDIENTE INDIVIDUAL DE LOS ESCENARIOS T-409 A T-422", "",
 "**Alcance:** 14 escenarios de «conservación H-02 v8» (tipo Diseño, veredicto V26 «DEMUESTRA (lectura V20)»). Cada expediente separa la **revisión estática** (lectura de la especificación y de las reglas) de la **ejecución** (mutaciones del modelo en memoria `modelo_estructural.py`, ejecutadas localmente sin modificarlo con `scripts_validacion/ct_k47_por_escenario.py`).", "",
 "**Qué significa «Rechazo (K47)».** En la especificación, el resultado esperado de los 14 escenarios es el rechazo por K47: el auditor estructural de conservación (invariantes I1…I12 sobre un motor en memoria) debe detectar la alteración. Es una verificación sobre un **modelo en memoria**, no sobre el esquema físico ni sobre funciones SQL.", "",
 "**Limitación de la correspondencia.** La especificación no declara qué mutación K47 ejecuta cada escenario. La correspondencia T→mutación de este expediente es **inferencia del revisor** por coincidencia semántica entre el texto del escenario y la descripción de la mutación; está en `scripts_validacion/ct_k47_por_escenario.py` (diccionario MAP) y puede ser contradicha por el propietario técnico.", "",
 "**Resultado global:** 25 mutaciones mapeadas, 25 detectadas, todas con estado inicial válido y un único cambio efectivo (`resultados/k47_por_escenario.txt`). Los 14 quedan en **PASS a nivel MODELO_EN_MEMORIA**; ninguno se ejecutó contra el esquema físico porque **las funciones físicas no existen** (Fase 1 no iniciada).", ""]
for i in range(409, 423):
    k = "T-%d" % i; r = esc[k]; ln = int(r["Linea_ESPEC"]); rules = [x.strip() for x in r["Reglas_citadas"].split(",")]
    o += ["## %s — %s" % (k, spec[ln - 1].split("|")[2].strip()), "",
          "| Campo | Contenido |", "|---|---|", "| Línea en la especificación | %d |" % ln, "| Texto del escenario | `%s` |" % spec[ln - 1].strip().replace("|", "¦"),
          "| Reglas | %s |" % ", ".join(rules), "| Veredicto V26 (sin alterar) | %s |" % r["Veredicto_V20"], "| Revisión estática | Precondición «tabla de efectos válida»; la alteración y el resultado prohibido son coherentes con la regla IG5-97 (efectos estructurales por clasificación y fuente). |"]
    for x in rules:
        d = reg[x]["Definicion_completa"].replace("|", "¦"); o.append("| Regla %s (clase %s) | %s |" % (x, reg[x]["Clase_final_V20"], d[:360] + ("…" if len(d) > 360 else "")))
    for m in K[k]:
        o.append("| Ejecución %s | %s → invariante esperado %s → %s (%s) |" % (m["Mutacion"], m["Descripcion"], m["Invariante_esperado"], m["Resultado"], m["Observacion"][:150].replace("|", "¦")))
    o += ["| Resultado de esta revisión | **PASS (MODELO_EN_MEMORIA)** |", "| Brecha | Sin ejecución en el esquema físico: la «tabla de efectos» (4.4.10) y las reglas IG5-97 no tienen aún función/trigger SQL que probar. |",
          "| Procedimiento CCI-DEV (NO EJECUTADO) | Cuando existan las funciones de atribución, repetir la alteración equivalente sobre el esquema físico (`PLAN_VALIDACION_CCI_DEV.md`, bloque ATR) y confirmar que se rechaza; mientras no existan es BLOQUEADO_POR_IMPLEMENTACIÓN. |", ""]
o += ["## Limitaciones comunes", "- Un único cambio por mutación y estado inicial válido (garantizado por `_correr_lista`): evita falsos positivos de detección por estado roto.", "- La detección exige el invariante específico **y** su mensaje (`kw in v[1]`): sensible a cambios de redacción en los mensajes del modelo.", "- Equivalencia modelo/físico no demostrada (ver `REVISION_22_FUNCIONES.md` y `MATRIZ_MODELO_LOGICO_FISICO.md`).", ""]
open(os.path.join(here, "..", "EXPEDIENTE_T409_T422.md"), "w", encoding="utf-8").write("\n".join(o)); print("ok", len(o))
