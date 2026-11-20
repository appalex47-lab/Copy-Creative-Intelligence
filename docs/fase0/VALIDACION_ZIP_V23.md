# VALIDACIÓN ZIP V23

## A. Identificación
- ZIP original: `CCI_FASE0_EXPEDIENTE_V21.zip` · SHA-256 `25ac41b0023632db7a970a851668ffc7fa713e180b7aa181c431b1c903debd68` (coincide con el de referencia; no se sobrescribió).
- ZIP nuevo: `CCI_FASE0_EXPEDIENTE_V21_V23.zip` · SHA-256 `7dd5e3b8c758c38ee55a780b5575f2042528f2cdb2a4ffeb745347820960d93f`
- Tamaño: 4376868 bytes · Archivos: 253 (252 en `SHA256SUMS.txt` + el propio `SHA256SUMS.txt`)
- Generado: 2026-11-20 13:58:10 CST
- El hash del ZIP final no puede estar dentro del ZIP; se da aquí.

## B. Corrección
- Archivo: `CCI_FASE0_EXPEDIENTE_V21/00_LEEME/LEEME_EXPEDIENTE_V21.md`, sección 9.
- Anterior: `cd <carpeta del paquete>/08_INTEGRIDAD_Y_MANIFIESTOS && sha256sum -c SHA256SUMS.txt` ejecutado desde la raíz `CCI_FASE0_EXPEDIENTE_V21/`
- Posterior:
```
cd CCI_FASE0_EXPEDIENTE_V21
sha256sum -c 08_INTEGRIDAD_Y_MANIFIESTOS/SHA256SUMS.txt
```
  más cuatro aclaraciones: se ejecuta desde la raíz extraída; las rutas son relativas a esa raíz; el manifiesto no incluye su propio hash; el hash del ZIP final va aparte, en el reporte de entrega. Se añadió además una línea en blanco para que el siguiente párrafo no se interprete como parte de la lista.
- Ejecutado exactamente así sobre el ZIP V23 extraído en carpeta limpia: **252 OK, código de salida 0**.

## C. Control de cambios (V23 contra V21, hash a hash)
- Documentos modificados: 1 (`LEEME_EXPEDIENTE_V21.md`) + 1 manifiesto regenerado (`SHA256SUMS.txt`). Archivos nuevos: 0. Eliminados: 0.
- Las 251 restantes son idénticas a V21, incluidos 51 archivos de scripts, resultados y logs verificados individualmente: no se modificó ninguna evidencia ni resultado.
- Resultados archivados sin cambio: batería 46/46 (x2), controles negativos 26/26, verificador 59/59 · 28/28 · 300/300, PostgreSQL 63/63 y mutaciones 14/14.
- Diff exacto del LEEME:
```diff
--- LEEME_original.md	2026-11-20 13:57:14.057339661 -0600
+++ new/CCI_FASE0_EXPEDIENTE_V21/00_LEEME/LEEME_EXPEDIENTE_V21.md	2026-11-20 13:57:27.498758138 -0600
@@ -35,7 +35,18 @@
 Orden sugerido: `07_.../00_ESTADOS_DE_VERIFICACION_Y_LIMITACIONES.md` → `INFORME_FINAL_V21.md` → `MATRIZ_CONCILIACION_V21.md` → `REGISTRO_DECISIONES_ABIERTAS_V21.md` → `AUDITORIA_FINAL_V21.md` → `INDICE_VIGENCIA_DOCUMENTAL_V21.md` (qué documento es vigente, histórico o sustituido) → `REPORTE_VALIDACION_INTEGRAL_V21.md`.
 
 ## 9. Reproducción de pruebas
-Comprobación de integridad del paquete (sin dependencias): `cd <carpeta del paquete>/08_INTEGRIDAD_Y_MANIFIESTOS && sha256sum -c SHA256SUMS.txt` ejecutado desde la raíz `CCI_FASE0_EXPEDIENTE_V21/` (la comprobación completa del ZIP se entrega aparte, junto al ZIP).
+Comprobación de integridad del paquete (sin dependencias), desde la carpeta donde se extrajo el ZIP:
+
+```
+cd CCI_FASE0_EXPEDIENTE_V21
+sha256sum -c 08_INTEGRIDAD_Y_MANIFIESTOS/SHA256SUMS.txt
+```
+
+- El comando debe ejecutarse desde la raíz del expediente extraído (`CCI_FASE0_EXPEDIENTE_V21/`).
+- Las rutas del manifiesto son relativas a esa raíz.
+- El manifiesto no incluye su propio hash.
+- El hash del ZIP final se proporciona por separado, en el reporte de entrega (la comprobación completa del ZIP se entrega aparte, junto al ZIP).
+
 Verificador completo (≈20 min), desde `05_LOGS_Y_EVIDENCIAS/arbol_original_docs_fase0/`:
 `env -i PATH=/usr/bin:/bin LC_ALL=C.UTF-8 PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 python3 -I herramientas/verificar_expediente.py --dir . --v33 ../original_externo_v3_3/fase0_v3_3_integral.md`
 Las demás pruebas están descritas en `REPORTE_REGRESION_FINAL.md` (V20) y en `03_SCRIPTS/`.
```

## D. Integridad
- Archivos incluidos: 253 · hashes verificados: 252 · coincidencias: 252 · discrepancias: 0 (sin rutas duplicadas, absolutas ni fuera de la raíz).
- Extracción: completa, sin errores. Comparación byte a byte (extraído vs carpeta empaquetada): 253/253 idénticos.

## E. Controles ejecutados sobre el ZIP final
```
PASS | ZIP original coincide con SHA-256 esperado | 
PASS | ZIP V23 distinto del original y original no sobrescrito | 
PASS | 1 zipfile.testzip | 
PASS | 2 unzip -t | No errors detected in compressed data of /home/claude/outputs/CCI_FASE0_EXPEDIEN
PASS | 3 extracción completa en carpeta limpia | 
PASS | 4 inventario del ZIP = archivos extraídos | 253
PASS |    carpeta raíz única CCI_FASE0_EXPEDIENTE_V21 | 
PASS | 5 SHA256 de todos los archivos (hashlib) | verificados=252 coincidencias=252 discrepancias=0
PASS |    sin rutas duplicadas, absolutas ni que escapen de la raíz | 
PASS |    manifiesto lista todos los archivos salvo SHA256SUMS.txt y no se incluye a sí mismo | listados=252
PASS | 6 sha256sum -c con la instrucción corregida exacta (desde la raíz extraída) | OK=252 rc=0
PASS | 7 byte a byte: extraídos = carpeta empaquetada | 
   añadidos=[] eliminados=[] modificados=['CCI_FASE0_EXPEDIENTE_V21/00_LEEME/LEEME_EXPEDIENTE_V21.md', 'CCI_FASE0_EXPEDIENTE_V21/08_INTEGRIDAD_Y_MANIFIESTOS/SHA256SUMS.txt']
PASS | 8 V23 vs V21: solo cambian LEEME y SHA256SUMS; sin añadidos ni eliminados | modificados=2 nuevos=0 eliminados=0
PASS |    las 251 restantes idénticas a V21 (hash a hash) | 
PASS | 9 documentos principales (9/9) | 
PASS |    6 scripts V21 | 
PASS |    11 evidencias V21 | 
PASS |    diff V20→V21 conservado | 
PASS | 10 resultados intactos: batería 46/46 (x2) | 
PASS |     controles negativos 26/26 | 
PASS |     verificador 59/59, 28/28, 300/300 | 
PASS |     PostgreSQL 63/63 y mutaciones 14/14 (salidas archivadas) | ['TOTAL pruebas=63 PASS=63 FAIL=0', 'TOTAL mutaciones=14 DETECTADAS=14']
PASS |     resultados y scripts idénticos a V21 | 51 archivos
PASS |     limitaciones y decisiones pendientes conservadas | faltan=[]
PASS |     LEEME: instrucción corregida presente, la anterior ausente | 
PASS | Git sin cambios (rama, HEAD, estado) y main intacta local y remota | 
RESUMEN V23: 26 controles, 26 PASS, 0 FAIL
```

## F. Alcance
Sin commit, push, merge ni PR; sin modificaciones en GitHub; `main` intacta (`6a1af2424ef39e0960b8f7e09d4e19ec52e6f046`, local y remoto); rama y estado de git idénticos a antes; sin operaciones sobre CCI-DEV ni CCI-PROD; Fase 1 no iniciada. No se volvió a ejecutar la batería (fuera de alcance). Esto no implica aceptación formal de Fase 0.

## G. Observaciones (registradas, no corregidas por estar fuera de alcance)
1. `INFORME_VERIFICACION_REPRODUCCION.md` indica la hora de la re-ejecución previa de la batería como «09:1x local» (aproximada).
2. El LEEME sigue sin listar, en su sección 11, los resultados reproducibles de forma explícita; los remite a `INFORME_VERIFICACION_REPRODUCCION.md`.
3. Las limitaciones se conservan tal cual; no se reprodujo PostgreSQL en esta tarea.
