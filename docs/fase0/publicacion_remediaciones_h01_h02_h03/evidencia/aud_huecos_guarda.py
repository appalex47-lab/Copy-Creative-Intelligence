import subprocess,shutil,os,sys,re,glob
S="/tmp/aud/pgO/sock";P="55432"
SRC="/tmp/aud/gc/docs/fase0/cierre_tecnico_fase0/scripts_validacion/cci_dev_NO_EJECUTADOS"
W="/tmp/aud/gaps2/w"
SC=["01_inventario_esquema_SOLO_LECTURA.sql","02_rls_privilegios_SOLO_LECTURA.sql","03_pruebas_rls_ROLLBACK.sql","04_trigger_r1_r9_ROLLBACK.sql","05_concurrencia_sesion_A.sql","05_concurrencia_sesion_B.sql"]
DEV="-c cci.validacion_autorizada=SI-CCI-DEV -c cci.entorno=CCI-DEV"
def sh(c,**k): return subprocess.run(c,shell=True,capture_output=True,text=True,**k)
def adm(sql,db="postgres"): return sh(f"psql -h {S} -p {P} -U cci_test -d {db} -qAtc \"{sql}\"")
adm("drop database if exists cci_gap"); adm("create database cci_gap")
sysid=adm("select system_identifier from pg_control_system()").stdout.strip()
def var(name,guard=None,inject=None):
    d=f"{W}/{name}"; shutil.rmtree(d,ignore_errors=True); shutil.copytree(SRC,d)
    g=open(f"{d}/00_guarda_destino.sql").read()
    if inject: g=g.replace("array[]::text[];  -- @@DEV_ALLOW@@",f"array['{inject}']::text[];  --")
    if guard is not None: g=guard
    open(f"{d}/00_guarda_destino.sql","w").write(g); return d
def run(d,s,opts=DEV,extra="",db="cci_gap",stdin=False):
    env=f"PGOPTIONS='{opts}'"
    cmd=f"cd {d} && {env} psql -h {S} -p {P} -U cci_test -d {db} -X {extra} " + (f"< {s}" if stdin else f"-f {s}")
    r=sh(cmd); o=r.stdout+r.stderr
    return ("RECHAZADO" if "NO EJECUTADO [G-" in o else ("GUARDA_OK" if "GUARDA OK" in o else "SIN_GUARDA_EJECUTO")), o
res=[]
def caso(id,desc,fn,esperado):
    out=[]
    for s in SC:
        try: v=fn(s)
        except Exception as e: v="ERR"
        out.append(v)
    ok=all(v==esperado for v in out)
    res.append((id,desc,esperado,out,ok))
    print(id,"OK" if ok else "HUECO",desc,out,flush=True)
d0=var("base")
# H1 base: listas vacías, DEV declarado -> RECHAZADO
caso("AG-01","DEV declarado, listas vacías (config de entrega)",lambda s:run(d0,s)[0],"RECHAZADO")
# H2 guarda vacía
d=var("vacia",guard=""); caso("AG-02","guarda vacía (0 bytes): ¿los scripts corren sin guarda?",lambda s:run(d,s)[0],"RECHAZADO")
d=var("solocom",guard="-- vacio\n"); caso("AG-03","guarda sólo comentario",lambda s:run(d,s)[0],"RECHAZADO")
d=var("trunc",guard=open(f"{SRC}/00_guarda_destino.sql").read().split("do $guarda$")[0]); caso("AG-04","guarda truncada antes del bloque DO",lambda s:run(d,s)[0],"RECHAZADO")
# H3 guarda con DO sintácticamente roto -> debe abortar
g=open(f"{SRC}/00_guarda_destino.sql").read().replace("begin\n","begin\n  perform 1/0;\n",1) if False else open(f"{SRC}/00_guarda_destino.sql").read()+"\nselect 1/0;\n"
# H4 manipulación: allowlist con sysid propio (config legítima) -> GUARDA_OK esperado (control positivo)
d=var("legit",inject=f"{sysid}|cci_gap"); caso("AG-05","control positivo: allowlist correcta -> pasa",lambda s:run(d,s)[0],"GUARDA_OK")
# H5 allowlist + denylist del mismo sysid -> RECHAZADO
d=var("deny",inject=f"{sysid}|cci_gap")
g=open(f"{d}/00_guarda_destino.sql").read().replace("array[]::text[];  -- @@PROD_DENY@@",f"array['{sysid}']::text[];  --")
open(f"{d}/00_guarda_destino.sql","w").write(g)
caso("AG-06","servidor en allow Y deny -> PROD gana",lambda s:run(d,s)[0],"RECHAZADO")
# H6 variantes de mayúsculas/espacios en allowlist
for n,e in [("mayus",f"{sysid}|CCI_GAP"),("espacio",f"{sysid} |cci_gap"),("sinbase",f"{sysid}"),("otrabase",f"{sysid}|postgres")]:
    d=var("al_"+n,inject=e); caso("AG-07"+n[0],f"allowlist variante '{n}' no coincide exacto",lambda s,d=d:run(d,s)[0],"RECHAZADO")
# H7 ALTER DATABASE / ROLE SET search_path malicioso
adm("create schema if not exists evil",db="cci_gap")
adm("create or replace function evil.pg_control_system() returns table(system_identifier bigint) language sql as 'select 1::bigint'",db="cci_gap")
adm("alter database cci_gap set search_path=evil,public")
d=var("sp_db",inject=f"1|cci_gap"); caso("AG-08","ALTER DATABASE SET search_path=evil con función falsa pg_control_system (allow '1|cci_gap')",lambda s:run(d,s)[0],"RECHAZADO")
adm("alter database cci_gap reset search_path")
adm("alter role cci_test set search_path=evil,public")
caso("AG-09","ALTER ROLE SET search_path=evil",lambda s:run(d,s)[0],"RECHAZADO")
adm("alter role cci_test reset search_path")
# H8 pg_temp
caso("AG-10","PGOPTIONS search_path=pg_temp,public",lambda s:run(d,s,opts=DEV+" -c search_path=pg_temp,evil")[0],"RECHAZADO")
# H9 stdin con guarda ausente del cwd / rogue
rog="/tmp/aud/gaps2/rogue"; shutil.rmtree(rog,ignore_errors=True); os.makedirs(rog)
open(f"{rog}/00_guarda_destino.sql","w").write("-- rogue vacío\n")
def stdin_rogue(s):
    cmd=f"cd {rog} && PGOPTIONS='{DEV}' psql -h {S} -p {P} -U cci_test -d cci_gap -X < {SRC}/{s}"
    o=sh(cmd); t=o.stdout+o.stderr
    return "RECHAZADO" if "NO EJECUTADO [G-" in t else ("GUARDA_OK" if "GUARDA OK" in t else ("ABORTA_SIN_GUARDA" if "No such file" in t or "no such file" in t else "SIN_GUARDA_EJECUTO"))
caso("AG-11","stdin (psql < script) con cwd rogue con guarda vacía",stdin_rogue,"RECHAZADO")
def stdin_nofile(s):
    e="/tmp/aud/gaps2/emptycwd"; os.makedirs(e,exist_ok=True)
    o=sh(f"cd {e} && PGOPTIONS='{DEV}' psql -h {S} -p {P} -U cci_test -d cci_gap -X < {SRC}/{s}"); t=o.stdout+o.stderr
    return "RECHAZADO" if "NO EJECUTADO [G-" in t else ("ABORTA_SIN_GUARDA" if "ould not open" in t or "No such file" in t or "does not exist" in t else "SIN_GUARDA_EJECUTO")
caso("AG-12","stdin con cwd sin guarda (archivo ausente)",stdin_nofile,"ABORTA_SIN_GUARDA")
# H10 ON_ERROR_STOP=0 y single-transaction
caso("AG-13","-v ON_ERROR_STOP=0 en CLI",lambda s:run(d0,s,extra="-v ON_ERROR_STOP=0")[0],"RECHAZADO")
caso("AG-14","--single-transaction",lambda s:run(d0,s,extra="--single-transaction")[0],"RECHAZADO")
caso("AG-15","ON_ERROR_ROLLBACK=on/interactive",lambda s:run(d0,s,extra="-v ON_ERROR_ROLLBACK=on")[0],"RECHAZADO")
# H11 variables declaradas con casing/espacios
for n,o in [("minus",'-c cci.validacion_autorizada=si-cci-dev -c cci.entorno=cci-dev'),("espacio",'-c cci.validacion_autorizada=SI-CCI-DEV\\  -c cci.entorno=CCI-DEV'),("cruzado","-c cci.validacion_autorizada=SI-CCI-DEV -c cci.entorno=LOCAL-TEMPORAL"),("vacio","")]:
    caso("AG-16"+n[0],f"variables {n}",lambda s,o=o:run(d0,s,opts=o)[0],"RECHAZADO")
# H12 DEV declarado contra servidor PROD simulado: nombre de base 'cci_dev' en servidor denylist
adm("create database cci_dev")
d=var("prodsim"); g=open(f"{d}/00_guarda_destino.sql").read().replace("array[]::text[];  -- @@PROD_DENY@@",f"array['{sysid}']::text[];  --"); open(f"{d}/00_guarda_destino.sql","w").write(g)
caso("AG-17","DEV declarado + base 'cci_dev' en servidor con sysid en denylist",lambda s:run(d,s,db="cci_dev")[0],"RECHAZADO")
# H13 clon: sysid en allow y base igual -> pasa (límite conocido)
d=var("clon",inject=f"{sysid}|cci_dev"); caso("AG-18","LÍMITE: clon con mismo sysid y base, sin denylist -> pasa (no distinguible)",lambda s:run(d,s,db="cci_dev")[0],"GUARDA_OK")
# H14 rol sin EXECUTE
adm("revoke execute on function pg_catalog.pg_control_system() from public",db="cci_gap")
adm("create role cci_noexec login"); 
d=var("noexec",inject=f"{sysid}|cci_gap")
def noexec(s):
    cmd=f"cd {d} && PGOPTIONS='{DEV}' psql -h {S} -p {P} -U cci_noexec -d cci_gap -X -f {s}"; o=sh(cmd); t=o.stdout+o.stderr
    return "RECHAZADO" if "G-IDENTIDAD-NO-VERIFICABLE" in t else "OTRO"
caso("AG-19","rol sin EXECUTE en pg_control_system -> identidad no verificable",noexec,"RECHAZADO")
adm("grant execute on function pg_catalog.pg_control_system() to public",db="cci_gap")
import json; json.dump(res,open("/tmp/aud/gaps2/resultados.json","w"))
print("TOTAL",len(res),"huecos",sum(1 for r in res if not r[4]))
