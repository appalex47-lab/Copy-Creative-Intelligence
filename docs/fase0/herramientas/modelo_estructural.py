"""Modelo estructural en memoria de K45 (integridad semántica) y K47 (conservación de atribuciones y cálculo de E).

Alcance: pruebas de modelo en memoria sobre entidades relacionadas. No es PostgreSQL ni Supabase: no valida RLS, transacciones,
concurrencia, locks ni rollback. Todos los datos son ficticios.
"""
import copy, difflib, hashlib, json

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

def _congelar(x):
    if isinstance(x, dict): return _Fila({k: _congelar(v) for k, v in x.items()})
    if isinstance(x, (list, tuple)): return tuple(_congelar(v) for v in x)
    return x

class RegistroResoluciones(dict):
    """Solo se agrega con agregar(). No hay asignación, reemplazo por el mismo ID, actualización ni eliminación."""
    def _no(s, *a, **k): raise ResolucionInmutable("el registro de resoluciones es de solo agregar")
    __setitem__ = __delitem__ = update = pop = popitem = clear = setdefault = __ior__ = _no
    def agregar(self, fila):
        if fila["id"] in self: raise ResolucionInmutable("el ID %s ya existe: una resolución no se reemplaza" % fila["id"])
        fila = dict(fila); fila["sello"] = sello_de(fila)
        dict.__setitem__(self, fila["id"], _congelar(fila)); return self[fila["id"]]

def _plano(o):
    """Copia plana (dict/list) de una estructura, apta para comparar instantáneas."""
    if isinstance(o, dict): return {k: _plano(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [_plano(v) for v in o]
    return copy.deepcopy(o)

CAMPOS_SOL = ("org", "atribucion", "afectado", "fuente", "pieza", "campo", "version_evidencia", "evento_motivador", "actor_cambio", "solicitante", "resolutor", "auth_uid", "evidencia", "motivo")

EVT_TIPO = {"brief": ("brief_editor", "brief_editor"), "promotion": ("promotion_editor", "promotion_editor"), "copy": ("copy_author", "copy_editor"), "asset": ("asset_uploader", "asset_uploader")}
TABLA_ATTR = {"brief": "brief_field_attributions", "promotion": "promotion_field_attributions", "copy": "copy_version_provenance", "asset": "copy_version_provenance"}
CLASIFICACIONES = ("sin_cambio", "introducido", "modificado", "sustituido", "eliminado")

class Motor:
    """Estado: versiones inmutables, atribuciones individuales, eventos, resoluciones y bitácora de estados (solo se agrega)."""
    def __init__(self, org="X"):
        self.org = org; self.v = {}; self.assets = {}; self.ev = {}; self.at = {}; self.est = []; self.res = RegistroResoluciones(); self.solicitudes = {}; self.arte_decl = {}; self.clas_hist = []
        self.members = {}; self.roles = {"revisor": {"piece.review"}, "editor": {"piece.edit"}, "admin": {"org.manage"}}; self.seq = 0; self.n = 0

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
    def introducir_campo(self, fuente, prev, nueva, campo, contenido, actor, pieza=None, refs=None, arte=None):
        pieza = pieza or (self.v[prev]["pieza"] if prev else "P1"); self._nueva(fuente, prev, nueva, pieza, refs or (self.v[prev]["refs"] if prev else None), actor, arte)
        self.v[nueva]["campos"][campo] = dict(contenido=contenido, clasif="introducido", eliminado=False); self.clas_hist.append((nueva, campo, "introducido"))
        e = self._evento(fuente, nueva, actor, campo); self._atribuir(fuente, nueva, campo, e, actor); return nueva
    def modificar_campo(self, fuente, prev, nueva, campo, contenido, actor):
        self._nueva(fuente, prev, nueva, self.v[prev]["pieza"], self.v[prev]["refs"], actor)
        self.v[nueva]["campos"][campo].update(contenido=contenido, clasif="modificado"); self.clas_hist.append((nueva, campo, "modificado"))
        e = self._evento(fuente, nueva, actor, campo); self._atribuir(fuente, nueva, campo, e, actor); return nueva
    def sustituir_campo(self, fuente, prev, nueva, campo, contenido, actor):
        self._nueva(fuente, prev, nueva, self.v[prev]["pieza"], self.v[prev]["refs"], actor)
        self.v[nueva]["campos"][campo].update(contenido=contenido, clasif="sustituido"); self.clas_hist.append((nueva, campo, "sustituido"))
        self._marcar_provisional(nueva, campo)
        e = self._evento(fuente, nueva, actor, campo); self._atribuir(fuente, nueva, campo, e, actor); return nueva
    def eliminar_campo(self, fuente, prev, nueva, campo, actor, material=True):
        self._nueva(fuente, prev, nueva, self.v[prev]["pieza"], self.v[prev]["refs"], actor)
        self.v[nueva]["campos"][campo].update(contenido=None, clasif="eliminado", eliminado=True); self.clas_hist.append((nueva, campo, "eliminado"))
        self._marcar_provisional(nueva, campo)
        if material: e = self._evento(fuente, nueva, actor, campo); self._atribuir(fuente, nueva, campo, e, actor)
        return nueva
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
    def registrar_asset(self, aid, copy_version, uploader, reused_from=None, material=True):
        """Asset nuevo (reused_from=None): uploader original y evento de carga. Asset reutilizado: conserva al uploader original y registra por separado al reutilizador y su evento."""
        pieza = self.v[copy_version]["pieza"]
        if reused_from is None:
            e = self._evento("asset", copy_version, uploader, "arte"); self.ev[e]["asset"] = aid; self.ev[e]["asset_version"] = 1
            self.assets[aid] = dict(id=aid, org=self.org, pieza=pieza, version_asset=1, tipo="nuevo", origen=None, previo=None, uploader=uploader, evento_carga=e, uploader_original=uploader, evento_carga_original=e,
                                    reutilizador=None, evento_reutilizacion=None, material=None, copy_version=copy_version)
            self._campo_arte(copy_version, aid, "introducido"); self._atribuir("asset", copy_version, "arte", e, uploader, used=aid)
            return aid
        raiz = self._raiz_asset(reused_from); er = self._evento("copy", copy_version, uploader, "arte"); self.ev[er]["asset"] = aid; self.ev[er]["asset_version"] = self.assets[reused_from]["version_asset"]
        self.assets[aid] = dict(id=aid, org=self.org, pieza=pieza, version_asset=1, tipo="reutilizado", origen=reused_from, origen_version_asset=self.assets[reused_from]["version_asset"], previo=None, uploader=None, evento_carga=None, uploader_original=raiz["uploader_original"],
                                evento_carga_original=raiz["evento_carga_original"], reutilizador=uploader, evento_reutilizacion=er, material=bool(material), copy_version=copy_version)
        cierre = set(self._cierre_asset(reused_from)); ov = self.assets[reused_from]["copy_version"]
        for b in sorted(self.activas(ov), key=lambda x: x["seq"]):
            if b["campo"] == "arte" and b.get("asset") in cierre:
                n = self._atribuir(b["fuente"], copy_version, "arte", b["evento"], b["persona"], "heredada", b["id"], b["origen_version"], aid)
                self.est.append(dict(seq=self.tick(), atr=n, estado="activa", resolucion=None, motivo="reutilización de %s" % reused_from))
        self._campo_arte(copy_version, aid, "introducido")
        if material: self._atribuir("copy", copy_version, "arte", er, uploader, used=aid)
        return aid
    def modificar_asset(self, prev, nueva, aid, aid_prev, editor):
        """Nueva versión del asset (fila nueva, previo = versión anterior). Quien la sube es el asset_uploader de esa fila; el uploader original y las atribuciones anteriores se conservan."""
        self._nueva("copy", prev, nueva, self.v[prev]["pieza"], self.v[prev]["refs"], editor); raiz = self._raiz_asset(aid_prev); e = self._evento("asset", nueva, editor, "arte"); self.ev[e]["asset"] = aid; self.ev[e]["asset_version"] = self.assets[aid_prev]["version_asset"] + 1
        self.assets[aid] = dict(id=aid, org=self.org, pieza=self.v[nueva]["pieza"], version_asset=self.assets[aid_prev]["version_asset"] + 1, tipo="modificado", origen=None, previo=aid_prev, uploader=editor, evento_carga=e,
                                uploader_original=raiz["uploader_original"], evento_carga_original=raiz["evento_carga_original"], reutilizador=None, evento_reutilizacion=None, material=None, copy_version=nueva)
        self._campo_arte(nueva, aid, "modificado"); self._marcar_provisional(nueva, "arte"); self._atribuir("asset", nueva, "arte", e, editor, used=aid); return nueva
    def sustituir_asset(self, prev, nueva, aid, aid_prev, uploader):
        self._nueva("copy", prev, nueva, self.v[prev]["pieza"], self.v[prev]["refs"], uploader); e = self._evento("asset", nueva, uploader, "arte"); self.ev[e]["asset"] = aid; self.ev[e]["asset_version"] = 1
        self.assets[aid] = dict(id=aid, org=self.org, pieza=self.v[nueva]["pieza"], version_asset=1, tipo="sustituto", origen=None, previo=None, sustituye=aid_prev, uploader=uploader, evento_carga=e, uploader_original=uploader,
                                evento_carga_original=e, reutilizador=None, evento_reutilizacion=None, material=None, copy_version=nueva)
        self._campo_arte(nueva, aid, "sustituido"); self._marcar_provisional(nueva, "arte"); self._atribuir("asset", nueva, "arte", e, uploader, used=aid); return nueva
    def eliminar_asset(self, prev, nueva, actor):
        return self.eliminar_campo("copy", prev, nueva, "arte", actor, True)

    # ---- 10: cambiar clasificación ----
    def cambiar_clasificacion(self, vid, campo, nueva, actor):
        assert nueva in CLASIFICACIONES
        self.clas_hist.append((vid, campo, nueva, "cambio por %s" % actor))
    def clasif_actual(self, vid, campo):
        h = [x for x in self.clas_hist if x[0] == vid and x[1] == campo]; return h[-1][2] if h else self.v[vid]["campos"][campo]["clasif"]

    # ---- 7, 8, 9: resoluciones de descarte (registros nuevos, con resultado definitivo y sello; nunca se modifican) ----
    def solicitar_resolucion(self, rid, **kw):
        """Formulario de solicitud: no es una resolución, no tiene resultado y no forma parte del estado auditado."""
        self.solicitudes[rid] = dict(kw); return rid
    def registrar_resolucion(self, rid, resultado, motivos=(), **sol):
        """Persiste una resolución con resultado definitivo ('aceptada' o 'rechazada'). El ID no puede existir."""
        assert resultado in ("aceptada", "rechazada")
        a = self.at.get(sol.get("atribucion")); p = sol.get("previo")
        fila = dict(id=rid, resultado=resultado, seq=self.tick(), motivos=tuple(motivos), version=a["version"] if a else None, version_origen=a["origen_version"] if a else None, previo=p,
                    previo_sello=self.res[p]["sello"] if p in self.res else None, **{k: sol.get(k) for k in CAMPOS_SOL})
        if resultado == "aceptada": fila["evidencia_historica"] = copy.deepcopy(self.v[sol["version_evidencia"]]["campos"].get(sol["campo"]))
        return self.res.agregar(fila)
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
            if o is not None and (e.get("asset_version") != o["version_asset"] or y.get("origen_version_asset") != o["version_asset"]): h.append("%s: el evento de reutilización de %s referencia otra versión de asset" % (cur, x))
            if e["version"] != y["copy_version"]: h.append("%s: el evento de reutilización de %s no referencia la versión exacta de copy" % (cur, x))
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
                if e.get("asset") != x or e.get("asset_version") != y["version_asset"]: out.append(("I23", "%s: el evento de carga de %s corresponde a otra versión del asset" % (cur, x)))
                if e["version"] != y["copy_version"]: out.append(("I23", "%s: el evento de carga de %s corresponde a otra versión de copy" % (cur, x)))
                if e["actor"] != u: out.append(("I23", "%s: el actor del evento de carga de %s no es el uploader" % (cur, x)))
                if e.get("auth") != u: out.append(("I23", "%s: el actor autenticado del evento de carga de %s no es el uploader" % (cur, x)))
                dirs = [b for b in AT.values() if b["persona"] == u and b.get("asset") == x and b["evento"] == y["evento_carga"] and b["rel"] == "directa"]
                if dirs and not any((b["version"], b["origen_version"], b["pieza"], b["org"], b.get("asset_version"), b["fuente"], b["campo"]) == (y["copy_version"], y["copy_version"], y["pieza"], y["org"], y["version_asset"], "asset", "arte") for b in dirs):
                    out.append(("I24", "%s: la atribución directa del uploader de %s no corresponde a la versión de copy, pieza u organización exactas" % (cur, x)))
            elif t == "reutilizado":
                r = y.get("reutilizador"); e = EV.get(y.get("evento_reutilizacion")); o = T.get(y.get("origen"))
                if y.get("uploader") is not None: out.append(("I17", "%s: el reutilizador figura como uploader de %s" % (cur, x)))
                m_ = MB.get(r)
                if m_ is not None and (m_["org"] != y["org"] or not m_.get("activo")): out.append(("I25", "%s: membresía inactiva o ajena del reutilizador %s" % (cur, r)))
                if y.get("evento_reutilizacion") is not None and [k for k, z in T.items() if z.get("evento_reutilizacion") == y["evento_reutilizacion"]] != [x]: out.append(("I25", "%s: la reutilización de %s no tiene evento propio" % (cur, x)))
                if e is None: continue
                if e["org"] != y["org"] or e["org"] != org: out.append(("I25", "%s: el evento de reutilización de %s pertenece a otra organización" % (cur, x)))
                if e["pieza"] != y["pieza"] or e["pieza"] != s["v"].get(y["copy_version"], {}).get("pieza"): out.append(("I25", "%s: el evento de reutilización de %s pertenece a otra pieza" % (cur, x)))
                if e["actor"] != r or e.get("auth") != r: out.append(("I25", "%s: el evento de reutilización de %s identifica a otro actor" % (cur, x)))
                if e.get("campo") != "arte" or e.get("asset") != x: out.append(("I25", "%s: el evento de reutilización de %s no es del asset exacto" % (cur, x)))
                if o is not None and (e.get("asset_version") != o["version_asset"] or y.get("origen_version_asset") != o["version_asset"]): out.append(("I25", "%s: el evento de reutilización de %s referencia otra versión de asset" % (cur, x)))
                if e["version"] != y["copy_version"]: out.append(("I25", "%s: el evento de reutilización de %s no referencia la versión exacta de copy" % (cur, x)))
    for b in AT.values():
        if b["version"] != cur or b["rel"] != "heredada" or not b.get("asset"): continue
        p = AT.get(b.get("previo"))
        if p is None: out.append(("I26", "%s: la atribución heredada %s carece de antecesor verificable" % (cur, b["id"])))
        elif (p["persona"], p["evento"], p["org"], p["fuente"], p["campo"], p["origen_version"]) != (b["persona"], b["evento"], b["org"], b["fuente"], b["campo"], b["origen_version"]) or p.get("asset") not in cierre(b["asset"]):
            out.append(("I26", "%s: el antecesor de la atribución heredada %s no corresponde a su cadena" % (cur, b["id"])))
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
    cod += [x for x in h if x[0] in ("I16", "I17", "I18", "I19", "I22", "I23", "I24", "I25", "I26") or (x[0] == "I20" and "registra arte o un asset" in x[1])]
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

def _mk(metodo, objetivo, fn):
    """Motor defectuoso: ejecuta el método correcto y después altera UNA relación del estado cuando el asset objetivo ya está registrado."""
    class _C(Motor): pass
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
A33 = _mk("modificar_asset", "a1b", lambda s: _set(_carga(s, "a1b"), version="cv1"))
A34 = _mk("registrar_asset", "a2", lambda s: _set(s.members["W"], activo=False))
A35 = _mk("registrar_asset", "a3", lambda s: _set(s.assets["a3"], evento_reutilizacion=s.assets["a2"]["evento_reutilizacion"]))
A36 = _mk("registrar_asset", "a1", lambda s: _set(_carga(s, "a1"), auth="Z"))
def _oculta(s): s.assets["ax"] = dict(id="ax", org="X", pieza="P1", version_asset=1, tipo="nuevo", origen=None, previo=None, uploader=None, evento_carga=None, uploader_original=None, evento_carga_original=None, reutilizador=None, evento_reutilizacion=None, material=None, copy_version="cv1")
A37 = _mk("introducir_campo", "cv1", _oculta)
ART_MUT2 = [("K47-A17", "el uploader pertenece a otra organización", "I22", A17, esc_art_nuevo, "otra organización"), ("K47-A18", "el uploader tiene membresía inactiva", "I22", A18, esc_art_nuevo, "membresía inactiva"),
            ("K47-A19", "el evento de carga pertenece a otra organización", "I23", A19, esc_art_nuevo, "otra organización"), ("K47-A20", "el evento de carga pertenece a otra pieza", "I23", A20, esc_art_nuevo, "otra pieza"),
            ("K47-A21", "el evento de carga corresponde a otra versión del asset", "I23", A21, esc_art_modificado, "otra versión del asset"), ("K47-A22", "el actor del evento de carga no es el uploader", "I23", A22, esc_art_nuevo, "no es el uploader"),
            ("K47-A23", "la atribución directa corresponde a otra versión de copy", "I24", A23, esc_art_reutilizado, "versión de copy"), ("K47-A24", "la atribución directa corresponde a otra pieza", "I24", A24, esc_art_reutilizado, "pieza"),
            ("K47-A25", "la atribución directa corresponde a otra organización", "I24", A25, esc_art_reutilizado, "organización"), ("K47-A26", "el evento de reutilización pertenece a otra organización", "I25", A26, esc_art_reutilizado, "otra organización"),
            ("K47-A27", "el evento de reutilización pertenece a otra pieza", "I25", A27, esc_art_reutilizado, "otra pieza"), ("K47-A28", "el evento de reutilización identifica a otro actor", "I25", A28, esc_art_reutilizado, "otro actor"),
            ("K47-A29", "el evento de reutilización referencia otra versión de asset", "I25", A29, esc_art_reutilizado, "otra versión de asset"), ("K47-A30", "la reutilización no referencia la versión exacta de copy", "I25", A30, esc_art_reutilizado, "versión exacta de copy"),
            ("K47-A31", "la reutilización intenta reemplazar al uploader original", "I17", A31, esc_art_reutilizado, "figura como uploader"), ("K47-A32", "la atribución heredada de asset carece de antecesor verificable", "I26", A32, esc_art_reutilizado, "antecesor verificable"),
            ("K47-A33", "el evento de carga corresponde a otra versión de copy", "I23", A33, esc_art_modificado, "otra versión de copy"), ("K47-A34", "el reutilizador tiene membresía inactiva", "I25", A34, esc_art_reutilizado, "membresía inactiva"),
            ("K47-A35", "dos reutilizaciones comparten el mismo evento", "I25", A35, esc_p10, "evento propio"), ("K47-A36", "el actor autenticado del evento de carga no es el uploader", "I23", A36, esc_art_nuevo, "autenticado"),
            ("K47-A37", "no_aplica oculta un asset registrado", "I20", A37, esc_art_noaplica, "no_aplica")]
ART_MUT = ART_MUT + ART_MUT2

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

BLOQ_IDS = {m[0] for m in ART_MUT2}
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
