# Escaneo de patrones de contradicción (solo lectura). Uso: cd evidence/cci-fase0 && python3 logs/scan_contradicciones.py
import re,os,sys
pats={'8/18':r'(?<![\d,.])8\s*/\s*18|(?<![\d,.])(?<!Entidad )8 de 18','D4.d pendiente':r'D4\.d[^\n]{0,80}(pendiente|no aprobad)','Adaptación pend. D-4':r'Adaptaci[oó]n pendiente de D-4','Prevalece este aviso':r'Prevalece este aviso','cinco cuestiones':r'cinco cuestiones','Supabase/PostgreSQL/RLS':r'Supabase|PostgreSQL|\bRLS\b','multiusuario':r'multiusuario|multi-usuario','Fase 0 aceptada':r'Fase 0[^\n]{0,60}(aceptad|COMPLETADA)','Q-7 pendiente':r'Q-7[^\n]{0,60}(pendiente|aplazad)','P4.4 aplazado':r'P4\.4[^\n]{0,40}(aplazad|pendiente)','D5.a–d abiertas':r'D5\.a[–-]d[^\n]{0,60}(abiert|pendient)','Fase 1 autorizada':r'Fase 1[^\n]{0,40}autorizad'}
vig=re.compile(r'ESTADO VIGENTE|ANTECEDENTE|SUPERAD|superad|hist[oó]ric|Nota fechada|NOTA DE ACTUALIZACI|Actualizaci[oó]n posterior|advertencia',re.I)
# v2 (2026-11-22, regularización): el aviso de vigencia se evalúa a nivel de PÁRRAFO (no de archivo) y cada coincidencia se clasifica.
# Clases: ANTECEDENTE_ADVERTIDO (el párrafo lleva marca de antecedente/superado/histórico), REVISION_HUMANA (sin marca en el párrafo pero el archivo
# tiene aviso de vigencia en otra parte: puede ser una alerta válida o un falso positivo), ERROR_REAL_PROBABLE (sin ninguna marca en el archivo).
# Esta herramienta es un barrido de patrones; el control semántico a nivel de frase está en logs/verificacion_semantica_fase0.py.
NEGW=re.compile(r'\b(sin|no hay|no se|ni|descart|excluy|prohib|pre-?condici[oó]n|requiere|hasta que|cuando|tras)\b|/\s*$',re.I)
out=[]
for r,_,fs in os.walk('.'):
    for f in sorted(fs):
        if not f.endswith(('.md','.txt')) or 'auditoria_integral' in r or r.startswith('./logs'): continue
        p=os.path.join(r,f); t=open(p,encoding='utf-8',errors='replace').read()
        hv=bool(vig.search(t)); paras=re.split(r'\n\s*\n|\n(?=\|)|\n(?=#)',t)
        for k,pt in pats.items():
            n=0; adv=0
            for para in paras:
                m=0
                for mm in re.finditer(pt,para):
                    ctx=para[max(0,mm.start()-90):mm.start()]
                    if NEGW.search(ctx): continue   # frase de exclusión («sin …», «no hay …», «pre-condición») no es afirmación de vigencia
                    m+=1
                if m:
                    n+=m
                    if vig.search(para): adv+=m
            if n:
                cl='ANTECEDENTE_ADVERTIDO' if adv==n else ('REVISION_HUMANA' if hv else 'ERROR_REAL_PROBABLE')
                out.append((p,k,n,adv,cl))
for o in out: print('%-85s %-26s %4d  con_marca_en_parrafo=%-3d %s'%o)
from collections import Counter
print('RESUMEN:',dict(Counter(o[4] for o in out)))
