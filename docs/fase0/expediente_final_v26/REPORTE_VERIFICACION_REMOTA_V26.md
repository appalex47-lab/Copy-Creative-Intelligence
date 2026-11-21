# REPORTE DE VERIFICACIÓN REMOTA V26 (previa a la publicación)

**Fecha:** 2026-11-20 (fecha local, America/Mexico_City; las salidas remotas llevan su sello en UTC) · **Rama:** `audit/fase0-v26-review` · **Base:** `audit/fase0-v25-review`, HEAD de publicación `c3adaf97588ce3b8fef075a44aff6336f4e8c266` (commit del expediente V25 `f235768135175ce3fcd9405a3a4d3a3a68311d3e`).

**V26 no constituye aceptación formal de Fase 0** (corresponde exclusivamente al propietario), no autoriza Fase 1 (NO INICIADA) y no toca Supabase, CCI-DEV ni CCI-PROD.

<!-- CONCILIACION:INICIO -->
| Concepto | Valor |
|---|---|
| Total de controles únicos | 94 |
| Total de ejecuciones | 238 |
| Controles PASS | 85 |
| Controles FAIL | 0 |
| Controles BLOCKED | 0 |
| Controles NOT VERIFIED | 5 |
| Controles PARTIAL | 4 |
| Ejecuciones PASS | 236 |
| Ejecuciones FAIL | 1 |
| Ejecuciones BLOCKED | 0 |
| Ejecuciones NOT VERIFIED | 0 |
| Ejecuciones PARTIAL | 1 |
<!-- CONCILIACION:FIN -->

Alcance: verificaciones contra GitHub realizadas **antes** de publicar V26 (la rama aún no existía: W01). La verificación posterior al push se registra en `REPORTE_PUBLICACION_V26_GITHUB.md`, fuera de este expediente. Los comandos exactos están en `remoto_R01_R08_reejecucion_V26.sh`, `remoto_RV01_RV11_reejecucion_V26.sh` y `remoto_W01_W03_previo_V26.sh`; el criterio PASS/FAIL de cada línea lo aplica `v26_evaluar.py` y consta en `EJECUCIONES_CONTROLES_V26.csv` con su línea.

| Verificación | Ejecuciones | Resultado | Salida cruda |
|---|---|---|---|
| R01–R08 (V24) | V25 re-ejecución, V26 re-ejecución | 8/8 PASS en cada una; 256 de 256 archivos del manifiesto V24 coinciden | `reejecucion_V26_R01_R08.txt` |
| RV01–RV06, RV08–RV11 (V25) | V25 original, V26 corrida 1, V26 corrida 2 | PASS en las tres; 274 de 274 archivos del manifiesto V25 coinciden | `reejecucion_V26_RV01_RV11_corrida2.txt` |
| RV07 (V25) | V26 corrida 1, V26 corrida 2 | corrida 1: FAIL por defecto del script (RV07.e); corrida 2: 7/7 PASS | `reejecucion_V26_RV01_RV11_corrida1_RV07e_FAIL_por_defecto_del_script.txt` y `reejecucion_V26_RV01_RV11_corrida2.txt` |
| W01–W03 (V26) | una | PASS | `reejecucion_V26_W01_W03_previo.txt` |

RV01 se ejecuta en variante: la punta actual de la rama V25 es el HEAD de publicación c3adaf97 y el commit del expediente f2357681 es su padre. RV10 usa el commit del expediente (7 commits por delante de `main`).

## Salida real de R01–R08
```
# Re-ejecución V26 de las verificaciones remotas de V24 (R01-R08) (2026-11-20T23:56:12Z)
R01 rama v24 existe y apunta a b88bde038e331ba67899632ca4e09eebf2cde82d: PASS
R02 commit expediente V24: padre=8674114c69881ff1ebda3c5db1f89f2a4d6d31c6 archivos=257 fuera_de_expediente_v24=0
R03 árbol remoto de b88bde038e331ba67899632ca4e09eebf2cde82d = local: PASS (641 blobs; truncated=false)
R04 descargados de GitHub y comparados con MANIFIESTO V24: 256 OK, 0 discrepancias, entradas=256
R05 V23: rama=8674114c69881ff1ebda3c5db1f89f2a4d6d31c6 árbol expediente_v23 en V24=0824c738f14c313b5f25149016a4622fe85fdeef en V23=0824c738f14c313b5f25149016a4622fe85fdeef
R06 V20=ac84133b776cc73c0cb3416e51e2767039bb5132 main=6a1af2424ef39e0960b8f7e09d4e19ec52e6f046
R07 PRs=0
R08 accesibles: 8692 5155 1508 2832 39287  bytes; reporte publicación: 4864
```

## Salida real de RV01–RV11 (corrida 2, con RV07)
```
# Re-ejecución V26 (RV01-RV11) de la verificación remota de V25: commit del expediente f235768 y HEAD publicado c3adaf9 (2026-11-20T23:57:10Z)
RV01 (variante V26: la punta actual es el HEAD de publicación c3adaf97588ce3b8fef075a44aff6336f4e8c266; el commit del expediente f235768135175ce3fcd9405a3a4d3a3a68311d3e es su padre) rama v25: ls-remote=c3adaf97588ce3b8fef075a44aff6336f4e8c266 REST=c3adaf97588ce3b8fef075a44aff6336f4e8c266 padre_de_HEAD=f235768135175ce3fcd9405a3a4d3a3a68311d3e -> PASS
RV02 padre del commit inicial: b88bde038e331ba67899632ca4e09eebf2cde82d (esperado b88bde038e331ba67899632ca4e09eebf2cde82d); nº de padres=1
RV03 expediente publicado: archivos bajo docs/fase0/expediente_final_v25/ en GitHub=275; árbol remoto = local: SI (916 blobs); truncado=false
RV04 manifiesto remoto idéntico al local: SI; entradas=274; existen en el árbol remoto: 274
RV05 archivos descargados de GitHub y comparados con el manifiesto: 274 OK, 0 discrepancias
RV06 reporte de validación remoto vs matriz de controles remota: matriz C=18 R=8 PASS=26 de 26; informe remoto declara 26 PASS=True, 18 controles=True, 16/16 y 18/18=True; reporte de validación: pasada A con 14 PASS y resumen 14/14=True; cifra V25 «16 controles»=True
RV07 (ref consultada c3adaf97588ce3b8fef075a44aff6336f4e8c266, rama audit/fase0-v25-review; repositorio appalex47-lab/Copy-Creative-Intelligence; 2026-11-20T23:57:33Z)
PASS | RV07.a el reporte de publicación remoto es idéntico byte a byte al del commit HEAD local | sha256=aaf98181b7d1192d215414435a4148dcee80e3fde42c48467bcd6087db3eb9da
PASS | RV07.b ambos reportes declaran 16 controles de validación (P01–P14 + Q01–Q02) y 11 verificaciones remotas (RV01–RV11) | 
PASS | RV07.c el bloque de la pasada A del reporte de validación remoto = salida cruda de la pasada A | 
PASS | RV07.d el bloque C del reporte de publicación remoto = salida cruda de la pasada C | 
PASS | RV07.e el bloque E del reporte de publicación remoto = salida cruda original de RV01–RV06 y RV08–RV11 (sin RV07) | 
PASS | RV07.f el SHA del commit del expediente citado en el reporte de publicación es el del padre del HEAD | 
PASS | RV07.g las etapas A–E del reporte de validación remoto coinciden con las del reporte de publicación (A 14/14, C 16/16, E RV01–RV11) | 
INFO | RV07 observación (no criterio de PASS): el resumen de resultados del reporte de publicación lista ['RV01', 'RV02', 'RV03', 'RV04', 'RV05', 'RV06', 'RV08', 'RV09', 'RV10', 'RV11'] y omite RV10 y RV11, aunque sus salidas están en el bloque E; y declara RV07 pendiente de ejecución
RESUMEN RV07: 7 comprobaciones, 7 PASS, 0 FAIL
RV08 archivos del commit: 275; fuera de docs/fase0/expediente_final_v25/: 0; estados distintos de added: 0
RV09 SHA: V20=ac84133b776cc73c0cb3416e51e2767039bb5132 V23=8674114c69881ff1ebda3c5db1f89f2a4d6d31c6 V24=b88bde038e331ba67899632ca4e09eebf2cde82d main=6a1af2424ef39e0960b8f7e09d4e19ec52e6f046
RV10 PRs (todos los estados)=0; merge de v25 en main: ahead (ahead_by=7, behind_by=0)
RV11 funcional/infra: archivos en docs/fase0/(herramientas|historico)/ o fuera de docs/fase0 en el commit=0; árbol de herramientas V25=árbol V24: 82c39ae9 vs 82c39ae9
```

## Salida real de W01–W03
```
# Verificaciones remotas previas a la publicación de V26 (2026-11-20T23:57:51Z)
W01 la rama audit/fase0-v26-review NO existe en el remoto antes de publicar: ls-remote='' REST={"message":"Not Found","documentation_url":"https://docs.git
W02 referencias remotas: main=6a1af2424ef39e0960b8f7e09d4e19ec52e6f046 V20=ac84133b776cc73c0cb3416e51e2767039bb5132 V23=8674114c69881ff1ebda3c5db1f89f2a4d6d31c6 V24=b88bde038e331ba67899632ca4e09eebf2cde82d V25=c3adaf97588ce3b8fef075a44aff6336f4e8c266
W03 árbol remoto del HEAD V25 c3adaf97588ce3b8fef075a44aff6336f4e8c266 = árbol local de la base de V26: SI (917 blobs; truncado=false); HEAD local de wt26=c3adaf97588ce3b8fef075a44aff6336f4e8c266
```
