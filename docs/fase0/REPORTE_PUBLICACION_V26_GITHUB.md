# REPORTE DE PUBLICACIÓN V26 EN GITHUB

- **Repositorio:** `appalex47-lab/Copy-Creative-Intelligence` · **Rama creada:** `audit/fase0-v26-review` (nueva; sin force push, sin PR, sin merge).
- **Base:** `audit/fase0-v25-review`, HEAD `c3adaf97588ce3b8fef075a44aff6336f4e8c266` (commit del expediente V25 `f235768135175ce3fcd9405a3a4d3a3a68311d3e`).
- **Commit del expediente V26:** `2366ee1f4f57b0389bc7baac55e57d3290c6fe69` (padre único `c3adaf97…`; 313 archivos añadidos, todos en `docs/fase0/expediente_final_v26/`). El commit de este reporte es el HEAD de la rama (un archivo no puede contener el SHA de su propio commit); su verificación se informa en la respuesta de entrega.
- **SHA-256 de `MANIFIESTO_SHA256_V26.txt`:** `1516112bcaae3a1b86dd533d54e0a77087e11d4be8c7e90c6c74dc2fe1d7da20` (312 entradas = todos los archivos del expediente salvo él mismo, por autorreferencia).
- **SHA de referencia sin cambios:** `main` `6a1af2424ef39e0960b8f7e09d4e19ec52e6f046`; V20 `ac84133b776cc73c0cb3416e51e2767039bb5132`; V23 `8674114c69881ff1ebda3c5db1f89f2a4d6d31c6`; V24 `b88bde038e331ba67899632ca4e09eebf2cde82d`; V25 `c3adaf97588ce3b8fef075a44aff6336f4e8c266`.
- **Cifras de conciliación del expediente (idénticas a las de sus documentos):** 94 controles únicos y 238 ejecuciones; controles PASS 85, FAIL 0, BLOCKED 0, NOT VERIFIED 5, PARTIAL 4; ejecuciones PASS 236, FAIL 1, BLOCKED 0, NOT VERIFIED 0, PARTIAL 1. La única ejecución FAIL es RV07 corrida 1 (defecto del propio script, corregido en la corrida 2).

## Etapas
A. Validación previa al manifiesto: S01–S18, 18/18 PASS (`expediente_final_v26/REPORTE_VALIDACION_V26.md`).
B. Manifiesto: `MANIFIESTO_SHA256_V26.txt`.
C. Validación posterior al manifiesto: S01–S18 repetidos + S19 + S20 = 20/20 PASS (abajo y en `evidencia_publicacion_V26/`).
D. Publicación: commit `2366ee1f…` y este reporte.
E. Verificación remota posterior al push: PV01–PV11 (abajo y en `evidencia_publicacion_V26/`).

## C. Salida real de la pasada posterior al manifiesto
```
PASS | S01 Copia íntegra de V25: los 275 archivos de V25_copia_integra y el reporte de publicación V25 son idénticos byte a byte a los de la rama V25 (commits f235768 y c3adaf9) | archivos=275 distintos=[] publicación V25 idéntica=True
PASS | S02 Manifiestos históricos dentro de la copia: V25 verifica 274/274 (hashlib y sha256sum -c); SHA256SUMS interno 252/252; el manifiesto V24 falla exactamente en los 3 archivos con nota V25 (esperado) | V25 hashlib=True sha256sum OK=274; SHA256SUMS interno OK=252; manifiesto V24 fallos=['INFORME_CORRECCIONES_V24.md', 'MATRIZ_OBSERVACIONES_V23_V24.md', 'REPORTE_VALIDACION_V24.md']
PASS | S03 Rutas únicas (sin distinguir mayúsculas) y no inseguras (absolutas, con .., con \, con espacios en los bordes) en todo el expediente V26 | archivos=313
PASS | S04 MATRIZ_CONTROLES_V26.csv: columnas obligatorias, IDs únicos, estados permitidos y campos obligatorios no vacíos | filas=94 vacíos=[]
PASS | S05 Toda evidencia citada en la matriz existe dentro del expediente (salvo S19–S20, cuya salida se publica fuera, y los controles L sin ejecución) | filas=94 sin evidencia existente=[]
PASS | S06 EJECUCIONES_CONTROLES_V26.csv coincide con las salidas crudas archivadas (línea y resultado), cada PASS tiene una ejecución PASS y el estado de la matriz es el de la última ejecución | ejecuciones=238 errores=[]
PASS | S07 Cifras de conciliación (controles únicos, ejecuciones, estados) idénticas en la matriz, el informe de conciliación, el reporte de validación, el LEEME y el informe de auditoría | cifras={'Total de controles únicos': 94, 'Total de ejecuciones': 238, 'Controles PASS': 85, 'Controles FAIL': 0, 'Controles BLOCKED': 0, 'Controles NOT VERIFIED': 5, 'Controles PARTIAL': 4}; discrepancias=[]
PASS | S08 Referencias a archivos en los documentos V26 existen; MAPA_REFERENCIAS_V26.csv regenerado coincide con el archivado y no tiene NO_RESUELTA | referencias V26 rotas=[]; mapa regenerado idéntico y sin NO_RESUELTA=True
PASS | S09 Los SHA de commit citados en los documentos V26 existen en el repositorio y corresponden al rol declarado | SHA citados (commits y el árbol expediente_v23 de la salida R05) verificados contra el repositorio; discrepancias=[]
PASS | S10 Bloques embebidos = salidas crudas: V25 (pasada A, pasada C, bloque E) y V26 (pasada A, verificación remota) | bloques embebidos comparados con las salidas crudas; discrepancias=[]
PASS | S11 Limitaciones técnicas y decisiones pendientes del propietario conservadas explícitamente en LEEME_V26 e INFORME_AUDITORIA_FINAL_V26 | faltan=[]
PASS | S12 LEEME_V26 explica V21, V22/V23, V24, V25 y V26, el estado histórico frente al de publicación, la exclusión del manifiesto, y que V26 no es aceptación formal de Fase 0 ni autoriza Fase 1 ni Supabase | faltan=[]
PASS | S13 Las salidas técnicas históricas contienen las líneas-resumen declaradas (59/59, 28/28, 300/300, 22 funciones, 63/63, 14/14, 46/46, 26/26, integridad, 8 de 9) y las limitaciones L01–L08 constan en el documento de estados | líneas-resumen y limitaciones verificadas; faltan=[]
PASS | S14 Sin controles duplicados: (versión de origen, objetivo) únicos; ninguna ejecución se cuenta como control; cada ejecución apunta a un control existente | controles=94 ejecuciones=238
PASS | S15 Alcance Git: respecto a la base c3adaf9 solo hay archivos nuevos bajo docs/fase0/expediente_final_v26/; ninguna modificación ni borrado; nada en herramientas/ ni historico/ | entradas en git status=313 fuera de alcance=[]
PASS | S16 Historia intacta: refs remotas y locales de main, V20, V23, V24 y V25 iguales a las esperadas; la rama de trabajo parte de c3adaf9 | main, V20, V23, V24 y V25 verificados en remoto y local; discrepancias=[]
PASS | S17 Limitaciones visibles en la matriz: L01–L08 y HT10 con estado PARTIAL/NOT VERIFIED; ningún FAIL ni BLOCKED oculto; la ejecución FAIL de RV07 (corrida 1) figura en ejecuciones | PARTIAL=4 NOT VERIFIED=5 ejecución FAIL de RV07=1
PASS | S18 Documentos de entrega V26 presentes (LEEME, informe de auditoría, conciliación, matrices, cambios, validación, verificación remota, mapa, evidencia) y el LEEME declara la exclusión del propio manifiesto | faltan=[]; declarados sin existir=[]; existentes sin declarar=[]
PASS | S19 (posterior al manifiesto) MANIFIESTO_SHA256_V26.txt cubre exactamente todos los archivos salvo él mismo y todos los hashes coinciden (hashlib) | archivos=312 coincidencias=312
PASS | S20 (posterior al manifiesto) sha256sum -c MANIFIESTO_SHA256_V26.txt desde expediente_final_v26/ (método independiente) | OK=312
RESUMEN V26: 20 controles, 20 PASS, 0 FAIL
```

## E. Salida real de la verificación remota del commit del expediente V26 (PV01–PV11)
```
# Verificación remota posterior al push del commit del expediente V26 (2026-11-21T00:09:31Z); repositorio appalex47-lab/Copy-Creative-Intelligence; rama audit/fase0-v26-review
PV01 rama V26: ls-remote=2366ee1f4f57b0389bc7baac55e57d3290c6fe69 REST=2366ee1f4f57b0389bc7baac55e57d3290c6fe69 esperado=2366ee1f4f57b0389bc7baac55e57d3290c6fe69
PV02 padre del commit del expediente V26: c3adaf97588ce3b8fef075a44aff6336f4e8c266 (esperado c3adaf97588ce3b8fef075a44aff6336f4e8c266); nº de padres=1
PV03 árbol remoto = árbol local: SI (1230 blobs; truncado=false); archivos bajo docs/fase0/expediente_final_v26/ en GitHub=313
PV04 manifiesto remoto idéntico al local: SI; entradas=312; existen en el árbol remoto: 312; sha256 del manifiesto remoto=1516112bcaae3a1b86dd533d54e0a77087e11d4be8c7e90c6c74dc2fe1d7da20
PV05 archivos descargados de GitHub y comparados con el manifiesto V26: 312 OK, 0 discrepancias
PV06 diferencia de árboles remotos HEAD V25 -> commit V26 (la API de commits de GitHub limita a 300 archivos por commit y este commit tiene 313 files changed, 118160 insertions(+); por eso se compara por árboles): añadidos=313; eliminados o modificados=0; añadidos fuera de docs/fase0/expediente_final_v26/=0
PV07 SHA remotos: main=6a1af2424ef39e0960b8f7e09d4e19ec52e6f046 V20=ac84133b776cc73c0cb3416e51e2767039bb5132 V23=8674114c69881ff1ebda3c5db1f89f2a4d6d31c6 V24=b88bde038e331ba67899632ca4e09eebf2cde82d V25=c3adaf97588ce3b8fef075a44aff6336f4e8c266
PV08 PRs (todos los estados)=0; V26 respecto a V25: ahead ahead_by=1 behind_by=0; V26 respecto a main: ahead ahead_by=9 behind_by=0
PV09 funcional/infra: rutas añadidas por V26 en docs/fase0/(herramientas|historico)/ o fuera de docs/fase0/=0 + 0; árbol de herramientas V26 vs V25: 82c39ae9 vs 82c39ae9
PV10 archivos clave accesibles (bytes): LEEME_V26.md=5330 INFORME_AUDITORIA_FINAL_V26.md=14972 INFORME_CONCILIACION_CONTROLES_V26.md=5464 MATRIZ_CONTROLES_V26.csv=46886 MATRIZ_CAMBIOS_V25_V26.md=5849 REPORTE_VALIDACION_V26.md=6535 REPORTE_VERIFICACION_REMOTA_V26.md=7272 MANIFIESTO_SHA256_V26.txt=51078 
PV11 matriz y ejecuciones remotas recontadas: controles=94 ejecuciones=238 PASS=85 FAIL=0 BLOCKED=0 NOT VERIFIED=5 PARTIAL=4; ejecuciones PASS=236 FAIL=1 PARTIAL=1; tabla del LEEME remoto coincide=True
```

Nota de transparencia: la primera ejecución de PV06 contaba los archivos con la API de commits de GitHub y dio 300 (la API limita `files` a 300 por commit; el commit tiene 313). Se sustituyó por la comparación de árboles remotos (añadidos=313, eliminados o modificados=0) y se volvieron a ejecutar PV01–PV11; la salida de arriba es la de esa segunda ejecución. La primera salida no se archivó.

## Resultado
PV01 a PV11 PASS. RV07 (verificación de V25 pendiente en V25) quedó resuelta dentro del expediente: PASS 7/7 en la corrida 2 (corrida 1 FAIL por defecto del script, archivada). Resultados de R01–R08 y RV01–RV11 en `expediente_final_v26/REPORTE_VERIFICACION_REMOTA_V26.md`.

## Limitaciones y pendientes (sin cambio)
Se conservan las de `expediente_final_v26/LEEME_V26.md`: 12 escenarios PARCIAL; T-409 a T-422 sin ejecución individual; 22 funciones validadas indirectamente; PostgreSQL temporal (63/63 y 14/14) ≠ esquema aprobado; sin validación física en CCI-DEV, ni de RLS, privilegios o concurrencia; R1–R9 no ejecutado; HV-02 / PO-05 sin verificación; decisiones del propietario abiertas (PO-05, G-1, G-5, G-10, DG-19, DG-20, DG-09, DG-12, DG-16, DG-18, DEP-RET-01, G-9, RP-01, P-01 a P-05, P-10 y OD-13).

## Confirmaciones
Sin merge, sin PR, sin force push; `main`, V20, V23, V24 y V25 sin modificar; sin cambios en código funcional, Supabase, CCI-DEV ni CCI-PROD; Fase 1 no iniciada. **V26 no constituye aceptación formal de Fase 0**, que corresponde exclusivamente al propietario.
