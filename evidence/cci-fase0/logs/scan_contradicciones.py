# Escaneo de patrones de contradicción (solo lectura). Uso: cd evidence/cci-fase0 && python3 logs/scan_contradicciones.py
import re,os,sys
pats={'8/18':r'8\s*/\s*18|8 de 18','D4.d pendiente':r'D4\.d[^\n]{0,80}(pendiente|no aprobad)','Adaptación pend. D-4':r'Adaptaci[oó]n pendiente de D-4','Prevalece este aviso':r'Prevalece este aviso','cinco cuestiones':r'cinco cuestiones','Supabase/PostgreSQL/RLS':r'Supabase|PostgreSQL|\bRLS\b','multiusuario':r'multiusuario|multi-usuario','Fase 0 aceptada':r'Fase 0[^\n]{0,60}(aceptad|COMPLETADA)','Q-7 pendiente':r'Q-7[^\n]{0,60}(pendiente|aplazad)','P4.4 aplazado':r'P4\.4[^\n]{0,40}(aplazad|pendiente)','D5.a–d abiertas':r'D5\.a[–-]d[^\n]{0,60}(abiert|pendient)','Fase 1 autorizada':r'Fase 1[^\n]{0,40}autorizad'}
vig=re.compile(r'ESTADO VIGENTE|ANTECEDENTE|SUPERAD|superad|hist[oó]ric|Nota fechada|NOTA DE ACTUALIZACI|Actualizaci[oó]n posterior|advertencia',re.I)
out=[]
for r,_,fs in os.walk('.'):
    for f in sorted(fs):
        if not f.endswith(('.md','.txt')) or 'auditoria_integral' in r or r.startswith('./logs'): continue
        p=os.path.join(r,f); t=open(p,encoding='utf-8',errors='replace').read()
        hv=bool(vig.search(t))
        for k,pt in pats.items():
            n=len(re.findall(pt,t))
            if n: out.append((p,k,n,hv))
for o in out: print('%-85s %-26s %4d  aviso_vigencia=%s'%o)
