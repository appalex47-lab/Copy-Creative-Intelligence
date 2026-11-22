# P4 — Decisiones que siguen pendientes (corte 2026-11-22 11:38)

> **ESTADO VIGENTE (regularización 2026-11-22, posterior al registro D4/D6/D7/D8):** **D4.a–d, D6.a–c, D7.a–c y D8 están RESUELTAS (11/11)** y registradas en `entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md`. **Ya no son pendientes y no deben volver a solicitarse.** D5.a–d siguen fuera del alcance vigente y no se reabren. **P4.A (conteo formal vigente): 9/18 aprobadas (50 %); 9/18 pendientes (50 %).** Aprobadas con definición mínima: entidades 1–8 y entidad 13 (Adaptación de canal), esta última por D4.c=A y **exclusivamente su definición mínima** (sin atributos, relaciones, cardinalidades, estructura interna, persistencia, versionado, mecanismos de generación o adaptación, reglas de auditoría ni fase de implementación). Entidad 9 (Hallazgo): suspendida, sin aprobar. Entidades 10–12 y 14–18: sin presentar o sin aprobar. Cambio 2026-11-22: de 8/18 a 9/18, fundamento D4.c=A.
> **P4.D / Q-7: RESUELTA → (a); P4.4 cerrada (ya no es pendiente).**
> **Siguen pendientes:** P4.B, P4.C, P4.E (E1–E5), Q-1, Q-2, entidad 9 y entidades 10–12 y 14–18, C-2 y C-3 (abiertas), aprobaciones 0.1–0.7, aceptación formal de Fase 0; Fase 1 no autorizada. Dentro de D6.c=A0 quedan sin decidir la clasificación del origen de los valores y L1/L2/L3.
> Todo texto más abajo que presente D4/D6/D7/D8 como pendientes o P4.A como 8/18 es **antecedente cronológico** y se conserva.


> **[ANTECEDENTE SUPERADO por el «ESTADO VIGENTE» de arriba] Corrección 2026-11-22 previa al registro:** D-5 resuelta; **D5.a–d fuera del alcance vigente (no pendientes, no abiertas, no se vuelven a preguntar)**. Pendientes del paquete vigente: D4.a–d, D6.a–c, D7.a–c, D8 (11 decisiones). Las menciones de D5.a–d como «abiertas» en las actualizaciones fechadas más abajo son antecedente cronológico y se conservan.

**Actualización:** P4.D resuelta (Q-7 = (a) cierra P4.4). P4.A en curso entidad por entidad: 1/18 resuelta (Campaña, definición mínima del propietario); 2/18 Brief resuelta (definición mínima del propietario); 3/18 Producto resuelta (definición mínima del propietario); 4/18 Oferta resuelta (definición mínima del propietario); 5/18 Copy resuelta (definición mínima del propietario); 6/18 CopyVariant resuelta (definición mínima; delimitación frente a ContentVersion pendiente, debe resolverse antes de especificar el modelo); 7/18 Pieza creativa resuelta (definición mínima del propietario); 8/18 Auditoría creativa resuelta (definición mínima del propietario; reauditoría nueva/modificada sin resolver); 9/18 Hallazgo de auditoría presentada y **suspendida** (`FICHA_P4A_09_HALLAZGO.md`). **D-1 RESUELTA (12:04; `D1_ANALISIS_CONTENIDO.md`); **D-2 RESUELTA (12:09; `D2_VARIANTE_FRENTE_A_VERSION.md`)**; **D-4 reformulada a asuntos residuales (12:21), pendiente; **D-5 RESUELTA (12:29; `D5_APROBACION.md`); cinco cuestiones abiertas de aprobación conservadas.** **D-3 RESUELTA (12:14; `D3_FAMILIAS_DE_REGLAS.md`); ubicación de reglas de copy pendiente de P4.B;** aprobabilidad pendiente de D-5.** **Ajuste de método (11:58):** revisión integral previa (`DIAGNOSTICO_INTEGRAL_18_ENTIDADES.md`, `MATRIZ_CONSOLIDADA_18_ENTIDADES.md`) antes de las entidades 9–18. P4.B: solo relaciones con respaldo expreso; cardinalidades aparte; Campaña–Oferta/Pieza pendientes. P4.C diferida (salvo indispensables del MVP). P4.E: E1–E5 pendientes, E2 espera a P12.

Solo modelo de entidades. No incluye P5, aprobaciones 0.1–0.7, aceptación de Fase 0 ni Fase 1. Ninguna decisión aquí autoriza implementación.

## Ya resuelto (no se reabre)
- P4.1: lista de **nombres** (A, l.348–365) confirmada; B = antecedente general.
- P4.2 (b): ReglaDeMarca y ReglaComercial independientes.
- P4.3: Evento de actividad (entidad propuesta), Etiqueta y Perfil local aprobados; Colección no incorporada.
- Q-7 (a): Campaña = entidad nueva, no equivale a `Project`; F11-D5 íntegra.
- P4.5: aprobación preliminar conservada (sin convertirla en definitiva).

## Pendientes

### P4.A — Definiciones funcionales de las 18 entidades
Procedencia: derivadas [D] con cita o propuesta mía [P]; ninguna aprobada. Opciones: (a) aprobar por entidad las que indiques; (b) aprobar con cambios; (c) dejar como borrador. Recomendación: (a), empezando por las [D]. Afecta: 05, 06, `LISTA_ORIGINAL_18_ENTIDADES.md`.

### P4.B — Relaciones y cardinalidades
- Campaña–Brief [D, maestra l.347] y Campaña–Resultado [D, l.639]: con base.
- Campaña–Oferta y Campaña–Pieza: **propuesta mía**, sin base explícita.
- Resto de relaciones: [D]/[P] según columna de procedencia.
Opciones: aprobar solo las [D]; aprobar también las [P] que elijas; rechazar. Recomendación: aprobar [D] y decidir las [P] una a una. Afecta: 05, 06, 07.

### P4.C — Atributos por entidad
Aún no aprobados (Q-7 condición 5 incluye los de Campaña). Opciones: especificarlos al cerrar P4.A/B, o diferirlos a la fase de especificación de cada módulo. Recomendación: diferir a la especificación del módulo, aprobando antes solo los obligatorios del MVP. Afecta: 06, 07.

### P4.D — Cierre de P4.4 (Campaña) — **RESUELTA** (2026-11-22; ver nota)
> **ESTADO VIGENTE:** P4.D / Q-7 **resuelta**: selección **(a)**; **P4.4 cerrada** por esta decisión; no quedan respuestas pendientes del propietario sobre Q-7. Alcance conservado exactamente (registro, sección «Q-7»): aprueba solo la **existencia** de la entidad Campaña (≠ `Project`; F11-D5 íntegra); **no** aprueba atributos, cardinalidades, estructura, estados ni implementación; las relaciones de Campaña son propuesta no aprobada. Fuente: `entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md`.
> *Planteamiento original (antecedente histórico):*
Confirmar que Q-7 = (a) cierra P4.4. Opciones: sí / no (indica qué falta). Recomendación: sí. Afecta: 05, CONCILIACION.

### P4.E — Convenciones de P4.5 aún sin cerrar
- E1 Fechas: confirmar ISO-8601 UTC solo para almacenamiento y cómo se guardan fechas comerciales/zona horaria (propuesta mía: campo de fecha local `YYYY-MM-DD` + zona declarada).
- E2 `revision`: no obligatoria; justificar necesidad (ligada a P12).
- E3 Archivar vs eliminar: definir semántica de `archivedAt` y de borrado.
- E4 Desconocido/cero/vacío/no aplicable: propuesta mía de representación (null vs ausente vs 0 vs marca explícita).
- E5 Hash de versiones: redacción como integridad/trazabilidad, no seguridad.
Recomendación: aprobar E1, E3, E4, E5 con mis propuestas y mantener E2 abierta hasta P12.

## Fuera de P4
Asignación de fase → Q-4/0.7; estructura del Evento → especificación posterior; Colección cerrada.

## Actualización 2026-11-22 — paquete único
Pendientes agrupados en `PAQUETE_DECISION_D1_D8.md`: G1 (D4.a–d), G2 (D5.a–d), G3 (D6, D8), G4 (D7.a–c) y Z-1 (estado de D-5). Sin decisiones nuevas registradas; recomendaciones no aprobadas. *[superado por decisión posterior: D5.a–d fuera del alcance vigente; ver nota superior]*

## Actualización 2026-11-22 12:35
Paquete vigente: `PAQUETE_DECISION_D4_D6_D7_D8.md` — D4.a–d, D6.a–c, D7.a–c, D8 (11 ítems, sin responder *[superado: respondidos y registrados]*). D-5 confirmada resuelta; D5.a–d fuera del alcance vigente (no pendientes). El paquete D1–D8 de 12:30 queda sustituido.

## Actualización 2026-11-22 (corrección documental)
D5.a–d: decisión definitiva del propietario = fuera del alcance vigente; D-5 resuelta. No se contabilizan. *[superado: D-4, D-6, D-7, D-8 resueltas; P4.A 9/18]* D-4, D-6, D-7, D-8 siguen pendientes. P4.A 8/18 aprobadas; entidad 9 y entidades 10–18 pendientes; Q-1 y Q-2 abiertas.

> **NOTA DE ACTUALIZACIÓN 2026-11-22 (registro D4/D6/D7/D8).** El propietario confirmó las 11 decisiones D4.a–d, D6.a–c, D7.a–c y D8; el registro autoritativo es `entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md` (sección «D-4, D-6, D-7 y D-8 — RESUELTAS»). Quedan **resueltas** D-4 (residual: D4.a–d), D-6 (D6.a–c), D-7 (D7.a–c) y D-8; **siguen pendientes** P4.B, P4.C, E1–E5, Q-1, Q-2 y, dentro de D6.c=A0, la clasificación de origen de los valores y L1/L2/L3. Este documento se conserva como antecedente; si alguna celda o texto lo contradice, prevalece el registro. Sin inferir aprobaciones de entidades, atributos, relaciones, cardinalidades, fases ni mecanismos técnicos.

## Actualización 2026-11-22 (regularización posterior al registro)
Las 11 decisiones D4/D6/D7/D8 están resueltas y registradas (no se piden de nuevo). P4.A: 8/18 → **9/18** por D4.c=A (entidad 13, solo definición mínima). Pendientes reales: ver «ESTADO VIGENTE» al inicio.
