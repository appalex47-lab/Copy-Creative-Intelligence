# AUDITORÍA INTEGRAL V16 (pendiente B)

> **Documento HISTÓRICO (V21, 2026-11-20):** evidencia de la etapa V16–V19 conservada tal como se produjo. Sus estados de publicación («local», «sin commit», «no publicado»), cifras (p. ej. 363 casos), clasificaciones de reglas (esquema V18/V19) y números de línea corresponden a la fecha de cada documento y **no** son el estado vigente. Estado vigente y fuente de verdad de cada dato: `../expediente_final_v21/INDICE_VIGENCIA_DOCUMENTAL_V21.md` y `../expediente_final_v21/MATRIZ_CONCILIACION_V21.md`.

## Alcance real de la lectura
- **Ejecutado (cobertura total):** cada una de las líneas de los 5 documentos activos (especificación 5012, informe 205, auditoría 895, roadmap 307, registro 791 antes de la nota) y de los 2 scripts (3139 y 1713) pasó por un escaneo programático: referencias de versión, IDs de reglas y escenarios, cifras, pendientes y frases de aceptación; además el verificador integral las comprueba (59 controles).
- **Revisión manual:** las 61 referencias sin regla automática clara, las secciones de estado (cabeceras, línea 15 y 157 del roadmap, registro v15) y los contextos de HV-01/HV-02.
- **No realizado:** lectura humana línea por línea de los 5012 renglones de la especificación. Por eso **C08 queda NO VERIFICABLE**.

## Matriz de referencias
`MATRIZ_REFERENCIAS_V16.csv` (1148 filas: archivo, línea, texto, clasificación H/A/I/U, justificación, resultado, corrección, evidencia). Resumen: A=125, H=1022, U=1, I=0. La clasificación automática usa reglas explícitas por tipo de contexto y es aproximada; el residuo se resolvió a mano.

## Hallazgos
Ver INVENTARIO_HALLAZGOS_Y_CORRECCIONES_V16.md (HV-01 corregido en local, HV-02 sin resolver).

## Comprobaciones de la auditoría anterior
1. Línea 15 del roadmap = v15: cumple. 2. Línea 157 (ahora 159) conserva v5: cumple. 3. Encabezado del roadmap «REVISIÓN v15»: cumple. 4. Especificación identifica v15: cumple. 5. y 6. Informe y auditoría distinguen V15 de V16: cumplen **solo en el árbol local**. 7. Registro conserva v4–v15 (v2/v3 en históricos): cumple. 8. Ninguna versión histórica presentada como vigente: cumple (tras HV-01). 9. Sin versiones inexistentes: cumple. 10. Sin sustitución global: cumple (diff de 4 archivos, 24 inserciones, 1 eliminación).

## Distinción de evidencia
Observado: contenido de archivos y git. Ejecutado: verificador, baterías en memoria, instrumentación. Inferido: la clasificación automática de las 1022 referencias históricas. Limitación: sin PostgreSQL/Supabase; sin lectura semántica completa. Pendiente de autorización: commit, push, aceptación del propietario.

## Actualización V17 (trabajo documental local posterior a V16; no publicado)

**Cuatro estados, siempre separados.** (1) Commit publicado: 6a1af24 (V16), sin cambios. (2) Árbol local: 5 documentos modificados + carpeta `evidencia_v16/`, sin commit. (3) Estado de auditoría: ver MATRIZ_C01_C30_V16.md. (4) Autorización de publicación: ninguna otorgada.

**C08, alcance real.** Lectura humana de las 1021 líneas narrativas de la especificación. Las 3312 líneas de tabla se procesaron de forma estructural, no se leyeron una a una en lenguaje natural. Matriz regla→decisión→escenario: `MATRIZ_SEMANTICA_REGLAS_V17.csv` (231 reglas). Resultado: 231/231 con definición, fila de cobertura y escenarios existentes (IS-/IP- se definen en la propia tabla de cobertura; IG5-104..116 tienen además una tabla de implementación en la línea 2349, sin contradicción). 41 reglas citan una decisión (DG/PO/OD/PC); 190 son diseño complementario sin decisión citada: es una característica del diseño, no una contradicción. Con esto C08 sigue NO VERIFICABLE: la equivalencia semántica regla↔escenario de las 231 reglas no se leyó una por una.

**C09, alcance de la detección.** Detecta automáticamente: patrones explícitos «v/V/versión/addendum/adenda N» y palabras clave. No detecta: sentido, formulaciones implícitas, si una cita es histórica o vigente sin palabras guía, contradicciones lógicas entre documentos, significado de celdas de tabla. Requiere interpretación humana: clasificación de las referencias residuales y casos ambiguos (HV-02). Las coincidencias de patrón no prueban cobertura semántica.

**Hallazgo S1 (corregido localmente).** Especificación, línea 3620: «14 nuevas» enumeraba 13 tablas (omitía attribution_discard_resolutions, v7). Se añadió «y una de la v7». Verificador tras el cambio, dos corridas completas: 59/59, 28/28, 300/300, 0 fallas, salida idéntica (SHA-256 2c79bb68…0d).

**HV-02.** Ver INVENTARIO_HALLAZGOS_Y_CORRECCIONES_V16.md.

## Actualización V18 (trabajo documental local posterior a V16; no publicado)

- **C08:** NO APROBADO. Matriz semántica de 231 reglas con clases A–E (A 39, B 14, C 173, D 0, E 5). 5 reglas con evidencia de escenario insuficiente (IG1-05, IG1-06, IG1-10, IG1-21, IG5-36); lectura de escenarios limitada a los dos primeros por regla. No se detectó ninguna contradicción (D = 0) entre especificación, escenarios y cobertura (bidireccional, 0 discrepancias). 154 de 231 reglas no tienen implementación (diseño documentado) y 77 citan su ID en el modelo o el verificador.
- **HV-02:** abierta. df5e227 no contiene el documento fuente; ningún ADDENDUM existe en la historia. PO-05 intacto.
- **Pruebas:** 22 funciones, 366 casos individuales PASS en el modelo en memoria (dos corridas idénticas). No son pruebas contra base real.
- **S1/S1b:** corregidas solo en local; matriz en MATRIZ_CONSISTENCIA_S1_V18.md.
- **Estado de publicación:** nada publicado desde V16 (HEAD 6a1af24).

## Dictamen V19 (trabajo documental local posterior a V16; no publicado)

**Dictamen: NO SE ACEPTA V16 integralmente.** Motivos: C08 no aprobado; HV-02 con inconsistencia heredada pendiente del propietario; modelo de tablas con dos puntos abiertos; validaciones externas sin ejecutar.
- C08: 231 reglas — A 53, B 20, D 153, E 5 (cinco pruebas diseñadas, no ejecutadas). 780 escenarios — L2 343, L3 258, L1 179 sin lectura semántica; 12 con demostración débil o parcial.
- HV-02: fuente localizada y verificada por huella; la frase es literal desde v3 hasta v9; sin decisión del propietario no se cambia PO-05.
- Regresión: ver REPORTE_REGRESION_V16.md.
- Lo aprobado se limita al árbol local (C12) y a la evidencia en memoria; nada está publicado.

## Nota V20 (2026-11-19) sobre el estado de publicación

Las expresiones «local», «no publicado» y «sin commit» de las secciones anteriores describen el estado en la fecha de cada sección (histórico, no se borra). Desde entonces V16–V19 se publicó en la rama `audit/fase0-v19-review` (commit `c6ef74be4db185ac3e4fd36810f24619e6f51fcf`); `main` sigue en V16. El trabajo V20 está en el árbol local sin commit. Estado vigente y cierre: `../expediente_final_v16_v19/`.
