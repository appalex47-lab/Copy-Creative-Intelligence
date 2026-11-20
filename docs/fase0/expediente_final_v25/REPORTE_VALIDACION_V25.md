# REPORTE DE VALIDACIÓN V25

Validación de la conciliación documental V25 (2026-11-20). **Cifra consolidada de controles de V25: 16 controles de validación distintos (P01–P14 y Q01–Q02) y 11 verificaciones remotas (RV01–RV11) aparte.** Se ejecutan en etapas:

| Etapa | Qué | Dónde se registra |
|---|---|---|
| A. Previa al manifiesto V25 | P01–P14 (14 controles) | este reporte (salida real, abajo) |
| B. Generación del manifiesto | `MANIFIESTO_SHA256_V25.txt` (todos los archivos salvo él mismo; excluirse es inevitable: un archivo no puede contener su propio hash) | `MANIFIESTO_SHA256_V25.txt` |
| C. Posterior al manifiesto | P01–P14 repetidos + Q01 (el manifiesto cubre exactamente los archivos y los hashes coinciden, hashlib) + Q02 (`sha256sum -c`, método independiente) = 16 controles | `../REPORTE_PUBLICACION_V25_GITHUB.md` |
| D. Publicación | commits en `audit/fase0-v25-review` | `../REPORTE_PUBLICACION_V25_GITHUB.md` |
| E. Verificación remota | RV01–RV11 contra GitHub | `../REPORTE_PUBLICACION_V25_GITHUB.md` |

Misma convención que la reconstrucción de V24: la pasada A es un subconjunto de la pasada C; no son controles distintos. No se repiten las 46 pruebas V21, los 26 controles negativos ni PostgreSQL (no se modificaron; se comprueba que sus resultados conservan el mismo SHA-256).

## Salida real de la pasada A (previa al manifiesto V25)
```
PASS | P01 Faltantes: ningún archivo de V24 ausente en V25 | archivos V24=258 ausentes=[]
PASS | P02 Adicionales: los archivos nuevos son exactamente los 17 declarados en MATRIZ_CAMBIOS | nuevos=16 adicionales=[] sin_crear=['MANIFIESTO_SHA256_V25.txt']
PASS | P03 Rutas duplicadas (sin distinguir mayúsculas) o inseguras (absolutas, con .., con \) | archivos=274
PASS | P04 Matriz de hashes V24→V25: idénticos/modificados/nuevos/ausentes | idénticos=254 modificados=4 nuevos=16 ausentes=0
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
RESUMEN V25: 14 controles, 14 PASS, 0 FAIL
```
