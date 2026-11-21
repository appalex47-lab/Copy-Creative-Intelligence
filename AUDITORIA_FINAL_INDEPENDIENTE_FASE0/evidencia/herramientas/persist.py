import subprocess,os,sys,json
sock,port,tree,out=sys.argv[1:5]
SEIS=["01_inventario_esquema_SOLO_LECTURA","02_rls_privilegios_SOLO_LECTURA","03_pruebas_rls_ROLLBACK","04_trigger_r1_r9_ROLLBACK","05_concurrencia_sesion_A","05_concurrencia_sesion_B"]
V=["-v","org=x","-v","org_a=x","-v","org_b=x","-v","uid_a=x","-v","uid_x=x","-v","piece=x","-v","attr=x"]
def sh(a,env=None): return subprocess.run(a,capture_output=True,text=True,env=dict(os.environ,PGHOST=sock,PGPORT=port,PGUSER="cci_test",**(env or {})))
def q(sql,db="cci_pers"): return sh(["psql","-qAt","-d",db,"-c",sql]).stdout.strip()
q("drop database if exists cci_pers","postgres"); q("create database cci_pers","postgres"); q("create table public.t(a int); insert into public.t values (1),(2)")
FP="select md5(string_agg(x,'|' order by x)) from (select 'cls:'||count(*) x from pg_class union all select 'proc:'||count(*) from pg_proc union all select 'ns:'||count(*) from pg_namespace union all select 'roles:'||count(*) from pg_roles union all select 't:'||md5(string_agg(a::text,',')) from public.t union all select 'xmin:'||max(age(xmin)) from public.t union all select 'ins:'||coalesce(sum(n_tup_ins+n_tup_upd+n_tup_del),0) from pg_stat_user_tables where schemaname='public' and relname='t') s"
R=[]
for sc in SEIS:
    a=q(FP); r=sh(["psql","-d","cci_pers","-X","-v","ON_ERROR_STOP=1"]+V+["-f",f"{tree}/{sc}.sql"],{"PGOPTIONS":"-c cci.validacion_autorizada=SI-CCI-DEV -c cci.entorno=CCI-DEV"}); b=q(FP)
    R.append(dict(script=sc,rc=r.returncode,rechazo="G-DESTINO-DESCONOCIDO" in (r.stdout+r.stderr),huella_antes=a,huella_despues=b,sin_cambios=a==b))
json.dump(R,open(out,"w"),indent=1,ensure_ascii=False)
for x in R: print(x["script"],x["rc"],x["rechazo"],x["sin_cambios"])
