import os, hashlib, subprocess, re, sys
W="/tmp/pub/wt24"; V4=W+"/docs/fase0/expediente_final_v24"; V3=W+"/docs/fase0/expediente_final_v23"; res=[]
def ok(n,c,d=""): res.append(c); print(("PASS" if c else "FAIL"),"|",n,"|",d)
sh=lambda p: hashlib.sha256(open(p,"rb").read()).hexdigest()
rd=lambda p: open(p,encoding="utf-8").read()
inv=dict((l.rstrip("\n").split("  ",1)[1],l.split("  ")[0]) for l in open("/tmp/pub/inv_v23_antes.txt"))
cur=lambda R: {os.path.relpath(os.path.join(a,f),R):sh(os.path.join(a,f)) for a,_,x in os.walk(R) for f in x}
v3=cur(V3); v4=cur(V4)
ok("V23 en el árbol de trabajo idéntico al inventario previo (253 archivos)", v3==inv and len(v3)==253)
ok("V23 sin cambios respecto al commit 8674114 (git)", subprocess.run(["git","status","--porcelain","--","docs/fase0/expediente_final_v23","docs/fase0/entregas","docs/fase0/VALIDACION_ZIP_V23.md","docs/fase0/REPORTE_PUBLICACION_V23_GITHUB.md"],cwd=W,capture_output=True,text=True).stdout=="")
base={k:v for k,v in v4.items() if k in inv}
chg=sorted(k for k in inv if v4.get(k)!=inv[k]); new=sorted(set(v4)-set(inv))
ok("V24 conserva los 253 archivos de V23", all(k in v4 for k in inv))
MOD=["00_LEEME/LEEME_EXPEDIENTE_V21.md","08_INTEGRIDAD_Y_MANIFIESTOS/SHA256SUMS.txt"]
ok("Solo difieren de V23 el LEEME y SHA256SUMS interno (los otros 251 conservan su SHA-256)", chg==MOD, "modificados=%s"%chg)
EXTRA={"INFORME_CORRECCIONES_V24.md","MATRIZ_OBSERVACIONES_V23_V24.md","REPORTE_VALIDACION_V24.md","MANIFIESTO_SHA256_V24.txt"}
ok("Archivos nuevos en V24 limitados a los 4 autorizados (los presentes)", set(new)<=EXTRA, "nuevos=%s"%new)
ev=[k for k in inv if k.startswith(("03_SCRIPTS","04_RESULTADOS","05_LOGS","02_MATRICES","06_DIFF"))]
ok("Evidencias técnicas, scripts, resultados, matrices y diff sin alteración", all(v4[k]==inv[k] for k in ev), "%d archivos"%len(ev))
L=rd(V4+"/00_LEEME/LEEME_EXPEDIENTE_V21.md")
ok("OBS-01: versión del expediente V21 / corrección V23 / revisión V24 distinguidas; sin «(empaquetado V22)» como versión", "Versión del expediente: V21.**" in L and "Corrección documental del paquete: V23.**" in L and "Revisión documental actual: V24.**" in L and "Versión: **V21** (empaquetado V22)" not in L)
s3=L.split("## 3. Origen exacto")[1].split("## 4.")[0]
ok("OBS-02 §3: declaración histórica conservada + aclaración", "NO está comprometido ni publicado" in s3 and "no describen el estado actual" in s3 and "audit/fase0-v23-review" in s3 and "no representa aceptación formal" in s3 and "No hubo merge ni modificación de `main`" in s3)
s15=L.split("## 15. Declaración")[1]
ok("OBS-02 §15: declaración histórica conservada + aclaración", "no se hizo commit, push, merge ni PR" in s15 and "Registro histórico" in s15 and "audit/fase0-v23-review" in s15 and "no es aceptación formal" in s15 and "sin merge" in s15)
s13=L.split("## 13. Limitaciones")[1].split("## 14.")[0]
need=["63/63 pruebas y 14/14 mutaciones","según la evidencia existente","12 escenarios permanecen PARCIAL","T-409 a T-422 no tienen ejecución individual propia","indirectamente por ejecución","no mediante lectura línea por línea","No se ha demostrado validación física en CCI-DEV","RLS, privilegios, concurrencia real","esquema físico aprobado","HV-02 / PO-05 continúa sin verificación"]
f=[k for k in need if k not in s13]; ok("OBS-03: limitaciones explícitas en LEEME §13", not f, "faltan=%s"%f)
doc=rd(V4+"/07_LIMITACIONES_Y_DECISIONES_PENDIENTES/00_ESTADOS_DE_VERIFICACION_Y_LIMITACIONES.md")+rd(V4+"/01_DOCUMENTOS_PRINCIPALES/INFORME_FINAL_V21.md")
f=[k for k in ["63/63","14/14","PARCIAL","T-409","línea a línea","CCI-DEV","RLS","privilegios","concurrencia","R1","HV-02","NO VERIFICABLE"] if k not in doc]; ok("OBS-03: documentos de limitaciones V23 (sin modificar) ya contienen cada limitación", not f, "faltan=%s"%f)
f=[k for k in ["T-03","T-06","T-10","T-47","T-78","T-80","T-124","T-137","T-138","T-139","T-140","T-166"] if k not in doc]; ok("12 escenarios PARCIAL listados", not f)
dd=rd(V4+"/01_DOCUMENTOS_PRINCIPALES/REGISTRO_DECISIONES_ABIERTAS_V21.md")+L
f=[k for k in ["PO-05","G-1","G-5","G-10","DG-19","DG-20","DG-09","DG-12","DG-16","DG-18","DEP-RET-01","G-9","RP-01","P-01","P-05","P-10","OD-13"] if k not in dd]; ok("Decisiones pendientes del propietario conservadas", not f, "faltan=%s"%f)
ok("Resultados 46/46 (x2), 26/26, 59/59, 300/300, 63/63, 14/14 intactos", rd(V4+"/04_RESULTADOS_DE_PRUEBAS/V21/salida_bateria_V21_corrida1.txt").count("PASS=46 FAIL=0")==1 and "DETECTADOS=26" in rd(V4+"/04_RESULTADOS_DE_PRUEBAS/V21/salida_controles_negativos_V21.txt") and "59 aprueban, 0 fallan" in rd(V4+"/04_RESULTADOS_DE_PRUEBAS/V21/salida_verificador_V21_corrida1.txt") and "300 detectadas" in rd(V4+"/04_RESULTADOS_DE_PRUEBAS/V21/salida_verificador_V21_corrida2.txt") and "TOTAL pruebas=63 PASS=63" in rd(V4+"/04_RESULTADOS_DE_PRUEBAS/V21/salida_PE_V21_corrida3.txt") and "DETECTADAS=14" in rd(V4+"/04_RESULTADOS_DE_PRUEBAS/V21/salida_PE_V21_mutaciones_corrida2.txt"))
r=subprocess.run("sha256sum -c --quiet 08_INTEGRIDAD_Y_MANIFIESTOS/SHA256SUMS.txt",shell=True,cwd=V4,capture_output=True,text=True)
ok("SHA256SUMS.txt interno regenerado y válido (no incluye su propio hash)", r.returncode==0 and "SHA256SUMS" not in rd(V4+"/08_INTEGRIDAD_Y_MANIFIESTOS/SHA256SUMS.txt") and len(rd(V4+"/08_INTEGRIDAD_Y_MANIFIESTOS/SHA256SUMS.txt").strip().split("\n"))==252)
fuera=subprocess.run("git status --porcelain -uall | grep -v ' docs/fase0/'",shell=True,cwd=W,capture_output=True,text=True).stdout.strip()
ok("Sin cambios fuera de docs/fase0/ y ninguno en herramientas/ o historico/ reales", fuera=="" and subprocess.run("git status --porcelain -uall | grep -E 'docs/fase0/(herramientas|historico)/'",shell=True,cwd=W,capture_output=True,text=True).stdout=="")
if os.path.exists(V4+"/MANIFIESTO_SHA256_V24.txt"):
    m=[l.rstrip("\n").split("  ",1) for l in open(V4+"/MANIFIESTO_SHA256_V24.txt",encoding="utf-8")]; cu=cur(V4); cu.pop("MANIFIESTO_SHA256_V24.txt")
    ok("MANIFIESTO_SHA256_V24 cubre exactamente todos los archivos de V24 (salvo él mismo) y todos los hashes coinciden", {p:h for h,p in m}==cu and len(m)==len(set(p for _,p in m)), "archivos=%d coinciden=%d"%(len(m),sum(1 for h,p in m if cu.get(p)==h)))
    r=subprocess.run("sha256sum -c --quiet MANIFIESTO_SHA256_V24.txt",shell=True,cwd=V4,capture_output=True,text=True); ok("sha256sum -c MANIFIESTO_SHA256_V24.txt desde expediente_final_v24/", r.returncode==0)
n=len(res); fl=res.count(False); print("RESUMEN V24: %d controles, %d PASS, %d FAIL"%(n,n-fl,fl)); sys.exit(1 if fl else 0)
