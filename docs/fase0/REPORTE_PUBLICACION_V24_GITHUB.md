# REPORTE DE PUBLICACIÓN V24 EN GITHUB

- **Repositorio:** `appalex47-lab/Copy-Creative-Intelligence` · **Rama creada:** `audit/fase0-v24-review` (nueva; sin force push)
- **Origen:** commit `8674114c69881ff1ebda3c5db1f89f2a4d6d31c6` (final de V23, rama `audit/fase0-v23-review`, intacta).
- **Commit V24 (expediente corregido):** `a1dfedb867a79386fd165cbb6fc2859057658705` (padre `8674114c…`). El commit de este reporte es el HEAD de la rama (un archivo no puede contener el SHA de su propio commit).
- **SHA de referencia:** V23 `8674114c69881ff1ebda3c5db1f89f2a4d6d31c6`; V20 (`audit/fase0-v19-review`) `ac84133b776cc73c0cb3416e51e2767039bb5132`; `main` inicial y final `6a1af2424ef39e0960b8f7e09d4e19ec52e6f046`.
- **Archivos publicados:** 257 en el commit V24 (todos añadidos, todos en `docs/fase0/expediente_final_v24/`): 253 del expediente V23 copiado, `INFORME_CORRECCIONES_V24.md`, `MATRIZ_OBSERVACIONES_V23_V24.md`, `REPORTE_VALIDACION_V24.md` y `MANIFIESTO_SHA256_V24.txt`; este reporte es el archivo 258 de la rama respecto a V23.

## Verificaciones remotas (GitHub: `ls-remote` y REST), tras el push
1. La rama `audit/fase0-v24-review` existe y apunta a `a1dfedb8…`: PASS.
2. REST `commits/a1dfedb8…`: padre `8674114c…`, 257 archivos, 0 fuera de `docs/fase0/expediente_final_v24/`: PASS.
3. Árbol remoto (REST `git/trees?recursive`, no truncado) idéntico al local: 640 blobs, 0 diferencias: PASS.
4. `MANIFIESTO_SHA256_V24.txt` descargado de GitHub: idéntico al local. Se descargaron de GitHub los 256 archivos que cubre y se comparó su SHA-256 con el manifiesto: **256 de 256 coinciden, 0 discrepancias**: PASS.
5. V23 intacta: las ramas `audit/fase0-v23-review` y V24 comparten el mismo SHA de árbol para `docs/fase0/expediente_final_v23` (`0824c738f14c313b5f25149016a4622fe85fdeef`) y `docs/fase0/entregas` (`e9210f811072ba309b20bccaa5fee969ccf2b562`); la rama V23 sigue en `8674114c…`: PASS.
6. V20 sigue en `ac84133b…`; `main` sigue en `6a1af242…`: PASS.
7. Pull requests (REST `pulls?state=all`): 0: PASS.
8. Documentos corregidos accesibles directamente en GitHub (LEEME, informe, matriz, reporte de validación, manifiesto): PASS (descargados en la comprobación 4).

## Validación local final (salida real, incluye los 2 controles del manifiesto V24)
```
PASS | V23 en el árbol de trabajo idéntico al inventario previo (253 archivos) | 
PASS | V23 sin cambios respecto al commit 8674114 (git) | 
PASS | V24 conserva los 253 archivos de V23 | 
PASS | Solo difieren de V23 el LEEME y SHA256SUMS interno (los otros 251 conservan su SHA-256) | modificados=['00_LEEME/LEEME_EXPEDIENTE_V21.md', '08_INTEGRIDAD_Y_MANIFIESTOS/SHA256SUMS.txt']
PASS | Archivos nuevos en V24 limitados a los 4 autorizados (los presentes) | nuevos=['INFORME_CORRECCIONES_V24.md', 'MANIFIESTO_SHA256_V24.txt', 'MATRIZ_OBSERVACIONES_V23_V24.md', 'REPORTE_VALIDACION_V24.md']
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
PASS | MANIFIESTO_SHA256_V24 cubre exactamente todos los archivos de V24 (salvo él mismo) y todos los hashes coinciden | archivos=256 coinciden=256
PASS | sha256sum -c MANIFIESTO_SHA256_V24.txt desde expediente_final_v24/ | 
RESUMEN V24: 18 controles, 18 PASS, 0 FAIL
```

## Limitaciones
- Las del expediente V21/V23 se conservan (ver `expediente_final_v24/INFORME_CORRECCIONES_V24.md` §2): sin validación física en CCI-DEV; PostgreSQL temporal ≠ esquema aprobado; sin RLS, privilegios ni concurrencia real; R1–R9 no ejecutado; 12 escenarios PARCIAL; T-409..T-422 sin ejecución individual; 22 funciones validadas indirectamente; HV-02 / PO-05 sin verificación; decisiones del propietario abiertas.
- La verificación remota de este reporte (archivo 258) se informa en la respuesta de entrega.

## Confirmaciones
Sin merge, sin PR, sin force push; `main`, V20 y V23 sin modificar; sin cambios en CCI-DEV, CCI-PROD ni Supabase; Fase 1 no iniciada. **La publicación no representa aceptación formal de Fase 0**, que corresponde exclusivamente al propietario.
