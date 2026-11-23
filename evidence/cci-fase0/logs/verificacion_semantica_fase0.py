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

# ---------------------------------------------------------------- v2 (segunda regularización): R-1, cuestiones residuales de D-3/D-5 y D5.a–d
NEGX=re.compile(r'\b(no|ni|sin|fuera|permanec\w*|ning[uú]n\w*|jam[aá]s|nunca)\b',re.I)
R1_ITEMS={1:r'reglas de copy',2:r'auditor[ií]a o validaciones previas',3:r'(se modifica|modificaci[oó]n de) un contenido aprobado',4:r'relaci[oó]n con las versiones|relaciona la aprobaci[oó]n con las versiones',5:r'identidad exacta',6:r'estados (documentados )?(del|en el) flujo'}
def c_r1_faltantes(sec):
    """Devuelve los números de cuestión residual (1 = D-3 reglas de copy; 2–6 = D-5 (1)–(5)) que NO aparecen en el texto de R-1."""
    return [k for k,rx in R1_ITEMS.items() if not re.search(rx,sec,re.I)]
def c_r1_reabre_d5ad(sec):
    """Frases de R-1 que mencionan D5.a–d sin una exclusión expresa (no reabre / fuera del alcance / no figuran)."""
    out=[]
    for s in sentences(sec):
        if re.search(r'D-?5\.[a-d]',s) and not NEGX.search(s): out.append(s.strip()[:120])
    return out
def c_d5ad_pendiente(s):
    return bool(re.search(r'D-?5\.[a-d]',s)) and bool(re.search(r'\b(pendientes?|abiertas?|por decidir|sin decidir|siguen abiertas)\b',s,re.I)) and not NEGX.search(s) and not re.search(r'antecedente|superad|hist[oó]ric',s,re.I)
def c_r1_como_resolucion(s):
    return bool(re.search(r'(?<![A-Za-z])R-1(?!\d)',s)) and bool(re.search(r'\b(queda resuelta|resuelve|resuelta|decisi[oó]n tomada|se decide|decidid[ao])\b',s,re.I)) and not NEGX.search(s)
def c_reco_como_aprobacion(s):
    """Recomendación de Claude presentada como decisión/aprobación del propietario (sin negación)."""
    if not re.search(r'Rec\. Claude|recomendaci[oó]n',s,re.I) or NEGX.search(s): return False
    a=re.search(r'\b(es|como|equivale a|constituye) (la |una )?(decisi[oó]n|aprobaci[oó]n) (del propietario|emitida)',s,re.I)
    b=re.search(r'(propietario|owner)[^.]{0,40}\b(decidi[oó]|aprob[oó]|acept[oó]|adopt[oó]|ratific[oó])\b[^.]{0,60}recomendaci[oó]n|recomendaci[oó]n[^.]{0,60}\b(fue|queda|qued[oó]) (aprobada|aceptada|adoptada|ratificada)\b',s,re.I)
    return bool(a or b)
def c_r1_con_d5ad(s):
    """Frase que une R-1 con D5.a–d sin exclusión expresa (R-1 no puede decidir ni reabrir D5.a–d)."""
    return bool(re.search(r'(?<![A-Za-z])R-1(?!\d)',s)) and bool(re.search(r'D-?5\.[a-d]',s)) and not NEGX.search(s)
def c_residuales_incompletos(s):
    return bool(re.search(r'puntos 1, 2, 3 y 5|\(1\), \(2\), \(3\) y \(5\)|cuestiones 1, 2, 3 y 5|subcuestiones[^.]{0,40}D-5[^.]{0,30}\b1, 2, 3 y 5',s))
def c_doc_r1_sin_seis(t):
    """Un documento que menciona la pregunta R-1 debe declarar las seis cuestiones (o remitir a la lista completa)."""
    return bool(re.search(r'(?<![A-Za-z])R-1(?!\d)',t)) and not re.search(r'seis cuestiones|cinco cuestiones residuales|\(1\) a \(5\)|cinco de D-5|seis cuestiones residuales',t)
def c_r1_fila_ok(k,fila):
    """La fila k de la tabla de R-1 debe contener su propia cuestión (no basta que el texto aparezca en otro lugar de la sección)."""
    return bool(re.search(R1_ITEMS[k],fila,re.I))
def c_doc06_marcado(t):
    """06_MODELO_DATOS_CCI.md: marcado como propuesta histórica no aprobada y sin afirmar que sea esquema vigente/definitivo."""
    return bool(re.search(r'PROPUESTA HIST[ÓO]RICA',t)) and bool(re.search(r'no es un esquema de datos aprobado',t,re.I)) and not re.search(r'esquema definitivo|contrato definitivo|es el esquema vigente',t,re.I)
R1_OK='''### R-1
Se aplazan seis cuestiones: la ubicación conceptual de la familia de reglas de copy (D-3) y las cinco de D-5: auditoría o validaciones previas; qué sucede cuando se modifica un contenido aprobado; relación con las versiones; identidad exacta del contenido; relación con los estados del flujo. No reabre D5.a–d, que permanecen fuera del alcance vigente. Una respuesta afirmativa se registra como aplazamiento.'''
PRUEBAS_V2=[
 ('R-1: texto completo (6/6) aprueba',lambda:c_r1_faltantes(R1_OK)==[],True),
 ('R-1: sin la identidad exacta del contenido (cuestión 4 de D-5) se detecta',lambda:c_r1_faltantes(R1_OK.replace('identidad exacta del contenido; ',''))==[5],True),
 ('R-1: sin la ubicación de las reglas de copy (D-3) se detecta',lambda:c_r1_faltantes(R1_OK.replace('reglas de copy','reglas')).__contains__(1),True),
 ('R-1: sin estados del flujo se detecta',lambda:c_r1_faltantes(R1_OK.replace('estados del flujo','otros temas'))==[6],True),
 ('R-1: D5.a–d con exclusión expresa no se detecta',lambda:c_r1_reabre_d5ad(R1_OK)==[],True),
 ('R-1: D5.c presentada como cuestión a decidir se detecta',lambda:len(c_r1_reabre_d5ad(R1_OK+' Decide además D5.c sobre versiones.'))==1,True),
 ('D5.a–d: «siguen abiertas» sin marca se detecta',lambda:c_d5ad_pendiente('D5.a–d siguen abiertas.'),True),
 ('D5.a–d: «no son pendientes» no se detecta',lambda:not c_d5ad_pendiente('D5.a–d fuera del alcance: no son pendientes ni abiertas.'),True),
 ('D5.a–d: antecedente superado no se detecta',lambda:not c_d5ad_pendiente('Antecedente superado: D5.a–d figuraban como abiertas.'),True),
 ('R-1: «R-1 queda resuelta» se detecta',lambda:c_r1_como_resolucion('R-1 queda resuelta por la ratificación.'),True),
 ('R-1: «no es una resolución» no se detecta',lambda:not c_r1_como_resolucion('R-1 no es una resolución: se registra como aplazamiento.'),True),
 ('recomendación presentada como decisión del propietario se detecta',lambda:c_reco_como_aprobacion('La recomendación de Claude es la decisión del propietario.'),True),
 ('recomendación [Rec. Claude] no vinculante no se detecta',lambda:not c_reco_como_aprobacion('[Rec. Claude] no es decisión del propietario.'),True),
 ('residuales de D-5: «puntos 1, 2, 3 y 5» (omite el 4) se detecta',lambda:c_residuales_incompletos('D-5 (puntos 1, 2, 3 y 5) no tienen decisión propia.'),True),
 ('residuales de D-5: lista (1) a (5) no se detecta',lambda:not c_residuales_incompletos('las cinco cuestiones (1) a (5) de D-5'),True),
 ('documento con R-1 sin las seis cuestiones se detecta',lambda:c_doc_r1_sin_seis('Responder R-1 si se quiere.'),True),
 ('documento con R-1 y «seis cuestiones» no se detecta',lambda:not c_doc_r1_sin_seis('Responder R-1: seis cuestiones residuales.'),True),
 ('recomendación: «el propietario decidió aprobar la recomendación de Claude» se detecta',lambda:c_reco_como_aprobacion('El propietario decidió aprobar la recomendación de Claude sobre R-1.'),True),
 ('recomendación: «la recomendación queda aprobada» se detecta',lambda:c_reco_como_aprobacion('La recomendación de Claude queda aprobada.'),True),
 ('recomendación: «el propietario no ha decidido sobre la recomendación» no se detecta',lambda:not c_reco_como_aprobacion('El propietario no ha decidido sobre la recomendación de Claude.'),True),
 ('R-1 + D5.c sin exclusión se detecta',lambda:c_r1_con_d5ad('R-1 incluye decidir D5.c (agrupación de las cuestiones 3 y 4).'),True),
 ('R-1 + D5.a–d con «no reabre» no se detecta',lambda:not c_r1_con_d5ad('R-1 no reabre D5.a–d, fuera del alcance vigente.'),True),
 ('R-1 por fila: fila (5) sin «identidad exacta» se detecta',lambda:not c_r1_fila_ok(5,'| 5 | D-5, cuestión (4) | La identidad del contenido |'),True),
 ('R-1 por fila: fila (5) con «identidad exacta» aprueba',lambda:c_r1_fila_ok(5,'| 5 | D-5, cuestión (4) | La identidad exacta del contenido al que se aplica cada aprobación |'),True),
 ('doc 06: sin marca histórica se detecta',lambda:not c_doc06_marcado('Esquema definitivo de datos.'),True),
 ('doc 06: con marca histórica y «no es un esquema de datos aprobado» aprueba',lambda:c_doc06_marcado('> PROPUESTA HISTÓRICA — NO APROBADA. No es un esquema de datos aprobado.'),True),
 ('doc 06: marca histórica pero «es el esquema definitivo» se detecta',lambda:not c_doc06_marcado('PROPUESTA HISTÓRICA. No es un esquema de datos aprobado. Es el esquema definitivo.'),True),
]
PRUEBAS=PRUEBAS+PRUEBAS_V2
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
# barrido ampliado (S10–S13): informes y controles fechados también describen el estado; solo se excluyen históricos, antecedentes, superados y la copia literal
VIG2=[p for p in files if not cls.get(p,'Histórico').startswith(('Hist','Antecedente','Superado')) and p!=LITERAL and cls.get(p)]
for p in VIG2:
    ls=txt[p].split('\n')
    for i,l in enumerate(ls):
        for s in sentences(l):
            if c_d5ad_pendiente(s): hallazgo('S10_D5ad_presentadas_como_pendientes_o_abiertas',p,i,s)
            if c_r1_como_resolucion(s): hallazgo('S11_R1_presentada_como_resolucion',p,i,s)
            if c_reco_como_aprobacion(s): hallazgo('S12_recomendacion_presentada_como_decision',p,i,s)
            if c_residuales_incompletos(s): hallazgo('S13_residuales_D5_incompletos_(omite_la_cuestion_4)',p,i,s)
            if c_r1_con_d5ad(s): hallazgo('S14_R1_vinculada_a_D5ad_sin_exclusion',p,i,s)
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
pq=txt[FM+'/PAQUETE_DECISION_APROBACIONES_0_1_A_0_7.md']
mm=re.search(r'## Pregunta R-1[^\n]*\n(.*?)(?=\n## )',pq,re.S)
sec=mm.group(1) if mm else ''
falt=c_r1_faltantes(sec); reab=c_r1_reabre_d5ad(sec)
filas=len(re.findall(r'^\| [1-6] \| D-[35]',sec,re.M))
filas_mal=[k for k in range(1,7) if not any(c_r1_fila_ok(k,l) for l in re.findall(r'^\| %d \| D-[35][^\n]*'%k,sec,re.M))]
mred=re.search(r'Redacción final[^\n]*\n?[^\n]*R-1\. Confirmo[^\n]*',sec)
red_mal=not (mred and not c_r1_faltantes(mred.group(0)) and re.search(r'seis cuestiones',mred.group(0)))
print('## R2 R-1 en el paquete: sección encontrada=%s; cuestiones ausentes=%s; filas de la tabla=%d (esperado 6); filas cuyo texto no contiene su cuestión=%s; redacción final completa=%s; frases que reabren D5.a–d=%s'%(bool(mm),falt or 'ninguna',filas,filas_mal or 'ninguna',not red_mal,reab or 'ninguna'))
if not mm or falt or filas!=6 or reab or filas_mal or red_mal: res['ERROR_REAL'].append(('R2_R1_incompleta_o_reabre_D5','entregables_formales/PAQUETE_DECISION_APROBACIONES_0_1_A_0_7.md',0,str((falt,filas,filas_mal,red_mal,reab)),''))
sinseis=[p[len(EV)+1:] for p in VIG if c_doc_r1_sin_seis(txt[p])]
print('## R3 documentos vigentes que mencionan R-1 sin declarar las seis cuestiones: %s'%(sinseis or 'ninguno'))
for x in sinseis: res['ERROR_REAL'].append(('R3_documento_con_R1_sin_seis_cuestiones',x,0,'',''))
reg_n=re.search(r'## Nota fechada \(no es decisión nueva\) — 2026-11-22: cuestiones residuales de D-3 y D-5 y pregunta R-1\n(.*)',reg,re.S)
okreg=bool(reg_n) and not c_r1_faltantes(reg_n.group(1)) and 'D5.a–d' in reg_n.group(1)
print('## R4 el registro autoritativo contiene la nota con las seis cuestiones y la protección de D5.a–d: %s'%okreg)
if not okreg: res['ERROR_REAL'].append(('R4_registro_sin_nota_de_cuestiones_residuales','entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md',0,'',''))
t06=txt[FM+'/06_MODELO_DATOS_CCI.md']
ok06=c_doc06_marcado(t06)
idx00=txt[EV+'/00_INDICE_VIGENTES_E_HISTORICOS.md']; idx16=txt[FM+'/16_INDICE_EVIDENCIAS_FASE0.md']
r00=[l for l in idx00.split('\n') if '06_MODELO_DATOS_CCI.md' in l and l.startswith('|')]
r16=[l for l in idx16.split('\n') if '06_MODELO_DATOS_CCI.md' in l and l.startswith('|')]
okidx=bool(r00) and all(re.search(r'hist[óo]rica',l,re.I) and re.search(r'no es (un )?esquema de datos aprobado',l,re.I) for l in r00+r16) and bool(r16)
print('## D4 06_MODELO_DATOS_CCI.md marcado como propuesta histórica no aprobada: %s; índices 00 y 16 lo clasifican igual: %s'%(ok06,okidx))
if not ok06: res['ERROR_REAL'].append(('D4_doc06_sin_marca_historica_o_afirma_esquema_definitivo','entregables_formales/06_MODELO_DATOS_CCI.md',0,'',''))
if not okidx: res['ERROR_REAL'].append(('D4_indices_clasifican_mal_el_doc06','00_INDICE_VIGENTES_E_HISTORICOS.md / 16_INDICE_EVIDENCIAS_FASE0.md',0,'',''))
print('## RESUMEN de hallazgos por clase')
for k,v in res.items(): print('   %-26s %d'%(k,len(v)))
for k in ('ERROR_REAL','REVISION_HUMANA','FALSO_POSITIVO_REVISADO'):
    for x in res[k][:80]: print('   [%s] %s | %s:%s | %s %s'%(k,x[0],x[1],x[2],x[3],('| '+x[4]) if x[4] else ''))
print('## ANTECEDENTE_ADVERTIDO (detalle por control)')
from collections import Counter
for c,n in sorted(Counter(x[0] for x in res['ANTECEDENTE_ADVERTIDO']).items()): print('   %-60s %d'%(c,n))
print('## Alcance: %d archivos .md/.txt revisados; %d clasificados vigentes/propuesta (S1–S9, frase a frase); %d no históricos (S10–S14)'%(len(files),len(VIG),len(VIG2)))
sys.exit(1 if res['ERROR_REAL'] or fall else 0)
