# P4.A — Entidad 8 de 18: Auditoría creativa (CreativeAudit) — RESUELTA
Estado: **RESUELTA 2026-11-22 11:55 → (b)** con la definición mínima del propietario y el alcance exacto de `REGISTRO_DECISIONES_RESUELTAS.md`. La ficha conserva el planteamiento original.

**Nombre canónico:** `Auditoría creativa` (lista A: `CreativeAudit`, l.355; B l.204 «Auditorías»).

**Definición propuesta (mínima):** Ejecución de una auditoría sobre un copy o una pieza visual dentro de CCI, cuyo resultado puede incluir una puntuación explicable y puede conservarse.

**Fuentes exactas:**
- A l.355 «CreativeAudit»; B l.204 «Auditorías» (lista de entidades).
- B l.421–422: Fase 3 «Auditar copys y piezas visuales»; A l.585–594: Fase 3 con auditoría de copy, auditoría visual, reglas de marca, hallazgos, severidad, puntuaciones, correcciones y reauditorías.
- B l.426 «Auditoría de copy» (claridad, ortografía, legibilidad, tono, consistencia, coherencia con brief, CTA, reglas de marca, afirmaciones no respaldadas, riesgos de comunicación) y B l.439 «Auditoría visual».
- B l.464–467 «Puntuación»: puntuaciones explicables con criterios y ponderaciones documentados; cálculo determinista; la IA puede sugerir hallazgos pero no modificar puntuaciones ni reglas.
- B l.472–477 «Corrección»: corregir, reauditar, comparar versiones, conservar historial.
- B l.489 «Auditorías repetidas» (Pruebas); B l.604 «Auditorías» en la Library; B l.630 «Auditorías vinculadas» en el versionado.

**Clasificación:**
- Nombre y existencia: solicitado.
- «Hay auditorías de copy y visuales», «producen hallazgos y puntuación explicable y determinista», «pueden repetirse (reauditar)», «se conservan en la Library», «se vinculan a versiones»: derivado de las citas.
- Que una Auditoría sea un registro con fecha y objetivo, que se aplique a una Versión (y no a un Copy o Pieza directamente), su estado y su cardinalidad con Hallazgo: **propuesta mía**, sin cita.

**Ambigüedades:**
1. Tus instrucciones listan «Auditorías» y los criterios que se auditan; no definen si la auditoría es un registro (evento) o una evaluación calculada sin registro propio. La lista A la nombra como entidad.
2. Objeto auditado: B l.422 dice «copys y piezas visuales»; B l.630 habla de «Auditorías vinculadas» a versiones. Si la auditoría se vincula a Copy/Pieza o a su Versión no está definido.
3. «Reauditar» y «Auditorías repetidas»: no dice si cada reauditoría es una nueva entidad o actualiza la anterior (afecta trazabilidad).
4. La puntuación: criterios y ponderaciones deben documentarse (B l.464–466); no se aprueban aquí.
5. Hallazgos (entidad 9) y reglas de marca (entidad 10): su relación con la auditoría queda para esas fichas y para P4.B.
6. Fase: Fase 3; asignación formal → Q-4.

**Consecuencias si se aprueba la definición mínima:**
- Auditoría creativa existe como entidad propia, con objeto auditado, estructura, puntuación y relaciones sin aprobar.
- La distinción entre auditoría nueva y reauditoría queda abierta.
- Entra en persistencia y exportación como entidad propia (diseño sin aprobar).
- No se aprueban criterios, ponderaciones ni reglas de auditoría.

**Recomendación mía:** aprobar la definición mínima sin precisar el objeto auditado ni cómo se representa una reauditoría; dejar eso para P4.B y la especificación de Fase 3.

**Opciones:** (a) aprobar la definición mínima · (b) aprobar con cambios (indícalos) · (c) aprobar el nombre pero tratar la auditoría como resultado calculado sin entidad propia · (d) diferir o rechazar.
