#!/usr/bin/env python3
# Uso: python3 -I -B ct_permutaciones_scripts.py <socket> <puerto> <salida.json>   (PostgreSQL TEMPORAL LOCAL). Independencia de ORDEN de los 6 scripts por permutaciones CONTROLADAS:
# (a) las 24 permutaciones de {01,02,03,04} sobre el mismo shim (cada una en una base nueva), (b) los scripts 05A/05B con A primero y con B primero, (c) permutaciones con ejecuciones REPETIDAS
# (01,01,02,03,03,04). Criterio: la salida NORMALIZADA (sin marcas de tiempo/pid/uuid generados) de cada script es idéntica en todas las permutaciones y la huella de la base no cambia.
# No normaliza nada más: las diferencias se reportan. 05A/05B dependen de la concurrencia entre ellas (B espera a A): su "orden" es A→B por diseño (se documenta, no se declara independencia).
import hashlib, itertools, json, os, re, subprocess, sys, threading, time
SOCK, PORT, OUT = sys.argv[1:4]
HERE = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.join(HERE, "cci_dev_NO_EJECUTADOS")
LOC = "-c cci.validacion_autorizada=SI-LOCAL-TEMPORAL -c cci.entorno=LOCAL-TEMPORAL"; U = "00000000-0000-0000-0000-0000000000"
SC = {"01": "01_inventario_esquema_SOLO_LECTURA", "02": "02_rls_privilegios_SOLO_LECTURA", "03": "03_pruebas_rls_ROLLBACK", "04": "04_trigger_r1_r9_ROLLBACK", "05A": "05_concurrencia_sesion_A", "05B": "05_concurrencia_sesion_B"}
H = hashlib.sha256(open(os.path.join(SRC, "00_guarda_destino.sql"), "rb").read()).hexdigest()
def sh(a, db, env_extra=None):
    e = dict(os.environ, PGHOST=SOCK, PGPORT=PORT, PGUSER="cci_test", PGOPTIONS=LOC, CCI_DIR=SRC, CCI_GUARDA_SHA256_APROBADO=H); e.update(env_extra or {})
    r = subprocess.run(["psql", "-X", "-d", db] + a, env=e, capture_output=True, text=True, timeout=180); return r.returncode, r.stdout + r.stderr
def q(sql, db="postgres"): return sh(["-qAt", "-v", "ON_ERROR_STOP=1", "-c", sql], db)[1].strip()
def norm(o): return re.sub(r"\d{4}-\d\d-\d\d[ T][\d:.]+(\+\d\d(:\d\d)?)?|huella=\w+|[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}|\bpid=\d+|/tmp/cci\.\w+/g\.sql:\d+|\(\d+(\.\d+)? ?(ms|s)\)|=\d+\.\d+s", "<v>", o)
V4 = ["-v", "org=%s01" % U, "-v", "attr=%s02" % U, "-v", "affected=%s03" % U, "-v", "requester=%s04" % U, "-v", "change_actor=%s05" % U, "-v", "r_ok=%s06" % U, "-v", "r_nomember=%s07" % U, "-v", "r_noreview=%s08" % U, "-v", "r_direct=%s09" % U, "-v", "r_inherited=%s10" % U, "-v", "r_othersrc=%s11" % U, "-v", "r_benef=%s12" % U]
V3 = ["-v", "org_a=a0000000-0000-0000-0000-000000000001", "-v", "org_b=a0000000-0000-0000-0000-000000000002", "-v", "uid_a=a0000000-0000-0000-0000-0000000000a1", "-v", "uid_x=a0000000-0000-0000-0000-0000000000c1"]
def ejecuta(k, db):
    f = ["-v", "ON_ERROR_STOP=1", "-f", os.path.join(SRC, SC[k] + ".sql")]
    return sh((V4 if k == "04" else V3 if k in ("01", "02", "03") else []) + f, db)
def huella(db): return q("select md5(coalesce((select string_agg(c.relname||c.relkind, ',' order by c.relname) from pg_class c join pg_namespace n on n.oid=c.relnamespace where n.nspname not in ('pg_catalog','information_schema','pg_toast') and n.nspname !~ '^pg_temp'),'') || (select count(*) from pg_proc p join pg_namespace n on n.oid=p.pronamespace where n.nspname not in ('pg_catalog','information_schema'))::text || coalesce((select string_agg(rolname, ',' order by rolname) from pg_roles where rolname !~ '^pg_'),''))", db)
def shim(db):
    q("drop database if exists " + db); q("create database " + db); sh(["-q", "-v", "ON_ERROR_STOP=1", "-v", "variante=corregida", "-f", os.path.join(HERE, "local_ext", "30_shim_rls_fixture_LOCAL.sql")], db)
REF = {}; REC = []
def registra(cid, orden, k, rc, o, h0, h1):
    n = hashlib.sha256(norm(o).encode()).hexdigest()[:16]; REF.setdefault(k, n)
    REC.append({"id": cid, "orden": orden, "script": k, "rc": rc, "huella_salida_normalizada": n, "igual_a_referencia": n == REF[k], "sin_cambios_persistentes": h0 == h1})
n = 0
for perm in itertools.permutations(["01", "02", "03", "04"]):
    n += 1; db = "cci_perm_%02d" % n; shim(db); h0 = huella(db)
    for k in perm: rc, o = ejecuta(k, db); registra("PERM-%02d" % n, "-".join(perm), k, rc, o, h0, huella(db))
    q("drop database " + db)
for i, perm in enumerate([("01", "01", "02", "03", "03", "04"), ("04", "03", "03", "02", "01", "01"), ("03", "01", "04", "01", "03", "02")], 1):
    db = "cci_permr_%d" % i; shim(db); h0 = huella(db)
    for k in perm: rc, o = ejecuta(k, db); registra("PERMR-%d" % i, "-".join(perm), k, rc, o, h0, huella(db))
    q("drop database " + db)
# 05 A/B: A primero (diseño) y B primero; la dependencia A→B es por diseño (B espera el bloqueo de A)
for etq, primero in (("A-primero", "A"), ("B-primero", "B")):
    q("drop database if exists cci_perm05"); q("create database cci_perm05"); sh(["-q", "-v", "ON_ERROR_STOP=1", "-f", os.path.join(HERE, "local_ext", "31_conc_smoke_fixture_LOCAL.sql")], "cci_perm05"); h0 = huella("cci_perm05")
    P = ["-v", "ON_ERROR_STOP=1", "-v", "org=%s01" % U, "-v", "piece=%s02" % U, "-v", "reviewer_a=%s0a" % U, "-v", "reviewer_b=%s0b" % U]; out = {}
    def go(k): out[k] = sh(P + ["-f", os.path.join(SRC, SC[k] + ".sql")], "cci_perm05")
    seg = "B" if primero == "A" else "A"; t1 = threading.Thread(target=go, args=("05" + primero,)); t1.start(); time.sleep(1.5); go("05" + seg); t1.join()
    for k in ("05A", "05B"): registra("PERM05-" + etq, etq, k, out[k][0], out[k][1], h0, huella("cci_perm05"))
    q("drop database cci_perm05")
def eq(k, pred=lambda r: True): return all(r["igual_a_referencia"] for r in REC if r["script"] == k and pred(r))
res = {"permutaciones_01_04": len([r for r in REC if r["id"].startswith("PERM-")]) // 4, "todas_salidas_iguales": {k: eq(k, lambda r: not r["id"].startswith("PERM05")) for k in ("01", "02", "03", "04")}, "sin_cambios_persistentes": all(r["sin_cambios_persistentes"] for r in REC),
       "05_A_primero_vs_B_primero_iguales": {k: eq(k, lambda r: r["id"].startswith("PERM05")) for k in ("05A", "05B")}}
json.dump({"resumen": res, "registros": REC}, open(OUT, "w"), ensure_ascii=False, indent=1); print(json.dumps(res, ensure_ascii=False))
