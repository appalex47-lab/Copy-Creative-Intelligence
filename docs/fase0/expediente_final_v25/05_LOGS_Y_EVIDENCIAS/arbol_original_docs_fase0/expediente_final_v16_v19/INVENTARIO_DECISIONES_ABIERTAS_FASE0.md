# INVENTARIO DE DECISIONES ABIERTAS DE LA FASE 0 (V20, corregido en V21)

**Versión:** V20 corregido en V21 · **Fecha:** 2026-11-19 (corrección V21: 2026-11-20; fuente de verdad vigente de decisiones: `../expediente_final_v21/REGISTRO_DECISIONES_ABIERTAS_V21.md`) · **Fuente:** especificación, registro histórico, adenda v9, `MATRIZ_FINAL_231_REGLAS_V16_V19.csv` · **Estado de verificación:** conteos computados; mapeo por familia (no por regla individual) donde se indica. Ninguna decisión se cierra aquí.

## G-1, G-5 y G-10 (abiertos: diseño no aceptado)
153 reglas son clase D (condicionadas por diseño no aceptado): IG5 78, IG10 26, IG1 18, IS 15, IM 9, IE 7. Mapeo por familia: IG1→G-1, IG5→G-5, IG10→G-10; IS/IM/IE son transversales y su dependencia concreta no se derivó regla por regla (se declara así). Las 78 restantes: 1 A, 8 B, 69 C (diseño documentado sin implementación demostrable), 0 E. Distribución vigente de las 231: A 1, B 8, C 69, D 153, E 0 (derivada de `MATRIZ_FINAL_231_REGLAS_V16_V19.csv`). Corrección V21: este inventario conservaba por error la distribución anterior a la ejecución de PE-01..PE-05 (B 3, E 5); las 5 reglas IG1-05, IG1-06, IG1-10, IG1-21 e IG5-36 pasaron de E a B en V20 (B 3 + 5 = 8); pasar a B significa «fixture PostgreSQL temporal PASS», no que el diseño esté implementado en el producto ni aceptado.
**Impacto de dejarlas abiertas:** las 153 reglas D no pueden pasar a «aceptadas»; no hay base para migraciones; Fase 1 no puede iniciar. Los 258 escenarios demostrados en modelo siguen sin valor de aceptación. No se escoge alternativa.

## Decisiones reservadas
| ID | Descripción (según fuentes) | Fuente | Estado | Evidencia | Siguiente requisito |
|---|---|---|---|---|---|
| RP-01 | Designar responsable del nivel 3 con identidad real | Registro histórico l.117; spec sec. P | PENDIENTE DEL PROPIETARIO | Adendas v4–v8 | Nombre del responsable |
| G-9 | Historial de revisor asignado (`piece_reviewer_assignments`) | Spec l.415 y siguientes | Abierta/condicionada | Diseño, sin SQL | Aceptación del diseño |
| P-01..P-05, P-10 | Pendientes del propietario de las adendas | Adenda v9 «Pendiente» | PENDIENTE DEL PROPIETARIO | Adenda v9 | Decisión expresa de cada uno |
| OD-13 | Decisión original reservada | Adenda v9; spec sec. P | PENDIENTE | Adenda v9 | Decisión del propietario |
| DEP-RET-01 | Dependencia de retención | Spec (8 líneas), DG-09 | Diferida | Spec | Resolver DG-09 |
| DG-09 | Retención | Spec l.40 | Diferida | Spec | Decisión de retención |
| DG-12 | Hash encadenado (a 6.6) | Spec l.40 | Diferida | Spec | Diseño de 6.6 |
| DG-16 | Umbrales, hasta resolver T-03 | Spec l.40 | Diferida | Spec | Resolver T-03 |
| DG-18 | `replaces_piece_id` opcional | Spec l.117 | Sujeta a decisión | Spec | Decisión del propietario |
| DG-19 | Canales y formatos reales de la organización | Spec IG1-32 | Pendiente de la organización | Spec | Catálogo real |
| DG-20 | Columna `approvals.decision` (CHECK = 'aprobada') para que la aprobación positiva sea inequívoca (RR-17) | Spec l.4786 (tabla de decisiones) y l.2778 (ampliación mínima); también citada en la sección P | Ampliación mínima de v3.3 «sujeta a tu aceptación» (la propia especificación la marca resuelta técnicamente, pero no aceptada) | Spec | Aceptación o rechazo del propietario |
| PO-05 | Aceptación de la Adenda v9 | Ver MATRIZ_HV02_PO05 | No aceptada | Adendas v1–v9 | Aceptación/correcciones del propietario |

Los textos exactos de P-01..P-05, P-10, OD-13 y DG-20 residen en la adenda v9 y la sección P de la especificación; esta tabla no los reinterpreta.
