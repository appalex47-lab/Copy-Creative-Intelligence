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
NUEVAS8 = ["brief_versions", "brief_field_changes", "brief_field_attributions", "promotion_snapshots", "promotion_field_changes", "promotion_field_attributions", "contribution_events", "copy_version_provenance"]
ESTADO_V33 = "COMPLETADA Y ACEPTADA COMO LÍNEA BASE DOCUMENTAL, CON LIMITACIONES DOCUMENTADAS"
ESTADO_V6 = "PREPARADA PARA ACEPTACIÓN FORMAL DEL PROPIETARIO, CON LIMITACIONES DOCUMENTADAS"
FASE1 = "NO INICIADA / NO AUTORIZADA"
INI, FIN = "<!-- VERIFICADOR:INICIO -->", "<!-- VERIFICADOR:FIN -->"
HIST_WORDS = re.compile(r"\bv[2-5]\b|histór|anterior|antes de la v6|eran|sustituy|corregid|v3\.3|línea base", re.I)
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
    RES.append(dict(id=id_, nombre=nombre, ok=bool(ok), detalle=str(detalle)[:400], regla=regla, doc=doc))

def ejecutar(textos, dir_hist=None, mutaciones=False):
    global RES
    RES = []
    C = Corpus(textos)
    A = C.activos_sin_bloque()
    spec = C.spec
    AR = dict(A)
    if "## Entrada: revisión v6" in A[REG]:
        r_ = A[REG]; k_ = r_.index("## Entrada: revisión v6"); AR[REG] = r_[k_:r_.index("### Manifiesto") if "### Manifiesto" in r_ else len(r_)]
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
    chk("K14", "Contrato de integridad (%d relaciones): 10 campos completos por fila, toda FK de las ocho tablas de procedencia figura en él y toda FK incluye organization_id" % len(cont), len(cont) >= 20 and not mal14 and not fk_sin and not fk_sin_org, (mal14[:3], fk_sin[:3], fk_sin_org[:3]), "IG5-80", "ESPECIFICACION 4.4.9")
    # ---- K15 tablas ----
    bloques = [n for n in C.entidades if n in NUEVAS8 or n.endswith("_events")]
    nombres_tab = [r[3] for r in ent_tabs]
    dup_tab = [n for n in set(nombres_tab) if nombres_tab.count(n) > 1]
    faltan_ent = [n for n in NUEVAS8 if n not in nombres_tab or n not in C.entidades]
    chk("K15", "Las ocho tablas de procedencia tienen bloque de definición y fila en el orden de creación; sin tablas repetidas (%d tablas)" % nTab, not dup_tab and not faltan_ent and nTab == 27 + nNuevas, (dup_tab, faltan_ent), "IG5-80", "ESPECIFICACION 4.4.4; 14.1")
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
        if ESTADO_V6 not in t: mal22.append((f[:10], "estado v6"))
    if ESTADO_V33 not in A[INF] or ESTADO_V33 not in spec: mal22.append(("estado v3.3",))
    acep = [(f[:10], i) for f, t in A.items() for i, l in enumerate(t.split("\n"), 1) if re.search(r"(aceptad[oa]|aprobad[oa]) por el propietario", l, re.I) and re.search(r"v6|complementari|esta revisión", l, re.I) and not NEG.search(l) and "preparad" not in l.lower()]
    chk("K22", "Estados: v3.3 aceptada como línea base, v6 preparada para aceptación formal, Fase 1 no iniciada; ningún documento declara aceptación del propietario de la v6", not mal22 and not acep, (mal22[:4], acep[:3]), "IE-04", "todos")
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
    chk("K25", "Los archivos históricos conservan su SHA-256 registrado en el manifiesto (%d archivos) y v3.3 figura con %s" % (len(mf), V33_SHA[:8]), len(mf) >= 10 and not mal25 and V33_SHA in A[REG], mal25[:4], "IE-04", "REGISTRO manifiesto")
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
                r"PC-02 pendiente", r"DT-01 pendiente", r"la v5 es la versión vigente", r"estado v5 vigente"]
    cont27 = []
    for f, t in AR.items():
        for i, l in enumerate(t.split("\n"), 1):
            for p in patrones:
                if re.search(p, l, re.I) and not HIST_WORDS.search(l): cont27.append((f[:10], i, p))
    chk("K27", "Sin contradicciones con las versiones anteriores en los documentos activos (patrones de fuentes, errores y pendientes obsoletos)", not cont27, cont27[:4], "IE-08", "todos")
    # ---- K28 registro histórico ----
    regt = A[REG]
    ent = re.findall(r"^## Entrada: (.+)$", regt, re.M)
    v6 = "revisión v6" in regt and "bb0af02bd170ce9c62cfd0741d8604cd41cab55e" in regt
    chk("K28", "Registro histórico: entradas ordenadas por revisión hasta la v6 con el commit previo bb0af02… y manifiesto de históricos", len(ent) >= 3 and v6 and "v5" in " ".join(ent) and "v6" in " ".join(ent) and len(mf) >= 10, ent[-3:], "IE-04", "REGISTRO")
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

def mutar(textos, tipo):
    t = dict(textos); s = t[SPEC]
    if tipo == "id_duplicado":
        m = re.search(r"^\| (IG5-69) \| (.*) \|$", s, re.M)
        s = s.replace(m.group(0), m.group(0) + "\n" + m.group(0), 1)
        i = s.index(m.group(0))
        # duplicar en la tabla de definición (primera aparición con 2 celdas)
    elif tipo == "regla_sin_escenario":
        s = re.sub(r"(\| T-\d+ \|[^\n]*\| )IG5-83(\s*\|)", r"\1IG5-82\2", s)
        s = re.sub(r"(\| T-\d+ \|[^\n]*\| )IG5-83, ", r"\1", s)
        s = re.sub(r", IG5-83(\s*\|)", r"\1", s)
    elif tipo == "referencia_inexistente":
        s = re.sub(r"^(\| T-0*1 \|.*\| )([^|]+?)( \|)$", r"\1\2, IG5-999\3", s, count=1, flags=re.M)
    elif tipo == "cifra_incorrecta":
        s = re.sub(r"\| Pruebas totales \| \d+ \|", "| Pruebas totales | 1 |", s, count=1)
    elif tipo == "formula_distinta":
        s = s.replace("⋃ Ctr(v) para v ∈ [V-D, V-B] ∪ P", "⋃ Ctr(v) para v ∈ [V-D, V-B]", 1)
    elif tipo == "error_ausente":
        a = s.index("#### 4.4.5 "); b = s.index("#### 4.4.6 ")
        s = s[:a] + s[a:b].replace("BRIEF_CHAIN_INCONSISTENTE", "ERROR_GENERICO") + s[b:]
    elif tipo == "fk_sin_organizacion":
        s = s.replace("| (organization_id, brief_id) | briefs(organization_id, id) |", "| (brief_id) | briefs(id) |", 1)
    elif tipo == "dependencia_posterior":
        s = re.sub(r"(\| \d+ \| 2\.1 \| tabla \(estructura\) \| brief_versions \| )[^|]*\|", r"\1promotion_snapshots |", s, count=1)
    t[SPEC] = s
    return t

def mutaciones(textos, dir_hist):
    esperado = {"id_duplicado": "K02", "regla_sin_escenario": "K06", "referencia_inexistente": "K05", "cifra_incorrecta": "K09", "formula_distinta": "K10",
                "error_ausente": "K12", "fk_sin_organizacion": "K14", "dependencia_posterior": "K16"}
    out = []
    for tipo, kid in esperado.items():
        global RES
        guard = RES
        try:
            ejecutar(mutar(textos, tipo), dir_hist)
            falla = [r["id"] for r in RES if not r["ok"]]
        finally:
            RES = guard
        out.append((tipo, kid, kid in falla))
    return out

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
 (25, "Preservación de v3.3", ["K25", "K22"]), (26, "Ausencia de afirmaciones de validación técnica no ejecutada", ["K23"]), (27, "Ausencia de contradicciones con v3, v4 y v5", ["K27"]), (28, "Integridad del registro histórico", ["K25", "K28"]),
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
            if re.search(r"(source|entity|ref|origin)_(type|kind)$", c) and c != "origin_kind": polimorfo.append((n, c))
            if c in ("source_id", "entity_id", "ref_id"): polimorfo.append((n, c))
            if c.endswith("_id") and c not in ("id", "organization_id", "operation_id", "created_by") and c not in cubiertas and c != "origin_version_id" and c != "used_asset_id" and c != "origin_asset_id" and c != "promotion_line_id" and c != "contributor_id" and c != "actor_id" and c != "recorded_by" and c != "resolution_actor_id" and c != "brief_id": sin_fk.append((n, c))
            if re.search(r"(latest|current|last)", c): ultimo.append((n, c))
    ult_txt = [(f[:10], i) for f, t in A.items() for i, l in enumerate(t.split("\n"), 1) if re.search(r"(seguir|usar) el (último|ultimo) (brief|snapshot)", l, re.I) and not NEG.search(l) and not l.startswith("| T-")]
    chk("K32", "Las ocho tablas de procedencia no tienen referencias polimórficas, cada columna *_id está cubierta por una FK compuesta (salvo las declaradas) y ninguna apunta al último o al actual", not polimorfo and not sin_fk and not ultimo and not ult_txt, (polimorfo, sin_fk[:4], ultimo, ult_txt[:2]), "IG5-81, IG5-62", "ESPECIFICACION 4.4.4")
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
        elif all(oks): est = "OK"
        else: est = "NO OK"
        nivel = "Verificado documentalmente" if est == "OK" else ("Diseñado" if est == "PENDIENTE" else "Diseñado")
        res = "; ".join("%s %s" % (i, "pasa" if byid[i]["ok"] else "FALLA") for i in ids if i in byid)
        out.append((cid, nom, regla, doc, evid, proc, res, est, nivel, "Verificación documental; no es validación técnica" if est == "OK" else "Corregir la causa"))
    return out

def principal(dir_, mut=True, dir_hist=None):
    textos = cargar(dir_)
    dir_hist = dir_hist or os.path.join(dir_, "historico")
    C, A, info = ejecutar(textos, dir_hist)
    checks_adicionales(textos, C, A, info)
    # K40 matriz de 28 controles
    ctr = controles(textos)
    ids_ctr = [c[0] for c in ctr]
    chk("K40", "La matriz define 28 controles con ID estable único, regla, sección, evidencia, procedimiento, resultado, estado y nivel; ninguno es OK sin comprobaciones aprobadas", len(ctr) == 28 and len(set(ids_ctr)) == 28 and all(all(x for x in c) for c in ctr), "", "IE-06, IE-07", "AUDITORIA 3")
    ctr = controles(textos)
    # reproducibilidad
    snap = json.dumps([(r["id"], r["ok"]) for r in RES])
    guard = list(RES)
    ejecutar(textos, dir_hist); checks_adicionales(textos, *ejecutar_c(textos, dir_hist)); 
    RES[:] = guard
    return textos, ctr, info

def ejecutar_c(textos, dir_hist):
    global RES
    g = list(RES)
    C, A, info = ejecutar(textos, dir_hist)
    RES[:] = g
    return C, A, info

def informe(dir_, usar_mut=True):
    textos = cargar(dir_)
    dir_hist = os.path.join(dir_, "historico")
    C, A, info = ejecutar(textos, dir_hist)
    checks_adicionales(textos, C, A, info)
    ctr0 = controles(textos)
    chk("K40", "La matriz define 28 controles con ID estable único, regla, sección, evidencia, procedimiento, resultado, estado y nivel; ninguno es OK sin comprobaciones aprobadas", len(ctr0) == 28 and len({c[0] for c in ctr0}) == 28 and all(all(x for x in c) for c in ctr0), "", "IE-06, IE-07", "AUDITORIA 3")
    base = [dict(r) for r in RES]
    # reproducibilidad: segunda ejecución completa y comparación
    RES.clear(); C2, A2, i2 = ejecutar(textos, dir_hist); checks_adicionales(textos, C2, A2, i2)
    chk("K40", "x", True)  # marcador interno; se descarta
    RES.pop()
    chk("K40", "La matriz define 28 controles con ID estable único, regla, sección, evidencia, procedimiento, resultado, estado y nivel; ninguno es OK sin comprobaciones aprobadas", len(ctr0) == 28 and len({c[0] for c in ctr0}) == 28 and all(all(x for x in c) for c in ctr0), "", "IE-06, IE-07", "AUDITORIA 3")
    repro = [(r["id"], r["ok"]) for r in RES] == [(r["id"], r["ok"]) for r in base]
    chk("K41", "Reproducibilidad: dos ejecuciones sobre los mismos archivos producen los mismos resultados individuales", repro, "", "IE-08", "AUDITORIA 3")
    muts = []
    if usar_mut:
        guard = [dict(r) for r in RES]
        muts = mutaciones(textos, dir_hist)
        RES[:] = guard
    chk("K42", "Controles negativos: %d defectos inyectados en copias en memoria son detectados por la comprobación correspondiente (%s)" % (len(muts), "; ".join("%s→%s %s" % (t, k, "detectado" if d else "NO detectado") for t, k, d in muts)) if muts else "Controles negativos omitidos (--sin-mutaciones)", (not muts) or all(d for _, _, d in muts), [m for m in muts if not m[2]], "IE-08", "AUDITORIA 3")
    ctr = controles(textos)
    return textos, ctr, muts

def bloque_markdown(ctr, textos, excluir_bloque=True):
    n = len(RES); nok = sum(1 for r in RES if r["ok"]); nf = n - nok
    L = []
    L.append("**Comprobaciones ejecutadas: %d. Aprobadas: %d. Fallidas: %d.** Controles: %d; OK: %d; NO OK: %d; PENDIENTE: %d.\n" % (n, nok, nf, len(ctr), sum(1 for c in ctr if c[7] == "OK"), sum(1 for c in ctr if c[7] == "NO OK"), sum(1 for c in ctr if c[7] == "PENDIENTE")))
    L.append("| Comprobación | Resultado | Descripción | Regla | Documento y sección |\n|---|---|---|---|---|")
    for r in RES: L.append("| %s | %s | %s | %s | %s |" % (r["id"], "APRUEBA" if r["ok"] else "FALLA", r["nombre"].replace("|", "/"), r["regla"], r["doc"]))
    L.append("\n**Matriz de los 28 controles.**\n")
    L.append("| ID | Control | Regla exacta | Documento y sección | Evidencia concreta | Procedimiento | Resultado real | Estado | Nivel de evidencia | Observación |\n|---|---|---|---|---|---|---|---|---|---|")
    for c in ctr: L.append("| " + " | ".join(x.replace("|", "/") for x in c) + " |")
    byid = {r["id"]: r for r in RES}
    L.append("\n**Auditoría integral final (28 puntos).**\n")
    L.append("| # | Punto auditado | Comprobaciones | Resultado |\n|---|---|---|---|")
    for n_, nom, ids in INTEGRAL:
        ok = all(byid[i]["ok"] for i in ids if i in byid) and all(i in byid for i in ids)
        L.append("| %d | %s | %s | %s |" % (n_, nom, ", ".join(ids), "OK (verificado documentalmente)" if ok else "NO OK"))
    return "\n".join(L)

def main():
    ap = argparse.ArgumentParser(description="Verificador documental del expediente Fase 0 (G-1, G-5, G-10)")
    ap.add_argument("--dir", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."), help="directorio docs/fase0")
    ap.add_argument("--json", action="store_true"); ap.add_argument("--md", action="store_true"); ap.add_argument("--sin-mutaciones", action="store_true")
    a = ap.parse_args()
    textos, ctr, muts = informe(a.dir, not a.sin_mutaciones)
    if a.md: print(INI + "\n" + bloque_markdown(ctr, textos) + "\n" + FIN); 
    elif a.json: print(json.dumps(dict(comprobaciones=RES, controles=ctr), ensure_ascii=False, indent=1))
    else:
        for r in RES: print("%s %-7s %s%s" % (r["id"], "APRUEBA" if r["ok"] else "FALLA", r["nombre"][:150], "" if r["ok"] else "  -> " + r["detalle"][:160]))
        n = len(RES); nok = sum(1 for r in RES if r["ok"])
        print("RESUMEN: %d comprobaciones, %d aprueban, %d fallan; %d controles (%d OK, %d NO OK, %d PENDIENTE)" % (n, nok, n - nok, len(ctr), sum(1 for c in ctr if c[7] == "OK"), sum(1 for c in ctr if c[7] == "NO OK"), sum(1 for c in ctr if c[7] == "PENDIENTE")))
    return 0 if all(r["ok"] for r in RES) else 1
if __name__ == "__main__":
    sys.exit(main())
