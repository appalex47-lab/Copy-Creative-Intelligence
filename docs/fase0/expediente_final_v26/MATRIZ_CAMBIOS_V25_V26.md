# MATRIZ DE CAMBIOS V25 → V26

**Fecha:** 2026-11-20 (fecha local, America/Mexico_City; las salidas remotas llevan su sello en UTC) · **Rama:** `audit/fase0-v26-review` · **Base:** `audit/fase0-v25-review`, HEAD de publicación `c3adaf97588ce3b8fef075a44aff6336f4e8c266` (commit del expediente V25 `f235768135175ce3fcd9405a3a4d3a3a68311d3e`).

**V26 no constituye aceptación formal de Fase 0** (corresponde exclusivamente al propietario), no autoriza Fase 1 (NO INICIADA) y no toca Supabase, CCI-DEV ni CCI-PROD.

## Resumen
- **Copia íntegra de V25:** los 275 archivos de `expediente_final_v25` están en `V25_copia_integra/` con el mismo contenido byte a byte (0 modificados, 0 ausentes, 0 añadidos dentro de esa carpeta). Su manifiesto V25 verifica 274/274 desde allí.
- **Copia del reporte de publicación V25** (fuera del expediente V25): `V25_publicacion/REPORTE_PUBLICACION_V25_GITHUB.md`, idéntico al HEAD de V25.
- **Documentos históricos con errata:** no se modifican. Las erratas están en el informe de auditoría: `V25_copia_integra/LEEME_V25.md` (D06: SHA256SUMS sí verifica 252/252) y `V25_publicacion/REPORTE_PUBLICACION_V25_GITHUB.md` (D02: resumen sin RV10/RV11 y RV07 pendiente).
- **Fuera de `docs/fase0/expediente_final_v26/`:** solo se añadirá `docs/fase0/REPORTE_PUBLICACION_V26_GITHUB.md` en un segundo commit. Nada más cambia en el repositorio.

## Nuevos en V26
| Archivo | Para qué |
|---|---|
| `LEEME_V26.md` | Relación entre versiones, estado histórico vs actual, integridad, limitaciones |
| `INFORME_AUDITORIA_FINAL_V26.md` | Auditoría, RV07, defectos D01–D13, revisión A–E |
| `INFORME_CONCILIACION_CONTROLES_V26.md` | Tabla de conciliación y reconciliación con cifras históricas |
| `MATRIZ_CONTROLES_V26.csv` | Matriz única: una fila por control (94) |
| `EJECUCIONES_CONTROLES_V26.csv` | Una fila por ejecución con salida cruda archivada (238) |
| `MATRIZ_CAMBIOS_V25_V26.md` | Este documento |
| `REPORTE_VALIDACION_V26.md` | Etapas de validación y salida de la pasada A |
| `REPORTE_VERIFICACION_REMOTA_V26.md` | Verificación remota previa a publicar (R01–R08, RV01–RV11, W01–W03) |
| `MAPA_REFERENCIAS_V26.csv` | Resolución de referencias a archivos de los documentos históricos |
| `MANIFIESTO_SHA256_V26.txt` | Manifiesto autónomo (todos los archivos salvo él mismo) |
| `V25_publicacion/REPORTE_PUBLICACION_V25_GITHUB.md` | Copia del reporte de publicación V25 |

## Evidencia nueva (`evidencia_reconstruccion_V26/`)
| Archivo | Naturaleza |
|---|---|
| `evidencia_reconstruccion_V26/comparacion_arbol_V25_remoto_vs_local.txt` | script de verificación remota |
| `evidencia_reconstruccion_V26/historico_V25_no_archivado/remoto25_script_original.sh` | restos de V25 recuperados del directorio de trabajo (no estaban en la rama V25) |
| `evidencia_reconstruccion_V26/historico_V25_no_archivado/remoto_RV_V25_salida_original_sin_RV07.txt` | restos de V25 recuperados del directorio de trabajo (no estaban en la rama V25) |
| `evidencia_reconstruccion_V26/historico_V25_no_archivado/restos_RV07_V25_reporte_publicacion_descargado_16-35.md` | restos de V25 recuperados del directorio de trabajo (no estaban en la rama V25) |
| `evidencia_reconstruccion_V26/historico_V25_no_archivado/restos_RV07_V25_reporte_validacion_descargado_16-35.md` | restos de V25 recuperados del directorio de trabajo (no estaban en la rama V25) |
| `evidencia_reconstruccion_V26/historico_V25_no_archivado/val25_pasada_A2_intermedia_no_archivada_en_V25.txt` | restos de V25 recuperados del directorio de trabajo (no estaban en la rama V25) |
| `evidencia_reconstruccion_V26/historico_V25_no_archivado/val25_pasada_A_previa_manifiesto.txt` | restos de V25 recuperados del directorio de trabajo (no estaban en la rama V25) |
| `evidencia_reconstruccion_V26/historico_V25_no_archivado/val25_pasada_C_posterior_manifiesto.txt` | restos de V25 recuperados del directorio de trabajo (no estaban en la rama V25) |
| `evidencia_reconstruccion_V26/inventario_arbol_HEAD_V25_blobs_git_remoto_GitHub.txt` | script de verificación remota |
| `evidencia_reconstruccion_V26/inventario_sha256_V25_copia_integra.txt` | inventario SHA-256 de la copia V25 |
| `evidencia_reconstruccion_V26/reejecucion_V26_R01_R08.txt` | salida cruda de una ejecución nueva V26 |
| `evidencia_reconstruccion_V26/reejecucion_V26_RV01_RV11_corrida1_RV07e_FAIL_por_defecto_del_script.txt` | salida cruda de una ejecución nueva V26 |
| `evidencia_reconstruccion_V26/reejecucion_V26_RV01_RV11_corrida2.txt` | salida cruda de una ejecución nueva V26 |
| `evidencia_reconstruccion_V26/reejecucion_V26_W01_W03_previo.txt` | salida cruda de una ejecución nueva V26 |
| `evidencia_reconstruccion_V26/reejecucion_V26_val24_sobre_V24.txt` | salida cruda de una ejecución nueva V26 |
| `evidencia_reconstruccion_V26/reejecucion_V26_val25_sobre_V25.txt` | salida cruda de una ejecución nueva V26 |
| `evidencia_reconstruccion_V26/remoto_R01_R08_reejecucion_V26.sh` | salida cruda de una ejecución nueva V26 |
| `evidencia_reconstruccion_V26/remoto_RV01_RV11_reejecucion_V26.sh` | salida cruda de una ejecución nueva V26 |
| `evidencia_reconstruccion_V26/remoto_W01_W03_previo_V26.sh` | script de verificación remota |
| `evidencia_reconstruccion_V26/rv07_comparar_reportes.py` | script RV07 |
| `evidencia_reconstruccion_V26/rv07_comparar_reportes_corrida1_con_defecto.py` | script RV07 |
| `evidencia_reconstruccion_V26/salida_val26_pasada_A_previa_manifiesto.txt` | salida cruda de la pasada A de V26 |
| `evidencia_reconstruccion_V26/v26_construir.py` | script V26 |
| `evidencia_reconstruccion_V26/v26_evaluar.py` | script V26 |
| `evidencia_reconstruccion_V26/v26_mapa_referencias.py` | script V26 |
| `evidencia_reconstruccion_V26/v26_registro.py` | script V26 |
| `evidencia_reconstruccion_V26/v26_validar.py` | script V26 |
