# REPORTE DE PUBLICACIÓN V25 EN GITHUB

- **Repositorio:** `appalex47-lab/Copy-Creative-Intelligence` · **Rama creada:** `audit/fase0-v25-review` (nueva; sin force push)
- **Origen:** commit `b88bde038e331ba67899632ca4e09eebf2cde82d` (final de V24).
- **Commit del expediente V25:** `f235768135175ce3fcd9405a3a4d3a3a68311d3e` (padre único `b88bde03…`; 275 archivos añadidos, todos en `docs/fase0/expediente_final_v25/`). El commit de este reporte es el HEAD de la rama (un archivo no puede contener el SHA de su propio commit).
- **SHA de referencia:** V20 `ac84133b776cc73c0cb3416e51e2767039bb5132`; V23 `8674114c69881ff1ebda3c5db1f89f2a4d6d31c6`; V24 `b88bde038e331ba67899632ca4e09eebf2cde82d` (commit del expediente V24 `a1dfedb867a79386fd165cbb6fc2859057658705`); `main` inicial y final `6a1af2424ef39e0960b8f7e09d4e19ec52e6f046`.
- **Cifra consolidada de controles:** V24 = 18 controles de validación documental distintos (todos PASS; ver `expediente_final_v25/INFORME_CONCILIACION_CONTROLES_V25.md`). V25 = 16 controles de validación (P01–P14 + Q01–Q02) y 11 verificaciones remotas (RV01–RV11).

## Etapas (V25)
A. Validación previa al manifiesto: P01–P14, 14/14 PASS (en `REPORTE_VALIDACION_V25.md`).
B. Manifiesto: `MANIFIESTO_SHA256_V25.txt`, 274 entradas = todos los archivos de V25 salvo él mismo (exclusión por autorreferencia).
C. Validación posterior al manifiesto: P01–P14 repetidos + Q01 y Q02 = 16/16 PASS (abajo).
D. Publicación: commit `f2357681…` y este reporte.
E. Verificación remota: RV01–RV11 (abajo).

## C. Salida real de la pasada posterior al manifiesto
```
PASS | P01 Faltantes: ningún archivo de V24 ausente en V25 | archivos V24=258 ausentes=[]
PASS | P02 Adicionales: los archivos nuevos son exactamente los 17 declarados en MATRIZ_CAMBIOS | nuevos=17 adicionales=[] sin_crear=[]
PASS | P03 Rutas duplicadas (sin distinguir mayúsculas) o inseguras (absolutas, con .., con \) | archivos=275
PASS | P04 Matriz de hashes V24→V25: idénticos/modificados/nuevos/ausentes | idénticos=254 modificados=4 nuevos=17 ausentes=0
PASS | P05 Los 4 modificados son solo inserciones: quitando la nota V25 se recupera el archivo V24 byte a byte | 
PASS | P06 Evidencias técnicas, scripts, resultados, matrices y diff de V24 sin alteración | 234 archivos
PASS | P07 Históricos V24 intactos; el manifiesto V24 falla exactamente en los 3 archivos con nota V25 (esperado) | fallos=['INFORME_CORRECCIONES_V24.md', 'MATRIZ_OBSERVACIONES_V23_V24.md', 'REPORTE_VALIDACION_V24.md']
PASS | P08 Cifra consolidada (18 controles distintos; 16 previa / 18 final; 8 remotos) presente y coherente en todos los documentos V25 | 
PASS | P09 Matriz de controles: 18 C + 8 R, estados válidos y cada PASS con evidencia existente | 
PASS | P10 Estados de la matriz = salidas crudas archivadas (pasada A: 16, pasada C: 18, re-ejecución V25: 18) | 
PASS | P11 Los bloques embebidos en los reportes V24 (A en validación, C en publicación) = salidas crudas archivadas | 
PASS | P12 Limitaciones y decisiones pendientes conservadas explícitamente | faltan=[]
PASS | P13 Alcance: nada fuera de docs/fase0/ ni en herramientas/ o historico/ reales | 
PASS | P14 LEEME_V25 explica V21 / V23 / V24 / V25 / no aceptación formal / no Fase 1 ni Supabase | 
PASS | Q01 MANIFIESTO_SHA256_V25 cubre exactamente todos los archivos (salvo él mismo) y todos los hashes coinciden (hashlib) | archivos=274 coincidencias=274
PASS | Q02 sha256sum -c MANIFIESTO_SHA256_V25.txt desde expediente_final_v25/ (método independiente) | OK=274
RESUMEN V25: 16 controles, 16 PASS, 0 FAIL
```

## E. Salida real de la verificación remota del commit del expediente (RV01–RV06, RV08–RV11)
```
# Verificación remota V25 del commit del expediente (2026-11-20T22:32:57Z)
RV01 rama v25 existe: ls-remote=f235768135175ce3fcd9405a3a4d3a3a68311d3e REST=f235768135175ce3fcd9405a3a4d3a3a68311d3e esperado=f235768135175ce3fcd9405a3a4d3a3a68311d3e
RV02 padre del commit inicial: b88bde038e331ba67899632ca4e09eebf2cde82d (esperado b88bde038e331ba67899632ca4e09eebf2cde82d); nº de padres=1
RV03 expediente publicado: archivos bajo docs/fase0/expediente_final_v25/ en GitHub=275; árbol remoto = local: SI (916 blobs); truncado=false
RV04 manifiesto remoto idéntico al local: SI; entradas=274; existen en el árbol remoto: 274
RV05 archivos descargados de GitHub y comparados con el manifiesto: 274 OK, 0 discrepancias
RV06 reporte de validación remoto vs matriz de controles remota: matriz C=18 R=8 PASS=26 de 26; informe remoto declara 26 PASS=True, 18 controles=True, 16/16 y 18/18=True; reporte de validación: pasada A con 14 PASS y resumen 14/14=True; cifra V25 «16 controles»=True
RV08 archivos del commit: 275; fuera de docs/fase0/expediente_final_v25/: 0; estados distintos de added: 0
RV09 SHA: V20=ac84133b776cc73c0cb3416e51e2767039bb5132 V23=8674114c69881ff1ebda3c5db1f89f2a4d6d31c6 V24=b88bde038e331ba67899632ca4e09eebf2cde82d main=6a1af2424ef39e0960b8f7e09d4e19ec52e6f046
RV10 PRs (todos los estados)=0; merge de v25 en main: ahead (ahead_by=7, behind_by=0)
RV11 funcional/infra: archivos en docs/fase0/(herramientas|historico)/ o fuera de docs/fase0 en el commit=0; árbol de herramientas V25=árbol V24: 82c39ae9 vs 82c39ae9
```
RV07 (el reporte de publicación coincide con el reporte de validación) solo puede comprobarse con este archivo ya publicado: se ejecuta tras el segundo commit y su resultado se informa en la respuesta de entrega, no aquí.

## Resultado de las verificaciones (resumen)
RV01 PASS · RV02 PASS (padre b88bde03) · RV03 PASS (275 archivos; árbol remoto = local, 916 blobs) · RV04 PASS (274 entradas, todas existen) · RV05 PASS (274 de 274 hashes coinciden) · RV06 PASS · RV08 PASS (0 archivos fuera de `docs/fase0/expediente_final_v25/`; todos añadidos) · RV09 PASS (V20, V23, V24 y `main` conservan su SHA) · RV10 PASS (0 PR; sin merge: la rama está 7 commits por delante de `main` y 0 por detrás) · RV11 PASS (sin cambios en herramientas/ ni fuera de `docs/fase0/`).

## Limitaciones
Las del expediente se conservan (ver `LEEME_V25.md` e `INFORME_CONCILIACION_CONTROLES_V25.md` §7): sin validación física en CCI-DEV; PostgreSQL temporal ≠ esquema aprobado (63/63 y 14/14 según la evidencia existente); 12 escenarios PARCIAL; T-409 a T-422 sin ejecución individual; 22 funciones validadas indirectamente; sin RLS, privilegios, concurrencia real ni esquema físico aprobado; R1–R9 no ejecutado; HV-02 / PO-05 sin verificación; decisiones del propietario abiertas.

## Confirmaciones
Sin merge, sin PR, sin force push; `main`, V20, V23 y V24 sin modificar; sin cambios en Supabase, CCI-DEV ni CCI-PROD; Fase 1 no iniciada. **V25 no constituye aceptación formal de Fase 0**, que corresponde exclusivamente al propietario.
