# Verificación semántica del expediente CCI Fase 0 (solo lectura). Uso (desde la raíz del repositorio):
#   python3 -I evidence/cci-fase0/logs/verificacion_semantica_fase0.py
# Complementa a verificacion_coherencia_posterior.py: aquí los controles evalúan SIGNIFICADO (estado de decisiones, entidades,
# aprobaciones, aplazamientos, relaciones) a nivel de frase, con pruebas positivas y negativas de cada control. Una coincidencia
# textual aislada no basta: cada hallazgo se clasifica en ERROR_REAL, ANTECEDENTE_ADVERTIDO, FALSO_POSITIVO_REVISADO o REVISION_HUMANA.
import re,os,sys,json
EV='evidence/cci-fase0'; FM=EV+'/entregables_formales'; AI=EV+'/auditoria_integral'
def rd(p): return open(p,encoding='utf-8',errors='replace').read()
# ---------------------------------------------------------------- vocabulario de estado vigente (fuente: REGISTRO_DECISIONES_RESUELTAS.md)
RESUELTAS_PQ=['P1','P2','P3','P4','P5','P9','P11','P12','P13','P14','Q-4','Q-7']
APLAZADAS=['P6','P7','P8','P10','P15','Q-1','Q-2','Q-3','Q-5','Q-6']
D_RES=['D-%d'%i for i in range(1,9)]
TOTAL_30=['P%d'%i for i in range(1,16)]+['Q-%d'%i for i in range(1,8)]+D_RES
MARK=re.compile(r'ESTADO VIGENTE|ANTECEDENTE|SUPERAD|superad|hist[oó]ric|Nota fechada|Alineaci[oó]n|NOTA DE ACTUALIZACI|Actualizaci[oó]n posterior|AVISO DE VIGENCIA|ADVERTENCIA|SUSTITUID|antes:|estado anterior|[Aa]ntes\b|anterior a la|previo a la|momento de su elaboraci|en su momento|RESPONDID|\[superado|\[vigente',re.I)
NEG=re.compile(r'\b(no|ni|sin|ninguna?|nunca|tampoco|pendiente de ser|aún no|todavía no|0/7|0 de 7)\b',re.I)
def sentences(line):
    return [s for s in re.split(r'(?<=[.;])\s+|\s+—\s+(?=[A-ZÁÉÍÓÚ])',line) if s.strip()]
def para_of(lines,i):
    a=i
    while a>0 and lines[a-1].strip(): a-=1
    b=i
    while b<len(lines)-1 and lines[b+1].strip(): b+=1
    return '\n'.join(lines[a:b+1])
# ---------------------------------------------------------------- controles a nivel de frase (funciones puras, probadas más abajo)
def c_conteo_entidades(s):
    """Frase con un conteo k/18 (o k de 18) distinto de 18/18 como estado de entidades aprobadas."""
    m=[int(x) for x in re.findall(r'(?<![\d,.])(\d{1,2})\s*/\s*18\b|(?<![\d,.])(\d{1,2}) de 18\b',s) for x in x if x]
    return [k for k in m if k!=18 and not re.search(r'[Ee]ntidad (\d+) de 18',s)]
def c_resuelta_como_pendiente(s,ids):
    out=[]
    for i in ids:
        for m in re.finditer(r'(?<![\w-])%s(?![\w.])'%re.escape(i),s):
            w=s[m.end():m.end()+70]
            if re.match(r'[^.;]{0,60}\b(pendiente|abierta|sin decidir|sin resolver|no resuelta|no decidida)\b',w,re.I) and not re.search(r'\b(resuelta|resuelto|resueltas|aplaz|ratific|antes de)\b',s[max(0,m.start()-30):m.end()+90],re.I) and not NEG.search(s[max(0,m.start()-12):m.start()]):
                out.append(i)
    return out
def c_aplazada_como_resuelta(s,ids):
    out=[]
    for i in ids:
        for m in re.finditer(r'(?<![\w-])%s(?![\w.])'%re.escape(i),s):
            w=s[m.end():m.end()+60]
            if re.match(r'[^.;|]{0,40}\b(resuelta|resuelto|decidida|decidido|aprobada|aprobado)\b',w) and not re.search(r'\b(no|ni|sin|antes de|hasta|cuando|aplaz|requiere|exige|debe)\b',s[max(0,m.start()-20):m.end()+70],re.I):
                out.append(i)
    return out
def c_aprobaciones_emitidas(s):
    if re.search(r'0\.1\s*(?:–|-|…|\.\.\.)\s*0\.7|aprobaciones formales|aprobaciones 0\.\d',s,re.I) and re.search(r'\b(emitid[ao]s?|aprobad[ao]s?|concedid[ao]s?)\b',s,re.I) and not NEG.search(s) and not re.search(r'\b(para|cuando|hasta|requier|exig|solicit|prepar|responder|someter)',s,re.I): return True
    return False
def c_fase_afirmada(s):
    return bool(re.search(r'Fase 0 (v3\.3 )?(est[aá] )?(ACEPTAD|aceptad)|Fase 1 (est[aá] )?(AUTORIZAD|autorizad)',s)) and not NEG.search(s) and not re.search(r'\b(cuando|hasta|tras|después|requiere|exige|si |solo con|condici|v3\.3|histó|anterior)',s)
def c_c2c3_resueltas(s):
    return bool(re.search(r'\bC-[23]\b',s)) and bool(re.search(r'\b(resuelt[ao]s?|cerrad[ao]s?|superad[ao]s?)\b',s)) and not NEG.search(s) and not re.search(r'\b(abiert|pendiente|limitaci)',s,re.I)
NOAPR=[('Campaña','Oferta'),('Campaña','Pieza'),('Brief','Oferta'),('Brief','Producto'),('Reglas de copy','ReglaDeMarca')]
def c_relacion_no_aprobada_como_aprobada(s):
    out=[]
    for a,b in NOAPR:
        if re.search(re.escape(a)+r'\s*(?:–|-|↔|con|y)\s*'+re.escape(b),s) and re.search(r'\baprobad[ao]s?\b',s) and not NEG.search(s) and not re.search(r'\b(propuesta|pendiente)\b',s,re.I): out.append((a,b))
    return out
def c_mvp_fase(s):
    """Frase que sitúa el fin del MVP en una fase distinta de la 2."""
    return bool(re.search(r'MVP[^.]{0,40}(fin|final|termina|concluye)[^.]{0,25}Fase\s*[345]\b|(fin|final)\s+(de la )?Fase\s*[345][^.]{0,30}MVP',s)) and not NEG.search(s)
def c_q4_abierta(s):
    return bool(re.search(r'Q-4[^.|]{0,40}\b(abierta|pendiente|sin decidir)\b|decisi[oó]n Q-4 abierta',s)) 
def c_atributos_aprobados(s):
    return bool(re.search(r'\b(atributos?|campos|cardinalidad(?:es)?)\b[^.;]{0,60}\baprobad[ao]s?\b',s)) and not NEG.search(s) and not re.search(r'\b(propuest|diferid|deben|podrán|solo)\b',s,re.I)
# ---------------------------------------------------------------- pruebas de cada control (positivas = debe detectar; negativas = no debe)
PRUEBAS=[
 ('conteo: «9/18 aprobadas» se detecta',lambda:c_conteo_entidades('P4.A vigente 9/18 aprobadas')==[9],True),
 ('conteo: «18/18» no se detecta',lambda:c_conteo_entidades('P4.A 18/18 aprobadas')==[],True),
 ('conteo: «Entidad 9 de 18» (ordinal) no se detecta',lambda:c_conteo_entidades('Entidad 9 de 18: Hallazgo')==[],True),
 ('conteo: «8/18» se detecta',lambda:c_conteo_entidades('quedan 8/18')==[8],True),
 ('resuelta-como-pendiente: «P5 pendiente» se detecta',lambda:c_resuelta_como_pendiente('| P5 | Binarios | Pendiente (indispensable) |',RESUELTAS_PQ)==['P5'],True),
 ('resuelta-como-pendiente: «P5 RESUELTA» no se detecta',lambda:c_resuelta_como_pendiente('P5 resuelta; pendiente solo el formato',RESUELTAS_PQ)==[],True),
 ('resuelta-como-pendiente: «P4 (parcial) pendiente» se detecta',lambda:c_resuelta_como_pendiente('P4 sigue pendiente de P4.B',RESUELTAS_PQ)==['P4'],True),
 ('resuelta-como-pendiente: ID dentro de otro («P41») no se detecta',lambda:c_resuelta_como_pendiente('P41 pendiente',RESUELTAS_PQ)==[],True),
 ('aplazada-como-resuelta: «P6 resuelta» se detecta',lambda:c_aplazada_como_resuelta('P6 resuelta el 2026-11-22',APLAZADAS)==['P6'],True),
 ('aplazada-como-resuelta: «P6 no resuelta» no se detecta',lambda:c_aplazada_como_resuelta('P6 no resuelta, aplazamiento aceptado',APLAZADAS)==[],True),
 ('aplazada-como-resuelta: «P8 se resolverá antes de Fase 2» no se detecta',lambda:c_aplazada_como_resuelta('P8 debe estar resuelta antes de Fase 2',APLAZADAS)==[],True),
 ('aprobaciones: «0.1–0.7 aprobadas» se detecta',lambda:c_aprobaciones_emitidas('Las aprobaciones 0.1–0.7 están aprobadas'),True),
 ('aprobaciones: «0/7 emitidas» no se detecta',lambda:not c_aprobaciones_emitidas('Aprobaciones 0.1–0.7: 0/7 emitidas'),True),
 ('aprobaciones: «ninguna aprobación 0.1–0.7 emitida» no se detecta',lambda:not c_aprobaciones_emitidas('Ninguna aprobación 0.1–0.7 está emitida'),True),
 ('aprobaciones: «para emitir las aprobaciones 0.1–0.7» no se detecta',lambda:not c_aprobaciones_emitidas('el propietario debe responder para emitir las aprobaciones 0.1–0.7 aprobadas o no'),True),
 ('fase: «Fase 0 aceptada» se detecta',lambda:c_fase_afirmada('La Fase 0 está aceptada por el propietario'),True),
 ('fase: «Fase 0 no aceptada» no se detecta',lambda:not c_fase_afirmada('La Fase 0 no está aceptada'),True),
 ('fase: «Fase 1 autorizada» se detecta',lambda:c_fase_afirmada('Fase 1 autorizada para iniciar'),True),
 ('fase: «una vez aceptada Fase 0» no se detecta',lambda:not c_fase_afirmada('Una vez aceptada Fase 0, deberá emitirse la autorización'),True),
 ('C-2/C-3: «C-2 y C-3 resueltas» se detecta',lambda:c_c2c3_resueltas('C-2 y C-3 quedaron resueltas'),True),
 ('C-2/C-3: «C-2 y C-3 abiertas» no se detecta',lambda:not c_c2c3_resueltas('C-2 y C-3 siguen abiertas'),True),
 ('C-2/C-3: «no resueltas» no se detecta',lambda:not c_c2c3_resueltas('C-2 y C-3 no están resueltas'),True),
 ('relación: «Campaña–Oferta aprobada» se detecta',lambda:c_relacion_no_aprobada_como_aprobada('La relación Campaña–Oferta está aprobada')==[('Campaña','Oferta')],True),
 ('relación: «Campaña–Oferta NO aprobada» no se detecta',lambda:c_relacion_no_aprobada_como_aprobada('Campaña–Oferta: no aprobada')==[],True),
 ('relación: «Campaña–Brief aprobada» no se detecta',lambda:c_relacion_no_aprobada_como_aprobada('Campaña–Brief aprobada')==[],True),
 ('relación: «Brief con Producto aprobado» se detecta',lambda:c_relacion_no_aprobada_como_aprobada('Brief con Producto aprobado')==[('Brief','Producto')],True),
 ('MVP: «MVP termina al concluir Fase 3» se detecta',lambda:c_mvp_fase('El MVP termina al concluir Fase 3'),True),
 ('MVP: «MVP termina al concluir Fase 2» no se detecta',lambda:not c_mvp_fase('El MVP termina al concluir Fase 2'),True),
 ('Q-4: «decisión Q-4 abierta» se detecta',lambda:c_q4_abierta('Definición del MVP (propuesta; decisión Q-4 abierta)'),True),
 ('Q-4: «Q-4 resuelta» no se detecta',lambda:not c_q4_abierta('Q-4 quedó resuelta'),True),
 ('atributos: «atributos aprobados» se detecta',lambda:c_atributos_aprobados('Los atributos de Brief están aprobados'),True),
 ('atributos: «los atributos no están aprobados» no se detecta',lambda:not c_atributos_aprobados('Los atributos no están aprobados'),True),
]
print('## PRUEBAS de los controles semánticos (casos positivos y negativos)')
fall=0
for d,fn,_ in PRUEBAS:
    ok=bool(fn()); fall+=0 if ok else 1; print('   [%s] %s'%('OK' if ok else 'FALLO',d))
print('   Resultado: %d/%d'%(len(PRUEBAS)-fall,len(PRUEBAS)))
# ---------------------------------------------------------------- datos reales
files=[]
for r,_,fs in os.walk(EV):
    for f in fs:
        if f.endswith(('.md','.txt')): files.append(os.path.join(r,f))
files.sort()
SELF=('logs/verificacion_semantica_fase0','logs/verificacion_coherencia_posterior','logs/verificaciones_de_preparacion','logs/verificar_expediente_historico','auditoria_integral/13_INFORME','logs/escaneo','logs/modelo_estructural')
files=[p for p in files if not any(s in p for s in SELF)]
txt={p:rd(p) for p in files}
cls={}
for l in txt[AI+'/05_INFORME_AUDITORIA_INTEGRAL.md'].split('\n'):
    m=re.match(r'\| `([^`]+)` \| ([^|]+) \| ([^|]+) \|',l)
    if m: cls[EV+'/'+m.group(1)]=m.group(2).strip()
LITERAL=EV+'/entregables_formales/PROPUESTA_MAESTRA_CIERRE_FASE0_v1.0.md'   # copia literal del texto ratificado (estado previo a la ratificación en su §20)
VIG=[p for p in files if cls.get(p,'').startswith(('Vigente','VIGENTE','Propuesta')) and p!=LITERAL]
# excepciones revisadas a mano (falsos positivos con su razón); nunca se desactiva un control
EXC=[('REGISTRO_DECISIONES_RESUELTAS.md','pasa de 8/18 a **9/18','Sección fechada del registro acumulativo (aclaración D4.c); superada cronológicamente por la ratificación B1 (18/18) en el mismo registro; el texto anterior se conserva por regla de historial')]
res={'ERROR_REAL':[],'ANTECEDENTE_ADVERTIDO':[],'FALSO_POSITIVO_REVISADO':[],'REVISION_HUMANA':[]}
def hallazgo(ctrl,p,i,s,kind=None):
    ls=txt[p].split('\n'); ctx=para_of(ls,i)
    for (fi,sub,razon) in EXC:
        if fi in p and sub in s: res['FALSO_POSITIVO_REVISADO'].append((ctrl,p[len(EV)+1:],i+1,s[:160],razon)); return
    cat='ANTECEDENTE_ADVERTIDO' if (MARK.search(ctx) or MARK.search(s)) else 'ERROR_REAL'
    res[cat].append((ctrl,p[len(EV)+1:],i+1,s.strip()[:200],''))
for p in VIG:
    ls=txt[p].split('\n')
    for i,l in enumerate(ls):
        if l.startswith('|') and p.endswith('13_REGISTRO_DECISIONES_PROPIETARIO.md') and False: continue
        for s in sentences(l):
            if c_conteo_entidades(s): hallazgo('S1_conteo_entidades_distinto_de_18',p,i,s)
            if c_resuelta_como_pendiente(s,RESUELTAS_PQ): hallazgo('S2_decision_resuelta_presentada_como_pendiente',p,i,s)
            if c_aplazada_como_resuelta(s,APLAZADAS): hallazgo('S3_aplazamiento_presentado_como_resuelto',p,i,s)
            if c_aprobaciones_emitidas(s): hallazgo('S4_aprobaciones_presentadas_como_emitidas',p,i,s)
            if c_fase_afirmada(s): hallazgo('S5_fase_0_aceptada_o_fase_1_autorizada',p,i,s)
            if c_c2c3_resueltas(s): hallazgo('S6_C2_C3_presentadas_como_resueltas',p,i,s)
            if c_relacion_no_aprobada_como_aprobada(s): hallazgo('S7_relacion_no_aprobada_presentada_como_aprobada',p,i,s)
            if c_mvp_fase(s) or c_q4_abierta(s): hallazgo('S8_roadmap_o_mvp_contradice_Q4',p,i,s)
            if c_atributos_aprobados(s): hallazgo('S9_atributos_o_cardinalidades_presentados_como_aprobados',p,i,s)
# ---------------------------------------------------------------- controles estructurales
reg=txt[FM+'/REGISTRO_DECISIONES_RESUELTAS.md']
prop=rd(LITERAL)
defs={}
for m in re.finditer(r'## P4\.A — Entidad (\d+): [^\n]*\n\*\*Definición aprobada \(literal\):\*\* «([^»]+)»',reg): defs[int(m.group(1))]=m.group(2).strip()
m=re.search(r'Texto exacto aprobado: «\*\*Adaptación de canal:\*\* ([^»]+)»',reg); defs[13]='**Adaptación de canal:** '+m.group(1).strip() if m else None
for m in re.finditer(r'- \*\*Entidad (\d+) — [^\n]*?Definición aprobada \(literal de la propuesta ratificada\): «([^»]+)»',reg): defs[int(m.group(1))]=m.group(2).strip()
print('## E1 definiciones mínimas en el registro: %d/18 (%s)'%(len([k for k,v in defs.items() if v]),sorted(k for k,v in defs.items() if v)==list(range(1,19))))
bad=[]
for b in re.split(r'\n(?=PE-\d\d — )',prop)[1:]:
    n=int(b[3:5]); d=re.search(r'Propuesta de definición:\n\n(.+?)\n\nLímites:',b,re.S).group(1).strip()
    if defs.get(n)!=d: bad.append(n)
print('## E2 definiciones 9–12 y 14–18 del registro = texto literal de la propuesta: %s'%('SÍ (9/9)' if not bad else 'NO %s'%bad))
m03=txt[AI+'/03_MATRIZ_MAESTRA_ENTIDADES_P4A.md']
rows={}
for l in m03.split('\n'):
    m=re.match(r'\| (\d+) \| ([^|]+) \| «(.+)» \| ([^|]+) \|$',l)
    if m: rows[int(m.group(1))]=m.group(3).strip()
mis=[n for n in range(1,19) if rows.get(n)!=defs.get(n)]
print('## E3 doc 03 (tabla A) reproduce fielmente las 18 definiciones del registro: %d/18; discrepancias: %s'%(18-len(mis),mis or 'ninguna'))
cons=txt[FM+'/MATRIZ_CONSOLIDADA_18_ENTIDADES.md']
est=[]
for n in range(1,19):
    m=re.search(r'^\| %d \| ([^|]+) \|'%n,cons,re.M)
    est.append((n,bool(m and re.search(r'Aprobada',m.group(1)))))
print('## E4 matriz consolidada: entidades con estado «Aprobada»: %d/18 (faltan: %s)'%(sum(1 for _,o in est if o),[n for n,o in est if not o] or 'ninguna'))
inf=[n for n,d in defs.items() if d and re.search(r'\b(obligatori|cardinalidad|atributo|campo|estado[s]? del|ciclo de vida|fórmula)',d,re.I)]
print('## E5 definiciones con vocabulario de atributos/cardinalidades/obligatoriedad (revisión humana): %s'%(inf or 'ninguna'))
b2=re.search(r'### B2 — P4\.B[^\n]*\n\*\*Aprueba:\*\*(.+?)\*\*NO aprueba\*\*',reg,re.S).group(1)
rels=[x for x in re.split(r';|\by\b',re.search(r'una por una\*\*: (.+)\.\s*$',b2.strip(),re.S).group(1)) if x.strip()] if re.search(r'una por una\*\*: (.+)\.\s*$',b2.strip(),re.S) else []
print('## R1 relaciones ratificadas en B2: 2 documentadas + %d una por una = %d (esperado 13)'%(len(rels),2+len(rels)))
# decisiones (30)
reg13=txt[FM+'/13_REGISTRO_DECISIONES_PROPIETARIO.md']
mat02=txt[AI+'/02_MATRIZ_MAESTRA_DECISIONES.md']
print('## D1 universo de decisiones de nivel superior: %d (esperado 30); resueltas %d (%s); aplazadas %d; abiertas de nivel superior: %d'%(len(TOTAL_30),len(RESUELTAS_PQ)+8,'P1,P2,P3,P4,P5,P9,P11–P14,Q-4,Q-7,D-1…D-8',len(APLAZADAS),len(TOTAL_30)-len(RESUELTAS_PQ)-8-len(APLAZADAS)))
for k in APLAZADAS:
    ok=re.search(r'\| %s \|[^\n]*(APLAZADA|aplazamiento aceptado)'%re.escape(k),reg13+mat02)
    if not ok: print('   FALLO D2: %s sin marca de aplazamiento en 13_REGISTRO o 02'%k); res['ERROR_REAL'].append(('D2_aplazamiento_sin_marca','',0,k,''))
for k in RESUELTAS_PQ[3:]:  # P4,P5,P9,P11-14,Q-4 resueltas por ratificación
    if k=='Q-7': continue
    ok=re.search(r'\| %s \|[^\n]*(RESUELTA por ratificación|resuelta)'%re.escape(k),reg13+mat02,re.I)
    if not ok: print('   FALLO D3: %s sin marca de resuelta en 13_REGISTRO o 02'%k); res['ERROR_REAL'].append(('D3_resuelta_sin_marca','',0,k,''))
ap=txt[FM+'/APROBACIONES_FASE0.md'].split('## 4. Antecedente')[0]   # la parte vigente; el antecedente está marcado como superado
filas=[l for l in ap.split('\n') if re.match(r'\| 0\.[1-7] ',l)]
emit=[l[:60] for l in filas if not re.search(r'PENDIENTE',l) or re.search(r'\|\s*(APROBADA|RECHAZADA)\s*\|',l)]
print('## A1 fichas 0.1–0.7 en la tabla vigente de APROBACIONES_FASE0: %d filas; con estado distinto de PENDIENTE: %s'%(len(filas),emit or 'ninguna'))
if len(filas)!=7 or emit: res['ERROR_REAL'].append(('A1_aprobaciones','entregables_formales/APROBACIONES_FASE0.md',0,str(emit),''))
obsol=[(l[:30],t) for l in filas for t in re.findall(r'P4 \(parcial|P4 sigue parcial|~~P3~~|pendiente[^|]{0,30}(?:P5|P9|P11|P12|P13)|(?:P5|P9|P11|P12|P13)[^|]{0,15}pendiente',l)]
print('## A2 prerrequisitos desactualizados en las fichas: %s'%(obsol or 'ninguno'))
if obsol: res['ERROR_REAL'].append(('A2_prerrequisitos_desactualizados','entregables_formales/APROBACIONES_FASE0.md',0,str(obsol),''))
for k in ('antecedente','superado'): pass
if len([k for k,v in defs.items() if v])!=18: res['ERROR_REAL'].append(('E1_definiciones_en_registro','',0,'faltan definiciones',''))
if bad: res['ERROR_REAL'].append(('E2_registro_distinto_de_propuesta','',0,str(bad),''))
if mis: res['ERROR_REAL'].append(('E3_doc03_distinto_del_registro','auditoria_integral/03_MATRIZ_MAESTRA_ENTIDADES_P4A.md',0,str(mis),''))
if sum(1 for _,o in est if o)!=18: res['ERROR_REAL'].append(('E4_matriz_consolidada_sin_18_aprobadas','entregables_formales/MATRIZ_CONSOLIDADA_18_ENTIDADES.md',0,str([n for n,o in est if not o]),''))
if len(rels)+2!=13: res['ERROR_REAL'].append(('R1_relaciones_ratificadas_distintas_de_13','',0,str(len(rels)+2),''))
print('## RESUMEN de hallazgos por clase')
for k,v in res.items(): print('   %-26s %d'%(k,len(v)))
for k in ('ERROR_REAL','REVISION_HUMANA','FALSO_POSITIVO_REVISADO'):
    for x in res[k][:80]: print('   [%s] %s | %s:%s | %s %s'%(k,x[0],x[1],x[2],x[3],('| '+x[4]) if x[4] else ''))
print('## ANTECEDENTE_ADVERTIDO (detalle por control)')
from collections import Counter
for c,n in sorted(Counter(x[0] for x in res['ANTECEDENTE_ADVERTIDO']).items()): print('   %-60s %d'%(c,n))
print('## Alcance: %d archivos .md/.txt revisados; %d clasificados vigentes/propuesta (frase a frase)'%(len(files),len(VIG)))
sys.exit(1 if res['ERROR_REAL'] or fall else 0)
