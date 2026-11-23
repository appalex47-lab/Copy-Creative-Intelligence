# P4.A — Entidad 4 de 18: Oferta (Offer) — RESUELTA
Estado: **RESUELTA 2026-11-22 11:47 → (b)** con la definición mínima del propietario y el alcance exacto de `REGISTRO_DECISIONES_RESUELTAS.md`. La ficha conserva el planteamiento original.

**Nombre canónico:** `Oferta` (lista A: `Offer`, l.351; B l.200 «Ofertas»).

**Definición propuesta (mínima):** Oferta comercial a la que se refiere el contenido y que el proceso de validación promocional revisa.

**Fuentes exactas:**
- A l.351 «Offer»; B l.200 «Ofertas» (lista de entidades).
- B l.351–354: «Oferta», «Beneficio», «Vigencia», «Condiciones» como campos del Brief.
- B l.506–517: el Promotion Validator valida precio original (l.508), precio promocional (l.509), descuento, vigencia, restricciones, productos incluidos (l.513), exclusiones, condiciones, texto legal y «Coherencia entre oferta y copy» (l.517); fórmula de descuento l.521.
- B l.585: «CCI valida promociones con reglas deterministas…»; B l.64: ninguna promoción se aprueba automáticamente por sugerencia de IA.

**Clasificación:**
- Nombre y existencia: solicitado.
- «El brief incluye una oferta con beneficio, vigencia y condiciones» y «el validador revisa precios, descuento, vigencia, restricciones, exclusiones, condiciones, texto legal y coherencia con el copy»: derivado de las citas.
- Que esos elementos sean atributos de una entidad Oferta, que la oferta «pertenezca a Campaña», la relación N–N con Producto, y la fase: **propuesta mía**, sin cita.

**Ambigüedades:**
1. B l.508–517 describe lo que se valida, sin decir qué entidad lo contiene. «Oferta» y «promoción» aparecen casi como sinónimos; no hay definición.
2. Ya señalaste la posible duplicidad de Vigencia/Condiciones entre Brief y Oferta; sigue sin resolver y afecta esta entidad.
3. No está dicho si el brief referencia una Oferta o la contiene.
4. Precios, descuento y moneda: la fórmula está en B l.521; unidades y redondeo dependen de decisiones aún abiertas (tolerancias, B l.523). No se aprueba nada de eso aquí.
5. Relaciones con Campaña, Producto, Brief y Copy: pendientes (P4.B; Campaña–Oferta es propuesta mía).
6. Fase: B l.351 apunta a Fase 2 y B l.508–517 a Fase 4; asignación formal → Q-4.

**Consecuencias si se aprueba la definición mínima:**
- Oferta existe como entidad propia, no solo como campo del Brief, sin aprobar atributos, cálculos ni relaciones.
- El validador queda referido a esta entidad como objeto de revisión; las reglas concretas siguen sin aprobar.
- Entra en persistencia y exportación como entidad propia (diseño sin aprobar).
- Si se prefiriera tratar la oferta como contenido del Brief, la entidad se retiraría y sus datos pasarían a campos; es decisión tuya.

**Recomendación mía:** aprobar la definición mínima, porque la lista de entidades la nombra y el validador la presupone; dejar atributos, duplicidad con Brief, cálculos y relaciones para P4.B/P4.C y la especificación.

**Opciones:** (a) aprobar la definición mínima · (b) aprobar con cambios (indícalos) · (c) aprobar el nombre pero tratarla como contenido del Brief, sin entidad propia · (d) diferir o rechazar.
