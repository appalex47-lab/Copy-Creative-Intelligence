# REPORTE DE VALIDACIÓN V24

> **Nota de conciliación V25 (2026-11-20):** cifra consolidada de V24 = **18 controles de validación documental distintos (C01–C18)**. Se ejecutaron en dos pasadas: la **previa al manifiesto** corrió C01–C16 (16/16 PASS) y la **final, posterior al manifiesto**, corrió C01–C18 (18/18 PASS): repitió C01–C16 y añadió C17–C18, que solo existen cuando el manifiesto ya está generado. Por eso el reporte de validación V24 muestra 16 y el de publicación V24 muestra 18: no se contradicen, son dos pasadas del mismo conjunto. Las 8 verificaciones remotas de publicación (R01–R08) se cuentan aparte. Reconstrucción completa en `INFORME_CONCILIACION_CONTROLES_V25.md` y `MATRIZ_CONTROLES_V25.csv`. El resto de este documento se conserva sin cambios como registro histórico de V24.

Validación **local** de la corrección documental V24 (2026-11-20). La verificación remota en GitHub se informa en `../REPORTE_PUBLICACION_V24_GITHUB.md` (no se afirma aquí). No se repitieron las 46 pruebas V21, los 26 controles negativos ni PostgreSQL: no se modificó su contenido; se comprobó que **cada archivo de resultados conserva el mismo SHA-256 que en V23**.

## Controles ejecutados (salida real, antes de generar `MANIFIESTO_SHA256_V24.txt`)
```
PASS | V23 en el árbol de trabajo idéntico al inventario previo (253 archivos) | 
PASS | V23 sin cambios respecto al commit 8674114 (git) | 
PASS | V24 conserva los 253 archivos de V23 | 
PASS | Solo difieren de V23 el LEEME y SHA256SUMS interno (los otros 251 conservan su SHA-256) | modificados=['00_LEEME/LEEME_EXPEDIENTE_V21.md', '08_INTEGRIDAD_Y_MANIFIESTOS/SHA256SUMS.txt']
PASS | Archivos nuevos en V24 limitados a los 4 autorizados (los presentes) | nuevos=['INFORME_CORRECCIONES_V24.md', 'MATRIZ_OBSERVACIONES_V23_V24.md']
PASS | Evidencias técnicas, scripts, resultados, matrices y diff sin alteración | 234 archivos
PASS | OBS-01: versión del expediente V21 / corrección V23 / revisión V24 distinguidas; sin «(empaquetado V22)» como versión | 
PASS | OBS-02 §3: declaración histórica conservada + aclaración | 
PASS | OBS-02 §15: declaración histórica conservada + aclaración | 
PASS | OBS-03: limitaciones explícitas en LEEME §13 | faltan=[]
PASS | OBS-03: documentos de limitaciones V23 (sin modificar) ya contienen cada limitación | faltan=[]
PASS | 12 escenarios PARCIAL listados | 
PASS | Decisiones pendientes del propietario conservadas | faltan=[]
PASS | Resultados 46/46 (x2), 26/26, 59/59, 300/300, 63/63, 14/14 intactos | 
PASS | SHA256SUMS.txt interno regenerado y válido (no incluye su propio hash) | 
PASS | Sin cambios fuera de docs/fase0/ y ninguno en herramientas/ o historico/ reales | 
RESUMEN V24: 16 controles, 16 PASS, 0 FAIL
```

## Controles que se ejecutan al final (el manifiesto incluye a este reporte, por lo que no puede ser verificado antes de escribirlo)
- `MANIFIESTO_SHA256_V24.txt` cubre exactamente todos los archivos de V24 salvo él mismo y todos los hashes coinciden.
- `sha256sum -c MANIFIESTO_SHA256_V24.txt` desde `expediente_final_v24/`.
El resultado de ambos se registra en `../REPORTE_PUBLICACION_V24_GITHUB.md`, junto con la verificación remota.

## Limitaciones que permanecen
Las del expediente V21/V23 (ver `INFORME_CORRECCIONES_V24.md` §2): sin validación física en CCI-DEV; PostgreSQL temporal ≠ esquema aprobado; sin RLS, privilegios ni concurrencia real; R1–R9 no ejecutado; 12 escenarios PARCIAL; T-409..T-422 sin ejecución individual; 22 funciones validadas indirectamente; HV-02 / PO-05 sin verificación; decisiones del propietario abiertas.
