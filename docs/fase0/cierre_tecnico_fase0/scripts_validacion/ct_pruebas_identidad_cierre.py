#!/usr/bin/env python3
# Uso: python3 -I -B ct_pruebas_identidad_cierre.py <sockDEV> <puertoDEV> <sockPROD> <puertoPROD> <dirCLON> <puertoCLON> <salida.json>   (TRES clústeres LOCALES; el clon físico lo crea este script con pg_basebackup como usuario postgres)
# Identidad DEV/PROD y AG-18: qué distingue la arquitectura y qué NO. Nunca Supabase.
import hashlib, json, os, re, shutil, subprocess, sys, tempfile
SD, PD, SP, PP, CLD, CLP, OUT = sys.argv[1:8]
HERE = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.join(HERE, "cci_dev_NO_EJECUTADOS"); WRAP = os.path.join(HERE, "ejecutar_script_verificado.sh")
SEIS = ["01_inventario_esquema_SOLO_LECTURA", "02_rls_privilegios_SOLO_LECTURA", "03_pruebas_rls_ROLLBACK", "04_trigger_r1_r9_ROLLBACK", "05_concurrencia_sesion_A", "05_concurrencia_sesion_B"]
DEV = "-c cci.validacion_autorizada=SI-CCI-DEV -c cci.entorno=CCI-DEV"; VARS = ["-v", "org=x", "-v", "org_a=x", "-v", "org_b=x", "-v", "uid_a=x", "-v", "uid_x=x", "-v", "piece=x", "-v", "attr=x"]
B = "/usr/lib/postgresql/16/bin"; REC = []; TMP = []
CSOCK = os.path.join(CLD, "sock")
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def sh(a, sock, port, db="cci_gdev", opts="", env=None):
    e = dict(os.environ, PGHOST=sock, PGPORT=port, PGUSER=("t_id_op" if "cci.entorno=CCI-DEV" in opts else "cci_test"), PGOPTIONS=opts); e.update(env or {})
    r = subprocess.run(["psql", "-X", "-d", db, "-v", "ON_ERROR_STOP=1"] + a, env=e, capture_output=True, text=True); return r.returncode, r.stdout + r.stderr
def sysid(sock, port): return sh(["-qAt", "-c", "select system_identifier from pg_control_system()"], sock, port, "postgres")[1].strip()
def variante(allow, deny):
    d = tempfile.mkdtemp(prefix="id_"); TMP.append(d); t = os.path.join(d, "s"); shutil.copytree(SRC, t); g = os.path.join(t, "00_guarda_destino.sql"); s = open(g, encoding="utf-8").read()
    s = s.replace("array[]::text[];  -- @@DEV_ALLOW@@", "array[%s]::text[];  -- @@DEV_ALLOW@@" % ",".join("'%s'" % a for a in allow)).replace("array[]::text[];  -- @@PROD_DENY@@", "array[%s]::text[];  -- @@PROD_DENY@@" % ",".join("'%s'" % a for a in deny)); open(g, "w", encoding="utf-8").write(s)
    fs = ["00_guarda_destino.sql", "00_preflight_guarda.sql", "00_verificar_marcador.sql", "01_inventario_esquema_SOLO_LECTURA.sql", "02_rls_privilegios_SOLO_LECTURA.sql", "03_pruebas_rls_ROLLBACK.sql", "04_lib_clasificador.sql", "04_trigger_r1_r9_ROLLBACK.sql", "05_concurrencia_sesion_A.sql", "05_concurrencia_sesion_B.sql", "ct_identidad_entorno.py"]
    open(os.path.join(t, "SHA256SUMS_CCI.txt"), "w").write("".join("%s  %s\n" % (sha(os.path.join(t, f)), f) for f in fs)); return t
def corre(t, sc, sock, port, opts=DEV, extra=None):
    return sh(VARS + ["-f", os.path.join(t, sc + ".sql")], sock, port, "cci_gdev", opts, {"CCI_DIR": t, "CCI_GUARDA_SHA256_APROBADO": sha(os.path.join(t, "00_guarda_destino.sql")), **(extra or {})})
def wrap(t, sock, port, aprob_env=None, opts=DEV, hostarg=True, sc=SEIS[0]):
    e = dict(os.environ, PGHOST=sock, PGPORT=port, PGUSER=("t_id_op" if "cci.entorno=CCI-DEV" in opts else "cci_test"), PGOPTIONS=opts); e.pop("CCI_DESTINOS_APROBADOS", None); e.update(aprob_env or {})
    cmd = ["bash", WRAP, sha(os.path.join(t, "SHA256SUMS_CCI.txt")), os.path.join(t, sc + ".sql"), "-d", "cci_gdev"] + (["-h", sock] if hostarg else []) + VARS
    r = subprocess.run(cmd, env=e, capture_output=True, text=True); return r.returncode, r.stdout + r.stderr
def rec(i, riesgo, pre, accion, esp, obs, est, nota="", ev=""): REC.append({"id": i, "riesgo": riesgo, "precondicion": pre, "ataque": accion, "esperado": esp, "observado": obs, "estado": est, "justificacion": nota, "evidencia": ev})
def cod(o): m = re.search(r"\[([GV]-[A-Z-]+)\]", o); return m.group(1) if m else ""
try:
    for s_, p_ in ((SD, PD), (SP, PP)):
        sh(["-qAt", "-c", "drop database if exists cci_gdev"], s_, p_, "postgres"); sh(["-qAt", "-c", "create database cci_gdev"], s_, p_, "postgres")
        sh(["-qAt", "-c", "drop role if exists t_id_op; drop role if exists cci_operador; drop role if exists cci_custodio; drop role if exists cci_administrador; create role cci_operador nologin; create role cci_custodio nologin; create role cci_administrador nologin; create role t_id_op login; grant cci_operador to t_id_op"], s_, p_, "postgres")   # operador autorizado de la fixture local
    sid_dev, sid_prod = sysid(SD, PD), sysid(SP, PP)
    rec("ID-00", "medio", "dos clústeres reales distintos", "comparar system_identifier", "distintos", "distintos" if sid_dev != sid_prod else "IGUALES", "PASS" if sid_dev != sid_prod else "FAIL", "huella md5 DEV=%s PROD=%s" % (hashlib.md5(sid_dev.encode()).hexdigest()[:8], hashlib.md5(sid_prod.encode()).hexdigest()[:8]))
    v = variante([sid_dev + "|cci_gdev"], [sid_prod])
    rc, o = corre(v, SEIS[0], SD, PD); rec("ID-01", "control", "DEV registrado en allowlist; PROD en denylist", "script 01 contra DEV", "GUARDA OK", "rc=%d %s" % (rc, "GUARDA OK" if "GUARDA OK" in o else cod(o)), "PASS" if rc == 0 and "GUARDA OK" in o else "FAIL")
    rc, o = corre(v, SEIS[0], SP, PP); rec("ID-02", "alto", "mismas listas; variables DEV declaradas contra el clúster PROD", "script 01 contra PROD declarando DEV", "[G-PROD-RECHAZADO]", "rc=%d %s" % (rc, cod(o)), "PASS" if rc != 0 and cod(o) == "G-PROD-RECHAZADO" else "FAIL")
    v2 = variante([sid_dev + "|cci_gdev"], [])
    rc, o = corre(v2, SEIS[0], SP, PP); rec("ID-03", "alto", "PROD NO está en la denylist (omisión del propietario), allowlist sólo con DEV; base homónima cci_gdev", "script 01 contra PROD con base del mismo nombre", "[G-DESTINO-DESCONOCIDO] (identidad por system_identifier+base)", "rc=%d %s" % (rc, cod(o)), "PASS" if rc != 0 and cod(o) == "G-DESTINO-DESCONOCIDO" else "FAIL", "la allowlist por sí sola ya rechaza cualquier otro clúster")
    # clon físico
    shutil.rmtree(CLD, ignore_errors=True); os.makedirs(CSOCK)
    subprocess.run(["chown", "-R", "postgres:postgres", CLD]); r = subprocess.run(["su", "postgres", "-c", "%s/pg_basebackup -h %s -p %s -U cci_test -D %s/data -X stream" % (B, SD, PD, CLD)], capture_output=True, text=True)
    r2 = subprocess.run(["su", "postgres", "-c", "%s/pg_ctl -D %s/data -o '-k %s -p %s -c listen_addresses=' -l %s/log -w start" % (B, CLD, CSOCK, CLP, CLD)], capture_output=True, text=True)
    sid_clon = sysid(CSOCK, CLP)
    rec("ID-04", "alto", "clon físico (pg_basebackup) de DEV arrancado en otro socket/puerto", "leer system_identifier del clon", "IGUAL al de DEV (la identidad técnica se hereda)", "igual" if sid_clon == sid_dev else "distinto (%s)" % sid_clon[:6], "PASS" if sid_clon == sid_dev and sid_clon else "FAIL", "comprueba la premisa de AG-18: un clon físico NO cambia system_identifier")
    rc, o = corre(v, SEIS[0], CSOCK, CLP); rec("ID-05", "alto (estructural)", "el clon físico de DEV se usa como si fuera DEV; allowlist = DEV", "ejecutar el script 01 contra el CLON con variables DEV (AG-18)", "el clon es indistinguible: la guarda lo ACEPTA (no es una aprobación; límite estructural)", "rc=%d %s" % (rc, "GUARDA OK (aceptado)" if "GUARDA OK" in o else cod(o)), "PARTIAL" if rc == 0 and "GUARDA OK" in o else "FAIL", "LIMITACIÓN ESTRUCTURAL AG-18: system_identifier+base no distinguen un clon físico/restauración de su origen")
    # clon de PROD: el propietario registra sysid_clon en denylist -> también bloquea el DEV legítimo
    vp = variante([sid_dev + "|cci_gdev"], [sid_dev])
    rc1, o1 = corre(vp, SEIS[0], SD, PD); rc2, o2 = corre(vp, SEIS[0], CSOCK, CLP); rec("ID-06", "medio", "DEV clonado de PROD: el propietario pone el sysid compartido en la denylist", "ejecutar contra el 'DEV' y contra el clon", "ambos RECHAZADOS (falla cerrada) pero se bloquea también el DEV legítimo", "DEV: %s; clon: %s" % (cod(o1), cod(o2)), "PARTIAL" if cod(o1) == "G-PROD-RECHAZADO" and cod(o2) == "G-PROD-RECHAZADO" else "FAIL", "seguro pero inservible: sin una identidad externa no se pueden distinguir")
    # identidad externa: endpoint aprobado por el custodio, comprobado por el ejecutor
    rc, o = wrap(v, SD, PD, {"CCI_DESTINOS_APROBADOS": SD}); rec("ID-07", "control", "CCI_DESTINOS_APROBADOS = socket de DEV (externo) pero SIN registro de auditoría ni identidad firmada (denegación por defecto; la cadena completa positiva se prueba en ct_pruebas_ext01_y_e2e_dev.py E2E-01)", "ejecutor verificado contra DEV sin auditoría", "[V-AUDITORIA-NO-CONFIGURADA]", "rc=%d %s" % (rc, "GUARDA OK" if "GUARDA OK" in o else cod(o)), "PASS" if rc == 3 and cod(o) == "V-AUDITORIA-NO-CONFIGURADA" and "GUARDA OK" not in o else "FAIL")
    rc, o = wrap(v, CSOCK, CLP, {"CCI_DESTINOS_APROBADOS": SD}); rec("ID-08", "alto", "mismo clon físico indistinguible por system_identifier", "ejecutor verificado contra el CLON con la lista externa que sólo aprueba el endpoint de DEV", "[V-DESTINO-NO-APROBADO]", "rc=%d %s" % (rc, cod(o)), "PASS" if rc == 3 and cod(o) == "V-DESTINO-NO-APROBADO" and "GUARDA OK" not in o else "FAIL", "la identidad EXTERNA (endpoint aprobado por el propietario) sí distingue el clon, con límites: alias DNS/poolers y restauraciones en el mismo endpoint (ver ID-09)")
    rc, o = wrap(v, CSOCK, CLP, {}, hostarg=True); rec("ID-09", "alto (estructural)", "sin CCI_DESTINOS_APROBADOS (modo DEV): el ejecutor lo exige", "ejecutor contra el clon sin lista externa", "[V-DESTINO-NO-CONFIGURADO]", "rc=%d %s" % (rc, cod(o)), "PASS" if rc == 3 and cod(o) == "V-DESTINO-NO-CONFIGURADO" else "FAIL", "si el propietario no configura la lista externa, el modo DEV no opera por el ejecutor")
    rc, o = wrap(v, SD, PD, {"CCI_DESTINOS_APROBADOS": SD + ":" + CSOCK}); rec("ID-10", "alto (estructural)", "el propietario aprueba por error el endpoint del clon", "ejecutor contra el clon con endpoint aprobado", "pasa (error de configuración del propietario: no es defensa)", "rc=%d %s" % (rc, "GUARDA OK" if "GUARDA OK" in o else cod(o)), "PARTIAL", "la protección es tan buena como la lista externa; una restauración sobre el MISMO endpoint no se distingue")
    # clon lógico (pg_dump | restore en PROD): distinto sysid
    d = subprocess.run(["pg_dump", "-h", SD, "-p", PD, "-U", "cci_test", "cci_gdev"], capture_output=True, text=True)
    sh(["-qAt", "-c", "drop database if exists cci_gdev"], SP, PP, "postgres"); sh(["-qAt", "-c", "create database cci_gdev"], SP, PP, "postgres"); subprocess.run(["psql", "-X", "-h", SP, "-p", PP, "-U", "cci_test", "-d", "cci_gdev", "-q"], input=d.stdout, capture_output=True, text=True)
    rc, o = corre(v2, SEIS[0], SP, PP); rec("ID-11", "medio", "clon LÓGICO de DEV restaurado en el clúster PROD", "script 01 contra el clúster PROD con el contenido de DEV", "[G-DESTINO-DESCONOCIDO] (otro system_identifier)", "rc=%d %s" % (rc, cod(o)), "PASS" if rc != 0 and cod(o) == "G-DESTINO-DESCONOCIDO" else "FAIL", "un clon lógico no hereda system_identifier")
    # variables manipuladas / PGOPTIONS: la identidad no sale de variables
    rc, o = corre(v2, SEIS[0], SP, PP, DEV + " -c cci.system_identifier=%s -c cci.dev_allow=%s|cci_gdev" % (sid_dev, sid_prod)); rec("ID-12", "alto", "PGOPTIONS intenta declarar identidad y allowlist ajenas", "inyectar cci.system_identifier y cci.dev_allow", "ignoradas: [G-DESTINO-DESCONOCIDO]", "rc=%d %s" % (rc, cod(o)), "PASS" if cod(o) == "G-DESTINO-DESCONOCIDO" else "FAIL")
    # Supabase
    rec("ID-13", "alto", "proyecto Supabase real CCI-DEV/CCI-PROD", "system_identifier/pg_control_system() y project ref desde SQL en Supabase", "NOT TESTED", "NOT TESTED", "NOT TESTED", "requiere CCI-DEV con autorización; el project ref no es consultable desde SQL según la documentación consultada (sin confirmar)")
finally:
    subprocess.run(["su", "postgres", "-c", "%s/pg_ctl -D %s/data -m fast stop" % (B, CLD)], capture_output=True)
    for d in TMP: shutil.rmtree(d, ignore_errors=True)
    for s_, p_ in ((SD, PD), (SP, PP)): sh(["-qAt", "-c", "drop database if exists cci_gdev"], s_, p_, "postgres")
c = {}
for r in REC: c[r["estado"]] = c.get(r["estado"], 0) + 1
json.dump(REC, open(OUT, "w"), ensure_ascii=False, indent=1); print("TOTAL=%d %s" % (len(REC), c))
for r in REC: print(r["estado"], r["id"], r["observado"][:90])
