# P4 — Decisiones que siguen pendientes (corte 2026-11-22 11:38)

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

### P4.D — Cierre de P4.4 (Campaña)
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
Pendientes agrupados en `PAQUETE_DECISION_D1_D8.md`: G1 (D4.a–d), G2 (D5.a–d), G3 (D6, D8), G4 (D7.a–c) y Z-1 (estado de D-5). Sin decisiones nuevas registradas; recomendaciones no aprobadas.

## Actualización 2026-11-22 12:35
Paquete vigente: `PAQUETE_DECISION_D4_D6_D7_D8.md` — D4.a–d, D6.a–c, D7.a–c, D8 (11 ítems, sin responder). D-5 confirmada resuelta; D5.a–d abiertas, fuera del paquete. El paquete D1–D8 de 12:30 queda sustituido.
