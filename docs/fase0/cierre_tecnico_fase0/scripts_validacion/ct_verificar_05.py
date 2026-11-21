#!/usr/bin/env python3
# ct_verificar_05.py — veredicto INDEPENDIENTE de la prueba de concurrencia 05A/05B. Entradas: salida de A, salida de B y evidencia de un OBSERVADOR (otra conexión que muestrea
# pg_stat_activity / pg_blocking_pids). Ni A ni B pueden emitir PASS por sí solos: PASS exige que el servidor haya mostrado a B bloqueado por EXACTAMENTE la sesión A.
# Uso: python3 -I -B ct_verificar_05.py <salida_A.txt> <salida_B.txt> <observador.json>   -> 'PASS' (rc 0) o 'FAIL [codigo]' (rc 3)
import json, re, sys
def veredicto(a, b, obs):
    ma = re.search(r"SESION_A_LISTA\s*\|\s*(\d+)\s*\|\s*(\d+)", a or "")
    if not ma: return False, "05-A-SALIDA-AUSENTE"
    pa = int(ma.group(1))
    mb = re.search(r"([\d.]+)\s*\|\s*\w*\s*\|\s*\w*\s*\|\s*(ESPERO|NO_ESPERO|CONFLICTO_TRAS_COMMIT_DE_A|BLOCKED|FAIL)\s*\|\s*(\d+)\s*\|\s*(\d+)", b or "")
    if not mb: return False, "05-B-SALIDA-AUSENTE"
    veredicto_b, pb, pa_obs = mb.group(2), int(mb.group(3)), int(mb.group(4))
    if veredicto_b != "ESPERO": return False, "05-B-NO-ESPERO (%s)" % veredicto_b
    if pa_obs != pa: return False, "05-PID-NO-COINCIDEN (A informa %d, B observó %d)" % (pa, pa_obs)
    if not isinstance(obs, list) or not obs: return False, "05-SIN-EVIDENCIA-INDEPENDIENTE"
    bl = [m for m in obs if m.get("application_name") == "cci_05B" and m.get("pid") == pb and m.get("wait_event_type") == "Lock"]
    if not bl: return False, "05-SIN-EVIDENCIA-INDEPENDIENTE (el observador no vio a B bloqueada)"
    if not any(pa in (m.get("blocking_pids") or []) for m in bl): return False, "05-BLOQUEO-POR-OTRA-SESION (el bloqueador observado no es A)"
    if not any(m.get("application_name") == "cci_05A" and m.get("pid") == pa for m in obs): return False, "05-A-NO-OBSERVADA"
    return True, "PASS"
if __name__ == "__main__":
    try: a, b, o = open(sys.argv[1], encoding="utf-8").read(), open(sys.argv[2], encoding="utf-8").read(), json.load(open(sys.argv[3], encoding="utf-8"))
    except Exception as e: print("FAIL [05-ENTRADA-INVALIDA] %r" % e); sys.exit(3)
    ok, c = veredicto(a, b, o); print("PASS" if ok else "FAIL [%s]" % c); sys.exit(0 if ok else 3)
