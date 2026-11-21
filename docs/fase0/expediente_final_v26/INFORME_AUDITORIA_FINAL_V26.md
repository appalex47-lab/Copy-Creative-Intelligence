# INFORME DE AUDITORÍA FINAL V26

**Fecha:** 2026-11-20 (fecha local, America/Mexico_City; las salidas remotas llevan su sello en UTC) · **Rama:** `audit/fase0-v26-review` · **Base:** `audit/fase0-v25-review`, HEAD de publicación `c3adaf97588ce3b8fef075a44aff6336f4e8c266` (commit del expediente V25 `f235768135175ce3fcd9405a3a4d3a3a68311d3e`).

**V26 no constituye aceptación formal de Fase 0** (corresponde exclusivamente al propietario), no autoriza Fase 1 (NO INICIADA) y no toca Supabase, CCI-DEV ni CCI-PROD.

## 1. Dictamen
V26 audita V25 contra sus evidencias y no contra sus reportes. Resultado: **no hay contradicción de resultados en V25**, pero sí defectos de trazabilidad (§4): RV07 sin salida cruda (resuelto con ejecución nueva, 7/7 PASS tras corregir un defecto de mi propio script), matriz de controles incompleta, errata en LEEME_V25 sobre SHA256SUMS, salidas crudas de V25 solo embebidas, expediente no autónomo y referencias históricas a rutas del diseño original. Todo lo corregible dentro del alcance se corrigió en V26 mediante documentos nuevos; las copias históricas se conservan **sin alterar** (alterarlas rompería sus manifiestos y la regla de no modificar resultados históricos).

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

Dictamen sobre Fase 0 (documental): el expediente es consistente, reproducible y verificable en lo que afirma; **no es una aceptación técnica**. Las limitaciones de §7 y las decisiones de §8 permanecen abiertas. La aceptación formal de Fase 0 corresponde exclusivamente al propietario.

## 2. Auditoría inicial (antes de modificar archivos)
- HEAD de `audit/fase0-v25-review` en GitHub = `c3adaf97588ce3b8fef075a44aff6336f4e8c266`, padre único `f235768135175ce3fcd9405a3a4d3a3a68311d3e` (commit del expediente V25), cuyo padre es `b88bde038e331ba67899632ca4e09eebf2cde82d` (V24).
- Referencias históricas verificadas en remoto (W02 y RV09): `main` `6a1af2424ef39e0960b8f7e09d4e19ec52e6f046`, V20 `ac84133b776cc73c0cb3416e51e2767039bb5132`, V23 `8674114c69881ff1ebda3c5db1f89f2a4d6d31c6`, V24 `b88bde038e331ba67899632ca4e09eebf2cde82d`, V25 `c3adaf97588ce3b8fef075a44aff6336f4e8c266`. La rama V26 no existía antes de publicar (W01).
- Árbol remoto del HEAD V25 = árbol local (917 blobs, no truncado; W03). Inventario con hashes de la copia V25: los 275 archivos de `V25_copia_integra/` coinciden con la rama V25 (S01) y con su manifiesto (274 entradas, S02).
- Árbol de trabajo limpio: la rama de trabajo parte del HEAD de V25 sin cambios ajenos (S15, S16).

## 3. RV07 (resolución definitiva)
- **Definición exacta:** V25 la describe como «el reporte de publicación coincide con el reporte de validación» y la deja para después del segundo commit. V26 la precisa en 7 comprobaciones (`evidencia_reconstruccion_V26/rv07_comparar_reportes.py`): RV07.a el reporte remoto es idéntico al del commit HEAD; RV07.b ambos declaran 16 controles de validación y 11 verificaciones remotas; RV07.c el bloque A del reporte de validación es la salida cruda de la pasada A; RV07.d el bloque C del reporte de publicación es la salida cruda de la pasada C; RV07.e el bloque E es la salida cruda original de RV01–RV06 y RV08–RV11; RV07.f el commit del expediente citado es el padre del HEAD; RV07.g las etapas A–E coinciden.
- **Evidencia previa:** no existía evidencia válida (solo descargas de los dos reportes a las 16:35 locales, sin comando ni resultado). No se reutilizó nada.
- **Ejecución:** contra GitHub (repositorio `appalex47-lab/Copy-Creative-Intelligence`, rama `audit/fase0-v25-review`, ref `c3adaf97588ce3b8fef075a44aff6336f4e8c266`). Corrida 1: 6/7 (RV07.e FAIL por un criterio arbitrario de mi script, que exigía al menos 5 líneas con ciertas palabras; el bloque era idéntico byte a byte a la salida cruda). Corrida 2, con el criterio eliminado: 7/7 PASS. Ambas salidas están archivadas.
- **Observación:** el resumen del reporte de publicación V25 omite RV10 y RV11 y declara RV07 pendiente (D02); se registra como errata, no es criterio de RV07.
- **Resultado:** RV07 PASS (ejecución nueva V26). Las 11 verificaciones RV01–RV11 tienen ahora once evidencias independientes: RV01–RV06 y RV08–RV11 en la salida original de V25 y en V26; RV07 en V26.

## 4. Defectos encontrados, causas y correcciones
| ID | Defecto | Causa | Corrección / tratamiento en V26 | Estado |
|---|---|---|---|---|
| D01 | RV07: V25 declara 11 verificaciones remotas y solo 10 tienen salida archivada; RV07 estaba definida de forma vaga («el reporte de publicación coincide con el reporte de validación») y el reporte V25 la dejaba «pendiente». | RV07 solo podía ejecutarse con el reporte de publicación ya publicado (segundo commit); su resultado se dio en la respuesta de entrega de V25 y no se archivó la salida. Quedaron únicamente descargas sin comando ni resultado. | Definición precisa (7 comprobaciones RV07.a–RV07.g), script archivado, ejecución contra GitHub en el HEAD c3adaf9 con salida cruda. La corrida 1 dio 6/7 por un defecto de mi propio script (criterio RV07.e con un umbral arbitrario, no del reporte V25); se archiva como ejecución FAIL y la corrida 2, con el script corregido, dio 7/7. La ejecución original de V25 no se cuenta. | Resuelto |
| D02 | El resumen de resultados del reporte de publicación V25 lista RV01–RV09, omite RV10 y RV11 (cuyas salidas sí están en su bloque E y pasan) y declara RV07 pendiente. | El resumen se redactó antes de ejecutar RV07 y se copió de una lista incompleta. | Errata registrada aquí y en la matriz de cambios; el documento histórico se conserva sin alterar (copia byte a byte). RV10 y RV11 constan como PASS con su salida cruda. | Resuelto (errata) |
| D03 | MATRIZ_CONTROLES_V25.csv solo contiene C01–C18 y R01–R08 (26 filas); no incluye los controles propios de V25 (P01–P14, Q01–Q02, RV01–RV11). | V25 se centró en conciliar V24. | MATRIZ_CONTROLES_V26.csv: una fila por control real de V24, V25 y V26, más pruebas técnicas históricas y limitaciones; ejecuciones en EJECUCIONES_CONTROLES_V26.csv. | Resuelto |
| D04 | «26 PASS» en V25 mezcla 18 controles documentales y 8 verificaciones remotas sin distinguir controles únicos de ejecuciones. | No había una tabla de conciliación con ambas magnitudes. | Tabla de conciliación con controles únicos y ejecuciones por estado (§1 del informe de conciliación), idéntica en los documentos V26 (S07). | Resuelto |
| D05 | Las salidas crudas de las pasadas A y C de V25 y de las verificaciones remotas RV solo estaban embebidas en reportes; no existían como archivos. Además existió una repetición intermedia de la pasada A (A2, salida idéntica) no documentada. | El flujo de V25 no archivó las salidas intermedias. | Recuperadas del directorio de trabajo y archivadas en evidencia_reconstruccion_V26/historico_V25_no_archivado/ (copias recuperadas; no estaban en la rama V25) y comparadas con los bloques embebidos (S10). A2 consta como ejecución histórica con esa salvedad. | Resuelto |
| D06 | LEEME_V25.md afirma que 08_INTEGRIDAD_Y_MANIFIESTOS/SHA256SUMS.txt «ya no verifica en 3 archivos con nota V25». | Redacción conjunta con el manifiesto V24, sin verificar el SHA256SUMS interno. | Comprobado: el SHA256SUMS interno verifica 252/252; solo el manifiesto V24 falla, exactamente en 3 archivos. Errata registrada (S02); LEEME_V25 se conserva sin alterar. | Resuelto (errata) |
| D07 | El expediente V25 no es autónomo: REPORTE_VALIDACION_V25 y los reportes V24 remiten a ../REPORTE_PUBLICACION_V2x_GITHUB.md, que no está dentro del expediente V25. | Los reportes de publicación se publicaron fuera de la carpeta del expediente. | V26 incluye V25_publicacion/REPORTE_PUBLICACION_V25_GITHUB.md (copia idéntica al HEAD de V25) y el mapa de referencias resuelve las rutas relativas. | Resuelto |
| D08 | Los documentos V21 citan archivos con rutas del diseño original (salidas/, scripts/, expediente_final_v21/ y nombres sueltos) que no existen literalmente en el paquete. | El paquete renombra rutas (08_INTEGRIDAD_Y_MANIFIESTOS/CORRESPONDENCIA_RUTAS_ORIGEN.csv) y los documentos históricos no se reescriben. | MAPA_REFERENCIAS_V26.csv: 271 referencias de los documentos de la copia V25; EXACTA=59, EXTERNA_AL_EXPEDIENTE=2, EXTERNA_AL_EXPEDIENTE_COPIADA=4, POR_CORRESPONDENCIA_RUTAS_ORIGEN=109, POR_NOMBRE_UNICO=28, POR_NOMBRE_VARIAS_COPIAS=69; ninguna sin resolver. Los documentos históricos no se modifican. | Resuelto (mapa) |
| D09 | El FAIL esperado de la reproducción V22 (manifiesto V21: «historico/ idénticos al commit V20», dependencia de Git) no figuraba en ninguna matriz de controles. | Solo constaba en INFORME_VERIFICACION_REPRODUCCION.md. | Fila HT10 con estado PARTIAL (8 de 9) en la matriz y en la conciliación. | Resuelto |
| D10 | Dos ejecuciones intermedias del validador V24 (15/16 y 16/16) no tienen salida archivada. | Solo existieron en la transcripción de la sesión V24. | No resoluble: la salida no existe. Se registran como declaradas sin evidencia (DECLARACIONES_SIN_EVIDENCIA en el informe de conciliación) y no se cuentan como ejecuciones. | Limitación documentada |
| D11 | Las verificaciones remotas R01–R08 originales de V24 no tienen salida cruda. | No se archivó en V24. | No resoluble históricamente. Re-ejecutadas en V25 y V26 contra GitHub (ejecuciones nuevas, salida cruda archivada); las originales no se cuentan. | Limitación documentada |
| D12 | El control C05 de V24 es débil (comprueba un subconjunto de los archivos autorizados, no que existan los 4). | Diseño del validador V24. | Sin cambio: su existencia queda cubierta por C17/C18. Se registra en la matriz (observaciones de C05). | Limitación documentada |
| D13 | V25 usa «16 controles» para su validación y «11 verificaciones» sin una cifra consolidada con V24 y con las pruebas técnicas históricas. | Cifras repartidas en varios documentos. | Cifra única de V26 con controles únicos (94) y ejecuciones (238), generada desde la matriz y comprobada por S07 en todos los documentos. | Resuelto |

## 5. Revisión por áreas
**A. Controles documentales V24 (C01–C18).** 18 controles; las dos pasadas históricas (16 + 18) y las dos re-ejecuciones (V25 y V26 sobre V24 publicado, 18/18 con los mismos estados) están archivadas; los bloques embebidos en los reportes V24 coinciden con las salidas crudas (S10). Causa de 16 vs 18: C17 y C18 solo se activan con el manifiesto presente. Intermedias no archivadas: D10.
**B. Controles remotos V24 (R01–R08).** Originales sin salida cruda (D11). Re-ejecuciones V25 y V26 contra GitHub: 8/8 PASS cada una; descargas: 256/256 archivos coinciden con el manifiesto V24.
**C. Controles V25 (P01–P14, Q01–Q02, RV01–RV11).** Re-ejecución de `V25_copia_integra/evidencia_reconstruccion_V25/val25.py` sobre V25 publicado: 16/16, salida idéntica byte a byte a la pasada C histórica. Remotos: RV01–RV11 PASS en V26 (RV01 en variante por el nuevo HEAD). Matriz V25 incompleta (D03); cifras reconciliadas (D04, D13).
**D. Integridad histórica.** Verificado en remoto y local: V23, V24, V25, V20 y `main` conservan sus SHA (W02, RV09, S16). Las evidencias técnicas originales de V25 coinciden byte a byte con su copia (S01). Las notas de conciliación V25 solo insertan una línea: quitándola se recupera cada original V24 (control P05, re-ejecutado en V26). Las copias históricas están identificadas como copias (LEEME_V26 §2).
**E. Revisión semántica.** Referencias a archivos: 271 en los documentos de la copia V25, ninguna sin resolver (D08). SHA de commit citados: todos existen y su rol coincide (S09). Fechas: en los documentos de la copia V25 analizados solo aparecen 2026-11-16, 2026-11-19 y 2026-11-20, coherentes con las versiones. Cifras: las apariciones de «16», «18», «26», «11», «8», «256», «274» y «275» corresponden a contextos distintos y quedan reconciliadas (informe de conciliación §3). 640 vs 641 blobs: refs distintas. Declaraciones históricas presentadas como actuales: el LEEME V21 y los reportes anteriores quedan acotados por LEEME_V26 §2. Controles duplicados: ninguno (S14). PASS sin soporte: ninguno (S06).

## 6. Integridad y punto fijo
Manifiesto autónomo `MANIFIESTO_SHA256_V26.txt` (todos los archivos salvo él mismo), verificado por dos métodos (S19 hashlib, S20 `sha256sum -c`) tras preparar el paquete definitivo. La pasada A (S01–S18) y los documentos que embeben sus bloques se generan hasta un **punto fijo**: se ejecuta A en modo preliminar, se embebe, y se vuelve a ejecutar hasta que la salida es idéntica a la embebida. S19 y S20 se consignan como PASS tras ejecutarlos sobre el paquete definitivo; si alguno fallara, se regeneraría el paquete y no se publicaría.

## 7. Limitaciones técnicas que permanecen
- **12 escenarios PARCIAL:** T-03, T-06, T-10, T-47, T-78, T-80, T-124, T-137, T-138, T-139, T-140, T-166 (controles L01).
- **T-409 a T-422** sin ejecución individual propia (L02).
- **22 funciones** validadas indirectamente (sensibilidad a mutaciones e independencia del auditor), no por lectura línea a línea (L03).
- **PostgreSQL temporal:** 63/63 pruebas y 14/14 mutaciones según la evidencia existente (HT05, HT06), sin equivalencia con el esquema físico aprobado (L04).
- **Sin validación física en CCI-DEV** (L05); sin validación real de **RLS, privilegios ni concurrencia** (L06).
- **R1–R9** (trigger de elegibilidad) no ejecutado (L07).
- **HV-02 / PO-05** sin verificación (L08).

## 8. Decisiones pendientes del propietario
PO-05, G-1, G-5, G-10, DG-19, DG-20, DG-09, DG-12, DG-16, DG-18, DEP-RET-01, G-9, RP-01, P-01 a P-05, P-10 y OD-13 (detalle en `V25_copia_integra/07_LIMITACIONES_Y_DECISIONES_PENDIENTES/INVENTARIO_DECISIONES_ABIERTAS_FASE0.md`). V26 no convierte ninguna en decisión aprobada.

## 9. Alcance y límites de esta auditoría (qué no se verificó)
- No se volvieron a ejecutar el verificador (~21 min), la batería V21 ni PostgreSQL; se verifican las salidas archivadas y su coherencia (HT01–HT10, S13).
- No se leyó línea por línea el contenido técnico de los 275 archivos heredados; se verificó su identidad byte a byte con V25 y la coherencia de referencias, cifras y estados.
- No se pueden recuperar las ejecuciones intermedias de V24 ni las salidas originales R01–R08 de V24 (D10, D11).
- Nada de lo que depende de CCI-DEV, Supabase o el esquema físico se simuló.
- La verificación remota posterior al push de V26 se registra fuera del expediente (no puede incluirse en un commit que aún no existe).
