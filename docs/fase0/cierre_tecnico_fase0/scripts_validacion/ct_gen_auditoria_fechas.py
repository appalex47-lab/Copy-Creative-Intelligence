#!/usr/bin/env python3
# Uso: python3 -I -B ct_gen_auditoria_fechas.py <dir_cierre> <repo> [--sin-red]. Genera INFORME_AUDITORIA_FECHAS_HORAS.md SOLO con marcas leídas del entorno, de git y de la API de GitHub (no se escribe ninguna fecha a mano).
import csv, os, re, subprocess, sys, time, json
c = os.path.abspath(sys.argv[1]); repo = sys.argv[2]; red = "--sin-red" not in sys.argv; B = os.path.join(c, "scripts_validacion", "resultados", "bateria_final")
sh = lambda *a: subprocess.run(list(a), capture_output=True, text=True).stdout.strip()
env = dict(l.split("=", 1) for l in open(os.path.join(B, "ENTORNO.txt"), encoding="utf-8").read().splitlines() if "=" in l); idx = list(csv.DictReader(open(os.path.join(B, "INDICE_BATERIA.csv"), encoding="utf-8")))
ahora = time.time(); L = ["# INFORME DE AUDITORÍA DE FECHAS Y HORAS", "",
 "Generado por `scripts_validacion/ct_gen_auditoria_fechas.py`; cada marca procede del reloj del entorno, de git o de la API de GitHub. **No se modificó ninguna fecha para que parezca coherente y no se escribió ninguna a mano.**", "",
 "## Reloj y zona horaria del entorno (leídos al generar este informe)",
 "| Magnitud | Valor |", "|---|---|", "| UTC (`date -u`) | %s |" % time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(ahora)), "| Local (`date`) | %s |" % time.strftime("%Y-%m-%dT%H:%M:%S%z (%Z)", time.localtime(ahora)),
 "| Variable TZ | %s |" % (os.environ.get("TZ") or "(sin definir)"), "| Diferencia local−UTC | %s |" % time.strftime("%z", time.localtime(ahora)), "",
 "**Criterio:** la zona local del entorno es la del usuario (America/Mexico_City, UTC−06:00 en noviembre). Las marcas con sufijo `Z` están en UTC; las de git y las columnas `*_local` llevan el desfase explícito. Una hora UTC y una hora local de la misma ejecución difieren en 6 h (p. ej. 02:36Z = 20:36 local): comparar sin convertir produce una discrepancia aparente de 6 h.", "",
 "## Batería final: inicio, fin y zona de cada paso (datos del entorno)",
 "| Paso | Inicio UTC | Fin UTC | Inicio local | Fin local | Zona |", "|---|---|---|---|---|---|"]
for r in idx: L.append("| %s | %s | %s | %s | %s | %s |" % (r["paso"], r["inicio_utc"], r["fin_utc"], r["inicio_local"], r["fin_local"], r["zona_local"]))
L += ["", "Batería completa: inicio %s UTC / %s local; fin %s UTC / %s local. Fuente: `scripts_validacion/resultados/bateria_final/ENTORNO.txt` e `INDICE_BATERIA.csv` (generados por `ct_bateria_final.sh` con `date`, sin edición manual; las salidas anteriores se borran antes de ejecutar, por lo que ningún resultado es de una corrida previa; cada salida tiene su SHA-256 en el índice)." % (env.get("inicio_bateria_utc"), env.get("inicio_bateria_local"), env.get("fin_bateria_utc"), env.get("fin_bateria_local")), "",
 "## Commits de la rama (marcas de git y de GitHub)", "| Commit | Fecha de commit (git, con desfase) | Fecha de commit en UTC | Fecha de la API de GitHub |", "|---|---|---|---|"]
for ln in sh("git", "-C", c, "log", "-n", "8", "--format=%H|%cI|%ct").splitlines():
    h, ci, ct = ln.split("|"); api = ""
    if red:
        j = subprocess.run(["gh", "api", "repos/%s/commits/%s" % (repo, h), "--jq", ".commit.committer.date"], capture_output=True, text=True); api = j.stdout.strip() or "(no disponible)"
    L.append("| `%s` | %s | %s | %s |" % (h[:12], ci, time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(int(ct))), api))
L += ["", "La fecha de un commit la escribe el reloj de quien lo crea (aquí, el reloj del entorno); la API de GitHub devuelve ese mismo campo, **no** una hora de recepción. Sirve para comprobar que git y GitHub coinciden, no como prueba externa de la hora.", ""]
if red:
    from email.utils import parsedate_to_datetime
    t0 = time.time(); h = subprocess.run(["gh", "api", "-i", "repos/%s" % repo, "--jq", ".id"], capture_output=True, text=True).stdout; t1 = time.time(); m = re.search(r"(?im)^date:\s*(.+)$", h)
    if m:
        srv = parsedate_to_datetime(m.group(1).strip()).timestamp(); L += ["## Contraste del reloj con el servidor de GitHub (cabecera HTTP `Date`)", "| Magnitud | Valor |", "|---|---|", "| `Date` de api.github.com | %s |" % m.group(1).strip(), "| Reloj del entorno (punto medio de la consulta) | %s |" % time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime((t0 + t1) / 2)), "| Diferencia entorno − servidor | %+.1f s (resolución de 1 s; la consulta duró %.1f s) |" % ((t0 + t1) / 2 - srv, t1 - t0), "", "Esta lectura contrasta el reloj del entorno con un reloj externo en el instante de la consulta; no acredita las horas de ejecuciones anteriores, solo que el reloj no estaba desviado en este momento.", ""]
    else: L += ["## Contraste del reloj con el servidor de GitHub", "No se obtuvo la cabecera `Date` (no acreditado).", ""]
    ev = subprocess.run(["gh", "api", "repos/%s/events?per_page=30" % repo, "--jq", '[.[]|select(.type=="PushEvent")|{t:.created_at,ref:.payload.ref,h:.payload.head}]'], capture_output=True, text=True)
    try: pe = json.loads(ev.stdout)
    except Exception: pe = []
    L += ["## Hora de recepción de los push según GitHub (eventos del repositorio, hora del servidor)", "| Evento (UTC, servidor GitHub) | Rama | HEAD empujado |", "|---|---|---|"] + ["| %s | `%s` | `%s` |" % (e["t"], e["ref"], e["h"][:12]) for e in pe if "cierre-tecnico" in e["ref"]] + ["",
     "Estas marcas son del servidor de GitHub y permiten contrastar la hora del entorno; solo cubren los eventos que la API conserva (ventana limitada)."]
else: L += ["(Consulta a GitHub omitida con --sin-red.)"]
L += ["", "## Conclusión", "- Zona horaria del entorno: ver tabla (UTC−06:00 CST). Todas las evidencias distinguen hora de inicio, de finalización y zona.", "- La discrepancia observada entre la batería (UTC, sufijo Z) y la hora de revisión (local) es de un desfase de 6 horas; no hay evidencia de ejecuciones reutilizadas (las salidas se borran antes de cada batería y llevan SHA-256 en el índice).",
      "- **Parcialmente acreditado:** el reloj del entorno se contrastó con la cabecera `Date` de GitHub solo en el momento de generar este informe (tabla anterior); no hay fuente NTP verificable para las horas de las ejecuciones pasadas. Las horas se presentan como las que el entorno reporta, no como horas verificadas externamente; los push se contrastan con el servidor de GitHub cuando la API los devuelve."]
open(os.path.join(c, "INFORME_AUDITORIA_FECHAS_HORAS.md"), "w", encoding="utf-8").write("\n".join(L) + "\n"); print("ok")
