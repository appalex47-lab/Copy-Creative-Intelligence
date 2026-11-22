# P4.A — Entidad 5 de 18: Copy — RESUELTA
Estado: **RESUELTA 2026-11-22 11:48 → (b)** con la definición mínima del propietario y el alcance exacto de `REGISTRO_DECISIONES_RESUELTAS.md`. La ficha conserva el planteamiento original.

**Nombre canónico:** `Copy` (lista A: `Copy`, l.352; B l.201 «Copys»).

**Definición propuesta (mínima):** Contenido textual que el usuario crea o escribe en Copy Studio, que puede editarse, guardarse, recuperarse y consultarse, y que puede ser auditado, validado y adaptado.

**Fuentes exactas:**
- A l.352 «Copy»; B l.201 «Copys» (lista de entidades).
- B l.337 Fase 2 «Copy Studio»; B l.414 «El usuario puede… generar o escribir copys…».
- B l.363–366 «Generación»: titulares, textos principales, descripciones, CTA.
- B l.374–383 «Editor»: crear, editar, duplicar, comparar, guardar, recuperar, etiquetar, buscar, exportar, consultar historial.
- B l.385+ «Reglas de copy» (longitud, ortografía, palabras obligatorias/prohibidas, consistencia, tono).
- B l.426 «Auditoría de copy»; B l.517 «Coherencia entre oferta y copy»; B l.563 «Copy fuente» (adaptación a canales); B l.598 «Copys» en la Creative Library; B l.19: flujo «Brief → Copy → …».

**Clasificación:**
- Nombre y existencia: solicitado.
- «El usuario crea/escribe copys»; contenido en forma de titulares, textos principales, descripciones y CTA; operaciones del editor; es objeto de auditoría y validación; es fuente de adaptaciones; se almacena en la Library: derivado de las citas.
- Que Copy tenga esos cuatro elementos como atributos, que «pertenezca a Brief/Campaña», sus cardinalidades con Variante y Versión, y su estado: **propuesta mía**, sin cita.

**Ambigüedades:**
1. B l.363–366 describe lo que se genera, no la forma del registro: un Copy podría ser un texto único con partes o un conjunto de piezas de texto. No está definido.
2. «Variantes» (B l.367–370) aparece junto a Generación; la entidad `CopyVariant` es la 6 y se resolverá aparte: no se decide aquí qué es variante y qué es copy.
3. «Consultar historial» (B l.383) apunta a versiones; `ContentVersion` es la entidad 14: relación pendiente.
4. «Generar» indica uso de IA (B l.414); cómo se identifica el origen (escrito/generado) no está definido y queda para la estrategia de IA.
5. Relación con Brief y Campaña: no citada como obligatoria (P4.B).
6. Fase: Fase 2 (B l.337); asignación formal → Q-4.

**Consecuencias si se aprueba la definición mínima:**
- Copy existe como entidad propia; sus partes, relaciones, estados y versiones quedan sin aprobar.
- Las entidades 6 (Variante) y 14 (Versión) deberán delimitarse frente a Copy cuando se presenten.
- Entra en persistencia y exportación como entidad propia (diseño sin aprobar).
- No se aprueban reglas de copy ni de auditoría.

**Recomendación mía:** aprobar la definición mínima sin aprobar la estructura interna ni las operaciones del editor como requisitos del modelo; delimitar Variante y Versión al presentarlas.

**Opciones:** (a) aprobar la definición mínima · (b) aprobar con cambios (indícalos) · (c) diferir o rechazar.
