# P4.A — Entidad 9 de 18: Hallazgo de auditoría (AuditFinding) — PENDIENTE DE DECISIÓN
Estado: presentada el 2026-11-22; **sin respuesta; decisión SUSPENDIDA (2026-11-22 11:58) hasta la revisión de coherencia del conjunto** (`DIAGNOSTICO_INTEGRAL_18_ENTIDADES.md`). No aprueba nada.

**Nombre canónico:** `Hallazgo de auditoría` (lista A: `AuditFinding`, l.356; B l.205 «Hallazgos»).

**Definición propuesta (mínima):** Problema o observación identificado durante una auditoría creativa, que debe poder explicarse y seguirse hasta su resolución.

**Fuentes exactas:**
- A l.356 «AuditFinding»; B l.205 «Hallazgos» (lista de entidades).
- B l.450–462, «Hallazgos»: «Cada hallazgo debe tener» (l.452): identificador, elemento afectado, evidencia, categoría, severidad, regla, recomendación, estado, resolución (l.454–462).
- B l.67 y A l.95: «Los hallazgos deben ser explicables.»
- B l.470: la IA puede sugerir hallazgos, pero no modificar puntuaciones ni reglas.
- B l.477–478: «Conservar historial», «Documentar hallazgos pendientes».
- B l.486 (Pruebas): «Reglas bloqueantes»; A l.590–591 (Fase 3): «Hallazgos», «Severidad».
- B l.494: «explica sus hallazgos y permite corregirlos».

**Clasificación:**
- Nombre y existencia: solicitado.
- Los 9 campos: **requeridos expresamente** por B l.452 («debe tener»), pero sin tipos, valores ni obligatoriedad adicional; es el respaldo textual más fuerte entre las entidades vistas hasta ahora. Lo señalo para que lo valores; no los trato como aprobados.
- «Son explicables», «los puede sugerir la IA», «pueden quedar pendientes», «se pueden corregir»: derivado de las citas.
- Que un Hallazgo pertenezca a una Auditoría, su cardinalidad, los valores de severidad/categoría/estado y que «Regla» sea una referencia a una regla del modelo: **propuesta mía**, sin cita.

**Ambigüedades:**
1. B l.452 exige los 9 campos pero no define sus valores (qué categorías, qué niveles de severidad, qué estados, qué es «resolución»).
2. «Regla» (campo) podría ser referencia a ReglaDeMarca o ReglaComercial (entidades 10 y 11) o texto; no está definido.
3. «Elemento afectado» no dice si apunta a Copy, Pieza o Versión; depende de la decisión pendiente sobre el objeto auditado (entidad 8).
4. B l.470 permite que la IA sugiera hallazgos: no define cómo se distingue un hallazgo sugerido por IA de uno determinista ni quién lo confirma.
5. Si un Hallazgo es entidad propia o parte de la Auditoría: la lista A lo nombra como entidad.
6. Fase: Fase 3; asignación formal → Q-4.

**Consecuencias si se aprueba la definición mínima:**
- Hallazgo de auditoría existe como entidad propia; sus campos, valores y relaciones siguen sin aprobar.
- Si luego decides aprobar los 9 campos, será una decisión separada (P4.C/especificación).
- Entra en persistencia y exportación como entidad propia (diseño sin aprobar).
- No se aprueban categorías, severidades ni estados.

**Recomendación mía:** aprobar la definición mínima y tratar los 9 campos como contenido requerido por las instrucciones, pendiente de tipos y valores; decidir en P4.C si se aprueban como atributos del MVP o se difieren a la especificación de Fase 3.

**Opciones:** (a) aprobar la definición mínima · (b) aprobar con cambios (indícalos) · (c) aprobar el nombre pero tratar los hallazgos como parte de la Auditoría, sin entidad propia · (d) diferir o rechazar.
