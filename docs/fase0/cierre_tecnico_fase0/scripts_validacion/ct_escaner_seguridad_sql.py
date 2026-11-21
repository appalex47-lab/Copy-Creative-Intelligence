#!/usr/bin/env python3
"""Escaner estatico de los 6 scripts SQL CCI-DEV + biblioteca. NO conecta a ninguna base.
Uso: python3 -I -B ct_escaner_seguridad_sql.py <dir_scripts> [salida.txt]"""
import re, sys, os, glob
d = sys.argv[1]; out = sys.argv[2] if len(sys.argv) > 2 else None
files = sorted(glob.glob(os.path.join(d, "*.sql")))
res = []; fails = 0
def chk(f, name, ok, det=""):
    global fails
    res.append((os.path.basename(f), name, "PASS" if ok else "FAIL", det))
    if not ok: fails += 1
def strip(s):
    s = re.sub(r"/\*.*?\*/", "", s, flags=re.S)
    return "\n".join(re.sub(r"--.*$", "", l) for l in s.splitlines())
for f in files:
    raw = open(f, encoding="utf-8").read(); code = strip(raw); low = code.lower()
    # texto sin literales ('...' y $q$...$q$) para no confundir cadenas con sentencias
    nolit = re.sub(r"\$(\w*)\$.*?\$\1\$", "''", code, flags=re.S); nolit = re.sub(r"'(?:[^']|'')*'", "''", nolit); nol = nolit.lower()
    base = os.path.basename(f)
    lib = base.startswith("04_lib")
    if not lib:
        chk(f, "guarda SI-CCI-DEV", "SI-CCI-DEV" in raw and "cci.validacion_autorizada" in raw)
        chk(f, "guarda LOCAL-TEMPORAL (socket, db ^cci_)", "SI-LOCAL-TEMPORAL" in raw and "inet_server_addr" in raw and "^cci_" in raw)
        chk(f, "guarda antes de cualquier SQL de datos", low.find("cci.validacion_autorizada") >= 0 and low.find("cci.validacion_autorizada") < (min([i for i in [low.find("insert into"), low.find("update "), low.find("pg_sleep")] if i >= 0] or [10**9])))
    chk(f, "sin COMMIT", not re.search(r"\bcommit\b", low) or "commit" in raw.lower() and not re.search(r"^\s*commit\s*;", low, re.M))
    chk(f, "sin DDL peligroso (drop/truncate/alter/grant/revoke/create role|extension)", not re.search(r"(?<![\w_])(drop\s+(table|schema|database|role|function|trigger|policy)|truncate|alter\s+(table|role|system|database)|grant\s|revoke\s|create\s+(role|extension|database|schema))", re.sub(r"pg_temp\.\w+","",nol)) or lib and not re.search(r"drop\s+(table|schema|database|role)|truncate|alter\s+(role|system|database)|grant\s|revoke\s|create\s+(role|extension|database|schema)", nol))
    chk(f, "sin DELETE/UPDATE/INSERT fuera de PROD-safe (solo en scripts con rollback)", (not re.search(r"\b(insert\s+into|update\s+\w|delete\s+from)", low)) or ("rollback" in low))
    chk(f, "sin metacomandos de conexion (\\c, \\connect, \\! , \\copy)", not re.search(r"^\s*\\(c|connect|!|copy)\b", code, re.M))
    chk(f, "sin refs de proyecto/URL/secretos/JWT", not re.search(r"(eyJ[A-Za-z0-9_-]{20,}|supabase\.co|sk-[A-Za-z0-9]{20,}|postgres(ql)?://\S+:\S+@|[a-z]{20}\.supabase)", raw))
    chk(f, "sin DDL de objetos permanentes (create table/function/trigger sin pg_temp/temp)", not re.search(r"create\s+(or\s+replace\s+)?(table|function|trigger|view|index)\s+(?!pg_temp|temp|if)", low) or base.startswith("03") and False)
    if re.search(r"\binsert\s+into|\bupdate\s+\w", low) and not lib:
        chk(f, "escrituras dentro de transaccion con rollback/ROLLBACK final", "begin" in low and "rollback" in low)
for r in res: print("%-6s %-42s %s %s" % (r[2], r[0], r[1], r[3]))
print("TOTAL=%d FAIL=%d" % (len(res), fails))
if out:
    with open(out, "w") as o:
        for r in res: o.write("%s | %s | %s | %s\n" % r[::-1][::-1] if False else "%s | %s | %s | %s\n" % (r[2], r[0], r[1], r[3]))
        o.write("TOTAL=%d FAIL=%d\n" % (len(res), fails))
sys.exit(1 if fails else 0)
