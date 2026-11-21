#!/usr/bin/env python3
# Genera ../REVISION_22_FUNCIONES.md y ../MATRIZ_FUNCION_REGLA_ESCENARIO_PRUEBA.csv. Uso: python3 -I -B ct_gen_revision_22.py <V26_dir> <insp22.json>
import json, sys, os, csv, glob, collections, re
v, jp = sys.argv[1], sys.argv[2]; here = os.path.dirname(os.path.abspath(__file__)); I = {o["funcion"]: o for o in json.load(open(jp, encoding="utf-8"))}
M = os.path.join(v, "V25_copia_integra", "02_MATRICES_E_INVENTARIOS")
cas = collections.defaultdict(list)
for r in csv.DictReader(open(glob.glob(M + "/*REGISTRO_CASOS_22*.csv")[0], encoding="utf-8")): cas[r["funcion"]].append(r)
ESC = list(csv.DictReader(open(glob.glob(M + "/*FINAL_780*.csv")[0], encoding="utf-8")))
rid = re.compile(r"\b(I[GSEMP]\d{0,2}-\d+)\b")
by_rule = collections.defaultdict(list)
for e in ESC:
    for r in rid.findall(e["Reglas_citadas"]): by_rule[r].append(e["Escenario"])
REGLAS = {r['Regla'] for r in csv.DictReader(open(glob.glob(M + '/*FINAL_231*.csv')[0], encoding='utf-8'))}
# (responsabilidad, reglas/invariantes, escenarios_relacionados_por_texto, riesgo/observación, brecha)
D = {
"pruebas_guarda": ("Intentos directos de alterar el registro de resoluciones (9) deben lanzar ResolucionInmutable y dejar el registro idéntico", "IG5-98; I13", "", "`except Exception: ok=False` convierte un error inesperado en «no rechazado» (conservador, no oculta fallos).", "Sólo guarda en memoria; el equivalente físico es trigger+privilegios (PRUEBAS_RLS_PRIVILEGIOS_CONCURRENCIA.md)."),
"pruebas_atomicidad": ("Reutilización de asset con elemento ausente/inconsistente falla antes de escribir y no deja registros parciales (20 casos: 8 propios + 12 de correr_mutaciones_rechazo)", "IG5-102; H-01", "T-3xx reutilización de arte", "Acoplamiento: reusa correr_mutaciones_rechazo; un fallo allí se propaga a esta función.", "Atomicidad física (transacción/rollback) no validada."),
"correr_mutaciones_rechazo": ("A54..A65: altera UNA relación del origen y exige rechazo antes de escribir, error identificado, estado idéntico, E nulo y sin impacto ni publicación", "IG5-102, IG5-103; relaciones RS-01 a RS-06", "T-3xx", "Código muerto `x0.E(\"ca\") if False else …` (línea 2264); inofensivo.", "FK compuestas RS-xx no ejecutadas en esquema físico."),
"correr_adversariales": ("Motor forzado acepta una alteración y el auditor independiente la detecta (16)", "IE-12; I1..I28", "T-4xx", "Lee la lista global ADV; depende de que ADV sea completa.", "Equivalencia auditor/SQL no demostrada."),
"correr_escenarios": ("12 escenarios A..L, resoluciones RS, uniformidad y metamorfismo con el motor correcto (17 casos)", "IG5-97; IG5-72; IG5-91", "T-409..T-422 (conservación)", "Casos con aserciones codificadas a mano (valores esperados fijos).", "Modelo en memoria, sin concurrencia."),
"correr_mutaciones_k47": ("36 mutaciones del auditor K47: cada una cambia UNA cosa y exige el invariante específico y su mensaje", "IG5-97, IE-12; I1..I12", "T-409..T-422 (25 de las 36 mapeadas)", "Detección exige coincidencia de mensaje (`kw in v[1]`): frágil ante cambios de redacción.", "11 mutaciones (M16, M21, M27..M36) sin escenario T asociado en el texto de la especificación."),
"correr_mutaciones_resoluciones": ("12 mutaciones R01..R12 de inmutabilidad y reglas de resoluciones de descarte", "IG5-98, IG5-93; I13", "T-413, T-414", "Igual que k47 (delegada en _correr_lista).", "Equivalente físico: trigger + índice único parcial (probado en PE_POSTGRESQL_V20 PG-AD)."),
"correr_mutaciones_assets": ("53 mutaciones de procedencia de arte (uploader, evento, atribución, reutilización)", "IG5-100, IG5-101, IG5-102, IG5-103", "T-3xx", "Igual que k47; 53 casos (A01..A53) dependen de IDs fijos.", "FK RS-xx no ejecutadas físicamente."),
"correr_positivos_arte": ("26 casos válidos de arte que el motor debe aceptar sin violaciones", "IG5-100, IG5-101, IG5-102", "T-3xx", "Contiene `if False` (línea 2276, en _pos13).", "Positivos sólo en el modelo."),
"correr_mutaciones_k45": ("27 mutaciones sobre la matriz 4.4.10 (K45) + 3 positivos; deepcopy del fixture", "IE-12; K45 C01..C15", "T-3xx (relaciones source_*)", "Único con `copy.deepcopy`; retorna tupla (res, positivos).", "Requiere la matriz de la especificación; no se ejecuta aislado."),
"correr_mutaciones_cadena": ("CHAIN-01..20 sobre eslabones intermedios de una cadena válida de tres niveles", "IG5-103; K56", "T-3xx cadena", "Lista CHAIN global; casos por eslabón.", "FK de cadena físicas no ejecutadas."),
"correr_adversariales_cadena": ("Motor forzado + auditor sobre la cadena (24); exige aceptación, detección, E bloqueado, impacto falla y no publica", "IG5-103; K56", "T-3xx", "`except Exception: acepta=False` anidado: un error inesperado se registra como «el motor no acepta» (hace fallar el caso, conservador).", "—"),
"correr_mutaciones_atribucion": ("12 mutaciones de atribución (I13, I15…) con autorretiro y resoluciones forzadas", "IG5-97; I13, I15", "T-409..T-422", "38 líneas sin try: una excepción aborta toda la función (no se aísla por caso).", "Sin concurrencia."),
"pruebas_atomicidad14": ("Atomicidad de v14 (carga de asset, reutilización): fallo a mitad, actor ajeno, versión inexistente; estado completo idéntico (11)", "IG5-102", "T-3xx", "4 bloques try; un `except Exception` amplio.", "Atomicidad física no validada."),
"pruebas_E14": ("Reconstrucción de E y elegibilidad del evaluador E1..E7 con fallo cerrado (6)", "IG5-108; IG5-42", "T-166, T-202", "Conjuntos esperados fijos (p. ej. {A,Pm,B,U,D,W}); usa comprensiones con efectos laterales (`[m.at.pop(...)]`).", "El trigger físico R1–R9 no existe."),
"correr_mutaciones_av": ("8 mutaciones: asset_version incorrecto en eslabones propios", "IG5-103; K58", "T-3xx", "Una línea; delega en _correr15.", "—"),
"correr_mutaciones_cf": ("8 mutaciones: campo incorrecto en eventos propios", "IG5-103; K58", "T-3xx", "Delega en _correr15.", "—"),
"correr_mutaciones_ac": ("6 mutaciones: combinaciones asset_version + campo", "IG5-103; K58", "T-3xx", "Delega en _correr15.", "—"),
"correr_positivos15": ("8 cadenas válidas v15 que deben aceptarse", "IG5-103", "T-3xx", "Contiene aserciones por AP.", "—"),
"correr_adversariales15": ("Motor forzado + auditor con v15 (8)", "IG5-103", "T-3xx", "`… if True else False` (línea 2959): condición tautológica, inofensiva.", "—"),
"pruebas_atomicidad15": ("Atomicidad antes/después de validar la raíz; el reintento sin fallo repone el estado (8)", "IG5-102", "T-3xx", "Verifica reintento (idempotencia lógica) sólo en memoria.", "Idempotencia física/concurrencia no validadas."),
"correr_mutaciones_modelo14": ("12 mutaciones del propio modelo (validación por eslabón convertida en no-op)", "K56-M", "—", "Es una prueba de la prueba (meta-mutación).", "—"),
}
DEF = [("DEF-F01", "correr_mutaciones_rechazo", 2264, "Rama muerta `x0.E(\"ca\") if False else calcular_E_verificado(...)`", "Ejecutar la función y leer la línea; la rama `x0.E` nunca se evalúa", "Resto de refactorización", "Ninguno funcional; confunde la lectura y oculta la intención", "Eliminar la rama muerta (en una copia; no se modificó el original)", "Re-ejecutar las 22 funciones y comparar los 366 casos"),
 ("DEF-F02", "correr_positivos_arte (_pos13)", 2276, "`ev[\"source_root_asset_id\"] if False else ...`", "Lectura de la línea", "Resto de refactorización", "Ninguno funcional", "Eliminar la rama muerta", "Re-ejecución de los 26 positivos"),
 ("DEF-F03", "correr_adversariales15", 2959, "`... if True else False`: condición tautológica", "Lectura de la línea", "Condición temporal dejada en el código", "Ninguno funcional", "Quitar el condicional", "Re-ejecución de los 8 adversariales"),
 ("DEF-F04", "correr_mutaciones_atribucion", 2585, "Sin try/except por caso: una excepción inesperada aborta los 12 casos en lugar de marcar uno como error", "Inspección AST (try=0 en 38 líneas)", "Diseño del arnés", "Un fallo del modelo se vería como caída de la función, no como FAIL localizado (no oculta fallos)", "Envolver por caso como hace _correr_lista", "Mutar el modelo para lanzar excepción y comprobar que sólo falla un caso"),
 ("DEF-F05", "correr_mutaciones_k47/resoluciones/assets (_correr_lista)", 2344, "La detección exige `kw in mensaje`: acopla la prueba a la redacción de mensajes del auditor", "Lectura de _correr_lista", "Diseño del arnés", "Un cambio de texto en un mensaje produciría falsos «no detectada» (falla visible, no un falso PASS)", "Identificar por código de violación y no por subcadena", "Cambiar la redacción de un mensaje y observar el resultado")]
DETAIL = {k: v for k, v in D.items()}
o = ["# REVISIÓN LÍNEA A LÍNEA DE LAS 22 FUNCIONES DE EJECUCIÓN", "",
 "**Fuente inspeccionada (sin modificar):** `docs/fase0/herramientas/modelo_estructural.py` (SHA-256 `cc87236a…`). **Método:** (1) lectura de cada función y de sus ayudantes críticos (`_correr_lista`, `_correr15`, `pruebas_E14`, `pruebas_guarda`, `correr_mutaciones_rechazo`, `pruebas_atomicidad`, `correr_adversariales_cadena`); (2) análisis estático automatizado por AST (`scripts_validacion/ct_inspeccion_22_funciones.py`: líneas, argumentos, dependencias, bloques try, `except` amplios, escrituras globales, uso de deepcopy); (3) ejecución local de las mutaciones K47 por escenario (`ct_k47_por_escenario.py`).", "",
 "**Etiquetas usadas:** `INSPECCION_ESTÁTICA_COMPLETA` (código leído/analizado por AST), `PRUEBA_LOCAL_EJECUTADA` (ejecutada en este cierre), `VALIDACIÓN_FÍSICA_PENDIENTE` (sin equivalente físico en CCI-DEV).", "",
 "**Honestidad de alcance.** «Línea por línea» se cumplió con lectura directa en las funciones críticas y con análisis AST sobre las 22; las funciones de una línea (k47, resoluciones, assets, av, cf, ac) son delegaciones a `_correr_lista`/`_correr15` y su lógica es la de esos ayudantes. No se reescribió ni se ejecutó el modelo completo de nuevo (V26 ya lo hizo: 366 casos, 0 fallos).", "",
 "## Rasgos comunes a las 22 funciones (verificados)", "",
 "- **Sin E/S externa:** `modelo_estructural.py` no contiene `open(`, ni `random`, `time`, `uuid`, `datetime` ni acceso a entorno (búsqueda realizada); importa `copy, functools, difflib, hashlib, json` y `contextlib`. Determinista.",
 "- **Sin escrituras globales:** el AST no encuentra `global` en ninguna de las 22; cada función construye su propio motor/fixture. Las listas de casos (K47_MUT, ART_MUT…) son de sólo lectura.",
 "- **Lecturas/escrituras:** sólo estructuras en memoria del propio motor (`Motor`, `m.res`, `m.at`, `m.assets`, `m.ev`); ninguna toca base de datos.",
 "- **Concurrencia/idempotencia:** el modelo es secuencial y de un solo hilo; no representa transacciones concurrentes. Dos ejecuciones consecutivas producen resultados idénticos (V20 corrida1/corrida2 y V26). La concurrencia es `VALIDACIÓN_FÍSICA_PENDIENTE`.",
 "- **Datos nulos/duplicados/inválidos:** cubiertos sólo donde hay casos explícitos (p. ej. evento de carga nulo, ID de asset duplicado, resolutor inválido); no hay prueba generalizada (fuzzing) de nulos en todos los campos.", "",
 "## Resumen por función", "", "| # | Función | Líneas | Casos | Resultado V26 | Responsabilidad | Reglas / invariantes | Estado de la inspección |", "|---|---|---|---|---|---|---|---|"]
i = 0; csvrows = []
for f, (resp, regl, escn, riesgo, brecha) in D.items():
    i += 1; a = I[f]; c = cas[f]; res = collections.Counter(x["resultado"] for x in c)
    o.append("| %d | `%s` | %d–%d (%d) | %d | %s | %s | %s | INSPECCION_ESTÁTICA_COMPLETA; PRUEBA_LOCAL_EJECUTADA (366/366 re-ejecutados, resultados/22_funciones_reejecucion_local.txt); VALIDACIÓN_FÍSICA_PENDIENTE |" % (i, f, a["linea_ini"], a["linea_fin"], a["n_lineas"], len(c), "PASS %d" % res.get("PASS", 0), resp.replace("|", "¦"), regl))
o += ["", "## Ficha detallada por función", ""]
i = 0
for f, (resp, regl, escn, riesgo, brecha) in D.items():
    i += 1; a = I[f]; c = cas[f]
    o += ["### %d. `%s`" % (i, f), "", "- **Identificador y ubicación:** `modelo_estructural.py` líneas %d–%d; SHA-256 del fuente de la función (16 primeros): `%s`." % (a["linea_ini"], a["linea_fin"], a["sha256_fuente"]),
          "- **Responsabilidad:** %s." % resp, "- **Entradas/salidas:** entradas: %s; salida: lista de resultados por caso (`%d` casos individuales en el registro V20/V26)." % ("ninguna (usa listas globales)" if not a["args"] else ", ".join(a["args"]), len(c)),
          "- **Reglas / invariantes:** %s. **Escenarios que citan esas reglas (calculado de la matriz de 780):** %s." % (regl, "; ".join("%s: %d escenarios%s" % (r, len(by_rule.get(r, [])), (" (p. ej. " + ", ".join(by_rule[r][:4]) + ")") if by_rule.get(r) else "") for r in sorted(set(rid.findall(regl)))) or "sin ID de regla individual"),
          "- **Dependencias internas (nombres del módulo):** %s." % (", ".join("`%s`" % x for x in a["dep_mod"][:12]) or "ninguna"), "- **Lecturas / escrituras:** sólo memoria del motor; sin E/S.",
          "- **Manejo de errores:** %d bloque(s) try, %d `except` amplios (`Exception`)." % (a["try_blocks"], a["except_amplio"]), "- **Riesgos de seguridad/integridad y observaciones:** %s" % riesgo,
          "- **Idempotencia/concurrencia:** determinista y secuencial; concurrencia no modelada.", "- **Pruebas existentes:** %d casos en `REGISTRO_CASOS_22_FUNCIONES_V20.csv`, todos PASS en V26." % len(c), "- **Brechas y recomendaciones:** %s" % brecha, ""]
o += ["## Defectos hallados", "", "Ninguno altera un resultado (no hay falsos PASS demostrados). Todos son de mantenibilidad o robustez del arnés; **no se modificó ninguna función original**.", "", "| ID | Función | Línea | Descripción | Reproducción | Causa raíz | Impacto | Corrección propuesta | Prueba necesaria |", "|---|---|---|---|---|---|---|---|---|"]
for d in DEF: o.append("| " + " | ".join(str(x).replace("|", "¦") for x in d) + " |")
o += ["", "## Límites de las 22 funciones como evidencia", "", "- Prueban un **modelo en memoria**; no demuestran FK, triggers, RLS, privilegios, transacciones ni concurrencia del esquema físico (ver `MATRIZ_MODELO_LOGICO_FISICO.md`).", "- 366 casos PASS significan que el modelo detecta las mutaciones que sus autores previeron; no demuestra exhaustividad para Fase 1.", "- La matriz función→regla→escenario→prueba está en `MATRIZ_FUNCION_REGLA_ESCENARIO_PRUEBA.csv`.", ""]

o += ["", "## Corrección final: clasificación de hallazgos, manejo de errores y conciliación de los 366 casos", "",
"### A. Clasificación de los hallazgos DEF-F01..F06", "",
"Categorías: **defecto funcional** (cambia un resultado), **riesgo técnico** (puede producir un resultado engañoso en otras condiciones), **código provisional** (residuo sin efecto), **decisión intencional** (diseño deliberado).", "",
"| ID | Hallazgo | Clasificación | Evidencia | ¿Afecta resultados actuales? | Corrección propuesta (NO aplicada: el código no se modifica) | Impacto de la corrección |", "|---|---|---|---|---|---|---|",
"| DEF-F01 | Rama muerta `x0.E(\"ca\") if False else calcular_E_verificado(...)` (l.2264) | **Código provisional** (residuo de refactor) | `ct_catalogo_except_y_ramas_muertas.py`: `correr_mutaciones_rechazo` idéntica con y sin la rama | No | Eliminar la rama | Nulo (equivalencia demostrada por ejecución) |",
"| DEF-F02 | `ev[...] if False else ...` (l.2276, `_pos13`) | **Código provisional** | Ídem para `correr_positivos_arte` | No | Eliminar la rama | Nulo |",
"| DEF-F03 | `... if True else False` (l.2959) | **Código provisional** (condición temporal tautológica) | Ídem para `correr_adversariales15` | No | Quitar el condicional | Nulo |",
"| DEF-F04 | `correr_mutaciones_atribucion` sin try por caso | **Riesgo técnico** | Inspección AST | No (0 excepciones en la ejecución) | Envolver por caso | Un fallo se localizaría en un caso en vez de abortar la función |",
"| DEF-F05 | Detección acoplada al texto del mensaje (`kw in mensaje`) | **Decisión intencional con riesgo técnico** (exige condición específica, no sólo el código) | Lectura de `_correr_lista` | No | Añadir identificación por código | Reduce el riesgo de falsos «no detectada» por cambios de redacción (falla visible, no falso PASS) |",
"| DEF-F06 | `_baterias14` captura `except Exception` y registra `(\"X\",\"EXC\",False)`; en `correr_mutaciones_modelo14` un fallo de batería cuenta como **detección** | **Riesgo técnico** (misma familia que el defecto del script 04: un error técnico puede leerse como detección) | `ct_exc_en_mutaciones_modelo14.py`: línea base 123 baterías, 0 fallos, 0 EXC; las 12 mutaciones K56 producen 0 entradas EXC y todas tienen fallos localizados | **No** (0 ocurrencias) | Distinguir EXC de fallo localizado y exigir al menos un fallo localizado para declarar «detectada» | Evita detecciones espurias por caída del modelo |", "",
"**Conclusión:** ningún hallazgo es un **defecto funcional** (ninguno altera un resultado actual); tres son código provisional, dos riesgos técnicos latentes con 0 ocurrencias y uno decisión intencional con riesgo técnico.", "",
"### B. Catálogo completo de `except Exception` (AST)", "",
"`resultados/catalogo_except_exception.csv`: 23 bloques; 19 **SEGUROS** (la excepción deja el caso en FAIL/ERROR y nunca en PASS: los manejadores asignan `False`, `err=` o `EXC`; en `_correr_lista` y `correr_mutaciones_k45` un error implica `det=False`); 4 **RIESGO_TECNICO** (los de `_baterias14`, ver DEF-F06). Ninguno asigna `True`. Propagación: el modelo no define una jerarquía de errores propia para fallos técnicos; sólo `ResolucionInmutable`, `OperacionInvalida/ReutilizacionInvalida` y `ProcedenciaIncompleta` son excepciones de dominio, y los manejadores amplios las agrupan con cualquier otra.", "",
"### C. Conciliación de los 366 casos (re-ejecución versionada)", "",
"`ct_reejecucion_22_funciones.py` (antes la re-ejecución no estaba versionada: brecha corregida) llama a las 22 funciones sin modificar el modelo y escribe `resultados/22_funciones_reejecucion_local.txt` (una línea por caso) y `resultados/22_funciones_conciliacion.csv` (casos por función).", "",
"| Verificación | Resultado |", "|---|---|", "| Funciones re-ejecutadas | 22 |", "| Casos reportados (suma por función) | **366** (366 PASS, 0 FAIL) |", "| Identificadores de caso repetidos entre funciones | 0 |",
"| Solapamiento estructural | `pruebas_atomicidad` (20 = 8 propios + 12) **llama a `correr_mutaciones_rechazo`** y reevalúa sus 12 fixtures con otro criterio (`atomico and rechaza`): son **12 evaluaciones distintas sobre 12 fixtures compartidos** |",
"| Lectura honesta de la cifra | **366 evaluaciones; 354 fixtures distintos.** La cifra 366 no es incorrecta, pero no equivale a 366 situaciones independientes |",
"| Suma por función | 9+20+12+16+17+36+12+53+26+30+24+24+12+11+6+8+8+6+8+8+8+12 = 366 (coincide con el REPORTE de V26) |",
"| `correr_mutaciones_k45` | 30 = 27 mutaciones + 3 positivos; los positivos devuelven `(nombre, violaciones)` y el OK es lista vacía (un adaptador ingenuo los contaría como fallo) |", "",
"**Nivel de evidencia:** ejecución local del modelo en memoria; no es validación física. Los 366 PASS significan que el modelo detecta/acepta lo que el propio modelo declara.", ""]
open(os.path.join(here, "..", "REVISION_22_FUNCIONES.md"), "w", encoding="utf-8").write("\n".join(o))
# matriz función-regla-escenario-prueba: reglas por función extraídas del texto (IDs IGx-nn/IE-nn/…) y escenarios que citan esas reglas
with open(os.path.join(here, "..", "MATRIZ_FUNCION_REGLA_ESCENARIO_PRUEBA.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh); w.writerow(["Funcion", "Linea_ini", "Linea_fin", "Casos", "Resultado_V26", "Regla", "N_escenarios_que_citan_la_regla", "Escenarios_muestra", "Prueba_evidencia", "Etiqueta"])
    for f, (resp, regl, escn, riesgo, brecha) in D.items():
        a = I[f]; rs = sorted(set(rid.findall(regl)))
        for r in rs or ["(invariante/control sin ID de regla: %s)" % regl]:
            ids = by_rule.get(r, []); w.writerow([f, a["linea_ini"], a["linea_fin"], len(cas[f]), "PASS %d/%d" % (sum(x["resultado"] == "PASS" for x in cas[f]), len(cas[f])), r, len(ids), " ".join(ids[:8]), "REGISTRO_CASOS_22_FUNCIONES_V20.csv (%s)" % f, "PRUEBA_LOCAL_EJECUTADA; VALIDACIÓN_FÍSICA_PENDIENTE"])
faltan=sorted({r for f,(a,b,c,d,e) in D.items() for r in rid.findall(b) if r not in REGLAS}); print("ok; reglas citadas inexistentes en la matriz de 231:", faltan)
