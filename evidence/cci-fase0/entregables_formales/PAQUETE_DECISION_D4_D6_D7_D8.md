# Paquete único de decisión D-4, D-6, D-7 y D-8 — 2026-11-22 (12:35)
> **Nota de corrección (2026-11-22, posterior a la revisión de ChatGPT).** La versión publicada en el commit `793d319` presentaba D5.a–d como «abiertas» y hacía depender D4.d de D5.c. Esas referencias se corrigieron conforme a la decisión del propietario: D-5 resuelta; D5.a–d fuera del alcance, sin condicionar D-4. Ninguna de las 11 decisiones queda resuelta por esta corrección. Ver `CONTROL_DE_CAMBIOS_CORRECCION_2026-11-22.md`.
**Sustituye** a `PAQUETE_DECISION_D1_D8.md` (12:30), cuyo alcance incluía D5.a–d: ese bloque quedó **fuera del alcance** por decisión del propietario. El anterior se conserva como histórico.
**Naturaleza:** análisis y propuesta. **No registra ni aprueba nada.** Toda «Recomendación» es propuesta mía.
**Procedencia:** **[S]** dicho por ti · **[D]** evidencia documental (A = instrucción Fase 0 de49cc27; B = instrucción maestra 5a9f5585; l. = línea; P1/P2/P3 = fichas resueltas) · **[P]** propuesta mía · **[I]** inferencia mía sin respaldo literal.
**Aclaración de estado:** con tu mensaje de 12:35, D-5 queda confirmada como **resuelta** (R3, conjunto (b), M-1). D5.a–d quedaron **expresamente fuera del alcance del paquete vigente**: no son decisiones pendientes, no se contabilizan como abiertas, no condicionan D-4 ni ninguna otra decisión y no se vuelven a preguntar.

---
## 1. Resumen ejecutivo
| Dep. | Qué falta decidir | Decisiones | Recomendación resumida [P] |
|---|---|---|---|
| D-4 | Cómo se delimita la Adaptación, su vínculo con Pieza, su definición mínima y si es aprobable | D4.a–d | A, A, A, A |
| D-6 | Qué es una Métrica: definición, valor, valor calculado y su coexistencia | D6.a–c | A, A, A |
| D-7 | Frontera Perfil local/Configuración; ubicación de tolerancias; Canales fijos o editables | D7.a–c | A, A, C |
| D-8 | Nombre de la entidad 16 | D8 | A (tras D6) |
**Total: 11 decisiones.** Ninguna alternativa crea entidades nuevas ni reabre D-1, D-2, D-3 o D-5.

## 2. Antecedentes preservados (sin reabrir)
D-1 (Adaptación = concepto propio derivado de copy fuente, nº 13; auditoría solo Copy y Pieza; Copy, Pieza y Adaptación versionables); D-2 (Variante = alternativa coexistente; Versión = evolución temporal; separadas; Variante sin versiones propias por ahora); D-3 (cuatro familias de reglas; solo ReglaDeMarca y ReglaComercial son entidades; reglas por canal = dimensión de aplicación del Canal; reglas de copy = familia conceptual con ubicación pendiente de P4.B); D-5 (R3; Copy y Pieza aprobables, Adaptación pendiente de D-4; M-1: la aprobación no certifica cumplimiento ni implica publicación); P1 (perfil local opcional con nombre visible opcional); P4.3 (existencia del Perfil local, no es componente de Configuración).

---
## 3. D-4 — Adaptación (entidad 13)
**Evidencia [D]:** B l.538–547 (canales, incluidos Banners, Landing y «otros formatos aprobados»); B l.563 «Copy fuente»; B l.673 y A l.44 (flujo hacia Revisión humana y Biblioteca); D-1.b/c/e; D-2; D-5.2.

### D4.a — Delimitación frente a Copy, Variante y Versión
- **A.** Concepto distinto de los tres, separado por criterio: Variante = alternativa del mismo contenido; Versión = evolución temporal; Adaptación = derivado de un copy fuente **para un canal destino**. No se decide si una adaptación puede tener variantes o versiones.
- **B.** Adaptación como tipo de Copy con canal. *Consecuencia:* contradice D-1.b; no es viable sin reabrirlo (por eso no lo recomiendo, pero lo muestro).
- **C.** Sin criterio hasta P4.B. *Consecuencia:* la definición de la 13 queda sin base.
- **D** (nueva). Delimitar solo frente a Copy y Variante ahora; frente a Versión en una decisión posterior del propietario. *Consecuencia:* progreso parcial, deja la relación con Versión abierta.
- Respaldo: A y D se apoyan en D-1.b y D-2.a [D]; que el criterio sea «canal destino» es [I] a partir de B l.563 y B l.538.
- **Recomendación [P]: A.** *Aprobaría:* el criterio distintivo. *No aprueba:* variantes/versiones propias de la Adaptación, cardinalidad, atributos, persistencia.

### D4.b — Vínculo con Pieza creativa
- **A.** Ninguna adaptación presupone una Pieza; el vínculo es posible y su forma va a P4.B.
- **B.** Las adaptaciones a canales visuales requieren Pieza. *Consecuencia:* presupone lo que indicaste no presuponer.
- **C.** Excluir toda relación Adaptación–Pieza. *Consecuencia:* choca con que Banners/Landing sean visuales [I].
- **D.** Diferir sin pronunciamiento. *Consecuencia:* la definición 13 no puede mencionar el vínculo.
- Respaldo: B l.545–546 [D]; que sean visuales es [I]. D-1.c [D] impide inferir auditabilidad.
- **Recomendación [P]: A.** *No aprueba:* relación, obligatoriedad, dirección ni auditabilidad.

### D4.c — Definición mínima de la entidad 13
- Texto propuesto [P] (si D4.a = A y D4.b = A): «**Adaptación de canal:** contenido derivado de un copy fuente y preparado para un canal destino, con identidad y trazabilidad propias; concepto distinto de Copy, Variante de copy y Versión de contenido. Puede relacionarse con una Pieza creativa cuando el canal sea visual.»
- **A.** Aprobar ese texto. **B.** Aprobarlo con tus ediciones. **C.** Diferir la definición.
- Respaldo: «identidad y trazabilidad» proviene de tu mensaje de 12:35 [S]; el resto de D-1.b [D].
- **Recomendación [P]: A.** *No aprueba:* atributos, relaciones, persistencia, aprobabilidad, auditabilidad ni el orden del flujo (B l.19 vs B l.673).

### D4.d — ¿Adaptación aprobable? (respetando D-5)
- **Base de evaluación:** D4.d se evalúa solo con las decisiones vigentes D-1, D-2 y D-5.3 (D-5.2 ya dejó la Adaptación pendiente de D-4). **No exige** ninguna resolución adicional de D-5. Que la Adaptación sea aprobable corresponde **exclusivamente a tu decisión** sobre D4.d; no está aprobada ni se da por resuelta.
- **A.** Aprobable, bajo los mismos límites de D-5.3 (no certifica cumplimiento, no implica publicación).
- **B.** No aprobable por ahora (la aprobación recae solo en Copy y Pieza).
- **C.** Diferir a P4.B/Fase 5.
- *Consecuencias:* A haría aprobable el contenido por canal (B l.673); B dejaría la adaptación fuera de la aprobación y sin lugar claro hacia la Biblioteca [I]; C conserva el estado actual (D-5.2: la Adaptación sigue sin decisión sobre su aprobabilidad).
- Respaldo: B l.673 [D]; que de ahí se derive aprobar la adaptación es [I].
- **Recomendación [P]: A.** *No aprueba:* mecanismo, identidad del contenido aprobado, relación con versiones, ni auditabilidad.

---
## 4. D-6 — Métrica
**Evidencia [D]:** A l.363–364 (`PerformanceRecord`, `Metric`); B l.210–211 («Resultados», «Métricas»); B l.635–651 (datos del usuario: Campaña, Canal, Contenido, Fecha, Impresiones, Clics, Conversiones, Inversión, Ventas; «distinguir datos manuales, importados y calculados»; «documentar fórmulas y evitar mostrar indicadores cuando no existan los datos necesarios»); tu definición aprobada de Campaña («Resultado de desempeño»). **Los originales no nombran ningún indicador de desempeño ni fórmula de desempeño** (la única fórmula es la de descuento, B l.519/521). Catálogo, fórmulas y mecanismos de cálculo: **sin respaldo y sin aprobar**.

**Qué significa «un Resultado contiene una métrica calculada» — lecturas posibles:**
- **L1.** El Resultado guarda solo datos ingresados; la métrica calculada se **deriva** de ellos al mostrarse [I; apoyo parcial en B l.651].
- **L2.** El Resultado guarda también el valor calculado [I; apoyo parcial en B l.649, que habla de «datos… calculados»].
- **L3.** El Resultado incluye una referencia a la definición de la métrica que originó el cálculo [I].
- **Respaldo literal:** solo que existen datos calculados (B l.649) y fórmulas documentadas (B l.651). Elegir entre L1, L2 y L3 **no está resuelto por la documentación**; por eso este paquete no lo decide y lo deja como límite en D6.c.

### D6.a — ¿Se distingue la definición de una métrica de su valor?
- **A.** Sí: dos conceptos distintos (definición = qué es el indicador y cómo se documenta; valor = lo que toma en un caso).
- **B.** No: Métrica = solo valor.
- **C.** No: Métrica = solo definición; los valores no son un concepto propio.
- *Consecuencias:* B vuelve innecesaria la fórmula documentada como concepto (B l.651) y cuestiona la entidad Métrica (P4.1); C no da lugar al «valor calculado» (B l.649).
- **Recomendación [P]: A.** *No aprueba:* atributos, fórmulas ni catálogo.

### D6.b — ¿Qué es un valor calculado?
- **A.** Un valor de métrica **cuyo origen es un cálculo** (frente a manual o importado, B l.649): distinción de origen, no un concepto separado.
- **B.** Un concepto distinto del valor, con identidad propia. *Consecuencia:* añade un concepto sin respaldo.
- **C.** No definirlo todavía. *Consecuencia:* queda sin responder la pregunta de B l.649.
- **Recomendación [P]: A.** *No aprueba:* mecanismo de cálculo, persistencia ni qué indicadores existen.

### D6.c — Coexistencia de definición y valor
- **A.** Coexisten **conceptualmente**: la entidad Métrica (17) corresponde a la definición; el valor (manual, importado o calculado) pertenece al Resultado (16). No se decide entre L1, L2 y L3 ni si el valor es una entidad aparte.
- **B.** Una sola entidad Métrica cubre definición y valores. *Consecuencia:* diluye la frontera con el Resultado.
- **C.** Solo valores; Métrica deja de ser entidad. *Consecuencia:* exige revisar expresamente P4.1 (no autorizado).
- **D.** Diferir a P4.B. *Consecuencia:* D8 no puede cerrarse con criterio.
- **Recomendación [P]: A.** *Aprobaría:* la coexistencia conceptual y la asignación de definición a Métrica. *No aprueba:* relación Métrica–Resultado, cardinalidad, atributos, fórmulas, catálogo, persistencia del valor calculado ni el campo «Contenido» (A-4, P4.B).

---
## 5. D-7 — Configuración y datos de referencia
**Evidencia [D]:** P1 [S: el perfil local incluye únicamente un nombre visible opcional, sin identidad autenticada]; P1/B l.51 y l.311 (Local Storage para preferencias ligeras; almacén `settings` ya existente); B l.234 (Local Storage no es base paralela); P2 (IndexedDB almacenamiento principal); P3 (históricos solo como referencia de vocabulario, no vinculante); B l.212 «Configuraciones»; B l.523 (tolerancias «configurables según decisión aprobada»); B l.538–556 (canales y reglas); D-3.b/c; D-1; D-2. **Q-1** (redondeo y tolerancias) y **Q-2** (canales y reglas) siguen pendientes y son decisiones tuyas aparte.
**Restricciones:** el Perfil local se mantiene como concepto propio; ninguna alternativa convierte Configuración, Perfil local o Canal en entidades adicionales (Canal y Configuración ya constan en las 18 por nombre).

### D7.a — Frontera Perfil local / Configuración
- **A.** Por naturaleza: Perfil local = datos de la persona usuaria local (hoy solo el nombre visible opcional); Configuración = preferencias de la aplicación.
- **B.** Por almacenamiento (lo ligero = Configuración). *Consecuencia:* mezcla concepto con almacenamiento y absorbe de hecho el Perfil local, lo que rechazaste.
- **C.** Diferir a P4.C.
- **D.** Declarar que no hay frontera que definir ahora (conceptos ya separados por P1/P4.3). *Consecuencia:* queda sin criterio para el futuro.
- Respaldo: A se apoya en P1 y P4.3 [D]; el criterio «naturaleza» es [P].
- **Recomendación [P]: A.** *No aprueba:* contenido de Configuración, más datos de Perfil, ni Local Storage vs IndexedDB.

### D7.b — Ubicación conceptual de las tolerancias (no sus valores)
- **A.** Parámetros de la **ReglaComercial** (D-3.b).
- **B.** Ajuste de **Configuración**.
- **C.** Parámetros asociados al **Canal** (reglas por canal, D-3.c), si la tolerancia varía por canal.
- **D.** Diferir hasta resolver Q-1.
- *Consecuencias:* A mantiene la tolerancia junto a la regla comercial que la usa [I]; B la separa de su regla y la vuelve global [I]; C supone que varía por canal, algo **sin respaldo** en B l.523 [I]; D no bloquea nada porque los valores ya esperan a Q-1.
- Respaldo: B l.523 («configurables») [D]; ubicación = [P].
- **Recomendación [P]: A** (solo conceptual). *No aprueba:* valores, redondeo, interfaz de edición, almacenamiento ni atributos. **Q-1 permanece pendiente.**

### D7.c — Canales: lista fija o editable
- **A.** Editable por la persona usuaria.
- **B.** Lista fija en código.
- **C.** Lista inicial aprobada + «otros formatos aprobados» (B l.547), con la forma de ampliarla diferida.
- **D.** Diferir hasta resolver Q-2.
- *Consecuencias:* A exige administración y reglas por canal editables (D-3.c); B contradice «otros formatos aprobados»; C respeta B l.547 sin fijar mecanismo; D deja la 12 sin criterio de variabilidad.
- Respaldo: B l.538–547 [D]; que «aprobados» sea aprobación del propietario es [I].
- **Recomendación [P]: C.** *No aprueba:* lista definitiva, reglas de canal, administración ni interfaz. **Q-2 permanece pendiente.**

---
## 6. D-8 — Nombre de la entidad 16 (`PerformanceRecord` no cambia como nombre técnico)
**Evidencia [D]:** A l.363; B l.210 «Resultados»; B l.635 «Registrar datos»; tu definición aprobada de Campaña («Resultado de desempeño»). **El nombre es independiente de la definición y de los atributos.**
- **A.** «Resultado de desempeño».
- **B.** «Registro de desempeño» (traducción literal).
- **C.** «Resultado» (B l.210).
- **D.** Diferir el nombre hasta P4.C.
- *Consecuencias:* A coincide con lo ya aprobado y se distingue de «Métrica» bajo D6.c = A; B es fiel al nombre técnico pero introduce un tercer término; C es corto pero ambiguo con «resultado de auditoría» [I]; D mantiene la tensión con la definición de Campaña.
- **Recomendación [P]: A**, **condicionada a D6.c**. Si D6.c = B o C el nombre debe reconsiderarse. *No aprueba:* definición de la 16, atributos, catálogo de métricas ni estructura de datos.

---
## 7. Revisión cruzada
| Eje | Hallazgo | Procedencia |
|---|---|---|
| Adaptación / Copy / Variante / Versión | D4.a = A es coherente con D-1.b y D-2.a; no hay contradicción | [D] |
| Adaptación y aprobación | D4.d = A respeta D-5.2 y D-5.3; D4.d no depende de ni condiciona ninguna cuestión adicional de D-5; se evalúa con D-1, D-2 y D-5.3 | [D] |
| Adaptación y auditoría | Ninguna alternativa la hace auditable (D-1.c) | [D] |
| Métrica / Resultado / nombre 16 | D6.c define la frontera; D8 depende de D6.c; la definición de Campaña ya usa «Resultado de desempeño» | [D] |
| Perfil local / Configuración | D7.a = A conserva P1 y P4.3 | [D] |
| Tolerancias / reglas comerciales / reglas por canal | D7.b = A usa D-3.b; D-3.c no se toca; C de D7.b es la única que cruza con reglas por canal y carece de respaldo | [D][I] |
| Canales / Adaptación / reglas por canal | D7.c define variabilidad del Canal; D4 usa el canal como destino; el contenido de las reglas de canal sigue en Q-2 | [D] |
| Q-1 / Q-2 | D-7 decide **dónde**, Q-1/Q-2 deciden **valores y canales**; ninguna se absorbe | [D] |
| Contradicciones con cerradas | Ninguna detectada en D-1, D-2, D-3, D-5 | verificado en registros |
| Falta de evidencia | indicadores y fórmulas de Métrica; lectura L1/L2/L3; variación de tolerancias por canal; contenido del Perfil más allá del nombre; forma de ampliar canales | [D] |

## 8. Matriz de dependencias cruzadas
| Ítem | Depende de | Condiciona |
|---|---|---|
| D4.a | D-1.b, D-2 | D4.c |
| D4.b | D-1.c, D4.a | D4.c |
| D4.c | D4.a, D4.b | entidad 13 |
| D4.d | D-1, D-2, D-5.3 (resueltas) | — (no condiciona ninguna otra decisión) |
| D6.a | P4.1 | D6.b, D6.c |
| D6.b | D6.a | D6.c |
| D6.c | D6.a, D6.b | D8 |
| D8 | D6.c | entidad 16 |
| D7.a | P1, P4.3 | entidades 12 y 18 |
| D7.b | D-3.b, Q-1 | entidad 11 |
| D7.c | D-3.c, Q-2 | entidad 12; D4 (canal destino) |
**Orden lógico:** D6.a → D6.b → D6.c → D8 · D4.a → D4.b → D4.c · D4.d (independiente de D4.a–c) · D7.a, D7.b, D7.c independientes. Los bloques D-4, D-6 y D-7 son independientes entre sí.

## 9. Propuesta de respuestas agrupadas (nada registrado)
- **D-4:** D4.a = A · D4.b = A · D4.c = A (o A con ediciones) · D4.d = A
- **D-6:** D6.a = A · D6.b = A · D6.c = A
- **D-7:** D7.a = A · D7.b = A · D7.c = C
- **D-8:** D8 = A
Fórmulas posibles: «Acepto todas las recomendaciones» o «Acepto todas salvo X = Y». Coherencia: D8 = A requiere D6.c = A; D4.c = A requiere D4.a = A y D4.b = A.

## 10. Asuntos que permanecen fuera
D5.a–d (decisión del propietario: fuera del alcance vigente; no pendientes, no abiertas, no se vuelven a preguntar); reapertura de D-1, D-2, D-3 y D-5; P4.B (relaciones, cardinalidades, Adaptación–Pieza, «Contenido» en Resultados A-4, Pieza–Copy A-5, reglas de copy, Variante en Biblioteca); P4.C (atributos, contenido de Perfil/Configuración); catálogo de métricas y fórmulas; valores de tolerancias (Q-1) y contenido de canales (Q-2); definición de las entidades 9 y 10–18 aún no presentadas; E1–E5; aprobaciones 0.1–0.7, aceptación de Fase 0 y Fase 1; rama pública y CCI-Evidence.

## 11. No verificado por mí
52 históricos de `docs/fase0` (solo búsquedas dirigidas); alineación de 05/06/07 con D-1/D-2/D-3/D-5; celdas antiguas de la matriz (prevalecen los avisos); pruebas, build, CI y `npm audit` (no re-ejecutados); otros navegadores distintos de Chrome 153; otras formulaciones de D-4 a D-8 previas a esta sesión; «19» = Evento de actividad (no asumido).
