#!/usr/bin/env python3
# Uso: python3 -I -B ct_pruebas_ext02_sonda.py <socket> <puerto> <salida.json>   Prueba la SONDA EXT-02 contra un clúster LOCAL (SIMULADO_LOCAL). No prueba Supabase: eso sigue BLOCKED hasta que el propietario la ejecute en CCI-DEV.
import json, os, subprocess, sys
S, P, OUT = sys.argv[1:4]; H = os.path.dirname(os.path.abspath(__file__)); T = os.path.join(H, "ct_ext02_validar_supabase_dev.py"); REC = []
def run(env, *a): e = {k: v for k, v in os.environ.items() if not k.startswith("CCI_") and not k.startswith("PG")}; e.update(env); r = subprocess.run(["python3", "-I", "-B", T, *a], capture_output=True, text=True, env=e); return r.returncode, r.stdout + r.stderr
base = {"PGHOST": S, "PGPORT": P, "PGUSER": "cci_test", "PGDATABASE": "postgres"}
def c(i, ob, ok, obs): REC.append({"id": i, "objetivo": ob, "observado": obs[:140], "estado": "PASS" if ok else "FAIL"}); print("PASS" if ok else "FAIL", i, ob)
rc, o = run(base, "--local"); c("EXT02-01", "sin CCI_EXT02_CONFIRMA_DEV la sonda se niega a conectar", rc == 2 and "X-SIN-CONFIRMACION" in o, o)
rc, o = run(dict(base, CCI_EXT02_CONFIRMA_DEV="SI-ES-CCI-DEV")); c("EXT02-02", "sin --local ni proyecto esperado se niega", rc == 2 and "X-PROYECTO-NO-COINCIDE" in o, o)
rc, o = run(dict(base, CCI_EXT02_CONFIRMA_DEV="SI-ES-CCI-DEV", PGHOST="db.abcd1234.supabase.co"), "--proyecto-esperado", "zzzz9999"); c("EXT02-03", "host que no contiene la referencia del proyecto esperado: se niega (antes de conectar)", rc == 2 and "X-PROYECTO-NO-COINCIDE" in o, o)
rc, o = run(dict(base, CCI_EXT02_CONFIRMA_DEV="SI-ES-CCI-DEV", PGHOST="db.abcd1234-prod.supabase.co"), "--proyecto-esperado", "abcd1234"); c("EXT02-04", "host con 'prod': se niega", rc == 2 and "X-PARECE-PROD" in o, o)
rc, o = run(dict(base, CCI_EXT02_CONFIRMA_DEV="SI-ES-CCI-DEV"), "--local"); d = json.loads(o) if o.startswith("{") else {}
c("EXT02-05", "contra clúster local: todos los checks PASS y etiquetado SIMULADO_LOCAL (no es evidencia de Supabase)", rc == 0 and d.get("modo") == "SIMULADO_LOCAL" and d.get("veredicto") == "PASS" and len(d.get("checks", [])) >= 10, o[:140])
rc, o = run(dict(base, CCI_EXT02_CONFIRMA_DEV="SI-ES-CCI-DEV", PGPORT="1"), "--local"); c("EXT02-06", "destino inalcanzable: nunca PASS", rc == 3 and '"veredicto": "PASS"' not in o, o[:140])
rc, o = run(dict(base, CCI_EXT02_CONFIRMA_DEV="SI-ES-CCI-DEV", PGUSER="cci_test"), "--local"); pers = subprocess.run(["psql", "-X", "-h", S, "-p", P, "-U", "cci_test", "-d", "postgres", "-qAt", "-c", "select count(*) from pg_class where relname='cci_sonda'"], capture_output=True, text=True).stdout.strip()
c("EXT02-07", "la sonda no deja objetos tras ejecutarse", pers == "0", "relname cci_sonda=%s" % pers)
json.dump(REC, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1); n = sum(r["estado"] == "FAIL" for r in REC); print("TOTAL=%d PASS=%d FAIL=%d" % (len(REC), len(REC) - n, n)); sys.exit(1 if n else 0)
