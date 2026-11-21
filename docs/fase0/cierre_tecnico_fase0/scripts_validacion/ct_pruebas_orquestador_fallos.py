#!/usr/bin/env python3
# Uso: python3 -I -B ct_pruebas_orquestador_fallos.py <raiz_repo> <salida.json>
# Meta-prueba del orquestador fail-fast. (1) Modo SIMULACIÓN (CCI_ORQ_SIMULAR=1; sólo máquina de estados; ningún veredicto real): fallo/bloqueo/excepción/mutación de archivo crítico/NOT_TESTED inyectados en CADA etapa A–K.
# (2) Fallos REALES en una copia git del repositorio: árbol sucio, SHA256SUMS alterado. Se comprueba: código de salida, etapas posteriores NO_STARTED y sin pasos, estado final correcto, run id nuevo en cada ejecución, BLOCKED/NOT_TESTED nunca PASS.
import json, os, re, shutil, subprocess, sys, tempfile
ROOT = os.path.abspath(sys.argv[1]); OUT = sys.argv[2]; ORQ = "docs/fase0/cierre_tecnico_fase0/scripts_validacion/ct_orquestador_fase0.py"; L = list("ABCDEFGHIJK"); REC = []; TMP = []
def copia():
    d = tempfile.mkdtemp(prefix="orq_meta."); TMP.append(d); rel = "docs/fase0/cierre_tecnico_fase0/scripts_validacion"; shutil.copytree(os.path.join(ROOT, rel), os.path.join(d, rel), ignore=shutil.ignore_patterns("__pycache__", "resultados")); return d
def corre(root, env=None, salida=None):
    s = salida or tempfile.mkdtemp(prefix="orq_out."); TMP.append(s); e = {k: v for k, v in os.environ.items() if not k.startswith("CCI_")}; e.update(env or {})
    r = subprocess.run(["python3", "-I", "-B", os.path.join(root, ORQ), root, s], capture_output=True, text=True, env=e, timeout=1800); J = json.load(open(os.path.join(s, "RESULTADO_ORQUESTADOR.json")))
    return r.returncode, J, r.stdout + r.stderr
def caso(i, ob, ok, obs): REC.append({"id": i, "objetivo": ob, "observado": str(obs)[:220], "estado": "PASS" if ok else "FAIL"}); print("PASS" if ok else "FAIL", i, ob, "->", str(obs)[:100])
SIM = {"CCI_ORQ_SIMULAR": "1"}; base = copia()
rc, J, _ = corre(base, SIM); caso("ORQ-S00", "simulación sin inyección: todas las etapas PASSED, código 0, estado SIMULACION_READY (nunca un veredicto real)", rc == 0 and J["estado_final"] == "SIMULACION_READY_FOR_OWNER_ACCEPTANCE" and all(v == "PASSED" for v in J["estados_etapas"].values()), (rc, J["estado_final"]))
r1 = J["ejecucion_id"]; rc, J2, _ = corre(base, SIM); caso("ORQ-S01", "cada ejecución genera un run id nuevo", J2["ejecucion_id"] != r1, (r1, J2["ejecucion_id"]))
for i, l in enumerate(L):
    posteriores = L[i + 1:]; previos = L[:i]
    for modo, rc_esp, fin in (("FAIL", 1, "SIMULACION_FAILED"), ("EXC", 1, "SIMULACION_FAILED"), ("MUTAR_CRITICO", 1, "SIMULACION_FAILED"), ("BLOCKED", 2, "SIMULACION_BLOCKED")):
        d = copia(); rc, J, o = corre(d, dict(SIM, CCI_ORQ_FALLO_EN="%s:%s" % (l, modo))); est = J["estados_etapas"]
        ok = (rc == rc_esp and J["estado_final"] == fin and est[l] in (("BLOCKED",) if modo == "BLOCKED" else ("FAILED",)) and all(est[x] == "PASSED" for x in previos) and all(est[x] == "NOT_STARTED" for x in posteriores)
              and not any(p["etapa"] in posteriores for p in J["pasos"]) and J["estado_final"] != "FASE0_READY_FOR_OWNER_ACCEPTANCE" and (modo != "MUTAR_CRITICO" or "críticos modificados" in J["causa"]) and (modo != "EXC" or "EXCEPCIÓN" in J["causa"]))
        caso("ORQ-%s-%s" % (l, modo), "%s inyectado en la etapa %s: detiene, código %d, etapas posteriores no iniciadas y sin pasos" % (modo, l, rc_esp), ok, (rc, J["estado_final"], est[l], "posteriores=%s" % {x: est[x] for x in posteriores[:2]}))
d = copia(); rc, J, o = corre(d, dict(SIM, CCI_ORQ_FALLO_EN="F:NOT_TESTED")); caso("ORQ-NT", "un paso NOT_TESTED nunca equivale a PASS: el estado final no es READY (BLOCKED, código 2) y el recuento lo declara", rc == 2 and "READY" not in J["estado_final"] and J["pasos_obligatorios"]["NOT_TESTED"] == 1, (rc, J["estado_final"], J["pasos_obligatorios"]))
# --- fallos REALES (modo normal, copia git)
def repo_git():
    d = tempfile.mkdtemp(prefix="orq_git."); TMP.append(d); subprocess.run(["git", "clone", "-q", "--no-hardlinks", ROOT, d], check=True, capture_output=True)
    subprocess.run(["git", "-C", d, "checkout", "-q", "--detach", subprocess.run(["git", "-C", ROOT, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()], check=True)
    rel = "docs/fase0/cierre_tecnico_fase0/scripts_validacion"; shutil.rmtree(os.path.join(d, rel)); shutil.copytree(os.path.join(ROOT, rel), os.path.join(d, rel), ignore=shutil.ignore_patterns("__pycache__"))   # el código EXACTO bajo prueba (incluye cambios aún sin commit en ROOT)
    subprocess.run("git -C '%s' add -A && git -C '%s' -c user.email=a@b -c user.name=meta commit -qm overlay --allow-empty" % (d, d), shell=True, check=True); return d
d = repo_git(); open(os.path.join(d, "docs/fase0/cierre_tecnico_fase0/scripts_validacion/archivo_sucio.txt"), "w").write("x"); rc, J, o = corre(d)
caso("ORQ-R1", "REAL: árbol git sucio -> FAILED en la etapa A, código 1, ninguna etapa posterior", rc == 1 and J["estado_final"] == "FASE0_FAILED" and J["estados_etapas"]["A"] == "FAILED" and all(v == "NOT_STARTED" for k, v in J["estados_etapas"].items() if k != "A"), (rc, J["estado_final"], J["causa"][:80]))
d = repo_git(); sv = os.path.join(d, "docs/fase0/cierre_tecnico_fase0/scripts_validacion/cci_dev_NO_EJECUTADOS"); open(os.path.join(sv, "02_rls_privilegios_SOLO_LECTURA.sql"), "a").write("\nselect 'alterado';\n")
subprocess.run("git -C '%s' -c user.email=a@b -c user.name=meta commit -qam meta-alterado" % d, shell=True, check=True); rc, J, o = corre(d)
caso("ORQ-R2", "REAL: script SQL alterado sin regenerar SHA256SUMS (árbol limpio): FAILED en A (sha256sums), código 1, sin clústeres ni etapas posteriores", rc == 1 and J["estados_etapas"]["A"] == "FAILED" and J["estados_etapas"]["B"] == "NOT_STARTED" and "sha256sums" in J["causa"], (rc, J["causa"][:100]))
for t in TMP: shutil.rmtree(t, ignore_errors=True)
json.dump(REC, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1); n = sum(r["estado"] == "FAIL" for r in REC); print("TOTAL=%d PASS=%d FAIL=%d" % (len(REC), len(REC) - n, n)); sys.exit(1 if n else 0)
