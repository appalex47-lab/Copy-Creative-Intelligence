#!/usr/bin/env python3
# ct_validar_listas_destinos.py — validación ESTRICTA de las listas de destinos (EXT-03). NO inventa valores: sólo valida los que entregue el propietario.
# Uso:
#   python3 -I -B ct_validar_listas_destinos.py archivo  LISTAS.json [--requerir-no-vacias]      valida el formato del archivo entregado por el propietario
#   python3 -I -B ct_validar_listas_destinos.py guarda   00_guarda_destino.sql --requerir-no-vacias   valida lo que la guarda contiene HOY (sin --requerir-no-vacias, vacío es sólo informativo)
#   python3 -I -B ct_validar_listas_destinos.py generar  LISTAS.json                                    imprime las dos líneas literales a pegar en la guarda (tras validar con --requerir-no-vacias)
# Formato LISTAS.json: {"schema":"cci-listas-destinos/1","dev_allow":["<system_identifier>|<base>",...],"prod_deny":["<system_identifier>",...]}
# Códigos: L-xx. rc 0 = válido, 3 = inválido (RECHAZADO [L-...]), 4 = error técnico. Una lista vacía cuando se exige NO-vacía es RECHAZO (no PASS).
import json, re, sys
class R(Exception):
    def __init__(s, c, d=""): s.c = c; s.d = d
def _sd(p):
    d = {}
    for k, v in p:
        if k in d: raise R("L-CLAVE-DUPLICADA", k)
        d[k] = v
    return d
SYS = re.compile(r"[1-9][0-9]{0,19}"); DB = re.compile(r"[A-Za-z_][A-Za-z0-9_]{0,62}"); MAXN = 64
def validar(dev, deny, req):
    if not isinstance(dev, list) or not isinstance(deny, list): raise R("L-TIPO", "las listas deben ser arreglos")
    if len(dev) > MAXN or len(deny) > MAXN: raise R("L-DEMASIADAS", "máximo %d entradas" % MAXN)
    if req and not dev: raise R("L-DEV-VACIA", "dev_allow vacía: el propietario debe aportar al menos un 'system_identifier|base' de CCI-DEV")
    if req and not deny: raise R("L-PROD-VACIA", "prod_deny vacía: el propietario debe aportar el system_identifier de CCI-PROD")
    ds = set()
    for e in dev:
        if not isinstance(e, str) or e.count("|") != 1: raise R("L-DEV-FORMATO", repr(e))
        s, b = e.split("|")
        if not SYS.fullmatch(s) or int(s) >= 2 ** 64: raise R("L-DEV-SYSID", repr(e))
        if not DB.fullmatch(b): raise R("L-DEV-BASE", repr(e))
        if len(set(s)) == 1: raise R("L-DEV-SYSID-MARCADOR", "identificador de relleno: " + e)
        if b.lower() in ("x", "xxx", "todo", "tbd", "changeme", "ejemplo"): raise R("L-DEV-BASE-MARCADOR", e)
        if e in ds: raise R("L-DEV-DUPLICADA", e)
        ds.add(e)
    ps = set()
    for e in deny:
        if not isinstance(e, str) or not SYS.fullmatch(e) or int(e) >= 2 ** 64: raise R("L-PROD-FORMATO", repr(e))
        if len(set(e)) == 1: raise R("L-PROD-SYSID-MARCADOR", e)
        if e in ps: raise R("L-PROD-DUPLICADA", e)
        ps.add(e)
    solap = {e.split("|")[0] for e in ds} & ps
    if solap: raise R("L-SOLAPAMIENTO", "un clúster no puede estar a la vez en CCI-DEV y en la lista de PRODUCCIÓN: " + ",".join(sorted(solap)))
    return "OK dev_allow=%d prod_deny=%d" % (len(ds), len(ps))
def desde_archivo(p):
    try: d = json.loads(open(p, "rb").read().decode("utf-8"), object_pairs_hook=_sd)
    except R: raise
    except FileNotFoundError: raise R("L-ARCHIVO-AUSENTE", p)
    except Exception as e: raise R("L-JSON", repr(e))
    if not isinstance(d, dict) or d.get("schema") != "cci-listas-destinos/1" or set(d) != {"schema", "dev_allow", "prod_deny"}: raise R("L-ESQUEMA", "claves exactas: schema, dev_allow, prod_deny")
    return d["dev_allow"], d["prod_deny"]
def desde_guarda(p):
    try: s = open(p, encoding="utf-8").read()
    except FileNotFoundError: raise R("L-ARCHIVO-AUSENTE", p)
    out = []
    for etq in ("DEV_ALLOW", "PROD_DENY"):
        m = re.findall(r"^\s*%s\s+text\[\]\s*:=\s*array\[(.*?)\]::text\[\];\s*--\s*@@%s@@" % ("dev_allow" if etq == "DEV_ALLOW" else "prod_deny", etq), s, re.M)
        if len(m) != 1: raise R("L-GUARDA-ESTRUCTURA", "no se encontró exactamente una línea de %s" % etq)
        body = m[0].strip(); out.append([] if not body else [x for x in re.findall(r"'([^']*)'", body)] if re.fullmatch(r"\s*'[^']*'\s*(,\s*'[^']*'\s*)*", body) else (_ for _ in ()).throw(R("L-GUARDA-LITERAL", "contenido no literal en " + etq)))
    return out[0], out[1]
if __name__ == "__main__":
    a = sys.argv[1:]; req = "--requerir-no-vacias" in a; a = [x for x in a if x != "--requerir-no-vacias"]
    try:
        if len(a) != 2 or a[0] not in ("archivo", "guarda", "generar"): print("uso: archivo|guarda|generar <ruta> [--requerir-no-vacias]", file=sys.stderr); sys.exit(2)
        dev, deny = desde_archivo(a[1]) if a[0] != "guarda" else desde_guarda(a[1])
        r = validar(dev, deny, req or a[0] == "generar")
        if a[0] == "generar": print("  dev_allow text[] := array[%s]::text[];  -- @@DEV_ALLOW@@" % ",".join("'%s'" % x for x in dev)); print("  prod_deny text[] := array[%s]::text[];  -- @@PROD_DENY@@" % ",".join("'%s'" % x for x in deny))
        else: print(r)
    except R as r: print("RECHAZADO [%s] %s" % (r.c, r.d)); sys.exit(3)
    except Exception as e: print("RECHAZADO [L-ERROR-TECNICO] %r" % e); sys.exit(4)
