---
name: informe_cierre_g1_g5_g10
description: Informe de la revisión v14 de G-1, G-5 y G-10 (cierre integral de la procedencia de assets, atomicidad, auditor independiente, atribuciones, evaluador e integridad referencial RS-01 a RS-08); diseño documental con pruebas de modelo en memoria; nada ejecutado en PostgreSQL
---

# INFORME — CIERRE INTEGRAL DE LA PROCEDENCIA DE ASSETS (revisión v14)

Sustituye al informe v13 (conservado en `historico/`). Diseño documental con pruebas de modelo en memoria: no se ejecutó SQL, código de producto, Supabase ni PostgreSQL. La «v14» de este documento es la revisión del diseño complementario; no es la Adenda v9 del propietario (PO-05).

## A. Dictamen ejecutivo

| Nivel | Estado | Alcance |
|---|---|---|
| 1. Fase 0 v3.3 | COMPLETADA Y ACEPTADA COMO LÍNEA BASE DOCUMENTAL, CON LIMITACIONES DOCUMENTADAS | No se reabre ni se modifica; SHA-256 `b5dccdc73a8103966ab1e1b1e84b2e7ead68cd736fba666ec71d0e790d51c1da` sin cambio |
| 2. Diseño complementario v14 (G-1, G-5, G-10) | COMPLETADO DOCUMENTALMENTE Y PREPARADO PARA ACEPTACIÓN FORMAL DEL PROPIETARIO, CON LIMITACIONES TÉCNICAS EXPLÍCITAS | Pendiente de aceptación formal del propietario; no validado técnicamente; la Adenda v9 sigue sin aceptar (PO-05) |
| 3. Fase 1 | NO INICIADA / NO AUTORIZADA | Requiere autorización expresa; este diseño no la concede |


**Niveles de evidencia usados en este expediente.**

| Nivel de evidencia | Significado | Alcance |
|---|---|---|
| Diseñado | La regla o el escenario está escrito en la especificación | Nada ejecutado |
| Verificado documentalmente | El verificador publicado comprobó coherencia entre los documentos: IDs, referencias, cifras, contratos, orden, estados | Resultado reproducible; no prueba que el diseño funcione en PostgreSQL |
| Validado técnicamente | Ejecución real contra PostgreSQL, RLS y Supabase con las pruebas de la matriz | **Pendiente**: ningún control ni escenario alcanza este nivel |


**Resultado de la verificación (calculado por el verificador publicado).**

| Control | Mutaciones | Detectadas | Casos positivos | Resultado |
|---|---|---|---|---|
| K45 | 27 | 27 | 3 casos positivos aprobados | OK |
| K46 | 12 | 12 | resolutores elegibles aceptados | OK |
| K47 | 36 | 36 | 12/12 escenarios A a L y comprobaciones U, S, X y R aprobados | OK |
| K47 resoluciones inmutables | 12 | 12 | escenario RS y 9 intentos directos rechazados | OK |
| K47 validación previa del origen (A54 a A65) | 12 | 12 | rechazo sin escritura, estado previo idéntico y E nulo en cada una; 20 pruebas de atomicidad aprobadas | OK |
| K47 procedencia e identidad del arte (A01 a A53) | 53 | 53 | 26/26 casos positivos de arte (P01 a P26) aprobados; 16/16 pruebas adversariales aprobadas | OK |
| K56 cadena, atribuciones y código del modelo (CHAIN, ATTR, K56-M) | 44 | 44 | ADVC 24/24, AT14 11/11 y E14 6/6 aprobadas | OK |
| FK01 a FK41 (K32, K44, K45 y K55) | 41 | 41 (lo calcula el verificador) | mutaciones estructurales sobre la especificación |  |
| K57 mutaciones documentales de trazabilidad | 8 | 8 (lo calcula el verificador) | K57-D01 a K57-D08 |  |
| Total estructural | 196 | 196 | más 25 mutaciones documentales M-01 a M-25, 41 mutaciones FK y 8 mutaciones K57-D |  |


La v14 audita la v13, corrige la validación de la cadena completa de procedencia (todos los eslabones, sus eventos, versiones, uploader original, atribución directa, organización, pieza y versiones de copy), refuerza la atomicidad, la conservación de atribuciones, la reconstrucción de E, la elegibilidad del evaluador y la independencia del auditor, y revisa la integridad referencial de RS-01 a RS-08 (la v13 declaró RS-01 a RS-08; RS-08 se agrega en la v14). Las pruebas son de modelo en memoria y comprobaciones documentales; **ninguna es una prueba en PostgreSQL ni Supabase** y la aceptación del propietario sigue pendiente.

## B. Qué se corrigió

### H-01 La cadena de procedencia se validaba solo en la raíz y en el eslabón inmediato

| Concepto | Detalle |
|---|---|
| Defecto en la v13 | `_origen_carga` y `_validar_reutilizacion` de la v13 contrastaban la raíz y tomaban los campos guardados en los eslabones intermedios (evento, uploader, atribución, organización, pieza, versión de copy, actor) como prueba de sí mismos: una corrupción solo intermedia podía aceptarse con una raíz correcta. |
| Corrección | `reconstruir_cadena_procedencia` recorre todos los eslabones hasta la raíz y valida 13 vínculos por eslabón contra los registros concretos (sección 4.4.16 B); devuelve error ante ambigüedad, ciclo, referencia ausente, evento intercambiado o compartido, atribución duplicada o de otro asset, y nunca declara válida una cadena incompleta. |
| Documento y sección | ESPECIFICACION 4.4.16 A y B |
| Reglas | IG5-104, IE-12 |
| Evidencia | CHAIN-01 a CHAIN-24 (24 mutaciones de eslabones, 4 de ellas sobre eslabones modificados) |
| Escenarios diseñados | T-627 a T-650 (24; ninguno ejecutado) |

### H-02 El orden de validación y escritura de una reutilización no usaba la cadena completa ni era atómico

| Concepto | Detalle |
|---|---|
| Defecto en la v13 | El registro de un asset y de su evento podía dejar registros parciales o un estado final inconsistente cuando la validación previa era débil. |
| Corrección | Orden documentado de 14 pasos: validación completa y acumulación de errores antes de escribir (pasos 1 a 12), escritura (13) y verificación final con restauración exacta (14); `_origen_carga`, `_validar_reutilizacion` y `registrar_asset` usan la reconstrucción de H-01. |
| Documento y sección | ESPECIFICACION 4.4.16 C y D |
| Reglas | IG5-104, IG5-105 |
| Evidencia | AT14-01 a AT14-11; K56-M03; K56-M07 |
| Escenarios diseñados | T-687 a T-697 (11; ninguno ejecutado) |

### H-03 El auditor no era independiente por eslabón ni detectaba modificación, duplicidad o ambigüedad

| Concepto | Detalle |
|---|---|
| Defecto en la v13 | El auditor de la v13 no recalculaba la cadena completa con implementación propia: un motor que aceptaba una cadena corrupta no siempre era detectado. |
| Corrección | `_hall_cadena` recalcula cada cadena desde las instantáneas sin llamar a funciones del motor (`_compartidas()` vacío); ADVC-01 a ADVC-24 fuerzan al motor a aceptar y exigen detección del auditor, E bloqueado y fallo cerrado de impacto y publicación. |
| Documento y sección | ESPECIFICACION 4.4.16 F |
| Reglas | IG5-106 |
| Evidencia | ADVC-01 a ADVC-24; K56-M04 |
| Escenarios diseñados | T-651 a T-674 (24; ninguno ejecutado) |

### H-04 La conservación de atribuciones y la inmutabilidad de resoluciones no tenían pruebas negativas específicas ni detectaban la reactivación

| Concepto | Detalle |
|---|---|
| Defecto en la v13 | Una atribución descartada podía volver a activa sin resolución sin ser detectada; faltaban mutaciones para duplicados, cambios de persona, pieza, versión o evento, modificación posterior de resoluciones y auto-retiro. |
| Corrección | Regla I15 del auditor de resoluciones (reactivación histórica → activa sin resolución) y doce mutaciones ATTR-01 a ATTR-12 desde un estado válido. |
| Documento y sección | ESPECIFICACION 4.4.16 G |
| Reglas | IG5-107 |
| Evidencia | ATTR-01 a ATTR-12; K56-M05 |
| Escenarios diseñados | T-675 a T-686 (12; ninguno ejecutado) |

### H-05 La reconstrucción de E y la elegibilidad del evaluador no estaban modeladas con fallo cerrado

| Concepto | Detalle |
|---|---|
| Defecto en la v13 | No había una función que decidiera, con los datos reales, quién es elegible para evaluar, ni asignación, confirmación y publicación revalidadas. |
| Corrección | `elegibilidad_evaluador` (E1 a E7), `asignar_evaluador`, `confirmar_independencia` e `intentar_publicacion` con revalidación; sin permisos nuevos ni asignación automática a Admin; la autoridad que asigna sigue en G-9 (abierto). |
| Documento y sección | ESPECIFICACION 4.4.16 H y O |
| Reglas | IG5-108 |
| Evidencia | E14-01 a E14-06; AT14-09; AT14-10; K56-M06 |
| Escenarios diseñados | T-698 a T-703 (6; ninguno ejecutado) |

### H-06 La integridad referencial RS-01 a RS-08 no tenía una auditoría completa por relación

| Concepto | Detalle |
|---|---|
| Defecto en la v13 | Faltaba la relación que ata el evento de carga original al asset raíz exacto (RS-08), una restricción única propia sobre el evento de reutilización, y la trazabilidad RS → mutaciones era inexacta. |
| Corrección | RS-08 y `unique(organization_id, reuse_event_id)`; auditoría de 20 puntos por relación (RS-01 a RS-08) calculada sobre el documento y el modelo; mutaciones FK16 a FK41; excepciones individuales con riesgo residual. |
| Documento y sección | ESPECIFICACION 4.4.15 y 4.4.16 I y J |
| Reglas | IG5-103, IG5-109 |
| Evidencia | FK01 a FK41; K32, K44, K45 y K55 |
| Escenarios diseñados | T-712 a T-719 (8; ninguno ejecutado) |

### H-07 La matriz de mutaciones no cubría el código nuevo

| Concepto | Detalle |
|---|---|
| Defecto en la v13 | Una defensa del modelo podía eliminarse sin que ninguna prueba fallara. |
| Corrección | Se conservan las mutaciones previas (K47-A33 a A48 y A54 a A65, P15 a P26, ADV6 a ADV16, FK01 a FK15) y se agregan CHAIN-01 a CHAIN-24, ATTR-01 a ATTR-12, FK16 a FK41 y K56-M01 a K56-M08 (degradación del propio código). |
| Documento y sección | ESPECIFICACION 4.4.16 E a K |
| Reglas | IG5-110 |
| Evidencia | K56-M01 a K56-M08 |
| Escenarios diseñados | T-704 a T-711 (8; ninguno ejecutado) |

### H-08 Las operaciones que escriben procedencia no eran todas atómicas

| Concepto | Detalle |
|---|---|
| Defecto en la v13 | Un fallo a mitad de una operación o una validación previa debilitada dejaba registros parciales. |
| Corrección | El decorador `_atomica` cubre 19 operaciones (altas, modificaciones, resoluciones, asignación, confirmación y publicación): captura del estado, verificación final y restauración exacta. |
| Documento y sección | ESPECIFICACION 4.4.16 D |
| Reglas | IG5-105 |
| Evidencia | AT14-01 a AT14-11 |
| Escenarios diseñados | T-687 a T-697 (11; ninguno ejecutado) |

### H-09 K55 comparaba sobre todo texto

| Concepto | Detalle |
|---|---|
| Defecto en la v13 | Las pruebas citadas por cada relación y las cifras del documento no se contrastaban con lo ejecutado. |
| Corrección | K55 verifica que los identificadores citados (K47-A y CHAIN) existen; K57 traza cada regla nueva a funciones existentes, pruebas existentes del conjunto ejecutado y verificador, y compara tablas y cifras del documento con las ejecutadas. |
| Documento y sección | ESPECIFICACION 4.4.16 L y M |
| Reglas | IG5-110 |
| Evidencia | K57-D01 a K57-D08 |
| Escenarios diseñados | T-720 a T-720 (1; ninguno ejecutado) |

### H-10 La reproducibilidad no cubría las nuevas baterías

| Concepto | Detalle |
|---|---|
| Defecto en la v13 | Los resultados nuevos debían ser deterministas y estar separados por categoría de evidencia. |
| Corrección | Dos ejecuciones limpias con `env -i` producen salidas --md y --json idénticas; la sección 4.4.16 N separa diseño, verificación documental, ejecución en memoria y ejecución en PostgreSQL o Supabase (ninguna). |
| Documento y sección | ESPECIFICACION 4.4.16 N; AUDITORIA 3 |
| Reglas | IG5-110 |
| Evidencia | K41 y la comparación de salidas de la publicación |
| Escenarios diseñados | T-721 a T-721 (1; ninguno ejecutado) |

### H-11 Los documentos debían describir la v14 sin contradicciones

| Concepto | Detalle |
|---|---|
| Defecto en la v13 | Especificación, informe, auditoría, roadmap, registro y herramientas debían contar lo mismo. |
| Corrección | Los cinco documentos se regeneran con las mismas cifras; se conservan las copias históricas v13 y las anteriores con su SHA-256 en el manifiesto. |
| Documento y sección | todos |
| Reglas | IG5-110, IE-12 |
| Evidencia | K09, K22, K25, K27, K28 |
| Escenarios diseñados | T-722 a T-722 (1; ninguno ejecutado) |

## C. Modelo y relaciones

| Elemento | Detalle |
|---|---|
| Tablas | 27 históricas sin cambio; 14 nuevas propuestas: `piece_classification_events`, `piece_reviewer_assignments`, `impact_evaluations`, `publication_attempts`, `channel_formats`, `brief_versions`, `promotion_snapshots`, `contribution_events`, `copy_version_provenance`, `brief_field_changes`, `brief_field_attributions`, `promotion_field_changes`, `promotion_field_attributions`, `attribution_discard_resolutions`; la v14 no crea tablas |
| Orden definitivo | 1.8 → 2.x → 2.1 → 2.3 → 2.5 → 2.7 → 3.x → 4.x → 5.1 → 5.3 → 6.x → 6.1 → 6.5 → 6.6 → 8.x |
| Atribución por campo | 12 campos materiales de brief y 9 de promoción; las atribuciones se conservan siempre; solo una resolución aceptada de `attribution_discard_resolutions` (independiente y con evidencia) las vuelve históricas; el historial no se reactiva sin resolución (regla I15) |
| Integridad | Toda FK es compuesta e incluye organization_id; RS-01 a RS-08 fijan la identidad exacta del origen; solo RS-06 es diferida; `unique(organization_id, reuse_event_id)` impide que un evento de reutilización pertenezca a dos assets |
| Funciones | create_brief_version, create_promotion_snapshot, create_copy_version, verify_field_provenance (interna), version_contributors y las anteriores; sin funciones ni triggers nuevos en la v14 |
| Límites | IS-11: superusuario, propietario, desactivación de triggers y edición manual no los impide el diseño |

## D. Fórmula de contribuyentes y elegibilidad

**E = Ctr(V-A) ∪ Inh(V-A) ∪ ⋃ Ctr(v) para v ∈ [V-D, V-B] ∪ P.** La fórmula, la exclusión del proponente de la clasificación vigente (DT-02) y la ausencia de autoevaluación y de asignación automática a Admin no cambian. E solo se reconstruye desde cadenas verificadas; un evaluador es elegible si cumple E1 a E7 (sección 4.4.16 H) y ante cualquier cadena incompleta se bloquean E, la evaluación, la confirmación de independencia y la aprobación o publicación, sin excepción de Admin. Quién puede registrar la asignación en `piece_reviewer_assignments` sigue en G-9 (abierto).

## E. Verificación

| Concepto | Resultado |
|---|---|
| Reglas de integridad | 225 |
| Pruebas diseñadas | 722 (documental 392 / técnica futura ejecutable 281 / infraestructura real 49); **ninguna ejecutada**; cobertura regla↔escenario completa según el verificador |
| Tablas propuestas | 41 (27 históricas + 14 nuevas) |
| Verificación documental y estructural | 57 comprobaciones y 270 mutaciones del verificador publicado; resultado real en AUDITORIA_FINAL_G1_G5_G10.md, sección 3 |
| Pruebas de modelo en memoria ejecutadas | K45 (15 controles), K47 (12 escenarios, 26 casos positivos de arte, 16 adversariales, 28 invariantes), K46, CHAIN 24, ADVC 24, ATTR 12, AT14 11, E14 6 y K56-M 8, con datos ficticios; resultado real en la auditoría |
| Pruebas técnicas pendientes | Todas las de PostgreSQL, RLS, Supabase, transacciones, concurrencia, bloqueos y rollback: nada de eso se ejecutó |

## F. Pendientes

PO-05 y aceptación de la Adenda v9; aceptación formal de esta revisión; DG-09, DG-12, DG-16, DG-18, DG-19, DG-20; RP-01; P-01 a P-05; P-10; OD-13; G-9 completo; DEP-RET-01; valores reales de canal y formato; validación de infraestructura; pruebas reales de PostgreSQL, RLS y Supabase; pruebas reales de concurrencia, bloqueos y rollback; validación externa y operativa. Ninguno se resuelve en esta revisión.

## G. Integridad y GitHub

SHA-256 de v3.3: `b5dccdc73a8103966ab1e1b1e84b2e7ead68cd736fba666ec71d0e790d51c1da` (sin cambio). Publicación en `main` de `appalex47-lab/Copy-Creative-Intelligence`, carpeta `docs/fase0/`. Commit anterior `d4044c2a618e8f492a2dd3b8cddcf1ccbd3d85a8`. El commit nuevo y los SHA-256 de los cinco documentos se informan en el mensaje final.

## H. Declaración de alcance

Sin código de aplicación, sin SQL ejecutable, sin migraciones, sin recursos Supabase, sin infraestructura ni despliegue; v3.3 sin alterar; T-02 conserva sus 13 transiciones y no hay permisos nuevos (17 claves físicas); Fase 1 no iniciada; ninguna decisión del propietario se da por tomada y no se declara aceptación del propietario.
