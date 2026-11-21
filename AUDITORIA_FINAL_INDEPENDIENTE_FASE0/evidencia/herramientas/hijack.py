import subprocess,sys,os
tree,sock,port,out=sys.argv[1:5]
SC=["01_inventario_esquema_SOLO_LECTURA","02_rls_privilegios_SOLO_LECTURA","03_pruebas_rls_ROLLBACK","04_trigger_r1_r9_ROLLBACK","05_concurrencia_sesion_A","05_concurrencia_sesion_B"]
def sh(a,env=None,**k): return subprocess.run(a,capture_output=True,text=True,env=dict(os.environ,PGHOST=sock,PGPORT=port,PGUSER="cci_test",**(env or {})),**k)
def adm(sql,db="postgres"): return sh(["psql","-qAt","-d",db,"-c",sql])
adm("drop database if exists cci_hj"); adm("create database cci_hj")
for f in ["current_setting(text)","current_setting(text, boolean)","to_regclass(text)","pg_get_userbyid(oid)"]:
    ret={"current_setting":"text","to_regclass":"regclass","pg_get_userbyid":"name"}[f.split("(")[0]]
    adm("create schema if not exists evil","cci_hj"); adm(f"create function evil.{f.split('(')[0]}({f.split('(')[1][:-1].replace(',',' a,')} a) returns {ret} language plpgsql as $x$ begin raise exception 'HIJACK-INVOCADO'; end $x$" if False else f"create function evil.{f} returns {ret} language plpgsql as $x$ begin raise exception 'HIJACK-INVOCADO'; end $x$","cci_hj")
L=[]
V=["-v","org=x","-v","org_a=x","-v","org_b=x","-v","uid_a=x","-v","uid_x=x","-v","piece=x","-v","attr=x"]
for s in SC:
    r=sh(["psql","-d","cci_hj","-X","-v","ON_ERROR_STOP=1"]+V+["-f",f"{tree}/{s}.sql"],env={"PGOPTIONS":"-c cci.validacion_autorizada=SI-LOCAL-TEMPORAL -c cci.entorno=LOCAL-TEMPORAL -c search_path=evil,pg_catalog"})
    o=r.stdout+r.stderr; L.append((s,"GUARDA OK" in o,"HIJACK-INVOCADO" in o,r.returncode))
with open(out,"w") as f:
    for s,g,h,rc in L: f.write(f"{s} | guarda_ok={g} | funcion_homonima_invocada={h} | rc={rc}\n")
print(open(out).read())
