# P4.A — Entidad 2 de 18: Brief — RESUELTA
Estado: **RESUELTA 2026-11-22 11:41 → (b)** con la definición mínima del propietario y el alcance exacto de `REGISTRO_DECISIONES_RESUELTAS.md`. La ficha conserva el planteamiento original.

**Nombre canónico:** `Brief` (lista A: `Brief`, l.349; B l.198 «Briefs»).

**Definición propuesta (mínima):** Requerimiento de contenido comercial que el usuario completa, y que reúne los datos de partida para crear un copy.

**Fuentes exactas:**
- A l.349 «Brief»; B l.198 «Briefs».
- B l.345–359: sección «Brief» con 13 campos listados: Campaña, Objetivo, Producto, Audiencia, Oferta, Beneficio, Vigencia, Condiciones, Tono, Mensaje central, Canal, Formato, CTA.
- B l.414 «El usuario puede… completar briefs…» (Fase 2).
- B l.402 «Briefs incompletos» (en Pruebas).
- B l.433 «Coherencia con brief» (criterio de auditoría).
- B l.19 / A l.44: flujo «Brief → Copy…».

**Clasificación:**
- Nombre y existencia: solicitado.
- «El usuario lo completa», los 13 campos como contenido del brief, existencia de briefs incompletos, flujo Brief → Copy, uso como referencia de coherencia en auditoría: derivado de las citas.
- Que el 13 sean atributos de la entidad con esos tipos, qué campos son obligatorios, qué estados tiene (incompleto/completo), cuál es la cardinalidad con Copy, y «pertenece a Campaña» (mi fila previa): **propuesta mía**.

**Ambigüedades:**
1. B l.347–359 lista los campos, no dice cuáles son obligatorios ni sus tipos. «Briefs incompletos» (l.402) indica que un brief puede estar incompleto, pero no define cómo se representa.
2. Campaña, Producto y Oferta aparecen como campos del brief: no dice si son referencias a entidades o texto. Campaña ya es entidad (Q-7); si el brief la referencia es obligatorio o no queda para P4.B.
3. «Vigencia» y «Condiciones» del brief podrían duplicar los de Oferta; tus instrucciones no lo resuelven.
4. Relación Brief–Copy: el flujo la sugiere; cardinalidad no citada (P4.B).
5. Fase: Fase 2 (B l.414); asignación formal → Q-4.

**Consecuencias si se aprueba la definición mínima:**
- Brief existe como entidad propia, con los 13 campos como contenido pretendido, sin aprobar tipos ni obligatoriedad (P4.C).
- Referencias a Campaña, Producto, Oferta y Copy se deciden en P4.B.
- Persistencia y exportación como entidad propia (diseño sin aprobar).
- Los briefs incompletos deberán poder guardarse (derivado de B l.402); cómo, queda para especificación.

**Recomendación mía:** aprobar la definición mínima sin enumerar los 13 campos como atributos aprobados; tratarlos como contenido citado, y decidir tipos y obligatoriedad en P4.C o en la especificación de Fase 2.

**Opciones:** (a) aprobar la definición mínima · (b) aprobar con cambios (indícalos) · (c) diferir o rechazar.
