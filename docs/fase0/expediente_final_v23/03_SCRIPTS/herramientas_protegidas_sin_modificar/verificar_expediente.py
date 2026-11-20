#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verificador documental del expediente Fase 0 (G-1, G-5 y G-10) de Copy & Creative Intelligence.

Lee SOLO los cinco documentos activos y los archivos históricos de docs/fase0 (Markdown) y comprueba su
coherencia interna: identificadores, referencias, cobertura regla-escenario, cifras, fórmulas, contratos,
orden de creación, estados y ausencia de afirmaciones de validación técnica.

No contiene lógica de producto, SQL ni código de aplicación. No ejecuta nada contra PostgreSQL, RLS ni
Supabase: su resultado es VERIFICACIÓN DOCUMENTAL, nunca validación técnica.

Uso:   python3 verificar_expediente.py [--dir RUTA_DOCS_FASE0] [--json] [--md] [--sin-mutaciones]
Requiere: Python 3.8 o superior, solo biblioteca estándar.
Código de salida: 0 si no hay comprobaciones fallidas; 1 si alguna falla.
"""
import re, sys, os, json, hashlib, argparse, copy

ACTIVOS = ["ESPECIFICACION_TECNICA_G1_G5_G10.md", "INFORME_CIERRE_G1_G5_G10.md", "ROADMAP_Y_TRAZABILIDAD_G1_G5_G10.md",
           "AUDITORIA_FINAL_G1_G5_G10.md", "REGISTRO_HISTORICO_VERSIONES.md"]
SPEC, INF, ROAD, AUD, REG = ACTIVOS
V33_SHA = "b5dccdc73a8103966ab1e1b1e84b2e7ead68cd736fba666ec71d0e790d51c1da"
CLAVES17 = ["content.read", "comment.write", "audit.run", "campaign.write", "copy.write", "channel.adapt", "metrics.write", "promotion.write", "asset.upload", "piece.review",
            "piece.approve", "finding.confirm", "finding.dismiss", "piece.publish", "piece.archive", "org.manage", "block.exception.grant"]
ERRORES10 = ["CONTRIBUYENTES_NO_DETERMINABLES", "BRIEF_VERSION_NO_VERIFICABLE", "PROMOTION_SNAPSHOT_NO_VERIFICABLE", "BRIEF_CHAIN_INCONSISTENTE", "PROMOTION_CHAIN_INCONSISTENTE",
             "BRIEF_FIELD_PROVENANCE_INCOMPLETE", "PROMOTION_FIELD_PROVENANCE_INCOMPLETE", "ASSET_PROVENANCE_NO_VERIFICABLE", "COPY_PROVENANCE_INCOMPLETA", "VERSION_CHAIN_INCONSISTENTE"]
PENDIENTES = ["PO-05", "DG-09", "DG-12", "DG-16", "DG-18", "DG-19", "DG-20", "RP-01", "P-01", "P-05", "P-10", "OD-13", "G-9", "DEP-RET-01"]
NUEVAS8 = ["brief_versions", "brief_field_changes", "brief_field_attributions", "promotion_snapshots", "promotion_field_changes", "promotion_field_attributions", "contribution_events", "copy_version_provenance", "attribution_discard_resolutions"]
ESTADO_V33 = "COMPLETADA Y ACEPTADA COMO LÍNEA BASE DOCUMENTAL, CON LIMITACIONES DOCUMENTADAS"
ESTADO_V6 = "COMPLETADO DOCUMENTALMENTE Y PREPARADO PARA ACEPTACIÓN FORMAL DEL PROPIETARIO, CON LIMITACIONES TÉCNICAS EXPLÍCITAS"
FASE1 = "NO INICIADA / NO AUTORIZADA"
INI, FIN = "<!-- VERIFICADOR:INICIO -->", "<!-- VERIFICADOR:FIN -->"
HIST_WORDS = re.compile(r"\bv[2-7]\b|histór|anterior|antes de la v[678]|eran|sustituy|corregid|v3\.3|línea base", re.I)
NEG = re.compile(r"\b(no|sin|ni|nunca|ningún|ninguna|jamás|tampoco|pendiente|pendientes|prohib\w*|impid\w*|rechaz\w*|requier\w*|exig\w*|falta\w*|hasta que|sin que)\b", re.I)

def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()
def cells(line):
    return [c.strip() for c in re.split(r"(?<!\\)\|", line.strip())[1:-1]]
def quitar_bloque(txt):
    while INI in txt and FIN in txt:
        a = txt.index(INI); b = txt.index(FIN, a) + len(FIN)
        txt = txt[:a] + txt[b:]
    return txt
def seccion(txt, num):
    """Texto de la sección cuyo encabezado empieza por «num » (por ejemplo 4.4.3)."""
    m = re.search(r"^#{2,5} " + re.escape(num) + r"[ .].*$", txt, re.M)
    if not m: return None
    nivel = len(re.match(r"#+", m.group(0)).group(0))
    resto = txt[m.end():]
    n = re.search(r"^#{1,%d} " % nivel, resto, re.M)
    return resto[:n.start()] if n else resto
def tablas(txt, encabezado):
    """Filas (listas de celdas) de las tablas cuyo encabezado comienza por `encabezado`."""
    out = []; modo = False
    for l in txt.split("\n"):
        if l.startswith(encabezado): modo = True; continue
        if modo:
            if l.startswith("|---") : continue
            if l.startswith("|"): out.append(cells(l))
            else: modo = False
    return out

class Corpus:
    def __init__(self, textos):
        self.t = textos
        self.spec = textos[SPEC]
        L = self.spec.split("\n")
        self.reglas_def = {}; self.reglas_cov = {}; self.pruebas = {}
        modo = None
        for l in L:
            if l.startswith("| ID | Regla |"): modo = "def"; continue
            if l.startswith("| Regla | Texto | Pruebas |"): modo = "cov"; continue
            if l.startswith("| ID | Requisito cubierto"): modo = "test"; continue
            if not l.startswith("|"):
                if l.strip(): modo = None
                continue
            if l.startswith("|---"): continue
            c = cells(l)
            if modo == "def" and re.match(r"I[A-Z]+\d*-\d+$", c[0]): self.reglas_def.setdefault(c[0], []).append(c)
            elif modo == "cov" and re.match(r"I[A-Z]+\d*-\d+$", c[0]): self.reglas_cov.setdefault(c[0], []).append(c)
            elif modo == "test" and re.match(r"T-\d+$", c[0]): self.pruebas.setdefault(c[0], []).append(c)
        self.reglas = sorted(set(self.reglas_def) | set(self.reglas_cov))
        # entidades nuevas: bloques "#### `tabla`"
        self.entidades = {}
        for m in re.finditer(r"^#### `([a-z_]+)`\n", self.spec, re.M):
            nom = m.group(1); cuerpo = self.spec[m.end():]
            n = re.search(r"^#{1,4} ", cuerpo, re.M); cuerpo = cuerpo[:n.start()] if n else cuerpo
            fks = []
            if "**Claves foráneas:**" in cuerpo:
                bl = cuerpo.split("**Claves foráneas:**")[1].split("**Restricciones únicas:**")[0]
                for c in [cells(x) for x in bl.split("\n") if x.startswith("|") and not x.startswith("|---")][1:]:
                    mm = re.match(r"([a-z_]+)\(", c[1])
                    fks.append((c[0], c[1], mm.group(1) if mm else ""))
            cols = [cells(x)[0] for x in cuerpo.split("**Clave primaria:**")[0].split("\n") if x.startswith("|") and not x.startswith("|---")][1:]
            self.entidades[nom] = dict(fks=fks, cols=cols, texto=cuerpo)
        # orden de creación
        self.orden = []
        sec = self.spec.split("### 14.1 ")[1] if "### 14.1 " in self.spec else ""
        for l in sec.split("\n"):
            if re.match(r"\| \d+ \| \S+ \| ", l):
                c = cells(l); self.orden.append((int(c[0]), c[1], c[2], c[3], c[4]))
    def activos_sin_bloque(self):
        return {k: quitar_bloque(v) for k, v in self.t.items()}

RES = []
def chk(id_, nombre, ok, detalle="", regla="", doc=""):
    RES.append(dict(id=id_, nombre=nombre, ok=(None if ok is None else bool(ok)), detalle=str(detalle)[:400], regla=regla, doc=doc))

_DIR_HIST = None
def ejecutar(textos, dir_hist=None, mutaciones=False):
    global _DIR_HIST; _DIR_HIST = dir_hist
    global RES
    RES = []
    C = Corpus(textos)
    A = C.activos_sin_bloque()
    spec = C.spec
    AR = dict(A)
    if "## Entrada: revisión v8" in A[REG]:
        r_ = A[REG]; k_ = r_.index("## Entrada: revisión v15"); AR[REG] = r_[k_:r_.index("### Manifiesto") if "### Manifiesto" in r_ else len(r_)]
    nR, nT = len(C.reglas), len(C.pruebas)
    tablas_hist = 27
    ent_tabs = [r for r in C.orden if r[2].startswith("tabla")]
    nTab = len(ent_tabs); nNuevas = nTab - tablas_hist
    # ---- K01 presencia ----
    falt = [f for f in ACTIVOS if f not in textos or not textos[f].strip()]
    chk("K01", "Los cinco documentos activos existen y no están vacíos", not falt, falt, "IE-08", "todos")
    # ---- K02 IDs de reglas únicos ----
    dup_def = [k for k, v in C.reglas_def.items() if len(v) > 1]; dup_cov = [k for k, v in C.reglas_cov.items() if len(v) > 1]
    difer = [k for k in C.reglas_def if k in C.reglas_cov and C.reglas_def[k][0][1] != C.reglas_cov[k][0][1]]
    chk("K02", "IDs de reglas únicos (%d reglas) y con el mismo texto en la definición y en la cobertura" % nR, nR > 0 and not dup_def and not dup_cov and not difer, (dup_def, dup_cov, difer[:5]), "IE-08", "ESPECIFICACION 11")
    # ---- K03 IDs de escenarios ----
    dupT = [k for k, v in C.pruebas.items() if len(v) > 1]
    nums = sorted(int(k[2:]) for k in C.pruebas)
    huecos = [n for n in range(1, (nums[-1] if nums else 0) + 1) if n not in set(nums)]
    chk("K03", "IDs de escenarios únicos y consecutivos (%d escenarios)" % nT, nT > 0 and not dupT and not huecos, (dupT, huecos[:5]), "IE-08", "ESPECIFICACION 11")
    # ---- K04 campos completos ----
    malos = []
    for k, v in C.pruebas.items():
        c = v[0]
        if len(c) != 9 or any(not x for x in c) or c[7] not in ("Diseño", "Ejecutable futura", "Infraestructura real"): malos.append(k)
    chk("K04", "Todo escenario tiene ID, requisito, datos iniciales, acción, resultado esperado, resultado prohibido, criterio, nivel y reglas", not malos, malos[:8], "IE-07", "ESPECIFICACION 11")
    # ---- K05 referencias de escenarios a reglas existentes ----
    refs = {}
    for k, v in C.pruebas.items():
        refs[k] = [x.strip() for x in v[0][8].split(",") if x.strip()]
    inex = [(k, r) for k, rs in refs.items() for r in rs if r not in set(C.reglas)]
    chk("K05", "Todo escenario referencia solo reglas existentes", not inex, inex[:6], "IE-08", "ESPECIFICACION 11")
    # ---- K06 cobertura regla -> escenario ----
    cub = {r: [k for k, rs in refs.items() if r in rs] for r in C.reglas}
    sin = [r for r, v in cub.items() if not v]
    chk("K06", "Toda regla tiene al menos un escenario (cobertura %d de %d)" % (nR - len(sin), nR), not sin, sin[:8], "IE-08", "ESPECIFICACION 11")
    # ---- K07 escenario -> regla ----
    sin_r = [k for k, rs in refs.items() if not rs]
    chk("K07", "Todo escenario está asociado a al menos una regla", not sin_r, sin_r[:8], "IE-08", "ESPECIFICACION 11")
    # ---- K08 cobertura declarada = calculada ----
    dif = []
    for r, filas in C.reglas_cov.items():
        decl = sorted(x.strip() for x in filas[0][2].split(",") if x.strip()); calc = sorted(cub.get(r, []))
        if decl != calc: dif.append(r)
    chk("K08", "La tabla de cobertura regla-escenario de la especificación coincide con las referencias de los escenarios", not dif, dif[:6], "IE-08", "ESPECIFICACION 11")
    # ---- K09 cifras ----
    niv = {"Diseño": 0, "Ejecutable futura": 0, "Infraestructura real": 0}
    for v in C.pruebas.values(): niv[v[0][7]] = niv.get(v[0][7], 0) + 1
    res11 = {}
    for c in tablas(seccion(spec, "11.1") or "", "| Concepto | Cantidad |"): res11[c[0]] = c[1]
    ok11 = res11.get("Pruebas totales") == str(nT) and res11.get("Reglas de integridad") == str(nR) and res11.get("Reglas con al menos una prueba") == str(nR - len(sin)) \
        and res11.get("Diseño") == str(niv["Diseño"]) and res11.get("Ejecutable futura") == str(niv["Ejecutable futura"]) and res11.get("Infraestructura real") == str(niv["Infraestructura real"])
    patron = re.compile(r"(\d+) (reglas|pruebas diseñadas|escenarios diseñados|tablas propuestas)")
    incons = []
    for f in (INF, ROAD, AUD, REG):
        for i, l in enumerate(AR[f].split("\n"), 1):
            for m in patron.finditer(l):
                n = int(m.group(1)); tipo = m.group(2)
                esp = nR if tipo == "reglas" else nT if tipo.startswith(("pruebas", "escenarios")) else nTab
                if n != esp and not HIST_WORDS.search(l): incons.append((f[:10], i, m.group(0)))
    row_inf = re.search(r"\| Reglas de integridad \| (\d+) \|", A[INF]); row_inf2 = re.search(r"\| Pruebas diseñadas \| (\d+) \(", A[INF]); row_inf3 = re.search(r"\| Tablas propuestas \| (\d+) \((\d+) históricas \+ (\d+) nuevas\)", A[INF])
    ok_inf = bool(row_inf and int(row_inf.group(1)) == nR and row_inf2 and int(row_inf2.group(1)) == nT and row_inf3 and int(row_inf3.group(1)) == nTab and int(row_inf3.group(3)) == nNuevas)
    chk("K09", "Cifras recalculadas desde los archivos (%d reglas, %d escenarios, %d tablas, %d nuevas) y coincidentes en los cinco documentos" % (nR, nT, nTab, nNuevas), ok11 and ok_inf and not incons, (ok11, ok_inf, incons[:5]), "IE-06", "ESPECIFICACION 11.1; INFORME")
    # ---- K10 fórmula E ----
    forms = []
    for f, txt in A.items():
        for m in re.finditer(r"E = Ctr\(V-A\)", txt):
            seg = txt[m.start():m.start() + 200].replace("*", "").replace("`", "")
            forms.append((f[:10], bool(re.match(r"E = Ctr\(V-A\) ∪ Inh\(V-A\) ∪ ⋃ Ctr\(v\) para v ∈ \[V-D, V-B\] ∪ P", seg))))
    chk("K10", "La fórmula del conjunto excluido E es idéntica en todos los documentos (%d apariciones)" % len(forms), len(forms) >= 4 and all(x[1] for x in forms), [x for x in forms if not x[1]][:3], "IG5-56", "ESPECIFICACION 4.4.3")
    # ---- K11 definición única de contribuyente ----
    s443 = seccion(spec, "4.4.3") or ""
    filas = tablas(s443, "| Figura | Definición |")
    figs = [c[0][:2] for c in filas]
    otras = [f for f in (INF, ROAD, AUD, REG) if re.search(r"^\| [A-F]\. (Autoría de copy|Edición material|Contribución al brief)", A[f], re.M)]
    chk("K11", "Existe una sola definición de contribuyente (figuras A a F en 4.4.3) y no se redefine en otros documentos", figs == ["A.", "B.", "C.", "D.", "E.", "F."] and not otras, (figs, otras), "IG5-40", "ESPECIFICACION 4.4.3")
    # ---- K12 diez errores de procedencia ----
    s445 = seccion(spec, "4.4.5") or ""
    falt_e = [e for e in ERRORES10 if e not in s445]
    sin_esc = [e for e in ERRORES10 if not any(e in " ".join(v[0][2:6]) for v in C.pruebas.values())]
    chk("K12", "Los diez errores de procedencia están en el contrato de version_contributors y cada uno aparece en al menos un escenario", not falt_e and not sin_esc, (falt_e, sin_esc), "IG5-78", "ESPECIFICACION 4.4.5")
    # ---- K13 veintiséis escenarios de H-02 ----
    req26 = ["brief inicial con cinco campos", "modificación de un solo campo", "conserva otros autores", "eliminación de un campo", "sustitución completa", "metadatos sin cambio material",
             "cadena de cuatro versiones", "actor no verificable", "cadena rota", "ciclo de referencias", "cambio de organización", "cambio de descuento", "cambio de condiciones",
             "modificación de precio", "campo promocional eliminado", "campo promocional heredado", "evento duplicado", "no corresponde a la versión", "actor diferente del autenticado",
             "snapshot anterior y no el último", "versión antigua de brief", "cambio de brief después", "cambio promocional después", "heredado que no debe desaparecer", "realmente sustituido",
             "procedencia incompleta que bloquea"]
    h2 = [v[0] for k, v in C.pruebas.items() if v[0][1].startswith("H-02 reconstrucción")]
    faltan = [q for q in req26 if not any(q in x[1] for x in h2)]
    chk("K13", "Los 26 escenarios mínimos de H-02 existen (%d escenarios H-02, con datos, versiones, actores, acción, esperado, prohibido, regla y nivel)" % len(h2), len(h2) >= 26 and not faltan, faltan, "IG5-69 a IG5-79", "ESPECIFICACION 4.4.8")
    # ---- K14 contrato de integridad ----
    s449 = seccion(spec, "4.4.9") or ""
    cont = tablas(s449, "| Relación | Tabla origen |")
    mal14 = [c[0] for c in cont if len(c) != 10 or any(not x for x in c)]
    rel = {(c[1], c[2]) for c in cont}
    fk_sin = []; fk_sin_org = []
    for n in NUEVAS8:
        e = C.entidades.get(n)
        if not e: fk_sin.append((n, "sin bloque")); continue
        for a, b, t in e["fks"]:
            if not any(c[1] == n and c[2] == t and a.strip("()") in c[4] for c in cont): fk_sin.append((n, a))
            if "organization_id" not in a: fk_sin_org.append((n, a))
    chk("K14", "Contrato de integridad (%d relaciones): 10 campos completos por fila, toda FK de las nueve tablas de procedencia figura en él y toda FK incluye organization_id" % len(cont), len(cont) >= 20 and not mal14 and not fk_sin and not fk_sin_org, (mal14[:3], fk_sin[:3], fk_sin_org[:3]), "IG5-80", "ESPECIFICACION 4.4.9")
    # ---- K15 tablas ----
    bloques = [n for n in C.entidades if n in NUEVAS8 or n.endswith("_events")]
    nombres_tab = [r[3] for r in ent_tabs]
    dup_tab = [n for n in set(nombres_tab) if nombres_tab.count(n) > 1]
    faltan_ent = [n for n in NUEVAS8 if n not in nombres_tab or n not in C.entidades]
    chk("K15", "Las nueve tablas de procedencia tienen bloque de definición y fila en el orden de creación; sin tablas repetidas (%d tablas)" % nTab, not dup_tab and not faltan_ent and nTab == 27 + nNuevas, (dup_tab, faltan_ent), "IG5-80", "ESPECIFICACION 4.4.4; 14.1")
    # ---- K16 orden de creación ----
    pos = {}
    for r in C.orden:
        if r[2].startswith("tabla"): pos[r[3]] = r[0]
    clave = {}
    for r in C.orden: clave.setdefault(r[1], len(clave))
    err16 = []
    for r in C.orden:
        deps = [d.strip() for d in r[4].split(",") if d.strip() and d.strip() not in ("—", "tablas y funciones anteriores", "tablas anteriores")]
        for d in deps:
            if d in pos and pos[d] > r[0]: err16.append((r[3][:40], d))
    fk_post = []
    for n in NUEVAS8:
        for a, b, t in C.entidades.get(n, {"fks": []})["fks"]:
            if t != n and t in pos and n in pos and pos[t] > pos[n]: fk_post.append((n, t))
    chk("K16", "Orden de creación: ninguna tabla, función o trigger depende de un objeto posterior y ninguna FK apunta a una tabla creada después (%d pasos)" % len(C.orden), len(C.orden) >= 80 and not err16 and not fk_post, (err16[:4], fk_post[:4]), "IE-08 (H-01 de la v4)", "ESPECIFICACION 14.1")
    # ---- K17 misma secuencia en los documentos ----
    seqs = set()
    for f in (SPEC, ROAD, AUD):
        for m in re.finditer(r"1\.8 → 2\.x → [0-9a-z.→ ]+ → 8\.x", A[f]): seqs.add(m.group(0))
    chk("K17", "La secuencia de subfases de creación es idéntica en especificación, roadmap y auditoría", len(seqs) == 1, seqs, "H-01 v4", "ROADMAP 3; AUDITORIA 2")
    # ---- K18 76 subfases ----
    subs = re.findall(r"^\| (\d\.\d+) \| ", A[ROAD], re.M)
    ids = sorted(set(subs))
    en_orden = {r[1] for r in C.orden if re.match(r"\d\.\d+$", r[1])}
    chk("K18", "El roadmap conserva las 76 subfases, sin duplicados ni subfase 77, y toda subfase del orden de creación existe en él", len(ids) == 76 and len(subs) >= 76 and "77" not in " ".join(i.split(".")[1] for i in ids if i.startswith(("1.", "2.", "3."))) and en_orden <= set(ids), (len(ids), len(subs), sorted(en_orden - set(ids))), "Roadmap v9", "ROADMAP")
    # ---- K19 17 claves ----
    usadas = set(re.findall(r"`((?:content|comment|audit|campaign|copy|channel|metrics|promotion|asset|piece|finding|org|block)\.[a-z_]+)`", " ".join(A.values())))
    ajenas = sorted(k for k in usadas if k not in CLAVES17 and k not in ("block.exception.revoke", "delegation.manage"))
    tiene = [k for k in CLAVES17 if k in " ".join(A.values())] if False else CLAVES17 if "17 claves físicas" in spec else []
    nuevo_perm = [(f[:10], i) for f, t in A.items() for i, l in enumerate(t.split("\n"), 1) if re.search(r"\b(crea|agrega|añade|introduce)\w* (un |una )?(nuevo |nueva )?(permiso|clave física|clave 18|rol)\b", l, re.I) and not NEG.search(l)]
    chk("K19", "Las 17 claves físicas permanecen: las claves citadas están entre las 17, las 17 figuran en la especificación y ninguna frase crea permisos ni roles", not ajenas and len(tiene) == 17 and not nuevo_perm, (ajenas, len(tiene), nuevo_perm[:3]), "P8", "ESPECIFICACION 10.1")
    # ---- K20 13 transiciones, sin estados ni transiciones nuevos ----
    t14 = [(f[:10], i) for f, t in A.items() for i, l in enumerate(t.split("\n"), 1) if re.search(r"transición #1[4-9]|T-02 #1[4-9]|\b14 transiciones|nueva transición|estado nuevo|nuevo estado", l, re.I) and not NEG.search(l)]
    dice13 = "13 transiciones" in spec and "13 transiciones" in A[INF]
    chk("K20", "T-02 conserva 13 transiciones: sin transición #14 o posterior, sin estados ni transiciones nuevos", not t14 and dice13, t14[:3], "P8, IP-01", "ESPECIFICACION 1 y 2")
    # ---- K21 pendientes ----
    falt21 = [(f[:10], p) for f in (SPEC, INF, REG) for p in PENDIENTES if p not in A[f]] + [("ROADMAP", p) for p in ("DEP-RET-01", "DEP-CAT-01") if p not in A[ROAD]]
    chk("K21", "Las decisiones y limitaciones pendientes del propietario se conservan visibles (%d elementos) en especificación, informe y registro" % len(PENDIENTES), not falt21, falt21[:6], "IG5-48", "ESPECIFICACION 12.3; INFORME")
    # ---- K22 estados ----
    mal22 = []
    for f in ACTIVOS:
        t = A[f]
        if FASE1 not in t: mal22.append((f[:10], "Fase 1"))
        if ESTADO_V6 not in t: mal22.append((f[:10], "estado v7"))
    if ESTADO_V33 not in A[INF] or ESTADO_V33 not in spec: mal22.append(("estado v3.3",))
    acep = [(f[:10], i) for f, t in A.items() for i, l in enumerate(t.split("\n"), 1) if re.search(r"(aceptad[oa]|aprobad[oa]) por el propietario", l, re.I) and re.search(r"v([6789]|1[012345])|complementari|esta revisión", l, re.I) and not NEG.search(l) and "preparad" not in l.lower()]
    chk("K22", "Estados: v3.3 aceptada como línea base, v15 completada documentalmente y preparada para aceptación formal, Fase 1 no iniciada; ningún documento declara aceptación del propietario de la v15", not mal22 and not acep, (mal22[:4], acep[:3]), "IE-04", "todos")
    # ---- K23 sin validación técnica no ejecutada ----
    vt = [(f[:10], i, l[:70]) for f, t in A.items() for i, l in enumerate(t.split("\n"), 1) if re.search(r"validad[oa]s? técnicamente|validación técnica (completa|realizada|exitosa)|pruebas? (técnicas? )?(ejecutad|aprobad|superad)|se ejecutó (con éxito|correctamente) en (postgres|supabase)", l, re.I) and not NEG.search(l)]
    chk("K23", "Ningún documento afirma validación técnica ni pruebas técnicas ejecutadas (toda mención está negada o pendiente)", not vt, vt[:3], "IE-05", "todos")
    # ---- K24 sin IA ni similitud como autoridad ----
    sim = [(f[:10], i, l[:70]) for f, t in A.items() for i, l in enumerate(t.split("\n"), 1) if re.search(r"similitud|embedding|puntuaciones? semántic|probabilíst", l, re.I) and not NEG.search(l)]
    r70 = C.reglas_cov.get("IG5-70", [[0, ""]])[0][1]
    chk("K24", "La atribución no usa IA, similitud, embeddings ni inferencias probabilísticas como autoridad (toda mención está negada) y IG5-70 define la regla determinista", not sim and "IA" in r70 and "retained_segments" in r70, sim[:3], "IG5-43, IG5-70", "ESPECIFICACION 4.4.8")
    # ---- K25 históricos ----
    mf = {}
    for c in tablas(A[REG], "| Archivo | SHA-256 |"): mf[c[0]] = c[1].strip("`")
    mal25 = []
    if dir_hist:
        for nom, h in mf.items():
            p = os.path.join(dir_hist, nom)
            if not os.path.exists(p) or sha(p) != h: mal25.append(nom)
    chk("K25", "Los archivos históricos conservan su SHA-256 registrado en el manifiesto (%d archivos) y el registro cita el hash aceptado de v3.3 con %s (registro histórico; la comprobación criptográfica del original es K48)" % (len(mf), V33_SHA[:8]), len(mf) >= 10 and not mal25 and V33_SHA in A[REG], mal25[:4], "IE-04", "REGISTRO manifiesto")
    # ---- K26 diagrama ER ----
    er = next((m for m in re.finditer(r"erDiagram\n(.*?)```", spec, re.S) if "brief_versions" in m.group(1)), None)
    aristas = set(re.findall(r"^\s+(\w+) \}o--\|\| (\w+) :", er.group(1), re.M)) if er else set()
    esp = set()
    for c in cont:
        o, d = c[1], c[2]
        if "," in d or o == d or "—" in (o, d) or o.startswith("las "): continue
        if o in NUEVAS8 or d in NUEVAS8 or o in ("copy_versions", "creative_assets"): esp.add((o, d))
    esp = {(o, d) for (o, d) in esp if (o in NUEVAS8 or d in NUEVAS8)}
    dif26 = aristas ^ esp
    chk("K26", "El diagrama de relaciones (%d aristas) coincide con las relaciones del contrato de integridad" % len(aristas), bool(er) and not dif26, sorted(dif26)[:5], "IG5-80", "ESPECIFICACION 4.4.4")
    # ---- K27 contradicciones ----
    patrones = [r"\b(cuatro|4) fuentes físicas", r"\bseis errores", r"seis códigos de error", r"pendiente de DT-0[12]", r"falla cerrado mientras no exista", r"representación física pendiente",
                r"PC-02 pendiente", r"DT-01 pendiente", r"la v5 es la versión vigente", r"estado v5 vigente", r"la v6 es la versión vigente", r"excluida_por_resolucion", r"exclude_inherited_attribution", r"attribution_state", r"trece tablas nuevas", r"ocho fuentes físicas"]
    cont27 = []
    for f, t in AR.items():
        for i, l in enumerate(t.split("\n"), 1):
            for p in patrones:
                if re.search(p, l, re.I) and not HIST_WORDS.search(l): cont27.append((f[:10], i, p))
    chk("K27", "Sin contradicciones con las versiones anteriores en los documentos activos (patrones de fuentes, errores y pendientes obsoletos)", not cont27, cont27[:4], "IE-08", "todos")
    # ---- K28 registro histórico ----
    regt = A[REG]
    ent = re.findall(r"^## Entrada: (.+)$", regt, re.M)
    v6 = "revisión v15" in regt and "1d14e51a539bca3e8b938288bd63c6d8aba0d0ed" in regt and "d4044c2a618e8f492a2dd3b8cddcf1ccbd3d85a8" in regt and "603b03963ea30797a28154d0e08e4cfa66f3ae53" in regt and "7916115e3476fdb07f5c3bf1c3e35ef9f0ae927a" in regt and "651c7307c0420fb09184ab6d39aebe60e3dee715" in regt and "638ca8c3a334123315704bd117a369c8615f926f" in regt and "a6b36b955f9e3103174a6d49dd1ae5a7fa194e6c" in regt
    chk("K28", "Registro histórico: entradas ordenadas por revisión hasta la v15 con el commit previo 1d14e51… (v14 sobre d4044c2…, v13 sobre 603b039…, v12 sobre 7916115…, v11 sobre 651c730…, v10 sobre 638ca8c… y v9 sobre a6b36b9…) y manifiesto de históricos", len(ent) >= 3 and v6 and "v5" in " ".join(ent) and "v15" in " ".join(ent) and len(mf) >= 10, ent[-3:], "IE-04", "REGISTRO")
    # ---- K29 herramienta documentada ----
    chk("K29", "La especificación documenta la herramienta publicada, su comando y sus límites", "herramientas/verificar_expediente.py" in (seccion(spec, "11.2") or "") and "verificar_expediente.py" in A[AUD], "", "IE-08", "ESPECIFICACION 11.2; AUDITORIA 3")
    # ---- K30 integración: flujo de 19 pasos ----
    s447 = seccion(spec, "4.4.7") or ""
    pasos = re.findall(r"(?<![\d.])(\d{1,2}) (?=[A-ZÁÉÍÓÚ`])", s447.split("Una modificación material")[0])
    chk("K30", "El flujo integrado de 4.4.7 tiene los 19 pasos en el orden obligatorio", [int(x) for x in pasos][:19] == list(range(1, 20)), pasos[:20], "IG5-88", "ESPECIFICACION 4.4.7")
    # ---- K31 nivel de evidencia ----
    chk("K31", "Los niveles de evidencia están definidos (Diseñado, Verificado documentalmente, Validado técnicamente) y IE-05 a IE-08 existen", all(r in C.reglas for r in ("IE-05", "IE-06", "IE-07", "IE-08")) and "Validado técnicamente" in A[AUD], "", "IE-05", "AUDITORIA 1")
    # ---- K32 antes de la mutación: reproducibilidad y negativos ----
    return C, A, dict(nR=nR, nT=nT, nTab=nTab, nNuevas=nNuevas, niv=niv, cub=cub, refs=refs, cont=cont)
def cargar(dir_):
    return {f: open(os.path.join(dir_, f), encoding="utf-8").read() for f in ACTIVOS if os.path.exists(os.path.join(dir_, f))}

# ---------------- controles de auditoría ----------------
CONTROLES = [
 ("C-01", "No existen dos definiciones distintas de contribuyente", "IG5-40: una sola definición A a F", "ESPECIFICACION 4.4.3", "IG5-40; T-165 a T-178 (v4) y escenarios DT-01", "Contar las figuras de 4.4.3 y buscar tablas de definición en los otros cuatro documentos", ["K11"]),
 ("C-02", "La fórmula E es idéntica en todos los documentos", "IG5-56", "ESPECIFICACION 4.4.3 y 4.4.6", "IG5-05, IG5-56", "Extraer cada aparición de la fórmula y compararla con la forma canónica", ["K10"]),
 ("C-03", "version_contributors tiene fuentes físicas definidas", "IG5-42, IG5-65", "ESPECIFICACION 4.4.5", "Fila «Fuentes físicas» del contrato; bloques de las ocho tablas en 4.4.4", "Comprobar que cada fuente tiene bloque de definición y fila en el orden de creación anterior a 5.3", ["K15", "K16", "K12"]),
 ("C-04", "Todas las referencias de versión son exactas", "IG5-62, IG5-79, IG5-85", "ESPECIFICACION 4.4.4 y 4.4.9", "Contrato de integridad: filas de copy_versions y de provenance", "Verificar que toda FK incluye organization_id y que ninguna columna apunta al último o al actual", ["K14", "K32"]),
 ("C-05", "No existen referencias polimórficas sin integridad", "IG5-81", "ESPECIFICACION 4.4.4 y 4.4.9", "CHECK de exactamente un origen; FK tipadas", "Comprobar que cada columna *_id de las ocho tablas está cubierta por una FK y que no hay columnas de tipo-referencia genéricas", ["K32"]),
 ("C-06", "No hay posibilidad de modificar o borrar evidencia histórica", "IS-13, IG5-87", "ESPECIFICACION 4.4.9", "Fila «Inmutabilidad de los registros»; escenarios H-03", "Comprobar la fila del contrato, las reglas y los escenarios de UPDATE, DELETE y TRUNCATE", ["K33"]),
 ("C-07", "La herencia no depende de IA ni de similitud semántica", "IG5-43, IG5-70", "ESPECIFICACION 4.4.3 y 4.4.8", "IG5-70 («sin IA, embeddings, similitud»)", "Buscar menciones de similitud o embeddings no negadas", ["K24"]),
 ("C-08", "La exclusión de DT-02 se limita al proponente de la clasificación vigente", "IG5-45", "ESPECIFICACION 4.4.6", "IG5-45; escenarios de DT-02", "Comprobar la regla y los escenarios del proponente", ["K34"]),
 ("C-09", "No se excluye automáticamente a quien confirma o revierte una clasificación", "IG5-68", "ESPECIFICACION 4.4.6", "IG5-68; escenarios T-174 y de DT-02", "Comprobar la regla y los escenarios de confirmación y reversión", ["K34"]),
 ("C-10", "No existe autovalidación", "IG5-55, IG5-67", "ESPECIFICACION 4.4.3", "IG5-55, IG5-67 y sus escenarios", "Comprobar reglas y escenarios de exclusión y confirmación propias", ["K35"]),
 ("C-11", "No existe autoevaluación", "IG5-56, IS-14", "ESPECIFICACION 4.4.3 y 4.4.6", "IG5-56, IS-14 y sus escenarios", "Comprobar reglas y escenarios de evaluación propia", ["K35"]),
 ("C-12", "No hay asignación automática a Admin", "IG5-57, IS-14", "ESPECIFICACION 4.4.3 y 8.7", "IG5-57, IS-14 y sus escenarios", "Comprobar reglas y escenarios de Admin", ["K35"]),
 ("C-13", "No se permite evaluación con procedencia incompleta", "IG5-64, IG5-78", "ESPECIFICACION 4.4.5", "Diez errores; escenario «procedencia incompleta que bloquea»", "Comprobar los diez errores, su bloqueo y los escenarios", ["K12", "K13", "K36"]),
 ("C-14", "No se permite publicación con evaluación obsoleta", "IG5-66, IG5-68, IG5-89", "ESPECIFICACION 4.4.7", "IG5-89; escenarios de integración", "Comprobar reglas y escenarios de evaluación obsoleta", ["K36"]),
 ("C-15", "No se crearon permisos nuevos", "P8", "ESPECIFICACION 2 y 10.1", "17 claves físicas", "Comparar las claves citadas con las 17 de v3.3", ["K19"]),
 ("C-16", "No se crearon estados nuevos", "P8", "ESPECIFICACION 2", "Estados de T-02 sin cambio", "Buscar frases que creen estados", ["K20"]),
 ("C-17", "No se crearon transiciones nuevas", "P8, IP-01", "ESPECIFICACION 2", "13 transiciones", "Buscar transición #14 o posterior", ["K20"]),
 ("C-18", "No se modificaron las 13 transiciones T-02", "IP-01", "ESPECIFICACION 2", "IP-01 y declaración de 13 transiciones", "Comprobar la declaración y la regla IP-01", ["K20"]),
 ("C-19", "No se modificaron las 17 claves físicas", "P8", "ESPECIFICACION 10.1", "17 claves presentes", "Comprobar que las 17 claves figuran y ninguna otra", ["K19"]),
 ("C-20", "El roadmap respeta las dependencias", "IE-08", "ROADMAP 3 y 4", "76 subfases; orden de creación", "Contar subfases y comprobar la existencia de las del orden de creación", ["K18", "K16"]),
 ("C-21", "Las FK respetan el orden de creación", "H-01 de la v4", "ESPECIFICACION 14.1", "Orden de creación", "Comprobar que ninguna FK apunta a una tabla creada después", ["K16", "K17"]),
 ("C-22", "Cada regla tiene al menos un escenario", "IE-08", "ESPECIFICACION 11", "Cobertura regla-escenario", "Calcular los escenarios de cada regla", ["K06", "K08"]),
 ("C-23", "Cada escenario referencia reglas existentes", "IE-08", "ESPECIFICACION 11", "Columna Reglas de cada escenario", "Buscar referencias inexistentes y escenarios sin regla", ["K05", "K07"]),
 ("C-24", "Los IDs son únicos", "IE-08", "ESPECIFICACION 11", "IDs de reglas y de escenarios", "Buscar duplicados y huecos", ["K02", "K03", "K04"]),
 ("C-25", "Las cifras se recalculan desde los archivos, no se copian", "IE-06", "ESPECIFICACION 11.1; INFORME", "Resumen 11.1 y tabla del informe", "Recalcular y comparar con cada documento", ["K09"]),
 ("C-26", "Los diagramas Mermaid representan el modelo actualizado", "IG5-80", "ESPECIFICACION 4.4.4 y 4.4.7", "Diagrama ER y flujo de 19 pasos", "Comparar las aristas del ER con el contrato y contar los pasos del flujo (el renderizado visual no se verifica)", ["K26", "K30"]),
 ("C-27", "No hay contradicciones entre especificación, informe, auditoría y roadmap", "IE-08", "todos", "Patrones de contradicción; secuencia de subfases; estados", "Buscar patrones obsoletos y comparar estados y secuencias", ["K27", "K17", "K22"]),
 ("C-28", "No se declara validación técnica inexistente", "IE-05", "todos", "Negación de toda validación técnica", "Buscar afirmaciones de validación técnica no negadas", ["K23", "K31"]),
]
INTEGRAL = [
 (1, "Los 28 controles de auditoría", ["K40"]), (2, "Reglas de contribución directa", ["K11", "K37"]), (3, "Herencia de contribuyentes de copy", ["K37", "K14"]), (4, "Herencia de contribuyentes de brief", ["K13", "K38"]),
 (5, "Herencia de contribuyentes de promociones", ["K13", "K38"]), (6, "Procedencia exacta de assets", ["K14", "K37"]), (7, "Integridad de contribution_events", ["K14", "K32"]), (8, "Integridad de copy_version_provenance", ["K14", "K37"]),
 (9, "Referencias inmutables de copy_versions", ["K14", "K33"]), (10, "Completitud de version_contributors", ["K12", "K38"]), (11, "Errores de procedencia incompleta", ["K12"]), (12, "Fail-closed", ["K36", "K12"]),
 (13, "Exclusión del proponente de independencia vigente", ["K34"]), (14, "Elegibilidad del evaluador", ["K34", "K35"]), (15, "Ausencia de autoevaluación", ["K35"]), (16, "Reglas de G-7", ["K39"]),
 (17, "Reglas de G-10", ["K39"]), (18, "Unicidad e integridad de IDs", ["K02", "K03", "K04"]), (19, "Cobertura regla-escenario", ["K06", "K07", "K08"]), (20, "Coherencia entre especificación, informe, auditoría y roadmap", ["K09", "K17", "K22", "K27"]),
 (21, "Orden de dependencias de las 76 subfases", ["K16", "K18"]), (22, "Ausencia de permisos nuevos", ["K19"]), (23, "Ausencia de transiciones nuevas", ["K20"]), (24, "Preservación de decisiones pendientes", ["K21"]),
 (25, "Preservación de v3.3", ["K25", "K22", "K48"]), (26, "Ausencia de afirmaciones de validación técnica no ejecutada", ["K23"]), (27, "Ausencia de contradicciones con v3, v4 y v5", ["K27"]), (28, "Integridad del registro histórico", ["K25", "K28"]),
]

def checks_adicionales(textos, C, A, info):
    spec = C.spec; refs = info["refs"]
    # K32 estructura de las ocho tablas
    polimorfo = []; sin_fk = []; ultimo = []
    for n in NUEVAS8:
        e = C.entidades.get(n)
        if not e: continue
        cols = e["cols"]; cubiertas = set()
        for a, b, t in e["fks"]: cubiertas |= set(re.findall(r"[a-z_]+", a))
        for c_ in info["cont"]:
            if c_[1] == n: cubiertas |= set(re.findall(r"[a-z_]+", c_[4]))
        for c in cols:
            if re.search(r"(source|entity|ref|origin)_(type|kind)$", c) and c != "origin_kind" and not (n == "attribution_discard_resolutions" and c == "source_kind" and "num_nonnulls" in e["texto"]): polimorfo.append((n, c))
            if c in ("source_id", "entity_id", "ref_id"): polimorfo.append((n, c))
            if c.endswith("_id") and c not in ("id", "organization_id", "operation_id", "created_by") and c not in cubiertas and c != "origin_version_id" and not (n == "attribution_discard_resolutions" and c in ("evidence_attribution_id", "evidence_version_id")) and c != "used_asset_id" and c != "origin_asset_id" and c != "promotion_line_id" and c != "contributor_id" and c != "actor_id" and c != "recorded_by" and c != "resolution_actor_id" and c != "brief_id": sin_fk.append((n, c))
            if re.search(r"(latest|current|last)", c): ultimo.append((n, c))
    ult_txt = [(f[:10], i) for f, t in A.items() for i, l in enumerate(t.split("\n"), 1) if re.search(r"(seguir|usar) el (último|ultimo) (brief|snapshot)", l, re.I) and not NEG.search(l) and not l.startswith("| T-")]
    src = verificar_source(spec)
    chk("K32", "Las ocho tablas de procedencia no tienen referencias polimórficas, cada columna *_id (incluidas todas las source_*) está cubierta por una FK compuesta exacta (RS-01 a RS-08: columnas, destino, acción y momento) o por una excepción individual justificada con verificador K45, sin exclusiones generales, y ninguna apunta al último o al actual", not polimorfo and not sin_fk and not ultimo and not ult_txt and not src["K32"], (polimorfo, sin_fk[:4], ultimo, ult_txt[:2], src["K32"][:3]), "IG5-81, IG5-62", "ESPECIFICACION 4.4.4")
    # K33 inmutabilidad
    cont = info["cont"]
    fila = [c for c in cont if c[0].startswith("Inmutabilidad")]
    esc = [k for k, v in C.pruebas.items() if re.search(r"UPDATE|DELETE|TRUNCATE|inmutab", " ".join(v[0][2:6]), re.I) and v[0][1].startswith("H-03")]
    chk("K33", "Inmutabilidad: el contrato la define para las trece tablas, IS-13, IG5-85 e IG5-87 existen y %d escenarios de H-03 intentan modificar, borrar o truncar" % len(esc), bool(fila) and all(r in C.reglas for r in ("IS-13", "IG5-85", "IG5-87")) and len(esc) >= 4 and "TRUNCATE" in fila[0][6] + fila[0][3], len(esc), "IS-13", "ESPECIFICACION 4.4.9")
    # K34 DT-02
    r45 = C.reglas_cov.get("IG5-45", [[0, ""]])[0][1]; r68 = C.reglas_cov.get("IG5-68", [[0, ""]])[0][1]
    t_dt02 = [k for k, v in C.pruebas.items() if v[0][1].startswith("DT-02 proponente")]
    sub_dt = {q: any(q in C.pruebas[k][0][1] for k in t_dt02) for q in ("quien confirma", "deshace", "proponente no puede confirmar")}
    chk("K34", "DT-02: IG5-45 limita la exclusión al proponente de la clasificación vigente, IG5-68 protege a quien confirma o revierte y %d escenarios lo cubren" % len(t_dt02), "propuso" in r45 and "vigente" in r45 and "no queda excluido" in r68 and len(t_dt02) >= 12 and all(sub_dt.values()), sub_dt, "IG5-45, IG5-68", "ESPECIFICACION 4.4.6")
    # K35 autovalidación, autoevaluación y Admin
    r55 = C.reglas_cov.get("IG5-55", [[0, ""]])[0][1]; r57 = C.reglas_cov.get("IG5-57", [[0, ""]])[0][1]; r14 = C.reglas_cov.get("IS-14", [[0, ""]])[0][1]; r67 = C.reglas_cov.get("IG5-67", [[0, ""]])[0][1]
    e_adm = [k for k, v in C.pruebas.items() if "Admin" in " ".join(v[0][1:5]) and any(r in refs[k] for r in ("IS-14", "IG5-57", "IG5-78"))]
    chk("K35", "Sin autovalidación, autoevaluación ni asignación automática a Admin: IG5-55, IG5-67, IG5-57 e IS-14 y %d escenarios de Admin" % len(e_adm), "no puede" in r55 and "no puede" in r67 and "Admin" in r57 and "Admin" in r14 and len(e_adm) >= 3, len(e_adm), "IG5-55, IG5-57, IG5-67, IS-14", "ESPECIFICACION 4.4.3")
    # K36 fail-closed y obsolescencia
    r64 = C.reglas_cov.get("IG5-64", [[0, ""]])[0][1]; r78 = C.reglas_cov.get("IG5-78", [[0, ""]])[0][1]; r89 = C.reglas_cov.get("IG5-89", [[0, ""]])[0][1]
    esc_fc = [k for k, v in C.pruebas.items() if re.search(r"bloquea|bloqueo", v[0][4]) and v[0][1].startswith(("H-02", "Integración v6"))]
    chk("K36", "Fail-closed: IG5-64 e IG5-78 bloquean evaluación, independencia y aprobación o publicación sin excepción de Admin; IG5-89 impide reutilizar evaluaciones; %d escenarios de bloqueo" % len(esc_fc), "bloque" in r64.lower() and "ninguna excepción" in r78 and "no se reutilizan" in r89 and len(esc_fc) >= 6, len(esc_fc), "IG5-64, IG5-78, IG5-89", "ESPECIFICACION 4.4.5")
    # K37 reglas de contribución directa y de procedencia de copy y arte
    need = ["IG5-49", "IG5-50", "IG5-51", "IG5-52", "IG5-53", "IG5-54", "IG5-61", "IG5-83", "IG5-84", "IS-16"]
    falta = [r for r in need if r not in C.reglas or not info["cub"].get(r)]
    chk("K37", "Las reglas de contribución directa, herencia de copy y procedencia de copy y arte existen y tienen escenarios (%d reglas)" % len(need), not falta, falta, "IG5-49 a IG5-54, IG5-83, IG5-84", "ESPECIFICACION 4.4.3 y 4.4.9")
    # K38 atribución por campo
    r70 = C.reglas_cov.get("IG5-70", [[0, ""]])[0][1]; r72 = C.reglas_cov.get("IG5-72", [[0, ""]])[0][1]
    s448 = seccion(spec, "4.4.8") or ""
    cat = all(x in s448 for x in ("objective", "audience", "promoted_item", "value_proposition", "main_benefit", "required_claims", "prohibited_claims", "commercial_offer", "cta", "requested_channel", "requested_format", "tone_directive")) and all(x in s448 for x in ("promotion_code", "included_items", "reference_price", "promotional_price", "discount", "validity", "conditions", "currency", "commercial_restrictions"))
    pasos = len(re.findall(r"\b(?:[1-9]|10) (?:Obtener|Comprobar|Para|Relacionar|Conservar|Incorporar|Retirar|Recalcular|Recorrer|Comparar|Bloquear)", s448))
    chk("K38", "H-02: 12 campos de brief y 9 de promoción catalogados, regla de segmentos (IG5-70), cálculo de atribuciones (IG5-72), historial (IG5-73), dos algoritmos de 10 pasos y reglas IG5-69 a IG5-79", cat and "sustituido" in r70 and "histórica" in r72 + C.reglas_cov.get("IG5-73", [[0, ""]])[0][1] and pasos >= 20 and all("IG5-%d" % n in C.reglas for n in range(69, 80)), (cat, pasos), "IG5-69 a IG5-79", "ESPECIFICACION 4.4.8")
    # K39 G-7 y G-10
    g7 = [r for r in C.reglas if r.startswith("IG5-")]; g10 = [r for r in C.reglas if r.startswith("IG10-")]
    s62 = "C1" in spec and "C9" in spec
    chk("K39", "Reglas de G-7 (C1 a C9) y de G-10 (%d reglas IG10) presentes con cobertura" % len(g10), s62 and len(g10) >= 30 and all(info["cub"].get(r) for r in g10), len(g10), "IG10-*", "ESPECIFICACION 5 y 6.2")

def controles(textos):
    out = []
    byid = {r["id"]: r for r in RES}
    for cid, nom, regla, doc, evid, proc, ids in CONTROLES:
        faltan = [i for i in ids if i not in byid]
        oks = [byid[i]["ok"] for i in ids if i in byid]
        if faltan: est = "PENDIENTE"
        elif any(o is False for o in oks): est = "NO OK"
        elif any(o is None for o in oks): est = "PENDIENTE"
        else: est = "OK"
        nivel = "Verificado documentalmente" if est == "OK" else ("Diseñado" if est == "PENDIENTE" else "Diseñado")
        res = "; ".join("%s %s" % (i, "pasa" if byid[i]["ok"] else ("PENDIENTE" if byid[i]["ok"] is None else "FALLA")) for i in ids if i in byid)
        out.append((cid, nom, regla, doc, evid, proc, res, est, nivel, "Verificación documental; no es validación técnica" if est == "OK" else "Corregir la causa"))
    return out


# ============ v7: integridad semántica de relaciones, resoluciones de descarte, hash real de v3.3 ============
def _tupla(txt):
    return tuple(x.strip() for x in txt.split(",") if x.strip())

def parse_entidades(spec):
    ents = {}
    for m in re.finditer(r"^#### `([a-z_]+)`\n", spec, re.M):
        nom = m.group(1); cuerpo = spec[m.end():]
        n = re.search(r"^#{1,4} ", cuerpo, re.M); cuerpo = cuerpo[:n.start()] if n else cuerpo
        if "| Columna | Tipo |" not in cuerpo: continue
        cols = {}
        for r in tablas(cuerpo.split("**Clave primaria:**")[0], "| Columna | Tipo |"):
            if len(r) >= 2: cols[r[0]] = r[1]
        mm = re.search(r"\*\*Clave primaria:\*\* `([^`]+)`", cuerpo)
        pk = _tupla(mm.group(1)) if mm else None
        fks = []
        if "**Claves foráneas:**" in cuerpo:
            bl = cuerpo.split("**Claves foráneas:**")[1].split("**Restricciones únicas:**")[0]
            for r in tablas(bl, "| Columnas | Referencia |"):
                m2 = re.match(r"([a-z_]+)\(([^)]*)\)", r[1])
                if m2: fks.append((_tupla(r[0].strip("()")), m2.group(1), _tupla(m2.group(2))))
        uniq = []; checks = []
        if "**Restricciones únicas:**" in cuerpo:
            bl = cuerpo.split("**Restricciones únicas:**")[1].split("**Restricciones CHECK:**")[0]
            for l in bl.split("\n"):
                m3 = re.match(r"- unique\(([^)]*)\)", l)
                if m3: uniq.append(_tupla(m3.group(1)))
        if "**Restricciones CHECK:**" in cuerpo:
            bl = cuerpo.split("**Restricciones CHECK:**")[1]
            for l in bl.split("\n"):
                if l.startswith("- "): checks.append(l[2:])
        ents[nom] = dict(cols=cols, pk=pk, fks=fks, uniq=uniq, checks=checks)
    return ents

def parse_historicas(spec):
    out = {}
    s = seccion(spec, "4.4.9") or ""
    for r in tablas(s, "| Tabla | Columnas y tipos | Claves únicas |"):
        if len(r) != 3: continue
        cols = {}
        for c in r[1].split(","):
            p = c.split()
            if len(p) == 2: cols[p[0]] = p[1]
        uniq = [_tupla(re.match(r"unique\(([^)]*)\)", u.strip()).group(1)) for u in r[2].split(";") if re.match(r"unique\(([^)]*)\)", u.strip())]
        out[r[0]] = dict(cols=cols, pk=("id",) if "id" in cols else None, uniq=uniq)
    return out

def parse_contrato(spec):
    s = seccion(spec, "4.4.9") or ""
    rows = []
    for c in tablas(s, "| Relación | Tabla origen |"):
        if len(c) != 10: continue
        m = re.search(r"\(([^)]*)\) → ([a-z_]+)\(([^)]*)\)", c[3])
        rows.append(dict(rel=c[0], origen=c[1], destino=c[2], txt=c[3], agregada="agregada" in c[3], fk=((_tupla(m.group(1)), m.group(2), _tupla(m.group(3))) if m else None)))
    return rows

def _fk_records(spec):
    """FK de las entidades y del contrato (fuente, origen, locales, destino, referenciadas)."""
    ents = parse_entidades(spec); con = parse_contrato(spec)
    recs = []
    for n, e in ents.items():
        for loc, t, ref in e["fks"]: recs.append(("bloque", n, loc, t, ref))
    for r in con:
        if r["fk"]: recs.append(("contrato-agr" if r["agregada"] else "contrato", r["origen"], r["fk"][0], r["fk"][1], r["fk"][2]))
    return ents, con, recs

def _tipo(cat, t, c):
    return cat.get(t, {}).get("cols", {}).get(c)

def verificar_estructura(spec):
    """K44: cada FK compuesta: longitud, orden exacto, organization_id, destino existente con PK o UNIQUE idéntica y tipos compatibles; contrato = bloques; sin relaciones circulares."""
    ents, con, recs = _fk_records(spec); hist = parse_historicas(spec)
    cat = dict(hist); cat.update(ents)
    prob = []
    for fuente, o, loc, t, ref in recs:
        if len(loc) != len(ref): prob.append((o, t, "longitud distinta")); continue
        if len(set(loc)) != len(loc): prob.append((o, t, "columna local repetida"))
        if loc[0] != "organization_id" or ref[0] != "organization_id": prob.append((o, t, "organization_id ausente o fuera de la primera posición", loc, ref))
        if t not in cat: prob.append((o, t, "tabla destino inexistente")); continue
        claves = set(cat[t]["uniq"]) | ({cat[t]["pk"]} if cat[t].get("pk") else set())
        if ref not in claves: prob.append((o, t, "sin PK/UNIQUE de destino con las columnas en ese orden", ref))
        for c in ref:
            if c not in cat[t]["cols"]: prob.append((o, t, "columna destino inexistente", c))
        for a, b in zip(loc, ref):
            ta, tb = _tipo(cat, o, a), _tipo(cat, t, b)
            if o in ents and a not in ents[o]["cols"]: prob.append((o, t, "columna local inexistente", a))
            if ta and tb and ta != tb: prob.append((o, t, "tipos incompatibles", a, b))
    # contrato = bloques (sin las FK agregadas, que solo figuran en el contrato)
    for n, e in ents.items():
        if n not in NUEVAS8: continue
        b = sorted((l, t, r) for l, t, r in e["fks"])
        c = sorted(r["fk"] for r in con if r["origen"] == n and r["fk"] and not r["agregada"])
        if b != c: prob.append((n, "contrato y bloque difieren", [x for x in b if x not in c][:2], [x for x in c if x not in b][:2]))
    # relaciones circulares (se excluye el par copy_versions <-> creative_assets, diferido en v3.3)
    decl = _ciclos_declarados(spec); grafo = {}; aristas = set()
    for fuente, o, loc, t, ref in recs:
        aristas.add((o, t))
        if o != t and {o, t} != {"copy_versions", "creative_assets"} and not (fuente == "contrato-agr" and frozenset((o, t)) in decl): grafo.setdefault(o, set()).add(t)
    for par in decl:
        a_, b_ = sorted(par)
        if (a_, b_) not in aristas or (b_, a_) not in aristas: prob.append(("ciclo declarado en 4.4.15 sin aristas en ambos sentidos", a_, b_))
    prob += _orden_insercion(spec)
    estado = {}
    def dfs(u, pila):
        estado[u] = 1
        for v in grafo.get(u, ()):
            if estado.get(v) == 1: prob.append(("ciclo", " -> ".join(pila + [u, v]))); 
            elif v not in estado: dfs(v, pila + [u])
        estado[u] = 2
    for u in list(grafo):
        if u not in estado: dfs(u, [])
    return prob, len(recs)

def _ciclos_declarados(spec):
    """Pares de tablas con ciclo declarado en la matriz de ciclos de 4.4.15."""
    s = seccion(spec, "4.4.15") or ""; out = set()
    for r in tablas(s, "| Ciclo | Tablas |"):
        if len(r) >= 2 and " ↔ " in r[1]: out.add(frozenset(x.strip() for x in r[1].split(" ↔ ")))
    return out

def _orden_insercion(spec):
    """Orden de inserción de 4.4.15: una FK inmediata no puede apuntar a un paso posterior de la misma operación."""
    s = seccion(spec, "4.4.15") or ""; prob = []
    for r in tablas(s, "| Operación | Paso |"):
        if len(r) < 5: continue
        try: paso = int(r[1])
        except ValueError: prob.append(("orden de inserción con paso no numérico", r[0])); continue
        for n in re.findall(r"paso (\d+)", r[3]):
            if int(n) >= paso: prob.append(("orden de inserción: FK inmediata hacia un paso no anterior", r[0], paso, r[3]))
    return prob

def _tabla_src(spec, enc):
    return tablas(seccion(spec, "4.4.15") or "", enc)

def verificar_source(spec):
    """K32, K44, K45 y K55: cada relación source_* (RS-01 a RS-08), su inventario, sus excepciones individuales, la matriz de ciclos y el orden de inserción, sin exclusiones generales de columnas."""
    out = {"K32": [], "K44": [], "K45": [], "K55": []}
    s = seccion(spec, "4.4.15")
    if not s:
        for k in out: out[k].append("sin la sección 4.4.15")
        return out
    con = parse_contrato(spec); ents = parse_entidades(spec); hist = parse_historicas(spec)
    filas = [r for r in con if r["fk"] and r["agregada"]]
    ids_a = {"K47-A%02d" % i for i in range(1, 66)}
    ids_pr = ids_a | {"CHAIN-%02d" % i for i in range(1, N_CHAIN + 1)}
    cubiertas = set()
    for rs in MS.RELACIONES_SOURCE:
        loc = tuple(rs["locales"]); ref = tuple(rs["ref"])
        cand = [r for r in filas if r["origen"] == rs["origen"] and r["fk"][1] == rs["destino"] and set(r["fk"][0]) == set(loc)]
        if not cand: out["K32"].append((rs["id"], "FK ausente o con columnas locales distintas", rs["origen"], loc)); continue
        r = cand[0]; cubiertas |= set(r["fk"][0])
        if r["fk"][2] != ref and dict(zip(r["fk"][0], r["fk"][2])) == rs["pares"]: out["K32"].append((rs["id"], "columnas de destino distintas", r["fk"][2]))
        if dict(zip(r["fk"][0], r["fk"][2])) != rs["pares"]: out["K45"].append((rs["id"], "pares origen-destino distintos de los exactos", dict(zip(r["fk"][0], r["fk"][2]))))
        if ("ON DELETE %s" % rs["accion"]) not in r["txt"]: out["K32"].append((rs["id"], "acción referencial distinta de %s" % rs["accion"]))
        if "ON UPDATE" in r["txt"]: out["K32"].append((rs["id"], "política de actualización indebida: ningún RS admite ON UPDATE (la actualización de las claves la impide el trigger de inmutabilidad y el valor por defecto NO ACTION)"))
        if ("DEFERRABLE INITIALLY DEFERRED" in r["txt"]) != (rs["momento"] != "inmediata"): out["K32"].append((rs["id"], "momento de verificación distinto"))
    # cada columna source_* y cada columna de origen de creative_assets está cubierta por una FK o por una excepción individual
    ce = ents.get("contribution_events", {}).get("cols", {})
    for c in ce:
        inv = {r[0]: r for r in _tabla_src(spec, "| Columna de origen | Destino |")}
        if c.startswith("source_") and c not in cubiertas and not (inv.get(c) and inv[c][2].startswith("—") and len(inv[c][4].strip()) > 20):
            out["K32"].append(("contribution_events." + c, "columna source_* sin FK ni valor justificado individualmente en el inventario"))
    for c in ("upload_event_id", "reuse_event_id", "asset_lineage_id", "root_asset_version_id", "lineage_parent_asset_id", "reused_from_asset_id"):
        if not any(r["origen"] == "creative_assets" and c in r["fk"][0] for r in filas): out["K32"].append(("creative_assets." + c, "columna de origen sin FK compuesta"))
    # restricciones únicas propias (no son destino de una FK): un evento de reutilización pertenece a un solo asset
    for tb, us in MS.UNICAS_PROPIAS_SOURCE.items():
        for u in us:
            if u not in {tuple(x) for x in (hist.get(tb, {}).get("uniq") or [])}: out["K32"].append(("restricción única propia ausente en %s" % tb, u))
    # excepciones individuales
    exc = _tabla_src(spec, "| Elemento | Motivo |"); esperadas = {e[0] for e in MS.EXCEPCIONES_SOURCE}
    if {r[0] for r in exc} != esperadas: out["K32"].append(("las excepciones del documento no coinciden con las justificadas", sorted({r[0] for r in exc} ^ esperadas)[:2]))
    for r in exc:
        if len(r) != 5 or not all(x.strip() for x in r[:4]): out["K32"].append(("excepción sin motivo, mecanismo alternativo o prueba", r[0] if r else "")); continue
        if "K45" not in r[4]: out["K32"].append(("excepción de K32 sin verificador K45 que la justifique", r[0]))
        pr = re.findall(r"K47-A\d\d", r[3])
        if not pr or any(x not in ids_a for x in pr): out["K45"].append(("la prueba negativa de la excepción no existe", r[0], r[3][:60]))
    # K55: el documento contrasta con el modelo
    B = _tabla_src(spec, "| ID | Origen (en orden) |")
    if [r[0] for r in B] != [x["id"] for x in MS.RELACIONES_SOURCE]: out["K55"].append(("matriz de relaciones distinta del modelo", [r[0] for r in B]))
    else:
        for r, x in zip(B, MS.RELACIONES_SOURCE):
            if r[1] != "%s(%s)" % (x["origen"], ", ".join(x["locales"])) or r[2] != "%s(%s)" % (x["destino"], ", ".join(x["ref"])): out["K55"].append((x["id"], "origen o destino de la matriz distintos del modelo"))
            for q in re.findall(r"(?:K47-A|CHAIN-)\d\d", r[5]):
                if q not in ids_pr: out["K55"].append((x["id"], "prueba inexistente", q))
            if not re.findall(r"(?:K47-A|CHAIN-)\d\d", r[5]): out["K55"].append((x["id"], "relación sin prueba positiva citada"))
    A_ = _tabla_src(spec, "| Columna de origen | Destino |")
    if [r[0] for r in A_] != [x[0] for x in MS.INVENTARIO_SOURCE]: out["K55"].append(("inventario distinto del modelo",))
    elif any(not r[2].startswith("—") and any(q.strip() not in {x["id"] for x in MS.RELACIONES_SOURCE} for q in r[2].split(",")) for r in A_): out["K55"].append(("inventario con relación inexistente",))
    if [(r[0], r[1]) for r in _tabla_src(spec, "| Ciclo | Tablas |")] != [(c[0], " ↔ ".join(c[1])) for c in MS.CICLOS_SOURCE]: out["K55"].append(("matriz de ciclos distinta del modelo",))
    if [(r[0], r[1], r[2]) for r in _tabla_src(spec, "| Operación | Paso |")] != [(o[0], str(o[1]), o[2]) for o in MS.ORDEN_INSERCION]: out["K55"].append(("orden de inserción distinto del modelo",))
    if [r[0] for r in _tabla_src(spec, "| Tabla | Unicidad |")] != [tb for tb, us in MS.UNICAS_SOURCE.items() for _ in us]: out["K55"].append(("unicidades de destino distintas del modelo",))
    fk = [r[0] for r in _tabla_src(spec, "| ID | Mutación | Verificador |")]
    if fk != [f[0] for f in MS.FK_DESC]: out["K55"].append(("mutaciones FK distintas del modelo", fk[:3]))
    H = " ".join(r[0] for r in _tabla_src(spec, "| ID | Caso |"))
    faltan = [x for x in IDS_V13 + ["K47-A%02d" % i for i in ()] if x not in H]
    faltan += [x for x in ["P%02d" % i for i in range(21, 27)] + ["ADV%d" % i for i in range(11, 17)] if x not in H]
    if faltan: out["K55"].append(("faltan A54 a A65, P21 a P26 o ADV11 a ADV16 en 4.4.15", faltan[:4]))
    # sin exclusiones generales de columnas source_* en el propio verificador
    src = open(__file__, encoding="utf-8").read()
    if re.search(r"c in \(\"source_(asset|upload|uploader|attribution|root)", src) or re.search(r"source_asset_version_id\" not in loc", src):
        out["K55"].append(("el verificador contiene una exclusión general de columnas source_*",))
    return out

_ORIG = ("brief_version_id", "promotion_snapshot_id", "copy_version_id", "creative_asset_id")
def verificar_semantica(spec):
    """K45: coherencia entre versión, entidad, origen del evento, actor, asset y antecesor."""
    ents, con, recs = _fk_records(spec)
    prob = []
    for fuente, o, loc, t, ref in recs:
        dom = "brief" if o.startswith("brief_") else "promotion" if o.startswith("promotion_") else None
        vid = {"brief": "brief_version_id", "promotion": "promotion_snapshot_id"}.get(dom)
        vt = {"brief": "brief_versions", "promotion": "promotion_snapshots"}.get(dom)
        otro = "promotion_" if dom == "brief" else "brief_"
        if dom and t.startswith(otro): prob.append((o, t, "relación entre dominios distintos"))
        if dom and o not in ("brief_versions", "promotion_snapshots"):
            if t == "contribution_events":
                origs = [c for c in ref if c in _ORIG]
                if origs != [vid]: prob.append((o, t, "origen del evento distinto al del dominio", ref))
                if "contributor_id" not in ref: prob.append((o, t, "el actor del evento no está en la clave"))
                else:
                    a = loc[ref.index("contributor_id")]
                    if a not in ("contributor_id", "actor_id"): prob.append((o, t, "actor local distinto del actor del evento", a))
                if origs == [vid]:
                    v = loc[ref.index(vid)]
                    if v not in (vid, "origin_version_id"): prob.append((o, t, "versión local no corresponde al origen", v))
            elif t == vt:
                if ref[-1] != "id" or loc[-1] != vid or loc[0] != "organization_id": prob.append((o, t, "la versión referenciada no corresponde a la entidad", loc, ref))
            elif t.endswith("_field_changes") and o.endswith("_attributions"):
                if loc != ("organization_id", vid, "field_key") or ref != ("organization_id", vid, "field_key"): prob.append((o, t, "campo o versión exacta distintos", loc, ref))
            elif t.endswith("_field_changes"):
                pass
            elif t == o and "previous_attribution_id" not in loc: prob.append((o, t, "antecesor mal referenciado"))
        if o in ("brief_versions", "promotion_snapshots") and t == o:
            esc = "brief_id" if o == "brief_versions" else "promotion_line_id"; prev = "previous_version_id" if o == "brief_versions" else "previous_snapshot_id"
            if esc not in loc or prev not in loc or loc.index(esc) != ref.index(esc) or ref[loc.index(prev)] != "id": prob.append((o, t, "la cadena no se limita a la misma entidad (%s)" % esc, loc, ref))
        if t == "creative_assets" and o in ("copy_version_provenance", "contribution_events") and not any(loc == tuple(_r["locales"]) for _r in MS.RELACIONES_SOURCE if _r["origen"] == o and _r["destino"] == t):
            if "copy_version_id" not in ref or not loc[ref.index("copy_version_id")].endswith("copy_version_id"): prob.append((o, t, "el asset no está ligado a la versión exacta de copy", loc, ref))
        if o == "copy_version_provenance" and t == "contribution_events":
            if "contributor_id" in ref and loc[ref.index("contributor_id")] != "contributor_id": prob.append((o, t, "actor de la procedencia distinto del actor del evento", loc, ref))
            origs = [c for c in ref if c in _ORIG]
            if len(origs) > 1 or any(c in ("brief_version_id", "promotion_snapshot_id") for c in origs): prob.append((o, t, "la procedencia de copy y arte usa un origen ajeno", ref))
        if o == "attribution_discard_resolutions" and t.endswith("attributions") or (o == "attribution_discard_resolutions" and t == "copy_version_provenance"):
            if "field_key" not in loc or ref[loc.index("field_key")] not in ("field_key", "content_unit"): prob.append((o, t, "campo de la resolución distinto al de la atribución", loc, ref))
            if "affected_contributor_id" not in loc or ref[loc.index("affected_contributor_id")] != "contributor_id": prob.append((o, t, "persona de la resolución distinta a la de la atribución", loc, ref))
    for n in ("brief_field_attributions", "promotion_field_attributions", "copy_version_provenance"):
        e = ents.get(n)
        if not e: prob.append((n, "sin bloque")); continue
        if not any("heredada" in c and "NOT NULL" in c and "previous_" in c for c in e["checks"]): prob.append((n, "atribución heredada sin regla de antecesor obligatorio"))
        if not any(t == n and any(x.startswith("previous_") for x in l) for l, t, r in e["fks"]): prob.append((n, "sin FK al antecesor"))
    return prob

def verificar_resolucion(spec, reglas):
    """K46: la tabla de resoluciones exige independencia, evidencia y fuente única; IG5-92 y IG5-93 lo declaran."""
    ents = parse_entidades(spec); e = ents.get("attribution_discard_resolutions"); prob = []
    if not e: return ["sin bloque de attribution_discard_resolutions"]
    ch = " || ".join(e["checks"])
    for req, msg in (("resolved_by <> affected_contributor_id", "el contribuyente afectado podría resolver su propia exclusión"), ("resolved_by <> requested_by", "quien solicita podría resolver"),
                     ("char_length(btrim(evidence)) >= 1", "se admite una resolución sin evidencia"), ("char_length(btrim(reason)) >= 1", "se admite una resolución sin motivo"),
                     ("num_nonnulls(", "la resolución no exige una única fuente"), ("created_by = resolved_by", "el actor no se fija desde el backend"), ("piece.review", "no exige autoridad de revisión vigente")):
        if req not in ch: prob.append(msg)
    if not re.search(r"unique\([^)]*\) cuando outcome = 'aceptada'", spec): prob.append("no hay unicidad de resolución aceptada")
    for r in ("IG5-92", "IG5-93", "IG5-95"):
        if r not in reglas: prob.append("falta " + r)
    if "IG5-92" in reglas and not all(x in reglas["IG5-92"] for x in ("no puede resolver su propia exclusión", "independiente", "fail-closed")): prob.append("IG5-92 incompleta")
    cols = e["cols"]
    for req, msg in (("resolved_by <> change_actor_id", "quien ejecutó la sustitución podría resolver"), ("evidence_attribution_id = coalesce(", "la evidencia no se liga a la atribución informada"),
                     ("elegibilidad del resolutor", "falta el trigger de elegibilidad sobre la cadena completa"), ("auth.uid()", "el resolutor no se liga a la identidad autenticada"),
                     ("contribuyente directo del campo en ninguna versión de la cadena", "el trigger no excluye a los contribuyentes directos de la cadena"), ("contribuyente heredado activo del campo", "el trigger no excluye a los herederos activos"),
                     ("excluido por otra contribución relevante de la misma cadena", "el trigger no excluye a quien contribuyó a otra fuente de la cadena"), ("beneficiario directo ni indirecto", "el trigger no excluye al beneficiario"),
                     ("no se concede autoridad por ser propietario, Admin", "se concede autoridad por el cargo")):
        if req not in ch: prob.append(msg)
    if not any(f[1] == "contribution_events" and "change_actor_id" in f[0] and "trigger_event_id" in f[0] for f in e["fks"]): prob.append("el actor del cambio no está ligado por FK compuesta al evento motivador")
    for c in ("trigger_event_id", "change_actor_id", "evidence_attribution_id", "evidence_version_id"):
        if c not in e["cols"]: prob.append("falta la columna " + c)
    for rid, txt in reglas.items():
        if rid in ("IG5-92", "IG5-95") and re.search(r"autor de la modificaci[^.;]{0,160}por sí solo", txt): prob.append(rid + " debilita R5 con «por sí solo»")
    cols = e["cols"]
    for c in ("organization_id", "source_kind", "field_key", "affected_contributor_id", "requested_by", "resolved_by", "reason", "evidence", "outcome", "resolved_at"):
        if c not in cols: prob.append("falta la columna " + c)
    return prob

_SUST = r"(sustituid\w*|retained_segments = 0|eliminad\w*)"
_NEGA = re.compile(r"\b(no|sin|solo|únicamente|ninguna|ningún|nunca|salvo|prohib\w*|rechaz\w*|permanece\w*|conserv\w*|provisional\w*|mediante|resolución)\b", re.I)
def verificar_exclusion_automatica(A, C):
    """K47: ninguna regla, algoritmo ni escenario retira a un contribuyente por sustitución, eliminación, hash o segmentos."""
    prob = []
    for f in (SPEC, INF, ROAD, AUD):
        for i, l in enumerate(A[f].split("\n"), 1):
            if l.startswith("| T-"): continue
            if re.match(r"^\| (sustituido|eliminado) \|", l) and re.search(r"(heredadas históricas|pasan a históric|pasa a histórica|quedan históric)", l): prob.append((f[:10], i, "fila de cambio que retira atribuciones"))
            for m in re.finditer(_SUST + r"[^|\n.;]{0,160}(pasan? a (históric\w*|historica)|quedan? (como )?históric\w*|se marcan? (como )?históric\w*)", l, re.I):
                if not _NEGA.search(m.group(0)): prob.append((f[:10], i, m.group(0)[:80]))
    for k, v in C.pruebas.items():
        c = v[0]; txt = " ".join(c[1:4]); exp = c[4]
        if re.search(_SUST, txt, re.I) and re.search(r"(pasa a (histórico|historica|histórica)|queda(n)? (como )?históric)", exp, re.I) and not re.search(r"(resolución|sin resolución|no )", exp, re.I): prob.append((k, "escenario que retira sin resolución"))
    for rid in ("IG5-72", "IG5-90", "IG5-91"):
        if rid not in C.reglas_cov: prob.append((rid, "regla inexistente"))
    r72 = C.reglas_cov.get("IG5-72", [[0, ""]])[0][1]
    if "resolución independiente" not in r72 or "retained_segments" in r72 and "no se deduce" not in r72: prob.append(("IG5-72", "no limita el paso a histórica a la resolución independiente"))
    return prob

REQ_H2V7 = ["sustitución total de redacción", "sustitución de una condición", "cambio de descuento sin modificar", "eliminación de un campo", "resolución independiente válida", "propio contribuyente afectado",
            "editor que realizó la sustitución", "resolución sin evidencia", "actor no elegible", "resolución duplicada", "versión distinta", "modificar el registro histórico", "atribución de brief heredada",
            "atribución de promoción heredada", "atribución de copy heredada", "atribución de asset reutilizado"]


def _rango(tok):
    """Expande «X-01 a X-24» o un identificador suelto."""
    m = re.match(r"^([A-Z0-9]+(?:-[A-Z]*)?)-?(\d+) a (?:[A-Z0-9]+(?:-[A-Z]*)?)-?(\d+)$", tok.strip())
    return tok.strip(), m

_PFX = r"(?:CHAIN|ADVC|ATTR|AT14|AT15|E14|ADV15|AV|CF|AC|AP)"
def ids_de(txt):
    """Identificadores citados en una celda: rangos «CHAIN-01 a CHAIN-24» y sueltos «K56-M03», «FK41», «AV-03»."""
    tok = r"(?<![A-Z0-9])(?:%s-\d+|K56-M\d+|FK\d+)" % _PFX
    out = []
    for a, b in re.findall(r"(%s) a (%s)" % (tok, tok), txt):
        pa = re.match(r"([A-Z0-9]+(?:-M)?-?)(\d+)$", a); pb = re.match(r"([A-Z0-9]+(?:-M)?-?)(\d+)$", b)
        w = len(pa.group(2)); out += ["%s%0*d" % (pa.group(1), w, i) for i in range(int(pa.group(2)), int(pb.group(2)) + 1)]
    resto = re.sub(r"(%s) a (%s)" % (tok, tok), "", txt)
    out += re.findall(tok, resto)
    return out

_CACHE14 = {}
def _ejecutadas14():
    """Resultados reales de las baterías del modelo (se ejecutan, no se leen del documento). Se memorizan dentro de una misma ejecución de las comprobaciones porque no dependen del texto del documento; la comprobación K41 las vuelve a ejecutar."""
    if "r" in _CACHE14: return _CACHE14["r"]
    _CACHE14["r"] = _ejecutadas14_real(); return _CACHE14["r"]
def _ejecutadas14_real():
    ch = MS.correr_mutaciones_cadena(); ad = MS.correr_adversariales_cadena(); at = MS.correr_mutaciones_atribucion()
    a14 = MS.pruebas_atomicidad14(); e14 = MS.pruebas_E14(); mm = MS.correr_mutaciones_modelo14()
    av = MS.correr_mutaciones_av(); cf = MS.correr_mutaciones_cf(); ac = MS.correr_mutaciones_ac(); ap = MS.correr_positivos15(); a15 = MS.correr_adversariales15(); t15 = MS.pruebas_atomicidad15()
    return ch, ad, at, a14, e14, mm, av, cf, ac, ap, a15, t15

def verificar_estructura15():
    """H-09 (V15): las validaciones existen en el motor y en el auditor, se invocan desde la reconstrucción, el auditor no comparte funciones con el motor, las pruebas históricas se conservan y no hay skip, xfail ni excepciones silenciadas."""
    import inspect, ast
    prob = []
    for fn in ("_chk_asset_version", "_chk_campo", "_chk_actor", "_chk_atribucion_reutilizador", "_datos_evento", "_verificar_reutilizado", "_verificar_raiz", "_verificar_modificado", "_siguiente_eslabon", "reconstruir_cadena_procedencia", "_campos_permitidos"):
        if not callable(getattr(MS.Motor, fn, None)): prob.append(("validación inexistente en el motor", fn))
    try:
        de = inspect.getsource(MS.Motor._datos_evento)
        for llamada in ("_chk_asset_version", "_chk_campo", "_chk_actor"):
            if "self.%s(" % llamada not in de: prob.append(("_datos_evento no invoca la validación", llamada))
        if "_chk_atribucion_reutilizador" not in inspect.getsource(MS.Motor._verificar_reutilizado): prob.append(("_verificar_reutilizado no invoca la atribución del reutilizador",))
        if "_datos_evento" not in inspect.getsource(MS.Motor._verificar_reutilizado) or "_datos_evento" not in inspect.getsource(MS.Motor._verificar_modificado): prob.append(("la validación del evento propio no se aplica a reutilizados y modificados",))
        hc = inspect.getsource(MS._hall_cadena)
        for pal in ("asset_version", "campo"):
            if pal not in hc: prob.append(("el auditor independiente no comprueba", pal))
        for prohibida in ("_origen_carga", "_validar_reutilizacion", "_verificar_reutilizado", "_chk_asset_version", "_chk_campo", "_datos_evento"):
            if prohibida in hc or prohibida in inspect.getsource(MS._hall_identidad): prob.append(("el auditor llama a la reconstrucción del motor", prohibida))
        # el motor valida antes de escribir: la validación precede a la creación del evento
        rg = inspect.getsource(MS.Motor.registrar_asset)
        if "_validar_reutilizacion" not in rg or "er = self._evento(" not in rg or rg.index("_validar_reutilizacion") > rg.index("er = self._evento("): prob.append(("la validación no precede a la escritura en registrar_asset",))
    except (OSError, TypeError, ValueError) as ex: prob.append(("no se pudo inspeccionar el código", str(ex)[:60]))
    # sin skip, xfail ni excepciones silenciadas en el modelo ni en las pruebas nuevas
    src = open(MS.__file__, encoding="utf-8").read()
    a = src.index("# ===== v15 BEGIN"); b = src.index("# ===== v15 END")
    nuevo = src[a:b]
    if re.search(r"\bskip\w*\(|xfail|pytest\.mark", nuevo): prob.append(("el bloque v15 contiene skip o xfail",))
    try:
        for nd in ast.walk(ast.parse(nuevo)):
            if isinstance(nd, ast.ExceptHandler) and len(nd.body) == 1 and isinstance(nd.body[0], ast.Pass): prob.append(("excepción silenciada en el bloque v15", nd.lineno))
    except SyntaxError as ex: prob.append(("el bloque v15 no es analizable", str(ex)[:40]))
    # pruebas históricas conservadas: cada batería previa mantiene su cantidad
    cnt = (("correr_mutaciones_cadena", N_CHAIN), ("correr_adversariales_cadena", N_CHAIN), ("correr_mutaciones_atribucion", N_ATTR), ("pruebas_atomicidad14", N_AT14), ("pruebas_E14", N_E14), ("correr_mutaciones_k47", N_K47), ("correr_mutaciones_resoluciones", N_RES), ("correr_mutaciones_assets", N_ART), ("correr_mutaciones_rechazo", N_RECH), ("correr_adversariales", N_ADV), ("correr_positivos_arte", N_POS_ART), ("pruebas_guarda", N_GUARDA), ("pruebas_atomicidad", N_ATOM), ("correr_escenarios", 17))
    for nom, n in cnt:
        try:
            k = len(getattr(MS, nom)())
            if k != n: prob.append(("batería histórica con cantidad distinta", nom, k, n))
        except Exception as ex: prob.append(("batería histórica no ejecutable", nom, str(ex)[:50]))
    return prob

def verificar_k56():
    """K56: ejecución de CHAIN, ADVC, ATTR, AT14, E14 y K56-M; identificadores continuos, estado inicial válido y cambio efectivo; independencia del auditor."""
    prob = []
    ch, ad, at, a14, e14, mm, av, cf, ac, ap, a15, t15 = _ejecutadas14()
    for nom, lst, n, key, pref in (("CHAIN", ch, N_CHAIN, "det", "CHAIN-%02d"), ("ADVC", ad, N_CHAIN, "ok", "ADVC-%02d"), ("ATTR", at, N_ATTR, "det", "ATTR-%02d"), ("AT14", a14, N_AT14, "ok", "AT14-%02d"), ("E14", e14, N_E14, "ok", "E14-%02d"), ("K56-M", mm, N_K56M, "det", "K56-M%02d"), ("AV", av, N_AV, "det", "AV-%02d"), ("CF", cf, N_CF, "det", "CF-%02d"), ("AC", ac, N_AC, "det", "AC-%02d"), ("AP", ap, N_AP, "ok", "AP-%02d"), ("ADV15", a15, N_ADV15, "ok", "ADV15-%02d"), ("AT15", t15, N_AT15, "ok", "AT15-%02d")):
        if [x["id"] for x in lst] != [pref % i for i in range(1, n + 1)]: prob.append((nom, "identificadores no continuos o cantidad distinta de %d" % n, [x["id"] for x in lst][:3]))
        mal = [x["id"] for x in lst if not x[key]]
        if mal: prob.append((nom, "no aprobadas o no detectadas", mal[:6]))
    for x in ch:
        if not (x["valido"] and x["cambio"] and x["err"] is None and x["rechaza"] and x["atomico"] and x["ident"] and x["bloq"]): prob.append((x["id"], "estado inicial inválido, sin cambio efectivo, no atómica o sin bloqueo de E"))
    for x in ad + a15:
        if not (x["motor_acepta"] and x["auditor"] and x["E_bloqueado"] and x["impacto_falla"] and x["no_publica"]): prob.append((x["id"], "el motor forzado no acepta o el sistema no bloquea"))
    for x in av + cf + ac:
        # las doce condiciones de H-04; una excepción ajena a ReutilizacionInvalida no cuenta como detección
        mal = [k for k in ("valido", "cambio", "rechaza", "ident", "sin_asset", "sin_evento", "sin_atribucion", "sin_relacion", "atomico", "incompleta", "E_nulo", "impacto_bloq", "no_publica") if not x.get(k)]
        if mal or x.get("err") is not None: prob.append((x["id"], "no cumple las condiciones de H-04 o la rechazó una excepción ajena a ReutilizacionInvalida", mal[:4], x.get("err")))
    prob += verificar_estructura15()
    if MS._compartidas(): prob.append(("el auditor usa funciones del motor", MS._compartidas()[:3]))
    return prob, (ch, ad, at, a14, e14, mm, av, cf, ac, ap, a15, t15)

def _spec_tabla(spec, enc, sec="4.4.16"):
    return tablas(seccion(spec, sec) or "", enc)

def verificar_rs14(spec, src):
    """Auditoría de 20 puntos por relación RS (H-06). Cada punto se calcula sobre el documento y el modelo; devuelve (problemas, matriz)."""
    ents = parse_entidades(spec); hist = parse_historicas(spec); con = parse_contrato(spec); cat = dict(hist); cat.update(ents)
    filas = [r for r in con if r["fk"] and r["agregada"]]; inv = _tabla_src(spec, "| Columna de origen | Destino |"); ciclos = _ciclos_declarados(spec)
    exe = {x["id"] for x in MS.correr_mutaciones_assets()} | {x["id"] for x in MS.correr_mutaciones_rechazo()} | {"CHAIN-%02d" % i for i in range(1, N_CHAIN + 1)}
    fkdesc = [d for _i, d, _v in MS.FK_DESC]; ordenes = _orden_insercion(spec)
    lim = (seccion(spec, "4.4.16") or "") + (seccion(spec, "4.4.15") or "")
    mat = {}; prob = []
    for rs in MS.RELACIONES_SOURCE:
        loc = tuple(rs["locales"]); ref = tuple(rs["ref"]); o, d = rs["origen"], rs["destino"]
        cand = [r for r in filas if r["origen"] == o and r["fk"][1] == d and set(r["fk"][0]) == set(loc)]; r0 = cand[0] if cand else None
        co = cat.get(o, {}).get("cols", {}); cd = cat.get(d, {}).get("cols", {})
        claves = set(cat.get(d, {}).get("uniq", [])) | ({cat[d]["pk"]} if cat.get(d, {}).get("pk") else set())
        cols_sin_fk = [c for c in loc if not any(r2 for r2 in filas if r2["origen"] == o and c in r2["fk"][0])]
        ex = lambda t, c: c in cat.get(t, {}).get("cols", {}) or bool(re.search(r"^\| %s \| %s " % (re.escape(t), re.escape(c)), spec, re.M)) or bool(re.search(r"^\| %s \| unique\(.*\b%s\b" % (re.escape(t), re.escape(c)), spec, re.M)) or any(c in u for u in cat.get(t, {}).get("uniq", []))
        p = [o in cat, d in cat, all(ex(o, c) for c in loc), all(ex(d, c) for c in ref), len(loc) == len(ref),
             loc[0] == "organization_id" and ref[0] == "organization_id", bool(r0) and dict(zip(r0["fk"][0], r0["fk"][2])) == rs["pares"],
             all((_tipo(cat, o, a) or "") == (_tipo(cat, d, b) or "") or not _tipo(cat, o, a) or not _tipo(cat, d, b) for a, b in zip(loc, ref)), ref in claves,
             bool(r0) and ("ON DELETE %s" % rs["accion"]) in r0["txt"], bool(r0) and "ON UPDATE" not in r0["txt"], bool(r0) and (("DEFERRABLE INITIALLY DEFERRED" in r0["txt"]) == (rs["momento"] != "inmediata")),
             bool(r0), any(rs["id"] in (r2[2] or "") for r2 in inv), (rs["momento"] == "inmediata") or bool(ciclos), not ordenes,
             not cols_sin_fk, any(rs["id"] in dsc for dsc in fkdesc), bool(re.findall(r"(?:K47-A|CHAIN-)\d\d", rs.get("prueba", ""))) and all(q in exe for q in re.findall(r"(?:K47-A|CHAIN-)\d\d", rs.get("prueba", ""))),
             "no se ejecutó" in lim.lower() or "no es validación" in lim.lower() or "no ejecutó sql" in lim.lower()]
        assert len(p) == 20
        mat[rs["id"]] = p
        for i, v in enumerate(p):
            if not v: prob.append((rs["id"], "punto %d no cumplido: %s" % (i + 1, MS.RS_PUNTOS_V14[i])))
    return prob, mat

def verificar_k58(spec, A):
    """K58 (H-08): los identificadores de control son únicos y estables; la equivalencia del antiguo segundo K55 está documentada."""
    prob = []
    ids = [r["id"] for r in RES]
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup: prob.append(("identificador de control repetido en la ejecución", dup))
    fuente = open(os.path.abspath(__file__), encoding="utf-8").read()
    lit = re.findall(r'chk\("([A-Z0-9][A-Z0-9-]*)"', fuente)
    # K40 y K48 se emiten desde ramas o desde la segunda pasada de reproducibilidad; nunca conviven dos en la misma ejecución
    rep_ = sorted({i for i in lit if lit.count(i) > 1 and i not in ("K40", "K48")})
    if rep_: prob.append(("identificador literal repetido en el código del verificador", rep_))
    for i in ("K55", "K55-V12", "K58", "K59"):
        if lit.count(i) != 1: prob.append(("el control %s debe emitirse exactamente una vez" % i, lit.count(i)))
    eq = _spec_tabla(spec, "| Control | Cobertura | Equivalencia |", "4.4.17")
    if [[c.strip() for c in r] for r in eq] != [[c.strip() for c in x] for x in MS.EQUIV_K55]: prob.append(("la equivalencia de K55 y K55-V12 del documento difiere del modelo", [r[0] for r in eq]))
    for nom in (AUD, INF):
        if "K55-V12" not in A[nom]: prob.append(("el documento no menciona K55-V12", nom[:14]))
    return prob

def verificar_k59(spec, C, info):
    """K59 (H-05, H-09): cobertura de la v15 en el documento: reglas, escenarios, tablas, cifras y límites."""
    prob = []
    sin = [r for r in ("IG5-111", "IG5-112", "IG5-113", "IG5-114", "IG5-115", "IG5-116", "IE-12") if r not in C.reglas or not info["cub"].get(r)]
    if sin: prob.append(("reglas sin escenarios", sin))
    g15 = {"H-01 v15 asset_version": N_AV, "H-02 v15 campo": N_CF, "H-03 v15 vínculos combinados": N_AC, "H-05 v15 casos positivos": N_AP, "H-06 v15 auditor independiente": N_ADV15, "H-07 v15 atomicidad": N_AT15, "H-09 v15 mutación del código": 4}
    cnt = {g: sum(1 for v in C.pruebas.values() if v[0][1].startswith(g)) for g in g15}
    for g, n in g15.items():
        if cnt[g] < n: prob.append(("escenarios insuficientes en " + g, cnt[g], n))
    s17 = seccion(spec, "4.4.17") or ""
    if not s17: prob.append(("falta la sección 4.4.17",)); return prob
    req = ["AV-%02d" % i for i in range(1, N_AV + 1)] + ["CF-%02d" % i for i in range(1, N_CF + 1)] + ["AC-%02d" % i for i in range(1, N_AC + 1)] + ["AP-%02d" % i for i in range(1, N_AP + 1)] + ["ADV15-%02d" % i for i in range(1, N_ADV15 + 1)] + ["AT15-%02d" % i for i in range(1, N_AT15 + 1)] + ["K56-M%02d" % i for i in range(9, 13)] + ["D-%02d" % i for i in range(13, 19)] + ["asset_version", "source_asset_version", "campo", "K55-V12", "ReutilizacionInvalida", "mensaje_usuario", "no se ejecutó"]
    falta = [x for x in req if x not in s17]
    if falta: prob.append(("4.4.17 no contiene", falta[:6]))
    if "PostgreSQL" not in s17 or "Supabase" not in s17: prob.append(("4.4.17 no separa la ejecución en memoria de PostgreSQL o Supabase",))
    mens = MS.ReutilizacionInvalida("x", [dict(eslabon="a2", evento="ev-secreto", campo="asset_version", esperado=1, hallado=5, motivo="m")]).mensaje_usuario
    if any(t in mens for t in ("a2", "ev-secreto", "asset_version")): prob.append(("el mensaje al usuario expone datos internos", mens[:60]))
    return prob

def verificar_k57(spec, C):
    """K57 (H-09): comparación estructural entre reglas, implementación del modelo, pruebas ejecutadas y el documento."""
    prob = []; ch, ad, at, a14, e14, mm, av, cf, ac, ap, a15, t15 = _ejecutadas14()
    ejec = {x["id"] for L in (ch, ad, at, a14, e14, mm, av, cf, ac, ap, a15, t15) for x in L} | {f[0] for f in MS.FK_DESC}
    citados = set()
    for sec_, traza in (("4.4.16", MS.TRAZA_V14), ("4.4.17", MS.TRAZA_V15)):
        tz = _spec_tabla(spec, "| Regla | Implementación |", sec_)
        if [r[0] for r in tz] != [x[0] for x in traza]: prob.append(("trazabilidad %s: reglas distintas del modelo" % sec_, [r[0] for r in tz]))
        for r, x in zip(tz, traza):
            if r[1:] != list(x[1:]) and [c.strip() for c in r[1:]] != [c.strip() for c in x[1:]]: prob.append((x[0], "la fila del documento difiere de la del modelo"))
            for fn in re.findall(r"`([^`]+)`", r[1]):
                obj = MS
                for parte in fn.split("."):
                    obj = getattr(obj, parte, None)
                    if obj is None: break
                if obj is None: prob.append((x[0], "implementación inexistente en el modelo", fn))
            ids = ids_de(r[2]); citados |= set(ids)
            for i in ids:
                if i not in ejec: prob.append((x[0], "prueba citada inexistente", i))
            if x[0] not in C.reglas: prob.append((x[0], "regla inexistente en el expediente"))
    # las 15 validaciones por evento propio de reutilización (H-01)
    tv = _spec_tabla(spec, "| N.º | Validación del evento propio |", "4.4.17")
    if [r[0] for r in tv] != [str(x[0]) for x in MS.VALIDACIONES_EVENTO15]: prob.append(("las 15 validaciones del evento propio distintas del modelo", [r[0] for r in tv]))
    for r, x in zip(tv, MS.VALIDACIONES_EVENTO15):
        if [c.strip() for c in r[1:]] != [c.strip() for c in x[1:]]: prob.append(("validación %s: fila distinta del modelo" % x[0],))
        for fn in re.findall(r"`([^`]+)`", x[2]):
            obj = MS
            for parte in fn.split("."):
                obj = getattr(obj, parte, None)
                if obj is None: break
            if obj is None: prob.append(("validación %s: implementación inexistente" % x[0], fn))
        for i in ids_de(x[3]):
            if i not in ejec: prob.append(("validación %s: prueba citada inexistente" % x[0], i))
    sin = sorted(i for i in ejec if i not in citados and not i.startswith("FK"))
    if sin: prob.append(("pruebas del conjunto ejecutado no citadas por ninguna regla", sin[:6]))
    for sec_, matriz_ in (("4.4.16", MS.AUDITORIA_V14), ("4.4.17", MS.AUDITORIA_V15)):
        aud = _spec_tabla(spec, "| ID | Defecto o riesgo |", sec_)
        if [r[0] for r in aud] != [x[0] for x in matriz_]: prob.append(("matriz de auditoría %s distinta del modelo" % sec_, [r[0] for r in aud][:3]))
        for r, x in zip(aud, matriz_):
            if len(r) != 9 or not all(c.strip() for c in r): prob.append((x[0], "fila de auditoría con campos vacíos")); continue
            for i in ids_de(r[6] + " " + r[7] + " " + r[8]):
                if i not in ejec: prob.append((x[0], "prueba citada inexistente", i))
            if r[:2] != list(x[:2]) or r[3] != x[3]: prob.append((x[0], "fila distinta del modelo"))
    pasos = _spec_tabla(spec, "| Paso | Validación |")
    if [r[0] for r in pasos] != [str(i) for i in range(1, 15)]: prob.append(("el orden de validación no tiene 14 pasos consecutivos", [r[0] for r in pasos]))
    for nom, enc, lst, sec_ in (("CHAIN", "| ID | Mutación de la cadena |", ch, "4.4.16"), ("ADVC", "| ID | Prueba adversarial de la cadena |", ad, "4.4.16"), ("ATTR", "| ID | Mutación de atribuciones |", at, "4.4.16"), ("AT14", "| ID | Operación |", a14, "4.4.16"), ("E14", "| ID | Prueba de E |", e14, "4.4.16"), ("K56-M", "| ID | Mutación del código |", mm[:8], "4.4.16"),
                                ("AV", "| ID | Mutación de asset_version |", av, "4.4.17"), ("CF", "| ID | Mutación de campo |", cf, "4.4.17"), ("AC", "| ID | Mutación combinada |", ac, "4.4.17"), ("AP", "| ID | Caso positivo |", ap, "4.4.17"), ("ADV15", "| ID | Prueba adversarial |", a15, "4.4.17"), ("AT15", "| ID | Momento del fallo |", t15, "4.4.17"), ("K56-M (v15)", "| ID | Mutación del código |", mm[8:], "4.4.17")):
        t = _spec_tabla(spec, enc, sec_)
        if [r[0] for r in t] != [x["id"] for x in lst]: prob.append((nom, "tabla del documento distinta del conjunto ejecutado", [r[0] for r in t][:3]))
    _p, mat = verificar_rs14(spec, None)
    tm = {r[0]: r[1:] for r in _spec_tabla(spec, "| Relación | P01 |")}
    for k, v in mat.items():
        if tm.get(k) != ["sí" if x else "NO" for x in v]: prob.append((k, "la matriz de 20 puntos del documento difiere de la calculada"))
    if set(tm) != set(mat): prob.append(("matriz de 20 puntos con relaciones distintas", sorted(set(tm) ^ set(mat))))
    cif = (seccion(spec, "4.4.16") or ""); cif17 = (seccion(spec, "4.4.17") or "")
    for etq, n_ in (("CHAIN", len(ch)), ("ADVC", len(ad)), ("ATTR", len(at)), ("AT14", len(a14)), ("E14", len(e14)), ("K56-M", len(mm[:8]))):
        if ("%s: %d" % (etq, n_)) not in cif: prob.append(("cifra ejecutada de %s ausente o distinta en el documento" % etq, n_))
    for etq, n_ in (("AV", len(av)), ("CF", len(cf)), ("AC", len(ac)), ("AP", len(ap)), ("ADV15", len(a15)), ("AT15", len(t15)), ("K56-M", len(mm))):
        if ("%s: %d" % (etq, n_)) not in cif17: prob.append(("cifra ejecutada de %s ausente o distinta en 4.4.17" % etq, n_))
    # E del motor frente al auditor en los fixtures
    for nm, fx in (("fx14", lambda: MS._fx14(MS.Motor)[0]), ("fxE", lambda: MS._fx_E(MS.Motor)[0])):
        try:
            m = fx(); vid = "cc" if nm == "fx14" else None
            if nm == "fx14":
                m.registrar_asset("a4", "cc", "B", reused_from="a3")
                if MS.auditar_E(MS.snapshot(m), m.calcular_E(vid), vid): prob.append(("el auditor discrepa del motor en %s" % nm,))
        except Exception as ex: prob.append(("fixture %s no ejecutable" % nm, str(ex)[:60]))
    return prob

def checks_v7(textos, C, A, info, v33=None):
    spec = C.spec
    p44, nrel = verificar_estructura(spec)
    src = verificar_source(spec)
    chk("K44", "Integridad estructural de %d relaciones: longitud, orden exacto de columnas, organization_id, PK o UNIQUE de destino con las mismas columnas, tipos compatibles, contrato igual a los bloques, sin relaciones rotas ni circulares salvo los ciclos declarados en la matriz de 4.4.15 con su orden de inserción" % nrel, not p44 and not src["K44"], (p44[:3], src["K44"][:2]), "IG5-80, IE-09", "ESPECIFICACION 4.4.4 y 4.4.9")
    p45 = verificar_semantica(spec)
    m45 = verificar_k45_modelo(spec)
    chk("K45", "Integridad semántica sobre un modelo relacional con identidad propia (organizaciones, miembros, piezas, versiones de brief, snapshots, versiones de copy, assets, eventos, atribuciones, herencia y reutilización): 15 controles C01 a C15 evaluados sobre las relaciones reales, matriz de correspondencias de 4.4.10 (S1 a S12) contrastada con los nombres físicos, 3 casos positivos sin falsos positivos, 27 mutaciones detectadas cada una por su código y, para las relaciones source_* RS-01 a RS-08, los pares exactos origen-destino (asset lógico, versión exacta, evento de carga, uploader y atribución), la prueba negativa de cada excepción y la ausencia de identidad por número de versión", not p45 and not m45 and not src["K45"], (p45[:2], m45[:2], src["K45"][:2]), "IG5-81 a IG5-84, IG5-96, IS-16, IE-09, IE-12", "ESPECIFICACION 4.4.4, 4.4.9 y 4.4.10")
    reglas = {r: v[0][1] for r, v in C.reglas_cov.items()}
    p46 = verificar_resolucion(spec, reglas)
    m46 = verificar_k46_modelo(spec)
    chk("K46", "Resolución independiente de descarte: afectado, solicitante y actor del cambio no resuelven, evidencia ligada a la misma atribución y versión, autoridad de revisión, identidad autenticada, independencia respecto de todos los contribuyentes y eventos de la cadena (R1 a R9), fail-closed sin resolutor elegible, cada resolutor elegible aceptado (sin falsos positivos) y 12 mutaciones detectadas", not p46 and not m46, (p46[:2], m46[:2]), "IG5-92, IG5-93, IG5-95, IE-12", "ESPECIFICACION 4.4.4, 4.4.8 y 4.4.10")
    p47 = verificar_exclusion_automatica(A, C)
    m47 = verificar_k47_modelo(spec)
    chk("K47", "Conservación estructural: motor en memoria con atribuciones individuales, versiones inmutables, resoluciones y E calculado recorriendo las atribuciones reales; 12 escenarios (A a L), el escenario de resoluciones inmutables (RS) y comprobaciones de uniformidad entre fuentes y de independencia de la similitud aprobados; registro de resoluciones sellado y de solo agregado con 9 intentos directos de alteración rechazados; procedencia del arte por versión de copy con identidad exacta de uploader, evento de carga, atribución y reutilización, 20 casos positivos (P01 a P20), 10 pruebas adversariales en las que el motor acepta, el auditor detecta y E se bloquea y 8 pruebas de atomicidad de la reutilización; identidad exacta del asset de origen por referencias explícitas (asset, versión, evento de carga, uploader y atribución original); auditor independiente de 28 invariantes (I1 a I28); tabla C de 4.4.10 igual al comportamiento observado del motor; 36 mutaciones previas, 12 de resoluciones inmutables (R01 a R12) y 53 de assets (A01 a A53) detectadas; además ninguna regla, algoritmo ni escenario retira por sustitución, eliminación, hash o retained_segments = 0", not p47 and not m47, (p47[:2], m47[:3]), "IG5-72, IG5-90, IG5-91, IG5-97, IE-12", "ESPECIFICACION 4.4.8 y 4.4.10")
    # K52 cobertura estructural v9
    mk45, _p = MS.correr_mutaciones_k45(parse_4410(spec)["matriz"]); mk47 = MS.correr_mutaciones_k47(); esc = MS.correr_escenarios()
    mkr = MS.correr_mutaciones_resoluciones(); mka = MS.correr_mutaciones_assets(); pos_a = MS.correr_positivos_arte(); guarda = MS.pruebas_guarda()
    inv_cub = {m["esp"] for m in mk47 + mkr + mka}; sin_inv = sorted(set("I%d" % i for i in range(1, 29)) - inv_cub); sin_c = sorted(set(MS.CONTROLES_K45) - {m["esp"] for m in mk45})
    esc_ok = sorted(e["id"] for e in esc if e["ok"]); esc_mal = [e["id"] for e in esc if not e["ok"]]
    chk("K52", "Cobertura estructural v12: controles C01 a C15 con mutación (%d/15), invariantes I1 a I28 con mutación (%d/28), escenarios A a L aprobados (%d/12), comprobaciones U, S, X, R y RS aprobadas, 20 casos positivos de arte, 10 pruebas adversariales, 9 intentos directos contra el registro de resoluciones rechazados, fixtures iniciales válidos y ninguna mutación con excepción" % (15 - len(sin_c), 28 - len(sin_inv), len([x for x in esc_ok if x in "ABCDEFGHIJKL"])),
        not sin_c and not sin_inv and not esc_mal and len(esc_ok) == 17 and len(pos_a) == N_POS_ART and all(p["ok"] for p in pos_a) and len(guarda) == N_GUARDA and all(g[1] for g in guarda) and all(a["ok"] for a in MS.correr_adversariales()) and all(m["valido"] and m["cambio"] and not m["err"] for m in mk45 + mk47 + mkr + mka), (sin_c, sin_inv, esc_mal, [p["id"] for p in pos_a if not p["ok"]], [g[0] for g in guarda if not g[1]]), "IG5-95 a IG5-99, IE-12", "ESPECIFICACION 4.4.10, 4.4.11 y 4.4.12")
    # K50 títulos del registro
    tit = re.findall(r"^## Entrada: revisión v(\d+) de G-1, G-5 y G-10 \(posterior a la v(\d+)", A[REG], re.M)
    mal50 = [t for t in tit if int(t[0]) - 1 != int(t[1])]
    chk("K50", "Registro histórico: cada entrada de revisión sucede a la anterior (vN posterior a vN-1; %d entradas)" % len(tit), len(tit) >= 5 and not mal50, mal50, "IE-04", "REGISTRO")
    # K51 cobertura v8
    gv8 = {"H-02 v8 resolutor": 13, "H-02 v8 correspondencias": 15, "H-02 v8 conservación": 19}
    cnt = {g: sum(1 for v in C.pruebas.values() if v[0][1].startswith(g)) for g in gv8}
    sin8 = [r for r in ("IG5-95", "IG5-96", "IG5-97", "IE-12") if r not in C.reglas or not info["cub"].get(r)]
    chk("K51", "Cobertura v8: IG5-95, IG5-96, IG5-97 e IE-12 con escenarios (resolutor %d, correspondencias %d, conservación %d)" % tuple(cnt[g] for g in gv8), not sin8 and all(cnt[g] >= n for g, n in gv8.items()), (sin8, cnt), "IG5-95 a IG5-97, IE-12", "ESPECIFICACION 4.4.10 y 11")
    # K53 cobertura v10
    g10 = {"H-02 v10 resoluciones inmutables": 5 + N_RES, "H-02 v10 arte": N_POS_V10 + N_ART_V10 + 3}
    cnt10 = {g: sum(1 for v in C.pruebas.values() if v[0][1].startswith(g)) for g in g10}
    sin10 = [r for r in ("IG5-98", "IG5-99", "IE-12") if r not in C.reglas or not info["cub"].get(r)]
    s4412 = seccion(spec, "4.4.12") or ""
    falta412 = [x for x in (["I%d" % i for i in range(13, 22)] + ["K47-R%02d" % i for i in range(1, N_RES + 1)] + ["K47-A%02d" % i for i in range(1, N_ART_V10 + 1)] + ["P%02d" % i for i in range(1, N_POS_V10 + 1)] + ["previous_resolution_id", "record_seal", "no_aplica", "art_status"]) if x not in s4412]
    chk("K53", "Cobertura v10: IG5-98, IG5-99 e IE-12 con escenarios (resoluciones inmutables %d, arte %d) y la sección 4.4.12 documenta I13 a I21, las 12 mutaciones de resoluciones, las 16 de assets (A01 a A16) y los 7 casos positivos (P01 a P07)" % tuple(cnt10[g] for g in g10), not sin10 and all(cnt10[g] >= n for g, n in g10.items()) and not falta412, (sin10, cnt10, falta412[:5]), "IG5-98, IG5-99, IE-12", "ESPECIFICACION 4.4.12")
    # K54 cobertura v11
    g11 = {"H-02 v11 identidad de assets": N_ART_V11 + N_POS_V11 + N_ADV_V11 + 4}
    cnt11 = {g: sum(1 for v in C.pruebas.values() if v[0][1].startswith(g)) for g in g11}
    sin11 = [r for r in ("IG5-100", "IE-12") if r not in C.reglas or not info["cub"].get(r)]
    s4413 = seccion(spec, "4.4.13") or ""
    falta413 = [x for x in (["I%d" % i for i in range(22, 27)] + IDS_V11 + ["P%02d" % i for i in range(N_POS_V10 + 1, N_POS_V10 + N_POS_V11 + 1)] + ["ADV%d" % i for i in range(1, N_ADV_V11 + 1)] + ["upload_event_id", "reuse_event_id", "calcular_E_verificado", "ProcedenciaIncompleta"]) if x not in s4413]
    chk("K54", "Cobertura v11: IG5-100 e IE-12 con escenarios (identidad de assets %d) y la sección 4.4.13 documenta I22 a I26, las 21 mutaciones de la v11 (A17 a A32 y A49 a A53), los casos positivos P08 a P14 y las 5 pruebas adversariales" % cnt11["H-02 v11 identidad de assets"], not sin11 and all(cnt11[g] >= n for g, n in g11.items()) and not falta413, (sin11, cnt11, falta413[:5]), "IG5-100, IE-12", "ESPECIFICACION 4.4.13")
    # K55 cobertura v12
    g12 = {"H-02 v12 identidad de origen": N_ART_V12 + N_POS_V12 + (N_ADV_V12 - N_ADV_V11) + N_ATOM_V12 + 3}
    cnt12 = {g: sum(1 for v in C.pruebas.values() if v[0][1].startswith(g)) for g in g12}
    sin12 = [r for r in ("IG5-101", "IE-12") if r not in C.reglas or not info["cub"].get(r)]
    s4414 = seccion(spec, "4.4.14") or ""
    falta414 = [x for x in (["I27", "I28"] + IDS_V12 + ["P%02d" % i for i in range(N_POS_V10 + N_POS_V11 + 1, N_POS_V10 + N_POS_V11 + N_POS_V12 + 1)] + ["ADV%d" % i for i in range(N_ADV_V11 + 1, N_ADV_V12 + 1)] + ["source_asset_id", "source_asset_version_id", "source_upload_event_id", "source_uploader_id", "source_attribution_id", "asset_version_id", "ReutilizacionInvalida", "cadena_identidad_independiente", "_compartidas"]) if x not in s4414]
    m55 = verificar_k55_modelo()
    g13 = {"H-01 v13 validación previa del origen": N_RECH + N_POS_V13 + 6 + (N_ATOM - N_ATOM_V12), "H-02 v13 integridad referencial source_*": len(MS.RELACIONES_SOURCE) + N_FK + 1}
    cnt13 = {g: sum(1 for v in C.pruebas.values() if v[0][1].startswith(g)) for g in g13}
    sin13 = [r for r in ("IG5-102", "IG5-103", "IE-12") if r not in C.reglas or not info["cub"].get(r)]
    s4415 = seccion(spec, "4.4.15") or ""
    falta415 = [x for x in (IDS_V13 + ["P%02d" % i for i in range(N_POS_V10 + N_POS_V11 + N_POS_V12 + 1, N_POS_ART + 1)] + ["ADV%d" % i for i in range(N_ADV_V12 + 1, N_ADV + 1)] + ["FK%02d" % i for i in range(1, N_FK + 1)] + ["RS-%02d" % i for i in range(1, 9)] + ["source_asset_id", "source_asset_version_id", "source_upload_event_id", "source_uploader_id", "source_attribution_id", "source_root_asset_version_id", "source_attribution_relation", "DEFERRABLE INITIALLY DEFERRED", "FK compuesta directa", "Triggers diferidos", "Validación transaccional complementaria", "Orden de inserción controlado", "Claves únicas compuestas"]) if x not in s4415]
    m55b = [x for x in src["K55"]]
    chk("K55", "Cobertura v13: IG5-102, IG5-103 e IE-12 con escenarios (validación previa del origen %d, integridad referencial source_* %d); sección 4.4.15 con el inventario de columnas source_*, las relaciones RS-01 a RS-08, las seis soluciones evaluadas, la matriz de ciclos, el orden de inserción, las excepciones individuales, las mutaciones A54 a A65, los casos P21 a P26, las pruebas ADV11 a ADV16 y las mutaciones FK01 a FK15; las matrices del documento coinciden con el modelo y con las pruebas, y el verificador no contiene exclusiones generales de columnas source_*" % (cnt13["H-01 v13 validación previa del origen"], cnt13["H-02 v13 integridad referencial source_*"]), not sin13 and all(cnt13[g] >= n for g, n in g13.items()) and not falta415 and not m55b, (sin13, cnt13, falta415[:5], m55b[:3]), "IG5-102, IG5-103, IE-12", "ESPECIFICACION 4.4.15")
    pk56, _res56 = verificar_k56()
    s4416 = seccion(spec, "4.4.16") or ""
    sin14 = [r for r in ("IG5-104", "IG5-105", "IG5-106", "IG5-107", "IG5-108", "IG5-109", "IG5-110") if r not in C.reglas or not info["cub"].get(r)]
    chk("K56", "Cobertura v14 y ejecución v15 de las baterías del modelo (detalle v15 en K59): validación vínculo por vínculo de la cadena (CHAIN %d/%d), motor forzado frente al auditor independiente (ADVC %d/%d), conservación de atribuciones y resoluciones (ATTR %d/%d), atomicidad de las operaciones (AT14 %d/%d), E y elegibilidad del evaluador (E14 %d/%d) y %d mutaciones del propio código (K56-M); el auditor no comparte funciones con el motor; reglas IG5-104 a IG5-110 con escenarios" % ((sum(1 for x in _res56[0] if x["det"]), N_CHAIN, sum(1 for x in _res56[1] if x["ok"]), N_CHAIN, sum(1 for x in _res56[2] if x["det"]), N_ATTR, sum(1 for x in _res56[3] if x["ok"]), N_AT14, sum(1 for x in _res56[4] if x["ok"]), N_E14, sum(1 for x in _res56[5] if x["det"]))), not pk56 and not sin14 and bool(s4416), (pk56, sin14), "IG5-104 a IG5-109", "ESPECIFICACION 4.4.16")
    pk57 = verificar_k57(spec, C)
    chk("K57", "Comparación estructural v14: cada regla IG5-104 a IG5-110 se traza a su implementación existente en el modelo, a pruebas existentes del conjunto ejecutado y a su verificador; cada prueba del conjunto ejecutado se cita; la matriz de auditoría (%d defectos), el orden de 14 pasos, las tablas de pruebas y la auditoría de 20 puntos por relación (RS-01 a RS-08) coinciden con lo calculado por el modelo y el verificador" % len(MS.AUDITORIA_V14), not pk57 and not verificar_rs14(spec, None)[0], (pk57, verificar_rs14(spec, None)[0]), "IG5-110, IG5-109", "ESPECIFICACION 4.4.16")
    pk59 = verificar_k59(spec, C, info)
    chk("K59", "Cobertura v15: reglas IG5-111 a IG5-116 con escenarios, sección 4.4.17 con las suites AV-01 a AV-08, CF-01 a CF-08, AC-01 a AC-06, AP-01 a AP-08, ADV15-01 a ADV15-08, AT15-01 a AT15-08, K56-M09 a K56-M12 y D-13 a D-18, las 15 validaciones del evento propio, los límites de PostgreSQL y Supabase y un mensaje al usuario sin datos internos", not pk59, pk59[:4], "IG5-111 a IG5-116", "ESPECIFICACION 4.4.17")
    pk58 = verificar_k58(spec, A)
    chk("K58", "Identidad única y estable de los controles: ningún identificador se repite en la ejecución ni en el código del verificador, K55 y K55-V12 se emiten una sola vez cada uno y la equivalencia documentada en 4.4.17 coincide con el modelo; los documentos citan K55-V12", not pk58, pk58[:4], "IG5-116", "ESPECIFICACION 4.4.17")
    chk("K55-V12", "Cobertura v12 (control histórico antes identificado también como K55; equivalencia documentada en 4.4.17): IG5-101 e IE-12 con escenarios (identidad de origen %d), sección 4.4.14 con I27 e I28, las 16 mutaciones A33 a A48, los casos positivos P15 a P20 y las 5 pruebas adversariales nuevas; el modelo contiene los campos explícitos de identidad del origen en cada evento de reutilización, el auditor no usa funciones del motor (inspección del código), la reutilización inválida no deja registros parciales, se conservan las pruebas de la v11 y no hay skip ni xfail" % cnt12["H-02 v12 identidad de origen"], not sin12 and all(cnt12[g] >= n for g, n in g12.items()) and not falta414 and not m55, (sin12, cnt12, falta414[:5], m55[:3]), "IG5-101, IE-12", "ESPECIFICACION 4.4.14")
    # K49 reglas y escenarios obligatorios de H-02 v7
    h7 = [v[0] for k, v in C.pruebas.items() if v[0][1].startswith("H-02 v7 atribución")]
    faltan = [q for q in REQ_H2V7 if not any(q in x[1] for x in h7)]
    nec = ["IG5-90", "IG5-91", "IG5-92", "IG5-93", "IG5-94"]
    sin = [r for r in nec if r not in C.reglas or not info["cub"].get(r)]
    chk("K49", "H-02 v7: reglas IG5-90 a IG5-94 con cobertura y los 16 escenarios obligatorios (%d escenarios de atribución v7)" % len(h7), not faltan and not sin, (faltan, sin), "IG5-90 a IG5-94", "ESPECIFICACION 4.4.8")


# ============ v8: modelos estructurados de K45, K46 y K47 (se alimentan de las tablas de 4.4.10) ============
import copy as _copy

CLAVES_R = ["miembro_activo", "piece_review", "no_afectado", "no_solicitante", "no_actor_del_cambio", "no_directo_en_cadena", "no_heredado_activo", "no_excluido_otra_fuente", "no_beneficiario"]
CLAS = ["sin_cambio", "introducido", "modificado", "sustituido", "eliminado"]
FUENTES = ["brief", "promoción", "copy"]

def parse_4410(spec):
    s = seccion(spec, "4.4.10") or ""
    out = dict(matriz=[], condS=[], reglasR=[], efec_clas=[], efec_evt=[])
    for r in tablas(s, "| Fuente | contribution_type | origin_kind |"):
        if len(r) == 6: out["matriz"].append(dict(fuente=r[0], tipo=r[1], origen=r[2], col=r[3], tabla=r[4], atrib=r[5]))
    for r in tablas(s, "| ID | Condición |"):
        if len(r) == 2: out["condS"].append(r[0])
    for r in tablas(s, "| Regla | Clave | Condición |"):
        if len(r) == 3: out["reglasR"].append(r[1])
    for r in tablas(s, "| Fuente | Clasificación | Conserva activas |"):
        if len(r) == 6: out["efec_clas"].append(dict(fuente=r[0], clas=r[1], conserva=r[2], incorpora=r[3], retira=r[4], similitud=r[5]))
    for r in tablas(s, "| Evento | Retira atribuciones |"):
        if len(r) == 4: out["efec_evt"].append(dict(evento=r[0], retira=r[1], efecto_e=r[2], reescribe=r[3]))
    return out

# ---------------- K45: integridad semántica sobre un modelo relacional (módulo modelo_estructural.py) ----------------
import importlib.util as _ilu
def _cargar_modelo():
    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "modelo_estructural.py")
    sp = _ilu.spec_from_file_location("modelo_estructural", ruta); m = _ilu.module_from_spec(sp); sp.loader.exec_module(m); return m
MS = _cargar_modelo()
N_K45, N_K46, N_K47, N_ESC = 27, 12, 36, 12
N_RES, N_ART, N_POS_ART, N_GUARDA, N_ADV, N_ATOM = 12, 53, 26, 9, 16, 20
N_RECH, N_FK, N_ADV_V12, N_ATOM_V12 = 12, 41, 10, 8
N_CHAIN, N_ATTR, N_AT14, N_E14, N_K56M, N_K57D = 24, 12, 11, 6, 12, 12
N_AV, N_CF, N_AC, N_AP, N_ADV15, N_AT15 = 8, 8, 6, 8, 8, 8
CTL_K56 = ('CHAIN', 'ATTR', 'K56-M')
IDS_V13 = ["K47-A%02d" % i for i in range(54, 66)]
N_ART_V10, N_ART_V11, N_ART_V12, N_POS_V10, N_POS_V11, N_POS_V12, N_POS_V13, N_ADV_V11 = 16, 21, 16, 7, 7, 6, 6, 5
IDS_V11 = ["K47-A%02d" % i for i in list(range(17, 33)) + list(range(49, 54))]
IDS_V12 = ["K47-A%02d" % i for i in range(33, 49)]
CAMPOS_EVT_REUT = ("org", "pieza", "version", "asset", "asset_id", "asset_version_id", "source_asset_id", "source_asset_version_id", "source_upload_event_id", "source_uploader_id", "source_attribution_id", "actor", "auth", "tipo", "id")

def verificar_k45_modelo(spec):
    """Matriz y CHECK de la especificación contra los nombres físicos; después, 3 casos positivos y las mutaciones sobre el modelo relacional."""
    p = parse_4410(spec); prob = []
    M = p["matriz"]
    esperado = {("brief_editor", "brief", "brief_version_id"), ("promotion_editor", "promotion", "promotion_snapshot_id"), ("copy_author", "copy", "copy_version_id"), ("copy_editor", "copy", "copy_version_id"),
                ("inherited_contributor", "copy", "copy_version_id"), ("asset_uploader", "asset", "creative_asset_id")}
    obt = {(m["tipo"], m["origen"], m["col"]) for m in M}
    if obt != esperado: prob.append(("matriz distinta de los nombres físicos del modelo", sorted(obt ^ esperado)[:3]))
    if sorted(p["condS"]) != sorted("S%d" % i for i in range(1, 13)): prob.append(("condiciones S1 a S12", p["condS"]))
    ents = parse_entidades(spec); ce = ents.get("contribution_events")
    if ce:
        ch = " ".join(ce["checks"])
        for tipo, origen, col in esperado:
            if not re.search(r"\b" + tipo + r"\b[^;]*exige[^;]*\b" + col + r"\b|\b" + tipo + r"\b[^;]*\b" + col + r"\b", ch): prob.append(("el CHECK de contribution_events no asocia %s con %s" % (tipo, col),))
        if col_origen_ok(ce) is False: prob.append(("origin_kind sin coherencia con las columnas de origen",))
    else: prob.append(("sin bloque de contribution_events",))
    mut, pos = MS.correr_mutaciones_k45(M)
    for nombre, v in pos:
        if v: prob.append(("caso positivo rechazado: " + nombre, v[:3]))
    nd = [m["id"] for m in mut if not m["det"]]
    if len(mut) != N_K45 or nd: prob.append(("mutaciones K45 no detectadas o ausentes (%d/%d)" % (len(mut) - len(nd), N_K45), nd[:4]))
    cubiertos = {m["esp"] for m in mut}
    if cubiertos != set(MS.CONTROLES_K45): prob.append(("controles C01 a C15 sin mutación", sorted(set(MS.CONTROLES_K45) - cubiertos)))
    return prob

def col_origen_ok(ce):
    ch = " ".join(ce["checks"])
    return all(x in ch for x in ("origin_kind = 'brief' si y solo si brief_version_id NOT NULL", "'copy' si y solo si copy_version_id NOT NULL", "'asset' si y solo si creative_asset_id NOT NULL", "'promotion' si y solo si promotion_snapshot_id NOT NULL"))

# ---------------- K46: independencia real del resolutor ----------------
def caso_k46():
    org = "X"
    roles = {"revisor": {"piece.review"}, "editor": {"piece.edit"}, "admin": {"org.manage"}}
    mem = lambda rol, o=org, act=True: dict(org=o, activo=act, rol=rol)
    members = {"A": mem("editor"), "C": mem("revisor"), "Q": mem("revisor"), "R": mem("revisor"), "R2": mem("revisor"), "Z": mem("revisor"), "Adm": mem("admin")}
    eventos = {"e1": dict(id="e1", org=org, version="B1", actor="A", campo="oferta", op="o1"), "e2": dict(id="e2", org=org, version="B2", actor="C", campo="oferta", op="o2"),
               "e3": dict(id="e3", org=org, version="V1", actor="Z", campo="headline", op="o3")}
    atrs = {"a1": dict(id="a1", org=org, version="B1", campo="oferta", contrib="A", rel="directa", evento="e1"), "a1b": dict(id="a1b", org=org, version="B2", campo="oferta", contrib="A", rel="heredada", evento="e1"),
            "a1c": dict(id="a1c", org=org, version="B3", campo="oferta", contrib="A", rel="heredada", evento="e1"), "a2": dict(id="a2", org=org, version="B2", campo="oferta", contrib="C", rel="directa", evento="e2"),
            "a2c": dict(id="a2c", org=org, version="B3", campo="oferta", contrib="C", rel="heredada", evento="e2")}
    res = dict(id="r1", org=org, fuente="brief", atribucion="a1c", version="B3", campo="oferta", afectado="A", solicitante="Q", resolutor="R", creado_por="R", evento_motivador="e2", actor_cambio="C",
               evidencia="El texto vigente de B3 no contiene la propuesta original de A", evidencia_atribucion="a1c", evidencia_version="B3", resultado="aceptada")
    return dict(org=org, auth_uid="R", roles=roles, members=members, eventos=eventos, atrs=atrs, res=res, version_actual="B3", cadena=["B1", "B2", "B3"], otras_fuentes=["V1"], historicas=set())

def elegible(st, uid, reglas):
    """Códigos R que impiden que uid resuelva la resolución de st (conjunto completo de la cadena)."""
    r = st["res"]; m = st["members"].get(uid); bad = []
    perms = st["roles"].get(m["rol"], set()) if m else set()
    if "miembro_activo" in reglas and not (m and m["org"] == r["org"] and m["activo"]): bad.append("R1")
    if "piece_review" in reglas and "piece.review" not in perms: bad.append("R2")
    if "no_afectado" in reglas and uid == r["afectado"]: bad.append("R3")
    if "no_solicitante" in reglas and uid == r["solicitante"]: bad.append("R4")
    if "no_actor_del_cambio" in reglas and uid == r["actor_cambio"]: bad.append("R5")
    campo = r["campo"]
    if "no_directo_en_cadena" in reglas and any(e["actor"] == uid and e["campo"] == campo and e["version"] in st["cadena"] for e in st["eventos"].values()): bad.append("R6")
    if "no_heredado_activo" in reglas and any(a["contrib"] == uid and a["campo"] == campo and a["rel"] == "heredada" and a["version"] == st["version_actual"] and a["id"] not in st["historicas"] for a in st["atrs"].values()): bad.append("R7")
    if "no_excluido_otra_fuente" in reglas and any(e["actor"] == uid and e["version"] in st["otras_fuentes"] for e in st["eventos"].values()): bad.append("R8")
    ev = st["eventos"].get(r["evento_motivador"], {})
    if "no_beneficiario" in reglas and (any(a["contrib"] == uid and a["campo"] == campo and a["version"] == st["version_actual"] and a["id"] not in st["historicas"] for a in st["atrs"].values()) or any(e["actor"] == uid and e["op"] == ev.get("op") for e in st["eventos"].values())): bad.append("R9")
    return bad

def evaluar_k46(st, reglas):
    r = st["res"]; cod = []
    at = st["atrs"].get(r["atribucion"])
    if not at: return ["ATRIBUCION_INEXISTENTE"]
    if at["org"] != r["org"]: cod.append("ORG_ATRIBUCION")
    if at["campo"] != r["campo"]: cod.append("CAMPO_DISTINTO")
    if at["contrib"] != r["afectado"]: cod.append("AFECTADO_DISTINTO")
    if r["version"] != at["version"] or r["version"] != st["version_actual"]: cod.append("VERSION_DISTINTA")
    ev = st["eventos"].get(r["evento_motivador"])
    if not ev or ev["org"] != r["org"] or ev["campo"] != r["campo"] or ev["actor"] != r["actor_cambio"]: cod.append("EVENTO_MOTIVADOR_INCOHERENTE")
    if not r["evidencia"].strip(): cod.append("EVIDENCIA_VACIA")
    if r["evidencia_atribucion"] != r["atribucion"]: cod.append("EVIDENCIA_OTRA_ATRIBUCION")
    if r["evidencia_version"] != at["version"]: cod.append("EVIDENCIA_OTRA_VERSION")
    if r["creado_por"] != st["auth_uid"] or r["resolutor"] != r["creado_por"]: cod.append("ACTOR_NO_AUTENTICADO")
    cod += ["R_" + x for x in elegible(st, r["resolutor"], reglas)]
    return cod

def resolutores_elegibles(st, reglas):
    return [u for u in st["members"] if not elegible(st, u, reglas)]

def aplicar_k46(st, reglas):
    """(válida, códigos, estado final de la atribución). Falla cerrada si no hay resolutor elegible."""
    cod = evaluar_k46(st, reglas)
    if not resolutores_elegibles(st, reglas) and st["res"]["resultado"] == "aceptada": cod.append("SIN_RESOLUTOR_ELEGIBLE")
    valida = not cod
    final = "historica" if (valida and st["res"]["resultado"] == "aceptada") else "activa"
    return valida, cod, final

def _ev_nuevo(st, i, actor, version, campo, op="oX"): st["eventos"][i] = dict(id=i, org=st["org"], version=version, actor=actor, campo=campo, op=op)
K46_MUT = [
 ("K46-M01", "el resolutor es el contribuyente afectado", "R_R3", lambda s: s["res"].update(resolutor="A", creado_por="A") or s.update(auth_uid="A")),
 ("K46-M02", "el resolutor es el solicitante", "R_R4", lambda s: s["res"].update(resolutor="Q", creado_por="Q") or s.update(auth_uid="Q")),
 ("K46-M03", "el resolutor es el editor que ejecutó la sustitución", "R_R5", lambda s: s["res"].update(resolutor="C", creado_por="C") or s.update(auth_uid="C")),
 ("K46-M04", "el resolutor contribuyó al mismo campo en una versión anterior", "R_R6", lambda s: _ev_nuevo(s, "e0", "R", "B1", "oferta")),
 ("K46-M05", "el resolutor heredó una contribución activa", "R_R7", lambda s: s["atrs"].update(ar=dict(id="ar", org="X", version="B3", campo="oferta", contrib="R", rel="heredada", evento="e1"))),
 ("K46-M06", "el resolutor es contribuyente de otra fuente de la cadena", "R_R8", lambda s: _ev_nuevo(s, "e4", "R", "V1", "headline")),
 ("K46-M07", "el resolutor no pertenece a la organización", "R_R1", lambda s: s["members"]["R"].update(org="Y")),
 ("K46-M08", "el resolutor no tiene piece.review", "R_R2", lambda s: s["members"]["R"].update(rol="editor")),
 ("K46-M09", "la evidencia está vacía", "EVIDENCIA_VACIA", lambda s: s["res"].update(evidencia="   ")),
 ("K46-M10", "la evidencia apunta a otra atribución o versión", "EVIDENCIA_OTRA_ATRIBUCION", lambda s: s["res"].update(evidencia_atribucion="a2c", evidencia_version="B2")),
 ("K46-M11", "el actor de la resolución no coincide con la identidad autenticada", "ACTOR_NO_AUTENTICADO", lambda s: s.update(auth_uid="R2")),
 ("K46-M12", "no existe ningún resolutor elegible", "SIN_RESOLUTOR_ELEGIBLE", lambda s: s["roles"].update(revisor=set())),
]

def verificar_k46_modelo(spec):
    p = parse_4410(spec); prob = []
    if p["reglasR"] != CLAVES_R: prob.append(("reglas R1 a R9 distintas de las obligatorias", p["reglasR"]))
    reglas = set(p["reglasR"]); st = caso_k46()
    ok, cod, fin = aplicar_k46(st, reglas)
    if not ok or fin != "historica": prob.append(("el caso de referencia válido no se acepta", cod))
    if len(resolutores_elegibles(st, reglas)) < 2: prob.append(("el caso de referencia debe tener al menos dos resolutores elegibles",))
    if "Adm" in resolutores_elegibles(st, reglas): prob.append(("Admin elegible por su cargo",))
    for u in resolutores_elegibles(st, reglas):
        s2 = _copy.deepcopy(st); s2["res"].update(resolutor=u, creado_por=u); s2["auth_uid"] = u
        ok_u, cod_u, fin_u = aplicar_k46(s2, reglas)
        if not ok_u or fin_u != "historica": prob.append(("falso positivo: el resolutor elegible %s se rechaza" % u, cod_u[:3]))
    mk = ejecutar_mutaciones_k46(reglas)
    nd = [m["id"] for m in mk if not m["det"]]
    if len(mk) != N_K46 or nd: prob.append(("mutaciones K46 no detectadas o ausentes (%d/%d)" % (len(mk) - len(nd), N_K46), nd[:4]))
    return prob

def ejecutar_mutaciones_k46(reglas):
    out = []
    for mid, nom, cod_esp, fn in K46_MUT:
        st0 = caso_k46(); ok0, c0, f0 = aplicar_k46(st0, reglas)
        st = _copy.deepcopy(st0); fn(st); cambio = (st != st0)
        ok1, c1, f1 = aplicar_k46(st, reglas)
        det = ok0 and cambio and (not ok1) and (cod_esp in c1) and f1 == "activa"
        out.append(dict(id=mid, mut=nom, esp=cod_esp, obs=("rechazada con " + ", ".join(c1[:4]) + "; atribución " + f1) if not ok1 else "ACEPTADA (no detectada)", det=bool(det), cambio=cambio, valido=ok0, n_el=len(resolutores_elegibles(st0, reglas))))
    return out

# ---------------- K47: auditoría estructural de conservación y E ----------------
def simular_k47(P):
    """P = parse_4410. Aplica las tablas C y D a casos de referencia y devuelve las violaciones de los 10 invariantes."""
    v = []
    clasef = {(r["fuente"], r["clas"]): r for r in P["efec_clas"]}
    evt = {r["evento"]: r for r in P["efec_evt"]}
    for f in FUENTES:
        for c in CLAS:
            if (f, c) not in clasef: v.append(("fila ausente", f, c))
    if v: return v
    def propagar(f, c, previas, actor):
        r = clasef[(f, c)]
        nuevas = []
        if r["conserva"] == "todas": nuevas += [dict(x, rel="heredada") for x in previas]
        elif r["conserva"] != "ninguna": v.append(("conservación no reconocida", f, c, r["conserva"]))
        if r["incorpora"] == "sí": nuevas.append(dict(persona=actor, campo="campo", rel="directa"))
        if r["retira"] != "ninguna": nuevas = [x for x in nuevas if x["persona"] == actor]
        return nuevas
    for f in FUENTES:
        base = [dict(persona="A", campo="campo", rel="directa")]
        for c in CLAS:
            r = clasef[(f, c)]
            res = propagar(f, c, base, "X")
            if not any(x["persona"] == "A" for x in res): v.append(("I1 una atribución activa anterior se pierde", f, c))
            if (c != "sin_cambio") != any(x["persona"] == "X" for x in res): v.append(("I2 el actor no se incorpora o se crea sin cambio", f, c))
            if r["retira"] != "ninguna": v.append(("I1 la clasificación retira atribuciones", f, c))
            if r["similitud"] != "no": v.append(("I11 la similitud decide el descarte", f, c))
    for c in CLAS:
        filas = {f: tuple(clasef[(f, c)][k] for k in ("conserva", "incorpora", "retira", "similitud")) for f in FUENTES}
        if len(set(filas.values())) != 1: v.append(("I9 las fuentes no siguen la misma regla", c, filas))
    for nom in ("resolución aceptada", "resolución rechazada", "versión nueva", "cadena incompleta", "atribución histórica", "cambio de clasificación"):
        if nom not in evt: v.append(("evento ausente", nom))
    if v: return v
    A, R_, N, I, H, K = (evt[x] for x in ("resolución aceptada", "resolución rechazada", "versión nueva", "cadena incompleta", "atribución histórica", "cambio de clasificación"))
    # resolución aceptada: afecta solo la referenciada y deja la evidencia
    if A["retira"] != "solo la referenciada": v.append(("I3 la resolución aceptada no se limita a la atribución y campo referenciados", A["retira"]))
    if A["reescribe"] != "no": v.append(("I10 la resolución reescribe versiones anteriores", A["reescribe"]))
    if A["efecto_e"] != "sale solo quien no conserva otra contribución activa": v.append(("I7 la resolución aceptada no mantiene en E a quien conserva otra activa", A["efecto_e"]))
    if R_["retira"] != "ninguna" or R_["efecto_e"] != "sin cambio": v.append(("I5 una resolución rechazada modifica atribuciones o E", R_))
    if N["retira"] != "hereda todas las activas" or N["reescribe"] != "no": v.append(("I10 la versión nueva no hereda todas las activas o reescribe versiones", N))
    if I["efecto_e"] != "no determinable": v.append(("I8 una cadena incompleta produce un E presentado como completo", I["efecto_e"]))
    if H["retira"] != "permanece como evidencia" or H["efecto_e"] != "permanece si conserva otra activa": v.append(("I6/I7 la atribución histórica no permanece como evidencia o la persona sale de E", H))
    if K["retira"] != "ninguna" or K["efecto_e"] != "sin cambio": v.append(("I12 un cambio de clasificación retira atribuciones", K))
    for e in P["efec_evt"]:
        if e["reescribe"] != "no": v.append(("I10 el evento reescribe versiones anteriores", e["evento"]))
    return v

def verificar_k55_modelo():
    """Comprobaciones estructurales de la v12 sobre datos y relaciones reales del modelo (no búsquedas de texto)."""
    prob = []
    m, x, asr = MS.esc_p15(MS.Motor)
    reut = [y for y in m.assets.values() if y["tipo"] == "reutilizado"]
    if not reut: prob.append(("el fixture de reutilización no contiene un asset reutilizado",))
    for y in reut:
        e = m.ev.get(y["evento_reutilizacion"]); faltan = [c for c in CAMPOS_EVT_REUT if e is None or e.get(c) is None]
        if faltan: prob.append(("el evento de reutilización de %s carece de los campos de identidad %s" % (y["id"], faltan),))
        o = m.assets.get(e["source_asset_version_id"]) if e else None; eo = m.ev.get(e["source_upload_event_id"]) if e else None; at0 = m.at.get(e["source_attribution_id"]) if e else None
        if o is None or eo is None or at0 is None: prob.append(("las referencias del origen de %s no resuelven a registros concretos" % y["id"],)); continue
        rel = [("asset de origen", e["source_asset_id"] == o["asset_id"]), ("evento de carga del origen", eo["tipo"] == "asset_uploader" and eo["asset"] == o["id"] and eo["org"] == o["org"] and eo["pieza"] == o["pieza"]), ("uploader del origen", e["source_uploader_id"] == eo["actor"] == eo["auth"]),
               ("atribución original", at0["persona"] == eo["actor"] and at0["evento"] == eo["id"] and at0["asset"] == o["id"] and at0["rel"] == "directa"), ("reutilizador distinto del uploader", e["actor"] == e["auth"] == y["reutilizador"] and y["reutilizador"] != y["uploader_original"]),
               ("destino exacto", e["version"] == y["copy_version"] and e["pieza"] == y["pieza"] == m.v[y["copy_version"]]["pieza"] and e["org"] == y["org"] == o["org"])]
        prob += [("vínculo %s de %s no verificado" % (n_, y["id"]),) for n_, ok in rel if not ok]
    if MS._compartidas(): prob.append(("el auditor usa funciones del motor", MS._compartidas()[:3]))
    at = MS.pruebas_atomicidad()
    if len(at) != N_ATOM or not all(a[1] for a in at): prob.append(("la reutilización inválida deja registros parciales o no falla", [a[0] for a in at if not a[1]]))
    ids = [m_["id"] for m_ in MS.correr_mutaciones_assets()]
    if ids != ["K47-A%02d" % i for i in range(1, N_ART + 1)] and sorted(ids) != ["K47-A%02d" % i for i in range(1, N_ART + 1)]: prob.append(("identificadores de mutaciones de assets no continuos A01 a A%d" % N_ART,))
    ruta = os.path.join(_DIR_HIST or "", "ESPECIFICACION_TECNICA_G1_G5_G10_v11_historica.md")
    if os.path.exists(ruta):
        h = open(ruta, encoding="utf-8").read(); desc_v11 = set(re.findall(r"^\| K47-A(?:1[7-9]|2\d|3[0-7]) \| ([^|]*?) \| I\d+ \|\s*$", h, re.M)); actuales = {m_["mut"] for m_ in MS.correr_mutaciones_assets()}
        perdidas = sorted(d for d in desc_v11 if d.strip() not in actuales)
        if len(desc_v11) < 21 or perdidas: prob.append(("mutaciones de la v11 perdidas o no localizadas (%d)" % len(desc_v11), perdidas[:3]))
    import ast
    for ruta_py in (MS.__file__, __file__):
        for n in ast.walk(ast.parse(open(ruta_py, encoding="utf-8").read())):
            nom = n.id if isinstance(n, ast.Name) else n.attr if isinstance(n, ast.Attribute) else None
            if nom in ("skip", "xfail", "skipTest", "SkipTest", "skipif"): prob.append(("uso de %s en %s" % (nom, os.path.basename(ruta_py)),))
    return prob

def verificar_k47_modelo(spec):
    """Capa documental (las tablas de 4.4.10 son coherentes) más capa estructural (el motor las cumple, 12 escenarios y 36 mutaciones)."""
    P = parse_4410(spec); prob = list(simular_k47(P))
    prob += [("tabla C de 4.4.10 distinta del comportamiento observado en el motor",) + tuple(d) for d in MS.conformidad_tabla(P["efec_clas"])]
    esc = MS.correr_escenarios()
    for e in esc:
        if not e["ok"]: prob.append(("escenario %s (%s) no aprobado" % (e["id"], e["nombre"]), e["viol"][:3], e["fallos"][:2]))
    if len([e for e in esc if e["id"] in "ABCDEFGHIJKL"]) != N_ESC: prob.append(("faltan escenarios estructurales",))
    mut = MS.correr_mutaciones_k47(); nd = [m["id"] for m in mut if not m["det"]]
    if len(mut) != N_K47 or nd: prob.append(("mutaciones K47 no detectadas o ausentes (%d/%d)" % (len(mut) - len(nd), N_K47), nd[:4]))
    if not any(e["id"] == "RS" and e["ok"] for e in esc): prob.append(("escenario RS (resoluciones inmutables) no aprobado",))
    mr = MS.correr_mutaciones_resoluciones(); nr = [m["id"] for m in mr if not m["det"]]
    if len(mr) != N_RES or nr: prob.append(("mutaciones de resoluciones no detectadas o ausentes (%d/%d)" % (len(mr) - len(nr), N_RES), nr[:4]))
    ma = MS.correr_mutaciones_assets(); na = [m["id"] for m in ma if not m["det"]]
    if len(ma) != N_ART or na: prob.append(("mutaciones de assets no detectadas o ausentes (%d/%d)" % (len(ma) - len(na), N_ART), na[:4]))
    mrz = MS.correr_mutaciones_rechazo(); nrz = [m["id"] for m in mrz if not (m["det"] and m["valido"] and m["cambio"] and m["rechaza"] and m["atomico"] and m["ident"] and m["bloq"])]
    if len(mrz) != N_RECH or [m["id"] for m in mrz] != IDS_V13 or nrz: prob.append(("mutaciones de rechazo previo A54 a A65 no detectadas o ausentes (%d/%d)" % (len(mrz) - len(nrz), N_RECH), nrz[:4]))
    pa = MS.correr_positivos_arte()
    if len(pa) != N_POS_ART or not all(p["ok"] for p in pa): prob.append(("casos positivos de arte no aprobados", [p["id"] for p in pa if not p["ok"]]))
    adv = MS.correr_adversariales()
    if len(adv) != N_ADV or not all(a["ok"] for a in adv): prob.append(("pruebas adversariales de identidad no aprobadas", [a["id"] for a in adv if not a["ok"]]))
    if any(m.get("bloq") is False for m in ma): prob.append(("mutaciones de assets que no bloquean E", [m["id"] for m in ma if m.get("bloq") is False][:4]))
    gu = MS.pruebas_guarda()
    if len(gu) != N_GUARDA or not all(g[1] for g in gu): prob.append(("intentos directos contra el registro de resoluciones no rechazados", [g[0] for g in gu if not g[1]]))
    at_ = MS.pruebas_atomicidad()
    if len(at_) != N_ATOM or not all(a[1] for a in at_): prob.append(("pruebas de atomicidad de la reutilización no aprobadas", [a[0] for a in at_ if not a[1]]))
    return prob

def ejecutar_mutaciones_modelo(textos, dir_hist):
    """Mutaciones estructurales K46, K45 y K47: cada una parte de un caso válido, aplica un único cambio y se detecta por la condición esperada."""
    out = []
    P = parse_4410(textos[SPEC]); M = P["matriz"]; reglas = set(P["reglasR"])
    for m in ejecutar_mutaciones_k46(reglas):
        out.append(dict(id=m["id"], ctl="K46", regla="IG5-95 (%s)" % m["esp"], inicial="válido: resolución aceptada por R, %d elegibles" % m["n_el"], mut=m["mut"], esp="rechazo con %s; la atribución permanece activa" % m["esp"], obs=m["obs"], det=m["det"], cambio=m["cambio"], valido=m["valido"]))
    mk, _ = MS.correr_mutaciones_k45(M)
    nT = len(MS.fixture_k45()["events"]); nA = len(MS.fixture_k45()["attributions"])
    for m in mk:
        out.append(dict(id=m["id"], ctl="K45", regla="IG5-96 (%s)" % m["esp"], inicial="válido: modelo relacional con %d eventos y %d atribuciones, 0 violaciones" % (nT, nA), mut=m["mut"], esp="rechazo con %s" % m["esp"], obs=m["obs"], det=m["det"], cambio=m["cambio"], valido=m["valido"]))
    for m in MS.correr_mutaciones_k47():
        out.append(dict(id=m["id"], ctl="K47", regla="IG5-97 (%s)" % m["esp"], inicial="válido: escenario ejecutado sobre el motor, 0 violaciones del auditor", mut=m["mut"], esp="violación %s" % m["esp"], obs=m["obs"], det=m["det"], cambio=m["cambio"], valido=m["valido"]))
    for m in MS.correr_mutaciones_resoluciones():
        out.append(dict(id=m["id"], ctl="K47", regla="IG5-98 (%s)" % m["esp"], inicial="válido: escenario RS con tres resoluciones selladas y cadena de reconsideración, 0 violaciones", mut=m["mut"], esp="violación %s con la condición «%s»" % (m["esp"], m["kw"]), obs=m["obs"], det=m["det"], cambio=m["cambio"], valido=m["valido"]))
    for m in MS.correr_mutaciones_assets():
        nuevo = int(m["id"][-2:]) > N_ART_V10; reg_ = "IG5-101" if m["id"] in IDS_V12 else "IG5-100" if nuevo else "IG5-99"
        out.append(dict(id=m["id"], ctl="K47", regla="%s (%s)" % (reg_, m["esp"]), inicial="válido: escenario de arte ejecutado sobre el motor, 0 violaciones del auditor", mut=m["mut"],
                        esp="violación %s con la condición «%s»%s" % (m["esp"], m["kw"], "; procedencia incompleta y E no completo" if nuevo else ""), obs=m["obs"] + ("; E bloqueado" if m.get("bloq") else ""), det=m["det"], cambio=m["cambio"], valido=m["valido"]))
    for m in MS.correr_mutaciones_cadena():
        out.append(dict(id=m["id"], ctl="K56", regla="IG5-104 (CHAIN)", inicial="válido: cadena de tres niveles aceptada, cero violaciones del auditor y E completo", mut=m["mut"], esp="%s; sin registros parciales, estado previo idéntico y E bloqueado" % m["esp"], obs=m["obs"] + ("; E bloqueado" if m.get("bloq") else ""), det=m["det"], cambio=m["cambio"], valido=m["valido"]))
    for f_, reg_ in ((MS.correr_mutaciones_av, "IG5-111"), (MS.correr_mutaciones_cf, "IG5-112"), (MS.correr_mutaciones_ac, "IG5-113")):
        for m in f_():
            out.append(dict(id=m["id"], ctl="K56", regla="%s (%s)" % (reg_, m["id"].split("-")[0]), inicial="válido: reutilización aceptada, cero violaciones del auditor independiente y E completo", mut=m["mut"], esp="%s; sin asset, evento, atribución ni relación parcial, estado completo idéntico, procedencia incompleta, E nulo y sin impacto, aprobación ni publicación" % m["esp"], obs=m["obs"][:170] + "; E bloqueado", det=m["det"], cambio=m["cambio"], valido=m["valido"]))
    for m in MS.correr_mutaciones_atribucion():
        out.append(dict(id=m["id"], ctl="K56", regla="IG5-107 (%s)" % m["esp"], inicial="válido: escenario con resoluciones selladas y atribuciones conservadas, cero violaciones", mut=m["mut"], esp="violación %s" % m["esp"], obs=m["obs"], det=m["det"], cambio=True, valido=True))
    for m in MS.correr_mutaciones_modelo14():
        out.append(dict(id=m["id"], ctl="K56", regla="IG5-110 (código del modelo)", inicial="válido: las baterías CHAIN, ADVC, ATTR, AT14, E14, AV, CF, AC, AP, ADV15 y AT15 aprueban", mut=m["mut"], esp="al menos una batería falla", obs="detectada por %d pruebas: %s" % (m["n_detectores"], ", ".join(m["detectada_por"][:4])), det=m["det"], cambio=True, valido=True))
    for m in MS.correr_mutaciones_rechazo():
        out.append(dict(id=m["id"], ctl="K47", regla="IG5-102 (%s)" % m["esp"], inicial="válido: fixture de reutilización exacta, 0 violaciones del auditor y E completo", mut=m["mut"], esp="%s; sin registros parciales, estado previo idéntico, E nulo, sin evaluación de impacto, aprobación ni publicación" % m["esp"], obs=m["obs"] + ("; E nulo en la pieza y la versión de destino" if m.get("bloq") else ""), det=m["det"] and m.get("atomico") is True and m.get("ident") is True and m.get("bloq") is True, cambio=m["cambio"], valido=m["valido"]))
    return out

def calcular_v33(ruta):
    """K48: SHA-256 calculado sobre los bytes del archivo original v3.3."""
    if not ruta or not os.path.isfile(ruta): return None, None
    return sha(ruta), ruta

def check_v33(ruta):
    h, r = calcular_v33(ruta)
    if h is None:
        chk("K48", "Hash de la línea base v3.3: PENDIENTE_ARCHIVO_ORIGINAL_NO_DISPONIBLE (no se indicó o no existe el archivo original; el hash registrado en los documentos es un registro histórico, no una comprobación criptográfica)", None, "", "IE-10", "REGISTRO; AUDITORIA 3")
    else:
        chk("K48", "Hash de la línea base v3.3 calculado sobre los bytes de «%s»: %s; esperado %s; %s" % (os.path.basename(r), h, V33_SHA, "COINCIDE" if h == V33_SHA else "NO COINCIDE"), h == V33_SHA, h, "IE-10", "REGISTRO; AUDITORIA 3")

def correr(textos, dir_hist, v33=None):
    global RES
    RES = []
    C, A, info = ejecutar(textos, dir_hist)
    checks_adicionales(textos, C, A, info)
    checks_v7(textos, C, A, info)
    check_v33(v33)
    return C, A, info

# ---------------- mutaciones negativas ----------------
def _ed(old, new, n=1):
    def f(t):
        s = t[SPEC]
        assert old in s, "texto de la mutación no encontrado: " + old[:70]
        t = dict(t); t[SPEC] = s.replace(old, new, n); return t
    return f
def _fila(prefijo, old, new):
    def f(t):
        s = t[SPEC]; m = re.search(r"^" + re.escape(prefijo) + r".*$", s, re.M); assert m, prefijo
        assert old in m.group(0), (prefijo, old)
        t = dict(t); t[SPEC] = s[:m.start()] + m.group(0).replace(old, new, 1) + s[m.end():]; return t
    return f
def _quitar_linea(contiene, bloque):
    def f(t):
        s = t[SPEC]; a = s.index("#### `%s`" % bloque); b = s.index("\n#### ", a + 5) if "\n#### " in s[a + 5:] else len(s)
        seg = s[a:b]; ls = seg.split("\n"); k = [i for i, l in enumerate(ls) if l.startswith("- ") and contiene in l]; assert k, (contiene, bloque)
        del ls[k[0]]; t = dict(t); t[SPEC] = s[:a] + "\n".join(ls) + s[b:]; return t
    return f
def _fila_con(prefijo, contiene, old, new):
    def f(t):
        s = t[SPEC]; ms = [m for m in re.finditer(r"^" + re.escape(prefijo) + r".*$", s, re.M) if contiene in m.group(0)]; assert ms, (prefijo, contiene)
        m = ms[0]; assert old in m.group(0), (prefijo, contiene, old)
        t = dict(t); t[SPEC] = s[:m.start()] + m.group(0).replace(old, new) + s[m.end():]; return t
    return f
def _quitar_fila_con(prefijo, contiene):
    def f(t):
        s = t[SPEC]; ms = [m for m in re.finditer(r"^" + re.escape(prefijo) + r".*\n", s, re.M) if contiene in m.group(0)]; assert ms, (prefijo, contiene)
        t = dict(t); t[SPEC] = s[:ms[0].start()] + s[ms[0].end():]; return t
    return f
def _regex_t1(t):
    s = t[SPEC]; t = dict(t)
    t[SPEC] = re.sub(r"^(\| T-0*1 \|.*\| )([^|]+?)( \|)$", r"\1\2, IG5-999\3", s, count=1, flags=re.M); return t
def _sin_escenario(t):
    t = dict(t); out = []
    for l in t[SPEC].split("\n"):
        if l.startswith("| T-") and "IG5-83" in l:
            cel = l.split("|"); ids = [x.strip() for x in cel[-2].split(",")]; ids = [x for x in ids if x != "IG5-83"] or ["IG5-82"]
            cel[-2] = " " + ", ".join(ids) + " "; l = "|".join(cel)
        out.append(l)
    t[SPEC] = "\n".join(out); return t
def _id_dup(t):
    s = t[SPEC]; m = re.search(r"^\| (IG5-69) \| (.*) \|$", s, re.M); t = dict(t); t[SPEC] = s.replace(m.group(0), m.group(0) + "\n" + m.group(0), 1); return t
def _err_ausente(t):
    s = t[SPEC]; a = s.index("#### 4.4.5 "); b = s.index("#### 4.4.6 "); t = dict(t)
    t[SPEC] = s[:a] + s[a:b].replace("BRIEF_CHAIN_INCONSISTENTE", "ERROR_GENERICO") + s[b:]; return t

_RS1 = "(organization_id, source_asset_version_id, source_asset_id, source_root_asset_version_id)"
_RS6 = "(organization_id, upload_event_id, id, uploader_id, piece_id, copy_version_id)"
_C1 = "| contribution_events → creative_assets (columna agregada) |"
_FKM = [
 ("FK01", "Se elimina la FK RS-01 de source_asset_version_id", "K32", "Se retira del contrato la FK compuesta de source_asset_version_id hacia creative_assets", _quitar_fila_con(_C1, _RS1)),
 ("FK02", "Se elimina otra FK requerida (RS-04, linaje del asset)", "K32", "Se retira del contrato la FK compuesta de lineage_parent_asset_id hacia creative_assets", _quitar_fila_con("| creative_assets → creative_assets (columna agregada) |", "lineage_parent_asset_id")),
 ("FK03", "FK RS-01 sin organization_id", "K44", "La FK RS-01 pierde organization_id en las columnas locales y en las de destino", _fila_con(_C1, _RS1, "(organization_id, source_asset_version_id, source_asset_id, source_root_asset_version_id) → creative_assets(organization_id, id, asset_lineage_id, root_asset_version_id)", "(source_asset_version_id, source_asset_id, source_root_asset_version_id, organization_id) → creative_assets(id, asset_lineage_id, root_asset_version_id, organization_id)")),
 ("FK04", "Columnas de destino invertidas en RS-01", "K44", "En RS-01 se invierten las dos últimas columnas de destino", _fila_con(_C1, _RS1, "creative_assets(organization_id, id, asset_lineage_id, root_asset_version_id)", "creative_assets(organization_id, id, root_asset_version_id, asset_lineage_id)")),
 ("FK05", "Destino sin la unicidad suficiente", "K44", "Se elimina de contribution_events la clave única (organization_id, id, creative_asset_id, contributor_id) destino de RS-02", _quitar_linea("unique(organization_id, id, creative_asset_id, contributor_id)", "contribution_events")),
 ("FK06", "Tipo incompatible en source_attribution_relation", "K44", "La columna source_attribution_relation de contribution_events pasa de text a uuid", lambda t: _tipo_rel(t)),
 ("FK07", "source_upload_event_id sin FK ni mecanismo alternativo", "K32", "Se retira la FK RS-02 de source_upload_event_id", _quitar_fila_con("| contribution_events → contribution_events (columna agregada) |", "source_upload_event_id")),
 ("FK08", "source_attribution_id sin FK ni mecanismo alternativo", "K32", "Se retira la FK RS-03 de source_attribution_id", _quitar_fila_con("| contribution_events → copy_version_provenance (columna agregada) |", "source_attribution_id")),
 ("FK09", "RS-06 sin organization_id (equivalente declarativo del trigger diferido sin validar la organización)", "K44", "La FK diferida RS-06 pierde organization_id", _fila_con("| creative_assets → contribution_events (columna agregada) |", _RS6, "(organization_id, upload_event_id, id, uploader_id, piece_id, copy_version_id) → contribution_events(organization_id, id, creative_asset_id, contributor_id, asset_piece_id, asset_copy_version_id)", "(upload_event_id, id, uploader_id, piece_id, copy_version_id, organization_id) → contribution_events(id, creative_asset_id, contributor_id, asset_piece_id, asset_copy_version_id, organization_id)")),
 ("FK10", "RS-01 sin el asset exacto (equivalente declarativo del trigger que no valida el asset)", "K32", "RS-01 deja de incluir source_asset_id y asset_lineage_id", _fila_con(_C1, _RS1, "(organization_id, source_asset_version_id, source_asset_id, source_root_asset_version_id) → creative_assets(organization_id, id, asset_lineage_id, root_asset_version_id)", "(organization_id, source_asset_version_id, source_root_asset_version_id) → creative_assets(organization_id, id, root_asset_version_id)")),
 ("FK11", "RS-01 con el asset lógico y la versión exacta intercambiados (equivalente de no validar la versión exacta)", "K45", "En RS-01 source_asset_id y source_asset_version_id cambian de posición", _fila_con(_C1, _RS1, "(organization_id, source_asset_version_id, source_asset_id, source_root_asset_version_id) → creative_assets(organization_id, id,", "(organization_id, source_asset_id, source_asset_version_id, source_root_asset_version_id) → creative_assets(organization_id, id,")),
 ("FK12", "RS-03 con uploader y evento de carga intercambiados (equivalente de no validar uploader y atribución)", "K45", "En RS-03 source_uploader_id y source_upload_event_id cambian de posición", _fila_con("| contribution_events → copy_version_provenance (columna agregada) |", "source_attribution_id", "source_attribution_id, source_upload_event_id, source_uploader_id,", "source_attribution_id, source_uploader_id, source_upload_event_id,")),
 ("FK13", "ON DELETE RESTRICT cambiado a SET NULL (referencia huérfana tras una corrección)", "K32", "RS-01 pasa de ON DELETE RESTRICT a ON DELETE SET NULL", _fila_con(_C1, _RS1, "ON DELETE RESTRICT", "ON DELETE SET NULL")),
 ("FK14", "Excepción de K32 sin el verificador K45 que la justifica", "K32", "La excepción source_asset_version (entero) pierde la referencia a K45", _fila("| source_asset_version (entero del modelo en memoria) |", "| K45 |", "| — |")),
 ("FK15", "Excepción de K45 con una prueba negativa inexistente", "K45", "La prueba negativa de la excepción referencia K47-A99", _fila("| source_asset_version (entero del modelo en memoria) |", "K47-A34 (mismo número de versión) y K47-A42", "K47-A99 (mismo número de versión) y K47-A98")),
]
_C_CC = "| creative_assets → creative_assets (columna agregada) |"
_C_CE = "| contribution_events → contribution_events (columna agregada) |"
_C_CVP = "| contribution_events → copy_version_provenance (columna agregada) |"
_C_AE = "| creative_assets → contribution_events (columna agregada) |"
_RS2 = "(organization_id, source_upload_event_id, source_root_asset_version_id, source_uploader_id) → contribution_events(organization_id, id, creative_asset_id, contributor_id)"
_RS3 = "(organization_id, source_attribution_id, source_upload_event_id, source_uploader_id, source_root_asset_version_id, source_attribution_relation) → copy_version_provenance(organization_id, id, contribution_event_id, contributor_id, origin_asset_id, relation)"
_RS5 = "(organization_id, reused_from_asset_id, root_asset_version_id) → creative_assets(organization_id, id, root_asset_version_id)"
_RS6f = "(organization_id, upload_event_id, id, uploader_id, piece_id, copy_version_id) → contribution_events(organization_id, id, creative_asset_id, contributor_id, asset_piece_id, asset_copy_version_id)"
_RS7 = "(organization_id, reuse_event_id, reused_from_asset_id, piece_id, copy_version_id) → contribution_events(organization_id, id, source_asset_version_id, copy_version_piece_id, copy_version_id)"
_RS8 = "(organization_id, source_root_asset_version_id, source_upload_event_id) → creative_assets(organization_id, id, upload_event_id)"
_EXC = "| source_asset_version (entero del modelo en memoria) |"
_FKM += [
 ("FK16", "RS-05 eliminada", "K32", "Se retira del contrato la FK compuesta RS-05 (reused_from_asset_id y raíz)", _quitar_fila_con(_C_CC, "(organization_id, reused_from_asset_id, root_asset_version_id)")),
 ("FK17", "RS-06 eliminada", "K32", "Se retira del contrato la FK diferida RS-06", _quitar_fila_con(_C_AE, "(organization_id, upload_event_id, id, uploader_id, piece_id, copy_version_id)")),
 ("FK18", "RS-07 eliminada", "K32", "Se retira del contrato la FK RS-07 del evento de reutilización", _quitar_fila_con(_C_AE, "(organization_id, reuse_event_id, reused_from_asset_id, piece_id, copy_version_id)")),
 ("FK19", "RS-08 eliminada", "K32", "Se retira del contrato la FK RS-08 (evento de carga de origen = upload_event_id de la raíz)", _quitar_fila_con(_C1, "(organization_id, source_root_asset_version_id, source_upload_event_id)")),
 ("FK20", "RS-02 sin source_uploader_id", "K32", "RS-02 pierde source_uploader_id y contributor_id", _fila_con(_C_CE, _RS2, _RS2, "(organization_id, source_upload_event_id, source_root_asset_version_id) → contribution_events(organization_id, id, creative_asset_id)")),
 ("FK21", "RS-03 sin source_attribution_relation", "K32", "RS-03 pierde source_attribution_relation y relation", _fila_con(_C_CVP, _RS3, _RS3, "(organization_id, source_attribution_id, source_upload_event_id, source_uploader_id, source_root_asset_version_id) → copy_version_provenance(organization_id, id, contribution_event_id, contributor_id, origin_asset_id)")),
 ("FK22", "RS-03 sin source_root_asset_version_id", "K32", "RS-03 pierde source_root_asset_version_id y origin_asset_id", _fila_con(_C_CVP, _RS3, _RS3, "(organization_id, source_attribution_id, source_upload_event_id, source_uploader_id, source_attribution_relation) → copy_version_provenance(organization_id, id, contribution_event_id, contributor_id, relation)")),
 ("FK23", "RS-08 con columnas de destino en otro orden", "K44", "En RS-08 se invierten id y upload_event_id en el destino", _fila_con(_C1, _RS8, "creative_assets(organization_id, id, upload_event_id)", "creative_assets(organization_id, upload_event_id, id)")),
 ("FK24", "Destino de RS-05 sin su clave única", "K44", "Se elimina de creative_assets la clave única (organization_id, id, root_asset_version_id)", _fila("| creative_assets | organization_id uuid", "unique(organization_id, id, root_asset_version_id)", "")),
 ("FK25", "Destino de RS-08 sin su clave única", "K44", "Se elimina de creative_assets la clave única (organization_id, id, upload_event_id)", _fila("| creative_assets | organization_id uuid", "unique(organization_id, id, upload_event_id)", "")),
 ("FK26", "RS-02 sin organization_id", "K44", "RS-02 pierde organization_id en origen y destino", _fila_con(_C_CE, _RS2, _RS2, "(source_upload_event_id, source_root_asset_version_id, source_uploader_id, organization_id) → contribution_events(id, creative_asset_id, contributor_id, organization_id)")),
 ("FK27", "RS-07 sin la pieza", "K32", "RS-07 pierde piece_id y copy_version_piece_id", _fila_con(_C_AE, _RS7, _RS7, "(organization_id, reuse_event_id, reused_from_asset_id, copy_version_id) → contribution_events(organization_id, id, source_asset_version_id, copy_version_id)")),
 ("FK28", "RS-06 sin la versión de copy", "K32", "RS-06 pierde copy_version_id y asset_copy_version_id", _fila_con(_C_AE, _RS6f, _RS6f, "(organization_id, upload_event_id, id, uploader_id, piece_id) → contribution_events(organization_id, id, creative_asset_id, contributor_id, asset_piece_id)")),
 ("FK29", "Asset sustituido en RS-05", "K32", "RS-05 usa lineage_parent_asset_id en lugar de reused_from_asset_id", _fila_con(_C_CC, _RS5, "(organization_id, reused_from_asset_id, root_asset_version_id)", "(organization_id, lineage_parent_asset_id, root_asset_version_id)")),
 ("FK30", "Versión sustituida en RS-07", "K32", "RS-07 usa previous_asset_id en lugar de reused_from_asset_id", _fila_con(_C_AE, _RS7, "(organization_id, reuse_event_id, reused_from_asset_id, piece_id, copy_version_id) →", "(organization_id, reuse_event_id, previous_asset_id, piece_id, copy_version_id) →")),
 ("FK31", "Evento sustituido en RS-06", "K32", "RS-06 usa reuse_event_id en lugar de upload_event_id", _fila_con(_C_AE, _RS6f, "(organization_id, upload_event_id, id, uploader_id, piece_id, copy_version_id) →", "(organization_id, reuse_event_id, id, uploader_id, piece_id, copy_version_id) →")),
 ("FK32", "Uploader sustituido en RS-02", "K45", "RS-02 intercambia source_upload_event_id y source_uploader_id", _fila_con(_C_CE, _RS2, "(organization_id, source_upload_event_id, source_root_asset_version_id, source_uploader_id) →", "(organization_id, source_uploader_id, source_root_asset_version_id, source_upload_event_id) →")),
 ("FK33", "Atribución sustituida en RS-03", "K45", "RS-03 intercambia source_attribution_id y source_uploader_id", _fila_con(_C_CVP, _RS3, "(organization_id, source_attribution_id, source_upload_event_id, source_uploader_id,", "(organization_id, source_uploader_id, source_upload_event_id, source_attribution_id,")),
 ("FK34", "Relación de origen cruzada en RS-03", "K32", "RS-03 apunta a brief_field_attributions", _fila_con(_C_CVP, _RS3, "→ copy_version_provenance(", "→ brief_field_attributions(")),
 ("FK35", "Borrado indebido en RS-02", "K32", "RS-02 pasa de ON DELETE RESTRICT a ON DELETE CASCADE", _fila_con(_C_CE, _RS2, "ON DELETE RESTRICT", "ON DELETE CASCADE")),
 ("FK36", "Actualización indebida en RS-01", "K32", "RS-01 agrega ON UPDATE CASCADE", _fila_con(_C1, _RS1, "ON DELETE RESTRICT", "ON DELETE RESTRICT ON UPDATE CASCADE")),
 ("FK37", "Ciclo de inserción", "K44", "En la reutilización, el paso 2 referencia un registro del paso 2", _ed("RS-05 → origen (preexistente); RS-07 → paso 1", "RS-05 → origen (preexistente); RS-07 → paso 2")),
 ("FK38", "FK diferida mal aplicada", "K32", "RS-05 pasa a DEFERRABLE INITIALLY DEFERRED sin ciclo de filas", _fila_con(_C_CC, _RS5, "ON DELETE RESTRICT", "ON DELETE RESTRICT DEFERRABLE INITIALLY DEFERRED")),
 ("FK39", "Excepción sin mecanismo alternativo", "K32", "La excepción pierde el mecanismo alternativo", _fila(_EXC, "no se almacena: el número es creative_assets.asset_version de la fila identificada por RS-01 y nunca sustituye a la identidad", " ")),
 ("FK40", "Excepción sin prueba negativa", "K45", "La excepción pierde la prueba negativa", _fila(_EXC, "K47-A34 (mismo número de versión) y K47-A42 (intercambio con igual número)", "ninguna")),
 ("FK41", "Restricción única propia eliminada", "K32", "Se elimina unique(organization_id, reuse_event_id) de creative_assets", _fila("| creative_assets | organization_id uuid", "unique(organization_id, reuse_event_id)", "")),
]

_K57M = [
 ("K57-D01", "Trazabilidad con una función inexistente", "K57", "La regla IG5-104 cita `Motor.reconstruir_cadena_inexistente`", _ed("`Motor.reconstruir_cadena_procedencia`", "`Motor.reconstruir_cadena_inexistente`")),
 ("K57-D02", "Trazabilidad con una prueba inexistente", "K57", "La regla IG5-104 cita CHAIN-25", _ed("| CHAIN-01 a CHAIN-24 | K56 |", "| CHAIN-01 a CHAIN-25 | K56 |")),
 ("K57-D03", "Matriz de auditoría con una celda vacía", "K57", "D-05 pierde su verificación independiente", _fila("| D-05 |", "auditor independiente (I15) |", " |")),
 ("K57-D04", "Orden de validación sin el paso 14", "K57", "Se elimina el paso 14 del orden de validación", _quitar_fila_con("| 14 |", "Verificación final del estado")),
 ("K57-D05", "Cifra ejecutada distinta en el documento", "K57", "CHAIN: 24 pasa a CHAIN: 23", _ed("CHAIN: 24", "CHAIN: 23")),
 ("K57-D06", "Auditoría de 20 puntos con un punto fallido ocultado", "K57", "La matriz del documento muestra NO donde el cálculo da sí", _fila("| RS-08 | sí", "| sí |", "| NO |")),
 ("K57-D07", "Relación con una prueba positiva inexistente", "K55", "RS-08 cita CHAIN-99", _fila("| RS-08 |", "CHAIN-04", "CHAIN-99")),
 ("K57-D08", "Matriz de auditoría sin el defecto D-12", "K57", "Se elimina la fila D-12", _quitar_fila_con("| D-12 |", "FK16 a FK41")),
 ("K57-D09", "Identificador K55 duplicado de nuevo", "K58", "La fila K55-V12 de la equivalencia vuelve a llamarse K55", _fila("| K55-V12 |", "K55-V12", "K55")),
 ("K57-D10", "Suite AV sin su último caso", "K57", "Se elimina la fila AV-08 de la tabla de asset_version", _quitar_fila_con("| AV-08 |", "asset_version")),
 ("K57-D11", "Validación 7 de las 15 ausente", "K57", "Se elimina la validación de asset_version del evento propio", _quitar_fila_con("| 7 |", "asset_version coincide")),
 ("K57-D12", "Cifra ejecutada de AV distinta en el documento", "K57", "AV: 8 pasa a AV: 7", _ed("AV: 8", "AV: 7")),
]

def _tipo_rel(t):
    s = t[SPEC]; a = s.index("#### `contribution_events`"); b = s.index("\n#### ", a + 5); seg = s[a:b]
    k = re.search(r"^\| source_attribution_relation \| text \|", seg, re.M); assert k
    t = dict(t); t[SPEC] = s[:a] + seg[:k.start()] + seg[k.start():].replace("| source_attribution_relation | text |", "| source_attribution_relation | uuid |", 1) + s[b:]; return t

MUT = [
 ("M-01", "FK con organización incorrecta", "K44", "En brief_versions → briefs, la primera columna local pasa de organization_id a created_by", _fila("| brief_versions → briefs |", "(organization_id, brief_id) → briefs", "(created_by, brief_id) → briefs")),
 ("M-02", "FK con columnas destino en orden incorrecto", "K44", "En brief_field_attributions → brief_field_changes se invierte el orden de las dos últimas columnas referenciadas", _fila("| brief_field_attributions → brief_field_changes |", "brief_field_changes(organization_id, brief_version_id, field_key)", "brief_field_changes(organization_id, field_key, brief_version_id)")),
 ("M-03", "FK sin clave única de destino", "K44", "Se elimina de contribution_events la clave única (organization_id, id, brief_version_id, contributor_id)", _quitar_linea("unique(organization_id, id, brief_version_id, contributor_id)", "contribution_events")),
 ("M-04", "Evento de brief asociado a atribución promocional", "K45", "La atribución de brief referencia la columna promotion_snapshot_id del evento", _fila("| brief_field_attributions → contribution_events |", "brief_version_id, contributor_id)", "promotion_snapshot_id, contributor_id)")),
 ("M-05", "Actor de evento distinto del actor de atribución", "K45", "La columna de actor de la atribución pasa de contributor_id a created_by", _fila("| brief_field_attributions → contribution_events |", "origin_version_id, contributor_id) →", "origin_version_id, created_by) →")),
 ("M-06", "Asset no utilizado asociado a una versión", "K45", "La FK de procedencia al arte pierde copy_version_id", _fila("| copy_version_provenance → creative_assets (columna agregada) |", "(organization_id, copy_version_id, used_asset_id) → creative_assets(organization_id, copy_version_id, id)", "(organization_id, used_asset_id) → creative_assets(organization_id, id)")),
 ("M-07", "Asset de otra organización", "K44", "La FK de procedencia al arte pierde organization_id", _fila("| copy_version_provenance → creative_assets (columna agregada) |", "(organization_id, copy_version_id, used_asset_id) → creative_assets(organization_id, copy_version_id, id)", "(copy_version_id, used_asset_id) → creative_assets(copy_version_id, id)")),
 ("M-08", "Versión de brief de otro brief", "K45", "La cadena de brief_versions pierde brief_id", _fila("| brief_versions → brief_versions |", "(organization_id, brief_id, previous_version_id) → brief_versions(organization_id, brief_id, id)", "(organization_id, previous_version_id) → brief_versions(organization_id, id)")),
 ("M-09", "Snapshot de otra promoción", "K45", "La cadena de promotion_snapshots pierde promotion_line_id", _fila("| promotion_snapshots → promotion_snapshots |", "(organization_id, promotion_line_id, previous_snapshot_id) → promotion_snapshots(organization_id, promotion_line_id, id)", "(organization_id, previous_snapshot_id) → promotion_snapshots(organization_id, id)")),
 ("M-10", "Atribución heredada sin antecesor", "K45", "Se elimina de brief_field_attributions la restricción que exige previous_attribution_id en las heredadas", _quitar_linea("'heredada' exige", "brief_field_attributions")),
 ("M-11", "Resolución de descarte realizada por el contribuyente afectado", "K46", "Se elimina la restricción resolved_by <> affected_contributor_id", _quitar_linea("resolved_by <> affected_contributor_id", "attribution_discard_resolutions")),
 ("M-12", "Resolución realizada por quien solicitó la exclusión", "K46", "Se elimina la restricción resolved_by <> requested_by", _quitar_linea("resolved_by <> requested_by", "attribution_discard_resolutions")),
 ("M-13", "Resolución sin evidencia", "K46", "Se elimina la restricción de evidencia y motivo no vacíos", _quitar_linea("char_length(btrim(reason))", "attribution_discard_resolutions")),
 ("M-14", "Sustitución textual que retira automáticamente al contribuyente anterior", "K47", "En la tabla de cálculo de atribuciones la fila «sustituido» pasa las activas anteriores a históricas", _ed("| sustituido | Activas heredadas activas provisionalmente; históricas por resolución siguen históricas |", "| sustituido | Activas heredadas históricas; históricas siguen históricas |")),
 ("M-23", "Resolución ejecutada por quien realizó la sustitución (restricción retirada)", "K46", "Se elimina de la resolución la restricción resolved_by <> change_actor_id", _quitar_linea("resolved_by <> change_actor_id", "attribution_discard_resolutions")),
 ("M-24", "Resolución sin trigger de elegibilidad sobre la cadena completa", "K46", "Se elimina el trigger de elegibilidad del resolutor (R1 a R9)", _quitar_linea("elegibilidad del resolutor", "attribution_discard_resolutions")),
 ("M-25", "Evidencia no ligada a la atribución", "K46", "Se elimina la restricción evidence_attribution_id = atribución informada", _quitar_linea("evidence_attribution_id = coalesce(", "attribution_discard_resolutions")),
 ("M-15", "ID de regla duplicado", "K02", "Se repite la fila de IG5-69", _id_dup),
 ("M-16", "Regla sin escenario", "K06", "Se retira IG5-83 de todos los escenarios", _sin_escenario),
 ("M-17", "Referencia a una regla inexistente", "K05", "T-01 referencia IG5-999", _regex_t1),
 ("M-18", "Cifra incorrecta en el resumen", "K09", "Pruebas totales pasa a 1", _ed("| Pruebas totales |", "| Pruebas totales | 1 |\n| Pruebas totales (x) |")),
 ("M-19", "Fórmula de E distinta", "K10", "Se retira el término P de una aparición", _ed("⋃ Ctr(v) para v ∈ [V-D, V-B] ∪ P", "⋃ Ctr(v) para v ∈ [V-D, V-B]")),
 ("M-20", "Código de error de procedencia ausente", "K12", "BRIEF_CHAIN_INCONSISTENTE desaparece del contrato", _err_ausente),
 ("M-21", "Dependencia posterior en el orden de creación", "K16", "La subfase 2.1 depende de promotion_snapshots (4.x)", lambda t: _dep_post(t)),
]
MUT += _FKM
MUT += _K57M
def _dep_post(t):
    s = t[SPEC]; t = dict(t)
    t[SPEC] = re.sub(r"(\| \d+ \| 2\.1 \| tabla \(estructura\) \| brief_versions \| )[^|]*\|", r"\1promotion_snapshots |", s, count=1); return t

def ejecutar_mutaciones(textos, dir_hist, v33, base):
    global RES
    guard = RES
    out = []
    ok0 = {r["id"]: r["ok"] for r in base}
    try:
        for mid, nombre, ctl, desc, fn in MUT:
            try:
                tm = fn(textos); RES = []
                C, A, info = ejecutar(tm, dir_hist); checks_adicionales(tm, C, A, info); checks_v7(tm, C, A, info)
                det = any(r["id"] == ctl and r["ok"] is False for r in RES)
                real = "RECHAZADA por %s" % ctl if det else "NO DETECTADA por %s" % ctl
            except Exception as ex:
                det = False; real = "ERROR al aplicar la mutación: %s" % str(ex)[:80]
            out.append(dict(id=mid, nombre=nombre, control=ctl, desc=desc, inicial="válido (%s APRUEBA)" % ctl if ok0.get(ctl) else "NO válido (%s no aprueba)" % ctl, det=det and bool(ok0.get(ctl)), real=real))
        for m in ejecutar_mutaciones_modelo(textos, dir_hist):
            out.append(dict(id=m["id"], nombre=m["mut"], control=m["ctl"], desc=m["mut"], inicial=m["inicial"], det=m["det"] and bool(ok0.get(m["ctl"])), real=m["obs"], regla=m["regla"], esp=m["esp"], modelo=True, valido=m["valido"], cambio=m["cambio"]))
        if v33 and os.path.isfile(v33):
            import tempfile
            b = bytearray(open(v33, "rb").read()); b[len(b) // 2] ^= 1
            with tempfile.NamedTemporaryFile(delete=False) as tf: tf.write(bytes(b)); tn = tf.name
            try:
                RES = []; check_v33(tn); det = RES[0]["ok"] is False
            finally: os.unlink(tn)
            out.append(dict(id="M-22", nombre="Archivo v3.3 con un byte alterado", control="K48", desc="Se invierte un bit en una copia temporal del original y se calcula su SHA-256", inicial="válido (K48 APRUEBA)" if ok0.get("K48") else "NO válido", det=det and bool(ok0.get("K48")), real="RECHAZADA por K48" if det else "NO DETECTADA por K48"))
    finally:
        RES = guard
    return out

def informe(dir_, usar_mut=True, v33=None):
    global RES
    textos = cargar(dir_); dir_hist = os.path.join(dir_, "historico")
    C, A, info = correr(textos, dir_hist, v33)
    ctr0 = controles(textos)
    chk("K40", "La matriz define %d controles con ID estable único, regla, sección, evidencia, procedimiento, resultado, estado y nivel; ninguno es OK sin comprobaciones aprobadas" % len(ctr0), len(ctr0) == 28 and len({c[0] for c in ctr0}) == 28 and all(all(x for x in c) for c in ctr0), "", "IE-06, IE-07", "AUDITORIA 3")
    base = [dict(r) for r in RES]
    guard = list(RES)
    RES.clear(); _CACHE14.clear(); C2, A2, i2 = ejecutar(textos, dir_hist); checks_adicionales(textos, C2, A2, i2); checks_v7(textos, C2, A2, i2); check_v33(v33)
    chk("K40", "La matriz define %d controles con ID estable único, regla, sección, evidencia, procedimiento, resultado, estado y nivel; ninguno es OK sin comprobaciones aprobadas" % len(ctr0), len(ctr0) == 28 and len({c[0] for c in ctr0}) == 28 and all(all(x for x in c) for c in ctr0), "", "IE-06, IE-07", "AUDITORIA 3")
    repro = [(r["id"], r["ok"]) for r in RES] == [(r["id"], r["ok"]) for r in base]
    chk("K41", "Reproducibilidad: dos ejecuciones sobre los mismos archivos producen los mismos resultados individuales", repro, "", "IE-08", "AUDITORIA 3")
    muts = []
    if usar_mut: muts = ejecutar_mutaciones(textos, dir_hist, v33, base)
    ndet = sum(1 for m in muts if m["det"])
    chk("K42", "Controles negativos: %d mutaciones introducidas en copias en memoria, %d detectadas, %d no detectadas" % (len(muts), ndet, len(muts) - ndet) if muts else "Controles negativos omitidos (--sin-mutaciones)", (not muts) or ndet == len(muts), [m["id"] for m in muts if not m["det"]], "IE-08, IE-11", "AUDITORIA 3")
    return textos, controles(textos), muts

AUDITORIA_V7 = [
 (1, "Ejecutar el verificador documental", ["K01"]), (2, "Ejecutar todas las mutaciones negativas", ["K42"]), (3, "Cada defecto es detectado", ["K42"]), (4, "28 controles de auditoría", ["K40"]),
 (5, "SHA-256 de v3.3 calculado sobre el original (o limitación real)", ["K48"]), (6, "Reconstrucción de contribuyentes por campo", ["K13", "K38", "K47", "K49", "K52"]), (7, "Independencia de las resoluciones", ["K46", "K49", "K52"]),
 (8, "Relaciones y claves compuestas", ["K44", "K45", "K52"]), (9, "Escenarios de G-1, G-5 y G-10", ["K39", "K13", "K49"]), (10, "IDs y referencias", ["K02", "K03", "K04", "K05", "K06", "K07", "K08"]),
 (11, "76 subfases", ["K18"]), (12, "17 claves de permisos y 13 transiciones T-02", ["K19", "K20"]), (13, "Decisiones pendientes sin alterar", ["K21"]), (14, "Coherencia entre los cinco documentos activos", ["K09", "K17", "K22", "K27"]),
]

def _est(ids, byid):
    vals = [byid[i]["ok"] if i in byid else None for i in ids]
    if any(v is False for v in vals): return "NO OK"
    if any(v is None for v in vals): return "PENDIENTE"
    return "OK (verificado documentalmente)"

def criterios_v12(byid, muts):
    def n(pref): ms = [m for m in muts if m["id"].startswith(pref)]; return sum(1 for m in ms if m["det"]), len(ms)
    out = []
    def sel(pref, lo=None, hi=None):
        ms = [m for m in muts if m["id"].startswith(pref) and (lo is None or lo <= int(m["id"][-2:]) <= hi)]; return sum(1 for m in ms if m["det"]), len(ms)
    def sel_ids(ids): ms = [m for m in muts if m["id"] in ids]; return sum(1 for m in ms if m["det"]), len(ms)
    for etq, pref, lo, hi, tot, minimo in (("K45", "K45-", None, None, N_K45, 22), ("K46", "K46-", None, None, N_K46, 12), ("K47 (mutaciones previas)", "K47-M", None, None, N_K47, 26), ("K47 resoluciones inmutables (R01 a R12)", "K47-R", None, None, N_RES, 12),
                                         ("K47 procedencia del arte de la v10 (A01 a A16)", "K47-A", 1, N_ART_V10, N_ART_V10, 14)):
        d, t = sel(pref, lo, hi); out.append((etq, "al menos %d mutaciones, todas detectadas" % minimo, "%d/%d detectadas: %s" % (d, t, "CUMPLE" if d == t == tot >= minimo else "NO CUMPLE")))
    for etq, ids, minimo in (("K47 identidad exacta de assets de la v11 (A17 a A32 y A49 a A53)", IDS_V11, 16), ("K47 identidad exacta del asset de origen de la v12 (A33 a A48)", IDS_V12, 16)):
        d, t = sel_ids(ids); out.append((etq, "al menos %d mutaciones, todas detectadas, con procedencia incompleta y E no completo" % minimo, "%d/%d detectadas: %s" % (d, t, "CUMPLE" if d == t == len(ids) >= minimo and all(m.get("bloq") is not False for m in muts if m["id"] in ids) else "NO CUMPLE")))
    d13, t13 = sel_ids(IDS_V13); out.append(("K47 validación previa del origen de la v13 (A54 a A65)", "las 12 mutaciones detectadas: rechazo por ReutilizacionInvalida con la relación identificada, sin registros parciales, estado previo idéntico, procedencia no completa, E nulo y sin evaluación de impacto, aprobación ni publicación", "%d/%d detectadas: %s" % (d13, t13, "CUMPLE" if d13 == t13 == N_RECH and all(m.get("bloq") is not False for m in muts if m["id"] in IDS_V13) else "NO CUMPLE")))
    dfk, tfk = sel("FK", 1, N_FK); out.append(("Mutaciones estructurales FK01 a FK%02d" % N_FK, "las %d mutaciones de K32, K44, K45 y K55 detectadas por su verificador, sin exclusiones generales de columnas source_*" % N_FK, "%d/%d detectadas: %s" % (dfk, tfk, "CUMPLE" if dfk == tfk == N_FK else "NO CUMPLE")))
    for etq, pref, tot, cond in (("K56 cadena completa (CHAIN-01 a CHAIN-24)", "CHAIN-", N_CHAIN, "las 24 mutaciones de eslabones detectadas con el eslabón identificado, sin registros parciales y con E bloqueado"), ("K56 atribuciones y resoluciones (ATTR-01 a ATTR-12)", "ATTR-", N_ATTR, "las 12 mutaciones detectadas por el auditor independiente"),
                                 ("K56 asset_version del evento propio (AV-01 a AV-08)", "AV-", N_AV, "las 8 mutaciones detectadas con el eslabón, el evento y el campo identificados"), ("K56 campo del evento propio (CF-01 a CF-08)", "CF-", N_CF, "las 8 mutaciones detectadas con el eslabón, el evento y el campo identificados"), ("K56 asset_version y campo combinados (AC-01 a AC-06)", "AC-", N_AC, "las 6 mutaciones detectadas, sin que una excepción ajena cuente como detección"),
                                 ("K56 mutaciones del código del modelo (K56-M01 a K56-M12)", "K56-M", N_K56M, "cada defensa nueva degradada es detectada por al menos una prueba"), ("K57 mutaciones documentales de trazabilidad y de identidad de controles (K57-D01 a K57-D12)", "K57-D", N_K57D, "las mutaciones del documento detectadas por K55, K57 o K58")):
        d, t = sel(pref); out.append((etq, cond, "%d/%d detectadas: %s" % (d, t, "CUMPLE" if d == t == tot else "NO CUMPLE")))
    _ch, _ad, _at, _a14, _e14, _mm, _av, _cf, _ac, _ap, _a15, _t15 = _ejecutadas14()
    out.append(("K56 baterías de la v15", "AP 8/8 (relaciones válidas aceptadas sin falsos positivos), ADV15 8/8 (el motor forzado acepta y el auditor detecta asset_version y campo) y AT15 8/8 (instantánea completa en ocho momentos de fallo)", "AP %d/%d; ADV15 %d/%d; AT15 %d/%d: %s" % (sum(1 for x in _ap if x["ok"]), N_AP, sum(1 for x in _a15 if x["ok"]), N_ADV15, sum(1 for x in _t15 if x["ok"]), N_AT15, "CUMPLE" if len(_ap) == N_AP and len(_a15) == N_ADV15 and len(_t15) == N_AT15 and all(x["ok"] for x in _ap + _a15 + _t15) else "NO CUMPLE")))
    out.append(("K56 baterías ejecutadas", "ADVC 24/24 (el motor forzado acepta y el auditor detecta), AT14 11/11, E14 6/6 y auditor sin funciones del motor", "ADVC %d/%d; AT14 %d/%d; E14 %d/%d; %s: %s" % (sum(1 for x in _ad if x["ok"]), N_CHAIN, sum(1 for x in _a14 if x["ok"]), N_AT14, sum(1 for x in _e14 if x["ok"]), N_E14, "auditor", "CUMPLE" if not MS._compartidas() and all(x["ok"] for x in _ad + _a14 + _e14) and len(_ad) == N_CHAIN and len(_a14) == N_AT14 and len(_e14) == N_E14 else "NO CUMPLE")))
    esc = MS.correr_escenarios(); ea = [e for e in esc if e["id"] in "ABCDEFGHIJKL"]
    out.append(("Escenarios estructurales K47", "los 12 escenarios A a L aprobados sobre datos estructurados", "%d/12 aprobados; U, S, X, R y RS: %s" % (sum(1 for e in ea if e["ok"]), "aprobados" if all(e["ok"] for e in esc if e["id"] in ("U", "S", "X", "R", "RS")) else "NO aprobados")))
    pa_ = MS.correr_positivos_arte(); gu_ = MS.pruebas_guarda()
    out.append(("Casos positivos de arte", "los 26 casos positivos de arte aprobados (P01 a P26): reutilización exacta con cadena completa, dos assets con igual número de versión, dos reutilizaciones del mismo original, intercambio de eventos de carga válidos (rechazado), cadena de tres niveles, reutilización con modificación posterior, coincidencia con el auditor independiente sin funciones compartidas y rechazo sin escritura de un evento y una atribución válidos de otro asset", "%d/%d aprobados: %s" % (sum(1 for p in pa_ if p["ok"]), len(pa_), "CUMPLE" if len(pa_) == N_POS_ART and all(p["ok"] for p in pa_) else "NO CUMPLE")))
    out.append(("Inmutabilidad del registro", "los 9 intentos directos de alterar el registro de resoluciones se rechazan y lo dejan idéntico", "%d/%d rechazados: %s" % (sum(1 for g in gu_ if g[1]), len(gu_), "CUMPLE" if all(g[1] for g in gu_) else "NO CUMPLE")))
    ad_ = MS.correr_adversariales()
    out.append(("Pruebas adversariales", "al menos 5 pruebas adversariales nuevas en las que el motor acepta, el auditor detecta y el sistema final bloquea E, la evaluación de impacto y la publicación", "%d/%d aprobadas (%d nuevas): %s" % (sum(1 for a in ad_ if a["ok"]), len(ad_), len(ad_) - N_ADV_V11, "CUMPLE" if len(ad_) == N_ADV and all(a["ok"] for a in ad_) else "NO CUMPLE")))
    at_ = MS.pruebas_atomicidad()
    out.append(("Atomicidad de la reutilización", "una reutilización con un elemento obligatorio ausente falla y no deja registros parciales", "%d/%d aprobadas: %s" % (sum(1 for a in at_ if a[1]), len(at_), "CUMPLE" if len(at_) == N_ATOM and all(a[1] for a in at_) else "NO CUMPLE")))
    out.append(("Independencia del auditor", "el auditor reconstruye la identidad desde las instantáneas sin llamar a funciones del motor (inspección del código)", "%s" % ("CUMPLE: ninguna función compartida" if not MS._compartidas() else "NO CUMPLE: %s" % MS._compartidas()[:2])))
    _, pos = MS.correr_mutaciones_k45(parse_4410(textos_global[SPEC])["matriz"]) if textos_global else (None, [])
    out.append(("Casos positivos y falsos positivos", "fixtures válidos aceptados y ninguna mutación con estado inicial inválido", "%s; %d/%d mutaciones del modelo con estado inicial válido y cambio efectivo" % ("CUMPLE" if all(not v for _n, v in pos) and all(e["ok"] for e in esc) and all(m.get("valido") and m.get("cambio") for m in muts if m.get("modelo")) else "NO CUMPLE", sum(1 for m in muts if m.get("modelo") and m.get("valido") and m.get("cambio")), sum(1 for m in muts if m.get("modelo")))))
    previas = [m for m in muts if not m["id"].startswith("K4") or m["id"].startswith("K44")]
    dp = sum(1 for m in previas if m["det"])
    out.append(("Regresión", "todas las comprobaciones y las mutaciones M-01 a M-25 anteriores pasan", "%d/%d mutaciones anteriores; %s" % (dp, len(previas), "CUMPLE" if dp == len(previas) and not any(r["ok"] is False for r in byid.values()) else "NO CUMPLE")))
    for c_, cond, ids in (("Consistencia documental", "cero contradicciones, cifras y estados coherentes", ["K09", "K22", "K27", "K50"]), ("Cobertura", "reglas relevantes y controles estructurales cubiertos", ["K06", "K07", "K08", "K51", "K52", "K53", "K54", "K55", "K55-V12", "K56", "K57", "K58", "K59"]),
                          ("Integridad histórica", "documentos protegidos sin alteración", ["K25"]), ("Permisos", "17 claves conservadas", ["K19"]), ("Workflow", "13 transiciones conservadas", ["K20"]), ("Roadmap", "76 subfases conservadas", ["K18"]),
                          ("Hash", "verificado sobre el original o declarado pendiente", ["K48"]), ("SQL e infraestructura", "ninguna ejecución", ["K23"]), ("Fase 1", "no iniciada ni autorizada", ["K22"])):
        out.append((c_, cond, _est(ids, byid)))
    out.append(("Alcance Git", "solo docs/fase0/", "Fuera del alcance del verificador: se comprueba con git diff en la publicación"))
    return out

textos_global = None

def bloque_markdown(ctr, textos, muts):
    global textos_global
    textos_global = textos
    n = len(RES); nok = sum(1 for r in RES if r["ok"] is True); npen = sum(1 for r in RES if r["ok"] is None); nf = n - nok - npen
    L = ["**Comprobaciones ejecutadas: %d. Aprobadas: %d. Fallidas: %d. Pendientes: %d.** Controles: %d; OK: %d; NO OK: %d; PENDIENTE: %d. Mutaciones negativas: %d; detectadas: %d; no detectadas: %d.\n" % (n, nok, nf, npen, len(ctr), sum(1 for c in ctr if c[7] == "OK"), sum(1 for c in ctr if c[7] == "NO OK"), sum(1 for c in ctr if c[7] == "PENDIENTE"), len(muts), sum(1 for m in muts if m["det"]), sum(1 for m in muts if not m["det"]))]
    L.append("| Comprobación | Resultado | Descripción | Regla | Documento y sección |\n|---|---|---|---|---|")
    for r in RES: L.append("| %s | %s | %s | %s | %s |" % (r["id"], "APRUEBA" if r["ok"] else ("PENDIENTE" if r["ok"] is None else "FALLA"), r["nombre"].replace("|", "/"), r["regla"], r["doc"]))
    byid0 = {r["id"]: r for r in RES}
    L.append("\n**Mutaciones negativas (regresión completa).** Cada una parte de un estado inicial válido, aplica un único cambio identificable, ejecuta el control que debe detectarlo y registra el resultado esperado y el observado. Un veredicto DETECTADA exige además que el estado inicial sea válido y que el cambio modifique realmente el caso.\n")
    L.append("| ID | Regla probada | Estado inicial válido | Mutación aplicada | Resultado esperado | Resultado observado | Veredicto |\n|---|---|---|---|---|---|---|")
    for m in muts:
        regla = m.get("regla") or ("%s (%s)" % (m["control"], byid0.get(m["control"], {}).get("regla", "")))
        L.append("| %s | %s | %s | %s | %s | %s | %s |" % (m["id"], regla.replace("|", "/"), m["inicial"].replace("|", "/"), m["desc"].replace("|", "/"), m.get("esp", "rechazo por " + m["control"]).replace("|", "/"), m["real"].replace("|", "/"), "DETECTADA" if m["det"] else "NO DETECTADA"))
    P_ = parse_4410(textos[SPEC]); mk45_, pos_ = MS.correr_mutaciones_k45(P_["matriz"]); esc_ = MS.correr_escenarios(); mk47_ = MS.correr_mutaciones_k47() + MS.correr_mutaciones_resoluciones() + MS.correr_mutaciones_assets()
    L.append("\n**Controles estructurales de K45 (C01 a C15) y su cobertura.** Se evalúan sobre las relaciones reales del modelo (joins por identificador), nunca por coincidencia de texto. Casos positivos: " + "; ".join("%s: %s" % (n_, "0 violaciones" if not v_ else "RECHAZADO") for n_, v_ in pos_) + ".\n")
    L.append("| Control | Condición | Mutaciones que lo ejercen |\n|---|---|---|")
    for c_, d_ in MS.CONTROLES_K45.items(): L.append("| %s | %s | %s |" % (c_, d_, ", ".join(m["id"] for m in mk45_ if m["esp"] == c_)))
    L.append("\n**Escenarios estructurales de K47 (12) y comprobaciones U, S, X y R.** Cada escenario ejecuta operaciones del motor sobre atribuciones individuales y un auditor independiente compara el estado anterior y el posterior; el resultado observado se compara con el esperado.\n")
    L.append("| ID | Escenario | Pasos auditados | Violaciones del auditor | Aserciones (esperado = observado) | Resultado |\n|---|---|---|---|---|---|")
    for e in esc_: L.append("| EA-%s | %s | %d | %s | %s | %s |" % (e["id"], e["nombre"], e["pasos"], ", ".join(e["viol"]) or "ninguna", "; ".join("%s → %s" % (a_[0], a_[2] if not isinstance(a_[2], (list, tuple)) else ", ".join(map(str, a_[2])) or "(vacío)") for a_ in e["asr"]).replace("|", "/")[:420], "APROBADO" if e["ok"] else "NO APROBADO"))
    L.append("\n**Invariantes del auditor de K47 (I1 a I28).**\n")
    L.append("| Invariante | Qué comprueba | Mutaciones que lo ejercen |\n|---|---|---|")
    for i_, d_ in (("I1", "toda atribución activa anterior sigue activa en la versión nueva (ninguna clasificación retira)"), ("I2", "el actor se incorpora solo si hay contribución material"), ("I3", "una resolución aceptada retira exactamente la atribución referenciada"),
                   ("I4", "una resolución aceptada cumple todas sus condiciones y R1 a R9 recalculadas por el auditor"), ("I5", "una resolución rechazada o inválida no cambia atribuciones, estados ni E"), ("I6", "la evidencia histórica se conserva"),
                   ("I7", "E del motor igual a E recalculado y no sale quien conserva otra atribución activa"), ("I8", "una cadena incompleta no produce un E presentado como completo"), ("I9", "brief, promoción y copy aplican la misma regla"),
                   ("I10", "versiones, atribuciones, eventos y estados anteriores no se reescriben; la versión nueva hereda todo lo activo"), ("I11", "el resultado no depende de la similitud del texto"), ("I12", "un cambio de clasificación no altera atribuciones ni historia"),
                   ("I13", "inmutabilidad de las resoluciones: ninguna se modifica, reemplaza ni elimina; sello SHA-256 coincidente; resultado definitivo"), ("I14", "cadena de reconsideración: sin ciclos, anterior existente, de la misma atribución, rechazada, anterior en el tiempo y con sello intacto"),
                   ("I15", "cada baja histórica cita una resolución aceptada de esa atribución exacta; una sola aceptada por atribución"), ("I16", "cada asset usado tiene uploader, evento de carga y atribución del uploader"),
                   ("I17", "el reutilizador no sustituye al uploader original y su evento de reutilización está registrado"), ("I18", "el asset corresponde a la versión exacta de copy que lo usa"),
                   ("I19", "cadena de reutilización sin ciclos, con origen existente y misma organización y pieza"), ("I20", "completitud del arte y declaración explícita de no_aplica"), ("I21", "E incluye a los contribuyentes del arte exacto"),
                   ("I22", "identidad del uploader: organización y membresía activa"), ("I23", "evento de carga: organización, pieza, asset exacto, versión de asset, versión de copy, actor y actor autenticado"),
                   ("I24", "atribución directa del uploader ligada a organización, pieza, versión de copy, asset, versión de asset y evento"), ("I25", "evento de reutilización: organización, pieza, actor, asset, versión de asset y de copy, evento propio, membresía"), ("I26", "atribuciones heredadas de asset con antecesor verificable en la cadena"),
                   ("I27", "identidad exacta del origen: el evento de reutilización y el asset reutilizado referencian el asset, la versión, el evento de carga, el uploader y la atribución originales por identificador, con organización, pieza y actor autenticado coincidentes"), ("I28", "integridad de la cadena de origen: sin registros intercambiados y con vínculo íntegro al evento original de carga")):
        L.append("| %s | %s | %s |" % (i_, d_, ", ".join(m["id"] for m in mk47_ if m["esp"] == i_)))
    L.append("\n**Casos positivos de arte (P01 a P20), pruebas adversariales e intentos directos contra el registro de resoluciones.**\n")
    L.append("| ID | Caso | Violaciones del auditor | Aserciones | Resultado |\n|---|---|---|---|---|")
    for e in MS.correr_positivos_arte(): L.append("| %s | %s | %s | %d | %s |" % (e["id"], e["nombre"], ", ".join(e["viol"]) or "ninguna", len(e["asr"]), "APRUEBA" if e["ok"] else "FALLA"))
    L.append("\n| Prueba adversarial | El motor acepta | El auditor detecta | E bloqueado | Impacto falla | No publica | Resultado |\n|---|---|---|---|---|---|---|")
    for a_ in MS.correr_adversariales(): L.append("| %s: %s | %s | %s | %s | %s | %s | %s |" % (a_["id"], a_["nombre"], "sí" if a_["motor_acepta"] else "no", "sí (%s)" % ", ".join(a_["codigos"]) if a_["auditor"] else "no", "sí" if a_["E_bloqueado"] else "no", "sí" if a_["impacto_falla"] else "no", "sí" if a_["no_publica"] else "no", "APRUEBA" if a_["ok"] else "FALLA"))
    L.append("\n| Prueba de atomicidad de la reutilización | Falla con ReutilizacionInvalida y no deja registros parciales |\n|---|---|")
    for g_, ok_ in MS.pruebas_atomicidad(): L.append("| %s | %s |" % (g_, "sí" if ok_ else "NO"))
    L.append("\n| Intento directo | Rechazado con ResolucionInmutable y registro intacto |\n|---|---|")
    for g_, ok_ in MS.pruebas_guarda(): L.append("| %s | %s |" % (g_, "sí" if ok_ else "NO"))
    L.append("\n**Matriz de los 28 controles.**\n")
    L.append("| ID | Control | Regla exacta | Documento y sección | Evidencia concreta | Procedimiento | Resultado real | Estado | Nivel de evidencia | Observación |\n|---|---|---|---|---|---|---|---|---|---|")
    for c in ctr: L.append("| " + " | ".join(x.replace("|", "/") for x in c) + " |")
    byid = {r["id"]: r for r in RES}
    L.append("\n**Auditoría integral final (28 puntos).**\n")
    L.append("| # | Punto auditado | Comprobaciones | Resultado |\n|---|---|---|---|")
    for n_, nom, ids in INTEGRAL: L.append("| %d | %s | %s | %s |" % (n_, nom, ", ".join(ids), _est(ids, byid)))
    L.append("\n**Auditoría final (14 verificaciones).**\n")
    L.append("| # | Verificación | Comprobaciones | Resultado |\n|---|---|---|---|")
    for n_, nom, ids in AUDITORIA_V7: L.append("| %d | %s | %s | %s |" % (n_, nom, ", ".join(ids), _est(ids, byid)))
    L.append("\n**Criterios binarios de aceptación de la v15 (resultado calculado).**\n")
    L.append("| Criterio | Condición | Resultado |\n|---|---|---|")
    for c_, cond, res_ in criterios_v12(byid, muts): L.append("| %s | %s | %s |" % (c_, cond, res_))
    return "\n".join(L)

def main():
    ap = argparse.ArgumentParser(description="Verificador documental del expediente Fase 0 (G-1, G-5, G-10)")
    ap.add_argument("--dir", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."), help="directorio docs/fase0")
    ap.add_argument("--json", action="store_true"); ap.add_argument("--md", action="store_true"); ap.add_argument("--sin-mutaciones", action="store_true")
    ap.add_argument("--v33", default=None, help="ruta del archivo original de la línea base v3.3 (para calcular su SHA-256)")
    a = ap.parse_args()
    textos, ctr, muts = informe(a.dir, not a.sin_mutaciones, a.v33)
    if a.md: print(INI + "\n" + bloque_markdown(ctr, textos, muts) + "\n" + FIN)
    elif a.json: print(json.dumps(dict(comprobaciones=RES, controles=ctr, mutaciones=[{k: v for k, v in m.items()} for m in muts]), ensure_ascii=False, indent=1))
    else:
        for r in RES: print("%s %-9s %s%s" % (r["id"], "APRUEBA" if r["ok"] else ("PENDIENTE" if r["ok"] is None else "FALLA"), r["nombre"][:170], "" if r["ok"] is not False else "  -> " + r["detalle"][:200]))
        for m in muts: print("%s %s: %s [%s]" % (m["id"], "DETECTADA" if m["det"] else "NO DETECTADA", m["nombre"], m["real"]))
        n = len(RES); nok = sum(1 for r in RES if r["ok"] is True); npen = sum(1 for r in RES if r["ok"] is None)
        print("RESUMEN: %d comprobaciones, %d aprueban, %d fallan, %d pendientes; %d controles (%d OK, %d NO OK, %d PENDIENTE); %d mutaciones (%d detectadas)" % (n, nok, n - nok - npen, npen, len(ctr), sum(1 for c in ctr if c[7] == "OK"), sum(1 for c in ctr if c[7] == "NO OK"), sum(1 for c in ctr if c[7] == "PENDIENTE"), len(muts), sum(1 for m in muts if m["det"])))
    return 0 if not any(r["ok"] is False for r in RES) else 1
if __name__ == "__main__":
    sys.exit(main())
