# Definición del MVP de CCI (propuesta; decisión Q-4 abierta)
**Propuesta:** MVP = fin de la Fase 2 (Command Center + Copy Studio persistentes, con exportación y respaldo básico). No se amplía el alcance por iniciativa propia; todo lo demás es posterior.

## Leyenda de sustento (revisión complementaria)
- **[S]** sustentado en el texto del propietario (lista de módulos y definición de las seis fases en la instrucción de Fase 0).
- **[D]** derivado por mí de decisiones o riesgos documentados en este expediente (`13_REGISTRO_DECISIONES_PROPIETARIO.md`, `14_MATRIZ_RIESGOS_CCI.md`); trazable, pero no dicho por el propietario.
- **[P]** propuesta mía **no sustentada** en un documento del propietario ni en evidencia: es juicio y requiere su validación. La **complejidad** es [P] en todos los módulos (no es una medición).

## Tabla por módulo
| # | Módulo | Fase | Problema y funcionalidad principal | Datos | Dependencias | Complejidad | Riesgos | Criterios |
|---|---|---|---|---|---|---|---|---|
| 1 | Command Center | 1 [S] | ver estado real, pendientes, actividad [S] | campañas, copys, actividad [D] | persistencia y dominio de Fase 1 [D] | Media [P] | mostrar datos ficticios como reales [D] | AC1-11 |
| 2 | Copy Studio | 2 [S] | brief, generación, variantes, editor, reglas [S] | campaña, brief, copy, versión, regla [D] | Fase 1; P8, Q-6 [D] | Alta [P] | claves de IA; ortografía sin diccionario [D] | AC2-01…08 |
| 3 | Creative Auditor | 3 [S] | auditoría de copy y visual, hallazgos, puntuación [S] | pieza, auditoría, hallazgo, regla [D] | Fase 2; P5, Q-5 [D] | Alta [P] | auditoría visual no determinista [D] | AC3-01…07 |
| 4 | Promotion Validator | 4 [S] | validaciones y cálculos de promociones [S] | oferta, producto [D] | Fase 3; Q-1 [D] | Media [P] | datos faltantes; redondeo [D] | AC4-01…04 |
| 5 | Channel Adaptation | 4 [S] | adaptación por canal con reglas y trazabilidad [S] | canal, adaptación [D] | Fase 4; Q-2 [D] | Media [P] | reglas de canal no aportadas [D] | AC4-05…06 |
| 6 | Creative Library | 5 [S] | reutilizar contenido (búsqueda, filtros, etiquetas) [P] | versiones, etiquetas [P] | Fase 5 y módulos previos [P] | Media [P] | volumen y cuota [P] | AC5-01 |
| 7 | Workflow & Approvals | 5 [S] | aprobación humana trazable, estados [S] | aprobación, versión [D] | Fase 5; Q-3 [D] | Media [P] | simular capacidades multiusuario (prohibido) [S] | AC5-02…04 |
| 8 | Performance Intelligence | 5 [S] | registrar resultados y calcular métricas [P] | resultado, métrica [D] | Fase 5 [P] | Media [P] | métricas sin datos suficientes [P] | AC5-05 |
| 9 | Brand Intelligence / Settings | **1 y 3 [P]** | preferencias y reglas de marca [P] | configuración, regla [D] | Fase 1 (preferencias); Fase 3 (reglas de marca) [P] | Baja–Media [P] | confundir preferencias con datos de negocio [P] | AC1-09, AC3-01 |

**Sin sustento explícito:** el módulo 9 **no figura en ninguna de las seis fases del propietario**; su ubicación en Fases 1 y 3 es propuesta mía [P]. Las columnas «Dependencias», «Complejidad» y «Riesgos» de los módulos 6 a 8 son [P] casi en su totalidad (ver marcas). Necesitan tu validación antes de usarse como compromiso.

**Usuario objetivo:** el usuario único del navegador (sin roles) [S]. **Posteriores y evoluciones** (no MVP, no aprobadas): sincronización, backend, cifrado local (P7), IA remota integrada, multiusuario.
