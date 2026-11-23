# P4.A — Entidad 3 de 18: Producto (Product) — RESUELTA
Estado: **RESUELTA 2026-11-22 11:44 → (b)** con la definición mínima del propietario y el alcance exacto de `REGISTRO_DECISIONES_RESUELTAS.md`. La ficha conserva el planteamiento original.

**Nombre canónico:** `Producto` (lista A: `Product`, l.350; B l.199 «Productos»).

**Definición propuesta (mínima):** Producto comercial al que se refiere el contenido y la validación promocional de CCI.

**Fuentes exactas:**
- A l.350 «Product»; B l.199 «Productos» (lista de entidades).
- B l.349 «Producto» como campo del Brief.
- B l.513 «Productos incluidos» entre los elementos que valida el Promotion Validator (Fase 4).

**Clasificación:**
- Nombre y existencia: solicitado.
- «Un brief indica un producto» y «una promoción incluye productos que se validan»: derivado de B l.349 y l.513.
- Todo lo demás: **propuesta mía**, sin cita: qué es un Producto (registro propio frente a texto libre), sus atributos (nombre, identificador, categoría…), su origen (capturado a mano o importado), la relación N–N con Oferta y su fase (Fase 2 y Fase 4 en mi fila previa).

**Ambigüedades:**
1. Tus instrucciones no definen qué es un Producto ni dan atributos. No mencionan catálogo ni SKU (busqué ambas instrucciones: sin resultados).
2. B l.349 lo lista como campo del Brief y B l.513 como elemento de validación: puede ser entidad con registro propio o simple texto dentro de Brief/Oferta. Nombrarlo en la lista de entidades sugiere lo primero, pero no lo especifica.
3. Origen de los datos: el modelo es browser-only sin backend; no está dicho si el usuario captura productos a mano, los importa o los escribe cada vez.
4. Relaciones con Brief y Oferta no citadas (P4.B).
5. Fase: B l.349 apunta a Fase 2 y B l.513 a Fase 4; asignación formal → Q-4.

**Consecuencias si se aprueba la definición mínima:**
- Producto existe como entidad propia (no solo texto), reutilizable entre briefs y ofertas, sin aprobar atributos ni relaciones (P4.B/P4.C).
- Si se prefiriera texto libre, la entidad se retiraría y Brief/Oferta guardarían el nombre como campo; es decisión tuya.
- Implica decidir después cómo se capturan o importan productos (especificación; no resuelto aquí).
- Entra en persistencia y exportación como entidad propia (diseño sin aprobar).

**Recomendación mía:** aprobar la existencia de Producto como entidad propia con la definición mínima, porque la lista de entidades lo nombra; dejar sin aprobar atributos, origen y relaciones.

**Opciones:** (a) aprobar la definición mínima · (b) aprobar con cambios (indícalos) · (c) aprobar el nombre pero tratarlo como campo de texto, sin entidad propia · (d) diferir o rechazar.
