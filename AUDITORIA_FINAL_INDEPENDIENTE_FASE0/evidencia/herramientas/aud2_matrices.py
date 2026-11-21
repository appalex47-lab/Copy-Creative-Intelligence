#!/usr/bin/env python3
# Matrices de integridad / ejecución / identidad de la guarda. Uso: aud2_matrices.py <arbol cci_dev_NO_EJECUTADOS> <estilo: guc|temp> <etiqueta> <sockDEV> <puertoDEV> <sockPROD> <puertoPROD> <salida.json>
import sys,os,shutil,subprocess,json,re,tempfile,hashlib
SRC,EST,ETQ,S1,P1,S2,P2,OUT=sys.argv[1:9]
SEIS=["01_inventario_esquema_SOLO_LECTURA","02_rls_privilegios_SOLO_LECTURA","03_pruebas_rls_ROLLBACK","04_trigger_r1_r9_ROLLBACK","05_concurrencia_sesion_A","05_concurrencia_sesion_B"]
DEV="-c cci.validacion_autorizada=SI-CCI-DEV -c cci.entorno=CCI-DEV"; LOC="-c cci.validacion_autorizada=SI-LOCAL-TEMPORAL -c cci.entorno=LOCAL-TEMPORAL"
V=["-v","org=x","-v","org_a=x","-v","org_b=x","-v","uid_a=x","-v","uid_x=x","-v","piece=x","-v","attr=x"]
FORJA="select set_config('cci.guarda_ok','1',false);\n" if EST=="guc" else "create temp table pg_temp.cci_guarda_ok (ok boolean);\n"
PRESET="-c cci.guarda_ok=1"
R=[]; W=tempfile.mkdtemp(prefix="m_")
def sh(a,sock,port,opts="",cwd=None,stdin=None,user="cci_test"):
    env=dict(os.environ,PGHOST=sock,PGPORT=port,PGUSER=user,PGOPTIONS=opts)
    r=subprocess.run(a,capture_output=True,text=True,env=env,cwd=cwd,stdin=stdin); return r.returncode,r.stdout+r.stderr
def adm(sql,sock=S1,port=P1,db="postgres"): return sh(["psql","-qAt","-d",db,"-c",sql],sock,port)[1].strip()
def clasif(rc,o):
    if "GUARDA OK" in o: return "PASA"
    m=re.search(r"ERROR:\s+NO EJECUTADO \[(G-[A-Z-]+)\]",o)
    if m: return "RECHAZA:"+m.group(1)
    if re.search(r"No such file|could not open|no such file",o): return "ABORTA:archivo"
    if rc!=0: return "ABORTA:rc=%d"%rc
    return "SIN_GUARDA_EJECUTO"
def variante(name,guard=None,allow=(),deny=(),sin=False):
    d=os.path.join(W,name); shutil.rmtree(d,ignore_errors=True); shutil.copytree(SRC,d); g=os.path.join(d,"00_guarda_destino.sql")
    if sin: os.remove(g); return d
    s=open(g,encoding="utf-8").read() if guard is None else guard
    if guard is None and (allow or deny):
        s=s.replace("array[]::text[];  -- @@DEV_ALLOW@@","array[%s]::text[];  --"%",".join("'%s'"%a for a in allow)).replace("array[]::text[];  -- @@PROD_DENY@@","array[%s]::text[];  --"%",".join("'%s'"%a for a in deny))
    open(g,"w",encoding="utf-8").write(s); return d
def registra(i,obj,pre,cmd,esp,obs,estado,ev): R.append(dict(id=i,objetivo=obj,precondicion=pre,comando=cmd,esperado=esp,observado=obs,estado=estado,evidencia=ev,arbol=ETQ))
def corre(d,sc,opts,sock=S1,port=P1,db="cci_m",modo="f_abs",cwd=None,extra=()):
    f=os.path.join(d,sc+".sql"); base=["psql","-d",db,"-X","-v","ON_ERROR_STOP=1","-P","pager=off"]+V+list(extra)
    if modo=="f_abs": return sh(base+["-f",f],sock,port,opts,cwd=cwd or "/tmp")
    if modo=="f_rel": return sh(base+["-f",sc+".sql"],sock,port,opts,cwd=d)
    if modo=="f_rel_otro": 
        o=os.path.join(W,"otro"); os.makedirs(o,exist_ok=True); rel=os.path.relpath(f,o); return sh(base+["-f",rel],sock,port,opts,cwd=o)
    if modo=="stdin_mismo": return sh(base,sock,port,opts,cwd=d,stdin=open(f,encoding="utf-8"))
    if modo=="stdin_otro_sin_guarda":
        o=os.path.join(W,"vacio_cwd"); os.makedirs(o,exist_ok=True); return sh(base,sock,port,opts,cwd=o,stdin=open(f,encoding="utf-8"))
    if modo=="stdin_rogue_vacio" or modo=="stdin_rogue_forja":
        o=os.path.join(W,modo); shutil.rmtree(o,ignore_errors=True); os.makedirs(o); open(os.path.join(o,"00_guarda_destino.sql"),"w").write("-- rogue\n" if modo.endswith("vacio") else FORJA)
        return sh(base,sock,port,opts,cwd=o,stdin=open(f,encoding="utf-8"))
adm("drop database if exists cci_m"); adm("create database cci_m"); adm("drop database if exists cci_m",S2,P2,); adm("create database cci_m",S2,P2)
sysid1=adm("select system_identifier from pg_control_system()"); sysid2=adm("select system_identifier from pg_control_system()",S2,P2)
g0=open(os.path.join(SRC,"00_guarda_destino.sql"),encoding="utf-8").read()
# ---- INTEGRIDAD DE LA GUARDA (6 scripts x condición) ----
casos=[("INT-01","guarda ausente",dict(sin=True),LOC,"RECHAZA|ABORTA","rechazo"),
 ("INT-02","guarda vacía (0 bytes)",dict(guard=""),LOC,"RECHAZA:G-GUARDA-NO-EJECUTADA","rechazo"),
 ("INT-03","guarda sólo comentario",dict(guard="-- vacio\n"),LOC,"RECHAZA:G-GUARDA-NO-EJECUTADA","rechazo"),
 ("INT-04","guarda truncada antes del bloque DO",dict(guard=g0.split("do $guarda$")[0]),LOC,"RECHAZA:G-GUARDA-NO-EJECUTADA","rechazo"),
 ("INT-05","guarda truncada a mitad del bloque DO (sintaxis rota)",dict(guard=g0[:len(g0)//2+len(g0.split("do $guarda$")[0])//2]),LOC,"ABORTA","rechazo"),
 ("INT-06","guarda con SÓLO el marcador final (guarda sustituida que forja el marcador)",dict(guard=FORJA),LOC,"(?!RECHAZA|ABORTA:archivo)","limite"),
 ("INT-07","guarda con SÓLO la primera línea del bloque (marcador inicial)",dict(guard=("select set_config('cci.guarda_ok','',false);\n" if EST=="guc" else "select 1;\n")),LOC,"RECHAZA:G-GUARDA-NO-EJECUTADA","rechazo"),
 ("INT-08","guarda sustituida por otro SQL inocuo (select 1;)",dict(guard="select 1;\n"),LOC,"RECHAZA:G-GUARDA-NO-EJECUTADA","rechazo"),
 ("INT-09","guarda con orden alterado: marcador creado ANTES de las comprobaciones y destino desconocido",dict(guard=None),DEV,"RECHAZA","rechazo")]
for i,desc,kw,opts,esp,tipo in casos:
    for sc in SEIS:
        kw2=dict(kw)
        if i=="INT-09":
            g=g0; m=("perform pg_catalog.set_config('cci.guarda_ok','1',false);\n" if EST=="guc" else "create temp table pg_temp.cci_guarda_ok (ok boolean);\n")
            g=g.replace("begin\n","begin\n  "+m,1); kw2=dict(guard=g)
        d=variante(f"{i}_{sc[:2]}{sc[-1]}",**kw2); rc,o=corre(d,sc,opts); c=clasif(rc,o)
        ok=bool(re.match(esp,c)); estado="PASS" if ok and tipo=="rechazo" else ("PARTIAL" if ok and tipo=="limite" else "FAIL")
        # un rechazo no debe haber emitido datos
        registra(f"{i}-{sc[:2]}{sc[-1]}",desc+" — "+sc,"árbol "+ETQ+"; variables LOCAL/DEV según caso; cci_m vacía","psql -f <script> con guarda variante ("+opts.split()[3]+")",esp+(" (límite estructural: sin hash externo no se detecta)" if tipo=="limite" else ""),c,estado,"aud2_matrices:"+i)
# ---- allowlist/denylist alteradas (tamper): sólo el hash externo lo detecta ----
for sc in SEIS:
    d=variante(f"TAM1_{sc[:2]}{sc[-1]}",allow=[sysid1+"|cci_m"]); rc,o=corre(d,sc,DEV); c=clasif(rc,o); registra(f"INT-10-{sc[:2]}{sc[-1]}","allowlist modificada (añade el destino): "+sc,"allowlist vacía versionada","psql -f con guarda editada","PASA (tamper no detectable sin hash externo)",c,"PARTIAL" if c=="PASA" else "FAIL","aud2_matrices:INT-10")
    d=variante(f"TAM2_{sc[:2]}{sc[-1]}",allow=[sysid1+"|cci_m"],deny=[sysid1]); rc,o=corre(d,sc,DEV); c=clasif(rc,o); registra(f"INT-11-{sc[:2]}{sc[-1]}","denylist con el destino + allowlist: PROD gana: "+sc,"","psql -f","RECHAZA:G-PROD-RECHAZADO",c,"PASS" if c=="RECHAZA:G-PROD-RECHAZADO" else "FAIL","aud2_matrices:INT-11")
    d=variante(f"TAM3_{sc[:2]}{sc[-1]}",allow=[sysid1+"|cci_m"],deny=[]); rc,o=corre(d,sc,DEV); c=clasif(rc,o); registra(f"INT-12-{sc[:2]}{sc[-1]}","denylist VACIADA (tamper) sobre un destino que era PROD: "+sc,"","psql -f","PASA (tamper no detectable sin hash externo)",c,"PARTIAL" if c=="PASA" else "FAIL","aud2_matrices:INT-12")
# ---- CONTEXTOS DE EJECUCIÓN ----
ctx=[("X-01","-f ruta absoluta desde otro cwd","f_abs","PASA|RECHAZA"),("X-02","-f ruta relativa desde el directorio del script","f_rel","PASA|RECHAZA"),("X-03","-f ruta relativa desde otro directorio","f_rel_otro","PASA|RECHAZA"),("X-04","stdin desde el directorio de los scripts (guarda real junto)","stdin_mismo","PASA|RECHAZA"),("X-05","stdin desde un directorio SIN guarda","stdin_otro_sin_guarda","ABORTA"),("X-06","stdin con guarda homónima VACÍA en el cwd","stdin_rogue_vacio","RECHAZA:G-GUARDA-NO-EJECUTADA|ABORTA"),("X-07","stdin con guarda homónima FORJADORA en el cwd (stdin no soportado)","stdin_rogue_forja","(?!RECHAZA)")]
for i,desc,modo,esp in ctx:
    for sc in SEIS:
        rc,o=corre(SRC,sc,LOC,modo=modo); c=clasif(rc,o); ok=bool(re.match(esp,c)); lim=(i=="X-07")
        registra(f"{i}-{sc[:2]}{sc[-1]}",desc+" — "+sc,"modo LOCAL en cci_m","psql ("+modo+")",esp+(" (límite: no usar stdin)" if lim else ""),c,("PARTIAL" if lim and ok and c!="ABORTA:archivo" else "PASS" if ok else "FAIL"),"aud2_matrices:"+i)
for sc in SEIS:
    rc,o=corre(SRC,sc,LOC,extra=["--single-transaction"]); c=clasif(rc,o); registra(f"X-08-{sc[:2]}{sc[-1]}","--single-transaction: "+sc,"modo LOCAL","psql --single-transaction","PASA|RECHAZA|ABORTA",c,"PASS" if c!="SIN_GUARDA_EJECUTO" else "FAIL","aud2_matrices:X-08")
    rc,o=corre(SRC,sc,DEV,extra=["-v","ON_ERROR_STOP=0"]); c=clasif(rc,o); registra(f"X-09-{sc[:2]}{sc[-1]}","-v ON_ERROR_STOP=0 con DEV y listas vacías: "+sc,"","psql -v ON_ERROR_STOP=0","RECHAZA:G-DESTINO-DESCONOCIDO",c,"PASS" if c=="RECHAZA:G-DESTINO-DESCONOCIDO" else "FAIL","aud2_matrices:X-09")
    d=variante(f"PRE_{sc[:2]}{sc[-1]}",guard=""); rc,o=corre(d,sc,LOC+" "+PRESET); c=clasif(rc,o); registra(f"X-10-{sc[:2]}{sc[-1]}","guarda vacía + marcador PREINSTALADO por PGOPTIONS cci.guarda_ok=1: "+sc,"","PGOPTIONS='... -c cci.guarda_ok=1'","RECHAZA:G-GUARDA-NO-EJECUTADA",c,"PASS" if c=="RECHAZA:G-GUARDA-NO-EJECUTADA" else "FAIL","aud2_matrices:X-10")
# ---- search_path ----
adm("create schema if not exists evil",S1,P1,"cci_m"); adm("create function evil.pg_control_system(out system_identifier bigint) returns bigint language sql as 'select 1::bigint'",S1,P1,"cci_m")
adm("alter database cci_m set search_path=evil,public"); 
d=variante("SP1",allow=["1|cci_m"]); 
for sc in SEIS:
    rc,o=corre(d,sc,DEV); c=clasif(rc,o); registra(f"SP-01-{sc[:2]}{sc[-1]}","ALTER DATABASE SET search_path=evil + pg_control_system falsa (allow '1|cci_m'): "+sc,"función falsa en evil","psql -f","RECHAZA (identidad real no está en allowlist)",c,"PASS" if c.startswith("RECHAZA") else "FAIL","aud2_matrices:SP-01")
adm("alter database cci_m reset search_path"); adm("alter role cci_test set search_path=evil,public")
for sc in SEIS:
    rc,o=corre(d,sc,DEV); c=clasif(rc,o); registra(f"SP-02-{sc[:2]}{sc[-1]}","ALTER ROLE SET search_path=evil: "+sc,"","psql -f","RECHAZA",c,"PASS" if c.startswith("RECHAZA") else "FAIL","aud2_matrices:SP-02")
adm("alter role cci_test reset search_path")
for sc in SEIS:
    rc,o=corre(d,sc,DEV+" -c search_path=pg_temp,evil"); c=clasif(rc,o); registra(f"SP-03-{sc[:2]}{sc[-1]}","pg_temp y evil primeros en el search_path (PGOPTIONS): "+sc,"","psql -f","RECHAZA",c,"PASS" if c.startswith("RECHAZA") else "FAIL","aud2_matrices:SP-03")
# persistencia: valor visto por la primera instrucción posterior a la guarda
for sc in SEIS:
    d2=variante("SP4_"+sc[:2]+sc[-1]); f=os.path.join(d2,sc+".sql"); t=open(f,encoding="utf-8").read(); k=("cci.guarda_ok" if EST=="guc" else "pg_temp.cci_guarda_ok"); i=t.index(k); j=t.index("\n",i)+1
    open(f,"w",encoding="utf-8").write(t[:j]+"select 'SPVAL=' || pg_catalog.current_setting('search_path') as sp;\n"+t[j:]); rc,o=corre(d2,sc,LOC+" -c search_path=evil,public,pg_temp"); m=re.search(r"SPVAL=(\S+)",o)
    registra(f"SP-04-{sc[:2]}{sc[-1]}","¿persiste el search_path de la guarda tras su bloque DO? (llamador: evil,public,pg_temp): "+sc,"","primera instrucción posterior a la guarda: current_setting('search_path')","El del LLAMADOR (la guarda NO persiste su search_path; por diseño)",m.group(1) if m else "sin SPVAL","PASS" if m and m.group(1)=="evil,public,pg_temp" else "FAIL","aud2_matrices:SP-04")
adm("drop schema evil cascade",S1,P1,"cci_m")
# ---- IDENTIDAD (dos clústeres reales) ----
for sc in SEIS:
    d=variante("ID1_"+sc[:2]+sc[-1],allow=[sysid1+"|cci_m"],deny=[sysid2]); 
    rc,o=corre(d,sc,DEV,sock=S1,port=P1); c=clasif(rc,o); registra(f"ID-01-{sc[:2]}{sc[-1]}","DEV real (clúster 1 en allowlist) con variables DEV: "+sc,"2 clústeres: C1=DEV en allowlist; C2=PROD en denylist","psql -f contra C1","PASA",c,"PASS" if c=="PASA" else "FAIL","aud2_matrices:ID-01")
    rc,o=corre(d,sc,DEV,sock=S2,port=P2); c=clasif(rc,o); registra(f"ID-02-{sc[:2]}{sc[-1]}","identidad DEV DECLARADA contra el servidor PROD (clúster 2 en denylist): "+sc,"mismas listas; variables DEV","psql -f contra C2 (mismo archivo de guarda)","RECHAZA:G-PROD-RECHAZADO",c,"PASS" if c=="RECHAZA:G-PROD-RECHAZADO" else "FAIL","aud2_matrices:ID-02")
    d=variante("ID3_"+sc[:2]+sc[-1],allow=[sysid1+"|cci_m"],deny=[]); rc,o=corre(d,sc,DEV,sock=S2,port=P2); c=clasif(rc,o); registra(f"ID-03-{sc[:2]}{sc[-1]}","servidor NO registrado (ni allow ni deny) con variables DEV: "+sc,"C2 no está en ninguna lista","psql -f contra C2","RECHAZA:G-DESTINO-DESCONOCIDO",c,"PASS" if c=="RECHAZA:G-DESTINO-DESCONOCIDO" else "FAIL","aud2_matrices:ID-03")
for k,(desc,al) in enumerate([("entrada vacía ''",[""]),("entrada '|'",["|"]),("sólo sysid sin base",[sysid1]),("mayúsculas en la base",[sysid1+"|CCI_M"]),("espacio sobrante",[sysid1+"|cci_m "]),("otra base",[sysid1+"|postgres"]),("sysid con ceros a la izquierda",["0"+sysid1+"|cci_m"])]):
    for sc in SEIS:
        d=variante(f"ID4_{k}_{sc[:2]}{sc[-1]}",allow=al); rc,o=corre(d,sc,DEV); c=clasif(rc,o); registra(f"ID-04{k}-{sc[:2]}{sc[-1]}",f"allowlist con {desc}: "+sc,"","psql -f","RECHAZA:G-DESTINO-DESCONOCIDO",c,"PASS" if c=="RECHAZA:G-DESTINO-DESCONOCIDO" else "FAIL","aud2_matrices:ID-04")
# rol sin EXECUTE
adm("revoke execute on function pg_catalog.pg_control_system() from public",S1,P1,"cci_m"); adm("drop role if exists cci_noexec"); adm("create role cci_noexec login"); adm("grant connect on database cci_m to cci_noexec")
for sc in SEIS:
    d=variante("ID5_"+sc[:2]+sc[-1],allow=[sysid1+"|cci_m"]); f=os.path.join(d,sc+".sql"); rc,o=sh(["psql","-d","cci_m","-X","-v","ON_ERROR_STOP=1"]+V+["-f",f],S1,P1,DEV,user="cci_noexec"); c=clasif(rc,o); registra(f"ID-05-{sc[:2]}{sc[-1]}","rol sin EXECUTE en pg_control_system(): "+sc,"revoke execute from public (cci_m)","psql -f como cci_noexec","RECHAZA:G-IDENTIDAD-NO-VERIFICABLE",c,"PASS" if c=="RECHAZA:G-IDENTIDAD-NO-VERIFICABLE" else "FAIL","aud2_matrices:ID-05")
adm("grant execute on function pg_catalog.pg_control_system() to public",S1,P1,"cci_m")
# clon: DEV = copia física de PROD -> mismo sysid y misma base (AG-18). Se simula con el mismo clúster registrado a la vez como allow (DEV) y destino real.
for sc in SEIS:
    d=variante("ID6_"+sc[:2]+sc[-1],allow=[sysid1+"|cci_m"]); rc,o=corre(d,sc,DEV); c=clasif(rc,o)
    registra(f"ID-06-{sc[:2]}{sc[-1]}","AG-18 clon/restauración física: servidor con el MISMO system_identifier y base que el DEV registrado: "+sc,"un clon físico hereda system_identifier y nombre de base","psql -f contra un servidor indistinguible del DEV registrado","NO distinguible: la guarda PASA (limitación estructural; sólo mitiga la denylist si PROD se registró, lo que a su vez bloquearía el clon)",c,"PARTIAL" if c=="PASA" else "FAIL","aud2_matrices:ID-06 (limitación estructural, no aprobación)")
json.dump(R,open(OUT,"w"),ensure_ascii=False,indent=1)
import collections; print(ETQ,collections.Counter(r["estado"] for r in R),len(R))
