"""Modelo estructural en memoria de K45 (integridad semántica) y K47 (conservación de atribuciones y cálculo de E).

Alcance: pruebas de modelo en memoria sobre entidades relacionadas. No es PostgreSQL ni Supabase: no valida RLS, transacciones,
concurrencia, locks ni rollback. Todos los datos son ficticios.
"""
import copy, functools, difflib, hashlib, json

# =====================================================================================================
# K45: modelo relacional de fuentes, eventos y atribuciones
# =====================================================================================================
COLS = {"brief": "brief_version_id", "promotion": "promotion_snapshot_id", "copy": "copy_version_id", "asset": "creative_asset_id"}
TABLA_ORIGEN = {"brief": "brief_versions", "promotion": "promotion_snapshots", "copy": "copy_versions", "asset": "assets"}
CONTROLES_K45 = {
    "C01": "la organización del evento, de la fuente y de la atribución coincide",
    "C02": "la pieza declarada por el evento y por la atribución coincide y es la de la versión atribuida",
    "C03": "la versión exacta de la fuente existe y pertenece a esa pieza",
    "C04": "el tipo de contribución corresponde al tipo de fuente (matriz autorizada)",
    "C05": "origin_kind corresponde a la columna física de origen (una sola columna tipada)",
    "C06": "la columna de origen apunta a una fila de la tabla correcta",
    "C07": "el actor de la atribución coincide con el actor del evento",
    "C08": "el evento corresponde a la versión exacta de origen de la atribución",
    "C09": "el campo material existe en esa versión y fuente",
    "C10": "la atribución heredada conserva fuente, evento, persona, campo y versión original",
    "C11": "la relación de herencia apunta a una atribución anterior de la misma cadena",
    "C12": "el asset original fue cargado por el uploader registrado",
    "C13": "el asset reutilizado existe y corresponde a la versión exacta de copy que lo usa",
    "C14": "el reutilizador no se convierte en uploader",
    "C15": "ninguna referencia cruza organizaciones o piezas",
}

def _cadena(T, fuente, vid):
    """Versión y antecesores en su cadena física (parent/previous), sin ciclos."""
    tabla = T[TABLA_ORIGEN[fuente]]; out = []; cur = vid
    while cur is not None and cur in tabla and cur not in out:
        out.append(cur); cur = tabla[cur].get("prev")
    return out

def _piezas_de(T, fuente, vid):
    """Piezas que utilizan físicamente la versión: copy y asset la declaran; brief y promoción por copy_versions que las usan."""
    if fuente in ("copy", "asset"):
        fila = T[TABLA_ORIGEN[fuente]].get(vid)
        return {fila["piece"]} if fila else set()
    col = "brief_version" if fuente == "brief" else "promotion_snapshot"
    return {c["piece"] for c in T["copy_versions"].values() if c.get(col) and vid in _cadena(T, fuente, c[col])}

def _campos(T, fuente, vid):
    if fuente == "asset":
        a = T["assets"].get(vid); return {a["field"]} if a else set()
    fila = T[TABLA_ORIGEN[fuente]].get(vid); return set(fila["fields"]) if fila else set()

def evaluar_k45_estructural(T, M):
    """Valida las relaciones reales del modelo. Devuelve lista de (código C, id, detalle)."""
    permit = {m["tipo"]: m["origen"] for m in M}
    tabla_attr = {}
    for m in M: tabla_attr.setdefault(m["atrib"], set()).add(m["origen"])
    v = []
    # ---------- C15: referencias cruzadas entre organizaciones o piezas en toda la estructura ----------
    org = lambda tabla, i: T[tabla][i]["org"] if i in T[tabla] else None
    for c in T["copy_versions"].values():
        for col, tab in (("brief_version", "brief_versions"), ("promotion_snapshot", "promotion_snapshots"), ("prev", "copy_versions")):
            if c.get(col) and org(tab, c[col]) != c["org"]: v.append(("C15", c["id"], "copy_versions.%s cruza organización" % col))
        if c.get("prev") and c["prev"] in T["copy_versions"] and T["copy_versions"][c["prev"]]["piece"] != c["piece"]: v.append(("C15", c["id"], "copy_versions.prev cruza pieza"))
        if T["pieces"].get(c["piece"], {}).get("org") != c["org"]: v.append(("C15", c["id"], "pieza de otra organización"))
    for a in T["assets"].values():
        cv = T["copy_versions"].get(a["copy_version"])
        if cv is None or cv["org"] != a["org"] or cv["piece"] != a["piece"]: v.append(("C15", a["id"], "asset ligado a versión de otra organización o pieza"))
        if a.get("reused_from"):
            o = T["assets"].get(a["reused_from"])
            if o is None or o["org"] != a["org"] or o["piece"] != a["piece"]: v.append(("C15", a["id"], "reused_from cruza organización o pieza"))
    for tab in ("brief_versions", "promotion_snapshots"):
        for r in T[tab].values():
            if r.get("prev") and org(tab, r["prev"]) != r["org"]: v.append(("C15", r["id"], "%s.prev cruza organización" % tab))
    # ---------- eventos ----------
    for e in T["events"].values():
        k = e["origin_kind"]
        # C04: tipo de contribución ↔ origen autorizado por la matriz
        if e["tipo"] not in permit or permit[e["tipo"]] != k: v.append(("C04", e["id"], "tipo %s con origen %s" % (e["tipo"], k)))
        # C05: una única columna tipada y coherente con origin_kind
        llenas = [x for x, c in COLS.items() if e.get(c) is not None]
        if llenas != [k]: v.append(("C05", e["id"], "origin_kind %s con columnas %s" % (k, llenas)))
        oid = e.get(COLS.get(k, "")) if k in COLS else None
        if oid is None and len(llenas) == 1: oid = e.get(COLS[llenas[0]])
        # C06: la columna apunta a la tabla correcta
        if oid is not None and k in TABLA_ORIGEN and oid not in T[TABLA_ORIGEN[k]]:
            if any(oid in T[t] for t in TABLA_ORIGEN.values()): v.append(("C06", e["id"], "%s apunta a una fila de otra tabla" % COLS[k]))
            else: v.append(("C03", e["id"], "la versión de origen %s no existe" % oid))
        src = T[TABLA_ORIGEN[k]].get(oid) if k in TABLA_ORIGEN and oid is not None else None
        if src is not None:
            if src["org"] != e["org"]: v.append(("C01", e["id"], "evento y fuente en organizaciones distintas"))
            if e["piece"] not in _piezas_de(T, k, oid): v.append(("C03", e["id"], "la versión %s no pertenece a la pieza %s" % (oid, e["piece"])))
        if T["pieces"].get(e["piece"], {}).get("org") != e["org"]: v.append(("C01", e["id"], "pieza de otra organización"))
        if e["actor"] not in T["members"] or T["members"][e["actor"]]["org"] != e["org"]: v.append(("C01", e["id"], "actor sin membresía en la organización del evento"))
        # C12, C14: assets
        if k == "asset" and src is not None:
            if src.get("reused_from"): v.append(("C14", e["id"], "el evento uploader apunta a un asset reutilizado: el reutilizador sería uploader"))
            elif src["uploaded_by"] != e["actor"]: v.append(("C12", e["id"], "uploader registrado %s distinto del actor %s" % (src["uploaded_by"], e["actor"])))
    # ---------- atribuciones ----------
    for a in T["attributions"].values():
        f = a["fuente"]; e = T["events"].get(a["event"])
        if e is None: v.append(("C08", a["id"], "evento inexistente")); continue
        if a["org"] != e["org"]: v.append(("C01", a["id"], "atribución y evento en organizaciones distintas"))
        vsrc = T[TABLA_ORIGEN["copy" if f == "asset" else f]].get(a["version"])
        if vsrc is None: v.append(("C03", a["id"], "versión atribuida inexistente")); continue
        if vsrc["org"] != a["org"]: v.append(("C01", a["id"], "atribución y versión en organizaciones distintas"))
        if a["piece"] != e["piece"] or a["piece"] not in _piezas_de(T, "copy" if f == "asset" else f, a["version"]): v.append(("C02", a["id"], "pieza declarada %s distinta de la del evento o de la versión" % a["piece"]))
        if a["contributor"] != e["actor"]: v.append(("C07", a["id"], "actor de atribución distinto del actor del evento"))
        if e["origin_kind"] != f or a["tabla"] not in tabla_attr or f not in tabla_attr.get(a["tabla"], set()): v.append(("C04", a["id"], "atribución de %s con evento de origen %s" % (f, e["origin_kind"])))
        # C08: versión exacta del evento
        k = e["origin_kind"]; oid = e.get(COLS.get(k, ""))
        origen_ev = T["assets"][oid]["copy_version"] if k == "asset" and oid in T["assets"] else oid
        if a["origin_version"] != origen_ev: v.append(("C08", a["id"], "versión de origen de la atribución %s distinta de la del evento %s" % (a["origin_version"], origen_ev)))
        if a["relation"] == "directa" and a["version"] != a["origin_version"]: v.append(("C08", a["id"], "atribución directa en una versión distinta de la de origen"))
        # C09: campo material
        if a["field"] not in _campos(T, "copy" if f == "asset" else f, a["version"]) or e["field"] != a["field"]: v.append(("C09", a["id"], "campo %s no existe en la versión o no coincide con el evento" % a["field"]))
        if f == "asset":
            usado = T["assets"].get(a.get("used_asset") or "")
            if usado is None or usado["org"] != a["org"] or usado["copy_version"] != a["version"] or usado["piece"] != a["piece"]: v.append(("C13", a["id"], "el asset usado no existe o no corresponde a la versión exacta de copy"))
            else:
                cur, n = usado, 0
                while cur.get("reused_from") and n < 20: cur = T["assets"].get(cur["reused_from"], {"id": None}); n += 1
                if cur.get("id") != oid: v.append(("C13", a["id"], "la cadena de reutilización no llega al asset del evento"))
                if a["relation"] == "directa" and usado.get("reused_from"): v.append(("C14", a["id"], "atribución directa de uploader sobre un asset reutilizado"))
        # C10, C11: herencia
        if a["relation"] == "heredada":
            p = T["attributions"].get(a["prev"]) if a["prev"] else None
            if not a["origin_version"] or a["origin_version"] == a["version"] or a["prev"] is None: v.append(("C10", a["id"], "heredada sin versión de origen distinta o sin antecesor"))
            elif p is None: v.append(("C11", a["id"], "el antecesor %s no existe" % a["prev"]))
            else:
                if (p["fuente"], p["origin_version"], p["event"], p["contributor"], p["field"]) != (f, a["origin_version"], a["event"], a["contributor"], a["field"]): v.append(("C10", a["id"], "no conserva fuente, versión original, evento, persona y campo del antecesor"))
                if p["org"] != a["org"] or p["piece"] != a["piece"] or p["version"] not in _cadena(T, "copy" if f == "asset" else f, a["version"])[1:]: v.append(("C11", a["id"], "el antecesor no es una versión anterior de la misma cadena, pieza y organización"))
    return v

def fixture_k45():
    X, Y = "X", "Y"
    T = dict(pieces={"P1": dict(id="P1", org=X), "P2": dict(id="P2", org=X)},
             members={u: dict(org=X) for u in ("A", "B", "H", "U", "W", "Z")},
             briefs={"B1": dict(id="B1", org=X), "B2": dict(id="B2", org=X)},
             brief_versions={"bv1": dict(id="bv1", org=X, brief="B1", prev=None, fields={"commercial_offer"}), "bv2": dict(id="bv2", org=X, brief="B1", prev="bv1", fields={"commercial_offer"}),
                             "bv_b": dict(id="bv_b", org=X, brief="B2", prev=None, fields={"commercial_offer"}), "bv_y": dict(id="bv_y", org=Y, brief="B9", prev=None, fields={"commercial_offer"})},
             promotion_snapshots={"ps1": dict(id="ps1", org=X, prev=None, fields={"discount"}), "ps2": dict(id="ps2", org=X, prev="ps1", fields={"discount"}), "ps_o": dict(id="ps_o", org=X, prev=None, fields={"discount"})},
             copy_versions={"cv1": dict(id="cv1", org=X, piece="P1", prev=None, brief_version="bv1", promotion_snapshot="ps1", fields={"headline", "arte"}),
                            "cv2": dict(id="cv2", org=X, piece="P1", prev="cv1", brief_version="bv2", promotion_snapshot="ps1", fields={"headline", "arte"}),
                            "cv3": dict(id="cv3", org=X, piece="P1", prev="cv2", brief_version="bv2", promotion_snapshot="ps1", fields={"headline", "arte"}),
                            "cv_p2": dict(id="cv_p2", org=X, piece="P2", prev=None, brief_version="bv_b", promotion_snapshot="ps_o", fields={"headline", "arte"})},
             assets={"a1": dict(id="a1", org=X, piece="P1", copy_version="cv1", uploaded_by="U", reused_from=None, field="arte"),
                     "a2": dict(id="a2", org=X, piece="P1", copy_version="cv2", uploaded_by="U", reused_from="a1", reused_by="W", field="arte"),
                     "a3": dict(id="a3", org=X, piece="P1", copy_version="cv3", uploaded_by="U", reused_from="a2", reused_by="W", field="arte"),
                     "a_x": dict(id="a_x", org=X, piece="P1", copy_version="cv2", uploaded_by="Z", reused_from=None, field="arte")},
             events={}, attributions={})
    def ev(i, tipo, k, oid, actor, piece, field):
        T["events"][i] = dict(id=i, org=X, piece=piece, tipo=tipo, origin_kind=k, actor=actor, field=field, **{c: None for c in COLS.values()}); T["events"][i][COLS[k]] = oid
    def at(i, tabla, f, ver, field, e, c, rel="directa", ov=None, prev=None, piece="P1", used=None):
        T["attributions"][i] = dict(id=i, org=X, piece=piece, tabla=tabla, fuente=f, version=ver, origin_version=ov if ov is not None else ver, field=field, event=e, contributor=c, relation=rel, prev=prev, used_asset=used)
    ev("e_b", "brief_editor", "brief", "bv1", "A", "P1", "commercial_offer"); ev("e_p", "promotion_editor", "promotion", "ps1", "H", "P1", "discount")
    ev("e_c1", "copy_editor", "copy", "cv1", "B", "P1", "headline"); ev("e_c2", "copy_author", "copy", "cv2", "W", "P1", "headline"); ev("e_a", "asset_uploader", "asset", "a1", "U", "P1", "arte")
    at("t_b1", "brief_field_attributions", "brief", "bv1", "commercial_offer", "e_b", "A"); at("t_b2", "brief_field_attributions", "brief", "bv2", "commercial_offer", "e_b", "A", "heredada", "bv1", "t_b1")
    at("t_p1", "promotion_field_attributions", "promotion", "ps1", "discount", "e_p", "H")
    at("t_c1", "copy_version_provenance", "copy", "cv1", "headline", "e_c1", "B"); at("t_c2h", "copy_version_provenance", "copy", "cv2", "headline", "e_c1", "B", "heredada", "cv1", "t_c1"); at("t_c2", "copy_version_provenance", "copy", "cv2", "headline", "e_c2", "W")
    at("t_a1", "copy_version_provenance", "asset", "cv1", "arte", "e_a", "U", used="a1"); at("t_a2", "copy_version_provenance", "asset", "cv2", "arte", "e_a", "U", "heredada", "cv1", "t_a1", used="a2")
    # fila de otra pieza y de otra organización, usadas por las mutaciones
    T["events"]["e_bo"] = dict(id="e_bo", org=X, piece="P2", tipo="brief_editor", origin_kind="brief", actor="Z", field="commercial_offer", **{c: None for c in COLS.values()}); T["events"]["e_bo"]["brief_version_id"] = "bv_b"
    at("t_bo", "brief_field_attributions", "brief", "bv_b", "commercial_offer", "e_bo", "Z", piece="P2")
    return T

def variantes_positivas_k45():
    base = fixture_k45(); out = [("base", base)]
    v = fixture_k45()
    v["events"]["e_i"] = dict(id="e_i", org="X", piece="P1", tipo="inherited_contributor", origin_kind="copy", actor="B", field="headline", **{c: None for c in COLS.values()}); v["events"]["e_i"]["copy_version_id"] = "cv2"
    v["attributions"]["t_ci"] = dict(id="t_ci", org="X", piece="P1", tabla="copy_version_provenance", fuente="copy", version="cv2", origin_version="cv2", field="headline", event="e_i", contributor="B", relation="directa", prev=None, used_asset=None)
    out.append(("evento inherited_contributor sobre copy", v))
    w = fixture_k45()
    w["attributions"]["t_a3"] = dict(id="t_a3", org="X", piece="P1", tabla="copy_version_provenance", fuente="asset", version="cv3", origin_version="cv1", field="arte", event="e_a", contributor="U", relation="heredada", prev="t_a2", used_asset="a3")
    out.append(("segunda reutilización del mismo asset (a1 → a2 → a3)", w))
    return out

def _ev(T, i, **kw): T["events"][i].update(kw)
def _at(T, i, **kw): T["attributions"][i].update(kw)
def _m11(T):
    T["events"]["e_a2"] = dict(id="e_a2", org="X", piece="P1", tipo="asset_uploader", origin_kind="asset", actor="W", field="arte", **{c: None for c in COLS.values()}); T["events"]["e_a2"]["creative_asset_id"] = "a2"
    _at(T, "t_a2", event="e_a2", contributor="W")

K45_MUT = [
 ("K45-M01", "brief_editor con origen de promoción", "C04", lambda T: _ev(T, "e_b", origin_kind="promotion", brief_version_id=None, promotion_snapshot_id="ps1")),
 ("K45-M02", "promotion_editor con origen de brief", "C04", lambda T: _ev(T, "e_p", origin_kind="brief", promotion_snapshot_id=None, brief_version_id="bv1")),
 ("K45-M03", "copy_editor con origen de asset", "C04", lambda T: _ev(T, "e_c1", origin_kind="asset", copy_version_id=None, creative_asset_id="a1")),
 ("K45-M04", "asset_uploader con origen de copy", "C04", lambda T: _ev(T, "e_a", origin_kind="copy", creative_asset_id=None, copy_version_id="cv1")),
 ("K45-M05", "actor del evento distinto del actor de la atribución", "C07", lambda T: _ev(T, "e_c1", actor="Z")),
 ("K45-M06", "evento de otra organización", "C01", lambda T: _ev(T, "e_p", org="Y")),
 ("K45-M07", "evento de otra pieza", "C02", lambda T: _ev(T, "e_c1", piece="P2")),
 ("K45-M08", "versión de origen de la atribución distinta de la del evento", "C08", lambda T: _at(T, "t_p1", origin_version="ps2")),
 ("K45-M09", "campo material inexistente en la versión", "C09", lambda T: _at(T, "t_b1", field="campo_inexistente")),
 ("K45-M10", "atribución de brief que referencia un evento de promoción", "C04", lambda T: _at(T, "t_b1", event="e_p", contributor="H")),
 ("K45-M11", "reutilizador registrado como uploader original", "C14", _m11),
 ("K45-M12", "procedencia heredada sin versión de origen", "C10", lambda T: _at(T, "t_b2", origin_version=None)),
 ("K45-M13", "evento cuya versión de origen no existe", "C03", lambda T: _ev(T, "e_c1", copy_version_id="cv_fantasma")),
 ("K45-M14", "combinación inherited_contributor con origen de asset no permitida", "C04", lambda T: (T["events"].update(e_i=dict(id="e_i", org="X", piece="P1", tipo="inherited_contributor", origin_kind="asset", actor="U", field="arte", **{c: None for c in COLS.values()})), T["events"]["e_i"].update(creative_asset_id="a1"), _at(T, "t_a1", event="e_i"))),
 ("K45-M15", "evento y atribución declaran P2 pero la versión física de copy pertenece a P1", "C03", lambda T: (_ev(T, "e_c1", piece="P2"), _at(T, "t_c1", piece="P2"))),
 ("K45-M16", "evento de brief apunta a una versión de brief de otra pieza", "C03", lambda T: _ev(T, "e_b", brief_version_id="bv_b")),
 ("K45-M17", "atribución de promoción apunta a un snapshot de otra pieza", "C02", lambda T: _at(T, "t_p1", version="ps_o", origin_version="ps_o")),
 ("K45-M18", "atribución de asset declara una pieza distinta a la del copy que usa el arte", "C02", lambda T: _at(T, "t_a1", piece="P2")),
 ("K45-M19", "asset reutilizado vinculado a una versión de copy distinta de la que declara la atribución", "C13", lambda T: T["assets"]["a2"].update(copy_version="cv1")),
 ("K45-M20", "evento de asset uploader de otra organización aunque el asset reutilizado es válido", "C01", lambda T: _ev(T, "e_a", org="Y")),
 ("K45-M21", "atribución heredada con origen válido pero relación de herencia hacia otra cadena", "C11", lambda T: _at(T, "t_b2", prev="t_bo")),
 ("K45-M22", "cambia la versión física de origen del evento manteniendo ids aparentemente válidos", "C08", lambda T: _ev(T, "e_c1", copy_version_id="cv2")),
 ("K45-M23", "origin_kind brief con la columna tipada de copy", "C05", lambda T: _ev(T, "e_b", brief_version_id=None, copy_version_id="cv1")),
 ("K45-M24", "copy_version_id apunta al identificador de un asset", "C06", lambda T: _ev(T, "e_c1", copy_version_id="a1")),
 ("K45-M25", "el asset original lo cargó una persona distinta del actor del evento", "C12", lambda T: T["assets"]["a1"].update(uploaded_by="Z")),
 ("K45-M26", "versión de copy de P1 referencia una versión de brief de otra organización", "C15", lambda T: T["copy_versions"]["cv2"].update(brief_version="bv_y")),
 ("K45-M27", "la atribución de asset reutilizado usa un asset de la misma versión cuya cadena de reutilización no llega al asset del evento", "C13", lambda T: _at(T, "t_a2", used_asset="a_x")),
]

# =====================================================================================================
# K47: motor de atribuciones individuales, resoluciones y cálculo de E
# =====================================================================================================

# =====================================================================================================
# Registro append-only de resoluciones de descarte (v10): la inmutabilidad es estructural, no una convención
# =====================================================================================================
class ResolucionInmutable(Exception):
    """Intento de modificar, reemplazar o eliminar una resolución ya persistida."""

def _canon(d):
    return json.dumps({k: v for k, v in d.items() if k != "sello"}, sort_keys=True, ensure_ascii=False)
def sello_de(d):
    return hashlib.sha256(_canon(d).encode("utf-8")).hexdigest()

class _Fila(dict):
    """Fila de resolución: no admite escritura, eliminación ni actualización una vez construida."""
    def _no(s, *a, **k): raise ResolucionInmutable("la fila de la resolución ya persistida no se modifica")
    __setitem__ = __delitem__ = update = pop = popitem = clear = setdefault = __ior__ = _no
    def __reduce__(s): return (_Fila, (dict(s),))

def _congelar(x):
    if isinstance(x, dict): return _Fila({k: _congelar(v) for k, v in x.items()})
    if isinstance(x, (list, tuple)): return tuple(_congelar(v) for v in x)
    return x

class RegistroResoluciones(dict):
    """Solo se agrega con agregar(). No hay asignación, reemplazo por el mismo ID, actualización ni eliminación."""
    def _no(s, *a, **k): raise ResolucionInmutable("el registro de resoluciones es de solo agregar")
    __setitem__ = __delitem__ = update = pop = popitem = clear = setdefault = __ior__ = _no
    def __reduce__(s): return (_reg_de, (list(dict.items(s)),))
    def agregar(self, fila):
        if fila["id"] in self: raise ResolucionInmutable("el ID %s ya existe: una resolución no se reemplaza" % fila["id"])
        fila = dict(fila); fila["sello"] = sello_de(fila)
        dict.__setitem__(self, fila["id"], _congelar(fila)); return self[fila["id"]]

def _reg_de(items):
    r = RegistroResoluciones()
    for k, v in items: dict.__setitem__(r, k, v)
    return r

def _plano(o):
    """Copia plana (dict/list) de una estructura, apta para comparar instantáneas."""
    if isinstance(o, dict): return {k: _plano(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [_plano(v) for v in o]
    return copy.deepcopy(o)

CAMPOS_SOL = ("org", "atribucion", "afectado", "fuente", "pieza", "campo", "version_evidencia", "evento_motivador", "actor_cambio", "solicitante", "resolutor", "auth_uid", "evidencia", "motivo")

EVT_TIPO = {"brief": ("brief_editor", "brief_editor"), "promotion": ("promotion_editor", "promotion_editor"), "copy": ("copy_author", "copy_editor"), "asset": ("asset_uploader", "asset_uploader")}
TABLA_ATTR = {"brief": "brief_field_attributions", "promotion": "promotion_field_attributions", "copy": "copy_version_provenance", "asset": "copy_version_provenance"}
CLASIFICACIONES = ("sin_cambio", "introducido", "modificado", "sustituido", "eliminado")

class OperacionInvalida(Exception):
    """Una operación cuyo estado final no cumple las invariantes se revierte por completo y se rechaza (v14, H-08)."""
def _atomica(aid_de=None):
    """v14 (H-02 y H-08): toda operación que escribe en el modelo es transaccional. Captura el estado completo, ejecuta, verifica el estado final (invariantes básicas y cadena de procedencia del asset afectado) y, ante cualquier fallo, restaura el estado exacto anterior."""
    def deco(fn):
        @functools.wraps(fn)
        def w(self, *a, **k):
            if self.__dict__.get("_tx", 0): return fn(self, *a, **k)
            ant = copy.deepcopy(self.__dict__); self._tx = 1
            try:
                r = fn(self, *a, **k); self._verificar_final(fn.__name__, aid_de(a, k) if aid_de else None); self._tx = 0; return r
            except BaseException:
                self.__dict__.clear(); self.__dict__.update(ant); raise
        return w
    return deco

class ReutilizacionInvalida(OperacionInvalida):
    """H-01 de la v12: una reutilización sin origen, versión, evento de carga, uploader o atribución verificables no se registra y no deja registros parciales.
    v15 (H-03): `detalles` conserva, para el expediente de auditoría, un registro estructurado por inconsistencia (eslabón, evento, campo, valor esperado, valor observado y motivo); `mensaje_usuario` no expone identificadores ni valores internos."""
    def __init__(self, msg="", detalles=()): super().__init__(msg); self.detalles = [dict(d) for d in detalles]
    @property
    def mensaje_usuario(self): return "La reutilización no se puede registrar: la procedencia del asset de origen no es verificable (%d inconsistencia(s)). El detalle técnico queda en el expediente de auditoría." % max(1, len(self.detalles))

class _Err(list):
    """Lista de mensajes de error con su registro estructurado (v15)."""
    def __init__(self, *a): super().__init__(*a); self.det = []
def _det(err, L, evento, campo, esperado, hallado, motivo):
    """Agrega una inconsistencia: el mensaje conserva la frase de motivo y añade evento, campo, valor esperado y valor observado; el registro estructurado se guarda en `err.det`."""
    err.append("%s %s [evento %s; campo %s; esperado %r; hallado %r]" % (L, motivo, evento, campo, esperado, hallado))
    if hasattr(err, "det"): err.det.append(dict(eslabon=L[len("[eslabón "):-1] if L.startswith("[eslabón ") else L, evento=evento, campo=campo, esperado=esperado, hallado=hallado, motivo=motivo))

class Motor:
    """Estado: versiones inmutables, atribuciones individuales, eventos, resoluciones y bitácora de estados (solo se agrega)."""
    def __init__(self, org="X"):
        self.org = org; self.v = {}; self.assets = {}; self.ev = {}; self.at = {}; self.est = []; self.res = RegistroResoluciones(); self.solicitudes = {}; self.arte_decl = {}; self.clas_hist = []
        self._tx = 0; self.asignaciones = {}; self.confirmaciones = []; self.intentos_pub = []; self.publicadas = set(); self.members = {}; self.roles = {"revisor": {"piece.review"}, "editor": {"piece.edit"}, "admin": {"org.manage"}}; self.seq = 0; self.n = 0

    # ---- utilidades ----
    def nid(self, p): self.n += 1; return "%s%d" % (p, self.n)
    def tick(self): self.seq += 1; return self.seq
    def estado(self, aid):
        e = [x for x in self.est if x["atr"] == aid]; return e[-1]["estado"] if e else "activa"
    def activas(self, vid, fuente=None): return [a for a in self.at.values() if a["version"] == vid and self.estado(a["id"]) == "activa" and (fuente is None or a["fuente"] == fuente)]
    def miembro(self, u, rol): self.members[u] = dict(org=self.org, activo=True, rol=rol)

    def _evento(self, fuente, vid, actor, campo, material=True):
        tipo = EVT_TIPO[fuente][1 if self.v[vid].get("prev") else 0] if fuente == "copy" else EVT_TIPO[fuente][0]
        i = self.nid("e"); self.ev[i] = dict(id=i, org=self.org, fuente=fuente, version=vid, pieza=self.v[vid]["pieza"], tipo=tipo, actor=actor, auth=actor, campo=campo, seq=self.tick(), op=self.n)
        return i
    def _atribuir(self, fuente, vid, campo, evento, persona, rel="directa", prev=None, origen=None, used=None):
        i = self.nid("t"); ev = self.ev[evento]
        self.at[i] = dict(id=i, persona=persona, org=self.org, fuente=fuente, pieza=self.v[vid]["pieza"], origen_version=origen or vid, version=vid, campo=campo, evento=evento, rel=rel, previo=prev,
                          linaje=(self.at[prev]["linaje"] if prev else i), seq=self.tick())
        if used: self.at[i]["asset"] = used; self.at[i]["asset_version"] = self.assets.get(used, {}).get("version_asset")
        return i

    # ---- 1 y 6: crear versión y heredar atribuciones activas ----
    @_atomica()
    def crear_version(self, fuente, vid, pieza, parent=None, refs=None, autor=None, arte=None):
        assert vid not in self.v
        campos = copy.deepcopy(self.v[parent]["campos"]) if parent else {}
        for c in campos.values(): c["clasif"] = "sin_cambio"
        self.v[vid] = dict(id=vid, fuente=fuente, pieza=pieza, prev=parent, campos=campos, refs=copy.deepcopy(refs or {}), autor=autor, seq=self.tick())
        if fuente == "copy":   # estado del arte: declaración explícita o heredada de la versión anterior; nunca se infiere de la ausencia de registros
            if arte is not None: self.arte_decl[vid] = dict(estado=arte, actor=autor, heredada_de=None, seq=self.tick())
            elif parent in self.arte_decl: self.arte_decl[vid] = dict(estado=self.arte_decl[parent]["estado"], actor=self.arte_decl[parent]["actor"], heredada_de=parent, seq=self.tick())
        if parent: self.heredar_atribuciones(parent, vid)
        return vid
    @_atomica()
    def heredar_atribuciones(self, parent, vid):
        for a in sorted(self.activas(parent), key=lambda x: x["seq"]):
            n = self._atribuir(a["fuente"], vid, a["campo"], a["evento"], a["persona"], "heredada", a["id"], a["origen_version"], a.get("asset"))
            self.est.append(dict(seq=self.tick(), atr=n, estado="activa", resolucion=None, motivo="heredada de %s" % a["id"]))

    def _nueva(self, fuente, prev, nueva, pieza, refs=None, autor=None, arte=None):
        return self.crear_version(fuente, nueva, pieza, prev, refs, autor, arte)
    def _marcar_provisional(self, vid, campo):
        for a in self.activas(vid):
            if a["campo"] == campo and a["rel"] == "heredada": self.est.append(dict(seq=self.tick(), atr=a["id"], estado="activa", resolucion=None, motivo="conservada provisionalmente"))

    # ---- 2 a 5: operaciones sobre campos (siempre generan una versión nueva) ----
    @_atomica()
    def introducir_campo(self, fuente, prev, nueva, campo, contenido, actor, pieza=None, refs=None, arte=None):
        pieza = pieza or (self.v[prev]["pieza"] if prev else "P1"); self._nueva(fuente, prev, nueva, pieza, refs or (self.v[prev]["refs"] if prev else None), actor, arte)
        self.v[nueva]["campos"][campo] = dict(contenido=contenido, clasif="introducido", eliminado=False); self.clas_hist.append((nueva, campo, "introducido"))
        e = self._evento(fuente, nueva, actor, campo); self._atribuir(fuente, nueva, campo, e, actor); return nueva
    @_atomica()
    def modificar_campo(self, fuente, prev, nueva, campo, contenido, actor):
        self._nueva(fuente, prev, nueva, self.v[prev]["pieza"], self.v[prev]["refs"], actor)
        self.v[nueva]["campos"][campo].update(contenido=contenido, clasif="modificado"); self.clas_hist.append((nueva, campo, "modificado"))
        e = self._evento(fuente, nueva, actor, campo); self._atribuir(fuente, nueva, campo, e, actor); return nueva
    @_atomica()
    def sustituir_campo(self, fuente, prev, nueva, campo, contenido, actor):
        self._nueva(fuente, prev, nueva, self.v[prev]["pieza"], self.v[prev]["refs"], actor)
        self.v[nueva]["campos"][campo].update(contenido=contenido, clasif="sustituido"); self.clas_hist.append((nueva, campo, "sustituido"))
        self._marcar_provisional(nueva, campo)
        e = self._evento(fuente, nueva, actor, campo); self._atribuir(fuente, nueva, campo, e, actor); return nueva
    @_atomica()
    def eliminar_campo(self, fuente, prev, nueva, campo, actor, material=True):
        self._nueva(fuente, prev, nueva, self.v[prev]["pieza"], self.v[prev]["refs"], actor)
        self.v[nueva]["campos"][campo].update(contenido=None, clasif="eliminado", eliminado=True); self.clas_hist.append((nueva, campo, "eliminado"))
        self._marcar_provisional(nueva, campo)
        if material: e = self._evento(fuente, nueva, actor, campo); self._atribuir(fuente, nueva, campo, e, actor)
        return nueva
    @_atomica()
    def version_sin_cambio(self, fuente, prev, nueva, actor):
        self._nueva(fuente, prev, nueva, self.v[prev]["pieza"], self.v[prev]["refs"], actor)
        for c in self.v[nueva]["campos"]: self.clas_hist.append((nueva, c, "sin_cambio"))
        return nueva
    # ---- arte: asset nuevo, reutilizado, modificado, sustituido y eliminado (v10) ----
    def _ev_asset(self, tipo, vid, actor, aid):
        i = self.nid("e"); self.ev[i] = dict(id=i, org=self.org, fuente="asset", version=vid, pieza=self.v[vid]["pieza"], tipo=tipo, actor=actor, auth=actor, campo="arte", seq=self.tick(), op=self.n, asset=aid); return i
    def _cierre_asset(self, aid):
        """Assets alcanzables por origen (reutilización) o previo (modificación), sin recorrer dos veces el mismo."""
        out = []; cola = [aid]
        while cola:
            x = cola.pop()
            if x in out or x not in self.assets: continue
            out.append(x); y = self.assets[x]; cola += [y.get("origen"), y.get("previo")]
        return out
    def _raiz_asset(self, aid):
        x = aid; vistos = []
        while x in self.assets and x not in vistos:
            vistos.append(x); y = self.assets[x]; nxt = y.get("origen") if y["tipo"] == "reutilizado" else y.get("previo") if y["tipo"] == "modificado" else None
            if nxt is None: return y
            x = nxt
        raise KeyError("cadena de origen no verificable desde %s" % aid)
    def _campo_arte(self, vid, aid, clasif):
        cv = self.v[vid]["campos"]
        if "arte" in cv: cv["arte"].update(contenido=aid, clasif=clasif, eliminado=False)
        else: cv["arte"] = dict(contenido=aid, clasif=clasif, eliminado=False)
        self.clas_hist.append((vid, "arte", clasif))
    def _invariantes_basicos(self):
        """Invariantes de integridad del estado completo del modelo (referencias de atribuciones, eventos, bitácora de estados y resoluciones)."""
        e = []
        for k, a in self.at.items():
            if a["id"] != k: e.append("la atribución %s está intercambiada con la clave %s" % (a["id"], k))
            if a["version"] not in self.v: e.append("la atribución %s referencia una versión inexistente" % k)
            if a["evento"] not in self.ev: e.append("la atribución %s referencia un evento inexistente" % k)
            if a["rel"] == "heredada" and a.get("previo") not in self.at: e.append("la atribución heredada %s carece de antecesor" % k)
        for k, v_ in self.ev.items():
            if v_.get("id") != k or v_["version"] not in self.v: e.append("el evento %s está intercambiado o referencia una versión inexistente" % k)
        for x in self.est:
            if x["atr"] not in self.at: e.append("la bitácora de estados referencia una atribución inexistente (%s)" % x["atr"])
        for k, r in self.res.items():
            if r["atribucion"] not in self.at: e.append("la resolución %s referencia una atribución inexistente" % k)
        return e
    def _verificar_final(self, op, aid):
        """Verificación del estado final dentro de la transacción: invariantes básicas y, si la operación escribe un asset, reconstrucción completa de su cadena de procedencia."""
        err = self._invariantes_basicos()
        if aid is not None and aid in self.assets: err += ["estado final: " + z for z in self.reconstruir_cadena_procedencia(aid)["errores"]]
        if err: raise OperacionInvalida("; ".join(err))
    def _siguiente_eslabon(self, y, err, L):
        """Un solo tipo de relación por eslabón: reutilizado → origen; modificado → versión anterior; nuevo/sustituto → raíz. Devuelve (siguiente, es_raíz)."""
        tipo = y["tipo"]; o = y.get("origen"); pv = y.get("previo")
        if tipo == "reutilizado":
            if o is not None and pv is not None: err.append("%s la cadena es ambigua: el asset reutilizado declara a la vez origen y versión anterior" % L); return None, False
            if o is None: err.append("%s falta la referencia al asset de origen del asset reutilizado" % L); return None, False
            return o, False
        if tipo == "modificado":
            if o is not None and pv is not None: err.append("%s la cadena es ambigua: el asset modificado declara a la vez origen y versión anterior" % L); return None, False
            if pv is None: err.append("%s falta la versión anterior del asset modificado: la cadena pierde su raíz original" % L); return None, False
            return pv, False
        if tipo in ("nuevo", "sustituto"):
            if o is not None or pv is not None: err.append("%s la cadena es ambigua: un asset raíz no puede declarar origen ni versión anterior" % L); return None, False
            return None, True
        err.append("%s el tipo de asset %r no es válido para la cadena de procedencia" % (L, tipo)); return None, False
    def reconstruir_cadena_procedencia(self, aid):
        """H-01 (v14): reconstrucción completa de la cadena de procedencia del asset exacto `aid`. Recorre CADA eslabón hasta la raíz (origen, versión anterior, evento propio, referencias source_*, organización, pieza, versión de copy, actor,
        actor autenticado, uploader original, atribución directa original) y los contrasta contra los registros concretos de eventos y atribuciones: ningún campo guardado en un eslabón prueba su propia validez. Detecta referencias ausentes, ciclos,
        cadenas ambiguas, versiones inexistentes, registros duplicados, organización o pieza cruzadas, versión de copy equivocada, evento que no corresponde a la operación, uploader o reutilizador equivocado y atribuciones de otro asset, evento, uploader o versión.
        Nunca devuelve una cadena válida (ok=True) si algún eslabón está incompleto o es inconsistente."""
        err = _Err(); links = []; vis = []; x = aid
        if aid not in self.assets: return dict(ok=False, errores=["el asset de origen %s no existe" % aid], detalles=[dict(eslabon=aid, evento=None, campo="asset", esperado="asset existente", hallado=None, motivo="el asset de origen no existe")], eslabones=[], raiz=None, evento_carga=None, uploader=None, atribucion=None)
        while True:
            L = "[eslabón %s]" % x
            if x not in self.assets: err.append("%s la referencia a un asset de la cadena es inexistente o ausente (referencia ausente)" % ("[eslabón %s]" % (vis[-1] if vis else aid))); break
            if x in vis: err.append("[eslabón %s] la referencia a %s cierra un ciclo: la cadena de origen de %s no es verificable (ciclo)" % (vis[-1], x, aid)); break
            vis.append(x); y = self.assets[x]; links.append(x)
            if y.get("id") != x or y.get("version_id") != x: err.append("%s la versión exacta del eslabón no está identificada por su propia fila" % L)
            nxt, raiz = self._siguiente_eslabon(y, err, L)
            if raiz or nxt is None: break
            x = nxt
        if err: return dict(ok=False, errores=list(err), detalles=list(err.det), eslabones=links, raiz=None, evento_carga=None, uploader=None, atribucion=None)
        r = self.assets[links[-1]]; rid = r["id"]; ue = r.get("evento_carga"); up = r.get("uploader"); at0 = self._verificar_raiz(r, err)
        for i, x in enumerate(links):
            y = self.assets[x]; L = "[eslabón %s]" % x
            if y["org"] != self.org: err.append("%s el asset pertenece a otra organización" % L) if x != rid else None
            if y["tipo"] != "nuevo" and y["tipo"] != "sustituto":
                if y.get("uploader_original") != up: err.append("%s la cadena de reutilización de %s no conserva el uploader original del asset raíz %s" % (L, aid, rid))
                if y.get("evento_carga_original") != ue: err.append("%s la cadena de reutilización de %s no conserva el evento original de carga del asset raíz %s" % (L, aid, rid))
            if x == rid: continue
            if y["tipo"] == "reutilizado": self._verificar_reutilizado(y, self.assets[y["origen"]], r, ue, up, at0, err)
            else: self._verificar_modificado(y, self.assets[y["previo"]], err)
        return dict(ok=not err, errores=list(err), detalles=list(err.det), eslabones=links, raiz=rid, evento_carga=ue, uploader=up, atribucion=at0)
    def _campos_permitidos(self):
        """Campos que un evento puede declarar: los de las versiones de copy, brief y promoción del modelo y el campo de arte."""
        return {"arte"} | {c for v in self.v.values() for c in v["campos"]}
    def _chk_actor(self, e, y, L, actor, err):
        """Actor del evento propio: coincide con el actor del eslabón, está autenticado como tal y es miembro activo de la organización."""
        ok = True; i = e.get("id")
        if actor is None or e.get("actor") != actor: _det(err, L, i, "actor", actor, e.get("actor"), "el actor del evento propio no coincide con el actor del eslabón"); ok = False
        if actor is None or e.get("auth") != actor: _det(err, L, i, "auth", actor, e.get("auth"), "el actor autenticado del evento propio no coincide con el actor del eslabón"); ok = False
        mm = self.members.get(actor)
        if mm is None or mm.get("org") != self.org or not mm.get("activo"): _det(err, L, i, "miembro", "miembro activo de %s" % self.org, None if mm is None else (mm.get("org"), mm.get("activo")), "el actor %s no es miembro activo de la organización" % actor); ok = False
        return ok
    def _chk_asset_version(self, e, y, L, err):
        """v15 (H-01): `asset_version` del evento propio es la versión exacta del asset de DESTINO que produjo el evento (no la del origen), y el par (asset, versión) del evento identifica la fila de ese asset."""
        ok = True; v = e.get("asset_version"); i = e.get("id")
        if isinstance(v, bool) or not isinstance(v, int) or v != y.get("version_asset"): _det(err, L, i, "asset_version", y.get("version_asset"), v, "el evento propio corresponde a otra versión del asset (asset_version)"); ok = False
        fila = self.assets.get(e.get("asset_version_id"))
        if fila is None or fila.get("version_asset") != v or fila.get("asset_id") != e.get("asset_id"): _det(err, L, i, "asset_version_id", (y.get("id"), y.get("asset_id"), y.get("version_asset")), (e.get("asset_version_id"), e.get("asset_id"), None if fila is None else fila.get("version_asset")), "el par asset-versión del evento propio no identifica la fila exacta del asset de destino (versión del asset)"); ok = False
        return ok
    def _chk_campo(self, e, y, L, err):
        """v15 (H-02): el evento propio de un asset está vinculado al campo «arte»: presente, permitido, igual a «arte» y coherente con el campo de arte de la versión de copy donde se usa el asset."""
        ok = True; i = e.get("id"); c = e.get("campo")
        if "campo" not in e or c is None: _det(err, L, i, "campo", "arte", c, "el evento propio no declara el campo (campo ausente)"); return False
        if c not in self._campos_permitidos(): _det(err, L, i, "campo", "arte", c, "el campo del evento propio no es un campo permitido (campo no permitido)"); ok = False
        elif c != "arte": _det(err, L, i, "campo", "arte", c, "el evento propio no está vinculado al campo arte (otro campo)"); ok = False
        arte = self.v.get(y.get("copy_version"), {}).get("campos", {}).get("arte")
        if arte is None or arte.get("contenido") != y.get("id"): _det(err, L, i, "copy_version.arte", y.get("id"), None if arte is None else arte.get("contenido"), "la versión de copy no usa este asset en el campo arte (versión de copy)"); ok = False
        return ok
    def _datos_evento(self, e, y, L, esperado_tipos, actor, err, cual):
        """Validaciones comunes del evento propio de un eslabón (reutilización o carga de una versión modificada): existencia, identidad, tipo, asset de destino, versión de destino (asset_version), campo, organización, pieza, versión de copy y actor."""
        if e is None: err.append("%s el evento propio (%s) no existe (referencia ausente)" % (L, cual)); (err.det.append(dict(eslabon=y["id"], evento=None, campo="evento", esperado="evento existente", hallado=None, motivo="el evento propio no existe")) if hasattr(err, "det") else None); return False
        ok = True; i = e.get("id"); ref = y.get("evento_reutilizacion") if cual == "reutilización" else y.get("evento_carga")
        if i != ref: _det(err, L, i, "id", ref, i, "el evento propio de %s está intercambiado: su registro no corresponde al identificador referenciado" % cual); ok = False
        if e.get("tipo") not in esperado_tipos: _det(err, L, i, "tipo", esperado_tipos, e.get("tipo"), "el evento propio no corresponde a la operación de %s" % cual); ok = False
        if e.get("asset") != y["id"] or e.get("asset_version_id") != y["id"] or e.get("asset_id") != y.get("asset_id"): _det(err, L, i, "asset", (y["id"], y.get("asset_id")), (e.get("asset"), e.get("asset_id")), "el evento propio corresponde a otro asset (%s) y no a este eslabón" % e.get("asset")); ok = False
        if not self._chk_asset_version(e, y, L, err): ok = False
        if not self._chk_campo(e, y, L, err): ok = False
        if e.get("org") != y.get("org") or e.get("org") != self.org: _det(err, L, i, "org", y.get("org"), e.get("org"), "el evento propio pertenece a otra organización"); ok = False
        if e.get("pieza") != y.get("pieza"): _det(err, L, i, "pieza", y.get("pieza"), e.get("pieza"), "el evento propio pertenece a otra pieza"); ok = False
        if e.get("version") != y.get("copy_version"): _det(err, L, i, "version", y.get("copy_version"), e.get("version"), "el evento propio corresponde a otra versión de copy"); ok = False
        if not self._chk_actor(e, y, L, actor, err): ok = False
        return ok
    def _verificar_reutilizado(self, y, o, r, ue, up, at0, err):
        x = y["id"]; L = "[eslabón %s]" % x; er = self.ev.get(y.get("evento_reutilizacion"))
        if y.get("origen") != o["id"]: err.append("%s el origen inmediato declarado no existe como versión exacta" % L)
        if o["org"] != y["org"]: err.append("%s el origen inmediato %s pertenece a otra organización" % (L, o["id"]))
        cv = self.v.get(y.get("copy_version"))
        if cv is None: err.append("%s la versión de copy %s no existe" % (L, y.get("copy_version")))
        elif cv["pieza"] != y.get("pieza"): err.append("%s la pieza del asset no coincide con la pieza de su versión de copy" % L)
        if not isinstance(o.get("version_asset"), int) or y.get("origen_version_asset") != o.get("version_asset"): err.append("%s la versión del asset de origen declarada (%s) no es la versión exacta del origen inmediato (%s)" % (L, y.get("origen_version_asset"), o.get("version_asset")))
        if y.get("asset_id") != x or y.get("version_asset") != 1: _det(err, L, er.get("id") if er else None, "version_asset", 1, y.get("version_asset"), "la fila del asset reutilizado no es la versión 1 de su propio linaje (versión del asset)")
        self._datos_evento(er, y, L, ("copy_author", "copy_editor"), y.get("reutilizador"), err, "reutilización")
        if er is not None:
            comp = [a for a in self.assets.values() if a.get("evento_reutilizacion") == er.get("id")]
            if len(comp) != 1: err.append("%s el evento propio de reutilización está compartido por varios assets (duplicada)" % L)
            exp = (("source_asset_id", o["asset_id"], "el asset de origen"), ("source_asset_version_id", o["id"], "la versión referenciada no es el origen inmediato exacto (versión)"), ("source_asset_version", o["version_asset"], "la versión del asset de origen (versión)"),
                   ("source_upload_event_id", ue, "el evento de carga original (evento de carga)"), ("source_uploader_id", up, "el uploader original (uploader)"), ("source_attribution_id", at0, "la atribución directa original (atribución)"),
                   ("source_root_asset_id", r["asset_id"], "el asset raíz"), ("source_root_asset_version_id", r["id"], "la versión exacta de la raíz"))
            for k, v, nom in exp:
                if er.get(k) != v: err.append("%s el campo %s del evento propio no corresponde a: %s (origen inmediato o raíz) (esperado %s, hallado %s)" % (L, k, nom, v, er.get(k)))
        for k, v in (("source_asset_id", o["asset_id"]), ("source_asset_version_id", o["id"]), ("source_upload_event_id", ue), ("source_attribution_id", at0), ("source_root_asset_id", r["asset_id"]), ("source_root_asset_version_id", r["id"])):
            if y.get(k) != v: err.append("%s el campo %s guardado en el asset no coincide con la reconstrucción independiente (esperado %s, hallado %s)" % (L, k, v, y.get(k)))
        if er is not None: self._chk_atribucion_reutilizador(y, er, err)
    def _chk_atribucion_reutilizador(self, y, er, err):
        """Atribución directa del reutilizador en el evento propio de reutilización: única, del asset, organización, pieza, versión de copy y campo «arte» exactos."""
        x = y["id"]; L = "[eslabón %s]" % x
        dirs = [b for b in self.at.values() if b["rel"] == "directa" and b["fuente"] == "copy" and b["evento"] == er.get("id")]
        if y.get("material"):
            ex = [b for b in dirs if b["persona"] == y.get("reutilizador") and b.get("asset") == x and (b["org"], b["pieza"], b["version"], b["campo"]) == (y["org"], y["pieza"], y["copy_version"], "arte")]
            if len(ex) > 1: err.append("%s la atribución directa del reutilizador está duplicada (duplicada)" % L)
            elif len(ex) == 0: err.append("%s falta la atribución directa del reutilizador en el evento propio de reutilización" % L)
            if len(dirs) != len(ex): err.append("%s existe una atribución directa del evento propio que no corresponde al reutilizador, asset o versión de copy exactos" % L)
        elif dirs: err.append("%s la reutilización no material tiene atribución directa del reutilizador" % L)
    def _verificar_modificado(self, y, p, err):
        x = y["id"]; L = "[eslabón %s]" % x; e = self.ev.get(y.get("evento_carga"))
        if y.get("previo") != p["id"] or y.get("asset_id") != p.get("asset_id") or y.get("version_asset") != p.get("version_asset", 0) + 1: err.append("%s la versión anterior no es la versión exacta inmediatamente anterior del mismo asset (versión anterior)" % L)
        if p["org"] != y["org"]: err.append("%s la versión anterior pertenece a otra organización" % L)
        if p["pieza"] != y["pieza"]: err.append("%s la versión anterior pertenece a otra pieza" % L)
        cv = self.v.get(y.get("copy_version"))
        if cv is None: err.append("%s la versión de copy %s no existe" % (L, y.get("copy_version")))
        elif cv["pieza"] != y.get("pieza"): err.append("%s la pieza del asset no coincide con la pieza de su versión de copy" % L)
        self._datos_evento(e, y, L, ("asset_uploader",), y.get("uploader"), err, "carga de la versión")
        if e is not None:
            dirs = [b for b in self.at.values() if b["rel"] == "directa" and b["fuente"] == "asset" and b["evento"] == e.get("id")]
            ex = [b for b in dirs if b["persona"] == y.get("uploader") and b.get("asset") == x and (b["org"], b["pieza"], b["version"], b["campo"]) == (y["org"], y["pieza"], y["copy_version"], "arte")]
            if len(ex) > 1: err.append("%s la atribución directa del editor de la versión está duplicada (duplicada)" % L)
            elif len(ex) == 0: err.append("%s falta la atribución directa del editor de la versión" % L)
    def _verificar_raiz(self, r, err):
        """Raíz de la cadena: registro exacto, evento original de carga, uploader original y atribución directa original (únicos y coherentes). Devuelve el id de la atribución directa o None."""
        rid = r["id"]; ue = r.get("evento_carga"); e = self.ev.get(ue); up = r.get("uploader")
        if r.get("org") != self.org: err.append("el asset raíz %s pertenece a otra organización" % rid)
        if e is None: err.append("el asset raíz %s no tiene evento original de carga" % rid); return None
        if e.get("id") != ue: err.append("el evento original de carga de %s está intercambiado: su registro no corresponde al identificador referenciado" % rid)
        if e.get("tipo") != "asset_uploader": err.append("el evento original de carga de %s no es un evento de carga de asset (%s)" % (rid, e.get("tipo")))
        if e.get("asset_id") != r.get("asset_id"): err.append("el evento original de carga corresponde a otro asset (%s) y no al asset raíz %s" % (e.get("asset"), rid))
        elif e.get("asset") != rid or e.get("asset_version_id") != rid or e.get("asset_version") != r.get("version_asset"): err.append("el evento original de carga corresponde a otra versión del mismo asset (%s) y no a la versión exacta de la raíz %s" % (e.get("asset"), rid))
        if e.get("campo") != "arte": err.append("el evento original de carga de %s no está vinculado al campo arte (campo %r)" % (rid, e.get("campo")))
        if e.get("org") != self.org or e.get("org") != r.get("org"): err.append("el evento original de carga de %s pertenece a otra organización" % rid)
        if e.get("pieza") != r.get("pieza"): err.append("el evento original de carga de %s pertenece a otra pieza" % rid)
        if e.get("version") != r.get("copy_version"): err.append("el evento original de carga de %s corresponde a otra versión de copy" % rid)
        if up is None or e.get("actor") != up or e.get("auth") != up: err.append("el actor del evento original de carga de %s no coincide con el uploader del asset raíz" % rid)
        mm = self.members.get(up)
        if mm is None or mm.get("org") != self.org: err.append("el uploader original de %s no es miembro de la organización" % rid)
        elif not mm.get("activo"): err.append("el uploader original de %s no tiene membresía activa" % rid)
        dirs = [b for b in self.at.values() if b["rel"] == "directa" and b["fuente"] == "asset" and (b.get("asset") == rid or b["evento"] == ue)]
        exactas = [b for b in dirs if b.get("asset") == rid and b["evento"] == ue and b["persona"] == up and (b["org"], b["pieza"], b["version"], b["origen_version"], b.get("asset_version"), b["campo"]) == (r["org"], r["pieza"], r["copy_version"], r["copy_version"], r["version_asset"], "arte")]
        if len(exactas) == 1: return exactas[0]["id"]
        if len(exactas) > 1: err.append("la atribución directa original de %s es ambigua" % rid)
        elif not dirs: err.append("no existe la atribución directa del uploader original del asset raíz %s" % rid)
        else:
            for b in dirs:
                if b["evento"] == ue and b.get("asset") != rid: err.append("la atribución directa %s pertenece a otro asset (%s) y no al asset raíz %s" % (b["id"], b.get("asset"), rid))
                elif b.get("asset") == rid and b["evento"] != ue: err.append("la atribución directa %s pertenece a otro evento de carga (%s) y no al evento original de %s" % (b["id"], b["evento"], rid))
                elif b.get("asset") == rid and b["persona"] != up: err.append("la atribución directa %s pertenece a otro uploader (%s) y no al uploader original %s" % (b["id"], b["persona"], up))
                else: err.append("la atribución directa %s no corresponde a la organización, pieza, versión de copy y versión de asset exactas del asset raíz %s" % (b["id"], rid))
        return None
    def _origen_carga(self, aid, err=None):
        """H-02 (v14): usa la reconstrucción completa de la cadena (todos los eslabones). No toma como verdad primaria el evento ni el uploader guardados en un asset reutilizado: solo los contrasta. Los problemas se acumulan en `err` o, si no se entrega, se lanza ReutilizacionInvalida.
        Devuelve (evento de carga original, uploader original, atribución directa original)."""
        propia = err is None; err = _Err() if err is None else err; c = self.reconstruir_cadena_procedencia(aid); err.extend(c["errores"])
        if hasattr(err, "det"): err.det.extend(c["detalles"])
        if propia and c["errores"]: raise ReutilizacionInvalida("; ".join(c["errores"]), c["detalles"])
        return c["evento_carga"], c["uploader"], c["atribucion"]
    def _validar_reutilizacion(self, aid, copy_version, uploader, reused_from):
        """H-01 (v12 y v13): valida todo antes de escribir. Orden: (1) identidad completa del origen y de su asset raíz, (2) evento original de carga, (3) atribución directa original, (4) membresía y actor del reutilizador,
        (5) pieza y versión exacta de copy de destino, (6) cadena de reutilización sin ciclos ni referencias ausentes; solo después se construyen los registros nuevos."""
        err = _Err(); o = self.assets.get(reused_from)
        if o is None: raise ReutilizacionInvalida("el asset de origen %s no existe" % reused_from, [dict(eslabon=reused_from, evento=None, campo="asset", esperado="asset existente", hallado=None, motivo="el asset de origen no existe")])
        if o.get("id") != reused_from or o.get("version_id") != reused_from or not isinstance(o.get("version_asset"), int): err.append("la versión exacta del asset de origen no está identificada")
        if o["org"] != self.org: err.append("el asset de origen pertenece a otra organización")
        self._origen_carga(reused_from, err)
        oc = self.v.get(o.get("copy_version")); propio = self.ev.get(o.get("evento_carga") if o["tipo"] != "reutilizado" else o.get("evento_reutilizacion"))
        if oc is None or oc["pieza"] != o["pieza"] or propio is None or propio.get("pieza") != o["pieza"] or propio.get("version") != o.get("copy_version"): err.append("la pieza y la versión de copy del asset de origen no coinciden con su evento propio")
        mm = self.members.get(uploader)
        if mm is None or mm["org"] != self.org or not mm.get("activo"): err.append("el reutilizador %s no es miembro activo de la organización" % uploader)
        if copy_version not in self.v: err.append("la versión de copy de destino %s no existe" % copy_version)
        if aid in self.assets: err.append("el asset %s ya existe" % aid)
        if aid in self._cierre_asset(reused_from): err.append("la reutilización crearía un ciclo en la cadena de origen")
        if err: raise ReutilizacionInvalida("; ".join(err), err.det)
        return self._origen_carga(reused_from)
    @_atomica(lambda a, k: a[0] if a else k['aid'])
    def registrar_asset(self, aid, copy_version, uploader, reused_from=None, material=True):
        """Asset nuevo (reused_from=None): uploader original y evento de carga. Asset reutilizado: valida antes de escribir todo el origen exacto (v12) y registra por separado al reutilizador y su evento, con referencias explícitas al origen."""
        if copy_version not in self.v: raise ReutilizacionInvalida("la versión de copy de destino %s no existe" % copy_version)
        mm_ = self.members.get(uploader)
        if mm_ is None or mm_["org"] != self.org or not mm_.get("activo"): raise ReutilizacionInvalida("el actor %s no es miembro activo de la organización" % uploader)
        if aid in self.assets: raise ReutilizacionInvalida("el asset %s ya existe" % aid)
        pieza = self.v[copy_version]["pieza"]
        if reused_from is None:
            e = self._evento("asset", copy_version, uploader, "arte"); self.ev[e].update(asset=aid, asset_id=aid, asset_version_id=aid, asset_version=1)
            self.assets[aid] = dict(id=aid, asset_id=aid, version_id=aid, org=self.org, pieza=pieza, version_asset=1, tipo="nuevo", origen=None, previo=None, uploader=uploader, evento_carga=e, uploader_original=uploader, evento_carga_original=e,
                                    reutilizador=None, evento_reutilizacion=None, material=None, copy_version=copy_version)
            self._campo_arte(copy_version, aid, "introducido"); self._atribuir("asset", copy_version, "arte", e, uploader, used=aid)
            return aid
        ue, up, at0 = self._validar_reutilizacion(aid, copy_version, uploader, reused_from); o = self.assets[reused_from]
        raiz = self._raiz_asset(reused_from); er = self._evento("copy", copy_version, uploader, "arte")
        self.ev[er].update(asset=aid, asset_id=aid, asset_version_id=aid, asset_version=1, source_asset_id=o["asset_id"], source_asset_version_id=reused_from, source_asset_version=o["version_asset"],
                           source_upload_event_id=ue, source_uploader_id=up, source_attribution_id=at0,
                           source_root_asset_id=raiz["asset_id"], source_root_asset_version_id=raiz["id"])
        self.assets[aid] = dict(id=aid, asset_id=aid, version_id=aid, org=self.org, pieza=pieza, version_asset=1, tipo="reutilizado", origen=reused_from, origen_version_asset=o["version_asset"], previo=None, uploader=None, evento_carga=None, uploader_original=raiz["uploader_original"],
                                evento_carga_original=raiz["evento_carga_original"], reutilizador=uploader, evento_reutilizacion=er, material=bool(material), copy_version=copy_version, procedencia="reutilizacion",
                                source_asset_id=o["asset_id"], source_asset_version_id=reused_from, source_upload_event_id=ue, source_attribution_id=at0,
                                source_root_asset_id=raiz["asset_id"], source_root_asset_version_id=raiz["id"])
        cierre = set(self._cierre_asset(reused_from)); ov = o["copy_version"]
        for b in sorted(self.activas(ov), key=lambda x: x["seq"]):
            if b["campo"] == "arte" and b.get("asset") in cierre:
                n = self._atribuir(b["fuente"], copy_version, "arte", b["evento"], b["persona"], "heredada", b["id"], b["origen_version"], aid)
                self.est.append(dict(seq=self.tick(), atr=n, estado="activa", resolucion=None, motivo="reutilización de %s" % reused_from))
        self._campo_arte(copy_version, aid, "introducido")
        if material: self._atribuir("copy", copy_version, "arte", er, uploader, used=aid)
        return aid
    def cadena_identidad(self, aid):
        """Eslabones de identidad del asset (motor): (asset, tipo, versión, evento de carga o de origen, uploader o reutilizador, evento de reutilización)."""
        out = []; vis = []; x = aid
        while x in self.assets and x not in vis:
            vis.append(x); y = self.assets[x]; t = y["tipo"]
            out.append((x, t, y["version_asset"], y.get("evento_carga") or y.get("source_upload_event_id"), y.get("uploader") or y.get("reutilizador"), y.get("evento_reutilizacion")))
            x = y.get("origen") if t == "reutilizado" else y.get("previo") if t == "modificado" else None
        return out
    @_atomica(lambda a, k: a[2])
    def modificar_asset(self, prev, nueva, aid, aid_prev, editor):
        """Nueva versión del asset (fila nueva, previo = versión anterior). Quien la sube es el asset_uploader de esa fila; el uploader original y las atribuciones anteriores se conservan."""
        self._nueva("copy", prev, nueva, self.v[prev]["pieza"], self.v[prev]["refs"], editor); raiz = self._raiz_asset(aid_prev); e = self._evento("asset", nueva, editor, "arte"); self.ev[e].update(asset=aid, asset_id=self.assets[aid_prev]["asset_id"], asset_version_id=aid, asset_version=self.assets[aid_prev]["version_asset"] + 1)
        self.assets[aid] = dict(id=aid, asset_id=self.assets[aid_prev]["asset_id"], version_id=aid, org=self.org, pieza=self.v[nueva]["pieza"], version_asset=self.assets[aid_prev]["version_asset"] + 1, tipo="modificado", origen=None, previo=aid_prev, uploader=editor, evento_carga=e,
                                uploader_original=raiz["uploader_original"], evento_carga_original=raiz["evento_carga_original"], reutilizador=None, evento_reutilizacion=None, material=None, copy_version=nueva)
        self._campo_arte(nueva, aid, "modificado"); self._marcar_provisional(nueva, "arte"); self._atribuir("asset", nueva, "arte", e, editor, used=aid); return nueva
    @_atomica(lambda a, k: a[2])
    def sustituir_asset(self, prev, nueva, aid, aid_prev, uploader):
        self._nueva("copy", prev, nueva, self.v[prev]["pieza"], self.v[prev]["refs"], uploader); e = self._evento("asset", nueva, uploader, "arte"); self.ev[e].update(asset=aid, asset_id=aid, asset_version_id=aid, asset_version=1)
        self.assets[aid] = dict(id=aid, asset_id=aid, version_id=aid, org=self.org, pieza=self.v[nueva]["pieza"], version_asset=1, tipo="sustituto", origen=None, previo=None, sustituye=aid_prev, uploader=uploader, evento_carga=e, uploader_original=uploader,
                                evento_carga_original=e, reutilizador=None, evento_reutilizacion=None, material=None, copy_version=nueva)
        self._campo_arte(nueva, aid, "sustituido"); self._marcar_provisional(nueva, "arte"); self._atribuir("asset", nueva, "arte", e, uploader, used=aid); return nueva
    @_atomica()
    def eliminar_asset(self, prev, nueva, actor):
        return self.eliminar_campo("copy", prev, nueva, "arte", actor, True)

    # ---- 10: cambiar clasificación ----
    @_atomica()
    def cambiar_clasificacion(self, vid, campo, nueva, actor):
        assert nueva in CLASIFICACIONES
        self.clas_hist.append((vid, campo, nueva, "cambio por %s" % actor))
    def clasif_actual(self, vid, campo):
        h = [x for x in self.clas_hist if x[0] == vid and x[1] == campo]; return h[-1][2] if h else self.v[vid]["campos"][campo]["clasif"]

    # ---- 7, 8, 9: resoluciones de descarte (registros nuevos, con resultado definitivo y sello; nunca se modifican) ----
    @_atomica()
    def solicitar_resolucion(self, rid, **kw):
        """Formulario de solicitud: no es una resolución, no tiene resultado y no forma parte del estado auditado."""
        self.solicitudes[rid] = dict(kw); return rid
    @_atomica()
    def registrar_resolucion(self, rid, resultado, motivos=(), **sol):
        """Persiste una resolución con resultado definitivo ('aceptada' o 'rechazada'). El ID no puede existir."""
        assert resultado in ("aceptada", "rechazada")
        a = self.at.get(sol.get("atribucion")); p = sol.get("previo")
        fila = dict(id=rid, resultado=resultado, seq=self.tick(), motivos=tuple(motivos), version=a["version"] if a else None, version_origen=a["origen_version"] if a else None, previo=p,
                    previo_sello=self.res[p]["sello"] if p in self.res else None, **{k: sol.get(k) for k in CAMPOS_SOL})
        if resultado == "aceptada": fila["evidencia_historica"] = copy.deepcopy(self.v[sol["version_evidencia"]]["campos"].get(sol["campo"]))
        return self.res.agregar(fila)
    @_atomica()
    def rechazar_resolucion(self, rid, motivos):
        """Decisión de rechazo: crea un registro nuevo y definitivo; la atribución no cambia."""
        self.registrar_resolucion(rid, "rechazada", motivos, **self.solicitudes[rid]); return False
    def validar_resolucion(self, sol):
        r = sol; a = self.at.get(r["atribucion"]); c = []
        if a is None: return ["V01"]
        if a["persona"] != r["afectado"]: c.append("V02")
        if a["fuente"] != r["fuente"] or a["org"] != r["org"]: c.append("V03")
        if a["pieza"] != r["pieza"]: c.append("V04")
        if a["campo"] != r["campo"]: c.append("V05")
        if r["version_evidencia"] != a["version"] or r["version_evidencia"] not in self.v or self.estado(a["id"]) != "activa": c.append("V06")
        mot = self.ev.get(r["evento_motivador"])
        if not mot or mot["campo"] != r["campo"]: c.append("V07")
        if not r.get("actor_cambio") or not mot or mot["actor"] != r["actor_cambio"]: c.append("V08")
        if not r.get("solicitante") or r["solicitante"] not in self.members: c.append("V09")
        if not (r.get("evidencia") or "").strip(): c.append("V11")
        if r.get("auth_uid") != r.get("resolutor"): c.append("V12")
        if r.get("previo") is not None:
            pr = self.res.get(r["previo"])
            if pr is None or pr["org"] != r["org"] or pr["atribucion"] != r["atribucion"] or pr["resultado"] != "rechazada": c.append("V13")
        c += elegibilidad_resolutor(self, r)
        return c
    @_atomica()
    def aplicar_resolucion(self, rid):
        if rid in self.res: raise ResolucionInmutable("el ID %s ya existe: una resolución no se reemplaza" % rid)
        sol = self.solicitudes[rid]; cod = self.validar_resolucion(sol)
        if cod: self.registrar_resolucion(rid, "rechazada", cod, **sol); return False
        self.registrar_resolucion(rid, "aceptada", (), **sol)
        self.est.append(dict(seq=self.tick(), atr=sol["atribucion"], estado="historica", resolucion=rid, motivo="resolución aceptada")); return True
    def cadena_resoluciones(self, atr):
        """Resoluciones de una atribución, de la más antigua a la más reciente (se recorre; no se edita ninguna fila)."""
        return [r["id"] for r in sorted((r for r in self.res.values() if r["atribucion"] == atr), key=lambda r: r["seq"])]
    def decision_vigente(self, atr):
        ch = self.cadena_resoluciones(atr); return self.res[ch[-1]]["resultado"] if ch else None

    # ---- 11, 12, 13: procedencia (incluye el arte) y E ----
    def _versiones_exactas(self, vid):
        v = self.v[vid]; out = [vid]; r = v["refs"]
        for k in ("brief", "promotion", "master"):
            if r.get(k): out.append(r[k])
        return out
    def _assets_exactos(self, vid):
        """Assets usados por cada versión de copy exacta: el vigente en el campo arte y los referenciados por sus atribuciones."""
        out = []
        for ve in self._versiones_exactas(vid):
            if ve not in self.v or self.v[ve]["fuente"] != "copy": continue
            campo = self.v[ve]["campos"].get("arte"); ids = [campo["contenido"]] if campo and not campo["eliminado"] and campo["contenido"] else []
            ids += [a["asset"] for a in self.at.values() if a["version"] == ve and a.get("asset")]
            for i in ids:
                if i not in out: out.append(i)
        return out
    def _fuentes_exactas(self, vid): return dict(versiones=self._versiones_exactas(vid), assets=self._assets_exactos(vid))
    def _cadena_prev(self, vid):
        out = []; cur = vid
        while cur in self.v and cur not in out: out.append(cur); cur = self.v[cur]["prev"]
        return out
    def _id_uploader(self, cur, x, y):
        """H-01 y H-02: identidad, membresía, evento de carga y atribución directa del uploader, relación por relación."""
        h = []; u = y.get("uploader"); mm = self.members.get(u)
        if mm is not None:
            if mm["org"] != y["org"] or mm["org"] != self.org: h.append("%s: el uploader %s del asset %s pertenece a otra organización" % (cur, u, x))
            if not mm.get("activo"): h.append("%s: el uploader %s del asset %s tiene membresía inactiva" % (cur, u, x))
        e = self.ev.get(y.get("evento_carga"))
        if e is not None:
            if e["org"] != y["org"] or e["org"] != self.org: h.append("%s: el evento de carga del asset %s pertenece a otra organización" % (cur, x))
            if e["pieza"] != y["pieza"]: h.append("%s: el evento de carga del asset %s pertenece a otra pieza" % (cur, x))
            if e.get("asset_version") != y["version_asset"]: h.append("%s: el evento de carga del asset %s corresponde a otra versión del asset" % (cur, x))
            if e.get("campo") != "arte": h.append("%s: el evento de carga del asset %s no está vinculado al campo arte" % (cur, x))
            if e["version"] != y["copy_version"]: h.append("%s: el evento de carga del asset %s corresponde a otra versión de copy" % (cur, x))
            if e.get("actor") != u: h.append("%s: el actor del evento de carga del asset %s no es el uploader" % (cur, x))
            if e.get("auth") != u: h.append("%s: el actor autenticado del evento de carga del asset %s no es el uploader" % (cur, x))
            directas = [b for b in self.at.values() if b["persona"] == u and b.get("asset") == x and b["evento"] == y["evento_carga"] and b["rel"] == "directa"]
            if directas and not any(b["version"] == y["copy_version"] and b["origen_version"] == y["copy_version"] and b["pieza"] == y["pieza"] and b["org"] == y["org"] and b.get("asset_version") == y["version_asset"] and b["fuente"] == "asset" and b["campo"] == "arte" for b in directas):
                h.append("%s: la atribución directa del uploader del asset %s no corresponde a la organización, pieza y versión exactas" % (cur, x))
        return h
    def _id_reutilizacion(self, cur, x, y):
        """H-03: identidad completa del evento de reutilización y diferenciación entre uploader original y reutilizador."""
        h = []; e = self.ev.get(y.get("evento_reutilizacion")); r = y.get("reutilizador"); o = self.assets.get(y.get("origen"))
        if y.get("uploader") is not None: h.append("%s: el reutilizador figura como uploader del asset reutilizado %s" % (cur, x))
        mm = self.members.get(r)
        if mm is not None and (mm["org"] != y["org"] or not mm.get("activo")): h.append("%s: membresía inactiva o ajena del reutilizador %s" % (cur, r))
        if y.get("evento_reutilizacion") is not None and any(z is not y and z.get("evento_reutilizacion") == y["evento_reutilizacion"] for z in self.assets.values()): h.append("%s: la reutilización de %s no tiene evento propio" % (cur, x))
        if e is not None:
            if e["org"] != y["org"] or e["org"] != self.org: h.append("%s: el evento de reutilización de %s pertenece a otra organización" % (cur, x))
            if e["pieza"] != y["pieza"] or e["pieza"] != self.v[y["copy_version"]]["pieza"]: h.append("%s: el evento de reutilización de %s pertenece a otra pieza" % (cur, x))
            if e.get("actor") != r or e.get("auth") != r: h.append("%s: el evento de reutilización de %s identifica a otro actor" % (cur, x))
            if e.get("campo") != "arte" or e.get("asset") != x: h.append("%s: el evento de reutilización de %s no es una reutilización del asset exacto" % (cur, x))
            if e.get("asset_version") != y["version_asset"] or e.get("asset_version_id") != x: h.append("%s: el evento de reutilización de %s referencia otra versión de asset (la versión del asset de destino no coincide)" % (cur, x))
            if o is not None and y.get("origen_version_asset") != o["version_asset"]: h.append("%s: el evento de reutilización de %s referencia otra versión de asset de origen" % (cur, x))
            if e["version"] != y["copy_version"]: h.append("%s: el evento de reutilización de %s no referencia la versión exacta de copy" % (cur, x))
        return h + self._id_origen(cur, x, y)
    def _id_origen(self, cur, x, y):
        """H-02 (v12): identidad exacta del origen de la reutilización por referencia a registros concretos; el número de versión, la pieza o la organización por sí solos no demuestran identidad."""
        h = []; e = self.ev.get(y.get("evento_reutilizacion"))
        if e is None: return h
        if e.get("id") != y["evento_reutilizacion"]: h.append("%s: el registro del evento de reutilización de %s no corresponde a su identificador" % (cur, x))
        o = self.assets.get(y.get("source_asset_version_id"))
        if y.get("origen") != y.get("source_asset_version_id"): h.append("%s: el reutilizado %s apunta a un origen distinto del declarado en la reutilización" % (cur, x))
        if o is None: h.append("%s: el origen declarado por %s no existe" % (cur, x)); return h
        if o.get("id") != y["source_asset_version_id"]: h.append("%s: el registro del asset de origen de %s no corresponde a su identificador" % (cur, x))
        if (e.get("source_asset_version_id"), e.get("source_asset_id")) != (o["id"], o.get("asset_id")) or y.get("source_asset_id") != o.get("asset_id"): h.append("%s: la reutilización %s no identifica el asset y la versión exactos del origen" % (cur, x))
        _eo = _Err(); ue, up, at0 = self._origen_carga(o["id"], _eo); eo = self.ev.get(ue); h += ["%s: %s" % (cur, z) for z in _eo]
        try: _rz = self._raiz_asset(o["id"])
        except KeyError: _rz = None
        if _rz is not None and (e.get("source_root_asset_version_id"), e.get("source_root_asset_id"), y.get("source_root_asset_version_id")) != (_rz["id"], _rz.get("asset_id"), _rz["id"]): h.append("%s: la reutilización %s no identifica el asset raíz y su versión exacta" % (cur, x))
        if e.get("source_upload_event_id") != ue or y.get("source_upload_event_id") != ue: h.append("%s: la reutilización %s no identifica el evento de carga del origen" % (cur, x))
        if eo is None or eo.get("id") != ue: h.append("%s: el evento de carga del origen de %s no existe o no corresponde a su identificador" % (cur, x))
        if e.get("source_uploader_id") != up: h.append("%s: la reutilización %s no identifica al uploader original del origen" % (cur, x))
        if e.get("source_attribution_id") != at0 or y.get("source_attribution_id") != at0: h.append("%s: la reutilización %s no referencia la atribución original del uploader" % (cur, x))
        if e.get("source_asset_version") != o["version_asset"]: h.append("%s: la versión de origen de la reutilización %s no coincide con el registro" % (cur, x))
        if o["org"] != self.org or o["org"] != y["org"]: h.append("%s: el origen de %s pertenece a otra organización" % (cur, x))
        oc = self.v.get(o.get("copy_version"))
        propio = self.ev.get(o.get("evento_carga") if o["tipo"] != "reutilizado" else o.get("evento_reutilizacion"))
        if oc is None or o["pieza"] != oc["pieza"] or propio is None or o["pieza"] != propio.get("pieza") or (eo is not None and eo.get("pieza") != self.assets.get(eo.get("asset"), {}).get("pieza")): h.append("%s: el origen de %s pertenece a otra pieza que su versión de copy y su evento" % (cur, x))
        if e.get("auth") != y.get("reutilizador"): h.append("%s: el actor autenticado de la reutilización %s no es el reutilizador registrado" % (cur, x))
        if e.get("asset_id") != y.get("asset_id") or e.get("asset_version_id") != x: h.append("%s: el evento de reutilización de %s no identifica el asset reutilizado y su versión" % (cur, x))
        try: raiz = self._raiz_asset(x)
        except KeyError: raiz = None
        if raiz is not None and (y.get("evento_carga_original") != raiz["evento_carga_original"] or self.ev.get(y.get("evento_carga_original")) is None): h.append("%s: la cadena de reutilización de %s perdió el vínculo con el evento original de carga" % (cur, x))
        return h
    def _huecos_ancestros(self, cur):
        """H-02 regla 7: toda atribución heredada de asset conserva la referencia verificable a su antecesora."""
        h = []
        for b in self.at.values():
            if b["version"] != cur or b["rel"] != "heredada" or not b.get("asset"): continue
            p = self.at.get(b.get("previo"))
            if p is None: h.append("%s: la atribución heredada %s carece de antecesor verificable" % (cur, b["id"]))
            elif (p["persona"], p["evento"], p["org"], p["fuente"], p["campo"], p["origen_version"]) != (b["persona"], b["evento"], b["org"], b["fuente"], b["campo"], b["origen_version"]) or p.get("asset") not in self._cierre_asset(b["asset"]):
                h.append("%s: el antecesor de la atribución heredada %s no corresponde a su cadena" % (cur, b["id"]))
        return h
    def _huecos_asset(self, cur, aid):
        h = []; vis = []; x = aid; ver = self.v[cur]; cad = self._cadena_prev(cur); cabeza = True
        while x is not None:
            if x in vis: h.append("%s: ciclo en la cadena de assets (%s)" % (cur, " → ".join(vis + [x]))); break
            vis.append(x); y = self.assets.get(x)
            if y is None: h.append("%s: el asset de origen %s no existe" % (cur, x)); break
            if y["org"] != self.org: h.append("%s: el asset %s pertenece a otra organización" % (cur, x))
            if cabeza and y["pieza"] != ver["pieza"]: h.append("%s: el asset %s pertenece a otra pieza sin relación válida" % (cur, x))
            if cabeza and y["copy_version"] not in cad: h.append("%s: el asset %s está vinculado a otra versión de copy (%s)" % (cur, x, y["copy_version"]))
            t = y["tipo"]; nxt = None
            if t in ("nuevo", "sustituto", "modificado"):
                if t == "modificado": nxt = y.get("previo")
                if t == "modificado" and nxt is None: h.append("%s: el asset modificado %s no referencia su versión anterior" % (cur, x))
                if not y.get("uploader") or y["uploader"] not in self.members: h.append("%s: el asset %s no tiene uploader registrado" % (cur, x))
                e = self.ev.get(y.get("evento_carga"))
                if not e or e["tipo"] != "asset_uploader" or e["actor"] != y.get("uploader") or e.get("asset") != x: h.append("%s: el asset %s no tiene evento de carga válido" % (cur, x))
                elif not any(b["persona"] == y["uploader"] and b.get("asset") == x and b["evento"] == y["evento_carga"] and b["rel"] == "directa" for b in self.at.values()): h.append("%s: falta la atribución directa del uploader del asset %s" % (cur, x))
                h += self._id_uploader(cur, x, y)
            elif t == "reutilizado":
                nxt = y.get("origen")
                if nxt is None: h.append("%s: el asset reutilizado %s no referencia su origen" % (cur, x))
                e = self.ev.get(y.get("evento_reutilizacion"))
                if not y.get("reutilizador") or not e or e["tipo"] not in ("copy_author", "copy_editor") or e["actor"] != y["reutilizador"] or e.get("asset") != x or e["version"] != y["copy_version"]: h.append("%s: el asset %s no tiene evento de reutilización válido" % (cur, x))
                try: raiz = self._raiz_asset(x)
                except KeyError: raiz = None
                h += self._id_reutilizacion(cur, x, y)
                if raiz is not None:
                    if y["uploader_original"] != raiz["uploader_original"] or y["evento_carga_original"] != raiz["evento_carga_original"]: h.append("%s: el uploader original del asset %s no coincide con el origen" % (cur, x))
                    if not any(b["persona"] == raiz["uploader_original"] and b["fuente"] == "asset" and b.get("asset") == x and b["version"] == y["copy_version"] for b in self.at.values()): h.append("%s: falta la atribución del uploader original en el asset reutilizado %s" % (cur, x))
                    if y.get("material") and not any(b["persona"] == y["reutilizador"] and b.get("asset") == x and b["evento"] == y["evento_reutilizacion"] and b["rel"] == "directa" for b in self.at.values()): h.append("%s: falta la atribución del reutilizador del asset %s" % (cur, x))
            else: h.append("%s: tipo de asset %s desconocido" % (cur, t))
            z = self.assets.get(nxt) if nxt else None
            if z is not None and z["org"] != y["org"]: h.append("%s: la cadena del asset %s cruza organizaciones" % (cur, x))
            if z is not None and z["pieza"] != y["pieza"] and t != "reutilizado": h.append("%s: la cadena del asset %s cruza piezas sin reutilización" % (cur, x))
            cabeza = False; x = nxt
        return h
    def _huecos_arte(self, cur):
        v = self.v[cur]
        if v["fuente"] != "copy": return []
        d = self.arte_decl.get(cur); campo = v["campos"].get("arte"); h = []
        if d is None: h.append("%s: arte sin declarar (la ausencia de registros no prueba no_aplica)" % cur)
        elif d["estado"] == "no_aplica" and (campo is not None or any(y["copy_version"] == cur for y in self.assets.values())): h.append("%s: se declara arte no_aplica pero la versión registra arte o un asset" % cur)
        elif d["estado"] == "con_arte" and campo is None: h.append("%s: se declara arte pero la versión no registra ningún asset" % cur)
        elif d["estado"] not in ("no_aplica", "con_arte"): h.append("%s: declaración de arte inválida" % cur)
        elif d["heredada_de"] is not None and d["heredada_de"] not in self.arte_decl: h.append("%s: la declaración de arte hereda de una versión sin declaración" % cur)
        elif not d.get("actor") and d["heredada_de"] is None: h.append("%s: la declaración de arte no identifica al actor" % cur)
        ids = []
        if campo is not None and not campo["eliminado"] and campo.get("contenido"): ids.append(campo["contenido"])
        ids += [a["asset"] for a in self.at.values() if a["version"] == cur and a.get("asset") and a["asset"] not in ids]
        for i in ids: h += self._huecos_asset(cur, i)
        return h + self._huecos_ancestros(cur)
    def reconstruir_procedencia(self, vid):
        """Recorre la cadena de cada fuente exacta (incluido el arte) y comprueba atribución por campo, herencia y procedencia de cada asset."""
        huecos = []; vistas = []
        for raiz in self._fuentes_exactas(vid)["versiones"]:
            cur = raiz
            while cur is not None:
                if cur not in self.v: huecos.append("versión %s ausente" % cur); break
                vistas.append(cur); ver = self.v[cur]
                for campo in ver["campos"]:
                    if not [a for a in self.at.values() if a["version"] == cur and a["campo"] == campo]: huecos.append("%s: campo %s sin atribución" % (cur, campo))
                huecos += self._huecos_arte(cur)
                p = ver["prev"]
                if p is not None and p in self.v:
                    for a in self.activas(p):
                        if not [b for b in self.at.values() if b["version"] == cur and b["linaje"] == a["linaje"]]: huecos.append("%s: no hereda la atribución %s" % (cur, a["id"]))
                cur = p
        return dict(versiones=vistas, completa=not huecos, huecos=huecos, assets=self._assets_exactos(vid))
    def calcular_E(self, vid):
        proc = self.reconstruir_procedencia(vid)
        if not proc["completa"]: return dict(completa=False, E=None, motivo=proc["huecos"])
        E = {}
        for v_ in self._versiones_exactas(vid):
            for a in self.activas(v_): E.setdefault(a["persona"], []).append(a["id"])
        return dict(completa=True, E=E, motivo=[], assets=proc["assets"])
    def procedencia_completa(self, vid): return self.reconstruir_procedencia(vid)["completa"]

def elegibilidad_resolutor(m, r):
    """K46 R1–R9 sobre la cadena completa: devuelve los códigos que impiden que el resolutor resuelva (vacío si es elegible)."""
    u = r.get("resolutor"); mem = m.members.get(u); c = []
    if not (mem and mem["org"] == r["org"] and mem["activo"]): c.append("R1")
    if "piece.review" not in (m.roles.get(mem["rol"], set()) if mem else set()): c.append("R2")
    if u == r["afectado"]: c.append("R3")
    if u == r.get("solicitante"): c.append("R4")
    if u == r.get("actor_cambio"): c.append("R5")
    campo = r["campo"]; actual = r["version_evidencia"]
    cadena = set()
    cur = actual
    while cur in m.v and cur not in cadena: cadena.add(cur); cur = m.v[cur]["prev"]
    if any(e["actor"] == u and e["campo"] == campo and e["version"] in cadena for e in m.ev.values()): c.append("R6")
    if any(a["persona"] == u and a["campo"] == campo and a["rel"] == "heredada" and a["version"] == actual and m.estado(a["id"]) == "activa" for a in m.at.values()): c.append("R7")
    otras = set(m._versiones_exactas(actual)) - {actual}
    if any(a["persona"] == u and a["version"] in otras for a in m.at.values()): c.append("R8")
    mot = m.ev.get(r["evento_motivador"], {})
    if any(a["persona"] == u and a["campo"] == campo and a["version"] == actual and m.estado(a["id"]) == "activa" for a in m.at.values()) or any(e["actor"] == u and e["op"] == mot.get("op") for e in m.ev.values()): c.append("R9")
    return c

def resolutores_elegibles(m, r):
    return [u for u in m.members if not elegibilidad_resolutor(m, dict(r, resolutor=u))]

# =====================================================================================================
# Auditor independiente: reimplementa las invariantes sobre las instantáneas, sin llamar al motor
# =====================================================================================================
def _estado(s, aid):
    e = [x for x in s["est"] if x["atr"] == aid]; return e[-1]["estado"] if e else "activa"
def _activos(s): return {a for a in s["at"] if _estado(s, a) == "activa"}
def _exactas(s, vid):
    r = s["v"][vid]["refs"]; return [vid] + [r[k] for k in ("brief", "promotion", "master") if r.get(k)]
def _cad(s, vid):
    out = []; cur = vid
    while cur in s["v"] and cur not in out: out.append(cur); cur = s["v"][cur]["prev"]
    return out
def _hall_arte(s, cur):
    """Auditor independiente de la procedencia del arte: reconstruye la cadena de cada asset desde las tablas, sin llamar al motor. Devuelve (código, mensaje)."""
    ver = s["v"].get(cur); out = []
    if ver is None or ver["fuente"] != "copy": return out
    ad = s["arte_decl"]; d = ad.get(cur); campo = ver["campos"].get("arte")
    if d is None: out.append(("I20", "%s: la versión no declara el estado del arte" % cur))
    elif d["estado"] not in ("no_aplica", "con_arte"): out.append(("I20", "%s: declaración de arte inválida" % cur))
    elif d["estado"] == "no_aplica" and (campo is not None or any(y_["copy_version"] == cur for y_ in s["assets"].values())): out.append(("I20", "%s: declara no_aplica pero registra arte o un asset" % cur))
    elif d["estado"] == "con_arte" and campo is None: out.append(("I20", "%s: declara arte sin asset" % cur))
    elif d.get("heredada_de") is None and not d.get("actor"): out.append(("I20", "%s: declaración de arte sin actor" % cur))
    elif d.get("heredada_de") is not None and d["heredada_de"] not in ad: out.append(("I20", "%s: la declaración heredada no tiene origen" % cur))
    ids = [campo["contenido"]] if campo and not campo["eliminado"] and campo.get("contenido") else []
    ids += [a["asset"] for a in s["at"].values() if a["version"] == cur and a.get("asset") and a["asset"] not in ids]
    cad = _cad(s, cur); T = s["assets"]
    def raiz(x):
        vis = []
        while x in T and x not in vis:
            vis.append(x); y = T[x]; n = y.get("origen") if y["tipo"] == "reutilizado" else y.get("previo") if y["tipo"] == "modificado" else None
            if n is None: return y
            x = n
        return None
    for aid in ids:
        x = aid; vis = []; cabeza = True
        while x is not None:
            if x in vis: out.append(("I19", "%s: ciclo en la cadena de assets %s" % (cur, " → ".join(vis + [x])))); break
            vis.append(x); y = T.get(x)
            if y is None: out.append(("I19", "%s: asset de origen %s inexistente" % (cur, x))); break
            if y["org"] != s["org"]: out.append(("I19", "%s: el asset %s pertenece a otra organización" % (cur, x)))
            if cabeza and y["pieza"] != ver["pieza"]: out.append(("I19", "%s: el asset %s pertenece a otra pieza sin relación válida" % (cur, x)))
            if cabeza and y["copy_version"] not in cad: out.append(("I18", "%s: el asset %s no corresponde a esta versión de copy (%s)" % (cur, x, y["copy_version"])))
            t = y["tipo"]; n = None; ev = s["ev"]
            if t in ("nuevo", "sustituto", "modificado"):
                if t == "modificado":
                    n = y.get("previo")
                    if n is None: out.append(("I19", "%s: asset modificado %s sin referencia a su versión anterior" % (cur, x)))
                if not y.get("uploader") or y["uploader"] not in s["members"]: out.append(("I16", "%s: asset %s sin uploader registrado" % (cur, x)))
                e = ev.get(y.get("evento_carga"))
                if not e or e["tipo"] != "asset_uploader" or e["actor"] != y.get("uploader") or e.get("asset") != x: out.append(("I16", "%s: asset %s sin evento de carga válido" % (cur, x)))
                elif not any(b["persona"] == y["uploader"] and b.get("asset") == x and b["evento"] == y["evento_carga"] and b["rel"] == "directa" for b in s["at"].values()): out.append(("I16", "%s: asset %s sin atribución directa del uploader" % (cur, x)))
            elif t == "reutilizado":
                n = y.get("origen")
                if n is None: out.append(("I19", "%s: asset reutilizado %s sin referencia al origen" % (cur, x)))
                e = ev.get(y.get("evento_reutilizacion"))
                if not y.get("reutilizador") or not e or e["tipo"] not in ("copy_author", "copy_editor") or e["actor"] != y["reutilizador"] or e.get("asset") != x or e["version"] != y["copy_version"]: out.append(("I17", "%s: asset %s sin evento de reutilización válido" % (cur, x)))
                r_ = raiz(x)
                if r_ is not None:
                    if (y["uploader_original"], y["evento_carga_original"]) != (r_["uploader_original"], r_["evento_carga_original"]): out.append(("I17", "%s: el uploader original del asset %s no coincide con el origen" % (cur, x)))
                    if not any(b["persona"] == r_["uploader_original"] and b["fuente"] == "asset" and b.get("asset") == x and b["version"] == y["copy_version"] for b in s["at"].values()): out.append(("I17", "%s: falta la atribución del uploader original en %s" % (cur, x)))
                    if y.get("material") and not any(b["persona"] == y["reutilizador"] and b.get("asset") == x and b["evento"] == y["evento_reutilizacion"] and b["rel"] == "directa" for b in s["at"].values()): out.append(("I17", "%s: falta la atribución propia del reutilizador de %s" % (cur, x)))
            else: out.append(("I19", "%s: tipo de asset desconocido en %s" % (cur, x)))
            z = T.get(n) if n else None
            if z is not None and z["org"] != y["org"]: out.append(("I19", "%s: la cadena de %s cruza organización" % (cur, x)))
            if z is not None and z["pieza"] != y["pieza"] and t != "reutilizado": out.append(("I19", "%s: la cadena de %s cruza pieza sin reutilización" % (cur, x)))
            cabeza = False; x = n
    out += _hall_identidad(s, cur, ids)
    out += _hall_cadena(s, cur, ids)
    return out
def _hall_identidad(s, cur, ids):
    """Auditor independiente H-01 a H-03: identidad del uploader, del evento de carga, de la atribución directa, de la reutilización y de los antecesores. Solo lee las tablas del estado."""
    out = []; T = s["assets"]; EV = s["ev"]; AT = s["at"]; MB = s["members"]; org = s["org"]; vistos = set()
    def cierre(a):
        r = []; q = [a]
        while q:
            z = q.pop()
            if z in r or z not in T: continue
            r.append(z); q += [T[z].get("origen"), T[z].get("previo")]
        return r
    for k_, v_ in EV.items():
        if v_.get("id") != k_: out.append(("I28", "%s: el evento %s está intercambiado: la clave no coincide con su identificador (%s)" % (cur, k_, v_.get("id"))))
    for k_, v_ in T.items():
        if v_.get("id") != k_: out.append(("I28", "%s: el asset %s está intercambiado: la clave no coincide con su identificador (%s)" % (cur, k_, v_.get("id"))))
    def raiz_(a):
        vis = []
        while a in T and a not in vis:
            vis.append(a); z = T[a]; n = z.get("origen") if z["tipo"] == "reutilizado" else z.get("previo") if z["tipo"] == "modificado" else None
            if n is None: return z
            a = n
        return None
    def carga_esperada(o):
        """Evento de carga, uploader y atribución directa esperados del asset raíz exacto de `o`, reconstruidos solo de las tablas (v13: de la raíz, no del campo guardado en el reutilizado ni del evento por su asset)."""
        r_ = raiz_(o["id"])
        if r_ is None: return None, None, None
        ue = r_.get("evento_carga"); up = r_.get("uploader")
        at0 = [b["id"] for b in AT.values() if b["rel"] == "directa" and b["fuente"] == "asset" and b.get("asset") == r_["id"] and b["evento"] == ue and b["persona"] == up and (b["org"], b["pieza"], b["version"], b["origen_version"], b.get("asset_version"), b["campo"]) == (r_["org"], r_["pieza"], r_["copy_version"], r_["copy_version"], r_["version_asset"], "arte")]
        return ue, up, (at0[0] if len(at0) == 1 else None)
    for aid in ids:
        for x in cierre(aid):
            if x in vistos: continue
            vistos.add(x); y = T[x]; t = y["tipo"]
            if t in ("nuevo", "sustituto", "modificado"):
                u = y.get("uploader"); m_ = MB.get(u)
                if m_ is not None and (m_["org"] != y["org"] or m_["org"] != org): out.append(("I22", "%s: el uploader %s de %s pertenece a otra organización" % (cur, u, x)))
                if m_ is not None and not m_.get("activo"): out.append(("I22", "%s: el uploader %s de %s tiene membresía inactiva" % (cur, u, x)))
                e = EV.get(y.get("evento_carga"))
                if e is None: continue
                if e["org"] != y["org"] or e["org"] != org: out.append(("I23", "%s: el evento de carga de %s pertenece a otra organización" % (cur, x)))
                if e["pieza"] != y["pieza"]: out.append(("I23", "%s: el evento de carga de %s pertenece a otra pieza" % (cur, x)))
                if e.get("asset") != x or e.get("asset_version") != y["version_asset"] or e.get("asset_version_id") != x: out.append(("I23", "%s: el evento de carga de %s corresponde a otra versión del asset" % (cur, x)))
                if e.get("campo") != "arte": out.append(("I23", "%s: el evento de carga de %s no está vinculado al campo arte" % (cur, x)))
                if e.get("tipo") != "asset_uploader": out.append(("I23", "%s: el evento de carga de %s no es un evento de carga de asset (%s)" % (cur, x, e.get("tipo"))))
                if e.get("asset") != x:
                    z_ = T.get(e.get("asset"))
                    if z_ is not None and EV.get(z_.get("evento_carga"), {}).get("asset") == x: out.append(("I28", "%s: los eventos de carga de %s y %s están intercambiados" % (cur, x, e.get("asset"))))
                if e["version"] != y["copy_version"]: out.append(("I23", "%s: el evento de carga de %s corresponde a otra versión de copy" % (cur, x)))
                if e["actor"] != u: out.append(("I23", "%s: el actor del evento de carga de %s no es el uploader" % (cur, x)))
                if e.get("auth") != u: out.append(("I23", "%s: el actor autenticado del evento de carga de %s no es el uploader" % (cur, x)))
                cand = [b for b in AT.values() if b["rel"] == "directa" and b["fuente"] == "asset" and (b.get("asset") == x or b["evento"] == y["evento_carga"])]
                exact = [b for b in cand if b.get("asset") == x and b["evento"] == y["evento_carga"] and b["persona"] == u and (b["version"], b["origen_version"], b["pieza"], b["org"], b.get("asset_version"), b["campo"]) == (y["copy_version"], y["copy_version"], y["pieza"], y["org"], y["version_asset"], "arte")]
                if len(exact) != 1:
                    if not cand: out.append(("I24", "%s: no existe la atribución directa del uploader de %s" % (cur, x)))
                    for b in cand:
                        if b["evento"] == y["evento_carga"] and b.get("asset") != x: out.append(("I24", "%s: la atribución directa del uploader de %s pertenece a otro asset (%s)" % (cur, x, b.get("asset"))))
                        elif b.get("asset") == x and b["evento"] != y["evento_carga"]: out.append(("I24", "%s: la atribución directa del uploader de %s pertenece a otro evento de carga" % (cur, x)))
                        elif b.get("asset") == x and b["persona"] != u: out.append(("I24", "%s: la atribución directa del uploader de %s pertenece a otro uploader (%s)" % (cur, x, b["persona"])))
                        elif b.get("asset") == x: out.append(("I24", "%s: la atribución directa del uploader de %s no corresponde a la versión de copy, pieza u organización exactas" % (cur, x)))
                    if len(exact) > 1: out.append(("I24", "%s: la atribución directa del uploader de %s es ambigua" % (cur, x)))
            elif t == "reutilizado":
                r = y.get("reutilizador"); e = EV.get(y.get("evento_reutilizacion")); o = T.get(y.get("origen"))
                if y.get("uploader") is not None: out.append(("I17", "%s: el reutilizador figura como uploader de %s" % (cur, x)))
                m_ = MB.get(r)
                if m_ is not None and (m_["org"] != y["org"] or not m_.get("activo")): out.append(("I25", "%s: membresía inactiva o ajena del reutilizador %s" % (cur, r)))
                if y.get("evento_reutilizacion") is not None and [k for k, z in T.items() if z.get("evento_reutilizacion") == y["evento_reutilizacion"]] != [x]: out.append(("I25", "%s: la reutilización de %s no tiene evento propio" % (cur, x)))
                if e is not None:
                    S_row, S_decl, S_ev = y.get("origen"), y.get("source_asset_version_id"), e.get("source_asset_version_id"); od = T.get(S_decl)
                    if S_row != S_decl: out.append(("I27", "%s: el asset reutilizado %s apunta a un origen (%s) distinto del declarado (%s)" % (cur, x, S_row, S_decl)))
                    if od is None: out.append(("I27", "%s: el origen declarado %s de %s no existe" % (cur, S_decl, x)))
                    else:
                        if S_ev != S_decl:
                            z = T.get(S_ev)
                            if z is None: out.append(("I27", "%s: el evento de reutilización de %s referencia un asset de origen inexistente" % (cur, x)))
                            elif z.get("asset_id") == od.get("asset_id"): out.append(("I27", "%s: el evento de reutilización de %s referencia otra versión del mismo asset de origen (%s en lugar de %s)" % (cur, x, S_ev, S_decl)))
                            elif z.get("version_asset") == od.get("version_asset"): out.append(("I27", "%s: el evento de reutilización de %s referencia otro asset de origen con el mismo número de versión (%s en lugar de %s)" % (cur, x, S_ev, S_decl)))
                            else: out.append(("I27", "%s: el evento de reutilización de %s referencia otro asset de origen de número de versión distinto (%s en lugar de %s)" % (cur, x, S_ev, S_decl)))
                        elif e.get("source_asset_id") != od.get("asset_id") or y.get("source_asset_id") != od.get("asset_id"): out.append(("I27", "%s: la reutilización de %s declara un identificador de asset de origen que no corresponde al registro" % (cur, x)))
                        ue, up_, at0 = carga_esperada(od); eu = EV.get(e.get("source_upload_event_id"))
                        if e.get("source_upload_event_id") != ue or y.get("source_upload_event_id") != ue:
                            if eu is None: out.append(("I27", "%s: el evento de reutilización de %s referencia un evento de carga de origen inexistente" % (cur, x)))
                            elif eu.get("tipo") != "asset_uploader": out.append(("I27", "%s: el evento de reutilización de %s referencia como evento de carga un evento que no es de carga (%s)" % (cur, x, eu.get("tipo"))))
                            elif T.get(eu.get("asset"), {}).get("asset_id") == od.get("asset_id"): out.append(("I27", "%s: el evento de reutilización de %s referencia el evento de carga de otra versión del mismo asset de origen" % (cur, x)))
                            else: out.append(("I27", "%s: el evento de reutilización de %s referencia el evento de carga de otro asset" % (cur, x)))
                        if e.get("source_uploader_id") != up_: out.append(("I27", "%s: el evento de reutilización de %s referencia otro uploader original (%s en lugar de %s)" % (cur, x, e.get("source_uploader_id"), up_)))
                        if e.get("source_attribution_id") != at0 or y.get("source_attribution_id") != at0: out.append(("I27", "%s: la reutilización de %s no referencia la atribución original del uploader" % (cur, x)))
                        if e.get("source_asset_version") != od.get("version_asset"): out.append(("I27", "%s: el evento de reutilización de %s referencia una versión de origen incorrecta (%s en lugar de %s)" % (cur, x, e.get("source_asset_version"), od.get("version_asset"))))
                        if od["org"] != org or od["org"] != y["org"]: out.append(("I27", "%s: el origen de %s pertenece a otra organización" % (cur, x)))
                        propio = EV.get(od.get("evento_carga") if od["tipo"] != "reutilizado" else od.get("evento_reutilizacion"))
                        if od["pieza"] != s["v"].get(od["copy_version"], {}).get("pieza") or propio is None or od["pieza"] != propio.get("pieza"): out.append(("I27", "%s: el origen de %s pertenece a otra pieza que su versión de copy y su evento" % (cur, x)))
                    if e.get("version") != y["copy_version"] and e.get("version") in s["v"] and s["v"][e["version"]]["pieza"] == y["pieza"]: out.append(("I27", "%s: el evento de reutilización de %s referencia otra versión de copy de la misma pieza (%s)" % (cur, x, e.get("version"))))
                    if e.get("actor") == r and e.get("auth") != r: out.append(("I27", "%s: el actor autenticado del evento de reutilización de %s no coincide con el reutilizador registrado" % (cur, x)))
                    if e.get("asset_id") != y.get("asset_id") or e.get("asset_version_id") != x: out.append(("I27", "%s: el evento de reutilización de %s no identifica el asset reutilizado y su versión" % (cur, x)))
                    rz = raiz_(x)
                    if rz is None: out.append(("I27", "%s: la cadena de origen de %s no es verificable (referencia ausente o ciclo)" % (cur, x)))
                    else:
                        if (e.get("source_root_asset_version_id"), e.get("source_root_asset_id"), y.get("source_root_asset_version_id")) != (rz["id"], rz.get("asset_id"), rz["id"]): out.append(("I27", "%s: la reutilización de %s no identifica el asset raíz y su versión exacta" % (cur, x)))
                        eu_ = EV.get(e.get("source_upload_event_id"))
                        if eu_ is not None and (eu_.get("asset") != rz["id"] or eu_.get("asset_version_id") != rz["id"]): out.append(("I27", "%s: el evento de carga referenciado por la reutilización de %s no corresponde al asset raíz %s" % (cur, x, rz["id"])))
                    if rz is not None and (y.get("evento_carga_original") != rz.get("evento_carga") or y.get("evento_carga_original") not in EV): out.append(("I28", "%s: la cadena de reutilización de %s pierde el vínculo con el evento original de carga" % (cur, x)))
                if e is None: continue
                if e["org"] != y["org"] or e["org"] != org: out.append(("I25", "%s: el evento de reutilización de %s pertenece a otra organización" % (cur, x)))
                if e["pieza"] != y["pieza"] or e["pieza"] != s["v"].get(y["copy_version"], {}).get("pieza"): out.append(("I25", "%s: el evento de reutilización de %s pertenece a otra pieza" % (cur, x)))
                if e["actor"] != r or e.get("auth") != r: out.append(("I25", "%s: el evento de reutilización de %s identifica a otro actor" % (cur, x)))
                if e.get("campo") != "arte" or e.get("asset") != x: out.append(("I25", "%s: el evento de reutilización de %s no es del asset exacto" % (cur, x)))
                if e.get("asset_version") != y["version_asset"] or e.get("asset_version_id") != x: out.append(("I25", "%s: el evento de reutilización de %s referencia otra versión de asset (la versión del asset de destino no coincide)" % (cur, x)))
                if o is not None and y.get("origen_version_asset") != o["version_asset"]: out.append(("I25", "%s: el evento de reutilización de %s referencia otra versión de asset de origen" % (cur, x)))
                if e["version"] != y["copy_version"]: out.append(("I25", "%s: el evento de reutilización de %s no referencia la versión exacta de copy" % (cur, x)))
    for b in AT.values():
        if b["version"] != cur or b["rel"] != "heredada" or not b.get("asset"): continue
        p = AT.get(b.get("previo"))
        if p is None: out.append(("I26", "%s: la atribución heredada %s carece de antecesor verificable" % (cur, b["id"])))
        elif (p["persona"], p["evento"], p["org"], p["fuente"], p["campo"], p["origen_version"]) != (b["persona"], b["evento"], b["org"], b["fuente"], b["campo"], b["origen_version"]) or p.get("asset") not in cierre(b["asset"]):
            out.append(("I26", "%s: el antecesor de la atribución heredada %s no corresponde a su cadena" % (cur, b["id"])))
    return out
def _hall_cadena(s, cur, ids):
    """Auditor independiente de la cadena completa de procedencia (v14, H-03). Implementación propia, sin llamar al motor ni a su reconstrucción: para cada asset recorre TODOS los eslabones leyendo solo las tablas de la instantánea, arma para cada eslabón la fila
    esperada del evento propio y de la atribución directa y la compara campo por campo con los registros guardados. Un campo guardado nunca se acepta como prueba de sí mismo. Códigos: I28 estructura de la cadena (ausencia, ciclo, ambigüedad), I27 relación de reutilización, I23 y I24 carga y atribución."""
    out = []; T = s["assets"]; EV = s["ev"]; AT = s["at"]; MB = s["members"]; V = s["v"]; org = s["org"]; hechos = set()
    def hal(cod, x, msg): out.append((cod, "%s: [eslabón %s] %s" % (cur, x, msg)))
    def difs(real, esperado): return ["%s (esperado %s, hallado %s)" % (k, v, real.get(k)) for k, v in esperado.items() if real.get(k) != v]
    for aid in ids:
        x = aid; vis = []; eslabones = []; roto = False
        while True:
            if x not in T: hal("I28", vis[-1] if vis else aid, "referencia ausente: el asset %s referenciado no existe" % x); roto = True; break
            if x in vis: hal("I28", vis[-1], "ciclo: la referencia vuelve a %s" % x); roto = True; break
            vis.append(x); y = T[x]; tp = y["tipo"]; o, pv = y.get("origen"), y.get("previo"); eslabones.append(x)
            if tp == "reutilizado": sig, fin = o, False; falta = o is None; amb = pv is not None
            elif tp == "modificado": sig, fin = pv, False; falta = pv is None; amb = o is not None
            elif tp in ("nuevo", "sustituto"): sig, fin = None, True; falta = False; amb = o is not None or pv is not None
            else: hal("I28", x, "tipo de asset no válido (%s)" % tp); roto = True; break
            if amb: hal("I28", x, "cadena ambigua: declara más de una relación de origen"); roto = True
            if falta: hal("I28", x, "referencia ausente: el eslabón no declara su origen o versión anterior"); roto = True
            if roto or fin: break
            x = sig
        if roto: continue
        R = T[eslabones[-1]]; ue = R.get("evento_carga"); upl = R.get("uploader")
        ar = [b["id"] for b in AT.values() if b["rel"] == "directa" and b["fuente"] == "asset" and b.get("asset") == R["id"] and b["evento"] == ue and b["persona"] == upl
              and (b["org"], b["pieza"], b["version"], b.get("asset_version"), b["campo"]) == (R["org"], R["pieza"], R["copy_version"], R["version_asset"], "arte")]
        atr_raiz = ar[0] if len(ar) == 1 else None
        for k, x in enumerate(eslabones):
            if x in hechos: continue
            hechos.add(x); y = T[x]; tp = y["tipo"]
            if y["org"] != org: hal("I27", x, "el asset pertenece a otra organización")
            cvr = V.get(y.get("copy_version"))
            if cvr is None or cvr["pieza"] != y["pieza"]: hal("I27", x, "la pieza o la versión de copy del asset no existen o no coinciden")
            if tp in ("reutilizado", "modificado") and (y.get("uploader_original") != upl or y.get("evento_carga_original") != ue): hal("I28", x, "no conserva el uploader original ni el evento original de carga de la raíz %s" % R["id"])
            arte_ = (cvr or {}).get("campos", {}).get("arte")
            if arte_ is None or arte_.get("contenido") != x: hal("I27", x, "la versión de copy %s no usa este asset en el campo arte (esperado %s, hallado %s)" % (y.get("copy_version"), x, None if arte_ is None else arte_.get("contenido")))
            if tp in ("nuevo", "sustituto"):
                ev = EV.get(y.get("evento_carga")); act = y.get("uploader")
                if ev is None: hal("I23", x, "el evento original de carga no existe"); continue
                esp = dict(id=y.get("evento_carga"), tipo="asset_uploader", asset=x, asset_id=y["asset_id"], asset_version_id=x, asset_version=y["version_asset"], campo="arte", org=y["org"], pieza=y["pieza"], version=y["copy_version"], actor=act, auth=act)
                for d in difs(ev, esp): hal("I23", x, "el evento original de carga difiere del esperado: " + d)
            if tp == "reutilizado":
                o = T[y["origen"]]; ev = EV.get(y.get("evento_reutilizacion")); act = y.get("reutilizador")
                if ev is None: hal("I25", x, "el evento propio de reutilización no existe"); continue
                if [z for z, w in T.items() if w.get("evento_reutilizacion") == ev.get("id")] != [x]: hal("I25", x, "el evento propio de reutilización pertenece a otro asset o está compartido")
                if o["org"] != y["org"]: hal("I27", x, "el origen inmediato %s pertenece a otra organización" % o["id"])
                if y.get("origen_version_asset") != o["version_asset"]: hal("I27", x, "la versión de origen guardada en el asset no es la del origen inmediato")
                if (y.get("asset_id"), y.get("version_asset")) != (x, 1): hal("I27", x, "la fila del asset reutilizado no es la versión 1 de su propio linaje (esperado %s, hallado %s)" % ((x, 1), (y.get("asset_id"), y.get("version_asset"))))
                esp = dict(id=y.get("evento_reutilizacion"), asset=x, asset_id=y["asset_id"], asset_version_id=x, asset_version=y["version_asset"], campo="arte", org=y["org"], pieza=y["pieza"], version=y["copy_version"], actor=act, auth=act,
                           source_asset_id=o["asset_id"], source_asset_version_id=o["id"], source_asset_version=o["version_asset"], source_upload_event_id=ue, source_uploader_id=upl, source_attribution_id=atr_raiz, source_root_asset_id=R["asset_id"], source_root_asset_version_id=R["id"])
                for d in difs(ev, esp): hal("I27", x, "el evento propio de reutilización difiere del esperado: " + d)
                if ev.get("tipo") not in ("copy_author", "copy_editor"): hal("I27", x, "el evento propio no es de reutilización (%s)" % ev.get("tipo"))
                for d in difs(y, dict(source_asset_id=o["asset_id"], source_asset_version_id=o["id"], source_upload_event_id=ue, source_attribution_id=atr_raiz, source_root_asset_id=R["asset_id"], source_root_asset_version_id=R["id"])): hal("I27", x, "el asset guardado difiere de la reconstrucción: " + d)
                mm = MB.get(act)
                if mm is None or mm["org"] != y["org"] or not mm.get("activo"): hal("I25", x, "el reutilizador no es miembro activo de la organización")
                ds = [b for b in AT.values() if b["rel"] == "directa" and b["fuente"] == "copy" and b["evento"] == ev.get("id")]
                ex = [b for b in ds if b["persona"] == act and b.get("asset") == x and (b["org"], b["pieza"], b["version"], b["campo"]) == (y["org"], y["pieza"], y["copy_version"], "arte")]
                if y.get("material") and len(ex) != 1: hal("I24", x, "la atribución directa del reutilizador %s (duplicada o ausente: %d)" % (act, len(ex)))
                if len(ds) != len(ex) or (not y.get("material") and ds): hal("I24", x, "hay una atribución directa del evento de reutilización que no corresponde al reutilizador o al asset exactos")
            elif tp == "modificado":
                pv = T[y["previo"]]; ev = EV.get(y.get("evento_carga")); act = y.get("uploader")
                if (pv["asset_id"], pv["version_asset"] + 1, pv["org"], pv["pieza"]) != (y["asset_id"], y["version_asset"], y["org"], y["pieza"]): hal("I28", x, "la versión anterior no es la inmediata del mismo asset, organización y pieza")
                if ev is None: hal("I23", x, "el evento propio de carga de la versión no existe"); continue
                esp = dict(id=y.get("evento_carga"), tipo="asset_uploader", asset=x, asset_id=y["asset_id"], asset_version_id=x, asset_version=y["version_asset"], campo="arte", org=y["org"], pieza=y["pieza"], version=y["copy_version"], actor=act, auth=act)
                for d in difs(ev, esp): hal("I23", x, "el evento propio de carga difiere del esperado: " + d)
                mm = MB.get(act)
                if mm is None or mm["org"] != y["org"] or not mm.get("activo"): hal("I22", x, "el editor de la versión no es miembro activo de la organización")
                ds = [b for b in AT.values() if b["rel"] == "directa" and b["fuente"] == "asset" and b["evento"] == ev.get("id")]
                ex = [b for b in ds if b["persona"] == act and b.get("asset") == x and (b["org"], b["pieza"], b["version"], b["campo"]) == (y["org"], y["pieza"], y["copy_version"], "arte")]
                if len(ex) != 1 or len(ds) != len(ex): hal("I24", x, "la atribución directa del editor (duplicada, ausente o de otro asset)")
    return out
def cadena_identidad_independiente(s, aid):
    """Eslabones de identidad reconstruidos solo desde la instantánea (sin llamar al motor): misma estructura que Motor.cadena_identidad."""
    out = []; vis = []; x = aid; T = s["assets"]
    while x in T and x not in vis:
        vis.append(x); y = T[x]; t = y["tipo"]
        out.append((x, t, y["version_asset"], y["evento_carga"] if y.get("evento_carga") else y.get("source_upload_event_id"), y["uploader"] if y.get("uploader") else y.get("reutilizador"), y.get("evento_reutilizacion")))
        x = y.get("origen") if t == "reutilizado" else y.get("previo") if t == "modificado" else None
    return out
def _hall_arte_exactas(s, vid):
    out = []
    for raiz in _exactas(s, vid):
        for cur in _cad(s, raiz): out += _hall_arte(s, cur)
    return out
def _completa_campos(s, vid):
    for raiz in _exactas(s, vid):
        cur = raiz
        while cur is not None:
            if cur not in s["v"]: return False
            ver = s["v"][cur]
            for campo in ver["campos"]:
                if not any(a["version"] == cur and a["campo"] == campo for a in s["at"].values()): return False
            p = ver["prev"]
            if p in s["v"]:
                for aid in _activos(s):
                    a = s["at"][aid]
                    if a["version"] == p and not any(b["version"] == cur and b["linaje"] == a["linaje"] for b in s["at"].values()): return False
            cur = p
    return True
def _completa(s, vid): return _completa_campos(s, vid) and not _hall_arte_exactas(s, vid)
def _E(s, vid):
    out = set()
    for ver in _exactas(s, vid):
        for aid in _activos(s):
            if s["at"][aid]["version"] == ver: out.add(s["at"][aid]["persona"])
    return out
def _lin(s, aid):
    a = s["at"][aid]; return (a["persona"], a["fuente"], a["campo"], a["evento"])

def snapshot(m):
    return copy.deepcopy(dict(v=m.v, at=m.at, ev=m.ev, est=m.est, res=_plano(m.res), assets=m.assets, arte_decl=m.arte_decl, org=m.org, clas_hist=m.clas_hist, members=m.members, roles={k: sorted(x) for k, x in m.roles.items()}))

def validar_resolucion_independiente(s, sol):
    """Segunda implementación de las condiciones de 4.5 (V01 a V13) y de las reglas R1–R9. Recibe la solicitud y la instantánea previa (no usa el motor)."""
    r = sol; a = s["at"].get(r["atribucion"]); bad = []
    if not a: return ["V01"]
    ok = [("V02", a["persona"] == r["afectado"]), ("V03", (a["fuente"], a["org"]) == (r["fuente"], r["org"])), ("V04", a["pieza"] == r["pieza"]), ("V05", a["campo"] == r["campo"]),
          ("V06", r["version_evidencia"] == a["version"] and r["version_evidencia"] in s["v"] and _estado(s, a["id"]) == "activa"), ("V12", r.get("auth_uid") == r.get("resolutor")), ("V11", bool((r.get("evidencia") or "").strip()))]
    if r.get("previo") is not None:
        pr = s["res"].get(r["previo"]); ok.append(("V13", bool(pr) and pr["org"] == r["org"] and pr["atribucion"] == r["atribucion"] and pr["resultado"] == "rechazada"))
    mot = s["ev"].get(r["evento_motivador"])
    ok += [("V07", bool(mot) and mot["campo"] == r["campo"]), ("V08", bool(r.get("actor_cambio")) and bool(mot) and mot["actor"] == r["actor_cambio"]), ("V09", bool(r.get("solicitante")) and r["solicitante"] in s["members"])]
    bad = [k for k, v in ok if not v]
    u = r["resolutor"]; mem = s["members"].get(u); campo = r["campo"]; actual = r["version_evidencia"]
    perms = set(s["roles"].get(mem["rol"], [])) if mem else set()
    reglas = {"R1": bool(mem) and mem["org"] == r["org"] and mem["activo"], "R2": "piece.review" in perms, "R3": u != r["afectado"], "R4": u != r.get("solicitante"), "R5": u != r.get("actor_cambio")}
    cadena = []; cur = actual
    while cur in s["v"] and cur not in cadena: cadena.append(cur); cur = s["v"][cur]["prev"]
    reglas["R6"] = not any(e["actor"] == u and e["campo"] == campo and e["version"] in cadena for e in s["ev"].values())
    reglas["R7"] = not any(a_["persona"] == u and a_["campo"] == campo and a_["rel"] == "heredada" and a_["version"] == actual and _estado(s, a_["id"]) == "activa" for a_ in s["at"].values())
    reglas["R8"] = not any(a_["persona"] == u and a_["version"] in set(_exactas(s, actual)) - {actual} for a_ in s["at"].values())
    reglas["R9"] = not (any(a_["persona"] == u and a_["campo"] == campo and a_["version"] == actual and _estado(s, a_["id"]) == "activa" for a_ in s["at"].values()) or any(e["actor"] == u and e["op"] == (mot or {}).get("op") for e in s["ev"].values()))
    return bad + [k for k, v in reglas.items() if not v]

def _v_sin_arte_nuevo(v1, v0, op):
    """True si la versión cambió. La única adición permitida a una versión existente es el campo arte, y solo al registrar un asset."""
    if v1 == v0: return False
    if op == "registrar_asset" and v1 is not None and "arte" not in v0["campos"] and "arte" in v1["campos"]:
        v1 = dict(v1, campos={k: c for k, c in v1["campos"].items() if k != "arte"}); return v1 != v0
    return True

def auditar(antes, despues, desc):
    """Compara dos instantáneas y devuelve los códigos de invariante violados (I1 a I12). desc describe la operación ejecutada."""
    cod = []; op = desc["op"]; a0, a1 = _activos(antes), _activos(despues)
    # I10: nada anterior se reescribe ni desaparece (solo se agrega)
    if any(_v_sin_arte_nuevo(despues["v"].get(k), x, desc["op"]) for k, x in antes["v"].items()) or any(despues["at"].get(k) != x for k, x in antes["at"].items()) or any(despues["ev"].get(k) != x for k, x in antes["ev"].items()) or despues["est"][:len(antes["est"])] != antes["est"]:
        cod.append(("I10", "una versión, atribución, evento o estado anterior fue modificado o eliminado"))
    if any(despues["assets"].get(k) != x for k, x in antes["assets"].items()) or any(despues["arte_decl"].get(k) != x for k, x in antes["arte_decl"].items()):
        cod.append(("I10", "un asset o una declaración de arte anterior fue modificado o eliminado"))
    cod += _auditar_resoluciones(antes, despues)
    # I6: la evidencia histórica se conserva
    if any(k not in despues["at"] for k in antes["at"]) or len(despues["est"]) < len(antes["est"]) or any(k not in despues["assets"] for k in antes["assets"]): cod.append(("I6", "una atribución, un asset o un registro histórico desapareció de la evidencia"))
    if op in ("introducir", "modificar", "sustituir", "eliminar", "sin_cambio"):
        n, p = desc["nueva"], desc["prev"]
        l0 = {_lin(antes, a) for a in a0 if antes["at"][a]["version"] == p}; l1 = {_lin(despues, a) for a in a1 if despues["at"][a]["version"] == n}
        if not l0 <= l1: cod.append(("I1", "una atribución activa anterior no sigue activa en la versión nueva: %s" % sorted(l0 - l1)[:2]))
        if despues["v"].get(n) and p in despues["v"]:
            esperadas = {antes["at"][a]["linaje"] for a in a0 if antes["at"][a]["version"] == p}
            if not esperadas <= {b["linaje"] for b in despues["at"].values() if b["version"] == n}: cod.append(("I10", "la versión nueva no hereda todas las atribuciones activas"))
        directas = [b for b in despues["at"].values() if b["version"] == n and b["rel"] == "directa" and b["persona"] == desc["actor"] and b["campo"] == desc.get("campo") and b["id"] not in antes["at"]]
        debe = op in ("introducir", "modificar", "sustituir") or (op == "eliminar" and desc.get("material", True))
        if debe and not directas: cod.append(("I2", "el actor no se incorporó"))
        if (not debe) and any(b["version"] == n and b["rel"] == "directa" and b["id"] not in antes["at"] and b["persona"] == desc["actor"] for b in despues["at"].values()): cod.append(("I2", "el actor se incorporó sin contribución material"))
        nuevos_estados = despues["est"][len(antes["est"]):]
        if any(e["estado"] == "historica" for e in nuevos_estados): cod.append(("I1", "una operación de contenido retiró atribuciones"))
    if op == "clasificar":
        if a0 != a1 or despues["est"] != antes["est"] or set(despues["at"]) != set(antes["at"]): cod.append(("I12", "el cambio de clasificación alteró atribuciones o estados"))
        if despues["clas_hist"][:len(antes["clas_hist"])] != antes["clas_hist"] or len(despues["clas_hist"]) != len(antes["clas_hist"]) + 1: cod.append(("I12", "el cambio de clasificación no se registró como historial nuevo"))
    if op in ("aplicar_resolucion", "rechazar_resolucion"):
        rid = desc["res"]; sol = desc["sol"]
        if rid in antes["res"] or rid not in despues["res"]: cod.append(("I13", "la resolución %s no quedó como registro nuevo" % rid)); return cod
        r = despues["res"][rid]; recalc = validar_resolucion_independiente(antes, sol); valido = not recalc
        acept = r["resultado"] == "aceptada"; ref = r["atribucion"]; ev_ = desc["vid"]
        if acept and not valido: cod.append(("I4", "una resolución aceptada incumple sus condiciones: %s" % recalc[:3]))
        if op == "aplicar_resolucion" and not acept and set(r.get("motivos", [])) != set(recalc): cod.append(("I4", "los motivos de rechazo del motor %s difieren de los recalculados por el auditor %s" % (sorted(r.get("motivos", [])), sorted(recalc))))
        if (not acept) or (not valido):
            if a0 != a1 or despues["est"] != antes["est"] or _E(antes, ev_) != _E(despues, ev_) or desc.get("E0") != desc.get("E1"): cod.append(("I5", "una resolución rechazada o inválida modificó atribuciones o E"))
        if acept and valido:
            if a0 - a1 != {ref} or (a1 - a0): cod.append(("I3", "la resolución retiró %s en lugar de solo la referenciada" % sorted(a0 - a1)[:3]))
            if _estado(despues, ref) != "historica" or r.get("evidencia_historica") is None: cod.append(("I6", "la atribución resuelta no queda como histórica con evidencia"))
            persona = antes["at"][ref]["persona"]; resto = {antes["at"][a]["persona"] for a in a0 if a != ref and antes["at"][a]["version"] in _exactas(antes, ev_)}
            if not resto <= _E(despues, ev_): cod.append(("I7", "salió de E una persona que conserva otra atribución activa"))
            if persona in resto and persona not in _E(despues, ev_): cod.append(("I7", "la persona con otra atribución activa salió de E"))
    return cod

def _sello_ind(r):
    """Recalcula el sello de una fila a partir de su contenido (implementación propia del auditor)."""
    return hashlib.sha256(json.dumps({k: v for k, v in r.items() if k != "sello"}, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()

def _auditar_resoluciones(antes, despues):
    """I13 inmutabilidad, I14 cadena de reconsideraciones, I15 correspondencia entre resolución y atribución exacta. Se evalúa en cada operación."""
    cod = []; R0, R1 = antes["res"], despues["res"]
    for k, r0 in R0.items():
        r1 = R1.get(k)
        if r1 is None: cod.append(("I13", "la resolución histórica %s fue eliminada" % k)); continue
        if r1 != r0:
            dif = sorted(f for f in set(r0) | set(r1) if r0.get(f) != r1.get(f))
            cod.append(("I13", "la resolución %s fue %s (campos: %s)" % (k, "reemplazada con el mismo ID" if r0.get("seq") != r1.get("seq") else "modificada", ", ".join(dif))))
    for k, r in R1.items():
        if r.get("sello") != _sello_ind(r): cod.append(("I13", "el sello de la resolución %s no coincide con su contenido" % k))
        if r["resultado"] not in ("aceptada", "rechazada"): cod.append(("I13", "la resolución %s tiene un resultado no definitivo (%s)" % (k, r["resultado"])))
    # I14: cadena de reconsideraciones
    for k, r in R1.items():
        p = r.get("previo")
        if p is None: continue
        pr = R1.get(p); vis = [k]; q = p
        while q is not None and q in R1 and q not in vis: vis.append(q); q = R1[q].get("previo")
        if q in vis: cod.append(("I14", "la cadena de reconsideraciones de %s contiene un ciclo" % k))
        if pr is None: cod.append(("I14", "la cadena de %s referencia un registro anterior inexistente (%s)" % (k, p))); continue
        if pr["atribucion"] != r["atribucion"] or pr["org"] != r["org"]: cod.append(("I14", "la cadena de %s referencia un registro de otra atribución u organización" % k))
        if pr["seq"] >= r["seq"]: cod.append(("I14", "el registro anterior de %s no es anterior en el tiempo" % k))
        if r.get("previo_sello") != pr["sello"] or r.get("previo_sello") != _sello_ind(pr): cod.append(("I14", "el sello del registro anterior de %s no coincide con el contenido actual (el anterior fue alterado)" % k))
        if pr["resultado"] != "rechazada": cod.append(("I14", "la reconsideración %s se apoya en una resolución que no fue rechazada" % k))
    # I15: cada baja cita una resolución aceptada de esa atribución exacta, y cada resolución aceptada tiene su baja
    bajas = [e for e in despues["est"] if e["estado"] == "historica"]
    for e in bajas:
        r = R1.get(e.get("resolucion"))
        if r is None or r["resultado"] != "aceptada" or r["atribucion"] != e["atr"]: cod.append(("I15", "la baja de %s cita la resolución %s, que no existe, no fue aceptada o no corresponde a esa atribución" % (e["atr"], e.get("resolucion"))))
    for k, r in R1.items():
        if r["resultado"] == "aceptada" and sum(1 for e in bajas if e.get("resolucion") == k and e["atr"] == r["atribucion"]) != 1: cod.append(("I15", "la resolución aceptada %s no tiene exactamente una baja registrada para su atribución" % k))
    for atr in {e["atr"] for e in despues["est"]}:
        seq_ = [e["estado"] for e in despues["est"] if e["atr"] == atr]
        if "historica" in seq_ and "activa" in seq_[seq_.index("historica"):]: cod.append(("I15", "la atribución histórica %s volvió a activa sin una resolución: una baja resuelta no se reactiva" % atr))
    for atr in {r["atribucion"] for r in R1.values() if r["resultado"] == "aceptada"}:
        if sum(1 for r in R1.values() if r["atribucion"] == atr and r["resultado"] == "aceptada") > 1: cod.append(("I15", "la atribución %s tiene más de una resolución aceptada" % atr))
    return cod

def _arte_personas(s, vid):
    return {s["at"][a]["persona"] for a in _activos(s) if s["at"][a].get("asset") and s["at"][a]["version"] in _exactas(s, vid)}

def auditar_E(estado, resultado, vid):
    """I7/I8: el E del motor debe coincidir con el E recalculado y no presentarse completo con procedencia incompleta (campos o arte).
    I16 a I19: corrupción registrada en la procedencia del arte. I20: arte incompleto con E completo. I21: contribuyentes del arte ausentes de E."""
    cod = []; h = _hall_arte_exactas(estado, vid); comp = _completa_campos(estado, vid) and not h
    if not comp and (resultado.get("completa") or resultado.get("E") is not None):
        cod.append(("I8", "procedencia incompleta presentada como completa o con E parcial"))
        if h: cod.append(("I20", "la procedencia del arte es incompleta pero el motor declara E completo: %s" % h[0][1]))
    cod += [x for x in h if x[0] in ("I16", "I17", "I18", "I19", "I22", "I23", "I24", "I25", "I26", "I27", "I28") or (x[0] == "I20" and "registra arte o un asset" in x[1])]
    if comp:
        if not resultado.get("completa") or set((resultado.get("E") or {}).keys()) != _E(estado, vid): cod.append(("I7", "E del motor distinto del E recalculado sobre las atribuciones reales"))
        if resultado.get("completa") and not _arte_personas(estado, vid) <= set(resultado.get("E") or {}): cod.append(("I21", "E omite a un contribuyente del arte: %s" % sorted(_arte_personas(estado, vid) - set(resultado.get("E") or {}))))
    return cod

class Ejecucion:
    """Ejecuta operaciones del motor y audita cada paso con el auditor independiente."""
    def __init__(self, motor): self.m = motor; self.viol = []; self.pasos = []
    def op(self, nombre, fn, **desc):
        res_op = nombre in ("aplicar_resolucion", "rechazar_resolucion")
        if res_op: desc["E0"] = self._eset(desc["vid"]); desc["sol"] = copy.deepcopy(self.m.solicitudes[desc["res"]])
        a = snapshot(self.m); r = fn(); b = snapshot(self.m)
        if res_op: desc["E1"] = self._eset(desc["vid"])
        v = auditar(a, b, dict(op=nombre, **desc)); self.viol += v; self.pasos.append((nombre, [x[0] for x in v])); return r
    def _eset(self, vid):
        r = self.m.calcular_E(vid); return None if r.get("E") is None else frozenset(r["E"])
    def E(self, vid):
        r = self.m.calcular_E(vid); self.viol += auditar_E(snapshot(self.m), r, vid); return r

def _res(m, rid, atr, resolutor, solicitante="Q", motivador=None, evidencia="El texto vigente ya no contiene la propuesta original de la persona afectada", version=None, auth=None, actor_cambio=None, campo=None, previo=None, motivo="El contenido cambió materialmente"):
    a = m.at[atr]; mot = motivador or [e["id"] for e in m.ev.values() if e["campo"] == a["campo"]][-1]
    return m.solicitar_resolucion(rid, org=m.org, atribucion=atr, afectado=a["persona"], fuente=a["fuente"], pieza=a["pieza"], campo=campo or a["campo"], version_evidencia=version or a["version"], evento_motivador=mot,
                                  actor_cambio=actor_cambio or m.ev[mot]["actor"], solicitante=solicitante, resolutor=resolutor, auth_uid=auth or resolutor, evidencia=evidencia, motivo=motivo, previo=previo)

def _base(cls=Motor):
    m = cls()
    for u, r in (("A", "editor"), ("B", "editor"), ("C", "editor"), ("D", "editor"), ("W", "editor"), ("Z", "editor"), ("Pm", "editor"), ("U", "editor"), ("Q", "revisor"), ("R", "revisor"), ("R2", "revisor"), ("Adm", "admin")): m.miembro(u, r)
    return m, Ejecucion(m)

def _lin_activos(m, vid): return sorted((a["persona"], a["campo"], a["fuente"]) for a in m.activas(vid))

# =====================================================================================================
# Escenarios estructurales A–L (datos ficticios, ejecutados sobre el motor y auditados paso a paso)
# =====================================================================================================
def _a_headline(m, x, v="v2"):
    return [a["id"] for a in m.at.values() if a["version"] == v and a["persona"] == "A" and a["campo"] == "headline"][0]

def esc_A(cls=Motor):
    m, x = _base(cls)
    x.op("introducir", lambda: m.introducir_campo("copy", None, "v1", "headline", "Compra hoy", "A", pieza="P1", arte="no_aplica"), prev=None, nueva="v1", actor="A", campo="headline")
    x.op("sustituir", lambda: m.sustituir_campo("copy", "v1", "v2", "headline", "Oferta nueva", "B"), prev="v1", nueva="v2", actor="B", campo="headline")
    e = x.E("v2"); asr = [("E tras la sustitución contiene a A y a B", ["A", "B"], sorted(e["E"] or {}))]
    asr.append(("la atribución de A sigue activa tras la sustitución", "activa", m.estado(_a_headline(m, x))))
    r = _res(m, "r1", _a_headline(m, x), "R", motivador=[k for k, ev in m.ev.items() if ev["actor"] == "B"][0])
    ok = x.op("aplicar_resolucion", lambda: m.aplicar_resolucion("r1"), res="r1", vid="v2")
    e2 = x.E("v2"); asr += [("resolución independiente válida aceptada", True, ok), ("E tras la resolución es solo B", ["B"], sorted(e2["E"] or {})), ("la atribución de A queda histórica", "historica", m.estado(_a_headline(m, x)))]
    return m, x, asr

def esc_B(cls=Motor):
    m, x = _base(cls)
    x.op("introducir", lambda: m.introducir_campo("copy", None, "v1", "headline", "Compra hoy", "A", pieza="P1", arte="no_aplica"), prev=None, nueva="v1", actor="A", campo="headline")
    x.op("eliminar", lambda: m.eliminar_campo("copy", "v1", "v2", "headline", "B", True), prev="v1", nueva="v2", actor="B", campo="headline", material=True)
    e = x.E("v2"); a = [a for a in m.at.values() if a["version"] == "v2" and a["persona"] == "A"][0]
    asr = [("E tras la eliminación contiene a A y a B", ["A", "B"], sorted(e["E"] or {})), ("A permanece activa provisionalmente", "activa", m.estado(a["id"])),
           ("B se incorpora con atribución directa", True, any(b["persona"] == "B" and b["rel"] == "directa" for b in m.at.values() if b["version"] == "v2")),
           ("el campo eliminado conserva su historial", True, m.v["v1"]["campos"]["headline"]["contenido"] == "Compra hoy" and m.v["v2"]["campos"]["headline"]["eliminado"])]
    x.op("eliminar", lambda: m.eliminar_campo("copy", "v2", "v3", "headline", "C", False), prev="v2", nueva="v3", actor="C", campo="headline", material=False)
    asr.append(("una eliminación no material no incorpora al actor", False, any(b["persona"] == "C" for b in m.at.values())))
    return m, x, asr

def _esc_dos_campos(cls):
    m, x = _base(cls)
    x.op("introducir", lambda: m.introducir_campo("copy", None, "v1", "headline", "Compra hoy", "A", pieza="P1", arte="no_aplica"), prev=None, nueva="v1", actor="A", campo="headline")
    x.op("introducir", lambda: m.introducir_campo("copy", "v1", "v2", "body", "Cuerpo", "A"), prev="v1", nueva="v2", actor="A", campo="body")
    x.op("sustituir", lambda: m.sustituir_campo("copy", "v2", "v3", "headline", "Oferta nueva", "B"), prev="v2", nueva="v3", actor="B", campo="headline")
    return m, x

def esc_C(cls=Motor):
    m, x = _esc_dos_campos(cls); a = _a_headline(m, x, "v3")
    _res(m, "r1", a, "R", motivador=[k for k, ev in m.ev.items() if ev["actor"] == "B"][0])
    ok = x.op("aplicar_resolucion", lambda: m.aplicar_resolucion("r1"), res="r1", vid="v3"); e = x.E("v3")
    asr = [("la resolución válida se acepta", True, ok), ("la atribución de headline de A pasa a histórica", "historica", m.estado(a)),
           ("A permanece en E por su atribución activa de body", True, "A" in (e["E"] or {})), ("la atribución de body sigue activa", True, any(b["persona"] == "A" and b["campo"] == "body" and m.estado(b["id"]) == "activa" for b in m.at.values() if b["version"] == "v3"))]
    return m, x, asr

def esc_D(cls=Motor):
    m, x = _base(cls)
    x.op("introducir", lambda: m.introducir_campo("brief", None, "bv1", "commercial_offer", "Oferta del brief", "A", pieza="P1", arte="no_aplica"), prev=None, nueva="bv1", actor="A", campo="commercial_offer")
    x.op("introducir", lambda: m.introducir_campo("copy", None, "cv1", "headline", "Compra hoy", "A", pieza="P1", arte="no_aplica", refs={"brief": "bv1"}), prev=None, nueva="cv1", actor="A", campo="headline")
    x.op("sustituir", lambda: m.sustituir_campo("copy", "cv1", "cv2", "headline", "Oferta nueva", "B"), prev="cv1", nueva="cv2", actor="B", campo="headline")
    a = _a_headline(m, x, "cv2"); _res(m, "r1", a, "R", motivador=[k for k, ev in m.ev.items() if ev["actor"] == "B"][0])
    ok = x.op("aplicar_resolucion", lambda: m.aplicar_resolucion("r1"), res="r1", vid="cv2"); e = x.E("cv2")
    asr = [("la resolución del copy se acepta", True, ok), ("la atribución del copy pasa a histórica", "historica", m.estado(a)),
           ("A permanece en E por el brief", True, "A" in (e["E"] or {})), ("la atribución de A en el brief sigue activa", True, any(b["persona"] == "A" and b["fuente"] == "brief" and m.estado(b["id"]) == "activa" for b in m.at.values()))]
    return m, x, asr

def _preparar_A(cls, tipo_res):
    m, x = _base(cls)
    x.op("introducir", lambda: m.introducir_campo("copy", None, "v1", "headline", "Compra hoy", "A", pieza="P1", arte="no_aplica"), prev=None, nueva="v1", actor="A", campo="headline")
    x.op("sustituir", lambda: m.sustituir_campo("copy", "v1", "v2", "headline", "Oferta nueva", "B"), prev="v1", nueva="v2", actor="B", campo="headline")
    return m, x

def esc_E(cls=Motor):
    m, x = _preparar_A(cls, "rechazada"); a = _a_headline(m, x); e0 = x.E("v2")
    _res(m, "r1", a, "R", motivador=[k for k, ev in m.ev.items() if ev["actor"] == "B"][0])
    x.op("rechazar_resolucion", lambda: m.rechazar_resolucion("r1", ["evidencia insuficiente según el revisor"]), res="r1", vid="v2"); e1 = x.E("v2")
    asr = [("la resolución rechazada no cambia la atribución", "activa", m.estado(a)), ("E no cambia", sorted(e0["E"]), sorted(e1["E"])), ("el resultado de la resolución es rechazada y definitivo", "rechazada", m.res["r1"]["resultado"])]
    return m, x, asr

def esc_F(cls=Motor):
    m, x = _preparar_A(cls, "inválida"); a = _a_headline(m, x); e0 = x.E("v2")
    _res(m, "r1", a, "R", motivador=[k for k, ev in m.ev.items() if ev["actor"] == "B"][0], version="v1")
    ok = x.op("aplicar_resolucion", lambda: m.aplicar_resolucion("r1"), res="r1", vid="v2"); e1 = x.E("v2")
    asr = [("la resolución con evidencia de otra versión no se aplica", False, ok), ("la atribución permanece activa", "activa", m.estado(a)), ("E no cambia", sorted(e0["E"]), sorted(e1["E"]))]
    return m, x, asr

def esc_G(cls=Motor):
    m, x = _base(cls)
    x.op("introducir", lambda: m.introducir_campo("copy", None, "v1", "headline", "Compra hoy", "A", pieza="P1", arte="no_aplica"), prev=None, nueva="v1", actor="A", campo="headline")
    x.op("introducir", lambda: m.introducir_campo("copy", "v1", "v2", "body", "Cuerpo", "B"), prev="v1", nueva="v2", actor="B", campo="body")
    x.op("sin_cambio", lambda: m.version_sin_cambio("copy", "v2", "v3", "C"), prev="v2", nueva="v3", actor="C")
    x.op("sin_cambio", lambda: m.version_sin_cambio("copy", "v3", "v4", "D"), prev="v3", nueva="v4", actor="D")
    e = x.E("v4"); lin = sorted((a["persona"], a["campo"], a["rel"]) for a in m.activas("v4"))
    asr = [("v4 conserva las atribuciones activas de A y B como heredadas", [("A", "headline", "heredada"), ("B", "body", "heredada")], lin), ("quien crea una versión sin cambio no se incorpora", False, "C" in (e["E"] or {}) or "D" in (e["E"] or {})),
           ("todas las atribuciones anteriores siguen existiendo", True, all(k in m.at for k in list(m.at)))]
    return m, x, asr

def esc_H(cls=Motor):
    m, x = _base(cls)
    x.op("introducir", lambda: m.introducir_campo("copy", None, "v1", "headline", "Compra hoy", "A", pieza="P1", arte="no_aplica"), prev=None, nueva="v1", actor="A", campo="headline")
    m.v["vx"] = dict(id="vx", fuente="copy", pieza="P1", prev=None, campos={"headline": dict(contenido="importada", clasif="introducido", eliminado=False)}, refs={}, autor=None, seq=m.tick())
    e = x.E("vx"); e1 = x.E("v1")
    asr = [("la versión importada sin evidencia no produce un E completo", False, e["completa"]), ("no se entrega un E parcial", None, e["E"]), ("la versión con procedencia sí produce E", ["A"], sorted(e1["E"]))]
    return m, x, asr

def esc_I(cls=Motor):
    m, x = _base(cls)
    x.op("introducir", lambda: m.introducir_campo("copy", None, "v1", "headline", "Compra hoy", "A", pieza="P1", arte="no_aplica"), prev=None, nueva="v1", actor="A", campo="headline")
    x.op("modificar", lambda: m.modificar_campo("copy", "v1", "v2", "headline", "Compra hoy y ahorra", "B"), prev="v1", nueva="v2", actor="B", campo="headline")
    e0 = x.E("v2"); h = len(m.clas_hist)
    x.op("clasificar", lambda: m.cambiar_clasificacion("v2", "headline", "sustituido", "Q"), vid="v2")
    e1 = x.E("v2")
    asr = [("la clasificación cambia", "sustituido", m.clasif_actual("v2", "headline")), ("E no cambia", sorted(e0["E"]), sorted(e1["E"])), ("la historia se conserva y se agrega un registro", h + 1, len(m.clas_hist)),
           ("ninguna atribución quedó histórica", True, all(m.estado(a) == "activa" for a in m.at))]
    return m, x, asr

def esc_J(cls=Motor):
    m, x = _base(cls)
    x.op("introducir", lambda: m.introducir_campo("copy", None, "cv1", "headline", "Compra hoy", "A", pieza="P1", arte="con_arte"), prev=None, nueva="cv1", actor="A", campo="headline")
    m.registrar_asset("a1", "cv1", "A")
    x.op("sustituir", lambda: m.sustituir_campo("copy", "cv1", "cv2", "headline", "Oferta nueva", "B"), prev="cv1", nueva="cv2", actor="B", campo="headline")
    a = _a_headline(m, x, "cv2"); _res(m, "r1", a, "R", motivador=[k for k, ev in m.ev.items() if ev["actor"] == "B"][0])
    ok = x.op("aplicar_resolucion", lambda: m.aplicar_resolucion("r1"), res="r1", vid="cv2"); e = x.E("cv2")
    asr = [("la resolución se acepta", True, ok), ("la atribución de headline de A queda histórica", "historica", m.estado(a)), ("A permanece en E por su carga del asset", True, "A" in (e["E"] or {})),
           ("la atribución de asset de A sigue activa", True, any(b["persona"] == "A" and b["fuente"] == "asset" and m.estado(b["id"]) == "activa" for b in m.at.values() if b["version"] == "cv2"))]
    return m, x, asr

def esc_K(cls=Motor):
    m, x = _base(cls)
    x.op("introducir", lambda: m.introducir_campo("brief", None, "bv", "commercial_offer", "Oferta", "C", pieza="P1", arte="no_aplica"), prev=None, nueva="bv", actor="C", campo="commercial_offer")
    x.op("introducir", lambda: m.introducir_campo("promotion", None, "ps", "discount", "20%", "Pm", pieza="P1", arte="no_aplica"), prev=None, nueva="ps", actor="Pm", campo="discount")
    x.op("introducir", lambda: m.introducir_campo("copy", None, "cvm", "headline", "Compra hoy", "A", pieza="P1", arte="con_arte"), prev=None, nueva="cvm", actor="A", campo="headline")
    m.registrar_asset("a1", "cvm", "U")
    x.op("introducir", lambda: m.introducir_campo("copy", None, "ca", "headline", "Adaptación", "W", pieza="P2", arte="con_arte", refs={"brief": "bv", "promotion": "ps", "master": "cvm"}), prev=None, nueva="ca", actor="W", campo="headline")
    m.registrar_asset("a2", "ca", "W", reused_from="a1")
    e = x.E("ca"); reut = [a for a in m.at.values() if a["version"] == "ca" and a["fuente"] == "asset"][0]
    asr = [("E de la adaptación incorpora copy, brief, promoción, asset y maestra", ["A", "C", "Pm", "U", "W"], sorted(e["E"] or {})), ("quien reutiliza el asset (W) no es el uploader del asset", "U", reut["persona"]),
           ("el asset reutilizado conserva el evento del uploader original", True, m.ev[reut["evento"]]["actor"] == "U")]
    return m, x, asr

def esc_L(cls=Motor):
    m, x = _preparar_A(cls, "sin elegible"); a = _a_headline(m, x); m.roles["revisor"] = set()
    r = _res(m, "r1", a, "R", motivador=[k for k, ev in m.ev.items() if ev["actor"] == "B"][0])
    elegibles = resolutores_elegibles(m, m.solicitudes["r1"])
    ok = x.op("aplicar_resolucion", lambda: m.aplicar_resolucion("r1"), res="r1", vid="v2"); e = x.E("v2")
    asr = [("no existe resolutor elegible", [], elegibles), ("la resolución no se aplica", False, ok), ("la atribución permanece activa", "activa", m.estado(a)), ("E no excluye a A", True, "A" in (e["E"] or {}))]
    return m, x, asr

ESCENARIOS = [("A", "conservación por sustitución", esc_A), ("B", "conservación por eliminación", esc_B), ("C", "varias atribuciones de una persona", esc_C), ("D", "varias fuentes", esc_D),
              ("E", "resolución rechazada", esc_E), ("F", "resolución inválida por evidencia de otra versión", esc_F), ("G", "herencia", esc_G), ("H", "cadena incompleta", esc_H),
              ("I", "clasificación modificada", esc_I), ("J", "resolución y contribución independiente", esc_J), ("K", "fuentes paralelas", esc_K), ("L", "sin resolutor elegible", esc_L)]

# ---- uniformidad entre fuentes (I9) y metamorfismo de similitud (I11) ----
def _firma(m):
    return [(vid, sorted((a["persona"], a["campo"], a["rel"], m.estado(a["id"])) for a in m.at.values() if a["version"] == vid), sorted((c, d["clasif"], d["eliminado"]) for c, d in v["campos"].items()),
             sorted(e["motivo"].split(" de ")[0] for e in m.est if m.at[e["atr"]]["version"] == vid)) for vid, v in sorted(m.v.items())]
def uniformidad(cls=Motor):
    firmas = {}
    for f in ("copy", "brief", "promotion"):
        m, x = _base(cls)
        x.op("introducir", lambda: m.introducir_campo(f, None, "v1", "f1", "texto uno", "A", pieza="P1", arte="no_aplica"), prev=None, nueva="v1", actor="A", campo="f1")
        x.op("modificar", lambda: m.modificar_campo(f, "v1", "v2", "f1", "texto dos", "B"), prev="v1", nueva="v2", actor="B", campo="f1")
        x.op("sustituir", lambda: m.sustituir_campo(f, "v2", "v3", "f1", "otro texto", "C"), prev="v2", nueva="v3", actor="C", campo="f1")
        x.op("eliminar", lambda: m.eliminar_campo(f, "v3", "v4", "f1", "D", True), prev="v3", nueva="v4", actor="D", campo="f1", material=True)
        firmas[f] = _firma(m)
    return firmas, ([] if firmas["copy"] == firmas["brief"] == firmas["promotion"] else [("I9", "las fuentes no aplican la misma regla")])
def metamorfico(cls=Motor):
    firmas = []
    for nuevo in ("Compra hoy con 20% de descuento en toda la tienda", "Zapatos de piel hechos a mano"):
        m, x = _base(cls)
        x.op("introducir", lambda: m.introducir_campo("copy", None, "v1", "headline", "Compra hoy con 25% de descuento en toda la tienda", "A", pieza="P1", arte="no_aplica"), prev=None, nueva="v1", actor="A", campo="headline")
        x.op("sustituir", lambda: m.sustituir_campo("copy", "v1", "v2", "headline", nuevo, "B"), prev="v1", nueva="v2", actor="B", campo="headline")
        firmas.append(sorted((a["persona"], a["campo"], a["rel"], m.estado(a["id"])) for a in m.at.values() if a["version"] == "v2"))
    return firmas, ([] if firmas[0] == firmas[1] else [("I11", "el resultado sobre las atribuciones depende de la similitud del texto")])
def conformidad_tabla(P_clas):
    """Observa en el motor, por fuente y clasificación, si conserva todas las atribuciones activas y si incorpora al actor; compara con la tabla C de 4.4.10."""
    nombres = {"brief": "brief", "promoción": "promotion", "copy": "copy"}; dif = []
    for fila in P_clas:
        f = nombres[fila["fuente"]]; c = fila["clas"]; m, x = _base()
        m.introducir_campo(f, None, "v1", "f1", "uno", "A", pieza="P1", arte="no_aplica"); fn = {"sin_cambio": lambda: m.version_sin_cambio(f, "v1", "v2", "X"), "introducido": lambda: m.introducir_campo(f, "v1", "v2", "f2", "dos", "X"),
            "modificado": lambda: m.modificar_campo(f, "v1", "v2", "f1", "tres", "X"), "sustituido": lambda: m.sustituir_campo(f, "v1", "v2", "f1", "cuatro", "X"), "eliminado": lambda: m.eliminar_campo(f, "v1", "v2", "f1", "X", True)}[c]
        fn(); act = m.activas("v2")
        cons = "todas" if any(a["persona"] == "A" and a["campo"] == "f1" for a in act) else "ninguna"; inc = "sí" if any(a["persona"] == "X" and a["rel"] == "directa" for a in act) else "no"
        if (cons, inc) != (fila["conserva"], fila["incorpora"]): dif.append((fila["fuente"], c, (cons, inc), (fila["conserva"], fila["incorpora"])))
    return dif

# =====================================================================================================
# Mutaciones K47: cada una sustituye UNA operación del motor por una variante defectuosa
# =====================================================================================================
def _retirar(m, atrs, motivo="defecto inyectado"):
    for a in atrs: m.est.append(dict(seq=m.tick(), atr=a, estado="historica", resolucion=None, motivo=motivo))

class M01(Motor):
    def sustituir_campo(s, fuente, prev, nueva, campo, contenido, actor):
        r = super().sustituir_campo(fuente, prev, nueva, campo, contenido, actor); _retirar(s, [a["id"] for a in s.activas(nueva) if a["campo"] == campo and a["rel"] == "heredada"]); return r
class M02(Motor):
    def eliminar_campo(s, fuente, prev, nueva, campo, actor, material=True):
        r = super().eliminar_campo(fuente, prev, nueva, campo, actor, material); _retirar(s, [a["id"] for a in s.activas(nueva) if a["campo"] == campo and a["rel"] == "heredada"]); return r
class M03(Motor):
    def modificar_campo(s, fuente, prev, nueva, campo, contenido, actor):
        r = super().modificar_campo(fuente, prev, nueva, campo, contenido, actor); _retirar(s, [a["id"] for a in s.activas(nueva) if a["campo"] == campo and a["rel"] == "heredada"][:1]); return r
class M04(Motor):
    def introducir_campo(s, fuente, prev, nueva, campo, contenido, actor, pieza=None, refs=None, arte=None):
        pieza = pieza or (s.v[prev]["pieza"] if prev else "P1"); s._nueva(fuente, prev, nueva, pieza, refs or (s.v[prev]["refs"] if prev else None), actor, arte)
        s.v[nueva]["campos"][campo] = dict(contenido=contenido, clasif="introducido", eliminado=False); s.clas_hist.append((nueva, campo, "introducido")); s._evento(fuente, nueva, actor, campo); return nueva
class M05(Motor):
    def calcular_E(s, vid):
        r = super().calcular_E(vid)
        if r["E"]:
            for rs in s.res.values():
                if rs["resultado"] == "rechazada": r["E"].pop(rs["afectado"], None)
        return r
class M06(Motor):
    def aplicar_resolucion(s, rid):
        ok = super().aplicar_resolucion(rid)
        if ok:
            r = s.res[rid]; otro = [a["id"] for a in s.activas(r["version_evidencia"]) if a["id"] != r["atribucion"] and a["persona"] != r["afectado"]][:1]; _retirar(s, otro)
        return ok
class M07(Motor):
    def aplicar_resolucion(s, rid):
        ok = super().aplicar_resolucion(rid)
        if ok: r = s.res[rid]; s.v[r["version_evidencia"]]["campos"][r["campo"]]["contenido"] = None
        return ok
class M08(Motor):
    def heredar_atribuciones(s, parent, vid):
        for a in sorted(s.activas(parent), key=lambda x: x["seq"])[1:]:
            n = s._atribuir(a["fuente"], vid, a["campo"], a["evento"], a["persona"], "heredada", a["id"], a["origen_version"], a.get("asset")); s.est.append(dict(seq=s.tick(), atr=n, estado="activa", resolucion=None, motivo="heredada de %s" % a["id"]))
class M09(Motor):
    def reconstruir_procedencia(s, vid): r = super().reconstruir_procedencia(vid); return dict(r, completa=True, huecos=[])
class M10(Motor):
    def calcular_E(s, vid):
        r = super().calcular_E(vid)
        if r["E"]:
            for rs in s.res.values():
                if rs["resultado"] == "aceptada": r["E"].pop(rs["afectado"], None)
        return r
class M11(Motor):
    def sustituir_campo(s, fuente, prev, nueva, campo, contenido, actor):
        if fuente != "brief": return super().sustituir_campo(fuente, prev, nueva, campo, contenido, actor)
        s._nueva(fuente, prev, nueva, s.v[prev]["pieza"], s.v[prev]["refs"], actor); s.v[nueva]["campos"][campo].update(contenido=contenido, clasif="sustituido"); s.clas_hist.append((nueva, campo, "sustituido"))
        e = s._evento(fuente, nueva, actor, campo); s._atribuir(fuente, nueva, campo, e, actor); return nueva
class M12(Motor):
    def eliminar_campo(s, fuente, prev, nueva, campo, actor, material=True):
        r = super().eliminar_campo(fuente, prev, nueva, campo, actor, material)
        if fuente == "promotion": s.v[nueva]["campos"][campo]["eliminado"] = False
        return r
class M13(Motor):
    def sustituir_campo(s, fuente, prev, nueva, campo, contenido, actor):
        antes = s.v[prev]["campos"][campo]["contenido"]; r = super().sustituir_campo(fuente, prev, nueva, campo, contenido, actor)
        if difflib.SequenceMatcher(None, antes or "", contenido).ratio() > 0.6: _retirar(s, [a["id"] for a in s.activas(nueva) if a["campo"] == campo and a["rel"] == "heredada"], "similitud alta")
        return r
class M14(Motor):
    def cambiar_clasificacion(s, vid, campo, nueva, actor):
        super().cambiar_clasificacion(vid, campo, nueva, actor); _retirar(s, [a["id"] for a in s.activas(vid) if a["campo"] == campo and a["rel"] == "heredada"])
class M15(Motor):
    def aplicar_resolucion(s, rid):
        ok = super().aplicar_resolucion(rid)
        if ok: r = s.res[rid]; _retirar(s, [a["id"] for a in s.activas(r["version_evidencia"]) if a["persona"] == r["afectado"] and a["campo"] != r["campo"]])
        return ok
class M16(Motor):
    def aplicar_resolucion(s, rid):
        ok = super().aplicar_resolucion(rid)
        if ok: r = s.res[rid]; _retirar(s, [a["id"] for a in s.at.values() if a["persona"] == r["afectado"] and a["fuente"] != r["fuente"] and s.estado(a["id"]) == "activa"])
        return ok
class M17(Motor):
    def aplicar_resolucion(s, rid):
        ok = super().aplicar_resolucion(rid)
        if ok: r = s.res[rid]; _retirar(s, [a["id"] for a in s.at.values() if a["persona"] == r["afectado"] and s.estado(a["id"]) == "activa"])
        return ok
class M18(Motor):
    def rechazar_resolucion(s, rid, motivos):
        r = super().rechazar_resolucion(rid, motivos); _retirar(s, [s.res[rid]["atribucion"]]); return r
class M19(Motor):
    def validar_resolucion(s, rid): return [c for c in super().validar_resolucion(rid) if c != "V06"]
class M27(Motor):
    def validar_resolucion(s, rid): return [c for c in super().validar_resolucion(rid) if not c.startswith("R")]
class M20(Motor):
    def heredar_atribuciones(s, parent, vid):
        for a in sorted(s.activas(parent), key=lambda x: x["seq"]):
            if a["rel"] == "heredada": continue
            n = s._atribuir(a["fuente"], vid, a["campo"], a["evento"], a["persona"], "heredada", a["id"], a["origen_version"], a.get("asset")); s.est.append(dict(seq=s.tick(), atr=n, estado="activa", resolucion=None, motivo="heredada de %s" % a["id"]))
class M21(Motor):
    def aplicar_resolucion(s, rid):
        ok = super().aplicar_resolucion(rid)
        if ok: ref = s.res[rid]["atribucion"]; del s.at[ref]
        return ok
class M22(Motor):
    def reconstruir_procedencia(s, vid):
        r = super().reconstruir_procedencia(vid); h = [x for x in r["huecos"] if not any(x.startswith(k + ":") and s.v.get(k, {}).get("fuente") == "brief" for k in s.v)]
        return dict(r, completa=not h, huecos=h)
class M23(Motor):
    def reconstruir_procedencia(s, vid):
        r = super().reconstruir_procedencia(vid); h = [x for x in r["huecos"] if not any(x.startswith(k + ":") and s.v.get(k, {}).get("fuente") == "promotion" for k in s.v)]
        return dict(r, completa=not h, huecos=h)
class M24(Motor):
    def aplicar_resolucion(s, rid):
        ok = super().aplicar_resolucion(rid)
        if ok: r = s.res[rid]; _retirar(s, [a["id"] for a in s.activas(r["version_evidencia"]) if a["persona"] == r["afectado"] and a["campo"] != r["campo"]]); s.est.append(dict(seq=s.tick(), atr=r["atribucion"], estado="activa", resolucion=rid, motivo="reactivada"))
        return ok
class M25(Motor):
    def calcular_E(s, vid):
        r = super().calcular_E(vid)
        if r["E"]:
            for rs in s.res.values():
                if rs["resultado"] == "aceptada" and len({a["fuente"] for a in s.at.values() if a["persona"] == rs["afectado"]}) > 1: r["E"].pop(rs["afectado"], None)
        return r
class M26(Motor):
    def aplicar_resolucion(s, rid):
        sol = s.solicitudes[rid]; cod = s.validar_resolucion(sol)
        if cod: s.registrar_resolucion(rid, "rechazada", cod, **sol); return False
        s.registrar_resolucion(rid, "aceptada", (), **sol)
        previos = [e for e in s.est if e["atr"] == sol["atribucion"]]
        if previos: previos[-1].update(estado="historica", resolucion=rid)
        else: s.est.append(dict(seq=s.tick(), atr=sol["atribucion"], estado="historica", resolucion=rid, motivo="resolución aceptada"))
        return True

def esc_indep(cls=Motor):
    m, x = _preparar_A(cls, "no independiente"); a = _a_headline(m, x); e0 = x.E("v2")
    _res(m, "r1", a, "B", motivador=[k for k, ev in m.ev.items() if ev["actor"] == "B"][0])
    ok = x.op("aplicar_resolucion", lambda: m.aplicar_resolucion("r1"), res="r1", vid="v2"); e1 = x.E("v2")
    return m, x, [("el editor que ejecutó la sustitución no puede resolver", False, ok), ("la atribución permanece activa", "activa", m.estado(a)), ("E no cambia", sorted(e0["E"]), sorted(e1["E"]))]
def _caso_R(k, cls):
    """Prepara una resolución cuyo resolutor incumple la regla Rk (y puede incumplir otras por solapamiento natural)."""
    m, x = _base(cls); sol = "Q"; res_ = "R"
    if k in ("R6", "R7", "R9"):
        x.op("introducir", lambda: m.introducir_campo("copy", None, "v1", "headline", "Compra hoy", "A", pieza="P1", arte="no_aplica"), prev=None, nueva="v1", actor="A", campo="headline")
        x.op("modificar", lambda: m.modificar_campo("copy", "v1", "v1b", "headline", "Compra hoy ya", "R2"), prev="v1", nueva="v1b", actor="R2", campo="headline")
        x.op("sustituir", lambda: m.sustituir_campo("copy", "v1b", "v2", "headline", "Oferta nueva", "B"), prev="v1b", nueva="v2", actor="B", campo="headline"); res_ = "R2"
    elif k == "R8":
        x.op("introducir", lambda: m.introducir_campo("brief", None, "bv", "commercial_offer", "Oferta", "R2", pieza="P1", arte="no_aplica"), prev=None, nueva="bv", actor="R2", campo="commercial_offer")
        x.op("introducir", lambda: m.introducir_campo("copy", None, "v1", "headline", "Compra hoy", "A", pieza="P1", arte="no_aplica", refs={"brief": "bv"}), prev=None, nueva="v1", actor="A", campo="headline")
        x.op("sustituir", lambda: m.sustituir_campo("copy", "v1", "v2", "headline", "Oferta nueva", "B"), prev="v1", nueva="v2", actor="B", campo="headline"); res_ = "R2"
    else:
        x.op("introducir", lambda: m.introducir_campo("copy", None, "v1", "headline", "Compra hoy", "A", pieza="P1", arte="no_aplica"), prev=None, nueva="v1", actor="A", campo="headline")
        x.op("sustituir", lambda: m.sustituir_campo("copy", "v1", "v2", "headline", "Oferta nueva", "B"), prev="v1", nueva="v2", actor="B", campo="headline")
        res_ = {"R1": "Zz", "R2": "C", "R3": "A", "R4": "R2", "R5": "B"}[k]
        if k == "R4": sol = "R2"
    a = _a_headline(m, x); _res(m, "r1", a, res_, solicitante=sol, motivador=[kk for kk, ev in m.ev.items() if ev["actor"] == "B"][0])
    return m, x, a
def esc_Rk(k):
    def f(cls=Motor):
        m, x, a = _caso_R(k, cls); ok = x.op("aplicar_resolucion", lambda: m.aplicar_resolucion("r1"), res="r1", vid="v2")
        return m, x, [("el resolutor que incumple %s no puede resolver" % k, False, ok), ("el motivo de rechazo incluye %s" % k, True, k in m.res["r1"].get("motivos", [])), ("la atribución permanece activa", "activa", m.estado(a))]
    f.__name__ = "esc_" + k; return f
def esc_Rtodas(cls=Motor):
    m0, x0 = _base(cls); asr = []; viol = []
    for k in ("R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9"):
        m, x, asr_k = esc_Rk(k)(cls); asr += [("%s: %s" % (k, a_[0]), a_[1], a_[2]) for a_ in asr_k]; viol += x.viol
    x0.viol += viol; return m0, x0, asr
def _sin_regla(k):
    class M(Motor):
        def validar_resolucion(s, rid): return [c for c in super().validar_resolucion(rid) if c != k]
    M.__name__ = "Msin" + k; return M
def esc_H_brief(cls=Motor):
    m, x = _base(cls)
    x.op("introducir", lambda: m.introducir_campo("copy", None, "cv1", "headline", "Compra hoy", "A", pieza="P1", arte="no_aplica", refs={"brief": "bvx"}), prev=None, nueva="cv1", actor="A", campo="headline")
    m.v["bvx"] = dict(id="bvx", fuente="brief", pieza="P1", prev=None, campos={"commercial_offer": dict(contenido="sin procedencia", clasif="introducido", eliminado=False)}, refs={}, autor=None, seq=m.tick())
    e = x.E("cv1"); return m, x, [("la procedencia del brief está incompleta: E no es completo", False, e["completa"])]
def esc_H_promo(cls=Motor):
    m, x = _base(cls)
    x.op("introducir", lambda: m.introducir_campo("copy", None, "cv1", "headline", "Compra hoy", "A", pieza="P1", arte="no_aplica", refs={"promotion": "psx"}), prev=None, nueva="cv1", actor="A", campo="headline")
    m.v["psx"] = dict(id="psx", fuente="promotion", pieza="P1", prev=None, campos={"discount": dict(contenido="sin procedencia", clasif="introducido", eliminado=False)}, refs={}, autor=None, seq=m.tick())
    e = x.E("cv1"); return m, x, [("la procedencia de la promoción está incompleta: E no es completo", False, e["completa"])]
def esc_intro(cls=Motor):
    m, x = _base(cls)
    x.op("introducir", lambda: m.introducir_campo("copy", None, "v1", "headline", "Compra hoy", "A", pieza="P1", arte="no_aplica"), prev=None, nueva="v1", actor="A", campo="headline")
    e = x.E("v1"); return m, x, [("el autor que introduce el campo se incorpora a E", ["A"], sorted(e["E"] or {}))]
def esc_mod(cls=Motor):
    m, x = _base(cls)
    x.op("introducir", lambda: m.introducir_campo("copy", None, "v1", "headline", "Compra hoy", "A", pieza="P1", arte="no_aplica"), prev=None, nueva="v1", actor="A", campo="headline")
    x.op("modificar", lambda: m.modificar_campo("copy", "v1", "v2", "headline", "Compra hoy y ahorra", "B"), prev="v1", nueva="v2", actor="B", campo="headline")
    e = x.E("v2"); return m, x, [("E tras la modificación contiene a A y a B", ["A", "B"], sorted(e["E"] or {}))]
def esc_unif(cls=Motor):
    firmas, v = uniformidad(cls); m, x = _base(cls); x.viol += v
    return m, x, [("las tres fuentes producen la misma firma estructural", True, not v)]
def esc_meta(cls=Motor):
    firmas, v = metamorfico(cls); m, x = _base(cls); x.viol += v
    return m, x, [("el resultado no depende de la similitud del texto", True, not v)]

K47_MUT = [
 ("K47-M01", "sustituir_campo retira automáticamente la atribución anterior", "I1", M01, esc_A), ("K47-M02", "eliminar_campo retira automáticamente la atribución anterior", "I1", M02, esc_B),
 ("K47-M03", "modificar_campo pierde una atribución previa", "I1", M03, esc_mod), ("K47-M04", "introducir_campo no incorpora al actor", "I2", M04, esc_intro),
 ("K47-M05", "el cálculo de E excluye a la persona afectada por una resolución rechazada", "I5", M05, esc_E), ("K47-M06", "la resolución aceptada retira otra atribución distinta", "I3", M06, esc_A),
 ("K47-M07", "la resolución aceptada altera una versión histórica", "I10", M07, esc_A), ("K47-M08", "crear_version omite una atribución heredada", "I10", M08, esc_G),
 ("K47-M09", "una cadena de copy incompleta se presenta como completa", "I8", M09, esc_H), ("K47-M10", "una resolución válida elimina de E a quien conserva otra atribución activa", "I7", M10, esc_C),
 ("K47-M11", "la sustitución difiere entre copy y brief", "I9", M11, esc_unif), ("K47-M12", "la eliminación difiere entre brief y promoción", "I9", M12, esc_unif),
 ("K47-M13", "la similitud textual determina el descarte", "I11", M13, esc_meta), ("K47-M14", "cambiar la clasificación retira atribuciones sin resolución", "I12", M14, esc_I),
 ("K47-M15", "resolución válida retira a quien conserva otra atribución activa en otro campo", "I7", M15, esc_C), ("K47-M16", "resolución válida retira a quien conserva una contribución activa en otra fuente", "I7", M16, esc_D),
 ("K47-M17", "resolver una atribución retira todas las atribuciones de la persona", "I3", M17, esc_C), ("K47-M18", "una resolución rechazada cambia el estado de una atribución", "I5", M18, esc_E),
 ("K47-M19", "una resolución con evidencia de otra versión modifica E", "I5", M19, esc_F), ("K47-M20", "crear_version omite una atribución heredada de segunda generación", "I10", M20, esc_G),
 ("K47-M21", "una atribución histórica desaparece de la evidencia", "I6", M21, esc_C), ("K47-M22", "la cadena de brief está incompleta pero E aparece como completo", "I8", M22, esc_H_brief),
 ("K47-M23", "la cadena de promoción está incompleta pero E aparece como completo", "I8", M23, esc_H_promo), ("K47-M24", "la resolución retira un campo distinto del que declara", "I3", M24, esc_C),
 ("K47-M25", "quien contribuye a dos fuentes sale de E al resolver solo una", "I7", M25, esc_D), ("K47-M26", "la resolución válida reescribe un registro anterior en lugar de agregar uno nuevo", "I10", M26, esc_A),
 ("K47-M27", "se acepta una resolución cuyo resolutor incumple la independencia (R1 a R9 no se aplican)", "I4", M27, esc_indep),
] + [("K47-M%d" % (28 + i), "el motor no evalúa la regla %s del resolutor (%s)" % (k, d), "I4", _sin_regla(k), esc_Rk(k)) for i, (k, d) in enumerate((("R1", "membresía activa"), ("R2", "piece.review"), ("R3", "afectado"), ("R4", "solicitante"), ("R5", "actor del cambio"),
                                                                                                                                      ("R6", "contribuyente directo de la cadena"), ("R7", "contribuyente heredado activo"), ("R8", "contribuyente de otra fuente de la cadena"), ("R9", "beneficiario")))]

# =====================================================================================================
# v10: escenario de resoluciones inmutables y cadena de reconsideración (base de R01–R12)
# =====================================================================================================
def esc_resol(cls=Motor):
    m, x = _base(cls)
    x.op("introducir", lambda: m.introducir_campo("copy", None, "v1", "headline", "Compra hoy", "A", pieza="P1", arte="no_aplica"), prev=None, nueva="v1", actor="A", campo="headline")
    x.op("sustituir", lambda: m.sustituir_campo("copy", "v1", "v2", "headline", "Oferta nueva", "B"), prev="v1", nueva="v2", actor="B", campo="headline")
    x.op("introducir", lambda: m.introducir_campo("copy", "v2", "v3", "body", "Cuerpo", "C"), prev="v2", nueva="v3", actor="C", campo="body")
    aA = _a_headline(m, x, "v2"); aC = [a["id"] for a in m.at.values() if a["version"] == "v3" and a["persona"] == "C" and a["campo"] == "body"][0]
    _res(m, "r1", aA, "R", evidencia="")
    ok1 = x.op("aplicar_resolucion", lambda: m.aplicar_resolucion("r1"), res="r1", vid="v2"); r1_antes = copy.deepcopy(_plano(m.res["r1"])); g = lambda rid, k: m.res[rid][k] if rid in m.res else None
    _res(m, "r2", aA, "R", previo="r1")
    ok2 = x.op("aplicar_resolucion", lambda: m.aplicar_resolucion("r2"), res="r2", vid="v2")
    _res(m, "r3", aC, "R2")
    x.op("rechazar_resolucion", lambda: m.rechazar_resolucion("r3", ["evidencia insuficiente según el revisor"]), res="r3", vid="v3")
    e2 = x.E("v2")
    asr = [("la primera resolución sin evidencia nace rechazada y definitiva", ("rechazada", False), (g("r1", "resultado"), ok1)), ("la reconsideración crea un registro nuevo que referencia al anterior", ("r1", "aceptada", True), (g("r2", "previo"), g("r2", "resultado"), ok2)),
           ("el registro rechazado original se conserva íntegro", r1_antes, _plano(m.res["r1"]) if "r1" in m.res else None), ("la cadena se obtiene recorriendo registros", ["r1", "r2"], m.cadena_resoluciones(aA)), ("la decisión vigente se deriva de la cadena", "aceptada", m.decision_vigente(aA)),
           ("solo la atribución exacta pasa a histórica", ("historica", "activa"), (m.estado(aA), m.estado(aC))), ("la resolución rechazada de otra atribución no cambia nada", "rechazada", g("r3", "resultado")), ("A sale de E porque no conserva otra atribución activa", False, "A" in (e2["E"] or {}))]
    return m, x, asr

def _alterar(s, rid, resellar=True, **cambios):
    """Defecto inyectado: reescribe una fila ya persistida eludiendo la guarda del registro (el auditor debe detectarlo igualmente)."""
    plano = {k: dict(v) for k, v in s.res.items()}; plano[rid] = dict(plano[rid], **cambios)
    if resellar: plano[rid]["sello"] = sello_de(plano[rid])
    s.res = plano
def _otra_atr(s, persona, campo): return [a["id"] for a in s.at.values() if a["persona"] == persona and a["campo"] == campo][0]

class _MR(Motor):
    """Base de las mutaciones R: la alteración se aplica al terminar la última operación del escenario (r3)."""
    def rechazar_resolucion(s, rid, motivos):
        r = super().rechazar_resolucion(rid, motivos)
        if rid == "r3": s.alterar()
        return r
class R01(_MR):
    def alterar(s): _alterar(s, "r2", resultado="rechazada")
class R02(_MR):
    def alterar(s): _alterar(s, "r2", evidencia="Evidencia distinta incorporada después")
class R03(_MR):
    def alterar(s): _alterar(s, "r2", resolutor="R2", auth_uid="R2")
class R04(_MR):
    def alterar(s): _alterar(s, "r2", solicitante="Pm")
class R05(_MR):
    def alterar(s): _alterar(s, "r2", atribucion=_otra_atr(s, "C", "body"))
class R06(_MR):
    def alterar(s): _alterar(s, "r2", version_evidencia="v1")
class R07(_MR):
    def alterar(s): s.res = {k: dict(v) for k, v in s.res.items() if k != "r1"}
class R08(_MR):
    def alterar(s): _alterar(s, "r1", resultado="aceptada", resolutor="R2", auth_uid="R2", evidencia="Registro nuevo con el mismo ID", seq=s.tick())
class R09(_MR):
    def alterar(s): _alterar(s, "r3", resultado="aceptada", motivos=[])
class R10(_MR):
    def alterar(s): s.est.append(dict(seq=s.tick(), atr=_otra_atr(s, "C", "body"), estado="historica", resolucion="r2", motivo="reutilización de una resolución aceptada"))
class R11(_MR):
    def alterar(s): _alterar(s, "r2", previo="r3", previo_sello=s.res["r3"]["sello"])
class R12(_MR):
    def alterar(s): _alterar(s, "r1", resultado="aceptada", resolutor="R", auth_uid="R", motivos=[], evidencia="Decisión posterior escrita sobre el registro anterior")

RES_MUT = [("K47-R01", "modificar el resultado de una resolución existente", "I13", R01, esc_resol, "resultado"), ("K47-R02", "modificar la evidencia de una resolución existente", "I13", R02, esc_resol, "evidencia"),
           ("K47-R03", "modificar el resolutor de una resolución existente", "I13", R03, esc_resol, "resolutor"), ("K47-R04", "modificar el solicitante de una resolución existente", "I13", R04, esc_resol, "solicitante"),
           ("K47-R05", "cambiar la atribución afectada por una resolución", "I15", R05, esc_resol, "no corresponde"), ("K47-R06", "cambiar la versión afectada por una resolución", "I13", R06, esc_resol, "version_evidencia"),
           ("K47-R07", "eliminar una resolución histórica", "I13", R07, esc_resol, "eliminada"), ("K47-R08", "reemplazar una resolución usando el mismo ID", "I13", R08, esc_resol, "reemplazada con el mismo ID"),
           ("K47-R09", "convertir una resolución rechazada en aceptada", "I15", R09, esc_resol, "aceptada"), ("K47-R10", "reutilizar una resolución aceptada para otra atribución", "I15", R10, esc_resol, "cita la resolución r2"),
           ("K47-R11", "alterar la cadena de reconsideraciones", "I14", R11, esc_resol, "otra atribución"), ("K47-R12", "reescribir una resolución anterior para simular una decisión posterior", "I14", R12, esc_resol, "anterior fue alterado")]

def pruebas_guarda():
    """Controles de la guarda estructural del registro (no son mutaciones): cada intento directo debe lanzar ResolucionInmutable y dejar el registro intacto."""
    m, x, _ = esc_resol(Motor); ref = _plano(m.res); out = []
    intentos = [("asignar un campo de una fila", lambda: m.res["r1"].__setitem__("resultado", "aceptada")), ("eliminar un campo de una fila", lambda: m.res["r1"].__delitem__("evidencia")), ("actualizar una fila", lambda: m.res["r1"].update(resolutor="R2")),
                ("reemplazar una fila con el mismo ID", lambda: m.res.__setitem__("r1", {"id": "r1"})), ("eliminar una resolución", lambda: m.res.__delitem__("r1")), ("vaciar el registro", lambda: m.res.clear()),
                ("agregar con un ID existente", lambda: m.res.agregar(dict(m.res["r1"]))), ("modificar la evidencia histórica anidada", lambda: m.res["r2"]["evidencia_historica"].__setitem__("contenido", "x")),
                ("volver a aplicar una resolución con el mismo ID", lambda: (m.solicitar_resolucion("r2", **{k: v for k, v in m.solicitudes["r2"].items()}), m.aplicar_resolucion("r2")))]
    for nombre, fn in intentos:
        try: fn(); ok = False
        except ResolucionInmutable: ok = True
        except Exception: ok = False
        out.append((nombre, ok and _plano(m.res) == ref))
    return out

# =====================================================================================================
# v10: escenarios de procedencia del arte (casos positivos y base de A01–A15)
# =====================================================================================================
def _intro_cv(x, m, vid, autor, pieza="P1", arte="con_arte", refs=None):
    x.op("introducir", lambda: m.introducir_campo("copy", None, vid, "headline", "Compra hoy", autor, pieza=pieza, refs=refs, arte=arte), prev=None, nueva=vid, actor=autor, campo="headline")

def esc_art_nuevo(cls=Motor):
    m, x = _base(cls); _intro_cv(x, m, "cv1", "A")
    x.op("registrar_asset", lambda: m.registrar_asset("a1", "cv1", "U")); e = x.E("cv1"); a1 = m.assets["a1"]; ev = m.ev.get(a1["evento_carga"], {}); at = [t for t in m.at.values() if t.get("asset") == "a1"]
    asr = [("el uploader original queda registrado", "U", a1["uploader_original"]), ("el evento de carga lo ejecutó el uploader", ("asset_uploader", "U"), (ev.get("tipo"), ev.get("actor"))), ("el asset queda vinculado a la organización, pieza y versión de copy exactas", ("X", "P1", "cv1"), (a1["org"], a1["pieza"], a1["copy_version"])),
           ("la atribución del uploader es directa y activa", [("U", "directa", "activa")], [(t["persona"], t["rel"], m.estado(t["id"])) for t in at]), ("E completo incluye al uploader y al autor del copy", ["A", "U"], sorted(e["E"] or {}))]
    return m, x, asr
def _reut(cls):
    m, x = _base(cls); _intro_cv(x, m, "cvm", "A"); x.op("registrar_asset", lambda: m.registrar_asset("a1", "cvm", "U"))
    _intro_cv(x, m, "ca", "W", pieza="P2", refs={"master": "cvm"}); x.op("registrar_asset", lambda: m.registrar_asset("a2", "ca", "W", reused_from="a1")); return m, x
def esc_art_reutilizado(cls=Motor):
    m, x = _reut(cls); e = x.E("ca"); a2 = m.assets["a2"]; ev = m.ev.get(a2["evento_reutilizacion"], {}); at = sorted((t["persona"], t["rel"]) for t in m.at.values() if t["version"] == "ca" and t.get("asset"))
    asr = [("el asset reutilizado conserva al uploader original distinto del reutilizador", ("U", "W"), (a2["uploader_original"], a2["reutilizador"])), ("el evento de reutilización lo ejecutó el reutilizador", ("copy_author", "W"), (ev.get("tipo"), ev.get("actor"))),
           ("el uploader original conserva su atribución heredada y el reutilizador una atribución directa propia", [("U", "heredada"), ("W", "directa")], at), ("el asset de origen y la versión exacta quedan referenciados", ("a1", "ca"), (a2["origen"], a2["copy_version"])), ("E incluye al uploader original y al reutilizador", ["A", "U", "W"], sorted(e["E"] or {}))]
    return m, x, asr
def esc_art_modificado(cls=Motor):
    m, x = _base(cls); _intro_cv(x, m, "cv1", "A"); x.op("registrar_asset", lambda: m.registrar_asset("a1", "cv1", "U")); a1_0 = copy.deepcopy(m.assets["a1"])
    x.op("modificar", lambda: m.modificar_asset("cv1", "cv2", "a1b", "a1", "D"), prev="cv1", nueva="cv2", actor="D", campo="arte"); e = x.E("cv2")
    at = sorted((t["persona"], t["rel"], m.estado(t["id"])) for t in m.at.values() if t["version"] == "cv2" and t.get("asset"))
    asr = [("la versión anterior del asset no se sobrescribe", a1_0, m.assets["a1"]), ("el asset nuevo referencia a su versión anterior", ("a1", 2), (m.assets["a1b"]["previo"], m.assets["a1b"]["version_asset"])),
           ("se conserva la atribución anterior y se agrega la del editor", [("D", "directa", "activa"), ("U", "heredada", "activa")], at), ("E incluye al uploader original y al editor", ["A", "D", "U"], sorted(e["E"] or {}))]
    return m, x, asr
def esc_art_sustituido(cls=Motor):
    m, x = _base(cls); _intro_cv(x, m, "cv1", "A"); x.op("registrar_asset", lambda: m.registrar_asset("a1", "cv1", "U"))
    x.op("sustituir", lambda: m.sustituir_asset("cv1", "cv2", "a2", "a1", "W"), prev="cv1", nueva="cv2", actor="W", campo="arte"); e = x.E("cv2")
    at = sorted((t["persona"], t["rel"], m.estado(t["id"])) for t in m.at.values() if t["version"] == "cv2" and t.get("asset"))
    asr = [("la atribución anterior se conserva y se agrega la nueva carga", [("U", "heredada", "activa"), ("W", "directa", "activa")], at), ("ninguna atribución pasó a histórica sin resolución", True, all(m.estado(t) == "activa" for t in m.at)), ("E incluye a ambos uploaders", ["A", "U", "W"], sorted(e["E"] or {}))]
    return m, x, asr
def esc_art_eliminado(cls=Motor):
    m, x = _base(cls); _intro_cv(x, m, "cv1", "A"); x.op("registrar_asset", lambda: m.registrar_asset("a1", "cv1", "U"))
    x.op("eliminar", lambda: m.eliminar_asset("cv1", "cv2", "D"), prev="cv1", nueva="cv2", actor="D", campo="arte", material=True); e = x.E("cv2")
    asr = [("el uso del asset queda eliminado y el historial se conserva", (True, True), (m.v["cv2"]["campos"]["arte"]["eliminado"], "a1" in m.assets)), ("la atribución del uploader no se elimina automáticamente", ["activa"], [m.estado(t["id"]) for t in m.at.values() if t["version"] == "cv2" and t.get("asset") == "a1"]), ("E conserva al uploader", True, "U" in (e["E"] or {}))]
    return m, x, asr
def esc_art_encadenado(cls=Motor):
    m, x = _reut(cls); _intro_cv(x, m, "cc", "D", pieza="P3", refs={"master": "ca"}); x.op("registrar_asset", lambda: m.registrar_asset("a3", "cc", "D", reused_from="a2")); e = x.E("cc")
    asr = [("la cadena a3 → a2 → a1 se reconstruye completa", ["a3", "a2", "a1"], sorted(m._cierre_asset("a3"), reverse=True)), ("el uploader original de la raíz se conserva en la cadena", "U", m.assets["a3"]["uploader_original"]), ("E incluye a la raíz, al intermedio y al último reutilizador", ["D", "U", "W"], sorted(e["E"] or {}))]
    return m, x, asr
def esc_art_noaplica(cls=Motor):
    m, x = _base(cls); _intro_cv(x, m, "cv1", "A", arte="no_aplica"); e1 = x.E("cv1")
    x.op("introducir", lambda: m.introducir_campo("copy", None, "cv2", "headline", "Otra pieza", "B", pieza="P1"), prev=None, nueva="cv2", actor="B", campo="headline"); e2 = x.E("cv2")
    asr = [("la versión declarada no_aplica produce E completo", True, e1["completa"]), ("la declaración identifica al actor y el estado", ("no_aplica", "A"), (m.arte_decl["cv1"]["estado"], m.arte_decl["cv1"]["actor"])),
           ("la ausencia de registros de arte no se acepta como no_aplica", (False, None), (e2["completa"], e2["E"]))]
    return m, x, asr
ESC_ARTE = [("PA1", "asset nuevo con uploader y evento de carga correctos", esc_art_nuevo), ("PA2", "asset reutilizado con uploader y reutilizador diferenciados", esc_art_reutilizado), ("PA3", "asset modificado con conservación de atribuciones", esc_art_modificado),
            ("PA4", "versión sin arte declarada no_aplica", esc_art_noaplica), ("PA5", "asset sustituido con conservación provisional", esc_art_sustituido), ("PA6", "asset eliminado con historial conservado", esc_art_eliminado), ("PA7", "reutilización encadenada completa", esc_art_encadenado)]

class _MA(Motor):
    def registrar_asset(s, aid, copy_version, uploader, reused_from=None, material=True):
        r = super().registrar_asset(aid, copy_version, uploader, reused_from, material); s.tocar(aid, copy_version, uploader, reused_from); return r
    def tocar(s, aid, cv, up, rf): pass
class A01(_MA):
    def tocar(s, aid, cv, up, rf): s.assets[aid]["uploader"] = None
class A02(_MA):
    def tocar(s, aid, cv, up, rf): s.assets[aid]["evento_carga"] = None
class A03(_MA):
    def tocar(s, aid, cv, up, rf):
        if rf: s.assets[aid]["org"] = "Y"
class A04(_MA):
    def tocar(s, aid, cv, up, rf):
        if rf: s.assets[aid]["pieza"] = "P9"
class A05(_MA):
    def tocar(s, aid, cv, up, rf):
        if rf: s.assets[aid]["copy_version"] = "cvm"
class A06(_MA):
    def tocar(s, aid, cv, up, rf):
        if rf:
            s.assets[aid]["uploader_original"] = up
            for t in s.at.values():
                if t.get("asset") == aid and t["rel"] == "heredada": t["persona"] = up
class A07(_MA):
    def tocar(s, aid, cv, up, rf):
        if rf: s.assets[aid]["evento_reutilizacion"] = None
class A08(_MA):
    def tocar(s, aid, cv, up, rf):
        if rf: s.assets[aid]["origen"] = None
class A09(_MA):
    def tocar(s, aid, cv, up, rf):
        if rf: s.assets[rf]["origen"] = aid; s.assets[rf]["tipo"] = "reutilizado"
class A10(_MA):
    def tocar(s, aid, cv, up, rf):
        if rf: s.assets[aid]["origen"] = "a_x"
class A11(Motor):
    def modificar_asset(s, prev, nueva, aid, aid_prev, editor):
        r = super().modificar_asset(prev, nueva, aid, aid_prev, editor); _retirar(s, [a["id"] for a in s.activas(nueva) if a["fuente"] == "asset" and a["rel"] == "heredada"]); return r
class A12(Motor):
    def sustituir_asset(s, prev, nueva, aid, aid_prev, uploader):
        r = super().sustituir_asset(prev, nueva, aid, aid_prev, uploader); _retirar(s, [a["id"] for a in s.activas(nueva) if a["fuente"] == "asset" and a["rel"] == "heredada"]); return r
class A13(Motor):
    def eliminar_asset(s, prev, nueva, actor):
        r = super().eliminar_asset(prev, nueva, actor)
        for k in [k for k, t in s.at.items() if t["fuente"] == "asset"]: del s.at[k]
        del s.assets["a1"]; return r
class A14(_MA):
    def tocar(s, aid, cv, up, rf): s.assets[aid]["uploader"] = None
    def _huecos_arte(s, cur): return []
class A15(Motor):
    def calcular_E(s, vid):
        r = super().calcular_E(vid)
        if r["E"]:
            for p in {t["persona"] for t in s.at.values() if t["fuente"] == "asset"} - {t["persona"] for t in s.at.values() if t["fuente"] != "asset"}: r["E"].pop(p, None)
        return r

class A16(Motor):
    def _huecos_arte(s, cur): return []

ART_MUT = [("K47-A01", "una versión usa un asset sin uploader", "I16", A01, esc_art_nuevo, "uploader"), ("K47-A02", "una versión usa un asset sin evento de carga", "I16", A02, esc_art_nuevo, "evento de carga"),
           ("K47-A03", "el asset pertenece a otra organización", "I19", A03, esc_art_reutilizado, "organización"), ("K47-A04", "el asset pertenece a otra pieza sin relación válida", "I19", A04, esc_art_reutilizado, "pieza"),
           ("K47-A05", "la reutilización apunta a otra versión de copy", "I18", A05, esc_art_reutilizado, "versión de copy"), ("K47-A06", "el reutilizador sustituye al uploader original", "I17", A06, esc_art_reutilizado, "uploader original"),
           ("K47-A07", "asset reutilizado sin evento de reutilización", "I17", A07, esc_art_reutilizado, "evento de reutilización"), ("K47-A08", "asset heredado sin referencia al origen", "I19", A08, esc_art_reutilizado, "sin referencia"),
           ("K47-A09", "la cadena de assets contiene un ciclo", "I19", A09, esc_art_reutilizado, "ciclo"), ("K47-A10", "el asset de origen no existe", "I19", A10, esc_art_reutilizado, "inexistente"),
           ("K47-A11", "un asset modificado pierde la atribución anterior", "I1", A11, esc_art_modificado, "retiró"), ("K47-A12", "un asset sustituido elimina la atribución anterior automáticamente", "I1", A12, esc_art_sustituido, "retiró"),
           ("K47-A13", "un asset eliminado borra su historial", "I6", A13, esc_art_eliminado, "desapareció"), ("K47-A14", "un arte incompleto permite declarar E completo", "I20", A14, esc_art_nuevo, "arte"),
           ("K47-A15", "el cálculo de E omite a los contribuyentes del arte", "I21", A15, esc_art_reutilizado, "omite"),
           ("K47-A16", "la ausencia de registros de arte se acepta como no_aplica", "I20", A16, esc_art_noaplica, "no declara")]


# =====================================================================================================
# v11: identidad exacta del uploader, del evento de carga, de la atribución y de la reutilización (H-01 a H-04)
# =====================================================================================================
class ProcedenciaIncompleta(Exception):
    """Fallo cerrado: no se evalúa impacto ni se publica con procedencia incompleta."""

def calcular_E_verificado(m, vid):
    """Camino único para usar E: el resultado del motor solo vale si el auditor independiente, que reconstruye desde las tablas, no encuentra ninguna inconsistencia."""
    r = m.calcular_E(vid); est = snapshot(m); viol = auditar_E(est, r, vid); h = _hall_arte_exactas(est, vid)
    if viol or h or not _completa(est, vid):
        motivo = [v[1] for v in viol] + [x[1] for x in h] + list(r.get("motivo") or [])
        return dict(completa=False, E=None, motivo=motivo, codigos=sorted({v[0] for v in viol} | {x[0] for x in h}), bloqueado_por="auditor" if (viol or h) and r.get("completa") else "motor")
    return r
def evaluar_impacto(m, vid):
    r = calcular_E_verificado(m, vid)
    if not r["completa"]: raise ProcedenciaIncompleta("; ".join(r["motivo"][:2]))
    return r
def puede_publicar(m, vid):
    try: evaluar_impacto(m, vid); return True
    except ProcedenciaIncompleta: return False

def _reut_doble(cls):
    m, x = _base(cls); _intro_cv(x, m, "cvm", "A"); x.op("registrar_asset", lambda: m.registrar_asset("a1", "cvm", "U"))
    _intro_cv(x, m, "ca", "W", pieza="P2", refs={"master": "cvm"}); x.op("registrar_asset", lambda: m.registrar_asset("a2", "ca", "W", reused_from="a1"))
    _intro_cv(x, m, "cb", "D", pieza="P3", refs={"master": "cvm"}); x.op("registrar_asset", lambda: m.registrar_asset("a3", "cb", "D", reused_from="a1")); return m, x
def _identidad_ok(m, aid):
    """Las diez relaciones de H-01, leídas por separado en el estado del modelo."""
    y = m.assets[aid]; e = m.ev[y["evento_carga"]]; u = y["uploader"]; mem = m.members[u]
    dirs = [b for b in m.at.values() if b["persona"] == u and b.get("asset") == aid and b["evento"] == y["evento_carga"] and b["rel"] == "directa"]
    return [("el uploader existe", True, u in m.members), ("pertenece a la organización del asset", y["org"], mem["org"]), ("membresía activa", True, mem["activo"]), ("el evento de carga existe", True, e is not None),
            ("organización del evento = organización del asset", y["org"], e["org"]), ("pieza del evento = pieza del asset", y["pieza"], e["pieza"]), ("asset exacto y versión de asset del evento", (aid, y["version_asset"]), (e["asset"], e["asset_version"])),
            ("actor autenticado del evento = uploader", (u, u), (e["actor"], e["auth"])), ("versión de copy del evento = versión de copy del asset", y["copy_version"], e["version"]),
            ("atribución directa de la misma cadena", [(y["org"], y["pieza"], y["copy_version"], aid, y["version_asset"], y["evento_carga"])], [(b["org"], b["pieza"], b["version"], b["asset"], b["asset_version"], b["evento"]) for b in dirs])]
def esc_p08(cls=Motor):
    m, x = _base(cls); _intro_cv(x, m, "cv1", "A"); x.op("registrar_asset", lambda: m.registrar_asset("a1", "cv1", "U")); e = x.E("cv1")
    return m, x, _identidad_ok(m, "a1") + [("E completo con el uploader", ["A", "U"], sorted(e["E"] or {}))]
def esc_p09(cls=Motor):
    m, x = _reut(cls); e = x.E("ca"); a2 = m.assets["a2"]; ev = m.ev[a2["evento_reutilizacion"]]; evo = m.ev[m.assets["a1"]["evento_carga"]]
    asr = [("uploader original y reutilizador son personas diferentes", ("U", "W"), (a2["uploader_original"], a2["reutilizador"])), ("el reutilizador no figura como uploader", None, a2["uploader"]),
           ("el evento de carga original sigue siendo el del uploader", ("asset_uploader", "U"), (evo["tipo"], evo["actor"])), ("el evento de reutilización es propio, de la pieza y versión de copy exactas", ("W", "P2", "ca", "a2"), (ev["actor"], ev["pieza"], ev["version"], ev["asset"])),
           ("ambos quedan atribuidos", [("U", "heredada"), ("W", "directa")], sorted((t["persona"], t["rel"]) for t in m.at.values() if t["version"] == "ca" and t.get("asset"))), ("E incluye a ambos", ["A", "U", "W"], sorted(e["E"] or {}))]
    return m, x, asr
def esc_p10(cls=Motor):
    m, x = _reut_doble(cls); ea = x.E("ca"); eb = x.E("cb"); a2, a3 = m.assets["a2"], m.assets["a3"]
    asr = [("cada reutilización tiene su propio evento", True, a2["evento_reutilizacion"] != a3["evento_reutilizacion"]), ("cada reutilización se liga a su versión de copy", (("ca", "a1"), ("cb", "a1")), ((a2["copy_version"], a2["origen"]), (a3["copy_version"], a3["origen"]))),
           ("el uploader original es el mismo en ambas", ("U", "U"), (a2["uploader_original"], a3["uploader_original"])), ("los eventos de reutilización no se sobrescriben y conservan su actor", ("W", "D"), (m.ev[a2["evento_reutilizacion"]]["actor"], m.ev[a3["evento_reutilizacion"]]["actor"])),
           ("E de cada versión incluye a su reutilizador", (["A", "U", "W"], ["A", "D", "U"]), (sorted(ea["E"] or {}), sorted(eb["E"] or {})))]
    return m, x, asr
def esc_p11(cls=Motor):
    m, x = _reut(cls); x.E("ca"); hs = [b for b in m.at.values() if b["version"] == "ca" and b["rel"] == "heredada" and b.get("asset")]
    asr = [("existe al menos una atribución heredada de asset", True, bool(hs)), ("cada heredada referencia a una antecesora existente de la misma persona y evento", [True], sorted({m.at[b["previo"]]["persona"] == b["persona"] and m.at[b["previo"]]["evento"] == b["evento"] for b in hs})),
           ("la antecesora pertenece a la cadena del asset", [True], sorted({m.at[b["previo"]]["asset"] in m._cierre_asset(b["asset"]) for b in hs})), ("el reconstructor no halla huecos de antecesor", [], m._huecos_ancestros("ca"))]
    return m, x, asr
def esc_p12(cls=Motor):
    m, x = _base(cls); _intro_cv(x, m, "cv1", "A"); x.op("registrar_asset", lambda: m.registrar_asset("a1", "cv1", "U"))
    x.op("modificar", lambda: m.modificar_asset("cv1", "cv2", "a1b", "a1", "D"), prev="cv1", nueva="cv2", actor="D", campo="arte"); e = x.E("cv2"); b = m.assets["a1b"]
    asr = [("el uploader original se conserva", ("U", m.ev[m.assets["a1"]["evento_carga"]]["actor"]), (b["uploader_original"], m.ev[b["evento_carga_original"]]["actor"])), ("el editor es quien subió la versión nueva del asset", "D", b["uploader"]),
           ("el uploader original conserva su atribución activa", True, any(t["persona"] == "U" and m.estado(t["id"]) == "activa" and t["version"] == "cv2" for t in m.at.values())), ("E incluye al uploader original y al editor", ["A", "D", "U"], sorted(e["E"] or {}))]
    return m, x, asr
def esc_p13(cls=Motor):
    m, x = _reut(cls); _intro_cv(x, m, "cc", "D", pieza="P3", refs={"master": "ca"}); x.op("registrar_asset", lambda: m.registrar_asset("a3", "cc", "D", reused_from="a2"))
    _intro_cv(x, m, "cd", "B", pieza="P4", refs={"master": "cc"}); x.op("registrar_asset", lambda: m.registrar_asset("a4", "cd", "B", reused_from="a3")); e = x.E("cd")
    asr = [("la cadena tiene cuatro eslabones", ["a4", "a3", "a2", "a1"], sorted(m._cierre_asset("a4"), reverse=True)), ("cada reutilización tiene un evento distinto", 3, len({m.assets[k]["evento_reutilizacion"] for k in ("a2", "a3", "a4")})),
           ("el uploader original se conserva en el último eslabón", "U", m.assets["a4"]["uploader_original"]), ("E incluye a todos los contribuyentes de la cadena", ["B", "D", "U", "W"], sorted(e["E"] or {}))]
    return m, x, asr
def esc_p14(cls=Motor):
    m, x = _base(cls); _intro_cv(x, m, "cv1", "A", arte="no_aplica"); e = x.E("cv1"); d = m.arte_decl["cv1"]
    asr = [("la versión declara no_aplica con actor", ("no_aplica", "A"), (d["estado"], d["actor"])), ("el modelo no contiene ningún asset de esa versión", [], [k for k, y in m.assets.items() if y["copy_version"] == "cv1"]),
           ("ninguna atribución de arte de esa versión", [], [t["id"] for t in m.at.values() if t["version"] == "cv1" and (t.get("asset") or t["campo"] == "arte")]), ("E completo sin contribuyentes de arte", (True, ["A"]), (e["completa"], sorted(e["E"] or {})))]
    return m, x, asr
ESC_ARTE = [(("P%02d" % (i + 1)),) + tuple(c[1:]) for i, c in enumerate(ESC_ARTE)] + [
    ("P08", "uploader válido con organización, pieza, evento y versión exactos", esc_p08), ("P09", "uploader original y reutilizador diferentes, ambos atribuidos", esc_p09), ("P10", "mismo asset reutilizado en dos versiones de copy con eventos independientes", esc_p10),
    ("P11", "atribución heredada válida con antecesor verificable", esc_p11), ("P12", "uploader original conservado tras modificar el asset", esc_p12), ("P13", "cadena de reutilización válida de más de dos versiones", esc_p13), ("P14", "ausencia real de arte declarada no_aplica", esc_p14)]

# =====================================================================================================
# v12: identidad exacta del asset de origen en las reutilizaciones (IG5-101)
# =====================================================================================================
def _fx12(cls, mod=False):
    """Estado válido: dos originales con el mismo número de versión (a1 de U y ax de Z), una versión 2 de cada uno (a1b y axb), un original de otra pieza (aq) y un tercer original de U (au); a2 reutiliza el origen elegido en la pieza P2."""
    m, x = _base(cls); _intro_cv(x, m, "cvm", "A"); x.op("registrar_asset", lambda: m.registrar_asset("a1", "cvm", "U")); src = "a1"
    if mod:
        x.op("modificar", lambda: m.modificar_asset("cvm", "cvm2", "a1b", "a1", "D"), prev="cvm", nueva="cvm2", actor="D", campo="arte"); src = "a1b"
    _intro_cv(x, m, "cvx", "B"); x.op("registrar_asset", lambda: m.registrar_asset("ax", "cvx", "Z"))
    x.op("modificar", lambda: m.modificar_asset("cvx", "cvx2", "axb", "ax", "C"), prev="cvx", nueva="cvx2", actor="C", campo="arte")
    _intro_cv(x, m, "cvq", "B", pieza="P5"); x.op("registrar_asset", lambda: m.registrar_asset("aq", "cvq", "Pm"))
    _intro_cv(x, m, "cvu", "B"); x.op("registrar_asset", lambda: m.registrar_asset("au", "cvu", "U"))
    _intro_cv(x, m, "ca", "W", pieza="P2", refs={"master": "cvm2" if mod else "cvm"}); x.op("registrar_asset", lambda: m.registrar_asset("a2", "ca", "W", reused_from=src))
    x.op("sin_cambio", lambda: m.version_sin_cambio("copy", "ca", "ca2", "W"), prev="ca", nueva="ca2", actor="W")
    return m, x
def _ev_carga(m, aid): return [e for e in m.ev.values() if e["tipo"] == "asset_uploader" and e.get("asset") == aid][0]
def _atr_dir(m, persona, aid): return [t["id"] for t in m.at.values() if t["persona"] == persona and t.get("asset") == aid and t["rel"] == "directa" and t["fuente"] == "asset"][0]
def _raiz_t(m, aid):
    """Raíz de la cadena recorrida en la prueba (independiente del motor)."""
    x = aid
    while True:
        y = m.assets[x]; n = y.get("origen") if y["tipo"] == "reutilizado" else y.get("previo") if y["tipo"] == "modificado" else None
        if n is None: return x
        x = n
def _asr_identidad(m, aid, src, org="X", pieza=None, cv=None, reut=None, up=None):
    """Los doce vínculos de identidad de una reutilización, cada uno contrastado con el registro concreto que debe referenciar (buscado en las tablas, no copiado del asset)."""
    y = m.assets[aid]; e = m.ev[y["evento_reutilizacion"]]; o = m.assets[src]; eo = _ev_carga(m, _raiz_t(m, src))
    return [("1 organización propietaria", org, e["org"]), ("2 pieza de destino", pieza or m.v[y["copy_version"]]["pieza"], e["pieza"]), ("3 versión exacta de copy de destino", cv or y["copy_version"], e["version"]),
            ("4 asset reutilizado", (aid, aid), (e["asset"], e["asset_id"])), ("5 versión exacta del asset reutilizado", aid, e["asset_version_id"]), ("6 asset de origen", o["asset_id"], e["source_asset_id"]),
            ("7 versión exacta del asset de origen", src, e["source_asset_version_id"]), ("8 evento original de carga", eo["id"], e["source_upload_event_id"]), ("9 evento de reutilización propio", (y["evento_reutilizacion"], "copy_author"), (e["id"], e["tipo"])),
            ("10 actor autenticado = reutilizador", (reut or y["reutilizador"],) * 3, (e["actor"], e["auth"], y["reutilizador"])), ("11 relación de procedencia con el original", "reutilizacion", y["procedencia"]),
            ("12 atribución original del uploader", _atr_dir(m, eo["actor"], eo["asset"]), e["source_attribution_id"]), ("uploader original distinto del reutilizador y conservado", (up or eo["actor"], True), (y["uploader_original"], y["uploader_original"] != y["reutilizador"] and y["uploader"] is None))]
def esc_o12(cls=Motor, mod=False):
    m, x = _fx12(cls, mod); e = x.E("ca2"); src = "a1b" if mod else "a1"
    return m, x, _asr_identidad(m, "a2", src, up="U" if mod else None) + [("E completo", True, e["completa"])]
def esc_o12m(cls=Motor): return esc_o12(cls, True)
def esc_p15(cls=Motor):
    m, x, asr = esc_o12(cls); e = m.calcular_E("ca2"); return m, x, asr + [("E incluye al autor del copy, al uploader original y al reutilizador y no a otros originales", ["A", "U", "W"], sorted(e["E"] or {}))]
def esc_p16(cls=Motor):
    m, x = _fx12(cls); _intro_cv(x, m, "cz", "D", pieza="P6", refs={"master": "cvx"}); x.op("registrar_asset", lambda: m.registrar_asset("a5", "cz", "D", reused_from="ax")); e1 = x.E("ca2"); e2 = x.E("cz"); a1, ax, a2, a5 = (m.assets[k] for k in ("a1", "ax", "a2", "a5"))
    asr = [("dos originales distintos comparten el número de versión 1", (1, 1), (a1["version_asset"], ax["version_asset"])), ("sus identificadores de asset y de versión son distintos", (True, True), (a1["asset_id"] != ax["asset_id"], a1["version_id"] != ax["version_id"])),
           ("sus eventos de carga son distintos", True, a1["evento_carga"] != ax["evento_carga"]), ("cada reutilización identifica a su propio original", (("a1", "a1"), ("ax", "ax")), ((m.ev[a2["evento_reutilizacion"]]["source_asset_id"], m.ev[a2["evento_reutilizacion"]]["source_asset_version_id"]), (m.ev[a5["evento_reutilizacion"]]["source_asset_id"], m.ev[a5["evento_reutilizacion"]]["source_asset_version_id"]))),
           ("cada reutilización identifica el evento de carga de su original", (a1["evento_carga"], ax["evento_carga"]), (m.ev[a2["evento_reutilizacion"]]["source_upload_event_id"], m.ev[a5["evento_reutilizacion"]]["source_upload_event_id"])),
           ("E de cada pieza contiene solo a los contribuyentes de su original", (["A", "U", "W"], ["B", "D", "Z"]), (sorted(e1["E"] or {}), sorted(e2["E"] or {})))]
    return m, x, asr
def esc_p17(cls=Motor):
    m, x = _reut_doble(cls); ea = x.E("ca"); eb = x.E("cb"); a2, a3 = m.assets["a2"], m.assets["a3"]; e2, e3 = m.ev[a2["evento_reutilizacion"]], m.ev[a3["evento_reutilizacion"]]
    asr = _asr_identidad(m, "a2", "a1") + _asr_identidad(m, "a3", "a1") + [("cada reutilización tiene su evento, pieza y versión de copy de destino", (("P2", "ca"), ("P3", "cb"), True), ((e2["pieza"], e2["version"]), (e3["pieza"], e3["version"]), e2["id"] != e3["id"])),
           ("ambas identifican el mismo original, su versión y su evento de carga", True, (e2["source_asset_version_id"], e2["source_upload_event_id"]) == (e3["source_asset_version_id"], e3["source_upload_event_id"]) == ("a1", m.assets["a1"]["evento_carga"])),
           ("E por pieza", (["A", "U", "W"], ["A", "D", "U"]), (sorted(ea["E"] or {}), sorted(eb["E"] or {})))]
    return m, x, asr
def esc_p18(cls=Motor):
    m, x = _reut(cls); _intro_cv(x, m, "cc", "D", pieza="P3", refs={"master": "ca"}); x.op("registrar_asset", lambda: m.registrar_asset("a3", "cc", "D", reused_from="a2")); e = x.E("cc"); e2, e3 = m.ev[m.assets["a2"]["evento_reutilizacion"]], m.ev[m.assets["a3"]["evento_reutilizacion"]]
    asr = [("a3 identifica como origen inmediato a a2 y su versión", ("a2", "a2"), (e3["source_asset_id"], e3["source_asset_version_id"])), ("el evento original de carga del origen es el de U, la raíz", m.assets["a1"]["evento_carga"], e3["source_upload_event_id"]),
           ("a2 identifica como origen a a1", ("a1", "a1", m.assets["a1"]["evento_carga"]), (e2["source_asset_id"], e2["source_asset_version_id"], e2["source_upload_event_id"])), ("cada actor intermedio tiene su evento propio", ("W", "D", True), (e2["actor"], e3["actor"], e2["id"] != e3["id"])),
           ("el uploader original se conserva en toda la cadena", ("U", "U"), (m.assets["a2"]["uploader_original"], m.assets["a3"]["uploader_original"])), ("ningún intermedio figura como uploader", (None, None), (m.assets["a2"]["uploader"], m.assets["a3"]["uploader"])),
           ("E incluye a la raíz, al intermedio y al último reutilizador", ["D", "U", "W"], sorted(e["E"] or {}))]
    return m, x, asr
def esc_p19(cls=Motor):
    m, x = _reut(cls); ev0 = copy.deepcopy(m.ev[m.assets["a2"]["evento_reutilizacion"]]); a20 = copy.deepcopy(m.assets["a2"])
    x.op("modificar", lambda: m.modificar_asset("ca", "cb", "a2b", "a2", "D"), prev="ca", nueva="cb", actor="D", campo="arte"); e = x.E("cb"); b = m.assets["a2b"]
    asr = [("el asset reutilizado modificado referencia a su versión anterior", ("a2", 2, "a2"), (b["previo"], b["version_asset"], b["asset_id"])), ("el evento de reutilización y el asset reutilizado no se sobrescriben", (ev0, a20), (m.ev[a20["evento_reutilizacion"]], m.assets["a2"])),
           ("la cadena conserva al uploader original", ("U", "U"), (b["uploader_original"], m.ev[b["evento_carga_original"]]["actor"])), ("el nuevo editor es el uploader de la versión nueva", "D", b["uploader"]), ("la procedencia del original se conserva", ("a1", "a1"), (m.ev[m.assets["a2"]["evento_reutilizacion"]]["source_asset_version_id"], m._raiz_asset("a2b")["id"])),
           ("E incluye al original, al reutilizador y al nuevo editor", ["A", "D", "U", "W"], sorted(e["E"] or {}))]
    return m, x, asr
def _compartidas():
    """Funciones del auditor independiente que usan funciones de validación o reconstrucción del motor (debe ser vacío)."""
    import ast, inspect
    prohibidas = {"_id_reutilizacion", "_id_uploader", "_id_origen", "_huecos_arte", "_huecos_asset", "_huecos_ancestros", "_origen_carga", "_validar_reutilizacion", "reconstruir_procedencia", "calcular_E", "cadena_identidad", "Motor", "_raiz_asset", "_cierre_asset"}; out = set()
    for f in (_hall_arte, _hall_identidad, _hall_cadena, cadena_identidad_independiente, _hall_arte_exactas, _completa):
        for n in ast.walk(ast.parse(inspect.getsource(f))):
            if isinstance(n, ast.Name) and n.id in prohibidas: out.add((f.__name__, n.id))
            if isinstance(n, ast.Attribute) and n.attr in prohibidas: out.add((f.__name__, n.attr))
    return sorted(out)
def esc_p20(cls=Motor):
    m, x = _reut(cls); _intro_cv(x, m, "cc", "D", pieza="P3", refs={"master": "ca"}); x.op("registrar_asset", lambda: m.registrar_asset("a3", "cc", "D", reused_from="a2")); e = x.E("cc"); est = snapshot(m)
    asr = [("el motor y el auditor reconstruyen la misma cadena de identidad", m.cadena_identidad("a3"), cadena_identidad_independiente(est, "a3")), ("la cadena tiene tres eslabones con evento propio cada uno de los reutilizados", 3, len(cadena_identidad_independiente(est, "a3"))),
           ("el auditor no usa funciones de validación ni de reconstrucción del motor", [], _compartidas()), ("el auditor no halla huecos de arte en la cadena válida", [], _hall_arte_exactas(est, "cc")), ("el E del motor coincide con el E recalculado por el auditor", sorted(_E(est, "cc")), sorted(e["E"] or {}))]
    return m, x, asr
ESC_ARTE += [("P15", "reutilización válida con identidad exacta del origen", esc_p15), ("P16", "dos assets distintos con el mismo número de versión", esc_p16), ("P17", "dos reutilizaciones del mismo asset original en dos piezas", esc_p17),
             ("P18", "cadena de tres niveles con eventos propios y uploader original conservado", esc_p18), ("P19", "reutilización y modificación posterior del asset reutilizado", esc_p19), ("P20", "motor y auditor reconstruyen la misma cadena sin compartir funciones", esc_p20)]

def _estado_completo(m):
    """Instantánea completa del motor (todas las tablas y contadores), para comparar antes y después de un intento fallido."""
    return copy.deepcopy(m.__dict__)
def pruebas_atomicidad():
    """H-01 (v12 y v13): una reutilización con un elemento obligatorio ausente o inconsistente falla antes de escribir y no deja registros parciales (comparación del estado completo, no solo del asset nuevo). Los ocho primeros casos son de la v12; los doce siguientes, A54 a A65."""
    casos = [("el asset de origen no existe", lambda m: None, "zz"), ("el origen no tiene evento de carga", lambda m: m.assets["a1"].update(evento_carga=None), "a1"), ("el uploader original no tiene membresía activa", lambda m: m.members["U"].update(activo=False), "a1"),
             ("no existe la atribución directa del uploader original", lambda m: [m.at.pop(k) for k in [t["id"] for t in m.at.values() if t["rel"] == "directa" and t.get("asset") == "a1"]], "a1"), ("el origen pertenece a otra organización", lambda m: m.assets["a1"].update(org="Y"), "a1"),
             ("la pieza del origen no coincide con su evento", lambda m: m.assets["a1"].update(pieza="P9"), "a1"), ("el reutilizador no es miembro activo", lambda m: m.members["W"].update(activo=False), "a1"), ("el identificador del asset reutilizado ya existe", lambda m: None, "dup")]
    out = []
    for nombre, corrompe, origen in casos:
        m, x = _base(Motor); _intro_cv(x, m, "cvm", "A"); m.registrar_asset("a1", "cvm", "U"); _intro_cv(x, m, "ca", "W", pieza="P2", refs={"master": "cvm"}); corrompe(m); antes = _estado_completo(m)
        try: m.registrar_asset("a1" if origen == "dup" else "a2", "ca", "W", reused_from="a1" if origen == "dup" else origen); ok = False
        except ReutilizacionInvalida: ok = True
        except Exception: ok = False
        out.append((nombre, ok and _estado_completo(m) == antes))
    for r in correr_mutaciones_rechazo(): out.append(("%s: %s" % (r["id"].replace("K47-", ""), r["mut"]), r["atomico"] and r["rechaza"]))
    return out

def _mk(metodo, objetivo, fn):
    """Motor defectuoso: ejecuta el método correcto y después altera UNA relación del estado cuando el asset objetivo ya está registrado."""
    class _C(Motor):
        _verificar_final = lambda s, op, aid: None   # el motor defectuoso no tiene la segunda línea de defensa: el auditor independiente debe detectar la alteración
    def envuelto(s, *a, **k):
        r = getattr(Motor, metodo)(s, *a, **k)
        if objetivo in a or objetivo in k.values(): fn(s)
        return r
    setattr(_C, metodo, envuelto); return _C
def _carga(s, aid): return s.ev[s.assets[aid]["evento_carga"]]
def _reu(s, aid): return s.ev[s.assets[aid]["evento_reutilizacion"]]
def _directa(s, aid): return [b for b in s.at.values() if b.get("asset") == aid and b["rel"] == "directa" and b["fuente"] == "asset"][0]
def _set(d, **kw): d.update(kw)
A17 = _mk("registrar_asset", "a1", lambda s: _set(s.members["U"], org="Y"))
A18 = _mk("registrar_asset", "a1", lambda s: _set(s.members["U"], activo=False))
A19 = _mk("registrar_asset", "a1", lambda s: _set(_carga(s, "a1"), org="Y"))
A20 = _mk("registrar_asset", "a1", lambda s: _set(_carga(s, "a1"), pieza="P9"))
A21 = _mk("modificar_asset", "a1b", lambda s: _set(_carga(s, "a1b"), asset_version=1))
A22 = _mk("registrar_asset", "a1", lambda s: _set(_carga(s, "a1"), actor="Z"))
A23 = _mk("registrar_asset", "a2", lambda s: _set(_directa(s, "a1"), version="ca"))
A24 = _mk("registrar_asset", "a2", lambda s: _set(_directa(s, "a1"), pieza="P9"))
A25 = _mk("registrar_asset", "a2", lambda s: _set(_directa(s, "a1"), org="Y"))
A26 = _mk("registrar_asset", "a2", lambda s: _set(_reu(s, "a2"), org="Y"))
A27 = _mk("registrar_asset", "a2", lambda s: _set(_reu(s, "a2"), pieza="P9"))
A28 = _mk("registrar_asset", "a2", lambda s: _set(_reu(s, "a2"), actor="Z", auth="Z"))
A29 = _mk("registrar_asset", "a2", lambda s: _set(_reu(s, "a2"), asset_version=9))
A30 = _mk("registrar_asset", "a2", lambda s: _set(_reu(s, "a2"), version="cvm"))
A31 = _mk("registrar_asset", "a2", lambda s: _set(s.assets["a2"], uploader="W"))
A32 = _mk("registrar_asset", "a2", lambda s: [_set(b, previo=None) for b in s.at.values() if b["version"] == "ca" and b["rel"] == "heredada" and b.get("asset") == "a2"])
A49 = _mk("modificar_asset", "a1b", lambda s: _set(_carga(s, "a1b"), version="cv1"))
A50 = _mk("registrar_asset", "a2", lambda s: _set(s.members["W"], activo=False))
A51 = _mk("registrar_asset", "a3", lambda s: _set(s.assets["a3"], evento_reutilizacion=s.assets["a2"]["evento_reutilizacion"]))
A52 = _mk("registrar_asset", "a1", lambda s: _set(_carga(s, "a1"), auth="Z"))
def _oculta(s): s.assets["ax"] = dict(id="ax", org="X", pieza="P1", version_asset=1, tipo="nuevo", origen=None, previo=None, uploader=None, evento_carga=None, uploader_original=None, evento_carga_original=None, reutilizador=None, evento_reutilizacion=None, material=None, copy_version="cv1")
A53 = _mk("introducir_campo", "cv1", _oculta)
ART_MUT2 = [("K47-A17", "el uploader pertenece a otra organización", "I22", A17, esc_art_nuevo, "otra organización"), ("K47-A18", "el uploader tiene membresía inactiva", "I22", A18, esc_art_nuevo, "membresía inactiva"),
            ("K47-A19", "el evento de carga pertenece a otra organización", "I23", A19, esc_art_nuevo, "otra organización"), ("K47-A20", "el evento de carga pertenece a otra pieza", "I23", A20, esc_art_nuevo, "otra pieza"),
            ("K47-A21", "el evento de carga corresponde a otra versión del asset", "I23", A21, esc_art_modificado, "otra versión del asset"), ("K47-A22", "el actor del evento de carga no es el uploader", "I23", A22, esc_art_nuevo, "no es el uploader"),
            ("K47-A23", "la atribución directa corresponde a otra versión de copy", "I24", A23, esc_art_reutilizado, "versión de copy"), ("K47-A24", "la atribución directa corresponde a otra pieza", "I24", A24, esc_art_reutilizado, "pieza"),
            ("K47-A25", "la atribución directa corresponde a otra organización", "I24", A25, esc_art_reutilizado, "organización"), ("K47-A26", "el evento de reutilización pertenece a otra organización", "I25", A26, esc_art_reutilizado, "otra organización"),
            ("K47-A27", "el evento de reutilización pertenece a otra pieza", "I25", A27, esc_art_reutilizado, "otra pieza"), ("K47-A28", "el evento de reutilización identifica a otro actor", "I25", A28, esc_art_reutilizado, "otro actor"),
            ("K47-A29", "el evento de reutilización referencia otra versión de asset", "I25", A29, esc_art_reutilizado, "otra versión de asset"), ("K47-A30", "la reutilización no referencia la versión exacta de copy", "I25", A30, esc_art_reutilizado, "versión exacta de copy"),
            ("K47-A31", "la reutilización intenta reemplazar al uploader original", "I17", A31, esc_art_reutilizado, "figura como uploader"), ("K47-A32", "la atribución heredada de asset carece de antecesor verificable", "I26", A32, esc_art_reutilizado, "antecesor verificable"),
            ("K47-A49", "el evento de carga corresponde a otra versión de copy", "I23", A49, esc_art_modificado, "otra versión de copy"), ("K47-A50", "el reutilizador tiene membresía inactiva", "I25", A50, esc_art_reutilizado, "membresía inactiva"),
            ("K47-A51", "dos reutilizaciones comparten el mismo evento", "I25", A51, esc_p10, "evento propio"), ("K47-A52", "el actor autenticado del evento de carga no es el uploader", "I23", A52, esc_art_nuevo, "autenticado"),
            ("K47-A53", "no_aplica oculta un asset registrado", "I20", A53, esc_art_noaplica, "no_aplica")]
ART_MUT = ART_MUT + ART_MUT2
ART_MUT2_FIN = len(ART_MUT)

# ---- v12: A33 a A48 (identidad exacta del origen) ----
def _src_set(s, **kw): _set(_reu(s, "a2"), **kw)
A33 = _mk("registrar_asset", "a2", lambda s: _src_set(s, source_asset_id=s.assets["axb"]["asset_id"], source_asset_version_id="axb"))
A34 = _mk("registrar_asset", "a2", lambda s: _src_set(s, source_asset_id="ax", source_asset_version_id="ax"))
A35 = _mk("registrar_asset", "a2", lambda s: _src_set(s, source_asset_version_id="a1"))
A36 = _mk("registrar_asset", "a2", lambda s: _src_set(s, source_upload_event_id=_ev_carga(s, "ax")["id"]))
A37 = _mk("registrar_asset", "a2", lambda s: _src_set(s, source_upload_event_id=_ev_carga(s, "a1b")["id"]))
A38 = _mk("registrar_asset", "a2", lambda s: _src_set(s, source_uploader_id="Z"))
A39 = _mk("registrar_asset", "a2", lambda s: _set(s.assets["a2"], origen="ax"))
A40 = _mk("registrar_asset", "a2", lambda s: _src_set(s, source_asset_version=7))
A41 = _mk("registrar_asset", "a2", lambda s: _src_set(s, source_upload_event_id=[e["id"] for e in s.ev.values() if e["version"] == "cvm" and e["tipo"] == "copy_author"][0]))
def _swap_assets(s):
    for k in ("evento_carga", "uploader", "uploader_original", "evento_carga_original"): s.assets["a1"][k], s.assets["ax"][k] = s.assets["ax"][k], s.assets["a1"][k]
A42 = _mk("registrar_asset", "a2", _swap_assets)
def _swap_events(s):
    e1, e2 = _ev_carga(s, "a1")["id"], _ev_carga(s, "ax")["id"]; s.ev[e1], s.ev[e2] = s.ev[e2], s.ev[e1]
A43 = _mk("registrar_asset", "a2", _swap_events)
A44 = _mk("registrar_asset", "a2", lambda s: _set(s.assets["a1"], pieza="P9"))
A45 = _mk("registrar_asset", "a2", lambda s: _set(s.assets["a1"], org="Y"))
A46 = _mk("registrar_asset", "a2", lambda s: _set(_reu(s, "a2"), version="ca2"))
A47 = _mk("registrar_asset", "a2", lambda s: _set(_reu(s, "a2"), auth="Z"))
A48 = _mk("registrar_asset", "a3", lambda s: _set(s.assets["a3"], evento_carga_original=None))
ART_MUT3 = [("K47-A33", "el evento referencia otro asset de origen de la misma organización", "I27", A33, esc_o12, "número de versión distinto"), ("K47-A34", "el evento referencia otro asset con el mismo número de versión", "I27", A34, esc_o12, "mismo número de versión"),
            ("K47-A35", "el evento referencia otra versión del mismo asset original", "I27", A35, esc_o12m, "otra versión del mismo asset de origen"), ("K47-A36", "el evento referencia un evento de carga de otro asset", "I27", A36, esc_o12, "evento de carga de otro asset"),
            ("K47-A37", "el evento referencia otro evento de carga del mismo asset, de otra versión", "I27", A37, esc_o12m, "evento de carga de otra versión"), ("K47-A38", "el evento referencia otro uploader original", "I27", A38, esc_o12, "otro uploader original"),
            ("K47-A39", "el asset reutilizado apunta a un origen distinto del declarado por el evento", "I27", A39, esc_o12, "distinto del declarado"), ("K47-A40", "el evento apunta al origen correcto pero a una versión incorrecta", "I27", A40, esc_o12, "versión de origen incorrecta"),
            ("K47-A41", "el evento apunta al asset correcto pero a otro evento que no es el de carga", "I27", A41, esc_o12, "que no es de carga"), ("K47-A42", "se intercambian dos assets con idéntico número de versión", "I28", A42, esc_o12, "están intercambiados"),
            ("K47-A43", "se intercambian dos eventos de carga de la misma organización y pieza", "I28", A43, esc_o12, "la clave no coincide con su identificador"), ("K47-A44", "el origen pertenece a otra pieza", "I27", A44, esc_o12, "otra pieza"),
            ("K47-A45", "el origen pertenece a otra organización", "I27", A45, esc_o12, "otra organización"), ("K47-A46", "el evento de reutilización referencia otra versión de copy", "I27", A46, esc_o12, "otra versión de copy de la misma pieza"),
            ("K47-A47", "el actor autenticado no coincide con el reutilizador registrado", "I27", A47, esc_o12, "no coincide con el reutilizador registrado"), ("K47-A48", "la cadena de reutilización pierde el vínculo con el evento original de carga", "I28", A48, esc_art_encadenado, "pierde el vínculo")]
ART_MUT = ART_MUT + ART_MUT3

# pruebas adversariales: el motor acepta, el auditor detecta, el sistema final bloquea
class _Ciego(Motor):
    """Motor que no valida la procedencia del arte (acepta cualquier caso)."""
    def _huecos_arte(s, cur): return []
def _adv(nombre, esc, vid, tamper, codigo):
    def f():
        m, x, _ = esc(_Ciego); tamper(m); r = m.calcular_E(vid); est = snapshot(m)
        cods = sorted({c[0] for c in auditar_E(est, r, vid)}); v = calcular_E_verificado(m, vid)
        try: evaluar_impacto(m, vid); falla = False
        except ProcedenciaIncompleta: falla = True
        return dict(id=nombre[0], nombre=nombre[1], motor_acepta=bool(r["completa"]) and r["E"] is not None, auditor=codigo in cods, E_bloqueado=(not v["completa"]) and v["E"] is None, impacto_falla=falla, no_publica=not puede_publicar(m, vid), codigos=cods)
    return f
ADV = [_adv(("ADV1", "uploader de otra organización"), esc_art_nuevo, "cv1", lambda m: _set(m.members["U"], org="Y"), "I22"), _adv(("ADV2", "evento de carga de otra pieza"), esc_art_nuevo, "cv1", lambda m: _set(_carga(m, "a1"), pieza="P9"), "I23"),
       _adv(("ADV3", "evento de reutilización de otro actor"), esc_art_reutilizado, "ca", lambda m: _set(_reu(m, "a2"), actor="Z", auth="Z"), "I25"),
       _adv(("ADV4", "atribución heredada sin antecesor"), esc_art_reutilizado, "ca", lambda m: [_set(b, previo=None) for b in m.at.values() if b["version"] == "ca" and b["rel"] == "heredada" and b.get("asset") == "a2"], "I26"),
       _adv(("ADV5", "uploader con membresía inactiva"), esc_art_nuevo, "cv1", lambda m: _set(m.members["U"], activo=False), "I22")]
def _foraneo(m):
    y = copy.deepcopy(m.assets["a1"]); y.update(id="yq", asset_id="yq", version_id="yq", org="Y"); ev = copy.deepcopy(_ev_carga(m, "a1")); ev.update(id="ey", org="Y", asset="yq", asset_id="yq", asset_version_id="yq"); y["evento_carga"] = y["evento_carga_original"] = "ey"; m.assets["yq"] = y; m.ev["ey"] = ev
ADV += [_adv(("ADV6", "asset diferente con el mismo número de versión"), esc_o12, "ca2", lambda m: _src_set(m, source_asset_id="ax", source_asset_version_id="ax"), "I27"),
        _adv(("ADV7", "evento de carga diferente del mismo uploader"), esc_o12, "ca2", lambda m: _src_set(m, source_upload_event_id=_ev_carga(m, "au")["id"]), "I27"),
        _adv(("ADV8", "versión de asset diferente del mismo origen"), esc_o12m, "ca2", lambda m: _src_set(m, source_asset_version_id="a1"), "I27"),
        _adv(("ADV9", "asset de otra pieza con el mismo número de versión"), esc_o12, "ca2", lambda m: _src_set(m, source_asset_id="aq", source_asset_version_id="aq"), "I27"),
        _adv(("ADV10", "asset de otra organización con identificadores de versión coincidentes"), esc_o12, "ca2", lambda m: (_foraneo(m), _src_set(m, source_asset_id="yq", source_asset_version_id="yq", source_upload_event_id="ey")), "I27")]
# ---- v13: A54 a A65 (el motor rechaza antes de escribir), P21 a P26 y ADV11 a ADV16 ----
def _fx13(cls=Motor):
    """Estado válido previo a la reutilización: a1 (raíz de U, v1) con su versión a1b (de D), ax (de Z) con el mismo número de versión, au (de U), todos en la pieza P1, y la copia de destino ca (P2) lista."""
    m, x = _base(cls); _intro_cv(x, m, "cvm", "A"); x.op("registrar_asset", lambda: m.registrar_asset("a1", "cvm", "U"))
    x.op("modificar", lambda: m.modificar_asset("cvm", "cvm2", "a1b", "a1", "D"), prev="cvm", nueva="cvm2", actor="D", campo="arte")
    _intro_cv(x, m, "cvx", "B"); x.op("registrar_asset", lambda: m.registrar_asset("ax", "cvx", "Z"))
    _intro_cv(x, m, "cvu", "B"); x.op("registrar_asset", lambda: m.registrar_asset("au", "cvu", "U"))
    _intro_cv(x, m, "cvq", "B", pieza="P5"); x.op("registrar_asset", lambda: m.registrar_asset("aq", "cvq", "Pm"))
    _intro_cv(x, m, "ca", "W", pieza="P2", refs={"master": "cvm"}); return m, x
def _ec(m, aid): return _ev_carga(m, aid)["id"]
def _swap_carga(m): m.assets["a1"]["evento_carga"], m.assets["ax"]["evento_carga"] = m.assets["ax"]["evento_carga"], m.assets["a1"]["evento_carga"]
def _quita_directa(m):
    for k in [b["id"] for b in m.at.values() if b["rel"] == "directa" and b["fuente"] == "asset" and b.get("asset") == "a1"]: del m.at[k]
ART_RECH = [("K47-A54", "el evento original de carga pertenece a otro asset de la misma organización y pieza", lambda m: _set(m.assets["a1"], evento_carga=_ec(m, "au")), "corresponde a otro asset"),
            ("K47-A55", "el evento original de carga pertenece a otro asset con el mismo número de versión", lambda m: _set(m.assets["a1"], evento_carga=_ec(m, "ax")), "corresponde a otro asset"),
            ("K47-A56", "el evento original de carga es el de otra versión del mismo asset raíz", lambda m: _set(m.assets["a1"], evento_carga=_ec(m, "a1b")), "otra versión del mismo asset"),
            ("K47-A57", "la atribución directa del uploader pertenece a otro evento de carga del mismo asset", lambda m: _set(_directa(m, "a1"), evento=_ec(m, "a1b")), "pertenece a otro evento de carga"),
            ("K47-A58", "la atribución directa pertenece a otro asset de la misma organización", lambda m: _set(_directa(m, "a1"), asset="au"), "pertenece a otro asset"),
            ("K47-A59", "la atribución directa pertenece a otro uploader", lambda m: _set(_directa(m, "a1"), persona="Z"), "pertenece a otro uploader"),
            ("K47-A60", "el actor del evento de carga no coincide con el uploader declarado", lambda m: _set(_carga(m, "a1"), actor="Z"), "no coincide con el uploader"),
            ("K47-A61", "el evento de carga es correcto pero está asociado a otra versión de copy", lambda m: _set(_carga(m, "a1"), version="cvu"), "otra versión de copy"),
            ("K47-A62", "el evento de carga es correcto pero está asociado a otra pieza", lambda m: _set(_carga(m, "a1"), pieza="P5"), "otra pieza"),
            ("K47-A63", "el uploader original no tiene membresía activa", lambda m: _set(m.members["U"], activo=False), "no tiene membresía activa"),
            ("K47-A64", "evento de carga y uploader correctos pero la atribución directa no existe", _quita_directa, "no existe la atribución directa"),
            ("K47-A65", "la referencia al evento de carga se intercambia con la de otro asset después de construir la cadena", _swap_carga, "corresponde a otro asset")]
ART_RECH_IDS = [r[0] for r in ART_RECH]
def _intento(m, origen="a1"):
    antes = _estado_completo(m)
    try: m.registrar_asset("a2", "ca", "W", reused_from=origen); return None, antes
    except ReutilizacionInvalida as ex: return str(ex), antes
def _bloqueada(m, vid):
    """E nulo, procedencia no completa y ni impacto ni publicación posibles sobre la versión `vid`."""
    r = calcular_E_verificado(m, vid)
    try: evaluar_impacto(m, vid); imp = False
    except ProcedenciaIncompleta: imp = True
    return (not r["completa"]) and r["E"] is None and imp and not puede_publicar(m, vid)
def correr_mutaciones_rechazo():
    """A54 a A65: cada una parte de un estado válido (en el que la reutilización se acepta y el auditor no halla violaciones), altera UNA relación del origen, y exige: el motor rechaza antes de escribir, el error identifica la relación, el estado completo queda idéntico, E es nulo y no hay impacto ni publicación."""
    res = []
    for mid, nom, corrompe, kw in ART_RECH:
        try:
            m0, x0 = _fx13(Motor); msg0, _ = _intento(m0); e0 = x0.E("ca") if False else calcular_E_verificado(m0, "ca"); inicial = msg0 is None and e0["completa"] and e0["E"] is not None and not auditar_E(snapshot(m0), m0.calcular_E("ca"), "ca") and not _hall_arte_exactas(snapshot(m0), "ca")
            m, x = _fx13(Motor); previo = _estado_completo(m); corrompe(m); cambio = _estado_completo(m) != previo; msg, antes = _intento(m)
            rechaza = msg is not None; atomico = _estado_completo(m) == antes and len(m.ev) == len(antes["ev"]) and len(m.at) == len(antes["at"]) and len(m.assets) == len(antes["assets"]) and "a2" not in m.assets
            ident = rechaza and kw in msg; bloq = _bloqueada(m, "ca") and _bloqueada(m, "cvm")
            err = None
        except Exception as ex: inicial = cambio = rechaza = atomico = ident = bloq = False; msg = ""; err = "%s: %s" % (type(ex).__name__, str(ex)[:60])
        det = bool(inicial and cambio and rechaza and atomico and ident and bloq and err is None)
        res.append(dict(id=mid, mut=nom, esp="rechazo del motor con «%s»" % kw, kw=kw, obs=("rechazada: " + (msg or "")[:150]) if rechaza else ("ACEPTADA" if err is None else "ERROR " + err), det=det, valido=bool(inicial), cambio=bool(cambio), err=err, rechaza=rechaza, atomico=atomico, ident=ident, bloq=bloq))
    return res

def _pos13(m, x, src="a1", cv="ca", aid="a2"):
    e = x.E(cv); est = snapshot(m); ev = m.ev[m.assets[aid]["evento_reutilizacion"]]; rz = _raiz_t(m, src); eo = _ev_carga(m, rz)
    return [("el motor registra la reutilización", True, aid in m.assets), ("asset raíz y versión exacta de la raíz", (rz, rz), (ev["source_root_asset_id"] if False else ev["source_root_asset_version_id"], m.assets[aid]["source_root_asset_version_id"])),
            ("evento original de carga = el de la raíz", eo["id"], ev["source_upload_event_id"]), ("el evento de carga apunta al asset raíz y a su versión exacta", (rz, rz), (eo["asset"], eo["asset_version_id"])),
            ("uploader original = actor del evento de carga de la raíz", (eo["actor"], eo["actor"]), (ev["source_uploader_id"], m.assets[aid]["uploader_original"])), ("atribución directa de la raíz, de ese uploader y de ese evento", _atr_dir(m, eo["actor"], rz), ev["source_attribution_id"]),
            ("el reutilizador figura distinto del uploader original", True, m.assets[aid]["reutilizador"] != m.assets[aid]["uploader_original"]), ("el auditor no halla violaciones", [], auditar_E(est, m.calcular_E(cv), cv) + _hall_arte_exactas(est, cv)), ("E completo", True, e["completa"])]
def esc_p21(cls=Motor):
    m, x = _fx13(cls); x.op("registrar_asset", lambda: m.registrar_asset("a2", "ca", "W", reused_from="a1")); return m, x, _pos13(m, x)
def esc_p22(cls=Motor):
    m, x = _fx13(cls); x.op("registrar_asset", lambda: m.registrar_asset("a2", "ca", "W", reused_from="a1")); _intro_cv(x, m, "cb", "D", pieza="P3", refs={"master": "cvx"}); x.op("registrar_asset", lambda: m.registrar_asset("a3", "cb", "D", reused_from="ax"))
    asr = _pos13(m, x) + _pos13(m, x, "ax", "cb", "a3") + [("dos assets distintos con el mismo número de versión", (1, 1, True), (m.assets["a1"]["version_asset"], m.assets["ax"]["version_asset"], m.assets["a2"]["source_upload_event_id"] != m.assets["a3"]["source_upload_event_id"])),
                                                         ("cada reutilización conserva su uploader original", ("U", "Z"), (m.assets["a2"]["uploader_original"], m.assets["a3"]["uploader_original"]))]
    return m, x, asr
def esc_p23(cls=Motor):
    m, x = _fx13(cls); ok0 = _intento(copy.deepcopy(m))[0] is None; _swap_carga(m); msg, antes = _intento(m)
    return m, x, [("con los dos eventos de carga válidos la reutilización se acepta", True, ok0), ("al intercambiar los eventos de carga de dos assets el motor rechaza", True, msg is not None and "corresponde a otro asset" in msg),
                  ("no se escribió ningún registro", True, _estado_completo(m) == antes), ("E de la versión de origen queda nulo y bloqueado", True, _bloqueada(m, "cvm"))]
def esc_p24(cls=Motor):
    m, x = _fx13(cls); x.op("registrar_asset", lambda: m.registrar_asset("a2", "ca", "W", reused_from="a1")); _intro_cv(x, m, "cb", "D", pieza="P3", refs={"master": "ca"}); x.op("registrar_asset", lambda: m.registrar_asset("a3", "cb", "D", reused_from="a2"))
    _intro_cv(x, m, "cc", "B", pieza="P4", refs={"master": "cb"}); x.op("registrar_asset", lambda: m.registrar_asset("a4", "cc", "B", reused_from="a3")); eo = _ev_carga(m, "a1"); asr = _pos13(m, x, "a3", "cc", "a4")
    return m, x, asr + [("los tres niveles conservan el evento original y el uploader de la raíz", [(eo["id"], "U")] * 3, [(m.assets[k]["source_upload_event_id"], m.assets[k]["uploader_original"]) for k in ("a2", "a3", "a4")]), ("la raíz de los tres niveles es a1", ["a1"] * 3, [m.assets[k]["source_root_asset_version_id"] for k in ("a2", "a3", "a4")])]
def esc_p25(cls=Motor):
    m, x = _fx13(cls); x.op("registrar_asset", lambda: m.registrar_asset("a2", "ca", "W", reused_from="a1")); e = x.E("ca"); est = snapshot(m)
    return m, x, _pos13(m, x) + [("el motor y el auditor reconstruyen la misma cadena", m.cadena_identidad("a2"), cadena_identidad_independiente(est, "a2")), ("el E del motor coincide con el recalculado por el auditor", sorted(_E(est, "ca")), sorted(e["E"] or {})),
                                ("el auditor no usa funciones del motor", [], _compartidas())]
def esc_p26(cls=Motor):
    m, x = _fx13(cls); ok_au = not [v for v in auditar_E(snapshot(m), m.calcular_E("cvu"), "cvu")]; _set(m.assets["a1"], evento_carga=_ec(m, "au")); msg, antes = _intento(m)
    return m, x, [("el evento de carga ajeno y su atribución son válidos para su propio asset", True, ok_au), ("la reutilización con el evento de otro asset se rechaza", True, msg is not None and "corresponde a otro asset" in msg), ("sin escritura alguna", True, _estado_completo(m) == antes and "a2" not in m.assets)]
ESC_ARTE += [("P21", "reutilización válida con asset raíz, versión, evento de carga, uploader y atribución exactos", esc_p21), ("P22", "dos assets de la misma organización y pieza con el mismo número de versión", esc_p22), ("P23", "dos eventos de carga válidos de assets distintos: intercambiarlos provoca rechazo", esc_p23),
             ("P24", "cadena de tres niveles con evento de carga y uploader de la raíz", esc_p24), ("P25", "reutilización válida con el auditor independiente coincidente", esc_p25), ("P26", "evento de carga y atribución válidos pero de otro asset: rechazo sin escritura", esc_p26)]

class _Forzado(_Ciego):
    """Motor que acepta cualquier reutilización: reproduce la validación débil de la v12 (toma el evento de carga guardado en el origen y la atribución por el asset del propio evento) y no revalida la procedencia."""
    def _verificar_final(s, op, aid): pass
    def _validar_reutilizacion(s, aid, copy_version, uploader, reused_from):
        o = s.assets[reused_from]; ue = o["evento_carga_original"] if o["tipo"] == "reutilizado" else o["evento_carga"]; e = s.ev.get(ue); up = e["actor"] if e else None
        at0 = [b["id"] for b in s.at.values() if e and b["persona"] == up and b["evento"] == ue and b["rel"] == "directa" and b.get("asset") == e.get("asset")]
        return ue, up, (at0[0] if at0 else None)
def _adv13(nombre, mid, codigo):
    corrompe = [r[2] for r in ART_RECH if r[0] == mid][0]
    def f():
        m, x = _fx13(_Forzado); corrompe(m); m.registrar_asset("a2", "ca", "W", reused_from="a1"); r = m.calcular_E("ca"); est = snapshot(m)
        cods = sorted({c[0] for c in auditar_E(est, r, "ca")}); v = calcular_E_verificado(m, "ca")
        try: evaluar_impacto(m, "ca"); falla = False
        except ProcedenciaIncompleta: falla = True
        return dict(id=nombre[0], nombre=nombre[1], motor_acepta=bool(r["completa"]) and r["E"] is not None and "a2" in m.assets, auditor=codigo in cods, E_bloqueado=(not v["completa"]) and v["E"] is None, impacto_falla=falla, no_publica=not puede_publicar(m, "ca"), codigos=cods)
    return f
ADV += [_adv13(("ADV11", "evento de carga de otro asset de la misma organización y pieza (A54)"), "K47-A54", "I23"), _adv13(("ADV12", "evento de carga de otro asset con el mismo número de versión (A55)"), "K47-A55", "I23"),
        _adv13(("ADV13", "atribución directa de otro evento de carga del mismo asset (A57)"), "K47-A57", "I24"), _adv13(("ADV14", "atribución directa de otro asset de la misma organización (A58)"), "K47-A58", "I24"),
        _adv13(("ADV15", "actor del evento de carga distinto del uploader declarado (A60)"), "K47-A60", "I23"), _adv13(("ADV16", "referencia al evento de carga intercambiada con otro asset (A65)"), "K47-A65", "I23")]

def correr_adversariales():
    out = []
    for f in ADV:
        r = f(); r["ok"] = r["motor_acepta"] and r["auditor"] and r["E_bloqueado"] and r["impacto_falla"] and r["no_publica"]; out.append(r)
    return out

def _estado_final(m): return repr(snapshot(m))

def correr_escenarios():
    """Los 12 escenarios más las comprobaciones de uniformidad y metamorfismo, con el motor correcto."""
    out = []
    for cod, nombre, fn in ESCENARIOS + [("U", "uniformidad entre copy, brief y promoción", esc_unif), ("S", "independencia de la similitud textual", esc_meta), ("X", "resolutor no independiente rechazado", esc_indep), ("R", "cada regla R1 a R9 impide resolver", esc_Rtodas), ("RS", "resoluciones inmutables y cadena de reconsideración", esc_resol)]:
        try:
            m, x, asr = fn(Motor); fallos = [a for a in asr if a[1] != a[2]]
            out.append(dict(id=cod, nombre=nombre, ok=not fallos and not x.viol, asr=asr, viol=[v[0] for v in x.viol], pasos=len(x.pasos), fallos=[(a[0], a[1], a[2]) for a in fallos]))
        except Exception as ex: out.append(dict(id=cod, nombre=nombre, ok=False, asr=[], viol=["EXCEPCIÓN %s" % type(ex).__name__], pasos=0, fallos=[(str(ex)[:80], "", "")]))
    return out

BLOQ_IDS = {m[0] for m in ART_MUT[16:]}
def _correr_lista(lista):
    """Cada mutación parte de un escenario válido (motor correcto), cambia UNA cosa (motor defectuoso) y exige el código y la condición específica."""
    res = []
    for mid, nom, inv, cls, esc, *kw in lista:
        kw = kw[0] if kw else ""
        try: m0, x0, a0 = esc(Motor); inicial_ok = not x0.viol and all(a[1] == a[2] for a in a0); f0 = _estado_final(m0)
        except Exception as ex: inicial_ok = False; f0 = ""
        try:
            m1, x1, a1 = esc(cls); cods = sorted({v[0] for v in x1.viol}); err = None; cambio = _estado_final(m1) != f0 or any(a[1] != a[2] for a in a1) or bool(cods)
            msg = [v[1] for v in x1.viol if v[0] == inv and kw in v[1]]
        except Exception as ex: cods = []; msg = []; err = "%s: %s" % (type(ex).__name__, str(ex)[:60]); cambio = False
        bloq = None
        if err is None and mid in BLOQ_IDS:
            bloq = any((not m1.calcular_E(v)["completa"]) and (not calcular_E_verificado(m1, v)["completa"]) and calcular_E_verificado(m1, v)["E"] is None for v in m1.v if m1.v[v]["fuente"] == "copy")
        det = inicial_ok and err is None and cambio and bool(msg) and (bloq is not False)
        res.append(dict(bloq=bloq, id=mid, mut=nom, esp=inv, kw=kw, obs=("detectada por " + ", ".join(cods) + (" · «%s»" % msg[0][:110] if msg else "")) if cods else ("ERROR de ejecución: %s" % err if err else "no detectada"), det=bool(det), valido=inicial_ok, cambio=bool(cambio), err=err))
    return res
def correr_mutaciones_k47(): return _correr_lista(K47_MUT)
def correr_mutaciones_resoluciones(): return _correr_lista(RES_MUT)
def correr_mutaciones_assets(): return _correr_lista(ART_MUT)
def correr_positivos_arte():
    out = []
    for cod, nombre, fn in ESC_ARTE:
        try: m, x, asr = fn(Motor); fallos = [a for a in asr if a[1] != a[2]]; out.append(dict(id=cod, nombre=nombre, ok=not fallos and not x.viol, asr=asr, viol=[v[0] for v in x.viol], fallos=[(a[0], a[1], a[2]) for a in fallos]))
        except Exception as ex: out.append(dict(id=cod, nombre=nombre, ok=False, asr=[], viol=["EXCEPCIÓN %s" % type(ex).__name__], fallos=[(str(ex)[:80], "", "")]))
    return out

def correr_mutaciones_k45(M):
    res = []; positivos = []
    for nombre, T in variantes_positivas_k45():
        v = evaluar_k45_estructural(T, M); positivos.append((nombre, v))
    for mid, nom, cod, fn in K45_MUT:
        T0 = fixture_k45(); v0 = evaluar_k45_estructural(T0, M); T = copy.deepcopy(T0)
        try: fn(T); err = None
        except Exception as ex: err = "%s: %s" % (type(ex).__name__, str(ex)[:60])
        cambio = T != T0
        try: v1 = evaluar_k45_estructural(T, M); e2 = None
        except Exception as ex: v1 = []; e2 = "%s: %s" % (type(ex).__name__, str(ex)[:60])
        codes = sorted({c[0] for c in v1})
        det = (not v0) and cambio and err is None and e2 is None and cod in codes
        res.append(dict(id=mid, mut=nom, esp=cod, obs=("rechazado con " + ", ".join(codes)) if codes else ("ERROR: %s" % (err or e2) if (err or e2) else "ACEPTADO (no detectado)"), det=bool(det), valido=not v0, cambio=cambio, err=err or e2))
    return res, positivos

# =====================================================================================================
# v13 (IG5-102, IG5-103): integridad referencial de las relaciones source_* y de creación de assets
# Datos del diseño físico (solo documentales). El verificador los contrasta con el contrato 4.4.9 y la sección 4.4.15;
# la sección 4.4.15 se genera a partir de estos mismos datos y la mutación de cualquiera de las dos partes se detecta.
# =====================================================================================================
def _rs(id_, origen, pares, destino, accion, momento, garantiza, prueba, fk):
    return dict(id=id_, origen=origen, locales=tuple(p[0] for p in pares), destino=destino, ref=tuple(p[1] for p in pares), pares=dict(pares), accion=accion, momento=momento, garantiza=garantiza, prueba=prueba, fk=fk)
RELACIONES_SOURCE = [
    _rs("RS-01", "contribution_events", (("organization_id", "organization_id"), ("source_asset_version_id", "id"), ("source_asset_id", "asset_lineage_id"), ("source_root_asset_version_id", "root_asset_version_id")), "creative_assets", "RESTRICT", "inmediata",
        "existencia del asset de origen; misma organización; versión exacta (fila); asset lógico exacto de esa versión; raíz exacta de su cadena", "K47-A33, K47-A34, K47-A35, K47-A45", ["FK01", "FK03", "FK04", "FK10", "FK11", "FK13"]),
    _rs("RS-02", "contribution_events", (("organization_id", "organization_id"), ("source_upload_event_id", "id"), ("source_root_asset_version_id", "creative_asset_id"), ("source_uploader_id", "contributor_id")), "contribution_events", "RESTRICT", "inmediata",
        "existencia del evento de carga; misma organización; el evento es de la fila raíz exacta (solo los eventos de carga tienen creative_asset_id); uploader igual al actor del evento", "K47-A36, K47-A37, K47-A38, K47-A54, K47-A55, K47-A56, K47-A60", ["FK02", "FK07", "FK09", "FK12"]),
    _rs("RS-03", "contribution_events", (("organization_id", "organization_id"), ("source_attribution_id", "id"), ("source_upload_event_id", "contribution_event_id"), ("source_uploader_id", "contributor_id"), ("source_root_asset_version_id", "origin_asset_id"), ("source_attribution_relation", "relation")), "copy_version_provenance", "RESTRICT", "inmediata",
        "existencia de la atribución; misma organización; atribución de ese evento, de ese uploader, del asset raíz exacto y de relación directa", "K47-A57, K47-A58, K47-A59, K47-A64", ["FK08", "FK12"]),
    _rs("RS-04", "creative_assets", (("organization_id", "organization_id"), ("lineage_parent_asset_id", "id"), ("asset_lineage_id", "asset_lineage_id"), ("root_asset_version_id", "root_asset_version_id")), "creative_assets", "RESTRICT", "inmediata",
        "una versión modificada conserva el asset lógico y la raíz de la versión anterior", "K47-A35, K47-A56", ["FK05"]),
    _rs("RS-05", "creative_assets", (("organization_id", "organization_id"), ("reused_from_asset_id", "id"), ("root_asset_version_id", "root_asset_version_id")), "creative_assets", "RESTRICT", "inmediata",
        "un asset reutilizado hereda la raíz exacta de su origen", "K47-A39, K47-A48", ["FK06"]),
    _rs("RS-06", "creative_assets", (("organization_id", "organization_id"), ("upload_event_id", "id"), ("id", "creative_asset_id"), ("uploader_id", "contributor_id"), ("piece_id", "asset_piece_id"), ("copy_version_id", "asset_copy_version_id")), "contribution_events", "NO ACTION", "DEFERRABLE INITIALLY DEFERRED",
        "el evento de carga de la fila es de esa fila, de su uploader, pieza y versión de copy; relación circular con el evento: se resuelve con esta única FK diferida", "K47-A19, K47-A20, K47-A22, K47-A60, K47-A61, K47-A62", ["FK13"]),
    _rs("RS-07", "creative_assets", (("organization_id", "organization_id"), ("reuse_event_id", "id"), ("reused_from_asset_id", "source_asset_version_id"), ("piece_id", "copy_version_piece_id"), ("copy_version_id", "copy_version_id")), "contribution_events", "RESTRICT", "inmediata",
        "el evento de reutilización es propio del asset, referencia el mismo origen y la misma pieza y versión exacta de copy de destino", "K47-A25, K47-A46, K47-A47", ["FK09"]),
    _rs("RS-08", "contribution_events", (("organization_id", "organization_id"), ("source_root_asset_version_id", "id"), ("source_upload_event_id", "upload_event_id")), "creative_assets", "RESTRICT", "inmediata",
        "el evento original de carga referenciado es exactamente el upload_event_id de la fila raíz (v14: cierra la brecha de que otro evento de carga de la misma fila, o de otra, satisficiera RS-02 y RS-03)", "K47-A54, K47-A55, CHAIN-04, CHAIN-18", ["FK19", "FK25"]),
]
UNICAS_SOURCE = {"contribution_events": [("organization_id", "id", "creative_asset_id", "contributor_id"), ("organization_id", "id", "creative_asset_id", "contributor_id", "asset_piece_id", "asset_copy_version_id"), ("organization_id", "id", "source_asset_version_id", "copy_version_piece_id", "copy_version_id")],
                 "copy_version_provenance": [("organization_id", "id", "contribution_event_id", "contributor_id", "origin_asset_id", "relation")],
                 "creative_assets": [("organization_id", "id", "asset_lineage_id", "root_asset_version_id"), ("organization_id", "id", "root_asset_version_id"), ("organization_id", "id", "upload_event_id")]}
# v14: restricciones únicas propias (no son destino de una FK): impiden que dos assets compartan el mismo evento de reutilización
UNICAS_PROPIAS_SOURCE = {"creative_assets": [("organization_id", "reuse_event_id")]}
# Inventario de las columnas source_* de contribution_events y de las relaciones indirectas (id de relación que las cubre)
INVENTARIO_SOURCE = [
 ("source_hash", "— (valor de integridad, no una referencia)", "—", "hash hexadecimal de 64 caracteres del origen (CHECK de formato)", "ninguna FK: el valor no identifica un registro; la identidad del origen la fijan RS-01, RS-02 y RS-03"),
    ("source_asset_id", "creative_assets.asset_lineage_id", "RS-01", "asset lógico de la versión de origen; la organización y el asset lógico los fija RS-01", "ninguna: FK declarativa compuesta"),
    ("source_asset_version_id", "creative_assets.id", "RS-01", "versión exacta (fila) del asset de origen; pieza y versión de copy del origen las fija la propia fila", "ninguna: FK declarativa compuesta"),
    ("source_root_asset_version_id", "creative_assets.root_asset_version_id, creative_assets.id y contribution_events.creative_asset_id", "RS-01, RS-02, RS-03, RS-08", "fila raíz exacta de la cadena; ancla las cuatro FK", "ninguna: FK declarativa compuesta"),
    ("source_upload_event_id", "contribution_events.id y creative_assets.upload_event_id", "RS-02, RS-08", "evento original de carga de la raíz: RS-08 lo ata al upload_event_id de la fila raíz y RS-02 a su creative_asset_id y su actor", "ninguna: autorreferencia declarativa; no hay ciclo de inserción (el evento original es anterior)"),
    ("source_uploader_id", "contribution_events.contributor_id y copy_version_provenance.contributor_id", "RS-02, RS-03", "uploader original, igual al actor del evento de carga y al de la atribución", "ninguna: FK declarativa compuesta"),
    ("source_attribution_id", "copy_version_provenance.id", "RS-03", "atribución directa original (evento, uploader, asset raíz y relación 'directa')", "ninguna: FK declarativa; el ciclo de tablas con copy_version_provenance se evita agregando la FK por ALTER en 3.x"),
    ("source_attribution_relation", "copy_version_provenance.relation", "RS-03", "constante 'directa' (CHECK) que permite fijar la relación en la FK", "ninguna: FK declarativa compuesta"),
    ("creative_assets.asset_lineage_id", "creative_assets.asset_lineage_id", "RS-04", "asset lógico: igual al de la versión anterior de la misma línea", "ninguna: FK declarativa compuesta"),
    ("creative_assets.lineage_parent_asset_id", "creative_assets.id", "RS-04", "versión anterior exacta de la misma línea y de la misma raíz", "ninguna: FK declarativa compuesta"),
    ("creative_assets.root_asset_version_id", "creative_assets.id", "RS-04, RS-05", "raíz exacta heredada de la versión anterior o del origen", "ninguna: FK declarativa compuesta"),
    ("creative_assets.reused_from_asset_id", "creative_assets.id", "RS-05", "origen exacto de un asset reutilizado, con la raíz heredada", "ninguna: FK declarativa compuesta"),
    ("creative_assets.upload_event_id", "contribution_events.id", "RS-06, RS-08", "relación indirecta: el evento de carga de la fila", "FK diferida: ciclo de inserción real con contribution_events.creative_asset_id"),
    ("creative_assets.reuse_event_id", "contribution_events.id", "RS-07", "relación indirecta: el evento propio de la reutilización", "ninguna: FK inmediata; el evento se inserta antes que el asset"),
]
# Excepciones: el único campo del modelo sin columna física, con su mecanismo alternativo y su prueba negativa específica en K45
EXCEPCIONES_SOURCE = [("source_asset_version (entero del modelo en memoria)", "no existe como columna: dos assets distintos pueden tener el mismo número", "no se almacena: el número es creative_assets.asset_version de la fila identificada por RS-01 y nunca sustituye a la identidad", "K47-A34 (mismo número de versión) y K47-A42 (intercambio con igual número)", "K45")]
# Ciclos entre tablas y su resolución (4.4.15): tablas, aristas, tipo de ciclo y orden de inserción
CICLOS_SOURCE = [("C-1", ("contribution_events", "copy_version_provenance"), "RS-03 contra contribution_event_id de copy_version_provenance", "solo de creación", "contribution_events (2.1) y copy_version_provenance (2.3) se crean antes; la FK RS-03 se agrega por ALTER en 3.x; no hay ciclo de filas: la atribución original es anterior a la reutilización"),
                 ("C-2", ("contribution_events", "creative_assets"), "RS-01, RS-07, RS-08 contra creative_asset_id y las FK de creative_assets", "solo de creación", "las FK se agregan por ALTER en 3.x; el evento de reutilización se inserta antes que el asset reutilizado y no lo referencia; no hay ciclo de filas"),
                 ("C-3", ("contribution_events", "creative_assets"), "RS-06 contra la FK de contribution_events a creative_assets", "de creación y de filas", "el asset de una carga y su evento de carga se referencian entre sí: ninguna FK inmediata permite insertar la primera fila; RS-06 es DEFERRABLE INITIALLY DEFERRED y se verifica al confirmar")]
ORDEN_INSERCION = [("carga nueva", 1, "creative_assets", "—", "RS-06 (diferida, al paso 2)"), ("carga nueva", 2, "contribution_events", "creative_asset_id → paso 1", "—"), ("carga nueva", 3, "copy_version_provenance", "contribution_event_id → paso 2", "—"),
                   ("modificación", 1, "creative_assets", "RS-04 → versión anterior (preexistente)", "RS-06 (diferida, al paso 2)"), ("modificación", 2, "contribution_events", "creative_asset_id → paso 1", "—"), ("modificación", 3, "copy_version_provenance", "contribution_event_id → paso 2", "—"),
                   ("reutilización", 1, "contribution_events", "RS-01, RS-02, RS-03, RS-08 → origen, raíz, evento y atribución (preexistentes)", "—"), ("reutilización", 2, "creative_assets", "RS-05 → origen (preexistente); RS-07 → paso 1", "—"), ("reutilización", 3, "copy_version_provenance", "contribution_event_id → paso 1", "—")]

# ===== v13: descripciones de las mutaciones estructurales FK01 a FK15 =====
FK_DESC = [("FK01", "eliminar la FK de source_asset_version_id (RS-01)", "K32"), ("FK02", "eliminar otra FK requerida (RS-04, linaje del asset)", "K32"),
 ("FK03", "FK RS-01 sin organization_id", "K44"), ("FK04", "columnas de destino invertidas en RS-01", "K44"),
 ("FK05", "destino de RS-02 sin la unicidad suficiente (org, id, creative_asset_id, contributor_id)", "K44"), ("FK06", "tipo incompatible de source_attribution_relation (RS-03)", "K44"),
 ("FK07", "source_upload_event_id sin FK (RS-02) ni mecanismo alternativo", "K32"), ("FK08", "source_attribution_id sin FK (RS-03) ni mecanismo alternativo", "K32"),
 ("FK09", "RS-06 (evento de carga del asset) sin organization_id: equivalente declarativo del trigger diferido sin validar la organización", "K44"),
 ("FK10", "RS-01 sin el asset exacto (source_asset_id → asset_lineage_id): equivalente declarativo del trigger que no valida el asset", "K32"),
 ("FK11", "RS-01 con source_asset_id y source_asset_version_id intercambiados: equivalente de no validar la versión exacta", "K45"),
 ("FK12", "RS-03 con source_uploader_id sustituido: equivalente de no validar uploader y atribución", "K45"),
 ("FK13", "RS-01 con ON DELETE RESTRICT cambiado a SET NULL: referencia huérfana tras una operación de corrección", "K32"),
 ("FK14", "excepción de K32 sin la referencia a K45 que la justifica", "K32"), ("FK15", "excepción de K45 con una prueba negativa inexistente", "K45")]

FK_DESC += [("FK16", "RS-05 eliminada (un asset reutilizado no hereda la raíz exacta de su origen)", "K32"), ("FK17", "RS-06 eliminada (el evento de carga de la fila no queda atado a su asset, uploader, pieza y versión de copy)", "K32"),
 ("FK18", "RS-07 eliminada (el evento de reutilización deja de ser propio del asset)", "K32"), ("FK19", "RS-08 eliminada (el evento de carga referenciado puede ser otro evento de la misma raíz)", "K32"),
 ("FK20", "RS-02 sin source_uploader_id (columna source_* y de destino contributor_id)", "K32"), ("FK21", "RS-03 sin source_attribution_relation (la atribución puede no ser la directa)", "K32"),
 ("FK22", "RS-03 sin source_root_asset_version_id (la atribución puede ser de otra raíz)", "K32"), ("FK23", "RS-08 con las columnas de destino en otro orden", "K44"),
 ("FK24", "destino de RS-05 sin su clave única (organization_id, id, root_asset_version_id)", "K44"), ("FK25", "destino de RS-08 sin su clave única (organization_id, id, upload_event_id)", "K44"),
 ("FK26", "RS-02 sin organization_id", "K44"), ("FK27", "RS-07 sin la pieza (piece_id y copy_version_piece_id)", "K32"), ("FK28", "RS-06 sin la versión de copy (copy_version_id y asset_copy_version_id)", "K32"),
 ("FK29", "asset sustituido: RS-05 con lineage_parent_asset_id en lugar de reused_from_asset_id", "K32"), ("FK30", "versión sustituida: RS-07 con previous_asset_id en lugar de reused_from_asset_id", "K32"),
 ("FK31", "evento sustituido: RS-06 con reuse_event_id en lugar de upload_event_id", "K32"), ("FK32", "uploader sustituido: RS-02 con source_uploader_id y source_upload_event_id intercambiados", "K45"),
 ("FK33", "atribución sustituida: RS-03 con source_attribution_id y source_uploader_id intercambiados", "K45"), ("FK34", "relación de origen cruzada: RS-03 apunta a brief_field_attributions", "K32"),
 ("FK35", "borrado indebido: RS-02 con ON DELETE CASCADE", "K32"), ("FK36", "actualización indebida: RS-01 con ON UPDATE CASCADE", "K32"), ("FK37", "ciclo de inserción: la reutilización referencia en el paso 2 un registro del paso 2", "K44"),
 ("FK38", "FK diferida mal aplicada: RS-05 declarada DEFERRABLE INITIALLY DEFERRED sin ciclo de filas", "K32"), ("FK39", "excepción sin mecanismo alternativo", "K32"), ("FK40", "excepción sin prueba negativa", "K45"),
 ("FK41", "se elimina la restricción única propia de creative_assets (organization_id, reuse_event_id)", "K32")]
for _r in RELACIONES_SOURCE: _r["fk"] = [f for f, d, _c in FK_DESC if _r["id"] in d]   # v14: la correspondencia se deriva de la descripción de cada mutación (en la v13 estaba escrita a mano y era inexacta)

# ===== v14 BEGIN: mutaciones de eslabones intermedios (CHAIN-01 a CHAIN-20) =====
def _fx14(cls=Motor):
    """Cadena a1 (raíz de U, P1) → a2 (reutiliza W, P2) → a3 (reutiliza D, P3); destino del intento: a4 (B, P4) desde a3. Incluye a1b (modificado de a1) y ay (reutilizado de ax, P6)."""
    m, x = _fx13(cls)
    x.op("registrar_asset", lambda: m.registrar_asset("a2", "ca", "W", reused_from="a1"))
    _intro_cv(x, m, "cb", "D", pieza="P3", refs={"master": "ca"}); x.op("registrar_asset", lambda: m.registrar_asset("a3", "cb", "D", reused_from="a2"))
    _intro_cv(x, m, "cc", "B", pieza="P4", refs={"master": "cb"})
    _intro_cv(x, m, "cy", "Pm", pieza="P6", refs={"master": "cvx"}); x.op("registrar_asset", lambda: m.registrar_asset("ay", "cy", "D", reused_from="ax"))
    return m, x
def _ev_pr(m, aid, **kw): m.ev[m.assets[aid]["evento_reutilizacion"]].update(**kw)
def _dup_atr(m, aid):
    b = [t for t in m.at.values() if t.get("asset") == aid and t["rel"] == "directa" and t["fuente"] == "copy"][0]; n = dict(b); n["id"] = "dup_" + b["id"]; m.at[n["id"]] = n
CHAIN = [
 ("CHAIN-01", "asset inmediato incorrecto, raíz correcta (el eslabón a3 apunta a a1 saltando a a2)", lambda m: m.assets["a3"].update(origen="a1"), "origen", "a3"),
 ("CHAIN-02", "versión inmediata incorrecta, raíz correcta (el evento de a3 declara otra versión del origen)", lambda m: _ev_pr(m, "a3", source_asset_version=7), "versión", "a3"),
 ("CHAIN-03", "evento propio de reutilización de otro eslabón (a3 usa el evento de a2)", lambda m: m.assets["a3"].update(evento_reutilizacion=m.assets["a2"]["evento_reutilizacion"]), "evento propio", "a3"),
 ("CHAIN-04", "evento original correcto en la raíz pero referencia intermedia incorrecta (a2 referencia el evento de carga de otro asset)", lambda m: _ev_pr(m, "a2", source_upload_event_id=_ec(m, "au")), "evento de carga", "a2"),
 ("CHAIN-05", "uploader correcto en la raíz y referencia intermedia a otra persona (a2)", lambda m: _ev_pr(m, "a2", source_uploader_id="Z"), "uploader", "a2"),
 ("CHAIN-06", "atribución raíz correcta pero referencia intermedia a otra atribución (a2)", lambda m: _ev_pr(m, "a2", source_attribution_id=_atr_dir(m, "U", "au")), "atribución", "a2"),
 ("CHAIN-07", "asset intermedio de otra organización (a2)", lambda m: m.assets["a2"].update(org="Y"), "organización", "a2"),
 ("CHAIN-08", "asset intermedio de otra pieza (a2)", lambda m: m.assets["a2"].update(pieza="P9"), "pieza", "a2"),
 ("CHAIN-09", "versión de copy del asset intermedio incorrecta (a2)", lambda m: m.assets["a2"].update(copy_version="cvu"), "versión de copy", "a2"),
 ("CHAIN-10", "actor autenticado incorrecto en el evento del eslabón intermedio (a2)", lambda m: _ev_pr(m, "a2", auth="Z"), "actor autenticado", "a2"),
 ("CHAIN-11", "cadena con referencia circular (a2 apunta a a3)", lambda m: m.assets["a2"].update(origen="a3"), "ciclo", "a2"),
 ("CHAIN-12", "cadena con dos raíces posibles (a2 con origen y versión previa)", lambda m: m.assets["a2"].update(previo="ax"), "ambigua", "a2"),
 ("CHAIN-13", "referencia faltante en un eslabón intermedio (a2 sin origen)", lambda m: m.assets["a2"].update(origen=None), "referencia", "a2"),
 ("CHAIN-14", "referencia duplicada: la atribución directa del reutilizador de a2 está duplicada", lambda m: _dup_atr(m, "a2"), "duplicada", "a2"),
 ("CHAIN-15", "datos de la raíz correctos y campos source_* intermedios intercambiados entre a2 y a3", lambda m: _swap_src(m), "source_asset_version_id", "a2"),
 ("CHAIN-16", "asset modificado que pierde la raíz original (a1b sin versión anterior)", lambda m: m.assets["a1b"].update(previo=None), "versión anterior", "a1b"),
 ("CHAIN-17", "reutilización de una versión anterior en lugar de la exacta (a2 referencia la versión a1 y a1b es la vigente del origen)", lambda m: _ev_pr(m, "a2", source_asset_version_id="a1b"), "versión", "a2"),
 ("CHAIN-18", "evento de carga válido de otro asset con el mismo número de versión (a2 referencia el de ax)", lambda m: _ev_pr(m, "a2", source_upload_event_id=_ec(m, "ax")), "evento de carga", "a2"),
 ("CHAIN-19", "evento de reutilización válido de otro asset (a3 usa el de ay)", lambda m: m.assets["a3"].update(evento_reutilizacion=m.assets["ay"]["evento_reutilizacion"]), "evento propio", "a3"),
 ("CHAIN-20", "cadena de tres niveles con corrupción solo en el nivel intermedio (el evento de a2 pertenece a otra versión de copy)", lambda m: _ev_pr(m, "a2", version="cvu"), "versión de copy", "a2"),
]
def _dup_atr_asset(m, aid):
    b = [t for t in m.at.values() if t.get("asset") == aid and t["rel"] == "directa" and t["fuente"] == "asset"][0]; n = dict(b); n["id"] = "dupa_" + b["id"]; m.at[n["id"]] = n
CHAIN += [
 ("CHAIN-21", "eslabón modificado intermedio con el evento de carga de otro asset (a1b usa el de ax)", lambda m: m.assets["a1b"].update(evento_carga=_ec(m, "ax")), "evento propio", "a1b"),
 ("CHAIN-22", "eslabón modificado intermedio con otro editor que el del evento (a1b declara al uploader Z)", lambda m: m.assets["a1b"].update(uploader="Z"), "actor", "a1b"),
 ("CHAIN-23", "eslabón modificado intermedio con número de versión que no sigue al anterior (a1b declara la versión 3)", lambda m: m.assets["a1b"].update(version_asset=3), "versión anterior", "a1b"),
 ("CHAIN-24", "eslabón modificado intermedio con la atribución directa del editor duplicada (a1b)", lambda m: _dup_atr_asset(m, "a1b"), "duplicada", "a1b"),
]
_CHAIN_A1B = ("CHAIN-16", "CHAIN-21", "CHAIN-22", "CHAIN-23", "CHAIN-24")
def _swap_src(m):
    e2, e3 = _reu(m, "a2"), _reu(m, "a3")
    for k in ("source_asset_version_id", "source_asset_id", "source_asset_version"): e2[k], e3[k] = e3[k], e2[k]
def _intento14(m, origen="a3"):
    antes = _estado_completo(m)
    try: m.registrar_asset("a4", "cc", "B", reused_from=origen); return None, antes
    except ReutilizacionInvalida as ex: return str(ex), antes
def correr_mutaciones_cadena():
    """CHAIN-01 a CHAIN-20 sobre eslabones intermedios: parten de una cadena válida de tres niveles (la reutilización de a3 se acepta y el auditor no halla violaciones), alteran UNA relación y exigen rechazo, error específico, estado idéntico, E incompleto, impacto, aprobación y publicación bloqueados."""
    res = []
    for mid, nom, corrompe, kw, eslabon in CHAIN:
        try:
            m0, x0 = _fx14(Motor); msg0, _ = _intento14(m0); inicial = msg0 is None and calcular_E_verificado(m0, "cc")["completa"] and not auditar_E(snapshot(m0), m0.calcular_E("cc"), "cc") and not _hall_arte_exactas(snapshot(m0), "cc")
            m, x = _fx14(Motor); previo = _estado_completo(m); corrompe(m); cambio = _estado_completo(m) != previo
            origen = "a1b" if mid in _CHAIN_A1B else "a3"; msg, antes = _intento14(m, origen)
            rechaza = msg is not None; atomico = _estado_completo(m) == antes and "a4" not in m.assets
            ident = rechaza and kw in msg and eslabon in msg; bloq = _bloqueada(m, "cb") or _bloqueada(m, "cvm2")
            err = None
        except Exception as ex: inicial = cambio = rechaza = atomico = ident = bloq = False; msg = ""; err = "%s: %s" % (type(ex).__name__, str(ex)[:80])
        det = bool(inicial and cambio and rechaza and atomico and ident and bloq and err is None)
        res.append(dict(id=mid, mut=nom, esp="rechazo del motor con «%s» y el eslabón %s" % (kw, eslabon), kw=kw, obs=("rechazada: " + (msg or "")[:170]) if rechaza else ("ACEPTADA" if err is None else "ERROR " + err), det=det, valido=bool(inicial), cambio=bool(cambio), err=err, rechaza=rechaza, atomico=atomico, ident=ident, bloq=bool(bloq)))
    return res
# ===== v14 END =====

# ===== v14: adversariales de la cadena completa (motor forzado + auditor independiente) =====
class _Forzado14(_Forzado):
    """Motor que acepta la reutilización aunque la cadena esté corrupta: validación débil de la v12 y resolución tolerante de la raíz (cae en a1 cuando la cadena no se puede recorrer). No se usa en producción: solo demuestra que el auditor detecta lo que el motor deja pasar."""
    def _raiz_asset(s, aid):
        try: return Motor._raiz_asset(s, aid)
        except KeyError: return s.assets["a1"]
def correr_adversariales_cadena():
    out = []
    for mid, nom, corrompe, kw, eslabon in CHAIN:
        try:
            m, x = _fx14(_Forzado14); corrompe(m); origen = "a1b" if mid in _CHAIN_A1B else "a3"
            try: m.registrar_asset("a4", "cc", "B", reused_from=origen); acepta = "a4" in m.assets
            except Exception: acepta = False
            est = snapshot(m); r = m.calcular_E("cc"); hall = auditar_E(est, r, "cc"); msgs = [c[1] for c in hall]; cods = sorted({c[0] for c in hall}); v = calcular_E_verificado(m, "cc")
            try: evaluar_impacto(m, "cc"); falla = False
            except ProcedenciaIncompleta: falla = True
            det_ = any(("[eslabón %s]" % eslabon) in z for z in msgs)
            out.append(dict(id=mid.replace("CHAIN", "ADVC"), nombre=nom, motor_acepta=acepta, auditor=det_, enlace=eslabon, E_bloqueado=(not v["completa"]) and v["E"] is None, impacto_falla=falla, no_publica=not puede_publicar(m, "cc"), codigos=cods))
        except Exception as ex: out.append(dict(id=mid.replace("CHAIN", "ADVC"), nombre=nom, motor_acepta=False, auditor=False, enlace=eslabon, E_bloqueado=False, impacto_falla=False, no_publica=False, codigos=[], error="%s: %s" % (type(ex).__name__, str(ex)[:80])))
        out[-1]["ok"] = out[-1]["motor_acepta"] and out[-1]["auditor"] and out[-1]["E_bloqueado"] and out[-1]["impacto_falla"] and out[-1]["no_publica"]
    return out

# ===== v14: mutaciones de atribuciones y resoluciones (ATTR-01 a ATTR-12) =====
class _ForzRes(Motor):
    """Motor que acepta toda resolución (validación sustituida): el auditor independiente debe detectar la aceptación indebida."""
    def validar_resolucion(s, sol): return []
def _sc_res(cls=Motor, quien="B", resolutor="R", solicitante="Q", **kw):
    """v1 (A introduce el headline) → v2 (`quien` sustituye) → solicitud r1 sobre la atribución de A; no se aplica."""
    m, x = _base(cls); m.miembro("Rb", "revisor")
    x.op("introducir", lambda: m.introducir_campo("copy", None, "v1", "headline", "Compra hoy", "A", pieza="P1", arte="no_aplica"), prev=None, nueva="v1", actor="A", campo="headline")
    x.op("sustituir", lambda: m.sustituir_campo("copy", "v1", "v2", "headline", "Oferta nueva", quien), prev="v1", nueva="v2", actor=quien, campo="headline")
    a = _a_headline(m, x); mot = [k for k, ev in m.ev.items() if ev["actor"] == quien][-1]; _res(m, "r1", a, resolutor, solicitante=solicitante, motivador=mot, **kw); return m, x, a
def _sc_res_aplicada():
    m, x, a = _sc_res(); x.op("aplicar_resolucion", lambda: m.aplicar_resolucion("r1"), res="r1", vid="v2"); return m, x, a
def _aud_estado(m, tocar):
    antes = snapshot(m); tocar(m); return sorted({c[0] for c in auditar(antes, snapshot(m), dict(op="ninguna"))})
def _set_res(m, k, **kw): dict.__setitem__(m.res, k, dict(m.res[k], **kw))
def _aplicar_y_auditar(cls, quien, resolutor, solicitante, cod, **kw):
    """Regla de elegibilidad o de evidencia violada: el motor honesto rechaza (conserva la atribución, E y estado) y el motor forzado que acepta es detectado por el auditor."""
    m, x, a = _sc_res(Motor, quien, resolutor, solicitante, **kw); e0 = sorted(m.calcular_E("v2")["E"]); antes = _estado_completo(m); ok = m.aplicar_resolucion("r1")
    rechaza = (not ok) and cod in m.res["r1"]["motivos"] and m.estado(a) == "activa" and sorted(m.calcular_E("v2")["E"]) == e0
    mf, xf, af = _sc_res(_ForzRes, quien, resolutor, solicitante, **kw); xf.op("aplicar_resolucion", lambda: mf.aplicar_resolucion("r1"), res="r1", vid="v2")
    return rechaza, ("I4" in {c[0] for c in xf.viol}), sorted({c[0] for c in xf.viol})
class _AutoRetiro(Motor):
    def sustituir_campo(s, fuente, prev, nueva, campo, contenido, actor):
        r = super().sustituir_campo(fuente, prev, nueva, campo, contenido, actor)
        if not (set(s.v[prev]["campos"][campo]["contenido"].split()) & set(contenido.split())): _retirar(s, [a["id"] for a in s.activas(nueva) if a["campo"] == campo and a["rel"] == "heredada"])
        return r
def correr_mutaciones_atribucion():
    out = []
    def reg(i, nom, esp, obs, det, **kw): out.append(dict(id=i, mut=nom, esp=esp, obs=obs, det=bool(det), **kw))
    # ATTR-01/02/03: la resolución aceptada se altera, se elimina o se duplica en el almacenamiento
    m, x, a = _sc_res_aplicada(); fila = dict(m.res["r1"])
    c = _aud_estado(m, lambda m: _set_res(m, "r1", evidencia="otra evidencia")); reg("ATTR-01", "resolución modificada después de su creación", "I13", ",".join(c), "I13" in c)
    m, x, a = _sc_res_aplicada(); c = _aud_estado(m, lambda m: dict.__delitem__(m.res, "r1")); reg("ATTR-02", "resolución eliminada", "I13 e I15", ",".join(c), "I13" in c and "I15" in c)
    m, x, a = _sc_res_aplicada()
    def dup(m): n = dict(m.res["r1"], id="r1b", seq=m.tick()); n["sello"] = _sello_ind(n); dict.__setitem__(m.res, "r1b", n)
    c = _aud_estado(m, dup); reg("ATTR-03", "resolución duplicada para la misma atribución", "I15", ",".join(c), "I15" in c)
    # ATTR-04..09: elegibilidad y evidencia
    for i, nom, quien, rs, sol, cod, kw in (("ATTR-04", "resolutor que fue el editor que sustituyó", "Rb", "Rb", "Q", "R5", {}), ("ATTR-05", "resolutor que fue el solicitante", "B", "R2", "R2", "R4", {}),
                                           ("ATTR-07", "evidencia ausente", "B", "R", "Q", "V11", dict(evidencia="  ")), ("ATTR-08", "evidencia de otro campo", "B", "R", "Q", "V05", dict(campo="subheadline")), ("ATTR-09", "evidencia de otra versión", "B", "R", "Q", "V06", dict(version="v1"))):
        rj, ad, cods = _aplicar_y_auditar(Motor, quien, rs, sol, cod, **kw); reg(i, nom, "rechazo del motor con %s y aceptación forzada detectada (I4)" % cod, "rechaza=%s auditor=%s %s" % (rj, ad, cods), rj and ad)
    # ATTR-06: resolutor que heredó la contribución evaluada (v1 A → v2 Rc modifica → v3 B sustituye)
    def sc6(cls):
        m, x = _base(cls); m.miembro("Rc", "revisor")
        x.op("introducir", lambda: m.introducir_campo("copy", None, "v1", "headline", "Compra hoy", "A", pieza="P1", arte="no_aplica"), prev=None, nueva="v1", actor="A", campo="headline")
        x.op("modificar", lambda: m.modificar_campo("copy", "v1", "v2", "headline", "Compra hoy mismo", "Rc"), prev="v1", nueva="v2", actor="Rc", campo="headline")
        x.op("sustituir", lambda: m.sustituir_campo("copy", "v2", "v3", "headline", "Oferta nueva", "B"), prev="v2", nueva="v3", actor="B", campo="headline")
        a = [t["id"] for t in m.at.values() if t["version"] == "v3" and t["persona"] == "A" and t["campo"] == "headline"][0]; _res(m, "r1", a, "Rc", motivador=[k for k, ev in m.ev.items() if ev["actor"] == "B"][-1], version="v3"); return m, x, a
    m, x, a = sc6(Motor); ok = m.aplicar_resolucion("r1"); rj = (not ok) and "R7" in m.res["r1"]["motivos"] and m.estado(a) == "activa"
    mf, xf, af = sc6(_ForzRes); xf.op("aplicar_resolucion", lambda: mf.aplicar_resolucion("r1"), res="r1", vid="v3"); ad = "I4" in {c[0] for c in xf.viol}
    reg("ATTR-06", "resolutor que heredó la contribución evaluada", "rechazo del motor con R7 y aceptación forzada detectada (I4)", "rechaza=%s auditor=%s" % (rj, ad), rj and ad)
    # ATTR-10: la reconsideración modifica el registro anterior
    m, x, a = _sc_res(); x.op("rechazar_resolucion", lambda: m.rechazar_resolucion("r1", ["evidencia insuficiente"]), res="r1", vid="v2")
    _res(m, "r2", a, "R", motivador=[k for k, ev in m.ev.items() if ev["actor"] == "B"][-1], previo="r1"); x.op("aplicar_resolucion", lambda: m.aplicar_resolucion("r2"), res="r2", vid="v2")
    c = _aud_estado(m, lambda m: _set_res(m, "r1", motivos=("sin motivo",))); reg("ATTR-10", "reconsideración que modifica el registro anterior", "I13 e I14", ",".join(c), "I13" in c and "I14" in c and m.estado(a) == "historica")
    # ATTR-11: atribución histórica reactivada sin resolución
    m, x, a = _sc_res_aplicada(); c = _aud_estado(m, lambda m: m.est.append(dict(seq=m.tick(), atr=a, estado="activa", resolucion=None, motivo="reactivada sin resolución"))); reg("ATTR-11", "atribución histórica reactivada sin resolución", "I15", ",".join(c), "I15" in c)
    # ATTR-12: atribución activa eliminada por coincidencia de segmentos (ningún segmento idéntico)
    m, x = _base(Motor); x.op("introducir", lambda: m.introducir_campo("copy", None, "v1", "headline", "Compra hoy", "A", pieza="P1", arte="no_aplica"), prev=None, nueva="v1", actor="A", campo="headline")
    x.op("sustituir", lambda: m.sustituir_campo("copy", "v1", "v2", "headline", "Oferta nueva", "B"), prev="v1", nueva="v2", actor="B", campo="headline")
    sano = any(t["persona"] == "A" and m.estado(t["id"]) == "activa" for t in m.activas("v2")) and not x.viol
    m2, x2 = _base(_AutoRetiro); x2.op("introducir", lambda: m2.introducir_campo("copy", None, "v1", "headline", "Compra hoy", "A", pieza="P1", arte="no_aplica"), prev=None, nueva="v1", actor="A", campo="headline")
    x2.op("sustituir", lambda: m2.sustituir_campo("copy", "v1", "v2", "headline", "Oferta nueva", "B"), prev="v1", nueva="v2", actor="B", campo="headline"); c = sorted({z[0] for z in x2.viol})
    reg("ATTR-12", "atribución activa eliminada por cero segmentos idénticos", "el motor conserva la atribución y el auditor detecta la eliminación (I1)", "motor conserva=%s auditor=%s" % (sano, c), sano and "I1" in c)
    return sorted(out, key=lambda r: r["id"])

# ===== v14: elegibilidad del evaluador, confirmación de independencia e intento de publicación (modelo en memoria de reglas ya documentadas: IG5-55, IG5-57, IG5-64, IG5-67, IG5-68, IG5-78, IG5-89) =====
def elegibilidad_evaluador(m, vid, u):
    """Códigos que impiden que `u` evalúe la versión `vid` (vacío si es elegible): E1 miembro activo de la organización, E2 permiso piece.review del rol, E3 asignación vigente, E4 independiente de E, E5 independiente de la clasificación evaluada,
    E6 independiente de las resoluciones aplicables, E7 procedencia completa (si no, ninguno es elegible: fallo cerrado). No usa permisos nuevos ni asigna automáticamente a Admin."""
    c = []; mem = m.members.get(u)
    if not (mem and mem["org"] == m.org and mem["activo"]): c.append("E1")
    if "piece.review" not in (m.roles.get(mem["rol"], set()) if mem else set()): c.append("E2")
    if u not in m.asignaciones.get(vid, ()): c.append("E3")
    r = calcular_E_verificado(m, vid)
    if not r["completa"]: c.append("E7")
    elif u in (r["E"] or {}): c.append("E4")
    exactas = m._versiones_exactas(vid)
    for v_ in exactas:
        for campo in m.v[v_]["campos"]:
            h = [x for x in m.clas_hist if x[0] == v_ and x[1] == campo]
            prop = h[-1][3].replace("cambio por ", "") if h and len(h[-1]) > 3 else m.v[v_].get("autor")
            if prop == u and "E5" not in c: c.append("E5")
    for rs in m.res.values():
        if rs["version"] in exactas and u in (rs.get("afectado"), rs.get("solicitante"), rs.get("actor_cambio")) and "E6" not in c: c.append("E6")
    return c
@_atomica()
def _asignar_evaluador(self, vid, u):
    """Asignación explícita; no existe asignación automática (ni a Admin ni al propietario)."""
    if vid not in self.v: raise OperacionInvalida("la versión %s no existe" % vid)
    self.asignaciones.setdefault(vid, set()).add(u)
@_atomica()
def _confirmar_independencia(self, vid, u):
    """Registra la confirmación solo si el evaluador es elegible en este momento (revalidación) y la procedencia está completa; si no, se rechaza sin escribir."""
    c = elegibilidad_evaluador(self, vid, u)
    if c: raise OperacionInvalida("el evaluador %s no puede confirmar la independencia: %s" % (u, ",".join(c)))
    self.confirmaciones.append(dict(version=vid, evaluador=u, seq=self.tick(), E=sorted(calcular_E_verificado(self, vid)["E"])))
@_atomica()
def _intentar_publicacion(self, vid, actor):
    """El intento se registra siempre (solo se agrega). La publicación exige procedencia completa verificada, una confirmación de independencia y que el evaluador siga siendo elegible; si no, queda bloqueada con sus motivos."""
    mot = []
    if not puede_publicar(self, vid): mot.append("procedencia incompleta o inconsistente")
    conf = [x for x in self.confirmaciones if x["version"] == vid]
    if not conf: mot.append("sin confirmación de independencia")
    elif elegibilidad_evaluador(self, vid, conf[-1]["evaluador"]): mot.append("el evaluador dejó de ser elegible")
    self.intentos_pub.append(dict(version=vid, actor=actor, seq=self.tick(), resultado="bloqueada" if mot else "publicada", motivos=tuple(mot)))
    if not mot: self.publicadas.add(vid)
    return not mot
Motor.asignar_evaluador = _asignar_evaluador; Motor.confirmar_independencia = _confirmar_independencia; Motor.intentar_publicacion = _intentar_publicacion

# ===== v14: atomicidad de las diez operaciones sobre procedencia (AT14-01 a AT14-10) =====
class _Falla(Motor):
    """Inyecta un fallo en la escritura (después de haber escrito parte del estado) para comprobar la reversión completa."""
    falla_en = None
    def _chk(s, donde):
        if s.__dict__.get("falla") == donde: raise RuntimeError("fallo inyectado en %s" % donde)
    def _campo_arte(s, vid, aid, clasif): r = super()._campo_arte(vid, aid, clasif); s._chk("campo_arte"); return r
    def _marcar_provisional(s, vid, campo): r = super()._marcar_provisional(vid, campo); s._chk("provisional"); return r
    def _atribuir(s, *a, **k): r = super()._atribuir(*a, **k); s._chk("atribuir"); return r
    def registrar_resolucion(s, rid, resultado, motivos=(), **sol): r = super().registrar_resolucion(rid, resultado, motivos, **sol); s._chk("resolucion"); return r
    def tick(s):
        if s.__dict__.get("falla") == "tick" and s.__dict__.get("_tx"): raise RuntimeError("fallo inyectado en tick")
        return super().tick()
def _sin_huerfanos(m):
    """Ninguna referencia colgante: assets con evento/origen/versión de copy existentes, atribuciones con evento y versión existentes."""
    e = m._invariantes_basicos()
    for k, a in m.assets.items():
        if a.get("copy_version") not in m.v or (a.get("evento_carga") or a.get("evento_reutilizacion")) not in m.ev: e.append("asset huérfano %s" % k)
    return not e
def pruebas_atomicidad14():
    out = []
    def caso(i, nom, fn):
        try: ok, obs = fn()
        except Exception as ex: ok, obs = False, "%s: %s" % (type(ex).__name__, str(ex)[:100])
        out.append(dict(id=i, nombre=nom, ok=bool(ok), obs=obs))
    def igual(m, intento, esperado=Exception):
        antes = _estado_completo(m)
        try: intento(); lanzo = False
        except esperado: lanzo = True
        return lanzo and _estado_completo(m) == antes
    def a01():
        m, x = _base(_Falla); _intro_cv(x, m, "cv", "A"); m.falla = "atribuir"; f1 = igual(m, lambda: m.registrar_asset("n1", "cv", "U")); m.falla = None
        f2 = igual(m, lambda: m.registrar_asset("n1", "cv", "Fantasma"), ReutilizacionInvalida); f3 = igual(m, lambda: m.registrar_asset("n1", "no_existe", "U"), ReutilizacionInvalida)
        m.registrar_asset("n1", "cv", "U"); return f1 and f2 and f3 and _sin_huerfanos(m) and m.reconstruir_cadena_procedencia("n1")["ok"], "fallo a mitad de escritura, actor ajeno y versión de copy inexistente revierten; el éxito deja una cadena válida"
    def a02():
        m, x = _fx14(_Falla); m.falla = "campo_arte"; f1 = igual(m, lambda: m.registrar_asset("a4", "cc", "B", reused_from="a3")); m.falla = "atribuir"; f2 = igual(m, lambda: m.registrar_asset("a4", "cc", "B", reused_from="a3")); m.falla = None
        m.registrar_asset("a4", "cc", "B", reused_from="a3"); return f1 and f2 and _sin_huerfanos(m) and m.reconstruir_cadena_procedencia("a4")["ok"] and not auditar_E(snapshot(m), m.calcular_E("cc"), "cc"), "el asset, el evento, la atribución, la relación de procedencia y el registro de reutilización no quedan parciales"
    def a03():
        m, x = _base(_Falla); _intro_cv(x, m, "cvm", "A"); m.registrar_asset("a1", "cvm", "U"); m.falla = "provisional"; f1 = igual(m, lambda: m.modificar_asset("cvm", "cvm2", "a1b", "a1", "D")); m.falla = None
        f2 = igual(m, lambda: m.modificar_asset("cvm", "cvm2", "a1b", "inexistente", "D"), KeyError); m.modificar_asset("cvm", "cvm2", "a1b", "a1", "D")
        return f1 and f2 and "cvm2" in m.v and _sin_huerfanos(m) and m.reconstruir_cadena_procedencia("a1b")["ok"], "una modificación fallida no crea versión, asset ni atribución"
    def a04():
        m, x = _base(_Falla); m.falla = "atribuir"; f1 = igual(m, lambda: m.introducir_campo("copy", None, "v1", "headline", "Compra", "A", pieza="P1", arte="no_aplica")); m.falla = None
        m.introducir_campo("copy", None, "v1", "headline", "Compra", "A", pieza="P1", arte="no_aplica"); return f1 and "v1" in m.v and len(m.at) == 1 and _sin_huerfanos(m), "el evento y la versión no quedan sin su atribución directa"
    def a05():
        m, x = _base(_Falla); m.introducir_campo("copy", None, "v1", "headline", "Compra", "A", pieza="P1", arte="no_aplica"); m.falla = "atribuir"; f1 = igual(m, lambda: m.version_sin_cambio("copy", "v1", "v2", "B")); m.falla = None
        m.version_sin_cambio("copy", "v1", "v2", "B"); return f1 and "v2" in m.v and len(m.activas("v2")) == 1 and _sin_huerfanos(m), "la herencia a mitad de camino no deja una versión con atribuciones parciales"
    def res(cls, previo):
        m, x, a = _sc_res(cls)
        if previo: m.rechazar_resolucion("r1", ["evidencia insuficiente"]); _res(m, "r2", a, "R", motivador=[k for k, ev in m.ev.items() if ev["actor"] == "B"][-1], previo="r1")
        return m, a
    def a06():
        m, a = res(_Falla, False); m.falla = "resolucion"; f1 = igual(m, lambda: m.aplicar_resolucion("r1")) and "r1" not in m.res and m.estado(a) == "activa"; m.falla = None
        ok = m.aplicar_resolucion("r1"); return f1 and ok and m.estado(a) == "historica" and _sin_huerfanos(m), "la resolución no queda persistida si el cambio de estado falla"
    def a07():
        m, a = res(_Falla, True); m.falla = "resolucion"; f1 = igual(m, lambda: m.aplicar_resolucion("r2")) and "r2" not in m.res and m.res["r1"]["resultado"] == "rechazada"; m.falla = None
        ok = m.aplicar_resolucion("r2"); return f1 and ok and m.res["r2"]["previo"] == "r1" and _sin_huerfanos(m), "la reconsideración fallida no toca el registro anterior ni deja un registro nuevo"
    def a08():
        m, x = _fx14(); m.registrar_asset("a4", "cc", "B", reused_from="a3"); antes = _estado_completo(m); evaluar_impacto(m, "cc"); f_ok = _estado_completo(m) == antes
        for k in [k for k, t in m.at.items() if t.get("asset") == "a1" and t["rel"] == "directa"]: m.at.pop(k)
        antes = _estado_completo(m)
        try: evaluar_impacto(m, "cc"); lanzo = False
        except ProcedenciaIncompleta: lanzo = True
        return f_ok and lanzo and _estado_completo(m) == antes and not puede_publicar(m, "cc"), "la evaluación de impacto no escribe; con procedencia incompleta falla cerrada sin cambiar el estado"
    def a09():
        m, x = _fx14(_Falla); m.registrar_asset("a4", "cc", "B", reused_from="a3"); [m.asignar_evaluador("cc", u) for u in ("R", "U", "Adm")]
        f1 = all(igual(m, lambda u=u: m.confirmar_independencia("cc", u), OperacionInvalida) for u in ("U", "Adm", "Z"))
        m.falla = "tick"; f2 = igual(m, lambda: m.confirmar_independencia("cc", "R")); m.falla = None; m.confirmar_independencia("cc", "R")
        return f1 and f2 and len(m.confirmaciones) == 1 and elegibilidad_evaluador(m, "cc", "U") == ["E2", "E4"] and elegibilidad_evaluador(m, "cc", "Z") == ["E2", "E3"], "el evaluador dentro de E, sin piece.review o sin asignación se rechaza sin escribir; el elegible se registra una vez"
    def a10():
        m, x = _fx14(_Falla); m.registrar_asset("a4", "cc", "B", reused_from="a3"); m.asignar_evaluador("cc", "R"); m.confirmar_independencia("cc", "R")
        m.falla = "tick"; f1 = igual(m, lambda: m.intentar_publicacion("cc", "Q")) and not m.intentos_pub; m.falla = None
        ok = m.intentar_publicacion("cc", "Q"); pub = "cc" in m.publicadas and m.intentos_pub[-1]["resultado"] == "publicada"
        _ev_pr(m, "a2", source_uploader_id="Z"); m.publicadas.discard("cc"); bloq = (not m.intentar_publicacion("cc", "Q")) and "cc" not in m.publicadas and m.intentos_pub[-1]["resultado"] == "bloqueada"
        return f1 and ok and pub and bloq, "el intento se registra solo si la operación termina; con procedencia incompleta queda bloqueado y no se alcanza un estado publicado"
    def a11():
        class _PreDebil(_Forzado14):
            _verificar_final = Motor._verificar_final
        m, x = _fx14(_PreDebil); _ev_pr(m, "a2", version="cvu"); previo = _estado_completo(m)
        try: m.registrar_asset("a4", "cc", "B", reused_from="a3"); lanzo = False
        except OperacionInvalida as ex: lanzo = "estado final" in str(ex)
        m2, x2 = _fx14(_PreDebil); m2.registrar_asset("a4", "cc", "B", reused_from="a3")
        return lanzo and _estado_completo(m) == previo and "a4" not in m.assets and m2.reconstruir_cadena_procedencia("a4")["ok"], "con la validación previa debilitada, la verificación final de la transacción rechaza una cadena inconsistente y restaura el estado exacto; con una cadena válida confirma"
    for i, nom, f in (("AT14-11", "verificación final de la transacción (segunda línea de defensa)", a11), ("AT14-01", "registrar carga de asset", a01), ("AT14-02", "registrar reutilización", a02), ("AT14-03", "registrar modificación de asset", a03), ("AT14-04", "registrar atribución", a04), ("AT14-05", "heredar atribuciones", a05),
                      ("AT14-06", "resolver descarte", a06), ("AT14-07", "reconsiderar una resolución", a07), ("AT14-08", "construir evaluación de impacto", a08), ("AT14-09", "confirmar independencia", a09), ("AT14-10", "registrar intento de publicación", a10)): caso(i, nom, f)
    return sorted(out, key=lambda r: r["id"])

# ===== v14: reconstrucción de E y elegibilidad del evaluador (E14-01 a E14-06) =====
def _fx_E(cls=Motor):
    m, x = _base(cls)
    x.op("introducir", lambda: m.introducir_campo("brief", None, "bv1", "commercial_offer", "Oferta", "A", pieza="P1"), prev=None, nueva="bv1", actor="A", campo="commercial_offer")
    x.op("introducir", lambda: m.introducir_campo("promotion", None, "pv1", "discount", "10%", "Pm", pieza="P1"), prev=None, nueva="pv1", actor="Pm", campo="discount")
    _intro_cv(x, m, "cvm", "B"); x.op("registrar_asset", lambda: m.registrar_asset("a1", "cvm", "U"))
    x.op("modificar", lambda: m.modificar_asset("cvm", "cvm2", "a1b", "a1", "D"), prev="cvm", nueva="cvm2", actor="D", campo="arte")
    _intro_cv(x, m, "cad", "W", pieza="P2", refs={"brief": "bv1", "promotion": "pv1", "master": "cvm2"}); x.op("registrar_asset", lambda: m.registrar_asset("a2", "cad", "W", reused_from="a1b"))
    return m, x
def pruebas_E14():
    out = []
    def caso(i, nom, fn):
        try: ok, obs = fn()
        except Exception as ex: ok, obs = False, "%s: %s" % (type(ex).__name__, str(ex)[:100])
        out.append(dict(id=i, nombre=nom, ok=bool(ok), obs=obs))
    def e1():
        m, x = _fx_E(); r = calcular_E_verificado(m, "cad"); est = snapshot(m)
        return r["completa"] and set(r["E"]) == {"A", "Pm", "B", "U", "D", "W"} and set(r["E"]) == _E(est, "cad") and not x.viol, "E = brief (A), datos promocionales (Pm), versión maestra exacta (B), uploader original del asset (U), editor material de la modificación (D) y autor de la adaptación y reutilizador (W): %s" % sorted(r["E"] or [])
    def e2():
        m, x = _fx_E(); [m.at.pop(k) for k in [k for k, t in m.at.items() if t["version"] == "cad" and t.get("asset") == "a2" and t["persona"] == "U"]]
        r = calcular_E_verificado(m, "cad"); return (not r["completa"]) and r["E"] is None, "sin la atribución heredada del uploader original, la procedencia es incompleta y E no se entrega"
    def e3():
        m, x = _fx_E(); [m.at.pop(k) for k in [k for k, t in m.at.items() if t["version"] == "bv1"]]
        r = calcular_E_verificado(m, "cad"); return (not r["completa"]) and r["E"] is None, "sin evidencia del brief, E no se entrega"
    def e4():
        m, x = _fx_E(); [m.asignar_evaluador("cad", u) for u in ("R", "Q", "Adm", "B", "Rb")]; m.miembro("Rb", "revisor")
        got = {u: elegibilidad_evaluador(m, "cad", u) for u in ("R", "Q", "Adm", "B", "Rb", "R2")}; m.cambiar_clasificacion("cad", "headline", "modificado", "Rb"); got["Rb"] = got["Rb"] + elegibilidad_evaluador(m, "cad", "Rb")
        return got == {"R": [], "Q": [], "Adm": ["E2"], "B": ["E2", "E4"], "Rb": ["E5"], "R2": ["E3"]}, "elegibilidad: miembro activo, piece.review, asignación, independencia de E y de la clasificación: %s" % got
    def e5():
        m, x = _fx_E(); m.members["R"]["activo"] = False; m.asignar_evaluador("cad", "R"); c1 = elegibilidad_evaluador(m, "cad", "R")
        m2, x2 = _fx_E(); m2.asignar_evaluador("cad", "R"); _ev_pr(m2, "a2", source_uploader_id="Z"); c2 = elegibilidad_evaluador(m2, "cad", "R")
        return "E1" in c1 and c2 == ["E7"], "un evaluador inactivo no es elegible; con procedencia incompleta ninguno es elegible (fallo cerrado, sin asignación automática a Admin)"
    def e6():
        m, x, a = _sc_res_aplicada(); m.asignar_evaluador("v2", "R"); m.asignar_evaluador("v2", "Q"); m.asignar_evaluador("v2", "R2")
        got = {u: elegibilidad_evaluador(m, "v2", u) for u in ("Q", "R", "R2")}
        return got["Q"] == ["E6"] and got["R2"] == [] and got["R"] == [], "el solicitante de una resolución aplicable no es independiente de ella (E6); el resolutor y otro revisor asignado sí lo son: %s" % got
    for i, nom, f in (("E14-01", "E reconstruido con todos los contribuyentes verificables", e1), ("E14-02", "falta la atribución heredada del uploader original: procedencia incompleta", e2), ("E14-03", "falta la evidencia del brief: procedencia incompleta", e3),
                      ("E14-04", "elegibilidad del evaluador por código E1 a E5", e4), ("E14-05", "evaluador inactivo y fallo cerrado con procedencia incompleta", e5), ("E14-06", "independencia de las resoluciones aplicables", e6)): caso(i, nom, f)
    return out

# ===== v15 BEGIN: integridad de los eventos propios en cada eslabón (AV, CF, AC, AP, ADV15, AT15) =====
def _fx15(cls=Motor, construida=False):
    """v14 más: a5 (W reutiliza la versión modificada a1b en P7) y a6 (D reutiliza a5 en P8), de modo que la modificación a1b queda como eslabón INTERMEDIO de la cadena a6 → a5 → a1b → a1; a2c (W reutiliza a1 en la misma pieza P2 que a2, ambos en la versión 1); destinos cf (P9, B), cg (P10, D). Con `construida`, a4 (B, desde a3) ya está registrada."""
    m, x = _fx14(cls)
    _intro_cv(x, m, "cd", "W", pieza="P7", refs={"master": "cvm2"}); x.op("registrar_asset", lambda: m.registrar_asset("a5", "cd", "W", reused_from="a1b"))
    _intro_cv(x, m, "ce", "D", pieza="P8", refs={"master": "cd"}); x.op("registrar_asset", lambda: m.registrar_asset("a6", "ce", "D", reused_from="a5"))
    _intro_cv(x, m, "cf", "B", pieza="P9", refs={"master": "ce"})
    _intro_cv(x, m, "cac", "W", pieza="P2", refs={"master": "cvm"}); x.op("registrar_asset", lambda: m.registrar_asset("a2c", "cac", "W", reused_from="a1"))
    if construida: x.op("registrar_asset", lambda: m.registrar_asset("a4", "cc", "B", reused_from="a3"))
    _intro_cv(x, m, "cg", "D", pieza="P10", refs={"master": "cc"})
    return m, x
def _quita_campo(m, aid): m.ev[m.assets[aid]["evento_reutilizacion"]].pop("campo")
def _swap_av(m):
    c, r = _carga(m, "a1b"), _reu(m, "a5"); c["asset_version"], r["asset_version"] = r["asset_version"], c["asset_version"]
def _swap_campo(m):
    r = _reu(m, "a2"); h = [e for e in m.ev.values() if e["version"] == "ca" and e["campo"] == "headline"][0]; r["campo"], h["campo"] = h["campo"], r["campo"]
def _cruce_a2(m):
    e2, ec = _reu(m, "a2"), _reu(m, "a2c"); e2["asset"], ec["asset"] = ec["asset"], e2["asset"]; e2["asset_version_id"], ec["asset_version_id"] = ec["asset_version_id"], e2["asset_version_id"]
_D_A6 = dict(origen="a6", destino=("a7", "cf", "B"))
_D_A3 = dict(origen="a3", destino=("a4", "cc", "B"))
_D_A4 = dict(origen="a4", destino=("a8", "cg", "D"), construida=True)
# (id, nombre, corrompe, campos esperados en el detalle, eslabón, escenario, versiones de copy cuya procedencia debe quedar incompleta)
AV = [
 ("AV-01", "asset_version del evento propio del último eslabón (a3) cambia a una versión inexistente", lambda m: _ev_pr(m, "a3", asset_version=7), ("asset_version",), "a3", _D_A3, ("cb", "cc")),
 ("AV-02", "asset_version del evento propio de un eslabón intermedio (a2) cambia a una versión inexistente", lambda m: _ev_pr(m, "a2", asset_version=5), ("asset_version",), "a2", _D_A3, ("cb", "ca")),
 ("AV-03", "asset_version de a3 usa un número de versión existente pero perteneciente a otro asset (el de la modificación a1b)", lambda m: _ev_pr(m, "a3", asset_version=m.assets["a1b"]["version_asset"]), ("asset_version",), "a3", _D_A3, ("cb", "cc")),
 ("AV-04", "el evento propio de la modificación intermedia a1b usa la versión anterior del mismo asset (1 en lugar de 2)", lambda m: _set(_carga(m, "a1b"), asset_version=1), ("asset_version",), "a1b", _D_A6, ("cvm2", "cd")),
 ("AV-05", "asset_version intercambiado entre dos eventos válidos (la modificación a1b y la reutilización a5)", _swap_av, ("asset_version",), "a5", _D_A6, ("cd", "cvm2")),
 ("AV-06", "asset_version de a5 guarda la versión del origen (2) en lugar de la del destino (1), con la raíz y las demás referencias correctas", lambda m: _ev_pr(m, "a5", asset_version=m.assets["a1b"]["version_asset"]), ("asset_version",), "a5", _D_A6, ("cd", "ce")),
 ("AV-07", "asset_version del evento propio de una modificación intermedia (a1b) cambia a otro número", lambda m: _set(_carga(m, "a1b"), asset_version=9), ("asset_version",), "a1b", _D_A6, ("cvm2", "ce")),
 ("AV-08", "asset_version de a3 se altera después de construir la cadena (a4 ya registrada)", lambda m: _ev_pr(m, "a3", asset_version=4), ("asset_version",), "a3", _D_A4, ("cb", "cc")),
]
CF = [
 ("CF-01", "el campo del evento propio del último eslabón (a3) cambia de arte a otro campo (precio)", lambda m: _ev_pr(m, "a3", campo="precio"), ("campo",), "a3", _D_A3, ("cb", "cc")),
 ("CF-02", "el campo del evento propio de un eslabón intermedio (a2) cambia de arte a otro campo (precio)", lambda m: _ev_pr(m, "a2", campo="precio"), ("campo",), "a2", _D_A3, ("cb", "ca")),
 ("CF-03", "se elimina el campo del evento propio de un eslabón intermedio (a2)", lambda m: _quita_campo(m, "a2"), ("campo",), "a2", _D_A3, ("cb", "ca")),
 ("CF-04", "el campo del evento propio del último eslabón (a3) es nulo", lambda m: _ev_pr(m, "a3", campo=None), ("campo",), "a3", _D_A3, ("cb", "cc")),
 ("CF-05", "el evento propio de la modificación a1b declara un campo permitido pero distinto de arte (headline)", lambda m: _set(_carga(m, "a1b"), campo="headline"), ("campo",), "a1b", _D_A6, ("cvm2", "ce")),
 ("CF-06", "el campo se intercambia entre dos eventos válidos (la reutilización de a2 y la introducción de headline de la misma versión de copy)", _swap_campo, ("campo",), "a2", _D_A3, ("cb", "ca")),
 ("CF-07", "el campo de a3 se modifica después de construir la cadena (a4 ya registrada)", lambda m: _ev_pr(m, "a3", campo="headline"), ("campo",), "a3", _D_A4, ("cb", "cc")),
 ("CF-08", "todos los identificadores de a5 son correctos y solo cambia el campo (headline)", lambda m: _ev_pr(m, "a5", campo="headline"), ("campo",), "a5", _D_A6, ("cd", "ce")),
]
AC = [
 ("AC-01", "asset_version incorrecto y campo correcto en a2", lambda m: _ev_pr(m, "a2", asset_version=5), ("asset_version",), "a2", _D_A3, ("cb", "ca")),
 ("AC-02", "asset_version correcto y campo incorrecto en a3", lambda m: _ev_pr(m, "a3", campo="headline"), ("campo",), "a3", _D_A3, ("cb", "cc")),
 ("AC-03", "asset_version y campo incorrectos en a3", lambda m: _ev_pr(m, "a3", asset_version=5, campo="precio"), ("asset_version", "campo"), "a3", _D_A3, ("cb", "cc")),
 ("AC-04", "asset_version y campo incorrectos a la vez en el eslabón intermedio a5, con la raíz intacta", lambda m: _ev_pr(m, "a5", asset_version=7, campo="headline"), ("asset_version", "campo"), "a5", _D_A6, ("cd", "ce")),
 ("AC-05", "asset_version y campo incorrectos en el último eslabón a6, con todos los anteriores correctos", lambda m: _ev_pr(m, "a6", asset_version=7, campo="headline"), ("asset_version", "campo"), "a6", _D_A6, ("ce", "cf")),
 ("AC-06", "a2 y a2c (misma pieza P2, ambos en la versión 1) con las referencias de asset y versión cruzadas entre sus eventos", _cruce_a2, ("asset", "asset_version_id"), "a2", _D_A3, ("cb", "ca")),
]
def _bloqueo15(m, vid):
    """(E nulo con procedencia incompleta, evaluación de impacto bloqueada, sin publicación ni aprobación) de la versión `vid`."""
    r = calcular_E_verificado(m, vid)
    try: evaluar_impacto(m, vid); imp = False
    except ProcedenciaIncompleta: imp = True
    return (not r["completa"]) and r["E"] is None, imp, not puede_publicar(m, vid)
def _inicial15(esc, fx):
    """Estado inicial válido: la reutilización se acepta sobre una copia, el auditor independiente no halla violaciones y E del destino está completo."""
    m0, x0 = fx(Motor, esc.get("construida", False)); o = esc["origen"]; a, cv, q = esc["destino"]
    try: m0.registrar_asset(a, cv, q, reused_from=o)
    except Exception: return False
    est = snapshot(m0); return a in m0.assets and calcular_E_verificado(m0, cv)["completa"] and not auditar_E(est, m0.calcular_E(cv), cv) and not _hall_arte_exactas(est, cv) and not _hall_cadena(est, cv, [a]) and not x0.viol
def _correr15(casos):
    """AV, CF y AC: cada caso parte de un estado válido, cambia UN dato y exige las doce condiciones de H-04. Una excepción distinta de ReutilizacionInvalida no cuenta como detección."""
    res = []
    for mid, nom, corrompe, campos, eslabon, esc, cvs in casos:
        r = dict(id=mid, mut=nom, esp="rechazo con el campo %s del eslabón %s" % (" y ".join(campos), eslabon), kw=" y ".join(campos), err=None)
        try:
            r["valido"] = bool(_inicial15(esc, _fx15)); m, x = _fx15(Motor, esc.get("construida", False)); previo = _estado_completo(m); corrompe(m); r["cambio"] = _estado_completo(m) != previo
            antes = _estado_completo(m); a, cv, q = esc["destino"]; n = (len(m.assets), len(m.ev), len(m.at), len(m.est), len(m.clas_hist)); exc = None
            try: m.registrar_asset(a, cv, q, reused_from=esc["origen"])
            except ReutilizacionInvalida as ex: exc = ex
            r["rechaza"] = exc is not None; det = exc.detalles if exc else []
            r["ident"] = bool(exc) and all(any(d["eslabon"] == eslabon and d["campo"] == c and d.get("evento") is not None for d in det) for c in campos) and all(c in str(exc) for c in campos)
            r["sin_asset"] = a not in m.assets and len(m.assets) == n[0]; r["sin_evento"] = len(m.ev) == n[1]; r["sin_atribucion"] = len(m.at) == n[2] and len(m.est) == n[3]; r["sin_relacion"] = len(m.clas_hist) == n[4] and m.v == antes["v"] and m.arte_decl == antes["arte_decl"]
            r["atomico"] = _estado_completo(m) == antes; r["incompleta"] = not m.reconstruir_cadena_procedencia(esc["origen"])["ok"]
            b = [_bloqueo15(m, v) for v in cvs]; r["E_nulo"] = all(z[0] for z in b); r["impacto_bloq"] = all(z[1] for z in b); r["no_publica"] = all(z[2] for z in b)
            r["obs"] = ("rechazada: " + str(exc)[:150]) if exc else "ACEPTADA"
        except Exception as ex:
            r["err"] = "%s: %s" % (type(ex).__name__, str(ex)[:80]); r["obs"] = "ERROR " + r["err"]
        r["det"] = r["err"] is None and all(r.get(k) for k in ("valido", "cambio", "rechaza", "ident", "sin_asset", "sin_evento", "sin_atribucion", "sin_relacion", "atomico", "incompleta", "E_nulo", "impacto_bloq", "no_publica"))
        for k in ("valido", "cambio", "rechaza", "ident", "sin_asset", "sin_evento", "sin_atribucion", "sin_relacion", "atomico", "incompleta", "E_nulo", "impacto_bloq", "no_publica"): r[k] = bool(r.get(k))
        res.append(r)
    return res
def correr_mutaciones_av(): return _correr15(AV)
def correr_mutaciones_cf(): return _correr15(CF)
def correr_mutaciones_ac(): return _correr15(AC)

# ---- AP-01 a AP-08: casos positivos (el control no bloquea relaciones válidas) ----
def _ap_cadena(n, quien=("W", "D", "B")):
    """Cadena a1 → a2 → … con `n` reutilizaciones sucesivas; devuelve (modelo, ejecución, lista de assets reutilizados)."""
    m, x = _fx13(Motor); ids = []; prev = "a1"; piezas = ["P2", "P3", "P4"]; cvs = ["ca", "cb", "cc"]; refs = "cvm"
    for i in range(n):
        if i: _intro_cv(x, m, cvs[i], quien[i], pieza=piezas[i], refs={"master": cvs[i - 1]})
        aid = "a%d" % (i + 2); x.op("registrar_asset", lambda aid=aid, i=i, prev=prev: m.registrar_asset(aid, cvs[i], quien[i], reused_from=prev)); ids.append(aid); prev = aid
    return m, x, ids
def _evs_cadena(m, aid):
    out = []; vis = []; z = aid
    while z in m.assets and z not in vis:
        vis.append(z); y = m.assets[z]; out.append(m.ev[y["evento_reutilizacion"] or y["evento_carga"]]); z = y.get("origen") if y["tipo"] == "reutilizado" else y.get("previo") if y["tipo"] == "modificado" else None
    return out
def _pos15_base(m, x, aid, cv):
    est = snapshot(m); r = m.reconstruir_cadena_procedencia(aid); e = x.E(cv)
    return [("el motor registró la reutilización sin rechazarla", True, aid in m.assets), ("la reconstrucción de la cadena es válida y sin detalles de error", (True, []), (r["ok"], r["detalles"])), ("el auditor independiente no halla violaciones", [], auditar_E(est, m.calcular_E(cv), cv) + _hall_arte_exactas(est, cv) + _hall_cadena(est, cv, [aid])),
            ("E completo", True, e["completa"]), ("sin violaciones de la ejecución", [], list(x.viol))]
def _ap01():
    m, x, ids = _ap_cadena(2); return _pos15_base(m, x, "a3", "cb") + [("cadena de dos niveles de reutilización: a3 → a2 → a1", ["a3", "a2", "a1"], m.reconstruir_cadena_procedencia("a3")["eslabones"])]
def _ap02():
    m, x, ids = _ap_cadena(3); return _pos15_base(m, x, "a4", "cc") + [("cadena de tres niveles de reutilización: a4 → a3 → a2 → a1", ["a4", "a3", "a2", "a1"], m.reconstruir_cadena_procedencia("a4")["eslabones"])]
def _ap03():
    m, x = _fx13(Motor); x.op("registrar_asset", lambda: m.registrar_asset("a2", "ca", "W", reused_from="a1")); _intro_cv(x, m, "cb", "D", pieza="P3", refs={"master": "cvx"}); x.op("registrar_asset", lambda: m.registrar_asset("a3", "cb", "D", reused_from="ax"))
    return _pos15_base(m, x, "a2", "ca") + _pos15_base(m, x, "a3", "cb") + [("a1 y ax tienen el mismo número de versión y son assets distintos", (1, 1, True), (m.assets["a1"]["version_asset"], m.assets["ax"]["version_asset"], m.assets["a1"]["asset_id"] != m.assets["ax"]["asset_id"])),
            ("cada reutilización conserva la identidad exacta de su propio origen y raíz", (("a1", "a1"), ("ax", "ax")), ((_reu(m, "a2")["source_asset_version_id"], _reu(m, "a2")["source_root_asset_version_id"]), (_reu(m, "a3")["source_asset_version_id"], _reu(m, "a3")["source_root_asset_version_id"])))]
def _ap04():
    m, x = _fx13(Motor); _intro_cv(x, m, "cd", "W", pieza="P7", refs={"master": "cvm2"}); x.op("registrar_asset", lambda: m.registrar_asset("a5", "cd", "W", reused_from="a1b")); e = _reu(m, "a5")
    return _pos15_base(m, x, "a5", "cd") + [("el evento propio identifica la versión del asset de destino (1)", 1, e["asset_version"]), ("source_asset_version identifica la versión del origen modificado (2)", 2, e["source_asset_version"]), ("ambas referencias son distintas y las dos se validan", True, e["asset_version"] != e["source_asset_version"]),
                                              ("la cadena pasa por la modificación", ["a5", "a1b", "a1"], m.reconstruir_cadena_procedencia("a5")["eslabones"])]
def _ap05():
    m, x, ids = _ap_cadena(2); return _pos15_base(m, x, "a3", "cb") + [("el uploader original (U) es distinto de cada reutilizador", True, all(m.assets[k]["uploader_original"] == "U" and m.assets[k]["reutilizador"] != "U" for k in ids)), ("la reconstrucción conserva al uploader original", "U", m.reconstruir_cadena_procedencia("a3")["uploader"])]
def _ap06():
    m, x, ids = _ap_cadena(2); r = m.reconstruir_cadena_procedencia("a3"); d = _directa(m, "a1"); e = _reu(m, "a3")
    return _pos15_base(m, x, "a3", "cb") + [("la atribución directa de la raíz es única, de U, del evento de carga y del asset raíz", [(d["id"], "U", "a1")], [(r["atribucion"], d["persona"], d["asset"])]), ("los dos eventos de reutilización la referencian exactamente", (d["id"], d["id"]), (_reu(m, "a2")["source_attribution_id"], e["source_attribution_id"]))]
def _ap07():
    m, x, ids = _ap_cadena(3); evs = _evs_cadena(m, "a4")
    return _pos15_base(m, x, "a4", "cc") + [("todos los eventos propios de la cadena están vinculados al campo arte", ["arte"] * 4, [e["campo"] for e in evs]), ("cada evento identifica la versión exacta de su propio asset de destino", [1] * 4, [e["asset_version"] for e in evs])]
def _ap08():
    m, x, ids = _ap_cadena(3); est = snapshot(m); e = x.E("cc")
    return _pos15_base(m, x, "a4", "cc") + [("el motor y el auditor reconstruyen la misma cadena de identidad", m.cadena_identidad("a4"), cadena_identidad_independiente(est, "a4")), ("el E del motor coincide con el E recalculado por el auditor", sorted(_E(est, "cc")), sorted(e["E"] or {})), ("el auditor no usa funciones del motor", [], _compartidas())]
AP = [("AP-01", "cadena válida de dos niveles de reutilización", _ap01), ("AP-02", "cadena válida de tres niveles de reutilización", _ap02), ("AP-03", "cadena válida con dos assets de igual número de versión y la identidad exacta conservada", _ap03), ("AP-04", "reutilización válida después de una modificación del asset", _ap04),
      ("AP-05", "uploader original distinto del reutilizador", _ap05), ("AP-06", "cadena válida con la atribución directa exacta", _ap06), ("AP-07", "cadena válida con todos los eventos propios vinculados al campo arte", _ap07), ("AP-08", "el motor y el auditor independiente coinciden en una cadena íntegra", _ap08)]
def correr_positivos15():
    out = []
    for i, nom, f in AP:
        try: comp = f(); mal = [c[0] for c in comp if c[1] != c[2]]; r = dict(id=i, nombre=nom, ok=not mal, n=len(comp), mal=mal[:3], err=None)
        except Exception as ex: r = dict(id=i, nombre=nom, ok=False, n=0, mal=[], err="%s: %s" % (type(ex).__name__, str(ex)[:80]))
        out.append(r)
    return out

# ---- ADV15-01 a ADV15-08: el motor acepta por sustitución controlada de su validación y el auditor independiente detecta ----
def _swap_ev_asset(m): m.assets["a3"]["evento_reutilizacion"] = m.assets["ay"]["evento_reutilizacion"]
ADV15 = [
 ("ADV15-01", "asset_version incorrecto en el eslabón intermedio (a2)", lambda m: _ev_pr(m, "a2", asset_version=5), "a2", ("asset_version",), "a3", False),
 ("ADV15-02", "asset_version incorrecto en el último eslabón (a3)", lambda m: _ev_pr(m, "a3", asset_version=5), "a3", ("asset_version",), "a3", False),
 ("ADV15-03", "campo incorrecto en el eslabón intermedio (a2)", lambda m: _ev_pr(m, "a2", campo="headline"), "a2", ("campo",), "a3", False),
 ("ADV15-04", "campo incorrecto en el último eslabón (a3)", lambda m: _ev_pr(m, "a3", campo="precio"), "a3", ("campo",), "a3", False),
 ("ADV15-05", "asset_version y campo incorrectos a la vez en el último eslabón (a3)", lambda m: _ev_pr(m, "a3", asset_version=5, campo="headline"), "a3", ("asset_version", "campo"), "a3", False),
 ("ADV15-06", "evento de reutilización de otro asset con el mismo número de versión (a3 usa el de ay)", _swap_ev_asset, "a3", ("asset", "id"), "a3", False),
 ("ADV15-07", "evento propio de la modificación intermedia con referencias incompatibles (el evento de a1b referencia el asset ax)", lambda m: _set(_carga(m, "a1b"), asset="ax", asset_id="ax", asset_version_id="ax"), "a1b", ("asset",), "a6", False),
 ("ADV15-08", "corrupción posterior a la construcción de la cadena (a4 registrada; después a3 cambia asset_version y campo)", lambda m: _ev_pr(m, "a3", asset_version=4, campo="headline"), "a3", ("asset_version", "campo"), "a4", True),
]
class _Forzado15(_Forzado14):
    """Motor que acepta la reutilización aunque la cadena esté corrupta (sustitución controlada de su validación previa y de su verificación final). Solo demuestra que el auditor detecta lo que el motor deja pasar."""
def correr_adversariales15():
    out = []
    for mid, nom, corrompe, eslabon, campos, origen, despues in ADV15:
        try:
            m, x = _fx15(_Forzado15, False); a, cv, q = ("a4", "cc", "B") if origen == "a3" else ("a7", "cf", "B")
            if despues: m.registrar_asset("a4", "cc", "B", reused_from="a3"); corrompe(m); a, cv, q = "a8", "cg", "D"; m.registrar_asset(a, cv, q, reused_from="a4")
            else:
                corrompe(m); m.registrar_asset(a, cv, q, reused_from=origen)
            acepta = a in m.assets
            est = snapshot(m); r = m.calcular_E(cv); hall = auditar_E(est, r, cv); msgs = [c[1] for c in hall]; cods = sorted({c[0] for c in hall}); v = calcular_E_verificado(m, cv)
            try: evaluar_impacto(m, cv); falla = False
            except ProcedenciaIncompleta: falla = True
            det_ = any(("[eslabón %s]" % eslabon) in z and any(c in z for c in campos) for z in msgs) if True else False
            det_campos = all(any(("[eslabón %s]" % eslabon) in z and c in z for z in msgs) for c in campos)
            out.append(dict(id=mid, nombre=nom, motor_acepta=acepta, auditor=bool(det_campos), enlace=eslabon, E_bloqueado=(not v["completa"]) and v["E"] is None, impacto_falla=falla, no_publica=not puede_publicar(m, cv), codigos=cods))
        except Exception as ex: out.append(dict(id=mid, nombre=nom, motor_acepta=False, auditor=False, enlace=eslabon, E_bloqueado=False, impacto_falla=False, no_publica=False, codigos=[], error="%s: %s" % (type(ex).__name__, str(ex)[:80])))
        out[-1]["ok"] = out[-1]["motor_acepta"] and out[-1]["auditor"] and out[-1]["E_bloqueado"] and out[-1]["impacto_falla"] and out[-1]["no_publica"]
    return out

# ---- AT15-01 a AT15-08: atomicidad con instantánea completa en ocho momentos del registro ----
class _Falla15(Motor):
    """Inyecta un fallo en un momento concreto de la validación o del registro de una reutilización."""
    def _f(s, donde):
        if s.__dict__.get("falla15") == donde: raise RuntimeError("fallo inyectado en %s" % donde)
    def _verificar_raiz(s, r, err): s._f("raiz"); return super()._verificar_raiz(r, err)
    def _verificar_reutilizado(s, y, o, r, ue, up, at0, err):
        if y["id"] == "a2": s._f("eslabon")
        return super()._verificar_reutilizado(y, o, r, ue, up, at0, err)
    def _chk_asset_version(s, e, y, L, err): s._f("asset_version"); return super()._chk_asset_version(e, y, L, err)
    def _chk_campo(s, e, y, L, err): s._f("campo"); return super()._chk_campo(e, y, L, err)
    def _chk_atribucion_reutilizador(s, y, er, err): s._f("atribucion"); return super()._chk_atribucion_reutilizador(y, er, err)
    def _chk_actor(s, e, y, L, actor, err): s._f("actor"); return super()._chk_actor(e, y, L, actor, err)
    def _evento(s, *a, **k): s._f("antes_escribir"); return super()._evento(*a, **k)
    def _atribuir(s, *a, **k): r = super()._atribuir(*a, **k); s._f("registro"); return r
def _derivados(m):
    """Datos derivados que pueden afectar a E: la reconstrucción de cada asset, E de cada versión de copy y las comprobaciones del estado."""
    return dict(cadenas={k: (m.reconstruir_cadena_procedencia(k)["ok"], m.reconstruir_cadena_procedencia(k)["eslabones"]) for k in sorted(m.assets)}, E={v: repr(m.calcular_E(v)) for v in sorted(m.v)}, invariantes=m._invariantes_basicos())
def pruebas_atomicidad15():
    out = []
    momentos = [("AT15-01", "antes de validar la raíz", "raiz"), ("AT15-02", "durante la validación de un eslabón intermedio", "eslabon"), ("AT15-03", "durante la validación de asset_version", "asset_version"), ("AT15-04", "durante la validación de campo", "campo"),
                ("AT15-05", "durante la validación de la atribución", "atribucion"), ("AT15-06", "durante la validación del actor", "actor"), ("AT15-07", "antes de escribir", "antes_escribir"), ("AT15-08", "durante el proceso de registro (con escritura parcial)", "registro")]
    for i, nom, donde in momentos:
        try:
            m, x = _fx14(_Falla15); der = _derivados(m); m.falla15 = donde; antes = _estado_completo(m); n = (len(m.assets), len(m.ev), len(m.at), len(m.est), len(m.v), len(m.clas_hist), len(m.res), len(m.arte_decl))
            try: m.registrar_asset("a4", "cc", "B", reused_from="a3"); lanzo = False
            except RuntimeError: lanzo = True
            est_ok = _estado_completo(m) == antes; m.falla15 = None; der2 = _derivados(m); m.falla15 = donde
            d = dict(
                lanzo=lanzo, estado=est_ok, derivados=der2 == der, cuentas=(len(m.assets), len(m.ev), len(m.at), len(m.est), len(m.v), len(m.clas_hist), len(m.res), len(m.arte_decl)) == n, sin_huerfanos=_sin_huerfanos(m), sin_asset="a4" not in m.assets)
            m.falla15 = None; m.registrar_asset("a4", "cc", "B", reused_from="a3"); d["reintento"] = m.reconstruir_cadena_procedencia("a4")["ok"] and not auditar_E(snapshot(m), m.calcular_E("cc"), "cc") and _sin_huerfanos(m)
            out.append(dict(id=i, nombre=nom, ok=all(d.values()), obs=", ".join(k for k, v in d.items() if not v) or "estado completo y derivados idénticos; el reintento sin fallo registra una cadena válida"))
        except Exception as ex: out.append(dict(id=i, nombre=nom, ok=False, obs="%s: %s" % (type(ex).__name__, str(ex)[:100])))
    return out
# ===== v15 END =====

# ===== v14: mutaciones del propio código del modelo (K56-M01 a K56-M08) =====
# Cada una degrada UNA pieza del código nuevo y exige que al menos una batería (CHAIN, ADVC, ATTR, AT14, E14) la detecte.
import contextlib as _cl
def _baterias14():
    r = []
    for nom, f, k in (("CHAIN", correr_mutaciones_cadena, "det"), ("ADVC", correr_adversariales_cadena, "ok"), ("ATTR", correr_mutaciones_atribucion, "det"), ("AV", correr_mutaciones_av, "det"), ("CF", correr_mutaciones_cf, "det"), ("AC", correr_mutaciones_ac, "det"), ("AP", correr_positivos15, "ok"), ("ADV15", correr_adversariales15, "ok")):
        try: r += [(nom, x["id"], bool(x[k])) for x in f()]
        except Exception as ex: r.append((nom, "EXC", False))
    try: r += [("AT14", x["id"], bool(x["ok"])) for x in pruebas_atomicidad14()]
    except Exception: r.append(("AT14", "EXC", False))
    try: r += [("AT15", x["id"], bool(x["ok"])) for x in pruebas_atomicidad15()]
    except Exception: r.append(("AT15", "EXC", False))
    try: r += [("E14", x["id"], bool(x["ok"])) for x in pruebas_E14()]
    except Exception: r.append(("E14", "EXC", False))
    return r
def _debil_siguiente(self, y, err, L):
    tipo = y["tipo"]; o = y.get("origen"); pv = y.get("previo")
    if tipo == "reutilizado": return (o, False) if o is not None else (None, False)
    if tipo == "modificado": return (pv, False) if pv is not None else (None, False)
    return None, True
def _k56_filtra_I15(f):
    def g(antes, despues):
        return [x for x in f(antes, despues) if "reactiv" not in str(x).lower()]
    return g
def _k56_sin_av_campo(f):
    def g(s, cur, ids):
        return [x for x in f(s, cur, ids) if "asset_version" not in x[1] and "campo" not in x[1]]
    return g
def _k56_sin_detalle(f):
    def g(self, aid):
        r = f(self, aid); r = dict(r); r["detalles"] = []; return r
    return g
def _k56_E4_ignorado(f):
    def g(m, vid, u):
        return [c for c in f(m, vid, u) if c != "E4"]
    return g
K56_MUT = [
 ("K56-M01", "la validación de cada eslabón reutilizado pasa a ser un no-op (solo se mira la raíz, como en la v13)", lambda: (Motor, "_verificar_reutilizado", lambda self, *a, **k: None)),
 ("K56-M02", "la reconstrucción ignora la ambigüedad origen/versión anterior", lambda: (Motor, "_siguiente_eslabon", _debil_siguiente)),
 ("K56-M03", "la verificación final de la transacción deja de ejecutarse", lambda: (Motor, "_verificar_final", lambda self, op, aid: None)),
 ("K56-M04", "el auditor independiente de cadena no devuelve hallazgos", lambda: (_sys_mod(), "_hall_cadena", lambda s, cur, ids: [])),
 ("K56-M05", "el auditor de resoluciones filtra la reactivación de atribuciones históricas", lambda: (_sys_mod(), "_auditar_resoluciones", _k56_filtra_I15(_auditar_resoluciones))),
 ("K56-M06", "la elegibilidad del evaluador ignora su pertenencia a E (E4)", lambda: (_sys_mod(), "elegibilidad_evaluador", _k56_E4_ignorado(elegibilidad_evaluador))),
 ("K56-M07", "registrar_asset se ejecuta sin la transacción (sin restauración ante fallo)", lambda: (Motor, "registrar_asset", Motor.registrar_asset.__wrapped__)),
 ("K56-M08", "la validación de una versión modificada pasa a ser un no-op", lambda: (Motor, "_verificar_modificado", lambda self, *a, **k: None)),
 ("K56-M09", "la validación de asset_version del evento propio pasa a ser un no-op (v14: solo se comparaba source_asset_version)", lambda: (Motor, "_chk_asset_version", lambda self, e, y, L, err: True)),
 ("K56-M10", "la validación del campo del evento propio pasa a ser un no-op (v14: no se comprobaba campo en la reconstrucción)", lambda: (Motor, "_chk_campo", lambda self, e, y, L, err: True)),
 ("K56-M11", "el auditor independiente de cadena deja de comparar asset_version y campo", lambda: (_sys_mod(), "_hall_cadena", _k56_sin_av_campo(_hall_cadena))),
 ("K56-M12", "la reconstrucción de la cadena no entrega el detalle estructurado de cada inconsistencia (eslabón, evento, campo, esperado, hallado)", lambda: (Motor, "reconstruir_cadena_procedencia", _k56_sin_detalle(Motor.reconstruir_cadena_procedencia))),
]
class _GlobalesProxy:
    """Lee y escribe las funciones del módulo en su espacio de nombres, aunque el módulo no esté registrado en sys.modules (carga por ruta)."""
    def __getattr__(self, n): return globals()[n]
    def __setattr__(self, n, v): globals()[n] = v
def _sys_mod(): return _GlobalesProxy()
def correr_mutaciones_modelo14():
    base = _baterias14(); assert all(x[2] for x in base), [x for x in base if not x[2]]
    out = []
    for mid, desc, fab in K56_MUT:
        obj, nom, nuevo = fab(); viejo = getattr(obj, nom); setattr(obj, nom, nuevo)
        try: r = _baterias14()
        finally: setattr(obj, nom, viejo)
        fallan = [x[0] + ":" + x[1] for x in r if not x[2]]
        out.append(dict(id=mid, mut=desc, det=bool(fallan), detectada_por=fallan[:6], n_detectores=len(fallan)))
    assert all(x[2] for x in _baterias14())
    return out

# ===== v14: datos de la auditoría, la trazabilidad y la auditoría por relación (se contrastan con el documento) =====
AUDITORIA_V14 = [
 ("D-01", "La cadena de procedencia se validaba solo en la raíz y en el eslabón inmediato", "`Motor._origen_carga` y `Motor._validar_reutilizacion` (v13)", "IG5-102", "una corrupción solo en un eslabón intermedio (evento, uploader, atribución, organización, pieza, versión de copy, actor) se aceptaba si la raíz era correcta", "reconstruir y validar vínculo por vínculo toda la cadena (`reconstruir_cadena_procedencia`)", "CHAIN-01 a CHAIN-24; K56-M01; K56-M08", "precondición válida de cada CHAIN (cadena de tres niveles aceptada, cero violaciones del auditor, E completo)", "`_hall_cadena` y ADVC-01 a ADVC-24"),
 ("D-02", "Un campo derivado guardado en un eslabón se aceptaba como prueba de sí mismo", "`Motor._origen_carga` (v13)", "IG5-102", "el evento, el uploader o la atribución guardados en el reutilizado reemplazaban la comprobación contra los registros concretos", "contrastar siempre contra el registro concreto del evento, la atribución y la versión", "CHAIN-03, CHAIN-05, CHAIN-06, CHAIN-15, CHAIN-19", "precondición válida de cada CHAIN", "`_hall_cadena` (ADVC-03, ADVC-05, ADVC-06, ADVC-15, ADVC-19)"),
 ("D-03", "Las operaciones que escriben no eran transaccionales ni verificaban el estado final", "`Motor.registrar_asset`, `modificar_asset`, `sustituir_asset`, `eliminar_asset`, `crear_version`, `heredar_atribuciones`, campos, resoluciones", "IG5-105", "un fallo a mitad de escritura o una validación previa debilitada dejaba registros parciales o un estado inconsistente", "decorador `_atomica`: captura del estado, verificación final y restauración exacta", "AT14-01 a AT14-11; K56-M03; K56-M07", "el éxito deja una cadena válida y cero huérfanos (AT14-01 a AT14-11)", "`_estado_completo` y `_sin_huerfanos` (comparación del estado completo)"),
 ("D-04", "El auditor no comprobaba por eslabón la modificación, la duplicidad ni la ambigüedad", "`_hall_arte` y `_hall_identidad` (v13)", "IG5-106", "un motor que acepta una cadena corrupta no era detectado en eslabones modificados, duplicados o ambiguos", "auditor independiente `_hall_cadena` con implementación propia", "ADVC-01 a ADVC-24; K56-M04", "cero hallazgos del auditor en los fixtures válidos", "`_compartidas()` vacío (el auditor no usa funciones del motor)"),
 ("D-05", "La reactivación de una atribución histórica sin resolución no se detectaba", "`_auditar_resoluciones` (v13)", "IG5-107", "una atribución descartada podía volver a activa sin una resolución que la ordenara", "regla I15 del auditor de resoluciones", "ATTR-11; K56-M05", "escenarios de resoluciones válidos sin violaciones (ATTR precondición)", "auditor independiente (I15)"),
 ("D-06", "Las pruebas negativas de conservación de atribuciones e inmutabilidad de resoluciones eran incompletas", "`correr_mutaciones_resoluciones` (v13)", "IG5-107", "no había mutación específica para duplicados, modificación posterior, cambio de persona, pieza, versión o evento, ni auto-retiro", "doce mutaciones específicas ATTR-01 a ATTR-12", "ATTR-01 a ATTR-12", "precondición válida de cada ATTR", "auditor independiente (I8, I13, I15)"),
 ("D-07", "El conjunto E y la elegibilidad del evaluador no se reconstruían con comprobación de fallo cerrado", "`calcular_E` (v13)", "IG5-108", "un evaluador inactivo, sin permiso, sin asignación o dentro de E, o con procedencia incompleta, no quedaba bloqueado de forma verificable", "`elegibilidad_evaluador` (E1 a E7), asignación explícita, confirmación y publicación con revalidación", "E14-01 a E14-06; AT14-09; AT14-10; K56-M06", "E14-01 y E14-04 (evaluador elegible y E completo)", "`auditar_E`"),
 ("D-08", "Un evento de carga de otra fila podía quedar referenciado como evento original (relación RS-08 ausente)", "contrato de integridad de `contribution_events` (v13)", "IG5-103", "RS-02 fija evento, raíz y uploader entre eventos, pero no ata el evento de carga al asset raíz exacto", "RS-08 hacia creative_assets(organization_id, id, upload_event_id) con su clave única", "FK19, FK23, FK25; CHAIN-04; CHAIN-18", "RS-08 presente en el contrato, el inventario y la matriz (K55)", "K32, K44 y K55"),
 ("D-09", "Un evento de reutilización podía pertenecer a más de un asset", "`creative_assets` (v13)", "IG5-103", "no había una restricción única propia sobre el evento de reutilización", "unique(organization_id, reuse_event_id)", "FK41", "restricción presente en 4.4.9 y en el ALTER (K32)", "K32"),
 ("D-10", "La trazabilidad de cada relación RS a sus mutaciones FK era inexacta", "`modelo_estructural.RELACIONES_SOURCE` (v13)", "IG5-103", "algunas relaciones listaban mutaciones que no las prueban", "lista derivada de la descripción de cada mutación", "FK01 a FK41", "cada RS tiene al menos una mutación y cada mutación nombra una RS (K55)", "K55 y K57"),
 ("D-11", "K55 comparaba sobre todo texto y no los identificadores de las pruebas de cada relación", "`verificar_source` (v13)", "IG5-103", "una prueba inexistente citada en una relación no se detectaba", "comparación estructural: cada identificador citado existe en las pruebas ejecutadas", "mutaciones de K55 y de K57", "K55 y K57 aprueban sobre el documento válido", "K57 (trazabilidad regla → implementación → prueba → verificador)"),
 ("D-12", "Las mutaciones FK cubrían 15 casos y no los pares, el momento, la acción, ON UPDATE, el ciclo de inserción ni la unicidad propia", "`_FKM` del verificador (v13)", "IG5-103", "una FK con pares, acción o momento erróneos en RS-02, RS-03, RS-05, RS-06, RS-07 o RS-08 no se detectaba", "mutaciones FK16 a FK41", "FK16 a FK41", "el documento válido pasa K32, K44, K45 y K55", "K32, K44, K45 y K55"),
]
TRAZA_V14 = [
 ("IG5-104", "`Motor.reconstruir_cadena_procedencia`, `Motor._siguiente_eslabon`, `Motor._verificar_reutilizado`, `Motor._verificar_modificado`, `Motor._verificar_raiz`, `Motor._datos_evento`, `Motor._origen_carga`", "CHAIN-01 a CHAIN-24", "K56"),
 ("IG5-105", "`_atomica`, `Motor._verificar_final`, `Motor._invariantes_basicos`", "AT14-01 a AT14-11; K56-M03; K56-M07", "K56"),
 ("IG5-106", "`_hall_cadena`, `auditar_E`, `_compartidas`", "ADVC-01 a ADVC-24; K56-M04", "K56"),
 ("IG5-107", "`_auditar_resoluciones`, `RegistroResoluciones`, `ResolucionInmutable`", "ATTR-01 a ATTR-12; K56-M05", "K56"),
 ("IG5-108", "`elegibilidad_evaluador`, `calcular_E_verificado`, `Motor.asignar_evaluador`, `Motor.confirmar_independencia`, `Motor.intentar_publicacion`", "E14-01 a E14-06; K56-M06", "K56"),
 ("IG5-109", "`RELACIONES_SOURCE`, `FK_DESC`, `UNICAS_SOURCE`, `UNICAS_PROPIAS_SOURCE`, `INVENTARIO_SOURCE`", "FK01 a FK41", "K32, K44, K45, K55"),
 ("IG5-110", "`AUDITORIA_V14`, `TRAZA_V14`, `RS_PUNTOS_V14`", "K56-M01 a K56-M08", "K57"),
]
RS_PUNTOS_V14 = [
 "tabla de origen existe", "tabla de destino existe", "columnas locales existen en el origen", "columnas referenciadas existen en el destino", "misma longitud de columnas",
 "organization_id en la primera posición de ambas listas", "orden y pares exactos según el modelo", "tipos compatibles columna a columna", "PK o UNIQUE de destino con las mismas columnas en el mismo orden",
 "acción ON DELETE esperada", "sin ON UPDATE", "momento de verificación esperado (inmediata o diferida)", "figura en el contrato de integridad", "figura en el inventario de columnas",
 "ciclo declarado o ausencia de ciclo de filas", "orden de inserción sin referencia a un paso no anterior", "columnas sin FK con excepción individual justificada (o sin excepciones)",
 "prueba negativa documental (al menos una mutación FK la nombra)", "prueba positiva de modelo en memoria (los identificadores citados existen)", "límite declarado: verificación documental, no validación en PostgreSQL",
]
assert len(RS_PUNTOS_V14) == 20

# ===== v15: datos de la auditoría, la trazabilidad, las 15 validaciones por evento propio y la equivalencia de K55 (se contrastan con el documento) =====
AUDITORIA_V15 = [
 ("D-13", "El evento propio de reutilización no se validaba contra la versión exacta del asset de destino (asset_version)", "`Motor._verificar_reutilizado` y `Motor._datos_evento` (v14)", "IG5-111", "solo se comparaba source_asset_version; un asset_version corrupto en cualquier eslabón se aceptaba y se guardaba la versión del origen en el evento del destino", "validar asset_version contra la versión exacta del asset que produjo el evento (`Motor._chk_asset_version`) y registrar la versión 1 del destino", "AV-01 a AV-08; K56-M09", "AP-04, AP-07", "auditor independiente `_hall_cadena`"),
 ("D-14", "El campo del evento propio no se comprobaba como «arte» en cada eslabón", "`Motor._datos_evento` y `reconstruir_cadena_procedencia` (v14)", "IG5-112", "un evento de reutilización o de carga intermedia vinculado a otro campo se aceptaba", "validar campo = arte y pertenencia a los campos permitidos (`Motor._chk_campo`)", "CF-01 a CF-08; K56-M10", "AP-07", "auditor independiente `_hall_cadena`"),
 ("D-15", "El rechazo no identificaba vínculo, evento, campo, valor esperado, valor hallado ni motivo", "`ReutilizacionInvalida` (v14)", "IG5-113", "un rechazo no permitía distinguir qué relación fallaba ni si otra excepción lo había provocado", "detalle estructurado por inconsistencia, sin datos internos en el mensaje al usuario", "AC-01 a AC-06; K56-M12", "AP-01 a AP-08", "mensaje_usuario sin identificadores internos"),
 ("D-16", "La atomicidad se probaba con pocos momentos de fallo y sin instantánea completa", "`pruebas_atomicidad14` (v14)", "IG5-114", "un fallo en la validación de asset_version, campo, actor o atribución, o durante el registro, no comparaba el estado completo ni los datos derivados", "instantánea completa antes y después y datos derivados idénticos en ocho momentos", "AT15-01 a AT15-08", "AT15-01 a AT15-08 (reintento sin fallo)", "`_estado_completo` y `_derivados`"),
 ("D-17", "El auditor independiente no comparaba asset_version ni campo por eslabón", "`_hall_cadena` (v14)", "IG5-115", "un motor que aceptaba un asset_version o un campo corrupto no era detectado", "`_hall_cadena` compara asset_version, campo, evento raíz y versión 1 con implementación propia", "ADV15-01 a ADV15-08; K56-M11", "AP-08", "`_compartidas` vacío"),
 ("D-18", "El identificador K55 estaba asignado a dos controles", "`verificar_expediente.py` (v12 a v14)", "IG5-116", "un identificador repetido impedía citar y mutar cada control de forma inequívoca", "segundo control renombrado a K55-V12 sin eliminar ninguna condición; K58 exige identificadores únicos y estables", "K57-D09 a K57-D12", "K58", "K58"),
]
TRAZA_V15 = [
 ("IG5-111", "`Motor._chk_asset_version`, `Motor._datos_evento`, `Motor._verificar_reutilizado`, `Motor.reconstruir_cadena_procedencia`", "AV-01 a AV-08; K56-M09", "K56"),
 ("IG5-112", "`Motor._chk_campo`, `Motor._campos_permitidos`, `Motor._datos_evento`", "CF-01 a CF-08; K56-M10", "K56"),
 ("IG5-113", "`ReutilizacionInvalida`, `Motor._chk_actor`, `Motor._chk_atribucion_reutilizador`, `_det`", "AC-01 a AC-06; AP-01 a AP-08; K56-M12", "K56"),
 ("IG5-114", "`_atomica`, `Motor._verificar_final`, `_derivados`, `_estado_completo`", "AT15-01 a AT15-08", "K56"),
 ("IG5-115", "`_hall_cadena`, `_hall_identidad`, `auditar_E`, `_compartidas`", "ADV15-01 a ADV15-08; K56-M11", "K56"),
 ("IG5-116", "`AUDITORIA_V15`, `TRAZA_V15`, `VALIDACIONES_EVENTO15`, `EQUIV_K55`", "K56-M09 a K56-M12", "K57, K58, K59"),
]
VALIDACIONES_EVENTO15 = [
 (1, "El evento existe", "`Motor._datos_evento`", "CHAIN-01 a CHAIN-24"),
 (2, "Su tipo corresponde a una reutilización", "`Motor._datos_evento`", "CHAIN-01 a CHAIN-24"),
 (3, "Pertenece a la organización correcta", "`Motor._datos_evento`", "CHAIN-01 a CHAIN-24"),
 (4, "Pertenece a la pieza correcta", "`Motor._datos_evento`", "CHAIN-01 a CHAIN-24"),
 (5, "Su actor autenticado coincide con el actor registrado", "`Motor._chk_actor`", "CHAIN-01 a CHAIN-24"),
 (6, "El asset de destino coincide con el asset que produjo el evento", "`Motor._datos_evento`", "AV-03; AC-06"),
 (7, "asset_version coincide con la versión exacta del asset de destino que produjo el evento", "`Motor._chk_asset_version`", "AV-01 a AV-08; AC-01; AC-03 a AC-05; K56-M09"),
 (8, "source_asset_id identifica el asset inmediato de origen", "`Motor._verificar_reutilizado`", "CHAIN-01 a CHAIN-24"),
 (9, "source_asset_version_id identifica su versión exacta", "`Motor._verificar_reutilizado`", "AC-06; CHAIN-01 a CHAIN-24"),
 (10, "source_asset_version coincide con el número de versión de esa referencia exacta", "`Motor._verificar_reutilizado`", "AV-06; AP-04"),
 (11, "source_upload_event_id identifica el evento original de carga del asset raíz", "`Motor._verificar_reutilizado`", "CHAIN-01 a CHAIN-24"),
 (12, "source_uploader_id coincide con el uploader original", "`Motor._verificar_reutilizado`", "CHAIN-01 a CHAIN-24; AP-05"),
 (13, "source_attribution_id identifica la atribución directa correspondiente", "`Motor._chk_atribucion_reutilizador`", "CHAIN-01 a CHAIN-24; AP-06"),
 (14, "El evento está vinculado al campo arte", "`Motor._chk_campo`", "CF-01 a CF-08; K56-M10"),
 (15, "La versión de copy coincide con la versión exacta donde se utiliza el asset", "`Motor._datos_evento`", "CHAIN-01 a CHAIN-24"),
]
EQUIV_K55 = [
 ("K55", "Cobertura v13 (4.4.15): IG5-102, IG5-103 e IE-12; inventario source_*, RS-01 a RS-08, matriz de ciclos, orden de inserción, mutaciones FK", "se conserva con su identificador"),
 ("K55-V12", "Cobertura v12 (4.4.14): IG5-101 e IE-12; I27 e I28, mutaciones A33 a A48, casos P15 a P20 y pruebas adversariales de identidad de origen", "antes también K55; se conservan sus condiciones íntegras"),
]
