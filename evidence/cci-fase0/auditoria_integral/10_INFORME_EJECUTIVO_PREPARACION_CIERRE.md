# Informe ejecutivo — preparación para el cierre de Fase 0 (2026-11-22, ronda final)
**Versión:** 3.0 (ronda de lectura completa; actualiza lectura y contradicciones) · **Fecha:** 2026-11-22 · **Estado:** vigente como informe de hechos · **Referencias:** `01`–`09`, `11`, `12`; base HEAD `13b25ca` (v2.0: `8dc47b2`).
**Qué es:** resumen de dónde está el expediente. **No es una aceptación ni una solicitud de aceptación.** Detalle en `01`–`09` y `11`.

## 1. Separación de planos
| Plano | Estado |
|---|---|
| Regularización documental | Realizada y publicada (ver `07_` y `08_`); contradicciones del expediente: ver `06_REGISTRO_CONTRADICCIONES.md` (ninguna requiere decisión del propietario salvo C-2/C-3 (CR-19…CR-22, hallados en la ronda de lectura, son documentales; CR-21 es una regresión propia ya restaurada), que son contradicciones históricas abiertas por la condición 7 de P3; CR-12 es una limitación por falta de evidencia) |
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
5. (CR-15 y CR-16 **no** son preguntas para el propietario: CR-15 es una asociación no confirmada que no se usa; CR-16 se resolvió por la independencia ya decidida entre D6.b y D6.c=A0.)
Después: aprobaciones 0.1–0.7 una por una, aceptación de Fase 0 y, aparte, autorización de Fase 1.

## 3. Porcentajes de avance (cada uno con alcance y base; sin ponderación)
| Indicador | Valor | Base de cálculo |
|---|---|---|
| Decisiones conceptuales resueltas / identificadas | **12/30 = 40,0 %** | Base: decisiones de nivel superior del expediente: P1–P15 (15), Q-1…Q-7 (7), D-1…D-8 (8) = 30. Resueltas: P1, P2, P3, Q-7, D-1…D-8 = 12. P4 y sus subdecisiones (P4.A–P4.E) **no** se cuentan como resueltas porque P4 sigue abierta; C-2/C-3 no son decisiones. La base mezcla decisiones de peso muy distinto: indicador orientativo, no un avance ponderado |
| Entidades aprobadas / 18 | **9/18 = 50,0 %** | Registro (1–8 y 13); definición mínima solamente |
| Documentación clasificada por vigencia / archivos del expediente | **107/107 (100 %)** | «Clasificado» = vigencia explícita en `05_` (todos los archivos de `evidence/cci-fase0/`, incluidos los 12 documentos de esta auditoría). No equivale a lectura íntegra ni a corrección de contenido. `docs/fase0` (59 archivos) se concilia aparte (`11_`, `12_`) |
| Archivos históricos/antecedentes con aviso de vigencia en el propio archivo / archivos históricos o antecedentes | **55/55 (100.0 %)** | Detección automática de marcas de vigencia (ver `logs/escaneo_contradicciones_2026-11-22_ronda_final.txt`); indicador de presentación, no de corrección de contenido |
| Archivos leídos (según el registro real) | **Expediente: LEÍDO_COMPLETO 103, NO_APLICABLE 4 de 107 archivos. `docs/fase0`: LEÍDO_COMPLETO 59 de 59 (por líneas únicas: 2 216 734 B de líneas únicas de 10 324 392 B; el resto es duplicado exacto)** | Ver `12_REGISTRO_LECTURA_Y_LIMITACIONES.md`: numerador, denominador y alcance por estado. No es un avance de Fase 0 |
| Pruebas ejecutadas / exigibles | **No calculable** | No existe una lista de pruebas exigibles para el cierre de Fase 0 y no se ejecutó ninguna en esta auditoría (los resultados de `logs/` son previos) |
| Integridad verificada / archivos inventariados | ver `08_` | Clon limpio; hashes y tamaños recalculados |
| Estado de publicación | Rama `evidence/cci-fase0-review` publicada; `main` sin cambios; sin PR ni merge | API |
| **Fase 0 global** | **No calculable** | No hay base objetiva ni ponderación aprobada |

## 4. Riesgos principales
- Entidades 10–12 con insuficiencia de evidencia (reglas de marca sin lista; Q-1/Q-2 sin datos).
- Las subcuestiones de A0 (origen de valores, L1/L2, L3) siguen abiertas y deben decidirse antes de P4.B/P4.C; no existe tensión con D6.b (CR-16 resuelta).
- C-2/C-3 abiertas: la presencia en `docs/fase0` de una «Fase 0 v3.3 aceptada» puede inducir a error si se lee sin el índice de conciliación.
