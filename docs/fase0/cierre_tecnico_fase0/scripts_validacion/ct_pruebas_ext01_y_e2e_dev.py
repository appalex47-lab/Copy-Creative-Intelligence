#!/usr/bin/env python3
# Uso: python3 -I -B ct_pruebas_ext01_y_e2e_dev.py <dirTrabajo> <puertoBase> <salida.json>   (root; clústeres LOCALES; nunca Supabase/CCI-PROD)
# Parte 1 (EXT-01): aprobación Ed25519 del hash del conjunto (custodio). Claves EFÍMERAS de prueba: demuestran el MECANISMO criptográfico; NO sustituyen la aprobación real de un custodio externo (no definido).
# Parte 2: cadena completa en modo CCI-DEV local con clones físicos reales: aprobación -> destino -> auditoría -> identidad firmada -> guarda con autorización de operador -> cuerpo.
# El árbol de prueba inyecta la lista de destinos DEV con el system_identifier LOCAL; la guarda real queda con listas vacías (EXT-03).
import hashlib, json, os, re, shutil, subprocess, sys, time
W, PB, OUT = sys.argv[1], int(sys.argv[2]), sys.argv[3]
HERE = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.join(HERE, "cci_dev_NO_EJECUTADOS"); WRAP = os.path.join(HERE, "ejecutar_script_verificado.sh"); BIN = "/usr/lib/postgresql/16/bin"
ONCE = ["00_guarda_destino.sql", "00_preflight_guarda.sql", "00_verificar_marcador.sql", "01_inventario_esquema_SOLO_LECTURA.sql", "02_rls_privilegios_SOLO_LECTURA.sql", "03_pruebas_rls_ROLLBACK.sql", "04_lib_clasificador.sql", "04_trigger_r1_r9_ROLLBACK.sql", "05_concurrencia_sesion_A.sql", "05_concurrencia_sesion_B.sql", "ct_identidad_entorno.py"]
CAN = "CANARIO-CUERPO-EJECUTADO"; VARS = ["-v", "org=x", "-v", "org_a=x", "-v", "org_b=x", "-v", "uid_a=x", "-v", "uid_x=x", "-v", "piece=x", "-v", "attr=x"]
LOC = "-c cci.validacion_autorizada=SI-LOCAL-TEMPORAL -c cci.entorno=LOCAL-TEMPORAL"; DEVO = "-c cci.validacion_autorizada=SI-CCI-DEV -c cci.entorno=CCI-DEV"
REC = []
def run(c, **k): return subprocess.run(c, capture_output=True, text=True, **k)
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def psql(sock, port, sql, db="postgres", user="cci_test"): return run(["psql", "-X", "-h", sock, "-p", str(port), "-U", user, "-d", db, "-qAt", "-c", sql]).stdout.strip()
def cluster(n, port): d = os.path.join(W, n); r = run(["bash", os.path.join(HERE, "ct_nuevo_cluster.sh"), d, str(port)]); assert r.returncode == 0, r.stderr; return d
def parar(d): run(["su", "postgres", "-c", "%s/pg_ctl -D %s/data -m fast stop" % (BIN, d)])
def clon(o, n, port):
    d = os.path.join(W, n); os.makedirs(d + "/sock"); run(["chown", "-R", "postgres:postgres", d])
    assert run(["su", "postgres", "-c", "%s/pg_basebackup -h %s/sock -p %d -U cci_test -D %s/data -X stream -c fast" % (BIN, o[0], o[1], d)]).returncode == 0; return d
def arrancar(datadir, sockdir, port, log): r = run(["su", "postgres", "-c", "%s/pg_ctl -D %s/data -o \"-k %s -p %d -c listen_addresses=\" -l %s -w start" % (BIN, datadir, sockdir, port, log)]); assert r.returncode == 0, r.stderr
def keypair(n):
    k = os.path.join(W, "k_%s.pem" % n); p = os.path.join(W, "k_%s.pub" % n); run(["openssl", "genpkey", "-algorithm", "ed25519", "-out", k]); run(["openssl", "pkey", "-in", k, "-pubout", "-out", p]); return k, p, sha(p)
def firmar(k, doc): assert run(["openssl", "pkeyutl", "-sign", "-inkey", k, "-rawin", "-in", doc, "-out", doc + ".sig"]).returncode == 0
def ts(t): return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t))
def mkset(nombre, allow=None, canario=True):
    t = os.path.join(W, "set_" + nombre); shutil.rmtree(t, ignore_errors=True); os.makedirs(t)
    for f in ONCE: shutil.copy(os.path.join(SRC, f), t)
    if allow:
        g = open(t + "/00_guarda_destino.sql", encoding="utf-8").read().replace("array[]::text[];  -- @@DEV_ALLOW@@", "array['%s']::text[];  -- @@DEV_ALLOW@@" % allow); open(t + "/00_guarda_destino.sql", "w", encoding="utf-8").write(g)
    if canario:
        s = open(t + "/01_inventario_esquema_SOLO_LECTURA.sql", encoding="utf-8").read(); i = s.index("\\ir 00_verificar_marcador.sql") + len("\\ir 00_verificar_marcador.sql"); open(t + "/01_inventario_esquema_SOLO_LECTURA.sql", "w", encoding="utf-8").write(s[:i] + "\n\\echo " + CAN + s[i:])
    sums(t); return t
def sums(t): open(t + "/SHA256SUMS_CCI.txt", "w").write("".join("%s  %s\n" % (sha(os.path.join(t, f)), f) for f in ONCE))
def aprobacion(k, t, nombre, dur=3600, tipo="aprobacion_integridad", sumsh=None, ini=None):
    p = os.path.join(W, "apr_" + nombre + ".json"); a = time.time()
    open(p, "w").write(json.dumps({"schema": "cci-aprobacion/1", "tipo": tipo, "sums_sha256": sumsh or sha(t + "/SHA256SUMS_CCI.txt"), "emitida_utc": ts(a - 60), "expira_utc": ts(a + dur), "custodio": "CUSTODIO-DE-PRUEBA-EFIMERO"}, indent=1) + "\n"); firmar(k, p); return p
def wrap(apr, t, sock, port, kpub, khash, env=None, opts=LOC, extra=None, user="cci_test", db="cci_gdev", sc="01_inventario_esquema_SOLO_LECTURA.sql"):
    e = {k: v for k, v in os.environ.items() if not k.startswith("CCI_")}; e.update(PGOPTIONS=opts, CCI_CUSTODIO_PUBKEY=kpub or "", CCI_CUSTODIO_PUBKEY_SHA256=khash or ""); e.update(env or {})
    r = run(["bash", WRAP, apr, os.path.join(t, sc), "-h", sock, "-p", str(port), "-U", user, "-d", db] + VARS + (extra or []), env=e); return r.returncode, r.stdout + r.stderr
def cod(o): m = re.findall(r"NO EJECUTADO \[([A-Z0-9-]+)\]", o); return m[0] if m else ""
def caso(i, ob, esp, res, nota="", extra_ok=True):
    rc, o = res
    if esp == "OK": ok = rc == 0 and "GUARDA OK" in o and CAN in o and extra_ok
    else: ok = rc != 0 and cod(o) == esp and CAN not in o and extra_ok
    REC.append({"id": i, "objetivo": ob, "esperado": esp, "observado": "rc=%d %s canario=%s" % (rc, cod(o) or ("GUARDA OK" if "GUARDA OK" in o else o[-80:].replace("\n", " ")), CAN in o), "estado": "PASS" if ok else "FAIL", "nota": nota}); print("%s | %s | %s | rc=%d %s" % ("PASS" if ok else "FAIL", i, ob, rc, cod(o) or ("OK" if "GUARDA OK" in o else o[-70:].replace("\n", " "))))
shutil.rmtree(W, ignore_errors=True); os.makedirs(W); os.chmod(W, 0o755)
DEV = cluster("dev", PB); PROD = cluster("prod", PB + 1); B = "cci_gdev"
for d, p in ((DEV, PB), (PROD, PB + 1)):
    psql(d + "/sock", p, "create database cci_gdev"); psql(d + "/sock", p, "create role cci_operador nologin; create role cci_custodio nologin; create role cci_administrador nologin; create role t_op login; grant cci_operador to t_op; create role t_sin login")
SD = psql(DEV + "/sock", PB, "select system_identifier from pg_control_system()"); SP = psql(PROD + "/sock", PB + 1, "select system_identifier from pg_control_system()")
KC, PC, HC = keypair("custodio"); KX, PX, HX = keypair("atacante"); KN, PN, HN = keypair("custodio_rotado")
S, SK = DEV + "/sock", PB
# ====== PARTE 1: EXT-01 ======
t = mkset("ok"); ap = aprobacion(KC, t, "ok")
caso("EXT01-01", "firma válida del custodio de prueba sobre el hash del conjunto (control positivo; criptografía local, NO custodio real)", "OK", wrap(ap, t, S, SK, PC, HC))
caso("EXT01-02", "mismo uso con hash hexadecimal directo (modo anterior) sigue funcionando", "OK", wrap(sha(t + "/SHA256SUMS_CCI.txt"), t, S, SK, "", ""))
x = os.path.join(W, "apr_sigbad.json"); shutil.copy(ap, x); sg = bytearray(open(ap + ".sig", "rb").read()); sg[5] ^= 1; open(x + ".sig", "wb").write(sg); caso("EXT01-03", "firma inválida (bit alterado)", "V-APROBACION-FIRMA-INVALIDA", wrap(x, t, S, SK, PC, HC))
caso("EXT01-04", "clave pública incorrecta con SHA-256 externo correcto de OTRA clave (la del atacante, anclada a su propio hash)", "V-APROBACION-FIRMA-INVALIDA", wrap(ap, t, S, SK, PX, HX))
caso("EXT01-05", "clave pública sustituida sin que coincida con el SHA-256 externo aprobado", "V-APROBACION-CLAVE-NO-APROBADA", wrap(ap, t, S, SK, PX, HC))
caso("EXT01-06", "sin clave del custodio configurada", "V-APROBACION-CLAVE-NO-CONFIGURADA", wrap(ap, t, S, SK, "", ""))
y = os.path.join(W, "apr_hashalt.json"); open(y, "w").write(open(ap).read().replace(sha(t + "/SHA256SUMS_CCI.txt"), "0" * 64)); shutil.copy(ap + ".sig", y + ".sig"); caso("EXT01-07", "hash alterado dentro de la aprobación después de firmar", "V-APROBACION-FIRMA-INVALIDA", wrap(y, t, S, SK, PC, HC))
z = aprobacion(KX, t, "hash_atacante", sumsh="0" * 64); caso("EXT01-08", "hash alterado y re-firmado por el atacante (clave no aprobada)", "V-APROBACION-FIRMA-INVALIDA", wrap(z, t, S, SK, PC, HC))
t2 = mkset("manif"); ap2 = aprobacion(KC, t2, "manif"); open(t2 + "/SHA256SUMS_CCI.txt", "a").write("# alterado\n"); caso("EXT01-09", "manifiesto SHA256SUMS alterado tras la aprobación", "V-SUMS-HASH-DISTINTO", wrap(ap2, t2, S, SK, PC, HC))
t3 = mkset("arch"); ap3 = aprobacion(KC, t3, "arch"); open(t3 + "/02_rls_privilegios_SOLO_LECTURA.sql", "a").write("select 'ALTERADO';\n"); caso("EXT01-10", "archivo del conjunto alterado sin regenerar el manifiesto", "V-ARCHIVO-ALTERADO", wrap(ap3, t3, S, SK, PC, HC))
sums(t3); caso("EXT01-11", "archivo alterado Y manifiesto regenerado por el atacante: la aprobación ya no corresponde", "V-SUMS-HASH-DISTINTO", wrap(ap3, t3, S, SK, PC, HC))
ae = aprobacion(KC, t, "exp", dur=-10); caso("EXT01-12", "aprobación caducada", "V-APROBACION-CADUCADA", wrap(ae, t, S, SK, PC, HC))
caso("EXT01-13", "aprobación REUTILIZADA: aprobación del conjunto anterior aplicada al conjunto modificado", "V-SUMS-HASH-DISTINTO", wrap(ap, t3, S, SK, PC, HC))
caso("EXT01-14", "aprobación revocada (hash en CCI_CUSTODIO_REVOCADOS_SHA256)", "V-APROBACION-REVOCADA", wrap(ap, t, S, SK, PC, HC, env={"CCI_CUSTODIO_REVOCADOS_SHA256": sha(t + "/SHA256SUMS_CCI.txt")}))
ak = aprobacion(KX, t, "custodio_no_autorizado"); caso("EXT01-15", "custodio NO autorizado: firma con clave que no es la aprobada por el propietario", "V-APROBACION-FIRMA-INVALIDA", wrap(ak, t, S, SK, PC, HC))
os.remove(ap + ".sig") if False else None; asn = os.path.join(W, "apr_sinfirma.json"); shutil.copy(ap, asn); caso("EXT01-16", "aprobación sin archivo .sig", "V-APROBACION-AUSENTE", wrap(asn, t, S, SK, PC, HC))
at = aprobacion(KC, t, "tipo", tipo="otra_cosa"); caso("EXT01-17", "aprobación firmada de otro tipo", "V-APROBACION-FORMATO", wrap(at, t, S, SK, PC, HC))
ad = os.path.join(W, "apr_dup.json"); open(ad, "w").write(open(ap).read().replace('"custodio"', '"sums_sha256": "%s",\n "custodio"' % ("1" * 64))); firmar(KC, ad); caso("EXT01-18", "dos sums_sha256 en la aprobación (firmada): ambigüedad rechazada", "V-APROBACION-FORMATO", wrap(ad, t, S, SK, PC, HC))
anr = aprobacion(KN, t, "rotada"); caso("EXT01-19", "rotación: aprobación con la clave NUEVA y su nuevo SHA-256", "OK", wrap(anr, t, S, SK, PN, HN))
caso("EXT01-20", "rotación: aprobación con la clave nueva frente al verificador anclado a la clave VIEJA", "V-APROBACION-FIRMA-INVALIDA", wrap(anr, t, S, SK, PC, HC))
caso("EXT01-21", "rotación: aprobación vieja frente al verificador anclado a la clave NUEVA", "V-APROBACION-FIRMA-INVALIDA", wrap(ap, t, S, SK, PN, HN))
caso("EXT01-22", "aprobación apuntando a un enlace simbólico de clave", "V-APROBACION-CLAVE-NO-CONFIGURADA", (lambda: (os.path.exists(W + "/lnk.pub") or os.symlink(PC, W + "/lnk.pub"), wrap(ap, t, S, SK, W + "/lnk.pub", HC))[1])())
# ====== PARTE 2: cadena completa CCI-DEV con clones físicos ======
tD = mkset("dev", allow="%s|%s" % (SD, B)); apD = aprobacion(KC, tD, "dev")
KA, PA, HA = keypair("autoridad")
def identidad(nombre, sysid, endpoint, entorno="CCI-DEV", proyecto="proj-dev-prueba", dur=3600, ini=None):
    d = os.path.join(W, "id_" + nombre); os.makedirs(d, exist_ok=True); a = time.time(); ini = a - 60 if ini is None else ini
    tk = {"schema": "cci-identidad-entorno/1", "tipo": "identidad_entorno", "entorno": entorno, "project_id": proyecto, "endpoint": endpoint, "base": B, "system_identifier": str(sysid), "serial": 5, "emitida_utc": ts(ini), "expira_utc": ts(ini + dur), "emisor": "AUTORIDAD-DE-PRUEBA-EFIMERA"}
    pol = {"schema": "cci-politica-confianza/1", "tipo": "politica_confianza", "emitida_utc": ts(a - 60), "expira_utc": ts(a + 86400), "entornos": {"CCI-DEV": {"proyectos_autorizados": ["proj-dev-prueba"], "serial_minimo": 3, "seriales_revocados": []}, "CCI-PROD": {"proyectos_autorizados": ["proj-prod-prueba"], "serial_minimo": 1, "seriales_revocados": []}}, "claves_revocadas_sha256": []}
    for n, o in (("token", tk), ("politica", pol)): p = os.path.join(d, n + ".json"); open(p, "w").write(json.dumps(o, indent=1)); firmar(KA, p); os.rename(p + ".sig", os.path.join(d, n + ".sig"))
    return d
LOGA = os.path.join(W, "auditoria.log"); iD = identidad("dev", SD, "%s:%d" % (S, SK))
def envdev(idir=iD, log=LOGA, destinos=None):
    e = {"CCI_DESTINOS_APROBADOS": destinos or S, "CCI_AUDITORIA_LOG": log or "", "CCI_IDENTIDAD_DIR": idir or "", "CCI_AUTORIDAD_PUBKEY": PA, "CCI_AUTORIDAD_PUBKEY_SHA256": HA}
    return {k: v for k, v in e.items() if v != ""}
def dev(user="t_op", sock=S, port=SK, env=None, ap=apD, t=tD): return wrap(ap, t, sock, port, PC, HC, env=env if env is not None else envdev(), opts=DEVO, user=user)
rc, o = dev(); lg = open(LOGA).read() if os.path.exists(LOGA) else ""
caso("E2E-01", "cadena completa CCI-DEV local: aprobación firmada + destino + identidad firmada + auditoría + operador autorizado", "OK", (rc, o), "", "db_user=t_op" in lg and "INICIO" in lg and "FIN" in lg and "rc=0" in lg)
caso("E2E-02", "sin CCI_IDENTIDAD_DIR/clave de autoridad (identidad no configurada)", "V-IDENTIDAD-NO-CONFIGURADA", dev(env={k: v for k, v in envdev().items() if k != "CCI_IDENTIDAD_DIR"}))
caso("E2E-03", "sin registro de auditoría configurado", "V-AUDITORIA-NO-CONFIGURADA", dev(env={k: v for k, v in envdev().items() if k != "CCI_AUDITORIA_LOG"}))
caso("E2E-04", "identidad caducada", "V-IDENTIDAD-CADUCADA", dev(env=envdev(idir=identidad("exp", SD, "%s:%d" % (S, SK), ini=time.time() - 7200))))
caso("E2E-05", "operador sin pertenencia a cci_operador (la identidad es válida, la guarda rechaza)", "", dev(user="t_sin"), "") if False else None
rc, o = dev(user="t_sin"); REC.append({"id": "E2E-05", "objetivo": "identidad válida pero operador sin rol cci_operador: rechaza la guarda", "esperado": "G-OPERADOR-NO-AUTORIZADO, sin canario", "observado": "rc=%d %s canario=%s" % (rc, re.findall(r"\[G-[A-Z-]+\]", o)[:1], CAN in o), "estado": "PASS" if rc != 0 and "[G-OPERADOR-NO-AUTORIZADO]" in o and CAN not in o else "FAIL", "nota": ""}); print(REC[-1]["estado"], "E2E-05", REC[-1]["observado"])
# clones físicos reales
CD = clon((DEV, SK), "clon_dev", PB + 2); CP = clon((PROD, PB + 1), "clon_prod", PB + 3)
arrancar(CD, CD + "/sock", PB + 2, CD + "/log"); arrancar(CP, CP + "/sock", PB + 3, CP + "/log")
caso("E2E-06", "CLON FÍSICO de PROD en otro endpoint, destino aprobado por error en la lista de hosts", "V-IDENTIDAD-ENDPOINT-DISTINTO", dev(sock=CP + "/sock", port=PB + 3, env=envdev(destinos=CP + "/sock")))
caso("E2E-07", "CLON FÍSICO de DEV en otro endpoint (misma base, mismo system_identifier)", "V-IDENTIDAD-ENDPOINT-DISTINTO", dev(sock=CD + "/sock", port=PB + 2, env=envdev(destinos=CD + "/sock")))
os.symlink(LOGA, W + "/log_enlace.log") if not os.path.exists(W + "/log_enlace.log") else None
caso("E2E-10", "registro de auditoría = /dev/null (ejecución sin registro real)", "V-AUDITORIA-INVALIDA", dev(env=envdev(log="/dev/null")))
caso("E2E-11", "registro de auditoría = enlace simbólico", "V-AUDITORIA-INVALIDA", dev(env=envdev(log=W + "/log_enlace.log")))
caso("E2E-12", "registro de auditoría con ruta relativa", "V-AUDITORIA-INVALIDA", dev(env=envdev(log="auditoria_rel.log")))
caso("E2E-13", "registro de auditoría en directorio inexistente (no escribible)", "V-AUDITORIA-NO-ESCRIBIBLE", dev(env=envdev(log=W + "/no_existe/dir/a.log")))
os.mkfifo(W + "/log_fifo.log") if not os.path.exists(W + "/log_fifo.log") else None
caso("E2E-14", "registro de auditoría = FIFO", "V-AUDITORIA-INVALIDA", dev(env=envdev(log=W + "/log_fifo.log")))
parar(CD); parar(CP); parar(DEV)
arrancar(CP, DEV + "/sock", SK, CP + "/log2")
caso("E2E-08", "TOMA DEL ENDPOINT: el clon físico de PROD arranca en el socket y puerto exactos de DEV (mismo host, puerto y base)", "V-IDENTIDAD-SYSID-DISTINTO", dev(), "el system_identifier real (que el clon hereda de PROD) no coincide con el firmado para DEV")
parar(PROD) if False else None
os.system("su postgres -c '%s/pg_ctl -D %s/data -m fast stop' >/dev/null 2>&1" % (BIN, CP))
arrancar(CD, DEV + "/sock", SK, CD + "/log2")
rc, o = dev(); lg2 = open(LOGA).read()
REC.append({"id": "E2E-09", "objetivo": "LÍMITE DOCUMENTADO: un clon físico de DEV que ocupa el endpoint de DEV ES indistinguible de DEV (y sólo contiene datos de DEV)", "esperado": "aceptado como DEV (no es un defecto: el riesgo AG-18 es confundir PROD con DEV)", "observado": "rc=%d guarda_ok=%s" % (rc, "GUARDA OK" in o), "estado": "PASS" if rc == 0 and "GUARDA OK" in o else "FAIL", "nota": "Si el clon de DEV fuera un problema, la autoridad debe emitir un nuevo token (nuevo serial/endpoint) y revocar el anterior."}); print(REC[-1]["estado"], "E2E-09", REC[-1]["observado"])
iR = identidad("rev", SD, "%s:%d" % (S, SK)); 
for p in (CD, PROD, DEV): parar(p)
json.dump(REC, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
n = sum(r["estado"] == "FAIL" for r in REC); print("TOTAL=%d PASS=%d FAIL=%d" % (len(REC), len(REC) - n, n)); sys.exit(1 if n else 0)
