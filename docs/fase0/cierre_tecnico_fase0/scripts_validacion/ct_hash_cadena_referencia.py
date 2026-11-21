#!/usr/bin/env python3
# DG-12 — Implementación de REFERENCIA (local, sin red) de la canonicalización y el hash encadenado propuestos. No es una decisión aprobada.
# Uso: python3 -I -B ct_hash_cadena_referencia.py [--pg <socket> <puerto>]   (con --pg contrasta el SHA-256 con PostgreSQL/pgcrypto del clúster TEMPORAL local)
import hashlib, json, unicodedata, sys, datetime as dt, subprocess
VER = "cci-hc-v1"
def _norm(v):
    if v is None: return None
    if isinstance(v, bool): return v
    if isinstance(v, int): return v
    if isinstance(v, float): raise ValueError("float prohibido: usar texto decimal (evita ambigüedad binaria)")
    if isinstance(v, dt.datetime):
        if v.tzinfo is None: raise ValueError("timestamp sin zona horaria prohibido")
        return v.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    if isinstance(v, str): return unicodedata.normalize("NFC", v)
    if isinstance(v, (list, tuple)): return [_norm(x) for x in v]
    if isinstance(v, dict): return {unicodedata.normalize("NFC", k): _norm(x) for k, x in v.items()}
    raise ValueError("tipo no soportado: %s" % type(v))
def canonico(fila: dict) -> bytes:
    """JSON con claves ordenadas, sin espacios, UTF-8 sin escapes ASCII, nulls explícitos; versión de formato como prefijo."""
    return (VER + "\n" + json.dumps(_norm(fila), sort_keys=True, separators=(",", ":"), ensure_ascii=False)).encode("utf-8")
def hash_fila(fila, hash_previo):  # hash_previo: hex de 64 o None (génesis = 64 ceros)
    prev = hash_previo or "0" * 64
    return hashlib.sha256(bytes.fromhex(prev) + canonico(fila)).hexdigest()
def construir(filas):
    out, h = [], None
    for f in filas: h = hash_fila(f, h); out.append(h)
    return out
def verificar(filas, hashes):
    """Devuelve el índice de la primera discrepancia o None."""
    h = None
    if len(filas) != len(hashes): return min(len(filas), len(hashes))
    for i, f in enumerate(filas):
        h = hash_fila(f, h)
        if h != hashes[i]: return i
    return None
T = dt.timezone(dt.timedelta(hours=-6))
F = [dict(id="a1", actor="u1", accion="aprobada", at=dt.datetime(2026, 11, 20, 10, 0, 0, 123456, tzinfo=dt.timezone.utc), nota=None),
     dict(id="a2", actor="u2", accion="rechazada", at=dt.datetime(2026, 11, 20, 11, 0, 0, tzinfo=T), nota="Ñandú"),
     dict(id="a3", actor="u1", accion="publicada", at=dt.datetime(2026, 11, 21, 0, 0, 0, tzinfo=dt.timezone.utc), nota="")]
R = []
def t(id_, desc, ok): R.append((id_, desc, "PASS" if ok else "FAIL"))
H = construir(F)
t("HC-01", "determinismo: dos construcciones idénticas", construir(F) == H)
t("HC-02", "independencia del orden de claves del origen", hash_fila(dict(reversed(list(F[0].items()))), None) == H[0])
t("HC-03", "zona horaria: misma instante en distinta zona produce el mismo hash", hash_fila(dict(F[0], at=F[0]["at"].astimezone(T)), None) == H[0])
t("HC-04", "null distinto de cadena vacía", hash_fila(dict(F[0], nota=""), None) != H[0])
t("HC-05", "NFC: 'é' compuesta y descompuesta producen el mismo hash", hash_fila(dict(F[0], nota="é"), None) == hash_fila(dict(F[0], nota="é"), None))
t("HC-06", "modificar un campo de la fila 2 se detecta en la fila 2", verificar([F[0], dict(F[1], nota="x"), F[2]], H) == 1)
t("HC-07", "borrar la fila 2 se detecta", verificar([F[0], F[2]], H) is not None)
t("HC-08", "reordenar filas se detecta", verificar([F[1], F[0], F[2]], H) == 0)
t("HC-09", "insertar una fila intermedia se detecta", verificar([F[0], dict(id="x", actor="u9", accion="x", at=F[0]["at"], nota=None), F[1], F[2]], H) is not None)
t("HC-10", "truncar el final se detecta por longitud (no por hash): requiere ancla externa del último hash", verificar(F[:2], H) is not None)
t("HC-11", "verificación íntegra de la cadena válida", verificar(F, H) is None)
try: hash_fila(dict(F[0], at=dt.datetime(2026, 1, 1)), None); ok = False
except ValueError: ok = True
t("HC-12", "timestamp sin zona se rechaza", ok)
try: hash_fila(dict(F[0], nota=1.5), None); ok = False
except ValueError: ok = True
t("HC-13", "float se rechaza (ambigüedad binaria)", ok)
t("HC-14", "versión de formato forma parte de la entrada (cambiar VER cambia el hash)", hashlib.sha256(bytes(32) + canonico(F[0]).replace(VER.encode(), b"cci-hc-v2", 1)).hexdigest() != H[0])
t("HC-15", "vector de regresión fijo de la fila 1 (generado por este mismo script: detecta cambios futuros, no es verificación independiente)", H[0] == "b0e998ca7d2dfdb2e1394f390fd032502be95e94e6a8c30bc86ff014f144602b")
if len(sys.argv) > 1 and sys.argv[1] == "--pg":
    sock, port = sys.argv[2], sys.argv[3]
    can = canonico(F[0]); q = "select encode(digest(decode('%s','hex') || convert_to($c$%s$c$,'UTF8'),'sha256'),'hex')" % ("00" * 32, can.decode("utf-8"))
    o = subprocess.run(["psql", "-h", sock, "-p", port, "-U", "cci_test", "-d", "cci_ct_ext", "-Atc", "create extension if not exists pgcrypto", "-c", q], capture_output=True, text=True).stdout.strip().split("\n")[-1]
    t("HC-16", "el SHA-256 de Python coincide con digest() de pgcrypto en el clúster local (misma entrada canónica)", o == H[0])
for r in R: print(" | ".join(r))
print("TOTAL=%d PASS=%d FAIL=%d" % (len(R), sum(r[2] == "PASS" for r in R), sum(r[2] == "FAIL" for r in R))); print("VECTOR fila1:", H[0])
