# CCI — Ronda única de decisiones del propietario: D4, D6, D7 y D8
**Fecha:** 2026-11-22 · **Estado:** propuesta consolidada. **No registra ninguna decisión, no modifica el expediente ni el repositorio.** Las «Recomendaciones de Claude» **no son decisiones del propietario**.
**Versión:** esta matriz es la **corrección final** de la revisada por ChatGPT en el commit `836f9c40b1c04e1bdc7a1358e7003452a58a172e` (anterior a esta corrección, citado solo como antecedente). **Referencia vigente:** el HEAD de la rama `evidence/cci-fase0-review` que contiene esta corrección; su SHA se verifica por API y se indica en el mensaje de entrega (un archivo no puede contener el hash de su propio commit). **Es el único documento que el propietario debe responder**; `PAQUETE_DECISION_D4_D6_D7_D8.md` es solo antecedente de análisis.
**Procedencia:** **[S]** dicho por el propietario · **[D]** evidencia documental (A = instrucción Fase 0; B = instrucción maestra; l. = línea; ambas son adjuntos del propietario, no publicados en el repositorio) · **[P]** propuesta de Claude · **[I]** inferencia de Claude sin respaldo literal.

## 0. Cómo responder (una sola vez)
Responde con una línea por ID, por ejemplo: `D4.a = A; D4.b = A; … ; D8 = A`. Cada letra reproduce abajo su contenido exacto: **la letra significa aceptar ese contenido y solo ese**. La opción **Z** («otra decisión del propietario») siempre existe: escribe tu texto y se registrará literalmente. Lo no respondido queda pendiente.

## 1. Marco que no se reabre
- D-1, D-2, D-3 y D-5 resueltas (R3; conjunto (b): Copy y Pieza aprobables, Adaptación pendiente de D-4; M-1). D5.a–d fuera del alcance: no se preguntan ni condicionan nada.
- Adaptación = concepto propio derivado de un copy fuente, con identidad y trazabilidad propia, nº 13 (`ChannelAdaptation`) [S, D-1.b]. La auditoría creativa sigue limitada a Copy y Pieza [S, D-1.c]. Copy, Pieza y Adaptación pueden tener versiones, sin aprobar mecanismos [S, D-1.d]. «Adaptación creativa» = Channel Adaptation, lectura provisional [S, D-1.e].
- Variante = alternativa coexistente; Versión = evolución temporal; Variante sin versiones propias por ahora [S, D-2].
- Familias de reglas: copy, marca, comerciales y canal; solo ReglaDeMarca y ReglaComercial son entidades; reglas por canal = dimensión de aplicación del Canal [S, D-3].
- Perfil local: concepto propio, no componente de Configuración [S, P4.3 y 12:01]; contenido aprobado en P1: solo nombre visible opcional [S, P1].
- P4.A: 8/18 aprobadas; 9 Hallazgo y 10–18 pendientes. Q-1 y Q-2 abiertas.
- Aprobar una definición conceptual **no** aprueba atributos, relaciones, cardinalidades, estructura técnica, implementación ni fases.

---
## 2. D4 — Adaptación (entidad 13, `ChannelAdaptation`)
**Evidencia [D]:** B l.538–547 (canales Ecommerce, App, WhatsApp, Email, Redes sociales, Banners, Landing pages, «otros formatos aprobados»); B l.563 «Copy fuente»; B l.673 y A l.44 (flujo hacia Revisión humana y Biblioteca); D-1.b/c/d/e; D-2; D-5.2/5.3.

### D4.a — Delimitación entre Adaptación, Copy, Variante de copy y Versión
| ID | Pregunta | Alternativas completas | Recomendación | Consecuencia (aprueba / no aprueba) | Dependencias | Decisión |
|---|---|---|---|---|---|---|
| D4.a | ¿Qué distingue a una Adaptación de Copy, Variante y Versión? | **A.** Concepto distinto de los tres, separado por criterio: Variante = alternativa del mismo contenido; Versión = evolución temporal; Adaptación = derivado de un copy fuente **para un canal destino**. No se decide si una adaptación puede tener variantes o versiones. | **Recomendada [P]** | *Aprueba:* el criterio distintivo. *No aprueba:* variantes/versiones propias de la Adaptación, cardinalidad, atributos, persistencia. Coherente con D-1.b y D-2.a. El criterio «canal destino» procede de B l.538/563 [D/I]. | D-1.b, D-2 | ☐ |
| D4.a | (idem) | **B.** La Adaptación es un tipo de Copy con canal. | No recomendada | Contradice D-1.b («concepto propio»); **exige reabrir D-1**, algo que esta ronda no permite. Se muestra solo por completitud. | D-1.b | ☐ |
| D4.a | (idem) | **C.** Sin criterio hasta P4.B. | No recomendada | La definición D4.c queda sin base y la 13 no puede delimitarse. | P4.B | ☐ |
| D4.a | (idem) | **D.** Delimitar solo frente a Copy y Variante ahora y frente a Versión en una decisión posterior. | No recomendada | Deja una pregunta para otra ronda, contra el objetivo de decidir todo de una vez. | D-2 | ☐ |
| D4.a | (idem) | **Z.** Otra decisión del propietario. | — | Se registra literalmente; si choca con D-1/D-2 se señalará. | — | ☐ |

### D4.b — Relación posible entre una adaptación visual y Pieza creativa
| ID | Pregunta | Alternativas completas | Recomendación | Consecuencia | Dependencias | Decisión |
|---|---|---|---|---|---|---|
| D4.b | ¿Se reconoce un vínculo posible entre Adaptación y Pieza? | **A.** Ninguna adaptación presupone una Pieza; el vínculo es **posible**, no presupuesto; su existencia y forma se tratan en P4.B. | **Recomendada [P]** | *Aprueba:* que el vínculo puede existir. *No aprueba:* relación, obligatoriedad, dirección, cardinalidad ni auditabilidad (D-1.c). Cabe con canales visuales (Banners, Landing; B l.545–546 [D], que sean visuales: [I]). | D-1.c | ☐ |
| D4.b | (idem) | **B.** Las adaptaciones a canales visuales **requieren** una Pieza. | No recomendada | Presupone lo que indicaste no presuponer; introduce relación obligatoria. | — | ☐ |
| D4.b | (idem) | **C.** Se excluye toda relación Adaptación–Pieza. | No recomendada | Choca con la existencia de canales visuales [I]; cierra una puerta que P4.B debería poder evaluar. | — | ☐ |
| D4.b | (idem) | **D.** Sin pronunciamiento ahora. | No recomendada | La definición D4.c no puede mencionar el vínculo; queda para P4.B. | P4.B | ☐ |
| D4.b | (idem) | **Z.** Otra decisión del propietario. | — | Literal. | — | ☐ |

### D4.c — Definición mínima de la Adaptación (entidad conceptual 13, `ChannelAdaptation`)
**Texto exacto propuesto A [P]** (válido si D4.b = A):
«**Adaptación de canal:** contenido derivado de un copy fuente y preparado para un canal destino, con identidad y trazabilidad propias; concepto distinto de Copy, Variante de copy y Versión de contenido. Puede relacionarse con una Pieza creativa cuando el canal sea visual.»
**Texto exacto A′ [P]** (el mismo **sin** la última oración; **neutral** respecto del vínculo con Pieza: no lo afirma ni lo niega):
«**Adaptación de canal:** contenido derivado de un copy fuente y preparado para un canal destino, con identidad y trazabilidad propias; concepto distinto de Copy, Variante de copy y Versión de contenido.»
**Qué implica cada parte:**
- «contenido derivado de un copy fuente»: origen en un Copy [S, D-1.b]; no dice cardinalidad ni cómo se enlaza.
- «preparado para un canal destino»: asocia conceptualmente la adaptación con un Canal (B l.538, 563 [D]); **no es una relación obligatoria, ni define reglas de canal, ni estados**.
- «identidad y trazabilidad propias»: lo dijiste el 12:35 [S] y D-1.b; no fija atributos.
- «distinto de Copy, Variante de copy y Versión»: requiere D4.a = A.
- «Puede relacionarse con una Pieza…»: solo posibilidad; requiere D4.b = A. No es relación obligatoria.
- **Silencios deliberados:** no menciona aprobabilidad (D4.d), auditabilidad (D-1.c), versiones propias, estados, atributos, cardinalidades ni persistencia.
| ID | Pregunta | Alternativas completas | Recomendación | Consecuencia | Dependencias | Decisión |
|---|---|---|---|---|---|---|
| D4.c | ¿Qué definición mínima se aprueba para la 13? | **A.** Texto A (arriba, con la oración sobre Pieza). | **Recomendada [P]** | *Aprueba:* ese texto y solo ese. *No aprueba:* nada de lo listado como silencios. | D4.a = A y D4.b = A (con D4.b = B, C o D es incompatible) | ☐ |
| D4.c | (idem) | **A′.** Texto A′ (sin la oración sobre Pieza). | Alternativa neutral; compatible con cualquier D4.b | Aprueba una definición más corta; el vínculo con Pieza queda fuera de la definición. Con D4.b = B prevalece la decisión conceptual de D4.b (vínculo obligatorio), pues A′ lo omite sin negarlo. | D4.a = A | ☐ |
| D4.c | (idem) | **B.** El texto A o A′ con tus ediciones (escríbelas). | — | Se aprobará solo tu redacción literal. Su compatibilidad con D4.a, D4.b, D-1 y D-2 **no se declara ahora**: se valida con el texto exacto, y no puede reabrir D-1 ni D-2 de forma implícita. | Según el texto | ☐ |
| D4.c | (idem) | **C.** Diferir la definición. | No recomendada | La entidad 13 sigue «no presentada»; bloquea P4.B sobre la Adaptación. | — | ☐ |
| D4.c | (idem) | **Z.** Otra decisión del propietario. | — | Literal. | — | ☐ |

### D4.d — ¿Puede la Adaptación ser objeto de aprobación humana?
**Base de evaluación:** D-1, D-2 y D-5.3 (aprobación humana de un contenido concreto, en las condiciones revisadas, para pasar a la Biblioteca; **no** certifica cumplimiento legal, comercial o de marca; **no** autoriza publicación ni distribución). **No depende de D5.c** ni lo reabre. Qué versión exacta se aprueba y cómo se relaciona con las versiones **no está determinado** y no se pregunta aquí.
| ID | Pregunta | Alternativas completas | Recomendación | Consecuencia | Dependencias | Decisión |
|---|---|---|---|---|---|---|
| D4.d | ¿Es la Adaptación aprobable? | **A.** Sí, aprobable bajo los mismos límites de D-5.3. | **Recomendada [P]** (respaldo: B l.673 flujo Channel Adaptation → Revisión humana → Biblioteca [D]; que ello implique aprobar la adaptación es [I]) | *Aprueba:* que puede ser objeto de aprobación humana en esos términos. *No aprueba:* mecanismo, atributos, estados, relación con versiones, auditabilidad (D-1.c sigue: la adaptación no se audita). Consecuencia: puede llegar a la Biblioteca aprobada sin auditoría creativa propia, coherente con M-1 («no sustituye auditorías»). | D-1, D-2, D-5.3 | ☐ |
| D4.d | (idem) | **B.** No aprobable por ahora (la aprobación recae solo en Copy y Pieza). | No recomendada | La adaptación queda sin lugar claro hacia la Biblioteca [I]. | D-5.2 | ☐ |
| D4.d | (idem) | **C.** Diferir a P4.B/Fase 5. | No recomendada | Mantiene el estado actual de D-5.2 (pendiente). | — | ☐ |
| D4.d | (idem) | **Z.** Otra decisión del propietario. | — | Literal. | — | ☐ |

---
## 3. D6 — Métricas y valores calculados
**Evidencia [D]:** A l.363–364 (`PerformanceRecord`, `Metric`); B l.210–211 («Resultados», «Métricas»); B l.635–651: «datos proporcionados por el usuario»: Campaña, Canal, Contenido, Fecha, Impresiones, Clics, Conversiones, Inversión, Ventas; «distinguir datos manuales, importados y calculados»; «documentar fórmulas y evitar mostrar indicadores cuando no existan los datos necesarios»; tu definición aprobada de Campaña («Resultado de desempeño»). **Los originales no nombran ningún indicador de desempeño ni fórmula de desempeño** (la única fórmula es la de descuento, B l.519, que no es una métrica de desempeño). **Catálogo de indicadores, fórmulas y mecanismos de cálculo: sin respaldo y sin aprobar; esta ronda no los define.**

### Las tres interpretaciones de «un Resultado contiene una métrica calculada»
Los ejemplos usan solo los datos de B l.637–645 y son **ilustrativos; no proponen ningún indicador, fórmula ni mecanismo**. Cada interpretación es una dimensión distinta:
- **Dimensión de almacenamiento del valor calculado** (excluyentes entre sí): **L1** o **L2**.
  - **L1 — derivado al mostrarse, sin guardarlo.** El Resultado guarda solo los datos ingresados (p. ej. Impresiones y Clics de una fecha); cualquier cifra calculada a partir de ellos se obtiene al mostrarla y no se conserva. *Se gana:* no hay valores guardados que queden obsoletos. *Se pierde:* no hay histórico del valor que se vio; si cambia una fórmula, cambian las cifras del pasado [I]. Respaldo parcial: B l.651 (no mostrar indicadores sin datos) [D/I].
  - **L2 — valor calculado conservado en el Resultado.** Además de Impresiones y Clics, el Resultado conserva la cifra derivada marcada como «calculada». *Se gana:* histórico fiel y exportación/importación directas. *Se pierde:* riesgo de inconsistencia si cambian datos o fórmula; exige reglas de recálculo no definidas. Respaldo parcial: B l.649 habla de datos «calculados» junto a manuales e importados [D].
- **Dimensión de referencia** (independiente de la anterior): **L3 — el Resultado referencia la definición de la métrica que originó el cálculo.** *Se gana:* trazabilidad de la fórmula documentada (B l.651). *Se pierde:* exige una relación Resultado–Métrica, materia de P4.B y no aprobada; por sí sola no dice si el valor se guarda.
- **L3 puede combinarse con L1 o con L2.** L1 y L2 no pueden combinarse entre sí (uno no guarda el valor y el otro sí).
- **No determinable con los documentos:** cuál combinación corresponde a la intención del propietario; qué indicadores existirán; si «calculado» alude al valor mostrado o al guardado.

### D6.a — Definición de una métrica frente a valor de una métrica
| ID | Pregunta | Alternativas completas | Recomendación | Consecuencia | Dependencias | Decisión |
|---|---|---|---|---|---|---|
| D6.a | ¿Son conceptos distintos la definición de una métrica y su valor? | **A.** Sí: definición = qué es el indicador y cómo se documenta; valor = lo que toma en un caso. | **Recomendada [P]** | *Aprueba:* la distinción conceptual. *No aprueba:* atributos, fórmulas, catálogo. Da lugar a la «fórmula documentada» (B l.651) y al «valor» manual/importado/calculado (B l.649). | P4.1 (sin dependencia de otras decisiones) | ☐ |
| D6.a | (idem) | **B.** No: Métrica = solo valor. | No recomendada | La fórmula documentada no tiene lugar propio y cuestiona que Métrica sea entidad (P4.1). | P4.1 | ☐ |
| D6.a | (idem) | **C.** No: Métrica = solo definición; los valores no son un concepto propio. | No recomendada | No da lugar a «valor calculado» (B l.649) como concepto. | — | ☐ |
| D6.a | (idem) | **Z.** Otra decisión del propietario. | — | Literal. | — | ☐ |

### D6.b — Significado conceptual de «valor calculado»
| ID | Pregunta | Alternativas completas | Recomendación | Consecuencia | Dependencias | Decisión |
|---|---|---|---|---|---|---|
| D6.b | ¿Qué es un valor calculado? | **A.** Un valor de métrica **cuyo origen es un cálculo** (frente a manual o importado, B l.649); distinción de origen, no un concepto separado. | **Recomendada [P]** | *Aprueba:* esa lectura. *No aprueba:* mecanismo de cálculo, persistencia ni indicadores. | D6.a = A o B (debe existir el concepto de valor); incompatible con D6.a = C | ☐ |
| D6.b | (idem) | **B.** Un concepto distinto del valor, con identidad propia. | No recomendada | Añade un concepto sin respaldo documental. | D6.a = A o B | ☐ |
| D6.b | (idem) | **C.** No definirlo todavía. | No recomendada | Deja sin responder la distinción de B l.649; limita D6.c a A0, B, C o D. | D6.a = A o B | ☐ |
| D6.b | (idem) | **Z.** Otra decisión del propietario. | — | Literal; se valida frente a D6.a. | D6.a | ☐ |

### D6.c — Ubicación conceptual de `Metric` (entidad 17) y de sus valores
**Regla de dependencia única (idéntica a la sección 6):** A0 **no necesita** D6.b y **no presupone ni aprueba D6.b = A**: solo ubica los valores en el Resultado y **puede dejar pendiente** la clasificación del origen de los valores (manual, importado o calculado), incluido el de «calculado» (D6.b = C). A1 a A5 **sí requieren** un significado de «valor calculado» (D6.b = A o B; se recomienda A), porque deciden cómo se trata ese valor. Todas las alternativas A requieren D6.a = A.
**«Sin L3» en A1 y A2:** L3 **no se adopta ni se excluye**; queda para P4.B. **No se ofrece** una alternativa que excluya L3 expresamente (si la quieres, usa Z) ni L1+L2 (excluyentes).
| ID | Pregunta | Alternativas completas | Recomendación | Consecuencia: se aprueba / queda pendiente / se gana y se pierde | Dependencias | Decisión |
|---|---|---|---|---|---|---|
| D6.c | ¿Dónde se ubican la Métrica y sus valores? | **A0.** `Metric` = **definición de una métrica**; los **valores** pertenecen al **Resultado** (entidad 16). No se decide todavía: (i) la clasificación del origen de los valores (manual, importado o calculado), que puede quedar pendiente; (ii) si el valor calculado se conserva en el Resultado (L2) o se deriva al mostrarse sin conservarse (L1); y, de manera independiente, (iii) si el Resultado referencia la definición de la métrica que originó el cálculo (L3). A0 no presupone ni aprueba D6.b = A. | **Recomendada [P]** (recomendación previa; **no aprobada**) | *Aprueba:* solo la asignación conceptual (Metric = definición; los valores pertenecen al Resultado). *Pendiente:* clasificación del origen de los valores (D6.b), L1/L2, L3, relación Métrica–Resultado, cardinalidad, atributos, fórmulas, catálogo, persistencia. *Se gana:* frontera clara sin comprometer almacenamiento; P4.1 intacta. *Se pierde:* nada queda cerrado sobre cómo se guarda el calculado. | D6.a = A; D6.b: cualquier respuesta, incluida C (diferir); no presupone D6.b = A | ☐ |
| D6.c | (idem) | **A1.** A0 + **L1** (calculado derivado al mostrarse, no guardado); L3 sin adoptar ni excluir. | No recomendada | *Aprueba además:* que el valor calculado no se conserva. *Pendiente:* L3 y todo lo demás de A0. *Se gana:* sin valores obsoletos. *Se pierde:* sin histórico del valor mostrado. Decide almacenamiento sin respaldo documental [I]. | D6.a = A; D6.b = A o B | ☐ |
| D6.c | (idem) | **A2.** A0 + **L2** (calculado conservado en el Resultado); L3 sin adoptar ni excluir. | No recomendada | *Aprueba además:* que el Resultado conserva el calculado. *Pendiente:* L3, reglas de recálculo y todo lo demás de A0. *Se gana:* histórico. *Se pierde:* riesgo de inconsistencia. | D6.a = A; D6.b = A o B | ☐ |
| D6.c | (idem) | **A3.** A0 + **L3** (el Resultado referencia la definición que originó el cálculo); **L1/L2 explícitamente sin decidir**. | No recomendada | *Aprueba además:* que existe esa referencia conceptual. *Pendiente:* L1/L2, forma de la relación (P4.B). *Se gana:* trazabilidad de fórmula. *Se pierde:* fija una relación antes de P4.B sin saber si el valor se guarda. | D6.a = A; D6.b = A o B | ☐ |
| D6.c | (idem) | **A4.** A0 + **L1 + L3**. | No recomendada | *Aprueba además:* calculado derivado al mostrarse y referencia a la definición. *Pendiente:* forma de la relación (P4.B) y lo demás de A0. *Se gana:* sin obsoletos y con trazabilidad. *Se pierde:* sin histórico del valor mostrado; compromete relación antes de P4.B. | D6.a = A; D6.b = A o B | ☐ |
| D6.c | (idem) | **A5.** A0 + **L2 + L3**. | No recomendada | *Aprueba además:* calculado conservado y referencia a la definición. *Pendiente:* reglas de recálculo, forma de la relación (P4.B) y lo demás de A0. *Se gana:* histórico y trazabilidad. *Se pierde:* riesgo de inconsistencia; compromete relación antes de P4.B. | D6.a = A; D6.b = A o B | ☐ |
| D6.c | (idem) | **B.** Una sola entidad Métrica cubre definición y valores. | No recomendada | *Se gana:* simplicidad. *Se pierde:* mezcla la definición con muchos valores y diluye la frontera con el Resultado. L1/L2/L3 quedan sin decidir. | D6.a = A; D6.b: cualquiera | ☐ |
| D6.c | (idem) | **C.** Solo valores; `Metric` deja de ser entidad. | No recomendada | *Se gana:* minimalismo. *Se pierde:* una entidad confirmada en P4.1 y el lugar de la fórmula documentada; **requiere revisión expresa de P4.1, no autorizada en esta ronda** (solo con un «Z» expreso). | D6.a = B; revisión expresa de P4.1 | ☐ |
| D6.c | (idem) | **D.** Diferir. | No recomendada | D8 y las definiciones de las entidades 16 y 17 quedan sin criterio. | — | ☐ |
| D6.c | (idem) | **Z.** Otra decisión del propietario. | — | Literal; si choca con P4.1 se señalará. | — | ☐ |

---
## 4. D7 — Perfil local, Configuración, tolerancias y canales
**Evidencia [D]:** P1 (perfil local con nombre visible opcional, sin identidad autenticada); B l.51 y l.311 (Local Storage para preferencias ligeras); B l.234 (Local Storage no es base paralela); P2 (IndexedDB principal); B l.212 «Configuraciones»; B l.523 (tolerancias «configurables según decisión aprobada»); B l.538–556 (canales y reglas); D-3.b/c; entidades 11, 12 y 18 de A. **Ninguna alternativa crea entidades adicionales.**

### D7.a — Perfil local frente a Configuración
| ID | Pregunta | Alternativas completas | Recomendación | Consecuencia | Dependencias | Decisión |
|---|---|---|---|---|---|---|
| D7.a | ¿Cómo se distinguen Perfil local y Configuración? | **A.** Por naturaleza: Perfil local = datos de la persona usuaria local (hoy solo el nombre visible opcional, P1); Configuración = preferencias de la aplicación. Conceptos separados. | **Recomendada [P]** | *Aprueba:* el criterio de distinción. *No aprueba:* contenido de Configuración, más datos de Perfil, ni Local Storage vs IndexedDB. Conserva tu decisión de mantener Perfil local como concepto propio. | P1, P4.3 | ☐ |
| D7.a | (idem) | **B.** Por almacenamiento (lo ligero = Configuración). | No recomendada | Mezcla concepto con almacenamiento y absorbe de hecho el Perfil local, **contrario a tu decisión previa**; solo ejecutable con un «Z» expreso. | P4.3 | ☐ |
| D7.a | (idem) | **C.** Diferir a P4.C. | No recomendada | Sin criterio para definir las entidades 18 y el Perfil. | P4.C | ☐ |
| D7.a | (idem) | **D.** No definir frontera (ya están separados por P1/P4.3). | No recomendada | Sin criterio futuro de qué va en cada uno. | — | ☐ |
| D7.a | (idem) | **Z.** Otra decisión del propietario. | — | Literal. | — | ☐ |

### D7.b — Ubicación conceptual de las tolerancias (no sus valores)
| ID | Pregunta | Alternativas completas | Recomendación | Consecuencia | Dependencias | Decisión |
|---|---|---|---|---|---|---|
| D7.b | ¿Dónde viven conceptualmente las tolerancias del descuento? | **A.** Son **parámetros de la ReglaComercial** (D-3.b). | **Recomendada [P]** | *Aprueba:* ubicación conceptual. *No aprueba:* valores, redondeo, interfaz de edición, almacenamiento ni atributos. Mantiene la tolerancia junto a la regla que la usa [I]. **Q-1 sigue abierta:** el valor y el redondeo los decides tú. | D-3.b, Q-1 | ☐ |
| D7.b | (idem) | **B.** Ajuste global de Configuración. | No recomendada | La separa de la regla que la usa [I]. | D7.a | ☐ |
| D7.b | (idem) | **C.** Parámetros asociados al Canal (si varía por canal). | No recomendada | Supone variación por canal, **sin respaldo** en B l.523; cruza con D-3.c. | D-3.c, D7.c | ☐ |
| D7.b | (idem) | **D.** Diferir hasta resolver Q-1. | No recomendada | Sin criterio hasta Q-1; no bloquea nada técnico. | Q-1 | ☐ |
| D7.b | (idem) | **Z.** Otra decisión del propietario. | — | Literal. | — | ☐ |

### D7.c — Alcance de la lista de canales y formatos
**Alternativa C recomendada, con sus consecuencias:** los canales B l.538–547 forman una lista inicial; «otros formatos aprobados» (B l.547) queda reconocido como posible ampliación. **El documento no define quién aprueba un formato nuevo, dónde se registra ni si se hace desde la aplicación.** Por eso, bajo C, **no se fija ningún mecanismo**: un canal o formato nuevo entraría solo mediante una **decisión expresa del propietario** (junto con sus reglas, materia de Q-2) y su alta quedaría registrada documentalmente; **no se aprueba ninguna pantalla de edición ni catálogo editable**.
| ID | Pregunta | Alternativas completas | Recomendación | Consecuencia | Dependencias | Decisión |
|---|---|---|---|---|---|---|
| D7.c | ¿Los canales son lista fija o editable? | **C.** Lista inicial (Ecommerce, App, WhatsApp, Email, Redes sociales, Banners, Landing pages) más «otros formatos aprobados» por el propietario; sin mecanismo de ampliación definido. | **Recomendada [P]** | *Aprueba:* el alcance (inicial + ampliable por aprobación del propietario). *No aprueba:* la lista definitiva, reglas de canal, administración, interfaz ni mecanismo. «Aprobados = por el propietario» es [I]. **Q-2 sigue abierta:** canales y reglas reales. | D-3.c, Q-2 | ☐ |
| D7.c | (idem) | **A.** Catálogo editable por la persona usuaria. | No recomendada | Exige administración y reglas por canal editables (D-3.c); mecanismo no definido. | D-3.c, Q-2 | ☐ |
| D7.c | (idem) | **B.** Lista fija en código. | No recomendada | Contradice «otros formatos aprobados» (B l.547). | — | ☐ |
| D7.c | (idem) | **D.** Diferir hasta resolver Q-2. | No recomendada | La entidad 12 queda sin criterio de variabilidad. | Q-2 | ☐ |
| D7.c | (idem) | **Z.** Otra decisión del propietario. | — | Literal. | — | ☐ |

---
## 5. D8 — Nombre canónico de la entidad de resultados (`PerformanceRecord`; el nombre técnico no cambia)
**Evidencia [D]:** A l.363; B l.210 «Resultados»; B l.635 «Registrar datos»; tu definición aprobada de Campaña («Resultado de desempeño»). El nombre es independiente de la definición y de los atributos; **no aprueba catálogo de métricas ni estructura de datos**.
**Nombre que correspondería a cada escenario de D6.c (sin resolverlo por inferencia):**
- D6.c = A0 a A5: «Resultado de desempeño» (coincide con tu definición de Campaña) o, como alternativas, «Registro de desempeño» o «Resultado».
- D6.c = B: «Registro de desempeño» encaja mejor, porque la Métrica absorbería los valores y «resultado» se solaparía con ellos [I].
- D6.c = C: «Resultado de desempeño», que contendría los valores incluidos los calculados; pero C exige revisar P4.1.
- D6.c = D (diferir): D8 también se difiere.
| ID | Pregunta | Alternativas completas | Recomendación | Consecuencia | Dependencias | Decisión |
|---|---|---|---|---|---|---|
| D8 | ¿Qué nombre canónico lleva la entidad 16? | **A.** «Resultado de desempeño». | **Recomendada [P]** si D6.c = A0–A5 | *Aprueba:* el nombre. *No aprueba:* definición, atributos, métricas ni estructura. Coincide con la definición aprobada de Campaña y se distingue de «Métrica» (definición). | D6.c | ☐ |
| D8 | (idem) | **B.** «Registro de desempeño» (traducción literal). | Recomendada [P] solo si D6.c = B | Fiel al nombre técnico; introduce un tercer término. | D6.c | ☐ |
| D8 | (idem) | **C.** «Resultado». | No recomendada | Corto, pero ambiguo con «resultado de auditoría» [I]. | D6.c | ☐ |
| D8 | (idem) | **D.** Diferir el nombre. | Recomendada [P] solo si D6.c = D | Mantiene la tensión con la definición de Campaña. | D6.c | ☐ |
| D8 | (idem) | **Z.** Otra decisión del propietario. | — | Literal. | — | ☐ |

---
## 6. Combinaciones compatibles y dependencias cruzadas (única fuente de las reglas; las filas de cada decisión son idénticas)
### 6.1 D4
| Combinación | ¿Coherente? | Motivo y alternativa compatible |
|---|---|---|
| D4.a = A + D4.b = A + D4.c = A + D4.d = A | Sí | Conjunto recomendado. |
| D4.b = A + D4.c = A | Sí | El texto A expresa una posibilidad, coherente con D4.b = A. |
| D4.b = A + D4.c = A′ | Sí | La definición omite el vínculo; se trata en P4.B. |
| D4.b = B (vínculo obligatorio) + D4.c = A | **No** | «Puede relacionarse» no expresa obligatoriedad. Compatible: D4.c = A′ o B/Z con redacción adecuada. |
| D4.b = B + D4.c = A′ | No contradictorias por sí mismas | A′ omite el vínculo sin negarlo; prevalece la decisión conceptual de D4.b. |
| D4.b = C (excluir vínculo) + D4.c = A | **No** | A afirma la posibilidad de relación. Compatible: D4.c = A′. |
| D4.b = C + D4.c = A′ | Sí | A′ es neutral. |
| D4.b = D (sin pronunciamiento) + D4.c = A | **No** | A afirma una posibilidad sobre la que no se decidió. Compatible: D4.c = A′. |
| D4.b = D + D4.c = A′ | Sí | A′ es neutral. |
| D4.b = cualquiera + D4.c = B o Z | **Sin compatibilidad automática** | Se evalúa con el texto exacto escrito por el propietario; no puede reabrir D-1 ni D-2 de forma implícita. |
| D4.a ≠ A + D4.c = A o A′ (**solo los textos fijos**) | **No** | Ambos textos afirman la distinción de D4.a = A. Con B/Z la compatibilidad depende de la redacción concreta. |
| D4.a = B | **No** | Contradice D-1.b y **no puede aprobarse sin una reapertura expresa de D-1, que esta ronda no autoriza**. Compatible: D4.a = A. |
| D4.d (cualquiera) con D4.a–c | Sí | D4.d es independiente; solo exige respetar D-5.3. |
### 6.2 D6 y D8
| Combinación | ¿Coherente? | Motivo y alternativa compatible |
|---|---|---|
| D6.a = A + D6.b = A + D6.c = A0 | Sí | Conjunto recomendado. |
| D6.c = A0 + D6.b = C (diferir) | Sí | A0 no clasifica el origen de los valores ni aprueba D6.b = A; esa clasificación queda pendiente. |
| D6.c = A0 + D6.b = A, B o Z | Sí | A0 no presupone D6.b = A, pero es compatible con cualquier respuesta; se aprueba la asignación de A0 y, aparte, la respuesta dada a D6.b. |
| D6.c = A1…A5 + D6.b = C | **No** | Eligen cómo tratar el valor calculado sin haberlo definido. Compatible: D6.b = A, o D6.c = A0. |
| D6.c = A1…A5 + D6.b = A o B | Sí | Hay significado de «valor calculado». |
| D6.c = A1…A5 o A0 o B + D6.a = B o C | **No** | Presuponen definición y valor distintos. Compatible: D6.a = A. |
| D6.c = C + D6.a = A | **No** | C elimina la entidad de definición. Compatible: D6.a = B y revisión expresa de P4.1 vía «Z». |
| D6.b (A, B o C) + D6.a = C | **No** | Sin concepto de valor no existe «valor calculado». Compatible: D6.a = A o B. |
| L1 + L2 (ninguna alternativa las combina) | **No** | Excluyentes: una no guarda el valor y la otra sí. |
| L3 con L1 o con L2 (A4, A5) | Sí | L3 es independiente del almacenamiento. |
| D8 = A + D6.c = A0…A5 | Sí | Conjunto recomendado. |
| D8 = A + D6.c = B | Sí, menos coherente | Con B encaja mejor D8 = B («Registro de desempeño»). |
| D8 = A/B/C + D6.c = D | **No** | Con D6.c diferida, el nombre no tiene criterio. Compatible: D8 = D. |
### 6.3 D7
| Combinación | ¿Coherente? | Motivo y alternativa compatible |
|---|---|---|
| D7.a = A + D7.b = A + D7.c = C | Sí | Conjunto recomendado. |
| D7.a = B | **No** sin «Z» expreso | Contradice tu decisión de mantener Perfil local como concepto propio. |
| D7.b = C + D7.c = A/B/D | Sí, con reservas | Supone que la tolerancia varía por canal; sin respaldo; depende de Q-2. |
### 6.4 Dependencias cruzadas (idénticas a la columna «Dependencias» de cada fila)
D4.c-A ← D4.a = A y D4.b = A · D4.c-A′ ← D4.a = A (neutral frente a D4.b) · D4.c-B/Z ← según el texto · D4.d ← D-1, D-2, D-5.3 · D6.a ← P4.1 · D6.b ← D6.a = A o B · D6.c-A0 ← D6.a = A (D6.b: cualquier respuesta; no presupone D6.b = A) · D6.c-A1…A5 ← D6.a = A y D6.b = A o B · D6.c-B ← D6.a = A · D6.c-C ← D6.a = B y revisión expresa de P4.1 · D6.c-D ← ninguna · D8 ← D6.c · D7.b ← D-3.b, Q-1 · D7.c ← D-3.c, Q-2. Los bloques D4, D6 y D7 son independientes entre sí.

## 7. Qué permanece pendiente tras tu respuesta
Q-1 (valores de redondeo y tolerancias) y Q-2 (canales reales y sus reglas); P4.B (relaciones y cardinalidades: Adaptación–Pieza, Métrica–Resultado, «Contenido» en Resultados A-4, Pieza–Copy A-5, ubicación de reglas de copy, Variante en Biblioteca); P4.C (atributos); entidad 9 Hallazgo y entidades 10–18; E1–E5; aprobaciones 0.1–0.7, aceptación de Fase 0 y Fase 1. Todo catálogo de indicadores y toda fórmula de desempeño.
**No puede determinarse con la documentación:** la lectura L1/L2/L3 deseada; los indicadores existentes; quién aprueba un canal nuevo y cómo se registra; cuántos datos tendrá el Perfil más allá del nombre; si la tolerancia varía por canal.

## 8. Plantilla de respuesta (copiar y completar)
`D4.a = _ ; D4.b = _ ; D4.c = _ ; D4.d = _ ; D6.a = _ ; D6.b = _ ; D6.c = _ ; D7.a = _ ; D7.b = _ ; D7.c = _ ; D8 = _`
Conjunto recomendado por Claude (no aprobado): `D4.a = A; D4.b = A; D4.c = A; D4.d = A; D6.a = A; D6.b = A; D6.c = A0; D7.a = A; D7.b = A; D7.c = C; D8 = A`. Cada letra significa aceptar exactamente el contenido reproducido en su fila. Para D6.c las opciones son A0, A1, A2, A3, A4, A5, B, C, D o Z.

## 9. Fuentes (rama `evidence/cci-fase0-review`)
Base: https://github.com/appalex47-lab/Copy-Creative-Intelligence/tree/evidence/cci-fase0-review/evidence/cci-fase0
- Paquete vigente: `entregables_formales/PAQUETE_DECISION_D4_D6_D7_D8.md` · Índice: `00_INDICE_VIGENTES_E_HISTORICOS.md` · Control de cambios: `entregables_formales/CONTROL_DE_CAMBIOS_CORRECCION_2026-11-22.md`
- Decisiones: `entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md`, `D1_ANALISIS_CONTENIDO.md`, `D2_VARIANTE_FRENTE_A_VERSION.md`, `D3_FAMILIAS_DE_REGLAS.md`, `D5_APROBACION.md`
- Entidades: `entregables_formales/FICHA_P4A_01_CAMPANA.md` … `FICHA_P4A_08_AUDITORIA_CREATIVA.md`, `FICHA_P4A_09_HALLAZGO.md`, `MATRIZ_CONSOLIDADA_18_ENTIDADES.md`, `CATALOGO_DEPENDENCIAS_D4_D8.md`
- P1/P2/P3: `entregables_formales/FICHA_P1.md`, `FICHA_P2.md`, `FICHA_P3.md`; Q-1/Q-2: `10_REGISTRO_DECISIONES.md`
- Instrucciones A y B: adjuntos del propietario (no publicados).

## 10. No verificado
Contenido de los 52 históricos de `docs/fase0`; alineación de 05/06/07 con las decisiones cerradas (solo advertidos); pruebas, build, CI; acceso de ChatGPT a la rama; existencia de `CCI-Evidence`; que el «19» sea Evento de actividad (no asumido).
