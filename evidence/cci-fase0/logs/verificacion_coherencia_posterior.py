# Verificación de coherencia posterior a las ediciones (solo lectura). Uso: cd <raíz del repo> && python3 evidence/cci-fase0/logs/verificacion_coherencia_posterior.py
import re,os,sys,subprocess,collections
EV='evidence/cci-fase0'
def git(*a): return subprocess.run(['git']+list(a),capture_output=True,text=True).stdout
files=[]
for r,_,fs in os.walk(EV):
    for f in fs:
        if f.endswith(('.md','.txt','.py')): files.append(os.path.join(r,f))
# Se excluyen de los escaneos los propios productos de esta verificación (autorreferencia): su informe 13_, este script y su salida.
SELF=('auditoria_integral/13_INFORME_VERIFICACION_COHERENCIA_POSTERIOR.md','logs/verificacion_coherencia_posterior.py','logs/verificacion_coherencia_posterior_2026-11-22.txt')
files=[p for p in files if p[len(EV)+1:] not in SELF]
files.sort()
txt={p:open(p,encoding='utf-8',errors='replace').read() for p in files}
# clasificación (doc 05)
cls={}
for l in txt[EV+'/auditoria_integral/05_INFORME_AUDITORIA_INTEGRAL.md'].split('\n'):
    m=re.match(r'\| `([^`]+)` \| ([^|]+) \| ([^|]+) \|',l)
    if m: cls[EV+'/'+m.group(1)]=m.group(2).strip()
VIGENTE=[p for p,c in cls.items() if c.startswith(('Vigente','VIGENTE','Propuesta vigente'))]
MARK=re.compile(r'ESTADO VIGENTE|ANTECEDENTE|SUPERAD|superad|hist[oó]ric|Nota fechada|NOTA DE ACTUALIZACI|Actualizaci[oó]n posterior|AVISO DE VIGENCIA|ADVERTENCIA|SUSTITUID|RESPONDID|\[vigente|vigente:|resuelt|RESUELT|ya no|queda sustituid|no vigente|no es el estado|no es decisi',re.I)
def para(lines,i):
    a=i
    while a>0 and lines[a-1].strip(): a-=1
    b=i
    while b<len(lines)-1 and lines[b+1].strip(): b+=1
    return '\n'.join(lines[a:b+1])
out=[];R={}
def rec(k,s): R.setdefault(k,[]).append(s)
# V1/V2 referencias
roots=[EV,EV+'/entregables_formales',EV+'/auditoria_integral',EV+'/anexos',EV+'/logs','docs/fase0','docs/fase0/historico','docs/fase0/herramientas']
ext=set()
for p in files:
    if p.endswith('.py'): continue
    d=os.path.dirname(p)
    for m in re.finditer(r'`([A-Za-z0-9_./\-]+\.(?:md|txt|py|sha256|log))`',txt[p]):
        t=m.group(1)
        if any(os.path.exists(os.path.join(r,t)) for r in roots+[d]) or os.path.exists(t): rec('V1_ok',1); continue
        rec('V1_sin_resolver',(p[len(EV)+1:],t))
    for m in re.finditer(r'\]\(([^)#\s]+)(?:#[^)]*)?\)',txt[p]):
        t=m.group(1)
        if t.startswith(('http','mailto')): continue
        if os.path.exists(os.path.join(d,t)): rec('V2_ok',1)
        else: rec('V2_roto',(p[len(EV)+1:],t))
# V4 decisiones
CAN={'D4.a':'A','D4.b':'A','D4.c':'A','D4.d':'A','D6.a':'A','D6.b':'A','D6.c':'A0','D7.a':'A','D7.b':'A','D7.c':'C','D8':'A'}
pat=re.compile(r'\b(D4\.[a-d]|D6\.[a-c]|D7\.[a-c]|D8)\s*(?:=|→|->)\s*\**\s*(A0|[A-D])\b')
for p in files:
    for i,l in enumerate(txt[p].split('\n'),1):
        for m in pat.finditer(l):
            k,v=m.groups()
            if v==CAN[k]: rec('V4_ok',1)
            else: rec('V4_discrepancia',(p[len(EV)+1:],i,m.group(0),l.strip()[:200]))
# V5 8/18 sin marca
for p in files:
    if '/logs/' in p or 'auditoria_integral/12_' in p: continue
    ls=txt[p].split('\n')
    for i,l in enumerate(ls):
        if re.search(r'\b8\s*/\s*18\b|\b8 de 18\b',l):
            ctx=para(ls,i)
            if MARK.search(ctx) or MARK.search(l): rec('V5_8de18_con_marca',(p[len(EV)+1:],i+1))
            else: rec('V5_8de18_sin_marca',(p[len(EV)+1:],i+1,l.strip()[:220]))
# V6 D4/D6/D7/D8 pendientes sin marca
for p in files:
    if '/logs/' in p or 'auditoria_integral/12_' in p: continue
    ls=txt[p].split('\n')
    for i,l in enumerate(ls):
        if re.search(r'(D4\.[a-d]|D6\.[a-c]|D7\.[a-c]|\bD8\b|D-4|D-6|D-7|D-8)[^\n]{0,80}(pendiente|sin responder|no resuelt|abiert)',l,re.I) or re.search(r'(pendiente|sin responder|abiert)[^\n]{0,60}(D4\.[a-d]|D6\.[a-c]|D7\.[a-c]|\bD8\b)',l,re.I):
            ctx=para(ls,i)
            if MARK.search(ctx): rec('V6_con_marca',(p[len(EV)+1:],i+1))
            else: rec('V6_sin_marca',(p[len(EV)+1:],i+1,l.strip()[:240]))
# V7 arquitectura en documentos vigentes/propuesta
ARQ=re.compile(r'Supabase|PostgreSQL|\bSQL\b|\bRLS\b|backend|multiusuario|multi-usuario|autenticaci|\blogin\b|sincroniza',re.I)
NEG=re.compile(r'\bsin\b|\bno\b|\bni\b|exclu|fuera|descart|hist[oó]ric|superad|anterior|antecedente|prohib|no hay|ausen|nunca|ning[uú]n|retirad|sustituid|reemplaz|diferid|no se|opcional|futur|potencial|sustituye|origen|línea',re.I)
for p in files:
    c=cls.get(p,'')
    if not c.startswith(('Vigente','VIGENTE','Propuesta')): continue
    ls=txt[p].split('\n')
    for i,l in enumerate(ls):
        if ARQ.search(l):
            if NEG.search(l): rec('V7_arq_con_negacion_o_historico',(p[len(EV)+1:],i+1))
            else: rec('V7_arq_SIN_negacion',(p[len(EV)+1:],i+1,l.strip()[:260]))
# V10 D5.a–d como pendiente
for p in files:
    if '/logs/' in p or 'auditoria_integral/12_' in p: continue
    ls=txt[p].split('\n')
    for i,l in enumerate(ls):
        if re.search(r'D5\.a[–-]d[^\n]{0,60}(abiert|pendiente)|(abiert|pendiente)[^\n]{0,40}D5\.a[–-]d',l):
            ctx=para(ls,i)
            if re.search(r'fuera del alcance|fuera de alcance|no (son|est[aá]n) pendiente|no pendiente|no abiert|antecedente|hist[oó]ric|superad|no se (re)?abren|conservan|conservad',ctx,re.I): rec('V10_ok',1)
            else: rec('V10_sin_marca',(p[len(EV)+1:],i+1,l.strip()[:240]))
# V12 aceptación Fase 0 / autorización Fase 1 afirmadas
for p in files:
    if '/logs/' in p or 'auditoria_integral/12_' in p: continue
    ls=txt[p].split('\n')
    for i,l in enumerate(ls):
        if re.search(r'Fase 0 (v3\.3 )?(est[aá] )?(ACEPTAD|aceptad)|Fase 1 (est[aá] )?(AUTORIZAD|autorizad)|acept(a|ó|amos) (la )?Fase 0|autoriz(a|ó) (la )?Fase 1',l):
            ctx=para(ls,i)
            if re.search(r'\bno\b|NO|sin |hist[oó]ric|pendiente|anterior|condici|cuando|hasta|tras|despu[eé]s|solo|requiere|exige|si ',ctx): rec('V12_con_negacion_o_condicion',(p[len(EV)+1:],i+1))
            else: rec('V12_AFIRMACION_sin_negacion',(p[len(EV)+1:],i+1,l.strip()[:240]))
# V8 commits
shas=set()
for p in files:
    for m in re.finditer(r'\b([0-9a-f]{7,40})\b',txt[p]):
        s=m.group(1)
        if re.search(r'[a-f]',s) and re.search(r'\d',s) and len(s) in (7,8,40) and re.search(r'(commit|HEAD|base|SHA|rama|`)'+r'[^\n]{0,0}',txt[p][max(0,m.start()-40):m.start()]): shas.add((s,p))
for s,p in sorted(shas):
    ok=subprocess.run(['git','cat-file','-e',s+'^{commit}'],capture_output=True).returncode==0
    rec('V8_commit_existe' if ok else 'V8_no_es_commit_o_no_existe',(p[len(EV)+1:],s))
# V3 truncamientos en historial
log=git('log','--format=%h','--','evidence/cci-fase0').split()
log.reverse()
prev={}
for c in log:
    tr=git('ls-tree','-r','-l',c,'--',EV).split('\n')
    cur={}
    for l in tr:
        m=re.match(r'\d+ blob \w+\s+(\d+)\t(.+)',l)
        if m: cur[m.group(2)]=int(m.group(1))
    for f,s in cur.items():
        if f in prev and prev[f]>200 and s<prev[f]*0.9 and not f.endswith(('sha256',)) : rec('V3_reduccion_>10%',(c,f[len(EV)+1:],prev[f],s))
    prev=cur
# X controles estructurales
def gshow(c,path):
    return subprocess.run(['git','show',c+':'+path],capture_output=True,text=True).stdout
D06=txt[EV+'/auditoria_integral/06_REGISTRO_CONTRADICCIONES.md']
crs=re.findall(r'^## (CR-\d\d)[^\n]*',D06,re.M)
rec('X1_CR_encabezados_22' if len(crs)==22 and len(set(crs))==22 else 'X1_FALLO_CR_encabezados',len(crs))
def estados(doc):
    d={}
    for blk in re.split(r'^## (?=CR-\d\d)',doc,flags=re.M)[1:]:
        k=blk[:5]; m=re.search(r'Estado final:\*\* \*\*([A-Z_]+)\*\*',blk); d[k]=m.group(1) if m else None
    return d
est=estados(D06); cnt=collections.Counter(est.values())
rec('X1b_distribucion_estados',dict(cnt))
ok13=gshow('13b25ca','evidence/cci-fase0/auditoria_integral/06_REGISTRO_CONTRADICCIONES.md')
est0=estados(ok13) if ok13 else {}
dif=[(k,est0.get(k),est.get(k)) for k in sorted(est0) if k<='CR-18' and est0.get(k)!=est.get(k)]
rec('X2_estados_CR01_18_sin_cambio_vs_13b25ca' if not dif and est0 else 'X2_CAMBIOS_CR01_18',dif if dif else len(est0))
rec('X3_CR_con_linea_evidencia' if len(re.findall(r'Evidencia de verificaci[oó]n',D06))>=22 else 'X3_FALTA_evidencia',len(re.findall(r'Evidencia de verificaci[oó]n',D06)))
for cr in ('CR-19','CR-20','CR-21','CR-22'):
    faltan=[n for n in ('00_INDICE_VIGENTES_E_HISTORICOS.md','README_ENTREGA.md','auditoria_integral/01_INDICE_MAESTRO_FASE0.md','auditoria_integral/05_INFORME_AUDITORIA_INTEGRAL.md','auditoria_integral/07_CONTROL_DE_CAMBIOS_AUDITORIA_INTEGRAL.md','auditoria_integral/10_INFORME_EJECUTIVO_PREPARACION_CIERRE.md') if cr.replace('CR-','CR-') not in txt[EV+'/'+n] and ('19…' not in txt[EV+'/'+n] and '19…CR-22' not in txt[EV+'/'+n] and 'CR-19' not in txt[EV+'/'+n])]
    rec('X4_CR19_22_reflejados_en_indices' if not faltan else 'X4_no_mencionado',(cr,faltan))
AP=txt[EV+'/entregables_formales/APROBACIONES_FASE0.md']
rec('X5_aprobaciones_PENDIENTE',len(re.findall(r'PENDIENTE',AP)))
rec('X5b_aprobaciones_APROBADA_afirmadas',len(re.findall(r'\|\s*(APROBAD[AO]|COMPLETAD[AO])\s*\|',AP)))
# X8 doc 05 vs árbol
rows05=set(cls.keys()); real=set(EV+'/'+p[len(EV)+1:] for p in files)|{EV+'/'+s for s in SELF}|{EV+'/MANIFEST.sha256',EV+'/INVENTARIO_PUBLICADO.sha256',EV+'/anexos/MANIFEST_informe_browser_only.sha256'}
allf=set()
for r,_,fs in os.walk(EV):
    for f in fs: allf.add(os.path.join(r,f))
rec('X8_doc05_filas_vs_arbol' if rows05==allf else 'X8_DIFERENCIA',(len(rows05),len(allf),sorted(allf-rows05)[:5],sorted(rows05-allf)[:5]))
# X9 doc 11 vs docs/fase0
import hashlib
D11=txt[EV+'/auditoria_integral/11_INDICE_CONCILIACION_DOCS_FASE0.md']
n_ok=n_bad=0
for m in re.finditer(r'\| `([^`]+)` \| (\d+) \| `([0-9a-f]{64})` \|',D11):
    f,sz,h=m.groups(); fp=None
    for cand in ('docs/fase0/'+f,'docs/fase0/herramientas/'+f):
        if os.path.exists(cand): fp=cand;break
    if fp and os.path.getsize(fp)==int(sz) and hashlib.sha256(open(fp,'rb').read()).hexdigest()==h: n_ok+=1
    else: n_bad+=1
rec('X9_doc11_resultado_OK' if n_bad==0 else 'X9_DISCREPANCIAS',(n_ok,n_bad))
# X10 documentos de docs/fase0 y main
# resumen
for k in sorted(R): 
    v=R[k]; print('##',k,len(v))
    if k.endswith(('_ok','_con_marca','_con_negacion_o_historico','_con_negacion_o_condicion','_existe')): continue
    for x in v[:400]: print('   ',x)
