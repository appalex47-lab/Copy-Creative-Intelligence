# Matriz maestra de entidades P4.A (2026-11-22)
**Subordinada al registro.** Las definiciones aprobadas se copian **literalmente** del registro (extracción automática de los bloques P4.A y D4.c; coincidencia exacta comprobada por el script de generación).
**Conteo formal vigente: 9/18 aprobadas (50 %); 9/18 pendientes (50 %).** Base: la lista de 18 nombres confirmada en P4.1 (A l.348–365). Las propuestas y recomendaciones **no** se cuentan como aprobaciones.

## A. Entidades aprobadas con definición mínima (9)
| # | Entidad | Definición aprobada (literal) | Fundamento |
|---|---|---|---|
| 1 | Campaña | «Campaña es una entidad propia de CCI, creada por el usuario e identificada por un nombre. Puede ser referenciada por un Brief y por un Resultado de desempeño, y puede utilizarse como criterio de catalogación en Creative Library.» | P4.A entidad 1 (opción (b)) |
| 2 | Brief | «Brief es una entidad propia de CCI que el usuario completa y que reúne información de partida para la creación de contenido (copy). Puede contener información incompleta.» | P4.A entidad 2 (opción (b)) |
| 3 | Producto | «Producto es una entidad propia de CCI que representa un producto comercial referenciado en la información de un Brief y considerado por el proceso de validación promocional.» | P4.A entidad 3 (opción (b)) |
| 4 | Oferta | «Oferta es una entidad propia de CCI que representa una oferta comercial asociada al contenido que se crea o revisa. Su información comercial puede ser relevante para la validación de promociones.» | P4.A entidad 4 (opción (b)) |
| 5 | Copy | «Copy es una entidad propia de CCI que representa contenido textual creado o escrito por el usuario y que puede utilizarse como objeto de edición, auditoría, validación y adaptación a distintos canales.» | P4.A entidad 5 (opción (b)) |
| 6 | Variante de copy | «Variante de copy es una entidad propia de CCI que representa una alternativa de contenido textual contemplada en el proceso de creación y generación de copy, que el usuario puede administrar y conservar de forma persistente.» | P4.A entidad 6 (opción (b)) |
| 7 | Pieza creativa | «Pieza creativa es una entidad propia de CCI que representa un recurso visual que puede ser objeto de auditoría visual y conservarse en Creative Library.» | P4.A entidad 7 (opción (b)) |
| 8 | Auditoría creativa | «Auditoría creativa es una entidad propia de CCI que representa una evaluación realizada sobre un copy o una pieza creativa, cuyo resultado puede incluir hallazgos y una puntuación explicable, y que puede conservarse para consulta y seguimiento.» | P4.A entidad 8 (opción (b)) |
| 13 | Adaptación de canal (`ChannelAdaptation`) | «**Adaptación de canal:** contenido derivado de un copy fuente y preparado para un canal destino, con identidad y trazabilidad propias; concepto distinto de Copy, Variante de copy y Versión de contenido. Puede relacionarse con una Pieza creativa cuando el canal sea visual.» | D4.c = A (2026-11-22) |

**No aprobado para NINGUNA de las 9:** atributos, relaciones, cardinalidades, estructura interna, estados, ciclo de vida, persistencia o versionado, mecanismos de generación/adaptación, reglas de auditoría, asignación de fase e implementación. Límites propios de cada entidad: registro, bloques «NO aprueba». Para la entidad 13 en particular: ninguno de los puntos anteriores; D4.a/D4.b/D4.d acotan su delimitación, su posible vínculo con Pieza creativa y su aprobabilidad bajo M-1/D-5.3 sin aprobar relación, cardinalidad ni auditoría directa.

## B. Entidad suspendida (1)
| # | Entidad | Estado | Nota |
|---|---|---|---|
| 9 | Hallazgo de auditoría (`AuditFinding`) | **Suspendida, sin aprobar** (2026-11-22 11:58) | Definición propuesta en `FICHA_P4A_09_HALLAZGO.md` (no aprobada). Se retoma en PAQ-1 |

## C. Entidades sin aprobación vigente (8)
| # | Entidad | Estado documental | Condicionantes ya resueltos | Pendiente |
|---|---|---|---|---|
| 10 | Regla de marca (`BrandRule`/ReglaDeMarca) | No presentada | P4.2=(b); D-3 | Definición mínima; el registro documenta que no hay lista específica de reglas de marca |
| 11 | Regla comercial (`CommercialRule`/ReglaComercial) | No presentada | P4.2=(b); D-3; D7.b=A (tolerancias = parámetros) | Definición; Q-1 |
| 12 | Canal (`Channel`) | No presentada | D-3.c (reglas por canal = dimensión del Canal); D7.c=C | Definición; Q-2 |
| 14 | Versión de contenido (`ContentVersion`) | No presentada | D-1.d, D-2 | Definición |
| 15 | Aprobación (`Approval`) | No presentada | D-5 (R3, (b), M-1); D4.d | Definición |
| 16 | Resultado de desempeño (`PerformanceRecord`) | No presentada; **nombre fijado por D8=A**, sin definición | D6.c=A0 (los valores pertenecen al Resultado) | Definición; A0-1/2/3 |
| 17 | Métrica (`Metric`) | No presentada; **ubicación conceptual por D6.c=A0** (definición de la métrica) | D6.a=A, D6.b=A | Definición; fórmulas/catálogo no decididos |
| 18 | Configuración de la aplicación (`ApplicationSettings`) | No presentada | D7.a=A (Perfil local ≠ Configuración) | Definición |

## D. Conceptos aprobados fuera de la lista de 18 (no cuentan en 9/18)
| Concepto | Decisión | Nota |
|---|---|---|
| Evento de actividad | P4.3: aprobada como **entidad propuesta**; estructura posterior | Relación con la numeración «19» no confirmada (ver CR-15) |
| Etiqueta | P4.3: aprobada | — |
| Perfil local | P4.3 + P1: aprobado; contenido: solo nombre visible opcional. D7.a=A fija solo el criterio de distinción frente a Configuración (no amplía el contenido) | — |
| Colección | No incorporada (decisión mantenida) | Se reabre solo con necesidad funcional demostrable |

## E. Atributos, relaciones y cardinalidades NO aprobados (resumen)
Ninguno está aprobado. Quedan para P4.B (relaciones/cardinalidades; con base expresa solo Campaña–Brief y Campaña–Resultado; Campaña–Oferta y Campaña–Pieza son propuestas) y P4.C (atributos; diferidos por el propietario a la especificación de cada módulo, salvo indispensables del MVP). Ver matriz 04.
