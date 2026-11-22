# Informe ejecutivo — preparación para el cierre de Fase 0 (2026-11-22)
**Qué es:** resumen de dónde está el expediente. **No es una aceptación ni una solicitud de aceptación.** Detalle en `01`–`09` y `11`.

## 1. Separación de planos
| Plano | Estado |
|---|---|
| Regularización documental | Realizada y publicada (ver `07_` y `08_`); 2 contradicciones abiertas que requieren al propietario (CR-15, CR-16) y 1 limitación (CR-12) |
| Decisiones conceptuales del propietario | Resueltas: P1, P2, P3, P4.1 (parcial), P4.2, P4.3, Q-7, D-1…D-8; pendientes: ver `02_` |
| Aprobaciones formales | 0.1–0.7: **pendientes** |
| Pruebas técnicas | No ejecutadas en esta auditoría; sin base de «exigibles» definida para Fase 0 |
| Aceptación de Fase 0 | **No aceptada** |
| Autorización de Fase 1 | **No autorizada**; independiente de la aceptación |

## 2. Qué falta para que el propietario pueda considerar el cierre (sin pedirlo aún)
1. PAQ-1 y PAQ-2: entidades 9–12 y 14–18 (+ A0-1/2/3).
2. PAQ-3 y PAQ-4: P4.B, P4.C, P4.E.
3. PAQ-5: Q-1…Q-6, C-2, C-3 (Q-1, Q-2 y Q-5 necesitan datos que solo el propietario puede aportar).
4. PAQ-6: P5, P9, P11–P14 (indispensables según el propio expediente); PAQ-7 antes de su fase.
5. Aclaraciones CR-15 y CR-16 si el propietario quiere cerrarlas.
Después: aprobaciones 0.1–0.7 una por una, aceptación de Fase 0 y, aparte, autorización de Fase 1.

## 3. Porcentajes de avance (cada uno con alcance y base; sin ponderación)
| Indicador | Valor | Base de cálculo |
|---|---|---|
| Decisiones conceptuales resueltas / identificadas | **12/30 = 40,0 %** | Base: decisiones de nivel superior del expediente: P1–P15 (15), Q-1…Q-7 (7), D-1…D-8 (8) = 30. Resueltas: P1, P2, P3, Q-7, D-1…D-8 = 12. P4 y sus subdecisiones (P4.A–P4.E) **no** se cuentan como resueltas porque P4 sigue abierta; C-2/C-3 no son decisiones. La base mezcla decisiones de peso muy distinto: indicador orientativo, no un avance ponderado |
| Entidades aprobadas / 18 | **9/18 = 50,0 %** | Registro (1–8 y 13); definición mínima solamente |
| Documentación regularizada / documentos legibles aplicables | **93/93 clasificados por vigencia (100 %)**; de ellos con nota o estado de vigencia **en el propio archivo**: calculado en `08_` (ver allí) | «Clasificado» = vigencia explícita en el índice maestro; no equivale a lectura íntegra ni a corrección de contenido. `docs/fase0` (59) se concilia aparte (`11_`) |
| Pruebas ejecutadas / exigibles | **No calculable** | No existe una lista de pruebas exigibles para el cierre de Fase 0 y no se ejecutó ninguna en esta auditoría (los resultados de `logs/` son previos) |
| Integridad verificada / archivos inventariados | ver `08_` | Clon limpio; hashes y tamaños recalculados |
| Estado de publicación | Rama `evidence/cci-fase0-review` publicada; `main` sin cambios; sin PR ni merge | API |
| **Fase 0 global** | **No calculable** | No hay base objetiva ni ponderación aprobada |

## 4. Riesgos principales
- Entidades 10–12 con insuficiencia de evidencia (reglas de marca sin lista; Q-1/Q-2 sin datos).
- Tensión A0/D6.b (CR-16) y numeración «19» (CR-15) si no se aclaran antes de P4.B/P4.C.
- C-2/C-3 abiertas: la presencia en `docs/fase0` de una «Fase 0 v3.3 aceptada» puede inducir a error si se lee sin el índice de conciliación.
