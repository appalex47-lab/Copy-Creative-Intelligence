# D-2 — Variante de copy frente a Versión (ContentVersion) — RESUELTA (2026-11-22 12:09)
## Resultado de D-2 (decisiones del propietario, con sus límites)
| Sub-decisión | Decisión | Límite exacto |
|---|---|---|
| D-2.a | **A**: conceptos separados. Variante = alternativa de contenido textual que puede coexistir con otras; Versión = evolución o revisión temporal de un contenido | Mantiene vigente la existencia de Variante (P4.A); no aprueba relaciones, cardinalidades, atributos, estructuras, mecanismos de versionado ni ciclo de vida |
| D-2.b | **(ii)**: la Variante no tiene versiones propias por ahora | No se prohíbe a futuro; requiere justificación funcional y decisión posterior |
| D-2.c | **(a)**: no ampliar Auditoría creativa | Sigue sobre Copy o Pieza; auditar una Variante directamente requiere decisión expresa |

**Siguen pendientes:** relaciones y cardinalidades entre Copy, Variante y Versión; presencia de Variante en la Creative Library; definición de ContentVersion (solo el nombre está confirmado); D-3 y D-5. Entidades 1–8 y D-1 intactas; Hallazgo (9) sin aprobar.

---
*Lo que sigue es el análisis original previo a la decisión, conservado como antecedente.*

**Naturaleza:** análisis y propuesta; **no aprueba nada.** No cambia las entidades 1–8 ni D-1; no decide D-3 ni D-5; no aprueba atributos, relaciones, cardinalidades ni mecanismos de versionado. Referencias: A = Fase 0 (`de49cc27`), B = instrucción maestra (`5a9f5585`).

## 1. Pregunta central
¿Variante de copy y Versión son conceptos distintos y necesarios, o hay duplicidad?
**Veredicto de la evidencia:** los nombres están separados en **ambas** listas (B l.202 «Variantes» y l.208 «Versiones»; A l.353 `CopyVariant` y l.361 `ContentVersion`), y cumplen **papeles distintos en el texto** (generación frente a historial). Las instrucciones **no definen la frontera**; hay que decidirla.

## 2. Evidencia textual original (E)
**Variante**
- B l.202 «Variantes»; A l.353 `CopyVariant`.
- B l.367–370, bajo «Generación»: «Variantes», «Alternativas de tono», «Variantes por objetivo», «Propuestas A/B».
- B l.405 «Variantes» en las pruebas de Fase 2; B l.414 «administrar variantes persistentes»; A l.512 y A l.578 («Variantes» junto a «Generación de copy» y, en A l.512, a «Reescritura»).
- Editor de Copy Studio: duplicar (B l.376), comparar (l.377), guardar, recuperar, consultar historial (l.378–383). El texto **no dice** si «duplicar/comparar» se refieren a variantes o a versiones.
- **No hay ninguna mención de variantes** en Fase 3 (auditoría), Fase 4 ni Fase 5, ni en la Creative Library (B l.596–605).

**Versión**
- B l.208 «Versiones»; A l.361 `ContentVersion`.
- Principio: «Las versiones deben conservar trazabilidad» (B l.68; A l.96).
- Creative Library: «Versiones» (B l.603).
- Sección «Versionado» (B l.623–631): historial, comparación, fecha, cambios, estado, auditorías vinculadas, motivos de modificación; cierre: «No sobrescribir silenciosamente contenido aprobado» (B l.633).
- Corrección (Fase 3): reauditar, «Comparar versiones», conservar historial (B l.475–477). Adaptación: «Versión» entre lo que se conserva (B l.566).
- Mención técnica distinta (formato de respaldo): «Versionado» en A l.447 (apartado de respaldo). Otras menciones de «Versionado» (B l.222, 232; A l.320, 405, 611) y «Historiales» (A l.420) **no verifiqué su contexto**; no las uso.

## 3. Decisiones tuyas ya aprobadas y aplicables
- **Variante de copy (6):** «alternativa de contenido textual contemplada en el proceso de creación y generación de copy, que el usuario puede administrar y conservar de forma persistente». Reconociste tono, objetivo y A/B como modalidades, sin tipos definitivos. **No aprobaste** equivalencia ni distinción técnica con ContentVersion; esa delimitación «debe resolverse antes de especificar el modelo».
- **D-1.d:** Copy, Pieza y Adaptación **pueden tener versiones** (sin estructuras ni mecanismos). **La Variante no quedó incluida ni excluida.**
- **Auditoría creativa (8) y D-1.c:** limitada a Copy o Pieza; auditar adaptaciones no aprobado; objeto directo o por versión sin resolver.
- **ContentVersion (14):** solo está confirmado el **nombre** (P4.1); no tiene definición aprobada.

## 4. Derivaciones razonables (D)
- **D-a** La variante es un **resultado de generación** (humana o con IA): alternativas **coexistentes** del mismo copy que difieren en tono, objetivo o propuesta de prueba (E de variante). La dimensión que las distingue es el **propósito**.
- **D-b** La versión es una **sucesión en el tiempo**: fecha, cambios, motivos y estado, y se enlaza a auditorías (B l.625–631, l.475–477).
- **D-c** Las auditorías se vinculan a versiones (B l.630), no a variantes; las variantes no aparecen en Fase 3.
- **D-d** La Library conserva versiones, no variantes (B l.596–605): la variante parece un concepto de **trabajo en Copy Studio**; la versión, uno **transversal** (Library, adaptación, auditorías).
- **D-e** Sin texto sobre: si una variante tiene historial, si se «elige» una variante, ni cómo se relaciona con el contenido aprobado.
- **Antecedente histórico no vinculante (P3; solo búsqueda dirigida, no lectura completa):** en `docs/fase0` (Supabase) el roadmap usa `copy_versions` inmutables para la «Generación de propuestas» (ROADMAP_Y_TRAZABILIDAD_G1_G5_G10, tabla de la fase 2.3, l.86–92 y l.163) y **no tiene tabla de variantes**; la «Comparación de variantes (A/B)» aparece solo en la fase 8.4 con `ab_tests`, marcada NO INICIADA, NO AUTORIZADA (l.289).

## 5. Tus cinco interpretaciones, frente a la evidencia
| Interpretación | Respaldo |
|---|---|
| Variante = alternativa que coexiste con otras | **Fuerte** (alternativas de tono, objetivo, A/B) |
| Versión = revisión temporal de un contenido | **Fuerte** (historial, fecha, cambios, motivos) |
| Variante con su propio historial de versiones | **Sin texto**; plausible; D-1.d no la reconoce |
| Variante = versión etiquetada por propósito | **Parcial**: el propósito caracteriza a la variante, pero el motivo de una versión es el *motivo del cambio*, no su propósito; y coexistencia ≠ sucesión |
| Versión suficiente para alternativas y cambios | **Posible técnicamente** (ramas), sin respaldo textual; el antecedente histórico lo hizo así, pero es no vinculante |

## 6. Propuestas mías (P, **no aprobadas**)
- **P-1** Criterio de distinción: la variante es un eje **horizontal** (alternativas simultáneas con propósito); la versión es un eje **vertical** (tiempo).
- **P-2** Mis documentos `05`, `06` y `07` ya proponían «Copy 1–N Variante» y «Copy/Variante 1–N Versión», con almacenes `variants` y `versions`. Es propuesta mía, sin aprobar; se ajustaría según lo que decidas.

## 7. Alternativas y consecuencias
**A. Conceptos separados** (variante = alternativa; versión = evolución temporal). Sub-pregunta: ¿la variante tiene versiones propias? (D-2.b).
**B. Un solo concepto.** Exigiría **revisión explícita de P4.1** (desaparecería el nombre 6 o el 14) y de tu aprobación de la entidad 6. No la propongo ni la asumo.
**C. Variante como clasificación de una versión.** Retiraría la entidad conceptual 6: también requiere **revisión explícita de P4.1 y de la entidad 6**.

| Aspecto | A. Separados | B. Unificados | C. Variante = clasificación de versión |
|---|---|---|---|
| **Copy** | Tiene alternativas **y** historial (dos ejes) | Un solo eje: todo es versión | Copy tiene versiones; la «variante» es una etiqueta de ellas |
| **Variante de copy** | Entidad propia, conservada (como aprobaste) | Desaparece o se absorbe | Sin identidad propia; contradice «entidad propia» (6) |
| **ContentVersion** | Estado temporal de Copy, Pieza y Adaptación (D-1.d) | Cubre además las alternativas | Lleva una clasificación (tono/objetivo/A-B) |
| **Auditoría creativa** | Audita Copy/Pieza (como aprobaste); la variante **no** quedaría auditada directamente (huecos que decidir) | Se audita «una versión»: resuelve el hueco, pero cambia el sentido de 8 | Igual que B |
| **Creative Library** | Conserva versiones (B l.603); la variante no figura en la Library (hueco a decidir en P4.B) | Versiones lo cubren todo | Versiones lo cubren todo |
| **Trazabilidad e historial** | Dos ejes: alternativas simultáneas e historial; riesgo de confundirlos | Un eje: las alternativas parecen una sucesión (sugiere orden o reemplazo que no hay) | Un eje con ramas; «Historial» y «Propuestas A/B» se mezclan |

## 8. Recomendación: **A, conceptos separados**
Justificación: (1) tus dos listas los nombran por separado; (2) el texto les da papeles distintos (generación frente a historial; la variante no aparece en Library ni en auditoría, la versión sí); (3) B y C obligarían a revisar P4.1 y la aprobación de la entidad 6, que acabas de dejar vigentes; (4) mantiene la distinción coexistencia/sucesión que la evidencia sostiene.

## 9. Decisiones concretas que necesito
- **D-2.a** ¿Adoptas A como principio conceptual (variante = alternativa coexistente con propósito; versión = evolución temporal), **sin aprobar mecanismos**? Opciones: A (recomendada) · B · C (con revisión explícita de P4.1 y de la entidad 6) · otra.
- **D-2.b** ¿La Variante puede tener versiones propias? (i) sí · (ii) **no por ahora**, sin excluirlo a futuro (**recomendada**: D-1.d solo reconoció Copy, Pieza y Adaptación) · (iii) diferir a P4.B/P4.C.
- **D-2.c** Auditoría de variantes: (a) **no ampliar por ahora** la Auditoría creativa (**recomendada**, coherente con D-1.c) · (b) ampliarla a variantes, lo que exigiría tu autorización expresa para modificar la definición de la entidad 8.

## 10. Sigue abierto (no se resuelve aquí)
Relaciones y cardinalidades entre Copy, Variante y Versión; presencia de Variante en la Library; «adopción» o elección de una variante; D-3 y D-5; qué significan «duplicar» y «comparar» en el editor.

## 11. No verificado
Los 52 archivos de `docs/fase0` no se leyeron completos: solo hice búsquedas dirigidas de «variante», `CopyVariant`, `ContentVersion` y `copy_versions`. Los contextos de las menciones técnicas de «Versionado» y «Historiales» arriba indicadas no se verificaron.
