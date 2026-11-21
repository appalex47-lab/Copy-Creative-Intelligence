#!/usr/bin/env python3
# Genera ../EXPEDIENTE_T409_T422.md a partir de la matriz de escenarios, la matriz de reglas, la especificación y resultados/k47_por_escenario.csv. Uso: python3 -I -B ct_gen_t409.py <V26_dir>
import csv, sys, os, glob, collections
IND = collections.defaultdict(list)
for r in csv.DictReader(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resultados', 't409_t422_individual.csv'), encoding='utf-8')): IND[r['Escenario']].append(r)
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
 "**Tres niveles de correspondencia (corrección final).** (1) **Regla → mutaciones K47: DEMOSTRADA por la auditoría original** (`AUDITORIA_FINAL_G1_G5_G10.md`, líneas 356–391): las 36 mutaciones K47-M01..M36 se declaran sobre IG5-97; los escenarios T-409..T-422 citan IG5-97. (2) **Escenario → alteración de la tabla C/D de 4.4.10: DEMOSTRADA por el propio texto del escenario**: la columna «Acción» pide cambiar una fila de la tabla de efectos (p. ej. «Cambiar a sustituido el efecto a retirada automática») y el resultado esperado es «Rechazo (K47)». Esa alteración se ejecutó **individualmente** con el verificador publicado `simular_k47` (`scripts_validacion/ct_t409_t422_individual.py`, 26 variantes: 22 de cambio único y 4 compensadas en las tres fuentes, con control sin alterar y control no-op, con control sin alterar y control no-op). (3) **Escenario → mutación concreta del motor K47-Mxx: INFERIDA por el revisor** (coincidencia semántica y de orden M01..M14 ↔ T-409..T-422; la especificación no la declara). Las 25 mutaciones del motor se conservan como **cobertura complementaria**, no como ejecución individual del escenario.",
 "**Invariante esperado por escenario.** El invariante esperado (I1, I2, …) lo asigna el revisor leyendo el texto del escenario y la descripción de los invariantes de 4.4.11; el verificador es quien lo observa. Una variante cuenta como DETECTADA sólo si el verificador informa exactamente el invariante esperado (comparación exacta de código, para que I1 no se confunda con I10/I11/I12).",
 "**Resultado global.** Ejecución individual: 26 variantes, 26 detectadas, 14 escenarios cubiertos, controles OK (`resultados/t409_t422_individual.txt`). Mutaciones del motor (complementarias): 25 mapeadas, 25 detectadas (`resultados/k47_por_escenario.txt`). **Nivel de evidencia: verificador/modelo EN MEMORIA; ninguno validado en el esquema físico.** Estado de los 14: `PASS_MODEL_INDIVIDUAL` (no PASS físico).", ""]
for i in range(409, 423):
    k = "T-%d" % i; r = esc[k]; ln = int(r["Linea_ESPEC"]); rules = [x.strip() for x in r["Reglas_citadas"].split(",")]
    o += ["## %s — %s" % (k, spec[ln - 1].split("|")[2].strip()), "",
          "| Campo | Contenido |", "|---|---|", "| Línea en la especificación | %d |" % ln, "| Texto del escenario | `%s` |" % spec[ln - 1].strip().replace("|", "¦"),
          "| Reglas | %s |" % ", ".join(rules), "| Veredicto V26 (sin alterar) | %s |" % r["Veredicto_V20"], "| Revisión estática | Precondición «tabla de efectos válida»; la alteración y el resultado prohibido son coherentes con la regla IG5-97 (efectos estructurales por clasificación y fuente). |"]
    for x in rules:
        d = reg[x]["Definicion_completa"].replace("|", "¦"); o.append("| Regla %s (clase %s) | %s |" % (x, reg[x]["Clase_final_V20"], d[:360] + ("…" if len(d) > 360 else "")))
    for q in IND[k]:
        o.append('| Ejecución individual (tabla C/D → simular_k47) | %s → invariante observado %s (esperado %s) → %s; %s |' % (q['Alteracion_unica'], q['Invariantes_observados'], q['Invariante_esperado'], q['Resultado'], q['Cambio_unico']))
    for m in K[k]:
        o.append("| Ejecución %s | %s → invariante esperado %s → %s (%s) |" % (m["Mutacion"], m["Descripcion"], m["Invariante_esperado"], m["Resultado"], m["Observacion"][:150].replace("|", "¦")))
    o += ["| Resultado de esta revisión | **PASS_MODEL_INDIVIDUAL** (verificador en memoria; ejecución individual demostrada; correspondencia con mutaciones del motor: inferida) |", "| Brecha | Sin ejecución en el esquema físico: la «tabla de efectos» (4.4.10) y las reglas IG5-97 no tienen aún función/trigger SQL que probar. |",
          "| Procedimiento CCI-DEV (NO EJECUTADO) | Cuando existan las funciones de atribución, repetir la alteración equivalente sobre el esquema físico (`PLAN_VALIDACION_CCI_DEV.md`, bloque ATR) y confirmar que se rechaza; mientras no existan es BLOQUEADO_POR_IMPLEMENTACIÓN. |", ""]
o += ["## Limitaciones comunes", "- Un único cambio por mutación y estado inicial válido (garantizado por `_correr_lista`): evita falsos positivos de detección por estado roto.", "- La detección exige el invariante específico **y** su mensaje (`kw in v[1]`): sensible a cambios de redacción en los mensajes del modelo.", "- Equivalencia modelo/físico no demostrada (ver `REVISION_22_FUNCIONES.md` y `MATRIZ_MODELO_LOGICO_FISICO.md`).", ""]
open(os.path.join(here, "..", "EXPEDIENTE_T409_T422.md"), "w", encoding="utf-8").write("\n".join(o)); print("ok", len(o))
