#!/usr/bin/env python3
# Uso: python3 -I -B ct_pruebas_identidad_firmada.py <dirTrabajo> <puertoBase> <salida.json>   (requiere root: crea 4 clústeres LOCALES: DEV, PROD, clon físico de DEV y clon físico de PROD con pg_basebackup). Nunca Supabase ni CCI-PROD real.
# AG-18: la identidad confiable se verifica FUERA del contenido clonable de la base. Claves Ed25519 EFÍMERAS de prueba (NO son la autoridad real, que no está definida). Sin simulación de identificadores: los system_identifier son los reales de cada clúster.
import hashlib, json, os, re, shutil, subprocess, sys, time, calendar
W, PB, OUT = sys.argv[1], int(sys.argv[2]), sys.argv[3]
HERE = os.path.dirname(os.path.abspath(__file__)); VER = os.path.join(HERE, "cci_dev_NO_EJECUTADOS", "ct_identidad_entorno.py"); BIN = "/usr/lib/postgresql/16/bin"
REC = []
def run(c, **k): return subprocess.run(c, capture_output=True, text=True, **k)
def psql(sock, port, sql, db="postgres"): return run(["psql", "-X", "-h", sock, "-p", str(port), "-U", "cci_test", "-d", db, "-qAt", "-c", sql]).stdout.strip()
def cluster(nombre, port): 
    d = os.path.join(W, nombre); r = run(["bash", os.path.join(HERE, "ct_nuevo_cluster.sh"), d, str(port)]); assert r.returncode == 0, r.stderr; return d
def clon(origen, nombre, port):
    d = os.path.join(W, nombre); shutil.rmtree(d, ignore_errors=True); os.makedirs(d + "/sock"); run(["chown", "-R", "postgres:postgres", d])
    r = run(["su", "postgres", "-c", "%s/pg_basebackup -h %s/sock -p %d -U cci_test -D %s/data -X stream -c fast" % (BIN, origen[0], origen[1], d)]); assert r.returncode == 0, r.stderr
    r = run(["su", "postgres", "-c", "%s/pg_ctl -D %s/data -o \"-k %s/sock -p %d -c listen_addresses=\" -l %s/log -w start" % (BIN, d, d, port, d)]); assert r.returncode == 0, r.stderr; return d
def parar(d): run(["su", "postgres", "-c", "%s/pg_ctl -D %s/data -m fast stop" % (BIN, d)])
def keypair(n):
    k = os.path.join(W, "k_%s.pem" % n); p = os.path.join(W, "k_%s.pub" % n); run(["openssl", "genpkey", "-algorithm", "ed25519", "-out", k]); run(["openssl", "pkey", "-in", k, "-pubout", "-out", p])
    return k, p, hashlib.sha256(open(p, "rb").read()).hexdigest()
def firma(k, doc, sig): assert run(["openssl", "pkeyutl", "-sign", "-inkey", k, "-rawin", "-in", doc, "-out", sig]).returncode == 0
def ts(t): return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t))
def emitir(dirx, k, entorno, proyecto, endpoint, base, sysid, serial=5, ini=None, dur=3600, politica=None, pol_ini=None):
    os.makedirs(dirx, exist_ok=True); ahora = time.time(); ini = ahora - 60 if ini is None else ini
    tk = {"schema": "cci-identidad-entorno/1", "tipo": "identidad_entorno", "entorno": entorno, "project_id": proyecto, "endpoint": endpoint, "base": base, "system_identifier": str(sysid), "serial": serial, "emitida_utc": ts(ini), "expira_utc": ts(ini + dur), "emisor": "AUTORIDAD-DE-PRUEBA-EFIMERA"}
    pol = politica or {"schema": "cci-politica-confianza/1", "tipo": "politica_confianza", "emitida_utc": ts(ahora - 60), "expira_utc": ts(ahora + 86400),
                       "entornos": {"CCI-DEV": {"proyectos_autorizados": ["proj-dev-prueba"], "serial_minimo": 3, "seriales_revocados": [4]}, "CCI-PROD": {"proyectos_autorizados": ["proj-prod-prueba"], "serial_minimo": 1, "seriales_revocados": []}}, "claves_revocadas_sha256": []}
    for n, o in (("token", tk), ("politica", pol)):
        p = os.path.join(dirx, n + ".json"); open(p, "w").write(json.dumps(o, indent=1)); firma(k, p, os.path.join(dirx, n + ".sig"))
    return dirx
def ver(idir, pub, h, entorno, endpoint, base, sysid, extra_env=None):
    r = run(["python3", "-I", "-B", VER, "verificar", "--identidad-dir", idir, "--pubkey", pub, "--pubkey-sha256", h, "--entorno", entorno, "--endpoint", endpoint, "--base", base, "--sysid", str(sysid)], env=dict(os.environ, **(extra_env or {})))
    return r.returncode, (r.stdout + r.stderr).strip()
def caso(i, ob, esp_cod, res, nota=""):
    rc, o = res; cod = re.findall(r"RECHAZADO \[(I-[A-Z-]+)\]", o)
    ok = (rc == 0 and o.startswith("OK")) if esp_cod == "OK" else (rc == 3 and cod[:1] == [esp_cod])
    REC.append({"id": i, "objetivo": ob, "esperado": esp_cod, "observado": "rc=%d %s" % (rc, o[:110]), "estado": "PASS" if ok else "FAIL", "nota": nota}); print("%s | %s | %s | rc=%d %s" % ("PASS" if ok else "FAIL", i, ob, rc, o[:90]))
shutil.rmtree(W, ignore_errors=True); os.makedirs(W); os.chmod(W, 0o755)
DEV = cluster("dev", PB); PROD = cluster("prod", PB + 1)
for d, p in ((DEV, PB), (PROD, PB + 1)): psql(d + "/sock", p, "create database cci_gdev", "postgres")
S = {n: psql(d + "/sock", p, "select system_identifier from pg_control_system()") for n, d, p in (("dev", DEV, PB), ("prod", PROD, PB + 1))}
# el token legítimo también queda GUARDADO DENTRO de la base DEV (contenido clonable): no debe servir de nada en un clon
KA, PA, HA = keypair("autoridad"); KO, PO, HO = keypair("otro_entorno"); KX, PX, HX = keypair("atacante")
EP = {"dev": "%s/sock:%d" % (DEV, PB), "prod": "%s/sock:%d" % (PROD, PB + 1)}
tdev = emitir(W + "/id_dev", KA, "CCI-DEV", "proj-dev-prueba", EP["dev"], "cci_gdev", S["dev"])
tj = open(tdev + "/token.json").read().replace("'", "''")
psql(DEV + "/sock", PB, "create table public.identidad_en_bd(t text); insert into public.identidad_en_bd values ('%s')" % tj, "cci_gdev")
CDEV = clon((DEV, PB), "clon_dev", PB + 2); CPROD = clon((PROD, PB + 1), "clon_prod", PB + 3)
S["clon_dev"] = psql(CDEV + "/sock", PB + 2, "select system_identifier from pg_control_system()"); S["clon_prod"] = psql(CPROD + "/sock", PB + 3, "select system_identifier from pg_control_system()")
EP["clon_dev"] = "%s/sock:%d" % (CDEV, PB + 2); EP["clon_prod"] = "%s/sock:%d" % (CPROD, PB + 3)
tbd = psql(CDEV + "/sock", PB + 2, "select t from public.identidad_en_bd", "cci_gdev")
REC.append({"id": "AG-00", "objetivo": "los clones físicos son reales: mismo system_identifier que su origen y contenido de la BD copiado (incluido el token guardado en ella)", "esperado": "sysid(clon)=sysid(origen) y token presente en el clon",
            "observado": "dev=%s clon_dev=%s prod=%s clon_prod=%s token_en_clon=%s" % (S["dev"], S["clon_dev"], S["prod"], S["clon_prod"], "identidad_entorno" in tbd),
            "estado": "PASS" if S["dev"] == S["clon_dev"] and S["prod"] == S["clon_prod"] and S["dev"] != S["prod"] and "identidad_entorno" in tbd else "FAIL", "nota": ""})
print(REC[-1]["estado"], REC[-1]["observado"])
B = "cci_gdev"
caso("AG-01", "DEV legítimo con identidad firmada vigente (caso positivo)", "OK", ver(tdev, PA, HA, "CCI-DEV", EP["dev"], B, S["dev"]))
caso("AG-02", "CLON FÍSICO de DEV en otro endpoint con el token legítimo de DEV (mismo system_identifier y mismo token copiado)", "I-ENDPOINT-DISTINTO", ver(tdev, PA, HA, "CCI-DEV", EP["clon_dev"], B, S["clon_dev"]), "el clon conserva system_identifier; lo que lo delata es el endpoint firmado")
open(W + "/tok_desde_bd.json", "w").write(tbd); os.makedirs(W + "/id_desde_bd", exist_ok=True); shutil.copy(W + "/id_dev/token.sig", W + "/id_desde_bd/token.sig"); shutil.copy(W + "/id_dev/politica.json", W + "/id_desde_bd/"); shutil.copy(W + "/id_dev/politica.sig", W + "/id_desde_bd/"); shutil.copy(W + "/tok_desde_bd.json", W + "/id_desde_bd/token.json")
caso("AG-03", "token tomado del CONTENIDO CLONADO de la base y usado desde el clon", "I-ENDPOINT-DISTINTO", ver(W + "/id_desde_bd", PA, HA, "CCI-DEV", EP["clon_dev"], B, S["clon_dev"]), "la BD puede guardar lo que sea: la verificación no lee la BD")
caso("AG-04", "CLON FÍSICO de PROD presentado como DEV con el token legítimo de DEV", "I-ENDPOINT-DISTINTO", ver(tdev, PA, HA, "CCI-DEV", EP["clon_prod"], B, S["clon_prod"]))
caso("AG-05", "CLON FÍSICO de PROD que reclama el endpoint firmado de DEV (altera el destino declarado): el system_identifier real delata a PROD", "I-SYSID-DISTINTO", ver(tdev, PA, HA, "CCI-DEV", EP["dev"], B, S["clon_prod"]))
caso("AG-06", "PROD real reclamado como DEV con el endpoint de DEV (parámetros alterados)", "I-SYSID-DISTINTO", ver(tdev, PA, HA, "CCI-DEV", EP["dev"], B, S["prod"]))
tprod = emitir(W + "/id_prod", KA, "CCI-PROD", "proj-prod-prueba", EP["prod"], B, S["prod"], serial=2)
caso("AG-07", "identidad legítima de PROD presentada cuando se exige DEV (clon de PROD con su identidad)", "I-ENTORNO-DISTINTO", ver(tprod, PA, HA, "CCI-DEV", EP["prod"], B, S["prod"]))
caso("AG-08", "PROD real nunca se acepta como DEV, ni con identidad de PROD y endpoint de PROD", "I-ENTORNO-DISTINTO", ver(tprod, PA, HA, "CCI-DEV", EP["prod"], B, S["prod"]), "prohibición por entorno exigido, no por inventario")
# 3) ausente
caso("AG-09", "identidad ausente (directorio inexistente)", "I-AUSENTE", ver(W + "/no_existe", PA, HA, "CCI-DEV", EP["dev"], B, S["dev"]))
os.makedirs(W + "/id_vacio", exist_ok=True); caso("AG-10", "identidad ausente (directorio vacío)", "I-AUSENTE", ver(W + "/id_vacio", PA, HA, "CCI-DEV", EP["dev"], B, S["dev"]))
# 4) falsificada
tf = emitir(W + "/id_falsa", KX, "CCI-DEV", "proj-dev-prueba", EP["dev"], B, S["dev"]); caso("AG-11", "identidad FALSIFICADA: firmada por clave del atacante (token y política), verificada con la clave aprobada", "I-POLITICA-FIRMA-INVALIDA", ver(tf, PA, HA, "CCI-DEV", EP["dev"], B, S["dev"]))
caso("AG-12", "identidad falsificada con la clave pública del atacante entregada junto (sin aprobación externa de su hash)", "I-CLAVE-NO-APROBADA", ver(tf, PX, HA, "CCI-DEV", EP["dev"], B, S["dev"]), "el atacante no controla el SHA-256 externo")
caso("AG-13", "sin SHA-256 externo de la clave", "I-CLAVE-NO-APROBADA", ver(tdev, PA, "", "CCI-DEV", EP["dev"], B, S["dev"]))
caso("AG-14", "clave pública ausente", "I-CLAVE-AUSENTE", ver(tdev, W + "/no.pub", HA, "CCI-DEV", EP["dev"], B, S["dev"]))
# política legítima + token del atacante
shutil.copytree(tdev, W + "/id_tok_falso", dirs_exist_ok=True); emitir(W + "/_t", KX, "CCI-DEV", "proj-dev-prueba", EP["dev"], B, S["dev"]); shutil.copy(W + "/_t/token.json", W + "/id_tok_falso/token.json"); shutil.copy(W + "/_t/token.sig", W + "/id_tok_falso/token.sig")
caso("AG-15", "política legítima pero token firmado por el atacante", "I-FIRMA-INVALIDA", ver(W + "/id_tok_falso", PA, HA, "CCI-DEV", EP["dev"], B, S["dev"]))
# 5) firma inválida
shutil.copytree(tdev, W + "/id_sig", dirs_exist_ok=True); sg = bytearray(open(W + "/id_sig/token.sig", "rb").read()); sg[3] ^= 1; open(W + "/id_sig/token.sig", "wb").write(sg)
caso("AG-16", "firma inválida (un bit alterado en token.sig)", "I-FIRMA-INVALIDA", ver(W + "/id_sig", PA, HA, "CCI-DEV", EP["dev"], B, S["dev"]))
shutil.copytree(tdev, W + "/id_alt", dirs_exist_ok=True); open(W + "/id_alt/token.json", "w").write(open(W + "/id_alt/token.json").read().replace("proj-dev-prueba", "proj-prod-prueba"))
caso("AG-17", "token alterado después de firmar (proyecto cambiado)", "I-FIRMA-INVALIDA", ver(W + "/id_alt", PA, HA, "CCI-DEV", EP["dev"], B, S["dev"]))
shutil.copytree(tdev, W + "/id_pal", dirs_exist_ok=True); open(W + "/id_pal/politica.json", "w").write(open(W + "/id_pal/politica.json").read().replace("proj-dev-prueba", "proj-atacante"))
caso("AG-18", "política alterada después de firmar", "I-POLITICA-FIRMA-INVALIDA", ver(W + "/id_pal", PA, HA, "CCI-DEV", EP["dev"], B, S["dev"]))
shutil.copytree(tdev, W + "/id_psig", dirs_exist_ok=True); os.remove(W + "/id_psig/politica.sig"); caso("AG-19", "política sin firma", "I-POLITICA-AUSENTE", ver(W + "/id_psig", PA, HA, "CCI-DEV", EP["dev"], B, S["dev"]))
# 6) firma de otro entorno
tdo = emitir(W + "/id_otra_clave", KO, "CCI-DEV", "proj-dev-prueba", EP["dev"], B, S["dev"]); caso("AG-20", "firma de otro entorno/autoridad (clave distinta de la aprobada)", "I-POLITICA-FIRMA-INVALIDA", ver(tdo, PA, HA, "CCI-DEV", EP["dev"], B, S["dev"]))
caso("AG-21", "token firmado por la autoridad pero con entorno PROD exigido como DEV", "I-ENTORNO-DISTINTO", ver(tprod, PA, HA, "CCI-DEV", EP["dev"], B, S["dev"]))
# 7) expirada
te = emitir(W + "/id_exp", KA, "CCI-DEV", "proj-dev-prueba", EP["dev"], B, S["dev"], ini=time.time() - 7200, dur=3600); caso("AG-22", "identidad caducada", "I-CADUCADA", ver(te, PA, HA, "CCI-DEV", EP["dev"], B, S["dev"]))
tn = emitir(W + "/id_futura", KA, "CCI-DEV", "proj-dev-prueba", EP["dev"], B, S["dev"], ini=time.time() + 3600); caso("AG-23", "identidad aún no vigente", "I-NO-VIGENTE-AUN", ver(tn, PA, HA, "CCI-DEV", EP["dev"], B, S["dev"]))
tl = emitir(W + "/id_larga", KA, "CCI-DEV", "proj-dev-prueba", EP["dev"], B, S["dev"], dur=30 * 86400); caso("AG-24", "validez excesiva (>7 días)", "I-VALIDEZ-EXCESIVA", ver(tl, PA, HA, "CCI-DEV", EP["dev"], B, S["dev"]))
caso("AG-25", "identidad válida evaluada con reloj posterior a su caducidad (reloj inyectado)", "I-CADUCADA", (lambda: (lambda r: r)(__import__("subprocess").run(["python3", "-I", "-B", "-c", "import sys; sys.path.insert(0, %r); import ct_identidad_entorno as m, time\ntry: print(m.verificar(%r,%r,%r,'CCI-DEV',%r,%r,%r, ahora=time.time()+7200))\nexcept m.Rechazo as r: print('RECHAZADO [%%s]' %% r.cod); sys.exit(3)" % (os.path.dirname(VER), tdev, PA, HA, EP["dev"], B, S["dev"])], capture_output=True, text=True)))() and (lambda r: (r.returncode, (r.stdout + r.stderr).strip()))(subprocess.run(["python3", "-I", "-B", "-c", "import sys; sys.path.insert(0, %r); import ct_identidad_entorno as m, time\ntry: print(m.verificar(%r,%r,%r,'CCI-DEV',%r,%r,%r, ahora=time.time()+7200))\nexcept m.Rechazo as r: print('RECHAZADO [%%s]' %% r.cod); sys.exit(3)" % (os.path.dirname(VER), tdev, PA, HA, EP["dev"], B, S["dev"])], capture_output=True, text=True)))
# 8) proyecto equivocado
tp = emitir(W + "/id_proy", KA, "CCI-DEV", "proj-prod-prueba", EP["dev"], B, S["dev"]); caso("AG-26", "identidad válida con proyecto de PROD en token DEV", "I-PROYECTO-NO-AUTORIZADO", ver(tp, PA, HA, "CCI-DEV", EP["dev"], B, S["dev"]))
tp2 = emitir(W + "/id_proy2", KA, "CCI-DEV", "proj-desconocido", EP["dev"], B, S["dev"]); caso("AG-27", "identidad válida con proyecto desconocido", "I-PROYECTO-NO-AUTORIZADO", ver(tp2, PA, HA, "CCI-DEV", EP["dev"], B, S["dev"]))
pol_inc = {"schema": "cci-politica-confianza/1", "tipo": "politica_confianza", "emitida_utc": ts(time.time() - 60), "expira_utc": ts(time.time() + 86400), "entornos": {"CCI-DEV": {"proyectos_autorizados": ["compartido"], "serial_minimo": 1, "seriales_revocados": []}, "CCI-PROD": {"proyectos_autorizados": ["compartido"], "serial_minimo": 1, "seriales_revocados": []}}, "claves_revocadas_sha256": []}
ti = emitir(W + "/id_incons", KA, "CCI-DEV", "compartido", EP["dev"], B, S["dev"], politica=pol_inc); caso("AG-28", "política inconsistente: mismo proyecto en DEV y PROD", "I-POLITICA-INCONSISTENTE", ver(ti, PA, HA, "CCI-DEV", EP["dev"], B, S["dev"]))
# 9) reutilización de identidad anterior
to = emitir(W + "/id_serial_viejo", KA, "CCI-DEV", "proj-dev-prueba", EP["dev"], B, S["dev"], serial=2); caso("AG-29", "reutilización de identidad anterior (serial < mínimo de la política)", "I-SERIAL-OBSOLETO", ver(to, PA, HA, "CCI-DEV", EP["dev"], B, S["dev"]))
tr = emitir(W + "/id_revocada", KA, "CCI-DEV", "proj-dev-prueba", EP["dev"], B, S["dev"], serial=4); caso("AG-30", "identidad revocada (serial 4 en seriales_revocados)", "I-REVOCADA", ver(tr, PA, HA, "CCI-DEV", EP["dev"], B, S["dev"]))
pol_rev = {"schema": "cci-politica-confianza/1", "tipo": "politica_confianza", "emitida_utc": ts(time.time() - 60), "expira_utc": ts(time.time() + 86400), "entornos": {"CCI-DEV": {"proyectos_autorizados": ["proj-dev-prueba"], "serial_minimo": 1, "seriales_revocados": []}, "CCI-PROD": {"proyectos_autorizados": ["proj-prod-prueba"], "serial_minimo": 1, "seriales_revocados": []}}, "claves_revocadas_sha256": [HA]}
tk_ = emitir(W + "/id_clave_rev", KA, "CCI-DEV", "proj-dev-prueba", EP["dev"], B, S["dev"], politica=pol_rev); caso("AG-31", "clave de la autoridad revocada en la política (rotación)", "I-CLAVE-REVOCADA", ver(tk_, PA, HA, "CCI-DEV", EP["dev"], B, S["dev"]))
# rotación: nueva clave aprobada firma política+token nuevos; la clave vieja deja de aceptarse con el SHA nuevo
KN, PN, HN = keypair("rotada"); tnw = emitir(W + "/id_rotada", KN, "CCI-DEV", "proj-dev-prueba", EP["dev"], B, S["dev"], serial=6)
caso("AG-32", "rotación: identidad firmada con la clave NUEVA, aprobada con su nuevo SHA-256", "OK", ver(tnw, PN, HN, "CCI-DEV", EP["dev"], B, S["dev"]))
caso("AG-33", "rotación: identidad con la clave NUEVA pero el verificador sigue anclado a la clave VIEJA", "I-POLITICA-FIRMA-INVALIDA", ver(tnw, PA, HA, "CCI-DEV", EP["dev"], B, S["dev"]))
# 10) parámetros de conexión alterados
caso("AG-34", "endpoint alterado (otro puerto)", "I-ENDPOINT-DISTINTO", ver(tdev, PA, HA, "CCI-DEV", EP["dev"].rsplit(":", 1)[0] + ":1", B, S["dev"]))
caso("AG-35", "base alterada", "I-BASE-DISTINTA", ver(tdev, PA, HA, "CCI-DEV", EP["dev"], "postgres", S["dev"]))
caso("AG-36", "system_identifier alterado", "I-SYSID-DISTINTO", ver(tdev, PA, HA, "CCI-DEV", EP["dev"], B, int(S["dev"]) + 1))
caso("AG-37", "entorno exigido alterado a PROD con identidad DEV", "I-ENTORNO-DISTINTO", ver(tdev, PA, HA, "CCI-DEV".replace("DEV", "PROD"), EP["dev"], B, S["dev"]))
# robustez: formato, JSON duplicado, enlace simbólico, error técnico no confundido con rechazo de negocio
shutil.copytree(tdev, W + "/id_dup", dirs_exist_ok=True); open(W + "/id_dup/token.json", "w").write('{"schema":"x","schema":"y"}'); firma(KA, W + "/id_dup/token.json", W + "/id_dup/token.sig"); caso("AG-38", "JSON con claves duplicadas (firmado)", "I-FORMATO", ver(W + "/id_dup", PA, HA, "CCI-DEV", EP["dev"], B, S["dev"]))
shutil.copytree(tdev, W + "/id_lnk", dirs_exist_ok=True); os.remove(W + "/id_lnk/token.json"); os.symlink(tdev + "/token.json", W + "/id_lnk/token.json"); caso("AG-39", "token.json como enlace simbólico", "I-AUSENTE", ver(W + "/id_lnk", PA, HA, "CCI-DEV", EP["dev"], B, S["dev"]))
open(W + "/basura.pub", "w").write("no es una clave"); caso("AG-40", "clave 'aprobada' ilegible/corrupta con SHA-256 coincidente: nunca OK", "I-POLITICA-FIRMA-INVALIDA", ver(tdev, W + "/basura.pub", hashlib.sha256(b"no es una clave").hexdigest(), "CCI-DEV", EP["dev"], B, S["dev"]))
r = run(["python3", "-I", "-B", VER, "verificar"]); REC.append({"id": "AG-41", "objetivo": "argumentos incompletos => no OK", "esperado": "rc!=0", "observado": "rc=%d" % r.returncode, "estado": "PASS" if r.returncode != 0 and not (r.stdout + r.stderr).startswith("OK") else "FAIL", "nota": ""})
for d in (DEV, PROD, CDEV, CPROD): parar(d)
json.dump(REC, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
n = sum(r["estado"] == "FAIL" for r in REC); print("TOTAL=%d PASS=%d FAIL=%d" % (len(REC), len(REC) - n, n)); sys.exit(1 if n else 0)
