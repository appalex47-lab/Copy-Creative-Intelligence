#!/usr/bin/env python3
"""Genera matrices y documentos de expediente_final_v26 a partir del registro (cifras idénticas por construcción). Uso: python3 -I v26_construir.py <raiz del worktree>"""
import csv, os, re, subprocess, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v26_evaluar as ev, v26_registro as rg

W = os.path.abspath(sys.argv[1]); X = W + "/docs/fase0/expediente_final_v26"; E = X + "/evidencia_reconstruccion_V26/"
rows, exe = rg.construir_registro(X)
cu, ce, cat = rg.conciliacion(rows, exe)

def wcsv(path, cols, data):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n", extrasaction="ignore"); w.writeheader(); w.writerows(data)
wcsv(X + "/MATRIZ_CONTROLES_V26.csv", rg.COLS, rows)
wcsv(X + "/EJECUCIONES_CONTROLES_V26.csv", rg.ECOLS, exe)
subprocess.run([sys.executable, "-I", E + "v26_mapa_referencias.py", X, X + "/MAPA_REFERENCIAS_V26.csv"], check=True, capture_output=True)
mapa = list(csv.DictReader(open(X + "/MAPA_REFERENCIAS_V26.csv", encoding="utf-8", newline="")))
mc = collections.Counter(r["estado"] for r in mapa)

N = len(rows); NX = len(exe)
BLOQUE = "<!-- CONCILIACION:INICIO -->\n| Concepto | Valor |\n|---|---|\n" + "\n".join("| %s | %d |" % (k, v) for k, v in [
    ("Total de controles únicos", N), ("Total de ejecuciones", NX), ("Controles PASS", cu["PASS"]), ("Controles FAIL", cu["FAIL"]), ("Controles BLOCKED", cu["BLOCKED"]),
    ("Controles NOT VERIFIED", cu["NOT VERIFIED"]), ("Controles PARTIAL", cu["PARTIAL"]), ("Ejecuciones PASS", ce["PASS"]), ("Ejecuciones FAIL", ce["FAIL"]),
    ("Ejecuciones BLOCKED", ce["BLOCKED"]), ("Ejecuciones NOT VERIFIED", ce["NOT VERIFIED"]), ("Ejecuciones PARTIAL", ce["PARTIAL"])]) + "\n<!-- CONCILIACION:FIN -->"

def tabla_cat():
    out = ["| Categoría | Controles únicos | Ejecuciones | PASS | FAIL | BLOCKED | NOT VERIFIED | PARTIAL |", "|---|---|---|---|---|---|---|---|"]
    for c, rs in cat.items():
        ids = {r["ID"] for r in rs}; xs = [x for x in exe if x["ID_control"] in ids]
        out.append("| %s | %d | %d | %d | %d | %d | %d | %d |" % (c, len(rs), len(xs), *[sum(r["Estado"] == s for r in rs) for s in ["PASS", "FAIL", "BLOCKED", "NOT VERIFIED", "PARTIAL"]]))
    return "\n".join(out)

def n_ids(pref, nn=None):
    return sum(1 for r in rows if r["ID"].startswith(pref) and (nn is None or not r["ID"].startswith(nn)))
nC, nR, nP, nQ, nRV, nW, nHT, nL, nS = n_ids("C"), sum(1 for r in rows if re.fullmatch(r"R\d\d", r["ID"])), n_ids("P"), n_ids("Q"), n_ids("RV"), n_ids("W"), n_ids("HT"), n_ids("L"), n_ids("S")
xp = lambda ids: sum(1 for x in exe if x["ID_control"] in ids)
xC = xp({"C%02d" % i for i in range(1, 19)}); xPQ = xp({"P%02d" % i for i in range(1, 15)} | {"Q01", "Q02"}); xRV = xp({"RV%02d" % i for i in range(1, 12)}); xHT = xp({"HT%02d" % i for i in range(1, 11)})
DEFECTOS = [
 ("D01", "RV07: V25 declara 11 verificaciones remotas y solo 10 tienen salida archivada; RV07 estaba definida de forma vaga («el reporte de publicación coincide con el reporte de validación») y el reporte V25 la dejaba «pendiente».",
  "RV07 solo podía ejecutarse con el reporte de publicación ya publicado (segundo commit); su resultado se dio en la respuesta de entrega de V25 y no se archivó la salida. Quedaron únicamente descargas sin comando ni resultado.",
  "Definición precisa (7 comprobaciones RV07.a–RV07.g), script archivado, ejecución contra GitHub en el HEAD c3adaf9 con salida cruda. La corrida 1 dio 6/7 por un defecto de mi propio script (criterio RV07.e con un umbral arbitrario, no del reporte V25); se archiva como ejecución FAIL y la corrida 2, con el script corregido, dio 7/7. La ejecución original de V25 no se cuenta.", "Resuelto"),
 ("D02", "El resumen de resultados del reporte de publicación V25 lista RV01–RV09, omite RV10 y RV11 (cuyas salidas sí están en su bloque E y pasan) y declara RV07 pendiente.", "El resumen se redactó antes de ejecutar RV07 y se copió de una lista incompleta.", "Errata registrada aquí y en la matriz de cambios; el documento histórico se conserva sin alterar (copia byte a byte). RV10 y RV11 constan como PASS con su salida cruda.", "Resuelto (errata)"),
 ("D03", "MATRIZ_CONTROLES_V25.csv solo contiene C01–C18 y R01–R08 (26 filas); no incluye los controles propios de V25 (P01–P14, Q01–Q02, RV01–RV11).", "V25 se centró en conciliar V24.", "MATRIZ_CONTROLES_V26.csv: una fila por control real de V24, V25 y V26, más pruebas técnicas históricas y limitaciones; ejecuciones en EJECUCIONES_CONTROLES_V26.csv.", "Resuelto"),
 ("D04", "«26 PASS» en V25 mezcla 18 controles documentales y 8 verificaciones remotas sin distinguir controles únicos de ejecuciones.", "No había una tabla de conciliación con ambas magnitudes.", "Tabla de conciliación con controles únicos y ejecuciones por estado (§1 del informe de conciliación), idéntica en los documentos V26 (S07).", "Resuelto"),
 ("D05", "Las salidas crudas de las pasadas A y C de V25 y de las verificaciones remotas RV solo estaban embebidas en reportes; no existían como archivos. Además existió una repetición intermedia de la pasada A (A2, salida idéntica) no documentada.", "El flujo de V25 no archivó las salidas intermedias.", "Recuperadas del directorio de trabajo y archivadas en evidencia_reconstruccion_V26/historico_V25_no_archivado/ (copias recuperadas; no estaban en la rama V25) y comparadas con los bloques embebidos (S10). A2 consta como ejecución histórica con esa salvedad.", "Resuelto"),
 ("D06", "LEEME_V25.md afirma que 08_INTEGRIDAD_Y_MANIFIESTOS/SHA256SUMS.txt «ya no verifica en 3 archivos con nota V25».", "Redacción conjunta con el manifiesto V24, sin verificar el SHA256SUMS interno.", "Comprobado: el SHA256SUMS interno verifica 252/252; solo el manifiesto V24 falla, exactamente en 3 archivos. Errata registrada (S02); LEEME_V25 se conserva sin alterar.", "Resuelto (errata)"),
 ("D07", "El expediente V25 no es autónomo: REPORTE_VALIDACION_V25 y los reportes V24 remiten a ../REPORTE_PUBLICACION_V2x_GITHUB.md, que no está dentro del expediente V25.", "Los reportes de publicación se publicaron fuera de la carpeta del expediente.", "V26 incluye V25_publicacion/REPORTE_PUBLICACION_V25_GITHUB.md (copia idéntica al HEAD de V25) y el mapa de referencias resuelve las rutas relativas.", "Resuelto"),
 ("D08", "Los documentos V21 citan archivos con rutas del diseño original (salidas/, scripts/, expediente_final_v21/ y nombres sueltos) que no existen literalmente en el paquete.", "El paquete renombra rutas (08_INTEGRIDAD_Y_MANIFIESTOS/CORRESPONDENCIA_RUTAS_ORIGEN.csv) y los documentos históricos no se reescriben.", "MAPA_REFERENCIAS_V26.csv: %d referencias de los documentos de la copia V25; %s; ninguna sin resolver. Los documentos históricos no se modifican." % (len(mapa), ", ".join("%s=%d" % kv for kv in sorted(mc.items()))), "Resuelto (mapa)"),
 ("D09", "El FAIL esperado de la reproducción V22 (manifiesto V21: «historico/ idénticos al commit V20», dependencia de Git) no figuraba en ninguna matriz de controles.", "Solo constaba en INFORME_VERIFICACION_REPRODUCCION.md.", "Fila HT10 con estado PARTIAL (8 de 9) en la matriz y en la conciliación.", "Resuelto"),
 ("D10", "Dos ejecuciones intermedias del validador V24 (15/16 y 16/16) no tienen salida archivada.", "Solo existieron en la transcripción de la sesión V24.", "No resoluble: la salida no existe. Se registran como declaradas sin evidencia (DECLARACIONES_SIN_EVIDENCIA en el informe de conciliación) y no se cuentan como ejecuciones.", "Limitación documentada"),
 ("D11", "Las verificaciones remotas R01–R08 originales de V24 no tienen salida cruda.", "No se archivó en V24.", "No resoluble históricamente. Re-ejecutadas en V25 y V26 contra GitHub (ejecuciones nuevas, salida cruda archivada); las originales no se cuentan.", "Limitación documentada"),
 ("D12", "El control C05 de V24 es débil (comprueba un subconjunto de los archivos autorizados, no que existan los 4).", "Diseño del validador V24.", "Sin cambio: su existencia queda cubierta por C17/C18. Se registra en la matriz (observaciones de C05).", "Limitación documentada"),
 ("D13", "V25 usa «16 controles» para su validación y «11 verificaciones» sin una cifra consolidada con V24 y con las pruebas técnicas históricas.", "Cifras repartidas en varios documentos.", "Cifra única de V26 con controles únicos (%d) y ejecuciones (%d), generada desde la matriz y comprobada por S07 en todos los documentos." % (N, NX), "Resuelto"),
]

def tdef():
    o = ["| ID | Defecto | Causa | Corrección / tratamiento en V26 | Estado |", "|---|---|---|---|---|"]
    for d in DEFECTOS: o.append("| " + " | ".join(x.replace("|", "/") for x in d) + " |")
    return "\n".join(o)

LIMIT = """- **12 escenarios PARCIAL:** T-03, T-06, T-10, T-47, T-78, T-80, T-124, T-137, T-138, T-139, T-140, T-166 (controles L01).
- **T-409 a T-422** sin ejecución individual propia (L02).
- **22 funciones** validadas indirectamente (sensibilidad a mutaciones e independencia del auditor), no por lectura línea a línea (L03).
- **PostgreSQL temporal:** 63/63 pruebas y 14/14 mutaciones según la evidencia existente (HT05, HT06), sin equivalencia con el esquema físico aprobado (L04).
- **Sin validación física en CCI-DEV** (L05); sin validación real de **RLS, privilegios ni concurrencia** (L06).
- **R1–R9** (trigger de elegibilidad) no ejecutado (L07).
- **HV-02 / PO-05** sin verificación (L08)."""
DECIS = "PO-05, G-1, G-5, G-10, DG-19, DG-20, DG-09, DG-12, DG-16, DG-18, DEP-RET-01, G-9, RP-01, P-01 a P-05, P-10 y OD-13 (detalle en `V25_copia_integra/07_LIMITACIONES_Y_DECISIONES_PENDIENTES/INVENTARIO_DECISIONES_ABIERTAS_FASE0.md`). V26 no convierte ninguna en decisión aprobada."
AVISO = "**V26 no constituye aceptación formal de Fase 0** (corresponde exclusivamente al propietario), no autoriza Fase 1 (NO INICIADA) y no toca Supabase, CCI-DEV ni CCI-PROD."
HDR = "**Fecha:** 2026-11-20 (fecha local, America/Mexico_City; las salidas remotas llevan su sello en UTC) · **Rama:** `audit/fase0-v26-review` · **Base:** `audit/fase0-v25-review`, HEAD de publicación `c3adaf97588ce3b8fef075a44aff6336f4e8c266` (commit del expediente V25 `f235768135175ce3fcd9405a3a4d3a3a68311d3e`)."

def w(name, text):
    open(X + "/" + name, "w", encoding="utf-8", newline="").write(text.rstrip("\n") + "\n")

# ------------------------------------------------------------------ LEEME
w("LEEME_V26.md", f"""# LEEME V26 — Auditoría integral, correcciones y cierre de trazabilidad

{HDR}

{AVISO}

## 1. Relación entre versiones (estado histórico de cada una)
- **V21:** expediente técnico de origen (contenido técnico y documental generado en V21: 231 reglas, 780 escenarios, 22 funciones, verificador, batería, PostgreSQL temporal).
- **V22/V23:** empaquetado en ZIP y corrección documental del paquete (V23 corrigió el comando de verificación del LEEME y regeneró el manifiesto).
- **V24:** corrigió observaciones documentales (identificación de versión, contexto histórico de las afirmaciones, limitaciones en el LEEME).
- **V25:** concilió los controles de V24 (16 vs 18): 18 controles distintos en dos pasadas, más 8 verificaciones remotas aparte.
- **V26:** auditoría integral de V25, resolución de RV07, matriz única de controles, correcciones documentales (por errata y mapas, sin alterar copias históricas) y cierre de trazabilidad.

## 2. Estado histórico frente al estado actual de publicación
Los documentos de V21 a V25 conservados en `V25_copia_integra/` describen **el estado en su fecha** (por ejemplo, «sin commit» en el LEEME V21 es histórico). El **estado actual de publicación** es el de la rama `audit/fase0-v26-review` en GitHub; su verificación remota posterior al push se registra en `REPORTE_PUBLICACION_V26_GITHUB.md`, fuera de este expediente. `V25_copia_integra/` y `V25_publicacion/` son **copias** de los archivos de la rama V25 (no son los originales de esa rama).

## 3. Qué contiene
- `V25_copia_integra/`: copia byte a byte de los 275 archivos de `expediente_final_v25` (rutas `00_…` a `08_…` y documentos V24/V25). Se conserva sin cambios para que sus manifiestos sigan verificando.
- `V25_publicacion/REPORTE_PUBLICACION_V25_GITHUB.md`: copia del reporte de publicación V25 (estaba fuera del expediente V25).
- Documentos V26: `INFORME_AUDITORIA_FINAL_V26.md`, `INFORME_CONCILIACION_CONTROLES_V26.md`, `MATRIZ_CONTROLES_V26.csv`, `EJECUCIONES_CONTROLES_V26.csv`, `MATRIZ_CAMBIOS_V25_V26.md`, `REPORTE_VALIDACION_V26.md`, `REPORTE_VERIFICACION_REMOTA_V26.md`, `MAPA_REFERENCIAS_V26.csv`, `MANIFIESTO_SHA256_V26.txt`.
- `evidencia_reconstruccion_V26/`: scripts, salidas crudas, restos recuperados de V25 y comparaciones para reproducir todo.

## 4. Cifras de conciliación (únicas para todos los documentos V26)
{BLOQUE}

Controles únicos = filas de la matriz. Ejecuciones = corridas con salida cruda archivada (una repetición de un control es una ejecución, no otro control). Las 4 declaraciones sin evidencia (D10, D11 y RV07 de V25) no se cuentan. El detalle por categoría está en el informe de conciliación.

## 5. Integridad
`MANIFIESTO_SHA256_V26.txt` cubre todos los archivos de este directorio **salvo él mismo** (un archivo no puede contener su propio hash). Verificación desde esta carpeta: `sha256sum -c MANIFIESTO_SHA256_V26.txt`. Los manifiestos históricos dentro de `V25_copia_integra/` se conservan: el de V25 verifica 274/274 desde esa carpeta, `08_INTEGRIDAD_Y_MANIFIESTOS/SHA256SUMS.txt` verifica 252/252 y el de V24 falla exactamente en los 3 archivos que V25 anotó (esperado).

## 6. Limitaciones técnicas que permanecen
{LIMIT}

## 7. Decisiones pendientes del propietario
{DECIS}

## 8. Qué no hace V26
No modifica `main`, V20, V23, V24 ni V25; no hay PR, merge ni force push; no cambia código funcional, resultados, clasificaciones ni decisiones; no toca Supabase; no inicia Fase 1.
""")

# ------------------------------------------------------------------ CONCILIACION
sin_ev = "\n".join("| %s | %s | %s | %s |" % t for t in rg.SIN_EVIDENCIA)
w("INFORME_CONCILIACION_CONTROLES_V26.md", f"""# INFORME DE CONCILIACIÓN DE CONTROLES V26

{HDR}

{AVISO}

## 1. Tabla de conciliación (única)
{BLOQUE}

### Por categoría
{tabla_cat()}

## 2. Cómo se cuenta
- **Control único:** una fila de `MATRIZ_CONTROLES_V26.csv` con ID propio. {nC} controles documentales de V24 (C01–C18) + {nP + nQ} de V25 (P01–P14 y Q01–Q02) + {nS} de V26 (S01–S20) = {nC + nP + nQ + nS} controles documentales; verificaciones remotas: {nR} de V24 (R01–R08) + {nRV} de V25 (RV01–RV11) + {nW} previas de V26 (W01–W03) = {nR + nRV + nW}; {nHT} pruebas técnicas históricas (HT01–HT10); {nL} limitaciones declaradas (L01–L08).
- **Ejecución:** una corrida con salida cruda archivada (`EJECUCIONES_CONTROLES_V26.csv`, línea exacta). Repetir un control es una ejecución nueva del mismo control, nunca otro control.
- **Estado de un control:** el de su última ejecución. Los controles L no tienen ejecución propia y conservan el estado declarado (PARTIAL o NOT VERIFIED).
- **Fechas:** fecha local (America/Mexico_City). Las salidas de verificación remota llevan además su sello UTC.

## 3. Reconciliación con las cifras anteriores
| Cifra histórica | Qué era | Dónde está en V26 |
|---|---|---|
| V24 «16» y «18» | Mismo conjunto C01–C18 en dos pasadas (A: C01–C16; C: C01–C18) | C01–C18: 1 control cada uno; ejecuciones: {xC} (A 16 + C 18 + re-ejecución V25 18 + re-ejecución V26 18) |
| V24 «8 verificaciones» | R01–R08 | R01–R08: ejecuciones nuevas V25 y V26 (16); las originales no se cuentan |
| V25 «26 PASS» | 18 C + 8 R de la matriz V25, sin los controles propios de V25 | Reemplazado por la tabla de §1 (D03, D04) |
| V25 «16 controles» | P01–P14 (pasada A) y P01–P14 + Q01–Q02 (pasada C) | P01–Q02: {nP + nQ} controles, {xPQ} ejecuciones (A, A2, C y re-ejecución V26) |
| V25 «11 verificaciones» | RV01–RV11 (10 con salida archivada; RV07 sin ella) | RV01–RV11: {xRV} ejecuciones (original V25 10 + V26 corrida 1 11 + corrida 2 11); RV07 solo en V26 (2 ejecuciones: FAIL por defecto del script y PASS) |
| V21/V22 pruebas técnicas | 59/59, 28/28, 300/300, 366 casos, 63/63, 14/14, 46/46, 26/26, integridad, 8 de 9 | HT01–HT10: {xHT} ejecuciones históricas, sin re-ejecución en V26 |

La diferencia entre los 640 blobs del reporte de publicación V24 y los 641 de la re-ejecución R03 no es contradicción: son dos refs distintas (commit del expediente V24 y HEAD de publicación, que añade un archivo).

## 4. Declaraciones sin evidencia (no cuentan como ejecuciones)
| Versión | Declaración | Dónde consta | Tratamiento |
|---|---|---|---|
{sin_ev}

## 5. Estados no PASS (visibles)
- **FAIL:** ningún control. Hay **una ejecución FAIL** (RV07, corrida 1 de V26, por un defecto del propio script de comprobación), archivada en `evidencia_reconstruccion_V26/reejecucion_V26_RV01_RV11_corrida1_RV07e_FAIL_por_defecto_del_script.txt`.
- **BLOCKED:** ninguno.
- **PARTIAL:** {cu['PARTIAL']} controles (HT10, L01, L02, L03).
- **NOT VERIFIED:** {cu['NOT VERIFIED']} controles (L04–L08).

## 6. Controles posteriores al manifiesto (S19 y S20)
Se ejecutan sobre el paquete definitivo; su salida cruda va en `REPORTE_PUBLICACION_V26_GITHUB.md` (fuera del expediente, porque un archivo no puede contener el hash de sí mismo ni de un manifiesto que lo incluya). Su estado se consigna tras ejecutarlos (punto fijo documentado en el informe de auditoría).
""")

# ------------------------------------------------------------------ AUDITORIA
ntot = len(os.listdir(X))
w("INFORME_AUDITORIA_FINAL_V26.md", f"""# INFORME DE AUDITORÍA FINAL V26

{HDR}

{AVISO}

## 1. Dictamen
V26 audita V25 contra sus evidencias y no contra sus reportes. Resultado: **no hay contradicción de resultados en V25**, pero sí defectos de trazabilidad (§4): RV07 sin salida cruda (resuelto con ejecución nueva, 7/7 PASS tras corregir un defecto de mi propio script), matriz de controles incompleta, errata en LEEME_V25 sobre SHA256SUMS, salidas crudas de V25 solo embebidas, expediente no autónomo y referencias históricas a rutas del diseño original. Todo lo corregible dentro del alcance se corrigió en V26 mediante documentos nuevos; las copias históricas se conservan **sin alterar** (alterarlas rompería sus manifiestos y la regla de no modificar resultados históricos).

{BLOQUE}

Dictamen sobre Fase 0 (documental): el expediente es consistente, reproducible y verificable en lo que afirma; **no es una aceptación técnica**. Las limitaciones de §7 y las decisiones de §8 permanecen abiertas. La aceptación formal de Fase 0 corresponde exclusivamente al propietario.

## 2. Auditoría inicial (antes de modificar archivos)
- HEAD de `audit/fase0-v25-review` en GitHub = `c3adaf97588ce3b8fef075a44aff6336f4e8c266`, padre único `f235768135175ce3fcd9405a3a4d3a3a68311d3e` (commit del expediente V25), cuyo padre es `b88bde038e331ba67899632ca4e09eebf2cde82d` (V24).
- Referencias históricas verificadas en remoto (W02 y RV09): `main` `6a1af2424ef39e0960b8f7e09d4e19ec52e6f046`, V20 `ac84133b776cc73c0cb3416e51e2767039bb5132`, V23 `8674114c69881ff1ebda3c5db1f89f2a4d6d31c6`, V24 `b88bde038e331ba67899632ca4e09eebf2cde82d`, V25 `c3adaf97588ce3b8fef075a44aff6336f4e8c266`. La rama V26 no existía antes de publicar (W01).
- Árbol remoto del HEAD V25 = árbol local (917 blobs, no truncado; W03). Inventario con hashes de la copia V25: los 275 archivos de `V25_copia_integra/` coinciden con la rama V25 (S01) y con su manifiesto (274 entradas, S02).
- Árbol de trabajo limpio: la rama de trabajo parte del HEAD de V25 sin cambios ajenos (S15, S16).

## 3. RV07 (resolución definitiva)
- **Definición exacta:** V25 la describe como «el reporte de publicación coincide con el reporte de validación» y la deja para después del segundo commit. V26 la precisa en 7 comprobaciones (`evidencia_reconstruccion_V26/rv07_comparar_reportes.py`): RV07.a el reporte remoto es idéntico al del commit HEAD; RV07.b ambos declaran 16 controles de validación y 11 verificaciones remotas; RV07.c el bloque A del reporte de validación es la salida cruda de la pasada A; RV07.d el bloque C del reporte de publicación es la salida cruda de la pasada C; RV07.e el bloque E es la salida cruda original de RV01–RV06 y RV08–RV11; RV07.f el commit del expediente citado es el padre del HEAD; RV07.g las etapas A–E coinciden.
- **Evidencia previa:** no existía evidencia válida (solo descargas de los dos reportes a las 16:35 locales, sin comando ni resultado). No se reutilizó nada.
- **Ejecución:** contra GitHub (repositorio `appalex47-lab/Copy-Creative-Intelligence`, rama `audit/fase0-v25-review`, ref `c3adaf97588ce3b8fef075a44aff6336f4e8c266`). Corrida 1: 6/7 (RV07.e FAIL por un criterio arbitrario de mi script, que exigía al menos 5 líneas con ciertas palabras; el bloque era idéntico byte a byte a la salida cruda). Corrida 2, con el criterio eliminado: 7/7 PASS. Ambas salidas están archivadas.
- **Observación:** el resumen del reporte de publicación V25 omite RV10 y RV11 y declara RV07 pendiente (D02); se registra como errata, no es criterio de RV07.
- **Resultado:** RV07 PASS (ejecución nueva V26). Las 11 verificaciones RV01–RV11 tienen ahora once evidencias independientes: RV01–RV06 y RV08–RV11 en la salida original de V25 y en V26; RV07 en V26.

## 4. Defectos encontrados, causas y correcciones
{tdef()}

## 5. Revisión por áreas
**A. Controles documentales V24 (C01–C18).** 18 controles; las dos pasadas históricas (16 + 18) y las dos re-ejecuciones (V25 y V26 sobre V24 publicado, 18/18 con los mismos estados) están archivadas; los bloques embebidos en los reportes V24 coinciden con las salidas crudas (S10). Causa de 16 vs 18: C17 y C18 solo se activan con el manifiesto presente. Intermedias no archivadas: D10.
**B. Controles remotos V24 (R01–R08).** Originales sin salida cruda (D11). Re-ejecuciones V25 y V26 contra GitHub: 8/8 PASS cada una; descargas: 256/256 archivos coinciden con el manifiesto V24.
**C. Controles V25 (P01–P14, Q01–Q02, RV01–RV11).** Re-ejecución de `V25_copia_integra/evidencia_reconstruccion_V25/val25.py` sobre V25 publicado: 16/16, salida idéntica byte a byte a la pasada C histórica. Remotos: RV01–RV11 PASS en V26 (RV01 en variante por el nuevo HEAD). Matriz V25 incompleta (D03); cifras reconciliadas (D04, D13).
**D. Integridad histórica.** Verificado en remoto y local: V23, V24, V25, V20 y `main` conservan sus SHA (W02, RV09, S16). Las evidencias técnicas originales de V25 coinciden byte a byte con su copia (S01). Las notas de conciliación V25 solo insertan una línea: quitándola se recupera cada original V24 (control P05, re-ejecutado en V26). Las copias históricas están identificadas como copias (LEEME_V26 §2).
**E. Revisión semántica.** Referencias a archivos: {len(mapa)} en los documentos de la copia V25, ninguna sin resolver (D08). SHA de commit citados: todos existen y su rol coincide (S09). Fechas: en los documentos de la copia V25 analizados solo aparecen 2026-11-16, 2026-11-19 y 2026-11-20, coherentes con las versiones. Cifras: las apariciones de «16», «18», «26», «11», «8», «256», «274» y «275» corresponden a contextos distintos y quedan reconciliadas (informe de conciliación §3). 640 vs 641 blobs: refs distintas. Declaraciones históricas presentadas como actuales: el LEEME V21 y los reportes anteriores quedan acotados por LEEME_V26 §2. Controles duplicados: ninguno (S14). PASS sin soporte: ninguno (S06).

## 6. Integridad y punto fijo
Manifiesto autónomo `MANIFIESTO_SHA256_V26.txt` (todos los archivos salvo él mismo), verificado por dos métodos (S19 hashlib, S20 `sha256sum -c`) tras preparar el paquete definitivo. La pasada A (S01–S18) y los documentos que embeben sus bloques se generan hasta un **punto fijo**: se ejecuta A en modo preliminar, se embebe, y se vuelve a ejecutar hasta que la salida es idéntica a la embebida. S19 y S20 se consignan como PASS tras ejecutarlos sobre el paquete definitivo; si alguno fallara, se regeneraría el paquete y no se publicaría.

## 7. Limitaciones técnicas que permanecen
{LIMIT}

## 8. Decisiones pendientes del propietario
{DECIS}

## 9. Alcance y límites de esta auditoría (qué no se verificó)
- No se volvieron a ejecutar el verificador (~21 min), la batería V21 ni PostgreSQL; se verifican las salidas archivadas y su coherencia (HT01–HT10, S13).
- No se leyó línea por línea el contenido técnico de los 275 archivos heredados; se verificó su identidad byte a byte con V25 y la coherencia de referencias, cifras y estados.
- No se pueden recuperar las ejecuciones intermedias de V24 ni las salidas originales R01–R08 de V24 (D10, D11).
- Nada de lo que depende de CCI-DEV, Supabase o el esquema físico se simuló.
- La verificación remota posterior al push de V26 se registra fuera del expediente (no puede incluirse en un commit que aún no existe).
""")

# ------------------------------------------------------------------ CAMBIOS
nuevos = ["LEEME_V26.md", "INFORME_AUDITORIA_FINAL_V26.md", "INFORME_CONCILIACION_CONTROLES_V26.md", "MATRIZ_CONTROLES_V26.csv", "EJECUCIONES_CONTROLES_V26.csv", "MATRIZ_CAMBIOS_V25_V26.md",
          "REPORTE_VALIDACION_V26.md", "REPORTE_VERIFICACION_REMOTA_V26.md", "MAPA_REFERENCIAS_V26.csv", "MANIFIESTO_SHA256_V26.txt", "V25_publicacion/REPORTE_PUBLICACION_V25_GITHUB.md"]
ev_files = sorted(os.path.relpath(os.path.join(a, f), X) for a, _, x in os.walk(E) for f in x)
ev_files = [p for p in ev_files if "salida_val26" not in p] + ["evidencia_reconstruccion_V26/salida_val26_pasada_A_previa_manifiesto.txt"]
ev_files = sorted(set(ev_files))
descr = {"historico_V25_no_archivado": "restos de V25 recuperados del directorio de trabajo (no estaban en la rama V25)", "reejecucion_V26": "salida cruda de una ejecución nueva V26", "remoto_": "script de verificación remota", "v26_": "script V26", "rv07": "script RV07", "salida_val26": "salida cruda de la pasada A de V26", "inventario_arbol": "inventario de blobs git del HEAD V25 (API de GitHub)", "inventario_sha256": "inventario SHA-256 de la copia V25", "comparacion_arbol": "comparación árbol remoto vs local de V25"}
def d_(p):
    b = os.path.basename(p)
    for k, v in descr.items():
        if k in p: return v
    return ""
filas = "\n".join("| `%s` | %s |" % (p, d_(p)) for p in ev_files)
w("MATRIZ_CAMBIOS_V25_V26.md", f"""# MATRIZ DE CAMBIOS V25 → V26

{HDR}

{AVISO}

## Resumen
- **Copia íntegra de V25:** los 275 archivos de `expediente_final_v25` están en `V25_copia_integra/` con el mismo contenido byte a byte (0 modificados, 0 ausentes, 0 añadidos dentro de esa carpeta). Su manifiesto V25 verifica 274/274 desde allí.
- **Copia del reporte de publicación V25** (fuera del expediente V25): `V25_publicacion/REPORTE_PUBLICACION_V25_GITHUB.md`, idéntico al HEAD de V25.
- **Documentos históricos con errata:** no se modifican. Las erratas están en el informe de auditoría: `V25_copia_integra/LEEME_V25.md` (D06: SHA256SUMS sí verifica 252/252) y `V25_publicacion/REPORTE_PUBLICACION_V25_GITHUB.md` (D02: resumen sin RV10/RV11 y RV07 pendiente).
- **Fuera de `docs/fase0/expediente_final_v26/`:** solo se añadirá `docs/fase0/REPORTE_PUBLICACION_V26_GITHUB.md` en un segundo commit. Nada más cambia en el repositorio.

## Nuevos en V26
| Archivo | Para qué |
|---|---|
| `LEEME_V26.md` | Relación entre versiones, estado histórico vs actual, integridad, limitaciones |
| `INFORME_AUDITORIA_FINAL_V26.md` | Auditoría, RV07, defectos D01–D13, revisión A–E |
| `INFORME_CONCILIACION_CONTROLES_V26.md` | Tabla de conciliación y reconciliación con cifras históricas |
| `MATRIZ_CONTROLES_V26.csv` | Matriz única: una fila por control ({N}) |
| `EJECUCIONES_CONTROLES_V26.csv` | Una fila por ejecución con salida cruda archivada ({NX}) |
| `MATRIZ_CAMBIOS_V25_V26.md` | Este documento |
| `REPORTE_VALIDACION_V26.md` | Etapas de validación y salida de la pasada A |
| `REPORTE_VERIFICACION_REMOTA_V26.md` | Verificación remota previa a publicar (R01–R08, RV01–RV11, W01–W03) |
| `MAPA_REFERENCIAS_V26.csv` | Resolución de referencias a archivos de los documentos históricos |
| `MANIFIESTO_SHA256_V26.txt` | Manifiesto autónomo (todos los archivos salvo él mismo) |
| `V25_publicacion/REPORTE_PUBLICACION_V25_GITHUB.md` | Copia del reporte de publicación V25 |

## Evidencia nueva (`evidencia_reconstruccion_V26/`)
| Archivo | Naturaleza |
|---|---|
{filas}
""")

# ------------------------------------------------------------------ VALIDACION
a_path = E + "salida_val26_pasada_A_previa_manifiesto.txt"
a_txt = open(a_path, encoding="utf-8", newline="").read() if os.path.exists(a_path) else "(pendiente: se genera con v26_validar.py A)\n"
w("REPORTE_VALIDACION_V26.md", f"""# REPORTE DE VALIDACIÓN V26

{HDR}

{AVISO}

{BLOQUE}

| Etapa | Qué | Dónde se registra |
|---|---|---|
| 0. Auditoría y re-ejecuciones previas | Re-ejecución de `V25_copia_integra/evidencia_reconstruccion_V25/val24.py` sobre V24 (18/18) y de `V25_copia_integra/evidencia_reconstruccion_V25/val25.py` sobre V25 (16/16); verificaciones remotas | `REPORTE_VERIFICACION_REMOTA_V26.md` y `evidencia_reconstruccion_V26/` |
| A. Previa al manifiesto | S01–S18 (18 controles) | este reporte (salida real, abajo) |
| B. Manifiesto | `MANIFIESTO_SHA256_V26.txt` (todos los archivos salvo él mismo, por autorreferencia) | `MANIFIESTO_SHA256_V26.txt` |
| C. Posterior al manifiesto | S01–S18 repetidos + S19 (hashlib) + S20 (`sha256sum -c`) = 20 controles | `REPORTE_PUBLICACION_V26_GITHUB.md` (fuera del expediente) |
| D. Publicación y verificación remota | Commits en `audit/fase0-v26-review` y consulta a GitHub | `REPORTE_PUBLICACION_V26_GITHUB.md` |

La pasada A es un subconjunto de la pasada C: S01–S18 son 18 controles, no 36. En la matriz cada uno es un control; sus dos pasadas son dos ejecuciones. No se repiten las 46 pruebas V21, los 26 controles negativos ni PostgreSQL (no se modificaron; S01 prueba que sus resultados son idénticos a V25).

## Salida real de la pasada A (previa al manifiesto V26)
```
{a_txt}```
""")

# ------------------------------------------------------------------ REMOTA
def rawb(n): return open(E + n, encoding="utf-8", newline="").read()
w("REPORTE_VERIFICACION_REMOTA_V26.md", f"""# REPORTE DE VERIFICACIÓN REMOTA V26 (previa a la publicación)

{HDR}

{AVISO}

{BLOQUE}

Alcance: verificaciones contra GitHub realizadas **antes** de publicar V26 (la rama aún no existía: W01). La verificación posterior al push se registra en `REPORTE_PUBLICACION_V26_GITHUB.md`, fuera de este expediente. Los comandos exactos están en `remoto_R01_R08_reejecucion_V26.sh`, `remoto_RV01_RV11_reejecucion_V26.sh` y `remoto_W01_W03_previo_V26.sh`; el criterio PASS/FAIL de cada línea lo aplica `v26_evaluar.py` y consta en `EJECUCIONES_CONTROLES_V26.csv` con su línea.

| Verificación | Ejecuciones | Resultado | Salida cruda |
|---|---|---|---|
| R01–R08 (V24) | V25 re-ejecución, V26 re-ejecución | 8/8 PASS en cada una; 256 de 256 archivos del manifiesto V24 coinciden | `reejecucion_V26_R01_R08.txt` |
| RV01–RV06, RV08–RV11 (V25) | V25 original, V26 corrida 1, V26 corrida 2 | PASS en las tres; 274 de 274 archivos del manifiesto V25 coinciden | `reejecucion_V26_RV01_RV11_corrida2.txt` |
| RV07 (V25) | V26 corrida 1, V26 corrida 2 | corrida 1: FAIL por defecto del script (RV07.e); corrida 2: 7/7 PASS | `reejecucion_V26_RV01_RV11_corrida1_RV07e_FAIL_por_defecto_del_script.txt` y `reejecucion_V26_RV01_RV11_corrida2.txt` |
| W01–W03 (V26) | una | PASS | `reejecucion_V26_W01_W03_previo.txt` |

RV01 se ejecuta en variante: la punta actual de la rama V25 es el HEAD de publicación c3adaf97 y el commit del expediente f2357681 es su padre. RV10 usa el commit del expediente (7 commits por delante de `main`).

## Salida real de R01–R08
```
{rawb("reejecucion_V26_R01_R08.txt")}```

## Salida real de RV01–RV11 (corrida 2, con RV07)
```
{rawb("reejecucion_V26_RV01_RV11_corrida2.txt")}```

## Salida real de W01–W03
```
{rawb("reejecucion_V26_W01_W03_previo.txt")}```
""")
print("construido: controles=%d ejecuciones=%d %s %s" % (N, NX, cu, ce))
