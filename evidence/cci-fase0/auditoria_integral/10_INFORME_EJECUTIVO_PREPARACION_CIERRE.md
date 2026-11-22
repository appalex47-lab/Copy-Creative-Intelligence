# Informe ejecutivo — preparación para el cierre de Fase 0 (2026-11-22, ronda final)
> **Nota fechada 2026-11-22 15:56 (ratificación del propietario «Confirmo todo» sobre la propuesta maestra B1–B10; no es decisión nueva de este documento):** las cifras de decisiones, entidades y planos de este informe fueron actualizadas (20/30; 18/18; 0/7). La sección 2 («Qué falta…») describe el estado previo a la ratificación; lo que sigue faltando es: aprobaciones 0.1–0.7, aceptación de Fase 0, autorización de Fase 1, C-2/C-3 y el momento de resolver los aplazamientos. Sin porcentaje global de Fase 0.
**Versión:** 3.3 (cifras de 114 archivos tras la ratificación 15:56 y cifras de decisiones/entidades actualizadas; v3.2: 111 archivos tras la corrección puntual de X4; v3.0 de la ronda de lectura completa + cifras de la ronda de verificación de coherencia posterior) · **Fecha:** 2026-11-22 · **Estado:** vigente como informe de hechos · **Referencias:** `01`–`09`, `11`, `12`; base HEAD `13b25ca` (v2.0: `8dc47b2`).
**Qué es:** resumen de dónde está el expediente. **No es una aceptación ni una solicitud de aceptación.** Detalle en `01`–`09` y `11`.

## 1. Separación de planos
| Plano | Estado |
|---|---|
| Regularización documental | Realizada y publicada (ver `07_` y `08_`); contradicciones del expediente: ver `06_REGISTRO_CONTRADICCIONES.md` (ninguna requiere decisión del propietario salvo C-2/C-3 (CR-19…CR-22, hallados en la ronda de lectura, son documentales; CR-21 es una regresión propia ya restaurada), que son contradicciones históricas abiertas por la condición 7 de P3; CR-12 es una limitación por falta de evidencia) |
| Decisiones conceptuales del propietario | Resueltas: P1, P2, P3, P4, P5, P9, P11–P14, Q-4, Q-7, D-1…D-8 (20/30); con aplazamiento aceptado: P6, P7, P8, P10, P15, Q-1, Q-2, Q-3, Q-5, Q-6; C-2/C-3 abiertas como limitación expresa; ver `02_` |
| Aprobaciones formales | 0.1–0.7: **pendientes (0/7)**; la ratificación 15:56 (B10) no emite ninguna |
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
| Decisiones conceptuales resueltas / identificadas | **20/30 = 66,7 %** (tras la ratificación 15:56; antes 12/30 = 40,0 %) | Base: decisiones de nivel superior del expediente: P1–P15 (15), Q-1…Q-7 (7), D-1…D-8 (8) = 30. Resueltas: P1, P2, P3, P4, P5, P9, P11, P12, P13, P14, Q-4, Q-7, D-1…D-8 = 20. Otras 10 (P6, P7, P8, P10, P15, Q-1, Q-2, Q-3, Q-5, Q-6) tienen **aplazamiento aceptado y no se cuentan como resueltas**; C-2/C-3 no son decisiones y siguen abiertas como limitación expresa. La base mezcla decisiones de peso muy distinto: indicador orientativo, no un avance ponderado |
| Entidades aprobadas / 18 | **18/18 = 100,0 %** (antes 9/18 = 50,0 %) | Registro (1–8 y 13 + 9–12 y 14–18 por ratificación 15:56); definición mínima solamente |
| Documentación clasificada por vigencia / archivos del expediente | **114/114 (100 %)** | «Clasificado» = vigencia explícita en `05_` (todos los archivos de `evidence/cci-fase0/`, incluidos los 13 documentos de esta auditoría y los 3 archivos `logs/verificacion_coherencia_posterior*`). No equivale a lectura íntegra ni a corrección de contenido. `docs/fase0` (59 archivos) se concilia aparte (`11_`, `12_`) |
| Archivos históricos/antecedentes con aviso de vigencia en el propio archivo / archivos históricos o antecedentes | **55/55 aplicables (100.0 %)** (58 archivos en esas clases; 3 «n/a»: 1 archivo de hashes y 2 informes derivados) | Detección automática a nivel de **archivo** (basta una marca en cualquier parte; ver `logs/escaneo_contradicciones_2026-11-22_ronda_final.txt` y `05_` §2); indicador de presentación, no de corrección de contenido ni de que cada afirmación histórica esté marcada |
| Archivos leídos (según el registro real) | **Expediente: LEÍDO_COMPLETO 104, NO_APLICABLE 10 de 114 archivos (la copia de la propuesta ratificada se leyó completa; son NO_APLICABLE, por generados, los de las rondas anteriores y, en esta ronda, el control de cambios y la salida del script). `docs/fase0`: LEÍDO_COMPLETO 59 de 59 (por líneas únicas: 2 216 734 B de líneas únicas de 10 324 392 B totales; el resto es duplicado exacto: **no** equivale a que el 100 % de los bytes se haya revisado individualmente)** | Ver `12_REGISTRO_LECTURA_Y_LIMITACIONES.md`: numerador, denominador y alcance por estado. No es un avance de Fase 0 |
| Pruebas ejecutadas / exigibles | **No calculable** | No existe una lista de pruebas exigibles para el cierre de Fase 0 y no se ejecutó ninguna en esta auditoría (los resultados de `logs/` son previos) |
| Verificación posterior a las ediciones, coherencia documental, integridad, decisiones, entidades y aprobaciones formales (ronda final de coherencia) | ver `13_INFORME_VERIFICACION_COHERENCIA_POSTERIOR.md` §16 (porcentajes separados con su base) | No se agregan en un porcentaje global |
| Integridad verificada / archivos inventariados | ver `08_` | Clon limpio; hashes y tamaños recalculados |
| Estado de publicación | Rama `evidence/cci-fase0-review` publicada; `main` sin cambios; sin PR ni merge | API |
| **Fase 0 global** | **No calculable** | No hay base objetiva ni ponderación aprobada |

## 4. Riesgos principales
- Entidades 10–12 con insuficiencia de evidencia (reglas de marca sin lista; Q-1/Q-2 sin datos).
- Las subcuestiones de A0 (origen de valores, L1/L2, L3) siguen abiertas y deben decidirse antes de P4.B/P4.C; no existe tensión con D6.b (CR-16 resuelta).
- C-2/C-3 abiertas: la presencia en `docs/fase0` de una «Fase 0 v3.3 aceptada» puede inducir a error si se lee sin el índice de conciliación.
