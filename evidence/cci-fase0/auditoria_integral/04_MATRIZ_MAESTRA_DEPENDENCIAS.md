# Matriz maestra de dependencias — P4.B / P4.C / P4.E / Q / C (2026-11-22)
**Subordinada al registro.** Muestra qué desbloquea cada cuestión; no decide nada. **[Rec. Claude]** = recomendación no vinculante.

## A. Dependencias entre cuestiones pendientes
| Cuestión | Depende de (pendiente) | Resuelta y aplicable | Desbloquea |
|---|---|---|---|
| PAQ-1 (entidades 9–12) | — | D-1, D-3, P4.2, D7.b, D7.c | P4.B, Q-5 (PE-09), Q-1/Q-2 (afinan 11/12) |
| PAQ-2 (entidades 14–18 + A0) | — | D-1, D-2, D-5, D6.a–c, D7.a, D8 | P4.B, P4.C |
| P4.B relaciones/cardinalidades | PAQ-1, PAQ-2 | Q-7 (solo existencia de Campaña); D4.b (vínculo posible Adaptación–Pieza, sin cardinalidad); D-3.c (ubicación de reglas de copy pendiente de P4.B) | P4.C |
| P4.C atributos | P4.B, Q-4 | Posición del propietario: diferir a especificación de módulo, salvo indispensables del MVP | Aprobación 0.3 |
| P4.E E1–E5 | E2 depende de P12 | P4.5 preliminar | 0.4 |
| Q-1 | D7.b (resuelta) | — | Entidad 11, Fase 4 |
| Q-2 | D7.c (resuelta) | — | Entidad 12, Fase 4 |
| Q-3 | D-5 (resuelta) | P1 (un solo usuario local) | Fase 5 |
| Q-4 MVP | P4 | — | P4.C, 0.6 |
| Q-5 puntuación | PE-09 | — | Fase 3 |
| Q-6 idioma | P13 | — | Fase 2 |
| C-2 | — (histórica) | P3 condición 7: no se resuelve por inferencia | P15 |
| C-3 | — (histórica) | P1 | P15 |
| P5, P9, P11–P14 | P5↔P6/P11; P12↔P11; P13↔P5,P6,P8 | — | 0.4, 0.7 |

## B. Dependencias de decisiones ya resueltas que dejan subcuestiones abiertas
| Decisión | Subcuestión abierta | Cuestión que la recoge |
|---|---|---|
| D6.c=A0 | origen del valor; L1/L2; L3 | A0-1, A0-2, A0-3 (PAQ-2) |
| D4.b=A | relación, obligatoriedad, dirección y cardinalidad Adaptación–Pieza | P4.B |
| D7.b=A | valores, redondeo | Q-1 |
| D7.c=C | lista definitiva, reglas de canal, mecanismo de ampliación | Q-2 |
| D-3 (reglas de copy) | ubicación en el modelo | P4.B |
| D-2.b | historial de versiones propio de Variante: «no por ahora, sin excluirlo a futuro» | No requiere decisión ahora |
| D-1.c / D-2.c | ampliar la Auditoría creativa a Adaptación o Variante: requiere decisión expresa futura | No requiere decisión ahora |
| Entidad 8 | reauditoría nueva/modificada sin resolver | P4.B/P4.C (registrado en ficha 8) |
| Brief–Oferta | duplicidad Vigencia/Condiciones abierta | P4.B/P4.C |

## C. Orden sugerido [Rec. Claude]
PAQ-1 y PAQ-2 en paralelo → P4.B → P4.C y P4.E → PAQ-5 (Q/C) y PAQ-6 (técnicas) en cualquier momento → PAQ-7 antes de su fase → aprobaciones 0.1–0.7 → aceptación de Fase 0 → autorización de Fase 1 (cada paso por separado).
