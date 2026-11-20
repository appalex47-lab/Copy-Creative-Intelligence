# INVENTARIO DE HALLAZGOS Y CORRECCIONES V16

| ID | Hallazgo | Evidencia | Clasificación | Acción | Estado |
|---|---|---|---|---|---|
| HV-01 | Ningún documento activo ni script mencionaba V16 | `grep -ci v16` = 0 en los 5 documentos y los 2 scripts sobre el commit 6a1af24 | Inconsistencia (omisión) | Nota de trazabilidad en REGISTRO y una frase en informe, auditoría y roadmap (ver TRAZABILIDAD_V15_V16.md) | Corregido **solo en el árbol local**; no publicado |
| HV-02 | `REGISTRO_HISTORICO_VERSIONES.md` línea 126: PO-05 dice «Aceptación formal del addendum v3», mientras el resto del registro identifica la Adenda v9 (PO-05) | Líneas 126, 149, 162, 177 | Ambigua (U): puede ser texto heredado o redacción deliberada | **No corregido**: toca un pendiente del propietario y no es una referencia a V16 | Requiere decisión del usuario |
| HV-03 | Primer texto de la nota V16 fue rechazado por K23 («Pruebas ejecutadas» sin negación) | Corrida sin mutaciones: 58/59, K23 en REGISTRO:808 | Defecto de mi propia redacción | Reformulé el texto; nuevo resultado 59/59 | Resuelto |
| HV-04 | Con el verificador sin `--v33` salen 299 mutaciones y K48 pendiente | Corridas del 2026-11-19 | Dependencia de entorno, no defecto | Documentado; con el original, 300/300 | Explicado |
| HV-05 | Las funciones `pruebas_guarda` y `pruebas_atomicidad` no exponían resultados individuales en el reporte | Código 1810 y 2104 | Limitación de evidencia | Script externo de instrumentación; 29/29 PASS | Resuelto sin tocar el repo |
| HV-06 | La línea 157 del roadmap pasó a la 159 por el párrafo insertado | `grep -n` | Efecto colateral esperado | Texto intacto | Aceptable |

## Revisión de contradicciones, duplicados y referencias (resultado ejecutado, escaneo de todas las líneas)
- Reglas IG5: 231 identificadores únicos; cada una con el mismo texto en definición y cobertura (K02); la única referencia a una regla inexistente (`IG5-999`) es la mutación M-17 intencional.
- Escenarios: 780, consecutivos, sin duplicados; ningún T-xxx referenciado sin escenario.
- Cifras (231 reglas, 780 escenarios, 41 tablas, 14 nuevas): coherentes en especificación, auditoría y registro; los valores distintos del registro corresponden a entradas de revisiones anteriores.
- Pendientes (PO-05, RP-01, G-9, P-01..P-05, P-10, OD-13, DEP-RET-01, DG-09/12/16/18/19/20) presentes en especificación, registro y roadmap; todas las menciones de aceptación del propietario están negadas.
- 1148 referencias de versión clasificadas (matriz CSV): 125 activas, 1022 históricas, 1 ambigua (HV-02), 0 inconsistentes tras la corrección HV-01.
- Referencias a versiones inexistentes (p. ej. v17 o posteriores): ninguna. Formas alternativas de citar versión (revisión N, V-N): solo falsos positivos (identificadores AV-0x).

No corregido ni investigado más allá: reglas contradictorias de fondo del diseño (requeriría lectura semántica de 5012 líneas; ver AUDITORIA_INTEGRAL_V16.md).

## Actualización V17

**HV-02 (investigada).** La frase «addendum v3» de PO-05 (registro, línea 126) entró en el commit df5e227 (extracción literal de la v2). Los archivos ADDENDUM no existen en el repositorio (solo sus huellas en el manifiesto, líneas 36-44), por lo que no se puede probar que «v3» corresponda a la Adenda v9. No se modificó PO-05. Estado: pendiente de decisión del propietario.

| ID | Hallazgo | Estado |
|---|---|---|
| HV-01 | Sin referencia a V16 en documentos activos | Corregido (solo local) |
| HV-02 | PO-05 «addendum v3» vs Adenda v9 | Requiere decisión del propietario |
| S1 | Especificación l.3620: «14 nuevas» listaba 13 | Corregido (solo local); verificador 59/59 ×2 |
| S2–S4 | Observaciones de estilo/históricas de la lectura narrativa | No corregido (sin efecto normativo; no se tocan históricos) |
| C08 | Equivalencia semántica regla↔escenario, 231 reglas | No verificable (estructura 231/231 OK) |
| C09 | Alcance de la detección automática | Documentado |
| HV-03..06 | Ver tabla anterior | Sin cambio |

Reglas sin decisión citada: 190 de 231 (diseño complementario, hallazgo informativo). Resolución propuesta: ninguna obligatoria; el propietario puede pedir asociarlas a una decisión.

## Actualización V18

**C08 (auditoría semántica de las 231 reglas):** `MATRIZ_SEMANTICA_REGLAS_V17.csv` (13 columnas: ID, definición, fuente, decisión, clase A–E, base, escenarios, resultado esperado, tipo, evidencia de implementación, líneas, consistencia, observación).
Clases: A (derivada de decisión citada) 39; B (cita explícita de un elemento de v3.3) 14; C (complementaria sin decisión explícita) 173; D (contradictoria) 0; E (evidencia insuficiente) 5.
- No se asignó ninguna decisión por similitud de palabras. A solo cuando la decisión está citada en la regla, su cobertura o la tabla 12.1. B solo cuando la regla cita T-02, 27 tablas, v3.3, 76 subfases, 17 claves o una sección 3.x de v3.3.
- Comprobaciones completas y automáticas: cobertura↔escenarios bidireccional (0 discrepancias en 231 reglas y 780 escenarios; ningún escenario cita una regla que no lo cita a él).
- Lectura humana: leí la definición de las 231 reglas y el resultado esperado de los dos primeros escenarios de cada una. Los escenarios restantes de reglas con más de dos no se leyeron uno a uno.
- E (5): IG1-05 (T-03 no prueba otra organización), IG1-06 (T-04 no reasigna un master_piece_id ya asignado), IG1-10 (T-06 no prueba inmutabilidad del vínculo), IG1-21 (T-10/T-47 no prueban que aprobar la maestra no aprueba la adaptación), IG5-36 (T-136 es positivo; ninguno prueba que cada una de las nueve columnas distinga el par). Puede existir un escenario no citado en la cobertura que las pruebe; no lo busqué por similitud.
- Evidencia de implementación: 77 reglas citan su ID en el modelo o el verificador; 154 son diseño documentado sin implementación.
- **Resultado: C08 NO APROBADO** (reglas con evidencia insuficiente + lectura parcial de escenarios).

**HV-02 (PO-05):** el commit df5e227 (2026-11-16, «extracción selectiva literal de la especificación e informe v2») introdujo la línea 126 con «addendum v3». Ningún archivo ADDENDUM existe en ningún commit de la historia (17 commits revisados); v3.3 no contiene PO-05 ni «addendum». El manifiesto registra una huella para un «addendum v3» (0a9a2ad8…) pero no el archivo. La tabla de evolución muestra PO-05 «pendiente del propietario» desde rev3 hasta rev10; es compatible con que «v3» fuera la revisión en la que nació PO-05, pero eso es una hipótesis, no una prueba. **Sin documento fuente: HV-02 sigue abierta; PO-05 sin modificar; decisión del propietario.**

**S1:** ver MATRIZ_CONSISTENCIA_S1_V18.md. Nuevo hallazgo S1b (línea 38, 13 de 14 tablas) corregido solo en local. Observaciones no corregidas: channel_formats sin tabla de columnas propia; fila «Fuentes físicas» (l.1270) sin attribution_discard_resolutions.

**Pruebas:** ver INVENTARIO_22_FUNCIONES_V18.md (22 funciones, 363 casos individuales, 0 fallos).

| ID | Estado final V18 |
|---|---|
| HV-01 | Corregido (solo local) |
| HV-02 | Abierta; requiere decisión del propietario |
| S1, S1b | Corregidos (solo local); verificador ver REPORTE_REGRESION |
| S2–S4 | No corregidos (estilo/históricos) |
| Observaciones channel_formats y l.1270 | No corregidas; requieren decisión de diseño |
| C08 | No aprobado (5 reglas E; lectura parcial de escenarios) |
| 190→173 reglas C sin decisión explícita | Informativo; el propietario puede pedir asociarlas a decisiones |

Precisión sobre la clase E: IG1-05 e IG1-06 se relacionan con DG-02 (tabla 12.1, «reglas IG1-03 a IG1-07») y serían A por decisión; se clasifican E porque el escenario citado no prueba su contenido. Sin esas dos, A = 39 y A + E con decisión = 41 (igual que en V17).

## Actualización V19 (trabajo documental local posterior a V16; no publicado)

### 1. Resolución de las cinco reglas E (C08)
Se leyeron la definición y TODOS los escenarios citados de cada una, y se buscaron en los 780 escenarios otros que pudieran demostrarlas (la búsqueda por términos solo sirvió para localizar candidatos que luego se leyeron; no se asignó nada por similitud).

| Regla | Comportamiento que debe demostrarse | Escenarios revisados | Resultado | Prueba propuesta |
|---|---|---|---|---|
| IG1-05 | Maestra y adaptación son de la misma organización | T-03 (versión inexistente / de otra pieza); T-118 (catálogo de otra organización) | No demostrada: T-03 no usa otra organización; T-118 es del catálogo | PE-01 |
| IG1-06 | master_piece_id no puede cambiarse ni anularse una vez asignado | T-01, T-02, T-04 | Sin evidencia directa: T-04 crea ciclos, no reasigna | PE-02 |
| IG1-10 | El vínculo versión→versión de la maestra es inmutable | T-06; T-312 (otra columna: brief_version_id, IG5-85) | Sin evidencia directa | PE-03 |
| IG1-21 | La aprobación se liga a la versión exacta; aprobar la maestra no aprueba la adaptación ni al revés | T-10, T-47 (no la demuestran); T-78 y T-81 (aprobación de otra pieza / de otra versión: sí demuestran el principio) | Evidencia indirecta: IG1-01 (cada pieza es una fila con identidad propia) + T-78 + T-81; falta un caso explícito maestra/adaptación | PE-04 |
| IG5-36 | El par evaluado se identifica por nueve columnas | T-136; T-137 a T-140 (citados en IG5-37) | Parcial: T-137 a T-140 rechazan la sustitución con otra versión de adaptación, otra V-D, otra V-B u otra adaptación (4 de 9). Sin escenario: organization_id, adaptation_asset_key, master_piece_id y el arte de V-B y de V-D. IG5-37 (ocho columnas) + organization_id = nueve: sin contradicción | PE-05 |

**Pruebas específicas diseñadas (no modifican reglas ni resultados esperados; numeración PE-xx para no alterar T-001..T-780, cuyo recuento fija el verificador):**
- **PE-01.** Precondición: maestra M de la organización A. Acción: crear una adaptación de la organización B con master_piece_id = M. Esperado: rechazo por la FK compuesta con organization_id; ninguna fila creada. Control positivo: la misma operación en A prospera.
- **PE-02.** Precondición: A es adaptación de M1. Acción: UPDATE de master_piece_id a M2, y UPDATE a NULL. Esperado: rechazo en ambos casos; el vínculo con M1 intacto.
- **PE-03.** Precondición: versión de A con master_copy_version_id = M v1. Acción: UPDATE a M v2. Esperado: rechazo del trigger de inmutabilidad; fila intacta.
- **PE-04.** Precondición: M v1 aprobada (#7), A v1 sin aprobación. Acción: evaluar C2 para A; después aprobar A v1 y evaluar C2 para una versión nueva de M sin aprobación. Esperado: C2 bloquea (SIN_APROBACION_V_A) en el primer caso y bloquea la versión nueva de M en el segundo; la aprobación de una pieza no satisface a la otra.
- **PE-05.** Precondición: e1 de un par. Acción: e2 con supersedes = e1 y un par distinto, variando una sola vez cada columna no cubierta (organization_id, asset_key, master_piece_id, arte de V-B, arte de V-D). Esperado: rechazo por la FK de sustitución en cada variante.

**Ejecución:** NO se ejecutaron. Verifican restricciones de PostgreSQL (FK compuestas, triggers, inmutabilidad) y el modelo en memoria no representa creative_pieces ni copy_versions; ejecutarlas exige SQL, vetado en esta misión. Quedan como pruebas pendientes de CCI-DEV (Fase 1). Las cinco reglas **permanecen en clase E**; no se modificó ninguna regla ni expectativa y no se añadieron escenarios a la especificación.

### 2. Las 173 reglas de clase C
Detalle por regla: `MATRIZ_SEMANTICA_REGLAS_V17.csv` (columnas V19: subclase, fuente normativa, razón, relación con otras reglas, intervención). Criterio: solo evidencia textual explícita.
- **A** (derivada de especificación aprobada): 0 de las 173 (las 14 que citan v3.3 ya estaban en la clase B de V18).
- **B** (complementaria derivada de otra regla: su texto cita expresamente otra regla): **20**.
- **C** (requiere decisión del propietario: cita un punto pendiente): **0**.
- **D** (sin fuente suficiente: ninguna cita a decisión, regla ni v3.3; su única fuente es la sección de diseño de esta especificación, no aceptada): **153**.
Lectura: las 20 B son legítimas si se acepta la regla citada. Las 153 D no son erróneas ni contradictorias; no tienen fuente independiente y su legitimidad depende de que el propietario acepte el diseño complementario de G-1, G-5 y G-10 (que sigue sin aceptarse). No se inventó ninguna fuente ni relación.
Resumen de las 231: A 53 (39 por decisión + 14 por cita de v3.3), B 20, D 153, E 5; clase «D contradictoria» de V18: 0.

### 3. Auditoría de tablas
Ver `MATRIZ_CONSISTENCIA_S1_V18.md`, sección V19. Resultado: `channel_formats` es una tabla física nueva (opción A) sin tabla de columnas formal; la fila «Fuentes físicas» (l.1270) omite `attribution_discard_resolutions` aunque el procedimiento del mismo contrato (paso 8) y la categoría 3 sí la usan; 22 + 5 = 27 y 27 + 14 = 41 confirmados.

### 4. HV-02 / PO-05 — informe
- Commit df5e227 (2026-11-16, «extracción selectiva literal de la especificación e informe v2»): introdujo en el registro la línea 126.
- **Fuente localizada:** los nueve archivos ADDENDUM_DECISIONES_PROPIETARIO_OD01_OD16 (v1 a v8 históricos y el vigente v9) existen en `/home/claude/` (fuera del repositorio); sus nueve SHA-256 (16 primeros caracteres) coinciden con el manifiesto del registro (líneas 36-44).
- La frase «Aceptación formal del addendum v3 (o correcciones).» figura **literal** en el campo «Decisión o información necesaria» del bloque PO-05 de los addendum v3, v4, v5, v6, v7, v8 y **v9 (vigente)**; no está en v1 ni v2. Es decir, la línea 126 reproduce fielmente el texto de la fuente; el «v3» es un residuo no actualizado dentro de la propia Adenda v9.
- Qué queda demostrado: el origen y la fidelidad de la línea 126. Qué NO se demuestra: que el propietario pretenda aceptar la v3 en lugar de la v9; v3 y v9 son documentos distintos con huellas distintas y no se declaran equivalentes.
- PO-05 no se modificó (punto reservado; el cambio, si procede, corresponde al propietario y alcanza también al texto de la Adenda v9).
- **Estado: origen explicado con fuente; inconsistencia textual persistente en la fuente; decisión pendiente del propietario** (confirmar que PO-05 se refiere a la Adenda v9 vigente). Archivo necesario para cualquier corrección: `ADDENDUM_DECISIONES_PROPIETARIO_OD01_OD16.md` (SHA-256 ccb1c546dfb62c1b…), que no está en el repositorio.

### 5. Lectura de los 780 escenarios
Matriz: `MATRIZ_ESCENARIOS_V19.csv`. Niveles: **L2** lectura semántica (343: los 330 no «Diseño» y 13 señalados por el cribado); **L3** vinculados por identificador a una prueba ejecutada PASS en el modelo (258; no se lee la equivalencia texto-prueba); **L1** solo estructura y cobertura bidireccional (179). No se leyeron semánticamente los 179 L1.
Escenarios que no demuestran todo lo que se les asocia (12): T-06 (no demuestra IG1-10), T-10 y T-47 (no IG1-21), T-03 (no IG1-05), T-124 (demostración débil de IP-05/IG5-09), T-166 (asociación débil con IG5-48), T-80 (asociación débil con IG5-27), y parciales T-137..T-140 (IG5-36) y T-78 (IG1-21, no citado en su cobertura). Varios escenarios con resultado «Rechazo» no identifican el mecanismo; no contradicen la regla. No se eliminó ni se alteró ningún escenario.

### 6. Estado final V19
| ID | Estado |
|---|---|
| HV-01 | Corregido (solo local) |
| HV-02 | Origen explicado con fuente; **requiere decisión del propietario** |
| S1, S1b | Corregidos (solo local) |
| Tablas: channel_formats sin columnas formales; l.1270 vs paso 8 | **No corregido; requiere decisión de diseño** |
| Cinco reglas E | **Abiertas**: 5 pruebas diseñadas, no ejecutables sin PostgreSQL |
| 153 reglas D | Abiertas: requieren aceptación del diseño por el propietario |
| 12 escenarios con demostración débil/parcial | Abiertos |
| 179 escenarios sin lectura semántica | **No verificable** (no leídos) |
| C08 | **NO APROBADO** |
