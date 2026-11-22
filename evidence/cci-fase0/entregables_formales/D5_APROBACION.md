# D-5 — Aprobación: representación, objetos aprobables y alcance — RESUELTA (2026-11-22 12:29)
## Resultado de D-5 (decisiones del propietario, con sus límites)
| Sub-decisión | Decisión | Límite exacto |
|---|---|---|
| D-5.1 | **R3**: se distingue el **estado del contenido** (situación en el flujo) y la **aprobación** (decisión humana registrada) | No aprueba dos entidades independientes, fuente de verdad, relaciones, cardinalidades, atributos, mecanismos de transición ni almacenamiento; P4.1 intacta; una revisión del inventario sería decisión independiente |
| D-5.2 | **Conjunto (b)**: Copy y Pieza creativa **aprobables**; Adaptación **pendiente** de D-4 y de decisión expresa; Variante, Campaña, Brief, Producto y Oferta **fuera del alcance actual** | La exclusión no es permanente ni decide su aprobación futura; tener versiones no implica ser aprobable |
| D-5.3 | **M-1**: decisión humana final por la que un contenido concreto, en las condiciones en que fue revisado, está conforme para pasar a la Biblioteca | No certifica cumplimiento legal, comercial ni de marca; no sustituye auditorías ni validaciones; no implica publicación, distribución ni uso en canales externos; no fija si la auditoría o validación previa es obligatoria; no resuelve la modificación posterior ni la identificación técnica del contenido revisado ni su relación con las versiones |

**Siguen abiertas:** (1) si la aprobación requiere auditoría o validaciones previas; (2) qué ocurre al modificar un contenido aprobado; (3) relación con las versiones; (4) identidad exacta del contenido aprobado; (5) relación con los estados del flujo. Además, la definición de la entidad 15 no está presentada.

---
*Lo que sigue es el análisis original previo a la decisión, conservado como antecedente. Sus recomendaciones sobre mecanismos (p. ej., «contenido concreto en el estado en que se revisó») se adoptaron solo en los términos de arriba.*

**Naturaleza:** análisis y propuesta; **no aprueba nada.** No aprueba atributos, relaciones, cardinalidades, estados, flujos, mecanismos técnicos ni estructuras de datos. No desarrolla D-4 (reformulada y pendiente), D-6, D-7 ni D-8; no avanza a P4.B ni P4.C. **No asume** que el «19» de mi diagnóstico sea Evento de actividad (inferencia mía sin confirmar; queda retirada de este análisis). Referencias: A = Fase 0 (`de49cc27`), B = instrucción maestra (`5a9f5585`).

## 1. Hechos documentados (evidencia textual original)
- **Flujo:** «Brief → Copy → Adaptación creativa → Auditoría → Validación promocional → Corrección → **Aprobación humana** → Biblioteca → Medición» (B l.19; A l.44). Flujo de integración: «… → Channel Adaptation → **Revisión humana** → Biblioteca → Performance Intelligence» (B l.673). Los órdenes difieren (ya documentado en D-1.e).
- **Principios:** «Ninguna promoción debe aprobarse automáticamente por una sugerencia de IA» (B l.64); «La aprobación final es humana» (B l.65); «Las aprobaciones deben ser humanas» (A l.93).
- **Entidad:** «Aprobaciones» (B l.209); `Approval` (A l.362). Fase 5 incluye «aprobaciones» (B l.83).
- **Workflow & Approvals (Fase 5):** siete «Estados propuestos»: borrador, en revisión, requiere corrección, corregido, aprobado, rechazado, archivado (B l.609–617), «de acuerdo con el flujo aprobado» (B l.619); «No simular usuarios, permisos o aprobaciones multiusuario que no existen en la arquitectura local» (B l.621).
- **Versionado:** «No sobrescribir silenciosamente contenido aprobado» (B l.633); la adaptación conserva «Estado de revisión» (B l.569).
- **Biblioteca:** lista Campañas, Copys, Piezas, Versiones, Auditorías (B l.596–605); **no** lista Adaptaciones ni Aprobaciones.
- **Lo que no dicen:** a qué objeto se aplica la aprobación; qué significa exactamente; si requiere auditoría o validación previa; si CCI «publica» contenido (la búsqueda de «publicar» solo devuelve commits y releases, no contenidos). No distingue «Aprobación humana» (l.19) de «Revisión humana» (l.673).
- **No confundir:** las «aprobaciones» 0.1–0.7 de A l.842–882 y A l.8 son del gobierno del proyecto (tuyas), no la entidad Approval del producto.

## 2. Decisiones tuyas aplicables
- **P4.1:** el nombre `Approval` (entidad 15) está confirmado; cambiar su condición de entidad sería una revisión explícita de P4.1. Su definición no está presentada.
- **P1:** aplicación de un único usuario local; el Workflow & Approvals es de un único usuario local, sin cuentas ni roles.
- **D-1.d:** Copy, Pieza y Adaptación pueden tener versiones, pero **no** se aprueba que sean aprobables; «contenido aprobado» no basta. **D-1.c:** Auditoría solo sobre Copy y Pieza. **D-2:** Variante y Versión separadas; la Variante no tiene versiones propias por ahora ni se audita. **D-1.a:** «contenido» es concepto paraguas sin entidad.
- **D-4 reformulada:** la definición de la entidad 13 y su delimitación están pendientes.

## 3. Derivaciones razonables (D)
- **D-a** La aprobación es una **decisión humana final** que ocurre **después de revisar y corregir** y **antes de pasar a la Biblioteca**; la IA no la sustituye.
- **D-b** Existe a la vez un **conjunto de estados del contenido** (B l.609–617) y una **entidad «Aprobación»** (listas A y B): el texto menciona ambos, sin relacionarlos.
- **D-c** La aprobación debe poder referirse a **un contenido concreto en el estado en que se revisó**, porque se prohíbe sobrescribir en silencio el contenido aprobado (B l.633). Cómo se logra queda abierto.
- **D-d** Entre los objetos que pasan por el flujo, Copy y Pieza son los que se auditan y los que la Biblioteca conserva (indicio de aprobación **antes** de la Biblioteca); la Adaptación tiene «estado de revisión» y aparece antes de la «Revisión humana» en B l.673.
- **D-e** «Promoción» es el único objeto nombrado expresamente en una regla de aprobación (B l.64), pero no está definido y, por tu decisión, no equivale a Oferta.

## 4. Propuestas mías (P, **no aprobadas**)
Las alternativas, la recomendación y los significados de las secciones 5 a 8.

## 5. D-5.1 — ¿Registro, estado u otra representación?
| Alternativa | Idea | Consecuencias |
|---|---|---|
| **R1. Solo estado** | Aprobar es pasar a «Aprobado» dentro de los estados del contenido | No hay registro de la decisión; **la entidad 15 perdería su razón de ser** → revisión explícita de P4.1. Sencillo, pero no conserva quién/cuándo/qué se aprobó |
| **R2. Solo registro** | La aprobación es un hecho fechado: una decisión humana sobre un objeto | Conserva la entidad 15 (P4.1). Los estados de B l.609–617 quedarían sin lugar definido |
| **R3. Dos conceptos con papeles distintos** | **Estado** = situación del contenido en el flujo; **Aprobación** = decisión humana registrada, que puede dar lugar al cambio de estado | Conserva P4.1 y respeta ambos textos. Riesgo: divergencia entre estado y decisión; no se decide cuál es fuente de verdad ni cómo se vinculan |
| **R4. Aprobación como evento** | Sería una entrada del historial de actividad, sin entidad propia | Exigiría revisión de P4.1; mezcla la decisión con el registro general de actividad (no se asume relación con Evento de actividad) |

**Efectos comunes:** sobre Versión (14): la aprobación debe poder apuntar a un contenido en un estado concreto (D-c); sobre el usuario único: no hay «quién» distinto del propietario (P1; B l.621); sobre «no sobrescribir»: R2 y R3 dejan constancia de lo aprobado; R1 no.

## 6. D-5.2 — ¿Qué objetos pueden ser aprobables?
| Objeto | Evidencia | Grado | Observación |
|---|---|---|---|
| Copy | Flujo l.19; auditado; Library lo conserva; «contenido aprobado» (l.633) | Derivado, moderado | Versionable (D-1.d) |
| Pieza creativa | Ídem | Derivado, moderado | Versionable (D-1.d) |
| Adaptación | «Revisión humana» tras Channel Adaptation (l.673); «estado de revisión» (l.569) | Derivado, moderado | **Su definición mínima está pendiente (D-4 reformulada)**; no auditable (D-1.c) |
| Variante de copy | Ninguna | Sin evidencia | Sin versiones propias (D-2.b); sin auditoría (D-2.c) |
| Campaña, Brief, Producto | Ninguna (el Brief solo puede estar «incompleto») | Sin evidencia | No se excluye a futuro |
| Oferta / «promoción» | Solo el principio B l.64 | Objeto no definido | Oferta ≠ Promoción por tu decisión |

**Conjuntos posibles:** (a) Copy, Pieza y Adaptación · (b) Copy y Pieza ahora; Adaptación tras definir la entidad 13 en D-4 · (c) solo Adaptación (lectura de B l.673) · (d) no fijar objetos todavía.

## 7. D-5.3 — Significado y alcance de la aprobación
**Hechos:** humana, final, posterior a la corrección, previa a la Biblioteca, no sustituible por IA, sin multiusuario.
**Alternativas de significado:**
- **M-1.** Decisión humana final de que **un contenido concreto, en el estado en que se revisó**, queda conforme para continuar a la Biblioteca. **No** certifica por sí misma el cumplimiento de reglas ni sustituye validaciones deterministas ni la validación comercial (B l.396–397), y **no implica publicación** (no hay publicación de contenidos en las instrucciones).
- **M-2.** Autorización de uso o publicación del contenido: **sin respaldo textual**.
- **M-3.** Solo el cambio al estado «Aprobado», sin significado propio: es R1 y exigiría revisar P4.1.

**Alcance por objeto (bajo M-1):** Copy y Pieza: lo aprobado es el contenido tal como estaba al revisarse; Adaptación (si se decide, ver D-4): ídem; promoción (B l.64): sin objeto definido.
**Abierto (mecanismos, fuera de D-5):** si la aprobación exige auditoría o validación previas o se bloquea por hallazgos bloqueantes (B l.486, l.530); qué ocurre al modificar un contenido aprobado; relación con las versiones.

## 8. Recomendación y decisiones que necesito
- **D-5.1:** **R3**, dos conceptos con papeles distintos, sin decidir fuente de verdad ni vínculo (conserva P4.1 y los dos textos). Opciones: R1 (con revisión de P4.1) · R2 · **R3** · R4 (con revisión de P4.1) · otra.
- **D-5.2:** **conjunto (b)**: Copy y Pieza como objetos aprobables (derivación moderada); Adaptación se decide tras D-4 porque su definición está pendiente; Variante, Campaña, Brief, Producto y Oferta: no aprobables por ahora, sin excluirlos a futuro; la «promoción» de B l.64 se documenta como principio, sin definir objeto. Opciones: (a) · **(b)** · (c) · (d).
- **D-5.3:** **M-1**, como significado mínimo, sin aprobar mecanismos. Opciones: **M-1** · M-2 · M-3 (con revisión de P4.1) · otra.
- **Condición común:** ninguna de estas decisiones aprobaría estados, flujos, atributos, relaciones ni cardinalidades.

## 9. Sigue abierto
Fuente de verdad entre estado y decisión; relación con la Versión; si la aprobación depende de auditoría o validaciones; qué es una «promoción»; diferencia entre «Aprobación humana» (B l.19) y «Revisión humana» (B l.673); relación con Evento de actividad (no asumida); definición de la entidad 15.

## 10. No verificado
Que «promoción» no esté definida en otros pasajes (la búsqueda cubrió «aprob», «publica» y «bibliot»); el contexto exacto de «Estado» en la sección Versionado; la aplicación de los estados B l.609–617 a objetos concretos.
