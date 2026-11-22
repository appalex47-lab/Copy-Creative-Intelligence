# Aprobaciones de Fase 0 — fichas individuales (ninguna aprobada)
Estado de todas: **PENDIENTE**. Ninguna se marca ni se infiere. Orden sugerido: primero las decisiones de `MATRIZ_DECISIONES_PROPIETARIO.md`, después estas aprobaciones, al final el cierre. Responder: «aprobada», «rechazada» o «con cambios: …».
| ID | Qué aceptas | Documentos que revisar | Requiere antes resueltas | Qué dejas fuera | Estado | Respuesta |
|---|---|---|---|---|---|---|
| 0.1 Diagnóstico | inventario y estado real del repositorio (fundación comprobada; producto inexistente) | `01`, `02`, `../03_CONCILIACION_DOCUMENTAL.md`, `../13_VERIFICACION_EJECUTADA.md` | ~~P3~~ resuelta (2026-11-22), P14 | no valida el diseño | PENDIENTE | — |
| 0.2 Arquitectura | especificación browser-only y sus límites | `04` | ~~P1~~ y ~~P2~~ resueltas (2026-11-22), P9, P12, P13 | no aprueba el dominio ni la persistencia detallada | PENDIENTE | — |
| 0.3 Dominio | entidades, relaciones y responsabilidades | `05`, `06` | ~~P1~~ resuelta (2026-11-22), ~~Q-7~~ resuelta (2026-11-22), P4 (parcial: nombres confirmados; ver `DECISIONES_P4_PENDIENTES.md`) | no aprueba el alcance del MVP | PENDIENTE | — |
| 0.4 Persistencia | IndexedDB, Local Storage, archivos y recuperación | `07`, `08` | P5, P11, P12 (P6 antes de Fase 2) | no aprueba cifrado (P7) ni hosting (P10) | PENDIENTE | — |
| 0.5 IA | estrategia de integración y privacidad | `09` | P8 (antes de Fase 2; no bloquea el cierre de Fase 0) | no autoriza ninguna integración | PENDIENTE | — |
| 0.6 MVP | alcance y prioridades | `10` | Q-4 | las columnas marcadas [P] siguen sin validar | PENDIENTE | — |
| 0.7 Roadmap | Fases 1–5 y criterios AC | `11`, `12`, `15` | las que cada fase declara | no inicia ninguna fase | PENDIENTE | — |
| Final | cerrar formalmente Fase 0 | todo el expediente | las 11 indispensables y 0.1–0.7 | **no** autoriza la Fase 1 | PENDIENTE | — |
| Aparte | autorizar el inicio de Fase 1 | — | cierre de Fase 0 | — | PENDIENTE | — |
Inseparables técnicamente: ninguna. 0.3 y 0.4 se tocan por P4/P5 (el modelo determina los stores), pero pueden responderse por separado.
