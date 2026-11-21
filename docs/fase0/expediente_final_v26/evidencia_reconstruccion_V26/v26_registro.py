#!/usr/bin/env python3
"""Registro de controles y ejecuciones de V26 (definiciones + lectura de salidas crudas). Módulo usado por v26_construir.py y v26_validar.py.
Todas las rutas de evidencia son relativas a expediente_final_v26/."""
import csv, io, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v26_evaluar as ev

FECHA = "2026-11-20"  # fecha local (America/Mexico_City); las salidas remotas llevan su propio sello en UTC
E25 = "V25_copia_integra/evidencia_reconstruccion_V25/"
E26 = "evidencia_reconstruccion_V26/"
H25 = E26 + "historico_V25_no_archivado/"
T21 = "V25_copia_integra/04_RESULTADOS_DE_PRUEBAS/V21/"
T22 = "V25_copia_integra/04_RESULTADOS_DE_PRUEBAS/V22_reproduccion_desde_copia/"
EXT_C = "../REPORTE_PUBLICACION_V26_GITHUB.md"  # evidencia de la pasada C de V26 (fuera del expediente)
LIM = "V25_copia_integra/07_LIMITACIONES_Y_DECISIONES_PENDIENTES/00_ESTADOS_DE_VERIFICACION_Y_LIMITACIONES.md"

COLS = ["ID", "Version_origen", "Categoria", "Objetivo", "Entrada", "Resultado_esperado", "Resultado_obtenido", "Evidencia_exacta", "Ruta_evidencia",
        "Ejecucion_historica_o_nueva", "Fecha_ejecucion", "Estado", "Observaciones", "Ejecuciones", "Estado_historico_original"]
ECOLS = ["ID_ejecucion", "ID_control", "Tipo", "Ejecutada_en_version", "Fecha", "Resultado", "Ruta_evidencia", "Linea", "Texto_clave", "Observaciones"]

def v25_matrix(root):
    t = ev.rd(root + "/V25_copia_integra/MATRIZ_CONTROLES_V25.csv")
    return {r["ID"]: r for r in csv.DictReader(io.StringIO(t, newline=""))}

def definiciones(root):
    """Devuelve lista de controles (dict) en orden de presentación."""
    m25 = v25_matrix(root); D = []
    def add(i, ver, cat, obj, ent, esp, **k):
        D.append(dict(ID=i, Version_origen=ver, Categoria=cat, Objetivo=obj, Entrada=ent, Resultado_esperado=esp, **k))
    for i in ["C%02d" % n for n in range(1, 19)]:
        r = m25[i]
        add(i, "V24", "Documental", r["Control"], r["Entrada"], r["Resultado esperado"], hist="V24")
    for i in ["R%02d" % n for n in range(1, 9)]:
        r = m25[i]
        add(i, "V24", "Verificación remota", r["Control"], r["Entrada"], r["Resultado esperado"])
    P = ev.parse_pass_lines(root + "/" + E25 + "salida_val24_pasada_C_posterior_manifiesto.txt")  # solo para validar que existe
    v25 = ev.parse_pass_lines(root + "/" + H25 + "val25_pasada_C_posterior_manifiesto.txt")
    for st, txt, n in v25:
        i = txt[:3]
        add(i, "V25", "Documental", re.sub(r"^[PQ]\d\d ", "", txt.split(" | ")[0]), "Árbol de V25 frente a V24 (commit %s) y manifiesto V25" % ev.V24END[:8], "PASS (sin discrepancias)")
    rvdef = {
        "RV01": ("La rama audit/fase0-v25-review existe y su punta es la esperada", "ls-remote y REST de GitHub", "punta = commit del expediente (V25 original) o HEAD de publicación con ese commit como padre (variante V26)"),
        "RV02": ("El commit del expediente V25 tiene como único padre el final de V24", "API de commits de GitHub", "padre = b88bde03…; 1 padre"),
        "RV03": ("El árbol remoto del commit del expediente V25 es idéntico al local", "git trees recursivo (GitHub) vs git ls-tree", "275 archivos bajo expediente_final_v25/; 916 blobs idénticos; no truncado"),
        "RV04": ("El manifiesto V25 remoto es idéntico al local y todas sus entradas existen en el árbol remoto", "MANIFIESTO_SHA256_V25.txt descargado", "274 entradas; 274 existen; idéntico"),
        "RV05": ("Los archivos descargados de GitHub coinciden con los hashes del manifiesto V25", "descarga de cada archivo del manifiesto", "274 OK, 0 discrepancias"),
        "RV06": ("Las cifras del informe, la matriz y el reporte de validación V25 remotos son coherentes entre sí", "tres documentos descargados", "matriz 18 C + 8 R todas PASS; informe 26 PASS; reporte A 14/14"),
        "RV07": ("El reporte de publicación V25 publicado en GitHub (HEAD) es coherente con el reporte de validación V25 y con las salidas crudas archivadas (definición precisa V26; V25 la dejó como «el reporte de publicación coincide con el reporte de validación»)", "REPORTE_PUBLICACION_V25_GITHUB.md y REPORTE_VALIDACION_V25.md descargados en el HEAD c3adaf9 + salidas crudas archivadas", "7 comprobaciones RV07.a–RV07.g PASS"),
        "RV08": ("El commit del expediente V25 solo añade archivos y todos bajo expediente_final_v25/", "API de commits", "275 archivos; 0 fuera; 0 con estado distinto de added"),
        "RV09": ("V20, V23, V24 y main mantienen sus SHA", "git ls-remote", "ac84133b…, 8674114c…, b88bde03…, 6a1af242…"),
        "RV10": ("Sin PR y la rama V25 no está fusionada en main", "API de pulls y compare", "0 PR; ahead_by=7, behind_by=0 (commit del expediente)"),
        "RV11": ("El commit del expediente V25 no toca código funcional ni infraestructura", "API de commits y árbol de herramientas/", "0 archivos fuera de docs/fase0 o en herramientas/historico; árbol de herramientas V25 = V24"),
    }
    for i, (o, e, x) in rvdef.items(): add(i, "V25", "Verificación remota", o, e, x)
    W = {"W01": ("La rama audit/fase0-v26-review no existe en el remoto antes de publicar", "git ls-remote y REST", "ref inexistente (404)"),
         "W02": ("Antes de publicar V26, main, V20, V23, V24 y V25 mantienen sus SHA históricos", "git ls-remote", "main 6a1af242…, V20 ac84133b…, V23 8674114c…, V24 b88bde03…, V25 c3adaf97…"),
         "W03": ("El árbol remoto del HEAD de V25 es idéntico al árbol local sobre el que se construye V26", "git trees recursivo (GitHub) vs git ls-tree", "917 blobs idénticos; no truncado; HEAD local de la rama de trabajo = c3adaf97…")}
    for i, (o, e, x) in W.items(): add(i, "V26", "Verificación remota", o, e, x)
    HT = [("HT01", "Verificador del expediente: 59 comprobaciones aprobadas", "RESUMEN: 59 comprobaciones, 59 aprueban, 0 fallan, 0 pendientes", [(T21 + "salida_verificador_V21_corrida1.txt", "V21"), (T21 + "salida_verificador_V21_corrida2.txt", "V21"), (T22 + "salida_verificador_reproducido_desde_copia.txt", "V22")]),
          ("HT02", "Verificador del expediente: 28 controles OK", "28 controles (28 OK, 0 NO OK, 0 PENDIENTE)", [(T21 + "salida_verificador_V21_corrida1.txt", "V21"), (T21 + "salida_verificador_V21_corrida2.txt", "V21"), (T22 + "salida_verificador_reproducido_desde_copia.txt", "V22")]),
          ("HT03", "Verificador del expediente: 300 mutaciones detectadas", "300 mutaciones (300 detectadas)", [(T21 + "salida_verificador_V21_corrida1.txt", "V21"), (T21 + "salida_verificador_V21_corrida2.txt", "V21"), (T22 + "salida_verificador_reproducido_desde_copia.txt", "V22")]),
          ("HT04", "22 funciones del modelo en memoria: 366 casos, 0 fallos", "TOTAL funciones=22 casos=366 fallos=0", [(T21 + "salida_22_funciones_V21_corrida3.txt", "V21"), (T22 + "salida_22_funciones_reproducida_desde_copia.txt", "V22")]),
          ("HT05", "PostgreSQL 16 temporal: 63 pruebas, 63 PASS", "TOTAL pruebas=63 PASS=63 FAIL=0", [(T21 + "salida_PE_V21_corrida3.txt", "V21")]),
          ("HT06", "PostgreSQL 16 temporal: 14 mutaciones detectadas", "TOTAL mutaciones=14 DETECTADAS=14", [(T21 + "salida_PE_V21_mutaciones_corrida2.txt", "V21")]),
          ("HT07", "Batería de cierre V21: 46 pruebas, 46 PASS", "RESUMEN BATERÍA V21: 46 pruebas; PASS=46 FAIL=0 BLOCKED=0", [(T21 + "salida_bateria_V21_corrida1.txt", "V21"), (T21 + "salida_bateria_V21_corrida2.txt", "V21")]),
          ("HT08", "Controles negativos de la batería V21: 26 detectados", "TOTAL controles negativos=26 DETECTADOS=26", [(T21 + "salida_controles_negativos_V21.txt", "V21")]),
          ("HT09", "Integridad SHA-256 del expediente V21 (dos métodos)", "RESUMEN INTEGRIDAD V21: TODO PASS", [(T21 + "salida_integridad_V21_corrida1.txt", "V21"), (T21 + "salida_integridad_V21_corrida2.txt", "V21")]),
          ("HT10", "Manifiesto V21 reproducido desde una copia sin Git (V22): 8 de 9 controles PASS y 1 FAIL esperado (historico/ idénticos al commit V20, dependencia de Git)", "8 de 9 controles PASS", [("V25_copia_integra/08_INTEGRIDAD_Y_MANIFIESTOS/INFORME_VERIFICACION_REPRODUCCION.md", "V22")])]
    for i, o, needle, fl in HT:
        add(i, "V21" if fl[0][1] == "V21" else "V22", "Prueba técnica histórica", o, "Salida cruda archivada en 04_RESULTADOS_DE_PRUEBAS/ (V21/V22)", needle + " (en la salida archivada)", ht=(needle, fl))
    L = [("L01", "Escenarios PARCIAL: 12 escenarios (T-03, T-06, T-10, T-47, T-78, T-80, T-124, T-137, T-138, T-139, T-140, T-166) no demuestran toda su obligación sin esquema físico", "12 escenarios PARCIAL", "PARTIAL"),
         ("L02", "T-409 a T-422 sin ejecución individual propia (cubiertos por lectura)", "T-409 a T-422", "PARTIAL"),
         ("L03", "Las 22 funciones del modelo: validación indirecta (sensibilidad a mutaciones e independencia del auditor), no lectura línea a línea", "Las 22 funciones", "PARTIAL"),
         ("L04", "Equivalencia entre el PostgreSQL temporal (63/63 pruebas, 14/14 mutaciones) y el esquema físico aprobado", "no es el esquema físico aprobado", "NOT VERIFIED"),
         ("L05", "Validación física en CCI-DEV", "validación física en CCI-DEV", "NOT VERIFIED"),
         ("L06", "Validación real de RLS, privilegios y concurrencia", "RLS, privilegios y concurrencia real", "NOT VERIFIED"),
         ("L07", "Trigger de elegibilidad R1–R9", "R1–R9", "NOT VERIFIED"),
         ("L08", "HV-02 / PO-05 (confirmación del propietario sobre la Adenda v9)", "HV-02 / PO-05: NO VERIFICABLE", "NOT VERIFIED")]
    for i, o, needle, st in L:
        add(i, "V21", "Alcance técnico (limitación)", o, "Declaración en " + LIM.split("/")[-1], "Limitación declarada y sin ejecución propia", estado_fijo=st, needle=needle)
    S = [("S01", "Copia íntegra de V25: los 275 archivos de V25_copia_integra y el reporte de publicación V25 son idénticos byte a byte a los de la rama V25 (commits f235768 y c3adaf9)"),
         ("S02", "Manifiestos históricos dentro de la copia: V25 verifica 274/274 (hashlib y sha256sum -c); SHA256SUMS interno 252/252; el manifiesto V24 falla exactamente en los 3 archivos con nota V25 (esperado)"),
         ("S03", "Rutas únicas (sin distinguir mayúsculas) y no inseguras (absolutas, con .., con \\, con espacios en los bordes) en todo el expediente V26"),
         ("S04", "MATRIZ_CONTROLES_V26.csv: columnas obligatorias, IDs únicos, estados permitidos y campos obligatorios no vacíos"),
         ("S05", "Toda evidencia citada en la matriz existe dentro del expediente (salvo S19–S20, cuya salida se publica fuera, y los controles L sin ejecución)"),
         ("S06", "EJECUCIONES_CONTROLES_V26.csv coincide con las salidas crudas archivadas (línea y resultado), cada PASS tiene una ejecución PASS y el estado de la matriz es el de la última ejecución"),
         ("S07", "Cifras de conciliación (controles únicos, ejecuciones, estados) idénticas en la matriz, el informe de conciliación, el reporte de validación, el LEEME y el informe de auditoría"),
         ("S08", "Referencias a archivos en los documentos V26 existen; MAPA_REFERENCIAS_V26.csv regenerado coincide con el archivado y no tiene NO_RESUELTA"),
         ("S09", "Los SHA de commit citados en los documentos V26 existen en el repositorio y corresponden al rol declarado"),
         ("S10", "Bloques embebidos = salidas crudas: V25 (pasada A, pasada C, bloque E) y V26 (pasada A, verificación remota)"),
         ("S11", "Limitaciones técnicas y decisiones pendientes del propietario conservadas explícitamente en LEEME_V26 e INFORME_AUDITORIA_FINAL_V26"),
         ("S12", "LEEME_V26 explica V21, V22/V23, V24, V25 y V26, el estado histórico frente al de publicación, la exclusión del manifiesto, y que V26 no es aceptación formal de Fase 0 ni autoriza Fase 1 ni Supabase"),
         ("S13", "Las salidas técnicas históricas contienen las líneas-resumen declaradas (59/59, 28/28, 300/300, 22 funciones, 63/63, 14/14, 46/46, 26/26, integridad, 8 de 9) y las limitaciones L01–L08 constan en el documento de estados"),
         ("S14", "Sin controles duplicados: (versión de origen, objetivo) únicos; ninguna ejecución se cuenta como control; cada ejecución apunta a un control existente"),
         ("S15", "Alcance Git: respecto a la base c3adaf9 solo hay archivos nuevos bajo docs/fase0/expediente_final_v26/; ninguna modificación ni borrado; nada en herramientas/ ni historico/"),
         ("S16", "Historia intacta: refs remotas y locales de main, V20, V23, V24 y V25 iguales a las esperadas; la rama de trabajo parte de c3adaf9"),
         ("S17", "Limitaciones visibles en la matriz: L01–L08 y HT10 con estado PARTIAL/NOT VERIFIED; ningún FAIL ni BLOCKED oculto; la ejecución FAIL de RV07 (corrida 1) figura en ejecuciones"),
         ("S18", "Documentos de entrega V26 presentes (LEEME, informe de auditoría, conciliación, matrices, cambios, validación, verificación remota, mapa, evidencia) y el LEEME declara la exclusión del propio manifiesto"),
         ("S19", "(posterior al manifiesto) MANIFIESTO_SHA256_V26.txt cubre exactamente todos los archivos salvo él mismo y todos los hashes coinciden (hashlib)"),
         ("S20", "(posterior al manifiesto) sha256sum -c MANIFIESTO_SHA256_V26.txt desde expediente_final_v26/ (método independiente)")]
    for i, o in S:
        add(i, "V26", "Documental", o, "Expediente V26 (árbol de trabajo) y repositorio", "PASS (sin discrepancias)", post=(i in ("S19", "S20")))
    return D

def ejecuciones(root, D):
    """Construye la lista de ejecuciones a partir de las salidas crudas. Cada ejecución: dict con las columnas ECOLS (sin ID_ejecucion)."""
    X = []
    def ex(cid, tipo, ver, res, ruta, linea, clave, obs=""): X.append(dict(ID_control=cid, Tipo=tipo, Ejecutada_en_version=ver, Fecha=FECHA, Resultado=res, Ruta_evidencia=ruta, Linea=linea, Texto_clave=clave, Observaciones=obs))
    R = lambda p: root + "/" + p
    # C01-C18: pasada A (V24), pasada C (V24), re-ejecución V25, re-ejecución V26
    for ruta, tipo, ver, obs in [(E25 + "salida_val24_pasada_A_previa_manifiesto.txt", "histórica", "V24", "pasada A previa al manifiesto (solo C01–C16)"),
                                 (E25 + "salida_val24_pasada_C_posterior_manifiesto.txt", "histórica", "V24", "pasada C posterior al manifiesto"),
                                 (E25 + "reejecucion_V25_val24_sobre_V24.txt", "nueva", "V25", "re-ejecución sobre V24 publicado"),
                                 (E26 + "reejecucion_V26_val24_sobre_V24.txt", "nueva", "V26", "re-ejecución sobre V24 publicado")]:
        for k, (st, txt, n) in enumerate(ev.parse_pass_lines(R(ruta)), 1):
            ex("C%02d" % k, tipo, ver, st, ruta, n, st + " |", obs)
    # R01-R08
    for ruta, ver in [(E25 + "reejecucion_V25_remoto_V24.txt", "V25"), (E26 + "reejecucion_V26_R01_R08.txt", "V26")]:
        for i, (st, n) in ev.eval_R(R(ruta)).items(): ex(i, "nueva", ver, st, ruta, n, i + " ", "re-ejecución contra GitHub de la verificación de V24 (la salida cruda original de V24 no se archivó)")
    # P/Q
    for ruta, tipo, ver, obs in [(H25 + "val25_pasada_A_previa_manifiesto.txt", "histórica", "V25", "pasada A previa al manifiesto V25"),
                                 (H25 + "val25_pasada_A2_intermedia_no_archivada_en_V25.txt", "histórica", "V25", "repetición intermedia de la pasada A (salida idéntica a A); no se había documentado ni archivado en V25"),
                                 (H25 + "val25_pasada_C_posterior_manifiesto.txt", "histórica", "V25", "pasada C posterior al manifiesto V25 (embebida en REPORTE_PUBLICACION_V25)"),
                                 (E26 + "reejecucion_V26_val25_sobre_V25.txt", "nueva", "V26", "re-ejecución de val25.py sobre V25 publicado")]:
        for i, (st, n) in ev.parse_val25(R(ruta)).items(): ex(i, tipo, ver, st, ruta, n, st + " | " + i + " ", obs)
    # RV
    for ruta, tipo, ver, obs in [(H25 + "remoto_RV_V25_salida_original_sin_RV07.txt", "histórica", "V25", "salida original de V25 (RV07 no incluida; ver D01)"),
                                 (E26 + "reejecucion_V26_RV01_RV11_corrida1_RV07e_FAIL_por_defecto_del_script.txt", "nueva", "V26", "corrida 1 de V26; RV07 FAIL por un defecto del propio script de comprobación (criterio RV07.e arbitrario), no del objeto verificado"),
                                 (E26 + "reejecucion_V26_RV01_RV11_corrida2.txt", "nueva", "V26", "corrida 2 de V26 con el script corregido")]:
        for i, (st, n) in ev.eval_RV(R(ruta)).items():
            ex(i, tipo, ver, st, ruta, n, "RESUMEN RV07:" if i == "RV07" else i + " ", obs)
    # W
    for i, (st, n) in ev.eval_W(R(E26 + "reejecucion_V26_W01_W03_previo.txt")).items(): ex(i, "nueva", "V26", st, E26 + "reejecucion_V26_W01_W03_previo.txt", n, i + " ", "verificación remota previa a la publicación de V26")
    # HT
    for d in D:
        if "ht" in d:
            needle, fl = d["ht"]
            for ruta, ver in fl:
                n = ev.has_line(R(ruta), needle)
                res = ("PARTIAL" if d["ID"] == "HT10" else "PASS") if n else "FAIL"
                ex(d["ID"], "histórica", ver, res, ruta, n, needle, "no re-ejecutada en V26: se verifica que la salida archivada contiene la línea-resumen (S13)")
    # S: pasadas A y C de V26
    sA = E26 + "salida_val26_pasada_A_previa_manifiesto.txt"; sC = EXT_C
    cres = {}
    cf = "/tmp/pub/v26/val26_C.txt"
    if os.path.exists(cf):
        for st, txt, n in ev.parse_pass_lines(cf):
            cres[txt[:3]] = (st, n)
    for d in D:
        if d["ID"].startswith("S"):
            i = d["ID"]
            if i not in ("S19", "S20"):
                st, n = (ev.parse_val25(R(sA)).get(i) or ("PASS", 0)) if os.path.exists(R(sA)) else ("PASS", 0)
                ex(i, "nueva", "V26", st, sA, n, st + " | " + i + " ", "pasada A previa al manifiesto V26")
            st, n = cres.get(i, ("PASS", 0))
            ex(i, "nueva", "V26", st, sC, "sección C", st + " | " + i + " ", "pasada C posterior al manifiesto V26; salida cruda fuera del expediente (no puede contener el hash de sí misma)")
    return X

def construir_registro(root):
    D = definiciones(root); X = ejecuciones(root, D)
    for k, x in enumerate(X, 1): x["ID_ejecucion"] = "EX-%04d" % k
    por = {}
    for x in X: por.setdefault(x["ID_control"], []).append(x)
    rows = []
    for d in D:
        xs = por.get(d["ID"], []); i = d["ID"]
        tipos = sorted(set(x["Tipo"] for x in xs))
        tip = "no ejecutada (limitación declarada)" if not xs else " + ".join(tipos)
        if "estado_fijo" in d:
            est = d["estado_fijo"]; hist = est
            ult = "sin ejecución propia; declarada en el documento de estados"; ruta = LIM; evi = "texto «%s» en el documento de estados" % d["needle"]; fecha = ""
        else:
            ult_x = xs[-1]; est = ult_x["Resultado"]
            if i == "HT10": est = "PARTIAL"
            hist = {"R": "NOT VERIFIED (salida cruda no archivada)", "RV07": "NOT VERIFIED (ejecución solo en la respuesta de entrega de V25; sin salida cruda)"}.get(i[0] if i[0] == "R" and not i.startswith("RV") else i, "")
            if i[0] == "R" and not i.startswith("RV") : hist = "NOT VERIFIED (salida cruda de V24 no archivada)"
            if i[0] in "CPQ" or i[:2] in ("RV",) and i != "RV07" or i[:2] == "HT": hist = next((x["Resultado"] for x in xs if x["Tipo"] == "histórica"), "") or ""
            if i[0] in ("W", "S"): hist = "n/a (control nuevo de V26)"
            npass = sum(x["Resultado"] == "PASS" for x in xs)
            nfail = sum(x["Resultado"] == "FAIL" for x in xs)
            ult = "%s en la última ejecución (%s); %d %s: %d PASS%s" % (ult_x["Resultado"], ult_x["Ejecutada_en_version"], len(xs), "ejecución" if len(xs) == 1 else "ejecuciones", npass, (", %d FAIL" % nfail) if nfail else "")
            ev_x = next((x for x in reversed(xs) if not x["Ruta_evidencia"].startswith("..")), ult_x)
            ruta = ev_x["Ruta_evidencia"]; evi = "línea %s de %s" % (ev_x["Linea"], os.path.basename(ruta)) if ev_x["Linea"] != "sección C" else "sección C de REPORTE_PUBLICACION_V26_GITHUB.md (fuera del expediente)"
            if ev_x is not ult_x: ult += "; evidencia dentro del expediente: pasada A; la pasada C se registra fuera"
            fecha = ult_x["Fecha"]
        obs = ""
        if i == "RV07": obs = "V25 lo declaró ejecutado tras el segundo commit sin archivar la salida (D01). V26: definición precisa, script y salida cruda archivados; la corrida 1 falló por un defecto del script y la corrida 2 pasó 7/7."
        elif i == "RV01": obs = "En V26 se ejecuta la variante: la punta actual es el HEAD de publicación c3adaf97 y el commit del expediente f2357681 es su padre."
        elif i[0] == "R" and not i.startswith("RV"): obs = "Histórico V24: la salida cruda no se archivó; no se cuenta como ejecución. Re-ejecutado en V25 y V26 (ejecuciones nuevas)."
        elif i in ("S19", "S20"): obs = "Se ejecuta sobre el paquete definitivo; su salida cruda va en REPORTE_PUBLICACION_V26_GITHUB.md (fuera del expediente) porque un archivo no puede contener su propio hash. El estado se consigna tras ejecutarlo (punto fijo documentado)."
        elif i == "HT10": obs = "PARTIAL: el FAIL esperado (comparación con el commit V20 vía Git en una copia sin repositorio) no es discrepancia de contenido, pero es un control no superado en esa reproducción."
        elif i[:2] == "HT": obs = "Histórico; no re-ejecutado en V26 (el verificador tarda ~21 min; las pruebas PostgreSQL requieren binarios y clúster temporal). S13 comprueba que la salida archivada contiene el resumen."
        elif i in ("L04", "L05", "L06", "L07", "L08"): obs = "NOT VERIFIED: no ejecutado ni ejecutable sin esquema físico aprobado / CCI-DEV / confirmación del propietario. V26 no lo simula."
        elif i in ("L01", "L02", "L03"): obs = "PARTIAL: cobertura parcial declarada; V26 no la amplía."
        elif i == "C05": obs = "Control de diseño débil (subconjunto de archivos autorizados); su existencia queda cubierta por C17/C18."
        rows.append(dict(ID=i, Version_origen=d["Version_origen"], Categoria=d["Categoria"], Objetivo=d["Objetivo"], Entrada=d["Entrada"], Resultado_esperado=d["Resultado_esperado"],
                         Resultado_obtenido=ult, Evidencia_exacta=evi, Ruta_evidencia=ruta, Ejecucion_historica_o_nueva=tip, Fecha_ejecucion=fecha, Estado=est, Observaciones=obs,
                         Ejecuciones=len(xs), Estado_historico_original=hist))
    return rows, X

SIN_EVIDENCIA = [
    ("V24", "Ejecución intermedia del validador V24 con 15/16 PASS (defecto de mayúsculas del propio validador, ya corregido)", "solo en la transcripción de la sesión V24", "no resoluble: la salida no existe; no se cuenta como ejecución"),
    ("V24", "Ejecución intermedia del validador V24 con 16/16 PASS antes de existir INFORME_CORRECCIONES_V24.md", "solo en la transcripción de la sesión V24", "no resoluble: la salida no existe; no se cuenta como ejecución"),
    ("V24", "Verificaciones remotas R01–R08 originales (declaradas en REPORTE_PUBLICACION_V24_GITHUB.md)", "reporte de publicación V24 (sin salida cruda)", "re-ejecutadas en V25 y V26 como ejecuciones nuevas; las originales no se cuentan"),
    ("V25", "RV07 declarada ejecutada tras el segundo commit de V25", "respuesta de entrega de V25 (sin salida cruda; solo restos de descargas sin comando ni resultado)", "ejecutada de nuevo en V26 con salida cruda; la de V25 no se cuenta"),
]

def conciliacion(rows, X):
    est = ["PASS", "FAIL", "BLOCKED", "NOT VERIFIED", "PARTIAL"]
    cu = {e: sum(r["Estado"] == e for r in rows) for e in est}
    ce = {e: sum(x["Resultado"] == e for x in X) for e in est}
    cat = {}
    for r in rows: cat.setdefault(r["Categoria"], []).append(r)
    return cu, ce, cat
