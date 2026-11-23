#!/usr/bin/env python3
"""Prueba de mutación del verificador semántico (segunda regularización, 2026-11-22).

Uso (desde la raíz del repositorio):  python3 -I evidence/cci-fase0/logs/prueba_mutacion_semantica.py
Para cada mutación copia el árbol `evidence/` a un directorio temporal, siembra UN defecto documental sintético,
ejecuta `verificacion_semantica_fase0.py` sobre la copia y comprueba que termina con código 1 y con el control esperado.
No modifica el árbol real. Son pruebas sintéticas de documentos: NO son pruebas de la aplicación.
"""
import os, re, shutil, subprocess, sys, tempfile
EV='evidence/cci-fase0/'
PQ='entregables_formales/PAQUETE_DECISION_APROBACIONES_0_1_A_0_7.md'
MUT=[
 ('M1_R1_omite_cuestion_4_D5 (identidad exacta del contenido)',PQ,lambda s: re.sub(r'\n\| 5 \| [^\n]*identidad exacta[^\n]*','',s),'R2_R1_incompleta_o_reabre_D5'),
 ('M2_R1_omite_D3_ubicacion_reglas_copy',PQ,lambda s: re.sub(r'\n\| 1 \| D-3 \|[^\n]*','',s),'R2_R1_incompleta_o_reabre_D5'),
 ('M3_D5ad_presentadas_como_pendientes_en_documento_vigente','entregables_formales/CONCILIACION_30_DECISIONES_Y_APLAZAMIENTOS.md',lambda s: s+'\n\nPendientes: D5.a–d siguen abiertas y bloquean D-4.\n','S10_D5ad_presentadas_como_pendientes_o_abiertas'),
 ('M4_R1_presentada_como_resuelta_en_informe','auditoria_integral/10_INFORME_EJECUTIVO_PREPARACION_CIERRE.md',lambda s: s+'\n\nR-1 queda resuelta por la ratificación.\n','S11_R1_presentada_como_resolucion'),
 ('M5_aprobaciones_0_1_0_7_extendidas_a_la_aceptacion_de_Fase_0','entregables_formales/APROBACIONES_FASE0.md',lambda s: s+'\n\nLas aprobaciones 0.1–0.7 implican la aceptación de Fase 0.\n','S4_aprobaciones_extendidas_a_lo_no_decidido'),
 ('M6_recomendacion_de_Claude_presentada_como_decision_del_propietario',PQ,lambda s: s+'\n\nEl propietario decidió aprobar la recomendación de Claude sobre R-1.\n','S12_recomendacion_presentada_como_decision'),
 ('M7_R1_reabre_D5c',PQ,lambda s: s+'\n\nR-1 incluye decidir D5.c (agrupación de las cuestiones 3 y 4).\n','S14_R1_vinculada_a_D5ad_sin_exclusion'),
 ('M8_doc_06_sin_marca_historica_y_afirmado_como_definitivo','entregables_formales/06_MODELO_DATOS_CCI.md',lambda s: s.replace('PROPUESTA HISTÓRICA','PROPUESTA VIGENTE').replace('no es un esquema de datos aprobado','es el esquema definitivo'),'D4_doc06_sin_marca_historica_o_afirma_esquema_definitivo'),
 ('M9_ficha_0_1_vuelve_a_PENDIENTE_pese_a_la_respuesta_del_propietario','entregables_formales/APROBACIONES_FASE0.md',lambda s: s.replace('| APROBADA (propietario, 2026-11-22 20:14) | «Apruebo 0.1 a 0.7 según las recomendaciones del paquete…» |','| PENDIENTE | — |',1),'A1_aprobaciones'),
 ('M10_Fase_1_marcada_como_autorizada_en_la_tabla','entregables_formales/APROBACIONES_FASE0.md',lambda s: s.replace('| — | — | PENDIENTE | — |\n| ','| — | — | PENDIENTE | — |\n| ',1) if False else re.sub(r'(\| Aparte \|[^\n]*)\| AUTORIZADA SOLO S1\.0 \([^|]*\| — \|',r'\1| APROBADA | — |',s,count=1,flags=re.M),'A1_aprobaciones'),
 ('M11_aprobacion_0_5_sin_limite_de_principios','entregables_formales/APROBACIONES_FASE0.md',lambda s: s+'\n\nLa ficha 0.5 está aprobada.\n','S4b_aprobacion_05_sin_limite_de_principios'),
 ('M12_documento_con_estado_previo_0_7_sin_la_nota_de_20_14','auditoria_integral/10_INFORME_EJECUTIVO_PREPARACION_CIERRE.md',lambda s: s.replace('2026-11-22 20:14','2026-11-22'),'S15_estado_previo_de_aprobaciones_sin_nota_20_14'),
 ('M13_registro_sin_la_respuesta_literal_del_propietario','entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md',lambda s: s.replace('R-1 sí.»','R-1 no.»',1),'A3_registro_sin_respuesta_del_propietario'),
 ('M14_fila_Final_vuelve_a_PENDIENTE_pese_a_la_aceptacion_del_propietario','entregables_formales/APROBACIONES_FASE0.md',lambda s: s.replace('| ACEPTADA (propietario, 2026-11-22 20:26) | «Acepto formalmente la Fase 0, con las limitaciones expresas C-2 y C-3 abiertas y los 10 aplazamientos pendientes. No autoriza la Fase 1.» |','| PENDIENTE | — |',1),'A1_aprobaciones'),
 ('M15_aceptacion_de_Fase_0_presentada_como_autorizacion_de_Fase_1','entregables_formales/APROBACIONES_FASE0.md',lambda s: s+'\n\nLa Fase 0 está aceptada, lo que autoriza la Fase 1.\n','S5b_aceptacion_de_fase_0_con_alcance_no_decidido'),
 ('M16_Fase_1_presentada_como_autorizada','entregables_formales/APROBACIONES_FASE0.md',lambda s: s+'\n\nCon esto la Fase 1 queda autorizada.\n','S5_fase_1_presentada_como_autorizada'),
 ('M17_documento_con_Fase_0_no_aceptada_sin_la_nota_de_20_26','auditoria_integral/10_INFORME_EJECUTIVO_PREPARACION_CIERRE.md',lambda s: s.replace('2026-11-22 20:26','2026-11-22'),'S16_estado_previo_de_la_aceptacion_sin_nota_20_26'),
 ('M18_registro_con_texto_literal_de_la_aceptacion_alterado','entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md',lambda s: s.replace('y los 10 aplazamientos pendientes. No autoriza la Fase 1.»','y los 10 aplazamientos pendientes.»',1),'A4_registro_sin_aceptacion_de_fase_0'),
 ('M19_aceptacion_de_Fase_0_presentada_como_cierre_de_C_2','entregables_formales/CONCILIACION_30_DECISIONES_Y_APLAZAMIENTOS.md',lambda s: s+'\n\nLa aceptación de la Fase 0 deja C-2 resuelta.\n','S5b_aceptacion_de_fase_0_con_alcance_no_decidido'),
 ('M20_documento_con_nota_20_26_sin_la_nota_20_59','entregables_formales/CONCILIACION_30_DECISIONES_Y_APLAZAMIENTOS.md',lambda s: s.replace('2026-11-22 20:59','2026-11-22 20:5X'),'S17_documento_con_nota_20_26_sin_la_nota_20_59'),
 ('M21_registro_con_texto_literal_de_la_autorizacion_alterado','entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md',lambda s: s.replace('y, solo tras mi aprobación expresa de sus resultados, las subfases S1.1','y las subfases S1.1',1),'A5_registro_sin_autorizacion_de_S1_0'),
 ('M22_S1_3_y_S1_4_presentadas_como_activas','README_ENTREGA.md',lambda s: s+'\n\nLas subfases S1.3 y S1.4 están autorizadas y activas.\n','S5c_S1_1_S1_2_o_Fase_1_completa_presentadas_como_autorizadas_o_activas'),
 ('M23_fila_Aparte_con_autorizacion_sin_limite_a_S1_0','entregables_formales/APROBACIONES_FASE0.md',lambda s: s.replace('AUTORIZADA SOLO S1.0 (propietario','AUTORIZADA (propietario',1),'A1_aprobaciones'),
 ('M24_delegacion_sin_aclarar_que_las_decisiones_son_de_Claude','entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md',lambda s: s.replace('no son decisiones personales del propietario','son decisiones del propietario',1),'A6_registro_sin_delegacion'),
]
def run(cwd):
    p=subprocess.run([sys.executable,'-I',EV+'logs/verificacion_semantica_fase0.py'],cwd=cwd,capture_output=True,text=True)
    return p.returncode,p.stdout+p.stderr
def main():
    root=os.getcwd(); assert os.path.isdir(os.path.join(root,'evidence/cci-fase0')),'ejecutar desde la raíz del repositorio'
    print('## Prueba de mutación del verificador semántico (19 defectos sintéticos; árbol real intacto)')
    with tempfile.TemporaryDirectory() as t:
        base=os.path.join(t,'base'); shutil.copytree(os.path.join(root,'evidence'),os.path.join(base,'evidence'))
        rc0,o0=run(base); print('## Control negativo (sin mutación): rc=%d (esperado 0)'%rc0)
        ok=rc0==0; det=0
        for name,path,fn,ctrl in MUT:
            w=os.path.join(t,'w'); shutil.rmtree(w,ignore_errors=True); shutil.copytree(os.path.join(base,'evidence'),os.path.join(w,'evidence'))
            f=os.path.join(w,EV,path); s=open(f,encoding='utf-8').read(); n=fn(s)
            if n==s: print('   [ERROR DE PRUEBA] la mutación no cambió el archivo:',name); ok=False; continue
            open(f,'w',encoding='utf-8').write(n)
            rc,o=run(w); hit=('[ERROR_REAL] '+ctrl) in o
            det+= 1 if (rc==1 and hit) else 0
            print('   [%s] %s -> rc=%d; control esperado %s %s'%('DETECTADA' if (rc==1 and hit) else 'NO DETECTADA',name,rc,ctrl,'(presente)' if hit else '(AUSENTE)'))
        print('## Resultado: %d/%d mutaciones detectadas; control sin mutación rc=%d'%(det,len(MUT),rc0))
        sys.exit(0 if (ok and det==len(MUT)) else 1)
main()
