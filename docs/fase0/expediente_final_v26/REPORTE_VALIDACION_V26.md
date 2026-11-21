# REPORTE DE VALIDACIÓN V26

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

| Etapa | Qué | Dónde se registra |
|---|---|---|
| 0. Auditoría y re-ejecuciones previas | Re-ejecución de `V25_copia_integra/evidencia_reconstruccion_V25/val24.py` sobre V24 (18/18) y de `V25_copia_integra/evidencia_reconstruccion_V25/val25.py` sobre V25 (16/16); verificaciones remotas | `REPORTE_VERIFICACION_REMOTA_V26.md` y `evidencia_reconstruccion_V26/` |
| A. Previa al manifiesto | S01–S18 (18 controles) | este reporte (salida real, abajo) |
| B. Manifiesto | `MANIFIESTO_SHA256_V26.txt` (todos los archivos salvo él mismo, por autorreferencia) | `MANIFIESTO_SHA256_V26.txt` |
| C. Posterior al manifiesto | S01–S18 repetidos + S19 (hashlib) + S20 (`sha256sum -c`) = 20 controles | `REPORTE_PUBLICACION_V26_GITHUB.md` (fuera del expediente) |
| D. Publicación y verificación remota | Commits en `audit/fase0-v26-review` y consulta a GitHub | `REPORTE_PUBLICACION_V26_GITHUB.md` |

La pasada A es un subconjunto de la pasada C: S01–S18 son 18 controles, no 36. En la matriz cada uno es un control; sus dos pasadas son dos ejecuciones. No se repiten las 46 pruebas V21, los 26 controles negativos ni PostgreSQL (no se modificaron; S01 prueba que sus resultados son idénticos a V25).

## Salida real de la pasada A (previa al manifiesto V26)
```
PASS | S01 Copia íntegra de V25: los 275 archivos de V25_copia_integra y el reporte de publicación V25 son idénticos byte a byte a los de la rama V25 (commits f235768 y c3adaf9) | archivos=275 distintos=[] publicación V25 idéntica=True
PASS | S02 Manifiestos históricos dentro de la copia: V25 verifica 274/274 (hashlib y sha256sum -c); SHA256SUMS interno 252/252; el manifiesto V24 falla exactamente en los 3 archivos con nota V25 (esperado) | V25 hashlib=True sha256sum OK=274; SHA256SUMS interno OK=252; manifiesto V24 fallos=['INFORME_CORRECCIONES_V24.md', 'MATRIZ_OBSERVACIONES_V23_V24.md', 'REPORTE_VALIDACION_V24.md']
PASS | S03 Rutas únicas (sin distinguir mayúsculas) y no inseguras (absolutas, con .., con \, con espacios en los bordes) en todo el expediente V26 | archivos=312
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
PASS | S15 Alcance Git: respecto a la base c3adaf9 solo hay archivos nuevos bajo docs/fase0/expediente_final_v26/; ninguna modificación ni borrado; nada en herramientas/ ni historico/ | entradas en git status=312 fuera de alcance=[]
PASS | S16 Historia intacta: refs remotas y locales de main, V20, V23, V24 y V25 iguales a las esperadas; la rama de trabajo parte de c3adaf9 | main, V20, V23, V24 y V25 verificados en remoto y local; discrepancias=[]
PASS | S17 Limitaciones visibles en la matriz: L01–L08 y HT10 con estado PARTIAL/NOT VERIFIED; ningún FAIL ni BLOCKED oculto; la ejecución FAIL de RV07 (corrida 1) figura en ejecuciones | PARTIAL=4 NOT VERIFIED=5 ejecución FAIL de RV07=1
PASS | S18 Documentos de entrega V26 presentes (LEEME, informe de auditoría, conciliación, matrices, cambios, validación, verificación remota, mapa, evidencia) y el LEEME declara la exclusión del propio manifiesto | faltan=[]; declarados sin existir=[]; existentes sin declarar=[]
RESUMEN V26: 18 controles, 18 PASS, 0 FAIL
```
