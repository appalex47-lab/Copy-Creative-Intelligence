# P4.A — Entidad 6 de 18: Variante de copy (CopyVariant) — RESUELTA
Estado: **RESUELTA 2026-11-22 11:51 → (b)** con la definición mínima del propietario y el alcance exacto de `REGISTRO_DECISIONES_RESUELTAS.md`. La ficha conserva el planteamiento original.

**Nombre canónico:** `Variante de copy` (lista A: `CopyVariant`, l.353; B l.202 «Variantes»).

**Definición propuesta (mínima):** Alternativa de un contenido textual (Copy), que el usuario puede crear y conservar.

**Fuentes exactas:**
- A l.353 «CopyVariant»; B l.202 «Variantes» (lista de entidades).
- B l.367–370, bajo «Generación»: «Variantes», «Alternativas de tono», «Variantes por objetivo», «Propuestas A/B».
- B l.414: «El usuario puede… administrar variantes persistentes» (Fase 2).
- Menciones en listas: B l.405 (Pruebas); A l.512 y l.578 («Variantes» junto a «Generación de copy»).

**Clasificación:**
- Nombre y existencia: solicitado.
- «Hay variantes de copy», «pueden ser alternativas de tono, por objetivo o propuestas A/B» y «el usuario las administra y se persisten»: derivado de las citas.
- Que una Variante «pertenezca a un Copy», su cardinalidad, sus atributos, su estado y cómo se compara con el Copy original: **propuesta mía**, sin cita.

**Ambigüedades:**
1. Tus instrucciones no dicen si una variante es un Copy completo con relación a otro Copy, o un registro distinto subordinado a un Copy. Esa delimitación frente a Copy (entidad 5, aprobada solo en forma mínima) no está definida.
2. Los tres tipos citados (tono, objetivo, A/B) pueden ser clasificaciones de una misma entidad o conceptos distintos; no se especifica.
3. «Propuestas A/B» sugiere comparación entre alternativas; CCI es browser-only y no mide por sí mismo pruebas A/B (los resultados los aporta el usuario, B l.635–649): el alcance de «A/B» no está definido.
4. Relación con Copy, ContentVersion (entidad 14) y Canal: no citada (P4.B).
5. Fase: Fase 2 (B l.414); asignación formal → Q-4.

**Consecuencias si se aprueba la definición mínima:**
- CopyVariant existe como entidad propia; no se decide si una variante es un Copy o algo subordinado.
- La delimitación frente a Copy y a ContentVersion queda abierta hasta P4.B.
- Entra en persistencia y exportación como entidad propia (diseño sin aprobar).
- No se aprueban clasificaciones (tono, objetivo, A/B) ni reglas de comparación.

**Recomendación mía:** aprobar la definición mínima (alternativa de un Copy, creada y conservada por el usuario) sin aprobar tipos ni estructura; decidir en P4.B si la relación con Copy es de pertenencia.

**Opciones:** (a) aprobar la definición mínima · (b) aprobar con cambios (indícalos) · (c) aprobar el nombre pero tratar las variantes como un Copy más (sin entidad propia) · (d) diferir o rechazar.
