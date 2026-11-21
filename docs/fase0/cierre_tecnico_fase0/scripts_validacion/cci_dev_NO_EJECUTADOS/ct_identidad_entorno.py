#!/usr/bin/env python3
# ct_identidad_entorno.py — verificador de IDENTIDAD DE ENTORNO FIRMADA (AG-18). Forma parte del conjunto cuyo SHA-256 aprueba el custodio (SHA256SUMS_CCI.txt).
# Uso: python3 -I -B ct_identidad_entorno.py verificar --identidad-dir D --pubkey K.pem --pubkey-sha256 H --entorno CCI-DEV --endpoint host:puerto --base BASE --sysid N
# Autoridad EXTERNA (no definida todavía; NO se inventa): emite y firma (Ed25519) dos documentos JSON: token.json (+ token.sig) y politica.json (+ politica.sig). La clave pública y su SHA-256 los entrega
# el propietario por un canal ajeno a este repositorio y a la base de datos. Nada de lo que verifica puede venir de una variable de sesión, una GUC o una tabla de la base (clonables).
# Rechazo por defecto: cualquier ausencia, alteración, caducidad o inconsistencia => 'RECHAZADO [I-CODIGO]' y rc=3.
# Un clon físico conserva system_identifier y datos, pero NO puede obtener un token: el token liga entorno + proyecto + endpoint + base + system_identifier y lo firma la autoridad.
import json, os, re, subprocess, sys, tempfile, hashlib, time, datetime
MAX_VALIDEZ_S = 7 * 24 * 3600
class Rechazo(Exception):
    def __init__(s, cod, det=""): s.cod = cod; s.det = det; super().__init__(cod)
def _bytes(p, cod):
    if not p or not os.path.isfile(p) or os.path.islink(p): raise Rechazo(cod, "ausente o enlace simbólico: %s" % p)
    return open(p, "rb").read()
def _sin_dup(pares):
    d = {}
    for k, v in pares:
        if k in d: raise Rechazo("I-FORMATO", "clave duplicada: %s" % k)
        d[k] = v
    return d
def _json(b, cod="I-FORMATO"):
    try: return json.loads(b.decode("utf-8"), object_pairs_hook=_sin_dup)
    except Rechazo: raise
    except Exception as e: raise Rechazo(cod, "JSON inválido: %r" % e)
def _firma_ok(doc_b, sig_b, pub_p):
    with tempfile.TemporaryDirectory(prefix="cci_fir.") as t:
        os.chmod(t, 0o700); a = os.path.join(t, "m"); s = os.path.join(t, "s"); open(a, "wb").write(doc_b); open(s, "wb").write(sig_b)
        r = subprocess.run(["/usr/bin/openssl", "pkeyutl", "-verify", "-pubin", "-inkey", pub_p, "-rawin", "-in", a, "-sigfile", s], capture_output=True, text=True)
        return r.returncode == 0 and "Verified" in r.stdout
def _t(s, cod):
    if not isinstance(s, str) or not re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", s): raise Rechazo(cod, "fecha mal formada: %r" % (s,))
    return calendar_ts(s)
def calendar_ts(s): import calendar; return calendar.timegm(time.strptime(s, "%Y-%m-%dT%H:%M:%SZ"))
def verificar(idir, pubkey, pub_sha, entorno, endpoint, base, sysid, ahora=None):
    ahora = time.time() if ahora is None else ahora
    if not re.fullmatch(r"[0-9a-f]{64}", pub_sha or ""): raise Rechazo("I-CLAVE-NO-APROBADA", "falta el SHA-256 externo de la clave pública")
    kb = _bytes(pubkey, "I-CLAVE-AUSENTE")
    if hashlib.sha256(kb).hexdigest() != pub_sha: raise Rechazo("I-CLAVE-NO-APROBADA", "la clave pública no coincide con el SHA-256 aprobado externamente")
    if not idir or not os.path.isdir(idir): raise Rechazo("I-AUSENTE", "falta el directorio de identidad")
    tb = _bytes(os.path.join(idir, "token.json"), "I-AUSENTE"); ts = _bytes(os.path.join(idir, "token.sig"), "I-AUSENTE")
    pb = _bytes(os.path.join(idir, "politica.json"), "I-POLITICA-AUSENTE"); ps = _bytes(os.path.join(idir, "politica.sig"), "I-POLITICA-AUSENTE")
    # 1) política de confianza (firmada): proyectos por entorno, serial mínimo, revocaciones
    if not _firma_ok(pb, ps, pubkey): raise Rechazo("I-POLITICA-FIRMA-INVALIDA")
    pol = _json(pb)
    if pol.get("schema") != "cci-politica-confianza/1" or pol.get("tipo") != "politica_confianza" or not isinstance(pol.get("entornos"), dict): raise Rechazo("I-FORMATO", "política")
    pe, px = _t(pol.get("emitida_utc"), "I-FORMATO"), _t(pol.get("expira_utc"), "I-FORMATO")
    if px - pe > MAX_VALIDEZ_S * 4: raise Rechazo("I-POLITICA-VALIDEZ-EXCESIVA")
    if ahora < pe: raise Rechazo("I-POLITICA-NO-VIGENTE"); 
    if ahora >= px: raise Rechazo("I-POLITICA-CADUCADA")
    if pub_sha in (pol.get("claves_revocadas_sha256") or []): raise Rechazo("I-CLAVE-REVOCADA")
    ents = pol["entornos"]
    if set(ents) - {"CCI-DEV", "CCI-PROD"}: raise Rechazo("I-FORMATO", "entorno desconocido en la política")
    dev_p = set((ents.get("CCI-DEV") or {}).get("proyectos_autorizados") or []); prod_p = set((ents.get("CCI-PROD") or {}).get("proyectos_autorizados") or [])
    if dev_p & prod_p: raise Rechazo("I-POLITICA-INCONSISTENTE", "un proyecto figura a la vez en DEV y PROD")
    # 2) token de identidad (firmado)
    if not _firma_ok(tb, ts, pubkey): raise Rechazo("I-FIRMA-INVALIDA")
    tk = _json(tb)
    req = ("schema", "tipo", "entorno", "project_id", "endpoint", "base", "system_identifier", "serial", "emitida_utc", "expira_utc", "emisor")
    if any(k not in tk for k in req) or tk["schema"] != "cci-identidad-entorno/1" or tk["tipo"] != "identidad_entorno": raise Rechazo("I-FORMATO", "token")
    if not isinstance(tk["serial"], int) or isinstance(tk["serial"], bool) or not re.fullmatch(r"\d+", str(tk["system_identifier"])): raise Rechazo("I-FORMATO", "tipos del token")
    te, tx = _t(tk["emitida_utc"], "I-FORMATO"), _t(tk["expira_utc"], "I-FORMATO")
    if tx - te > MAX_VALIDEZ_S: raise Rechazo("I-VALIDEZ-EXCESIVA", "la identidad no puede durar más de 7 días")
    if ahora < te: raise Rechazo("I-NO-VIGENTE-AUN")
    if ahora >= tx: raise Rechazo("I-CADUCADA")
    if tk["entorno"] not in ents: raise Rechazo("I-ENTORNO-NO-EN-POLITICA")
    if tk["entorno"] != entorno: raise Rechazo("I-ENTORNO-DISTINTO", "el token es de otro entorno")
    pol_e = ents[tk["entorno"]]
    if tk["project_id"] not in (pol_e.get("proyectos_autorizados") or []): raise Rechazo("I-PROYECTO-NO-AUTORIZADO")
    if tk["endpoint"] != endpoint: raise Rechazo("I-ENDPOINT-DISTINTO", "el destino real no es el endpoint firmado")
    if tk["base"] != base: raise Rechazo("I-BASE-DISTINTA")
    if str(tk["system_identifier"]) != str(sysid): raise Rechazo("I-SYSID-DISTINTO", "el clúster real no es el firmado (clon o restauración)")
    if tk["serial"] < int(pol_e.get("serial_minimo", 1)): raise Rechazo("I-SERIAL-OBSOLETO", "identidad anterior reutilizada")
    if tk["serial"] in (pol_e.get("seriales_revocados") or []): raise Rechazo("I-REVOCADA")
    return "OK entorno=%s proyecto=%s serial=%d" % (tk["entorno"], tk["project_id"], tk["serial"])
if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] != "verificar": print("uso: verificar --identidad-dir D --pubkey K --pubkey-sha256 H --entorno E --endpoint H:P --base B --sysid N", file=sys.stderr); sys.exit(2)
    o = {a[i][2:].replace("-", "_"): a[i + 1] for i in range(1, len(a) - 1, 2) if a[i].startswith("--")}
    try: print(verificar(o.get("identidad_dir"), o.get("pubkey"), o.get("pubkey_sha256"), o.get("entorno"), o.get("endpoint"), o.get("base"), o.get("sysid")))
    except Rechazo as r: print("RECHAZADO [%s] %s" % (r.cod, r.det)); sys.exit(3)
    except Exception as e: print("RECHAZADO [I-ERROR-TECNICO] %r" % e); sys.exit(4)
