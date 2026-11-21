#!/usr/bin/env python3
# Uso: python3 -I -B ct_pruebas_05_secuencia.py <socket> <puerto> <salida.json>   (PostgreSQL TEMPORAL LOCAL). Resolución de la dependencia 05A/05B (AUD-RF-04):
# A y B no se validan entre sí; el veredicto lo da ct_verificar_05.py con un observador independiente. Pruebas positivas y negativas (salida eliminada/alterada/intercambiada, observador ausente/ajeno, impostores).
import hashlib, json, os, re, subprocess, sys, threading, time, tempfile
SOCK, PORT, OUT = sys.argv[1:4]; HERE = os.path.dirname(os.path.abspath(__file__)); S = os.path.join(HERE, "cci_dev_NO_EJECUTADOS"); sys.path.insert(0, HERE)
import ct_verificar_05 as V
L = "-c cci.validacion_autorizada=SI-LOCAL-TEMPORAL -c cci.entorno=LOCAL-TEMPORAL"; U = "00000000-0000-0000-0000-0000000000"
ENV = dict(os.environ, PGHOST=SOCK, PGPORT=PORT, PGUSER="cci_test", PGOPTIONS=L, CCI_DIR=S, CCI_GUARDA_SHA256_APROBADO=hashlib.sha256(open(os.path.join(S, "00_guarda_destino.sql"), "rb").read()).hexdigest())
PV = ["-v", "org=" + U + "01", "-v", "piece=" + U + "02", "-v", "reviewer_a=" + U + "0a", "-v", "reviewer_b=" + U + "0b"]
def psql(args, db="cci_conc_smoke", env=None, timeout=120):
    r = subprocess.run(["psql", "-X", "-v", "ON_ERROR_STOP=1", "-P", "pager=off", "-d", db] + args, capture_output=True, text=True, env=env or ENV, timeout=timeout); return r.stdout + r.stderr
def q(sql, db="cci_conc_smoke"): return psql(["-qAt", "-c", sql], db=db).strip()
subprocess.run(["psql", "-X", "-d", "postgres", "-qAtc", "drop database if exists cci_conc_smoke", "-c", "create database cci_conc_smoke"], env=ENV, capture_output=True)
psql(["-q", "-f", os.path.join(HERE, "local_ext", "31_conc_smoke_fixture_LOCAL.sql")])
REC = []
def reg(i, obj, esp, obs, ok, nota=""): REC.append({"id": i, "objetivo": obj, "esperado": esp, "observado": obs, "estado": "PASS" if ok else "FAIL", "nota": nota}); print("%s | %s | %s | %s" % ("PASS" if ok else "FAIL", i, obj, obs))
def corrida():
    ra = {}; rb = {}; muestras = []; fin = threading.Event()
    def a(): ra["t"] = psql(PV + ["-f", os.path.join(S, "05_concurrencia_sesion_A.sql")])
    def obs():
        while not fin.is_set():
            o = q("select coalesce(json_agg(json_build_object('pid',pid,'application_name',application_name,'wait_event_type',wait_event_type,'blocking_pids',pg_blocking_pids(pid))),'[]') from pg_stat_activity where application_name in ('cci_05A','cci_05B')", db="postgres")
            try: muestras.extend(json.loads(o))
            except Exception: pass
            time.sleep(0.1)
    ta = threading.Thread(target=a); to = threading.Thread(target=obs); ta.start(); to.start(); time.sleep(1.5)
    rb["t"] = psql(PV + ["-f", os.path.join(S, "05_concurrencia_sesion_B.sql")]); ta.join(); fin.set(); to.join()
    return ra["t"], rb["t"], muestras
A, B, OBS = corrida()
ok, c = V.veredicto(A, B, OBS); reg("05-P1", "A y B reales + observador independiente", "PASS", c, ok)
reg("05-P2", "B no emite PASS propio (veredicto_propio ESPERO, no PASS)", "sin la palabra PASS en la salida de B", "PASS" not in B, "PASS" not in B)
ok, c = V.veredicto("", B, OBS); reg("05-N1", "salida de A eliminada", "FAIL 05-A-SALIDA-AUSENTE", c, (not ok) and "A-SALIDA-AUSENTE" in c)
ok, c = V.veredicto(A, "", OBS); reg("05-N2", "salida de B eliminada", "FAIL 05-B-SALIDA-AUSENTE", c, (not ok) and "B-SALIDA-AUSENTE" in c)
ok, c = V.veredicto(A, B.replace("ESPERO", "NO_ESPERO", 1), OBS); reg("05-N3", "veredicto de B alterado (ESPERO→NO_ESPERO)", "FAIL", c, not ok)
mb = re.search(r"(\|\s*ESPERO\s*\|\s*)(\d+)", B); Bf = B[:mb.start(2)] + str(int(mb.group(2)) + 7) + B[mb.end(2):]
ok, c = V.veredicto(A, Bf, OBS); reg("05-N4", "pid de B falsificado", "FAIL (sin evidencia del observador)", c, not ok)
ok, c = V.veredicto(B, A, OBS); reg("05-N5", "salidas de A y B intercambiadas", "FAIL", c, not ok)
ok, c = V.veredicto(A, B, []); reg("05-N6", "observador ausente (sin evidencia independiente)", "FAIL 05-SIN-EVIDENCIA-INDEPENDIENTE", c, (not ok) and "SIN-EVIDENCIA" in c)
OBS2 = [dict(m, blocking_pids=[999999] if m.get("application_name") == "cci_05B" else m.get("blocking_pids")) for m in OBS]
ok, c = V.veredicto(A, B, OBS2); reg("05-N7", "el bloqueador observado no es A", "FAIL 05-BLOQUEO-POR-OTRA-SESION", c, (not ok) and "OTRA-SESION" in c)
A2, B2, OBS_2 = corrida(); ok, c = V.veredicto(A2, B2, OBS_2); reg("05-P3", "segunda corrida independiente", "PASS", c, ok)
ok, c = V.veredicto(A, B, OBS_2); reg("05-N8", "evidencia de OTRA corrida (resultado heredado)", "FAIL", c, not ok)
# B sola: no debe ejecutarse ni dar PASS
Bs = psql(PV + ["-f", os.path.join(S, "05_concurrencia_sesion_B.sql")]); reg("05-N9", "B sin A: BLOCKED y sin inserción", "BLOCKED [05-A-NO-PRESENTE], 0 filas", "BLOCKED [05-A-NO-PRESENTE]" in Bs and q("select count(*) from public.piece_reviewer_assignments") == "0", "BLOCKED [05-A-NO-PRESENTE]" in Bs and q("select count(*) from public.piece_reviewer_assignments") == "0")
# impostor 1: sesión que se hace llamar cci_05A pero NO tiene transacción abierta con xid
imp = subprocess.Popen(["psql", "-X", "-d", "cci_conc_smoke", "-qAtc", "set application_name='cci_05A'; select pg_sleep(4)"], env=ENV, stdout=subprocess.PIPE, stderr=subprocess.PIPE); time.sleep(1)
Bi = psql(PV + ["-f", os.path.join(S, "05_concurrencia_sesion_B.sql")]); imp.wait()
reg("05-N10", "impostor 'cci_05A' sin xid", "B BLOQUEADA", "BLOCKED [05-A-NO-PRESENTE]" in Bi and "ESPERO" not in Bi, "BLOCKED [05-A-NO-PRESENTE]" in Bi and "ESPERO" not in Bi)
# impostor 2: sesión 'cci_05A' con xid pero sobre OTRA pieza (no bloquea a B): B no espera => B NO_ESPERO => veredicto FAIL
imp = subprocess.Popen(["psql", "-X", "-d", "cci_conc_smoke", "-qAtc", "set application_name='cci_05A'; begin; select pg_catalog.txid_current(); select pg_sleep(5); rollback;"], env=ENV, stdout=subprocess.PIPE, stderr=subprocess.PIPE); time.sleep(1)
Bj = psql(PV + ["-f", os.path.join(S, "05_concurrencia_sesion_B.sql")]); imp.wait()
fake_a = "SESION_A_LISTA | 1 | 1"; ok, c = V.veredicto(fake_a, Bj, [])
reg("05-N11", "impostor 'cci_05A' con xid pero sin conflicto", "B no espera y el veredicto es FAIL", c + " | B:" + ("NO_ESPERO" if "NO_ESPERO" in Bj else "?"), (not ok) and ("NO_ESPERO" in Bj or "BLOCKED" in Bj))
reg("05-N12", "sin residuos tras todas las corridas", "0 filas", q("select count(*) from public.piece_reviewer_assignments"), q("select count(*) from public.piece_reviewer_assignments") == "0")
json.dump(REC, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
n = sum(r["estado"] == "FAIL" for r in REC); print("TOTAL=%d PASS=%d FAIL=%d" % (len(REC), len(REC) - n, n)); sys.exit(1 if n else 0)
